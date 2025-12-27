#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研究设计技能 - 集成分析模块
综合文献分析、方法匹配和设计评估，提供完整的研究设计指导
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any
import json
import os
from pathlib import Path
import warnings

# 导入各模块
from literature_analysis import LiteratureAnalyzer
from method_matching import MethodMatcher, ResearchPurpose as ResearchPurposeEnum
from design_evaluation import DesignEvaluator, QualityDimension


class IntegratedResearchDesigner:
    """集成研究设计器 - 综合分析研究设计的各个方面"""
    
    def __init__(self, skill_root: str = "."):
        self.skill_root = Path(skill_root)
        self.literature_analyzer = LiteratureAnalyzer()
        self.method_matcher = MethodMatcher()
        self.design_evaluator = DesignEvaluator()
        
        # 分析状态跟踪
        self.analysis_state = {
            'phase': 'initiated',
            'literature_analysis': None,
            'method_matching': None,
            'design_evaluation': None,
            'final_recommendation': None
        }
    
    def load_literature_data(self, data: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """加载文献数据"""
        return self.literature_analyzer.load_literature_data(data)
    
    def execute_literature_analysis(self) -> Dict[str, Any]:
        """执行文献分析"""
        print("📚 开始文献分析...")
        
        # 执行趋势分析
        trend_analysis = self.literature_analyzer.analyze_publication_trends()
        
        # 执行主题分析
        theme_analysis = self.literature_analyzer.analyze_research_themes(top_n=10)
        
        # 识别知识缺口
        knowledge_gaps = self.literature_analyzer.identify_knowledge_gaps()
        
        # 生成报告
        report = self.literature_analyzer.generate_literature_report()
        
        # 从分析结果中提取研究方向
        research_directions = self._extract_research_directions(
            theme_analysis, knowledge_gaps
        )
        
        literature_results = {
            'trend_analysis': trend_analysis,
            'theme_analysis': theme_analysis,
            'knowledge_gaps': knowledge_gaps,
            'report': report,
            'suggested_directions': research_directions
        }
        
        self.analysis_state['phase'] = 'literature_analysis'
        self.analysis_state['literature_analysis'] = literature_results
        
        print("  ✓ 文献分析完成")
        return literature_results
    
    def execute_method_matching(self, research_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """执行方法匹配"""
        print("🔍 开始方法匹配...")
        
        # 从研究上下文确定研究目的
        research_purpose = self._determine_research_purpose(research_context)
        
        # 从研究上下文提取约束条件
        sample_size = research_context.get('target_sample_size')
        time_constraint = research_context.get('time_constraint', 'flexible')
        resource_level = research_context.get('resource_level', 'adequate')
        ethical_considerations = research_context.get('ethical_sensitivity', False)
        
        # 执行匹配
        matched_methods = self.method_matcher.match_methods(
            research_purpose=research_purpose,
            sample_size=sample_size,
            time_constraint=time_constraint,
            resource_level=resource_level,
            ethical_considerations=ethical_considerations
        )
        
        method_results = {
            'matched_methods': matched_methods,
            'recommendation_report': self.method_matcher.generate_method_recommendation_report()
        }
        
        self.analysis_state['phase'] = 'method_matching'
        self.analysis_state['method_matching'] = method_results
        
        print("  ✓ 方法匹配完成")
        return matched_methods
    
    def execute_design_evaluation(self, design_elements: Dict[str, Any]) -> Any:
        """执行设计评估"""
        print("⚖️ 开始设计评估...")
        
        # 执行评估
        evaluation = self.design_evaluator.evaluate_design(design_elements)
        
        evaluation_results = {
            'evaluation': evaluation,
            'report': self.design_evaluator.generate_evaluation_report()
        }
        
        self.analysis_state['phase'] = 'design_evaluation'
        self.analysis_state['design_evaluation'] = evaluation_results
        
        print("  ✓ 设计评估完成")
        return evaluation
    
    def generate_final_recommendation(self, research_context: Dict[str, Any]) -> Dict[str, Any]:
        """生成最终推荐"""
        print("📋 生成最终推荐...")
        
        # 综合所有分析结果
        literature_analysis = self.analysis_state['literature_analysis']
        method_matching = self.analysis_state['method_matching']
        design_evaluation = self.analysis_state['design_evaluation']
        
        # 生成综合建议
        recommendation = self._synthesize_recommendation(
            literature_analysis, method_matching, design_evaluation, research_context
        )
        
        self.analysis_state['phase'] = 'final_recommendation'
        self.analysis_state['final_recommendation'] = recommendation
        
        print("  ✓ 最终推荐生成完成")
        return recommendation
    
    def _extract_research_directions(
        self, 
        theme_analysis: Dict[str, Any], 
        knowledge_gaps: List[Dict[str, Any]]
    ) -> List[str]:
        """从文献分析中提取研究方向"""
        directions = []
        
        # 从高频主题提取方向
        top_keywords = theme_analysis.get('top_keywords', {})
        if top_keywords:
            directions.extend(list(top_keywords.keys())[:3])
        
        # 从知识缺口提取方向
        for gap in knowledge_gaps:
            if gap.get('gap_type') == 'thematic':
                directions.append(f"填补{gap.get('description', '知识缺口')}")
            elif gap.get('gap_type') == 'temporal':
                directions.append(f"关注{gap.get('description', '时间段')}的研究")
        
        return directions
    
    def _determine_research_purpose(self, research_context: Dict[str, Any]) -> ResearchPurposeEnum:
        """确定研究目的"""
        purpose_str = research_context.get('research_purpose', '').lower()

        if 'explore' in purpose_str or '探索' in purpose_str:
            return ResearchPurposeEnum.EXPLORATORY
        elif 'describe' in purpose_str or '描述' in purpose_str:
            return ResearchPurposeEnum.DESCRIPTIVE
        elif 'explain' in purpose_str or '解释' in purpose_str:
            return ResearchPurposeEnum.EXPLANATORY
        elif 'evaluate' in purpose_str or '评价' in purpose_str:
            return ResearchPurposeEnum.EVALUATIVE
        else:
            # 根据其他上下文信息推断
            if research_context.get('hypothesis_testing', False):
                return ResearchPurposeEnum.EXPLANATORY
            elif research_context.get('phenomenon_understanding', False):
                return ResearchPurposeEnum.EXPLORATORY
            else:
                return ResearchPurposeEnum.DESCRIPTIVE
    
    def _synthesize_recommendation(
        self,
        literature_analysis: Dict[str, Any],
        method_matching: List[Dict[str, Any]],
        design_evaluation: Any,
        research_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """综合推荐"""
        recommendation = {
            'executive_summary': self._generate_executive_summary(
                literature_analysis, method_matching, design_evaluation
            ),
            'research_question_refinement': self._refine_research_questions(
                research_context, literature_analysis
            ),
            'methodology_recommendation': self._select_optimal_method(
                method_matching['matched_methods']
            ),
            'design_improvements': self._suggest_design_improvements(
                design_evaluation
            ),
            'implementation_plan': self._generate_implementation_plan(
                method_matching, design_evaluation
            ),
            'risk_mitigation': self._identify_mitigation_strategies(
                design_evaluation
            )
        }
        
        return recommendation
    
    def _generate_executive_summary(
        self,
        literature_analysis: Dict[str, Any],
        method_matching: List[Dict[str, Any]],
        design_evaluation: Any
    ) -> str:
        """生成执行摘要"""
        summary_parts = []
        
        # 文献分析摘要
        gaps = literature_analysis.get('knowledge_gaps', [])
        if gaps:
            summary_parts.append(f"识别到{len(gaps)}个知识缺口，建议重点关注。")
        
        # 方法匹配摘要
        top_methods = method_matching['matched_methods'][:2]
        if top_methods:
            top_design = top_methods[0]['design'].value
            summary_parts.append(f"推荐使用{top_design}设计，匹配度评分为{top_methods[0]['fit_score']:.1f}。")
        
        # 设计评估摘要
        if isinstance(design_evaluation, dict):
            overall_score = design_evaluation['evaluation'].overall_score
        else:
            overall_score = design_evaluation.evaluation.overall_score
        if overall_score >= 0.8:
            summary_parts.append(f"设计质量优秀(评分:{overall_score:.2f})，可直接实施。")
        elif overall_score >= 0.6:
            summary_parts.append(f"设计质量良好(评分:{overall_score:.2f})，建议根据反馈改进。")
        else:
            summary_parts.append(f"设计质量一般(评分:{overall_score:.2f})，需要重大改进。")
        
        return " ".join(summary_parts)
    
    def _refine_research_questions(
        self,
        research_context: Dict[str, Any],
        literature_analysis: Dict[str, Any]
    ) -> List[str]:
        """优化研究问题"""
        original_questions = research_context.get('research_questions', [])
        knowledge_gaps = literature_analysis.get('knowledge_gaps', [])
        
        refined_questions = []
        
        # 基于知识缺口优化问题
        for gap in knowledge_gaps:
            if gap.get('gap_type') == 'thematic':
                refined_questions.append(f"如何解决{gap.get('description', '特定领域')}的知识缺口?")
        
        # 添加原始问题
        refined_questions.extend(original_questions)
        
        return refined_questions[:5]  # 最多5个
    
    def _select_optimal_method(self, matched_methods: List[Dict[str, Any]]) -> Dict[str, Any]:
        """选择最优方法"""
        if not matched_methods:
            return {'design': '未找到合适方法', 'reasoning': '请提供更多研究信息'}
        
        # 选择匹配度最高的方法
        best_method = max(matched_methods, key=lambda x: x['fit_score'])
        
        return {
            'design': best_method['design'].value,
            'fit_score': best_method['fit_score'],
            'suitability_reasons': best_method['suitability_reasons'],
            'considerations': best_method['limitations']
        }
    
    def _suggest_design_improvements(self, design_evaluation: Any) -> List[str]:
        """建议设计改进"""
        if isinstance(design_evaluation, dict):
            weaknesses = design_evaluation['evaluation'].weaknesses
            recommendations = design_evaluation['evaluation'].recommendations
        else:
            weaknesses = design_evaluation.evaluation.weaknesses
            recommendations = design_evaluation.evaluation.recommendations

        # 结合弱点和建议生成改进措施
        improvements = []
        improvements.extend(recommendations)

        return improvements[:10]  # 最多10个改进措施
    
    def _generate_implementation_plan(
        self,
        method_matching: List[Dict[str, Any]],
        design_evaluation: Any
    ) -> Dict[str, Any]:
        """生成实施计划"""
        optimal_method = self._select_optimal_method(method_matching['matched_methods'])
        
        return {
            'recommended_design': optimal_method['design'],
            'key_activities': [
                '文献回顾和理论构建',
                '研究工具开发和验证',
                '样本招募和数据收集',
                '数据分析和结果解释',
                '报告撰写和成果发布'
            ],
            'critical_success_factors': [
                '充足的样本量',
                '高质量的数据收集',
                '适当的分析方法',
                '有效的伦理审查'
            ],
            'timeline_estimate': '6-12个月（根据研究复杂度调整）'
        }
    
    def _identify_mitigation_strategies(self, design_evaluation: Any) -> List[str]:
        """识别缓解策略"""
        if isinstance(design_evaluation, dict):
            risks = design_evaluation['evaluation'].risk_assessment
            weaknesses = design_evaluation['evaluation'].weaknesses
        else:
            risks = design_evaluation.evaluation.risk_assessment
            weaknesses = design_evaluation.evaluation.weaknesses

        strategies = []
        
        for risk_type, level_desc in risks.items():
            if '高' in level_desc:
                if risk_type == 'data_loss':
                    strategies.append("实施多重数据备份策略，包括云端和本地备份")
                elif risk_type == 'consent_violation':
                    strategies.append("制定详细的知情同意流程，包括撤回机制")
                elif risk_type == 'selection_bias':
                    strategies.append("使用更严格的抽样策略，增加验证程序")
                elif risk_type == 'budget_overrun':
                    strategies.append("制定详细的预算计划，预留应急资金")
        
        # 基于弱点制定策略
        for weakness in weaknesses:
            if '样本量' in weakness:
                strategies.append("重新计算样本量，考虑流失率")
            if '伦理' in weakness:
                strategies.append("完善伦理审查材料，加强保护措施")
        
        return strategies
    
    def execute_complete_analysis(
        self,
        literature_data: Union[str, pd.DataFrame],
        research_context: Dict[str, Any],
        design_elements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """执行完整分析流程"""
        print("🚀 开始综合研究设计分析...")
        
        # 1. 文献分析
        self.load_literature_data(literature_data)
        literature_results = self.execute_literature_analysis()
        
        # 2. 方法匹配
        method_results = self.execute_method_matching(research_context)
        
        # 3. 设计评估
        evaluation_results = self.execute_design_evaluation(design_elements)
        
        # 4. 生成最终推荐
        final_recommendation = self.generate_final_recommendation(research_context)
        
        # 整合所有结果
        complete_analysis = {
            'literature_analysis': literature_results,
            'method_matching': method_results,
            'design_evaluation': evaluation_results,
            'final_recommendation': final_recommendation,
            'analysis_summary': self._generate_analysis_summary()
        }
        
        return complete_analysis
    
    def _generate_analysis_summary(self) -> str:
        """生成分析摘要"""
        lit_analysis = self.analysis_state.get('literature_analysis', {})
        method_match = self.analysis_state.get('method_matching', {})
        design_eval = self.analysis_state.get('design_evaluation', {})
        
        summary = []
        summary.append("综合研究设计分析已完成")
        
        if 'knowledge_gaps' in lit_analysis:
            gap_count = len(lit_analysis['knowledge_gaps'])
            summary.append(f"识别了{gap_count}个知识缺口")
        
        if 'matched_methods' in method_match:
            method_count = len(method_match['matched_methods'])
            summary.append(f"评估了{method_count}种方法的适用性")
        
        if 'evaluation' in design_eval:
            overall_score = design_eval['evaluation'].overall_score
            summary.append(f"设计总体评分为{overall_score:.2f}")
        
        return "; ".join(summary)


def main():
    """示例用法"""
    print("🔄 研究设计 - 集成分析模块演示")
    
    # 创建集成分析器
    designer = IntegratedResearchDesigner()
    
    # 创建示例文献数据
    np.random.seed(42)
    sample_literature = pd.DataFrame({
        'title': [
            'The Impact of Social Media on Mental Health',
            'Digital Technology and Psychological Well-being',
            'Social Networks Effects on Individual Behavior',
            'Technology Adoption in Modern Society',
            'Psychological Factors in Digital Engagement'
        ] * 2,  # 重复以增加样本量
        'author': [
            'Smith, J.', 'Johnson, A.', 'Williams, R.',
            'Brown, S.', 'Davis, M.', 'Miller, T.',
            'Wilson, K.', 'Moore, L.', 'Taylor, P.', 'Anderson, H.'
        ],
        'year': np.random.choice(range(2018, 2024), 10),
        'journal': [
            'Journal of Psychology', 'Digital Society Review', 'Tech & Behavior',
            'Modern Psychology', 'Cyberpsychology', 'Social Science Today',
            'Technology Quarterly', 'Digital Research', 'Psychological Science',
            'Online Behavior Studies'
        ],
        'abstract': [
            'This study examines the relationship between social media usage and mental health outcomes...',
            'Research on how digital technology affects psychological well-being...',
            'Analysis of how social networks influence individual behavioral patterns...',
            'Investigation of technology adoption trends in contemporary society...',
            'Study of psychological factors affecting digital engagement...',
            'Patterns of social media usage among young people...',
            'Examining the digital divide and technology access issues...',
            'Role of online communities in providing social support...',
            'Impact of cyberbullying on mental health outcomes...',
            'Privacy concerns in the age of digital technology...'
        ] * 1  # 保持与abstract列表长度一致
    })
    
    # 定义研究上下文
    research_context = {
        'research_topic': '社交媒体对心理健康的影响',
        'research_purpose': '探索和解释',
        'target_population': '大学生群体',
        'hypothesis_testing': True,
        'phenomenon_understanding': False,
        'target_sample_size': 300,
        'time_constraint': 'medium',
        'resource_level': 'adequate',
        'ethical_sensitivity': True,
        'research_questions': [
            '社交媒体使用如何影响大学生的心理健康？',
            '哪些心理因素在其中起到中介作用？'
        ]
    }
    
    # 定义设计元素
    design_elements = {
        'theoretical_framework': '基于社会认知理论和压力应对理论',
        'research_hypotheses': [
            '社交媒体使用时间与焦虑水平正相关',
            '社交比较在其中起中介作用'
        ],
        'variable_relationships': '社交媒体使用 -> 社交比较 -> 心理健康',
        'novelty_indicators': '在特定文化背景下验证理论模型',
        'sampling_strategy': '分层随机抽样',
        'data_collection_methods': '问卷调查、认知测试',
        'sample_size_calculation': '基于功效分析，α=0.05, β=0.2, 效应量=0.3',
        'power_analysis': '事后功效分析确认达到0.8的统计功效',
        'statistical_methods': '结构方程模型、中介效应检验',
        'time_schedule': '6个月',
        'resource_allocation': '预算15万元，2名研究人员',
        'informed_consent_process': '书面知情同意',
        'data_management_plan': '加密存储，权限控制',
        'risk_control_measures': '数据泄露应急预案',
        'bias_control_measures': '随机分配，统计控制'
    }
    
    # 执行完整分析
    complete_results = designer.execute_complete_analysis(
        sample_literature,
        research_context,
        design_elements
    )
    
    # 输出结果摘要
    print(f"\n✅ 分析完成！")
    print(f"知识缺口数量: {len(complete_results['literature_analysis']['knowledge_gaps'])}")
    if isinstance(complete_results['method_matching'], dict):
        print(f"匹配方法数量: {len(complete_results['method_matching']['matched_methods'])}")
    else:
        print(f"匹配方法数量: {len(complete_results['method_matching'])}")
    # 检查design_evaluation的结构
    design_eval_data = complete_results['design_evaluation']
    if isinstance(design_eval_data, dict) and 'evaluation' in design_eval_data:
        design_eval_obj = design_eval_data['evaluation']
    else:
        design_eval_obj = design_eval_data
    if hasattr(design_eval_obj, 'overall_score'):
        overall_score = design_eval_obj.overall_score
    else:
        overall_score = getattr(design_eval_obj, 'overall_score', 0)
    print(f"设计总体评分: {overall_score:.2f}")
    print(f"建议改进措施: {len(complete_results['final_recommendation']['design_improvements'])}项")
    
    # 输出最终推荐摘要
    final_rec = complete_results['final_recommendation']
    print(f"\n📋 最终推荐摘要:")
    print(f"执行摘要: {final_rec['executive_summary']}")
    print(f"推荐设计: {final_rec['methodology_recommendation']['design']}")
    print(f"研究问题优化: {len(final_rec['research_question_refinement'])}个")
    
    print("\n🎯 分析流程已全部完成！")


if __name__ == "__main__":
    main()