#!/usr/bin/env python3
"""
描述性统计工具

功能：
1. 集中趋势（均值、中位数、众数）
2. 离散程度（标准差、方差、极差）
3. 分布形态（偏度、峰度）
4. 频数分布

标准化接口：argparse + 三层JSON输出
"""

import argparse
import json
import sys
from datetime import datetime
from typing import List

import numpy as np
from scipy import stats


def calculate_descriptive_stats(data: List[float]) -> dict:
    """计算描述性统计"""
    arr = np.array(data)
    
    return {
        # 集中趋势
        'mean': round(float(np.mean(arr)), 4),
        'median': round(float(np.median(arr)), 4),
        'mode': round(float(stats.mode(arr, keepdims=True)[0][0]), 4) if len(arr) > 0 else None,
        
        # 离散程度
        'std': round(float(np.std(arr, ddof=1)), 4),
        'variance': round(float(np.var(arr, ddof=1)), 4),
        'range': round(float(np.ptp(arr)), 4),
        'iqr': round(float(stats.iqr(arr)), 4),
        
        # 分布形态
        'skewness': round(float(stats.skew(arr)), 4),
        'kurtosis': round(float(stats.kurtosis(arr)), 4),
        
        # 基本信息
        'count': len(arr),
        'min': round(float(np.min(arr)), 4),
        'max': round(float(np.max(arr)), 4),
        'q1': round(float(np.percentile(arr, 25)), 4),
        'q3': round(float(np.percentile(arr, 75)), 4)
    }


def main():
    parser = argparse.ArgumentParser(
        description='描述性统计工具',
        epilog='示例：python descriptive_stats.py --input data.json --column scores'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--column', '-c', default='values', help='数据列名')
    parser.add_argument('--output', '-o', default='descriptive.json', help='输出文件')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data_input = json.load(f)
            
        # 支持多种格式
        if isinstance(data_input, list):
            data = data_input
        elif args.column in data_input:
            data = data_input[args.column]
        elif 'data' in data_input and args.column in data_input['data']:
            data = data_input['data'][args.column]
        else:
            print(f"错误：找不到列 '{args.column}'", file=sys.stderr)
            sys.exit(1)
    
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 计算统计量
    stats_result = calculate_descriptive_stats(data)
    
    end_time = datetime.now()
    
    # 标准化输出
    output = {
        'summary': {
            'count': stats_result['count'],
            'mean': stats_result['mean'],
            'std': stats_result['std'],
            'min': stats_result['min'],
            'max': stats_result['max'],
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'descriptive_statistics': stats_result
        },
        'metadata': {
            'input_file': args.input,
            'column': args.column,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'mathematical-statistics'
        }
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 描述性统计完成")
    print(f"  - 样本量：{stats_result['count']}")
    print(f"  - 均值：{stats_result['mean']:.2f}")
    print(f"  - 标准差：{stats_result['std']:.2f}")
    print(f"  - 输出文件：{args.output}")


if __name__ == '__main__':
    main()
