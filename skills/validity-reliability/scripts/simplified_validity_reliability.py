"""
Simplified Validity and Reliability Analysis Toolkit
使用Python标准库的简化信度效度分析工具包
"""

import statistics
import math
from typing import List, Dict, Tuple, Any

class SimplifiedValidityReliability:
    """简化信度效度分析工具包（仅使用Python标准库）"""
    
    def __init__(self):
        self.data = None
        self.results = {}
    
    def load_data(self, data_dict: Dict[str, List[float]]):
        """加载数据"""
        self.data = data_dict
        print(f"数据加载成功: {len(data_dict)} 个项目")
        return self.data
    
    def cronbach_alpha(self, items: List[str] = None) -> Dict[str, Any]:
        """计算Cronbach's Alpha（简化版）"""
        if items is None:
            items = list(self.data.keys())
        
        # 检查数据完整性
        n_items = len(items)
        if n_items < 2:
            return {'alpha': 0, 'interpretation': '项目数量不足'}
        
        # 计算每个被试的总分
        n_respondents = len(self.data[items[0]])
        total_scores = []
        
        for i in range(n_respondents):
            total = sum(self.data[item][i] for item in items)
            total_scores.append(total)
        
        # 计算总分方差
        total_variance = statistics.variance(total_scores) if len(total_scores) > 1 else 0
        
        # 计算每个项目的方差
        item_variances = []
        for item in items:
            item_values = self.data[item]
            if len(item_values) > 1:
                item_var = statistics.variance(item_values)
            else:
                item_var = 0
            item_variances.append(item_var)
        
        sum_item_variances = sum(item_variances)
        
        # 计算Cronbach's Alpha
        if total_variance == 0:
            alpha = 0
        else:
            alpha = (n_items / (n_items - 1)) * (1 - sum_item_variances / total_variance)
        
        # 确保alpha在0-1范围内
        alpha = max(0, min(1, alpha))
        
        result = {
            'alpha': alpha,
            'n_items': n_items,
            'n_respondents': n_respondents,
            'interpretation': self._interpret_reliability(alpha)
        }
        
        return result
    
    def item_total_correlation(self, items: List[str] = None) -> Dict[str, float]:
        """计算项目-总分相关（简化版）"""
        if items is None:
            items = list(self.data.keys())
        
        # 计算总分
        n_respondents = len(self.data[items[0]])
        total_scores = []
        
        for i in range(n_respondents):
            total = sum(self.data[item][i] for item in items)
            total_scores.append(total)
        
        # 计算每个项目与总分的相关
        correlations = {}
        for item in items:
            item_values = self.data[item]
            correlation = self._correlation_coefficient(item_values, total_scores)
            correlations[item] = correlation
        
        return correlations
    
    def _correlation_coefficient(self, x: List[float], y: List[float]) -> float:
        """计算相关系数"""
        if len(x) != len(y) or len(x) < 2:
            return 0
        
        n = len(x)
        mean_x = statistics.mean(x)
        mean_y = statistics.mean(y)
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        sum_sq_x = sum((xi - mean_x) ** 2 for xi in x)
        sum_sq_y = sum((yi - mean_y) ** 2 for yi in y)
        
        denominator = math.sqrt(sum_sq_x * sum_sq_y)
        
        if denominator == 0:
            return 0
        
        return numerator / denominator
    
    def split_half_reliability(self, items: List[str] = None) -> Dict[str, float]:
        """分半信度（简化版）"""
        if items is None:
            items = list(self.data.keys())
        
        n_items = len(items)
        if n_items < 4:
            return {'split_half': 0, 'interpretation': '项目数量不足'}
        
        # 将项目分成两半
        half = n_items // 2
        first_half = items[:half]
        second_half = items[half:]
        
        # 计算两半的总分
        n_respondents = len(self.data[items[0]])
        first_half_scores = []
        second_half_scores = []
        
        for i in range(n_respondents):
            first_total = sum(self.data[item][i] for item in first_half)
            second_total = sum(self.data[item][i] for item in second_half)
            first_half_scores.append(first_total)
            second_half_scores.append(second_total)
        
        # 计算两半的相关系数
        correlation = self._correlation_coefficient(first_half_scores, second_half_scores)
        
        # Spearman-Brown校正
        spearman_brown = (2 * correlation) / (1 + correlation) if correlation != -1 else 0
        
        return {
            'split_half': spearman_brown,
            'correlation': correlation,
            'interpretation': self._interpret_reliability(spearman_brown)
        }
    
    def content_validity_index(self, expert_ratings: Dict[str, List[int]]) -> Dict[str, float]:
        """内容效度指数（简化版）"""
        # CVI计算
        n_experts = len(next(iter(expert_ratings.values())))
        essential_ratings = {}
        
        for item, ratings in expert_ratings.items():
            # 假设3分表示"必要"
            essential_count = sum(1 for rating in ratings if rating >= 3)
            cvr = (essential_count - n_experts / 2) / (n_experts / 2)
            essential_ratings[item] = cvr
        
        # 量表水平CVI
        cvi_s = statistics.mean(essential_ratings.values())
        
        return {
            'cvr_by_item': essential_ratings,
            'cvi_scale': cvi_s,
            'interpretation': self._interpret_cvi(cvi_s)
        }
    
    def _interpret_reliability(self, alpha: float) -> str:
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
    
    def _interpret_cvi(self, cvi_value: float) -> str:
        """解释CVI值"""
        if cvi_value >= 0.99:
            return "优秀的内容效度"
        elif cvi_value >= 0.80:
            return "良好的内容效度"
        elif cvi_value >= 0.70:
            return "可接受的内容效度"
        else:
            return "需要改进的内容效度"
    
    def generate_report(self) -> str:
        """生成分析报告"""
        if not self.data:
            return "无数据可分析"
        
        items = list(self.data.keys())
        report = ["# 简化信度效度分析报告\n"]
        
        # 信度分析
        cronbach_result = self.cronbach_alpha(items)
        report.append("## 信度分析")
        report.append(f"- Cronbach's Alpha: {cronbach_result['alpha']:.3f}")
        report.append(f"- 项目数量: {cronbach_result['n_items']}")
        report.append(f"- 样本数量: {cronbach_result['n_respondents']}")
        report.append(f"- 信度评价: {cronbach_result['interpretation']}")
        
        # 分半信度
        split_half_result = self.split_half_reliability(items)
        report.append(f"\n- 分半信度: {split_half_result['split_half']:.3f}")
        report.append(f"- 分半信度评价: {split_half_result['interpretation']}")
        
        # 项目-总分相关
        item_total_corr = self.item_total_correlation(items)
        report.append("\n## 项目-总分相关")
        for item, corr in item_total_corr.items():
            report.append(f"- {item}: {corr:.3f}")
        
        return "\n".join(report)

# 使用示例
def main():
    """主函数示例"""
    # 创建分析器实例
    analyzer = SimplifiedValidityReliability()
    
    # 创建模拟量表数据（5个项目，10个被试）
    np = __import__('numpy')  # 动态导入numpy（如果可用）
    
    # 如果numpy不可用，使用随机数生成
    try:
        np.random.seed(42)
        data = {
            'item1': [4, 5, 3, 4, 5, 4, 3, 5, 4, 4],
            'item2': [4, 4, 4, 5, 4, 3, 4, 4, 5, 4],
            'item3': [3, 4, 5, 3, 4, 4, 5, 3, 4, 5],
            'item4': [5, 3, 4, 4, 3, 5, 4, 4, 3, 4],
            'item5': [4, 4, 3, 5, 4, 4, 3, 5, 4, 3]
        }
    except:
        # 简单的模拟数据
        data = {
            'item1': [4, 5, 3, 4, 5, 4, 3, 5, 4, 4],
            'item2': [4, 4, 4, 5, 4, 3, 4, 4, 5, 4],
            'item3': [3, 4, 5, 3, 4, 4, 5, 3, 4, 5],
            'item4': [5, 3, 4, 4, 3, 5, 4, 4, 3, 4],
            'item5': [4, 4, 3, 5, 4, 4, 3, 5, 4, 3]
        }
    
    # 加载数据
    analyzer.load_data(data)
    
    # 信度分析
    print("=== 信度分析 ===")
    cronbach_result = analyzer.cronbach_alpha()
    print(f"Cronbach's Alpha: {cronbach_result['alpha']:.3f}")
    print(f"信度评价: {cronbach_result['interpretation']}")
    
    # 分半信度
    split_half_result = analyzer.split_half_reliability()
    print(f"分半信度: {split_half_result['split_half']:.3f}")
    print(f"分半信度评价: {split_half_result['interpretation']}")
    
    # 项目-总分相关
    print("\n=== 项目-总分相关 ===")
    item_total_corr = analyzer.item_total_correlation()
    for item, corr in item_total_corr.items():
        print(f"{item}: {corr:.3f}")
    
    # 生成报告
    print("\n=== 分析报告 ===")
    report = analyzer.generate_report()
    print(report)

if __name__ == "__main__":
    main()
