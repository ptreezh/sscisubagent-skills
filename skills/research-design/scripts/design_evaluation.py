#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研究设计技能 - 设计评估模块
评估研究设计的质量、可行性和有效性
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any
import warnings
from dataclasses import dataclass
from enum import Enum


class QualityDimension(Enum):
    """质量维度枚举"""
    SCIENTIFIC_RIGOR = "科学严谨性"
    FEASIBILITY = "可行性"
    ETHICAL_INTEGRITY = "伦理完整性"
    PRACTICAL_IMPACT = "实践影响力"
    THEORETICAL_CONTRIBUTION = "理论贡献"


@dataclass
class DesignEvaluation:
    """设计评估结果"""
    overall_score: float
    dimension_scores: Dict[QualityDimension, float]
    strengths: List[str]
    weaknesses: List[str]
    recommendations: List[str]
    risk_assessment: Dict[str, str]


class DesignEvaluator:
    """设计评估器 - 评估研究设计的各个方面"""
    
    def __init__(self):
        self.evaluation_criteria = self._initialize_criteria()
        self.evaluated_design = None
    
    def _initialize_criteria(self) -> Dict[str, Any]:
        """初始化评估标准"""
        return {
            'scientific_rigor': {
                'construct_validity': {
                    'weight': 0.25,
                    'indicators': [
                        '操作定义清晰',
                        '测量工具有效',
                        '理论框架明确',
                        '变量关系合理'
                    ]
                },
                'statistical_conclusion_validity': {
                    'weight': 0.20,
                    'indicators': [
                        '样本量充足',
                        '统计方法恰当',
                        '检验功效足够',
                        '多重比较校正'
                    ]
                },
                'internal_validity': {
                    'weight': 0.30,
                    'indicators': [
                        '控制混淆变量',
                        '排除竞争解释',
                        '因果关系清晰',
                        '历史影响控制'
                    ]
                },
                'external_validity': {
                    'weight': 0.25,
                    'indicators': [
                        '样本代表性',
                        '情境普遍性',
                        '时间稳定性',
                        '跨群体适用'
                    ]
                }
            },
            'feasibility': {
                'time_feasibility': {
                    'weight': 0.30,
                    'indicators': [
                        '时间安排合理',
                        '阶段划分明确',
                        '里程碑设置',
                        '缓冲时间预留'
                    ]
                },
                'resource_feasibility': {
                    'weight': 0.40,
                    'indicators': [
                        '预算分配合理',
                        '人员配备充足',
                        '设备工具具备',
                        '合作关系建立'
                    ]
                },
                'technical_feasibility': {
                    'weight': 0.30,
                    'indicators': [
                        '技术能力匹配',
                        '工具可用性',
                        '数据获取可能',
                        '分析方法可行'
                    ]
                }
            },
            'ethical_integrity': {
                'informed_consent': {
                    'weight': 0.25,
                    'indicators': [
                        '信息充分',
                        '理解能力',
                        '自愿参与',
                        '退出权保障'
                    ]
                },
                'privacy_protection': {
                    'weight': 0.25,
                    'indicators': [
                        '数据匿名化',
                        '安全存储',
                        '访问控制',
                        '销毁计划'
                    ]
                },
                'risk_benefit_balance': {
                    'weight': 0.30,
                    'indicators': [
                        '风险最小化',
                        '受益最大化',
                        '风险可控',
                        '应急措施'
                    ]
                },
                'fair_subject_selection': {
                    'weight': 0.20,
                    'indicators': [
                        '选择公正',
                        '弱势保护',
                        '负担公平',
                        '利益公平'
                    ]
                }
            },
            'practical_impact': {
                'relevance': {
                    'weight': 0.40,
                    'indicators': [
                        '问题重要',
                        '社会需求',
                        '实践意义',
                        '政策相关'
                    ]
                },
                'implementation_feasibility': {
                    'weight': 0.30,
                    'indicators': [
                        '应用可能',
                        '推广潜力',
                        '成本效益',
                        '可持续性'
                    ]
                },
                'dissemination_potential': {
                    'weight': 0.30,
                    'indicators': [
                        '受众明确',
                        '渠道畅通',
                        '形式适宜',
                        '时机恰当'
                    ]
                }
            }
        }
    
    def evaluate_design(
        self,
        design_elements: Dict[str, Any],
        weights: Optional[Dict[QualityDimension, float]] = None
    ) -> DesignEvaluation:
        """
        评估研究设计
        
        Args:
            design_elements: 设计元素字典
            weights: 各维度权重
            
        Returns:
            DesignEvaluation: 评估结果
        """
        if weights is None:
            weights = {
                QualityDimension.SCIENTIFIC_RIGOR: 0.35,
                QualityDimension.FEASIBILITY: 0.25,
                QualityDimension.ETHICAL_INTEGRITY: 0.20,
                QualityDimension.PRACTICAL_IMPACT: 0.15,
                QualityDimension.THEORETICAL_CONTRIBUTION: 0.05
            }
        
        # 评估各维度
        dimension_scores = {}
        
        # 科学严谨性
        scientific_score = self._evaluate_scientific_rigor(design_elements)
        dimension_scores[QualityDimension.SCIENTIFIC_RIGOR] = scientific_score
        
        # 可行性
        feasibility_score = self._evaluate_feasibility(design_elements)
        dimension_scores[QualityDimension.FEASIBILITY] = feasibility_score
        
        # 伦理完整性
        ethical_score = self._evaluate_ethical_integrity(design_elements)
        dimension_scores[QualityDimension.ETHICAL_INTEGRITY] = ethical_score
        
        # 实践影响力
        practical_score = self._evaluate_practical_impact(design_elements)
        dimension_scores[QualityDimension.PRACTICAL_IMPACT] = practical_score
        
        # 理论贡献（简化评估）
        theoretical_score = self._evaluate_theoretical_contribution(design_elements)
        dimension_scores[QualityDimension.THEORETICAL_CONTRIBUTION] = theoretical_score
        
        # 计算总体评分
        overall_score = sum(
            dimension_scores[dim] * weights[dim] 
            for dim in weights
        )
        
        # 识别优势和劣势
        strengths, weaknesses = self._identify_strengths_weaknesses(
            dimension_scores, design_elements
        )
        
        # 生成建议
        recommendations = self._generate_recommendations(
            weaknesses, dimension_scores
        )
        
        # 风险评估
        risk_assessment = self._assess_risks(design_elements)
        
        evaluation = DesignEvaluation(
            overall_score=overall_score,
            dimension_scores=dimension_scores,
            strengths=strengths,
            weaknesses=weaknesses,
            recommendations=recommendations,
            risk_assessment=risk_assessment
        )
        
        self.evaluated_design = evaluation
        return evaluation
    
    def _evaluate_scientific_rigor(self, design_elements: Dict[str, Any]) -> float:
        """评估科学严谨性"""
        criteria = self.evaluation_criteria['scientific_rigor']
        scores = {}
        
        # 构念效度
        construct_indicators = criteria['construct_validity']['indicators']
        construct_score = self._check_indicators(
            design_elements, construct_indicators, 'construct_validity'
        )
        scores['construct'] = construct_score
        
        # 统计结论效度
        stat_indicators = criteria['statistical_conclusion_validity']['indicators']
        stat_score = self._check_indicators(
            design_elements, stat_indicators, 'statistical_validity'
        )
        scores['statistical'] = stat_score
        
        # 内部效度
        internal_indicators = criteria['internal_validity']['indicators']
        internal_score = self._check_indicators(
            design_elements, internal_indicators, 'internal_validity'
        )
        scores['internal'] = internal_score
        
        # 外部效度
        external_indicators = criteria['external_validity']['indicators']
        external_score = self._check_indicators(
            design_elements, external_indicators, 'external_validity'
        )
        scores['external'] = external_score
        
        # 加权计算
        total_score = (
            scores['construct'] * criteria['construct_validity']['weight'] +
            scores['statistical'] * criteria['statistical_conclusion_validity']['weight'] +
            scores['internal'] * criteria['internal_validity']['weight'] +
            scores['external'] * criteria['external_validity']['weight']
        )
        
        return total_score
    
    def _evaluate_feasibility(self, design_elements: Dict[str, Any]) -> float:
        """评估可行性"""
        criteria = self.evaluation_criteria['feasibility']
        scores = {}
        
        # 时间可行性
        time_indicators = criteria['time_feasibility']['indicators']
        time_score = self._check_indicators(
            design_elements, time_indicators, 'time_feasibility'
        )
        scores['time'] = time_score
        
        # 资源可行性
        resource_indicators = criteria['resource_feasibility']['indicators']
        resource_score = self._check_indicators(
            design_elements, resource_indicators, 'resource_feasibility'
        )
        scores['resource'] = resource_score
        
        # 技术可行性
        tech_indicators = criteria['technical_feasibility']['indicators']
        tech_score = self._check_indicators(
            design_elements, tech_indicators, 'technical_feasibility'
        )
        scores['tech'] = tech_score
        
        # 加权计算
        total_score = (
            scores['time'] * criteria['time_feasibility']['weight'] +
            scores['resource'] * criteria['resource_feasibility']['weight'] +
            scores['tech'] * criteria['technical_feasibility']['weight']
        )
        
        return total_score
    
    def _evaluate_ethical_integrity(self, design_elements: Dict[str, Any]) -> float:
        """评估伦理完整性"""
        criteria = self.evaluation_criteria['ethical_integrity']
        scores = {}
        
        # 知情同意
        consent_indicators = criteria['informed_consent']['indicators']
        consent_score = self._check_indicators(
            design_elements, consent_indicators, 'informed_consent'
        )
        scores['consent'] = consent_score
        
        # 隐私保护
        privacy_indicators = criteria['privacy_protection']['indicators']
        privacy_score = self._check_indicators(
            design_elements, privacy_indicators, 'privacy_protection'
        )
        scores['privacy'] = privacy_score
        
        # 风险收益平衡
        risk_indicators = criteria['risk_benefit_balance']['indicators']
        risk_score = self._check_indicators(
            design_elements, risk_indicators, 'risk_benefit_balance'
        )
        scores['risk'] = risk_score
        
        # 公平受试者选择
        fair_indicators = criteria['fair_subject_selection']['indicators']
        fair_score = self._check_indicators(
            design_elements, fair_indicators, 'fair_subject_selection'
        )
        scores['fair'] = fair_score
        
        # 加权计算
        total_score = (
            scores['consent'] * criteria['informed_consent']['weight'] +
            scores['privacy'] * criteria['privacy_protection']['weight'] +
            scores['risk'] * criteria['risk_benefit_balance']['weight'] +
            scores['fair'] * criteria['fair_subject_selection']['weight']
        )
        
        return total_score
    
    def _evaluate_practical_impact(self, design_elements: Dict[str, Any]) -> float:
        """评估实践影响力"""
        criteria = self.evaluation_criteria['practical_impact']
        scores = {}
        
        # 相关性
        relevance_indicators = criteria['relevance']['indicators']
        relevance_score = self._check_indicators(
            design_elements, relevance_indicators, 'relevance'
        )
        scores['relevance'] = relevance_score
        
        # 实施可行性
        impl_indicators = criteria['implementation_feasibility']['indicators']
        impl_score = self._check_indicators(
            design_elements, impl_indicators, 'implementation_feasibility'
        )
        scores['implementation'] = impl_score
        
        # 传播潜力
        dissemination_indicators = criteria['dissemination_potential']['indicators']
        dissemination_score = self._check_indicators(
            design_elements, dissemination_indicators, 'dissemination_potential'
        )
        scores['dissemination'] = dissemination_score
        
        # 加权计算
        total_score = (
            scores['relevance'] * criteria['relevance']['weight'] +
            scores['implementation'] * criteria['implementation_feasibility']['weight'] +
            scores['dissemination'] * criteria['dissemination_potential']['weight']
        )
        
        return total_score
    
    def _evaluate_theoretical_contribution(self, design_elements: Dict[str, Any]) -> float:
        """评估理论贡献（简化）"""
        # 检查是否包含理论框架、假设、变量关系等元素
        contribution_score = 0.0
        
        if design_elements.get('theoretical_framework'):
            contribution_score += 0.3
        if design_elements.get('research_hypotheses'):
            contribution_score += 0.3
        if design_elements.get('variable_relationships'):
            contribution_score += 0.2
        if design_elements.get('novelty_indicators'):
            contribution_score += 0.2
        
        return min(contribution_score, 1.0)  # 限制在0-1范围内
    
    def _check_indicators(self, design_elements: Dict[str, Any], indicators: List[str], section_key: str) -> float:
        """检查指标满足情况"""
        if section_key in design_elements:
            section_content = design_elements[section_key]
            if isinstance(section_content, str):
                # 搜索关键词
                content_lower = section_content.lower()
                satisfied = sum(1 for indicator in indicators if indicator.split()[0].lower() in content_lower)
                return satisfied / len(indicators) if len(indicators) > 0 else 0.0
            elif isinstance(section_content, (list, tuple)):
                # 检查列表中是否包含指标关键词
                content_str = ' '.join(str(item) for item in section_content).lower()
                satisfied = sum(1 for indicator in indicators if indicator.split()[0].lower() in content_str)
                return satisfied / len(indicators) if len(indicators) > 0 else 0.0
        
        return 0.0
    
    def _identify_strengths_weaknesses(
        self, 
        dimension_scores: Dict[QualityDimension, float], 
        design_elements: Dict[str, Any]
    ) -> Tuple[List[str], List[str]]:
        """识别优势和劣势"""
        strengths = []
        weaknesses = []
        
        # 按维度分析
        for dimension, score in dimension_scores.items():
            if score >= 0.8:
                strengths.append(f"{dimension.value}: 得分较高 ({score:.2f})")
            elif score <= 0.5:
                weaknesses.append(f"{dimension.value}: 得分较低 ({score:.2f})")
        
        # 检查具体设计元素
        if 'sample_size_calculation' in design_elements:
            strengths.append("样本量计算充分")
        else:
            weaknesses.append("缺少样本量计算")
        
        if 'power_analysis' in design_elements:
            strengths.append("统计功效分析完整")
        else:
            weaknesses.append("缺少统计功效分析")
        
        if 'data_management_plan' in design_elements:
            strengths.append("数据管理计划完整")
        else:
            weaknesses.append("缺少数据管理计划")
        
        if 'risk_control_measures' in design_elements:
            strengths.append("风险控制措施明确")
        else:
            weaknesses.append("缺少风险控制措施")
        
        return strengths, weaknesses
    
    def _generate_recommendations(
        self, 
        weaknesses: List[str], 
        dimension_scores: Dict[QualityDimension, float]
    ) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于劣势生成建议
        for weakness in weaknesses:
            if "科学严谨性" in weakness:
                recommendations.append("加强理论框架构建，明确变量定义和关系假设")
            elif "可行性" in weakness:
                recommendations.append("重新评估时间和资源需求，制定更现实的计划")
            elif "伦理完整性" in weakness:
                recommendations.append("完善伦理审查程序，加强隐私保护措施")
            elif "实践影响力" in weakness:
                recommendations.append("增强研究问题的相关性，考虑实践应用价值")
            elif "样本量" in weakness:
                recommendations.append("进行样本量计算，确保统计功效")
            elif "数据管理" in weakness:
                recommendations.append("制定详细的数据管理计划，包括存储、备份和安全措施")
        
        # 基于低分维度生成建议
        for dimension, score in dimension_scores.items():
            if score < 0.6:
                if dimension == QualityDimension.SCIENTIFIC_RIGOR:
                    recommendations.append("强化研究设计的科学性，重视效度控制")
                elif dimension == QualityDimension.FEASIBILITY:
                    recommendations.append("重新评估可行性，调整不现实的期望")
                elif dimension == QualityDimension.ETHICAL_INTEGRITY:
                    recommendations.append("加强伦理考量，确保符合伦理标准")
                elif dimension == QualityDimension.PRACTICAL_IMPACT:
                    recommendations.append("提升研究的实用价值，考虑成果转化途径")
        
        return recommendations
    
    def _assess_risks(self, design_elements: Dict[str, Any]) -> Dict[str, str]:
        """评估风险"""
        risks = {}
        
        # 数据相关风险
        if not design_elements.get('data_backup_strategy'):
            risks['data_loss'] = "高：缺少数据备份策略"
        else:
            risks['data_loss'] = "低：有数据备份策略"
        
        # 伦理风险
        if not design_elements.get('informed_consent_process'):
            risks['consent_violation'] = "高：缺少知情同意程序"
        else:
            risks['consent_violation'] = "中：有知情同意程序但需细化"
        
        # 偏倚风险
        if not design_elements.get('bias_control_measures'):
            risks['selection_bias'] = "中：缺少偏倚控制措施"
        else:
            risks['selection_bias'] = "低：有偏倚控制措施"
        
        # 资源风险
        if not design_elements.get('budget_contingency'):
            risks['budget_overrun'] = "高：缺少预算应急计划"
        else:
            risks['budget_overrun'] = "中：有预算应急但比例可能不足"
        
        return risks
    
    def generate_evaluation_report(self) -> str:
        """生成评估报告"""
        if self.evaluated_design is None:
            return "未进行设计评估"
        
        report = []
        report.append("# 研究设计评估报告\n")
        
        # 总体评分
        report.append(f"## 总体评分: {self.evaluated_design.overall_score:.2f}/1.0\n")
        
        # 各维度评分
        report.append("## 各维度评分:\n")
        for dimension, score in self.evaluated_design.dimension_scores.items():
            report.append(f"- {dimension.value}: {score:.2f}/1.0\n")
        report.append("\n")
        
        # 优势
        report.append("## 主要优势:\n")
        if self.evaluated_design.strengths:
            for strength in self.evaluated_design.strengths:
                report.append(f"- {strength}\n")
        else:
            report.append("- 无明显优势\n")
        report.append("\n")
        
        # 劣势
        report.append("## 主要劣势:\n")
        if self.evaluated_design.weaknesses:
            for weakness in self.evaluated_design.weaknesses:
                report.append(f"- {weakness}\n")
        else:
            report.append("- 无明显劣势\n")
        report.append("\n")
        
        # 建议
        report.append("## 改进建议:\n")
        if self.evaluated_design.recommendations:
            for i, recommendation in enumerate(self.evaluated_design.recommendations, 1):
                report.append(f"{i}. {recommendation}\n")
        else:
            report.append("- 无需改进建议\n")
        report.append("\n")
        
        # 风险评估
        report.append("## 风险评估:\n")
        for risk_type, level_desc in self.evaluated_design.risk_assessment.items():
            report.append(f"- {risk_type}: {level_desc}\n")
        report.append("\n")
        
        # 总结
        report.append("## 评估总结:\n")
        overall_score = self.evaluated_design.overall_score
        if overall_score >= 0.8:
            summary = "研究设计质量优秀，各方面考虑周全，可直接实施"
        elif overall_score >= 0.6:
            summary = "研究设计质量良好，但需要根据建议进行改进"
        elif overall_score >= 0.4:
            summary = "研究设计质量一般，需要较多改进后方可实施"
        else:
            summary = "研究设计质量较差，需要重大修改后重新评估"
        
        report.append(summary)
        
        return "".join(report)


def main():
    """示例用法"""
    print("⚖️ 研究设计 - 设计评估模块演示")
    
    # 创建示例设计元素
    sample_design = {
        'theoretical_framework': '基于社会认知理论，探讨自我效能感对学习行为的影响',
        'research_hypotheses': ['自我效能感正向影响学习行为', '动机在其中起中介作用'],
        'variable_relationships': '自我效能感 -> 动机 -> 学习行为',
        'novelty_indicators': '首次在中国大学生群体中验证该理论模型',
        'sampling_strategy': '分层随机抽样，按年级和专业分层',
        'data_collection_methods': '问卷调查、深度访谈、学习平台数据',
        'sample_size_calculation': '基于功效分析，α=0.05, β=0.2, 效应量=0.3, 需要288个样本',
        'power_analysis': '事后功效分析确认达到0.8的统计功效',
        'statistical_methods': '结构方程模型、中介效应检验、多群组分析',
        'time_schedule': '第1-2月文献回顾，第3-4月数据收集，第5-6月分析，第7月报告',
        'resource_allocation': '预算10万元，3名研究人员，6个月时间',
        'informed_consent_process': '书面知情同意，明示权利和退出机制',
        'data_management_plan': '加密存储，权限控制，定期备份',
        'risk_control_measures': '数据泄露应急预案，参与者心理支持',
        'bias_control_measures': '随机分配，盲法评估，统计控制'
    }
    
    # 初始化评估器
    evaluator = DesignEvaluator()
    
    # 执行评估
    evaluation = evaluator.evaluate_design(sample_design)
    
    # 显示评估结果
    print(f"总体评分: {evaluation.overall_score:.2f}")
    print("\n各维度评分:")
    for dimension, score in evaluation.dimension_scores.items():
        print(f"  {dimension.value}: {score:.2f}")
    
    print(f"\n优势数量: {len(evaluation.strengths)}")
    print(f"劣势数量: {len(evaluation.weaknesses)}")
    print(f"建议数量: {len(evaluation.recommendations)}")
    
    # 生成完整报告
    print("\n--- 完整评估报告 ---")
    report = evaluator.generate_evaluation_report()
    print(report)
    
    print("✅ 设计评估完成！")


if __name__ == "__main__":
    main()