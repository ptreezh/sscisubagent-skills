#!/usr/bin/env python3
"""
核心范畴识别工具

功能：
1. 计算范畴的解释力（explanatory power）
2. 计算范畴的连接度（connectivity）
3. 计算范畴的数据支持（data support）
4. 综合评分并排序范畴
5. 验证核心范畴

标准化接口：
- 使用argparse命令行接口
- 输出三层JSON格式（summary + details + metadata）
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple


def calculate_explanatory_power(category: Dict, all_data: List) -> float:
    """
    计算范畴的解释力
    
    解释力 = 该范畴能解释的数据片段数 / 总数据片段数
    """
    category_data_count = category.get('data_support', 0)
    total_data_count = sum(cat.get('data_support', 0) for cat in all_data)
    
    if total_data_count == 0:
        return 0.0
    
    return category_data_count / total_data_count


def calculate_connectivity(category: Dict, relations: List[Dict]) -> float:
    """
    计算范畴的连接度
    
    连接度 = 该范畴的关系数 / 总关系数
    """
    category_id = category.get('id') or category.get('name')
    
    # 统计该范畴作为source或target的关系数
    connections = 0
    for rel in relations:
        if rel.get('source') == category_id or rel.get('target') == category_id:
            connections += 1
    
    total_relations = len(relations)
    if total_relations == 0:
        return 0.0
    
    return connections / total_relations


def calculate_data_support(category: Dict, all_data: List) -> float:
    """
    计算范畴的数据支持度
    
    数据支持度 = 该范畴的数据片段数 / 最大数据片段数
    """
    category_data_count = category.get('data_support', 0)
    max_data_count = max((cat.get('data_support', 0) for cat in all_data), default=1)
    
    if max_data_count == 0:
        return 0.0
    
    return category_data_count / max_data_count


def rank_categories(categories: List[Dict], relations: List[Dict]) -> List[Dict]:
    """
    综合评分并排序范畴
    
    综合分数 = 解释力 * 0.4 + 连接度 * 0.3 + 数据支持 * 0.3
    """
    ranked = []
    
    for category in categories:
        explanatory = calculate_explanatory_power(category, categories)
        connectivity = calculate_connectivity(category, relations)
        data_support = calculate_data_support(category, categories)
        
        # 综合评分
        overall_score = (explanatory * 0.4 + 
                        connectivity * 0.3 + 
                        data_support * 0.3)
        
        ranked.append({
            **category,
            'scores': {
                'explanatory_power': round(explanatory, 3),
                'connectivity': round(connectivity, 3),
                'data_support': round(data_support, 3),
                'overall': round(overall_score, 3)
            }
        })
    
    # 按综合分数降序排序
    ranked.sort(key=lambda x: x['scores']['overall'], reverse=True)
    
    return ranked


def validate_core_category(category: Dict, criteria: Dict) -> Tuple[bool, List[str]]:
    """
    验证核心范畴是否符合标准
    
    标准：
    - 解释力 >= 0.15 (解释至少15%的数据)
    - 连接度 >= 0.20 (参与至少20%的关系)
    - 数据支持 >= 0.50 (至少有50%的最大数据支持)
    - 综合分数 >= 0.60
    """
    issues = []
    scores = category.get('scores', {})
    
    min_explanatory = criteria.get('min_explanatory', 0.15)
    min_connectivity = criteria.get('min_connectivity', 0.20)
    min_data_support = criteria.get('min_data_support', 0.50)
    min_overall = criteria.get('min_overall', 0.60)
    
    if scores.get('explanatory_power', 0) < min_explanatory:
        issues.append(f"解释力不足 ({scores.get('explanatory_power', 0):.3f} < {min_explanatory})")
    
    if scores.get('connectivity', 0) < min_connectivity:
        issues.append(f"连接度不足 ({scores.get('connectivity', 0):.3f} < {min_connectivity})")
    
    if scores.get('data_support', 0) < min_data_support:
        issues.append(f"数据支持不足 ({scores.get('data_support', 0):.3f} < {min_data_support})")
    
    if scores.get('overall', 0) < min_overall:
        issues.append(f"综合分数不足 ({scores.get('overall', 0):.3f} < {min_overall})")
    
    is_valid = len(issues) == 0
    
    return is_valid, issues


def main():
    parser = argparse.ArgumentParser(
        description='核心范畴识别工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例用法:
  python identify_core_category.py --input categories.json --relations relationships.json
  python identify_core_category.py -i categories.json -r relationships.json -o core.json
  python identify_core_category.py -i categories.json -r relationships.json --top 3
        '''
    )
    
    parser.add_argument('--input', '-i', required=True,
                       help='输入的范畴文件（JSON格式）')
    parser.add_argument('--relations', '-r', required=True,
                       help='输入的关系文件（JSON格式）')
    parser.add_argument('--output', '-o', default='core_category.json',
                       help='输出文件名（默认：core_category.json）')
    parser.add_argument('--top', '-t', type=int, default=1,
                       help='输出前N个核心范畴（默认：1）')
    parser.add_argument('--criteria', '-c', type=str,
                       help='验证标准JSON文件（可选）')
    
    args = parser.parse_args()
    
    # 读取输入文件
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            input_data = json.load(f)
            categories = input_data.get('details', {}).get('categories', [])
            if not categories:
                categories = input_data.get('categories', [])
    except Exception as e:
        print(f"错误：无法读取范畴文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    try:
        with open(args.relations, 'r', encoding='utf-8') as f:
            relations_data = json.load(f)
            relations = relations_data.get('details', {}).get('relations', [])
            if not relations:
                relations = relations_data.get('relations', [])
    except Exception as e:
        print(f"错误：无法读取关系文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    # 读取验证标准（如果提供）
    criteria = {
        'min_explanatory': 0.15,
        'min_connectivity': 0.20,
        'min_data_support': 0.50,
        'min_overall': 0.60
    }
    if args.criteria:
        try:
            with open(args.criteria, 'r', encoding='utf-8') as f:
                criteria.update(json.load(f))
        except Exception as e:
            print(f"警告：无法读取验证标准文件，使用默认标准 - {e}", file=sys.stderr)
    
    # 处理开始时间
    start_time = datetime.now()
    
    # 排序范畴
    ranked_categories = rank_categories(categories, relations)
    
    # 选择核心范畴
    core_categories = ranked_categories[:args.top]
    
    # 验证核心范畴
    for category in core_categories:
        is_valid, issues = validate_core_category(category, criteria)
        category['validation'] = {
            'is_valid': is_valid,
            'issues': issues
        }
    
    # 处理结束时间
    end_time = datetime.now()
    processing_time = (end_time - start_time).total_seconds()
    
    # 构建标准化输出
    output = {
        'summary': {
            'total_categories': len(categories),
            'core_categories_count': len(core_categories),
            'core_category_names': [cat.get('name', cat.get('id')) for cat in core_categories],
            'top_score': core_categories[0]['scores']['overall'] if core_categories else 0,
            'processing_time': round(processing_time, 2)
        },
        'details': {
            'core_categories': core_categories,
            'all_ranked_categories': ranked_categories,
            'criteria_used': criteria
        },
        'metadata': {
            'input_file': args.input,
            'relations_file': args.relations,
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'performing-selective-coding'
        }
    }
    
    # 写入输出文件
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"✓ 核心范畴识别完成")
        print(f"  - 总范畴数：{len(categories)}")
        print(f"  - 核心范畴：{', '.join(output['summary']['core_category_names'])}")
        print(f"  - 最高分数：{output['summary']['top_score']:.3f}")
        print(f"  - 输出文件：{args.output}")
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
