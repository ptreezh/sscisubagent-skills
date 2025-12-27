#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fsQCA技能全面系统测试脚本
验证所有功能模块、定性定量结合机制、渐进式披露等功能
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys
import os
import json
from typing import Dict, List, Tuple, Optional, Any

# 添加脚本目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

from calibration import FSCCalibration, consistency_xy, coverage_xy
from truth_table import FuzzyTruthTableBuilder
from minimization import FSCMinimizer


def test_calibration_module():
    """测试校准模块的所有功能"""
    print("🧪 测试校准模块...")
    
    # 创建测试数据
    np.random.seed(42)
    test_data = pd.Series(np.random.uniform(0, 10, 20), name='test_var')
    
    # 初始化校准器
    calibrator = FSCCalibration()
    
    # 测试所有校准方法
    methods = ['direct', 'threshold', 'interpolation', 'gaussian', 'sigmoid', 'indirect']
    results = {}
    
    for method in methods:
        try:
            if method == 'direct':
                calibrated = calibrator.calibrate_variable(test_data, method=method, thresholds=(8, 5, 2))
            elif method == 'threshold':
                calibrated = calibrator.calibrate_variable(test_data, method=method, thresholds=(7, 3))
            else:
                calibrated = calibrator.calibrate_variable(test_data, method=method)
            
            # 验证校准结果
            assert calibrated.min() >= 0, f"{method}校准结果小于0"
            assert calibrated.max() <= 1, f"{method}校准结果大于1"
            assert len(calibrated) == len(test_data), f"{method}校准长度不匹配"
            
            results[method] = {
                'range': (calibrated.min(), calibrated.max()),
                'valid': True,
                'length': len(calibrated)
            }
            print(f"  ✓ {method}校准: 范围 [{calibrated.min():.3f}, {calibrated.max():.3f}]")
        except Exception as e:
            results[method] = {'valid': False, 'error': str(e)}
            print(f"  ✗ {method}校准: 失败 - {str(e)}")
    
    # 测试一致性、覆盖度计算函数
    try:
        test_x = pd.Series([0.8, 0.6, 0.9, 0.3, 0.7])
        test_y = pd.Series([0.9, 0.5, 0.7, 0.2, 0.8])
        
        consistency = consistency_xy(test_x, test_y)
        coverage = coverage_xy(test_x, test_y)
        
        assert 0 <= consistency <= 1, "一致性值超出范围"
        assert 0 <= coverage <= 1, "覆盖度值超出范围"
        
        print(f"  ✓ 一致性计算: {consistency:.3f}")
        print(f"  ✓ 覆盖度计算: {coverage:.3f}")
        results['consistency_coverage'] = {'valid': True, 'consistency': consistency, 'coverage': coverage}
    except Exception as e:
        print(f"  ✗ 一致性/覆盖度计算: 失败 - {str(e)}")
        results['consistency_coverage'] = {'valid': False, 'error': str(e)}
    
    print("  校准模块测试完成\n")
    return results


def test_truth_table_module():
    """测试真值表模块的所有功能"""
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
    
    results = {}
    
    try:
        # 构建真值表
        truth_table = tt_builder.build_truth_table(
            test_data,
            ['A', 'B', 'C'],
            'outcome'
        )
        
        # 验证真值表结构
        assert 'configuration' in truth_table.columns, "缺少configuration列"
        assert 'consistency' in truth_table.columns, "缺少consistency列"
        assert 'outcome' in truth_table.columns, "缺少outcome列"
        
        print(f"  ✓ 真值表形状: {truth_table.shape}")
        print(f"  ✓ 矛盾组合数量: {len(tt_builder.contradictory_cases)}")
        print(f"  ✓ 逻辑余项数量: {len(tt_builder.logical_remainders)}")
        
        results['build'] = {
            'valid': True,
            'shape': truth_table.shape,
            'contradictory_count': len(tt_builder.contradictory_cases),
            'remainder_count': len(tt_builder.logical_remainders)
        }
        
        # 测试矛盾组合处理
        processed_table = tt_builder.handle_contradictions(method='remove')
        print(f"  ✓ 矛盾处理后形状: {processed_table.shape}")
        
        results['contradiction_handling'] = {
            'valid': True,
            'processed_shape': processed_table.shape
        }
        
        # 测试质量指标计算
        quality_metrics = tt_builder.calculate_quality_metrics()
        print(f"  ✓ 质量指标: {quality_metrics}")
        
        results['quality_metrics'] = {
            'valid': True,
            'metrics': quality_metrics
        }
        
    except Exception as e:
        print(f"  ✗ 真值表构建: 失败 - {str(e)}")
        results['build'] = {'valid': False, 'error': str(e)}
    
    print("  真值表模块测试完成\n")
    return results


def test_minimization_module():
    """测试最小化模块的所有功能"""
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
    
    results = {}
    
    try:
        # 执行最小化
        solutions = minimizer.minimize(truth_table, ['A', 'B', 'C'])
        
        print(f"  ✓ 生成解的数量: {len(solutions)}")
        for i, solution in enumerate(solutions):
            print(f"    解 {i+1} ({solution.solution_type.value}): 一致性={solution.consistency:.3f}, 覆盖度={solution.coverage:.3f}")
        
        results['minimization'] = {
            'valid': True,
            'solution_count': len(solutions),
            'solutions': [
                {
                    'type': solution.solution_type.value,
                    'expression': solution.expression,
                    'consistency': solution.consistency,
                    'coverage': solution.coverage,
                    'complexity': solution.complexity
                } for solution in solutions
            ]
        }
        
        # 测试解的质量评估
        if solutions:
            quality_metrics = minimizer.calculate_solution_quality(solutions[0], truth_table)
            print(f"  ✓ 解质量指标: {quality_metrics}")
            
            results['quality_assessment'] = {
                'valid': True,
                'metrics': quality_metrics
            }
            
            # 测试解的评估
            evaluation = minimizer.evaluate_solution(solutions[0], truth_table, ['A', 'B', 'C'], 'outcome')
            print(f"  ✓ 解评估: {evaluation['solution_type']}, 解释性={evaluation['interpretability']:.3f}, 稳健性={evaluation['robustness']:.3f}")
            
            results['solution_evaluation'] = {
                'valid': True,
                'evaluation': evaluation
            }
        
    except Exception as e:
        print(f"  ✗ 最小化执行: 失败 - {str(e)}")
        results['minimization'] = {'valid': False, 'error': str(e)}
    
    print("  最小化模块测试完成\n")
    return results


def test_integration_module():
    """测试集成分析模块的所有功能"""
    print("🧪 测试集成分析模块...")
    
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
        
        # 测试各阶段功能
        research_context = {
            'research_question': '测试研究问题',
            'theoretical_framework': '测试框架',
            'case_description': '10个测试案例'
        }
        
        # 1. 理论分析阶段
        theoretical_analysis = analyzer.execute_theoretical_analysis(research_context)
        print("  ✓ 理论分析阶段完成")
        
        # 2. 校准指导阶段
        calibration_plan = analyzer.execute_calibration_guidance(sample_data, theoretical_analysis)
        print("  ✓ 校准指导阶段完成")
        
        # 3. 定量分析阶段
        conditions = ['A', 'B', 'C']
        outcome = 'Y'
        quantitative_results = analyzer.execute_quantitative_analysis(
            sample_data, conditions, outcome, calibration_plan
        )
        print("  ✓ 定量分析阶段完成")
        
        # 4. 结果解释阶段
        interpretation = analyzer.execute_result_interpretation(
            quantitative_results, theoretical_analysis
        )
        print("  ✓ 结果解释阶段完成")
        
        # 5. 生成报告
        report = analyzer.generate_analysis_report("comprehensive_test_report.md")
        print("  ✓ 报告生成完成")
        
        results = {
            'theoretical_analysis': {'valid': True},
            'calibration_guidance': {'valid': True},
            'quantitative_analysis': {'valid': True},
            'result_interpretation': {'valid': True},
            'report_generation': {'valid': True},
            'integration_success': True
        }
        
        print(f"  ✓ 集成分析流程完成，当前阶段: {analyzer.analysis_state['phase']}")
        
    except Exception as e:
        print(f"  ✗ 集成分析流程: 失败 - {str(e)}")
        results = {
            'integration_success': False,
            'error': str(e)
        }
    
    print("  集成分析模块测试完成\n")
    return results


def test_documentation_links():
    """测试所有文档链接的有效性"""
    print("🧪 测试文档链接...")
    
    skill_root = Path(__file__).parent
    results = {}
    
    # 测试提示词文件
    prompt_files = [
        'prompts/theoretical-analysis.md',
        'prompts/calibration-guidance.md',
        'prompts/result-interpretation.md',
        'prompts/theoretical-analysis-outline.md',
        'prompts/calibration-guidance-outline.md',
        'prompts/result-interpretation-outline.md'
    ]
    
    prompt_results = {}
    for file_path in prompt_files:
        full_path = skill_root / file_path
        exists = full_path.exists()
        prompt_results[file_path] = exists
        if exists:
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - 不存在")
    
    results['prompts'] = prompt_results
    
    # 测试参考文档
    reference_files = [
        'references/METHODOLOGY.md',
        'references/BEST_PRACTICES.md',
        'references/METHODOLOGY-outline.md',
        'references/BEST_PRACTICES-outline.md'
    ]
    
    reference_results = {}
    for file_path in reference_files:
        full_path = skill_root / file_path
        exists = full_path.exists()
        reference_results[file_path] = exists
        if exists:
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - 不存在")
    
    results['references'] = reference_results
    
    # 测试脚本文件
    script_files = [
        'scripts/calibration.py',
        'scripts/truth_table.py',
        'scripts/minimization.py',
        'scripts/integrated_analysis.py'
    ]
    
    script_results = {}
    for file_path in script_files:
        full_path = skill_root / file_path
        exists = full_path.exists()
        script_results[file_path] = exists
        if exists:
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - 不存在")
    
    results['scripts'] = script_results
    
    # 测试资产文件
    asset_files = [
        'assets/templates/report_template.md'
    ]
    
    asset_results = {}
    for file_path in asset_files:
        full_path = skill_root / file_path
        exists = full_path.exists()
        asset_results[file_path] = exists
        if exists:
            print(f"  ✓ {file_path}")
        else:
            print(f"  ✗ {file_path} - 不存在")
    
    results['assets'] = asset_results
    
    print("  文档链接测试完成\n")
    return results


def test_progressive_disclosure():
    """测试渐进式披露功能"""
    print("🧪 测试渐进式披露功能...")
    
    skill_root = Path(__file__).parent
    
    # 读取SKILL.md文件，验证其结构
    skill_file = skill_root / 'SKILL.md'
    if not skill_file.exists():
        print("  ✗ SKILL.md 文件不存在")
        return {'valid': False, 'error': 'SKILL.md not found'}
    
    with open(skill_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否包含渐进式披露结构
    has_level_1 = 'Level 1: 核心元数据' in content
    has_level_2 = 'Level 2: 操作框架' in content
    has_level_3 = 'Level 3: 专业提示词' in content
    has_level_4 = 'Level 4: 计算脚本' in content
    
    print(f"  ✓ Level 1 (核心元数据): {'✓' if has_level_1 else '✗'}")
    print(f"  ✓ Level 2 (操作框架): {'✓' if has_level_2 else '✗'}")
    print(f"  ✓ Level 3 (专业提示词): {'✓' if has_level_3 else '✗'}")
    print(f"  ✓ Level 4 (计算脚本): {'✓' if has_level_4 else '✗'}")
    
    # 检查是否包含定性定量结合机制
    has_qualitative_quantitative = '定性定量结合机制' in content
    print(f"  ✓ 定性定量结合机制: {'✓' if has_qualitative_quantitative else '✗'}")
    
    results = {
        'valid': all([has_level_1, has_level_2, has_level_3, has_level_4]),
        'levels': {
            'level_1': has_level_1,
            'level_2': has_level_2,
            'level_3': has_level_3,
            'level_4': has_level_4
        },
        'qualitative_quantitative': has_qualitative_quantitative
    }
    
    print("  渐进式披露功能测试完成\n")
    return results


def test_qualitative_quantitative_integration():
    """测试定性定量结合机制"""
    print("🧪 测试定性定量结合机制...")
    
    # 验证集成分析器如何协调定性与定量
    try:
        from integrated_analysis import IntegratedFSCAnalyzer
        
        # 检查类的结构
        analyzer = IntegratedFSCAnalyzer('.')
        
        # 验证是否包含定性方法
        has_theoretical_analysis = hasattr(analyzer, 'execute_theoretical_analysis')
        has_calibration_guidance = hasattr(analyzer, 'execute_calibration_guidance')
        has_result_interpretation = hasattr(analyzer, 'execute_result_interpretation')
        
        # 验证是否包含定量组件
        has_calibrator = hasattr(analyzer, 'calibrator')
        has_truth_table_builder = hasattr(analyzer, 'truth_table_builder')
        has_minimizer = hasattr(analyzer, 'minimizer')
        
        print(f"  ✓ 定性方法 - 理论分析: {'✓' if has_theoretical_analysis else '✗'}")
        print(f"  ✓ 定性方法 - 校准指导: {'✓' if has_calibration_guidance else '✗'}")
        print(f"  ✓ 定性方法 - 结果解释: {'✓' if has_result_interpretation else '✗'}")
        print(f"  ✓ 定量组件 - 校准器: {'✓' if has_calibrator else '✗'}")
        print(f"  ✓ 定量组件 - 真值表构建器: {'✓' if has_truth_table_builder else '✗'}")
        print(f"  ✓ 定量组件 - 最小化器: {'✓' if has_minimizer else '✗'}")
        
        results = {
            'valid': all([
                has_theoretical_analysis, 
                has_calibration_guidance, 
                has_result_interpretation,
                has_calibrator,
                has_truth_table_builder,
                has_minimizer
            ]),
            'qualitative_methods': {
                'theoretical_analysis': has_theoretical_analysis,
                'calibration_guidance': has_calibration_guidance,
                'result_interpretation': has_result_interpretation
            },
            'quantitative_components': {
                'calibrator': has_calibrator,
                'truth_table_builder': has_truth_table_builder,
                'minimizer': has_minimizer
            }
        }
        
    except Exception as e:
        print(f"  ✗ 定性定量结合机制: 失败 - {str(e)}")
        results = {'valid': False, 'error': str(e)}
    
    print("  定性定量结合机制测试完成\n")
    return results


def generate_test_report(all_results):
    """生成测试报告"""
    print("📄 生成测试报告...")
    
    report_path = Path(__file__).parent / 'comprehensive_test_report.json'
    
    # 保存详细结果
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"  ✓ 测试报告已保存到: {report_path}")
    
    # 生成摘要
    total_tests = len(all_results)
    passed_tests = sum(1 for result in all_results.values() if result.get('valid', False))
    
    print(f"\n📊 测试摘要:")
    print(f"  总测试项: {total_tests}")
    print(f"  通过测试: {passed_tests}")
    print(f"  失败测试: {total_tests - passed_tests}")
    print(f"  成功率: {passed_tests/total_tests*100:.1f}%")
    
    return report_path


def main():
    """主测试函数"""
    print("🔍 开始fsQCA技能全面系统测试\n")
    
    all_results = {}
    
    # 1. 测试校准模块
    all_results['calibration'] = test_calibration_module()
    
    # 2. 测试真值表模块
    all_results['truth_table'] = test_truth_table_module()
    
    # 3. 测试最小化模块
    all_results['minimization'] = test_minimization_module()
    
    # 4. 测试集成分析模块
    all_results['integration'] = test_integration_module()
    
    # 5. 测试渐进式披露功能
    all_results['progressive_disclosure'] = test_progressive_disclosure()
    
    # 6. 测试定性定量结合机制
    all_results['qualitative_quantitative'] = test_qualitative_quantitative_integration()
    
    # 7. 测试文档链接
    all_results['documentation'] = test_documentation_links()
    
    # 8. 生成测试报告
    report_path = generate_test_report(all_results)
    
    print(f"\n✅ 所有测试完成！详细报告请查看: {report_path}")
    
    return all_results


if __name__ == "__main__":
    main()