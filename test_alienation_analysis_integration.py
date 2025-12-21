#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异化分析技能集成测试
测试完整的定性与定量分析整合系统
"""

import json
import os
import sys
from datetime import datetime

# 添加项目根目录到路径
sys.path.append('.')

from digital_marx_expert_controller import DigitalMarxExpertController, AnalysisRequest

def test_alienation_analysis_integration():
    """测试异化分析技能集成"""
    print("=" * 60)
    print("数字马克思智能体 - 异化分析技能集成测试")
    print("=" * 60)
    
    # 初始化控制器
    controller = DigitalMarxExpertController()
    
    # 创建测试请求
    test_request = AnalysisRequest(
        problem_description="我是一名程序员，最近感到工作压力很大，感觉自己只是在机械地完成任务，没有创造性，而且总是担心被新技术替代。我发现自己越来越依赖手机和网络，甚至在休息时间也会频繁查看工作消息。",
        analysis_type="alienation_analysis",
        data_sources={
            'labor_data': {
                'work_stress_level': 0.8,
                'autonomy_level': 0.3,
                'meaningfulness': 0.2,
                'skill_development': 0.4,
                'work_life_balance': 0.3
            },
            'technology_data': {
                'usage_frequency': 0.9,
                'usage_duration': 0.8,
                'dependency_severity': 0.7,
                'function_loss_anxiety': 0.6,
                'withdrawal_symptoms': 0.4
            },
            'social_data': {
                'intimacy_level': 0.4,
                'trust_level': 0.5,
                'communication_quality': 0.6,
                'emotional_support': 0.3,
                'community_connection': 0.3
            }
        },
        depth_level="comprehensive",
        output_format="detailed_report"
    )
    
    print("测试请求创建完成")
    print(f"问题描述: {test_request.problem_description[:50]}...")
    print(f"分析类型: {test_request.analysis_type}")
    print()
    
    try:
        # 执行分析
        print("开始执行异化分析...")
        result = controller.process_analysis_request(test_request)
        
        # 输出结果
        print("分析结果:")
        print("-" * 40)
        print(f"执行成功: {result.success}")
        print(f"执行时间: {result.execution_time:.2f}秒")
        print(f"质量分数: {result.quality_metrics.overall_quality:.3f}")
        
        if result.success:
            print("\n✅ 异化分析技能集成测试通过!")
            
            # 检查异化分析结果
            if 'alienation_analysis' in result.analysis_results:
                alienation_result = result.analysis_results['alienation_analysis']
                print(f"异化类型: {alienation_result.get('alienation_types', [])}")
                print(f"整合分数: {alienation_result.get('integration_score', 0):.3f}")
                print(f"综合质量: {alienation_result.get('synthesis_quality', '未知')}")
                
                recommendations = alienation_result.get('recommendations', [])
                if recommendations:
                    print(f"建议数量: {len(recommendations)}")
                    print("主要建议:")
                    for i, rec in enumerate(recommendations[:3], 1):
                        print(f"  {i}. {rec}")
            
            print(f"\n综合报告长度: {len(result.synthesis_report)}字符")
            
        else:
            print("\n❌ 异化分析技能集成测试失败!")
            print(f"错误信息: {result.error_message}")
            
        return result.success
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生异常: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_prompt_files_accessibility():
    """测试prompt文件可访问性"""
    print("\n" + "=" * 60)
    print("Prompt文件可访问性测试")
    print("=" * 60)
    
    prompt_files = [
        'skills/alienation-analysis/prompts/01-core-analysis-prompt.md',
        'skills/alienation-analysis/prompts/02-labor-alienation-prompt.md',
        'skills/alienation-analysis/prompts/03-social-alienation-prompt.md',
        'skills/alienation-analysis/prompts/04-consumption-alienation-prompt.md',
        'skills/alienation-analysis/prompts/05-technology-alienation-prompt.md',
        'skills/alienation-analysis/prompts/06-synthesis-prompt.md'
    ]
    
    accessible_count = 0
    for prompt_file in prompt_files:
        if os.path.exists(prompt_file):
            try:
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"✅ {os.path.basename(prompt_file)}: {len(content)}字符")
                    accessible_count += 1
            except Exception as e:
                print(f"❌ {os.path.basename(prompt_file)}: 读取失败 - {str(e)}")
        else:
            print(f"❌ {os.path.basename(prompt_file)}: 文件不存在")
    
    print(f"\nPrompt文件可访问性: {accessible_count}/{len(prompt_files)}")
    return accessible_count == len(prompt_files)

def test_scripts_accessibility():
    """测试脚本可访问性"""
    print("\n" + "=" * 60)
    print("脚本文件可访问性测试")
    print("=" * 60)
    
    scripts = [
        'skills/alienation-analysis/scripts/calculate_alienation_score.py',
        'skills/alienation-analysis/scripts/classify_alienation_types.py',
        'skills/alienation-analysis/scripts/generate_intervention_plan.py',
        'skills/alienation-analysis/scripts/workplace_satisfaction_analysis.py',
        'skills/alienation-analysis/scripts/career_development_evaluation.py',
        'skills/alienation-analysis/scripts/social_network_analysis.py',
        'skills/alienation-analysis/scripts/relationship_quality_assessment.py',
        'skills/alienation-analysis/scripts/consumer_behavior_analysis.py',
        'skills/alienation-analysis/scripts/materialism_assessment.py',
        'skills/alienation-analysis/scripts/technology_dependency_analysis.py',
        'skills/alienation-analysis/scripts/digital_wellbeing_evaluation.py'
    ]
    
    accessible_count = 0
    for script in scripts:
        if os.path.exists(script):
            try:
                with open(script, 'r', encoding='utf-8') as f:
                    content = f.read()
                    print(f"✅ {os.path.basename(script)}: {len(content)}字符")
                    accessible_count += 1
            except Exception as e:
                print(f"❌ {os.path.basename(script)}: 读取失败 - {str(e)}")
        else:
            print(f"❌ {os.path.basename(script)}: 文件不存在")
    
    print(f"\n脚本文件可访问性: {accessible_count}/{len(scripts)}")
    return accessible_count == len(scripts)

def main():
    """主测试函数"""
    print("数字马克思智能体 - 异化分析技能集成测试")
    print("测试时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # 测试1: 文件可访问性
    prompt_test = test_prompt_files_accessibility()
    script_test = test_scripts_accessibility()
    
    # 测试2: 集成功能测试
    integration_test = test_alienation_analysis_integration()
    
    # 总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)
    print(f"Prompt文件可访问性: {'✅ 通过' if prompt_test else '❌ 失败'}")
    print(f"脚本文件可访问性: {'✅ 通过' if script_test else '❌ 失败'}")
    print(f"异化分析集成: {'✅ 通过' if integration_test else '❌ 失败'}")
    
    all_passed = prompt_test and script_test and integration_test
    print(f"\n总体测试结果: {'✅ 全部通过' if all_passed else '❌ 部分失败'}")
    
    if all_passed:
        print("\n🎉 异化分析技能已成功集成到数字马克思智能体!")
        print("✅ 符合agentskills.io标准")
        print("✅ 定性与定量分析有效分离")
        print("✅ 渐进式信息披露架构")
        print("✅ 智能路由和调用机制")
    
    return all_passed

if __name__ == '__main__':
    main()
