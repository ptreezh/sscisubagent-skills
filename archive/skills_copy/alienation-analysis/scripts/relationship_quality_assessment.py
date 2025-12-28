#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关系质量评估器
评估个体各种社会关系的质量和健康状况
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
import json


class RelationshipType(Enum):
    """关系类型"""
    FAMILY = "family"
    ROMANTIC = "romantic"
    FRIENDSHIP = "friendship"
    PROFESSIONAL = "professional"
    NEIGHBORHOOD = "neighborhood"
    ONLINE = "online"


@dataclass
class RelationshipMetrics:
    """关系指标数据类"""
    intimacy_level: float            # 亲密程度
    trust_level: float               # 信任水平
    communication_quality: float     # 沟通质量
    emotional_support: float         # 情感支持
    conflict_resolution: float       # 冲突解决能力
    commitment_level: float          # 承诺水平
    reciprocity: float               # 互惠性
    authenticity: float              # 真实性
    stability: float                 # 稳定性
    growth_potential: float          # 成长潜力


class RelationshipQualityAssessment:
    """关系质量评估器"""
    
    def __init__(self):
        self.relationship_weights = {
            'intimacy_level': 0.15,
            'trust_level': 0.15,
            'communication_quality': 0.12,
            'emotional_support': 0.12,
            'conflict_resolution': 0.10,
            'commitment_level': 0.10,
            'reciprocity': 0.08,
            'authenticity': 0.08,
            'stability': 0.05,
            'growth_potential': 0.05
        }
        
        self.quality_thresholds = {
            'excellent': 0.85,
            'good': 0.70,
            'satisfactory': 0.55,
            'needs_improvement': 0.40,
            'poor': 0.25
        }
        
        self.relationship_stages = {
            'formation': {'duration_months': 6, 'expected_quality': 0.4},
            'development': {'duration_months': 24, 'expected_quality': 0.6},
            'maturity': {'duration_months': 60, 'expected_quality': 0.8},
            'decline': {'duration_months': 999, 'expected_quality': 0.5}
        }
    
    def assess_relationship_quality(self, relationship_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估关系质量
        
        Args:
            relationship_data: 关系数据字典
            
        Returns:
            评估结果字典
        """
        # 解析关系数据
        relationship_type = relationship_data.get('type', RelationshipType.FRIENDSHIP.value)
        duration_months = relationship_data.get('duration_months', 0)
        metrics_data = relationship_data.get('metrics', {})
        
        # 创建关系指标对象
        metrics = self._create_relationship_metrics(metrics_data)
        
        # 计算综合质量分数
        quality_score = self._calculate_quality_score(metrics)
        
        # 评估关系阶段
        relationship_stage = self._assess_relationship_stage(duration_months, quality_score)
        
        # 分析关系维度
        relationship_dimensions = self._analyze_relationship_dimensions(metrics)
        
        # 识别关系优势
        relationship_strengths = self._identify_relationship_strengths(metrics)
        
        # 识别关系问题
        relationship_issues = self._identify_relationship_issues(metrics)
        
        # 评估关系健康度
        relationship_health = self._assess_relationship_health(metrics, relationship_stage)
        
        # 预测关系发展
        relationship_prediction = self._predict_relationship_development(
            metrics, relationship_stage, duration_months)
        
        # 评估社会异化相关性
        alienation_correlation = self._assess_alienation_correlation(metrics)
        
        return {
            'overall_quality_score': quality_score,
            'quality_level': self._determine_quality_level(quality_score),
            'relationship_type': relationship_type,
            'relationship_stage': relationship_stage,
            'relationship_dimensions': relationship_dimensions,
            'relationship_strengths': relationship_strengths,
            'relationship_issues': relationship_issues,
            'relationship_health': relationship_health,
            'relationship_prediction': relationship_prediction,
            'alienation_correlation': alienation_correlation,
            'improvement_suggestions': self._generate_improvement_suggestions(metrics),
            'assessment_timestamp': datetime.now().isoformat()
        }
    
    def _create_relationship_metrics(self, data: Dict[str, float]) -> RelationshipMetrics:
        """创建关系指标对象"""
        # 设置默认值
        default_values = {
            'intimacy_level': 0.5,
            'trust_level': 0.5,
            'communication_quality': 0.5,
            'emotional_support': 0.5,
            'conflict_resolution': 0.5,
            'commitment_level': 0.5,
            'reciprocity': 0.5,
            'authenticity': 0.5,
            'stability': 0.5,
            'growth_potential': 0.5
        }
        
        # 合并数据
        merged_data = {**default_values, **data}
        
        return RelationshipMetrics(**merged_data)
    
    def _calculate_quality_score(self, metrics: RelationshipMetrics) -> float:
        """计算综合质量分数"""
        weights = self.relationship_weights
        values = [
            metrics.intimacy_level * weights['intimacy_level'],
            metrics.trust_level * weights['trust_level'],
            metrics.communication_quality * weights['communication_quality'],
            metrics.emotional_support * weights['emotional_support'],
            metrics.conflict_resolution * weights['conflict_resolution'],
            metrics.commitment_level * weights['commitment_level'],
            metrics.reciprocity * weights['reciprocity'],
            metrics.authenticity * weights['authenticity'],
            metrics.stability * weights['stability'],
            metrics.growth_potential * weights['growth_potential']
        ]
        
        return sum(values)
    
    def _assess_relationship_stage(self, duration_months: float, quality_score: float) -> str:
        """评估关系阶段"""
        if duration_months < 6:
            return 'formation'
        elif duration_months < 24:
            return 'development'
        elif duration_months < 60:
            return 'maturity'
        else:
            # 基于质量分数判断是否衰退
            if quality_score < 0.4:
                return 'decline'
            else:
                return 'maturity'
    
    def _analyze_relationship_dimensions(self, metrics: RelationshipMetrics) -> Dict[str, float]:
        """分析关系维度"""
        return {
            'emotional_connection': (
                metrics.intimacy_level * 0.4 +
                metrics.trust_level * 0.3 +
                metrics.emotional_support * 0.3
            ),
            'communication_effectiveness': (
                metrics.communication_quality * 0.6 +
                metrics.conflict_resolution * 0.4
            ),
            'relationship_investment': (
                metrics.commitment_level * 0.5 +
                metrics.reciprocity * 0.3 +
                metrics.stability * 0.2
            ),
            'relationship_authenticity': (
                metrics.authenticity * 0.7 +
                metrics.growth_potential * 0.3
            )
        }
    
    def _identify_relationship_strengths(self, metrics: RelationshipMetrics) -> List[str]:
        """识别关系优势"""
        strengths = []
        
        if metrics.intimacy_level > self.quality_thresholds['good']:
            strengths.append('高度亲密的情感连接')
        if metrics.trust_level > self.quality_thresholds['good']:
            strengths.append('坚实的信任基础')
        if metrics.communication_quality > self.quality_thresholds['good']:
            strengths.append('优质的沟通交流')
        if metrics.emotional_support > self.quality_thresholds['good']:
            strengths.append('充分的情感支持')
        if metrics.conflict_resolution > self.quality_thresholds['good']:
            strengths.append('良好的冲突解决能力')
        if metrics.authenticity > self.quality_thresholds['good']:
            strengths.append('真实自然的相处方式')
        if metrics.stability > self.quality_thresholds['good']:
            strengths.append('稳定可靠的关系基础')
        
        return strengths
    
    def _identify_relationship_issues(self, metrics: RelationshipMetrics) -> List[str]:
        """识别关系问题"""
        issues = []
        
        if metrics.intimacy_level < self.quality_thresholds['needs_improvement']:
            issues.append('情感亲密程度不足')
        if metrics.trust_level < self.quality_thresholds['needs_improvement']:
            issues.append('信任关系需要加强')
        if metrics.communication_quality < self.quality_thresholds['needs_improvement']:
            issues.append('沟通交流存在问题')
        if metrics.emotional_support < self.quality_thresholds['needs_improvement']:
            issues.append('情感支持不够充分')
        if metrics.conflict_resolution < self.quality_thresholds['needs_improvement']:
            issues.append('冲突处理能力不足')
        if metrics.commitment_level < self.quality_thresholds['needs_improvement']:
            issues.append('关系承诺水平较低')
        if metrics.reciprocity < self.quality_thresholds['needs_improvement']:
            issues.append('关系互惠性不足')
        if metrics.authenticity < self.quality_thresholds['needs_improvement']:
            issues.append('关系真实性有待提升')
        
        return issues
    
    def _assess_relationship_health(self, metrics: RelationshipMetrics, 
                                  relationship_stage: str) -> Dict[str, Any]:
        """评估关系健康度"""
        # 计算健康度分数
        health_score = self._calculate_quality_score(metrics)
        
        # 获取该阶段的期望质量
        expected_quality = self.relationship_stages.get(relationship_stage, {}).get('expected_quality', 0.5)
        
        # 评估健康状态
        health_assessment = self._determine_health_status(health_score, expected_quality)
        
        return {
            'health_score': health_score,
            'health_status': health_assessment,
            'stage_appropriateness': self._assess_stage_appropriateness(health_score, expected_quality),
            'health_trend': self._assess_health_trend(metrics),
            'risk_factors': self._identify_health_risks(metrics)
        }
    
    def _predict_relationship_development(self, metrics: RelationshipMetrics, 
                                        relationship_stage: str, 
                                        duration_months: float) -> Dict[str, Any]:
        """预测关系发展"""
        # 基于当前指标预测发展轨迹
        development_trajectory = self._calculate_development_trajectory(
            metrics, relationship_stage, duration_months)
        
        # 识别发展机会
        development_opportunities = self._identify_development_opportunities(metrics)
        
        # 预测潜在挑战
        potential_challenges = self._predict_potential_challenges(metrics, relationship_stage)
        
        return {
            'development_trajectory': development_trajectory,
            'development_opportunities': development_opportunities,
            'potential_challenges': potential_challenges,
            'success_probability': self._calculate_success_probability(metrics),
            'key_success_factors': self._identify_success_factors(metrics)
        }
    
    def _assess_alienation_correlation(self, metrics: RelationshipMetrics) -> Dict[str, float]:
        """评估与社会异化的相关性"""
        # 关系质量与社会异化的负相关
        alienation_correlation = 1 - (
            metrics.intimacy_level * 0.25 +
            metrics.trust_level * 0.2 +
            metrics.communication_quality * 0.15 +
            metrics.emotional_support * 0.15 +
            metrics.authenticity * 0.15 +
            metrics.reciprocity * 0.1
        )
        
        return {
            'social_alienation_correlation': max(0, min(1, alienation_correlation)),
            'alienation_risk_level': self._determine_risk_level(alienation_correlation),
            'isolation_indicators': self._identify_isolation_indicators(metrics)
        }
    
    def _determine_quality_level(self, quality: float) -> str:
        """确定质量等级"""
        if quality >= self.quality_thresholds['excellent']:
            return '优秀'
        elif quality >= self.quality_thresholds['good']:
            return '良好'
        elif quality >= self.quality_thresholds['satisfactory']:
            return '满意'
        elif quality >= self.quality_thresholds['needs_improvement']:
            return '需要改进'
        else:
            return '较差'
    
    def _determine_health_status(self, health_score: float, expected_quality: float) -> str:
        """确定健康状态"""
        if health_score >= expected_quality * 1.1:
            return '非常健康'
        elif health_score >= expected_quality:
            return '健康'
        elif health_score >= expected_quality * 0.8:
            return '一般健康'
        else:
            return '不健康'
    
    def _assess_stage_appropriateness(self, health_score: float, expected_quality: float) -> str:
        """评估阶段适宜性"""
        if health_score >= expected_quality * 1.1:
            return '超越阶段期望'
        elif health_score >= expected_quality * 0.9:
            return '符合阶段期望'
        else:
            return '低于阶段期望'
    
    def _assess_health_trend(self, metrics: RelationshipMetrics) -> str:
        """评估健康趋势"""
        # 基于关键指标评估趋势
        trend_indicators = [
            metrics.growth_potential,
            metrics.stability,
            metrics.commitment_level
        ]
        
        avg_trend = np.mean(trend_indicators)
        
        if avg_trend > 0.7:
            return '上升趋势'
        elif avg_trend > 0.5:
            return '稳定趋势'
        else:
            return '下降趋势'
    
    def _identify_health_risks(self, metrics: RelationshipMetrics) -> List[str]:
        """识别健康风险"""
        risks = []
        
        if metrics.stability < 0.4:
            risks.append('关系稳定性不足')
        if metrics.conflict_resolution < 0.4:
            risks.append('冲突处理能力不足')
        if metrics.trust_level < 0.4:
            risks.append('信任关系薄弱')
        if metrics.communication_quality < 0.4:
            risks.append('沟通质量存在问题')
        if metrics.commitment_level < 0.4:
            risks.append('关系承诺不足')
        
        return risks
    
    def _calculate_development_trajectory(self, metrics: RelationshipMetrics, 
                                        relationship_stage: str, 
                                        duration_months: float) -> Dict[str, float]:
        """计算发展轨迹"""
        # 短期预测 (6个月)
        short_term = self._predict_short_term_development(metrics, 6)
        
        # 中期预测 (24个月)
        medium_term = self._predict_medium_term_development(metrics, 24)
        
        # 长期预测 (60个月)
        long_term = self._predict_long_term_development(metrics, 60)
        
        return {
            '6_months': short_term,
            '24_months': medium_term,
            '60_months': long_term
        }
    
    def _predict_short_term_development(self, metrics: RelationshipMetrics, months: int) -> float:
        """预测短期发展"""
        # 短期发展主要看沟通质量和冲突解决
        development_factors = (
            metrics.communication_quality * 0.4 +
            metrics.conflict_resolution * 0.3 +
            metrics.growth_potential * 0.3
        )
        
        time_impact = months / 24  # 最多2年的发展潜力
        return min(1.0, development_factors * (1 + time_impact * 0.2))
    
    def _predict_medium_term_development(self, metrics: RelationshipMetrics, months: int) -> float:
        """预测中期发展"""
        # 中期发展看信任、承诺和稳定性
        development_factors = (
            metrics.trust_level * 0.3 +
            metrics.commitment_level * 0.3 +
            metrics.stability * 0.2 +
            metrics.emotional_support * 0.2
        )
        
        time_impact = months / 60  # 最多5年的发展潜力
        return min(1.0, development_factors * (1 + time_impact * 0.3))
    
    def _predict_long_term_development(self, metrics: RelationshipMetrics, months: int) -> float:
        """预测长期发展"""
        # 长期发展看综合质量
        base_quality = self._calculate_quality_score(metrics)
        
        time_impact = months / 120  # 最多10年的发展潜力
        return min(1.0, base_quality * (1 + time_impact * 0.4))
    
    def _identify_development_opportunities(self, metrics: RelationshipMetrics) -> List[str]:
        """识别发展机会"""
        opportunities = []
        
        if metrics.growth_potential > 0.7:
            opportunities.append('关系具有很大发展潜力')
        if metrics.communication_quality > 0.7:
            opportunities.append('良好沟通为关系发展奠定基础')
        if metrics.emotional_support > 0.7:
            opportunities.append('充分情感支持促进关系深化')
        if metrics.trust_level > 0.7:
            opportunities.append('坚实的信任基础有利于长期发展')
        if metrics.authenticity > 0.7:
            opportunities.append('真实性有利于建立深层连接')
        
        return opportunities
    
    def _predict_potential_challenges(self, metrics: RelationshipMetrics, 
                                    relationship_stage: str) -> List[str]:
        """预测潜在挑战"""
        challenges = []
        
        if metrics.conflict_resolution < 0.5:
            challenges.append('冲突处理能力不足可能影响关系稳定')
        if metrics.commitment_level < 0.5:
            challenges.append('承诺水平不足可能导致关系疏远')
        if metrics.stability < 0.5:
            challenges.append('关系稳定性不足容易受到外界影响')
        if metrics.communication_quality < 0.5:
            challenges.append('沟通问题可能积累成重大矛盾')
        if relationship_stage == 'decline':
            challenges.append('关系处于衰退期需要特别关注')
        
        return challenges
    
    def _calculate_success_probability(self, metrics: RelationshipMetrics) -> float:
        """计算成功概率"""
        # 基于关键成功因素计算
        success_factors = (
            metrics.trust_level * 0.25 +
            metrics.communication_quality * 0.20 +
            metrics.commitment_level * 0.20 +
            metrics.emotional_support * 0.15 +
            metrics.conflict_resolution * 0.10 +
            metrics.authenticity * 0.10
        )
        
        return min(0.95, max(0.05, success_factors))
    
    def _identify_success_factors(self, metrics: RelationshipMetrics) -> List[str]:
        """识别成功因素"""
        factors = []
        
        if metrics.trust_level > 0.6:
            factors.append('信任是关系成功的核心要素')
        if metrics.communication_quality > 0.6:
            factors.append('有效沟通是关系维护的关键')
        if metrics.commitment_level > 0.6:
            factors.append('相互承诺是关系稳定的基础')
        if metrics.emotional_support > 0.6:
            factors.append('情感支持促进关系深化')
        if metrics.conflict_resolution > 0.6:
            factors.append('冲突解决能力维护关系和谐')
        
        return factors
    
    def _determine_risk_level(self, risk: float) -> str:
        """确定风险等级"""
        if risk >= 0.7:
            return '高风险'
        elif risk >= 0.5:
            return '中等风险'
        elif risk >= 0.3:
            return '低风险'
        else:
            return '极低风险'
    
    def _identify_isolation_indicators(self, metrics: RelationshipMetrics) -> List[str]:
        """识别孤立指标"""
        indicators = []
        
        if metrics.intimacy_level < 0.3:
            indicators.append('缺乏深层情感连接')
        if metrics.trust_level < 0.3:
            indicators.append('信任关系严重缺失')
        if metrics.communication_quality < 0.3:
            indicators.append('沟通交流严重障碍')
        if metrics.emotional_support < 0.3:
            indicators.append('情感支持严重不足')
        if metrics.reciprocity < 0.3:
            indicators.append('关系互惠性严重不足')
        
        return indicators
    
    def _generate_improvement_suggestions(self, metrics: RelationshipMetrics) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if metrics.intimacy_level < 0.6:
            suggestions.append('增加情感交流，深化亲密关系')
        if metrics.trust_level < 0.6:
            suggestions.append('建立信任，通过诚实和可靠行为赢得信任')
        if metrics.communication_quality < 0.6:
            suggestions.append('改善沟通技巧，学会倾听和表达')
        if metrics.emotional_support < 0.6:
            suggestions.append('提供更多情感支持和理解')
        if metrics.conflict_resolution < 0.6:
            suggestions.append('学习冲突解决技巧，寻求双赢解决方案')
        if metrics.commitment_level < 0.6:
            suggestions.append('明确关系承诺，展现长期投入意愿')
        if metrics.reciprocity < 0.6:
            suggestions.append('增强关系互惠性，给予和接受并重')
        if metrics.authenticity < 0.6:
            suggestions.append('保持真实自我，避免过度迎合')
        
        return suggestions
    
    def batch_assess_relationships(self, relationship_dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量评估关系质量"""
        if not relationship_dataset:
            return {'error': '关系数据为空'}
        
        results = []
        for data in relationship_dataset:
            result = self.assess_relationship_quality(data)
            results.append(result)
        
        # 计算统计汇总
        quality_scores = [r['overall_quality_score'] for r in results]
        
        # 按关系类型统计
        type_statistics = {}
        for result in results:
            rel_type = result['relationship_type']
            if rel_type not in type_statistics:
                type_statistics[rel_type] = []
            type_statistics[rel_type].append(result['overall_quality_score'])
        
        return {
            'individual_assessments': results,
            'overall_statistics': {
                'mean_quality_score': np.mean(quality_scores),
                'median_quality_score': np.median(quality_scores),
                'std_quality_score': np.std(quality_scores),
                'high_quality_relationships': sum(1 for s in quality_scores if s >= 0.85),
                'poor_quality_relationships': sum(1 for s in quality_scores if s < 0.40),
                'total_relationships': len(relationship_dataset)
            },
            'type_statistics': {
                rel_type: {
                    'mean_score': np.mean(scores),
                    'count': len(scores)
                } for rel_type, scores in type_statistics.items()
            },
            'assessment_timestamp': datetime.now().isoformat()
        }


def main():
    """主函数 - 用于测试"""
    assessor = RelationshipQualityAssessment()
    
    # 测试数据
    test_data = {
        'type': 'friendship',
        'duration_months': 18,
        'metrics': {
            'intimacy_level': 0.7,
            'trust_level': 0.8,
            'communication_quality': 0.6,
            'emotional_support': 0.7,
            'conflict_resolution': 0.5,
            'commitment_level': 0.6,
            'reciprocity': 0.7,
            'authenticity': 0.8,
            'stability': 0.7,
            'growth_potential': 0.6
        }
    }
    
    # 评估关系质量
    result = assessor.assess_relationship_quality(test_data)
    
    # 打印结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()