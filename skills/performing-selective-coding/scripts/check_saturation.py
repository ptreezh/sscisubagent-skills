#!/usr/bin/env python3
"""
理论饱和度检验工具

功能：
1. 检查新概念出现率（new concepts rate）
2. 检查范畴完整性（category completeness）
3. 检查关系稳定性（relationship stability）
4. 评估理论完整性（theory completeness）
5. 生成饱和度报告（saturation report）

标准化接口：argparse + 三层JSON输出
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List


def check_new_concepts(new_data: List, existing_concepts: List) -> Dict:
    """检查新概念出现率"""
    new_concepts = []
    
    for item in new_data:
        concept = item.get('concept') or item.get('name')
        if concept and concept not in existing_concepts:
            new_concepts.append(concept)
    
    new_concept_rate = len(new_concepts) / len(new_data) if new_data else 0
    
    return {
        'new_concepts': new_concepts,
        'new_concept_count': len(new_concepts),
        'new_concept_rate': round(new_concept_rate, 3),
        'is_saturated': new_concept_rate < 0.05  # <5%认为饱和
    }


def check_category_completeness(categories: List[Dict]) -> Dict:
    """检查范畴完整性"""
    complete_categories = 0
    
    for cat in categories:
        # 检查是否有定义、属性、案例
        has_definition = bool(cat.get('definition'))
        has_properties = bool(cat.get('properties'))
        has_examples = bool(cat.get('examples'))
        
        if has_definition and has_properties and has_examples:
            complete_categories += 1
    
    completeness = complete_categories / len(categories) if categories else 0
    
    return {
        'total_categories': len(categories),
        'complete_categories': complete_categories,
        'completeness_rate': round(completeness, 3),
        'is_saturated': completeness >= 0.90  # ≥90%认为饱和
    }


def check_relation_stability(relations: List, new_relations: List) -> Dict:
    """检查关系稳定性"""
    # 简化：检查新关系的比例
    new_relation_count = len(new_relations)
    total_relations = len(relations) + new_relation_count
    
    new_relation_rate = new_relation_count / total_relations if total_relations else 0
    
    return {
        'existing_relations': len(relations),
        'new_relations': new_relation_count,
        'new_relation_rate': round(new_relation_rate, 3),
        'is_saturated': new_relation_rate < 0.10  # <10%认为饱和
    }


def assess_theory_completeness(theory: Dict) -> Dict:
    """评估理论完整性"""
    # 检查理论的核心组件
    has_core_category = bool(theory.get('core_category'))
    has_propositions = bool(theory.get('propositions'))
    has_framework = bool(theory.get('framework'))
    has_boundaries = bool(theory.get('boundaries'))
    
    components = [has_core_category, has_propositions, has_framework, has_boundaries]
    completeness = sum(components) / len(components)
    
    return {
        'has_core_category': has_core_category,
        'has_propositions': has_propositions,
        'has_framework': has_framework,
        'has_boundaries': has_boundaries,
        'completeness_rate': round(completeness, 3),
        'is_saturated': completeness >= 0.90
    }


def generate_saturation_report(checks: Dict) -> str:
    """生成饱和度报告"""
    report_lines = ["# 理论饱和度检验报告\n"]
    
    # 概念饱和度
    concept_check = checks['concept_saturation']
    report_lines.append(f"## 1. 概念饱和度")
    report_lines.append(f"- 新概念率：{concept_check['new_concept_rate']:.1%}")
    report_lines.append(f"- 状态：{'✓ 已饱和' if concept_check['is_saturated'] else '✗ 未饱和'}\n")
    
    # 范畴完整性
    category_check = checks['category_completeness']
    report_lines.append(f"## 2. 范畴完整性")
    report_lines.append(f"- 完整率：{category_check['completeness_rate']:.1%}")
    report_lines.append(f"- 状态：{'✓ 已饱和' if category_check['is_saturated'] else '✗ 未饱和'}\n")
    
    # 关系稳定性
    relation_check = checks['relation_stability']
    report_lines.append(f"## 3. 关系稳定性")
    report_lines.append(f"- 新关系率：{relation_check['new_relation_rate']:.1%}")
    report_lines.append(f"- 状态：{'✓ 已饱和' if relation_check['is_saturated'] else '✗ 未饱和'}\n")
    
    # 理论完整性
    theory_check = checks['theory_completeness']
    report_lines.append(f"## 4. 理论完整性")
    report_lines.append(f"- 完整率：{theory_check['completeness_rate']:.1%}")
    report_lines.append(f"- 状态：{'✓ 已饱和' if theory_check['is_saturated'] else '✗ 未饱和'}\n")
    
    # 综合判断
    all_saturated = all([
        concept_check['is_saturated'],
        category_check['is_saturated'],
        relation_check['is_saturated'],
        theory_check['is_saturated']
    ])
    
    report_lines.append(f"## 综合判断")
    report_lines.append(f"**{'✓ 理论已达到饱和' if all_saturated else '✗ 理论尚未饱和'}**")
    
    return '\n'.join(report_lines)


def main():
    parser = argparse.ArgumentParser(
        description='理论饱和度检验工具',
        epilog='示例：python check_saturation.py -e existing.json -n new.json'
    )
    
    parser.add_argument('--existing', '-e', required=True, help='现有数据/理论文件')
    parser.add_argument('--new', '-n', required=True, help='新数据文件')
    parser.add_argument('--output', '-o', default='saturation.json', help='输出文件')
    
    args = parser.parse_args()
    
    # 读取输入
    try:
        with open(args.existing, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(args.new, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 执行检验
    checks = {
        'concept_saturation': check_new_concepts(
            new_data.get('concepts', []),
            existing.get('concepts', [])
        ),
        'category_completeness': check_category_completeness(
            existing.get('categories', [])
        ),
        'relation_stability': check_relation_stability(
            existing.get('relations', []),
            new_data.get('relations', [])
        ),
        'theory_completeness': assess_theory_completeness(
            existing.get('theory', {})
        )
    }
    
    report_text = generate_saturation_report(checks)
    
    # 综合饱和度评分
    saturation_score = sum([
        checks['concept_saturation']['is_saturated'],
        checks['category_completeness']['is_saturated'],
        checks['relation_stability']['is_saturated'],
        checks['theory_completeness']['is_saturated']
    ]) / 4.0
    
    end_time = datetime.now()
    
    # 输出
    output = {
        'summary': {
            'saturation_score': round(saturation_score, 3),
            'is_fully_saturated': saturation_score >= 1.0,
            'saturated_dimensions': sum([
                checks['concept_saturation']['is_saturated'],
                checks['category_completeness']['is_saturated'],
                checks['relation_stability']['is_saturated'],
                checks['theory_completeness']['is_saturated']
            ]),
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'checks': checks,
            'report_text': report_text
        },
        'metadata': {
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'performing-selective-coding'
        }
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 饱和度检验完成")
    print(f"  - 饱和度评分：{saturation_score:.1%}")
    print(f"  - 饱和维度：{output['summary']['saturated_dimensions']}/4")
    print(f"  - 输出文件：{args.output}")


if __name__ == '__main__':
    main()
