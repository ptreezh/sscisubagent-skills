#!/usr/bin/env python3
"""
效度分析工具

功能：
1. 内容效度分析（Content Validity）
2. 结构效度分析（Construct Validity）
3. 效标效度分析（Criterion Validity）
4. 聚合效度分析（Convergent/Discriminant Validity）

标准化接口：argparse + 三层JSON输出
"""

import argparse
import json
import sys
from datetime import datetime
from typing import List, Dict

import numpy as np
from scipy import stats


def calculate_content_validity(expert_ratings: List[Dict]) -> Dict:
    """计算内容效度（基于专家评定）"""
    if not expert_ratings:
        return {'content_validity_index': 0.0, 'n_experts': 0}
    
    # 计算每个项目的效度指数
    item_validity = []
    for item in expert_ratings:
        ratings = item.get('ratings', [])
        if ratings:
            # 计算内容效度比率（评分≥3的比例）
            valid_ratings = sum(1 for r in ratings if r >= 3)
            cvi = valid_ratings / len(ratings)
            item_validity.append(cvi)
    
    # 计算整体内容效度指数
    if item_validity:
        cvi = np.mean(item_validity)
    else:
        cvi = 0.0
    
    # 解释标准
    if cvi >= 0.90:
        interpretation = "优秀"
    elif cvi >= 0.80:
        interpretation = "良好"
    elif cvi >= 0.70:
        interpretation = "可接受"
    else:
        interpretation = "需要改进"
    
    return {
        'content_validity_index': round(float(cvi), 4),
        'n_experts': len(expert_ratings),
        'n_items': len(item_validity),
        'item_validity': [round(v, 4) for v in item_validity],
        'interpretation': interpretation
    }


def calculate_construct_validity(test_scores: List[float], related_scores: List[float]) -> Dict:
    """计算结构效度（与相关构念的相关性）"""
    if len(test_scores) != len(related_scores) or len(test_scores) < 3:
        return {'construct_validity': 0.0, 'n_pairs': 0}
    
    # 计算相关系数
    correlation, p_value = stats.pearsonr(test_scores, related_scores)
    
    # 解释标准
    if correlation >= 0.70:
        interpretation = "优秀"
    elif correlation >= 0.50:
        interpretation = "良好"
    elif correlation >= 0.30:
        interpretation = "可接受"
    else:
        interpretation = "需要改进"
    
    return {
        'construct_validity': round(float(correlation), 4),
        'p_value': round(float(p_value), 4),
        'n_pairs': len(test_scores),
        'interpretation': interpretation,
        'statistical_significance': p_value < 0.05
    }


def calculate_criterion_validity(test_scores: List[float], criterion_scores: List[float]) -> Dict:
    """计算效标效度（与外部标准的关联）"""
    if len(test_scores) != len(criterion_scores) or len(test_scores) < 3:
        return {'criterion_validity': 0.0, 'n_pairs': 0}
    
    # 计算相关系数
    correlation, p_value = stats.pearsonr(test_scores, criterion_scores)
    
    # 计算预测效度（R²）
    r_squared = correlation ** 2
    
    # 解释标准
    if correlation >= 0.80:
        interpretation = "优秀"
    elif correlation >= 0.60:
        interpretation = "良好"
    elif correlation >= 0.40:
        interpretation = "可接受"
    else:
        interpretation = "需要改进"
    
    return {
        'criterion_validity': round(float(correlation), 4),
        'r_squared': round(float(r_squared), 4),
        'p_value': round(float(p_value), 4),
        'n_pairs': len(test_scores),
        'interpretation': interpretation,
        'statistical_significance': p_value < 0.05
    }


def calculate_convergent_discriminant(test1_scores: List[float], test2_scores: List[float], 
                                     unrelated_scores: List[float]) -> Dict:
    """计算聚合效度和区分效度"""
    # 聚合效度：测量同一构念的不同方法的相关性
    if len(test1_scores) != len(test2_scores):
        convergent = 0.0
        convergent_p = 1.0
    else:
        convergent, convergent_p = stats.pearsonr(test1_scores, test2_scores)
    
    # 区分效度：测量不同构念的相关性（应该很低）
    if len(test1_scores) != len(unrelated_scores):
        discriminant = 0.0
        discriminant_p = 1.0
    else:
        discriminant, discriminant_p = stats.pearsonr(test1_scores, unrelated_scores)
    
    # 判断标准
    convergent_acceptable = convergent >= 0.70 and convergent_p < 0.05
    discriminant_acceptable = abs(discriminant) < 0.30 or discriminant_p >= 0.05
    
    return {
        'convergent_validity': {
            'correlation': round(float(convergent), 4),
            'p_value': round(float(convergent_p), 4),
            'acceptable': convergent_acceptable
        },
        'discriminant_validity': {
            'correlation': round(float(discriminant), 4),
            'p_value': round(float(discriminant_p), 4),
            'acceptable': discriminant_acceptable
        },
        'overall_validity': convergent_acceptable and discriminant_acceptable
    }


def main():
    parser = argparse.ArgumentParser(
        description='效度分析工具',
        epilog='示例：python validity_analysis.py --input data.json --type content'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--type', '-t', required=True,
                       choices=['content', 'construct', 'criterion', 'convergent'],
                       help='效度类型')
    parser.add_argument('--output', '-o', default='validity.json', help='输出文件')
    parser.add_argument('--test-column', help='测试分数列名（用于construct/criterion）')
    parser.add_argument('--related-column', help='相关分数列名（用于construct）')
    parser.add_argument('--criterion-column', help='效标分数列名（用于criterion）')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data_input = json.load(f)
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 根据类型计算效度
    if args.type == 'content':
        result = calculate_content_validity(data_input.get('expert_ratings', []))
        
    elif args.type == 'construct':
        if not args.test_column or not args.related_column:
            print("错误：结构效度需要指定--test-column和--related-column", file=sys.stderr)
            sys.exit(1)
        test_scores = data_input.get(args.test_column, [])
        related_scores = data_input.get(args.related_column, [])
        result = calculate_construct_validity(test_scores, related_scores)
        
    elif args.type == 'criterion':
        if not args.test_column or not args.criterion_column:
            print("错误：效标效度需要指定--test-column和--criterion-column", file=sys.stderr)
            sys.exit(1)
        test_scores = data_input.get(args.test_column, [])
        criterion_scores = data_input.get(args.criterion_column, [])
        result = calculate_criterion_validity(test_scores, criterion_scores)
        
    elif args.type == 'convergent':
        test1_scores = data_input.get('test1_scores', [])
        test2_scores = data_input.get('test2_scores', [])
        unrelated_scores = data_input.get('unrelated_scores', [])
        result = calculate_convergent_discriminant(test1_scores, test2_scores, unrelated_scores)
    
    end_time = datetime.now()
    
    # 标准化输出
    output = {
        'summary': {
            'validity_type': args.type,
            'validity_value': result.get(f'{args.type}_validity', 0.0) if args.type != 'convergent' else result.get('overall_validity', False),
            'interpretation': result.get('interpretation', ''),
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'validity_analysis': result
        },
        'metadata': {
            'input_file': args.input,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'validity-reliability'
        }
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 效度分析完成")
    print(f"  - 类型：{args.type}")
    if args.type != 'convergent':
        print(f"  - 效度值：{result.get(f'{args.type}_validity', 0.0):.4f}")
    print(f"  - 解释：{result.get('interpretation', '')}")
    print(f"  - 输出文件：{args.output}")


if __name__ == '__main__':
    main()