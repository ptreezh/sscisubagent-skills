#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DID技能集成测试脚本
测试所有组件的基本功能和集成效果
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

# 测试导入
try:
    from did_estimator import DIDEstimator
    from parallel_trend import ParallelTrendTester
    from robustness_test import RobustnessTester
    from visualization import DIDVisualizer
    from integrated_did import IntegratedDIDAnalyzer
    print("✅ 所有模块导入成功")
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    exit(1)

def test_basic_functionality():
    """测试基本功能"""
    print("\n🧪 测试基本功能...")
    
    # 创建测试数据
    np.random.seed(42)
    n_entities = 20
    n_periods = 6
    entities = [f"entity_{i}" for i in range(n_entities)]
    periods = list(range(2018, 2018 + n_periods))
    
    data = []
    for entity in entities:
        base_outcome = 100 + np.random.normal(0, 8)
        
        for period in periods:
            treat = 1 if entity in ['entity_1', 'entity_2', 'entity_3'] and period >= 2020 else 0
            outcome = base_outcome + (period - 2018) * 1.5 + np.random.normal(0, 4)
            
            if treat == 1:
                outcome += 12
            
            data.append({
                'entity': entity,
                'year': period,
                'treatment': treat,
                'outcome': outcome,
                'control_var1': np.random.normal(0, 1),
                'control_var2': np.random.normal(0, 1)
            })
    
    df = pd.DataFrame(data)
    print(f"✅ 测试数据创建成功: {len(df)} 行, {df['entity'].nunique()} 个实体")
    
    # 测试DID估计器
    try:
        estimator = DIDEstimator()
        results = estimator.estimate_twoway_fe(
            df, 'entity', 'year', 'treatment', 'outcome', 
            control_vars=['control_var1', 'control_var2']
        )
        print(f"✅ DID估计成功: 效应={results['did_effect']:.3f}, p值={results['did_pvalue']:.3f}")
    except Exception as e:
        print(f"❌ DID估计失败: {e}")
        return False
    
    # 测试平行趋势检验
    try:
        trend_tester = ParallelTrendTester()
        trend_results = trend_tester.test_parallel_trend(
            df, 'entity', 'year', 'treatment', 'outcome'
        )
        print(f"✅ 平行趋势检验成功")
    except Exception as e:
        print(f"❌ 平行趋势检验失败: {e}")
        return False
    
    # 测试稳健性检验
    try:
        robustness_tester = RobustnessTester()
        robustness_results = robustness_tester.run_robustness_tests(
            df, 'entity', 'year', 'treatment', 'outcome', results
        )
        print(f"✅ 稳健性检验成功")
    except Exception as e:
        print(f"❌ 稳健性检验失败: {e}")
        return False
    
    # 测试可视化
    try:
        visualizer = DIDVisualizer()
        visualizer.create_parallel_trend_plot(df, 'entity', 'year', 'treatment', 'outcome')
        print("✅ 可视化图表创建成功")
    except Exception as e:
        print(f"❌ 可视化创建失败: {e}")
        return False
    
    return True

def test_file_structure():
    """测试文件结构完整性"""
    print("\n📁 检查文件结构...")
    
    skill_root = Path("D:/stigmergy-CLI-Multi-Agents/sscisubagent-skills/did-analysis")
    
    required_files = {
        'SKILL.md': skill_root / 'SKILL.md',
        'scripts/did_estimator.py': skill_root / 'scripts' / 'did_estimator.py',
        'scripts/parallel_trend.py': skill_root / 'scripts' / 'parallel_trend.py',
        'scripts/robustness_test.py': skill_root / 'scripts' / 'robustness_test.py',
        'scripts/visualization.py': skill_root / 'scripts' / 'visualization.py',
        'scripts/integrated_did.py': skill_root / 'scripts' / 'integrated_did.py',
        'prompts/experimental-design.md': skill_root / 'prompts' / 'experimental-design.md',
        'prompts/model-specification.md': skill_root / 'prompts' / 'model-specification.md',
        'prompts/causal-interpretation.md': skill_root / 'prompts' / 'causal-interpretation.md',
        'prompts/policy-recommendation.md': skill_root / 'prompts' / 'policy-recommendation.md',
        'references/BEST_PRACTICES.md': skill_root / 'references' / 'BEST_PRACTICES.md'
    }
    
    missing_files = []
    for file_desc, file_path in required_files.items():
        if file_path.exists():
            print(f"✅ {file_desc}")
        else:
            print(f"❌ {file_desc} - 文件缺失")
            missing_files.append(file_desc)
    
    return len(missing_files) == 0

def test_prompt_loading():
    """测试提示词文件加载"""
    print("\n📝 测试提示词文件加载...")
    
    skill_root = Path("D:/stigmergy-CLI-Multi-Agents/sscisubagent-skills/did-analysis")
    
    prompt_files = [
        'experimental-design.md',
        'model-specification.md', 
        'causal-interpretation.md',
        'policy-recommendation.md'
    ]
    
    for prompt_file in prompt_files:
        try:
            prompt_path = skill_root / 'prompts' / prompt_file
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查YAML frontmatter
            if content.startswith('---'):
                print(f"✅ {prompt_file} - YAML frontmatter正确")
            else:
                print(f"❌ {prompt_file} - 缺少YAML frontmatter")
                
            # 检查内容长度
            if len(content) > 1000:
                print(f"✅ {prompt_file} - 内容长度充足")
            else:
                print(f"⚠️ {prompt_file} - 内容可能过短")
                
        except Exception as e:
            print(f"❌ {prompt_file} - 加载失败: {e}")
            return False
    
    return True

def test_integration_quality():
    """测试集成质量"""
    print("\n🔗 测试集成质量...")
    
    try:
        skill_root = Path("D:/stigmergy-CLI-Multi-Agents/sscisubagent-skills/did-analysis")
        analyzer = IntegratedDIDAnalyzer(str(skill_root))
        
        # 测试提示词加载
        experimental_design = analyzer.load_prompt_content("experimental-design")
        model_specification = analyzer.load_prompt_content("model-specification")
        causal_interpretation = analyzer.load_prompt_content("causal-interpretation")
        policy_recommendation = analyzer.load_prompt_content("policy-recommendation")
        
        print("✅ 所有提示词加载成功")
        
        # 检查提示词内容质量
        prompts = {
            'experimental-design': experimental_design,
            'model-specification': model_specification,
            'causal-interpretation': causal_interpretation,
            'policy-recommendation': policy_recommendation
        }
        
        for name, content in prompts.items():
            lines = content.split('\n')
            non_empty_lines = [line for line in lines if line.strip()]
            
            if len(non_empty_lines) > 50:
                print(f"✅ {name} - 内容丰富")
            else:
                print(f"⚠️ {name} - 内容可能不够详细")
                
            if '##' in content:
                print(f"✅ {name} - 结构清晰")
            else:
                print(f"⚠️ {name} - 结构可能不够清晰")
        
        return True
        
    except Exception as e:
        print(f"❌ 集成质量测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("🚀 开始DID技能全面测试...")
    print("=" * 50)
    
    # 测试文件结构
    structure_ok = test_file_structure()
    
    # 测试提示词加载
    prompt_ok = test_prompt_loading()
    
    # 测试基本功能
    functionality_ok = test_basic_functionality()
    
    # 测试集成质量
    integration_ok = test_integration_quality()
    
    # 总结测试结果
    print("\n" + "=" * 50)
    print("📊 测试结果总结:")
    print(f"文件结构: {'✅ 通过' if structure_ok else '❌ 失败'}")
    print(f"提示词加载: {'✅ 通过' if prompt_ok else '❌ 失败'}")
    print(f"基本功能: {'✅ 通过' if functionality_ok else '❌ 失败'}")
    print(f"集成质量: {'✅ 通过' if integration_ok else '❌ 失败'}")
    
    overall_success = structure_ok and prompt_ok and functionality_ok and integration_ok
    print(f"\n🎯 总体结果: {'✅ 全部通过' if overall_success else '❌ 存在问题'}")
    
    if overall_success:
        print("\n🎉 DID技能设计完成，所有组件运行正常！")
        print("💡 建议: 可以开始使用技能进行实际的DID分析")
    else:
        print("\n⚠️ 发现问题，请根据上述提示进行修复")
    
    return overall_success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)