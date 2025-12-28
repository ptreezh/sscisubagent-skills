#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异化分析核心引擎
Alienation Analysis Core Engine

统一处理所有异化分析功能，减少模块依赖，提高可信度和维护性。
最小化外部依赖，使用纯Python实现核心功能。

作者: socienceAI.com
版本: 2.0.0 (优化版)
日期: 2025-12-21
"""

import json
import math
import statistics
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum
import warnings

# 版本兼容性处理
try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False
    warnings.warn("NumPy not available, using fallback implementations")

try:
    import pandas as pd
    HAS_PANDAS = True
except ImportError:
    HAS_PANDAS = False


class AlienationType(Enum):
    """异化类型枚举"""
    LABOR = "labor"
    SOCIAL = "social"
    CONSUMPTION = "consumption"
    TECHNOLOGY = "technology"


@dataclass
class AlienationMetrics:
    """异化指标数据类"""
    # 劳动异化指标
    work_autonomy: float = 0.5          # 工作自主性
    work_meaning: float = 0.5           # 工作意义感
    work_satisfaction: float = 0.5      # 工作满意度
    skill_development: float = 0.5      # 技能发展机会
    
    # 社会异化指标
    relationship_quality: float = 0.5   # 关系质量
    social_connection: float = 0.5      # 社会连接
    community_participation: float = 0.5  # 社区参与
    social_support: float = 0.5         # 社会支持
    
    # 消费异化指标
    consumption_rationality: float = 0.5  # 消费理性
    materialism_level: float = 0.5       # 物质主义程度
    consumption_satisfaction: float = 0.5 # 消费满意度
    debt_level: float = 0.5              # 债务水平
    
    # 技术异化指标
    technology_dependency: float = 0.5   # 技术依赖
    digital_wellbeing: float = 0.5       # 数字幸福感
    technology_control: float = 0.5      # 技术控制感
    digital_balance: float = 0.5         # 数字平衡


@dataclass
class AlienationResult:
    """异化分析结果"""
    alienation_score: float = 0.0
    primary_alienation_type: str = ""
    alienation_level: str = ""
    analysis_dimensions: Dict[str, float] = field(default_factory=dict)
    risk_factors: List[str] = field(default_factory=list)
    intervention_priorities: List[str] = field(default_factory=list)
    success: bool = True
    error_message: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class AlienationAnalysisEngine:
    """异化分析核心引擎"""
    
    def __init__(self):
        """初始化分析引擎"""
        self.version = "2.0.0"
        self.minimal_mode = not HAS_NUMPY  # 如果没有numpy，使用最小模式
        
        # 异化类型权重配置
        self.alienation_weights = {
            'labor': {
                'work_autonomy': 0.25,
                'work_meaning': 0.30,
                'work_satisfaction': 0.25,
                'skill_development': 0.20
            },
            'social': {
                'relationship_quality': 0.30,
                'social_connection': 0.25,
                'community_participation': 0.20,
                'social_support': 0.25
            },
            'consumption': {
                'consumption_rationality': 0.30,
                'materialism_level': 0.25,
                'consumption_satisfaction': 0.25,
                'debt_level': 0.20
            },
            'technology': {
                'technology_dependency': 0.30,
                'digital_wellbeing': 0.25,
                'technology_control': 0.25,
                'digital_balance': 0.20
            }
        }
        
        # 异化程度阈值
        self.alienation_thresholds = {
            'minimal': 0.20,
            'mild': 0.40,
            'moderate': 0.60,
            'severe': 0.80
        }
    
    def analyze_alienation(self, metrics_data: Dict[str, Any]) -> AlienationResult:
        """
        核心异化分析功能
        
        Args:
            metrics_data: 异化指标数据
            
        Returns:
            AlienationResult: 分析结果
        """
        try:
            # 创建指标对象
            metrics = self._create_metrics_object(metrics_data)
            
            # 计算各类异化分数
            alienation_scores = self._calculate_alienation_scores(metrics)
            
            # 确定主要异化类型
            primary_type = self._determine_primary_alienation_type(alienation_scores)
            
            # 确定异化程度
            alienation_level = self._assess_alienation_level(alienation_scores[primary_type])
            
            # 分析具体维度
            dimension_analysis = self._analyze_dimensions(metrics, primary_type)
            
            # 识别风险因素
            risk_factors = self._identify_risk_factors(metrics, primary_type)
            
            # 生成干预优先级
            intervention_priorities = self._generate_intervention_priorities(
                metrics, primary_type, alienation_scores
            )
            
            return AlienationResult(
                alienation_score=alienation_scores[primary_type],
                primary_alienation_type=primary_type,
                alienation_level=alienation_level,
                analysis_dimensions=dimension_analysis,
                risk_factors=risk_factors,
                intervention_priorities=intervention_priorities,
                success=True
            )
            
        except Exception as e:
            return AlienationResult(
                success=False,
                error_message=f"异化分析失败: {str(e)}"
            )
    
    def _create_metrics_object(self, data: Dict[str, Any]) -> AlienationMetrics:
        """创建异化指标对象"""
        # 提取指标数据，提供默认值
        metrics_dict = {}
        
        # 劳动异化指标
        metrics_dict.update({
            'work_autonomy': data.get('work_autonomy', 0.5),
            'work_meaning': data.get('work_meaning', 0.5),
            'work_satisfaction': data.get('work_satisfaction', 0.5),
            'skill_development': data.get('skill_development', 0.5)
        })
        
        # 社会异化指标
        metrics_dict.update({
            'relationship_quality': data.get('relationship_quality', 0.5),
            'social_connection': data.get('social_connection', 0.5),
            'community_participation': data.get('community_participation', 0.5),
            'social_support': data.get('social_support', 0.5)
        })
        
        # 消费异化指标
        metrics_dict.update({
            'consumption_rationality': data.get('consumption_rationality', 0.5),
            'materialism_level': data.get('materialism_level', 0.5),
            'consumption_satisfaction': data.get('consumption_satisfaction', 0.5),
            'debt_level': data.get('debt_level', 0.5)
        })
        
        # 技术异化指标
        metrics_dict.update({
            'technology_dependency': data.get('technology_dependency', 0.5),
            'digital_wellbeing': data.get('digital_wellbeing', 0.5),
            'technology_control': data.get('technology_control', 0.5),
            'digital_balance': data.get('digital_balance', 0.5)
        })
        
        return AlienationMetrics(**metrics_dict)
    
    def _calculate_alienation_scores(self, metrics: AlienationMetrics) -> Dict[str, float]:
        """计算各类异化分数"""
        scores = {}
        
        # 计算劳动异化分数 (分数越低，异化越严重)
        labor_score = (
            (1 - metrics.work_autonomy) * self.alienation_weights['labor']['work_autonomy'] +
            (1 - metrics.work_meaning) * self.alienation_weights['labor']['work_meaning'] +
            (1 - metrics.work_satisfaction) * self.alienation_weights['labor']['work_satisfaction'] +
            (1 - metrics.skill_development) * self.alienation_weights['labor']['skill_development']
        )
        scores['labor'] = min(1.0, labor_score)
        
        # 计算社会异化分数
        social_score = (
            (1 - metrics.relationship_quality) * self.alienation_weights['social']['relationship_quality'] +
            (1 - metrics.social_connection) * self.alienation_weights['social']['social_connection'] +
            (1 - metrics.community_participation) * self.alienation_weights['social']['community_participation'] +
            (1 - metrics.social_support) * self.alienation_weights['social']['social_support']
        )
        scores['social'] = min(1.0, social_score)
        
        # 计算消费异化分数
        consumption_score = (
            (1 - metrics.consumption_rationality) * self.alienation_weights['consumption']['consumption_rationality'] +
            metrics.materialism_level * self.alienation_weights['consumption']['materialism_level'] +
            (1 - metrics.consumption_satisfaction) * self.alienation_weights['consumption']['consumption_satisfaction'] +
            metrics.debt_level * self.alienation_weights['consumption']['debt_level']
        )
        scores['consumption'] = min(1.0, consumption_score)
        
        # 计算技术异化分数
        technology_score = (
            metrics.technology_dependency * self.alienation_weights['technology']['technology_dependency'] +
            (1 - metrics.digital_wellbeing) * self.alienation_weights['technology']['digital_wellbeing'] +
            (1 - metrics.technology_control) * self.alienation_weights['technology']['technology_control'] +
            (1 - metrics.digital_balance) * self.alienation_weights['technology']['digital_balance']
        )
        scores['technology'] = min(1.0, technology_score)
        
        return scores
    
    def _determine_primary_alienation_type(self, scores: Dict[str, float]) -> str:
        """确定主要异化类型"""
        if not scores:
            return "social"  # 默认类型
        
        return max(scores, key=scores.get)
    
    def _assess_alienation_level(self, score: float) -> str:
        """评估异化程度"""
        if score >= self.alienation_thresholds['severe']:
            return "严重异化"
        elif score >= self.alienation_thresholds['moderate']:
            return "中度异化"
        elif score >= self.alienation_thresholds['mild']:
            return "轻度异化"
        elif score >= self.alienation_thresholds['minimal']:
            return "微度异化"
        else:
            return "正常状态"
    
    def _analyze_dimensions(self, metrics: AlienationMetrics, primary_type: str) -> Dict[str, float]:
        """分析具体维度"""
        if primary_type == 'labor':
            return {
                '工作自主性': 1 - metrics.work_autonomy,
                '工作意义感': 1 - metrics.work_meaning,
                '工作满意度': 1 - metrics.work_satisfaction,
                '技能发展': 1 - metrics.skill_development
            }
        elif primary_type == 'social':
            return {
                '关系质量': 1 - metrics.relationship_quality,
                '社会连接': 1 - metrics.social_connection,
                '社区参与': 1 - metrics.community_participation,
                '社会支持': 1 - metrics.social_support
            }
        elif primary_type == 'consumption':
            return {
                '消费理性': 1 - metrics.consumption_rationality,
                '物质主义': metrics.materialism_level,
                '消费满意度': 1 - metrics.consumption_satisfaction,
                '债务水平': metrics.debt_level
            }
        elif primary_type == 'technology':
            return {
                '技术依赖': metrics.technology_dependency,
                '数字幸福感': 1 - metrics.digital_wellbeing,
                '技术控制': 1 - metrics.technology_control,
                '数字平衡': 1 - metrics.digital_balance
            }
        
        return {}
    
    def _identify_risk_factors(self, metrics: AlienationMetrics, primary_type: str) -> List[str]:
        """识别风险因素"""
        risk_factors = []
        
        # 通用风险因素
        if primary_type == 'labor':
            if metrics.work_autonomy < 0.3:
                risk_factors.append("工作自主性严重不足")
            if metrics.work_meaning < 0.3:
                risk_factors.append("工作意义感严重缺失")
            if metrics.work_satisfaction < 0.3:
                risk_factors.append("工作满意度严重偏低")
            if metrics.skill_development < 0.3:
                risk_factors.append("技能发展机会严重受限")
                
        elif primary_type == 'social':
            if metrics.relationship_quality < 0.3:
                risk_factors.append("人际关系质量严重不佳")
            if metrics.social_connection < 0.3:
                risk_factors.append("社会连接严重不足")
            if metrics.community_participation < 0.3:
                risk_factors.append("社区参与严重缺乏")
            if metrics.social_support < 0.3:
                risk_factors.append("社会支持系统严重薄弱")
                
        elif primary_type == 'consumption':
            if metrics.consumption_rationality < 0.3:
                risk_factors.append("消费理性严重不足")
            if metrics.materialism_level > 0.7:
                risk_factors.append("物质主义倾向过于严重")
            if metrics.debt_level > 0.7:
                risk_factors.append("债务负担过于沉重")
            if metrics.consumption_satisfaction < 0.3:
                risk_factors.append("消费满意度严重偏低")
                
        elif primary_type == 'technology':
            if metrics.technology_dependency > 0.7:
                risk_factors.append("技术依赖程度过于严重")
            if metrics.digital_wellbeing < 0.3:
                risk_factors.append("数字幸福感严重不足")
            if metrics.technology_control < 0.3:
                risk_factors.append("技术控制感严重缺失")
            if metrics.digital_balance < 0.3:
                risk_factors.append("数字生活严重失衡")
        
        return risk_factors
    
    def _generate_intervention_priorities(self, metrics: AlienationMetrics, 
                                        primary_type: str, 
                                        scores: Dict[str, float]) -> List[str]:
        """生成干预优先级"""
        priorities = []
        
        # 基于主要异化类型生成优先级
        if primary_type == 'labor':
            priorities.extend([
                "提升工作自主性和创造性",
                "增强工作意义感和价值认同",
                "改善工作条件和满意度",
                "提供技能发展机会"
            ])
        elif primary_type == 'social':
            priorities.extend([
                "改善人际关系质量",
                "扩大和深化社会连接",
                "积极参与社区活动",
                "建立社会支持网络"
            ])
        elif primary_type == 'consumption':
            priorities.extend([
                "提升消费理性和判断力",
                "降低物质主义倾向",
                "控制债务和财务风险",
                "提高消费满意度"
            ])
        elif primary_type == 'technology':
            priorities.extend([
                "减少技术依赖程度",
                "提升数字幸福感",
                "增强技术控制能力",
                "建立数字生活平衡"
            ])
        
        # 基于分数排序优先级
        if scores[primary_type] > 0.7:
            priorities.insert(0, "紧急干预：当前异化程度严重")
        elif scores[primary_type] > 0.5:
            priorities.insert(0, "重要干预：当前异化程度较高")
        
        return priorities
    
    def batch_analyze(self, dataset: List[Dict[str, Any]]) -> Dict[str, Any]:
        """批量异化分析"""
        results = []
        for i, data in enumerate(dataset):
            try:
                result = self.analyze_alienation(data)
                result.individual_id = f"individual_{i+1}"
                results.append(result)
            except Exception as e:
                results.append(AlienationResult(
                    success=False,
                    error_message=f"个体 {i+1} 分析失败: {str(e)}"
                ))
        
        # 计算统计汇总
        successful_results = [r for r in results if r.success]
        
        if not successful_results:
            return {
                'error': '所有分析都失败了',
                'results': results
            }
        
        # 统计信息
        alienation_scores = [r.alienation_score for r in successful_results]
        
        # 类型分布统计
        type_distribution = {}
        for result in successful_results:
            atype = result.primary_alienation_type
            type_distribution[atype] = type_distribution.get(atype, 0) + 1
        
        # 程度分布统计
        level_distribution = {}
        for result in successful_results:
            level = result.alienation_level
            level_distribution[level] = level_distribution.get(level, 0) + 1
        
        return {
            'individual_results': results,
            'summary_statistics': {
                'total_analyzed': len(dataset),
                'successful_analysis': len(successful_results),
                'failure_count': len(dataset) - len(successful_results),
                'mean_alienation_score': statistics.mean(alienation_scores) if alienation_scores else 0,
                'median_alienation_score': statistics.median(alienation_scores) if alienation_scores else 0,
                'alienation_type_distribution': type_distribution,
                'alienation_level_distribution': level_distribution
            },
            'analysis_timestamp': datetime.now().isoformat(),
            'engine_version': self.version
        }
    
    def get_analysis_template(self) -> Dict[str, Any]:
        """获取分析模板"""
        return {
            'labor_indicators': {
                'work_autonomy': 0.5,
                'work_meaning': 0.5,
                'work_satisfaction': 0.5,
                'skill_development': 0.5
            },
            'social_indicators': {
                'relationship_quality': 0.5,
                'social_connection': 0.5,
                'community_participation': 0.5,
                'social_support': 0.5
            },
            'consumption_indicators': {
                'consumption_rationality': 0.5,
                'materialism_level': 0.5,
                'consumption_satisfaction': 0.5,
                'debt_level': 0.5
            },
            'technology_indicators': {
                'technology_dependency': 0.5,
                'digital_wellbeing': 0.5,
                'technology_control': 0.5,
                'digital_balance': 0.5
            }
        }
    
    def export_results(self, result: AlienationResult, format: str = 'json') -> str:
        """导出分析结果"""
        if format.lower() == 'json':
            return json.dumps({
                'alienation_score': result.alienation_score,
                'primary_alienation_type': result.primary_alienation_type,
                'alienation_level': result.alienation_level,
                'analysis_dimensions': result.analysis_dimensions,
                'risk_factors': result.risk_factors,
                'intervention_priorities': result.intervention_priorities,
                'timestamp': result.timestamp,
                'success': result.success,
                'error_message': result.error_message
            }, ensure_ascii=False, indent=2)
        else:
            # 简单文本格式
            lines = [
                f"异化分析报告",
                f"=" * 20,
                f"主要异化类型: {result.primary_alienation_type}",
                f"异化程度: {result.alienation_level}",
                f"异化分数: {result.alienation_score:.3f}",
                f"",
                f"具体维度分析:",
            ]
            
            for dimension, score in result.analysis_dimensions.items():
                lines.append(f"  {dimension}: {score:.3f}")
            
            lines.extend([
                "",
                f"风险因素:",
            ])
            
            for factor in result.risk_factors:
                lines.append(f"  - {factor}")
            
            lines.extend([
                "",
                f"干预优先级:",
            ])
            
            for priority in result.intervention_priorities:
                lines.append(f"  - {priority}")
            
            lines.append(f"\n分析时间: {result.timestamp}")
            
            return "\n".join(lines)


def main():
    """主函数 - 测试用例"""
    # 创建分析引擎
    engine = AlienationAnalysisEngine()
    
    # 测试数据
    test_data = {
        'work_autonomy': 0.3,  # 工作自主性低
        'work_meaning': 0.2,   # 工作意义感低
        'work_satisfaction': 0.4,  # 工作满意度中等
        'skill_development': 0.3,  # 技能发展机会少
        
        'relationship_quality': 0.6,
        'social_connection': 0.5,
        'community_participation': 0.4,
        'social_support': 0.5,
        
        'consumption_rationality': 0.7,
        'materialism_level': 0.6,
        'consumption_satisfaction': 0.5,
        'debt_level': 0.4,
        
        'technology_dependency': 0.8,  # 技术依赖高
        'digital_wellbeing': 0.3,     # 数字幸福感低
        'technology_control': 0.4,    # 技术控制感低
        'digital_balance': 0.3        # 数字平衡差
    }
    
    # 执行分析
    print("异化分析引擎测试")
    print("=" * 30)
    
    result = engine.analyze_alienation(test_data)
    
    if result.success:
        print(f"✅ 分析成功!")
        print(f"主要异化类型: {result.primary_alienation_type}")
        print(f"异化程度: {result.alienation_level}")
        print(f"异化分数: {result.alienation_score:.3f}")
        print(f"\n具体维度:")
        for dimension, score in result.analysis_dimensions.items():
            print(f"  {dimension}: {score:.3f}")
        print(f"\n风险因素:")
        for factor in result.risk_factors:
            print(f"  - {factor}")
        print(f"\n干预优先级:")
        for priority in result.intervention_priorities:
            print(f"  - {priority}")
    else:
        print(f"❌ 分析失败: {result.error_message}")
    
    # 导出结果
    print(f"\n导出结果:")
    print(engine.export_results(result, 'text'))


if __name__ == '__main__':
    main()
