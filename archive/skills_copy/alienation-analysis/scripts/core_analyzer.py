#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异化分析核心引擎
整合所有异化分析的核心功能，提供统一接口
"""

import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum

# 最小化外部依赖
try:
    import numpy as np
except ImportError:
    # 如果numpy不可用，使用纯Python实现
    class np:
        @staticmethod
        def mean(values):
            return sum(values) / len(values) if values else 0.0
        
        @staticmethod
        def std(values):
            if not values:
                return 0.0
            mean_val = sum(values) / len(values)
            variance = sum((x - mean_val) ** 2 for x in values) / len(values)
            return variance ** 0.5

class AlienationType(Enum):
    """异化类型枚举"""
    LABOR = "labor"
    SOCIAL = "social"
    CONSUMPTION = "consumption"
    TECHNOLOGY = "technology"
    COMPREHENSIVE = "comprehensive"

@dataclass
class AlienationMetrics:
    """异化指标数据类"""
    labor_alienation: float = 0.0
    social_alienation: float = 0.0
    consumption_alienation: float = 0.0
    technology_alienation: float = 0.0
    overall_alienation: float = 0.0

@dataclass
class AnalysisResult:
    """分析结果数据类"""
    alienation_types: List[AlienationType]
    metrics: AlienationMetrics
    severity_level: str
    risk_factors: List[str]
    recommendations: List[str]
    intervention_plan: Dict[str, Any]
    confidence_score: float

class CoreAlienationAnalyzer:
    """异化分析核心引擎"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # 异化程度阈值
        self.thresholds = {
            'minimal': 0.2,
            'mild': 0.4,
            'moderate': 0.6,
            'severe': 0.8
        }
        
        # 权重配置
        self.weights = {
            'labor': 0.3,
            'social': 0.25,
            'consumption': 0.25,
            'technology': 0.2
        }
    
    def analyze_comprehensive_alienation(self, data: Dict[str, Any]) -> AnalysisResult:
        """综合异化分析"""
        try:
            # 识别主要异化类型
            alienation_types = self._identify_alienation_types(data)
            
            # 计算异化指标
            metrics = self._calculate_alienation_metrics(data, alienation_types)
            
            # 评估严重程度
            severity_level = self._assess_severity_level(metrics.overall_alienation)
            
            # 识别风险因素
            risk_factors = self._identify_risk_factors(data, alienation_types)
            
            # 生成建议
            recommendations = self._generate_recommendations(alienation_types, metrics)
            
            # 生成干预计划
            intervention_plan = self._generate_intervention_plan(alienation_types, severity_level)
            
            # 计算置信度
            confidence_score = self._calculate_confidence_score(data)
            
            return AnalysisResult(
                alienation_types=alienation_types,
                metrics=metrics,
                severity_level=severity_level,
                risk_factors=risk_factors,
                recommendations=recommendations,
                intervention_plan=intervention_plan,
                confidence_score=confidence_score
            )
            
        except Exception as e:
            self.logger.error(f"异化分析失败: {str(e)}")
            return self._create_error_result(str(e))
    
    def _identify_alienation_types(self, data: Dict[str, Any]) -> List[AlienationType]:
        """识别主要异化类型"""
        identified_types = []
        
        # 检查劳动异化指标
        if self._has_labor_data(data):
            labor_score = self._calculate_labor_score(data)
            if labor_score > self.thresholds['mild']:
                identified_types.append(AlienationType.LABOR)
        
        # 检查社会异化指标
        if self._has_social_data(data):
            social_score = self._calculate_social_score(data)
            if social_score > self.thresholds['mild']:
                identified_types.append(AlienationType.SOCIAL)
        
        # 检查消费异化指标
        if self._has_consumption_data(data):
            consumption_score = self._calculate_consumption_score(data)
            if consumption_score > self.thresholds['mild']:
                identified_types.append(AlienationType.CONSUMPTION)
        
        # 检查技术异化指标
        if self._has_technology_data(data):
            technology_score = self._calculate_technology_score(data)
            if technology_score > self.thresholds['mild']:
                identified_types.append(AlienationType.TECHNOLOGY)
        
        # 如果没有明确识别出类型，进行综合分析
        if not identified_types:
            identified_types = [AlienationType.COMPREHENSIVE]
        
        return identified_types
    
    def _calculate_alienation_metrics(self, data: Dict[str, Any], 
                                    alienation_types: List[AlienationType]) -> AlienationMetrics:
        """计算异化指标"""
        metrics = AlienationMetrics()
        
        # 计算各项异化分数
        if AlienationType.LABOR in alienation_types or AlienationType.COMPREHENSIVE in alienation_types:
            metrics.labor_alienation = self._calculate_labor_score(data)
        
        if AlienationType.SOCIAL in alienation_types or AlienationType.COMPREHENSIVE in alienation_types:
            metrics.social_alienation = self._calculate_social_score(data)
        
        if AlienationType.CONSUMPTION in alienation_types or AlienationType.COMPREHENSIVE in alienation_types:
            metrics.consumption_alienation = self._calculate_consumption_score(data)
        
        if AlienationType.TECHNOLOGY in alienation_types or AlienationType.COMPREHENSIVE in alienation_types:
            metrics.technology_alienation = self._calculate_technology_score(data)
        
        # 计算综合异化分数
        metrics.overall_alienation = self._calculate_overall_score(metrics)
        
        return metrics
    
    def _calculate_labor_score(self, data: Dict[str, Any]) -> float:
        """计算劳动异化分数"""
        labor_data = data.get('labor_data', {})
        if not labor_data:
            return 0.0
        
        # 基础劳动指标
        stress_level = labor_data.get('work_stress_level', 0.5)
        autonomy_level = labor_data.get('autonomy_level', 0.5)
        meaningfulness = labor_data.get('meaningfulness', 0.5)
        skill_development = labor_data.get('skill_development', 0.5)
        work_life_balance = labor_data.get('work_life_balance', 0.5)
        
        # 计算劳动异化分数（负向指标高表示异化严重）
        alienation_score = (
            stress_level * 0.3 +
            (1 - autonomy_level) * 0.25 +
            (1 - meaningfulness) * 0.25 +
            (1 - skill_development) * 0.1 +
            (1 - work_life_balance) * 0.1
        )
        
        return min(1.0, alienation_score)
    
    def _calculate_social_score(self, data: Dict[str, Any]) -> float:
        """计算社会异化分数"""
        social_data = data.get('social_data', {})
        if not social_data:
            return 0.0
        
        # 基础社会指标
        intimacy_level = social_data.get('intimacy_level', 0.5)
        trust_level = social_data.get('trust_level', 0.5)
        communication_quality = social_data.get('communication_quality', 0.5)
        emotional_support = social_data.get('emotional_support', 0.5)
        community_connection = social_data.get('community_connection', 0.5)
        
        # 计算社会异化分数
        alienation_score = (
            (1 - intimacy_level) * 0.25 +
            (1 - trust_level) * 0.25 +
            (1 - communication_quality) * 0.2 +
            (1 - emotional_support) * 0.15 +
            (1 - community_connection) * 0.15
        )
        
        return min(1.0, alienation_score)
    
    def _calculate_consumption_score(self, data: Dict[str, Any]) -> float:
        """计算消费异化分数"""
        consumption_data = data.get('consumption_data', {})
        if not consumption_data:
            return 0.0
        
        # 基础消费指标
        impulse_purchase_ratio = consumption_data.get('impulse_purchase_ratio', 0.2)
        status_purchase_ratio = consumption_data.get('status_purchase_ratio', 0.2)
        materialism_level = consumption_data.get('materialism_level', 0.3)
        debt_to_income_ratio = consumption_data.get('debt_to_income_ratio', 0.1)
        
        # 计算消费异化分数
        alienation_score = (
            impulse_purchase_ratio * 0.3 +
            status_purchase_ratio * 0.25 +
            materialism_level * 0.25 +
            debt_to_income_ratio * 0.2
        )
        
        return min(1.0, alienation_score)
    
    def _calculate_technology_score(self, data: Dict[str, Any]) -> float:
        """计算技术异化分数"""
        technology_data = data.get('technology_data', {})
        if not technology_data:
            return 0.0
        
        # 基础技术指标
        usage_frequency = technology_data.get('usage_frequency', 0.5)
        usage_duration = technology_data.get('usage_duration', 0.5)
        dependency_severity = technology_data.get('dependency_severity', 0.3)
        function_loss_anxiety = technology_data.get('function_loss_anxiety', 0.3)
        
        # 计算技术异化分数
        alienation_score = (
            usage_frequency * 0.2 +
            usage_duration * 0.25 +
            dependency_severity * 0.3 +
            function_loss_anxiety * 0.25
        )
        
        return min(1.0, alienation_score)
    
    def _calculate_overall_score(self, metrics: AlienationMetrics) -> float:
        """计算综合异化分数"""
        scores = []
        weights = []
        
        if metrics.labor_alienation > 0:
            scores.append(metrics.labor_alienation)
            weights.append(self.weights['labor'])
        
        if metrics.social_alienation > 0:
            scores.append(metrics.social_alienation)
            weights.append(self.weights['social'])
        
        if metrics.consumption_alienation > 0:
            scores.append(metrics.consumption_alienation)
            weights.append(self.weights['consumption'])
        
        if metrics.technology_alienation > 0:
            scores.append(metrics.technology_alienation)
            weights.append(self.weights['technology'])
        
        if not scores:
            return 0.0
        
        # 加权平均
        weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
        total_weight = sum(weights)
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _assess_severity_level(self, overall_score: float) -> str:
        """评估异化严重程度"""
        if overall_score >= self.thresholds['severe']:
            return '严重异化'
        elif overall_score >= self.thresholds['moderate']:
            return '中度异化'
        elif overall_score >= self.thresholds['mild']:
            return '轻度异化'
        else:
            return '最小异化'
    
    def _identify_risk_factors(self, data: Dict[str, Any], 
                             alienation_types: List[AlienationType]) -> List[str]:
        """识别风险因素"""
        risk_factors = []
        
        for alienation_type in alienation_types:
            if alienation_type == AlienationType.LABOR:
                risk_factors.extend(self._identify_labor_risks(data))
            elif alienation_type == AlienationType.SOCIAL:
                risk_factors.extend(self._identify_social_risks(data))
            elif alienation_type == AlienationType.CONSUMPTION:
                risk_factors.extend(self._identify_consumption_risks(data))
            elif alienation_type == AlienationType.TECHNOLOGY:
                risk_factors.extend(self._identify_technology_risks(data))
        
        return list(set(risk_factors))  # 去重
    
    def _identify_labor_risks(self, data: Dict[str, Any]) -> List[str]:
        """识别劳动异化风险因素"""
        risks = []
        labor_data = data.get('labor_data', {})
        
        if labor_data.get('work_stress_level', 0) > 0.7:
            risks.append('工作压力过高')
        if labor_data.get('autonomy_level', 1) < 0.3:
            risks.append('工作自主性严重不足')
        if labor_data.get('meaningfulness', 1) < 0.3:
            risks.append('工作意义感缺失')
        if labor_data.get('work_life_balance', 1) < 0.3:
            risks.append('工作生活严重失衡')
        
        return risks
    
    def _identify_social_risks(self, data: Dict[str, Any]) -> List[str]:
        """识别社会异化风险因素"""
        risks = []
        social_data = data.get('social_data', {})
        
        if social_data.get('intimacy_level', 1) < 0.4:
            risks.append('人际关系深度不足')
        if social_data.get('trust_level', 1) < 0.4:
            risks.append('信任关系薄弱')
        if social_data.get('emotional_support', 1) < 0.4:
            risks.append('情感支持不足')
        if social_data.get('community_connection', 1) < 0.4:
            risks.append('社区连接缺失')
        
        return risks
    
    def _identify_consumption_risks(self, data: Dict[str, Any]) -> List[str]:
        """识别消费异化风险因素"""
        risks = []
        consumption_data = data.get('consumption_data', {})
        
        if consumption_data.get('impulse_purchase_ratio', 0) > 0.5:
            risks.append('冲动消费频繁')
        if consumption_data.get('status_purchase_ratio', 0) > 0.4:
            risks.append('地位性消费过度')
        if consumption_data.get('materialism_level', 0) > 0.6:
            risks.append('物质主义倾向严重')
        if consumption_data.get('debt_to_income_ratio', 0) > 0.3:
            risks.append('债务负担过重')
        
        return risks
    
    def _identify_technology_risks(self, data: Dict[str, Any]) -> List[str]:
        """识别技术异化风险因素"""
        risks = []
        technology_data = data.get('technology_data', {})
        
        if technology_data.get('usage_frequency', 0) > 0.8:
            risks.append('技术使用频率过高')
        if technology_data.get('dependency_severity', 0) > 0.6:
            risks.append('技术依赖严重')
        if technology_data.get('function_loss_anxiety', 0) > 0.5:
            risks.append('功能缺失焦虑严重')
        
        return risks
    
    def _generate_recommendations(self, alienation_types: List[AlienationType], 
                                metrics: AlienationMetrics) -> List[str]:
        """生成建议"""
        recommendations = []
        
        for alienation_type in alienation_types:
            if alienation_type == AlienationType.LABOR:
                recommendations.extend([
                    '建立工作生活边界，设定明确的工作时间',
                    '寻找工作中的意义和价值，提升工作满意度',
                    '发展工作自主性，主动承担有挑战性的任务',
                    '加强职业技能发展，持续学习新知识'
                ])
            elif alienation_type == AlienationType.SOCIAL:
                recommendations.extend([
                    '深化人际关系，投入更多时间在重要关系上',
                    '积极参与社区活动，建立社会连接',
                    '寻求和提供情感支持，建立互助网络',
                    '培养信任关系，通过诚实和可靠行为建立信任'
                ])
            elif alienation_type == AlienationType.CONSUMPTION:
                recommendations.extend([
                    '建立理性的消费观念，避免冲动购买',
                    '区分必需品和奢侈品，优先满足基本需求',
                    '寻找非物质性的满足方式，如兴趣爱好和人际关系',
                    '制定预算计划，控制消费支出'
                ])
            elif alienation_type == AlienationType.TECHNOLOGY:
                recommendations.extend([
                    '设定技术使用时间限制，建立数字排毒时间',
                    '培养非技术性的兴趣爱好和技能',
                    '学会技术管理，主动控制使用行为',
                    '加强面对面交流，减少虚拟社交依赖'
                ])
        
        # 去重并限制数量
        unique_recommendations = list(set(recommendations))
        return unique_recommendations[:8]  # 最多返回8条建议
    
    def _generate_intervention_plan(self, alienation_types: List[AlienationType], 
                                  severity_level: str) -> Dict[str, Any]:
        """生成干预计划"""
        plan = {
            'immediate_actions': [],
            'medium_term_goals': [],
            'long_term_vision': [],
            'success_indicators': []
        }
        
        # 根据严重程度制定不同层次的计划
        if severity_level in ['严重异化', '中度异化']:
            plan['immediate_actions'] = [
                '寻求专业心理咨询或治疗',
                '建立紧急支持系统',
                '识别和避免触发因素'
            ]
            plan['medium_term_goals'] = [
                '系统性改善异化状况',
                '建立健康的生活习惯',
                '扩大社会支持网络'
            ]
        else:
            plan['immediate_actions'] = [
                '调整生活方式和习惯',
                '加强自我反思和认知'
            ]
            plan['medium_term_goals'] = [
                '深化个人成长和发展',
                '建立长期改善计划'
            ]
        
        plan['long_term_vision'] = [
            '实现个人全面发展',
            '建立有意义的人生目标',
            '为社会进步做出贡献'
        ]
        
        plan['success_indicators'] = [
            '异化程度显著降低',
            '生活质量明显提升',
            '人际关系更加和谐',
            '工作满意度提高'
        ]
        
        return plan
    
    def _calculate_confidence_score(self, data: Dict[str, Any]) -> float:
        """计算分析置信度"""
        data_quality_score = 0.0
        data_sources_count = 0
        
        # 检查各类数据的完整性和质量
        if self._has_labor_data(data):
            data_quality_score += 0.25
            data_sources_count += 1
        if self._has_social_data(data):
            data_quality_score += 0.25
            data_sources_count += 1
        if self._has_consumption_data(data):
            data_quality_score += 0.25
            data_sources_count += 1
        if self._has_technology_data(data):
            data_quality_score += 0.25
            data_sources_count += 1
        
        # 数据源越多，置信度越高
        source_bonus = min(0.2, data_sources_count * 0.05)
        
        return min(1.0, data_quality_score + source_bonus)
    
    def _has_labor_data(self, data: Dict[str, Any]) -> bool:
        """检查是否有劳动数据"""
        labor_data = data.get('labor_data', {})
        return bool(labor_data)
    
    def _has_social_data(self, data: Dict[str, Any]) -> bool:
        """检查是否有社会数据"""
        social_data = data.get('social_data', {})
        return bool(social_data)
    
    def _has_consumption_data(self, data: Dict[str, Any]) -> bool:
        """检查是否有消费数据"""
        consumption_data = data.get('consumption_data', {})
        return bool(consumption_data)
    
    def _has_technology_data(self, data: Dict[str, Any]) -> bool:
        """检查是否有技术数据"""
        technology_data = data.get('technology_data', {})
        return bool(technology_data)
    
    def _create_error_result(self, error_message: str) -> AnalysisResult:
        """创建错误结果"""
        return AnalysisResult(
            alienation_types=[AlienationType.COMPREHENSIVE],
            metrics=AlienationMetrics(),
            severity_level='未知',
            risk_factors=[f'分析过程出错: {error_message}'],
            recommendations=['建议重新提交完整的数据进行分析'],
            intervention_plan={'error': error_message},
            confidence_score=0.0
        )

# 便捷接口函数
def analyze_alienation(data: Dict[str, Any]) -> Dict[str, Any]:
    """便捷的异化分析接口"""
    analyzer = CoreAlienationAnalyzer()
    result = analyzer.analyze_comprehensive_alienation(data)
    
    return {
        'alienation_types': [t.value for t in result.alienation_types],
        'metrics': {
            'labor_alienation': result.metrics.labor_alienation,
            'social_alienation': result.metrics.social_alienation,
            'consumption_alienation': result.metrics.consumption_alienation,
            'technology_alienation': result.metrics.technology_alienation,
            'overall_alienation': result.metrics.overall_alienation
        },
        'severity_level': result.severity_level,
        'risk_factors': result.risk_factors,
        'recommendations': result.recommendations,
        'intervention_plan': result.intervention_plan,
        'confidence_score': result.confidence_score,
        'analysis_timestamp': datetime.now().isoformat()
    }

if __name__ == '__main__':
    # 测试代码
    test_data = {
        'labor_data': {
            'work_stress_level': 0.8,
            'autonomy_level': 0.3,
            'meaningfulness': 0.2,
            'work_life_balance': 0.3
        },
        'technology_data': {
            'usage_frequency': 0.9,
            'dependency_severity': 0.7
        }
    }
    
    result = analyze_alienation(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))