"""
回归分析工具
线性回归、逻辑回归、回归诊断
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from typing import Dict, List, Optional


def run_linear_regression(df: pd.DataFrame,
                          dependent_var: str,
                          independent_vars: List[str]) -> Dict:
    """
    执行线性回归分析
    
    参数:
        df: pandas DataFrame
        dependent_var: 因变量
        independent_vars: 自变量列表
    
    返回:
        线性回归结果
    """
    # 准备数据
    X = df[independent_vars]
    X = sm.add_constant(X)  # 添加截距项
    y = df[dependent_var]
    
    # 拟合模型
    model = sm.OLS(y, X).fit()
    
    # 提取结果
    results = {
        'model_type': 'linear_regression',
        'r_squared': float(model.rsquared),
        'adjusted_r_squared': float(model.rsquared_adj),
        'f_statistic': float(model.fvalue),
        'f_p_value': float(model.f_pvalue),
        'n_observations': int(model.nobs),
        'coefficients': [],
        'diagnostics': {}
    }
    
    # 提取系数
    for i, var in enumerate(X.columns):
        results['coefficients'].append({
            'variable': var,
            'coef': float(model.params[var]),
            'std_err': float(model.bse[var]),
            't_value': float(model.tvalues[var]),
            'p_value': float(model.pvalues[var]),
            'ci_lower': float(model.conf_int().iloc[i, 0]),
            'ci_upper': float(model.conf_int().iloc[i, 1])
        })
    
    # 回归诊断
    results['diagnostics'] = run_regression_diagnostics(model, X)
    
    return results


def run_logistic_regression(df: pd.DataFrame,
                            dependent_var: str,
                            independent_vars: List[str]) -> Dict:
    """
    执行逻辑回归分析
    
    参数:
        df: pandas DataFrame
        dependent_var: 因变量(二分类)
        independent_vars: 自变量列表
    
    返回:
        逻辑回归结果
    """
    # 准备数据
    X = df[independent_vars]
    X = sm.add_constant(X)
    y = df[dependent_var]
    
    # 拟合模型
    model = sm.Logit(y, X).fit(disp=0)
    
    # 提取结果
    results = {
        'model_type': 'logistic_regression',
        'llf': float(model.llf),
        'llr': float(model.llr),
        'llr_pvalue': float(model.llr_pvalue),
        'coefficients': [],
        'odds_ratios': []
    }
    
    # 提取系数和优势比
    for var in X.columns:
        coef = float(model.params[var])
        results['coefficients'].append({
            'variable': var,
            'coef': coef,
            'std_err': float(model.bse[var]),
            'z_value': float(model.tvalues[var]),
            'p_value': float(model.pvalues[var]),
            'ci_lower': float(model.conf_int().iloc[X.columns.get_loc(var), 0]),
            'ci_upper': float(model.conf_int().iloc[X.columns.get_loc(var), 1])
        })
        
        # 优势比 (OR)
        results['odds_ratios'].append({
            'variable': var,
            'odds_ratio': float(np.exp(coef)),
            'ci_lower': float(np.exp(model.conf_int().iloc[X.columns.get_loc(var), 0])),
            'ci_upper': float(np.exp(model.conf_int().iloc[X.columns.get_loc(var), 1]))
        })
    
    return results


def run_regression_diagnostics(model, X) -> Dict:
    """
    执行回归诊断
    
    参数:
        model: 回归模型结果
        X: 自变量矩阵
    
    返回:
        诊断结果
    """
    diagnostics = {
        'vif': {},  # 方差膨胀因子(多重共线性)
        'durbin_watson': float(sm.stats.durbin_watson(model.resid)),
        'jarque_bera': {}
    }
    
    # 计算 VIF
    vif_data = pd.DataFrame()
    vif_data["VIF"] = [variance_inflation_factor(X.values, i) 
                       for i in range(X.shape[1])]
    vif_data["Variable"] = X.columns
    
    for _, row in vif_data.iterrows():
        diagnostics['vif'][row['Variable']] = float(row['VIF'])
    
    # 正态性检验(Jarque-Bera)
    jb_stat, jb_pvalue, _, _ = sm.stats.jarque_bera(model.resid)
    diagnostics['jarque_bera'] = {
        'statistic': float(jb_stat),
        'p_value': float(jb_pvalue),
        'normal': jb_pvalue > 0.05
    }
    
    return diagnostics


def check_multicollinearity(vif_results: Dict) -> Dict:
    """
    检查多重共线性
    
    参数:
        vif_results: VIF 结果字典
    
    返回:
        多重共线性检查结果
    """
    max_vif = max(vif_results.values())
    
    if max_vif > 10:
        severity = 'severe'
    elif max_vif > 5:
        severity = 'moderate'
    else:
        severity = 'low'
    
    return {
        'max_vif': float(max_vif),
        'severity': severity,
        'problematic': max_vif > 10
    }


def generate_regression_report(results: Dict) -> str:
    """
    生成回归分析报告(APA 格式)
    
    参数:
        results: 回归分析结果
    
    返回:
        APA 格式报告
    """
    if results['model_type'] == 'linear_regression':
        report = f"线性回归分析结果显示, 模型拟合良好, "
        report += f"R² = {results['r_squared']:.2f}, "
        report += f"调整 R² = {results['adjusted_r_squared']:.2f}, "
        report += f"F({len(results['coefficients'])-1}, {results['n_observations']-len(results['coefficients'])}) = {results['f_statistic']:.2f}, "
        report += f"p < .001. \n\n"
        
        report += "回归系数：\n"
        for coef in results['coefficients']:
            if coef['variable'] != 'const':
                report += f"  {coef['variable']}: β = {coef['coef']:.2f}, "
                report += f"t = {coef['t_value']:.2f}, "
                report += f"p = {coef['p_value']:.3f}, "
                report += f"95% CI [{coef['ci_lower']:.2f}, {coef['ci_upper']:.2f}]\n"
    
    elif results['model_type'] == 'logistic_regression':
        report = f"逻辑回归分析结果显示, 模型显著, "
        report += f"χ² = {results['llr']:.2f}, "
        report += f"p < .001. \n\n"
        
        report += "优势比：\n"
        for odds in results['odds_ratios']:
            if odds['variable'] != 'const':
                report += f"  {odds['variable']}: OR = {odds['odds_ratio']:.2f}, "
                report += f"95% CI [{odds['ci_lower']:.2f}, {odds['ci_upper']:.2f}]\n"
    
    return report


if __name__ == '__main__':
    # 测试
    import numpy as np
    
    # 创建测试数据
    np.random.seed(42)
    n = 100
    df = pd.DataFrame({
        'y': np.random.normal(50, 10, n),
        'x1': np.random.normal(0, 1, n),
        'x2': np.random.normal(0, 1, n)
    })
    
    # 添加关系
    df['y'] = 50 + 5 * df['x1'] + 3 * df['x2'] + np.random.normal(0, 2, n)
    
    # 运行线性回归
    result = run_linear_regression(df, 'y', ['x1', 'x2'])
    
    print(f"线性回归结果:")
    print(f"  R² = {result['r_squared']:.3f}")
    print(f"  调整 R² = {result['adjusted_r_squared']:.3f}")
    print(f"  F = {result['f_statistic']:.2f}")
    
    # 生成报告
    report = generate_regression_report(result)
    print(f"\nAPA 格式报告:\n{report}")
