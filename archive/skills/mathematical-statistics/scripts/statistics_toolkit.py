"""
Social Science Statistics Analysis Toolkit
完整的数理统计分析工具包
"""

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
    t_test_result = analyzer._two_sample_t_test('income', 'income', alpha=0.05)
    print("两样本t检验结果:")
    for key, value in t_test_result.items():
        print(f"  {key}: {value}")

if __name__ == "__main__":
    main()
