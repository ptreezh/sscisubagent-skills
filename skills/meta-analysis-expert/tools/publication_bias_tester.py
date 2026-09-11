#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
元分析专家 - 发表偏倚检测工具
Publication Bias Tester for Meta-Analysis

功能:
- 漏斗图分析
- Egger检验
- Begg检验
- Trim-and-fill方法
- Fail-safe N计算
- 发表偏倚报告生成

作者: Meta-Analysis Expert v5.0.0
创建时间: 2026-03-15
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from pathlib import Path
import json


@dataclass
class PublicationBiasResult:
    """发表偏倚检测结果"""
    test_name: str
    statistic: float
    p_value: float
    interpretation: str
    evidence_of_bias: bool
    
    def to_dict(self) -> Dict:
        return {
            "test_name": self.test_name,
            "statistic": round(self.statistic, 4),
            "p_value": round(self.p_value, 4),
            "interpretation": self.interpretation,
            "evidence_of_bias": self.evidence_of_bias
        }


class PublicationBiasTester:
    """发表偏倚检测器"""
    
    def __init__(self):
        pass
    
    def egger_test(
        self,
        effect_sizes: List[float],
        standard_errors: List[float]
    ) -> PublicationBiasResult:
        """
        Egger回归检验
        
        原理：如果不存在发表偏倚，效应量应与精度无关。
        Egger检验通过回归标准误与效应量来检测不对称性。
        
        回归: ES/SSE = a + b × (1/SSE)
        
        如果截距a显著不为零，提示存在发表偏倚。
        """
        n = len(effect_sizes)
        
        if n < 3:
            return PublicationBiasResult(
                test_name="Egger Test",
                statistic=0,
                p_value=1.0,
                interpretation="Insufficient studies for Egger test (need ≥3)",
                evidence_of_bias=False
            )
        
        # 计算标准化效应量和精度倒数
        # SSE = ES / SE, precision = 1/SE
        y = [es / se for es, se in zip(effect_sizes, standard_errors)]
        x = [1 / se for se in standard_errors]
        
        # 线性回归: y = a + b*x
        n_points = len(x)
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi**2 for xi in x)
        
        # 斜率和截距
        denominator = n_points * sum_x2 - sum_x**2
        if denominator == 0:
            return PublicationBiasResult(
                test_name="Egger Test",
                statistic=0,
                p_value=1.0,
                interpretation="Cannot compute - collinear data",
                evidence_of_bias=False
            )
        
        slope = (n_points * sum_xy - sum_x * sum_y) / denominator
        intercept = (sum_y - slope * sum_x) / n_points
        
        # 截距的标准误
        se_intercept = math.sqrt(
            sum((yi - intercept - slope * xi)**2 for xi, yi in zip(x, y)) /
            (n_points - 2) *
            sum_x2 / denominator
        )
        
        # t检验
        t_stat = intercept / se_intercept if se_intercept > 0 else 0
        
        # p值 (双尾t检验，df = n-2)
        df = n_points - 2
        p_value = self._t_to_p(t_stat, df)
        
        # 解释
        if p_value < 0.05:
            interpretation = f"Significant asymmetry detected (p={p_value:.3f}). Evidence of publication bias."
            evidence = True
        else:
            interpretation = f"No significant asymmetry (p={p_value:.3f}). Little evidence of publication bias."
            evidence = False
        
        return PublicationBiasResult(
            test_name="Egger Test",
            statistic=t_stat,
            p_value=p_value,
            interpretation=interpretation,
            evidence_of_bias=evidence
        )
    
    def begg_test(
        self,
        effect_sizes: List[float],
        variances: List[float]
    ) -> PublicationBiasResult:
        """
        Begg秩相关检验
        
        原理：如果不存在发表偏倚，效应量与方差应该无关。
        使用Kendall's tau秩相关检验。
        """
        import itertools
        
        n = len(effect_sizes)
        
        if n < 4:
            return PublicationBiasResult(
                test_name="Begg Test",
                statistic=0,
                p_value=1.0,
                interpretation="Insufficient studies for Begg test (need ≥4)",
                evidence_of_bias=False
            )
        
        # 计算标准化效应量
        # 使用固定效应加权
        weights = [1/v for v in variances]
        sum_w = sum(weights)
        weighted_mean = sum(w * es for w, es in zip(weights, effect_sizes)) / sum_w
        
        # 标准化效应量
        adjusted_es = [(es - weighted_mean) / math.sqrt(v) for es, v in zip(effect_sizes, variances)]
        
        # 方差的秩
        variance_ranks = self._rank(variances)
        es_ranks = self._rank(adjusted_es)
        
        # 计算Kendall's tau
        concordant = 0
        discordant = 0
        
        for i in range(n):
            for j in range(i + 1, n):
                # 检查一致性
                var_diff = variance_ranks[i] - variance_ranks[j]
                es_diff = es_ranks[i] - es_ranks[j]
                
                if var_diff * es_diff > 0:
                    concordant += 1
                elif var_diff * es_diff < 0:
                    discordant += 1
        
        n_pairs = n * (n - 1) / 2
        tau = (concordant - discordant) / n_pairs if n_pairs > 0 else 0
        
        # 连续性校正的z检验
        z = (tau * (n - 1)) / math.sqrt(2 * (2 * n + 5) / 9)
        
        # p值
        p_value = 2 * (1 - self._normal_cdf(abs(z)))
        
        # 解释
        if p_value < 0.05:
            interpretation = f"Significant rank correlation (tau={tau:.3f}, p={p_value:.3f}). Evidence of publication bias."
            evidence = True
        else:
            interpretation = f"No significant rank correlation (tau={tau:.3f}, p={p_value:.3f}). Little evidence of publication bias."
            evidence = False
        
        return PublicationBiasResult(
            test_name="Begg Test",
            statistic=z,
            p_value=p_value,
            interpretation=interpretation,
            evidence_of_bias=evidence
        )
    
    def fail_safe_n(
        self,
        effect_sizes: List[float],
        variances: List[float],
        alpha: float = 0.05
    ) -> Dict:
        """
        Fail-safe N (Rosenthal方法)
        
        计算需要多少个"无效"研究才能使元分析结果不再显著。
        """
        n = len(effect_sizes)
        k = n
        
        # 计算总Z值
        weights = [1/v for v in variances]
        sum_w = sum(weights)
        weighted_mean = sum(w * es for w, es in zip(weights, effect_sizes)) / sum_w
        
        # 总Z值
        z_sum = weighted_mean * math.sqrt(sum_w)
        
        # 临界Z值
        z_critical = 1.96 if alpha == 0.05 else 2.576
        
        # Fail-safe N
        # N = (k * Z_sum² / Z_critical²) - k
        if z_sum > z_critical:
            n_fs = int((k * z_sum**2 / z_critical**2) - k)
        else:
            n_fs = 0
        
        # 解释
        # 常用标准: N_fs > 5k + 10 认为稳健
        threshold = 5 * k + 10
        robust = n_fs > threshold
        
        return {
            "fail_safe_n": n_fs,
            "total_z": round(z_sum, 3),
            "critical_z": z_critical,
            "robustness_threshold": threshold,
            "is_robust": robust,
            "interpretation": f"Need {n_fs} null studies to nullify the effect. " + 
                            ("Result is robust." if robust else "Result may not be robust.")
        }
    
    def trim_and_fill(
        self,
        effect_sizes: List[float],
        variances: List[float],
        max_iter: int = 50
    ) -> Dict:
        """
        Trim-and-fill方法 (Duval & Tweedie)
        
        估计并填补缺失的研究，校正发表偏倚。
        """
        n = len(effect_sizes)
        
        # 按效应量排序
        sorted_data = sorted(zip(effect_sizes, variances), key=lambda x: x[0])
        sorted_es = [x[0] for x in sorted_data]
        sorted_var = [x[1] for x in sorted_data]
        
        # 计算加权中位数
        weights = [1/v for v in sorted_var]
        sum_w = sum(weights)
        weighted_median = sum(w * es for w, es in zip(weights, sorted_es)) / sum_w
        
        # 估计缺失研究数量 (简化实现)
        # 使用L0估计器
        gamma = 0  # 缺失研究数量估计
        
        for _ in range(max_iter):
            # 计算不对称性
            positive_side = [es for es in sorted_es if es >= weighted_median]
            negative_side = [es for es in sorted_es if es < weighted_median]
            
            # 简化：假设右侧缺失
            expected_ratio = len(positive_side) / (len(negative_side) + 1)
            
            if expected_ratio > 1.5:
                gamma += 1
                # 添加一个镜像研究
                mirror_es = 2 * weighted_median - min(positive_side)
                sorted_es.append(mirror_es)
                sorted_var.append(sorted_var[sorted_es.index(min(positive_side))])
            else:
                break
        
        # 重新计算效应量
        new_weights = [1/v for v in sorted_var]
        new_sum_w = sum(new_weights)
        adjusted_mean = sum(w * es for w, es in zip(new_weights, sorted_es)) / new_sum_w
        
        return {
            "original_studies": n,
            "trimmed_studies": gamma,
            "adjusted_estimate": round(adjusted_mean, 4),
            "original_estimate": round(
                sum(w * es for w, es in zip([1/v for v in variances], effect_sizes)) / 
                sum([1/v for v in variances]), 4
            ),
            "interpretation": f"Estimated {gamma} missing studies. " + 
                            f"Adjusted effect: {adjusted_mean:.3f}"
        }
    
    def funnel_plot_data(
        self,
        effect_sizes: List[float],
        standard_errors: List[float]
    ) -> Dict:
        """
        生成漏斗图数据
        """
        # 加权平均效应量
        weights = [1/se**2 for se in standard_errors]
        weighted_mean = sum(w * es for w, es in zip(weights, effect_sizes)) / sum(weights)
        
        # 漏斗图的对称线
        se_range = max(standard_errors) * 1.1
        
        return {
            "studies": [
                {"effect_size": es, "se": se, "weight": w}
                for es, se, w in zip(effect_sizes, standard_errors, weights)
            ],
            "center_line": weighted_mean,
            "funnel_bounds": {
                "upper": [weighted_mean + 1.96 * se for se in [0, se_range]],
                "lower": [weighted_mean - 1.96 * se for se in [0, se_range]]
            }
        }
    
    def comprehensive_analysis(
        self,
        effect_sizes: List[float],
        variances: List[float]
    ) -> Dict:
        """
        综合发表偏倚分析
        """
        standard_errors = [math.sqrt(v) for v in variances]
        
        # 执行多种检验
        egger = self.egger_test(effect_sizes, standard_errors)
        begg = self.begg_test(effect_sizes, variances)
        failsafe = self.fail_safe_n(effect_sizes, variances)
        trimfill = self.trim_and_fill(effect_sizes, variances)
        funnel = self.funnel_plot_data(effect_sizes, standard_errors)
        
        # 综合判断
        evidence_count = sum([
            egger.evidence_of_bias,
            begg.evidence_of_bias,
            failsafe["is_robust"] == False
        ])
        
        if evidence_count >= 2:
            overall = "Strong evidence of publication bias. Results should be interpreted with caution."
        elif evidence_count == 1:
            overall = "Some evidence of publication bias. Sensitivity analysis recommended."
        else:
            overall = "Little evidence of publication bias. Results appear robust."
        
        return {
            "egger_test": egger.to_dict(),
            "begg_test": begg.to_dict(),
            "fail_safe_n": failsafe,
            "trim_and_fill": trimfill,
            "funnel_plot": funnel,
            "overall_assessment": overall
        }
    
    def generate_report(self, analysis: Dict) -> str:
        """生成发表偏倚报告"""
        report = f"""
# 发表偏倚分析报告

## 1. Egger回归检验

- **统计量**: t = {analysis['egger_test']['statistic']:.3f}
- **p值**: {analysis['egger_test']['p_value']:.4f}
- **结论**: {analysis['egger_test']['interpretation']}

## 2. Begg秩相关检验

- **统计量**: z = {analysis['begg_test']['statistic']:.3f}
- **p值**: {analysis['begg_test']['p_value']:.4f}
- **结论**: {analysis['begg_test']['interpretation']}

## 3. Fail-safe N (Rosenthal)

- **Fail-safe N**: {analysis['fail_safe_n']['fail_safe_n']}
- **稳健性阈值**: {analysis['fail_safe_n']['robustness_threshold']}
- **稳健性评估**: {'稳健' if analysis['fail_safe_n']['is_robust'] else '可能不稳健'}
- **解释**: {analysis['fail_safe_n']['interpretation']}

## 4. Trim-and-fill校正

- **原始研究数**: {analysis['trim_and_fill']['original_studies']}
- **估计缺失研究**: {analysis['trim_and_fill']['trimmed_studies']}
- **原始效应量**: {analysis['trim_and_fill']['original_estimate']}
- **校正后效应量**: {analysis['trim_and_fill']['adjusted_estimate']}
- **解释**: {analysis['trim_and_fill']['interpretation']}

## 综合评估

{analysis['overall_assessment']}

## 建议

"""
        
        if "Strong evidence" in analysis['overall_assessment']:
            report += """
1. 结果应谨慎解释
2. 报告校正后的效应量估计
3. 进行敏感性分析
4. 考虑进行灰色文献搜索
"""
        else:
            report += """
1. 发表偏倚风险较低
2. 继续报告原始结果
3. 可进行敏感性分析作为补充
"""
        
        return report
    
    # 辅助函数
    
    def _rank(self, values: List[float]) -> List[float]:
        """计算秩"""
        sorted_indices = sorted(range(len(values)), key=lambda i: values[i])
        ranks = [0] * len(values)
        for rank, idx in enumerate(sorted_indices):
            ranks[idx] = rank + 1
        return ranks
    
    def _normal_cdf(self, x: float) -> float:
        """标准正态CDF"""
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    
    def _t_to_p(self, t: float, df: int) -> float:
        """t值转p值（近似）"""
        # 使用正态近似（大样本）
        if df >= 30:
            return 2 * (1 - self._normal_cdf(abs(t)))
        
        # 小样本校正
        # 简化实现
        p_approx = 2 * (1 - self._normal_cdf(abs(t)))
        return min(max(p_approx, 0.0001), 0.9999)


def test_publication_bias(
    effect_sizes: List[float],
    variances: List[float]
) -> Dict:
    """
    发表偏倚检验 - 主入口函数
    """
    tester = PublicationBiasTester()
    return tester.comprehensive_analysis(effect_sizes, variances)


# 示例使用
if __name__ == "__main__":
    # 模拟数据：存在潜在发表偏倚的数据
    # 大效应量研究较多，小效应量研究较少
    effect_sizes = [0.85, 0.72, 0.68, 0.55, 0.52, 0.45, 0.42, 0.38]
    variances = [0.03, 0.04, 0.05, 0.06, 0.04, 0.08, 0.07, 0.09]
    
    tester = PublicationBiasTester()
    
    print("=" * 60)
    print("发表偏倚检测工具")
    print("=" * 60)
    
    # 综合分析
    analysis = tester.comprehensive_analysis(effect_sizes, variances)
    
    print("\n【Egger检验】")
    print(f"  t = {analysis['egger_test']['statistic']:.3f}, p = {analysis['egger_test']['p_value']:.4f}")
    print(f"  {analysis['egger_test']['interpretation']}")
    
    print("\n【Begg检验】")
    print(f"  z = {analysis['begg_test']['statistic']:.3f}, p = {analysis['begg_test']['p_value']:.4f}")
    print(f"  {analysis['begg_test']['interpretation']}")
    
    print("\n【Fail-safe N】")
    print(f"  N = {analysis['fail_safe_n']['fail_safe_n']}")
    print(f"  {analysis['fail_safe_n']['interpretation']}")
    
    print("\n【Trim-and-fill】")
    print(f"  估计缺失研究: {analysis['trim_and_fill']['trimmed_studies']}")
    print(f"  校正效应量: {analysis['trim_and_fill']['adjusted_estimate']}")
    
    print("\n【综合评估】")
    print(analysis['overall_assessment'])
    
    print("\n" + "=" * 60)
    print(tester.generate_report(analysis))
