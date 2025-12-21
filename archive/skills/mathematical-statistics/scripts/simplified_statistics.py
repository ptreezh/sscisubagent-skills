"""
Simplified Statistics Toolkit for Claude Code Skills
使用Python标准库的简化统计工具包
"""

import statistics
import math
from typing import List, Dict, Tuple, Any
import random

class SimplifiedStatistics:
    """简化统计分析工具包（仅使用Python标准库）"""
    
    def __init__(self):
        self.data = None
        self.results = {}
    
    def load_data(self, data_list: List[float] = None, data_dict: Dict[str, List[float]] = None):
        """加载数据"""
        if data_list:
            self.data = {'values': data_list}
        elif data_dict:
            self.data = data_dict
        else:
            raise ValueError("请提供数据列表或数据字典")
        
        print(f"数据加载成功")
        return self.data
    
    def descriptive_statistics(self, column: str = 'values') -> Dict[str, float]:
        """描述性统计分析"""
        if column not in self.data:
            raise ValueError(f"列 '{column}' 不存在")
        
        data_values = self.data[column]
        n = len(data_values)
        
        if n == 0:
            return {}
        
        # 基础统计量
        mean_val = statistics.mean(data_values)
        median_val = statistics.median(data_values)
        
        try:
            mode_val = statistics.mode(data_values)
        except statistics.StatisticsError:
            mode_val = None
        
        stdev_val = statistics.stdev(data_values) if n > 1 else 0
        variance_val = statistics.variance(data_values) if n > 1 else 0
        
        min_val = min(data_values)
        max_val = max(data_values)
        range_val = max_val - min_val
        
        # 分位数
        sorted_data = sorted(data_values)
        q1_index = int(n * 0.25)
        q3_index = int(n * 0.75)
        q1_val = sorted_data[q1_index]
        q3_val = sorted_data[q3_index]
        iqr_val = q3_val - q1_val
        
        # 变异系数
        cv_val = stdev_val / mean_val if mean_val != 0 else 0
        
        result = {
            'count': n,
            'mean': mean_val,
            'median': median_val,
            'mode': mode_val,
            'std': stdev_val,
            'var': variance_val,
            'min': min_val,
            'max': max_val,
            'range': range_val,
            'q1': q1_val,
            'q3': q3_val,
            'iqr': iqr_val,
            'cv': cv_val
        }
        
        return result
    
    def t_test_one_sample(self, column: str, population_mean: float, alpha: float = 0.05) -> Dict[str, Any]:
        """单样本t检验（简化版）"""
        if column not in self.data:
            raise ValueError(f"列 '{column}' 不存在")
        
        data_values = self.data[column]
        n = len(data_values)
        
        if n < 2:
            raise ValueError("样本量至少为2")
        
        mean_val = statistics.mean(data_values)
        stdev_val = statistics.stdev(data_values)
        
        # t统计量
        t_stat = (mean_val - population_mean) / (stdev_val / math.sqrt(n))
        
        # 简化的p值计算（仅用于演示）
        # 实际应用中应该使用scipy.stats.t.cdf
        abs_t = abs(t_stat)
        if abs_t > 2.576:
            p_value = 0.01
        elif abs_t > 1.96:
            p_value = 0.05
        elif abs_t > 1.645:
            p_value = 0.1
        else:
            p_value = 0.2
        
        # 置信区间
        se = stdev_val / math.sqrt(n)
        t_critical = 1.96  # 简化，实际应该查t分布表
        margin_error = t_critical * se
        ci_lower = mean_val - margin_error
        ci_upper = mean_val + margin_error
        
        # 效应量 (Cohen's d)
        cohens_d = (mean_val - population_mean) / stdev_val
        
        result = {
            'test': 'One Sample t-test (Simplified)',
            'sample_size': n,
            'sample_mean': mean_val,
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
    
    def correlation_analysis(self, col1: str, col2: str) -> Dict[str, float]:
        """相关分析（简化版）"""
        if col1 not in self.data or col2 not in self.data:
            raise ValueError(f"列 '{col1}' 或 '{col2}' 不存在")
        
        x_values = self.data[col1]
        y_values = self.data[col2]
        
        if len(x_values) != len(y_values):
            raise ValueError("两列数据长度不一致")
        
        n = len(x_values)
        if n < 2:
            return {'correlation': 0, 'interpretation': '数据不足'}
        
        # 计算皮尔逊相关系数
        mean_x = statistics.mean(x_values)
        mean_y = statistics.mean(y_values)
        
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
        sum_sq_x = sum((x - mean_x) ** 2 for x in x_values)
        sum_sq_y = sum((y - mean_y) ** 2 for y in y_values)
        
        denominator = math.sqrt(sum_sq_x * sum_sq_y)
        
        if denominator == 0:
            correlation = 0
        else:
            correlation = numerator / denominator
        
        result = {
            'correlation': correlation,
            'interpretation': self._interpret_correlation(correlation)
        }
        
        return result
    
    def _interpret_cohens_d(self, d: float) -> str:
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
    
    def _interpret_correlation(self, r: float) -> str:
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
    
    def generate_summary_report(self) -> str:
        """生成分析报告"""
        report = ["# 简化统计分析报告\n"]
        
        for column in self.data.keys():
            if column == 'values':
                desc_stats = self.descriptive_statistics(column)
                report.append(f"## 描述性统计")
                for key, value in desc_stats.items():
                    report.append(f"- {key}: {value:.3f}" if isinstance(value, float) else f"- {key}: {value}")
                
                # 单样本t检验示例
                t_test_result = self.t_test_one_sample(column, 0)
                report.append(f"\n## 单样本t检验 (与0比较)")
                for key, value in t_test_result.items():
                    if key not in ['confidence_interval']:
                        report.append(f"- {key}: {value}")
                    else:
                        report.append(f"- {key}: ({value[0]:.3f}, {value[1]:.3f})")
                report.append("")
        
        return "\n".join(report)

# 使用示例
def main():
    """主函数示例"""
    # 创建分析器实例
    analyzer = SimplifiedStatistics()
    
    # 创建测试数据
    test_data = [25, 30, 35, 40, 45, 50, 55, 60, 65, 70]
    
    # 加载数据
    analyzer.load_data(data_list=test_data)
    
    # 描述性统计
    print("=== 描述性统计分析 ===")
    desc_results = analyzer.descriptive_statistics()
    for key, value in desc_results.items():
        print(f"{key}: {value:.3f}" if isinstance(value, float) else f"{key}: {value}")
    
    # 单样本t检验
    print("\n=== 单样本t检验 ===")
    t_test_result = analyzer.t_test_one_sample('values', 40)
    for key, value in t_test_result.items():
        if key not in ['confidence_interval']:
            print(f"{key}: {value}")
        else:
            print(f"{key}: ({value[0]:.3f}, {value[1]:.3f})")
    
    # 生成报告
    print("\n=== 分析报告 ===")
    report = analyzer.generate_summary_report()
    print(report)

if __name__ == "__main__":
    main()
