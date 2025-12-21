#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成测试 - 轴心编码完整流程
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from identify_categories import cluster_codes_to_categories, name_category, define_category
from build_relationships import identify_causal_relations, identify_conditional_relations
from construct_paradigm import build_paradigm_model, validate_paradigm

def test_complete_axial_coding_workflow():
    """测试完整轴心编码流程"""
    print("🧪 测试轴心编码完整流程...")
    
    # 模拟开放编码结果
    codes = [
        {'concept': '寻求教师指导', 'frequency': 10, 'definition': '主动向教师寻求帮助'},
        {'concept': '获得教师支持', 'frequency': 8, 'definition': '从教师处获得支持'},
        {'concept': '建立同伴关系', 'frequency': 7, 'definition': '与同学建立关系'},
        {'concept': '互相帮助学习', 'frequency': 6, 'definition': '同学间互相帮助'},
        {'concept': '制定学习计划', 'frequency': 9, 'definition': '制定详细计划'},
        {'concept': '执行学习计划', 'frequency': 5, 'definition': '坚持执行计划'},
        {'concept': '体验学业压力', 'frequency': 8, 'definition': '感受学习压力'},
        {'concept': '调整学习策略', 'frequency': 4, 'definition': '调整学习方法'},
        {'concept': '实现学业进步', 'frequency': 7, 'definition': '取得学习进步'},
        {'concept': '提升学习信心', 'frequency': 5, 'definition': '增强学习信心'},
    ]
    
    # 步骤1：识别范畴
    categories = cluster_codes_to_categories(codes, n_categories=3, min_codes=2)
    assert len(categories) > 0, "范畴识别失败"
    print(f"  ✅ 步骤1-范畴识别: {len(categories)} 个范畴")
    
    # 为范畴命名
    for cat in categories:
        cat['name'] = name_category(cat['codes'])
        cat['definition'] = define_category(cat['codes'])
    
    print(f"     范畴: {', '.join([c['name'] for c in categories])}")
    
    # 步骤2：识别关系
    causal_relations = identify_causal_relations(categories)
    conditional_relations = identify_conditional_relations(categories)
    all_relations = causal_relations + conditional_relations
    
    print(f"  ✅ 步骤2-关系识别: {len(all_relations)} 个关系")
    
    # 步骤3：构建Paradigm
    paradigm = build_paradigm_model(categories, all_relations)
    assert paradigm['phenomenon'] is not None, "Paradigm构建失败"
    print(f"  ✅ 步骤3-Paradigm构建: 核心现象='{paradigm['phenomenon']}'")
    
    # 步骤4：验证模型
    validation = validate_paradigm(paradigm)
    print(f"  ✅ 步骤4-模型验证: 完整度={validation['completeness_score']*100:.0f}%")
    
    if validation['issues']:
        print(f"     ⚠️  问题: {', '.join(validation['issues'])}")
    
    return True

def main():
    print("=" * 60)
    print("轴心编码技能 - 集成测试")
    print("=" * 60)
    
    try:
        if test_complete_axial_coding_workflow():
            print("\n✅ 集成测试通过")
            print("=" * 60)
            return 0
    except Exception as e:
        print(f"\n❌ 集成测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
