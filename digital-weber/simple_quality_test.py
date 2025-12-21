#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单质量测试 - 验证优化版分析器的质量提升效果
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'scripts'))

try:
    from optimized_weberian_analyzer import OptimizedWeberianAnalyzer
    print("✓ 优化版分析器导入成功")
except ImportError as e:
    print(f"✗ 优化版分析器导入失败: {e}")
    sys.exit(1)


def simple_quality_test():
    """简单质量测试"""
    
    print("\n=== 简单质量测试 ===\n")
    
    # 初始化优化版分析器
    analyzer = OptimizedWeberianAnalyzer()
    
    # 测试文本数据
    test_text = """
    现代官僚组织作为一种理性的组织形式，追求效率最大化和程序规范化。
    组织成员按照明确的规则和程序行动，个人的情感和偏好被排除在决策过程之外。
    这种非人格化的管理方式确保了组织的公正性和效率，体现了韦伯所说的形式理性。
    
    从社会行动的角度看，组织成员的行为主要表现为目的理性行动，
    他们为了实现组织目标而选择最有效的手段。然而，在组织文化层面，
    价值理性行动也发挥着重要作用，成员们对组织使命和价值理念的认同
    构成了组织凝聚力的基础。
    
    理性化过程在组织中表现得尤为明显。除魅过程深入推进，
    传统和神秘的因素被理性计算所取代。形式理性在各个领域扩展，
    但实质理性的价值却时常被忽视，这正是韦伯所关注的现代性困境。
    """
    
    print("1. 执行优化版分析")
    print("-" * 30)
    
    try:
        # 执行优化版分析
        action_results = analyzer.analyze_social_action_typology_optimized(test_text)
        
        print("✓ 分析执行成功")
        print(f"✓ 行动类型: {action_results['action_type']}")
        print(f"✓ 理性分数: {action_results['rationality_score']:.2f}")
        
        # 获取质量分数
        if 'quality_metrics' in action_results:
            quality_score = action_results['quality_metrics']['overall_quality']
            print(f"✓ 质量分数: {quality_score:.2f}/10")
            
            # 质量评估
            if quality_score >= 8.0:
                quality_level = "优秀"
            elif quality_score >= 6.0:
                quality_level = "良好"
            elif quality_score >= 4.0:
                quality_level = "一般"
            else:
                quality_level = "需要改进"
            
            print(f"✓ 质量等级: {quality_level}")
            
            # 与原始版本对比
            original_quality = 3.83
            improvement = quality_score - original_quality
            improvement_percent = (improvement / original_quality) * 100
            
            print(f"\n2. 质量提升对比")
            print("-" * 30)
            print(f"✓ 原始版本质量: {original_quality:.2f}/10")
            print(f"✓ 优化版本质量: {quality_score:.2f}/10")
            print(f"✓ 提升幅度: {improvement:.2f}分 ({improvement_percent:.1f}%)")
            
            # 提升效果评估
            if improvement >= 2.0:
                print("🎉 质量提升显著！")
            elif improvement >= 1.0:
                print("✅ 质量明显提升")
            elif improvement > 0:
                print("📈 质量有所提升")
            else:
                print("⚠️  质量没有提升")
            
            # 详细质量指标
            print(f"\n3. 详细质量指标")
            print("-" * 30)
            quality = action_results['quality_metrics']
            print(f"✓ 完整性: {quality.get('completeness', 0):.2f}")
            print(f"✓ 平衡性: {quality.get('balance', 0):.2f}")
            print(f"✓ 清晰度: {quality.get('clarity', 0):.2f}")
            print(f"✓ 平均分: {quality.get('avg_score', 0):.2f}")
            
            # 各类型行动分析
            print(f"\n4. 各类型行动分析")
            print("-" * 30)
            
            action_types = [
                ('purposive_rationality', '目的理性'),
                ('value_rationality', '价值理性'),
                ('affective_action', '情感性'),
                ('traditional_action', '传统性')
            ]
            
            for action_type, type_name in action_types:
                if action_type in action_results:
                    result = action_results[action_type]
                    print(f"✓ {type_name}: {result['score']:.2f} ({result['level']})")
            
            return quality_score >= 6.0
            
        else:
            print("✗ 缺少质量指标")
            return False
            
    except Exception as e:
        print(f"✗ 分析执行失败: {e}")
        return False


def test_multiple_cases():
    """多用例测试"""
    
    print("\n=== 多用例测试 ===\n")
    
    analyzer = OptimizedWeberianAnalyzer()
    
    test_cases = [
        {
            'name': '高度理性化',
            'text': '''
            现代企业以效率最大化为目标，通过科学管理和理性决策实现组织目标。
            管理者基于数据和逻辑分析制定策略，员工按照规章制度执行任务。
            这种理性化的管理模式确保了组织的高效运转和可持续发展。
            '''
        },
        {
            'name': '混合类型',
            'text': '''
            传统家族企业既继承了历史悠久的经营理念，又积极采用现代管理方法。
            创始人的个人魅力和领导才能在企业中发挥重要作用，
            同时也建立了完善的制度体系来规范企业运作。
            '''
        }
    ]
    
    scores = []
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"测试用例 {i}: {test_case['name']}")
        print("-" * 30)
        
        try:
            action_results = analyzer.analyze_social_action_typology_optimized(test_case['text'])
            quality_score = action_results['quality_metrics']['overall_quality']
            scores.append(quality_score)
            
            print(f"✓ 质量分数: {quality_score:.2f}/10")
            print(f"✓ 行动类型: {action_results['action_type']}")
            
        except Exception as e:
            print(f"✗ 测试失败: {e}")
            scores.append(0.0)
        
        print()
    
    # 统计结果
    avg_score = sum(scores) / len(scores)
    max_score = max(scores)
    min_score = min(scores)
    
    print("=== 统计结果 ===")
    print(f"平均质量分数: {avg_score:.2f}/10")
    print(f"最高质量分数: {max_score:.2f}/10")
    print(f"最低质量分数: {min_score:.2f}/10")
    print(f"测试用例数量: {len(test_cases)}")
    
    return avg_score >= 6.0


if __name__ == "__main__":
    print("开始简单质量测试...")
    
    success1 = simple_quality_test()
    success2 = test_multiple_cases()
    
    print("\n=== 测试总结 ===")
    
    if success1 and success2:
        print("🎉 所有测试通过！")
        print("✅ 优化版韦伯分析器质量显著提升，可信可行！")
        print("✅ 第一性原理优化策略有效！")
    else:
        print("⚠️ 部分测试失败")
        print("❌ 需要进一步优化")
    
    sys.exit(0 if success1 and success2 else 1)