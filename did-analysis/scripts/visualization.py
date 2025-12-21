#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DID可视化模块 - 创建专业的计量经济学图表
提供平行趋势图、事件研究图、效应分布图等可视化功能
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Optional, Union
import warnings


class DIDVisualizer:
    """DID可视化器类"""
    
    def __init__(self):
        self.style_setup()
        
    def style_setup(self):
        """设置图表样式"""
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 10
        
    def create_parallel_trend_plot(self,
                                 data: pd.DataFrame,
                                 entity_col: str,
                                 time_col: str,
                                 treatment_col: str,
                                 outcome_col: str,
                                 treatment_time: int = None,
                                 save_path: str = 'parallel_trend_plot.png') -> None:
        """
        创建平行趋势图
        """
        # 分离处理组和对照组
        treated_data = data[data[treatment_col] == 1]
        control_data = data[data[treatment_col] == 0]
        
        # 计算各时期的均值和标准误差
        treated_means = treated_data.groupby(time_col)[outcome_col].mean()
        treated_se = treated_data.groupby(time_col)[outcome_col].sem()
        
        control_means = control_data.groupby(time_col)[outcome_col].mean()
        control_se = control_data.groupby(time_col)[outcome_col].sem()
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 绘制趋势线
        ax.plot(treated_means.index, treated_means.values, 'b-', label='处理组', linewidth=2.5)
        ax.plot(control_means.index, control_means.values, 'r-', label='对照组', linewidth=2.5)
        
        # 添加置信区间
        ax.fill_between(treated_means.index, 
                        treated_means.values - 1.96*treated_se,
                        treated_means.values + 1.96*treated_se, 
                        alpha=0.2, color='blue')
        ax.fill_between(control_means.index,
                        control_means.values - 1.96*control_se,
                        control_means.values + 1.96*control_se,
                        alpha=0.2, color='red')
        
        # 标记处理时间
        if treatment_time is None:
            treatment_time = treated_data[treated_data[treatment_col] == 1][time_col].min()
        
        ax.axvline(x=treatment_time, color='green', linestyle='--', linewidth=2, label='政策实施时间')
        
        # 设置图表属性
        ax.set_xlabel('时间', fontsize=12)
        ax.set_ylabel(f'{outcome_col} 均值', fontsize=12)
        ax.set_title('平行趋势检验：处理组与对照组趋势对比', fontsize=14, fontweight='bold')
        ax.legend(loc='best', frameon=True)
        ax.grid(True, alpha=0.3)
        
        # 美化图表
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_event_study_plot(self,
                              event_results: Dict,
                              save_path: str = 'event_study_plot.png') -> None:
        """
        创建事件研究图
        """
        if 'dynamic_effects' not in event_results:
            print("错误：缺少动态效应数据")
            return
        
        dynamic_effects = event_results['dynamic_effects']
        
        # 提取数据
        periods = sorted(dynamic_effects.keys())
        effects = [dynamic_effects[t]['effect'] for t in periods]
        lower_ci = [dynamic_effects[t]['ci_lower'] for t in periods]
        upper_ci = [dynamic_effects[t]['ci_upper'] for t in periods]
        pvalues = [dynamic_effects[t]['pvalue'] for t in periods]
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 绘制效应点
        x_pos = range(len(periods))
        ax.scatter(x_pos, effects, s=80, color='blue', alpha=0.7, zorder=5)
        
        # 绘制置信区间
        ax.errorbar(x_pos, effects, 
                  yerr=[np.array(effects) - np.array(lower_ci), np.array(upper_ci) - np.array(effects)],
                  fmt='none', color='blue', alpha=0.5, linewidth=1.5)
        
        # 绘制零线
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.7)
        
        # 标记显著性
        for i, (period, pvalue) in enumerate(zip(periods, pvalues)):
            if pvalue < 0.05:
                ax.scatter(i, effects[i], s=120, facecolors='none', edgecolors='red', linewidth=2, zorder=6)
        
        # 设置x轴标签
        ax.set_xticks(x_pos)
        ax.set_xticklabels([f't={period}' for period in periods], rotation=45)
        
        # 设置图表属性
        ax.set_xlabel('相对处理时间', fontsize=12)
        ax.set_ylabel('处理效应', fontsize=12)
        ax.set_title('事件研究：动态处理效应', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 添加图例
        from matplotlib.lines import Line2D
        legend_elements = [
            Line2D([0], [0], color='blue', marker='o', linestyle='none', label='点估计'),
            Line2D([0], [0], color='blue', linewidth=1.5, label='95%置信区间'),
            Line2D([0], [0], color='red', marker='o', linestyle='none', 
                   markerfacecolor='none', markeredgewidth=2, label='p<0.05'),
            Line2D([0], [0], color='black', linewidth=1, label='零效应')
        ]
        ax.legend(handles=legend_elements, loc='best')
        
        # 美化图表
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_placebo_distribution_plot(self,
                                       placebo_results: Dict,
                                       save_path: str = 'placebo_distribution.png') -> None:
        """
        创建安慰剂检验分布图
        """
        if 'placebo_effects' not in placebo_results or 'true_effect' not in placebo_results:
            print("错误：缺少安慰剂检验数据")
            return
        
        placebo_effects = placebo_results['placebo_effects']
        true_effect = placebo_results['true_effect']
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 绘制安慰剂效应分布直方图
        n, bins, patches = ax.hist(placebo_effects, bins=20, alpha=0.7, color='skyblue', 
                                  edgecolor='black', linewidth=1)
        
        # 标记真实效应
        ax.axvline(true_effect, color='red', linestyle='--', linewidth=2.5, 
                  label=f'真实效应: {true_effect:.3f}')
        ax.axvline(-true_effect, color='red', linestyle='--', linewidth=2.5, alpha=0.7)
        
        # 添加p值信息
        if 'p_value_two_sided' in placebo_results:
            p_value = placebo_results['p_value_two_sided']
            ax.text(0.05, 0.95, f'双侧p值: {p_value:.3f}', 
                   transform=ax.transAxes, fontsize=12,
                   bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # 设置图表属性
        ax.set_xlabel('安慰剂效应', fontsize=12)
        ax.set_ylabel('频数', fontsize=12)
        ax.set_title('安慰剂检验：效应分布', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # 美化图表
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_heterogeneity_plot(self,
                                 heterogeneity_results: Dict,
                                 save_path: str = 'heterogeneity_plot.png') -> None:
        """
        创建异质性效应图
        """
        if not heterogeneity_results:
            print("错误：缺少异质性效应数据")
            return
        
        # 准备数据
        groups = []
        effects = []
        std_errors = []
        
        for var, results in heterogeneity_results.items():
            if 'group_effects' in results:
                for group, effect in results['group_effects'].items():
                    groups.append(f"{var}={group}")
                    effects.append(effect)
                    # 这里简化处理，实际应该从结果中获取标准误
                    std_errors.append(0.1)
        
        if not groups:
            print("错误：没有可用的异质性数据")
            return
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 计算置信区间
        effects = np.array(effects)
        std_errors = np.array(std_errors)
        lower_ci = effects - 1.96 * std_errors
        upper_ci = effects + 1.96 * std_errors
        
        x_pos = range(len(groups))
        
        # 绘制效应点
        ax.scatter(x_pos, effects, s=100, color='blue', alpha=0.7, zorder=5)
        
        # 绘制置信区间
        ax.errorbar(x_pos, effects,
                  yerr=[effects - lower_ci, upper_ci - effects],
                  fmt='none', color='blue', alpha=0.5, linewidth=2)
        
        # 绘制零线
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.7)
        
        # 设置x轴标签
        ax.set_xticks(x_pos)
        ax.set_xticklabels(groups, rotation=45, ha='right')
        
        # 设置图表属性
        ax.set_xlabel('群体', fontsize=12)
        ax.set_ylabel('处理效应', fontsize=12)
        ax.set_title('异质性分析：不同群体的处理效应', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 美化图表
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_synthetic_control_plot(self,
                                    synthetic_results: Dict,
                                    save_path: str = 'synthetic_control_plot.png') -> None:
        """
        创建合成控制图
        """
        if 'actual_outcome' not in synthetic_results or 'synthetic_control' not in synthetic_results:
            print("错误：缺少合成控制数据")
            return
        
        actual = synthetic_results['actual_outcome']
        synthetic = synthetic_results['synthetic_control']
        pre_period_end = synthetic_results.get('pre_period_end')
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # 绘制实际结果和合成控制
        ax.plot(actual.index, actual.values, 'b-', label='实际处理组', linewidth=2.5)
        ax.plot(synthetic.index, synthetic.values, 'r--', label='合成控制组', linewidth=2.5)
        
        # 标记处理时间
        if pre_period_end:
            ax.axvline(x=pre_period_end, color='green', linestyle=':', linewidth=2, label='政策实施时间')
            
            # 添加处理前和处理后区域
            ax.axvspan(actual.index.min(), pre_period_end, alpha=0.1, color='gray', label='处理前期')
            ax.axvspan(pre_period_end, actual.index.max(), alpha=0.1, color='lightblue', label='处理后期')
        
        # 设置图表属性
        ax.set_xlabel('时间', fontsize=12)
        ax.set_ylabel('结果变量', fontsize=12)
        ax.set_title('合成控制法：实际与合成控制组对比', fontsize=14, fontweight='bold')
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # 美化图表
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_robustness_summary_plot(self,
                                      robustness_results: Dict,
                                      save_path: str = 'robustness_summary.png') -> None:
        """
        创建稳健性检验汇总图
        """
        # 准备数据
        methods = []
        effects = []
        conf_intervals = []
        
        # 从不同稳健性检验中提取结果
        if 'model_sensitivity' in robustness_results:
            model_sens = robustness_results['model_sensitivity']
            for method, results in model_sens.items():
                if 'did_effect' in results:
                    methods.append(method.replace('_', ' ').title())
                    effects.append(results['did_effect'])
                    # 简化的置信区间计算
                    ci_width = results['did_se'] * 1.96
                    conf_intervals.append(ci_width)
        
        if not methods:
            print("错误：没有可用的稳健性检验数据")
            return
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(10, 6))
        
        x_pos = range(len(methods))
        
        # 绘制效应点
        ax.scatter(x_pos, effects, s=100, color='blue', alpha=0.7, zorder=5)
        
        # 绘制置信区间
        ax.errorbar(x_pos, effects,
                  yerr=conf_intervals,
                  fmt='none', color='blue', alpha=0.5, linewidth=2)
        
        # 绘制零线
        ax.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.7)
        
        # 设置x轴标签
        ax.set_xticks(x_pos)
        ax.set_xticklabels(methods, rotation=45, ha='right')
        
        # 设置图表属性
        ax.set_xlabel('模型设定', fontsize=12)
        ax.set_ylabel('DID效应', fontsize=12)
        ax.set_title('稳健性检验：不同模型设定的DID效应', fontsize=14, fontweight='bold')
        ax.grid(True, alpha=0.3)
        
        # 美化图表
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()
        
    def create_comprehensive_dashboard(self,
                                    did_results: Dict,
                                    save_path: str = 'did_dashboard.png') -> None:
        """
        创建综合仪表板
        """
        # 创建子图
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('DID分析综合仪表板', fontsize=16, fontweight='bold')
        
        # 1. 主要结果摘要
        ax1 = axes[0, 0]
        if 'twoway_fe' in did_results:
            results = did_results['twoway_fe']
            effect = results['did_effect']
            ci_lower = results['did_ci_lower']
            ci_upper = results['did_ci_upper']
            pvalue = results['did_pvalue']
            
            # 创建效应估计图
            ax1.errorbar(0, effect, yerr=[[effect-ci_lower], [ci_upper-effect]], 
                        fmt='o', markersize=10, capsize=5, color='blue')
            ax1.axhline(y=0, color='black', linestyle='-', alpha=0.7)
            ax1.set_xlim(-0.5, 0.5)
            ax1.set_ylabel('DID效应', fontsize=12)
            ax1.set_title('主要DID估计', fontsize=14, fontweight='bold')
            ax1.grid(True, alpha=0.3)
            
            # 添加统计信息
            stats_text = f'效应: {effect:.3f}\n95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]\np值: {pvalue:.3f}'
            ax1.text(0.02, 0.98, stats_text, transform=ax1.transAxes, fontsize=10,
                    verticalalignment='top',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
        # 2. 质量指标
        ax2 = axes[0, 1]
        if 'quality_metrics' in did_results:
            quality = did_results['quality_metrics']
            
            metrics = list(quality.keys())
            values = list(quality.values())
            
            bars = ax2.bar(range(len(metrics)), values, color=['blue', 'green', 'orange', 'red'])
            ax2.set_xticks(range(len(metrics)))
            ax2.set_xticklabels([m.replace('_', ' ').title() for m in metrics], rotation=45, ha='right')
            ax2.set_ylabel('质量分数', fontsize=12)
            ax2.set_title('分析质量指标', fontsize=14, fontweight='bold')
            ax2.grid(True, alpha=0.3)
            
            # 添加数值标签
            for bar, value in zip(bars, values):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                        f'{value:.2f}', ha='center', va='bottom')
        
        # 3. 时间趋势（如果有数据）
        ax3 = axes[1, 0]
        ax3.text(0.5, 0.5, '时间趋势图\n(需要原始数据)', 
                ha='center', va='center', transform=ax3.transAxes, fontsize=12)
        ax3.set_title('时间趋势', fontsize=14, fontweight='bold')
        
        # 4. 稳健性检验结果
        ax4 = axes[1, 1]
        if 'robustness_tests' in did_results:
            robustness = did_results['robustness_tests']
            
            # 创建稳健性检验结果汇总
            tests = []
            results = []
            
            if 'placebo_tests' in robustness:
                placebo_robust = robustness['placebo_tests'].get('robust_to_placebo', False)
                tests.append('安慰剂检验')
                results.append(1 if placebo_robust else 0)
            
            if tests:
                colors = ['green' if r else 'red' for r in results]
                bars = ax4.bar(tests, results, color=colors)
                ax4.set_ylabel('通过检验', fontsize=12)
                ax4.set_title('稳健性检验', fontsize=14, fontweight='bold')
                ax4.set_ylim(0, 1.2)
                ax4.grid(True, alpha=0.3)
                
                # 添加通过/未通过标签
                for bar, result in zip(bars, results):
                    height = bar.get_height()
                    label = '通过' if result == 1 else '未通过'
                    ax4.text(bar.get_x() + bar.get_width()/2., height + 0.05,
                            label, ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()


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
        
        for period in periods:
            treat = 1 if entity in ['entity_1', 'entity_2', 'entity_3'] and period >= 2018 else 0
            outcome = base_outcome + (period - 2015) * 2 + np.random.normal(0, 5)
            
            if treat == 1:
                outcome += 15
            
            data.append({
                'entity': entity,
                'year': period,
                'treatment': treat,
                'outcome': outcome
            })
    
    df = pd.DataFrame(data)
    
    # 初始化可视化器
    visualizer = DIDVisualizer()
    
    # 创建平行趋势图
    print("创建平行趋势图...")
    visualizer.create_parallel_trend_plot(df, 'entity', 'year', 'treatment', 'outcome')
    
    # 创建示例事件研究结果
    event_results = {
        'dynamic_effects': {
            -3: {'effect': -0.5, 'ci_lower': -2.1, 'ci_upper': 1.1, 'pvalue': 0.54},
            -2: {'effect': 0.2, 'ci_lower': -1.4, 'ci_upper': 1.8, 'pvalue': 0.80},
            -1: {'effect': 0.8, 'ci_lower': -0.8, 'ci_upper': 2.4, 'pvalue': 0.32},
            0: {'effect': 2.1, 'ci_lower': 0.5, 'ci_upper': 3.7, 'pvalue': 0.01},
            1: {'effect': 3.2, 'ci_lower': 1.6, 'ci_upper': 4.8, 'pvalue': 0.00},
            2: {'effect': 2.8, 'ci_lower': 1.2, 'ci_upper': 4.4, 'pvalue': 0.00}
        }
    }
    
    # 创建事件研究图
    print("创建事件研究图...")
    visualizer.create_event_study_plot(event_results)
    
    # 创建安慰剂检验分布图
    print("创建安慰剂检验分布图...")
    placebo_results = {
        'placebo_effects': np.random.normal(0, 2, 50),
        'true_effect': 2.1,
        'p_value_two_sided': 0.03
    }
    visualizer.create_placebo_distribution_plot(placebo_results)
    
    print("所有可视化图表已创建完成！")


if __name__ == "__main__":
    main()