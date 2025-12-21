#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双重差分法(DID)估计器 - 核心计量经济学算法
提供多种DID估计方法，包括双向固定效应、合成控制、异质性分析等
"""

import pandas as pd
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from scipy import stats
import warnings
from typing import Dict, List, Tuple, Optional, Union
import matplotlib.pyplot as plt
import seaborn as sns


class DIDEstimator:
    """DID估计器类 - 实现多种DID估计方法"""
    
    def __init__(self):
        self.estimated_models = {}
        self.estimation_results = {}
        self.diagnostics = {}
        
    def estimate_twoway_fe(self,
                          data: pd.DataFrame,
                          entity_col: str,
                          time_col: str,
                          treatment_col: str,
                          outcome_col: str,
                          control_vars: List[str] = None,
                          cluster_se: str = None) -> Dict:
        """
        估计双向固定效应DID模型
        
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
        cluster_se : str
            聚类标准误的聚类变量
            
        Returns:
        --------
        Dict
            估计结果和诊断信息
        """
        # 构建处理效应交互项
        data['treat'] = data[treatment_col]
        data['post'] = (data[time_col] >= data[time_col].median()).astype(int)
        data['did'] = data['treat'] * data['post']
        
        # 构建回归公式
        formula_parts = [f"{outcome_col} ~ did"]
        
        if control_vars:
            formula_parts.append(" + " + " + ".join(control_vars))
        
        formula = formula_parts[0] + "".join(formula_parts[1:])
        
        # 估计模型
        if cluster_se:
            # 使用聚类标准误
            model = smf.ols(formula, data=data).fit(cov_type='cluster', 
                                                   cov_kwds={'groups': data[cluster_se]})
        else:
            model = smf.ols(formula, data=data).fit()
        
        # 提取DID效应
        did_effect = model.params['did']
        did_se = model.bse['did']
        did_pvalue = model.pvalues['did']
        did_ci = model.conf_int().loc['did']
        
        # 计算R方
        r_squared = model.rsquared
        adj_r_squared = model.rsquared_adj
        
        # F检验
        f_statistic = model.fvalue
        f_pvalue = model.f_pvalue
        
        results = {
            'model_type': 'twoway_fe',
            'did_effect': did_effect,
            'did_se': did_se,
            'did_pvalue': did_pvalue,
            'did_ci_lower': did_ci[0],
            'did_ci_upper': did_ci[1],
            'r_squared': r_squared,
            'adj_r_squared': adj_r_squared,
            'f_statistic': f_statistic,
            'f_pvalue': f_pvalue,
            'n_obs': len(data),
            'summary': model.summary(),
            'fitted_values': model.fittedvalues,
            'residuals': model.resid
        }
        
        # 保存结果
        self.estimated_models['twoway_fe'] = model
        self.estimation_results['twoway_fe'] = results
        
        return results
    
    def estimate_event_study(self,
                           data: pd.DataFrame,
                           entity_col: str,
                           time_col: str,
                           treatment_col: str,
                           outcome_col: str,
                           control_vars: List[str] = None,
                           reference_period: int = -1) -> Dict:
        """
        估计事件研究DID模型（动态效应）
        
        Parameters:
        -----------
        reference_period : int
            参考时期（通常设为处理前一期）
        """
        # 创建事件时间变量
        data_sorted = data.sort_values([entity_col, time_col])
        
        # 为每个实体确定处理时间
        treatment_time = data_sorted[data_sorted[treatment_col] == 1].groupby(entity_col)[time_col].min()
        
        # 创建事件时间变量，处理缺失值
        def calculate_event_time(row):
            entity_treatment_time = treatment_time.get(row[entity_col])
            if pd.isna(entity_treatment_time):
                return np.nan
            return row[time_col] - entity_treatment_time
        
        data['event_time'] = data.apply(calculate_event_time, axis=1)
        
        # 创建事件时间虚拟变量
        event_times = sorted(data['event_time'].dropna().unique())
        event_times = [t for t in event_times if t != reference_period]
        
        for t in event_times:
            # 清理列名，避免特殊字符
            clean_t = str(t).replace('-', 'minus').replace('+', 'plus')
            data[f'event_{clean_t}'] = (data['event_time'] == t).astype(int)
        
        # 构建回归公式
        event_dummies = []
        for t in event_times:
            clean_t = str(t).replace('-', 'minus').replace('+', 'plus')
            event_dummies.append(f'event_{clean_t}')
        formula_parts = [f"{outcome_col} ~ " + " + ".join(event_dummies)]
        
        if control_vars:
            formula_parts.append(" + " + " + ".join(control_vars))
        
        formula = formula_parts[0] + "".join(formula_parts[1:])
        
        # 估计模型
        model = smf.ols(formula, data=data).fit()
        
        # 提取动态效应
        dynamic_effects = {}
        for t in event_times:
            clean_t = str(t).replace('-', 'minus').replace('+', 'plus')
            col_name = f'event_{clean_t}'
            if col_name in model.params:
                dynamic_effects[t] = {
                    'effect': model.params[col_name],
                    'se': model.bse[col_name],
                    'pvalue': model.pvalues[col_name],
                    'ci_lower': model.conf_int().loc[col_name, 0],
                    'ci_upper': model.conf_int().loc[col_name, 1]
                }
        
        results = {
            'model_type': 'event_study',
            'dynamic_effects': dynamic_effects,
            'event_times': event_times,
            'reference_period': reference_period,
            'r_squared': model.rsquared,
            'n_obs': len(data),
            'summary': model.summary()
        }
        
        self.estimated_models['event_study'] = model
        self.estimation_results['event_study'] = results
        
        return results
    
    def estimate_synthetic_control(self,
                                 data: pd.DataFrame,
                                 entity_col: str,
                                 time_col: str,
                                 treatment_col: str,
                                 outcome_col: str,
                                 treated_entity: str,
                                 pre_period_end: int) -> Dict:
        """
        估计合成控制DID模型
        
        Parameters:
        -----------
        treated_entity : str
            处理组实体的标识
        pre_period_end : int
            处理前时期的结束时间
        """
        # 分离处理组和控制组
        treated_data = data[data[entity_col] == treated_entity].copy()
        control_data = data[data[entity_col] != treated_entity].copy()
        
        # 预处理时期数据
        pre_treated = treated_data[treated_data[time_col] <= pre_period_end]
        pre_control = control_data[control_data[time_col] <= pre_period_end]
        
        # 构建合成控制权重
        # 这里简化处理，实际应用中需要更复杂的优化算法
        control_entities = control_data[entity_col].unique()
        n_controls = len(control_entities)
        
        # 简单平均权重（实际应该使用优化算法）
        weights = np.ones(n_controls) / n_controls
        
        # 构建合成控制组
        synthetic_control = []
        for t in treated_data[time_col].unique():
            if t <= pre_period_end:
                # 处理前期使用历史数据
                control_avg = pre_control[pre_control[time_col] == t][outcome_col].mean()
            else:
                # 处理期使用控制组数据
                current_control = control_data[control_data[time_col] == t]
                control_avg = current_control[outcome_col].mean()
            
            synthetic_control.append(control_avg)
        
        synthetic_control = pd.Series(synthetic_control, index=treated_data[time_col].values)
        
        # 计算处理效应
        actual_outcome = treated_data.set_index(time_col)[outcome_col]
        treatment_effect = actual_outcome - synthetic_control
        
        # 预处理期拟合优度
        pre_period_fit = pre_treated.set_index(time_col)[outcome_col] - synthetic_control[synthetic_control.index <= pre_period_end]
        rmspe = np.sqrt(np.mean(pre_period_fit**2))
        
        results = {
            'model_type': 'synthetic_control',
            'treated_entity': treated_entity,
            'weights': dict(zip(control_entities, weights)),
            'synthetic_control': synthetic_control,
            'actual_outcome': actual_outcome,
            'treatment_effect': treatment_effect,
            'pre_period_rmspe': rmspe,
            'pre_period_end': pre_period_end
        }
        
        self.estimation_results['synthetic_control'] = results
        
        return results
    
    def estimate_heterogeneous_effects(self,
                                     data: pd.DataFrame,
                                     entity_col: str,
                                     time_col: str,
                                     treatment_col: str,
                                     outcome_col: str,
                                     heterogeneity_vars: List[str],
                                     control_vars: List[str] = None) -> Dict:
        """
        估计异质性处理效应
        
        Parameters:
        -----------
        heterogeneity_vars : List[str]
            异质性分析变量列表
        """
        results = {}
        
        # 基础DID估计
        base_results = self.estimate_twoway_fe(
            data, entity_col, time_col, treatment_col, outcome_col, control_vars
        )
        
        # 对每个异质性变量进行分析
        for var in heterogeneity_vars:
            if var not in data.columns:
                continue
                
            # 创建三重交互项
            data['het_var'] = data[var]
            data['did_het'] = data['did'] * data['het_var']
            
            # 构建回归公式
            formula_parts = [f"{outcome_col} ~ did + het_var + did_het"]
            
            if control_vars:
                formula_parts.append(" + " + " + ".join(control_vars))
            
            formula = formula_parts[0] + "".join(formula_parts[1:])
            
            # 估计模型
            model = smf.ols(formula, data=data).fit()
            
            # 提取异质性效应
            het_effect = model.params['did_het']
            het_se = model.bse['did_het']
            het_pvalue = model.pvalues['did_het']
            het_ci = model.conf_int().loc['did_het']
            
            # 计算不同组的效应
            var_categories = data[var].unique()
            group_effects = {}
            
            for cat in var_categories:
                group_data = data[data[var] == cat]
                if len(group_data) > 10:  # 确保有足够样本
                    group_result = self.estimate_twoway_fe(
                        group_data, entity_col, time_col, treatment_col, outcome_col, control_vars
                    )
                    group_effects[cat] = group_result['did_effect']
            
            results[var] = {
                'interaction_effect': het_effect,
                'interaction_se': het_se,
                'interaction_pvalue': het_pvalue,
                'interaction_ci_lower': het_ci[0],
                'interaction_ci_upper': het_ci[1],
                'group_effects': group_effects,
                'n_categories': len(var_categories),
                'summary': model.summary()
            }
        
        self.estimation_results['heterogeneous_effects'] = results
        
        return results
    
    def calculate_placebo_tests(self,
                              data: pd.DataFrame,
                              entity_col: str,
                              time_col: str,
                              treatment_col: str,
                              outcome_col: str,
                              control_vars: List[str] = None,
                              n_placebo: int = 50) -> Dict:
        """
        进行安慰剂检验
        
        Parameters:
        -----------
        n_placebo : int
            安慰剂检验次数
        """
        np.random.seed(42)  # 确保可重复性
        
        # 获取真实处理效应
        true_results = self.estimate_twoway_fe(
            data, entity_col, time_col, treatment_col, outcome_col, control_vars
        )
        true_effect = true_results['did_effect']
        
        # 进行安慰剂检验
        placebo_effects = []
        placebo_pvalues = []
        
        entities = data[entity_col].unique()
        treated_entities = data[data[treatment_col] == 1][entity_col].unique()
        control_entities = [e for e in entities if e not in treated_entities]
        
        for i in range(min(n_placebo, len(control_entities))):
            # 随机选择安慰剂处理组
            placebo_entity = np.random.choice(control_entities)
            
            # 创建安慰剂处理变量
            data_placebo = data.copy()
            data_placebo['placebo_treat'] = (data_placebo[entity_col] == placebo_entity).astype(int)
            
            # 获取安慰剂实体的真实处理时间
            if len(data[data[treatment_col] == 1]) > 0:
                true_treatment_time = data[data[treatment_col] == 1][time_col].min()
                data_placebo['placebo_post'] = (data_placebo[time_col] >= true_treatment_time).astype(int)
                data_placebo['placebo_did'] = data_placebo['placebo_treat'] * data_placebo['placebo_post']
                
                # 估计安慰剂效应
                try:
                    formula_parts = [f"{outcome_col} ~ placebo_did"]
                    if control_vars:
                        formula_parts.append(" + " + " + ".join(control_vars))
                    formula = formula_parts[0] + "".join(formula_parts[1:])
                    
                    model = smf.ols(formula, data=data_placebo).fit()
                    
                    if 'placebo_did' in model.params:
                        placebo_effect = model.params['placebo_did']
                        placebo_pvalue = model.pvalues['placebo_did']
                        
                        placebo_effects.append(placebo_effect)
                        placebo_pvalues.append(placebo_pvalue)
                except:
                    continue
        
        # 计算p值
        placebo_effects = np.array(placebo_effects)
        p_value_two_sided = np.mean(np.abs(placebo_effects) >= np.abs(true_effect))
        p_value_one_sided = np.mean(placebo_effects >= true_effect)
        
        results = {
            'true_effect': true_effect,
            'placebo_effects': placebo_effects,
            'n_placebo': len(placebo_effects),
            'p_value_two_sided': p_value_two_sided,
            'p_value_one_sided': p_value_one_sided,
            'placebo_mean': np.mean(placebo_effects),
            'placebo_std': np.std(placebo_effects)
        }
        
        self.estimation_results['placebo_tests'] = results
        
        return results
    
    def generate_summary_report(self) -> str:
        """生成DID估计摘要报告"""
        report = []
        report.append("# DID估计结果摘要\n")
        
        for model_name, results in self.estimation_results.items():
            report.append(f"## {model_name.replace('_', ' ').title()}\n")
            
            if model_name == 'twoway_fe':
                report.append(f"- DID效应: {results['did_effect']:.4f}")
                report.append(f"- 标准误: {results['did_se']:.4f}")
                report.append(f"- p值: {results['did_pvalue']:.4f}")
                report.append(f"- 95%置信区间: [{results['did_ci_lower']:.4f}, {results['did_ci_upper']:.4f}]")
                report.append(f"- R²: {results['r_squared']:.4f}")
                
            elif model_name == 'event_study':
                report.append("### 动态效应:\n")
                for time_point, effect in results['dynamic_effects'].items():
                    report.append(f"- 时期{time_point}: {effect['effect']:.4f} (p={effect['pvalue']:.4f})")
                    
            elif model_name == 'synthetic_control':
                report.append(f"- 处理实体: {results['treated_entity']}")
                report.append(f"- 预处理期RMSPE: {results['pre_period_rmspe']:.4f}")
                
            elif model_name == 'heterogeneous_effects':
                report.append("### 异质性效应:\n")
                for var, effect in results.items():
                    report.append(f"- {var}: 交互效应={effect['interaction_effect']:.4f} (p={effect['interaction_pvalue']:.4f})")
                    
            elif model_name == 'placebo_tests':
                report.append(f"- 真实效应: {results['true_effect']:.4f}")
                report.append(f"- 安慰剂检验p值(双侧): {results['p_value_two_sided']:.4f}")
            
            report.append("")
        
        return "\n".join(report)


def main():
    """示例用法"""
    # 创建示例面板数据
    np.random.seed(42)
    n_entities = 50
    n_periods = 10
    entities = [f"entity_{i}" for i in range(n_entities)]
    periods = list(range(2010, 2010 + n_periods))
    
    data = []
    for entity in entities:
        for period in periods:
            # 生成基础特征
            base_outcome = 100 + np.random.normal(0, 10)
            
            # 处理效应
            treat = 0
            if entity in ['entity_1', 'entity_2', 'entity_3'] and period >= 2015:
                treat = 1
                base_outcome += 20  # 处理效应
            
            # 个体固定效应
            entity_fe = np.random.normal(0, 5)
            
            # 时间固定效应
            time_fe = (period - 2010) * 2
            
            outcome = base_outcome + entity_fe + time_fe + np.random.normal(0, 5)
            
            data.append({
                'entity': entity,
                'year': period,
                'treatment': treat,
                'outcome': outcome,
                'control_var1': np.random.normal(0, 1),
                'control_var2': np.random.normal(0, 1)
            })
    
    df = pd.DataFrame(data)
    
    # 初始化DID估计器
    estimator = DIDEstimator()
    
    # 估计双向固定效应模型
    print("估计双向固定效应DID模型...")
    twoway_results = estimator.estimate_twoway_fe(
        df, 'entity', 'year', 'treatment', 'outcome', 
        control_vars=['control_var1', 'control_var2']
    )
    
    # 估计事件研究模型
    print("\n估计事件研究模型...")
    event_results = estimator.estimate_event_study(
        df, 'entity', 'year', 'treatment', 'outcome',
        control_vars=['control_var1', 'control_var2']
    )
    
    # 估计异质性效应
    print("\n估计异质性效应...")
    df['heterogeneity_var'] = np.random.choice([0, 1], len(df))
    het_results = estimator.estimate_heterogeneous_effects(
        df, 'entity', 'year', 'treatment', 'outcome',
        heterogeneity_vars=['heterogeneity_var'],
        control_vars=['control_var1', 'control_var2']
    )
    
    # 进行安慰剂检验
    print("\n进行安慰剂检验...")
    placebo_results = estimator.calculate_placebo_tests(
        df, 'entity', 'year', 'treatment', 'outcome',
        control_vars=['control_var1', 'control_var2'],
        n_placebo=20
    )
    
    # 生成摘要报告
    print("\n=== DID估计摘要报告 ===")
    summary = estimator.generate_summary_report()
    print(summary)


if __name__ == "__main__":
    main()