#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研究设计技能 - 方法匹配模块
基于研究问题和目标匹配最合适的研究方法和设计
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any
import warnings
from enum import Enum


class ResearchPurpose(Enum):
    """研究目的枚举"""
    EXPLORATORY = "探索性"
    DESCRIPTIVE = "描述性"
    EXPLANATORY = "解释性"
    EVALUATIVE = "评价性"


class ResearchMethod(Enum):
    """研究方法枚举"""
    QUALITATIVE = "定性研究"
    QUANTITATIVE = "定量研究"
    MIXED_METHODS = "混合方法"


class ResearchDesign(Enum):
    """研究设计枚举"""
    EXPERIMENTAL = "实验设计"
    QUASI_EXPERIMENTAL = "准实验设计"
    SURVEY = "调查研究"
    CASE_STUDY = "案例研究"
    PHENOMENOLOGY = "现象学研究"
    GROUNDED_THEORY = "扎根理论"
    ETHNOGRAPHY = "民族志"
    NARRATIVE = "叙事研究"
    CONVERGENT_PARALLEL = "收敛式并行设计"
    EXPLANATORY_SEQUENTIAL = "解释性顺序设计"
    EXPLORATORY_SEQUENTIAL = "探索性顺序设计"
    EMBEDDED = "嵌入式设计"


class MethodMatcher:
    """方法匹配器 - 基于研究特征匹配最合适的方法"""
    
    def __init__(self):
        self.matching_rules = self._initialize_matching_rules()
        self.method_evaluation = {}
    
    def _initialize_matching_rules(self) -> Dict[str, Any]:
        """初始化匹配规则"""
        return {
            'purpose_design_mapping': {
                ResearchPurpose.EXPLORATORY: [
                    ResearchDesign.CASE_STUDY,
                    ResearchDesign.PHENOMENOLOGY,
                    ResearchDesign.GROUNDED_THEORY,
                    ResearchDesign.ETHNOGRAPHY
                ],
                ResearchPurpose.DESCRIPTIVE: [
                    ResearchDesign.SURVEY,
                    ResearchDesign.CASE_STUDY,
                    ResearchDesign.NARRATIVE
                ],
                ResearchPurpose.EXPLANATORY: [
                    ResearchDesign.EXPERIMENTAL,
                    ResearchDesign.QUASI_EXPERIMENTAL,
                    ResearchDesign.SURVEY
                ],
                ResearchPurpose.EVALUATIVE: [
                    ResearchDesign.EXPERIMENTAL,
                    ResearchDesign.QUASI_EXPERIMENTAL,
                    ResearchDesign.SURVEY
                ]
            },
            'method_purpose_mapping': {
                ResearchMethod.QUALITATIVE: [
                    ResearchPurpose.EXPLORATORY,
                    ResearchPurpose.DESCRIPTIVE
                ],
                ResearchMethod.QUANTITATIVE: [
                    ResearchPurpose.DESCRIPTIVE,
                    ResearchPurpose.EXPLANATORY,
                    ResearchPurpose.EVALUATIVE
                ],
                ResearchMethod.MIXED_METHODS: [
                    ResearchPurpose.EXPLORATORY,
                    ResearchPurpose.DESCRIPTIVE,
                    ResearchPurpose.EXPLANATORY,
                    ResearchPurpose.EVALUATIVE
                ]
            },
            'design_characteristics': {
                ResearchDesign.EXPERIMENTAL: {
                    'control_level': 'high',
                    'randomization': True,
                    'causal_inference': True,
                    'time_span': 'medium',
                    'cost': 'high',
                    'ethical_complexity': 'medium'
                },
                ResearchDesign.QUASI_EXPERIMENTAL: {
                    'control_level': 'medium',
                    'randomization': False,
                    'causal_inference': 'possible',
                    'time_span': 'medium',
                    'cost': 'medium',
                    'ethical_complexity': 'medium'
                },
                ResearchDesign.SURVEY: {
                    'control_level': 'low',
                    'randomization': 'sampling',
                    'causal_inference': False,
                    'time_span': 'short',
                    'cost': 'low',
                    'ethical_complexity': 'low'
                },
                ResearchDesign.CASE_STUDY: {
                    'control_level': 'low',
                    'randomization': False,
                    'causal_inference': 'descriptive',
                    'time_span': 'long',
                    'cost': 'medium',
                    'ethical_complexity': 'low'
                },
                ResearchDesign.PHENOMENOLOGY: {
                    'control_level': 'none',
                    'randomization': False,
                    'causal_inference': 'understanding',
                    'time_span': 'long',
                    'cost': 'low',
                    'ethical_complexity': 'low'
                },
                ResearchDesign.GROUNDED_THEORY: {
                    'control_level': 'none',
                    'randomization': False,
                    'causal_inference': 'theoretical',
                    'time_span': 'long',
                    'cost': 'medium',
                    'ethical_complexity': 'low'
                },
                ResearchDesign.ETHNOGRAPHY: {
                    'control_level': 'none',
                    'randomization': False,
                    'causal_inference': 'cultural',
                    'time_span': 'very_long',
                    'cost': 'high',
                    'ethical_complexity': 'high'
                },
                ResearchDesign.NARRATIVE: {
                    'control_level': 'none',
                    'randomization': False,
                    'causal_inference': 'experiential',
                    'time_span': 'medium',
                    'cost': 'low',
                    'ethical_complexity': 'medium'
                },
                ResearchDesign.CONVERGENT_PARALLEL: {
                    'control_level': 'mixed',
                    'randomization': 'depends',
                    'causal_inference': 'mixed',
                    'time_span': 'long',
                    'cost': 'high',
                    'ethical_complexity': 'medium'
                },
                ResearchDesign.EXPLANATORY_SEQUENTIAL: {
                    'control_level': 'mixed',
                    'randomization': 'depends',
                    'causal_inference': 'mixed',
                    'time_span': 'very_long',
                    'cost': 'high',
                    'ethical_complexity': 'medium'
                },
                ResearchDesign.EXPLORATORY_SEQUENTIAL: {
                    'control_level': 'mixed',
                    'randomization': 'depends',
                    'causal_inference': 'mixed',
                    'time_span': 'very_long',
                    'cost': 'high',
                    'ethical_complexity': 'medium'
                },
                ResearchDesign.EMBEDDED: {
                    'control_level': 'mixed',
                    'randomization': 'depends',
                    'causal_inference': 'mixed',
                    'time_span': 'long',
                    'cost': 'medium',
                    'ethical_complexity': 'medium'
                }
            }
        }
    
    def match_methods(
        self,
        research_purpose: ResearchPurpose,
        sample_size: Optional[int] = None,
        time_constraint: str = 'flexible',  # 'short', 'medium', 'long', 'flexible'
        resource_level: str = 'adequate',   # 'limited', 'adequate', 'abundant'
        ethical_considerations: bool = False
    ) -> List[Dict[str, Any]]:
        """
        匹配最适合的研究方法和设计
        
        Args:
            research_purpose: 研究目的
            sample_size: 样本量
            time_constraint: 时间约束
            resource_level: 资源水平
            ethical_considerations: 伦理考虑
            
        Returns:
            List: 匹配的方法和设计列表
        """
        matched_methods = []
        
        # 基于研究目的匹配设计
        possible_designs = self.matching_rules['purpose_design_mapping'].get(research_purpose, [])
        
        for design in possible_designs:
            characteristics = self.matching_rules['design_characteristics'][design]
            
            # 评估设计与约束条件的匹配度
            score = self._evaluate_design_fit(
                design, characteristics, sample_size, 
                time_constraint, resource_level, ethical_considerations
            )
            
            matched_methods.append({
                'design': design,
                'characteristics': characteristics,
                'fit_score': score,
                'suitability_reasons': self._generate_suitability_reasons(
                    design, research_purpose, characteristics
                ),
                'limitations': self._identify_limitations(design, characteristics)
            })
        
        # 按匹配度排序
        matched_methods.sort(key=lambda x: x['fit_score'], reverse=True)
        
        self.method_evaluation = {
            'input_parameters': {
                'research_purpose': research_purpose.value,
                'sample_size': sample_size,
                'time_constraint': time_constraint,
                'resource_level': resource_level,
                'ethical_considerations': ethical_considerations
            },
            'matched_methods': matched_methods
        }
        
        return matched_methods
    
    def _evaluate_design_fit(
        self,
        design: ResearchDesign,
        characteristics: Dict[str, Any],
        sample_size: Optional[int],
        time_constraint: str,
        resource_level: str,
        ethical_considerations: bool
    ) -> float:
        """评估设计与约束条件的匹配度"""
        score = 0.0
        max_score = 10.0
        
        # 时间匹配度
        if time_constraint == 'short':
            if characteristics['time_span'] in ['short', 'none']:
                score += 2.5
            elif characteristics['time_span'] == 'medium':
                score += 1.5
            else:
                score += 0.5  # 长时间设计得分较低
        elif time_constraint == 'long':
            if characteristics['time_span'] in ['long', 'very_long']:
                score += 2.5
            else:
                score += 1.0
        
        # 资源匹配度
        if resource_level == 'limited':
            if characteristics['cost'] == 'low':
                score += 2.5
            elif characteristics['cost'] == 'medium':
                score += 1.5
            else:
                score += 0.5
        elif resource_level == 'abundant':
            if characteristics['cost'] == 'high':
                score += 2.5  # 高资源可以支持高成本设计
            else:
                score += 2.0
        else:  # adequate
            if characteristics['cost'] == 'medium':
                score += 2.5
            else:
                score += 1.5
        
        # 伦理复杂度
        if ethical_considerations and characteristics['ethical_complexity'] == 'high':
            score -= 1.0  # 伦理敏感研究避免高伦理复杂度设计
        elif not ethical_considerations and characteristics['ethical_complexity'] == 'high':
            score += 0.5  # 非敏感研究可以承受一定伦理复杂度
        
        # 随机化需求
        if sample_size and sample_size < 30 and characteristics['randomization'] is True:
            score -= 1.0  # 小样本难以有效随机化
        
        return min(score, max_score)
    
    def _generate_suitability_reasons(
        self,
        design: ResearchDesign,
        research_purpose: ResearchPurpose,
        characteristics: Dict[str, Any]
    ) -> List[str]:
        """生成适合性原因"""
        reasons = []
        
        # 基于研究目的
        if research_purpose == ResearchPurpose.EXPLORATORY:
            if design in [ResearchDesign.CASE_STUDY, ResearchDesign.PHENOMENOLOGY, ResearchDesign.GROUNDED_THEORY]:
                reasons.append("适合深入探索未知现象")
        elif research_purpose == ResearchPurpose.DESCRIPTIVE:
            if design == ResearchDesign.SURVEY:
                reasons.append("适合大规模描述现象分布")
        elif research_purpose == ResearchPurpose.EXPLANATORY:
            if characteristics['causal_inference'] in [True, 'possible']:
                reasons.append("适合探索变量间因果关系")
        
        # 基于设计特征
        if characteristics['control_level'] == 'high':
            reasons.append("提供较强的内部效度")
        elif characteristics['control_level'] == 'none':
            reasons.append("适合自然情境下的深入理解")
        
        if characteristics['causal_inference'] == True:
            reasons.append("支持因果推断")
        elif characteristics['causal_inference'] == 'understanding':
            reasons.append("适合理解深层机制")
        
        return reasons
    
    def _identify_limitations(
        self,
        design: ResearchDesign,
        characteristics: Dict[str, Any]
    ) -> List[str]:
        """识别局限性"""
        limitations = []
        
        if characteristics['control_level'] == 'low':
            limitations.append("外部效度可能受限")
        elif characteristics['control_level'] == 'high':
            limitations.append("生态效度可能受限")
        
        if characteristics['time_span'] == 'very_long':
            limitations.append("时间成本高，可能存在流失")
        
        if characteristics['cost'] == 'high':
            limitations.append("资源需求大")
        
        if characteristics['ethical_complexity'] == 'high':
            limitations.append("伦理审查复杂")
        
        if not characteristics['randomization']:
            limitations.append("可能存在选择偏倚")
        
        return limitations
    
    def generate_method_recommendation_report(self) -> str:
        """生成方法推荐报告"""
        if not self.method_evaluation:
            return "未进行方法匹配分析"
        
        report = []
        report.append("# 研究方法推荐报告\n")
        
        # 输入参数
        input_params = self.method_evaluation['input_parameters']
        report.append("## 研究参数\n")
        report.append(f"- 研究目的: {input_params['research_purpose']}\n")
        report.append(f"- 样本量: {input_params['sample_size'] or '未指定'}\n")
        report.append(f"- 时间约束: {input_params['time_constraint']}\n")
        report.append(f"- 资源水平: {input_params['resource_level']}\n")
        report.append(f"- 伦理考虑: {'是' if input_params['ethical_considerations'] else '否'}\n\n")
        
        # 推荐结果
        report.append("## 方法推荐结果\n")
        for i, method in enumerate(self.method_evaluation['matched_methods'], 1):
            design = method['design']
            fit_score = method['fit_score']
            
            report.append(f"### 推荐 {i}: {design.value}\n")
            report.append(f"**匹配度评分**: {fit_score:.1f}/10.0\n\n")
            
            # 适合性原因
            if method['suitability_reasons']:
                report.append("**适合性原因**:\n")
                for reason in method['suitability_reasons']:
                    report.append(f"- {reason}\n")
                report.append("\n")
            
            # 局限性
            if method['limitations']:
                report.append("**主要局限性**:\n")
                for limitation in method['limitations']:
                    report.append(f"- {limitation}\n")
                report.append("\n")
            
            # 设计特征
            characteristics = method['characteristics']
            report.append("**设计特征**:\n")
            report.append(f"- 控制水平: {characteristics['control_level']}\n")
            report.append(f"- 随机化: {characteristics['randomization']}\n")
            report.append(f"- 因果推断: {characteristics['causal_inference']}\n")
            report.append(f"- 时间跨度: {characteristics['time_span']}\n")
            report.append(f"- 成本水平: {characteristics['cost']}\n")
            report.append(f"- 伦理复杂度: {characteristics['ethical_complexity']}\n\n")
        
        return "".join(report)


def main():
    """示例用法"""
    print("🔍 研究设计 - 方法匹配模块演示")
    
    # 初始化匹配器
    matcher = MethodMatcher()
    
    # 示例1: 探索性研究
    print("\n--- 示例1: 探索性研究 ---")
    exploratory_matches = matcher.match_methods(
        research_purpose=ResearchPurpose.EXPLORATORY,
        sample_size=15,
        time_constraint='long',
        resource_level='adequate',
        ethical_considerations=False
    )
    
    for match in exploratory_matches[:3]:  # 显示前3个匹配
        print(f"设计: {match['design'].value}")
        print(f"匹配度: {match['fit_score']:.1f}/10.0")
        print(f"适合性原因: {', '.join(match['suitability_reasons'][:2])}")
        print(f"局限性: {', '.join(match['limitations'][:2])}")
        print("-" * 50)
    
    # 示例2: 评价性研究
    print("\n--- 示例2: 评价性研究 ---")
    evaluative_matches = matcher.match_methods(
        research_purpose=ResearchPurpose.EVALUATIVE,
        sample_size=200,
        time_constraint='medium',
        resource_level='abundant',
        ethical_considerations=True
    )
    
    for match in evaluative_matches[:3]:  # 显示前3个匹配
        print(f"设计: {match['design'].value}")
        print(f"匹配度: {match['fit_score']:.1f}/10.0")
        print(f"适合性原因: {', '.join(match['suitability_reasons'][:2])}")
        print(f"局限性: {', '.join(match['limitations'][:2])}")
        print("-" * 50)
    
    # 生成完整报告
    print("\n--- 完整推荐报告 ---")
    report = matcher.generate_method_recommendation_report()
    print(report)
    
    print("✅ 方法匹配完成！")


if __name__ == "__main__":
    main()