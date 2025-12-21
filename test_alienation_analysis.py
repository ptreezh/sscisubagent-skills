#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异化现象分析技能测试脚本
Alienation Analysis Skill Test Script

测试新创建的异化现象分析技能是否能够正常工作。

作者: 数字马克思智能体开发团队
版本: 1.0.0
日期: 2025-12-21
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from digital_marx_expert_controller import DigitalMarxExpertController, AnalysisRequest
import json

def test_alienation_analysis():
    """测试异化分析功能"""
    print("开始测试异化现象分析功能...")
    
    # 创建智能体控制器
    controller = DigitalMarxExpertController()
    
    # 创建异化分析测试请求
    alienation_request = AnalysisRequest(
        problem_description="分析平台经济中外卖骑手的劳动异化现象",
        analysis_type="alienation_analysis",
        data_sources={
            'labor_data': {
                'working_hours': 12,
                'wage_level': 'low',
                'work_autonomy': 'very_low',
                'skill_development': 'limited',
                'job_security': 'uncertain'
            },
            'platform_data': {
                'algorithm_control': 'high',
                'performance_monitoring': 'constant',
                'customer_rating_impact': 'significant',
                'income_volatility': 'high'
            },
            'social_data': {
                'community_support': 'low',
                'unionization': 'minimal',
                'social_recognition': 'negative',
                'career_prospects': 'limited'
            }
        },
        depth_level="comprehensive",
        output_format="detailed_report"
    )
    
    # 执行异化分析
    print("\n执行异化分析...")
    result = controller.process_analysis_request(alienation_request)
    
    # 输出结果
    print("\n" + "="*80)
    print("异化现象分析测试结果")
    print("="*80)
    print(f"分析成功: {result.success}")
    print(f"执行时间: {result.execution_time:.2f}秒")
    print(f"质量分数: {result.quality_metrics.overall_quality:.3f}")
    
    if result.error_message:
        print(f"错误信息: {result.error_message}")
    
    print("\n" + result.synthesis_report)
    
    # 检查是否包含异化分析内容
    if 'alienation_analysis' in result.analysis_results:
        alienation_result = result.analysis_results['alienation_analysis']
        print("\n" + "="*80)
        print("异化分析详细结果")
        print("="*80)
        
        if 'labor_alienation' in alienation_result:
            labor_alienation = alienation_result['labor_alienation']
            print("劳动异化分析:")
            for key, value in labor_alienation.items():
                if isinstance(value, dict) and 'manifestation' in value:
                    print(f"  - {key}: {value['manifestation']}")
                elif isinstance(value, dict) and 'score' in value:
                    print(f"  - {key}: {value['score']:.2f}/1.00")
        
        if 'alienation_intensity' in alienation_result:
            intensity = alienation_result['alienation_intensity']
            print(f"\n异化强度评估:")
            print(f"  - 总体分数: {intensity.get('overall_score', 0):.2f}/1.00")
            print(f"  - 严重程度: {intensity.get('severity_level', '未知')}")
            print(f"  - 主要类型: {', '.join(intensity.get('primary_types', []))}")
    
    # 导出结果
    output_file = controller.export_analysis_result(result, "alienation_analysis_test.json")
    print(f"\n分析结果已保存到: {output_file}")
    
    return result.success

def test_keyword_trigger():
    """测试关键词触发异化分析"""
    print("\n\n开始测试关键词触发异化分析...")
    
    controller = DigitalMarxExpertController()
    
    # 创建包含异化关键词的测试请求
    keyword_request = AnalysisRequest(
        problem_description="分析技术异化和消费异化对现代人生活的影响",
        analysis_type="comprehensive",
        data_sources={
            'technology_data': {
                'screen_time': 'high',
                'digital_dependency': 'severe',
                'social_media_usage': 'excessive'
            },
            'consumption_data': {
                'shopping_frequency': 'high',
                'debt_level': 'rising',
                'material_satisfaction': 'decreasing'
            }
        }
    )
    
    print("测试请求描述:", keyword_request.problem_description)
    
    result = controller.process_analysis_request(keyword_request)
    
    print(f"是否触发异化分析: {'alienation_analysis' in result.analysis_results}")
    
    if 'alienation_analysis' in result.analysis_results:
        print("✅ 关键词成功触发异化分析!")
    else:
        print("❌ 关键词未能触发异化分析")
    
    return 'alienation_analysis' in result.analysis_results

def main():
    """主测试函数"""
    print("数字马克思智能体 - 异化现象分析功能测试")
    print("="*80)
    
    # 测试1: 异化分析功能
    test1_success = test_alienation_analysis()
    
    # 测试2: 关键词触发
    test2_success = test_keyword_trigger()
    
    # 总结
    print("\n" + "="*80)
    print("测试总结")
    print("="*80)
    print(f"异化分析功能测试: {'✅ 通过' if test1_success else '❌ 失败'}")
    print(f"关键词触发测试: {'✅ 通过' if test2_success else '❌ 失败'}")
    
    if test1_success and test2_success:
        print("\n🎉 所有测试通过！异化现象分析功能创建成功！")
        return True
    else:
        print("\n⚠️ 部分测试失败，需要进一步调试。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)