#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
物质主义评估器
评估个体的物质主义价值观和物质追求程度
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json


class MaterialismDimension(Enum):
    """物质主义维度"""
    ACQUISITION_ORIENTATION = "acquisition"    # 获取导向
    POSSESSION_FOCUS = "possession"            # 占有聚焦
    DEFINING_SUCCESS = "success"               # 成功定义


@dataclass
class MaterialismMetrics:
    """物质主义指标数据类"""
    acquisition_importance: float       # 获取的重要性
    possession_satisfaction: float      # 占有带来的满足感
    success_definitions: float          # 成功定义标准
    material_aspiration: float         # 物质追求欲望
    consumer_attitudes: float          # 消费态度
    wealth_importance: float           # 财富重要性
    status_through_ownership: float    # 通过拥有获得地位
    happiness_correlation: float       # 物质与幸福的关联度
    self_esteem_correlation: float     # 物质与自尊的关联度
    life_satisfaction_correlation: float  # 物质与生活满意度的关联度


class MaterialismAssessment:
    """物质主义评估器"""
    
    def __init__(self):
        self.materialism_weights = {
            'acquisition_importance': 0.15,
            'possession_satisfaction': 0.12,
            'success_definitions': 0.15,
            'material_aspiration': 0.12,
            'consumer_attitudes': 0.10,
            'wealth_importance': 0.12,
            'status_through_ownership': 0.10,
            'happiness_correlation': 0.05,
            'self_esteem_correlation': 0.05,
            'life_satisfaction_correlation': 0.04
        }
        
        self.materialism_thresholds = {
            'high_materialism': 0.75,
            'moderate_materialism': 0.55,
            'low_materialism': 0.35,
            'minimal_materialism': 0.20
        }
        
        self.assessment_dimensions = {
            'acquisition_orientation': [
                'acquisition_importance', 'material_aspiration', 'wealth_importance'
            ],
            'possession_focus': [
                'possession_satisfaction', 'status_through_ownership'
            ],
            'defining_success': [
                'success_definitions', 'consumer_attitudes'
            ]
        }
    
    def assess_materialism(self, materialism_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估物质主义程度
        
        Args:
            materialism_data: 物质主义数据字典
            
        Returns:
            评估结果字典
        """
        # 解析数据
        metrics_data = materialism_data.get('metrics', {})
        questionnaire_responses = materialism_data.get('questionnaire_responses', [])
        behavioral_indicators = materialism_data.get('behavioral_indicators', {})
        
        # 创建物质主义指标
        metrics = self._create_materialism_metrics(metrics_data)
        
        # 计算综合物质主义分数
        materialism_score = self._calculate_materialism_score(metrics)
        
        # 分析物质主义维度
        dimension_analysis = self._analyze_materialism_dimensions(metrics)
        
        # 评估物质主义水平
        materialism_level = self._assess_materialism_level(materialism_score)
        
        # 分析价值观取向
        value_orientation = self._analyze_value_orientation(metrics)
        
        # 评估与幸福的关系
        happiness_relationship = self._assess_happiness_relationship(metrics)
        
        # 分析消费行为相关性
        consumption_correlation = self._analyze_consumption_correlation(metrics)
        
        # 预测物质主义发展
        materialism_evolution = self._predict_materialism_evolution(metrics)
        
        # 评估与消费异化的相关性
        alienation_correlation = self._assess_alienation_correlation(metrics)
        
        return {
            'materialism_score': materialism_score,
            'materialism_level': materialism_level,
            'dimension_analysis': dimension_analysis,
            'value_orientation': value_orientation,
            'happiness_relationship': happiness_relationship,
            'consumption_correlation': consumption_correlation,
            'materialism_evolution': materialism_evolution,
            'alienation_correlation': alienation_correlation,
            'intervention_suggestions': self._generate_intervention_suggestions(metrics),
            'assessment_timestamp': datetime.now().isoformat()
        }
    
    def _create_materialism_metrics(self, data: Dict[str, float]) -> MaterialismMetrics:
        """创建物质主义指标"""
        # 设置默认值
        default_values = {
            'acquisition_importance': 0.5,
            'possession_satisfaction': 0.5,
            'success_definitions': 0.5,
            'material_aspiration': 0.5,
            'consumer_attitudes': 0.5,
            'wealth_importance': 0.5,
            'status_through_ownership': 0.5,
            'happiness_correlation': 0.5,
            'self_esteem_correlation': 0.5,
            'life_satisfaction_correlation': 0.5
        }
        
        # 合并数据
        merged_data = {**default_values, **data}
        
        return MaterialismMetrics(**merged_data)
    
    def _calculate_materialism_score(self, metrics: MaterialismMetrics) -> float:
        """计算综合物质主义分数"""
        weights = self.materialism_weights
        values = [
            metrics.acquisition_importance * weights['acquisition_importance'],
            metrics.possession_satisfaction * weights['possession_satisfaction'],
            metrics.success_definitions * weights['success_definitions'],
            metrics.material_aspiration * weights['material_aspiration'],
            metrics.consumer_attitudes * weights['consumer_attitudes'],
            metrics.wealth_importance * weights['wealth_importance'],
            metrics.status_through_ownership * weights['status_through_ownership'],
            metrics.happiness_correlation * weights['happiness_correlation'],
            metrics.self_esteem_correlation * weights['self_esteem_correlation'],
            metrics.life_satisfaction_correlation * weights['life_satisfaction_correlation']
        ]
        
        return sum(values)
    
    def _analyze_materialism_dimensions(self, metrics: MaterialismMetrics) -> Dict[str, float]:
        """分析物质主义维度"""
        dimensions = {}
        
        for dimension, indicators in self.assessment_dimensions.items():
            dimension_score = np.mean([
                getattr(metrics, indicator) for indicator in indicators
            ])
            dimensions[dimension] = dimension_score
        
        return dimensions
    
    def _assess_materialism_level(self, materialism_score: float) -> str:
        """评估物质主义水平"""
        if materialism_score >= self.materialism_thresholds['high_materialism']:
            return '高度物质主义'
        elif materialism_score >= self.materialism_thresholds['moderate_materialism']:
            return '中等物质主义'
        elif materialism_score >= self.materialism_thresholds['low_materialism']:
            return '轻度物质主义'
        else:
            return '最低物质主义'
    
    def _analyze_value_orientation(self, metrics: MaterialismMetrics) -> Dict[str, Any]:
        """分析价值观取向"""
        # 分析物质价值与精神价值的比重
        material_orientation = (
            metrics.acquisition_importance * 0.3 +
            metrics.wealth_importance * 0.3 +
            metrics.success_definitions * 0.2 +
            metrics.status_through_ownership * 0.2
        )
        
        # 分析内在动机与外在动机
        intrinsic_motivation = 1 - (
            metrics.happiness_correlation * 0.4 +
            metrics.self_esteem_correlation * 0.3 +
            metrics.life_satisfaction_correlation * 0.3
        )
        
        return {
            'material_orientation_score': material_orientation,
            'intrinsic_motivation_score': intrinsic_motivation,
            'dominant_orientation': 'material' if material_orientation > 0.6 else 'balanced',
            'motivation_balance': self._assess_motivation_balance(intrinsic_motivation)
        }
    
    def _assess_happiness_relationship(self, metrics: MaterialismMetrics) -> Dict[str, Any]:
        """评估与幸福的关系"""
        # 计算物质与幸福的关联度
        happiness_indicators = {
            'happiness_correlation': metrics.happiness_correlation,
            'self_esteem_correlation': metrics.self_esteem_correlation,
            'life_satisfaction_correlation': metrics.life_satisfaction_correlation
        }
        
        avg_happiness_correlation = np.mean(list(happiness_indicators.values()))
        
        # 评估依赖程度
        dependence_level = self._assess_happiness_dependence(happiness_indicators)
        
        # 预测幸福影响
        happiness_impact = self._predict_happiness_impact(metrics)
        
        return {
            'happiness_correlation': avg_happiness_correlation,
            'happiness_dependence_level': dependence_level,
            'happiness_impact_prediction': happiness_impact,
            'wellbeing_risk_factors': self._identify_wellbeing_risks(happiness_indicators)
        }
    
    def _analyze_consumption_correlation(self, metrics: MaterialismMetrics) -> Dict[str, Any]:
        """分析与消费的关系"""
        # 计算消费导向程度
        consumption_orientation = (
            metrics.consumer_attitudes * 0.4 +
            metrics.status_through_ownership * 0.3 +
            metrics.possession_satisfaction * 0.3
        )
        
        # 评估消费动机
        consumption_motivations = {
            'status_motivation': metrics.status_through_ownership,
            'satisfaction_motivation': metrics.possession_satisfaction,
            'acquisition_motivation': metrics.acquisition_importance
        }
        
        return {
            'consumption_orientation': consumption_orientation,
            'consumption_motivations': consumption_motivations,
            'consumption_risk_level': self._assess_consumption_risk(consumption_orientation)
        }
    
    def _predict_materialism_evolution(self, metrics: MaterialismMetrics) -> Dict[str, Any]:
        """预测物质主义发展"""
        # 基于当前指标预测发展趋势
        evolution_factors = {
            'material_aspiration': metrics.material_aspiration,
            'success_definitions': metrics.success_definitions,
            'wealth_importance': metrics.wealth_importance
        }
        
        # 计算发展趋势
        evolution_score = np.mean(list(evolution_factors.values()))
        
        # 预测风险因素
        risk_factors = self._identify_materialism_risks(metrics)
        
        return {
            'evolution_trend': self._determine_evolution_trend(evolution_score),
            'evolution_score': evolution_score,
            'risk_factors': risk_factors,
            'intervention_timing': self._determine_intervention_timing(evolution_score)
        }
    
    def _assess_alienation_correlation(self, metrics: MaterialismMetrics) -> Dict[str, float]:
        """评估与消费异化的相关性"""
        # 物质主义与消费异化的强相关性
        alienation_correlation = (
            metrics.acquisition_importance * 0.25 +
            metrics.possession_satisfaction * 0.20 +
            metrics.success_definitions * 0.20 +
            metrics.material_aspiration * 0.15 +
            metrics.status_through_ownership * 0.20
        )
        
        return {
            'materialism_alienation_correlation': alienation_correlation,
            'alienation_risk_level': self._determine_alienation_risk_level(alienation_correlation),
            'materialism_indicators': self._identify_materialism_indicators(metrics)
        }
    
    def _assess_motivation_balance(self, intrinsic_motivation: float) -> str:
        """评估动机平衡"""
        if intrinsic_motivation > 0.7:
            return '内在动机主导'
        elif intrinsic_motivation > 0.5:
            return '动机平衡'
        elif intrinsic_motivation > 0.3:
            return '外在动机偏重'
        else:
            return '外在动机主导'
    
    def _assess_happiness_dependence(self, happiness_indicators: Dict[str, float]) -> str:
        """评估幸福依赖程度"""
        avg_correlation = np.mean(list(happiness_indicators.values()))
        
        if avg_correlation > 0.7:
            return '高度依赖'
        elif avg_correlation > 0.5:
            return '中等依赖'
        elif avg_correlation > 0.3:
            return '轻度依赖'
        else:
            return '低度依赖'
    
    def _predict_happiness_impact(self, metrics: MaterialismMetrics) -> str:
        """预测对幸福的影响"""
        # 基于物质主义指标预测影响
        negative_indicators = (
            metrics.happiness_correlation * 0.3 +
            metrics.self_esteem_correlation * 0.3 +
            metrics.life_satisfaction_correlation * 0.4
        )
        
        if negative_indicators > 0.6:
            return '负面影响'
        elif negative_indicators > 0.4:
            return '中性影响'
        else:
            return '正面影响'
    
    def _identify_wellbeing_risks(self, happiness_indicators: Dict[str, float]) -> List[str]:
        """识别幸福风险因素"""
        risks = []
        
        for indicator, score in happiness_indicators.items():
            if score > 0.6:
                if 'happiness' in indicator:
                    risks.append('过度依赖物质获得幸福')
                elif 'self_esteem' in indicator:
                    risks.append('自尊心过度依赖物质')
                elif 'satisfaction' in indicator:
                    risks.append('生活满意度过度依赖物质')
        
        return risks
    
    def _assess_consumption_risk(self, consumption_orientation: float) -> str:
        """评估消费风险"""
        if consumption_orientation > 0.7:
            return '高风险'
        elif consumption_orientation > 0.5:
            return '中等风险'
        elif consumption_orientation > 0.3:
            return '低风险'
        else:
            return '极低风险'
    
    def _identify_materialism_risks(self, metrics: MaterialismMetrics) -> List[str]:
        """识别物质主义风险因素"""
        risks = []
        
        if metrics.material_aspiration > 0.7:
            risks.append('物质欲望过高')
        if metrics.success_definitions > 0.7:
            risks.append('成功定义过于物质化')
        if metrics.wealth_importance > 0.7:
            risks.append('对财富过度重视')
        if metrics.status_through_ownership > 0.6:
            risks.append('通过拥有获得地位的风险')
        if metrics.happiness_correlation > 0.6:
            risks.append('幸福过度依赖物质')
        
        return risks
    
    def _determine_evolution_trend(self, evolution_score: float) -> str:
        """确定发展趋势"""
        if evolution_score > 0.7:
            return '物质主义增强趋势'
        elif evolution_score > 0.5:
            return '物质主义稳定趋势'
        elif evolution_score > 0.3:
            return '物质主义减弱趋势'
        else:
            return '物质主义下降趋势'
    
    def _determine_intervention_timing(self, evolution_score: float) -> str:
        """确定干预时机"""
        if evolution_score > 0.8:
            return '急需干预'
        elif evolution_score > 0.6:
            return '近期干预'
        elif evolution_score > 0.4:
            return '中期关注'
        else:
            return '持续观察'
    
    def _determine_alienation_risk_level(self, risk: float) -> str:
        """确定异化风险等级"""
        if risk >= self.materialism_thresholds['high_materialism']:
            return '高风险'
        elif risk >= self.materialism_thresholds['moderate_materialism']:
            return '中等风险'
        elif risk >= self.materialism_thresholds['low_materialism']:
            return '低风险'
        else:
            return '极低风险'
    
    def _identify_materialism_indicators(self, metrics: MaterialismMetrics) -> List[str]:
        """识别物质主义指标"""
        indicators = []
        
        if metrics.acquisition_importance > 0.6:
            indicators.append('过度重视物质获取')
        if metrics.possession_satisfaction > 0.6:
            indicators.append('过度依赖占有获得满足')
        if metrics.success_definitions > 0.6:
            indicators.append('成功定义过于物质化')
        if metrics.material_aspiration > 0.6:
            indicators.append('物质欲望过高')
        if metrics.status_through_ownership > 0.6:
            indicators.append('通过拥有获得地位')
        if metrics.wealth_importance > 0.6:
            indicators.append('对财富过度重视')
        if metrics.happiness_correlation > 0.6:
            indicators.append('幸福过度依赖物质')
        
        return indicators
    
    def _generate_intervention_suggestions(self, metrics: MaterialismMetrics) -> List[str]:
        """生成干预建议"""
        suggestions = []
        
        if metrics.acquisition_importance > 0.6:
            suggestions.append('重新评估获取物质的重要性，关注非物质价值')
        if metrics.possession_satisfaction > 0.6:
            suggestions.append('寻找非占有性的满足方式，如精神追求和人际关系')
        if metrics.success_definitions > 0.6:
            suggestions.append('重新定义成功标准，增加内在价值和精神成就')
        if metrics.material_aspiration > 0.6:
            suggestions.append('控制物质欲望，培养知足常乐的心态')
        if metrics.wealth_importance > 0.6:
            suggestions.append('重新认识财富的意义，注重精神财富的积累')
        if metrics.status_through_ownership > 0.6:
            suggestions.append('建立基于内在品质的自尊，减少对外在物质的依赖')
        if metrics.happiness_correlation > 0.6:
            suggestions.append('发展多样化的幸福来源，如人际关系、个人成长、贡献社会')
        
        return suggestions
    
    def batch_assess_materialism(self, materialism_dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量评估物质主义"""
        if not materialism_dataset:
            return {'error': '物质主义数据为空'}
        
        results = []
        for data in materialism_dataset:
            result = self.assess_materialism(data)
            results.append(result)
        
        # 计算统计汇总
        materialism_scores = [r['materialism_score'] for r in results]
        
        # 按物质主义水平统计
        level_statistics = {}
        for result in results:
            level = result['materialism_level']
            if level not in level_statistics:
                level_statistics[level] = []
            level_statistics[level].append(result['materialism_score'])
        
        return {
            'individual_assessments': results,
            'overall_statistics': {
                'mean_materialism_score': np.mean(materialism_scores),
                'median_materialism_score': np.median(materialism_scores),
                'std_materialism_score': np.std(materialism_scores),
                'high_materialism_count': sum(1 for s in materialism_scores if s >= 0.75),
                'low_materialism_count': sum(1 for s in materialism_scores if s < 0.35),
                'total_assessed': len(materialism_dataset)
            },
            'level_statistics': {
                level: {
                    'mean_score': np.mean(scores),
                    'count': len(scores)
                } for level, scores in level_statistics.items()
            },
            'assessment_timestamp': datetime.now().isoformat()
        }


def main():
    """主函数 - 用于测试"""
    assessor = MaterialismAssessment()
    
    # 测试数据
    test_data = {
        'metrics': {
            'acquisition_importance': 0.6,
            'possession_satisfaction': 0.5,
            'success_definitions': 0.7,
            'material_aspiration': 0.6,
            'consumer_attitudes': 0.6,
            'wealth_importance': 0.7,
            'status_through_ownership': 0.5,
            'happiness_correlation': 0.6,
            'self_esteem_correlation': 0.5,
            'life_satisfaction_correlation': 0.4
        }
    }
    
    # 评估物质主义
    result = assessor.assess_materialism(test_data)
    
    # 打印结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()