#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fsQCA技能测试脚本
验证各个模块的功能
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os

# 添加脚本目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from calibration import FSCCalibration, consistency_xy, coverage_xy
from truth_table import FuzzyTruthTableBuilder
from minimization import FSCMinimizer


def test_calibration():
    """测试校准模块"""
    print("🧪 测试校准模块...")
    
    # 创建测试数据
    np.random.seed(42)
    test_data = pd.Series(np.random.uniform(0, 10, 20), name='test_var')
    
    # 初始化校准器
    calibrator = FSCCalibration()
    
    # 测试不同的校准方法
    methods = ['direct', 'threshold', 'interpolation', 'gaussian', 'sigmoid']
    
    for method in methods:
        try:
            calibrated = calibrator.calibrate_variable(test_data, method=method)
            print(f"  {method}校准: 范围 [{calibrated.min():.3f}, {calibrated.max():.3f}] - ✓")
        except Exception as e:
            print(f"  {method}校准: 失败 - {str(e)}")
    
    print("  校准模块测试完成\n")


def test_truth_table():
    """测试真值表模块"""
    print("🧪 测试真值表模块...")
    
    # 创建测试数据
    np.random.seed(42)
    test_data = pd.DataFrame({
        'A': np.random.uniform(0, 1, 20),
        'B': np.random.uniform(0, 1, 20),
        'C': np.random.uniform(0, 1, 20),
        'outcome': np.random.uniform(0, 1, 20)
    })
    
    # 初始化真值表构建器
    tt_builder = FuzzyTruthTableBuilder()
    
    try:
        # 构建真值表
        truth_table = tt_builder.build_truth_table(
            test_data,
            ['A', 'B', 'C'],
            'outcome'
        )
        
        print(f"  真值表形状: {truth_table.shape}")
        print(f"  矛盾组合数量: {len(tt_builder.contradictory_cases)}")
        print(f"  逻辑余项数量: {len(tt_builder.logical_remainders)}")
        print("  真值表模块测试完成\n")
    except Exception as e:
        print(f"  真值表模块测试失败: {str(e)}\n")


def test_minimization():
    """测试最小化模块"""
    print("🧪 测试最小化模块...")
    
    # 创建模拟真值表数据
    np.random.seed(42)
    
    # 模拟真值表数据
    sample_configs = [
        (1, 0, 1),  # 配置1
        (1, 1, 0),  # 配置2
        (0, 1, 1),  # 配置3
        (1, 1, 1),  # 配置4
    ]
    
    sample_data = []
    for i, config in enumerate(sample_configs):
        sample_data.append({
            'configuration': config,
            'frequency': np.random.randint(1, 5),
            'outcome': np.random.uniform(0.6, 1.0),  # 正面结果
            'consistency': np.random.uniform(0.8, 1.0),
            'cases': [f'case_{i*3+j}' for j in range(np.random.randint(1, 4))],
            'n_cases': np.random.randint(1, 4),
            'inclusion_score': np.random.uniform(0.7, 1.0),
            'PRI_consistency': np.random.uniform(0.75, 1.0),
            'remainder': False,
            'contradictory': False
        })
    
    truth_table = pd.DataFrame(sample_data)
    
    # 添加条件列的平均值
    for i, condition in enumerate(['A', 'B', 'C']):
        truth_table[f'avg_{condition}'] = [config[i] for config in sample_configs]
    
    # 初始化最小化器
    minimizer = FSCMinimizer()
    
    try:
        # 执行最小化
        solutions = minimizer.minimize(truth_table, ['A', 'B', 'C'])
        
        print(f"  生成解的数量: {len(solutions)}")
        for i, solution in enumerate(solutions):
            print(f"    解 {i+1}: {solution.solution_type.value}, 一致性={solution.consistency:.3f}, 覆盖度={solution.coverage:.3f}")
        
        print("  最小化模块测试完成\n")
    except Exception as e:
        print(f"  最小化模块测试失败: {str(e)}\n")


def test_integration():
    """测试模块集成"""
    print("🧪 测试模块集成...")
    
    try:
        # 导入集成分析器
        from integrated_analysis import IntegratedFSCAnalyzer
        
        # 创建示例数据
        np.random.seed(42)
        sample_data = pd.DataFrame({
            'case_id': range(1, 11),
            'A': np.random.uniform(0, 1, 10),
            'B': np.random.uniform(0, 1, 10),
            'C': np.random.uniform(0, 1, 10),
            'Y': np.random.uniform(0, 1, 10)
        })
        
        # 初始化分析器
        skill_root = os.path.dirname(__file__)
        analyzer = IntegratedFSCAnalyzer(skill_root)
        
        # 执行分析流程
        research_context = {
            'research_question': '测试研究问题',
            'theoretical_framework': '测试框架',
            'case_description': '10个测试案例'
        }
        
        # 理论分析
        theoretical_analysis = analyzer.execute_theoretical_analysis(research_context)
        
        # 校准指导
        calibration_plan = analyzer.execute_calibration_guidance(sample_data, theoretical_analysis)
        
        # 定量分析
        conditions = ['A', 'B', 'C']
        outcome = 'Y'
        quantitative_results = analyzer.execute_quantitative_analysis(
            sample_data, conditions, outcome, calibration_plan
        )
        
        # 结果解释
        interpretation = analyzer.execute_result_interpretation(
            quantitative_results, theoretical_analysis
        )
        
        print("  集成分析流程完成")
        print(f"  分析阶段: {analyzer.analysis_state['phase']}")
        print("  模块集成测试完成\n")
        
    except Exception as e:
        print(f"  模块集成测试失败: {str(e)}\n")


def main():
    """主测试函数"""
    print("🔍 开始fsQCA技能功能测试\n")
    
    # 依次测试各模块
    test_calibration()
    test_truth_table()
    test_minimization()
    test_integration()
    
    print("✅ 所有测试完成！")


if __name__ == "__main__":
    main()