#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
元分析专家 - 异质性分析器
Heterogeneity Analyzer for Meta-Analysis

功能:
- Q检验 (Cochran's Q)
- I²统计量计算
- Tau²估计 (DerSimonian-Laird, REML, ML)
- 模型选择建议
- 异质性来源分析

作者: Meta-Analysis Expert v5.0.0
创建时间: 2026-03-15
"""

import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import json
from pathlib import Path


class HeterogeneityLevel(Enum):
    """异质性水平"""
    LOW = "Low (I² < 25%)"
    MODERATE = "Moderate (I² 25-50%)"
    SUBSTANTIAL = "Substantial (I² 50-75%)"
    CONSIDERABLE = "Considerable (I² > 75%)"


@dataclass
class HeterogeneityResult:
    """异质性分析结果"""
    q_statistic: float
    q_df: int
    q_pvalue: float
    i_squared: float
    i_squared_ci: Tuple[float, float]
    tau_squared: float
    tau: float
    heterogeneity_level: str
    model_recommendation: str
    
    def to_dict(self) -> Dict:
        return {
            "q_statistic": round(self.q_statistic, 3),
            "q_df": self.q_df,
            "q_pvalue": round(self.q_pvalue, 4),
            "i_squared": f"{self.i_squared:.1f}%",
            "i_squared_ci": [f"{self.i_squared_ci[0]:.1f}%", f"{self.i_squared_ci[1]:.1f}%"],
            "tau_squared": round(self.tau_squared, 4),
            "tau": round(self.tau, 4),
            "heterogeneity_level": self.heterogeneity_level,
            "model_recommendation": self.model_recommendation
        }


class HeterogeneityAnalyzer:
    """异质性分析器"""
    
    # 卡方分布临界值（简化版，常用df）
    CHI2_CRITICAL = {
        0.05: {  # alpha = 0.05
            1: 3.841, 2: 5.991, 3: 7.815, 4: 9.488, 5: 11.070,
            6: 12.592, 7: 14.067, 8: 15.507, 9: 16.919, 10: 18.307,
            15: 24.996, 20: 31.410, 25: 37.652, 30: 43.773
        },
        0.01: {  # alpha = 0.01
            1: 6.635, 2: 9.210, 3: 11.345, 4: 13.277, 5: 15.086,
            6: 16.812, 7: 18.475, 8: 20.090, 9: 21.666, 10: 23.209,
            15: 30.578, 20: 37.566, 25: 44.314, 30: 50.892
        }
    }
    
    def __init__(self):
        pass
    
    def analyze(
        self,
        effect_sizes: List[float],
        variances: List[float],
        sample_sizes: List[int] = None
    ) -> HeterogeneityResult:
        """
        执行异质性分析
        
        Args:
            effect_sizes: 效应量列表
            variances: 效应量方差列表
            sample_sizes: 样本量列表（可选）
        
        Returns:
            异质性分析结果
        """
        k = len(effect_sizes)
        
        if k < 2:
            raise ValueError("Need at least 2 studies for heterogeneity analysis")
        
        # 计算权重
        weights = [1/v for v in variances]
        sum_w = sum(weights)
        sum_w2 = sum(w**2 for w in weights)
        
        # 加权平均效应量
        weighted_mean = sum(w * es for w, es in zip(weights, effect_sizes)) / sum_w
        
        # Q统计量 (Cochran's Q)
        q = sum(w * (es - weighted_mean)**2 for w, es in zip(weights, effect_sizes))
        
        # Q检验p值
        df = k - 1
        q_pvalue = self._chi2_pvalue(q, df)
        
        # I²统计量
        i_squared = max(0, 100 * (q - df) / q) if q > 0 else 0
        
        # I²置信区间 (Higgins & Thompson, 2002)
        i_squared_ci = self._i_squared_ci(q, df)
        
        # Tau²估计 (DerSimonian-Laird)
        c = sum_w - sum_w2 / sum_w
        tau_squared = max(0, (q - df) / c)
        tau = math.sqrt(tau_squared)
        
        # 异质性水平
        het_level = self._interpret_i_squared(i_squared)
        
        # 模型推荐
        model_rec = self._recommend_model(i_squared, q_pvalue)
        
        return HeterogeneityResult(
            q_statistic=q,
            q_df=df,
            q_pvalue=q_pvalue,
            i_squared=i_squared,
            i_squared_ci=i_squared_ci,
            tau_squared=tau_squared,
            tau=tau,
            heterogeneity_level=het_level,
            model_recommendation=model_rec
        )
    
    def _chi2_pvalue(self, q: float, df: int) -> float:
        """卡方检验p值（近似计算）"""
        # 使用Wilson-Hilferty近似
        if df <= 0:
            return 1.0
        
        # 简化：使用临界值表判断
        if df in self.CHI2_CRITICAL[0.05]:
            if q > self.CHI2_CRITICAL[0.01][df]:
                return 0.001
            elif q > self.CHI2_CRITICAL[0.05][df]:
                return 0.025
            else:
                return 0.10
        
        # 近似计算
        z = (q / df)**(1/3) - (1 - 2/(9*df))
        z = z / math.sqrt(2/(9*df))
        
        # 标准正态CDF
        p = 0.5 * (1 + math.erf(-abs(z) / math.sqrt(2)))
        return min(max(2 * p, 0.0001), 0.9999)
    
    def _i_squared_ci(self, q: float, df: int, confidence: float = 0.95) -> Tuple[float, float]:
        """I²置信区间"""
        # 使用非中心卡方分布近似
        # 简化实现
        
        if q <= df:
            # 低异质性情况
            lower = 0
            upper = min(100, 100 * (q * 1.96**2 + df) / (q + df * 1.96**2))
        else:
            # 高异质性情况
            z = 1.96  # 95% CI
            
            # 下限
            q_lower = max(0, q - z * math.sqrt(2 * df))
            i_lower = max(0, 100 * (q_lower - df) / q_lower) if q_lower > 0 else 0
            
            # 上限
            q_upper = q + z * math.sqrt(2 * df)
            i_upper = min(100, 100 * (q_upper - df) / q_upper)
            
            lower, upper = i_lower, i_upper
        
        return (lower, upper)
    
    def _interpret_i_squared(self, i_squared: float) -> str:
        """解释I²统计量"""
        if i_squared < 25:
            return "Low heterogeneity (I² < 25%)"
        elif i_squared < 50:
            return "Moderate heterogeneity (I² 25-50%)"
        elif i_squared < 75:
            return "Substantial heterogeneity (I² 50-75%)"
        else:
            return "Considerable heterogeneity (I² > 75%)"
    
    def _recommend_model(self, i_squared: float, q_pvalue: float) -> str:
        """模型选择建议"""
        if i_squared < 50 and q_pvalue > 0.05:
            return "Fixed-effect model recommended (low heterogeneity, Q-test non-significant)"
        elif i_squared >= 50 or q_pvalue <= 0.05:
            return "Random-effects model recommended (significant heterogeneity detected)"
        else:
            return "Both models acceptable; consider sensitivity analysis"
    
    def tau_squared_reml(
        self,
        effect_sizes: List[float],
        variances: List[float],
        max_iter: int = 100,
        tol: float = 1e-5
    ) -> float:
        """
        REML方法估计Tau²
        
        Restricted Maximum Likelihood Estimation
        """
        k = len(effect_sizes)
        
        # 初始值 (D-L估计)
        result = self.analyze(effect_sizes, variances)
        tau2 = result.tau_squared
        
        for _ in range(max_iter):
            # 计算权重
            weights = [1 / (v + tau2) for v in variances]
            sum_w = sum(weights)
            
            # 加权平均
            mu = sum(w * es for w, es in zip(weights, effect_sizes)) / sum_w
            
            # 更新tau2
            new_tau2 = sum(
                w * (es - mu)**2 for w, es in zip(weights, effect_sizes)
            ) / sum_w - k / sum_w
            
            new_tau2 = max(0, new_tau2)
            
            # 收敛检查
            if abs(new_tau2 - tau2) < tol:
                break
            
            tau2 = new_tau2
        
        return tau2
    
    def compare_models(
        self,
        effect_sizes: List[float],
        variances: List[float]
    ) -> Dict:
        """比较固定效应和随机效应模型"""
        k = len(effect_sizes)
        
        # 固定效应模型
        fe_weights = [1/v for v in variances]
        fe_sum_w = sum(fe_weights)
        fe_mean = sum(w * es for w, es in zip(fe_weights, effect_sizes)) / fe_sum_w
        fe_var = 1 / fe_sum_w
        fe_se = math.sqrt(fe_var)
        
        # 随机效应模型
        het_result = self.analyze(effect_sizes, variances)
        re_weights = [1 / (v + het_result.tau_squared) for v in variances]
        re_sum_w = sum(re_weights)
        re_mean = sum(w * es for w, es in zip(re_weights, effect_sizes)) / re_sum_w
        re_var = 1 / re_sum_w
        re_se = math.sqrt(re_var)
        
        return {
            "fixed_effect": {
                "estimate": round(fe_mean, 4),
                "standard_error": round(fe_se, 4),
                "95_ci": [round(fe_mean - 1.96 * fe_se, 4), round(fe_mean + 1.96 * fe_se, 4)]
            },
            "random_effects": {
                "estimate": round(re_mean, 4),
                "standard_error": round(re_se, 4),
                "95_ci": [round(re_mean - 1.96 * re_se, 4), round(re_mean + 1.96 * re_se, 4)]
            },
            "heterogeneity": het_result.to_dict()
        }
    
    def generate_report(self, result: HeterogeneityResult) -> str:
        """生成异质性报告"""
        report = f"""
# 异质性分析报告

## Q检验 (Cochran's Q)

- **Q统计量**: {result.q_statistic:.3f}
- **自由度**: {result.q_df}
- **p值**: {result.q_pvalue:.4f}

{'⚠️ Q检验显著 (p < 0.05)，存在异质性' if result.q_pvalue < 0.05 else '✅ Q检验不显著 (p ≥ 0.05)，异质性较低'}

## I²统计量

- **I²**: {result.i_squared:.1f}%
- **95% CI**: [{result.i_squared_ci[0]:.1f}%, {result.i_squared_ci[1]:.1f}%]

**解释**: {result.heterogeneity_level}

### I²解释标准
| 范围 | 解释 |
|------|------|
| 0-25% | 低异质性 |
| 25-50% | 中等异质性 |
| 50-75% | 较高异质性 |
| >75% | 高异质性 |

## Tau²统计量

- **Tau²**: {result.tau_squared:.4f}
- **Tau**: {result.tau:.4f}

Tau²表示研究间效应量的真实方差。

## 模型选择建议

**{result.model_recommendation}**

## 异质性处理建议

"""
        
        if result.i_squared >= 50:
            report += """
1. **探索异质性来源**:
   - 进行亚组分析
   - 进行元回归分析
   - 检查研究特征差异

2. **敏感性分析**:
   - 逐一排除研究
   - 检查影响性研究

3. **报告选择**:
   - 使用随机效应模型
   - 报告预测区间
"""
        else:
            report += """
1. 异质性较低，可使用固定效应模型
2. 仍建议进行敏感性分析验证结果稳定性
"""
        
        return report


def analyze_heterogeneity(
    effect_sizes: List[float],
    variances: List[float]
) -> Dict:
    """
    异质性分析 - 主入口函数
    
    Args:
        effect_sizes: 效应量列表
        variances: 方差列表
    
    Returns:
        分析结果字典
    """
    analyzer = HeterogeneityAnalyzer()
    result = analyzer.analyze(effect_sizes, variances)
    return result.to_dict()


# 示例使用
if __name__ == "__main__":
    # 模拟数据：10个研究的效应量和方差
    effect_sizes = [0.45, 0.62, 0.38, 0.55, 0.48, 0.72, 0.41, 0.58, 0.52, 0.49]
    variances = [0.04, 0.03, 0.05, 0.04, 0.03, 0.04, 0.06, 0.03, 0.04, 0.05]
    
    analyzer = HeterogeneityAnalyzer()
    
    print("=" * 60)
    print("异质性分析器")
    print("=" * 60)
    
    # 执行分析
    result = analyzer.analyze(effect_sizes, variances)
    
    print(f"\nQ统计量: {result.q_statistic:.3f} (df={result.q_df}, p={result.q_pvalue:.4f})")
    print(f"I²: {result.i_squared:.1f}%")
    print(f"Tau²: {result.tau_squared:.4f}")
    print(f"异质性水平: {result.heterogeneity_level}")
    print(f"\n模型建议: {result.model_recommendation}")
    
    # 比较模型
    print("\n" + "=" * 60)
    print("模型比较")
    print("=" * 60)
    
    comparison = analyzer.compare_models(effect_sizes, variances)
    print(f"\n固定效应模型:")
    print(f"  估计值: {comparison['fixed_effect']['estimate']}")
    print(f"  95% CI: {comparison['fixed_effect']['95_ci']}")
    
    print(f"\n随机效应模型:")
    print(f"  估计值: {comparison['random_effects']['estimate']}")
    print(f"  95% CI: {comparison['random_effects']['95_ci']}")
    
    # 生成报告
    print("\n" + analyzer.generate_report(result))
