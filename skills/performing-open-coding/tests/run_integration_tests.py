#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集成测试运行器 - 快速验证核心功能
"""

import sys
from pathlib import Path

# 添加scripts到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

def test_preprocess():
    """测试文本预处理"""
    from preprocess_text import tokenize_chinese, remove_stopwords, preprocess_text
    
    print("🧪 测试 preprocess_text...")
    
    # 测试分词
    words = tokenize_chinese("学生寻求老师的帮助")
    assert len(words) > 0, "分词失败"
    print(f"  ✅ 分词: {len(words)} 个词")
    
    # 测试停用词过滤
    filtered = remove_stopwords(['学习', '的', '方法'])
    assert '的' not in filtered, "停用词过滤失败"
    print(f"  ✅ 停用词过滤: {len(filtered)} 个词")
    
    # 测试完整流程
    result = preprocess_text("学生寻求帮助。老师提供指导。")
    assert 'segments' in result, "预处理流程失败"
    print(f"  ✅ 完整流程: {result['total_words']} 个词")
    
    return True

def test_auto_loader():
    """测试自动加载器"""
    from auto_loader import OpenCodingAutoLoader
    
    print("🧪 测试 auto_loader...")
    
    loader = OpenCodingAutoLoader()
    
    # 测试概念提取
    concepts = loader.quick_concept_extract("学生寻求老师的帮助和指导")
    assert len(concepts) > 0, "概念提取失败"
    print(f"  ✅ 概念提取: {len(concepts)} 个概念")
    
    # 测试概念分类
    concept_type = loader._classify_concept("寻求帮助")
    assert concept_type == '行动概念', "概念分类失败"
    print(f"  ✅ 概念分类: {concept_type}")
    
    # 测试编码建议
    suggestions = loader.generate_coding_suggestions(concepts)
    assert len(suggestions) > 0, "编码建议生成失败"
    print(f"  ✅ 编码建议: {len(suggestions)} 条")
    
    return True

def test_compare_codes():
    """测试持续比较"""
    from compare_codes import calculate_similarity, identify_duplicates
    
    print("🧪 测试 compare_codes...")
    
    # 测试相似度计算
    sim = calculate_similarity("寻求帮助", "寻求帮助")
    assert sim > 0.9, "相似度计算失败"
    print(f"  ✅ 相似度计算: {sim:.2f}")
    
    # 测试重复识别
    codes = [
        {'concept': '寻求帮助', 'frequency': 5},
        {'concept': '寻求帮助', 'frequency': 3}
    ]
    duplicates = identify_duplicates(codes, threshold=0.8)
    assert len(duplicates) > 0, "重复识别失败"
    print(f"  ✅ 重复识别: {len(duplicates)} 对")
    
    return True

def test_integration_workflow():
    """测试完整集成流程"""
    from preprocess_text import preprocess_text
    from auto_loader import OpenCodingAutoLoader
    from compare_codes import identify_duplicates
    
    print("🧪 测试集成流程...")
    
    text = """
    学生寻求老师的帮助。老师提供学习指导。
    学生建立学习计划。执行学习计划。
    """
    
    # 1. 预处理
    preprocessed = preprocess_text(text)
    print(f"  ✅ 步骤1-预处理: {preprocessed['total_words']} 个词")
    
    # 2. 概念提取
    loader = OpenCodingAutoLoader()
    concepts = loader.quick_concept_extract(text)
    print(f"  ✅ 步骤2-概念提取: {len(concepts)} 个概念")
    
    # 3. 持续比较
    duplicates = identify_duplicates(concepts, threshold=0.7)
    print(f"  ✅ 步骤3-持续比较: {len(duplicates)} 对重复")
    
    return True

def main():
    """运行所有测试"""
    print("=" * 60)
    print("开放编码技能 - 集成测试")
    print("=" * 60)
    
    tests = [
        ("文本预处理", test_preprocess),
        ("自动加载器", test_auto_loader),
        ("持续比较", test_compare_codes),
        ("集成流程", test_integration_workflow)
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"✅ {name} - 通过\n")
        except Exception as e:
            failed += 1
            print(f"❌ {name} - 失败: {e}\n")
    
    print("=" * 60)
    print(f"测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    if failed == 0:
        print("🎉 所有测试通过！")
        return 0
    else:
        print(f"⚠️  {failed} 个测试失败")
        return 1

if __name__ == "__main__":
    sys.exit(main())
