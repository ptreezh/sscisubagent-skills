"""
描述统计计算工具
集中趋势、离散程度、分布形态
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict


def calculate_central_tendency(df: pd.DataFrame) -> Dict:
    """
    计算集中趋势指标
    
    参数:
        df: pandas DataFrame
    
    返回:
        集中趋势指标字典
    """
    central_tendency = {}
    
    for col in df.select_dtypes(include=[np.number]).columns:
        central_tendency[col] = {
            'mean': float(df[col].mean()),
            'median': float(df[col].median()),
            'mode': float(df[col].mode().iloc[0]) if len(df[col].mode()) > 0 else None
        }
    
    return central_tendency


def calculate_dispersion(df: pd.DataFrame) -> Dict:
    """
    计算离散程度指标
    
    参数:
        df: pandas DataFrame
    
    返回:
        离散程度指标字典
    """
    dispersion = {}
    
    for col in df.select_dtypes(include=[np.number]).columns:
        dispersion[col] = {
            'std': float(df[col].std()),
            'variance': float(df[col].var()),
            'range': float(df[col].max() - df[col].min()),
            'min': float(df[col].min()),
            'max': float(df[col].max()),
            'q1': float(df[col].quantile(0.25)),
            'q3': float(df[col].quantile(0.75)),
            'iqr': float(df[col].quantile(0.75) - df[col].quantile(0.25))
        }
    
    return dispersion


def calculate_distribution(df: pd.DataFrame) -> Dict:
    """
    计算分布形态指标
    
    参数:
        df: pandas DataFrame
    
    返回:
        分布形态指标字典
    """
    distribution = {}
    
    for col in df.select_dtypes(include=[np.number]).columns:
        distribution[col] = {
            'skewness': float(stats.skew(df[col])),
            'kurtosis': float(stats.kurtosis(df[col]))
        }
    
    return distribution


def calculate_descriptive_stats(df: pd.DataFrame) -> Dict:
    """
    计算完整的描述统计
    
    参数:
        df: pandas DataFrame
    
    返回:
        描述统计结果
    """
    return {
        'central_tendency': calculate_central_tendency(df),
        'dispersion': calculate_dispersion(df),
        'distribution': calculate_distribution(df),
        'num_observations': len(df),
        'num_variables': len(df.columns)
    }


def generate_descriptive_report(descriptive_stats: Dict) -> str:
    """
    生成描述统计报告
    
    参数:
        descriptive_stats: 描述统计结果
    
    返回:
        报告文本
    """
    report = "# 描述统计报告\n\n"
    
    report += "## 集中趋势\n\n"
    for var, stats_data in descriptive_stats['central_tendency'].items():
        report += f"**{var}**: 均值={stats_data['mean']:.2f}, "
        report += f"中位数={stats_data['median']:.2f}, "
        report += f"众数={stats_data['mode']:.2f}\n"
    
    report += "\n## 离散程度\n\n"
    for var, stats_data in descriptive_stats['dispersion'].items():
        report += f"**{var}**: 标准差={stats_data['std']:.2f}, "
        report += f"方差={stats_data['variance']:.2f}, "
        report += f"极差={stats_data['range']:.2f}\n"
    
    report += "\n## 分布形态\n\n"
    for var, stats_data in descriptive_stats['distribution'].items():
        report += f"**{var}**: 偏度={stats_data['skewness']:.2f}, "
        report += f"峰度={stats_data['kurtosis']:.2f}\n"
    
    return report


if __name__ == '__main__':
    # 测试
    import pandas as pd
    import numpy as np
    
    # 创建测试数据
    np.random.seed(42)
    df = pd.DataFrame({
        'a': np.random.normal(0, 1, 100),
        'b': np.random.normal(5, 2, 100),
        'c': np.random.exponential(1, 100)
    })
    
    # 计算描述统计
    result = calculate_descriptive_stats(df)
    
    print("描述统计结果:")
    print(f"  观测数：{result['num_observations']}")
    print(f"  变量数：{result['num_variables']}")
    
    # 生成报告
    report = generate_descriptive_report(result)
    print("\n报告:")
    print(report)
