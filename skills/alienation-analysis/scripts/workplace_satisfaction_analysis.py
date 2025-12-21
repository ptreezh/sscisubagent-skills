#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
工作场所满意度分析器
分析劳动者的工作满意度相关指标和数据
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SatisfactionMetrics:
    """满意度指标数据类"""
    overall_satisfaction: float  # 总体满意度 (0-1)
    job_security: float          # 工作安全感
    work_environment: float      # 工作环境满意度
    career_development: float    # 职业发展满意度
    compensation: float          # 薪酬满意度
    work_life_balance: float     # 工作生活平衡
    management_satisfaction: float  # 管理满意度
    autonomy: float              # 工作自主性
    skill_utilization: float     # 技能运用程度
    meaningful_work: float       # 工作意义感


class WorkplaceSatisfactionAnalyzer:
    """工作场所满意度分析器"""
    
    def __init__(self):
        self.satisfaction_weights = {
            'overall_satisfaction': 0.25,
            'job_security': 0.15,
            'work_environment': 0.10,
            'career_development': 0.15,
            'compensation': 0.10,
            'work_life_balance': 0.10,
            'management_satisfaction': 0.05,
            'autonomy': 0.05,
            'skill_utilization': 0.03,
            'meaningful_work': 0.02
        }
        
        self.satisfaction_thresholds = {
            'high': 0.8,
            'good': 0.6,
            'moderate': 0.4,
            'low': 0.2
        }
    
    def analyze_workplace_satisfaction(self, satisfaction_data: Dict[str, float]) -> Dict[str, Any]:
        """
        分析工作场所满意度
        
        Args:
            satisfaction_data: 满意度数据字典
            
        Returns:
            分析结果字典
        """
        # 创建满意度指标对象
        metrics = self._create_satisfaction_metrics(satisfaction_data)
        
        # 计算综合满意度
        overall_satisfaction = self._calculate_weighted_satisfaction(metrics)
        
        # 分析满意度维度
        dimension_analysis = self._analyze_satisfaction_dimensions(metrics)
        
        # 识别满意度问题
        problem_areas = self._identify_satisfaction_problems(metrics)
        
        # 评估工作动机
        motivation_assessment = self._assess_work_motivation(metrics)
        
        # 预测离职风险
        turnover_risk = self._assess_turnover_risk(overall_satisfaction, dimension_analysis)
        
        return {
            'overall_satisfaction': overall_satisfaction,
            'satisfaction_level': self._determine_satisfaction_level(overall_satisfaction),
            'dimension_analysis': dimension_analysis,
            'problem_areas': problem_areas,
            'motivation_assessment': motivation_assessment,
            'turnover_risk': turnover_risk,
            'improvement_priorities': self._prioritize_improvements(metrics),
            'alienation_correlation': self._assess_alienation_correlation(metrics),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _create_satisfaction_metrics(self, data: Dict[str, float]) -> SatisfactionMetrics:
        """创建满意度指标对象"""
        # 设置默认值
        default_values = {
            'overall_satisfaction': 0.5,
            'job_security': 0.5,
            'work_environment': 0.5,
            'career_development': 0.5,
            'compensation': 0.5,
            'work_life_balance': 0.5,
            'management_satisfaction': 0.5,
            'autonomy': 0.5,
            'skill_utilization': 0.5,
            'meaningful_work': 0.5
        }
        
        # 合并数据
        merged_data = {**default_values, **data}
        
        return SatisfactionMetrics(**merged_data)
    
    def _calculate_weighted_satisfaction(self, metrics: SatisfactionMetrics) -> float:
        """计算加权满意度分数"""
        weights = self.satisfaction_weights
        values = [
            metrics.overall_satisfaction * weights['overall_satisfaction'],
            metrics.job_security * weights['job_security'],
            metrics.work_environment * weights['work_environment'],
            metrics.career_development * weights['career_development'],
            metrics.compensation * weights['compensation'],
            metrics.work_life_balance * weights['work_life_balance'],
            metrics.management_satisfaction * weights['management_satisfaction'],
            metrics.autonomy * weights['autonomy'],
            metrics.skill_utilization * weights['skill_utilization'],
            metrics.meaningful_work * weights['meaningful_work']
        ]
        
        return sum(values)
    
    def _analyze_satisfaction_dimensions(self, metrics: SatisfactionMetrics) -> Dict[str, float]:
        """分析各满意度维度"""
        return {
            'economic_satisfaction': (metrics.compensation + metrics.job_security) / 2,
            'social_satisfaction': (metrics.work_environment + metrics.management_satisfaction) / 2,
            'development_satisfaction': (metrics.career_development + metrics.skill_utilization) / 2,
            'autonomy_satisfaction': (metrics.autonomy + metrics.meaningful_work) / 2,
            'life_balance_satisfaction': metrics.work_life_balance
        }
    
    def _identify_satisfaction_problems(self, metrics: SatisfactionMetrics) -> List[str]:
        """识别满意度问题领域"""
        problems = []
        
        if metrics.overall_satisfaction < self.satisfaction_thresholds['moderate']:
            problems.append('总体工作满意度偏低')
        if metrics.job_security < self.satisfaction_thresholds['moderate']:
            problems.append('工作安全感不足')
        if metrics.career_development < self.satisfaction_thresholds['moderate']:
            problems.append('职业发展机会有限')
        if metrics.compensation < self.satisfaction_thresholds['moderate']:
            problems.append('薪酬满意度不足')
        if metrics.work_life_balance < self.satisfaction_thresholds['moderate']:
            problems.append('工作生活平衡失调')
        if metrics.autonomy < self.satisfaction_thresholds['moderate']:
            problems.append('工作自主性不足')
        if metrics.meaningful_work < self.satisfaction_thresholds['moderate']:
            problems.append('工作意义感缺失')
        
        return problems
    
    def _assess_work_motivation(self, metrics: SatisfactionMetrics) -> Dict[str, float]:
        """评估工作动机"""
        intrinsic_motivation = (
            metrics.meaningful_work * 0.4 +
            metrics.autonomy * 0.3 +
            metrics.skill_utilization * 0.3
        )
        
        extrinsic_motivation = (
            metrics.compensation * 0.5 +
            metrics.job_security * 0.3 +
            metrics.career_development * 0.2
        )
        
        return {
            'intrinsic_motivation': intrinsic_motivation,
            'extrinsic_motivation': extrinsic_motivation,
            'motivation_balance': 1 - abs(intrinsic_motivation - extrinsic_motivation),
            'motivation_health': (intrinsic_motivation + extrinsic_motivation) / 2
        }
    
    def _assess_turnover_risk(self, overall_satisfaction: float, 
                            dimension_analysis: Dict[str, float]) -> Dict[str, float]:
        """评估离职风险"""
        # 基于满意度计算离职风险
        base_risk = 1 - overall_satisfaction
        
        # 考虑各个维度的影响
        risk_factors = [
            dimension_analysis.get('economic_satisfaction', 0.5),
            dimension_analysis.get('development_satisfaction', 0.5),
            dimension_analysis.get('autonomy_satisfaction', 0.5)
        ]
        
        risk_adjustment = np.mean(risk_factors)
        adjusted_risk = base_risk * (1 + (1 - risk_adjustment) * 0.5)
        
        return {
            'overall_turnover_risk': min(1.0, adjusted_risk),
            'risk_level': self._determine_risk_level(adjusted_risk),
            'key_risk_factors': self._identify_risk_factors(dimension_analysis)
        }
    
    def _determine_satisfaction_level(self, satisfaction: float) -> str:
        """确定满意度等级"""
        if satisfaction >= self.satisfaction_thresholds['high']:
            return '高'
        elif satisfaction >= self.satisfaction_thresholds['good']:
            return '良好'
        elif satisfaction >= self.satisfaction_thresholds['moderate']:
            return '中等'
        else:
            return '低'
    
    def _determine_risk_level(self, risk: float) -> str:
        """确定风险等级"""
        if risk >= 0.8:
            return '极高'
        elif risk >= 0.6:
            return '高'
        elif risk >= 0.4:
            return '中等'
        else:
            return '低'
    
    def _identify_risk_factors(self, dimension_analysis: Dict[str, float]) -> List[str]:
        """识别风险因素"""
        risk_factors = []
        
        for dimension, score in dimension_analysis.items():
            if score < self.satisfaction_thresholds['moderate']:
                risk_factors.append(f'{dimension}满意度低')
        
        return risk_factors
    
    def _prioritize_improvements(self, metrics: SatisfactionMetrics) -> List[Tuple[str, float]]:
        """确定改进优先级"""
        improvements = [
            ('overall_satisfaction', metrics.overall_satisfaction),
            ('job_security', metrics.job_security),
            ('career_development', metrics.career_development),
            ('compensation', metrics.compensation),
            ('work_life_balance', metrics.work_life_balance),
            ('work_environment', metrics.work_environment),
            ('management_satisfaction', metrics.management_satisfaction),
            ('autonomy', metrics.autonomy),
            ('skill_utilization', metrics.skill_utilization),
            ('meaningful_work', metrics.meaningful_work)
        ]
        
        # 按满意度分数排序，分数越低优先级越高
        improvements.sort(key=lambda x: x[1])
        
        return improvements[:5]  # 返回前5个优先级
    
    def _assess_alienation_correlation(self, metrics: SatisfactionMetrics) -> Dict[str, float]:
        """评估与异化的相关性"""
        # 工作满意度与劳动异化的负相关关系
        labor_alienation_correlation = 1 - (
            metrics.overall_satisfaction * 0.3 +
            metrics.autonomy * 0.25 +
            metrics.meaningful_work * 0.25 +
            metrics.skill_utilization * 0.2
        )
        
        return {
            'labor_alienation_correlation': max(0, min(1, labor_alienation_correlation)),
            'alienation_risk_level': self._determine_risk_level(labor_alienation_correlation),
            'correlation_strength': self._determine_correlation_strength(labor_alienation_correlation)
        }
    
    def _determine_correlation_strength(self, correlation: float) -> str:
        """确定相关性强度"""
        if correlation >= 0.8:
            return '强'
        elif correlation >= 0.6:
            return '中等'
        elif correlation >= 0.4:
            return '弱'
        else:
            return '极弱'
    
    def batch_analyze_satisfaction(self, satisfaction_dataset: List[Dict[str, float]]) -> Dict[str, Any]:
        """批量分析满意度数据"""
        if not satisfaction_dataset:
            return {'error': '数据为空'}
        
        results = []
        for data in satisfaction_dataset:
            result = self.analyze_workplace_satisfaction(data)
            results.append(result)
        
        # 计算统计汇总
        overall_satisfactions = [r['overall_satisfaction'] for r in results]
        
        return {
            'individual_results': results,
            'statistics': {
                'mean_satisfaction': np.mean(overall_satisfactions),
                'median_satisfaction': np.median(overall_satisfactions),
                'std_satisfaction': np.std(overall_satisfactions),
                'high_satisfaction_count': sum(1 for s in overall_satisfactions if s >= 0.8),
                'low_satisfaction_count': sum(1 for s in overall_satisfactions if s < 0.4),
                'total_respondents': len(satisfaction_dataset)
            },
            'analysis_timestamp': datetime.now().isoformat()
        }


def main():
    """主函数 - 用于测试"""
    analyzer = WorkplaceSatisfactionAnalyzer()
    
    # 测试数据
    test_data = {
        'overall_satisfaction': 0.6,
        'job_security': 0.7,
        'work_environment': 0.5,
        'career_development': 0.4,
        'compensation': 0.6,
        'work_life_balance': 0.3,
        'management_satisfaction': 0.7,
        'autonomy': 0.4,
        'skill_utilization': 0.5,
        'meaningful_work': 0.3
    }
    
    # 分析工作满意度
    result = analyzer.analyze_workplace_satisfaction(test_data)
    
    # 打印结果
    import json
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()