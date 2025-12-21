#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
消费行为分析器
分析个体的消费行为模式和消费异化程度
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json


class PurchaseMotivation(Enum):
    """购买动机类型"""
    UTILITY = "utility"           # 实用性需求
    EMOTIONAL = "emotional"       # 情感需求
    SOCIAL = "social"            # 社会需求
    STATUS = "status"            # 地位需求
    IMPULSE = "impulse"          # 冲动购买
    COMPULSIVE = "compulsive"    # 强迫性购买


@dataclass
class ConsumerBehaviorMetrics:
    """消费行为指标数据类"""
    purchase_frequency: float         # 购买频率
    average_spending: float          # 平均消费金额
    impulse_purchase_ratio: float    # 冲动购买比例
    utility_purchase_ratio: float    # 实用性购买比例
    status_purchase_ratio: float     # 地位性购买比例
    emotional_purchase_ratio: float  # 情感性购买比例
    price_sensitivity: float         # 价格敏感性
    brand_loyalty: float            # 品牌忠诚度
    shopping_satisfaction: float     # 购物满意度
    debt_to_income_ratio: float     # 债务收入比


class ConsumerBehaviorAnalyzer:
    """消费行为分析器"""
    
    def __init__(self):
        self.consumption_weights = {
            'purchase_frequency': 0.10,
            'average_spending': 0.08,
            'impulse_purchase_ratio': 0.20,
            'utility_purchase_ratio': 0.15,
            'status_purchase_ratio': 0.15,
            'emotional_purchase_ratio': 0.12,
            'price_sensitivity': 0.08,
            'brand_loyalty': 0.05,
            'shopping_satisfaction': 0.05,
            'debt_to_income_ratio': 0.02
        }
        
        self.alienation_thresholds = {
            'high_alienation': 0.70,
            'moderate_alienation': 0.50,
            'low_alienation': 0.30,
            'minimal_alienation': 0.15
        }
        
        self.consumer_segments = {
            'rational_consumer': {
                'utility_ratio': 0.7,
                'impulse_ratio': 0.1,
                'price_sensitivity': 0.8
            },
            'emotional_consumer': {
                'emotional_ratio': 0.6,
                'impulse_ratio': 0.3,
                'shopping_satisfaction': 0.8
            },
            'status_consumer': {
                'status_ratio': 0.5,
                'brand_loyalty': 0.8,
                'spending_level': 'high'
            },
            'compulsive_consumer': {
                'impulse_ratio': 0.6,
                'debt_ratio': 0.4,
                'satisfaction': 0.3
            }
        }
    
    def analyze_consumer_behavior(self, behavior_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析消费行为
        
        Args:
            behavior_data: 消费行为数据字典
            
        Returns:
            分析结果字典
        """
        # 解析消费数据
        metrics_data = behavior_data.get('metrics', {})
        purchase_history = behavior_data.get('purchase_history', [])
        financial_data = behavior_data.get('financial_data', {})
        
        # 创建消费行为指标
        metrics = self._create_consumer_metrics(metrics_data)
        
        # 计算消费异化程度
        alienation_score = self._calculate_alienation_score(metrics)
        
        # 分析消费模式
        consumption_patterns = self._analyze_consumption_patterns(metrics)
        
        # 识别消费者类型
        consumer_segment = self._identify_consumer_segment(metrics)
        
        # 分析购买动机
        purchase_motivations = self._analyze_purchase_motivations(metrics)
        
        # 评估消费理性
        rationality_assessment = self._assess_consumption_rationality(metrics)
        
        # 分析消费压力
        consumption_pressures = self._analyze_consumption_pressures(metrics)
        
        # 预测消费趋势
        consumption_trends = self._predict_consumption_trends(metrics)
        
        # 评估与消费异化的相关性
        alienation_correlation = self._assess_alienation_correlation(metrics)
        
        return {
            'alienation_score': alienation_score,
            'alienation_level': self._determine_alienation_level(alienation_score),
            'consumption_patterns': consumption_patterns,
            'consumer_segment': consumer_segment,
            'purchase_motivations': purchase_motivations,
            'rationality_assessment': rationality_assessment,
            'consumption_pressures': consumption_pressures,
            'consumption_trends': consumption_trends,
            'alienation_correlation': alienation_correlation,
            'intervention_recommendations': self._generate_intervention_recommendations(metrics),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _create_consumer_metrics(self, data: Dict[str, float]) -> ConsumerBehaviorMetrics:
        """创建消费行为指标"""
        # 设置默认值
        default_values = {
            'purchase_frequency': 0.5,
            'average_spending': 0.5,
            'impulse_purchase_ratio': 0.2,
            'utility_purchase_ratio': 0.6,
            'status_purchase_ratio': 0.2,
            'emotional_purchase_ratio': 0.2,
            'price_sensitivity': 0.5,
            'brand_loyalty': 0.5,
            'shopping_satisfaction': 0.5,
            'debt_to_income_ratio': 0.1
        }
        
        # 合并数据
        merged_data = {**default_values, **data}
        
        return ConsumerBehaviorMetrics(**merged_data)
    
    def _calculate_alienation_score(self, metrics: ConsumerBehaviorMetrics) -> float:
        """计算消费异化分数"""
        # 异化指标权重
        alienation_weights = {
            'impulse_purchase_ratio': 0.25,      # 冲动购买权重最高
            'status_purchase_ratio': 0.20,       # 地位性购买
            'emotional_purchase_ratio': 0.20,    # 情感性购买
            'debt_to_income_ratio': 0.15,        # 债务负担
            'brand_loyalty': 0.10,              # 品牌盲从
            'shopping_satisfaction': 0.10        # 购物满意度 (负相关)
        }
        
        # 计算异化分数
        alienation_score = (
            metrics.impulse_purchase_ratio * alienation_weights['impulse_purchase_ratio'] +
            metrics.status_purchase_ratio * alienation_weights['status_purchase_ratio'] +
            metrics.emotional_purchase_ratio * alienation_weights['emotional_purchase_ratio'] +
            metrics.debt_to_income_ratio * alienation_weights['debt_to_income_ratio'] +
            metrics.brand_loyalty * alienation_weights['brand_loyalty'] +
            (1 - metrics.shopping_satisfaction) * alienation_weights['shopping_satisfaction']
        )
        
        return min(1.0, alienation_score)
    
    def _analyze_consumption_patterns(self, metrics: ConsumerBehaviorMetrics) -> Dict[str, Any]:
        """分析消费模式"""
        return {
            'primary_consumption_type': self._identify_primary_consumption_type(metrics),
            'consumption_balance': self._assess_consumption_balance(metrics),
            'consumption_intensity': self._assess_consumption_intensity(metrics),
            'consumption_sustainability': self._assess_consumption_sustainability(metrics)
        }
    
    def _identify_consumer_segment(self, metrics: ConsumerBehaviorMetrics) -> str:
        """识别消费者类型"""
        # 计算与各类型消费者的相似度
        similarities = {}
        
        # 理性消费者
        rational_score = (
            metrics.utility_purchase_ratio * 0.4 +
            (1 - metrics.impulse_purchase_ratio) * 0.3 +
            metrics.price_sensitivity * 0.3
        )
        similarities['rational_consumer'] = rational_score
        
        # 情感消费者
        emotional_score = (
            metrics.emotional_purchase_ratio * 0.4 +
            metrics.impulse_purchase_ratio * 0.3 +
            metrics.shopping_satisfaction * 0.3
        )
        similarities['emotional_consumer'] = emotional_score
        
        # 地位消费者
        status_score = (
            metrics.status_purchase_ratio * 0.5 +
            metrics.brand_loyalty * 0.3 +
            metrics.average_spending * 0.2
        )
        similarities['status_consumer'] = status_score
        
        # 强迫性消费者
        compulsive_score = (
            metrics.impulse_purchase_ratio * 0.4 +
            metrics.debt_to_income_ratio * 0.3 +
            (1 - metrics.shopping_satisfaction) * 0.3
        )
        similarities['compulsive_consumer'] = compulsive_score
        
        # 返回相似度最高的类型
        return max(similarities, key=similarities.get)
    
    def _analyze_purchase_motivations(self, metrics: ConsumerBehaviorMetrics) -> Dict[str, float]:
        """分析购买动机"""
        return {
            'utility_motivation': metrics.utility_purchase_ratio,
            'emotional_motivation': metrics.emotional_purchase_ratio,
            'social_motivation': metrics.status_purchase_ratio,
            'impulse_motivation': metrics.impulse_purchase_ratio,
            'dominant_motivation': self._identify_dominant_motivation(metrics)
        }
    
    def _assess_consumption_rationality(self, metrics: ConsumerBehaviorMetrics) -> Dict[str, Any]:
        """评估消费理性"""
        # 计算理性分数
        rationality_score = (
            metrics.utility_purchase_ratio * 0.3 +
            (1 - metrics.impulse_purchase_ratio) * 0.25 +
            metrics.price_sensitivity * 0.2 +
            (1 - metrics.status_purchase_ratio) * 0.15 +
            (1 - metrics.debt_to_income_ratio) * 0.1
        )
        
        return {
            'rationality_score': rationality_score,
            'rationality_level': self._determine_rationality_level(rationality_score),
            'irrational_indicators': self._identify_irrational_indicators(metrics),
            'rational_strategies': self._suggest_rational_strategies(metrics)
        }
    
    def _analyze_consumption_pressures(self, metrics: ConsumerBehaviorMetrics) -> Dict[str, Any]:
        """分析消费压力"""
        # 计算消费压力指标
        pressure_indicators = {
            'financial_pressure': min(1.0, metrics.debt_to_income_ratio * 2),
            'social_pressure': metrics.status_purchase_ratio,
            'emotional_pressure': metrics.emotional_purchase_ratio,
            'impulse_pressure': metrics.impulse_purchase_ratio
        }
        
        total_pressure = np.mean(list(pressure_indicators.values()))
        
        return {
            'pressure_indicators': pressure_indicators,
            'total_pressure_score': total_pressure,
            'pressure_level': self._determine_pressure_level(total_pressure),
            'pressure_sources': self._identify_pressure_sources(pressure_indicators)
        }
    
    def _predict_consumption_trends(self, metrics: ConsumerBehaviorMetrics) -> Dict[str, Any]:
        """预测消费趋势"""
        # 基于当前指标预测未来趋势
        trends = {
            'spending_trajectory': self._predict_spending_trajectory(metrics),
            'debt_accumulation': self._predict_debt_accumulation(metrics),
            'satisfaction_evolution': self._predict_satisfaction_evolution(metrics),
            'behavior_change_probability': self._predict_behavior_change(metrics)
        }
        
        return trends
    
    def _assess_alienation_correlation(self, metrics: ConsumerBehaviorMetrics) -> Dict[str, float]:
        """评估与消费异化的相关性"""
        # 消费异化相关性
        alienation_correlation = (
            metrics.impulse_purchase_ratio * 0.3 +
            metrics.status_purchase_ratio * 0.25 +
            metrics.emotional_purchase_ratio * 0.25 +
            metrics.debt_to_income_ratio * 0.2
        )
        
        return {
            'consumption_alienation_correlation': alienation_correlation,
            'alienation_risk_level': self._determine_alienation_risk_level(alienation_correlation),
            'materialism_indicators': self._identify_materialism_indicators(metrics)
        }
    
    def _identify_primary_consumption_type(self, metrics: ConsumerBehaviorMetrics) -> str:
        """识别主要消费类型"""
        purchase_types = {
            '实用性消费': metrics.utility_purchase_ratio,
            '情感性消费': metrics.emotional_purchase_ratio,
            '地位性消费': metrics.status_purchase_ratio,
            '冲动性消费': metrics.impulse_purchase_ratio
        }
        
        return max(purchase_types, key=purchase_types.get)
    
    def _assess_consumption_balance(self, metrics: ConsumerBehaviorMetrics) -> str:
        """评估消费平衡性"""
        # 计算消费类型的多样性
        consumption_scores = [
            metrics.utility_purchase_ratio,
            metrics.emotional_purchase_ratio,
            metrics.status_purchase_ratio,
            metrics.impulse_purchase_ratio
        ]
        
        # 计算标准差衡量平衡性
        std_dev = np.std(consumption_scores)
        
        if std_dev < 0.1:
            return '高度平衡'
        elif std_dev < 0.2:
            return '相对平衡'
        elif std_dev < 0.3:
            return '轻度失衡'
        else:
            return '严重失衡'
    
    def _assess_consumption_intensity(self, metrics: ConsumerBehaviorMetrics) -> str:
        """评估消费强度"""
        intensity_score = (
            metrics.purchase_frequency * 0.3 +
            metrics.average_spending * 0.3 +
            metrics.impulse_purchase_ratio * 0.2 +
            metrics.debt_to_income_ratio * 0.2
        )
        
        if intensity_score > 0.7:
            return '高强度'
        elif intensity_score > 0.5:
            return '中等强度'
        elif intensity_score > 0.3:
            return '低强度'
        else:
            return '极低强度'
    
    def _assess_consumption_sustainability(self, metrics: ConsumerBehaviorMetrics) -> str:
        """评估消费可持续性"""
        sustainability_score = (
            (1 - metrics.debt_to_income_ratio) * 0.4 +
            metrics.utility_purchase_ratio * 0.3 +
            (1 - metrics.impulse_purchase_ratio) * 0.2 +
            metrics.price_sensitivity * 0.1
        )
        
        if sustainability_score > 0.7:
            return '高度可持续'
        elif sustainability_score > 0.5:
            return '中等可持续'
        elif sustainability_score > 0.3:
            return '低可持续'
        else:
            return '不可持续'
    
    def _identify_dominant_motivation(self, metrics: ConsumerBehaviorMetrics) -> str:
        """识别主导动机"""
        motivations = {
            '实用性': metrics.utility_purchase_ratio,
            '情感性': metrics.emotional_purchase_ratio,
            '地位性': metrics.status_purchase_ratio,
            '冲动性': metrics.impulse_purchase_ratio
        }
        
        return max(motivations, key=motivations.get)
    
    def _determine_rationality_level(self, rationality: float) -> str:
        """确定理性水平"""
        if rationality > 0.8:
            return '高度理性'
        elif rationality > 0.6:
            return '理性'
        elif rationality > 0.4:
            return '一般理性'
        else:
            return '非理性'
    
    def _identify_irrational_indicators(self, metrics: ConsumerBehaviorMetrics) -> List[str]:
        """识别非理性指标"""
        indicators = []
        
        if metrics.impulse_purchase_ratio > 0.5:
            indicators.append('冲动购买比例过高')
        if metrics.status_purchase_ratio > 0.4:
            indicators.append('地位性消费过多')
        if metrics.debt_to_income_ratio > 0.3:
            indicators.append('债务负担过重')
        if metrics.emotional_purchase_ratio > 0.5:
            indicators.append('情感性消费过度')
        if metrics.brand_loyalty > 0.8:
            indicators.append('品牌盲从严重')
        
        return indicators
    
    def _suggest_rational_strategies(self, metrics: ConsumerBehaviorMetrics) -> List[str]:
        """建议理性策略"""
        strategies = []
        
        if metrics.impulse_purchase_ratio > 0.3:
            strategies.append('建立购买冷却期，避免冲动购买')
        if metrics.status_purchase_ratio > 0.3:
            strategies.append('重新评估消费动机，减少地位性消费')
        if metrics.emotional_purchase_ratio > 0.4:
            strategies.append('寻找非消费性的情感满足方式')
        if metrics.debt_to_income_ratio > 0.2:
            strategies.append('制定债务偿还计划，控制新债务')
        if metrics.brand_loyalty > 0.7:
            strategies.append('比较不同品牌，做出理性选择')
        
        return strategies
    
    def _determine_pressure_level(self, pressure: float) -> str:
        """确定压力水平"""
        if pressure > 0.7:
            return '高压力'
        elif pressure > 0.5:
            return '中等压力'
        elif pressure > 0.3:
            return '低压力'
        else:
            return '无压力'
    
    def _identify_pressure_sources(self, indicators: Dict[str, float]) -> List[str]:
        """识别压力来源"""
        sources = []
        
        for pressure_type, score in indicators.items():
            if score > 0.6:
                if pressure_type == 'financial_pressure':
                    sources.append('经济压力')
                elif pressure_type == 'social_pressure':
                    sources.append('社会压力')
                elif pressure_type == 'emotional_pressure':
                    sources.append('情感压力')
                elif pressure_type == 'impulse_pressure':
                    sources.append('冲动压力')
        
        return sources
    
    def _predict_spending_trajectory(self, metrics: ConsumerBehaviorMetrics) -> str:
        """预测消费轨迹"""
        # 基于当前消费模式预测趋势
        trend_factors = (
            metrics.purchase_frequency * 0.3 +
            metrics.impulse_purchase_ratio * 0.3 +
            metrics.average_spending * 0.2 +
            metrics.debt_to_income_ratio * 0.2
        )
        
        if trend_factors > 0.6:
            return '上升趋势'
        elif trend_factors > 0.4:
            return '稳定趋势'
        else:
            return '下降趋势'
    
    def _predict_debt_accumulation(self, metrics: ConsumerBehaviorMetrics) -> str:
        """预测债务累积"""
        if metrics.debt_to_income_ratio > 0.5:
            return '快速累积'
        elif metrics.debt_to_income_ratio > 0.3:
            return '缓慢累积'
        elif metrics.debt_to_income_ratio > 0.1:
            return '稳定累积'
        else:
            return '债务减少'
    
    def _predict_satisfaction_evolution(self, metrics: ConsumerBehaviorMetrics) -> str:
        """预测满意度变化"""
        if metrics.shopping_satisfaction > 0.6:
            return '满意度上升'
        elif metrics.shopping_satisfaction > 0.4:
            return '满意度稳定'
        else:
            return '满意度下降'
    
    def _predict_behavior_change(self, metrics: ConsumerBehaviorMetrics) -> float:
        """预测行为改变概率"""
        # 基于不理性指标预测改变概率
        irrational_score = (
            metrics.impulse_purchase_ratio * 0.3 +
            metrics.status_purchase_ratio * 0.25 +
            metrics.emotional_purchase_ratio * 0.25 +
            metrics.debt_to_income_ratio * 0.2
        )
        
        return min(0.9, max(0.1, irrational_score * 1.2))
    
    def _determine_alienation_level(self, alienation: float) -> str:
        """确定异化水平"""
        if alienation >= self.alienation_thresholds['high_alienation']:
            return '高度异化'
        elif alienation >= self.alienation_thresholds['moderate_alienation']:
            return '中度异化'
        elif alienation >= self.alienation_thresholds['low_alienation']:
            return '轻度异化'
        else:
            return '最小异化'
    
    def _determine_alienation_risk_level(self, risk: float) -> str:
        """确定异化风险等级"""
        if risk >= self.alienation_thresholds['high_alienation']:
            return '高风险'
        elif risk >= self.alienation_thresholds['moderate_alienation']:
            return '中等风险'
        elif risk >= self.alienation_thresholds['low_alienation']:
            return '低风险'
        else:
            return '极低风险'
    
    def _identify_materialism_indicators(self, metrics: ConsumerBehaviorMetrics) -> List[str]:
        """识别物质主义指标"""
        indicators = []
        
        if metrics.status_purchase_ratio > 0.4:
            indicators.append('过度追求地位性消费')
        if metrics.brand_loyalty > 0.7:
            indicators.append('品牌盲从严重')
        if metrics.impulse_purchase_ratio > 0.4:
            indicators.append('冲动购买频繁')
        if metrics.emotional_purchase_ratio > 0.5:
            indicators.append('通过消费寻求情感满足')
        if metrics.debt_to_income_ratio > 0.3:
            indicators.append('债务负担过重')
        
        return indicators
    
    def _generate_intervention_recommendations(self, metrics: ConsumerBehaviorMetrics) -> List[str]:
        """生成干预建议"""
        recommendations = []
        
        if metrics.impulse_purchase_ratio > 0.3:
            recommendations.append('建立购买延迟机制，控制冲动购买')
        if metrics.status_purchase_ratio > 0.3:
            recommendations.append('重新评估消费价值观，减少地位性消费')
        if metrics.emotional_purchase_ratio > 0.4:
            recommendations.append('发展非消费性的情感满足方式')
        if metrics.debt_to_income_ratio > 0.2:
            recommendations.append('制定债务管理计划，优先偿还高利息债务')
        if metrics.brand_loyalty > 0.6:
            recommendations.append('比较购物，理性选择性价比高的产品')
        if metrics.price_sensitivity < 0.4:
            recommendations.append('增强价格意识，关注产品性价比')
        
        return recommendations
    
    def batch_analyze_consumer_behavior(self, behavior_dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量分析消费行为"""
        if not behavior_dataset:
            return {'error': '消费数据为空'}
        
        results = []
        for data in behavior_dataset:
            result = self.analyze_consumer_behavior(data)
            results.append(result)
        
        # 计算统计汇总
        alienation_scores = [r['alienation_score'] for r in results]
        
        # 按消费者类型统计
        segment_statistics = {}
        for result in results:
            segment = result['consumer_segment']
            if segment not in segment_statistics:
                segment_statistics[segment] = []
            segment_statistics[segment].append(result['alienation_score'])
        
        return {
            'individual_analyses': results,
            'overall_statistics': {
                'mean_alienation_score': np.mean(alienation_scores),
                'median_alienation_score': np.median(alienation_scores),
                'std_alienation_score': np.std(alienation_scores),
                'high_alienation_count': sum(1 for s in alienation_scores if s >= 0.70),
                'low_alienation_count': sum(1 for s in alienation_scores if s < 0.30),
                'total_analyzed': len(behavior_dataset)
            },
            'segment_statistics': {
                segment: {
                    'mean_alienation': np.mean(scores),
                    'count': len(scores)
                } for segment, scores in segment_statistics.items()
            },
            'analysis_timestamp': datetime.now().isoformat()
        }


def main():
    """主函数 - 用于测试"""
    analyzer = ConsumerBehaviorAnalyzer()
    
    # 测试数据
    test_data = {
        'metrics': {
            'purchase_frequency': 0.6,
            'average_spending': 0.7,
            'impulse_purchase_ratio': 0.3,
            'utility_purchase_ratio': 0.5,
            'status_purchase_ratio': 0.2,
            'emotional_purchase_ratio': 0.4,
            'price_sensitivity': 0.6,
            'brand_loyalty': 0.7,
            'shopping_satisfaction': 0.5,
            'debt_to_income_ratio': 0.15
        }
    }
    
    # 分析消费行为
    result = analyzer.analyze_consumer_behavior(test_data)
    
    # 打印结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()