#!/usr/bin/env python3
"""
信度分析工具

功能：
1. Cronbach's α系数
2. 折半信度（Split-half reliability）
3. 重测信度（Test-retest reliability）
4. 评分者间信度（Inter-rater reliability）

标准化接口：argparse + 三层JSON输出
"""

import argparse
import json
import sys
from datetime import datetime
from typing import List, Dict

import numpy as np
from scipy import stats


def calculate_cronbach_alpha(data: List[List[float]]) -> Dict:
    """计算Cronbach's α系数"""
    if not data or len(data) < 2:
        return {'alpha': 0.0, 'n_items': 0, 'n_subjects': 0}
    
    arr = np.array(data)
    n_items = arr.shape[1]
    n_subjects = arr.shape[0]
    
    # 计算每个项目的方差
    item_variances = np.var(arr, axis=0, ddof=1)
    
    # 计算总分方差
    total_scores = np.sum(arr, axis=1)
    total_variance = np.var(total_scores, ddof=1)
    
    # Cronbach's α公式
    alpha = (n_items / (n_items - 1)) * (1 - np.sum(item_variances) / total_variance)
    
    # 解释标准
    if alpha >= 0.9:
        interpretation = "优秀"
    elif alpha >= 0.8:
        interpretation = "良好"
    elif alpha >= 0.7:
        interpretation = "可接受"
    elif alpha >= 0.6:
        interpretation = " questionable"
    elif alpha >= 0.5:
        interpretation = "差"
    else:
        interpretation = "不可接受"
    
    return {
        'alpha': round(float(alpha), 4),
        'n_items': n_items,
        'n_subjects': n_subjects,
        'interpretation': interpretation,
        'item_variances': [round(float(v), 4) for v in item_variances],
        'total_variance': round(float(total_variance), 4)
    }


def calculate_split_half(data: List[List[float]]) -> Dict:
    """计算折半信度"""
    if not data or len(data) < 2:
        return {'split_half': 0.0, 'n_items': 0}
    
    arr = np.array(data)
    n_items = arr.shape[1]
    
    # 将项目分为两半
    half = n_items // 2
    first_half = arr[:, :half]
    second_half = arr[:, half:n_items]
    
    # 计算两半的总分
    first_scores = np.sum(first_half, axis=1)
    second_scores = np.sum(second_half, axis=1)
    
    # 计算相关系数
    correlation, p_value = stats.pearsonr(first_scores, second_scores)
    
    # Spearman-Brown校正
    if correlation >= 1.0:  # 避免除零
        correlation = 0.999
    sb_coefficient = (2 * correlation) / (1 + correlation)
    
    return {
        'split_half': round(float(sb_coefficient), 4),
        'raw_correlation': round(float(correlation), 4),
        'p_value': round(float(p_value), 4),
        'n_items': n_items,
        'first_half_items': half,
        'second_half_items': n_items - half
    }


def calculate_test_retest(test_data: List[float], retest_data: List[float]) -> Dict:
    """计算重测信度"""
    if len(test_data) != len(retest_data) or len(test_data) < 3:
        return {'test_retest': 0.0, 'n_pairs': 0}
    
    # 计算相关系数
    correlation, p_value = stats.pearsonr(test_data, retest_data)
    
    # 解释标准
    if correlation >= 0.8:
        interpretation = "优秀"
    elif correlation >= 0.6:
        interpretation = "良好"
    elif correlation >= 0.4:
        interpretation = "可接受"
    else:
        interpretation = "差"
    
    return {
        'test_retest': round(float(correlation), 4),
        'p_value': round(float(p_value), 4),
        'interpretation': interpretation,
        'n_pairs': len(test_data)
    }


def calculate_inter_rater(data: Dict[str, List[float]]) -> Dict:
    """计算评分者间信度（使用Kendall's W）"""
    n_raters = len(data)
    if n_raters < 2:
        return {'kendall_w': 0.0, 'n_raters': 0}
    
    # 转换为矩阵
    ratings = []
    for rater_scores in data.values():
        ratings.append(rater_scores)
    
    arr = np.array(ratings)
    n_items = arr.shape[1]
    
    # 计算Kendall's W
    sum_ranks = np.sum(arr, axis=0)
    mean_ranks = np.mean(sum_ranks)
    ss = np.sum((sum_ranks - mean_ranks) ** 2)
    
    # 最大可能的平方和
    max_ss = (n_raters ** 2 * (n_items ** 3 - n_items)) / 12
    
    if max_ss > 0:
        kendall_w = ss / max_ss
    else:
        kendall_w = 0.0
    
    # 解释标准
    if kendall_w >= 0.8:
        interpretation = "优秀"
    elif kendall_w >= 0.6:
        interpretation = "良好"
    elif kendall_w >= 0.4:
        interpretation = "可接受"
    else:
        interpretation = "差"
    
    return {
        'kendall_w': round(float(kendall_w), 4),
        'interpretation': interpretation,
        'n_raters': n_raters,
        'n_items': n_items
    }


def main():
    parser = argparse.ArgumentParser(
        description='信度分析工具',
        epilog='示例：python reliability_analysis.py --input data.json --type cronbach'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--type', '-t', required=True,
                       choices=['cronbach', 'split_half', 'test_retest', 'inter_rater'],
                       help='信度类型')
    parser.add_argument('--output', '-o', default='reliability.json', help='输出文件')
    parser.add_argument('--test-column', help='重测信度的第一次测试列名')
    parser.add_argument('--retest-column', help='重测信度的第二次测试列名')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data_input = json.load(f)
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 根据类型计算信度
    if args.type == 'cronbach':
        if isinstance(data_input, list):
            data = data_input
        else:
            data = list(data_input.values())
        result = calculate_cronbach_alpha(data)
        
    elif args.type == 'split_half':
        if isinstance(data_input, list):
            data = data_input
        else:
            data = list(data_input.values())
        result = calculate_split_half(data)
        
    elif args.type == 'test_retest':
        if not args.test_column or not args.retest_column:
            print("错误：重测信度需要指定--test-column和--retest-column", file=sys.stderr)
            sys.exit(1)
        test_data = data_input.get(args.test_column, [])
        retest_data = data_input.get(args.retest_column, [])
        result = calculate_test_retest(test_data, retest_data)
        
    elif args.type == 'inter_rater':
        result = calculate_inter_rater(data_input)
    
    end_time = datetime.now()
    
    # 标准化输出
    output = {
        'summary': {
            'reliability_type': args.type,
            'reliability_value': result.get(f'{args.type}', 0.0),
            'interpretation': result.get('interpretation', ''),
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'reliability_analysis': result
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
    
    print(f"✓ 信度分析完成")
    print(f"  - 类型：{args.type}")
    print(f"  - 信度值：{result.get(f'{args.type}', 0.0):.4f}")
    print(f"  - 解释：{result.get('interpretation', '')}")
    print(f"  - 输出文件：{args.output}")


if __name__ == '__main__':
    main()