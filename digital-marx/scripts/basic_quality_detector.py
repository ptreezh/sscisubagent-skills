#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数字马克思基础质量检测系统
建立多层次、专业化的质量检测机制，确保分析结果的科学性和准确性
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import json
import os
import sys
from datetime import datetime
import unittest
from dataclasses import dataclass
from enum import Enum

# 导入分析器
from dialectical_thinking_analyzer import DialecticalThinkingAnalyzer
from enhanced_historical_materialism_analyzer import EnhancedHistoricalMaterialismAnalyzer


class QualityLevel(Enum):
    """质量等级"""
    EXCELLENT = "优秀"
    GOOD = "良好"
    AVERAGE = "一般"
    POOR = "需要改进"


@dataclass
class QualityMetrics:
    """质量指标"""
    theoretical_accuracy: float
    methodological_soundness: float
    analytical_depth: float
    logical_coherence: float
    practical_relevance: float
    overall_quality: float
    quality_level: QualityLevel


@dataclass
class QualityIssue:
    """质量问题"""
    issue_type: str
    description: str
    severity: str
    suggestion: str


class BasicQualityDetector:
    """基础质量检测器"""
    
    def __init__(self):
        # 初始化分析器
        self.dialectical_analyzer = DialecticalThinkingAnalyzer()
        self.historical_analyzer = EnhancedHistoricalMaterialismAnalyzer()
        
        # 质量标准定义
        self.quality_standards = {
            'theoretical_accuracy': {
                'min_score': 7.0,
                'weight': 0.3,
                'description': '理论准确性检验'
            },
            'methodological_soundness': {
                'min_score': 7.0,
                'weight': 0.25,
                'description': '方法论科学性检验'
            },
            'analytical_depth': {
                'min_score': 6.0,
                'weight': 0.2,
                'description': '分析深度检验'
            },
            'logical_coherence': {
                'min_score': 6.0,
                'weight': 0.15,
                'description': '逻辑连贯性检验'
            },
            'practical_relevance': {
                'min_score': 6.0,
                'weight': 0.1,
                'description': '实践相关性检验'
            }
        }
        
        # 检测历史
        self.detection_history = []
    
    def comprehensive_quality_detection(self, text_data: str) -> Dict:
        """综合质量检测"""
        
        # 执行各项分析
        dialectical_results = self.dialectical_analyzer.comprehensive_dialectical_analysis(text_data)
        historical_results = self.historical_analyzer.comprehensive_historical_materialism_analysis(text_data)
        
        # 计算各项质量指标
        theoretical_accuracy = self._assess_theoretical_accuracy(dialectical_results, historical_results)
        methodological_soundness = self._assess_methodological_soundness(dialectical_results, historical_results)
        analytical_depth = self._assess_analytical_depth(dialectical_results, historical_results)
        logical_coherence = self._assess_logical_coherence(dialectical_results, historical_results)
        practical_relevance = self._assess_practical_relevance(text_data, dialectical_results, historical_results)
        
        # 计算综合质量
        overall_quality = self._calculate_overall_quality(
            theoretical_accuracy, methodological_soundness, 
            analytical_depth, logical_coherence, practical_relevance
        )
        
        # 确定质量等级
        quality_level = self._determine_quality_level(overall_quality)
        
        # 识别质量问题
        quality_issues = self._identify_quality_issues(
            theoretical_accuracy, methodological_soundness, analytical_depth,
            logical_coherence, practical_relevance
        )
        
        # 生成改进建议
        improvement_suggestions = self._generate_improvement_suggestions(quality_issues)
        
        # 构建质量指标对象
        quality_metrics = QualityMetrics(
            theoretical_accuracy=theoretical_accuracy,
            methodological_soundness=methodological_soundness,
            analytical_depth=analytical_depth,
            logical_coherence=logical_coherence,
            practical_relevance=practical_relevance,
            overall_quality=overall_quality,
            quality_level=quality_level
        )
        
        # 检测结果
        detection_result = {
            'quality_metrics': quality_metrics,
            'quality_issues': quality_issues,
            'improvement_suggestions': improvement_suggestions,
            'dialectical_results': dialectical_results,
            'historical_results': historical_results,
            'detection_timestamp': datetime.now().isoformat()
        }
        
        # 记录检测历史
        self._record_detection(detection_result)
        
        return detection_result
    
    def _assess_theoretical_accuracy(self, dialectical_results: Dict, historical_results: Dict) -> float:
        """评估理论准确性"""
        
        # 辩证思维理论准确性
        dialectical_quality = dialectical_results.get('overall_dialectical_level', {}).get('overall_score', 0)
        
        # 历史唯物主义理论准确性
        historical_quality = historical_results.get('overall_theoretical_level', {}).get('overall_score', 0)
        
        # 理论概念使用准确性
        concept_accuracy = self._assess_concept_accuracy(dialectical_results, historical_results)
        
        # 理论逻辑严密性
        logic_accuracy = self._assess_theoretical_logic(dialectical_results, historical_results)
        
        # 综合理论准确性分数
        theoretical_accuracy = (dialectical_quality * 0.3 + 
                              historical_quality * 0.3 + 
                              concept_accuracy * 0.2 + 
                              logic_accuracy * 0.2)
        
        return min(theoretical_accuracy, 10.0)
    
    def _assess_concept_accuracy(self, dialectical_results: Dict, historical_results: Dict) -> float:
        """评估概念使用准确性"""
        
        # 从辩证思维分析中提取概念使用情况
        unity_analysis = dialectical_results.get('unity_of_opposites', {})
        contradictions = unity_analysis.get('contradictions', [])
        
        # 检查矛盾识别的准确性
        contradiction_accuracy = 0
        if contradictions:
            # 检查是否识别了真正的对立统一关系
            valid_contradictions = 0
            for contradiction in contradictions:
                if self._is_valid_contradiction(contradiction):
                    valid_contradictions += 1
            
            contradiction_accuracy = (valid_contradictions / len(contradictions)) * 10
        
        # 从历史唯物主义分析中提取概念使用情况
        contradiction_analysis = historical_results.get('contradiction_analysis', {})
        adaptation_level = contradiction_analysis.get('adaptation_level', {}).get('adaptation_quality', 0)
        
        # 综合概念准确性
        concept_accuracy = (contradiction_accuracy + adaptation_level) / 2
        
        return concept_accuracy
    
    def _is_valid_contradiction(self, contradiction) -> bool:
        """检查矛盾识别是否有效"""
        # 这里应该有更复杂的逻辑来验证矛盾的有效性
        # 简化处理，假设所有识别的矛盾都是有效的
        return True
    
    def _assess_theoretical_logic(self, dialectical_results: Dict, historical_results: Dict) -> float:
        """评估理论逻辑严密性"""
        
        # 辩证思维逻辑性
        dialectical_coherence = dialectical_results.get('internal_connections', {}).get('overall_coherence_score', 0)
        
        # 历史唯物主义逻辑性
        historical_coherence = historical_results.get('internal_connections', {}).get('overall_coherence_score', 0)
        
        # 理论逻辑综合分数
        logic_accuracy = (dialectical_coherence + historical_coherence) / 2
        
        return logic_accuracy
    
    def _assess_methodological_soundness(self, dialectical_results: Dict, historical_results: Dict) -> float:
        """评估方法论科学性"""
        
        # 辩证思维方法论
        dialectical_methodology = self._assess_dialectical_methodology(dialectical_results)
        
        # 历史唯物主义方法论
        historical_methodology = self._assess_historical_methodology(historical_results)
        
        # 方法论科学性综合分数
        methodological_soundness = (dialectical_methodology + historical_methodology) / 2
        
        return methodological_soundness
    
    def _assess_dialectical_methodology(self, dialectical_results: Dict) -> float:
        """评估辩证思维方法论"""
        
        # 检查三大规律的运用
        unity_quality = dialectical_results.get('unity_of_opposites', {}).get('dialectical_quality', {}).get('overall_quality', 0)
        quantity_quality = dialectical_results.get('quantity_quality_change', {}).get('synthesis_quality', 0)
        negation_quality = dialectical_results.get('negation_of_negation', {}).get('synthesis_level', 0)
        
        # 将质量等级转换为分数
        quality_mapping = {'优秀': 9.0, '良好': 7.0, '一般': 5.0, '需要改进': 3.0}
        
        unity_score = quality_mapping.get(unity_quality, 5.0) if isinstance(unity_quality, str) else unity_quality
        quantity_score = quality_mapping.get(quantity_quality, 5.0) if isinstance(quantity_quality, str) else quantity_quality
        negation_score = quality_mapping.get(negation_quality, 5.0) if isinstance(negation_quality, str) else negation_quality
        
        # 辩证方法论分数
        dialectical_methodology = (unity_score + quantity_score + negation_score) / 3
        
        return dialectical_methodology
    
    def _assess_historical_methodology(self, historical_results: Dict) -> float:
        """评估历史唯物主义方法论"""
        
        # 检查三大分析的运用
        contradiction_quality = historical_results.get('contradiction_analysis', {}).get('contradiction_quality', {}).get('overall_quality', 0)
        base_quality = historical_results.get('base_superstructure_analysis', {}).get('base_superstructure_quality', {}).get('overall_quality', 0)
        formation_quality = historical_results.get('formation_analysis', {}).get('formation_quality', {}).get('overall_quality', 0)
        
        # 历史唯物主义方法论分数
        historical_methodology = (contradiction_quality + base_quality + formation_quality) / 3
        
        return historical_methodology
    
    def _assess_analytical_depth(self, dialectical_results: Dict, historical_results: Dict) -> float:
        """评估分析深度"""
        
        # 辩证思维分析深度
        dialectical_depth = self._assess_dialectical_depth(dialectical_results)
        
        # 历史唯物主义分析深度
        historical_depth = self._assess_historical_depth(historical_results)
        
        # 综合分析深度
        analytical_depth = (dialectical_depth + historical_depth) / 2
        
        return analytical_depth
    
    def _assess_dialectical_depth(self, dialectical_results: Dict) -> float:
        """评估辩证思维分析深度"""
        
        # 检查分析的层次性
        contradictions = dialectical_results.get('unity_of_opposites', {}).get('contradictions', [])
        contradiction_depth = min(len(contradictions) * 2, 10)  # 每个矛盾2分，最高10分
        
        # 检查分析的全面性
        unity_score = dialectical_results.get('unity_of_opposites', {}).get('dialectical_quality', {}).get('overall_quality', 0)
        quantity_score = dialectical_results.get('quantity_quality_change', {}).get('synthesis_quality', 0)
        negation_score = dialectical_results.get('negation_of_negation', {}).get('synthesis_level', 0)
        
        # 深度分数
        dialectical_depth = (contradiction_depth + unity_score + quantity_score + negation_score) / 4
        
        return dialectical_depth
    
    def _assess_historical_depth(self, historical_results: Dict) -> float:
        """评估历史唯物主义分析深度"""
        
        # 检查社会形态识别的准确性
        formation_confidence = historical_results.get('formation_analysis', {}).get('current_formation', {}).get('confidence', 0)
        formation_depth = formation_confidence * 10
        
        # 检查主要矛盾分析的深度
        primary_contradiction = historical_results.get('formation_analysis', {}).get('primary_contradiction')
        if primary_contradiction:
            contradiction_intensity = getattr(primary_contradiction, 'contradiction_intensity', 0)
            contradiction_depth = min(contradiction_intensity, 10)
        else:
            contradiction_depth = 0
        
        # 深度分数
        historical_depth = (formation_depth + contradiction_depth) / 2
        
        return historical_depth
    
    def _assess_logical_coherence(self, dialectical_results: Dict, historical_results: Dict) -> float:
        """评估逻辑连贯性"""
        
        # 内部逻辑连贯性
        dialectical_coherence = dialectical_results.get('internal_connections', {}).get('overall_coherence_score', 0)
        historical_coherence = historical_results.get('internal_connections', {}).get('overall_coherence_score', 0)
        
        # 跨模块逻辑连贯性
        cross_module_coherence = self._assess_cross_module_coherence(dialectical_results, historical_results)
        
        # 综合逻辑连贯性
        logical_coherence = (dialectical_coherence + historical_coherence + cross_module_coherence) / 3
        
        return logical_coherence
    
    def _assess_cross_module_coherence(self, dialectical_results: Dict, historical_results: Dict) -> float:
        """评估跨模块逻辑连贯性"""
        
        # 检查辩证思维与历史唯物主义的一致性
        dialectical_level = dialectical_results.get('overall_dialectical_level', {}).get('overall_score', 0)
        historical_level = historical_results.get('overall_theoretical_level', {}).get('overall_score', 0)
        
        # 一致性分数
        coherence_score = 10 - abs(dialectical_level - historical_level)
        
        return max(coherence_score, 0)
    
    def _assess_practical_relevance(self, text_data: str, dialectical_results: Dict, historical_results: Dict) -> float:
        """评估实践相关性"""
        
        # 问题针对性
        problem_targeting = self._assess_problem_targeting(text_data)
        
        # 现实意义
        practical_significance = self._assess_practical_significance(text_data)
        
        # 应用价值
        application_value = self._assess_application_value(dialectical_results, historical_results)
        
        # 综合实践相关性
        practical_relevance = (problem_targeting + practical_significance + application_value) / 3
        
        return practical_relevance
    
    def _assess_problem_targeting(self, text_data: str) -> float:
        """评估问题针对性"""
        
        # 检查是否涉及现实社会问题
        problem_indicators = ['问题', '挑战', '困难', '矛盾', '冲突', '危机', '发展', '改革']
        
        problem_count = 0
        for indicator in problem_indicators:
            if indicator in text_data:
                problem_count += 1
        
        # 针对性分数
        targeting_score = min(problem_count * 2, 10)
        
        return targeting_score
    
    def _assess_practical_significance(self, text_data: str) -> float:
        """评估现实意义"""
        
        # 检查是否涉及现实意义相关词汇
        significance_indicators = ['现实', '实际', '实践', '应用', '指导', '意义', '价值']
        
        significance_count = 0
        for indicator in significance_indicators:
            if indicator in text_data:
                significance_count += 1
        
        # 现实意义分数
        significance_score = min(significance_count * 1.5, 10)
        
        return significance_score
    
    def _assess_application_value(self, dialectical_results: Dict, historical_results: Dict) -> float:
        """评估应用价值"""
        
        # 检查是否提供了具体的分析结论
        dialectical_conclusions = len(dialectical_results.get('overall_dialectical_level', {}).get('improvement_directions', []))
        historical_conclusions = len(historical_results.get('overall_theoretical_level', {}).get('improvement_directions', []))
        
        # 应用价值分数
        application_score = min((dialectical_conclusions + historical_conclusions) * 1.5, 10)
        
        return application_score
    
    def _calculate_overall_quality(self, theoretical_accuracy: float,
                                  methodological_soundness: float,
                                  analytical_depth: float,
                                  logical_coherence: float,
                                  practical_relevance: float) -> float:
        """计算综合质量分数"""
        
        # 根据权重计算综合分数
        weights = self.quality_standards
        
        overall_quality = (
            theoretical_accuracy * weights['theoretical_accuracy']['weight'] +
            methodological_soundness * weights['methodological_soundness']['weight'] +
            analytical_depth * weights['analytical_depth']['weight'] +
            logical_coherence * weights['logical_coherence']['weight'] +
            practical_relevance * weights['practical_relevance']['weight']
        )
        
        return overall_quality
    
    def _determine_quality_level(self, overall_quality: float) -> QualityLevel:
        """确定质量等级"""
        
        if overall_quality >= 8.5:
            return QualityLevel.EXCELLENT
        elif overall_quality >= 7.0:
            return QualityLevel.GOOD
        elif overall_quality >= 5.5:
            return QualityLevel.AVERAGE
        else:
            return QualityLevel.POOR
    
    def _identify_quality_issues(self, theoretical_accuracy: float,
                                 methodological_soundness: float,
                                 analytical_depth: float,
                                 logical_coherence: float,
                                 practical_relevance: float) -> List[QualityIssue]:
        """识别质量问题"""
        
        issues = []
        
        # 检查各项指标是否达标
        if theoretical_accuracy < self.quality_standards['theoretical_accuracy']['min_score']:
            issues.append(QualityIssue(
                issue_type="theoretical_accuracy",
                description=f"理论准确性不足: {theoretical_accuracy:.2f} < {self.quality_standards['theoretical_accuracy']['min_score']}",
                severity="high",
                suggestion="加强马克思主义基本原理的学习和应用"
            ))
        
        if methodological_soundness < self.quality_standards['methodological_soundness']['min_score']:
            issues.append(QualityIssue(
                issue_type="methodological_soundness",
                description=f"方法论科学性不足: {methodological_soundness:.2f} < {self.quality_standards['methodological_soundness']['min_score']}",
                severity="high",
                suggestion="完善辩证思维和历史唯物主义方法论"
            ))
        
        if analytical_depth < self.quality_standards['analytical_depth']['min_score']:
            issues.append(QualityIssue(
                issue_type="analytical_depth",
                description=f"分析深度不足: {analytical_depth:.2f} < {self.quality_standards['analytical_depth']['min_score']}",
                severity="medium",
                suggestion="深化理论分析，增强层次性和全面性"
            ))
        
        if logical_coherence < self.quality_standards['logical_coherence']['min_score']:
            issues.append(QualityIssue(
                issue_type="logical_coherence",
                description=f"逻辑连贯性不足: {logical_coherence:.2f} < {self.quality_standards['logical_coherence']['min_score']}",
                severity="medium",
                suggestion="加强逻辑推理的严密性和一致性"
            ))
        
        if practical_relevance < self.quality_standards['practical_relevance']['min_score']:
            issues.append(QualityIssue(
                issue_type="practical_relevance",
                description=f"实践相关性不足: {practical_relevance:.2f} < {self.quality_standards['practical_relevance']['min_score']}",
                severity="low",
                suggestion="增强分析的现实针对性和应用价值"
            ))
        
        return issues
    
    def _generate_improvement_suggestions(self, quality_issues: List[QualityIssue]) -> List[str]:
        """生成改进建议"""
        
        suggestions = []
        
        # 根据问题类型生成具体建议
        for issue in quality_issues:
            if issue.issue_type == "theoretical_accuracy":
                suggestions.extend([
                    "深入学习马克思主义基本原理",
                    "准确理解和运用核心概念",
                    "避免理论概念的误用和滥用"
                ])
            elif issue.issue_type == "methodological_soundness":
                suggestions.extend([
                    "掌握辩证思维的基本方法",
                    "熟练运用历史唯物主义分析框架",
                    "避免机械唯物主义和教条主义"
                ])
            elif issue.issue_type == "analytical_depth":
                suggestions.extend([
                    "深化理论分析的层次性",
                    "增强分析的全面性和系统性",
                    "避免表面化和简单化倾向"
                ])
            elif issue.issue_type == "logical_coherence":
                suggestions.extend([
                    "加强逻辑推理的严密性",
                    "确保分析结论的一致性",
                    "避免逻辑矛盾和混乱"
                ])
            elif issue.issue_type == "practical_relevance":
                suggestions.extend([
                    "增强分析的现实针对性",
                    "提高理论的应用价值",
                    "避免脱离实际的空泛分析"
                ])
        
        # 去重并返回
        return list(set(suggestions))
    
    def _record_detection(self, detection_result: Dict):
        """记录检测历史"""
        
        detection_record = {
            'timestamp': detection_result['detection_timestamp'],
            'overall_quality': detection_result['quality_metrics'].overall_quality,
            'quality_level': detection_result['quality_metrics'].quality_level.value,
            'issue_count': len(detection_result['quality_issues'])
        }
        
        self.detection_history.append(detection_record)
        
        # 保持历史记录不超过100条
        if len(self.detection_history) > 100:
            self.detection_history = self.detection_history[-100:]
    
    def generate_quality_report(self, detection_result: Dict) -> str:
        """生成质量检测报告"""
        
        quality_metrics = detection_result['quality_metrics']
        quality_issues = detection_result['quality_issues']
        improvement_suggestions = detection_result['improvement_suggestions']
        
        report = []
        report.append("# 数字马克思质量检测报告")
        report.append(f"检测时间: {detection_result['detection_timestamp']}")
        report.append("")
        
        # 总体评估
        report.append("## 总体评估")
        report.append(f"- 综合质量分数: {quality_metrics.overall_quality:.2f}/10")
        report.append(f"- 质量等级: {quality_metrics.quality_level.value}")
        report.append(f"- 检测结果: {'通过' if quality_metrics.quality_level != QualityLevel.POOR else '未通过'}")
        report.append("")
        
        # 各项指标
        report.append("## 各项质量指标")
        report.append(f"- 理论准确性: {quality_metrics.theoretical_accuracy:.2f}/10")
        report.append(f"- 方法论科学性: {quality_metrics.methodological_soundness:.2f}/10")
        report.append(f"- 分析深度: {quality_metrics.analytical_depth:.2f}/10")
        report.append(f"- 逻辑连贯性: {quality_metrics.logical_coherence:.2f}/10")
        report.append(f"- 实践相关性: {quality_metrics.practical_relevance:.2f}/10")
        report.append("")
        
        # 质量问题
        if quality_issues:
            report.append("## 质量问题")
            for issue in quality_issues:
                report.append(f"- **{issue.issue_type}**: {issue.description}")
                report.append(f"  - 严重程度: {issue.severity}")
                report.append(f"  - 改进建议: {issue.suggestion}")
            report.append("")
        
        # 改进建议
        if improvement_suggestions:
            report.append("## 改进建议")
            for i, suggestion in enumerate(improvement_suggestions, 1):
                report.append(f"{i}. {suggestion}")
            report.append("")
        
        # 质量趋势
        if len(self.detection_history) > 1:
            report.append("## 质量趋势")
            recent_scores = [record['overall_quality'] for record in self.detection_history[-5:]]
            trend = "上升" if recent_scores[-1] > recent_scores[0] else "下降" if recent_scores[-1] < recent_scores[0] else "稳定"
            report.append(f"- 最近5次检测趋势: {trend}")
            report.append(f"- 平均质量分数: {sum(recent_scores)/len(recent_scores):.2f}")
            report.append("")
        
        # 总结
        report.append("## 总结")
        if quality_metrics.quality_level == QualityLevel.EXCELLENT:
            report.append("分析质量优秀，达到了专业理论水准。")
        elif quality_metrics.quality_level == QualityLevel.GOOD:
            report.append("分析质量良好，具有较好的理论水平。")
        elif quality_metrics.quality_level == QualityLevel.AVERAGE:
            report.append("分析质量一般，需要在理论深度和方法论方面进一步提升。")
        else:
            report.append("分析质量需要改进，建议系统学习马克思主义基本理论。")
        
        return "\n".join(report)
    
    def save_detection_result(self, detection_result: Dict, output_file: str = None) -> str:
        """保存检测结果"""
        
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"marx_quality_detection_{timestamp}.json"
        
        try:
            # 转换QualityLevel为字符串以便JSON序列化
            result_copy = detection_result.copy()
            result_copy['quality_metrics'] = {
                'theoretical_accuracy': result_copy['quality_metrics'].theoretical_accuracy,
                'methodological_soundness': result_copy['quality_metrics'].methodological_soundness,
                'analytical_depth': result_copy['quality_metrics'].analytical_depth,
                'logical_coherence': result_copy['quality_metrics'].logical_coherence,
                'practical_relevance': result_copy['quality_metrics'].practical_relevance,
                'overall_quality': result_copy['quality_metrics'].overall_quality,
                'quality_level': result_copy['quality_metrics'].quality_level.value
            }
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result_copy, f, ensure_ascii=False, indent=2, default=str)
            
            return output_file
            
        except Exception as e:
            print(f"保存检测结果失败: {str(e)}")
            return ""
    
    def get_quality_statistics(self) -> Dict:
        """获取质量统计信息"""
        
        if not self.detection_history:
            return {
                'total_detections': 0,
                'average_quality': 0,
                'quality_distribution': {},
                'improvement_trend': '无数据'
            }
        
        total_detections = len(self.detection_history)
        average_quality = sum(record['overall_quality'] for record in self.detection_history) / total_detections
        
        # 质量分布
        quality_distribution = {}
        for record in self.detection_history:
            level = record['quality_level']
            quality_distribution[level] = quality_distribution.get(level, 0) + 1
        
        # 改进趋势
        if total_detections >= 2:
            recent_avg = sum(record['overall_quality'] for record in self.detection_history[-5:]) / min(5, total_detections)
            earlier_avg = sum(record['overall_quality'] for record in self.detection_history[:-5]) / max(1, total_detections - 5)
            
            if recent_avg > earlier_avg + 0.5:
                improvement_trend = "明显改善"
            elif recent_avg > earlier_avg:
                improvement_trend = "有所改善"
            elif recent_avg < earlier_avg - 0.5:
                improvement_trend = "明显下降"
            elif recent_avg < earlier_avg:
                improvement_trend = "有所下降"
            else:
                improvement_trend = "保持稳定"
        else:
            improvement_trend = "数据不足"
        
        return {
            'total_detections': total_detections,
            'average_quality': average_quality,
            'quality_distribution': quality_distribution,
            'improvement_trend': improvement_trend
        }


def main():
    """测试基础质量检测系统"""
    detector = BasicQualityDetector()
    
    test_text = """
    在当代中国特色社会主义发展中，生产力与生产关系的矛盾运动推动着社会进步。
    数字技术的快速发展带来了生产力的显著提升，但传统的生产关系在一定程度上
    制约了这种发展。这种对立统一的关系体现了马克思主义辩证法的基本原理。
    
    经济基础的变革要求上层建筑的相应调整。社会主义民主政治不断完善，
    法律体系日益健全，马克思主义指导地位更加巩固。上层建筑对经济基础
    发挥着积极的反作用，推动了经济社会的协调发展。
    
    当前社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的
    发展之间的矛盾。这一矛盾的科学判断体现了历史唯物主义的基本原理，
    为新时代的发展指明了方向。人民群众在历史发展中发挥着主体作用，
    是推动社会进步的根本力量。
    """
    
    print("=== 基础质量检测系统测试 ===")
    
    # 执行质量检测
    detection_result = detector.comprehensive_quality_detection(test_text)
    
    # 显示检测结果
    quality_metrics = detection_result['quality_metrics']
    print(f"\n综合质量分数: {quality_metrics.overall_quality:.2f}/10")
    print(f"质量等级: {quality_metrics.quality_level.value}")
    
    # 显示各项指标
    print(f"\n各项指标:")
    print(f"- 理论准确性: {quality_metrics.theoretical_accuracy:.2f}/10")
    print(f"- 方法论科学性: {quality_metrics.methodological_soundness:.2f}/10")
    print(f"- 分析深度: {quality_metrics.analytical_depth:.2f}/10")
    print(f"- 逻辑连贯性: {quality_metrics.logical_coherence:.2f}/10")
    print(f"- 实践相关性: {quality_metrics.practical_relevance:.2f}/10")
    
    # 显示质量问题
    quality_issues = detection_result['quality_issues']
    if quality_issues:
        print(f"\n质量问题 ({len(quality_issues)}个):")
        for issue in quality_issues:
            print(f"- {issue.issue_type}: {issue.description}")
    
    # 显示改进建议
    improvement_suggestions = detection_result['improvement_suggestions']
    if improvement_suggestions:
        print(f"\n改进建议:")
        for suggestion in improvement_suggestions:
            print(f"- {suggestion}")
    
    # 生成质量报告
    quality_report = detector.generate_quality_report(detection_result)
    
    # 保存检测结果
    output_file = detector.save_detection_result(detection_result)
    if output_file:
        print(f"\n检测结果已保存到: {output_file}")
    
    # 显示质量统计
    statistics = detector.get_quality_statistics()
    print(f"\n质量统计:")
    print(f"- 总检测次数: {statistics['total_detections']}")
    print(f"- 平均质量分数: {statistics['average_quality']:.2f}")
    print(f"- 改进趋势: {statistics['improvement_trend']}")
    
    # 显示报告
    print(f"\n{quality_report}")


if __name__ == "__main__":
    main()