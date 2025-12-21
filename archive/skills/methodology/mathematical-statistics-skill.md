# Mathematical Statistics Skill for Social Sciences

## 技能概述

数理统计技能为社会科学研究提供全面的统计分析支持，包括描述性统计、推断统计、回归分析、方差分析、因子分析等，确保研究数据分析的科学性和准确性。

## 核心功能

### 1. 描述性统计分析
- **集中趋势测量**: 均值、中位数、众数、几何平均数
- **离散程度测量**: 标准差、方差、极差、四分位距、变异系数
- **分布形态测量**: 偏度、峰度、正态性检验
- **数据可视化**: 直方图、箱线图、Q-Q图、散点图

### 2. 推断统计分析
- **参数估计**: 点估计、区间估计、置信区间
- **假设检验**: t检验、卡方检验、F检验、非参数检验
- **效应量计算**: Cohen's d、eta平方、相关系数
- **统计功效分析**: 功效计算、样本量估计

### 3. 回归分析
- **简单线性回归**: 模型拟合、假设检验、预测
- **多元线性回归**: 变量选择、多重共线性诊断
- **逻辑回归**: 二分类、多分类、有序分类
- **回归诊断**: 残差分析、影响点检测、模型验证

### 4. 方差分析
- **单因素方差分析**: 组间差异检验、事后比较
- **多因素方差分析**: 主效应、交互效应、简单效应
- **重复测量方差分析**: 球形检验、校正方法
- **协方差分析**: 控制变量影响、调整均值

### 5. 因子分析与信度分析
- **探索性因子分析**: 因子提取、因子旋转、因子得分
- **验证性因子分析**: 模型拟合、因子效度检验
- **信度分析**: 内部一致性、重测信度、评分者信度
- **效度分析**: 内容效度、结构效度、效标效度

## 程序脚本示例

### Python统计分析脚本

```python
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import FactorAnalysis
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from statsmodels.formula.api import ols
import pingouin as pg
from scipy.stats import shapiro, normaltest, anderson
import warnings
warnings.filterwarnings('ignore')

class SocialScienceStatistics:
    """社会科学统计分析工具包"""
    
    def __init__(self):
        self.data = None
        self.results = {}
        
    def load_data(self, data_path=None, data_frame=None):
        """加载数据"""
        if data_path:
            self.data = pd.read_csv(data_path)
        elif data_frame is not None:
            self.data = data_frame.copy()
        else:
            raise ValueError("请提供数据路径或DataFrame")
        
        print(f"数据加载成功: {self.data.shape[0]} 行, {self.data.shape[1]} 列")
        return self.data.head()
    
    def descriptive_statistics(self, columns=None, include_plots=True):
        """描述性统计分析"""
        if columns is None:
            columns = self.data.select_dtypes(include=[np.number]).columns.tolist()
        
        results = {}
        
        for col in columns:
            data_col = self.data[col].dropna()
            
            # 基础统计量
            desc_stats = {
                'count': len(data_col),
                'mean': data_col.mean(),
                'median': data_col.median(),
                'mode': data_col.mode().iloc[0] if not data_col.mode().empty else np.nan,
                'std': data_col.std(),
                'var': data_col.var(),
                'min': data_col.min(),
                'max': data_col.max(),
                'range': data_col.max() - data_col.min(),
                'q1': data_col.quantile(0.25),
                'q3': data_col.quantile(0.75),
                'iqr': data_col.quantile(0.75) - data_col.quantile(0.25),
                'skewness': stats.skew(data_col),
                'kurtosis': stats.kurtosis(data_col),
                'cv': data_col.std() / data_col.mean() if data_col.mean() != 0 else np.nan
            }
            
            # 正态性检验
            normality_tests = self._test_normality(data_col)
            desc_stats.update(normality_tests)
            
            results[col] = desc_stats
        
        self.results['descriptive'] = results
        
        if include_plots:
            self._create_descriptive_plots(columns)
        
        return pd.DataFrame(results).T
    
    def _test_normality(self, data):
        """正态性检验"""
        tests = {}
        
        # Shapiro-Wilk检验 (适用于小样本)
        if len(data) <= 5000:
            shapiro_stat, shapiro_p = shapiro(data)
            tests['shapiro_wilk'] = {'statistic': shapiro_stat, 'p_value': shapiro_p}
        
        # D'Agostino's K^2检验
        dagostino_stat, dagostino_p = normaltest(data)
        tests['dagostino_k2'] = {'statistic': dagostino_stat, 'p_value': dagostino_p}
        
        # Anderson-Darling检验
        anderson_result = anderson(data, dist='norm')
        tests['anderson_darling'] = {
            'statistic': anderson_result.statistic,
            'critical_values': anderson_result.critical_values,
            'significance_levels': anderson_result.significance_levels
        }
        
        return tests
    
    def _create_descriptive_plots(self, columns):
        """创建描述性统计图表"""
        fig, axes = plt.subplots(len(columns), 3, figsize=(15, 5*len(columns)))
        if len(columns) == 1:
            axes = axes.reshape(1, -1)
        
        for i, col in enumerate(columns):
            data_col = self.data[col].dropna()
            
            # 直方图
            axes[i, 0].hist(data_col, bins=30, alpha=0.7, edgecolor='black')
            axes[i, 0].set_title(f'{col} - 直方图')
            axes[i, 0].set_xlabel(col)
            axes[i, 0].set_ylabel('频数')
            
            # 箱线图
            axes[i, 1].boxplot(data_col)
            axes[i, 1].set_title(f'{col} - 箱线图')
            axes[i, 1].set_ylabel(col)
            
            # Q-Q图
            stats.probplot(data_col, dist="norm", plot=axes[i, 2])
            axes[i, 2].set_title(f'{col} - Q-Q图')
        
        plt.tight_layout()
        plt.savefig('descriptive_statistics_plots.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def hypothesis_testing(self, test_type, **kwargs):
        """假设检验"""
        if test_type == 'one_sample_t':
            return self._one_sample_t_test(**kwargs)
        elif test_type == 'two_sample_t':
            return self._two_sample_t_test(**kwargs)
        elif test_type == 'paired_t':
            return self._paired_t_test(**kwargs)
        elif test_type == 'chi_square':
            return self._chi_square_test(**kwargs)
        elif test_type == 'mann_whitney':
            return self._mann_whitney_test(**kwargs)
        elif test_type == 'wilcoxon':
            return self._wilcoxon_test(**kwargs)
        else:
            raise ValueError(f"不支持的检验类型: {test_type}")
    
    def _one_sample_t_test(self, column, population_mean, alpha=0.05):
        """单样本t检验"""
        data = self.data[column].dropna()
        t_stat, p_value = stats.ttest_1samp(data, population_mean)
        
        # 计算置信区间
        mean = data.mean()
        sem = stats.sem(data)
        ci_lower, ci_upper = stats.t.interval(1-alpha, len(data)-1, loc=mean, scale=sem)
        
        # 计算效应量 (Cohen's d)
        cohens_d = (mean - population_mean) / data.std()
        
        result = {
            'test': 'One Sample t-test',
            'sample_size': len(data),
            'sample_mean': mean,
            'population_mean': population_mean,
            't_statistic': t_stat,
            'p_value': p_value,
            'alpha': alpha,
            'significant': p_value < alpha,
            'confidence_interval': (ci_lower, ci_upper),
            'cohens_d': cohens_d,
            'effect_size_interpretation': self._interpret_cohens_d(cohens_d)
        }
        
        return result
    
    def _two_sample_t_test(self, column1, column2, equal_var=True, alpha=0.05):
        """两独立样本t检验"""
        data1 = self.data[column1].dropna()
        data2 = self.data[column2].dropna()
        
        t_stat, p_value = stats.ttest_ind(data1, data2, equal_var=equal_var)
        
        # 计算效应量 (Cohen's d)
        pooled_std = np.sqrt(((len(data1)-1)*data1.var() + (len(data2)-1)*data2.var()) / 
                            (len(data1) + len(data2) - 2))
        cohens_d = (data1.mean() - data2.mean()) / pooled_std
        
        # 计算置信区间
        mean_diff = data1.mean() - data2.mean()
        se_diff = np.sqrt(data1.var()/len(data1) + data2.var()/len(data2))
        ci_lower, ci_upper = stats.t.interval(1-alpha, len(data1)+len(data2)-2, 
                                             loc=mean_diff, scale=se_diff)
        
        result = {
            'test': 'Two Sample t-test',
            'group1_size': len(data1),
            'group2_size': len(data2),
            'group1_mean': data1.mean(),
            'group2_mean': data2.mean(),
            'mean_difference': mean_diff,
            't_statistic': t_stat,
            'p_value': p_value,
            'alpha': alpha,
            'significant': p_value < alpha,
            'confidence_interval': (ci_lower, ci_upper),
            'cohens_d': cohens_d,
            'effect_size_interpretation': self._interpret_cohens_d(cohens_d),
            'equal_variance_assumed': equal_var
        }
        
        return result
    
    def _paired_t_test(self, column1, column2, alpha=0.05):
        """配对样本t检验"""
        data1 = self.data[column1].dropna()
        data2 = self.data[column2].dropna()
        
        # 确保配对
        min_length = min(len(data1), len(data2))
        data1 = data1[:min_length]
        data2 = data2[:min_length]
        
        t_stat, p_value = stats.ttest_rel(data1, data2)
        
        # 计算效应量 (Cohen's d for paired samples)
        differences = data1 - data2
        cohens_d = differences.mean() / differences.std()
        
        # 计算置信区间
        mean_diff = differences.mean()
        se_diff = stats.sem(differences)
        ci_lower, ci_upper = stats.t.interval(1-alpha, len(differences)-1, 
                                             loc=mean_diff, scale=se_diff)
        
        result = {
            'test': 'Paired t-test',
            'sample_size': len(differences),
            'mean_difference': mean_diff,
            't_statistic': t_stat,
            'p_value': p_value,
            'alpha': alpha,
            'significant': p_value < alpha,
            'confidence_interval': (ci_lower, ci_upper),
            'cohens_d': cohens_d,
            'effect_size_interpretation': self._interpret_cohens_d(cohens_d)
        }
        
        return result
    
    def _chi_square_test(self, column1, column2, alpha=0.05):
        """卡方独立性检验"""
        contingency_table = pd.crosstab(self.data[column1], self.data[column2])
        chi2_stat, p_value, dof, expected = stats.chi2_contingency(contingency_table)
        
        # 计算Cramer's V
        n = contingency_table.sum().sum()
        cramers_v = np.sqrt(chi2_stat / (n * (min(contingency_table.shape) - 1)))
        
        result = {
            'test': 'Chi-square Test of Independence',
            'contingency_table': contingency_table,
            'chi2_statistic': chi2_stat,
            'p_value': p_value,
            'degrees_of_freedom': dof,
            'alpha': alpha,
            'significant': p_value < alpha,
            'cramers_v': cramers_v,
            'effect_size_interpretation': self._interpret_cramers_v(cramers_v)
        }
        
        return result
    
    def _mann_whitney_test(self, column1, column2, alpha=0.05):
        """Mann-Whitney U检验"""
        data1 = self.data[column1].dropna()
        data2 = self.data[column2].dropna()
        
        u_stat, p_value = stats.mannwhitneyu(data1, data2, alternative='two-sided')
        
        # 计算效应量 (r)
        z_score = stats.norm.ppf(1 - p_value/2)
        n1, n2 = len(data1), len(data2)
        r = z_score / np.sqrt(n1 + n2)
        
        result = {
            'test': 'Mann-Whitney U Test',
            'group1_size': n1,
            'group2_size': n2,
            'group1_median': data1.median(),
            'group2_median': data2.median(),
            'u_statistic': u_stat,
            'p_value': p_value,
            'alpha': alpha,
            'significant': p_value < alpha,
            'effect_size_r': r,
            'effect_size_interpretation': self._interpret_effect_size_r(r)
        }
        
        return result
    
    def _wilcoxon_test(self, column1, column2, alpha=0.05):
        """Wilcoxon符号秩检验"""
        data1 = self.data[column1].dropna()
        data2 = self.data[column2].dropna()
        
        # 确保配对
        min_length = min(len(data1), len(data2))
        data1 = data1[:min_length]
        data2 = data2[:min_length]
        
        stat, p_value = stats.wilcoxon(data1, data2)
        
        # 计算效应量 (r)
        z_score = stats.norm.ppf(1 - p_value/2)
        n = len(data1)
        r = z_score / np.sqrt(n)
        
        result = {
            'test': 'Wilcoxon Signed-Rank Test',
            'sample_size': n,
            'statistic': stat,
            'p_value': p_value,
            'alpha': alpha,
            'significant': p_value < alpha,
            'effect_size_r': r,
            'effect_size_interpretation': self._interpret_effect_size_r(r)
        }
        
        return result
    
    def _interpret_cohens_d(self, d):
        """解释Cohen's d效应量"""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "极小效应"
        elif abs_d < 0.5:
            return "小效应"
        elif abs_d < 0.8:
            return "中等效应"
        else:
            return "大效应"
    
    def _interpret_cramers_v(self, v):
        """解释Cramer's V效应量"""
        if v < 0.1:
            return "极小关联"
        elif v < 0.3:
            return "小关联"
        elif v < 0.5:
            return "中等关联"
        else:
            return "大关联"
    
    def _interpret_effect_size_r(self, r):
        """解释r效应量"""
        abs_r = abs(r)
        if abs_r < 0.1:
            return "极小效应"
        elif abs_r < 0.3:
            return "小效应"
        elif abs_r < 0.5:
            return "中等效应"
        else:
            return "大效应"
    
    def correlation_analysis(self, columns, method='pearson', alpha=0.05):
        """相关性分析"""
        data_subset = self.data[columns].dropna()
        
        if method == 'pearson':
            corr_matrix, p_values = self._pearson_correlation(data_subset)
        elif method == 'spearman':
            corr_matrix, p_values = self._spearman_correlation(data_subset)
        else:
            raise ValueError("方法必须是 'pearson' 或 'spearman'")
        
        # 创建相关性热图
        self._create_correlation_heatmap(corr_matrix, p_values, alpha, method)
        
        result = {
            'correlation_matrix': corr_matrix,
            'p_values': p_values,
            'method': method,
            'alpha': alpha,
            'significant_correlations': self._find_significant_correlations(corr_matrix, p_values, alpha)
        }
        
        return result
    
    def _pearson_correlation(self, data):
        """Pearson相关性分析"""
        n = len(data)
        corr_matrix = data.corr(method='pearson')
        
        # 计算p值
        p_values = pd.DataFrame(index=corr_matrix.index, columns=corr_matrix.columns)
        
        for i, col1 in enumerate(data.columns):
            for j, col2 in enumerate(data.columns):
                if i <= j:
                    _, p_val = stats.pearsonr(data[col1], data[col2])
                    p_values.iloc[i, j] = p_val
                    p_values.iloc[j, i] = p_val
        
        return corr_matrix, p_values
    
    def _spearman_correlation(self, data):
        """Spearman相关性分析"""
        n = len(data)
        corr_matrix = data.corr(method='spearman')
        
        # 计算p值
        p_values = pd.DataFrame(index=corr_matrix.index, columns=corr_matrix.columns)
        
        for i, col1 in enumerate(data.columns):
            for j, col2 in enumerate(data.columns):
                if i <= j:
                    _, p_val = stats.spearmanr(data[col1], data[col2])
                    p_values.iloc[i, j] = p_val
                    p_values.iloc[j, i] = p_val
        
        return corr_matrix, p_values
    
    def _create_correlation_heatmap(self, corr_matrix, p_values, alpha, method):
        """创建相关性热图"""
        # 创建掩码，只显示下三角
        mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
        
        # 创建图形
        plt.figure(figsize=(10, 8))
        
        # 绘制热图
        sns.heatmap(corr_matrix, mask=mask, annot=True, cmap='coolwarm', center=0,
                   square=True, fmt='.2f', cbar_kws={"shrink": .8})
        
        # 标记显著相关性
        for i in range(len(corr_matrix)):
            for j in range(len(corr_matrix.columns)):
                if i < j and p_values.iloc[i, j] < alpha:
                    plt.text(j+0.5, i+0.5, '*', ha='center', va='center', 
                            color='black', fontsize=12, fontweight='bold')
        
        plt.title(f'{method.capitalize()} 相关性矩阵 (* p < {alpha})')
        plt.tight_layout()
        plt.savefig(f'{method}_correlation_heatmap.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _find_significant_correlations(self, corr_matrix, p_values, alpha):
        """查找显著相关性"""
        significant = []
        
        for i in range(len(corr_matrix)):
            for j in range(i+1, len(corr_matrix.columns)):
                if p_values.iloc[i, j] < alpha:
                    significant.append({
                        'variable1': corr_matrix.index[i],
                        'variable2': corr_matrix.columns[j],
                        'correlation': corr_matrix.iloc[i, j],
                        'p_value': p_values.iloc[i, j],
                        'interpretation': self._interpret_correlation(corr_matrix.iloc[i, j])
                    })
        
        return significant
    
    def _interpret_correlation(self, r):
        """解释相关系数"""
        abs_r = abs(r)
        strength = ""
        if abs_r < 0.1:
            strength = "极弱"
        elif abs_r < 0.3:
            strength = "弱"
        elif abs_r < 0.5:
            strength = "中等"
        elif abs_r < 0.7:
            strength = "强"
        else:
            strength = "极强"
        
        direction = "正相关" if r > 0 else "负相关"
        return f"{strength}{direction}"
    
    def regression_analysis(self, dependent_var, independent_vars, 
                          regression_type='linear', alpha=0.05):
        """回归分析"""
        X = self.data[independent_vars]
        y = self.data[dependent_var]
        
        # 处理缺失值
        complete_cases = ~(X.isnull().any(axis=1) | y.isnull())
        X = X[complete_cases]
        y = y[complete_cases]
        
        if regression_type == 'linear':
            return self._linear_regression(X, y, alpha)
        elif regression_type == 'logistic':
            return self._logistic_regression(X, y, alpha)
        else:
            raise ValueError("回归类型必须是 'linear' 或 'logistic'")
    
    def _linear_regression(self, X, y, alpha):
        """线性回归分析"""
        # 添加常数项
        X_with_const = sm.add_constant(X)
        
        # 拟合模型
        model = sm.OLS(y, X_with_const).fit()
        
        # 计算VIF（多重共线性诊断）
        vif = self._calculate_vif(X)
        
        # 残差分析
        residual_analysis = self._analyze_residuals(model, y)
        
        result = {
            'model_type': 'Linear Regression',
            'model_summary': model.summary().as_text(),
            'coefficients': model.params.to_dict(),
            'standard_errors': model.bse.to_dict(),
            't_values': model.tvalues.to_dict(),
            'p_values': model.pvalues.to_dict(),
            'confidence_intervals': model.conf_int(alpha).to_dict(),
            'r_squared': model.rsquared,
            'adj_r_squared': model.rsquared_adj,
            'f_statistic': model.fvalue,
            'f_p_value': model.f_pvalue,
            'aic': model.aic,
            'bic': model.bic,
            'vif': vif,
            'residual_analysis': residual_analysis,
            'assumptions_check': self._check_regression_assumptions(model, y)
        }
        
        return result
    
    def _logistic_regression(self, X, y, alpha):
        """逻辑回归分析"""
        # 添加常数项
        X_with_const = sm.add_constant(X)
        
        # 拟合模型
        model = sm.Logit(y, X_with_const).fit(disp=0)
        
        # 计算VIF
        vif = self._calculate_vif(X)
        
        # 模型拟合优度
        pseudo_r2 = model.prsquared
        llr_pvalue = model.llr_pvalue
        
        # 预测和分类准确率
        y_pred_proba = model.predict(X_with_const)
        y_pred = (y_pred_proba >= 0.5).astype(int)
        accuracy = (y_pred == y).mean()
        
        result = {
            'model_type': 'Logistic Regression',
            'model_summary': model.summary().as_text(),
            'coefficients': model.params.to_dict(),
            'standard_errors': model.bse.to_dict(),
            'z_values': model.tvalues.to_dict(),
            'p_values': model.pvalues.to_dict(),
            'confidence_intervals': model.conf_int(alpha).to_dict(),
            'pseudo_r_squared': pseudo_r2,
            'llr_p_value': llr_pvalue,
            'aic': model.aic,
            'bic': model.bic,
            'vif': vif,
            'accuracy': accuracy,
            'predicted_probabilities': y_pred_proba
        }
        
        return result
    
    def _calculate_vif(self, X):
        """计算方差膨胀因子"""
        from statsmodels.stats.outliers_influence import variance_inflation_factor
        
        vif_data = pd.DataFrame()
        vif_data["variable"] = X.columns
        vif_data["VIF"] = [variance_inflation_factor(X.values, i) 
                          for i in range(X.shape[1])]
        
        # 添加解释
        vif_data["interpretation"] = vif_data["VIF"].apply(self._interpret_vif)
        
        return vif_data
    
    def _interpret_vif(self, vif):
        """解释VIF值"""
        if vif < 2:
            return "无多重共线性问题"
        elif vif < 5:
            return "轻微多重共线性"
        elif vif < 10:
            return "中等多重共线性"
        else:
            return "严重多重共线性"
    
    def _analyze_residuals(self, model, y):
        """残差分析"""
        residuals = model.resid
        fitted_values = model.fittedvalues
        
        # 残差正态性检验
        shapiro_stat, shapiro_p = stats.shapiro(residuals)
        
        # 残差独立性检验 (Durbin-Watson)
        from statsmodels.stats.stattools import durbin_watson
        dw_stat = durbin_watson(residuals)
        
        # 同方差性检验
        from statsmodels.stats.diagnostic import het_breuschpagan
        bp_stat, bp_p, _, _ = het_breuschpagan(residuals, model.model.exog)
        
        # 创建残差图
        self._create_residual_plots(residuals, fitted_values)
        
        return {
            'shapiro_wilk': {'statistic': shapiro_stat, 'p_value': shapiro_p},
            'durbin_watson': dw_stat,
            'breusch_pagan': {'statistic': bp_stat, 'p_value': bp_p},
            'residual_mean': residuals.mean(),
            'residual_std': residuals.std()
        }
    
    def _create_residual_plots(self, residuals, fitted_values):
        """创建残差图"""
        fig, axes = plt.subplots(2, 2, figsize=(12, 10))
        
        # 残差vs拟合值图
        axes[0, 0].scatter(fitted_values, residuals, alpha=0.6)
        axes[0, 0].axhline(y=0, color='r', linestyle='--')
        axes[0, 0].set_xlabel('拟合值')
        axes[0, 0].set_ylabel('残差')
        axes[0, 0].set_title('残差 vs 拟合值')
        
        # 残差Q-Q图
        stats.probplot(residuals, dist="norm", plot=axes[0, 1])
        axes[0, 1].set_title('残差 Q-Q图')
        
        # 残差直方图
        axes[1, 0].hist(residuals, bins=30, alpha=0.7, edgecolor='black')
        axes[1, 0].set_xlabel('残差')
        axes[1, 0].set_ylabel('频数')
        axes[1, 0].set_title('残差分布')
        
        # 残差vs杠杆值图
        influence = model.get_influence()
        leverage = influence.hat_matrix_diag
        axes[1, 1].scatter(leverage, residuals, alpha=0.6)
        axes[1, 1].set_xlabel('杠杆值')
        axes[1, 1].set_ylabel('残差')
        axes[1, 1].set_title('残差 vs 杠杆值')
        
        plt.tight_layout()
        plt.savefig('residual_analysis.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _check_regression_assumptions(self, model, y):
        """检查回归假设"""
        residuals = model.resid
        
        assumptions = {
            'linearity': "需要通过残差vs拟合值图检查",
            'independence': f"Durbin-Watson统计量: {self._analyze_residuals(model, y)['durbin_watson']:.3f}",
            'normality': f"Shapiro-Wilk检验: p = {self._analyze_residuals(model, y)['shapiro_wilk']['p_value']:.4f}",
            'homoscedasticity': f"Breusch-Pagan检验: p = {self._analyze_residuals(model, y)['breusch_pagan']['p_value']:.4f}",
            'multicollinearity': "见VIF分析结果"
        }
        
        return assumptions
    
    def anova_analysis(self, dependent_var, factor_vars, alpha=0.05):
        """方差分析"""
        if len(factor_vars) == 1:
            return self._one_way_anova(dependent_var, factor_vars[0], alpha)
        elif len(factor_vars) == 2:
            return self._two_way_anova(dependent_var, factor_vars, alpha)
        else:
            return self._n_way_anova(dependent_var, factor_vars, alpha)
    
    def _one_way_anova(self, dependent_var, factor_var, alpha):
        """单因素方差分析"""
        # 移除缺失值
        data_clean = self.data[[dependent_var, factor_var]].dropna()
        
        # 执行方差分析
        formula = f'{dependent_var} ~ C({factor_var})'
        model = ols(formula, data=data_clean).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        
        # 计算效应量 (eta squared)
        ss_total = anova_table['sum_sq'].sum()
        ss_between = anova_table.loc[f'C({factor_var})', 'sum_sq']
        eta_squared = ss_between / ss_total
        
        # 事后检验 (Tukey HSD)
        from statsmodels.stats.multicomp import pairwise_tukeyhsd
        tukey_result = pairwise_tukeyhsd(data_clean[dependent_var], data_clean[factor_var])
        
        result = {
            'test': 'One-way ANOVA',
            'dependent_variable': dependent_var,
            'factor': factor_var,
            'anova_table': anova_table,
            'eta_squared': eta_squared,
            'effect_size_interpretation': self._interpret_eta_squared(eta_squared),
            'tukey_hsd': tukey_result._results_table,
            'group_descriptives': data_clean.groupby(factor_var)[dependent_var].describe()
        }
        
        return result
    
    def _two_way_anova(self, dependent_var, factor_vars, alpha):
        """两因素方差分析"""
        # 移除缺失值
        vars_to_include = [dependent_var] + factor_vars
        data_clean = self.data[vars_to_include].dropna()
        
        # 执行方差分析
        formula = f'{dependent_var} ~ C({factor_vars[0]}) + C({factor_vars[1]}) + C({factor_vars[0]}):C({factor_vars[1]})'
        model = ols(formula, data=data_clean).fit()
        anova_table = sm.stats.anova_lm(model, typ=2)
        
        # 计算效应量
        ss_total = anova_table['sum_sq'].sum()
        eta_squared = {}
        for effect in anova_table.index:
            if effect != 'Residual':
                ss_effect = anova_table.loc[effect, 'sum_sq']
                eta_squared[effect] = ss_effect / ss_total
        
        result = {
            'test': 'Two-way ANOVA',
            'dependent_variable': dependent_var,
            'factors': factor_vars,
            'anova_table': anova_table,
            'eta_squared': eta_squared,
            'interaction_effect': f'C({factor_vars[0]}):C({factor_vars[1]})' in anova_table.index
        }
        
        return result
    
    def _interpret_eta_squared(self, eta_sq):
        """解释eta平方效应量"""
        if eta_sq < 0.01:
            return "极小效应"
        elif eta_sq < 0.06:
            return "小效应"
        elif eta_sq < 0.14:
            return "中等效应"
        else:
            return "大效应"
    
    def factor_analysis(self, variables, n_factors=None, rotation='varimax'):
        """因子分析"""
        # 数据准备
        data_subset = self.data[variables].dropna()
        
        # 标准化数据
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data_subset)
        
        # KMO和Bartlett检验
        kmo_result = self._kmo_test(data_scaled)
        bartlett_result = self._bartlett_test(data_scaled)
        
        # 确定因子数量
        if n_factors is None:
            n_factors = self._determine_factors(data_scaled)
        
        # 执行因子分析
        fa = FactorAnalysis(n_components=n_factors, rotation=rotation, random_state=42)
        fa.fit(data_scaled)
        
        # 因子载荷矩阵
        loadings = pd.DataFrame(
            fa.components_.T,
            index=variables,
            columns=[f'Factor_{i+1}' for i in range(n_factors)]
        )
        
        # 因子得分
        factor_scores = fa.transform(data_scaled)
        
        result = {
            'kmo_test': kmo_result,
            'bartlett_test': bartlett_result,
            'n_factors': n_factors,
            'rotation': rotation,
            'loadings': loadings,
            'factor_scores': factor_scores,
            'explained_variance': fa.explained_variance_,
            'explained_variance_ratio': fa.explained_variance_ratio_,
            'communalities': self._calculate_communalities(loadings)
        }
        
        return result
    
    def _kmo_test(self, data):
        """KMO检验"""
        from factor_analyzer import calculate_kmo
        kmo_all, kmo_model = calculate_kmo(data)
        
        return {
            'kmo_overall': kmo_model,
            'kmo_individual': kmo_all,
            'interpretation': self._interpret_kmo(kmo_model)
        }
    
    def _bartlett_test(self, data):
        """Bartlett球形检验"""
        from factor_analyzer import calculate_bartlett_sphericity
        chi_square, p_value = calculate_bartlett_sphericity(data)
        
        return {
            'chi_square': chi_square,
            'p_value': p_value,
            'significant': p_value < 0.05
        }
    
    def _interpret_kmo(self, kmo_value):
        """解释KMO值"""
        if kmo_value < 0.5:
            return "不适合进行因子分析"
        elif kmo_value < 0.6:
            return "不太适合"
        elif kmo_value < 0.7:
            return "中等程度适合"
        elif kmo_value < 0.8:
            return "适合"
        elif kmo_value < 0.9:
            return "很适合"
        else:
            return "非常适合"
    
    def _determine_factors(self, data):
        """确定因子数量"""
        # 特征值大于1准则
        from factor_analyzer import FactorAnalyzer
        fa = FactorAnalyzer(rotation=None)
        fa.fit(data)
        ev, _ = fa.get_eigenvalues()
        n_factors_eigen = sum(ev > 1)
        
        # 碎石图准则
        plt.figure(figsize=(8, 6))
        plt.plot(range(1, len(ev) + 1), ev, 'bo-')
        plt.axhline(y=1, color='r', linestyle='--')
        plt.xlabel('因子数量')
        plt.ylabel('特征值')
        plt.title('碎石图')
        plt.grid(True)
        plt.savefig('scree_plot.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        return max(1, n_factors_eigen)
    
    def _calculate_communalities(self, loadings):
        """计算共同度"""
        communalities = (loadings ** 2).sum(axis=1)
        return communalities.to_dict()
    
    def reliability_analysis(self, items):
        """信度分析"""
        # 移除缺失值
        data_clean = self.data[items].dropna()
        
        # Cronbach's Alpha
        cronbach_alpha = self._calculate_cronbach_alpha(data_clean)
        
        # 分半信度
        split_half = self._calculate_split_half_reliability(data_clean)
        
        # 项目统计
        item_stats = self._calculate_item_statistics(data_clean)
        
        # 删除项后的Alpha
        alpha_if_deleted = self._calculate_alpha_if_deleted(data_clean)
        
        result = {
            'cronbach_alpha': cronbach_alpha,
            'split_half_reliability': split_half,
            'item_statistics': item_stats,
            'alpha_if_deleted': alpha_if_deleted,
            'interpretation': self._interpret_reliability(cronbach_alpha)
        }
        
        return result
    
    def _calculate_cronbach_alpha(self, data):
        """计算Cronbach's Alpha"""
        from pingouin import cronbach_alpha
        alpha, _ = cronbach_alpha(data)
        return alpha
    
    def _calculate_split_half_reliability(self, data):
        """计算分半信度"""
        n_items = data.shape[1]
        half = n_items // 2
        
        first_half = data.iloc[:, :half]
        second_half = data.iloc[:, half:]
        
        # 计算两半的总分
        first_half_score = first_half.sum(axis=1)
        second_half_score = second_half.sum(axis=1)
        
        # 计算相关系数
        correlation, _ = stats.pearsonr(first_half_score, second_half_score)
        
        # Spearman-Brown校正
        spearman_brown = (2 * correlation) / (1 + correlation)
        
        return spearman_brown
    
    def _calculate_item_statistics(self, data):
        """计算项目统计"""
        item_stats = {}
        
        for item in data.columns:
            item_data = data[item]
            
            stats_dict = {
                'mean': item_data.mean(),
                'std': item_data.std(),
                'item_total_correlation': self._item_total_correlation(data, item),
                'skewness': stats.skew(item_data),
                'kurtosis': stats.kurtosis(item_data)
            }
            
            item_stats[item] = stats_dict
        
        return pd.DataFrame(item_stats).T
    
    def _item_total_correlation(self, data, item):
        """计算项目-总分相关"""
        total_scores = data.drop(columns=[item]).sum(axis=1)
        correlation, _ = stats.pearsonr(data[item], total_scores)
        return correlation
    
    def _calculate_alpha_if_deleted(self, data):
        """计算删除某项后的Alpha"""
        alpha_if_deleted = {}
        
        for item in data.columns:
            data_without_item = data.drop(columns=[item])
            alpha = self._calculate_cronbach_alpha(data_without_item)
            alpha_if_deleted[item] = alpha
        
        return alpha_if_deleted
    
    def _interpret_reliability(self, alpha):
        """解释信度系数"""
        if alpha < 0.6:
            return "不可接受"
        elif alpha < 0.7:
            return "可接受但需改进"
        elif alpha < 0.8:
            return "可接受"
        elif alpha < 0.9:
            return "良好"
        else:
            return "优秀"
    
    def power_analysis(self, test_type, effect_size=None, sample_size=None, 
                      power=None, alpha=0.05, **kwargs):
        """统计功效分析"""
        from statsmodels.stats.power import (TTestIndPower, TTestPower, 
                                           GofChisquarePower, FTestAnovaPower)
        
        if test_type == 'two_sample_t':
            power_analysis = TTestIndPower()
        elif test_type == 'one_sample_t':
            power_analysis = TTestPower()
        elif test_type == 'chi_square':
            power_analysis = GofChisquarePower()
        elif test_type == 'anova':
            power_analysis = FTestAnovaPower()
        else:
            raise ValueError("不支持的检验类型")
        
        # 计算缺失的参数
        if effect_size is None:
            effect_size = power_analysis.solve_power(sample_size=sample_size, 
                                                   power=power, alpha=alpha, **kwargs)
        elif sample_size is None:
            sample_size = power_analysis.solve_power(effect_size=effect_size, 
                                                   power=power, alpha=alpha, **kwargs)
        elif power is None:
            power = power_analysis.solve_power(effect_size=effect_size, 
                                             sample_size=sample_size, alpha=alpha, **kwargs)
        
        # 创建功效曲线
        self._create_power_curve(power_analysis, test_type, alpha)
        
        result = {
            'test_type': test_type,
            'effect_size': effect_size,
            'sample_size': sample_size,
            'power': power,
            'alpha': alpha,
            'effect_size_interpretation': self._interpret_effect_size(effect_size, test_type)
        }
        
        return result
    
    def _create_power_curve(self, power_analysis, test_type, alpha):
        """创建功效曲线"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # 效应量 vs 样本量
        effect_sizes = np.linspace(0.1, 1.0, 50)
        sample_sizes = np.arange(10, 200, 5)
        
        for power in [0.7, 0.8, 0.9]:
            n_needed = []
            for es in effect_sizes:
                if test_type == 'two_sample_t':
                    n = power_analysis.solve_power(effect_size=es, power=power, alpha=alpha)
                else:
                    n = power_analysis.solve_power(effect_size=es, power=power, alpha=alpha, 
                                                 nobs=None)
                n_needed.append(n)
            
            axes[0].plot(effect_sizes, n_needed, label=f'Power = {power}')
        
        axes[0].set_xlabel('效应量')
        axes[0].set_ylabel('所需样本量')
        axes[0].set_title('效应量 vs 样本量')
        axes[0].legend()
        axes[0].grid(True)
        
        # 功效 vs 样本量
        for es in [0.2, 0.5, 0.8]:
            powers = []
            for n in sample_sizes:
                if test_type == 'two_sample_t':
                    power = power_analysis.power(effect_size=es, nobs1=n, alpha=alpha)
                else:
                    power = power_analysis.power(effect_size=es, nobs=n, alpha=alpha)
                powers.append(power)
            
            axes[1].plot(sample_sizes, powers, label=f'Effect Size = {es}')
        
        axes[1].set_xlabel('样本量')
        axes[1].set_ylabel('统计功效')
        axes[1].set_title('功效 vs 样本量')
        axes[1].legend()
        axes[1].grid(True)
        
        # 功效 vs 效应量
        for n in [30, 50, 100]:
            powers = []
            for es in effect_sizes:
                if test_type == 'two_sample_t':
                    power = power_analysis.power(effect_size=es, nobs1=n, alpha=alpha)
                else:
                    power = power_analysis.power(effect_size=es, nobs=n, alpha=alpha)
                powers.append(power)
            
            axes[2].plot(effect_sizes, powers, label=f'N = {n}')
        
        axes[2].set_xlabel('效应量')
        axes[2].set_ylabel('统计功效')
        axes[2].set_title('功效 vs 效应量')
        axes[2].legend()
        axes[2].grid(True)
        
        plt.tight_layout()
        plt.savefig('power_analysis_curves.png', dpi=300, bbox_inches='tight')
        plt.show()
    
    def _interpret_effect_size(self, effect_size, test_type):
        """解释效应量"""
        if test_type in ['two_sample_t', 'one_sample_t']:
            return self._interpret_cohens_d(effect_size)
        elif test_type == 'chi_square':
            return self._interpret_cramers_v(effect_size)
        elif test_type == 'anova':
            return self._interpret_eta_squared(effect_size)
        else:
            return "需要具体解释"
    
    def generate_report(self, output_file='statistical_analysis_report.md'):
        """生成统计分析报告"""
        report = ["# 社会科学统计分析报告\n"]
        
        # 描述性统计
        if 'descriptive' in self.results:
            report.append("## 描述性统计分析")
            desc_df = pd.DataFrame(self.results['descriptive']).T
            report.append(desc_df.to_markdown())
            report.append("")
        
        # 假设检验结果
        for test_name, test_result in self.results.items():
            if test_name != 'descriptive' and isinstance(test_result, dict):
                report.append(f"## {test_name.replace('_', ' ').title()}")
                
                for key, value in test_result.items():
                    if isinstance(value, dict):
                        report.append(f"### {key}")
                        for sub_key, sub_value in value.items():
                            report.append(f"- {sub_key}: {sub_value}")
                    else:
                        report.append(f"- {key}: {value}")
                
                report.append("")
        
        # 保存报告
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(report))
        
        print(f"统计分析报告已保存到 {output_file}")

# 使用示例
def main():
    """主函数示例"""
    # 创建模拟数据
    np.random.seed(42)
    n = 200
    
    data = pd.DataFrame({
        'age': np.random.normal(35, 10, n),
        'income': np.random.normal(50000, 15000, n),
        'education_years': np.random.normal(16, 3, n),
        'satisfaction': np.random.normal(7, 2, n),
        'gender': np.random.choice(['Male', 'Female'], n),
        'group': np.random.choice(['A', 'B', 'C'], n),
        'treatment': np.random.choice([0, 1], n)
    })
    
    # 确保数据合理性
    data['age'] = np.clip(data['age'], 18, 80)
    data['income'] = np.clip(data['income'], 20000, 100000)
    data['education_years'] = np.clip(data['education_years'], 8, 25)
    data['satisfaction'] = np.clip(data['satisfaction'], 1, 10)
    
    # 创建分析器实例
    analyzer = SocialScienceStatistics()
    analyzer.load_data(data_frame=data)
    
    # 1. 描述性统计分析
    print("=== 描述性统计分析 ===")
    desc_results = analyzer.descriptive_statistics(['age', 'income', 'education_years', 'satisfaction'])
    print(desc_results)
    
    # 2. 假设检验
    print("\n=== 假设检验 ===")
    
    # 两样本t检验
    male_income = data[data['gender'] == 'Male']['income']
    female_income = data[data['gender'] == 'Female']['income']
    t_test_result = analyzer._two_sample_t_test('income', 'income', alpha=0.05)
    print("两样本t检验结果:")
    for key, value in t_test_result.items():
        print(f"  {key}: {value}")
    
    # 3. 相关性分析
    print("\n=== 相关性分析 ===")
    corr_results = analyzer.correlation_analysis(['age', 'income', 'education_years', 'satisfaction'])
    print("显著相关性:")
    for corr in corr_results['significant_correlations']:
        print(f"  {corr['variable1']} - {corr['variable2']}: {corr['correlation']:.3f} ({corr['interpretation']})")
    
    # 4. 回归分析
    print("\n=== 回归分析 ===")
    regression_results = analyzer.regression_analysis('satisfaction', ['age', 'income', 'education_years'])
    print(f"R²: {regression_results['r_squared']:.3f}")
    print(f"调整R²: {regression_results['adj_r_squared']:.3f}")
    print(f"F统计量: {regression_results['f_statistic']:.3f} (p = {regression_results['f_p_value']:.4f})")
    
    # 5. 方差分析
    print("\n=== 方差分析 ===")
    anova_results = analyzer.anova_analysis('satisfaction', ['group'])
    print(f"效应量 (eta²): {anova_results['eta_squared']:.3f} ({anova_results['effect_size_interpretation']})")
    
    # 6. 信度分析
    print("\n=== 信度分析 ===")
    # 创建多项目量表数据
    scale_items = [f'item_{i}' for i in range(1, 6)]
    scale_data = pd.DataFrame({
        item: np.random.normal(5, 1.5, n) for item in scale_items
    })
    scale_data = np.clip(scale_data, 1, 7)
    analyzer.data = pd.concat([analyzer.data, scale_data], axis=1)
    
    reliability_results = analyzer.reliability_analysis(scale_items)
    print(f"Cronbach's Alpha: {reliability_results['cronbach_alpha']:.3f} ({reliability_results['interpretation']})")
    
    # 7. 功效分析
    print("\n=== 功效分析 ===")
    power_results = analyzer.power_analysis('two_sample_t', effect_size=0.5, power=0.8, alpha=0.05)
    print(f"所需样本量: {power_results['sample_size']:.0f}")
    
    # 生成完整报告
    analyzer.generate_report()
    
    print("\n统计分析完成！报告和图表已保存。")

if __name__ == "__main__":
    main()
```