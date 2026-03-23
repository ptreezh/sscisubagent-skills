"""
数据准备工具
数据清洗、缺失值处理、异常值检测
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple


def load_data(data: Dict) -> pd.DataFrame:
    """
    加载数据
    
    参数:
        data: 数据字典 {'format': 'csv', 'content': 'data/...'}
    
    返回:
        pandas DataFrame
    """
    format_type = data.get('format', 'csv')
    content = data.get('content', '')
    
    if format_type == 'csv':
        from io import StringIO
        df = pd.read_csv(StringIO(content))
    elif format_type == 'json':
        df = pd.read_json(content)
    else:
        raise ValueError(f"Unsupported format: {format_type}")
    
    return df


def handle_missing_values(df: pd.DataFrame, 
                          strategy: str = 'drop',
                          threshold: float = 0.5) -> Tuple[pd.DataFrame, Dict]:
    """
    处理缺失值
    
    参数:
        df: pandas DataFrame
        strategy: 处理策略 ('drop', 'mean', 'median', 'mode')
        threshold: 缺失值阈值(超过此比例则删除列)
    
    返回:
        处理后的 DataFrame 和统计信息
    """
    # 计算缺失值统计
    missing_stats = {
        'total_missing': int(df.isnull().sum().sum()),
        'missing_by_column': df.isnull().sum().to_dict(),
        'missing_percentage': (df.isnull().sum() / len(df) * 100).to_dict()
    }
    
    # 删除缺失值过多的列
    cols_to_drop = [
        col for col in df.columns 
        if missing_stats['missing_percentage'][col] > threshold * 100
    ]
    df = df.drop(columns=cols_to_drop)
    
    # 处理剩余缺失值
    if strategy == 'drop':
        df = df.dropna()
    elif strategy == 'mean':
        df = df.fillna(df.mean(numeric_only=True))
    elif strategy == 'median':
        df = df.fillna(df.median(numeric_only=True))
    elif strategy == 'mode':
        df = df.fillna(df.mode().iloc[0])
    
    missing_stats['cols_dropped'] = cols_to_drop
    missing_stats['final_missing'] = int(df.isnull().sum().sum())
    
    return df, missing_stats


def detect_outliers(df: pd.DataFrame, 
                    method: str = 'iqr',
                    threshold: float = 1.5) -> Dict:
    """
    检测异常值
    
    参数:
        df: pandas DataFrame
        method: 检测方法 ('iqr', 'zscore')
        threshold: 阈值
    
    返回:
        异常值检测结果
    """
    outliers = {}
    
    for col in df.select_dtypes(include=[np.number]).columns:
        if method == 'iqr':
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            outlier_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            outliers[col] = {
                'method': 'iqr',
                'lower_bound': float(lower_bound),
                'upper_bound': float(upper_bound),
                'num_outliers': int(outlier_mask.sum()),
                'outlier_indices': df[outlier_mask].index.tolist()
            }
        
        elif method == 'zscore':
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            outlier_mask = z_scores > threshold
            
            outliers[col] = {
                'method': 'zscore',
                'threshold': threshold,
                'num_outliers': int(outlier_mask.sum()),
                'outlier_indices': df[outlier_mask].index.tolist()
            }
    
    return {
        'total_outliers': sum(v['num_outliers'] for v in outliers.values()),
        'by_column': outliers
    }


def prepare_data(data: Dict, 
                 missing_strategy: str = 'drop',
                 outlier_method: str = 'iqr',
                 remove_outliers: bool = False) -> Dict:
    """
    完整的数据准备流程
    
    参数:
        data: 原始数据
        missing_strategy: 缺失值处理策略
        outlier_method: 异常值检测方法
        remove_outliers: 是否删除异常值
    
    返回:
        数据准备结果
    """
    # 加载数据
    df = load_data(data)
    
    # 原始统计
    original_stats = {
        'num_observations': len(df),
        'num_variables': len(df.columns),
        'columns': list(df.columns)
    }
    
    # 处理缺失值
    df, missing_stats = handle_missing_values(df, strategy=missing_strategy)
    
    # 检测异常值
    outliers = detect_outliers(df, method=outlier_method)
    
    # 删除异常值(可选)
    if remove_outliers:
        all_outlier_indices = set()
        for col_outliers in outliers['by_column'].values():
            all_outlier_indices.update(col_outliers['outlier_indices'])
        
        df = df.drop(index=list(all_outlier_indices))
    
    # 最终统计
    final_stats = {
        'num_observations': len(df),
        'num_variables': len(df.columns),
        'observations_removed': original_stats['num_observations'] - len(df)
    }
    
    return {
        'data': df.to_dict('records'),
        'original_stats': original_stats,
        'missing_stats': missing_stats,
        'outliers': outliers,
        'final_stats': final_stats,
        'status': 'success'
    }


if __name__ == '__main__':
    # 测试
    import io
    
    test_data = {
        'format': 'csv',
        'content': '''a,b,c,d
1,2,3,4
5,6,7,8
9,10,11,12
13,14,15,100'''
    }
    
    result = prepare_data(test_data)
    print(f"数据准备完成:")
    print(f"  原始观测：{result['original_stats']['num_observations']}")
    print(f"  最终观测：{result['final_stats']['num_observations']}")
    print(f"  缺失值：{result['missing_stats']['total_missing']}")
    print(f"  异常值：{result['outliers']['total_outliers']}")
