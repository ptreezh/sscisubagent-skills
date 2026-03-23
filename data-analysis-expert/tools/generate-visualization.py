"""
数据可视化工具
直方图、箱线图、散点图、热力图
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Optional
import io
import base64


def create_histogram(df: pd.DataFrame,
                     column: str,
                     bins: int = 30,
                     title: str = None) -> Dict:
    """
    创建直方图
    
    参数:
        df: pandas DataFrame
        column: 列名
        bins: 箱数
        title: 标题
    
    返回:
        图表数据(base64 编码)
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.hist(df[column], bins=bins, edgecolor='black', alpha=0.7)
    ax.set_xlabel(column)
    ax.set_ylabel('Frequency')
    ax.set_title(title or f'Distribution of {column}')
    ax.grid(True, alpha=0.3)
    
    # 保存为 base64
    img_data = save_plot_to_base64(fig)
    plt.close()
    
    return {
        'plot_type': 'histogram',
        'column': column,
        'image_data': img_data
    }


def create_boxplot(df: pd.DataFrame,
                   value_col: str,
                   group_col: Optional[str] = None,
                   title: str = None) -> Dict:
    """
    创建箱线图
    
    参数:
        df: pandas DataFrame
        value_col: 值列
        group_col: 分组列(可选)
        title: 标题
    
    返回:
        图表数据
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if group_col:
        sns.boxplot(x=group_col, y=value_col, data=df, ax=ax)
    else:
        ax.boxplot(df[value_col].dropna())
        ax.set_xticklabels([value_col])
    
    ax.set_title(title or f'Boxplot of {value_col}')
    ax.grid(True, alpha=0.3)
    
    img_data = save_plot_to_base64(fig)
    plt.close()
    
    return {
        'plot_type': 'boxplot',
        'value_column': value_col,
        'group_column': group_col,
        'image_data': img_data
    }


def create_scatterplot(df: pd.DataFrame,
                       x_col: str,
                       y_col: str,
                       hue_col: Optional[str] = None,
                       title: str = None) -> Dict:
    """
    创建散点图
    
    参数:
        df: pandas DataFrame
        x_col: x 轴列
        y_col: y 轴列
        hue_col: 着色列(可选)
        title: 标题
    
    返回:
        图表数据
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if hue_col:
        sns.scatterplot(x=x_col, y=y_col, hue=hue_col, data=df, ax=ax)
    else:
        sns.scatterplot(x=x_col, y=y_col, data=df, ax=ax)
    
    ax.set_title(title or f'{x_col} vs {y_col}')
    ax.grid(True, alpha=0.3)
    
    img_data = save_plot_to_base64(fig)
    plt.close()
    
    return {
        'plot_type': 'scatterplot',
        'x_column': x_col,
        'y_column': y_col,
        'hue_column': hue_col,
        'image_data': img_data
    }


def create_correlation_heatmap(df: pd.DataFrame,
                               title: str = None) -> Dict:
    """
    创建相关矩阵热力图
    
    参数:
        df: pandas DataFrame
        title: 标题
    
    返回:
        图表数据
    """
    # 计算相关矩阵
    corr_matrix = df.select_dtypes(include=[np.number]).corr()
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                center=0, ax=ax, square=True)
    ax.set_title(title or 'Correlation Matrix')
    
    img_data = save_plot_to_base64(fig)
    plt.close()
    
    return {
        'plot_type': 'correlation_heatmap',
        'correlation_matrix': corr_matrix.to_dict(),
        'image_data': img_data
    }


def save_plot_to_base64(fig) -> str:
    """
    保存图表为 base64 字符串
    
    参数:
        fig: matplotlib figure
    
    返回:
        base64 编码的字符串
    """
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight', dpi=100)
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return f"data:image/png;base64,{img_base64}"


def generate_visualizations(df: pd.DataFrame,
                            plot_types: List[str] = None) -> Dict:
    """
    生成多种可视化
    
    参数:
        df: pandas DataFrame
        plot_types: 图表类型列表
    
    返回:
        可视化结果
    """
    if plot_types is None:
        plot_types = ['histogram', 'boxplot', 'correlation_heatmap']
    
    plots = []
    
    # 数值列
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if 'histogram' in plot_types:
        for col in numeric_cols[:5]:  # 最多 5 个
            plots.append(create_histogram(df, col))
    
    if 'boxplot' in plot_types:
        for col in numeric_cols[:5]:
            plots.append(create_boxplot(df, col))
    
    if 'correlation_heatmap' in plot_types and len(numeric_cols) >= 2:
        plots.append(create_correlation_heatmap(df))
    
    return {
        'plots': plots,
        'num_plots': len(plots)
    }


if __name__ == '__main__':
    # 测试
    import numpy as np
    
    # 创建测试数据
    np.random.seed(42)
    df = pd.DataFrame({
        'a': np.random.normal(0, 1, 100),
        'b': np.random.normal(5, 2, 100),
        'c': np.random.normal(0, 1, 100)
    })
    df['d'] = df['a'] + df['c'] + np.random.normal(0, 0.5, 100)
    
    # 生成可视化
    result = generate_visualizations(df)
    
    print(f"生成 {result['num_plots']} 个图表")
    for plot in result['plots']:
        print(f"  - {plot['plot_type']}: {plot.get('column', plot.get('x_column', 'N/A'))}")
