#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研究设计技能 - 完整功能测试脚本
验证所有模块和功能的正常工作
"""

import pandas as pd
import numpy as np
import sys
import os
from pathlib import Path

# 添加脚本目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

def test_literature_analysis():
    """测试文献分析模块"""
    print("🧪 测试文献分析模块...")
    try:
        from literature_analysis import LiteratureAnalyzer
        
        # 创建示例数据
        np.random.seed(42)
        sample_data = pd.DataFrame({
            'title': [
                'The Impact of Social Media on Mental Health',
                'Digital Technology and Psychological Well-being',
                'Social Networks Effects on Individual Behavior',
                'Technology Adoption in Modern Society',
                'Psychological Factors in Digital Engagement'
            ] * 2,
            'author': [
                'Smith, J.', 'Johnson, A.', 'Williams, R.',
                'Brown, S.', 'Davis, M.', 'Miller, T.',
                'Wilson, K.', 'Moore, L.', 'Taylor, P.', 'Anderson, H.'
            ],
            'year': np.random.choice(range(2018, 2024), 10),
            'journal': [
                'Journal of Psychology', 'Digital Society Review', 'Tech & Behavior',
                'Modern Psychology', 'Cyberpsychology', 'Social Science Today',
                'Technology Quarterly', 'Digital Research', 'Psychological Science',
                'Online Behavior Studies'
            ],
            'abstract': [
                'This study examines the relationship between social media usage and mental health outcomes...',
                'Research on how digital technology affects psychological well-being...',
                'Analysis of how social networks influence individual behavioral patterns...',
                'Investigation of technology adoption trends in contemporary society...',
                'Study of psychological factors affecting digital engagement...',
                'Patterns of social media usage among young people...',
                'Examining the digital divide and technology access issues...',
                'Role of online communities in providing social support...',
                'Impact of cyberbullying on mental health outcomes...',
                'Privacy concerns in the age of digital technology...'
            ]
        })
        
        # 初始化分析器
        analyzer = LiteratureAnalyzer()
        
        # 加载数据
        analyzer.load_literature_data(sample_data)
        
        # 执行分析
        trend_analysis = analyzer.analyze_publication_trends()
        theme_analysis = analyzer.analyze_research_themes(top_n=5)
        knowledge_gaps = analyzer.identify_knowledge_gaps()
        report = analyzer.generate_literature_report()
        
        print("  ✓ 文献分析模块测试通过")
        return True
    except Exception as e:
        print(f"  ✗ 文献分析模块测试失败: {str(e)}")
        return False

def test_method_matching():
    """测试方法匹配模块"""
    print("🧪 测试方法匹配模块...")
    try:
        from method_matching import MethodMatcher, ResearchPurpose
        
        # 初始化匹配器
        matcher = MethodMatcher()
        
        # 测试探索性研究
        exploratory_matches = matcher.match_methods(
            research_purpose=ResearchPurpose.EXPLORATORY,
            sample_size=15,
            time_constraint='long',
            resource_level='adequate',
            ethical_considerations=False
        )
        
        # 测试评价性研究
        evaluative_matches = matcher.match_methods(
            research_purpose=ResearchPurpose.EVALUATIVE,
            sample_size=200,
            time_constraint='medium',
            resource_level='abundant',
            ethical_considerations=True
        )
        
        # 生成报告
        report = matcher.generate_method_recommendation_report()
        
        print("  ✓ 方法匹配模块测试通过")
        return True
    except Exception as e:
        print(f"  ✗ 方法匹配模块测试失败: {str(e)}")
        return False

def test_design_evaluation():
    """测试设计评估模块"""
    print("🧪 测试设计评估模块...")
    try:
        from design_evaluation import DesignEvaluator, QualityDimension
        
        # 初始化评估器
        evaluator = DesignEvaluator()
        
        # 创建示例设计元素
        sample_design = {
            'theoretical_framework': '基于社会认知理论，探讨自我效能感对学习行为的影响',
            'research_hypotheses': ['自我效能感正向影响学习行为', '动机在其中起中介作用'],
            'variable_relationships': '自我效能感 -> 动机 -> 学习行为',
            'novelty_indicators': '首次在中国大学生群体中验证该理论模型',
            'sampling_strategy': '分层随机抽样，按年级和专业分层',
            'data_collection_methods': '问卷调查、深度访谈、学习平台数据',
            'sample_size_calculation': '基于功效分析，α=0.05, β=0.2, 效应量=0.3, 需要288个样本',
            'power_analysis': '事后功效分析确认达到0.8的统计功效',
            'statistical_methods': '结构方程模型、中介效应检验、多群组分析',
            'time_schedule': '第1-2月文献回顾，第3-4月数据收集，第5-6月分析，第7月报告',
            'resource_allocation': '预算10万元，3名研究人员，6个月时间',
            'informed_consent_process': '书面知情同意，明示权利和退出机制',
            'data_management_plan': '加密存储，权限控制，定期备份',
            'risk_control_measures': '数据泄露应急预案，参与者心理支持',
            'bias_control_measures': '随机分配，盲法评估，统计控制'
        }
        
        # 执行评估
        evaluation = evaluator.evaluate_design(sample_design)
        report = evaluator.generate_evaluation_report()
        
        print("  ✓ 设计评估模块测试通过")
        return True
    except Exception as e:
        print(f"  ✗ 设计评估模块测试失败: {str(e)}")
        return False

def test_integrated_analysis():
    """测试集成分析模块"""
    print("🧪 测试集成分析模块...")
    try:
        from integrated_analysis import IntegratedResearchDesigner
        
        # 创建集成分析器
        designer = IntegratedResearchDesigner()
        
        # 创建示例文献数据
        np.random.seed(42)
        sample_literature = pd.DataFrame({
            'title': [
                'The Impact of Social Media on Mental Health',
                'Digital Technology and Psychological Well-being',
                'Social Networks Effects on Individual Behavior',
                'Technology Adoption in Modern Society',
                'Psychological Factors in Digital Engagement'
            ] * 2,
            'author': [
                'Smith, J.', 'Johnson, A.', 'Williams, R.',
                'Brown, S.', 'Davis, M.', 'Miller, T.',
                'Wilson, K.', 'Moore, L.', 'Taylor, P.', 'Anderson, H.'
            ],
            'year': np.random.choice(range(2018, 2024), 10),
            'journal': [
                'Journal of Psychology', 'Digital Society Review', 'Tech & Behavior',
                'Modern Psychology', 'Cyberpsychology', 'Social Science Today',
                'Technology Quarterly', 'Digital Research', 'Psychological Science',
                'Online Behavior Studies'
            ],
            'abstract': [
                'This study examines the relationship between social media usage and mental health outcomes...',
                'Research on how digital technology affects psychological well-being...',
                'Analysis of how social networks influence individual behavioral patterns...',
                'Investigation of technology adoption trends in contemporary society...',
                'Study of psychological factors affecting digital engagement...',
                'Patterns of social media usage among young people...',
                'Examining the digital divide and technology access issues...',
                'Role of online communities in providing social support...',
                'Impact of cyberbullying on mental health outcomes...',
                'Privacy concerns in the age of digital technology...'
            ]
        })
        
        # 定义研究上下文
        research_context = {
            'research_topic': '社交媒体对心理健康的影响',
            'research_purpose': '探索和解释',
            'target_population': '大学生群体',
            'hypothesis_testing': True,
            'phenomenon_understanding': False,
            'target_sample_size': 300,
            'time_constraint': 'medium',
            'resource_level': 'adequate',
            'ethical_sensitivity': True,
            'research_questions': [
                '社交媒体使用如何影响大学生的心理健康？',
                '哪些心理因素在其中起到中介作用？'
            ]
        }
        
        # 定义设计元素
        design_elements = {
            'theoretical_framework': '基于社会认知理论和压力应对理论',
            'research_hypotheses': [
                '社交媒体使用时间与焦虑水平正相关',
                '社交比较在其中起中介作用'
            ],
            'variable_relationships': '社交媒体使用 -> 社交比较 -> 心理健康',
            'novelty_indicators': '在特定文化背景下验证理论模型',
            'sampling_strategy': '分层随机抽样',
            'data_collection_methods': '问卷调查、认知测试',
            'sample_size_calculation': '基于功效分析，α=0.05, β=0.2, 效应量=0.3',
            'power_analysis': '事后功效分析确认达到0.8的统计功效',
            'statistical_methods': '结构方程模型、中介效应检验',
            'time_schedule': '6个月',
            'resource_allocation': '预算15万元，2名研究人员',
            'informed_consent_process': '书面知情同意',
            'data_management_plan': '加密存储，权限控制',
            'risk_control_measures': '数据泄露应急预案',
            'bias_control_measures': '随机分配，统计控制'
        }
        
        # 执行完整分析
        complete_results = designer.execute_complete_analysis(
            sample_literature,
            research_context,
            design_elements
        )
        
        print("  ✓ 集成分析模块测试通过")
        return True
    except Exception as e:
        print(f"  ✗ 集成分析模块测试失败: {str(e)}")
        return False

def main():
    """主测试函数"""
    print("🔍 开始研究设计技能完整功能测试...\n")
    
    # 测试所有模块
    tests = [
        test_literature_analysis,
        test_method_matching,
        test_design_evaluation,
        test_integrated_analysis
    ]
    
    results = []
    for test_func in tests:
        result = test_func()
        results.append(result)
        print()
    
    # 汇总结果
    passed = sum(results)
    total = len(results)
    
    print(f"✅ 测试完成！ {passed}/{total} 个模块测试通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！研究设计技能功能完整正常。")
        return True
    else:
        print(f"\n⚠️  {total-passed} 个模块测试失败，请检查相关功能。")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)