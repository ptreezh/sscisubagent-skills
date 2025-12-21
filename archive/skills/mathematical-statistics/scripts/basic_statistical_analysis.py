#!/usr/bin/env python3
"""
基础统计分析工具

功能：
1. 描述性统计（均值、中位数、标准差等）
2. 基础假设检验（t检验、卡方检验）
3. 相关性分析
4. 简单回归分析

标准化接口：argparse + 三层JSON输出
不依赖高级统计包（statsmodels, pingouin等）
"""

import argparse
import json
import sys
import math
from datetime import datetime
from typing import Dict, List, Any, Tuple
from collections import Counter


def mean(data: List[float]) -> float:
    """计算均值"""
    if not data:
        return 0
    return sum(data) / len(data)


def median(data: List[float]) -> float:
    """计算中位数"""
    if not data:
        return 0
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 0:
        return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
    else:
        return sorted_data[n//2]


def std(data: List[float]) -> float:
    """计算标准差"""
    if len(data) < 2:
        return 0
    avg = mean(data)
    variance = sum((x - avg) ** 2 for x in data) / (len(data) - 1)
    return math.sqrt(variance)


def variance(data: List[float]) -> float:
    """计算方差"""
    if len(data) < 2:
        return 0
    avg = mean(data)
    return sum((x - avg) ** 2 for x in data) / (len(data) - 1)


def describe_data(data: List[float]) -> Dict[str, float]:
    """描述性统计"""
    if not data:
        return {}
    
    sorted_data = sorted(data)
    n = len(data)
    
    return {
        'count': n,
        'mean': mean(data),
        'median': median(data),
        'std': std(data),
        'variance': variance(data),
        'min': min(data),
        'max': max(data),
        'range': max(data) - min(data),
        'q25': sorted_data[n//4] if n > 0 else 0,
        'q75': sorted_data[3*n//4] if n > 0 else 0,
        'iqr': sorted_data[3*n//4] - sorted_data[n//4] if n > 0 else 0
    }


def pearson_correlation(x: List[float], y: List[float]) -> float:
    """计算皮尔逊相关系数"""
    if len(x) != len(y) or len(x) < 2:
        return 0
    
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x2 = sum(xi * xi for xi in x)
    sum_y2 = sum(yi * yi for yi in y)
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator = math.sqrt((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y))
    
    if denominator == 0:
        return 0
    
    return numerator / denominator


def t_test_independent(x: List[float], y: List[float]) -> Dict[str, float]:
    """独立样本t检验"""
    if len(x) < 2 or len(y) < 2:
        return {'error': '样本量不足'}
    
    mean_x, mean_y = mean(x), mean(y)
    var_x, var_y = variance(x), variance(y)
    n_x, n_y = len(x), len(y)
    
    # 合并方差
    pooled_var = ((n_x - 1) * var_x + (n_y - 1) * var_y) / (n_x + n_y - 2)
    
    # t统计量
    se = math.sqrt(pooled_var * (1/n_x + 1/n_y))
    t_stat = (mean_x - mean_y) / se if se != 0 else 0
    
    # 自由度
    df = n_x + n_y - 2
    
    # 估算p值（使用近似方法）
    # 这里使用简化的近似方法，实际应用中可能需要更精确的计算
    p_value = 2 * (1 - min(1, abs(t_stat) / 4))  # 简化的p值估算
    
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'degrees_of_freedom': df,
        'mean_difference': mean_x - mean_y,
        'effect_size': (mean_x - mean_y) / math.sqrt(pooled_var)  # Cohen's d
    }


def chi_square_test(observed: List[List[int]]) -> Dict[str, Any]:
    """卡方独立性检验"""
    if not observed or not observed[0]:
        return {'error': '观测数据为空'}
    
    rows, cols = len(observed), len(observed[0])
    
    # 计算行和列的总和
    row_totals = [sum(observed[i]) for i in range(rows)]
    col_totals = [sum(observed[i][j] for i in range(rows)) for j in range(cols)]
    total = sum(row_totals)
    
    if total == 0:
        return {'error': '总观测数为0'}
    
    # 计算期望值
    expected = []
    for i in range(rows):
        expected_row = []
        for j in range(cols):
            exp_val = (row_totals[i] * col_totals[j]) / total
            expected_row.append(exp_val)
        expected.append(expected_row)
    
    # 计算卡方统计量
    chi2 = 0
    for i in range(rows):
        for j in range(cols):
            if expected[i][j] != 0:
                chi2 += (observed[i][j] - expected[i][j]) ** 2 / expected[i][j]
    
    # 自由度
    df = (rows - 1) * (cols - 1)
    
    # 估算p值（使用近似方法）
    # 这里使用简化的近似方法
    p_value = math.exp(-chi2 / 2) if df > 0 else 1
    
    return {
        'chi2_statistic': chi2,
        'p_value': p_value,
        'degrees_of_freedom': df,
        'contingency_table': observed,
        'expected_frequencies': expected
    }


def simple_linear_regression(x: List[float], y: List[float]) -> Dict[str, float]:
    """简单线性回归"""
    if len(x) != len(y) or len(x) < 2:
        return {'error': '数据不足或长度不匹配'}
    
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x2 = sum(xi * xi for xi in x)
    
    # 计算回归系数
    denominator = n * sum_x2 - sum_x * sum_x
    if denominator == 0:
        return {'error': '无法计算回归系数（x值全部相同）'}
    
    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n
    
    # 计算预测值和残差
    y_pred = [intercept + slope * xi for xi in x]
    residuals = [y[i] - y_pred[i] for i in range(n)]
    
    # 计算R²
    ss_res = sum(res ** 2 for res in residuals)
    ss_tot = sum((yi - mean(y)) ** 2 for yi in y)
    r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    return {
        'slope': slope,
        'intercept': intercept,
        'r_squared': r_squared,
        'regression_equation': f'y = {intercept:.4f} + {slope:.4f}x',
        'predictions': y_pred
    }


def main():
    parser = argparse.ArgumentParser(
        description='基础统计分析工具（不依赖高级统计包）',
        epilog='示例：python basic_statistical_analysis.py --input data.json --output results.json --analysis descriptive'
    )
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--output', '-o', default='stats_results.json', help='输出文件')
    parser.add_argument('--analysis', '-a', required=True, 
                       choices=['descriptive', 'correlation', 't_test', 'chi_square', 'regression'],
                       help='分析类型')
    parser.add_argument('--x-column', '-x', help='X轴数据列名（相关性/回归分析）')
    parser.add_argument('--y-column', '-y', help='Y轴数据列名（相关性/回归分析）')
    parser.add_argument('--group-column', '-g', help='分组列名（t检验）')
    
    args = parser.parse_args()

    # 读取输入数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)

    start_time = datetime.now()

    results = {}
    
    if args.analysis == 'descriptive':
        # 描述性统计
        if args.x_column and args.x_column in data:
            column_data = data[args.x_column]
            if isinstance(column_data, list):
                results = {
                    'variable': args.x_column,
                    'descriptive_stats': describe_data([x for x in column_data if isinstance(x, (int, float))])
                }
            else:
                results = {'error': f'列 {args.x_column} 不是列表格式'}
        else:
            results = {'error': '需要指定要分析的列名'}
    
    elif args.analysis == 'correlation':
        # 相关性分析
        if args.x_column and args.y_column and args.x_column in data and args.y_column in data:
            x_data = [x for x in data[args.x_column] if isinstance(x, (int, float))]
            y_data = [y for y in data[args.y_column] if isinstance(y, (int, float))]
            
            if len(x_data) == len(y_data):
                correlation = pearson_correlation(x_data, y_data)
                results = {
                    'variables': [args.x_column, args.y_column],
                    'correlation': correlation,
                    'n_observations': len(x_data)
                }
            else:
                results = {'error': 'X和Y列的数据长度不一致'}
        else:
            results = {'error': '需要指定X和Y列名'}
    
    elif args.analysis == 't_test':
        # t检验
        if args.x_column and args.group_column and args.x_column in data and args.group_column in data:
            x_data = [x for x in data[args.x_column] if isinstance(x, (int, float))]
            group_data = data[args.group_column]
            
            if len(x_data) == len(group_data):
                # 分组数据
                groups = {}
                for i, group in enumerate(group_data):
                    if group not in groups:
                        groups[group] = []
                    if i < len(x_data):  # 防止索引错误
                        groups[group].append(x_data[i])
                
                if len(groups) >= 2:
                    # 取前两组进行t检验
                    group_names = list(groups.keys())[:2]
                    group1_data = groups[group_names[0]]
                    group2_data = groups[group_names[1]]
                    
                    t_test_result = t_test_independent(group1_data, group2_data)
                    results = {
                        'groups': group_names,
                        'group1_size': len(group1_data),
                        'group2_size': len(group2_data),
                        't_test_result': t_test_result
                    }
                else:
                    results = {'error': '需要至少两组数据'}
            else:
                results = {'error': 'X列和分组列的数据长度不一致'}
        else:
            results = {'error': '需要指定X列和分组列名'}
    
    elif args.analysis == 'chi_square':
        # 卡方检验
        if args.x_column and args.y_column and args.x_column in data and args.y_column in data:
            x_data = data[args.x_column]
            y_data = data[args.y_column]
            
            if len(x_data) == len(y_data):
                # 构建列联表
                contingency = {}
                for i in range(len(x_data)):
                    x_val, y_val = str(x_data[i]), str(y_data[i])
                    if x_val not in contingency:
                        contingency[x_val] = {}
                    if y_val not in contingency[x_val]:
                        contingency[x_val][y_val] = 0
                    contingency[x_val][y_val] += 1
                
                # 转换为矩阵格式
                x_vals = sorted(contingency.keys())
                y_vals = set()
                for x_val in x_vals:
                    y_vals.update(contingency[x_val].keys())
                y_vals = sorted(list(y_vals))
                
                observed_matrix = []
                for x_val in x_vals:
                    row = []
                    for y_val in y_vals:
                        row.append(contingency[x_val].get(y_val, 0))
                    observed_matrix.append(row)
                
                chi_square_result = chi_square_test(observed_matrix)
                results = {
                    'variables': [args.x_column, args.y_column],
                    'contingency_table': {x: {y: contingency[x].get(y, 0) for y in y_vals} for x in x_vals},
                    'chi_square_result': chi_square_result
                }
            else:
                results = {'error': 'X和Y列的数据长度不一致'}
        else:
            results = {'error': '需要指定X和Y列名'}
    
    elif args.analysis == 'regression':
        # 简单线性回归
        if args.x_column and args.y_column and args.x_column in data and args.y_column in data:
            x_data = [x for x in data[args.x_column] if isinstance(x, (int, float))]
            y_data = [y for y in data[args.y_column] if isinstance(y, (int, float))]
            
            if len(x_data) == len(y_data):
                regression_result = simple_linear_regression(x_data, y_data)
                results = {
                    'variables': {'x': args.x_column, 'y': args.y_column},
                    'regression_result': regression_result,
                    'n_observations': len(x_data)
                }
            else:
                results = {'error': 'X和Y列的数据长度不一致'}
        else:
            results = {'error': '需要指定X和Y列名'}

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'analysis_type': args.analysis,
            'input_file': args.input,
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': results,
        'metadata': {
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'mathematical-statistics'
        }
    }

    # 保存输出
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ 统计分析完成")
    print(f"  - 分析类型: {args.analysis}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()