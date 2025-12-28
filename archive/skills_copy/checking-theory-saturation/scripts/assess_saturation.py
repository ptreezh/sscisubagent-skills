#!/usr/bin/env python3
"""
综合饱和度评估工具

功能：
1. 检查概念饱和度（新概念出现率）
2. 检查范畴完整性（定义、属性、案例）
3. 检查关系稳定性（新关系出现率）
4. 检查理论完整性（核心组件）
5. 生成综合饱和度报告

标准化接口：argparse + 三层JSON输出
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List


def check_concept_saturation(new_data: List, existing_concepts: List) -> Dict:
    """检查概念饱和度"""
    new_concepts = []
    
    for item in new_data:
        concept = item.get('concept') or item.get('name') or item.get('code')
        if concept and concept not in existing_concepts:
            new_concepts.append(concept)
    
    new_concept_rate = len(new_concepts) / len(new_data) if new_data else 0
    
    return {
        'new_concepts': new_concepts,
        'new_concept_count': len(new_concepts),
        'total_new_data': len(new_data),
        'new_concept_rate': round(new_concept_rate, 3),
        'is_saturated': new_concept_rate < 0.05,  # <5%认为饱和
        'saturation_level': 'high' if new_concept_rate < 0.05 else 
                           'medium' if new_concept_rate < 0.10 else 'low'
    }


def check_category_completeness(categories: List[Dict]) -> Dict:
    """检查范畴完整性"""
    complete_count = 0
    incomplete_categories = []
    
    for cat in categories:
        has_definition = bool(cat.get('definition'))
        has_properties = bool(cat.get('properties') or cat.get('attributes'))
        has_examples = bool(cat.get('examples') or cat.get('cases'))
        
        is_complete = has_definition and has_properties and has_examples
        
        if is_complete:
            complete_count += 1
        else:
            incomplete_categories.append({
                'name': cat.get('name', cat.get('id')),
                'missing': [
                    'definition' if not has_definition else None,
                    'properties' if not has_properties else None,
                    'examples' if not has_examples else None
                ]
            })
    
    completeness = complete_count / len(categories) if categories else 0
    
    return {
        'total_categories': len(categories),
        'complete_categories': complete_count,
        'incomplete_categories': incomplete_categories,
        'completeness_rate': round(completeness, 3),
        'is_saturated': completeness >= 0.90,
        'saturation_level': 'high' if completeness >= 0.90 else 
                           'medium' if completeness >= 0.70 else 'low'
    }


def check_relation_stability(existing_relations: List, new_relations: List) -> Dict:
    """检查关系稳定性"""
    # 构建关系的唯一标识
    def relation_key(rel):
        source = rel.get('source')
        target = rel.get('target')
        rel_type = rel.get('type', 'unknown')
        return f"{source}-{target}-{rel_type}"
    
    existing_keys = {relation_key(rel) for rel in existing_relations}
    new_keys = {relation_key(rel) for rel in new_relations}
    
    truly_new = new_keys - existing_keys
    new_relation_count = len(truly_new)
    
    total_relations = len(existing_relations) + new_relation_count
    new_relation_rate = new_relation_count / total_relations if total_relations else 0
    
    return {
        'existing_relations': len(existing_relations),
        'new_relations_submitted': len(new_relations),
        'truly_new_relations': new_relation_count,
        'new_relation_rate': round(new_relation_rate, 3),
        'is_saturated': new_relation_rate < 0.10,
        'saturation_level': 'high' if new_relation_rate < 0.10 else 
                           'medium' if new_relation_rate < 0.20 else 'low'
    }


def check_theory_completeness(theory: Dict) -> Dict:
    """检查理论完整性"""
    components = {
        'core_category': bool(theory.get('core_category') or theory.get('core_concept')),
        'propositions': bool(theory.get('propositions')),
        'framework': bool(theory.get('framework') or theory.get('conceptual_framework')),
        'boundaries': bool(theory.get('boundaries') or theory.get('scope'))
    }
    
    complete_count = sum(components.values())
    completeness = complete_count / len(components)
    
    missing = [name for name, exists in components.items() if not exists]
    
    return {
        'components': components,
        'complete_components': complete_count,
        'total_components': len(components),
        'missing_components': missing,
        'completeness_rate': round(completeness, 3),
        'is_saturated': completeness >= 0.90,
        'saturation_level': 'high' if completeness >= 0.90 else 
                           'medium' if completeness >= 0.70 else 'low'
    }


def calculate_overall_saturation(checks: Dict) -> Dict:
    """计算综合饱和度"""
    saturation_scores = {
        'concept': 1.0 if checks['concept_saturation']['is_saturated'] else 0.0,
        'category': 1.0 if checks['category_completeness']['is_saturated'] else 0.0,
        'relation': 1.0 if checks['relation_stability']['is_saturated'] else 0.0,
        'theory': 1.0 if checks['theory_completeness']['is_saturated'] else 0.0
    }
    
    overall_score = sum(saturation_scores.values()) / len(saturation_scores)
    saturated_count = sum(saturation_scores.values())
    
    # 综合判断
    if saturated_count == 4:
        level = 'fully_saturated'
        recommendation = '理论已完全饱和，可以结束数据收集'
    elif saturated_count >= 3:
        level = 'mostly_saturated'
        recommendation = '理论基本饱和，建议补充少量数据验证'
    elif saturated_count >= 2:
        level = 'partially_saturated'
        recommendation = '理论部分饱和，需要继续数据收集'
    else:
        level = 'not_saturated'
        recommendation = '理论未饱和，需要大量数据收集'
    
    return {
        'overall_score': round(overall_score, 3),
        'saturated_dimensions': int(saturated_count),
        'saturation_level': level,
        'recommendation': recommendation,
        'dimension_scores': saturation_scores
    }


def generate_report(checks: Dict, overall: Dict) -> str:
    """生成饱和度报告"""
    lines = ["# 理论饱和度检验报告\n"]
    
    # 综合评估
    lines.append(f"## 综合评估")
    lines.append(f"- **饱和度评分**：{overall['overall_score']:.1%}")
    lines.append(f"- **饱和维度**：{overall['saturated_dimensions']}/4")
    lines.append(f"- **饱和水平**：{overall['saturation_level']}")
    lines.append(f"- **建议**：{overall['recommendation']}\n")
    
    # 各维度详情
    lines.append(f"## 1. 概念饱和度")
    cs = checks['concept_saturation']
    lines.append(f"- 新概念率：{cs['new_concept_rate']:.1%}")
    lines.append(f"- 状态：{'✓ 已饱和' if cs['is_saturated'] else '✗ 未饱和'}\n")
    
    lines.append(f"## 2. 范畴完整性")
    cc = checks['category_completeness']
    lines.append(f"- 完整率：{cc['completeness_rate']:.1%}")
    lines.append(f"- 状态：{'✓ 已饱和' if cc['is_saturated'] else '✗ 未饱和'}\n")
    
    lines.append(f"## 3. 关系稳定性")
    rs = checks['relation_stability']
    lines.append(f"- 新关系率：{rs['new_relation_rate']:.1%}")
    lines.append(f"- 状态：{'✓ 已饱和' if rs['is_saturated'] else '✗ 未饱和'}\n")
    
    lines.append(f"## 4. 理论完整性")
    tc = checks['theory_completeness']
    lines.append(f"- 完整率：{tc['completeness_rate']:.1%}")
    lines.append(f"- 状态：{'✓ 已饱和' if tc['is_saturated'] else '✗ 未饱和'}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(
        description='综合饱和度评估工具',
        epilog='示例：python assess_saturation.py -e existing.json -n new.json'
    )
    
    parser.add_argument('--existing', '-e', required=True, help='现有理论/数据文件')
    parser.add_argument('--new', '-n', required=True, help='新数据文件')
    parser.add_argument('--output', '-o', default='saturation_report.json', help='输出文件')
    
    args = parser.parse_args()
    
    # 读取输入
    try:
        with open(args.existing, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    except Exception as e:
        print(f"错误：无法读取现有数据 - {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(args.new, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取新数据 - {e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 执行四个维度的检验
    checks = {
        'concept_saturation': check_concept_saturation(
            new_data.get('concepts', new_data.get('codes', [])),
            existing.get('concepts', existing.get('codes', []))
        ),
        'category_completeness': check_category_completeness(
            existing.get('categories', [])
        ),
        'relation_stability': check_relation_stability(
            existing.get('relations', existing.get('relationships', [])),
            new_data.get('relations', new_data.get('relationships', []))
        ),
        'theory_completeness': check_theory_completeness(
            existing.get('theory', existing)
        )
    }
    
    # 计算综合饱和度
    overall = calculate_overall_saturation(checks)
    
    # 生成报告
    report_text = generate_report(checks, overall)
    
    end_time = datetime.now()
    
    # 标准化输出
    output = {
        'summary': {
            'overall_score': overall['overall_score'],
            'saturated_dimensions': overall['saturated_dimensions'],
            'saturation_level': overall['saturation_level'],
            'recommendation': overall['recommendation'],
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'dimension_checks': checks,
            'dimension_scores': overall['dimension_scores'],
            'report_text': report_text
        },
        'metadata': {
            'existing_file': args.existing,
            'new_file': args.new,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'checking-theory-saturation'
        }
    }
    
    # 写入输出
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 饱和度检验完成")
    print(f"  - 饱和度评分：{overall['overall_score']:.1%}")
    print(f"  - 饱和维度：{overall['saturated_dimensions']}/4")
    print(f"  - 饱和水平：{overall['saturation_level']}")
    print(f"  - 输出文件：{args.output}")


if __name__ == '__main__':
    main()
