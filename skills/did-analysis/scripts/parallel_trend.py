#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
平行趋势检验模块 - 检验DID的核心假设
提供多种平行趋势检验方法和可视化分析
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from typing import Dict, List, Tuple, Optional, Union
import warnings


class ParallelTrendTester:
    """平行趋势检验器类"""
    
    def __init__(self):
        self.test_results = {}
        self.visualizations = {}
        
    def test_parallel_trend(self,
                           data: pd.DataFrame,
                           entity_col: str,
                           time_col: str,
                           treatment_col: str,
                           outcome_col: str,
                           control_vars: List[str] = None,
                           pre_periods: int = None) -> Dict:
        """
        综合平行趋势检验
        
        Parameters:
        -----------
        data : pd.DataFrame
            面板数据
        entity_col : str
            个体标识列名
        time_col : str
            时间标识列名
        treatment_col : str
            处理变量列名
        outcome_col : str
            结果变量列名
        control_vars : List[str]
            控制变量列表
        pre_periods : int
            处理前期数限制
            
        Returns:
        --------
        Dict
            平行趋势检验结果
        """
        results = {}
        
        # 1. 图形检验
        results['visual_test'] = self.visual_trend_test(
            data, entity_col, time_col, treatment_col, outcome_col
        )
        
        # 2. 统计检验
        results['statistical_test'] = self.statistical_trend_test(
            data, entity_col, time_col, treatment_col, outcome_col, control_vars
        )
        
        # 3. 事件研究检验
        results['event_study_test'] = self.event_study_trend_test(
            data, entity_col, time_col, treatment_col, outcome_col, control_vars, pre_periods
        )
        
        # 4. 预处理效应检验
        results['pre_treatment_test'] = self.pre_treatment_effects_test(
            data, entity_col, time_col, treatment_col, outcome_col, control_vars
        )
        
        # 5. 综合评估
        results['overall_assessment'] = self.assess_parallel_trend_validity(results)
        
        self.test_results = results
        return results
    
    def visual_trend_test(self,
                         data: pd.DataFrame,
                         entity_col: str,
                         time_col: str,
                         treatment_col: str,
                         outcome_col: str) -> Dict:
        """
        图形趋势检验
        """
        # 分离处理组和对照组
        treated_data = data[data[treatment_col] == 1]
        control_data = data[data[treatment_col] == 0]
        
        # 计算各时期的均值
        treated_trends = treated_data.groupby(time_col)[outcome_col].mean()
        control_trends = control_data.groupby(time_col)[outcome_col].mean()
        
        # 计算标准误差
        treated_se = treated_data.groupby(time_col)[outcome_col].sem()
        control_se = control_data.groupby(time_col)[outcome_col].sem()
        
        # 创建图形
        plt.figure(figsize=(12, 6))
        
        # 绘制趋势线
        plt.plot(treated_trends.index, treated_trends.values, 'b-', label='处理组', linewidth=2)
        plt.plot(control_trends.index, control_trends.values, 'r-', label='对照组', linewidth=2)
        
        # 添加置信区间
        plt.fill_between(treated_trends.index, 
                        treated_trends.values - 1.96*treated_se,
                        treated_trends.values + 1.96*treated_se, 
                        alpha=0.2, color='blue')
        plt.fill_between(control_trends.index,
                        control_trends.values - 1.96*control_se,
                        control_trends.values + 1.96*control_se,
                        alpha=0.2, color='red')
        
        plt.xlabel('时间')
        plt.ylabel(f'{outcome_col} 均值')
        plt.title('平行趋势检验：处理组与对照组趋势对比')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # 保存图形
        plt.tight_layout()
        plt.savefig('parallel_trend_test.png', dpi=300, bbox_inches='tight')
        plt.close()
        
        return {
            'treated_trends': treated_trends.to_dict(),
            'control_trends': control_trends.to_dict(),
            'treated_se': treated_se.to_dict(),
            'control_se': control_se.to_dict(),
            'plot_saved': True
        }
    
    def statistical_trend_test(self,
                              data: pd.DataFrame,
                              entity_col: str,
                              time_col: str,
                              treatment_col: str,
                              outcome_col: str,
                              control_vars: List[str] = None) -> Dict:
        """
        统计趋势检验 - 检验处理组和对照组趋势差异的显著性
        """
        # 获取处理前的数据
        treatment_time = data[data[treatment_col] == 1][time_col].min()
        pre_data = data[data[time_col] < treatment_time].copy()
        
        if len(pre_data) == 0:
            return {'error': '没有处理前数据'}
        
        # 创建时间趋势变量
        pre_data = pre_data.sort_values([entity_col, time_col])
        pre_data['time_trend'] = pre_data.groupby(entity_col).cumcount()
        
        # 构建回归公式
        formula_parts = [f"{outcome_col} ~ time_trend * {treatment_col}"]
        
        if control_vars:
            formula_parts.append(" + " + " + ".join(control_vars))
        
        formula = formula_parts[0] + "".join(formula_parts[1:])
        
        # 估计模型
        try:
            model = smf.ols(formula, data=pre_data).fit()
            
            # 提取交互项系数
            interaction_term = f"time_trend:{treatment_col}"
            if interaction_term in model.params:
                interaction_coef = model.params[interaction_term]
                interaction_se = model.bse[interaction_term]
                interaction_pvalue = model.pvalues[interaction_term]
                
                # 计算F检验
                f_test = model.f_test(f"{interaction_term} = 0")
                
                return {
                    'interaction_coefficient': interaction_coef,
                    'interaction_se': interaction_se,
                    'interaction_pvalue': interaction_pvalue,
                    'f_statistic': f_test.fvalue,
                    'f_pvalue': f_test.pvalue,
                    'parallel_trend_assumed': interaction_pvalue > 0.05,
                    'model_summary': model.summary()
                }
            else:
                return {'error': '交互项不存在'}
                
        except Exception as e:
            return {'error': f'模型估计失败: {str(e)}'}
    
    def event_study_trend_test(self,
                              data: pd.DataFrame,
                              entity_col: str,
                              time_col: str,
                              treatment_col: str,
                              outcome_col: str,
                              control_vars: List[str] = None,
                              pre_periods: int = None) -> Dict:
        """
        事件研究趋势检验
        """
        # 确定处理时间
        treatment_time = data[data[treatment_col] == 1][time_col].min()
        
        # 创建相对时间变量
        data['relative_time'] = data[time_col] - treatment_time
        
        # 限制到处理前时期
        if pre_periods:
            pre_data = data[data['relative_time'] < 0]
            pre_data = pre_data[data['relative_time'] >= -pre_periods]
        else:
            pre_data = data[data['relative_time'] < 0]
        
        if len(pre_data) == 0:
            return {'error': '没有足够的处理前数据'}
        
        # 创建时期虚拟变量
        relative_times = sorted(pre_data['relative_time'].unique())
        reference_time = -1  # 以处理前一期为参考
        
        for t in relative_times:
            if t != reference_time:
                clean_t = str(t).replace('-', 'minus')
                pre_data[f'lead_{clean_t}'] = (pre_data['relative_time'] == t).astype(int)
        
        # 构建回归公式
        lead_vars = []
        for t in relative_times:
            if t != reference_time:
                clean_t = str(t).replace('-', 'minus')
                lead_vars.append(f'lead_{clean_t}')
        
        formula_parts = [f"{outcome_col} ~ " + " + ".join(lead_vars)]
        
        if control_vars:
            formula_parts.append(" + " + " + ".join(control_vars))
        
        formula = formula_parts[0] + "".join(formula_parts[1:])
        
        # 估计模型
        try:
            model = smf.ols(formula, data=pre_data).fit()
            
            # 提取前置效应
            lead_effects = {}
            for t in relative_times:
                if t != reference_time:
                    clean_t = str(t).replace('-', 'minus')
                    col_name = f'lead_{clean_t}'
                    if col_name in model.params:
                        lead_effects[t] = {
                            'coefficient': model.params[col_name],
                            'se': model.bse[col_name],
                            'pvalue': model.pvalues[col_name]
                        }
            
            # 联合检验所有前置效应是否为0
            if lead_effects:
                lead_vars_test = [f'lead_{str(t).replace("-", "minus")}' for t in lead_effects.keys()]
                if lead_vars_test:
                    f_test = model.f_test(" = 0".join(lead_vars_test))
                    
                    return {
                        'lead_effects': lead_effects,
                        'joint_f_statistic': f_test.fvalue,
                        'joint_pvalue': f_test.pvalue,
                        'parallel_trend_supported': f_test.pvalue > 0.05,
                        'reference_period': reference_time,
                        'model_summary': model.summary()
                    }
            
            return {'error': '无法计算前置效应'}
            
        except Exception as e:
            return {'error': f'事件研究模型估计失败: {str(e)}'}
    
    def pre_treatment_effects_test(self,
                                  data: pd.DataFrame,
                                  entity_col: str,
                                  time_col: str,
                                  treatment_col: str,
                                  outcome_col: str,
                                  control_vars: List[str] = None) -> Dict:
        """
        预处理效应检验 - 检验是否存在预期效应
        """
        # 确定处理时间
        treatment_time = data[data[treatment_col] == 1][time_col].min()
        
        # 创建处理前虚拟变量
        data['pre_treatment'] = (data[time_col] < treatment_time).astype(int)
        
        # 创建交互项
        data['treatment_pre'] = data[treatment_col] * data['pre_treatment']
        
        # 构建回归公式
        formula_parts = [f"{outcome_col} ~ {treatment_col} + pre_treatment + treatment_pre"]
        
        if control_vars:
            formula_parts.append(" + " + " + ".join(control_vars))
        
        formula = formula_parts[0] + "".join(formula_parts[1:])
        
        # 估计模型
        try:
            model = smf.ols(formula, data=data).fit()
            
            # 检验预处理交互项
            if 'treatment_pre' in model.params:
                pre_coef = model.params['treatment_pre']
                pre_se = model.bse['treatment_pre']
                pre_pvalue = model.pvalues['treatment_pre']
                
                return {
                    'pre_treatment_coefficient': pre_coef,
                    'pre_treatment_se': pre_se,
                    'pre_treatment_pvalue': pre_pvalue,
                    'no_anticipation_effect': pre_pvalue > 0.05,
                    'interpretation': '无预期效应' if pre_pvalue > 0.05 else '存在预期效应',
                    'model_summary': model.summary()
                }
            else:
                return {'error': '预处理交互项不存在'}
                
        except Exception as e:
            return {'error': f'预处理效应检验失败: {str(e)}'}
    
    def assess_parallel_trend_validity(self, test_results: Dict) -> Dict:
        """
        综合评估平行趋势假设的有效性
        """
        assessment = {
            'overall_validity': 'unknown',
            'evidence_summary': {},
            'confidence_level': 'low',
            'recommendations': []
        }
        
        evidence_count = 0
        supporting_evidence = 0
        
        # 检查统计检验
        if 'statistical_test' in test_results and 'parallel_trend_assumed' in test_results['statistical_test']:
            evidence_count += 1
            if test_results['statistical_test']['parallel_trend_assumed']:
                supporting_evidence += 1
            assessment['evidence_summary']['statistical_test'] = test_results['statistical_test']['parallel_trend_assumed']
        
        # 检查事件研究检验
        if 'event_study_test' in test_results and 'parallel_trend_supported' in test_results['event_study_test']:
            evidence_count += 1
            if test_results['event_study_test']['parallel_trend_supported']:
                supporting_evidence += 1
            assessment['evidence_summary']['event_study'] = test_results['event_study_test']['parallel_trend_supported']
        
        # 检查预处理效应检验
        if 'pre_treatment_test' in test_results and 'no_anticipation_effect' in test_results['pre_treatment_test']:
            evidence_count += 1
            if test_results['pre_treatment_test']['no_anticipation_effect']:
                supporting_evidence += 1
            assessment['evidence_summary']['no_anticipation'] = test_results['pre_treatment_test']['no_anticipation_effect']
        
        # 计算总体有效性
        if evidence_count > 0:
            support_ratio = supporting_evidence / evidence_count
            
            if support_ratio >= 0.75:
                assessment['overall_validity'] = 'strongly_supported'
                assessment['confidence_level'] = 'high'
            elif support_ratio >= 0.5:
                assessment['overall_validity'] = 'moderately_supported'
                assessment['confidence_level'] = 'medium'
            else:
                assessment['overall_validity'] = 'weakly_supported'
                assessment['confidence_level'] = 'low'
        
        # 生成建议
        if assessment['overall_validity'] in ['strongly_supported', 'moderately_supported']:
            assessment['recommendations'].append('平行趋势假设得到支持，可以继续DID分析')
        else:
            assessment['recommendations'].append('平行趋势假设证据不足，需要谨慎解释DID结果')
            assessment['recommendations'].append('考虑使用其他因果推断方法或重新设计实验')
        
        if evidence_count < 3:
            assessment['recommendations'].append('建议进行更多的平行趋势检验以增强结论可靠性')
        
        return assessment


def main():
    """示例用法"""
    # 创建示例数据
    np.random.seed(42)
    n_entities = 20
    n_periods = 8
    entities = [f"entity_{i}" for i in range(n_entities)]
    periods = list(range(2015, 2015 + n_periods))
    
    data = []
    for entity in entities:
        base_outcome = 100 + np.random.normal(0, 10)
        entity_trend = np.random.normal(0, 2)
        
        for period in periods:
            time_trend = (period - 2015) * 1.5
            treat = 1 if entity in ['entity_1', 'entity_2', 'entity_3'] and period >= 2018 else 0
            
            # 平行趋势：处理组和对照组有相同的时间趋势
            outcome = base_outcome + entity_trend + time_trend + np.random.normal(0, 5)
            
            # 处理效应（只在处理后）
            if treat == 1:
                outcome += 15
            
            data.append({
                'entity': entity,
                'year': period,
                'treatment': treat,
                'outcome': outcome
            })
    
    df = pd.DataFrame(data)
    
    # 初始化检验器
    tester = ParallelTrendTester()
    
    # 执行平行趋势检验
    print("执行平行趋势检验...")
    results = tester.test_parallel_trend(
        df, 'entity', 'year', 'treatment', 'outcome'
    )
    
    # 输出结果
    print("\n=== 平行趋势检验结果 ===")
    
    if 'statistical_test' in results:
        stat_test = results['statistical_test']
        if 'parallel_trend_assumed' in stat_test:
            print(f"统计检验: 平行趋势假设{'成立' if stat_test['parallel_trend_assumed'] else '不成立'} (p={stat_test.get('interaction_pvalue', 'N/A')})")
    
    if 'event_study_test' in results:
        event_test = results['event_study_test']
        if 'parallel_trend_supported' in event_test:
            print(f"事件研究检验: 平行趋势{'得到支持' if event_test['parallel_trend_supported'] else '未得到支持'} (p={event_test.get('joint_pvalue', 'N/A')})")
    
    if 'pre_treatment_test' in results:
        pre_test = results['pre_treatment_test']
        if 'no_anticipation_effect' in pre_test:
            print(f"预处理效应检验: {'无预期效应' if pre_test['no_anticipation_effect'] else '存在预期效应'} (p={pre_test.get('pre_treatment_pvalue', 'N/A')})")
    
    if 'overall_assessment' in results:
        overall = results['overall_assessment']
        print(f"\n总体评估: {overall['overall_validity']}")
        print(f"置信水平: {overall['confidence_level']}")
        print("建议:")
        for rec in overall['recommendations']:
            print(f"- {rec}")


if __name__ == "__main__":
    main()