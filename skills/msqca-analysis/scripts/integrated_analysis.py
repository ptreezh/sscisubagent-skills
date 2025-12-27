#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
msQCA集成分析脚本 - 定性与定量完美结合的核心引擎
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
from calibration import QCACalibration
from truth_table import TruthTableBuilder
from minimization import BooleanMinimizer


class IntegratedQCAAnalyzer:
    """集成QCA分析器 - 定性与定量完美结合"""
    
    def __init__(self, skill_root: str):
        self.skill_root = Path(skill_root)
        self.prompts_dir = self.skill_root / "prompts"
        self.scripts_dir = self.skill_root / "scripts"
        self.references_dir = self.skill_root / "references"
        
        # 初始化定量分析组件
        self.calibrator = QCACalibration()
        self.truth_table_builder = TruthTableBuilder()
        self.minimizer = BooleanMinimizer()
        
        # 分析状态跟踪
        self.analysis_state = {
            'phase': 'initiated',
            'theoretical_analysis': None,
            'calibration_plan': None,
            'quantitative_results': None,
            'interpretation': None
        }
    
    def load_prompt_content(self, prompt_name: str) -> str:
        """加载提示词内容"""
        prompt_file = self.prompts_dir / f"{prompt_name}.md"
        if not prompt_file.exists():
            raise FileNotFoundError(f"提示词文件不存在: {prompt_file}")
        
        with open(prompt_file, 'r', encoding='utf-8') as f:
            return f.read()
    
    def execute_theoretical_analysis(self, 
                                   research_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行理论分析阶段
        
        这个方法会加载理论分析提示词，指导AI进行深度理论分析
        """
        print("🎯 开始理论分析阶段...")
        
        # 加载理论分析提示词
        theoretical_prompt = self.load_prompt_content("theoretical-analysis")
        
        # 构建理论分析指导
        analysis_guidance = {
            'prompt_content': theoretical_prompt,
            'research_context': research_context,
            'analysis_focus': [
                'theoretical_framework',
                'condition_selection', 
                'causal_mechanisms',
                'calibration_theory'
            ],
            'output_requirements': {
                'theoretical_framework': '核心概念和假设',
                'selected_conditions': '条件变量选择理由',
                'causal_paths': '预期因果路径',
                'calibration_guidance': '校准理论依据'
            }
        }
        
        # 更新分析状态
        self.analysis_state['phase'] = 'theoretical_analysis'
        self.analysis_state['theoretical_analysis'] = analysis_guidance
        
        return analysis_guidance
    
    def execute_calibration_guidance(self,
                                   data: pd.DataFrame,
                                   theoretical_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行校准指导阶段
        
        结合理论分析和数据特征，制定校准方案
        """
        print("📊 制定校准方案...")
        
        # 加载校准指导提示词
        calibration_prompt = self.load_prompt_content("calibration-guidance")
        
        # 数据特征分析
        data_characteristics = self._analyze_data_characteristics(data)
        
        # 构建校准指导
        calibration_guidance = {
            'prompt_content': calibration_prompt,
            'data_characteristics': data_characteristics,
            'theoretical_analysis': theoretical_analysis,
            'calibration_decisions': {},
            'quality_checks': []
        }
        
        # 为每个变量制定校准方案
        for column in data.columns:
            if column != 'case_id' and column != 'case_description':
                var_info = data_characteristics[column]
                calibration_plan = self._create_variable_calibration_plan(
                    column, var_info, theoretical_analysis
                )
                calibration_guidance['calibration_decisions'][column] = calibration_plan
        
        # 更新分析状态
        self.analysis_state['phase'] = 'calibration_guidance'
        self.analysis_state['calibration_plan'] = calibration_guidance
        
        return calibration_guidance
    
    def execute_quantitative_analysis(self,
                                    data: pd.DataFrame,
                                    conditions: List[str],
                                    outcome: str,
                                    calibration_plan: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行定量分析阶段
        
        根据校准计划执行具体的定量计算
        """
        print("🔬 执行定量分析...")
        
        # 第一步：执行校准
        print("  - 执行数据校准...")
        calibrated_data = self._perform_calibration(data, calibration_plan)
        
        # 第二步：构建真值表
        print("  - 构建真值表...")
        truth_table = self.truth_table_builder.build_truth_table(
            calibrated_data, conditions, outcome
        )
        
        # 处理矛盾组合
        if len(self.truth_table_builder.contradictory_cases) > 0:
            print("  - 处理矛盾组合...")
            truth_table = self.truth_table_builder.handle_contradictions(method='remove')
        
        # 第三步：逻辑最小化
        print("  - 执行逻辑最小化...")
        solutions = self.minimizer.minimize(truth_table, conditions)
        
        # 第四步：质量评估
        print("  - 评估分析质量...")
        quality_metrics = self._calculate_analysis_quality(
            calibrated_data, truth_table, solutions
        )
        
        # 整合定量结果
        quantitative_results = {
            'calibrated_data': calibrated_data,
            'truth_table': truth_table,
            'solutions': solutions,
            'quality_metrics': quality_metrics,
            'technical_details': {
                'n_cases': len(calibrated_data),
                'n_conditions': len(conditions),
                'n_positive_cases': len(truth_table[truth_table['result_type'] == 1]),
                'n_contradictions': len(self.truth_table_builder.contradictory_cases),
                'n_logical_remainders': len(self.truth_table_builder.logical_remainders)
            }
        }
        
        # 更新分析状态
        self.analysis_state['phase'] = 'quantitative_analysis'
        self.analysis_state['quantitative_results'] = quantitative_results
        
        return quantitative_results
    
    def execute_result_interpretation(self,
                                    quantitative_results: Dict[str, Any],
                                    theoretical_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        执行结果解释阶段
        
        加载结果解释提示词，指导AI进行深度结果解释
        """
        print("📝 深度解释分析结果...")
        
        # 加载结果解释提示词
        interpretation_prompt = self.load_prompt_content("result-interpretation")
        
        # 准备解释所需的信息
        interpretation_context = {
            'prompt_content': interpretation_prompt,
            'quantitative_results': quantitative_results,
            'theoretical_analysis': theoretical_analysis,
            'interpretation_focus': [
                'solution_analysis',
                'causal_mechanisms',
                'theoretical_contributions',
                'practical_implications'
            ]
        }
        
        # 生成解释指导
        interpretation_guidance = self._create_interpretation_guidance(
            quantitative_results, theoretical_analysis
        )
        
        interpretation_context['interpretation_guidance'] = interpretation_guidance
        
        # 更新分析状态
        self.analysis_state['phase'] = 'result_interpretation'
        self.analysis_state['interpretation'] = interpretation_context
        
        return interpretation_context
    
    def _analyze_data_characteristics(self, data: pd.DataFrame) -> Dict[str, Any]:
        """分析数据特征"""
        characteristics = {}
        
        for column in data.columns:
            if column not in ['case_id', 'case_description']:
                col_data = data[column].dropna()
                
                characteristics[column] = {
                    'type': self._determine_variable_type(col_data),
                    'n_missing': data[column].isna().sum(),
                    'missing_rate': data[column].isna().sum() / len(data),
                    'unique_values': col_data.nunique(),
                    'value_range': [col_data.min(), col_data.max()] if col_data.dtype in ['int64', 'float64'] else list(col_data.unique()),
                    'distribution': self._describe_distribution(col_data)
                }
        
        return characteristics
    
    def _determine_variable_type(self, series: pd.Series) -> str:
        """确定变量类型"""
        if series.dtype in ['int64', 'float64']:
            if series.nunique() <= 10:
                return 'discrete_numeric'
            else:
                return 'continuous'
        else:
            if series.nunique() <= 10:
                return 'categorical'
            else:
                return 'text'
    
    def _describe_distribution(self, series: pd.Series) -> Dict[str, Any]:
        """描述数据分布"""
        if series.dtype in ['int64', 'float64']:
            # 检查数据是否为空或全部为NaN
            if len(series) == 0 or series.isna().all():
                return {
                    'mean': np.nan,
                    'std': np.nan,
                    'skewness': np.nan,
                    'kurtosis': np.nan,
                    'distribution_shape': 'undefined'
                }

            # 使用安全的统计计算
            return {
                'mean': series.mean() if not np.isnan(series.mean()) else np.nan,
                'std': series.std() if not np.isnan(series.std()) else np.nan,
                'skewness': series.skew() if not np.isnan(series.skew()) else np.nan,
                'kurtosis': series.kurtosis() if not np.isnan(series.kurtosis()) else np.nan,
                'distribution_shape': self._identify_distribution_shape(series.dropna())
            }
        else:
            value_counts = series.value_counts()
            return {
                'value_counts': value_counts.to_dict(),
                'most_common': value_counts.index[0] if len(value_counts) > 0 else None
            }
    
    def _identify_distribution_shape(self, series: pd.Series) -> str:
        """识别分布形状"""
        skewness = series.skew()
        kurtosis = series.kurtosis()
        
        if abs(skewness) < 0.5 and abs(kurtosis) < 0.5:
            return 'normal'
        elif skewness > 1:
            return 'right_skewed'
        elif skewness < -1:
            return 'left_skewed'
        elif kurtosis > 1:
            return 'heavy_tailed'
        else:
            return 'irregular'
    
    def _create_variable_calibration_plan(self,
                                        variable: str,
                                        var_info: Dict[str, Any],
                                        theoretical_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """为变量创建校准计划"""
        plan = {
            'variable': variable,
            'variable_type': var_info['type'],
            'data_quality': {
                'missing_rate': var_info['missing_rate'],
                'unique_values': var_info['unique_values']
            }
        }
        
        # 根据变量类型推荐校准方法
        if var_info['type'] == 'continuous':
            if var_info['unique_values'] > 20:
                plan['recommended_method'] = 'direct'
                plan['reason'] = '连续变量，取值丰富，适合直接校准'
            else:
                plan['recommended_method'] = 'indirect'
                plan['reason'] = '连续变量但取值有限，适合间接校准'
        elif var_info['type'] == 'discrete_numeric':
            plan['recommended_method'] = 'multi_value'
            plan['reason'] = '离散数值变量，适合多值校准'
        else:
            plan['recommended_method'] = 'multi_value'
            plan['reason'] = '分类变量，适合多值校准'
        
        # 如果有理论分析，整合理论指导
        if theoretical_analysis and 'calibration_guidance' in theoretical_analysis:
            plan['theoretical_guidance'] = theoretical_analysis['calibration_guidance']
        
        return plan
    
    def _perform_calibration(self,
                           data: pd.DataFrame,
                           calibration_plan: Dict[str, Any]) -> pd.DataFrame:
        """执行数据校准"""
        calibrated_data = data.copy()
        
        for variable, plan in calibration_plan['calibration_decisions'].items():
            if variable in data.columns:
                method = plan['recommended_method']
                
                # 根据计划执行校准
                if method == 'auto':
                    calibrated_series = self.calibrator.calibrate_variable(
                        data[variable], method='auto'
                    )
                elif method == 'direct':
                    # 这里可以添加具体的阈值设定
                    calibrated_series = self.calibrator.calibrate_variable(
                        data[variable], method='direct'
                    )
                elif method == 'indirect':
                    calibrated_series = self.calibrator.calibrate_variable(
                        data[variable], method='indirect'
                    )
                elif method == 'multi_value':
                    calibrated_series = self.calibrator.calibrate_variable(
                        data[variable], method='multi_value'
                    )
                else:
                    calibrated_series = data[variable]  # 保持原值
                
                calibrated_data[variable] = calibrated_series
        
        return calibrated_data
    
    def _calculate_analysis_quality(self,
                                  calibrated_data: pd.DataFrame,
                                  truth_table: pd.DataFrame,
                                  solutions: List) -> Dict[str, Any]:
        """计算分析质量指标"""
        quality_metrics = {}

        # 数据质量指标
        if calibrated_data.size > 0:
            completeness = 1.0 - calibrated_data.isna().sum().sum() / calibrated_data.size
            calibration_coverage = len(calibrated_data.dropna()) / len(calibrated_data) if len(calibrated_data) > 0 else 0
            quality_metrics['data_quality'] = {
                'completeness': completeness if not np.isnan(completeness) else 0.0,
                'calibration_coverage': calibration_coverage
            }
        else:
            quality_metrics['data_quality'] = {
                'completeness': 0.0,
                'calibration_coverage': 0.0
            }

        # 真值表质量指标
        truth_table_quality = self.truth_table_builder.calculate_quality_metrics()
        quality_metrics['truth_table_quality'] = truth_table_quality

        # 解质量指标
        if solutions:
            # 过滤掉无效解（coverage或consistency为NaN的解）
            valid_solutions = [sol for sol in solutions if not (np.isnan(sol.coverage) or np.isnan(sol.consistency))]
            if valid_solutions:
                best_solution = max(valid_solutions, key=lambda x: x.coverage * x.consistency)
                quality_metrics['solution_quality'] = {
                    'best_coverage': best_solution.coverage,
                    'best_consistency': best_solution.consistency,
                    'solution_complexity': best_solution.complexity,
                    'n_solutions': len(solutions)
                }

        # 综合质量分数
        quality_metrics['overall_quality'] = self._calculate_overall_quality(quality_metrics)

        return quality_metrics
    
    def _calculate_overall_quality(self, quality_metrics: Dict[str, Any]) -> float:
        """计算综合质量分数"""
        # 从质量指标中获取数据质量分数
        data_quality = quality_metrics.get('data_quality', {})
        data_score = data_quality.get('completeness', 0.0)

        # 处理NaN值
        if np.isnan(data_score):
            data_score = 0.0

        # 获取真值表质量分数
        if 'truth_table_quality' in quality_metrics:
            contradiction_rate = quality_metrics['truth_table_quality'].get('contradiction_rate', 0.0)
            if np.isnan(contradiction_rate):
                contradiction_rate = 0.0
            table_score = min(1.0, 1.0 - contradiction_rate)
        else:
            table_score = 0.5

        # 获取解质量分数
        if 'solution_quality' in quality_metrics:
            best_coverage = quality_metrics['solution_quality'].get('best_coverage', 0.0)
            best_consistency = quality_metrics['solution_quality'].get('best_consistency', 0.0)

            # 处理NaN值
            if np.isnan(best_coverage):
                best_coverage = 0.0
            if np.isnan(best_consistency):
                best_consistency = 0.0

            solution_score = (best_coverage + best_consistency) / 2
        else:
            solution_score = 0.5

        # 处理可能的NaN值
        if np.isnan(data_score):
            data_score = 0.0
        if np.isnan(table_score):
            table_score = 0.0
        if np.isnan(solution_score):
            solution_score = 0.0

        # 加权平均
        overall_score = (data_score * 0.3 + table_score * 0.4 + solution_score * 0.3)

        # 确保结果是有效数值
        if np.isnan(overall_score) or np.isinf(overall_score):
            overall_score = 0.0

        return overall_score
    
    def _create_interpretation_guidance(self,
                                      quantitative_results: Dict[str, Any],
                                      theoretical_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """创建结果解释指导"""
        guidance = {
            'solutions_summary': [],
            'key_findings': [],
            'interpretation_questions': []
        }
        
        # 总结解方案
        for i, solution in enumerate(quantitative_results['solutions']):
            solution_summary = {
                'solution_id': i + 1,
                'type': solution.solution_type.value,
                'expression': solution.expression,
                'coverage': solution.coverage,
                'consistency': solution.consistency,
                'complexity': solution.complexity
            }
            guidance['solutions_summary'].append(solution_summary)
        
        # 识别关键发现
        best_solution = max(quantitative_results['solutions'], 
                          key=lambda x: x.coverage * x.consistency)
        
        guidance['key_findings'] = [
            f"最优解覆盖度: {best_solution.coverage:.3f}",
            f"最优解一致性: {best_solution.consistency:.3f}",
            f"质蕴含项数量: {len(best_solution.prime_implicants)}",
            f"案例总数: {quantitative_results['technical_details']['n_cases']}",
            f"正面案例数: {quantitative_results['technical_details']['n_positive_cases']}"
        ]
        
        # 生成解释问题
        guidance['interpretation_questions'] = [
            "这些因果路径背后的理论机制是什么？",
            "不同路径适用于什么样的情境条件？",
            "研究发现对现有理论有什么贡献？",
            "如何将这些发现转化为实践建议？",
            "研究的局限性是什么，未来研究方向如何？"
        ]
        
        return guidance
    
    def generate_analysis_report(self, output_file: str = None) -> str:
        """生成完整的分析报告"""
        report_sections = []
        
        # 报告标题
        report_sections.append("# msQCA集成分析报告\n")
        
        # 理论分析部分
        if self.analysis_state['theoretical_analysis']:
            report_sections.append("## 🎯 理论分析\n")
            report_sections.append("理论分析已完成，详见分析指导文档。\n")
        
        # 校准方案部分
        if self.analysis_state['calibration_plan']:
            report_sections.append("## 📊 校准方案\n")
            calibration_plan = self.analysis_state['calibration_plan']
            for var, plan in calibration_plan['calibration_decisions'].items():
                report_sections.append(f"**{var}**: {plan['recommended_method']} - {plan['reason']}\n")
        
        # 定量结果部分
        if self.analysis_state['quantitative_results']:
            report_sections.append("## 🔬 定量分析结果\n")
            results = self.analysis_state['quantitative_results']
            
            report_sections.append("### 质量指标\n")
            quality = results['quality_metrics']
            report_sections.append(f"- 数据完整性: {quality['data_quality']['completeness']:.3f}\n")
            report_sections.append(f"- 综合质量: {quality['overall_quality']:.3f}\n")
            
            report_sections.append("### 最优解\n")
            best_solution = max(results['solutions'], key=lambda x: x.coverage * x.consistency)
            report_sections.append(f"- 表达式: {best_solution.expression}\n")
            report_sections.append(f"- 覆盖度: {best_solution.coverage:.3f}\n")
            report_sections.append(f"- 一致性: {best_solution.consistency:.3f}\n")
        
        # 结果解释部分
        if self.analysis_state['interpretation']:
            report_sections.append("## 📝 结果解释\n")
            interpretation = self.analysis_state['interpretation']
            report_sections.append("结果解释指导已生成，请参考解释提示词进行深度分析。\n")
        
        # 生成报告
        report = "\n".join(report_sections)
        
        # 保存报告
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"分析报告已保存到: {output_file}")
        
        return report


def main():
    """示例用法"""
    # 设置技能根目录
    skill_root = "D:/stigmergy-CLI-Multi-Agents/sscisubagent-skills/msqca-analysis"
    
    # 初始化集成分析器
    analyzer = IntegratedQCAAnalyzer(skill_root)
    
    # 创建示例数据
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'case_id': range(1, 21),
        'A': np.random.choice([0, 1, 2], 20),
        'B': np.random.choice([0, 1, 2], 20),
        'C': np.random.choice([0, 1, 2], 20),
        'Y': np.random.uniform(0, 1, 20)
    })
    
    print("🚀 开始msQCA集成分析...")
    
    # 第一步：理论分析
    research_context = {
        'research_question': '什么条件组合导致高绩效？',
        'theoretical_framework': '资源基础观',
        'case_description': '20个组织案例'
    }
    
    theoretical_analysis = analyzer.execute_theoretical_analysis(research_context)
    
    # 第二步：校准指导
    calibration_plan = analyzer.execute_calibration_guidance(
        sample_data, theoretical_analysis
    )
    
    # 第三步：定量分析
    conditions = ['A', 'B', 'C']
    outcome = 'Y'
    
    quantitative_results = analyzer.execute_quantitative_analysis(
        sample_data, conditions, outcome, calibration_plan
    )
    
    # 第四步：结果解释
    interpretation = analyzer.execute_result_interpretation(
        quantitative_results, theoretical_analysis
    )
    
    # 生成报告
    report = analyzer.generate_analysis_report("integrated_analysis_report.md")
    
    print("✅ msQCA集成分析完成！")
    print(f"分析阶段: {analyzer.analysis_state['phase']}")
    print("详细报告已生成，请查看各阶段的提示词指导进行深度分析。")


if __name__ == "__main__":
    main()