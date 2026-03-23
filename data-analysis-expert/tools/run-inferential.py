"""
推断统计检验工具
t 检验、ANOVA、卡方检验、效应量计算
"""

import pandas as pd
import numpy as np
from scipy import stats
from typing import Dict, List, Optional, Tuple


def run_t_test(df: pd.DataFrame,
               dependent_var: str,
               grouping_var: str,
               test_type: str = 'independent') -> Dict:
    """
    执行 t 检验
    
    参数:
        df: pandas DataFrame
        dependent_var: 因变量
        grouping_var: 分组变量
        test_type: 检验类型 ('independent', 'paired', 'one_sample')
    
    返回:
        t 检验结果
    """
    if test_type == 'independent':
        # 独立样本 t 检验
        groups = df[grouping_var].unique()
        group1 = df[df[grouping_var] == groups[0]][dependent_var]
        group2 = df[df[grouping_var] == groups[1]][dependent_var]
        
        t_stat, p_value = stats.ttest_ind(group1, group2, equal_var=False)
        
        # 计算效应量 (Cohen's d)
        pooled_std = np.sqrt((group1.std()**2 + group2.std()**2) / 2)
        cohens_d = (group1.mean() - group2.mean()) / pooled_std
        
    elif test_type == 'paired':
        # 配对样本 t 检验
        t_stat, p_value = stats.ttest_rel(
            df[df[grouping_var] == groups[0]][dependent_var],
            df[df[grouping_var] == groups[1]][dependent_var]
        )
        cohens_d = None  # 配对 t 检验效应量计算复杂
    
    elif test_type == 'one_sample':
        # 单样本 t 检验
        t_stat, p_value = stats.ttest_onesample(df[dependent_var], 0)
        cohens_d = None
    
    else:
        raise ValueError(f"Unknown test_type: {test_type}")
    
    return {
        'test_type': test_type,
        't_statistic': float(t_stat),
        'p_value': float(p_value),
        'cohens_d': float(cohens_d) if cohens_d else None,
        'significant': p_value < 0.05
    }


def run_anova(df: pd.DataFrame,
              dependent_var: str,
              grouping_var: str) -> Dict:
    """
    执行单因素方差分析 (ANOVA)
    
    参数:
        df: pandas DataFrame
        dependent_var: 因变量
        grouping_var: 分组变量
    
    返回:
        ANOVA 结果
    """
    groups = [group[dependent_var].values for name, group in df.groupby(grouping_var)]
    
    f_stat, p_value = stats.f_oneway(*groups)
    
    # 计算效应量 (eta-squared)
    grand_mean = df[dependent_var].mean()
    ss_total = ((df[dependent_var] - grand_mean) ** 2).sum()
    ss_between = sum([len(group) * (group[dependent_var].mean() - grand_mean) ** 2 
                      for name, group in df.groupby(grouping_var)])
    eta_squared = ss_between / ss_total
    
    return {
        'test_type': 'one_way_anova',
        'f_statistic': float(f_stat),
        'p_value': float(p_value),
        'eta_squared': float(eta_squared),
        'significant': p_value < 0.05
    }


def run_chi_square(df: pd.DataFrame,
                   var1: str,
                   var2: str) -> Dict:
    """
    执行卡方检验
    
    参数:
        df: pandas DataFrame
        var1: 变量 1
        var2: 变量 2
    
    返回:
        卡方检验结果
    """
    contingency_table = pd.crosstab(df[var1], df[var2])
    
    chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
    
    # 计算效应量 (Cramer's V)
    n = contingency_table.sum().sum()
    min_dim = min(contingency_table.shape) - 1
    cramers_v = np.sqrt(chi2 / (n * min_dim))
    
    return {
        'test_type': 'chi_square',
        'chi2_statistic': float(chi2),
        'p_value': float(p_value),
        'degrees_of_freedom': int(dof),
        'cramers_v': float(cramers_v),
        'significant': p_value < 0.05
    }


def calculate_correlation(df: pd.DataFrame,
                          var1: str,
                          var2: str,
                          method: str = 'pearson') -> Dict:
    """
    计算相关系数
    
    参数:
        df: pandas DataFrame
        var1: 变量 1
        var2: 变量 2
        method: 相关方法 ('pearson', 'spearman')
    
    返回:
        相关分析结果
    """
    if method == 'pearson':
        corr, p_value = stats.pearsonr(df[var1], df[var2])
    elif method == 'spearman':
        corr, p_value = stats.spearmanr(df[var1], df[var2])
    else:
        raise ValueError(f"Unknown method: {method}")
    
    return {
        'test_type': 'correlation',
        'method': method,
        'correlation': float(corr),
        'p_value': float(p_value),
        'significant': p_value < 0.05
    }


def run_inferential_analysis(df: pd.DataFrame,
                             analysis_config: Dict) -> Dict:
    """
    执行推断统计分析
    
    参数:
        df: pandas DataFrame
        analysis_config: 分析配置字典
    
    返回:
        推断分析结果
    """
    test_type = analysis_config.get('test_type', 't_test')
    results = {}
    
    if test_type == 't_test':
        results = run_t_test(
            df,
            analysis_config['dependent_var'],
            analysis_config['grouping_var'],
            analysis_config.get('test_type', 'independent')
        )
    
    elif test_type == 'anova':
        results = run_anova(
            df,
            analysis_config['dependent_var'],
            analysis_config['grouping_var']
        )
    
    elif test_type == 'chi_square':
        results = run_chi_square(
            df,
            analysis_config['var1'],
            analysis_config['var2']
        )
    
    elif test_type == 'correlation':
        results = calculate_correlation(
            df,
            analysis_config['var1'],
            analysis_config['var2'],
            analysis_config.get('method', 'pearson')
        )
    
    return results


def generate_inferential_report(results: Dict) -> str:
    """
    生成推断统计报告(APA 格式)
    
    参数:
        results: 推断分析结果
    
    返回:
        APA 格式报告
    """
    test_type = results['test_type']
    
    if test_type in ['independent', 'paired', 'one_sample']:
        report = f"独立样本 t 检验结果显示, "
        report += f"t = {results['t_statistic']:.2f}, "
        report += f"p = {results['p_value']:.3f}, "
        if results.get('cohens_d'):
            report += f"Cohen's d = {results['cohens_d']:.2f}, "
        report += "差异" if results['significant'] else "差异不"
        report += "显著. "
    
    elif test_type == 'one_way_anova':
        report = f"单因素方差分析结果显示, "
        report += f"F = {results['f_statistic']:.2f}, "
        report += f"p = {results['p_value']:.3f}, "
        report += f"η² = {results['eta_squared']:.2f}, "
        report += "效应" if results['significant'] else "效应不"
        report += "显著. "
    
    elif test_type == 'chi_square':
        report = f"卡方检验结果显示, "
        report += f"χ²({results['degrees_of_freedom']}) = {results['chi2_statistic']:.2f}, "
        report += f"p = {results['p_value']:.3f}, "
        report += f"Cramer's V = {results['cramers_v']:.2f}, "
        report += "关联" if results['significant'] else "关联不"
        report += "显著. "
    
    elif test_type == 'correlation':
        method = results.get('method', 'pearson')
        report = f"{method.capitalize()}相关分析显示, "
        report += f"r = {results['correlation']:.2f}, "
        report += f"p = {results['p_value']:.3f}, "
        report += "相关" if results['significant'] else "相关不"
        report += "显著. "
    
    return report


if __name__ == '__main__':
    # 测试
    import numpy as np
    
    # 创建测试数据
    np.random.seed(42)
    df = pd.DataFrame({
        'score': np.concatenate([
            np.random.normal(75, 10, 30),
            np.random.normal(80, 10, 30)
        ]),
        'group': ['A'] * 30 + ['B'] * 30
    })
    
    # 运行 t 检验
    result = run_t_test(df, 'score', 'group', 'independent')
    print(f"t 检验结果:")
    print(f"  t = {result['t_statistic']:.2f}")
    print(f"  p = {result['p_value']:.3f}")
    print(f"  d = {result['cohens_d']:.2f}")
    print(f"  显著：{result['significant']}")
    
    # 生成报告
    report = generate_inferential_report(result)
    print(f"\nAPA 格式报告:\n{report}")
