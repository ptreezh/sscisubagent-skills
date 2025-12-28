#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
职业发展评估器
评估个体的职业发展状况和成长潜力
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum


class CareerStage(Enum):
    """职业发展阶段"""
    ENTRY = "entry"           # 入职期
    GROWTH = "growth"         # 成长期
    MATURE = "mature"         # 成熟期
    DECLINE = "decline"       # 衰退期
    TRANSITION = "transition" # 转换期


@dataclass
class CareerMetrics:
    """职业发展指标数据类"""
    skill_development: float        # 技能发展水平
    career_advancement: float       # 职业晋升速度
    learning_opportunities: float   # 学习机会
    mentorship_quality: float       # 导师指导质量
    networking: float              # 职业网络建设
    work_challenges: float         # 工作挑战性
    recognition: float             # 工作认可度
    autonomy_level: float          # 工作自主性
    work_meaning: float            # 工作意义感
    future_prospects: float        # 未来前景


class CareerDevelopmentEvaluator:
    """职业发展评估器"""
    
    def __init__(self):
        self.career_weights = {
            'skill_development': 0.20,
            'career_advancement': 0.18,
            'learning_opportunities': 0.15,
            'mentorship_quality': 0.10,
            'networking': 0.10,
            'work_challenges': 0.10,
            'recognition': 0.07,
            'autonomy_level': 0.05,
            'work_meaning': 0.03,
            'future_prospects': 0.02
        }
        
        self.development_thresholds = {
            'excellent': 0.85,
            'good': 0.70,
            'satisfactory': 0.55,
            'needs_improvement': 0.40,
            'poor': 0.25
        }
    
    def evaluate_career_development(self, career_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        评估职业发展状况
        
        Args:
            career_data: 职业发展数据字典
            
        Returns:
            评估结果字典
        """
        # 解析输入数据
        metrics = self._extract_career_metrics(career_data)
        work_experience = career_data.get('work_experience_years', 0)
        current_position = career_data.get('current_position_level', 1)
        
        # 计算综合发展评分
        development_score = self._calculate_development_score(metrics)
        
        # 评估职业发展阶段
        career_stage = self._assess_career_stage(work_experience, current_position, metrics)
        
        # 分析发展维度
        development_dimensions = self._analyze_development_dimensions(metrics)
        
        # 识别发展障碍
        development_barriers = self._identify_development_barriers(metrics)
        
        # 评估成长潜力
        growth_potential = self._assess_growth_potential(metrics, career_stage)
        
        # 预测发展轨迹
        development_trajectory = self._predict_development_trajectory(
            metrics, career_stage, work_experience)
        
        # 评估异化相关性
        alienation_correlation = self._assess_alienation_correlation(metrics)
        
        return {
            'overall_development_score': development_score,
            'development_level': self._determine_development_level(development_score),
            'career_stage': career_stage.value,
            'development_dimensions': development_dimensions,
            'development_barriers': development_barriers,
            'growth_potential': growth_potential,
            'development_trajectory': development_trajectory,
            'alienation_correlation': alienation_correlation,
            'development_recommendations': self._generate_development_recommendations(metrics),
            'evaluation_timestamp': datetime.now().isoformat()
        }
    
    def _extract_career_metrics(self, data: Dict[str, Any]) -> CareerMetrics:
        """提取职业发展指标"""
        # 设置默认值
        default_values = {
            'skill_development': 0.5,
            'career_advancement': 0.5,
            'learning_opportunities': 0.5,
            'mentorship_quality': 0.5,
            'networking': 0.5,
            'work_challenges': 0.5,
            'recognition': 0.5,
            'autonomy_level': 0.5,
            'work_meaning': 0.5,
            'future_prospects': 0.5
        }
        
        # 合并数据
        merged_data = {**default_values}
        
        # 从数据中提取各项指标
        if 'metrics' in data:
            merged_data.update(data['metrics'])
        else:
            # 从扁平化数据中提取
            for key in default_values:
                if key in data:
                    merged_data[key] = data[key]
        
        return CareerMetrics(**merged_data)
    
    def _calculate_development_score(self, metrics: CareerMetrics) -> float:
        """计算综合发展评分"""
        weights = self.career_weights
        values = [
            metrics.skill_development * weights['skill_development'],
            metrics.career_advancement * weights['career_advancement'],
            metrics.learning_opportunities * weights['learning_opportunities'],
            metrics.mentorship_quality * weights['mentorship_quality'],
            metrics.networking * weights['networking'],
            metrics.work_challenges * weights['work_challenges'],
            metrics.recognition * weights['recognition'],
            metrics.autonomy_level * weights['autonomy_level'],
            metrics.work_meaning * weights['work_meaning'],
            metrics.future_prospects * weights['future_prospects']
        ]
        
        return sum(values)
    
    def _assess_career_stage(self, work_experience: float, 
                           current_position: int, metrics: CareerMetrics) -> CareerStage:
        """评估职业发展阶段"""
        # 基于工作经验和当前职位评估
        if work_experience < 2:
            return CareerStage.ENTRY
        elif work_experience < 5:
            if current_position <= 2:
                return CareerStage.GROWTH
            else:
                return CareerStage.MATURE
        elif work_experience < 15:
            if metrics.career_advancement > 0.7:
                return CareerStage.MATURE
            else:
                return CareerStage.GROWTH
        else:
            if metrics.future_prospects > 0.6:
                return CareerStage.MATURE
            else:
                return CareerStage.DECLINE
    
    def _analyze_development_dimensions(self, metrics: CareerMetrics) -> Dict[str, float]:
        """分析发展维度"""
        return {
            'competency_development': (
                metrics.skill_development * 0.4 +
                metrics.work_challenges * 0.3 +
                metrics.learning_opportunities * 0.3
            ),
            'career_progression': (
                metrics.career_advancement * 0.5 +
                metrics.recognition * 0.3 +
                metrics.future_prospects * 0.2
            ),
            'professional_network': (
                metrics.networking * 0.6 +
                metrics.mentorship_quality * 0.4
            ),
            'autonomy_empowerment': (
                metrics.autonomy_level * 0.7 +
                metrics.work_meaning * 0.3
            )
        }
    
    def _identify_development_barriers(self, metrics: CareerMetrics) -> List[str]:
        """识别发展障碍"""
        barriers = []
        
        if metrics.skill_development < self.development_thresholds['satisfactory']:
            barriers.append('技能发展机会不足')
        if metrics.career_advancement < self.development_thresholds['satisfactory']:
            barriers.append('职业晋升通道不畅')
        if metrics.learning_opportunities < self.development_thresholds['satisfactory']:
            barriers.append('学习发展资源有限')
        if metrics.mentorship_quality < self.development_thresholds['satisfactory']:
            barriers.append('缺乏有效导师指导')
        if metrics.networking < self.development_thresholds['satisfactory']:
            barriers.append('职业网络建设不足')
        if metrics.work_challenges < self.development_thresholds['satisfactory']:
            barriers.append('工作挑战性不足')
        if metrics.future_prospects < self.development_thresholds['satisfactory']:
            barriers.append('职业前景不明确')
        
        return barriers
    
    def _assess_growth_potential(self, metrics: CareerMetrics, 
                               career_stage: CareerStage) -> Dict[str, Any]:
        """评估成长潜力"""
        # 计算潜力分数
        potential_score = (
            metrics.skill_development * 0.3 +
            metrics.learning_opportunities * 0.25 +
            metrics.work_challenges * 0.2 +
            metrics.future_prospects * 0.15 +
            metrics.career_advancement * 0.1
        )
        
        # 根据职业阶段调整潜力评估
        stage_multipliers = {
            CareerStage.ENTRY: 1.2,      # 入职期潜力大
            CareerStage.GROWTH: 1.1,     # 成长期仍有潜力
            CareerStage.MATURE: 0.9,     # 成熟期潜力相对稳定
            CareerStage.DECLINE: 0.7,    # 衰退期潜力下降
            CareerStage.TRANSITION: 1.0  # 转换期潜力待定
        }
        
        adjusted_potential = potential_score * stage_multipliers.get(career_stage, 1.0)
        
        return {
            'raw_potential_score': potential_score,
            'adjusted_potential_score': min(1.0, adjusted_potential),
            'potential_level': self._determine_potential_level(adjusted_potential),
            'stage_appropriate': self._assess_stage_appropriateness(career_stage, adjusted_potential)
        }
    
    def _predict_development_trajectory(self, metrics: CareerMetrics, 
                                      career_stage: CareerStage, 
                                      work_experience: float) -> Dict[str, Any]:
        """预测发展轨迹"""
        # 基于当前指标预测未来发展
        current_score = self._calculate_development_score(metrics)
        
        # 模拟不同时间点的发展轨迹
        trajectories = {
            '6_months': self._predict_short_term_trajectory(current_score, metrics, 0.5),
            '1_year': self._predict_medium_term_trajectory(current_score, metrics, 1),
            '3_years': self._predict_long_term_trajectory(current_score, metrics, 3)
        }
        
        return {
            'current_position': current_score,
            'trajectory_projections': trajectories,
            'development_risk_factors': self._identify_trajectory_risks(metrics),
            'optimization_opportunities': self._identify_optimization_opportunities(metrics)
        }
    
    def _predict_short_term_trajectory(self, current_score: float, 
                                     metrics: CareerMetrics, months: float) -> float:
        """预测短期发展轨迹"""
        # 短期发展主要看学习机会和工作挑战
        growth_factors = (
            metrics.learning_opportunities * 0.6 +
            metrics.work_challenges * 0.4
        )
        
        # 应用时间衰减
        time_factor = months / 12  # 转换为年
        growth_impact = growth_factors * time_factor * 0.1  # 最多10%的增长
        
        return min(1.0, current_score + growth_impact)
    
    def _predict_medium_term_trajectory(self, current_score: float, 
                                      metrics: CareerMetrics, years: float) -> float:
        """预测中期发展轨迹"""
        # 中期发展看技能发展和职业晋升
        growth_factors = (
            metrics.skill_development * 0.4 +
            metrics.career_advancement * 0.3 +
            metrics.future_prospects * 0.3
        )
        
        growth_impact = growth_factors * years * 0.15  # 最多15%的增长
        
        return min(1.0, current_score + growth_impact)
    
    def _predict_long_term_trajectory(self, current_score: float, 
                                    metrics: CareerMetrics, years: float) -> float:
        """预测长期发展轨迹"""
        # 长期发展看综合指标
        growth_factors = self._calculate_development_score(metrics)
        
        growth_impact = growth_factors * years * 0.2  # 最多20%的增长
        
        return min(1.0, current_score + growth_impact)
    
    def _assess_alienation_correlation(self, metrics: CareerMetrics) -> Dict[str, float]:
        """评估与职业异化的相关性"""
        # 职业发展受限与劳动异化的相关性
        alienation_correlation = 1 - (
            metrics.skill_development * 0.25 +
            metrics.work_challenges * 0.2 +
            metrics.autonomy_level * 0.2 +
            metrics.work_meaning * 0.2 +
            metrics.career_advancement * 0.15
        )
        
        return {
            'career_alienation_correlation': max(0, min(1, alienation_correlation)),
            'alienation_risk_level': self._determine_risk_level(alienation_correlation),
            'key_alienation_factors': self._identify_alienation_factors(metrics)
        }
    
    def _determine_development_level(self, score: float) -> str:
        """确定发展水平"""
        if score >= self.development_thresholds['excellent']:
            return '优秀'
        elif score >= self.development_thresholds['good']:
            return '良好'
        elif score >= self.development_thresholds['satisfactory']:
            return '满意'
        elif score >= self.development_thresholds['needs_improvement']:
            return '需要改进'
        else:
            return '较差'
    
    def _determine_potential_level(self, potential: float) -> str:
        """确定潜力水平"""
        if potential >= 0.8:
            return '高'
        elif potential >= 0.6:
            return '中等'
        elif potential >= 0.4:
            return '一般'
        else:
            return '低'
    
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
    
    def _assess_stage_appropriateness(self, career_stage: CareerStage, potential: float) -> str:
        """评估阶段适宜性"""
        stage_expectations = {
            CareerStage.ENTRY: (0.3, 0.7),
            CareerStage.GROWTH: (0.4, 0.8),
            CareerStage.MATURE: (0.5, 0.9),
            CareerStage.DECLINE: (0.2, 0.6),
            CareerStage.TRANSITION: (0.3, 0.8)
        }
        
        min_exp, max_exp = stage_expectations.get(career_stage, (0.3, 0.7))
        
        if min_exp <= potential <= max_exp:
            return '符合阶段期望'
        elif potential < min_exp:
            return '低于阶段期望'
        else:
            return '超越阶段期望'
    
    def _identify_trajectory_risks(self, metrics: CareerMetrics) -> List[str]:
        """识别发展轨迹风险"""
        risks = []
        
        if metrics.learning_opportunities < 0.4:
            risks.append('学习机会不足影响长期发展')
        if metrics.future_prospects < 0.4:
            risks.append('职业前景不明影响发展动力')
        if metrics.work_challenges < 0.4:
            risks.append('挑战性不足限制能力提升')
        if metrics.career_advancement < 0.4:
            risks.append('晋升通道不畅影响发展积极性')
        
        return risks
    
    def _identify_optimization_opportunities(self, metrics: CareerMetrics) -> List[str]:
        """识别优化机会"""
        opportunities = []
        
        if metrics.learning_opportunities > 0.7:
            opportunities.append('充分利用学习机会加速发展')
        if metrics.mentorship_quality > 0.7:
            opportunities.append('加强导师指导提升发展效率')
        if metrics.networking > 0.7:
            opportunities.append('扩展职业网络创造更多机会')
        if metrics.work_challenges > 0.7:
            opportunities.append('承担更多挑战促进能力提升')
        
        return opportunities
    
    def _identify_alienation_factors(self, metrics: CareerMetrics) -> List[str]:
        """识别异化因素"""
        factors = []
        
        if metrics.skill_development < 0.5:
            factors.append('技能发展受限导致能力异化')
        if metrics.autonomy_level < 0.5:
            factors.append('工作自主性不足导致异化')
        if metrics.work_meaning < 0.5:
            factors.append('工作意义感缺失导致本质异化')
        if metrics.career_advancement < 0.5:
            factors.append('职业发展受限导致发展异化')
        
        return factors
    
    def _generate_development_recommendations(self, metrics: CareerMetrics) -> List[str]:
        """生成发展建议"""
        recommendations = []
        
        if metrics.skill_development < 0.6:
            recommendations.append('积极参与技能培训和能力提升项目')
        if metrics.learning_opportunities < 0.6:
            recommendations.append('主动寻求学习和发展机会')
        if metrics.networking < 0.6:
            recommendations.append('加强职业网络建设和人际关系维护')
        if metrics.mentorship_quality < 0.6:
            recommendations.append('寻找或建立有效的导师关系')
        if metrics.work_challenges < 0.6:
            recommendations.append('主动承担更具挑战性的工作任务')
        if metrics.future_prospects < 0.6:
            recommendations.append('明确职业发展目标和规划路径')
        
        return recommendations
    
    def batch_evaluate_career(self, career_dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量评估职业发展"""
        if not career_dataset:
            return {'error': '数据为空'}
        
        results = []
        for data in career_dataset:
            result = self.evaluate_career_development(data)
            results.append(result)
        
        # 计算统计汇总
        development_scores = [r['overall_development_score'] for r in results]
        
        return {
            'individual_results': results,
            'statistics': {
                'mean_development_score': np.mean(development_scores),
                'median_development_score': np.median(development_scores),
                'std_development_score': np.std(development_scores),
                'excellent_developers': sum(1 for s in development_scores if s >= 0.85),
                'poor_developers': sum(1 for s in development_scores if s < 0.40),
                'total_evaluated': len(career_dataset)
            },
            'evaluation_timestamp': datetime.now().isoformat()
        }


def main():
    """主函数 - 用于测试"""
    evaluator = CareerDevelopmentEvaluator()
    
    # 测试数据
    test_data = {
        'work_experience_years': 3,
        'current_position_level': 2,
        'metrics': {
            'skill_development': 0.7,
            'career_advancement': 0.5,
            'learning_opportunities': 0.6,
            'mentorship_quality': 0.4,
            'networking': 0.5,
            'work_challenges': 0.6,
            'recognition': 0.7,
            'autonomy_level': 0.5,
            'work_meaning': 0.6,
            'future_prospects': 0.5
        }
    }
    
    # 评估职业发展
    result = evaluator.evaluate_career_development(test_data)
    
    # 打印结果
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()