"""
Validity and Reliability Analysis Toolkit
信度效度分析工具包
"""

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import FactorAnalysis
from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity, calculate_kmo
import pingouin as pg
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')

class ValidityReliabilityAnalyzer:
    """信度效度分析器"""
    
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
    
    def reliability_analysis(self, items, alpha=0.05):
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
        
        # McDonald's Omega
        omega = self._calculate_omega(data_clean)
        
        result = {
            'cronbach_alpha': cronbach_alpha,
            'omega': omega,
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
    
    def _calculate_omega(self, data):
        """计算McDonald's Omega"""
        # 使用因子分析计算Omega
        fa = FactorAnalyzer(n_factors=1, rotation=None)
        fa.fit(data)
        
        loadings = fa.loadings_.flatten()
        loadings_sq = loadings ** 2
        error_variances = 1 - loadings_sq
        
        omega = np.sum(loadings_sq) / (np.sum(loadings_sq) + np.sum(error_variances))
        return omega
    
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
                'kurtosis': stats.kurtosis(item_data),
                'difficulty': item_data.mean() / item_data.max() if item_data.max() > 0 else 0
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
    
    def construct_validity_analysis(self, items, n_factors=None, rotation='varimax'):
        """构念效度分析"""
        # 数据准备
        data_subset = self.data[items].dropna()
        
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
            index=items,
            columns=[f'Factor_{i+1}' for i in range(n_factors)]
        )
        
        # 因子得分
        factor_scores = fa.transform(data_scaled)
        
        # 收敛效度和区分效度
        validity_metrics = self._calculate_validity_metrics(data_scaled, loadings)
        
        result = {
            'kmo_test': kmo_result,
            'bartlett_test': bartlett_result,
            'n_factors': n_factors,
            'rotation': rotation,
            'loadings': loadings,
            'factor_scores': factor_scores,
            'explained_variance': fa.explained_variance_,
            'explained_variance_ratio': fa.explained_variance_ratio_,
            'communalities': self._calculate_communalities(loadings),
            'validity_metrics': validity_metrics
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
        
        # 碎石图
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
    
    def _calculate_validity_metrics(self, data, loadings):
        """计算效度指标"""
        # 收敛效度 (AVE)
        n_factors = loadings.shape[1]
        ave_values = {}
        
        for i in range(n_factors):
            factor_items = loadings.iloc[:, i]
            factor_loadings_sq = factor_items ** 2
            ave = np.sum(factor_loadings_sq) / len(factor_loadings_sq)
            ave_values[f'Factor_{i+1}'] = ave
        
        # 区分效度 (Fornell-Larcker准则)
        factor_correlations = np.corrcoef(data.T)
        
        return {
            'convergent_validity': ave_values,
            'discriminant_validity': factor_correlations,
            'composite_reliability': self._calculate_composite_reliability(loadings)
        }
    
    def _calculate_composite_reliability(self, loadings):
        """计算组合信度"""
        n_factors = loadings.shape[1]
        cr_values = {}
        
        for i in range(n_factors):
            factor_loadings = loadings.iloc[:, i]
            loadings_sq = factor_loadings ** 2
            sum_loadings_sq = np.sum(loadings_sq)
            sum_error_variances = np.sum(1 - loadings_sq)
            
            cr = sum_loadings_sq / (sum_loadings_sq + sum_error_variances)
            cr_values[f'Factor_{i+1}'] = cr
        
        return cr_values
    
    def content_validity_analysis(self, expert_ratings):
        """内容效度分析"""
        """
        expert_ratings: DataFrame，行为专家，列为项目
        """
        # 计算内容效度比 (CVR)
        n_experts = len(expert_ratings)
        essential_ratings = (expert_ratings == 3).sum()  # 假设3分表示"必要"
        cvr = (essential_ratings - n_experts/2) / (n_experts/2)
        
        # 计算内容效度指数 (CVI)
        cvi_i = (expert_ratings >= 3).sum() / n_experts  # 项目水平CVI
        cvi_s = cvr.mean()  # 量表水平CVI
        
        result = {
            'content_validity_ratio': cvr,
            'cvi_item': cvi_i,
            'cvi_scale': cvi_s,
            'interpretation': self._interpret_cvi(cvi_s)
        }
        
        return result
    
    def _interpret_cvi(self, cvi_value):
        """解释CVI值"""
        if cvi_value >= 0.99:
            return "优秀的内容效度"
        elif cvi_value >= 0.80:
            return "良好的内容效度"
        elif cvi_value >= 0.70:
            return "可接受的内容效度"
        else:
            return "需要改进的内容效度"
    
    def criterion_validity_analysis(self, scale_scores, criterion_measures):
        """效标效度分析"""
        """
        scale_scores: 量表总分
        criterion_measures: 效标测量
        """
        correlations = {}
        
        for criterion in criterion_measures.columns:
            corr, p_value = stats.pearsonr(scale_scores, criterion_measures[criterion])
            correlations[criterion] = {
                'correlation': corr,
                'p_value': p_value,
                'significant': p_value < 0.05,
                'interpretation': self._interpret_correlation(corr)
            }
        
        return correlations
    
    def _interpret_correlation(self, r):
        """解释相关系数"""
        abs_r = abs(r)
        if abs_r < 0.1:
            return "极弱相关"
        elif abs_r < 0.3:
            return "弱相关"
        elif abs_r < 0.5:
            return "中等相关"
        elif abs_r < 0.7:
            return "强相关"
        else:
            return "极强相关"
    
    def generate_report(self, output_file='validity_reliability_report.md'):
        """生成分析报告"""
        report = ["# 信度效度分析报告\n"]
        
        for test_name, test_result in self.results.items():
            if isinstance(test_result, dict):
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
        
        print(f"信度效度分析报告已保存到 {output_file}")

# 使用示例
def main():
    """主函数示例"""
    # 创建模拟量表数据
    np.random.seed(42)
    n = 300
    
    # 6个项目的量表
    scale_data = pd.DataFrame({
        'item1': np.random.normal(4, 1, n),
        'item2': np.random.normal(4.2, 1.1, n),
        'item3': np.random.normal(3.8, 0.9, n),
        'item4': np.random.normal(4.1, 1.2, n),
        'item5': np.random.normal(3.9, 1.0, n),
        'item6': np.random.normal(4.3, 1.1, n)
    })
    
    # 确保数据在合理范围内（1-5分李克特量表）
    for col in scale_data.columns:
        scale_data[col] = np.clip(scale_data[col], 1, 5)
    
    # 创建分析器实例
    analyzer = ValidityReliabilityAnalyzer()
    analyzer.load_data(data_frame=scale_data)
    
    # 1. 信度分析
    print("=== 信度分析 ===")
    reliability_results = analyzer.reliability_analysis(scale_data.columns.tolist())
    print(f"Cronbach's Alpha: {reliability_results['cronbach_alpha']:.3f}")
    print(f"McDonald's Omega: {reliability_results['omega']:.3f}")
    print(f"分半信度: {reliability_results['split_half_reliability']:.3f}")
    print(f"信度评价: {reliability_results['interpretation']}")
    
    # 2. 构念效度分析
    print("\n=== 构念效度分析 ===")
    validity_results = analyzer.construct_validity_analysis(scale_data.columns.tolist())
    print(f"KMO值: {validity_results['kmo_test']['kmo_overall']:.3f}")
    print(f"KMO评价: {validity_results['kmo_test']['interpretation']}")
    print(f"因子数量: {validity_results['n_factors']}")
    
    # 3. 专家评分（模拟）
    print("\n=== 内容效度分析 ===")
    expert_ratings = pd.DataFrame({
        'item1': np.random.choice([1, 2, 3], size=5, p=[0.1, 0.2, 0.7]),
        'item2': np.random.choice([1, 2, 3], size=5, p=[0.1, 0.3, 0.6]),
        'item3': np.random.choice([1, 2, 3], size=5, p=[0.2, 0.2, 0.6]),
        'item4': np.random.choice([1, 2, 3], size=5, p=[0.1, 0.2, 0.7]),
        'item5': np.random.choice([1, 2, 3], size=5, p=[0.1, 0.3, 0.6]),
        'item6': np.random.choice([1, 2, 3], size=5, p=[0.1, 0.2, 0.7])
    })
    
    content_validity = analyzer.content_validity_analysis(expert_ratings)
    print(f"内容效度指数 (CVI): {content_validity['cvi_scale']:.3f}")
    print(f"内容效度评价: {content_validity['interpretation']}")
    
    # 4. 效标效度（模拟）
    print("\n=== 效标效度分析 ===")
    scale_scores = scale_data.sum(axis=1)
    criterion_measures = pd.DataFrame({
        'job_performance': np.random.normal(3.5, 0.8, n),
        'job_satisfaction': np.random.normal(3.8, 0.7, n),
        'turnover_intention': np.random.normal(2.5, 0.9, n)
    })
    
    criterion_validity = analyzer.criterion_validity_analysis(scale_scores, criterion_measures)
    for criterion, results in criterion_validity.items():
        print(f"{criterion}: r = {results['correlation']:.3f}, p = {results['p_value']:.3f} ({results['interpretation']})")
    
    # 生成完整报告
    analyzer.results = {
        'reliability_analysis': reliability_results,
        'construct_validity': validity_results,
        'content_validity': content_validity,
        'criterion_validity': criterion_validity
    }
    analyzer.generate_report()
    
    print("\n信度效度分析完成！报告已保存。")

if __name__ == "__main__":
    main()
