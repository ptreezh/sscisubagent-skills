#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数字幸福感评估器
评估个体在数字化生活中的幸福感和生活质量
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json


class WellbeingDimension(Enum):
    """幸福感维度"""
    PSYCHOLOGICAL = "psychological"    # 心理幸福感
    SOCIAL = "social"                  # 社交幸福感
    PHYSICAL = "physical"             # 身体健康
    ENVIRONMENTAL = "environmental"    # 环境适应
    PURPOSE = "purpose"               # 生活目标


@dataclass
class DigitalWellbeingMetrics:
    """数字幸福感指标数据类"""
    life_satisfaction: float          # 生活满意度
    digital_stress_level: float       # 数字压力水平
    work_life_balance: float          # 工作生活平衡
    social_connection_quality: float  # 社交连接质量
    digital_sleep_quality: float      # 数字睡眠质量
    physical_health_impact: float     # 身体健康影响
    mental_health_impact: float       # 心理健康影响
    digital_literacy: float           # 数字素养
    privacy_satisfaction: float       # 隐私满意度
    technology_control: float         # 技术控制感
    digital_identity_clarity: float   # 数字身份清晰度
    online_offline_balance: float     # 线上线下平衡


class DigitalWellbeingEvaluator:
    """数字幸福感评估器"""
    
    def __init__(self):
        self.wellbeing_weights = {
            'life_satisfaction': 0.12,
            'digital_stress_level': 0.10,
            'work_life_balance': 0.10,
            'social_connection_quality': 0.10,
            'digital_sleep_quality': 0.08,
            'physical_health_impact': 0.08,
            'mental_health_impact': 0.10,
            'digital_literacy': 0.05,
            'privacy_satisfaction': 0.05,
            'technology_control': 0.08,
            'digital_identity_clarity': 0.07,
            'online_offline_balance': 0.07
        }
        
        self.wellbeing_thresholds = {
            'excellent_wellbeing': 0.80,
            'good_wellbeing': 0.65,
            'moderate_wellbeing': 0.50,
            'poor_wellbeing': 0.35,
            'very_poor_wellbeing': 0.20
        }
        
        self.wellbeing_dimensions = {
            'psychological': [
                'life_satisfaction', 'digital_stress_level', 'mental_health_impact'
            ],
            'social': [
                'social_connection_quality', 'online_offline_balance'
            ],
            'physical': [
                'digital_sleep_quality', 'physical_health_impact'
            ],
            'environmental': [
                'work_life_balance', 'technology_control'
            ],
            'purpose': [
                'digital_identity_clarity', 'digital_literacy'
            ]
        }
    
    def evaluate_digital_wellbeing(self, wellbeing_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估数字幸福感
        
        Args:
            wellbeing_data: 幸福感数据字典
            
        Returns:
            评估结果字典
        """
        # 解析数据
        metrics_data = wellbeing_data.get('metrics', {})
        lifestyle_data = wellbeing_data.get('lifestyle_data', {})
        health_data = wellbeing_data.get('health_data', {})
        
        # 创建数字幸福感指标
        metrics = self._create_wellbeing_metrics(metrics_data)
        
        # 计算综合幸福感分数
        wellbeing_score = self._calculate_wellbeing_score(metrics)
        
        # 分析幸福感维度
        dimension_analysis = self._analyze_wellbeing_dimensions(metrics)
        
        # 评估幸福感水平
        wellbeing_level = self._assess_wellbeing_level(wellbeing_score)
        
        # 分析数字生活平衡
        digital_balance = self._analyze_digital_balance(metrics)
        
        # 识别幸福感风险因素
        risk_factors = self._identify_wellbeing_risks(metrics)
        
        # 评估数字化适应能力
        adaptation_assessment = self._assess_digital_adaptation(metrics)
        
        # 预测幸福感发展
        wellbeing_trends = self._predict_wellbeing_trends(metrics)
        
        # 评估与异化的关系
        alienation_correlation = self._assess_alienation_correlation(metrics)
        
        return {
            'wellbeing_score': wellbeing_score,
            'wellbeing_level': wellbeing_level,
            'dimension_analysis': dimension_analysis,
            'digital_balance': digital_balance,
            'risk_factors': risk_factors,
            'adaptation_assessment': adaptation_assessment,
            'wellbeing_trends': wellbeing_trends,
            'alienation_correlation': alienation_correlation,
            'improvement_recommendations': self._generate_improvement_recommendations(metrics),
            'evaluation_timestamp': datetime.now().isoformat()
        }
    
    def _create_wellbeing_metrics(self, data: Dict[str, float]) -> DigitalWellbeingMetrics:
        """创建数字幸福感指标"""
        # 设置默认值
        default_values = {
            'life_satisfaction': 0.6,
            'digital_stress_level': 0.4,
            'work_life_balance': 0.6,
            'social_connection_quality': 0.6,
            'digital_sleep_quality': 0.6,
            'physical_health_impact': 0.3,
            'mental_health_impact': 0.3,
            'digital_literacy': 0.6,
            'privacy_satisfaction': 0.5,
            'technology_control': 0.5,
            'digital_identity_clarity': 0.5,
            'online_offline_balance': 0.6
        }
        
        # 合并数据
        merged_data = {**default_values, **data}
        
        # 特殊处理负相关指标
        merged_data['digital_stress_level'] = 1 - merged_data['digital_stress_level']
        merged_data['physical_health_impact'] = 1 - merged_data['physical_health_impact']
        merged_data['mental_health_impact'] = 1 - merged_data['mental_health_impact']
        
        return DigitalWellbeingMetrics(**merged_data)
    
    def _calculate_wellbeing_score(self, metrics: DigitalWellbeingMetrics) -> float:
        """计算综合幸福感分数"""
        weights = self.wellbeing_weights
        values = [
            metrics.life_satisfaction * weights['life_satisfaction'],
            metrics.digital_stress_level * weights['digital_stress_level'],
            metrics.work_life_balance * weights['work_life_balance'],
            metrics.social_connection_quality * weights['social_connection_quality'],
            metrics.digital_sleep_quality * weights['digital_sleep_quality'],
            metrics.physical_health_impact * weights['physical_health_impact'],
            metrics.mental_health_impact * weights['mental_health_impact'],
            metrics.digital_literacy * weights['digital_literacy'],
            metrics.privacy_satisfaction * weights['privacy_satisfaction'],
            metrics.technology_control * weights['technology_control'],
            metrics.digital_identity_clarity * weights['digital_identity_clarity'],
            metrics.online_offline_balance * weights['online_offline_balance']
        ]
        
        return sum(values)
    
    def _analyze_wellbeing_dimensions(self, metrics: DigitalWellbeingMetrics) -> Dict[str, float]:
        """分析幸福感维度"""
        dimensions = {}
        
        for dimension, indicators in self.wellbeing_dimensions.items():
            dimension_score = np.mean([
                getattr(metrics, indicator) for indicator in indicators
            ])
            dimensions[dimension] = dimension_score
        
        return dimensions
    
    def _assess_wellbeing_level(self, wellbeing_score: float) -> str:
        """评估幸福感水平"""
        if wellbeing_score >= self.wellbeing_thresholds['excellent_wellbeing']:
            return '优秀幸福感'
        elif wellbeing_score >= self.wellbeing_thresholds['good_wellbeing']:
            return '良好幸福感'
        elif wellbeing_score >= self.wellbeing_thresholds['moderate_wellbeing']:
            return '中等幸福感'
        elif wellbeing_score >= self.wellbeing_thresholds['poor_wellbeing']:
            return '较差幸福感'
        else:
            return '很差幸福感'
    
    def _analyze_digital_balance(self, metrics: DigitalWellbeingMetrics) -> Dict[str, Any]:
        """分析数字生活平衡"""
        # 计算各维度平衡性
        balance_dimensions = {
            'work_life_balance': metrics.work_life_balance,
            'online_offline_balance': metrics.online_offline_balance,
            'social_connection_balance': metrics.social_connection_quality,
            'sleep_balance': metrics.digital_sleep_quality
        }
        
        # 计算总体平衡分数
        total_balance = np.mean(list(balance_dimensions.values()))
        
        # 识别平衡问题
        balance_issues = self._identify_balance_issues(balance_dimensions)
        
        return {
            'balance_dimensions': balance_dimensions,
            'total_balance_score': total_balance,
            'balance_level': self._assess_balance_level(total_balance),
            'balance_issues': balance_issues,
            'balance_recommendations': self._suggest_balance_improvements(balance_dimensions)
        }
    
    def _identify_wellbeing_risks(self, metrics: DigitalWellbeingMetrics) -> List[str]:
        """识别幸福感风险因素"""
        risks = []
        
        if metrics.digital_stress_level < 0.5:
            risks.append('数字压力过高')
        if metrics.work_life_balance < 0.5:
            risks.append('工作生活失衡')
        if metrics.social_connection_quality < 0.5:
            risks.append('社交连接质量差')
        if metrics.digital_sleep_quality < 0.5:
            risks.append('数字睡眠质量差')
        if metrics.physical_health_impact < 0.6:
            risks.append('身体健康受数字生活影响')
        if metrics.mental_health_impact < 0.6:
            risks.append('心理健康受数字生活影响')
        if metrics.technology_control < 0.4:
            risks.append('技术控制感不足')
        if metrics.online_offline_balance < 0.5:
            risks.append('线上线下平衡失调')
        
        return risks
    
    def _assess_digital_adaptation(self, metrics: DigitalWellbeingMetrics) -> Dict[str, Any]:
        """评估数字化适应能力"""
        # 计算适应能力分数
        adaptation_score = (
            metrics.digital_literacy * 0.3 +
            metrics.technology_control * 0.3 +
            metrics.digital_identity_clarity * 0.2 +
            metrics.privacy_satisfaction * 0.2
        )
        
        # 分析适应挑战
        adaptation_challenges = self._identify_adaptation_challenges(metrics)
        
        # 评估适应策略
        adaptation_strategies = self._suggest_adaptation_strategies(metrics)
        
        return {
            'adaptation_score': adaptation_score,
            'adaptation_level': self._determine_adaptation_level(adaptation_score),
            'adaptation_challenges': adaptation_challenges,
            'adaptation_strategies': adaptation_strategies
        }
    
    def _predict_wellbeing_trends(self, metrics: DigitalWellbeingMetrics) -> Dict[str, Any]:
        """预测幸福感发展趋势"""
        # 基于当前指标预测趋势
        trend_factors = {
            'positive_indicators': (
                metrics.life_satisfaction * 0.25 +
                metrics.work_life_balance * 0.20 +
                metrics.social_connection_quality * 0.20 +
                metrics.technology_control * 0.15 +
                metrics.digital_literacy * 0.20
            ),
            'negative_indicators': (
                (1 - metrics.digital_stress_level) * 0.3 +
                (1 - metrics.physical_health_impact) * 0.25 +
                (1 - metrics.mental_health_impact) * 0.25 +
                (1 - metrics.online_offline_balance) * 0.20
            )
        }
        
        # 计算趋势方向
        trend_direction = self._calculate_trend_direction(trend_factors)
        
        return {
            'trend_factors': trend_factors,
            'trend_direction': trend_direction,
            'wellbeing_trajectory': self._determine_wellbeing_trajectory(trend_factors),
            'intervention_timing': self._assess_intervention_timing(trend_factors)
        }
    
    def _assess_alienation_correlation(self, metrics: DigitalWellbeingMetrics) -> Dict[str, float]:
        """评估与异化的相关性"""
        # 数字幸福感与数字异化的负相关
        alienation_correlation = (
            (1 - metrics.life_satisfaction) * 0.20 +
            (1 - metrics.digital_stress_level) * 0.15 +
            (1 - metrics.work_life_balance) * 0.15 +
            (1 - metrics.social_connection_quality) * 0.15 +
            (1 - metrics.technology_control) * 0.15 +
            (1 - metrics.online_offline_balance) * 0.20
        )
        
        return {
            'digital_wellbeing_alienation_correlation': alienation_correlation,
            'alienation_risk_level': self._determine_alienation_risk_level(alienation_correlation),
            'wellbeing_protection_factors': self._identify_protection_factors(metrics)
        }
    
    def _identify_balance_issues(self, balance_dimensions: Dict[str, float]) -> List[str]:
        """识别平衡问题"""
        issues = []
        
        for dimension, score in balance_dimensions.items():
            if score < 0.5:
                if dimension == 'work_life_balance':
                    issues.append('工作生活失衡')
                elif dimension == 'online_offline_balance':
                    issues.append('线上线下失衡')
                elif dimension == 'social_connection_balance':
                    issues.append('社交连接失衡')
                elif dimension == 'sleep_balance':
                    issues.append('睡眠平衡失调')
        
        return issues
    
    def _assess_balance_level(self, balance_score: float) -> str:
        """评估平衡水平"""
        if balance_score > 0.7:
            return '高度平衡'
        elif balance_score > 0.6:
            return '良好平衡'
        elif balance_score > 0.5:
            return '一般平衡'
        elif balance_score > 0.4:
            return '轻度失衡'
        else:
            return '严重失衡'
    
    def _suggest_balance_improvements(self, balance_dimensions: Dict[str, float]) -> List[str]:
        """建议平衡改善"""
        suggestions = []
        
        if balance_dimensions['work_life_balance'] < 0.6:
            suggestions.append('建立明确的数字边界，设定工作时间和私人时间')
        if balance_dimensions['online_offline_balance'] < 0.6:
            suggestions.append('增加线下活动时间，培养非数字化兴趣爱好')
        if balance_dimensions['social_connection_balance'] < 0.6:
            suggestions.append('平衡线上线下社交，增加面对面交流')
        if balance_dimensions['sleep_balance'] < 0.6:
            suggestions.append('建立健康的数字睡眠习惯，避免睡前数字设备使用')
        
        return suggestions
    
    def _identify_adaptation_challenges(self, metrics: DigitalWellbeingMetrics) -> List[str]:
        """识别适应挑战"""
        challenges = []
        
        if metrics.digital_literacy < 0.5:
            challenges.append('数字素养不足')
        if metrics.technology_control < 0.4:
            challenges.append('技术控制能力不足')
        if metrics.digital_identity_clarity < 0.4:
            challenges.append('数字身份认知模糊')
        if metrics.privacy_satisfaction < 0.4:
            challenges.append('隐私保护满意度低')
        
        return challenges
    
    def _suggest_adaptation_strategies(self, metrics: DigitalWellbeingMetrics) -> List[str]:
        """建议适应策略"""
        strategies = []
        
        if metrics.digital_literacy < 0.6:
            strategies.append('提升数字技能和素养')
        if metrics.technology_control < 0.6:
            strategies.append('发展技术管理和控制技能')
        if metrics.digital_identity_clarity < 0.6:
            strategies.append('明确和建构个人数字身份')
        if metrics.privacy_satisfaction < 0.6:
            strategies.append('加强隐私保护意识和技能')
        
        return strategies
    
    def _determine_adaptation_level(self, adaptation_score: float) -> str:
        """确定适应水平"""
        if adaptation_score > 0.7:
            return '高度适应'
        elif adaptation_score > 0.6:
            return '良好适应'
        elif adaptation_score > 0.5:
            return '一般适应'
        elif adaptation_score > 0.4:
            return '轻度不适'
        else:
            return '严重不适'
    
    def _calculate_trend_direction(self, trend_factors: Dict[str, float]) -> str:
        """计算趋势方向"""
        positive = trend_factors['positive_indicators']
        negative = trend_factors['negative_indicators']
        
        if positive > 0.7 and negative > 0.7:
            return '持续改善'
        elif positive > 0.6 and negative > 0.6:
            return '稳步提升'
        elif positive > 0.5 and negative > 0.5:
            return '缓慢改善'
        elif positive < 0.4 and negative < 0.4:
            return '持续恶化'
        elif positive < 0.5 and negative < 0.5:
            return '稳步下降'
        else:
            return '波动状态'
    
    def _determine_wellbeing_trajectory(self, trend_factors: Dict[str, float]) -> str:
        """确定幸福感轨迹"""
        positive = trend_factors['positive_indicators']
        negative = trend_factors['negative_indicators']
        
        if positive > 0.6 and negative > 0.6:
            return '积极发展轨迹'
        elif positive > 0.4 and negative > 0.4:
            return '稳定发展轨迹'
        elif positive < 0.4 and negative < 0.4:
            return '消极发展轨迹'
        else:
            return '不稳定轨迹'
    
    def _assess_intervention_timing(self, trend_factors: Dict[str, float]) -> str:
        """评估干预时机"""
        positive = trend_factors['positive_indicators']
        negative = trend_factors['negative_indicators']
        
        if positive < 0.4 and negative < 0.4:
            return '急需干预'
        elif positive < 0.5 or negative < 0.5:
            return '重要干预'
        elif positive > 0.6 and negative > 0.6:
            return '预防性干预'
        else:
            return '持续关注'
    
    def _determine_alienation_risk_level(self, risk: float) -> str:
        """确定异化风险等级"""
        if risk >= self.wellbeing_thresholds['poor_wellbeing']:
            return '高风险'
        elif risk >= self.wellbeing_thresholds['moderate_wellbeing']:
            return '中等风险'
        elif risk >= self.wellbeing_thresholds['good_wellbeing']:
            return '低风险'
        else:
            return '极低风险'
    
    def _identify_protection_factors(self, metrics: DigitalWellbeingMetrics) -> List[str]:
        """识别保护因子"""
        factors = []
        
        if metrics.life_satisfaction > 0.7:
            factors.append('高度生活满意度')
        if metrics.work_life_balance > 0.7:
            factors.append('良好工作生活平衡')
        if metrics.social_connection_quality > 0.7:
            factors.append('优质社交连接')
        if metrics.technology_control > 0.6:
            factors.append('强技术控制感')
        if metrics.digital_literacy > 0.6:
            factors.append('高数字素养')
        if metrics.online_offline_balance > 0.6:
            factors.append('良好线上线下平衡')
        
        return factors
    
    def _generate_improvement_recommendations(self, metrics: DigitalWellbeingMetrics) -> List[str]:
        """生成改善建议"""
        recommendations = []
        
        if metrics.life_satisfaction < 0.6:
            recommendations.append('重新审视生活价值观，寻找生活意义和目标')
        if metrics.digital_stress_level < 0.6:
            recommendations.append('减少数字压力，建立健康的数字生活习惯')
        if metrics.work_life_balance < 0.6:
            recommendations.append('建立清晰的工作生活边界')
        if metrics.social_connection_quality < 0.6:
            recommendations.append('改善社交质量，培养深度人际关系')
        if metrics.digital_sleep_quality < 0.6:
            recommendations.append('改善数字睡眠习惯，建立健康的睡眠环境')
        if metrics.physical_health_impact < 0.7:
            recommendations.append('减少数字设备对身体健康的不良影响')
        if metrics.mental_health_impact < 0.7:
            recommendations.append('关注心理健康，培养积极的数字心态')
        if metrics.technology_control < 0.6:
            recommendations.append('增强技术控制能力，主动管理数字生活')
        if metrics.privacy_satisfaction < 0.6:
            recommendations.append('加强隐私保护，提升数字安全感')
        if metrics.digital_identity_clarity < 0.6:
            recommendations.append('明确和建构积极的数字身份')
        if metrics.online_offline_balance < 0.6:
            recommendations.append('平衡线上线下生活，增加真实世界体验')
        
        return recommendations
    
    def batch_evaluate_wellbeing(self, wellbeing_dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量评估数字幸福感"""
        if not wellbeing_dataset:
            return {'error': '幸福感数据为空'}
        
        results = []
        for data in wellbeing_dataset:
            result = self.evaluate_digital_wellbeing(data)
            results.append(result)
        
        # 计算统计汇总
        wellbeing_scores = [r['wellbeing_score'] for r in results]
        
        # 按幸福感水平统计
        level_statistics = {}
        for result in results:
            level = result['wellbeing_level']
            if level not in level_statistics:
                level_statistics[level] = []
            level_statistics[level].append(result['wellbeing_score'])
        
        return {
            'individual_evaluations': results,
            'overall_statistics': {
                'mean_wellbeing_score': np.mean(wellbeing_scores),
                'median_wellbeing_score': np.median(wellbeing_scores),
                'std_wellbeing_score': np.std(wellbeing_scores),
                'excellent_wellbeing_count': sum(1 for s in wellbeing_scores if s >= 0.80),
                'poor_wellbeing_count': sum(1 for s in wellbeing_scores if s < 0.35),
                'total_evaluated': len(wellbeing_dataset)
            },
            'level_statistics': {
                level: {
                    'mean_score': np.mean(scores),
                    'count': len(scores)
                } for level, scores in level_statistics.items()
            },
            'evaluation_timestamp': datetime.now().isoformat()
        }


def main():
    """主函数 - 用于测试"""
    evaluator = DigitalWellbeingEvaluator()
    
    # 测试数据
    test_data = {
        'metrics': {
            'life_satisfaction': 0.6,
            'digital_stress_level': 0.5,
            'work_life_balance': 0.6,
            'social_connection_quality': 0.7,
            'digital_sleep_quality': 0.5,
            'physical_health_impact': 0.7,
            'mental_health_impact': 0.6,
            'digital_literacy': 0.6,
            'privacy_satisfaction': 0.5,
            'technology_control': 0.5,
            'digital_identity_clarity': 0.6,
            'online_offline_balance': 0.5
        }
    }
    
    # 评估数字幸福感
    result = evaluator.evaluate_digital_wellbeing(test_data)
    
    # 打印结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()