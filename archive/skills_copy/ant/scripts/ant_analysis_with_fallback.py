#!/usr/bin/env python3
"""
ANT分析工具包 - 智能依赖管理和功能降级系统

此脚本提供ANT分析功能，优先使用高级依赖包，如不可用则自动降级到基础实现
"""

import argparse
import json
import sys
import importlib
import subprocess
import os
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
import logging


def install_package(package_name: str) -> bool:
    """尝试安装包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False


def check_and_import(module_name: str, package_name: Optional[str] = None) -> Any:
    """检查并导入模块，如失败则返回None"""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        if package_name:
            print(f"模块 {module_name} 未找到，正在尝试安装 {package_name}...")
            if install_package(package_name):
                try:
                    return importlib.import_module(module_name)
                except ImportError:
                    print(f"安装后仍然无法导入 {module_name}")
                    return None
            else:
                print(f"无法安装 {package_name}")
                return None
        return None


# 尝试导入高级包
np = check_and_import("numpy")
pd = check_and_import("pandas")
sm = check_and_import("statsmodels.api", "statsmodels")
pg = check_and_import("pingouin", "pingouin")
nx = check_and_import("networkx", "networkx")
sns = check_and_import("seaborn", "seaborn")
plt = check_and_import("matplotlib.pyplot", "matplotlib")

# 检查高级功能是否可用
ADVANCED_STATS_AVAILABLE = all([np, pd, sm])
ADVANCED_NETWORK_AVAILABLE = nx is not None
ADVANCED_ANALYSIS_AVAILABLE = pg is not None

if ADVANCED_STATS_AVAILABLE:
    print("✓ 高级统计分析功能可用")
else:
    print("ℹ 使用基础统计分析功能")

if ADVANCED_NETWORK_AVAILABLE:
    print("✓ 高级网络分析功能可用")
else:
    print("ℹ 使用基础网络分析功能")

if ADVANCED_ANALYSIS_AVAILABLE:
    print("✓ 高级分析功能可用")
else:
    print("ℹ 使用基础分析功能")


def safe_import_fallback(module_name: str, fallback_func: Callable, package_name: str = None):
    """
    安全导入，失败时返回降级函数
    """
    try:
        module = importlib.import_module(module_name)
        return module
    except ImportError:
        if package_name:
            success = install_package(package_name)
            if success:
                try:
                    return importlib.import_module(module_name)
                except ImportError:
                    return fallback_func
        return fallback_func


def basic_mean(data: List[float]) -> float:
    """基础均值计算"""
    if not data:
        return 0
    return sum(data) / len(data)


def basic_std(data: List[float]) -> float:
    """基础标准差计算"""
    if len(data) < 2:
        return 0
    mean_val = basic_mean(data)
    variance = sum((x - mean_val) ** 2 for x in data) / (len(data) - 1)
    return variance ** 0.5


def basic_correlation(x: List[float], y: List[float]) -> float:
    """基础相关性计算"""
    if len(x) != len(y) or len(x) < 2:
        return 0
    
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_xy = sum(x[i] * y[i] for i in range(n))
    sum_x2 = sum(xi * xi for xi in x)
    sum_y2 = sum(yi * yi for yi in y)
    
    numerator = n * sum_xy - sum_x * sum_y
    denominator = ((n * sum_x2 - sum_x * sum_x) * (n * sum_y2 - sum_y * sum_y)) ** 0.5
    
    if denominator == 0:
        return 0
    
    return numerator / denominator


def advanced_descriptive_stats(data: List[float]) -> Dict[str, float]:
    """高级描述性统计（如果可用）"""
    if ADVANCED_STATS_AVAILABLE:
        try:
            import numpy as np
            import pandas as pd
            import scipy.stats as stats

            series = pd.Series(data)
            desc = series.describe()

            result = {
                'count': int(desc['count']),
                'mean': float(desc['mean']),
                'std': float(desc['std']) if not pd.isna(desc['std']) else 0,
                'min': float(desc['min']),
                'max': float(desc['max']),
                '25%': float(desc['25%']),
                '50%': float(desc['50%']),
                '75%': float(desc['75%']),
                'range': float(desc['max'] - desc['min'])
            }

            # 添加偏度和峰度
            result['skewness'] = float(stats.skew(series))
            result['kurtosis'] = float(stats.kurtosis(series))

            return result
        except Exception as e:
            print(f"高级统计分析失败: {e}，使用基础分析")

    # 降级到基础实现
    if not data:
        return {}

    sorted_data = sorted(data)
    n = len(data)

    return {
        'count': n,
        'mean': basic_mean(data),
        'median': sorted_data[n//2] if n % 2 == 1 else (sorted_data[n//2-1] + sorted_data[n//2]) / 2,
        'std': basic_std(data),
        'min': min(data),
        'max': max(data),
        'range': max(data) - min(data),
        'q25': sorted_data[n//4] if n > 0 else 0,
        'q75': sorted_data[3*n//4] if n > 0 else 0,
        'iqr': (sorted_data[3*n//4] - sorted_data[n//4]) if n > 0 else 0
    }


def advanced_correlation_analysis(x: List[float], y: List[float]) -> Dict[str, Any]:
    """高级相关性分析（如果可用）"""
    if ADVANCED_ANALYSIS_AVAILABLE and ADVANCED_STATS_AVAILABLE:
        try:
            import pingouin as pg
            import pandas as pd
            import numpy as np
            
            df = pd.DataFrame({'x': x, 'y': y})
            corr_result = pg.corr(x, y)
            
            return {
                'correlation': float(corr_result['r'].iloc[0]),
                'p_value': float(corr_result['p-val'].iloc[0]),
                'confidence_interval': [float(corr_result['CI95%'][0][0]), float(corr_result['CI95%'][0][1])],
                'n': int(corr_result['n'].iloc[0])
            }
        except Exception:
            pass  # 降级到基础实现
    
    if ADVANCED_STATS_AVAILABLE:
        try:
            from scipy.stats import pearsonr
            corr, p_value = pearsonr(x, y)
            return {
                'correlation': float(corr),
                'p_value': float(p_value),
                'n': len(x)
            }
        except Exception:
            pass  # 降级到基础实现
    
    # 最终降级到基础实现
    return {
        'correlation': basic_correlation(x, y),
        'n': len(x)
    }


def advanced_network_analysis(edges: List[tuple], nodes: List[str] = None) -> Dict[str, Any]:
    """高级网络分析（如果可用）"""
    if ADVANCED_NETWORK_AVAILABLE:
        try:
            import networkx as nx
            
            G = nx.Graph()
            if nodes:
                G.add_nodes_from(nodes)
            G.add_edges_from(edges)
            
            # 计算网络指标
            results = {
                'num_nodes': G.number_of_nodes(),
                'num_edges': G.number_of_edges(),
                'density': nx.density(G),
                'is_connected': nx.is_connected(G),
                'components': nx.number_connected_components(G)
            }
            
            if G.number_of_nodes() > 0:
                results['avg_clustering'] = nx.average_clustering(G)
                results['avg_shortest_path'] = nx.average_shortest_path_length(G) if nx.is_connected(G) else float('inf')
                
                # 中心性指标
                if G.number_of_nodes() > 1:
                    results['centrality'] = {
                        'degree': dict(nx.degree_centrality(G)),
                        'betweenness': dict(nx.betweenness_centrality(G)),
                        'closeness': dict(nx.closeness_centrality(G))
                    }
            
            return results
        except Exception as e:
            print(f"高级网络分析失败: {e}，使用基础分析")
    
    # 降级到基础实现
    # 基础网络指标计算
    node_set = set()
    for edge in edges:
        node_set.add(edge[0])
        node_set.add(edge[1])
    
    return {
        'num_nodes': len(node_set),
        'num_edges': len(edges),
        'nodes': list(node_set),
        'edges': edges
    }


def main():
    parser = argparse.ArgumentParser(
        description='ANT分析工具（支持高级功能，提供优雅降级）',
        epilog='示例：python ant_analysis_tool.py --input data.json --output results.json --method descriptive'
    )
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON格式）')
    parser.add_argument('--output', '-o', default='ant_results.json', help='输出文件')
    parser.add_argument('--method', '-m', required=True,
                       choices=['descriptive', 'correlation', 'network', 'translation', 'actors'],
                       help='分析方法')
    parser.add_argument('--x-column', help='X轴数据列名（相关性分析）')
    parser.add_argument('--y-column', help='Y轴数据列名（相关性分析）')
    parser.add_argument('--actor-column', help='行动者数据列名（行动者分析）')
    
    args = parser.parse_args()

    start_time = datetime.now()

    # 读取输入数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)

    results = {}

    if args.method == 'descriptive':
        if args.x_column and args.x_column in data:
            column_data = [x for x in data[args.x_column] if isinstance(x, (int, float))]
            results = {
                'variable': args.x_column,
                'descriptive_stats': advanced_descriptive_stats(column_data),
                'using_advanced': ADVANCED_STATS_AVAILABLE
            }
        else:
            results = {'error': '需要指定有效的数据列名'}

    elif args.method == 'correlation':
        if args.x_column and args.y_column and args.x_column in data and args.y_column in data:
            x_data = [x for x in data[args.x_column] if isinstance(x, (int, float))]
            y_data = [y for y in data[args.y_column] if isinstance(y, (int, float))]
            
            if len(x_data) == len(y_data):
                results = {
                    'variables': [args.x_column, args.y_column],
                    'correlation_analysis': advanced_correlation_analysis(x_data, y_data),
                    'using_advanced': ADVANCED_ANALYSIS_AVAILABLE or ADVANCED_STATS_AVAILABLE
                }
            else:
                results = {'error': 'X和Y列数据长度不匹配'}
        else:
            results = {'error': '需要指定有效的X和Y数据列名'}

    elif args.method == 'network':
        # 网络分析
        if 'edges' in data:
            edges = [(item['source'], item['target']) for item in data['edges']]
            nodes = data.get('nodes')
            results = {
                'network_analysis': advanced_network_analysis(edges, nodes),
                'using_advanced': ADVANCED_NETWORK_AVAILABLE
            }
        else:
            results = {'error': '数据中未找到edges字段'}

    # 其他方法...

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'method': args.method,
            'input_file': args.input,
            'processing_time': round((end_time - start_time).total_seconds(), 2),
            'advanced_features_available': {
                'statistics': ADVANCED_STATS_AVAILABLE,
                'network_analysis': ADVANCED_NETWORK_AVAILABLE,
                'advanced_analysis': ADVANCED_ANALYSIS_AVAILABLE
            }
        },
        'details': results,
        'metadata': {
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '2.0.0',
            'skill': 'ant'
        }
    }

    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ ANT分析完成")
    print(f"  - 方法: {args.method}")
    print(f"  - 高级统计: {'启用' if ADVANCED_STATS_AVAILABLE else '禁用'}")
    print(f"  - 高级网络: {'启用' if ADVANCED_NETWORK_AVAILABLE else '禁用'}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()