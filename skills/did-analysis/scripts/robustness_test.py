#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
稳健性检验模块 - 确保DID结果的可靠性
提供多种稳健性检验方法，包括安慰剂检验、敏感性分析等
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from typing import Dict, List, Tuple, Optional, Union
import warnings


class RobustnessTester:
    """稳健性检验器类"""
    
    def __init__(self):
        self.test_results = {}
        
    def run_robustness_tests(self,
                           data: pd.DataFrame,
                           entity_col: str,
                           time_col: str,
                           treatment_col: str,
                           outcome_col: str,
                           baseline_results: Dict) -> Dict:
        """
        运行全面的稳健性检验
        
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
        baseline_results : Dict
            基准DID结果
            
        Returns:
        --------
        Dict
            稳健性检验结果
        """
        results = {}
        
        # 1. 安慰剂检验
        results['placebo_tests'] = self.placebo_tests(
            data, entity_col, time_col, treatment_col, outcome_col, baseline_results
        )
        
        # 2. 样本敏感性分析
        results['sample_sensitivity'] = self.sample_sensitivity_analysis(
            data, entity_col, time_col, treatment_col, outcome_col
        )
        
        # 3. 模型设定敏感性分析
        results['model_sensitivity'] = self.model_sensitivity_analysis(
            data, entity_col, time_col, treatment_col, outcome_col
        )
        
        # 4. 时间窗口敏感性分析
        results['time_window_sensitivity'] = self.time_window_sensitivity_analysis(
            data, entity_col, time_col, treatment_col, outcome_col
        )
        
        # 5. 控制变量敏感性分析
        results['control_variable_sensitivity'] = self.control_variable_sensitivity_analysis(
            data, entity_col, time_col, treatment_col, outcome_col
        )
        
        # 6. 综合稳健性评估
        results['overall_robustness'] = self.assess_overall_robustness(
            results, baseline_results
        )
        
        self.test_results = results
        return results
    
    def placebo_tests(self,
                     data: pd.DataFrame,
                     entity_col: str,
                     time_col: str,
                     treatment_col: str,
                     outcome_col: str,
                     baseline_results: Dict,
                     n_placebo: int = 50) -> Dict:
        """
        安慰剂检验
        """
        np.random.seed(42)  # 确保可重复性
        
        # 获取真实处理效应
        true_effect = baseline_results.get('did_effect', 0)
        
        # 获取处理组和对照组
        treated_entities = data[data[treatment_col] == 1][entity_col].unique()
        control_entities = data[data[treatment_col] == 0][entity_col].unique()
        
        placebo_effects = []
        placebo_pvalues = []
        
        # 进行多次安慰剂检验
        for i in range(min(n_placebo, len(control_entities))):
            # 随机选择安慰剂处理组
            placebo_entity = np.random.choice(control_entities)
            
            # 创建安慰剂处理变量
            data_placebo = data.copy()
            data_placebo['placebo_treatment'] = (data_placebo[entity_col] == placebo_entity).astype(int)
            
            # 获取真实处理时间
            if len(data[data[treatment_col] == 1]) > 0:
                true_treatment_time = data[data[treatment_col] == 1][time_col].min()
                data_placebo['placebo_post'] = (data_placebo[time_col] >= true_treatment_time).astype(int)
                data_placebo['placebo_did'] = data_placebo['placebo_treatment'] * data_placebo['placebo_post']
                
                # 估计安慰剂效应
                try:
                    model = smf.ols(f"{outcome_col} ~ placebo_did", data=data_placebo).fit()
                    
                    if 'placebo_did' in model.params:
                        placebo_effect = model.params['placebo_did']
                        placebo_pvalue = model.pvalues['placebo_did']
                        
                        placebo_effects.append(placebo_effect)
                        placebo_pvalues.append(placebo_pvalue)
                except:
                    continue
        
        # 计算p值
        placebo_effects = np.array(placebo_effects)
        if len(placebo_effects) > 0:
            p_value_two_sided = np.mean(np.abs(placebo_effects) >= np.abs(true_effect))
            p_value_one_sided = np.mean(placebo_effects >= true_effect)
            
            # 创建安慰剂检验分布图
            self._create_placebo_distribution_plot(placebo_effects, true_effect)
            
            return {
                'true_effect': true_effect,
                'placebo_effects': placebo_effects,
                'n_placebo': len(placebo_effects),
                'p_value_two_sided': p_value_two_sided,
                'p_value_one_sided': p_value_one_sided,
                'placebo_mean': np.mean(placebo_effects),
                'placebo_std': np.std(placebo_effects),
                'placebo_min': np.min(placebo_effects),
                'placebo_max': np.max(placebo_effects),
                'robust_to_placebo': p_value_two_sided < 0.05
            }
        else:
            return {'error': '无法进行安慰剂检验'}
    
    def sample_sensitivity_analysis(self,
                                  data: pd.DataFrame,
                                  entity_col: str,
                                  time_col: str,
                                  treatment_col: str,
                                  outcome_col: str) -> Dict:
        """
        样本敏感性分析
        """
        results = {}
        
        # 1. 留一法分析
        results['leave_one_out'] = self.leave_one_out_analysis(
            data, entity_col, time_col, treatment_col, outcome_col
        )
        
        # 2. 随机子样本分析
        results['random_subsample'] = self.random_subsample_analysis(
            data, entity_col, time_col, treatment_col, outcome_col
        )
        
        # 3. 时间子期间分析
        results['time_subsample'] = self.time_subsample_analysis(
            data, entity_col, time_col, treatment_col, outcome_col
        )
        
        return results
    
    def leave_one_out_analysis(self,
                             data: pd.DataFrame,
                             entity_col: str,
                             time_col: str,
                             treatment_col: str,
                             outcome_col: str) -> Dict:
        """
        留一法分析
        """
        treated_entities = data[data[treatment_col] == 1][entity_col].unique()
        leave_one_out_effects = []
        
        for entity in treated_entities:
            # 移除一个处理组实体
            data_subset = data[data[entity_col] != entity].copy()
            
            # 重新估计DID
            try:
                data_subset['post'] = (data_subset[time_col] >= data_subset[data_subset[treatment_col] == 1][time_col].min()).astype(int)
                data_subset['did'] = data_subset[treatment_col] * data_subset['post']
                
                model = smf.ols(f"{outcome_col} ~ did", data=data_subset).fit()
                
                if 'did' in model.params:
                    leave_one_out_effects.append(model.params['did'])
            except:
                continue
        
        if len(leave_one_out_effects) > 0:
            return {
                'leave_one_out_effects': leave_one_out_effects,
                'n_observations': len(leave_one_out_effects),
                'mean_effect': np.mean(leave_one_out_effects),
                'std_effect': np.std(leave_one_out_effects),
                'min_effect': np.min(leave_one_out_effects),
                'max_effect': np.max(leave_one_out_effects),
                'coefficient_of_variation': np.std(leave_one_out_effects) / np.abs(np.mean(leave_one_out_effects))
            }
        else:
            return {'error': '留一法分析失败'}
    
    def random_subsample_analysis(self,
                                data: pd.DataFrame,
                                entity_col: str,
                                time_col: str,
                                treatment_col: str,
                                outcome_col: str,
                                n_samples: int = 10,
                                sample_ratio: float = 0.8) -> Dict:
        """
        随机子样本分析
        """
        subsample_effects = []
        
        for i in range(n_samples):
            # 随机抽样
            data_subsample = data.sample(frac=sample_ratio, random_state=i).copy()
            
            # 估计DID
            try:
                data_subsample['post'] = (data_subsample[time_col] >= data_subsample[data_subsample[treatment_col] == 1][time_col].min()).astype(int)
                data_subsample['did'] = data_subsample[treatment_col] * data_subsample['post']
                
                model = smf.ols(f"{outcome_col} ~ did", data=data_subsample).fit()
                
                if 'did' in model.params:
                    subsample_effects.append(model.params['did'])
            except:
                continue
        
        if len(subsample_effects) > 0:
            return {
                'subsample_effects': subsample_effects,
                'n_samples': len(subsample_effects),
                'mean_effect': np.mean(subsample_effects),
                'std_effect': np.std(subsample_effects),
                'min_effect': np.min(subsample_effects),
                'max_effect': np.max(subsample_effects)
            }
        else:
            return {'error': '随机子样本分析失败'}
    
    def time_subsample_analysis(self,
                              data: pd.DataFrame,
                              entity_col: str,
                              time_col: str,
                              treatment_col: str,
                              outcome_col: str) -> Dict:
        """
        时间子期间分析
        """
        time_periods = sorted(data[time_col].unique())
        time_effects = {}
        
        # 分析不同时间窗口的效应
        for start_idx in range(len(time_periods) - 3):
            for end_idx in range(start_idx + 3, len(time_periods)):
                window_start = time_periods[start_idx]
                window_end = time_periods[end_idx]
                
                data_window = data[(data[time_col] >= window_start) & (data[time_col] <= window_end)].copy()
                
                # 确保窗口内有处理组和对照组
                if (len(data_window[data_window[treatment_col] == 1]) > 0 and 
                    len(data_window[data_window[treatment_col] == 0]) > 0):
                    
                    try:
                        data_window['post'] = (data_window[time_col] >= data_window[data_window[treatment_col] == 1][time_col].min()).astype(int)
                        data_window['did'] = data_window[treatment_col] * data_window['post']
                        
                        model = smf.ols(f"{outcome_col} ~ did", data=data_window).fit()
                        
                        if 'did' in model.params:
                            window_key = f"{window_start}-{window_end}"
                            time_effects[window_key] = {
                                'effect': model.params['did'],
                                'se': model.bse['did'],
                                'pvalue': model.pvalues['did'],
                                'n_obs': len(data_window)
                            }
                    except:
                        continue
        
        return {
            'time_window_effects': time_effects,
            'n_windows': len(time_effects)
        }
    
    def model_sensitivity_analysis(self,
                                 data: pd.DataFrame,
                                 entity_col: str,
                                 time_col: str,
                                 treatment_col: str,
                                 outcome_col: str) -> Dict:
        """
        模型设定敏感性分析
        """
        results = {}
        
        # 1. 无控制变量模型
        try:
            data_copy = data.copy()
            data_copy['post'] = (data_copy[time_col] >= data_copy[data_copy[treatment_col] == 1][time_col].min()).astype(int)
            data_copy['did'] = data_copy[treatment_col] * data_copy['post']
            
            model_no_controls = smf.ols(f"{outcome_col} ~ did", data=data_copy).fit()
            results['no_controls'] = {
                'did_effect': model_no_controls.params['did'],
                'did_se': model_no_controls.bse['did'],
                'did_pvalue': model_no_controls.pvalues['did'],
                'r_squared': model_no_controls.rsquared
            }
        except:
            results['no_controls'] = {'error': '无控制变量模型估计失败'}
        
        # 2. 包含个体固定效应模型
        try:
            model_entity_fe = smf.ols(f"{outcome_col} ~ did + C({entity_col})", data=data_copy).fit()
            results['entity_fixed_effects'] = {
                'did_effect': model_entity_fe.params['did'],
                'did_se': model_entity_fe.bse['did'],
                'did_pvalue': model_entity_fe.pvalues['did'],
                'r_squared': model_entity_fe.rsquared
            }
        except:
            results['entity_fixed_effects'] = {'error': '个体固定效应模型估计失败'}
        
        # 3. 包含时间固定效应模型
        try:
            model_time_fe = smf.ols(f"{outcome_col} ~ did + C({time_col})", data=data_copy).fit()
            results['time_fixed_effects'] = {
                'did_effect': model_time_fe.params['did'],
                'did_se': model_time_fe.bse['did'],
                'did_pvalue': model_time_fe.pvalues['did'],
                'r_squared': model_time_fe.rsquared
            }
        except:
            results['time_fixed_effects'] = {'error': '时间固定效应模型估计失败'}
        
        return results
    
    def time_window_sensitivity_analysis(self,
                                      data: pd.DataFrame,
                                      entity_col: str,
                                      time_col: str,
                                      treatment_col: str,
                                      outcome_col: str) -> Dict:
        """
        时间窗口敏感性分析
        """
        treatment_time = data[data[treatment_col] == 1][time_col].min()
        time_periods = sorted(data[time_col].unique())
        
        results = {}
        
        # 测试不同的处理前窗口长度
        pre_window_options = [2, 3, 4, 5] if len([p for p in time_periods if p < treatment_time]) >= 5 else [2, 3]
        
        for pre_window in pre_window_options:
            pre_start = treatment_time - pre_window
            
            data_window = data[data[time_col] >= pre_start].copy()
            
            if len(data_window) > 0:
                try:
                    data_window['post'] = (data_window[time_col] >= treatment_time).astype(int)
                    data_window['did'] = data_window[treatment_col] * data_window['post']
                    
                    model = smf.ols(f"{outcome_col} ~ did", data=data_window).fit()
                    
                    if 'did' in model.params:
                        results[f'pre_window_{pre_window}'] = {
                            'did_effect': model.params['did'],
                            'did_se': model.bse['did'],
                            'did_pvalue': model.pvalues['did'],
                            'n_obs': len(data_window),
                            'window_start': pre_start,
                            'window_end': max(data_window[time_col])
                        }
                except:
                    continue
        
        return results
    
    def control_variable_sensitivity_analysis(self,
                                            data: pd.DataFrame,
                                            entity_col: str,
                                            time_col: str,
                                            treatment_col: str,
                                            outcome_col: str) -> Dict:
        """
        控制变量敏感性分析
        """
        # 识别可能的控制变量（数值型变量）
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        possible_controls = [col for col in numeric_cols if col not in [entity_col, time_col, treatment_col, outcome_col]]
        
        results = {}
        
        # 基准模型（无控制变量）
        data_copy = data.copy()
        data_copy['post'] = (data_copy[time_col] >= data_copy[data_copy[treatment_col] == 1][time_col].min()).astype(int)
        data_copy['did'] = data_copy[treatment_col] * data_copy['post']
        
        try:
            model_baseline = smf.ols(f"{outcome_col} ~ did", data=data_copy).fit()
            baseline_effect = model_baseline.params['did']
            results['baseline'] = {
                'did_effect': baseline_effect,
                'did_se': model_baseline.bse['did'],
                'did_pvalue': model_baseline.pvalues['did']
            }
        except:
            return {'error': '基准模型估计失败'}
        
        # 逐一添加控制变量
        for control_var in possible_controls:
            try:
                formula = f"{outcome_col} ~ did + {control_var}"
                model = smf.ols(formula, data=data_copy).fit()
                
                if 'did' in model.params:
                    results[control_var] = {
                        'did_effect': model.params['did'],
                        'did_se': model.bse['did'],
                        'did_pvalue': model.pvalues['did'],
                        'effect_change': model.params['did'] - baseline_effect,
                        'percent_change': (model.params['did'] - baseline_effect) / abs(baseline_effect) * 100
                    }
            except:
                continue
        
        return results
    
    def assess_overall_robustness(self,
                                robustness_results: Dict,
                                baseline_results: Dict) -> Dict:
        """
        综合稳健性评估
        """
        assessment = {
            'overall_robustness': 'unknown',
            'robustness_scores': {},
            'summary': {},
            'recommendations': []
        }
        
        scores = []
        
        # 评估安慰剂检验
        if 'placebo_tests' in robustness_results and 'robust_to_placebo' in robustness_results['placebo_tests']:
            placebo_robust = robustness_results['placebo_tests']['robust_to_placebo']
            assessment['robustness_scores']['placebo'] = 1.0 if placebo_robust else 0.3
            scores.append(assessment['robustness_scores']['placebo'])
        
        # 评估样本敏感性
        if 'sample_sensitivity' in robustness_results:
            sample_sens = robustness_results['sample_sensitivity']
            
            # 留一法分析
            if 'leave_one_out' in sample_sens and 'coefficient_of_variation' in sample_sens['leave_one_out']:
                cv = sample_sens['leave_one_out']['coefficient_of_variation']
                sample_score = max(0.2, 1.0 - cv)  # CV越小越稳健
                assessment['robustness_scores']['leave_one_out'] = sample_score
                scores.append(sample_score)
        
        # 评估模型设定敏感性
        if 'model_sensitivity' in robustness_results:
            model_sens = robustness_results['model_sensitivity']
            
            # 比较不同模型的效应
            effects = []
            if 'no_controls' in model_sens and 'did_effect' in model_sens['no_controls']:
                effects.append(model_sens['no_controls']['did_effect'])
            
            if 'entity_fixed_effects' in model_sens and 'did_effect' in model_sens['entity_fixed_effects']:
                effects.append(model_sens['entity_fixed_effects']['did_effect'])
            
            if len(effects) > 1:
                effect_std = np.std(effects)
                effect_mean = np.mean(np.abs(effects))
                cv = effect_std / effect_mean if effect_mean > 0 else 1
                model_score = max(0.2, 1.0 - cv)
                assessment['robustness_scores']['model_specification'] = model_score
                scores.append(model_score)
        
        # 计算总体稳健性分数
        if scores:
            overall_score = np.mean(scores)
            
            if overall_score >= 0.8:
                assessment['overall_robustness'] = 'highly_robust'
            elif overall_score >= 0.6:
                assessment['overall_robustness'] = 'moderately_robust'
            elif overall_score >= 0.4:
                assessment['overall_robustness'] = 'somewhat_robust'
            else:
                assessment['overall_robustness'] = 'not_robust'
            
            assessment['summary']['overall_score'] = overall_score
            assessment['summary']['n_tests'] = len(scores)
        
        # 生成建议
        if assessment['overall_robustness'] in ['highly_robust', 'moderately_robust']:
            assessment['recommendations'].append('DID结果具有良好的稳健性，可以较为自信地进行因果推断')
        else:
            assessment['recommendations'].append('DID结果的稳健性不足，需要谨慎解释因果效应')
            assessment['recommendations'].append('建议考虑其他因果推断方法或改进实验设计')
        
        return assessment
    
    def _create_placebo_distribution_plot(self, placebo_effects: np.ndarray, true_effect: float):
        """创建安慰剂检验分布图"""
        plt.figure(figsize=(10, 6))
        
        # 绘制安慰剂效应分布直方图
        plt.hist(placebo_effects, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
        
        # 标记真实效应
        plt.axvline(true_effect, color='red', linestyle='--', linewidth=2, label=f'真实效应: {true_effect:.3f}')
        plt.axvline(-true_effect, color='red', linestyle='--', linewidth=2, alpha=0.7)
        
        plt.xlabel('安慰剂效应')
        plt.ylabel('频数')
        plt.title('安慰剂检验效应分布')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('placebo_test_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()


def main():
    """示例用法"""
    # 创建示例数据
    np.random.seed(42)
    n_entities = 30
    n_periods = 8
    entities = [f"entity_{i}" for i in range(n_entities)]
    periods = list(range(2015, 2015 + n_periods))
    
    data = []
    for entity in entities:
        base_outcome = 100 + np.random.normal(0, 10)
        
        for period in periods:
            treat = 1 if entity in ['entity_1', 'entity_2', 'entity_3'] and period >= 2018 else 0
            outcome = base_outcome + (period - 2015) * 2 + np.random.normal(0, 5)
            
            if treat == 1:
                outcome += 15
            
            data.append({
                'entity': entity,
                'year': period,
                'treatment': treat,
                'outcome': outcome,
                'control_var1': np.random.normal(0, 1),
                'control_var2': np.random.normal(0, 1)
            })
    
    df = pd.DataFrame(data)
    
    # 估计基准DID模型
    df['post'] = (df['year'] >= 2018).astype(int)
    df['did'] = df['treatment'] * df['post']
    
    baseline_model = smf.ols('outcome ~ did', data=df).fit()
    baseline_results = {
        'did_effect': baseline_model.params['did'],
        'did_se': baseline_model.bse['did'],
        'did_pvalue': baseline_model.pvalues['did']
    }
    
    # 初始化稳健性检验器
    tester = RobustnessTester()
    
    # 运行稳健性检验
    print("运行稳健性检验...")
    results = tester.run_robustness_tests(
        df, 'entity', 'year', 'treatment', 'outcome', baseline_results
    )
    
    # 输出结果
    print("\n=== 稳健性检验结果 ===")
    
    if 'placebo_tests' in results:
        placebo = results['placebo_tests']
        if 'robust_to_placebo' in placebo:
            print(f"安慰剂检验: {'通过' if placebo['robust_to_placebo'] else '未通过'} (p={placebo.get('p_value_two_sided', 'N/A')})")
    
    if 'overall_robustness' in results:
        overall = results['overall_robustness']
        print(f"\n总体稳健性: {overall['overall_robustness']}")
        print("建议:")
        for rec in overall['recommendations']:
            print(f"- {rec}")


if __name__ == "__main__":
    main()