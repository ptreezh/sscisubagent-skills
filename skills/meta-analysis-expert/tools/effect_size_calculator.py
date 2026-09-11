#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
元分析专家 - 效应量计算器
Effect Size Calculator for Meta-Analysis

功能:
- 计算多种效应量类型
- 效应量转换
- 置信区间计算
- 方差估计

作者: Meta-Analysis Expert v5.0.0
创建时间: 2026-03-15
"""

import math
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import json

# 跨平台兼容
from pathlib import Path

def get_output_dir() -> Path:
    """获取输出目录"""
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


class EffectSizeType(Enum):
    """效应量类型枚举"""
    D = "Cohen's d"
    G = "Hedges' g"
    R = "Pearson r"
    OR = "Odds Ratio"
    RR = "Risk Ratio"
    RD = "Risk Difference"
    MD = "Mean Difference"
    SMD = "Standardized Mean Difference"
    IRR = "Incidence Rate Ratio"


@dataclass
class EffectSizeResult:
    """效应量计算结果"""
    effect_size: float
    effect_size_type: str
    confidence_interval: Tuple[float, float]
    standard_error: float
    variance: float
    sample_size: int
    p_value: Optional[float] = None
    
    def to_dict(self) -> Dict:
        return {
            "effect_size": round(self.effect_size, 4),
            "effect_size_type": self.effect_size_type,
            "confidence_interval": [round(self.confidence_interval[0], 4), round(self.confidence_interval[1], 4)],
            "standard_error": round(self.standard_error, 4),
            "variance": round(self.variance, 6),
            "sample_size": self.sample_size,
            "p_value": round(self.p_value, 4) if self.p_value else None
        }


class EffectSizeCalculator:
    """效应量计算器"""
    
    # Z值常量
    Z_95 = 1.96
    Z_99 = 2.576
    Z_90 = 1.645
    
    def __init__(self, confidence_level: float = 0.95):
        """
        初始化
        
        Args:
            confidence_level: 置信水平 (0.90, 0.95, 0.99)
        """
        self.confidence_level = confidence_level
        self.z_value = self._get_z_value(confidence_level)
    
    def _get_z_value(self, confidence_level: float) -> float:
        """获取Z值"""
        z_values = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
        return z_values.get(confidence_level, 1.96)
    
    # ==================== 连续变量效应量 ====================
    
    def cohen_d(
        self,
        mean1: float, mean2: float,
        sd1: float, sd2: float,
        n1: int, n2: int
    ) -> EffectSizeResult:
        """
        计算Cohen's d
        
        Cohen's d = (M1 - M2) / SD_pooled
        
        Args:
            mean1, mean2: 两组均值
            sd1, sd2: 两组标准差
            n1, n2: 两组样本量
        """
        # 合并标准差
        pooled_sd = self._pooled_sd(sd1, sd2, n1, n2)
        
        # Cohen's d
        d = (mean1 - mean2) / pooled_sd
        
        # 方差 (Hedges & Olkin, 1985)
        variance = (n1 + n2) / (n1 * n2) + d**2 / (2 * (n1 + n2))
        
        # 标准误
        se = math.sqrt(variance)
        
        # 置信区间
        ci_lower = d - self.z_value * se
        ci_upper = d + self.z_value * se
        
        # p值 (双尾)
        z_stat = d / se
        p_value = self._z_to_p(z_stat)
        
        return EffectSizeResult(
            effect_size=d,
            effect_size_type="Cohen's d",
            confidence_interval=(ci_lower, ci_upper),
            standard_error=se,
            variance=variance,
            sample_size=n1 + n2,
            p_value=p_value
        )
    
    def hedges_g(
        self,
        mean1: float, mean2: float,
        sd1: float, sd2: float,
        n1: int, n2: int
    ) -> EffectSizeResult:
        """
        计算Hedges' g (校正小样本偏差的Cohen's d)
        
        Hedges' g = Cohen's d × J
        
        其中 J = 1 - (3 / (4 * df - 1))
        """
        # 先计算Cohen's d
        d_result = self.cohen_d(mean1, mean2, sd1, sd2, n1, n2)
        
        # 校正因子
        df = n1 + n2 - 2
        j = 1 - (3 / (4 * df - 1))
        
        # Hedges' g
        g = d_result.effect_size * j
        
        # 校正后方差
        variance = d_result.variance * j**2
        
        # 标准误
        se = math.sqrt(variance)
        
        # 置信区间
        ci_lower = g - self.z_value * se
        ci_upper = g + self.z_value * se
        
        # p值
        z_stat = g / se
        p_value = self._z_to_p(z_stat)
        
        return EffectSizeResult(
            effect_size=g,
            effect_size_type="Hedges' g",
            confidence_interval=(ci_lower, ci_upper),
            standard_error=se,
            variance=variance,
            sample_size=n1 + n2,
            p_value=p_value
        )
    
    def pearson_r(
        self,
        r: float,
        n: int
    ) -> EffectSizeResult:
        """
        计算Pearson r相关系数的元分析效应量
        
        使用Fisher's z转换
        """
        # Fisher's z转换
        z = 0.5 * math.log((1 + r) / (1 - r))
        
        # 标准误
        se = 1 / math.sqrt(n - 3)
        
        # 置信区间 (Fisher's z尺度)
        z_lower = z - self.z_value * se
        z_upper = z + self.z_value * se
        
        # 转回r尺度
        ci_lower = (math.exp(2 * z_lower) - 1) / (math.exp(2 * z_lower) + 1)
        ci_upper = (math.exp(2 * z_upper) - 1) / (math.exp(2 * z_upper) + 1)
        
        # 方差
        variance = se**2
        
        # p值
        z_stat = abs(z / se)
        p_value = 2 * (1 - self._normal_cdf(z_stat))
        
        return EffectSizeResult(
            effect_size=r,
            effect_size_type="Pearson r",
            confidence_interval=(ci_lower, ci_upper),
            standard_error=se,
            variance=variance,
            sample_size=n,
            p_value=p_value
        )
    
    # ==================== 二分类变量效应量 ====================
    
    def odds_ratio(
        self,
        a: int, b: int, c: int, d: int
    ) -> EffectSizeResult:
        """
        计算优势比 (Odds Ratio)
        
        OR = (a/c) / (b/d) = ad/bc
        
        2×2表:
                    Event    No Event
        Group 1      a          b
        Group 2      c          d
        """
        # 添加0.5校正（如果有零单元格）
        correction = 0.5 if (a == 0 or b == 0 or c == 0 or d == 0) else 0
        
        a_adj = a + correction
        b_adj = b + correction
        c_adj = c + correction
        d_adj = d + correction
        
        # OR
        or_value = (a_adj * d_adj) / (b_adj * c_adj)
        
        # 对数OR
        log_or = math.log(or_value)
        
        # 对数OR的方差
        variance = 1/a_adj + 1/b_adj + 1/c_adj + 1/d_adj
        
        # 标准误
        se = math.sqrt(variance)
        
        # 置信区间 (对数尺度)
        log_ci_lower = log_or - self.z_value * se
        log_ci_upper = log_or + self.z_value * se
        
        # 转回OR尺度
        ci_lower = math.exp(log_ci_lower)
        ci_upper = math.exp(log_ci_upper)
        
        # p值 (Wald检验)
        z_stat = log_or / se
        p_value = 2 * (1 - self._normal_cdf(abs(z_stat)))
        
        return EffectSizeResult(
            effect_size=or_value,
            effect_size_type="Odds Ratio",
            confidence_interval=(ci_lower, ci_upper),
            standard_error=se,
            variance=variance,
            sample_size=a + b + c + d,
            p_value=p_value
        )
    
    def risk_ratio(
        self,
        a: int, b: int, c: int, d: int
    ) -> EffectSizeResult:
        """
        计算风险比 (Risk Ratio / Relative Risk)
        
        RR = (a/(a+b)) / (c/(c+d))
        """
        n1 = a + b  # 第一组总数
        n2 = c + d  # 第二组总数
        
        # 避免除零
        if n1 == 0 or n2 == 0:
            raise ValueError("Group totals cannot be zero")
        
        # 添加校正
        correction = 0.5 if (a == 0 or c == 0) else 0
        a_adj = a + correction
        c_adj = c + correction
        n1_adj = n1 + correction
        n2_adj = n2 + correction
        
        # RR
        rr = (a_adj / n1_adj) / (c_adj / n2_adj)
        
        # 对数RR
        log_rr = math.log(rr)
        
        # 对数RR的方差
        variance = (1/a_adj - 1/n1_adj + 1/c_adj - 1/n2_adj)
        
        # 标准误
        se = math.sqrt(variance)
        
        # 置信区间
        log_ci_lower = log_rr - self.z_value * se
        log_ci_upper = log_rr + self.z_value * se
        
        ci_lower = math.exp(log_ci_lower)
        ci_upper = math.exp(log_ci_upper)
        
        # p值
        z_stat = log_rr / se
        p_value = 2 * (1 - self._normal_cdf(abs(z_stat)))
        
        return EffectSizeResult(
            effect_size=rr,
            effect_size_type="Risk Ratio",
            confidence_interval=(ci_lower, ci_upper),
            standard_error=se,
            variance=variance,
            sample_size=n1 + n2,
            p_value=p_value
        )
    
    def risk_difference(
        self,
        a: int, b: int, c: int, d: int
    ) -> EffectSizeResult:
        """
        计算风险差 (Risk Difference / Absolute Risk Reduction)
        
        RD = a/(a+b) - c/(c+d)
        """
        n1 = a + b
        n2 = c + d
        
        # 事件率
        p1 = a / n1
        p2 = c / n2
        
        # RD
        rd = p1 - p2
        
        # 方差
        variance = (p1 * (1 - p1) / n1) + (p2 * (1 - p2) / n2)
        
        # 标准误
        se = math.sqrt(variance)
        
        # 置信区间
        ci_lower = rd - self.z_value * se
        ci_upper = rd + self.z_value * se
        
        # p值
        z_stat = rd / se
        p_value = 2 * (1 - self._normal_cdf(abs(z_stat)))
        
        return EffectSizeResult(
            effect_size=rd,
            effect_size_type="Risk Difference",
            confidence_interval=(ci_lower, ci_upper),
            standard_error=se,
            variance=variance,
            sample_size=n1 + n2,
            p_value=p_value
        )
    
    # ==================== 效应量转换 ====================
    
    def d_to_r(self, d: float) -> float:
        """Cohen's d 转换为 Pearson r"""
        return d / math.sqrt(d**2 + 4)
    
    def r_to_d(self, r: float) -> float:
        """Pearson r 转换为 Cohen's d"""
        return 2 * r / math.sqrt(1 - r**2)
    
    def d_to_or(self, d: float) -> float:
        """Cohen's d 转换为 Odds Ratio"""
        return math.exp(d * math.pi / math.sqrt(3))
    
    def or_to_d(self, or_value: float) -> float:
        """Odds Ratio 转换为 Cohen's d"""
        return math.log(or_value) * math.sqrt(3) / math.pi
    
    def r_to_or(self, r: float) -> float:
        """Pearson r 转换为 Odds Ratio"""
        d = self.r_to_d(r)
        return self.d_to_or(d)
    
    # ==================== 辅助函数 ====================
    
    def _pooled_sd(self, sd1: float, sd2: float, n1: int, n2: int) -> float:
        """计算合并标准差"""
        return math.sqrt(
            ((n1 - 1) * sd1**2 + (n2 - 1) * sd2**2) / (n1 + n2 - 2)
        )
    
    def _normal_cdf(self, x: float) -> float:
        """标准正态分布累积分布函数（近似）"""
        # 使用误差函数近似
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    
    def _z_to_p(self, z: float, two_tailed: bool = True) -> float:
        """Z值转p值"""
        p = 2 * (1 - self._normal_cdf(abs(z)))
        return p if two_tailed else p / 2
    
    # ==================== 批量计算 ====================
    
    def calculate_from_studies(
        self,
        studies: List[Dict],
        effect_size_type: str
    ) -> List[Dict]:
        """
        批量计算多个研究的效应量
        
        Args:
            studies: 研究数据列表
            effect_size_type: 效应量类型 ('d', 'g', 'r', 'or', 'rr', 'rd')
        
        Returns:
            效应量结果列表
        """
        results = []
        
        for i, study in enumerate(studies):
            try:
                if effect_size_type.lower() == 'd':
                    result = self.cohen_d(
                        study['mean1'], study['mean2'],
                        study['sd1'], study['sd2'],
                        study['n1'], study['n2']
                    )
                elif effect_size_type.lower() == 'g':
                    result = self.hedges_g(
                        study['mean1'], study['mean2'],
                        study['sd1'], study['sd2'],
                        study['n1'], study['n2']
                    )
                elif effect_size_type.lower() == 'r':
                    result = self.pearson_r(study['r'], study['n'])
                elif effect_size_type.lower() == 'or':
                    result = self.odds_ratio(
                        study['a'], study['b'], study['c'], study['d']
                    )
                elif effect_size_type.lower() == 'rr':
                    result = self.risk_ratio(
                        study['a'], study['b'], study['c'], study['d']
                    )
                elif effect_size_type.lower() == 'rd':
                    result = self.risk_difference(
                        study['a'], study['b'], study['c'], study['d']
                    )
                else:
                    raise ValueError(f"Unknown effect size type: {effect_size_type}")
                
                result_dict = result.to_dict()
                result_dict['study_id'] = study.get('study_id', f'Study_{i+1}')
                result_dict['study_name'] = study.get('study_name', f'Study {i+1}')
                results.append(result_dict)
                
            except Exception as e:
                results.append({
                    'study_id': study.get('study_id', f'Study_{i+1}'),
                    'study_name': study.get('study_name', f'Study {i+1}'),
                    'error': str(e)
                })
        
        return results


def interpret_effect_size(d: float) -> str:
    """解释效应量大小 (Cohen's conventions)"""
    abs_d = abs(d)
    if abs_d < 0.2:
        return "Trivial/Very Small"
    elif abs_d < 0.5:
        return "Small"
    elif abs_d < 0.8:
        return "Medium"
    else:
        return "Large"


def interpret_or(or_value: float) -> str:
    """解释优势比"""
    if or_value < 0.9:
        return f"Protective effect (reduced risk)"
    elif or_value > 1.1:
        return f"Risk factor (increased risk)"
    else:
        return "No meaningful effect"


# 示例使用
if __name__ == "__main__":
    calculator = EffectSizeCalculator(confidence_level=0.95)
    
    print("=" * 60)
    print("元分析效应量计算器")
    print("=" * 60)
    
    # 示例1: Cohen's d
    print("\n【示例1: Cohen's d - 连续变量】")
    d_result = calculator.cohen_d(
        mean1=85.2, mean2=78.5,
        sd1=12.3, sd2=11.8,
        n1=50, n2=45
    )
    print(f"Cohen's d = {d_result.effect_size:.3f}")
    print(f"95% CI: [{d_result.confidence_interval[0]:.3f}, {d_result.confidence_interval[1]:.3f}]")
    print(f"解释: {interpret_effect_size(d_result.effect_size)}")
    
    # 示例2: Hedges' g
    print("\n【示例2: Hedges' g - 小样本校正】")
    g_result = calculator.hedges_g(
        mean1=85.2, mean2=78.5,
        sd1=12.3, sd2=11.8,
        n1=50, n2=45
    )
    print(f"Hedges' g = {g_result.effect_size:.3f}")
    print(f"95% CI: [{g_result.confidence_interval[0]:.3f}, {g_result.confidence_interval[1]:.3f}]")
    
    # 示例3: Odds Ratio
    print("\n【示例3: Odds Ratio - 二分类变量】")
    or_result = calculator.odds_ratio(
        a=45, b=55,   # 干预组: 45事件, 55非事件
        c=30, d=70    # 对照组: 30事件, 70非事件
    )
    print(f"OR = {or_result.effect_size:.3f}")
    print(f"95% CI: [{or_result.confidence_interval[0]:.3f}, {or_result.confidence_interval[1]:.3f}]")
    print(f"解释: {interpret_or(or_result.effect_size)}")
    
    # 示例4: Risk Ratio
    print("\n【示例4: Risk Ratio - 相对风险】")
    rr_result = calculator.risk_ratio(
        a=45, b=55,
        c=30, d=70
    )
    print(f"RR = {rr_result.effect_size:.3f}")
    print(f"95% CI: [{rr_result.confidence_interval[0]:.3f}, {rr_result.confidence_interval[1]:.3f}]")
    
    # 示例5: 效应量转换
    print("\n【示例5: 效应量转换】")
    d = 0.5
    print(f"Cohen's d = {d}")
    print(f"  → Pearson r = {calculator.d_to_r(d):.3f}")
    print(f"  → Odds Ratio = {calculator.d_to_or(d):.3f}")
    
    print("\n" + "=" * 60)
    print("效应量计算器已加载完成")
