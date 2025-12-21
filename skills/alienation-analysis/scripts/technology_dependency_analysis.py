#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术依赖分析器
分析个体对技术的依赖程度和技术异化状况
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json


class TechnologyType(Enum):
    """技术类型"""
    SMARTPHONE = "smartphone"
    SOCIAL_MEDIA = "social_media"
    GAMING = "gaming"
    WORK_TECH = "work_technology"
    SMART_HOME = "smart_home"
    AUTOMATION = "automation"


@dataclass
class TechnologyMetrics:
    """技术依赖指标数据类"""
    usage_frequency: float           # 使用频率
    usage_duration: float           # 使用时长
    dependency_severity: float      # 依赖严重程度
    function_loss_anxiety: float    # 功能缺失焦虑
    withdrawal_symptoms: float      # 戒断症状
    productivity_impact: float      # 对生产力的影响
    social_interaction_impact: float # 对社交的影响
    privacy_concerns: float         # 隐私担忧
    control_perception: float       # 控制感知
    technological_anxiety: float    # 技术焦虑


class TechnologyDependencyAnalyzer:
    """技术依赖分析器"""
    
    def __init__(self):
        self.dependency_weights = {
            'usage_frequency': 0.12,
            'usage_duration': 0.15,
            'dependency_severity': 0.20,
            'function_loss_anxiety': 0.12,
            'withdrawal_symptoms': 0.15,
            'productivity_impact': 0.08,
            'social_interaction_impact': 0.08,
            'privacy_concerns': 0.05,
            'control_perception': 0.03,
            'technological_anxiety': 0.02
        }
        
        self.dependency_thresholds = {
            'severe_dependency': 0.75,
            'moderate_dependency': 0.55,
            'mild_dependency': 0.35,
            'minimal_dependency': 0.20
        }
        
        self.technology_categories = {
            'communication_tech': ['smartphone', 'social_media'],
            'work_tech': ['work_technology'],
            'entertainment_tech': ['gaming'],
            'lifestyle_tech': ['smart_home', 'automation']
        }
    
    def analyze_technology_dependency(self, dependency_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析技术依赖
        
        Args:
            dependency_data: 技术依赖数据字典
            
        Returns:
            分析结果字典
        """
        # 解析数据
        overall_metrics = dependency_data.get('overall_metrics', {})
        category_metrics = dependency_data.get('category_metrics', {})
        behavioral_data = dependency_data.get('behavioral_data', {})
        
        # 创建技术依赖指标
        metrics = self._create_technology_metrics(overall_metrics)
        
        # 计算综合依赖分数
        dependency_score = self._calculate_dependency_score(metrics)
        
        # 分析依赖类型
        dependency_types = self._analyze_dependency_types(metrics)
        
        # 评估依赖严重程度
        dependency_level = self._assess_dependency_level(dependency_score)
        
        # 分析影响领域
        impact_analysis = self._analyze_dependency_impact(metrics)
        
        # 识别依赖模式
        dependency_patterns = self._identify_dependency_patterns(metrics)
        
        # 评估技术控制能力
        control_assessment = self._assess_technology_control(metrics)
        
        # 预测依赖发展
        dependency_evolution = self._predict_dependency_evolution(metrics)
        
        # 评估与技术异化的相关性
        alienation_correlation = self._assess_alienation_correlation(metrics)
        
        return {
            'dependency_score': dependency_score,
            'dependency_level': dependency_level,
            'dependency_types': dependency_types,
            'impact_analysis': impact_analysis,
            'dependency_patterns': dependency_patterns,
            'control_assessment': control_assessment,
            'dependency_evolution': dependency_evolution,
            'alienation_correlation': alienation_correlation,
            'intervention_recommendations': self._generate_intervention_recommendations(metrics),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _create_technology_metrics(self, data: Dict[str, float]) -> TechnologyMetrics:
        """创建技术依赖指标"""
        # 设置默认值
        default_values = {
            'usage_frequency': 0.5,
            'usage_duration': 0.5,
            'dependency_severity': 0.3,
            'function_loss_anxiety': 0.3,
            'withdrawal_symptoms': 0.2,
            'productivity_impact': 0.3,
            'social_interaction_impact': 0.3,
            'privacy_concerns': 0.4,
            'control_perception': 0.5,
            'technological_anxiety': 0.3
        }
        
        # 合并数据
        merged_data = {**default_values, **data}
        
        return TechnologyMetrics(**merged_data)
    
    def _calculate_dependency_score(self, metrics: TechnologyMetrics) -> float:
        """计算综合依赖分数"""
        weights = self.dependency_weights
        values = [
            metrics.usage_frequency * weights['usage_frequency'],
            metrics.usage_duration * weights['usage_duration'],
            metrics.dependency_severity * weights['dependency_severity'],
            metrics.function_loss_anxiety * weights['function_loss_anxiety'],
            metrics.withdrawal_symptoms * weights['withdrawal_symptoms'],
            metrics.productivity_impact * weights['productivity_impact'],
            metrics.social_interaction_impact * weights['social_interaction_impact'],
            metrics.privacy_concerns * weights['privacy_concerns'],
            metrics.control_perception * weights['control_perception'],
            metrics.technological_anxiety * weights['technological_anxiety']
        ]
        
        return sum(values)
    
    def _analyze_dependency_types(self, metrics: TechnologyMetrics) -> Dict[str, float]:
        """分析依赖类型"""
        return {
            'functional_dependency': (
                metrics.dependency_severity * 0.4 +
                metrics.function_loss_anxiety * 0.3 +
                metrics.usage_frequency * 0.3
            ),
            'emotional_dependency': (
                metrics.withdrawal_symptoms * 0.5 +
                metrics.technological_anxiety * 0.3 +
                metrics.usage_duration * 0.2
            ),
            'social_dependency': (
                metrics.social_interaction_impact * 0.6 +
                metrics.usage_frequency * 0.4
            ),
            'productivity_dependency': (
                metrics.productivity_impact * 0.7 +
                metrics.usage_frequency * 0.3
            )
        }
    
    def _assess_dependency_level(self, dependency_score: float) -> str:
        """评估依赖程度"""
        if dependency_score >= self.dependency_thresholds['severe_dependency']:
            return '严重依赖'
        elif dependency_score >= self.dependency_thresholds['moderate_dependency']:
            return '中等依赖'
        elif dependency_score >= self.dependency_thresholds['mild_dependency']:
            return '轻度依赖'
        else:
            return '最小依赖'
    
    def _analyze_dependency_impact(self, metrics: TechnologyMetrics) -> Dict[str, Any]:
        """分析依赖影响"""
        impact_dimensions = {
            'productivity_impact': metrics.productivity_impact,
            'social_impact': metrics.social_interaction_impact,
            'psychological_impact': (
                metrics.withdrawal_symptoms * 0.4 +
                metrics.technological_anxiety * 0.3 +
                metrics.function_loss_anxiety * 0.3
            ),
            'privacy_impact': metrics.privacy_concerns
        }
        
        # 计算总体影响分数
        total_impact = np.mean(list(impact_dimensions.values()))
        
        return {
            'impact_dimensions': impact_dimensions,
            'total_impact_score': total_impact,
            'impact_severity': self._assess_impact_severity(total_impact),
            'priority_intervention_areas': self._identify_priority_areas(impact_dimensions)
        }
    
    def _identify_dependency_patterns(self, metrics: TechnologyMetrics) -> Dict[str, Any]:
        """识别依赖模式"""
        patterns = {}
        
        # 使用强度模式
        if metrics.usage_frequency > 0.7 and metrics.usage_duration > 0.7:
            patterns['intensive_use_pattern'] = '高强度使用模式'
        elif metrics.usage_frequency > 0.5 or metrics.usage_duration > 0.5:
            patterns['moderate_use_pattern'] = '适度使用模式'
        else:
            patterns['minimal_use_pattern'] = '最小使用模式'
        
        # 依赖特征模式
        if metrics.withdrawal_symptoms > 0.6:
            patterns['addiction_like_pattern'] = '成瘾型依赖模式'
        if metrics.function_loss_anxiety > 0.6:
            patterns['anxiety_driven_pattern'] = '焦虑驱动模式'
        if metrics.productivity_impact > 0.6:
            patterns['productivity_disruption_pattern'] = '生产力干扰模式'
        
        return patterns
    
    def _assess_technology_control(self, metrics: TechnologyMetrics) -> Dict[str, Any]:
        """评估技术控制能力"""
        # 计算控制能力分数
        control_score = (
            (1 - metrics.dependency_severity) * 0.3 +
            (1 - metrics.withdrawal_symptoms) * 0.3 +
            metrics.control_perception * 0.2 +
            (1 - metrics.technological_anxiety) * 0.2
        )
        
        return {
            'control_score': control_score,
            'control_level': self._determine_control_level(control_score),
            'control_strategies': self._suggest_control_strategies(metrics),
            'control_barriers': self._identify_control_barriers(metrics)
        }
    
    def _predict_dependency_evolution(self, metrics: TechnologyMetrics) -> Dict[str, Any]:
        """预测依赖发展"""
        # 基于当前指标预测发展趋势
        evolution_factors = {
            'usage_trend': (
                metrics.usage_frequency * 0.4 +
                metrics.usage_duration * 0.3 +
                metrics.dependency_severity * 0.3
            ),
            'risk_acceleration': (
                metrics.withdrawal_symptoms * 0.3 +
                metrics.function_loss_anxiety * 0.3 +
                metrics.technological_anxiety * 0.4
            )
        }
        
        # 计算发展轨迹
        trajectory = self._calculate_evolution_trajectory(evolution_factors)
        
        return {
            'evolution_factors': evolution_factors,
            'predicted_trajectory': trajectory,
            'risk_acceleration_rate': evolution_factors['risk_acceleration'],
            'intervention_urgency': self._assess_intervention_urgency(evolution_factors)
        }
    
    def _assess_alienation_correlation(self, metrics: TechnologyMetrics) -> Dict[str, float]:
        """评估与技术异化的相关性"""
        # 技术依赖与技术异化的强相关性
        alienation_correlation = (
            metrics.dependency_severity * 0.25 +
            metrics.withdrawal_symptoms * 0.20 +
            metrics.function_loss_anxiety * 0.20 +
            metrics.usage_duration * 0.15 +
            metrics.technological_anxiety * 0.10 +
            metrics.social_interaction_impact * 0.10
        )
        
        return {
            'technology_alienation_correlation': alienation_correlation,
            'alienation_risk_level': self._determine_alienation_risk_level(alienation_correlation),
            'alienation_indicators': self._identify_alienation_indicators(metrics)
        }
    
    def _assess_impact_severity(self, impact_score: float) -> str:
        """评估影响严重程度"""
        if impact_score > 0.7:
            return '严重影响'
        elif impact_score > 0.5:
            return '中等影响'
        elif impact_score > 0.3:
            return '轻度影响'
        else:
            return '最小影响'
    
    def _identify_priority_areas(self, impact_dimensions: Dict[str, float]) -> List[str]:
        """识别优先干预领域"""
        priority_areas = []
        
        # 按影响程度排序
        sorted_dimensions = sorted(impact_dimensions.items(), key=lambda x: x[1], reverse=True)
        
        for dimension, score in sorted_dimensions:
            if score > 0.6:
                if dimension == 'productivity_impact':
                    priority_areas.append('生产力影响')
                elif dimension == 'social_impact':
                    priority_areas.append('社交影响')
                elif dimension == 'psychological_impact':
                    priority_areas.append('心理影响')
                elif dimension == 'privacy_impact':
                    priority_areas.append('隐私影响')
        
        return priority_areas[:3]  # 返回前3个优先领域
    
    def _determine_control_level(self, control_score: float) -> str:
        """确定控制水平"""
        if control_score > 0.7:
            return '强控制'
        elif control_score > 0.5:
            return '中等控制'
        elif control_score > 0.3:
            return '弱控制'
        else:
            return '失控'
    
    def _suggest_control_strategies(self, metrics: TechnologyMetrics) -> List[str]:
        """建议控制策略"""
        strategies = []
        
        if metrics.usage_duration > 0.6:
            strategies.append('设定使用时间限制，建立数字排毒时间')
        if metrics.dependency_severity > 0.6:
            strategies.append('逐步减少依赖，寻找替代活动')
        if metrics.withdrawal_symptoms > 0.5:
            strategies.append('识别戒断症状，寻求专业帮助')
        if metrics.function_loss_anxiety > 0.5:
            strategies.append('增强技术独立性，发展非技术技能')
        if metrics.technological_anxiety > 0.5:
            strategies.append('学习技术管理技能，减少技术焦虑')
        
        return strategies
    
    def _identify_control_barriers(self, metrics: TechnologyMetrics) -> List[str]:
        """识别控制障碍"""
        barriers = []
        
        if metrics.dependency_severity > 0.7:
            barriers.append('依赖程度过高，难以自我控制')
        if metrics.withdrawal_symptoms > 0.6:
            barriers.append('戒断症状严重，影响正常生活')
        if metrics.function_loss_anxiety > 0.6:
            barriers.append('功能缺失焦虑强烈，不敢减少使用')
        if metrics.productivity_impact > 0.6:
            barriers.append('生产力过度依赖技术')
        if metrics.social_interaction_impact > 0.6:
            barriers.append('社交功能过度依赖技术')
        
        return barriers
    
    def _calculate_evolution_trajectory(self, evolution_factors: Dict[str, float]) -> str:
        """计算发展轨迹"""
        usage_trend = evolution_factors['usage_trend']
        risk_acceleration = evolution_factors['risk_acceleration']
        
        if usage_trend > 0.6 and risk_acceleration > 0.6:
            return '快速恶化轨迹'
        elif usage_trend > 0.6 or risk_acceleration > 0.6:
            return '缓慢恶化轨迹'
        elif usage_trend < 0.4 and risk_acceleration < 0.4:
            return '改善轨迹'
        else:
            return '稳定轨迹'
    
    def _assess_intervention_urgency(self, evolution_factors: Dict[str, float]) -> str:
        """评估干预紧急程度"""
        avg_factors = np.mean(list(evolution_factors.values()))
        
        if avg_factors > 0.7:
            return '紧急'
        elif avg_factors > 0.5:
            return '重要'
        elif avg_factors > 0.3:
            return '一般'
        else:
            return '低优先级'
    
    def _determine_alienation_risk_level(self, risk: float) -> str:
        """确定异化风险等级"""
        if risk >= self.dependency_thresholds['severe_dependency']:
            return '高风险'
        elif risk >= self.dependency_thresholds['moderate_dependency']:
            return '中等风险'
        elif risk >= self.dependency_thresholds['mild_dependency']:
            return '低风险'
        else:
            return '极低风险'
    
    def _identify_alienation_indicators(self, metrics: TechnologyMetrics) -> List[str]:
        """识别异化指标"""
        indicators = []
        
        if metrics.dependency_severity > 0.6:
            indicators.append('技术依赖严重')
        if metrics.withdrawal_symptoms > 0.5:
            indicators.append('出现技术戒断症状')
        if metrics.function_loss_anxiety > 0.6:
            indicators.append('功能缺失焦虑严重')
        if metrics.usage_duration > 0.7:
            indicators.append('过度使用技术')
        if metrics.social_interaction_impact > 0.6:
            indicators.append('技术影响正常社交')
        if metrics.productivity_impact > 0.6:
            indicators.append('生产力过度依赖技术')
        if metrics.technological_anxiety > 0.5:
            indicators.append('技术焦虑严重')
        
        return indicators
    
    def _generate_intervention_recommendations(self, metrics: TechnologyMetrics) -> List[str]:
        """生成干预建议"""
        recommendations = []
        
        if metrics.usage_duration > 0.6:
            recommendations.append('建立技术使用时间管理机制')
        if metrics.dependency_severity > 0.5:
            recommendations.append('逐步减少技术依赖，发展替代技能')
        if metrics.withdrawal_symptoms > 0.4:
            recommendations.append('识别和处理技术戒断症状')
        if metrics.function_loss_anxiety > 0.5:
            recommendations.append('增强技术独立性和应对能力')
        if metrics.productivity_impact > 0.5:
            recommendations.append('开发非技术性的生产力技能')
        if metrics.social_interaction_impact > 0.5:
            recommendations.append('加强面对面社交技能')
        if metrics.technological_anxiety > 0.4:
            recommendations.append('学习和实践技术管理技能')
        if metrics.privacy_concerns > 0.6:
            recommendations.append('加强隐私保护意识和措施')
        
        return recommendations
    
    def batch_analyze_dependency(self, dependency_dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量分析技术依赖"""
        if not dependency_dataset:
            return {'error': '技术依赖数据为空'}
        
        results = []
        for data in dependency_dataset:
            result = self.analyze_technology_dependency(data)
            results.append(result)
        
        # 计算统计汇总
        dependency_scores = [r['dependency_score'] for r in results]
        
        # 按依赖程度统计
        level_statistics = {}
        for result in results:
            level = result['dependency_level']
            if level not in level_statistics:
                level_statistics[level] = []
            level_statistics[level].append(result['dependency_score'])
        
        return {
            'individual_analyses': results,
            'overall_statistics': {
                'mean_dependency_score': np.mean(dependency_scores),
                'median_dependency_score': np.median(dependency_scores),
                'std_dependency_score': np.std(dependency_scores),
                'severe_dependency_count': sum(1 for s in dependency_scores if s >= 0.75),
                'minimal_dependency_count': sum(1 for s in dependency_scores if s < 0.35),
                'total_analyzed': len(dependency_dataset)
            },
            'level_statistics': {
                level: {
                    'mean_score': np.mean(scores),
                    'count': len(scores)
                } for level, scores in level_statistics.items()
            },
            'analysis_timestamp': datetime.now().isoformat()
        }


def main():
    """主函数 - 用于测试"""
    analyzer = TechnologyDependencyAnalyzer()
    
    # 测试数据
    test_data = {
        'overall_metrics': {
            'usage_frequency': 0.8,
            'usage_duration': 0.7,
            'dependency_severity': 0.6,
            'function_loss_anxiety': 0.5,
            'withdrawal_symptoms': 0.4,
            'productivity_impact': 0.6,
            'social_interaction_impact': 0.5,
            'privacy_concerns': 0.6,
            'control_perception': 0.4,
            'technological_anxiety': 0.5
        }
    }
    
    # 分析技术依赖
    result = analyzer.analyze_technology_dependency(test_data)
    
    # 打印结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()