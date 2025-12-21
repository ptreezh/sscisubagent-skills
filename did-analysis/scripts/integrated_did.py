#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DID集成分析脚本 - 计量理论、统计方法、政策实践与数据科学的完美结合
根据AI分析决策，调用相应的定性提示词和定量算法
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any
import json
import os
from pathlib import Path
import warnings

# 导入定量分析模块
from did_estimator import DIDEstimator
from parallel_trend import ParallelTrendTester
from robustness_test import RobustnessTester
from visualization import DIDVisualizer


class IntegratedDIDAnalyzer:
    """集成DID分析器 - 理论与实践的完美结合"""
    
    def __init__(self, skill_root: str):
        self.skill_root = Path(skill_root)
        self.prompts_dir = self.skill_root / "prompts"
        self.scripts_dir = self.skill_root / "scripts"
        self.references_dir = self.skill_root / "references"
        
        # 初始化定量分析组件
        self.estimator = DIDEstimator()
        self.trend_tester = ParallelTrendTester()
        self.robustness_tester = RobustnessTester()
        self.visualizer = DIDVisualizer()
        
        # 分析状态跟踪
        self.analysis_state = {
            'phase': 'initiated',
            'experimental_design': None,
            'model_specification': None,
            'estimation_results': None,
            'causal_interpretation': None,
            'policy_recommendations': None
        }
    
    def load_prompt_content(self, prompt_name: str) -> str:
        """加载提示词内容"""
        prompt_file = self.prompts_dir / f"{prompt_name}.md"
        if not prompt_file.exists():
            raise FileNotFoundError(f"提示词文件不存在: {prompt_file}")
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def execute_experimental_design(self, 
                                  policy_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行实验设计阶段
        
        这个方法会加载实验设计提示词，指导AI进行深度政策机制分析
        """
        print("🎯 开始实验设计阶段...")
        
        # 加载实验设计提示词
        design_prompt = self.load_prompt_content("experimental-design")
        
        # 构建实验设计指导
        design_guidance = {
            'prompt_content': design_prompt,
            'policy_context': policy_context,
            'design_focus': [
                'policy_mechanism',
                'group_selection', 
                'time_window',
                'treatment_intensity'
            ],
            'output_requirements': {
                'mechanism_analysis': '政策作用机制分析',
                'group_selection_plan': '实验组对照组选择方案',
                'time_window_design': '时间窗口设计',
                'variable_specification': '变量设定方案'
            }
        }
        
        # 更新分析状态
        self.analysis_state['phase'] = 'experimental_design'
        self.analysis_state['experimental_design'] = design_guidance
        
        return design_guidance
    
    def execute_model_specification(self,
                                  data: pd.DataFrame,
                                  experimental_design: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行模型设定阶段
        
        结合实验设计和数据特征，制定DID模型设定方案
        """
        print("📊 制定DID模型设定...")
        
        # 加载模型设定提示词
        specification_prompt = self.load_prompt_content("model-specification")
        
        # 数据特征分析
        data_characteristics = self._analyze_panel_data_characteristics(data)
        
        # 构建模型设定指导
        specification_guidance = {
            'prompt_content': specification_prompt,
            'data_characteristics': data_characteristics,
            'experimental_design': experimental_design,
            'model_specifications': {},
            'identification_strategy': {}
        }
        
        # 为每个模型类型设定具体方案
        model_types = ['twoway_fe', 'event_study', 'synthetic_control', 'heterogeneous_effects']
        
        for model_type in model_types:
            model_spec = self._create_model_specification(
                model_type, data, data_characteristics, experimental_design
            )
            specification_guidance['model_specifications'][model_type] = model_spec
        
        # 制定因果识别策略
        specification_guidance['identification_strategy'] = self._create_identification_strategy(
            data_characteristics, experimental_design
        )
        
        # 更新分析状态
        self.analysis_state['phase'] = 'model_specification'
        self.analysis_state['model_specification'] = specification_guidance
        
        return specification_guidance
    
    def execute_did_estimation(self,
                              data: pd.DataFrame,
                              entity_col: str,
                              time_col: str,
                              treatment_col: str,
                              outcome_col: str,
                              model_specification: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行DID估计阶段
        
        根据模型设定执行具体的计量估计
        """
        print("🔬 执行DID计量估计...")
        
        # 第一步：平行趋势检验
        print("  - 执行平行趋势检验...")
        parallel_trend_results = self.trend_tester.test_parallel_trend(
            data, entity_col, time_col, treatment_col, outcome_col
        )
        
        # 第二步：基础DID估计
        print("  - 估计基础DID模型...")
        control_vars = model_specification.get('control_variables', [])
        twoway_results = self.estimator.estimate_twoway_fe(
            data, entity_col, time_col, treatment_col, outcome_col, control_vars
        )
        
        # 第三步：事件研究估计
        print("  - 估计事件研究模型...")
        event_results = self.estimator.estimate_event_study(
            data, entity_col, time_col, treatment_col, outcome_col, control_vars
        )
        
        # 第四步：异质性效应分析
        print("  - 分析异质性效应...")
        heterogeneity_vars = model_specification.get('heterogeneity_vars', [])
        het_results = {}
        if heterogeneity_vars:
            het_results = self.estimator.estimate_heterogeneous_effects(
                data, entity_col, time_col, treatment_col, outcome_col, heterogeneity_vars, control_vars
            )
        
        # 第五步：稳健性检验
        print("  - 执行稳健性检验...")
        robustness_results = self.robustness_tester.run_robustness_tests(
            data, entity_col, time_col, treatment_col, outcome_col, twoway_results
        )
        
        # 整合估计结果
        estimation_results = {
            'parallel_trend_test': parallel_trend_results,
            'twoway_fe': twoway_results,
            'event_study': event_results,
            'heterogeneous_effects': het_results,
            'robustness_tests': robustness_results,
            'data_summary': self._summarize_data(data, entity_col, time_col, treatment_col, outcome_col),
            'quality_metrics': self._calculate_estimation_quality(
                parallel_trend_results, twoway_results, robustness_results
            )
        }
        
        # 更新分析状态
        self.analysis_state['phase'] = 'did_estimation'
        self.analysis_state['estimation_results'] = estimation_results
        
        return estimation_results
    
    def execute_causal_interpretation(self,
                                    estimation_results: Dict[str, Any],
                                    experimental_design: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行因果解释阶段
        
        加载因果解释提示词，指导AI进行深度因果机制阐释
        """
        print("📝 深度解释因果效应...")
        
        # 加载因果解释提示词
        interpretation_prompt = self.load_prompt_content("causal-interpretation")
        
        # 准备解释所需的信息
        interpretation_context = {
            'prompt_content': interpretation_prompt,
            'estimation_results': estimation_results,
            'experimental_design': experimental_design,
            'interpretation_focus': [
                'effect_size_interpretation',
                'causal_mechanism',
                'parallel_trend_assessment',
                'robustness_evaluation',
                'policy_implications'
            ]
        }
        
        # 生成解释指导
        interpretation_guidance = self._create_interpretation_guidance(
            estimation_results, experimental_design
        )
        
        interpretation_context['interpretation_guidance'] = interpretation_guidance
        
        # 更新分析状态
        self.analysis_state['phase'] = 'causal_interpretation'
        self.analysis_state['causal_interpretation'] = interpretation_context
        
        return interpretation_context
    
    def execute_policy_recommendations(self,
                                     causal_interpretation: Dict[str, Any],
                                     policy_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行政策建议阶段
        
        基于因果解释和政策背景制定政策建议
        """
        print("🎯 制定政策建议...")
        
        # 加载政策建议提示词
        recommendation_prompt = self.load_prompt_content("policy-recommendation")
        
        # 构建政策建议指导
        recommendation_context = {
            'prompt_content': recommendation_prompt,
            'causal_interpretation': causal_interpretation,
            'policy_context': policy_context,
            'recommendation_types': [
                'policy_continuation',
                'policy_optimization',
                'policy_expansion',
                'policy_innovation'
            ]
        }
        
        # 生成政策建议指导
        recommendation_guidance = self._create_policy_recommendation_guidance(
            causal_interpretation, policy_context
        )
        
        recommendation_context['recommendation_guidance'] = recommendation_guidance
        
        # 更新分析状态
        self.analysis_state['phase'] = 'policy_recommendations'
        self.analysis_state['policy_recommendations'] = recommendation_context
        
        return recommendation_context
    
    def _analyze_panel_data_characteristics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """分析面板数据特征"""
        characteristics = {}
        
        # 基本数据结构
        characteristics['data_structure'] = {
            'n_rows': len(data),
            'n_columns': len(data.columns),
            'memory_usage': data.memory_usage(deep=True).sum()
        }
        
        # 面板数据特征
        entity_col = data.select_dtypes(include=['object']).columns[0] if len(data.select_dtypes(include=['object']).columns) > 0 else None
        time_col = data.select_dtypes(include=['int64', 'float64']).columns[0] if len(data.select_dtypes(include=['int64', 'float64']).columns) > 0 else None
        
        if entity_col and time_col:
            characteristics['panel_structure'] = {
                'n_entities': data[entity_col].nunique(),
                'n_periods': data[time_col].nunique(),
                'balance_ratio': len(data) / (data[entity_col].nunique() * data[time_col].nunique()),
                'time_span': [data[time_col].min(), data[time_col].max()]
            }
        
        # 变量特征
        characteristics['variable_characteristics'] = {}
        for col in data.columns:
            if data[col].dtype in ['int64', 'float64']:
                characteristics['variable_characteristics'][col] = {
                    'dtype': 'numeric',
                    'missing_rate': data[col].isna().sum() / len(data),
                    'mean': data[col].mean(),
                    'std': data[col].std(),
                    'min': data[col].min(),
                    'max': data[col].max()
                }
            else:
                characteristics['variable_characteristics'][col] = {
                    'dtype': 'categorical',
                    'missing_rate': data[col].isna().sum() / len(data),
                    'n_unique': data[col].nunique(),
                    'most_frequent': data[col].mode().iloc[0] if len(data[col].mode()) > 0 else None
                }
        
        return characteristics
    
    def _create_model_specification(self,
                                  model_type: str,
                                  data: pd.DataFrame,
                                  data_characteristics: Dict[str, Any],
                                  experimental_design: Dict[str, Any]) -> Dict[str, Any]:
        """为特定模型类型创建设定方案"""
        spec = {
            'model_type': model_type,
            'suitability': self._assess_model_suitability(model_type, data_characteristics),
            'specification_details': {},
            'identification_assumptions': [],
            'data_requirements': {}
        }
        
        if model_type == 'twoway_fe':
            spec['specification_details'] = {
                'entity_effects': True,
                'time_effects': True,
                'interaction_term': 'treatment * post',
                'control_variables': experimental_design.get('control_variables', [])
            }
            spec['identification_assumptions'] = [
                '平行趋势假设',
                '无预期效应',
                'SUTVA假设'
            ]
            
        elif model_type == 'event_study':
            spec['specification_details'] = {
                'event_time_dummies': True,
                'reference_period': -1,
                'dynamic_effects': True,
                'leads_and_lags': True
            }
            spec['identification_assumptions'] = [
                '平行趋势假设',
                '无预期效应',
                '效应线性性'
            ]
            
        elif model_type == 'synthetic_control':
            spec['specification_details'] = {
                'treated_unit': experimental_design.get('treated_entity'),
                'donor_pool': experimental_design.get('control_entities'),
                'pre_treatment_periods': experimental_design.get('pre_period_length'),
                'optimization_method': 'least_squares'
            }
            spec['identification_assumptions'] = [
                '合成控制权重非负',
                '权重和为1',
                '无未观测因素干扰'
            ]
            
        elif model_type == 'heterogeneous_effects':
            spec['specification_details'] = {
                'heterogeneity_vars': experimental_design.get('heterogeneity_vars', []),
                'interaction_terms': True,
                'subgroup_analysis': True
            }
            spec['identification_assumptions'] = [
                '平行趋势假设在各组成立',
                '异质性外生性'
            ]
        
        return spec
    
    def _assess_model_suitability(self, model_type: str, data_characteristics: Dict[str, Any]) -> str:
        """评估模型适合性"""
        if 'panel_structure' not in data_characteristics:
            return 'unknown'
        
        n_entities = data_characteristics['panel_structure']['n_entities']
        n_periods = data_characteristics['panel_structure']['n_periods']
        balance_ratio = data_characteristics['panel_structure']['balance_ratio']
        
        if model_type == 'twoway_fe':
            if n_entities >= 10 and n_periods >= 3 and balance_ratio > 0.7:
                return 'highly_suitable'
            elif n_entities >= 5 and n_periods >= 2:
                return 'moderately_suitable'
            else:
                return 'not_suitable'
                
        elif model_type == 'event_study':
            if n_periods >= 5 and balance_ratio > 0.8:
                return 'highly_suitable'
            elif n_periods >= 3:
                return 'moderately_suitable'
            else:
                return 'not_suitable'
                
        elif model_type == 'synthetic_control':
            if n_entities >= 20 and n_periods >= 5:
                return 'highly_suitable'
            elif n_entities >= 10 and n_periods >= 3:
                return 'moderately_suitable'
            else:
                return 'not_suitable'
                
        elif model_type == 'heterogeneous_effects':
            if n_entities >= 20:
                return 'highly_suitable'
            elif n_entities >= 10:
                return 'moderately_suitable'
            else:
                return 'not_suitable'
        
        return 'unknown'
    
    def _create_identification_strategy(self,
                                      data_characteristics: Dict[str, Any],
                                      experimental_design: Dict[str, Any]) -> Dict[str, Any]:
        """创建因果识别策略"""
        strategy = {
            'primary_strategy': 'difference_in_differences',
            'identification_assumptions': [],
            'threats_to_identification': [],
            'mitigation_strategies': []
        }
        
        # 基本DID假设
        strategy['identification_assumptions'] = [
            '平行趋势假设',
            '无预期效应',
            '处理外生性',
            '稳定单位处理值假设(SUTVA)',
            '无同时期其他政策干预'
        ]
        
        # 识别威胁
        strategy['threats_to_identification'] = [
            '处理组和对照组趋势差异',
            '预期效应存在',
            '处理内生性',
            '同时期政策干扰',
            '测量误差'
        ]
        
        # 缓解策略
        strategy['mitigation_strategies'] = [
            '平行趋势检验',
            '事件研究分析',
            '工具变量法',
            '安慰剂检验',
            '稳健性检验'
        ]
        
        return strategy
    
    def _summarize_data(self, data: pd.DataFrame, entity_col: str, time_col: str, 
                        treatment_col: str, outcome_col: str) -> Dict[str, Any]:
        """总结数据特征"""
        summary = {}
        
        # 处理组统计
        treated_data = data[data[treatment_col] == 1]
        control_data = data[data[treatment_col] == 0]
        
        summary['treatment_stats'] = {
            'n_treated_entities': treated_data[entity_col].nunique(),
            'n_control_entities': control_data[entity_col].nunique(),
            'treatment_rate': len(treated_data) / len(data),
            'outcome_mean_treated': treated_data[outcome_col].mean(),
            'outcome_mean_control': control_data[outcome_col].mean()
        }
        
        # 时间趋势
        time_trends = data.groupby([time_col, treatment_col])[outcome_col].mean().unstack()
        summary['time_trends'] = time_trends.to_dict()
        
        return summary
    
    def _calculate_estimation_quality(self,
                                    parallel_trend_results: Dict[str, Any],
                                    twoway_results: Dict[str, Any],
                                    robustness_results: Dict[str, Any]) -> Dict[str, Any]:
        """计算估计质量指标"""
        quality = {}
        
        # 平行趋势检验质量
        if 'parallel_trend_pvalue' in parallel_trend_results:
            quality['parallel_trend'] = {
                'assumption_met': parallel_trend_results['parallel_trend_pvalue'] > 0.05,
                'p_value': parallel_trend_results['parallel_trend_pvalue'],
                'confidence': 'high' if parallel_trend_results['parallel_trend_pvalue'] > 0.1 else 'medium'
            }
        
        # DID估计质量
        quality['did_estimation'] = {
            'statistical_significance': twoway_results['did_pvalue'] < 0.05,
            'effect_size': abs(twoway_results['did_effect']),
            'precision': twoway_results['did_se'] / abs(twoway_results['did_effect']),
            'model_fit': twoway_results['r_squared']
        }
        
        # 稳健性质量
        if 'placebo_pvalue' in robustness_results:
            quality['robustness'] = {
                'placebo_test_passed': robustness_results['placebo_pvalue'] < 0.05,
                'sensitivity_analysis': 'stable' if robustness_results.get('sensitivity_stable', False) else 'unstable'
            }
        
        # 综合质量分数
        quality_scores = []
        if 'parallel_trend' in quality:
            quality_scores.append(1.0 if quality['parallel_trend']['assumption_met'] else 0.5)
        if 'did_estimation' in quality:
            quality_scores.append(min(1.0, quality['did_estimation']['model_fit'] * 2))
        if 'robustness' in quality:
            quality_scores.append(1.0 if quality['robustness']['placebo_test_passed'] else 0.5)
        
        quality['overall_quality'] = np.mean(quality_scores) if quality_scores else 0.5
        
        return quality
    
    def _create_interpretation_guidance(self,
                                      estimation_results: Dict[str, Any],
                                      experimental_design: Dict[str, Any]) -> Dict[str, Any]:
        """创建因果解释指导"""
        guidance = {
            'effect_interpretation': {},
            'mechanism_analysis': {},
            'robustness_assessment': {},
            'interpretation_questions': []
        }
        
        # 效应解释指导
        if 'twoway_fe' in estimation_results:
            did_results = estimation_results['twoway_fe']
            guidance['effect_interpretation'] = {
                'point_estimate': did_results['did_effect'],
                'confidence_interval': [did_results['did_ci_lower'], did_results['did_ci_upper']],
                'statistical_significance': did_results['did_pvalue'],
                'economic_significance': self._assess_economic_significance(did_results),
                'interpretation_focus': [
                    '效应大小的实际含义',
                    '置信区间的政策含义',
                    '统计显著性与实际意义的关系'
                ]
            }
        
        # 机制分析指导
        guidance['mechanism_analysis'] = {
            'parallel_trend_status': estimation_results.get('parallel_trend_test', {}),
            'dynamic_effects': estimation_results.get('event_study', {}),
            'heterogeneity_patterns': estimation_results.get('heterogeneous_effects', {}),
            'analysis_questions': [
                '政策通过什么渠道产生效应？',
                '效应是否随时间变化？',
                '不同群体的效应差异如何解释？'
            ]
        }
        
        # 稳健性评估指导
        guidance['robustness_assessment'] = {
            'robustness_results': estimation_results.get('robustness_tests', {}),
            'quality_metrics': estimation_results.get('quality_metrics', {}),
            'assessment_criteria': [
                '平行趋势假设是否满足？',
                '安慰剂检验是否通过？',
                '不同模型设定的结果是否一致？'
            ]
        }
        
        # 解释问题
        guidance['interpretation_questions'] = [
            "估计的因果效应在理论和实践上意味着什么？",
            "平行趋势假设的满足程度如何影响因果推断的可靠性？",
            "异质性效应揭示的政策含义是什么？",
            "稳健性检验结果对因果推断的信心有何影响？",
            "研究结果对政策制定有什么具体指导意义？"
        ]
        
        return guidance
    
    def _assess_economic_significance(self, did_results: Dict[str, Any]) -> str:
        """评估经济显著性"""
        effect_size = abs(did_results['did_effect'])
        
        # 简化的经济显著性评估（实际应用中需要具体领域知识）
        if effect_size > 10:
            return 'large'
        elif effect_size > 5:
            return 'medium'
        elif effect_size > 1:
            return 'small'
        else:
            return 'minimal'
    
    def _create_policy_recommendation_guidance(self,
                                             causal_interpretation: Dict[str, Any],
                                             policy_context: Dict[str, Any]) -> Dict[str, Any]:
        """创建政策建议指导"""
        guidance = {
            'effectiveness_assessment': {},
            'recommendation_types': {},
            'implementation_considerations': {},
            'risk_assessment': {}
        }
        
        # 有效性评估
        if 'estimation_results' in causal_interpretation:
            estimation = causal_interpretation['estimation_results']
            guidance['effectiveness_assessment'] = {
                'policy_effectiveness': self._assess_policy_effectiveness(estimation),
                'cost_benefit_considerations': self._generate_cost_benefit_considerations(estimation),
                'target_group_benefits': self._identify_target_group_benefits(estimation)
            }
        
        # 建议类型
        guidance['recommendation_types'] = {
            'continuation': {
                'condition': 'effect_positive_and_significant',
                'rationale': '政策产生了预期效果'
            },
            'optimization': {
                'condition': 'effect_moderate_or_heterogeneous',
                'rationale': '政策有改进空间'
            },
            'expansion': {
                'condition': 'effect_large_and_robust',
                'rationale': '政策效果显著且稳健'
            },
            'termination': {
                'condition': 'effect_negative_or_insignificant',
                'rationale': '政策未产生预期效果'
            }
        }
        
        # 实施考虑
        guidance['implementation_considerations'] = {
            'scalability': '政策是否可以扩大规模？',
            'resource_requirements': '实施政策需要什么资源？',
            'institutional_capacity': '是否有足够的制度能力？',
            'political_feasibility': '政治上是否可行？'
        }
        
        # 风险评估
        guidance['risk_assessment'] = {
            'external_validity': '结果是否可以推广到其他情境？',
            'unintended_consequences': '是否存在潜在的负面效应？',
            'sustainability': '政策效果是否可持续？',
            'equity_implications': '政策对不同群体的影响是否公平？'
        }
        
        return guidance
    
    def _assess_policy_effectiveness(self, estimation_results: Dict[str, Any]) -> str:
        """评估政策有效性"""
        if 'twoway_fe' not in estimation_results:
            return 'unknown'
        
        did_results = estimation_results['twoway_fe']
        effect = did_results['did_effect']
        pvalue = did_results['did_pvalue']
        
        if pvalue < 0.05 and effect > 0:
            return 'effective'
        elif pvalue < 0.05 and effect < 0:
            return 'counterproductive'
        elif pvalue >= 0.05:
            return 'ineffective'
        else:
            return 'unclear'
    
    def _generate_cost_benefit_considerations(self, estimation_results: Dict[str, Any]) -> List[str]:
        """生成成本效益考虑"""
        return [
            "政策实施成本与效应大小的比较",
            "长期效应与短期效应的权衡",
            "直接效应与间接效应的综合评估",
            "可量化收益与不可量化收益的平衡"
        ]
    
    def _identify_target_group_benefits(self, estimation_results: Dict[str, Any]) -> List[str]:
        """识别目标群体收益"""
        benefits = []
        
        if 'heterogeneous_effects' in estimation_results:
            het_results = estimation_results['heterogeneous_effects']
            for var, effects in het_results.items():
                if 'group_effects' in effects:
                    for group, effect in effects['group_effects'].items():
                        if effect > 0:
                            benefits.append(f"{var}={group}群体: 正面效应")
        
        return benefits
    
    def generate_comprehensive_report(self, output_file: str = None) -> str:
        """生成完整的DID分析报告"""
        report_sections = []
        
        # 报告标题
        report_sections.append("# DID因果推断分析报告\n")
        
        # 实验设计部分
        if self.analysis_state['experimental_design']:
            report_sections.append("## 🎯 实验设计\n")
            report_sections.append("实验设计已完成，详见实验设计指导文档。\n")
        
        # 模型设定部分
        if self.analysis_state['model_specification']:
            report_sections.append("## 📊 模型设定\n")
            model_spec = self.analysis_state['model_specification']
            report_sections.append("模型设定方案已制定，包含多种DID估计方法。\n")
        
        # 估计结果部分
        if self.analysis_state['estimation_results']:
            report_sections.append("## 🔬 DID估计结果\n")
            results = self.analysis_state['estimation_results']
            
            report_sections.append("### 主要估计结果\n")
            if 'twoway_fe' in results:
                did = results['twoway_fe']
                report_sections.append(f"- DID效应: {did['did_effect']:.4f} (p={did['did_pvalue']:.4f})\n")
                report_sections.append(f"- 95%置信区间: [{did['did_ci_lower']:.4f}, {did['did_ci_upper']:.4f}]\n")
                report_sections.append(f"- R²: {did['r_squared']:.4f}\n")
            
            report_sections.append("### 平行趋势检验\n")
            if 'parallel_trend_test' in results:
                pt = results['parallel_trend_test']
                if 'parallel_trend_pvalue' in pt:
                    report_sections.append(f"- 平行趋势检验p值: {pt['parallel_trend_pvalue']:.4f}\n")
            
            report_sections.append("### 稳健性检验\n")
            if 'robustness_tests' in results:
                rt = results['robustness_tests']
                if 'placebo_pvalue' in rt:
                    report_sections.append(f"- 安慰剂检验p值: {rt['placebo_pvalue']:.4f}\n")
        
        # 因果解释部分
        if self.analysis_state['causal_interpretation']:
            report_sections.append("## 📝 因果解释\n")
            interpretation = self.analysis_state['causal_interpretation']
            report_sections.append("因果解释指导已生成，请参考因果解释提示词进行深度分析。\n")
        
        # 政策建议部分
        if self.analysis_state['policy_recommendations']:
            report_sections.append("## 🎯 政策建议\n")
            recommendations = self.analysis_state['policy_recommendations']
            report_sections.append("政策建议指导已生成，请参考政策建议提示词制定具体建议。\n")
        
        # 生成报告
        report = "\n".join(report_sections)
        
        # 保存报告
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"DID分析报告已保存到: {output_file}")
        
        return report


def main():
    """示例用法"""
    # 设置技能根目录
    skill_root = "D:/stigmergy-CLI-Multi-Agents/sscisubagent-skills/did-analysis"
    
    # 初始化集成分析器
    analyzer = IntegratedDIDAnalyzer(skill_root)
    
    # 创建示例面板数据
    np.random.seed(42)
    n_entities = 30
    n_periods = 8
    entities = [f"entity_{i}" for i in range(n_entities)]
    periods = list(range(2015, 2015 + n_periods))
    
    data = []
    for entity in entities:
        base_outcome = 100 + np.random.normal(0, 10)
        entity_fe = np.random.normal(0, 5)
        
        for period in periods:
            time_fe = (period - 2015) * 2
            treat = 0
            
            # 处理效应
            if entity in ['entity_1', 'entity_2', 'entity_3'] and period >= 2018:
                treat = 1
                treatment_effect = 15
            else:
                treatment_effect = 0
            
            outcome = (base_outcome + entity_fe + time_fe + treatment_effect + 
                     np.random.normal(0, 5))
            
            data.append({
                'entity': entity,
                'year': period,
                'treatment': treat,
                'outcome': outcome,
                'control_var1': np.random.normal(0, 1),
                'control_var2': np.random.normal(0, 1)
            })
    
    df = pd.DataFrame(data)
    
    print("🚀 开始DID集成分析...")
    
    # 第一步：实验设计
    policy_context = {
        'policy_name': '教育质量提升政策',
        'policy_objective': '提高学生学业成绩',
        'implementation_year': 2018,
        'target_population': '中小学学生'
    }
    
    experimental_design = analyzer.execute_experimental_design(policy_context)
    
    # 第二步：模型设定
    model_specification = analyzer.execute_model_specification(df, experimental_design)
    
    # 第三步：DID估计
    estimation_results = analyzer.execute_did_estimation(
        df, 'entity', 'year', 'treatment', 'outcome', model_specification
    )
    
    # 第四步：因果解释
    causal_interpretation = analyzer.execute_causal_interpretation(
        estimation_results, experimental_design
    )
    
    # 第五步：政策建议
    policy_recommendations = analyzer.execute_policy_recommendations(
        causal_interpretation, policy_context
    )
    
    # 生成报告
    report = analyzer.generate_comprehensive_report("did_analysis_report.md")
    
    print("✅ DID集成分析完成！")
    print(f"分析阶段: {analyzer.analysis_state['phase']}")
    print("详细报告已生成，请查看各阶段的提示词指导进行深度分析。")


if __name__ == "__main__":
    main()
