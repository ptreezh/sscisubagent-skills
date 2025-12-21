#!/usr/bin/env python3
"""
高级统计分析工具（支持高级依赖包，提供优雅降级）

功能：
1. 描述性统计（均值、中位数、标准差等）
2. 基础假设检验（t检验、卡方检验）
3. 相关性分析
4. 回归分析
5. 方差分析
6. 因子分析

优先使用高级依赖包（statsmodels, pingouin, scikit-learn），若不可用则降级到基础实现
"""

import argparse
import json
import sys
import math
import importlib
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter
import subprocess
import os


def check_and_install_package(package_name: str) -> bool:
    """检查并尝试安装包"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        print(f"正在安装 {package_name}...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
            return True
        except subprocess.CalledProcessError:
            print(f"无法安装 {package_name}，将使用降级功能")
            return False


# 检查高级包是否可用
STATS_AVAILABLE = check_and_install_package("statsmodels")
PINGOUIN_AVAILABLE = check_and_install_package("pingouin")
SKLEARN_AVAILABLE = check_and_install_package("scikit-learn")
FACTOR_AVAILABLE = check_and_install_package("factor-analyzer")


# 高级包导入（如果可用）
if STATS_AVAILABLE:
    try:
        import numpy as np
        import pandas as pd
        import statsmodels.api as sm
        from statsmodels.formula.api import ols
        from scipy import stats as scipy_stats
    except ImportError:
        STATS_AVAILABLE = False

if PINGOUIN_AVAILABLE:
    try:
        import pingouin as pg
    except ImportError:
        PINGOUIN_AVAILABLE = False

if SKLEARN_AVAILABLE:
    try:
        from sklearn.decomposition import FactorAnalysis, PCA
        from sklearn.linear_model import LinearRegression
        from sklearn.metrics import r2_score
    except ImportError:
        SKLEARN_AVAILABLE = False

# 如果高级包不可用，使用基础实现
if not STATS_AVAILABLE:
    import numpy as np
    import pandas as pd


def mean(data: List[float]) -> float:
    """计算均值（基础实现）"""
    if not data:
        return 0
    return sum(data) / len(data)


def median(data: List[float]) -> float:
    """计算中位数（基础实现）"""
    if not data:
        return 0
    sorted_data = sorted(data)
    n = len(sorted_data)
    if n % 2 == 0:
        return (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
    else:
        return sorted_data[n//2]


def std(data: List[float]) -> float:
    """计算标准差（基础实现）"""
    if len(data) < 2:
        return 0
    avg = mean(data)
    variance = sum((x - avg) ** 2 for x in data) / (len(data) - 1)
    return math.sqrt(variance)


def pearson_correlation(x: List[float], y: List[float]) -> float:
    """计算皮尔逊相关系数（基础实现）"""
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


def basic_descriptive_stats(data: List[float]) -> Dict[str, float]:
    """基础描述性统计"""
    if not data:
        return {}
    
    sorted_data = sorted(data)
    n = len(data)
    
    return {
        'count': n,
        'mean': mean(data),
        'median': median(data),
        'std': std(data),
        'min': min(data) if data else 0,
        'max': max(data) if data else 0,
        'range': max(data) - min(data) if data else 0,
        'q25': sorted_data[n//4] if n > 0 else 0,
        'q75': sorted_data[3*n//4] if n > 0 else 0,
        'iqr': sorted_data[3*n//4] - sorted_data[n//4] if n > 0 else 0
    }


def advanced_descriptive_stats(data: pd.Series) -> Dict[str, Any]:
    """高级描述性统计（使用pandas + scipy）"""
    if not STATS_AVAILABLE:
        return basic_descriptive_stats(data.tolist())
    
    try:
        # 使用pandas的describe方法
        desc = data.describe()
        result = {
            'count': int(desc['count']),
            'mean': float(desc['mean']),
            'std': float(desc['std']) if not pd.isna(desc['std']) else 0,
            'min': float(desc['min']),
            'max': float(desc['max']),
            '25%': float(desc['25%']),
            '50%': float(desc['50%']),  # median
            '75%': float(desc['75%']),
            'range': float(desc['max'] - desc['min'])
        }
        
        # 添加偏度和峰度
        result['skewness'] = float(scipy_stats.skew(data.dropna()))
        result['kurtosis'] = float(scipy_stats.kurtosis(data.dropna()))
        
        return result
    except Exception:
        # 降级到基础实现
        return basic_descriptive_stats(data.dropna().tolist())


def basic_t_test(x: List[float], y: List[float]) -> Dict[str, float]:
    """基础t检验实现"""
    if len(x) < 2 or len(y) < 2:
        return {'error': '样本量不足'}
    
    mean_x, mean_y = mean(x), mean(y)
    var_x = sum((xi - mean_x)**2 for xi in x) / (len(x) - 1) if len(x) > 1 else 0
    var_y = sum((yi - mean_y)**2 for yi in y) / (len(y) - 1) if len(y) > 1 else 0
    n_x, n_y = len(x), len(y)
    
    # 合并方差
    pooled_var = ((n_x - 1) * var_x + (n_y - 1) * var_y) / (n_x + n_y - 2)
    
    # t统计量
    se = math.sqrt(pooled_var * (1/n_x + 1/n_y))
    t_stat = (mean_x - mean_y) / se if se != 0 else 0
    
    # 自由度
    df = n_x + n_y - 2
    
    # 估算p值（使用近似方法）
    p_value = 2 * (1 - min(1, abs(t_stat) / 4))  # 简化的p值估算
    
    return {
        't_statistic': t_stat,
        'p_value': p_value,
        'degrees_of_freedom': df,
        'mean_difference': mean_x - mean_y,
        'effect_size': (mean_x - mean_y) / math.sqrt(pooled_var) if pooled_var > 0 else 0  # Cohen's d
    }


def advanced_t_test(x: List[float], y: List[float]) -> Dict[str, Any]:
    """高级t检验（使用pingouin或statsmodels）"""
    if PINGOUIN_AVAILABLE:
        try:
            import pingouin as pg
            result = pg.ttest(x, y)
            return {
                't_statistic': float(result['T'].iloc[0]),
                'p_value': float(result['p-val'].iloc[0]),
                'degrees_of_freedom': float(result['dof'].iloc[0]),
                'effect_size': float(result['cohen-d'].iloc[0]) if 'cohen-d' in result.columns else 0
            }
        except Exception:
            pass  # 降级到基础实现或statsmodels
    
    if STATS_AVAILABLE:
        try:
            from scipy import stats
            t_stat, p_value = stats.ttest_ind(x, y)
            # 计算效应量 (Cohen's d)
            pooled_std = math.sqrt(((len(x)-1)*np.var(x, ddof=1) + (len(y)-1)*np.var(y, ddof=1)) /
                                  (len(x) + len(y) - 2))
            cohens_d = (np.mean(x) - np.mean(y)) / pooled_std if pooled_std != 0 else 0
            
            return {
                't_statistic': float(t_stat),
                'p_value': float(p_value),
                'degrees_of_freedom': len(x) + len(y) - 2,
                'effect_size': cohens_d
            }
        except Exception:
            pass  # 降级到基础实现
    
    # 最终降级到基础实现
    return basic_t_test(x, y)


def basic_regression_analysis(x: List[float], y: List[float]) -> Dict[str, Any]:
    """基础回归分析"""
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


def advanced_regression_analysis(x: List[float], y: List[float]) -> Dict[str, Any]:
    """高级回归分析（使用sklearn或statsmodels）"""
    if SKLEARN_AVAILABLE:
        try:
            X = np.array(x).reshape(-1, 1)
            y = np.array(y)
            
            model = LinearRegression().fit(X, y)
            y_pred = model.predict(X)
            r_squared = r2_score(y, y_pred)
            
            return {
                'slope': float(model.coef_[0]),
                'intercept': float(model.intercept_),
                'r_squared': float(r_squared),
                'regression_equation': f'y = {model.intercept_:.4f} + {model.coef_[0]:.4f}x',
                'predictions': y_pred.tolist()
            }
        except Exception:
            pass  # 降级到基础实现或statsmodels
    
    if STATS_AVAILABLE:
        try:
            X = sm.add_constant(x)  # 添加常数项
            model = sm.OLS(y, X).fit()
            
            return {
                'slope': float(model.params.iloc[1]),
                'intercept': float(model.params.iloc[0]),
                'r_squared': float(model.rsquared),
                'regression_equation': f'y = {model.params.iloc[0]:.4f} + {model.params.iloc[1]:.4f}x',
                'predictions': model.fittedvalues.tolist(),
                'model_summary': model.summary().as_text()[:500]  # 只取前500字符
            }
        except Exception:
            pass  # 降级到基础实现
    
    # 最终降级到基础实现
    return basic_regression_analysis(x, y)


def basic_factor_analysis(data: List[List[float]], n_factors: int = 2) -> Dict[str, Any]:
    """基础因子分析（降级实现）"""
    # 这里提供一个非常基础的实现，实际应用中可能需要更复杂的算法
    return {
        'error': '因子分析需要高级依赖包，当前使用基础实现',
        'n_factors_requested': n_factors,
        'data_shape': [len(data), len(data[0]) if data else 0]
    }


def advanced_factor_analysis(data: List[List[float]], n_factors: int = 2) -> Dict[str, Any]:
    """高级因子分析（使用sklearn或factor-analyzer）"""
    if SKLEARN_AVAILABLE:
        try:
            X = np.array(data)
            fa = FactorAnalysis(n_components=n_factors, random_state=42)
            factors = fa.fit_transform(X)
            
            return {
                'factors': factors.tolist(),
                'components': fa.components_.tolist(),
                'factor_variance': fa.noise_variance_.tolist() if hasattr(fa, 'noise_variance_') else [],
                'n_factors_extracted': n_factors
            }
        except Exception:
            pass  # 降级到基础实现
    
    if FACTOR_AVAILABLE:
        try:
            from factor_analyzer import FactorAnalyzer
            X = np.array(data)
            
            fa = FactorAnalyzer(n_factors=n_factors, rotation=None)
            fa.fit(X)
            
            return {
                'factors': fa.transform(X).tolist(),
                'components': fa.loadings_.tolist(),
                'eigenvalues': fa.get_eigenvalues()[0].tolist(),
                'n_factors_extracted': n_factors
            }
        except Exception:
            pass  # 降级到基础实现
    
    # 最终降级到基础实现
    return basic_factor_analysis(data, n_factors)


def main():
    parser = argparse.ArgumentParser(
        description='高级统计分析工具（支持高级依赖包，提供优雅降级）',
        epilog='示例：python advanced_statistical_analysis.py --input data.json --output results.json --analysis descriptive'
    )
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--output', '-o', default='stats_results.json', help='输出文件')
    parser.add_argument('--analysis', '-a', required=True, 
                       choices=['descriptive', 'correlation', 't_test', 'regression', 'factor'],
                       help='分析类型')
    parser.add_argument('--x-column', '-x', help='X轴数据列名')
    parser.add_argument('--y-column', '-y', help='Y轴数据列名')
    parser.add_argument('--group-column', '-g', help='分组列名（t检验）')
    parser.add_argument('--n-factors', '-f', type=int, default=2, help='因子分析的因子数')
    
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
    available_packages = {
        'statsmodels': STATS_AVAILABLE,
        'pingouin': PINGOUIN_AVAILABLE,
        'scikit-learn': SKLEARN_AVAILABLE,
        'factor-analyzer': FACTOR_AVAILABLE
    }
    
    if args.analysis == 'descriptive':
        # 描述性统计
        if args.x_column and args.x_column in data:
            column_data = data[args.x_column]
            if isinstance(column_data, list):
                series_data = pd.Series([x for x in column_data if isinstance(x, (int, float))])
                results = {
                    'variable': args.x_column,
                    'descriptive_stats': advanced_descriptive_stats(series_data),
                    'using_advanced': STATS_AVAILABLE
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
            
            if len(x_data) == len(y_data) and len(x_data) > 0:
                if STATS_AVAILABLE:
                    # 使用pandas计算相关性
                    df = pd.DataFrame({'x': x_data, 'y': y_data})
                    correlation = float(df['x'].corr(df['y']))
                else:
                    # 使用基础实现
                    correlation = pearson_correlation(x_data, y_data)
                
                results = {
                    'variables': [args.x_column, args.y_column],
                    'correlation': correlation,
                    'n_observations': len(x_data),
                    'using_advanced': STATS_AVAILABLE
                }
            else:
                results = {'error': 'X和Y列的数据长度不一致或为空'}
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
                    
                    t_test_result = advanced_t_test(group1_data, group2_data)
                    results = {
                        'groups': group_names,
                        'group1_size': len(group1_data),
                        'group2_size': len(group2_data),
                        't_test_result': t_test_result,
                        'using_advanced': PINGOUIN_AVAILABLE or STATS_AVAILABLE
                    }
                else:
                    results = {'error': '需要至少两组数据'}
            else:
                results = {'error': 'X列和分组列的数据长度不一致'}
        else:
            results = {'error': '需要指定X列和分组列名'}
    
    elif args.analysis == 'regression':
        # 回归分析
        if args.x_column and args.y_column and args.x_column in data and args.y_column in data:
            x_data = [x for x in data[args.x_column] if isinstance(x, (int, float))]
            y_data = [y for y in data[args.y_column] if isinstance(y, (int, float))]
            
            if len(x_data) == len(y_data):
                regression_result = advanced_regression_analysis(x_data, y_data)
                results = {
                    'variables': {'x': args.x_column, 'y': args.y_column},
                    'regression_result': regression_result,
                    'n_observations': len(x_data),
                    'using_advanced': SKLEARN_AVAILABLE or STATS_AVAILABLE
                }
            else:
                results = {'error': 'X和Y列的数据长度不一致'}
        else:
            results = {'error': '需要指定X和Y列名'}
    
    elif args.analysis == 'factor':
        # 因子分析
        if isinstance(data, list) and all(isinstance(row, list) for row in data):
            factor_result = advanced_factor_analysis(data, args.n_factors)
            results = {
                'factor_analysis_result': factor_result,
                'n_factors_requested': args.n_factors,
                'using_advanced': SKLEARN_AVAILABLE or FACTOR_AVAILABLE
            }
        else:
            results = {'error': '因子分析需要输入为二维数值列表'}

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'analysis_type': args.analysis,
            'input_file': args.input,
            'processing_time': round((end_time - start_time).total_seconds(), 2),
            'available_packages': available_packages
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
    print(f"  - 高级包可用: {sum(available_packages.values())}/{len(available_packages)}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()