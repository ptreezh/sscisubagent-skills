#!/usr/bin/env python3
"""
Soul Agent Creator 测试用例

用法:
    python tests/test_creation.py
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from tools import list_skills, generate_soul_config, validate_soul_config


def test_list_skills():
    """测试技能列表功能"""
    print("\n" + "=" * 60)
    print("测试：list_skills")
    print("=" * 60)
    
    # 测试列出所有技能
    skills = list_skills.list_all()
    print(f"\n✅ 列出所有技能：共 {len(skills)} 个")
    
    # 测试按类别列出
    qualitative = list_skills.list_by_category("qualitative")
    print(f"✅ 质性研究方法：共 {len(qualitative)} 个")
    
    quantitative = list_skills.list_by_category("quantitative")
    print(f"✅ 定量研究方法：共 {len(quantitative)} 个")
    
    # 测试获取单个技能
    gt = list_skills.get_skill("grounded-theory")
    print(f"✅ 获取 grounded-theory: {gt['name']}")
    
    # 测试推荐
    recs = list_skills.recommend_by_field("管理学")
    print(f"✅ 管理学推荐：{', '.join(recs[:3])}")
    
    # 测试搜索
    results = list_skills.search_by_keyword("网络")
    print(f"✅ 搜索'网络': {', '.join(results)}")
    
    print("\n✅ list_skills 测试通过")
    return True


def test_generate_soul_config():
    """测试配置生成功"""
    print("\n" + "=" * 60)
    print("测试：generate_soul_config")
    print("=" * 60)
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 测试创建 grounded-theory 分身
        result = generate_soul_config.create(
            skill_id="grounded-theory",
            custom_name="测试扎根理论助手",
            output_dir=temp_dir,
            verbose=True
        )
        
        print(f"\n✅ 创建结果:")
        print(f"   Soul ID: {result['soul_id']}")
        print(f"   名称：{result['display_name']}")
        print(f"   路径：{result['output_dir']}")
        print(f"   文件：{', '.join(result['files'])}")
        
        # 验证文件存在
        soul_dir = Path(result['output_dir'])
        required_files = ["SOUL.md", "SOUL_CONFIG.yaml", "METHODOLOGY.md", "README.md", "metadata.json"]
        
        for filename in required_files:
            file_path = soul_dir / filename
            assert file_path.exists(), f"文件缺失：{filename}"
            print(f"✅ 文件存在：{filename}")
        
        # 验证目录结构
        required_dirs = ["memory/lessons", "memory/patterns", "evolution", "cases/positive", "cases/negative"]
        for dirname in required_dirs:
            dir_path = soul_dir / dirname
            assert dir_path.exists(), f"目录缺失：{dirname}"
            print(f"✅ 目录存在：{dirname}")
        
        print("\n✅ generate_soul_config 测试通过")
        return True
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)


def test_validate_soul_config():
    """测试验证功能"""
    print("\n" + "=" * 60)
    print("测试：validate_soul_config")
    print("=" * 60)
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 先创建分身
        result = generate_soul_config.create(
            skill_id="social-network-analysis",
            custom_name="测试 SNA 助手",
            output_dir=temp_dir,
            verbose=False
        )
        
        # 测试验证
        soul_dir = Path(result['output_dir'])
        validation_result = validate_soul_config.check_soul_config(str(soul_dir))
        
        print(f"\n验证结果:")
        print(f"   Soul ID: {validation_result['soul_id']}")
        print(f"   通过：{validation_result['passed']}")
        print(f"   失败：{validation_result['failed']}")
        print(f"   警告：{validation_result['warnings']}")
        print(f"   总体：{'✅ 通过' if validation_result['overall'] == 'pass' else '❌ 失败'}")
        
        # 打印详细报告
        print("\n" + validate_soul_config.format_report(validation_result))
        
        assert validation_result['overall'] == 'pass', "验证应该通过"
        
        print("\n✅ validate_soul_config 测试通过")
        return True
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)


def test_full_workflow():
    """测试完整工作流"""
    print("\n" + "=" * 60)
    print("测试：完整工作流")
    print("=" * 60)
    
    # 创建临时目录
    temp_dir = tempfile.mkdtemp()
    
    try:
        # 1. 列出技能
        print("\n1️⃣ 列出可用技能...")
        skills = list_skills.list_all()
        print(f"   可用技能：{len(skills)} 个")
        
        # 2. 推荐技能
        print("\n2️⃣ 根据领域推荐...")
        recs = list_skills.recommend_by_field("社会学")
        print(f"   推荐：{', '.join(recs)}")
        
        # 3. 创建分身
        print("\n3️⃣ 创建分身...")
        result = generate_soul_config.create(
            skill_id=recs[0],
            custom_name="完整测试分身",
            output_dir=temp_dir,
            verbose=False
        )
        print(f"   创建成功：{result['soul_id']}")
        
        # 4. 验证配置
        print("\n4️⃣ 验证配置...")
        soul_dir = Path(result['output_dir'])
        validation_result = validate_soul_config.check_soul_config(str(soul_dir))
        print(f"   验证结果：{'✅ 通过' if validation_result['overall'] == 'pass' else '❌ 失败'}")
        
        assert validation_result['overall'] == 'pass', "完整工作流应该通过"
        
        print("\n✅ 完整工作流测试通过")
        return True
        
    finally:
        # 清理临时目录
        shutil.rmtree(temp_dir)


def run_all_tests():
    """运行所有测试"""
    print("\n" + "=" * 70)
    print("  Soul Agent Creator - 测试套件")
    print("=" * 70)
    
    tests = [
        ("list_skills", test_list_skills),
        ("generate_soul_config", test_generate_soul_config),
        ("validate_soul_config", test_validate_soul_config),
        ("full_workflow", test_full_workflow),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, success, None))
        except Exception as e:
            results.append((name, False, str(e)))
    
    # 打印总结
    print("\n" + "=" * 70)
    print("  测试总结")
    print("=" * 70)
    
    passed = sum(1 for _, success, _ in results if success)
    total = len(results)
    
    for name, success, error in results:
        status = "✅ 通过" if success else f"❌ 失败：{error}"
        print(f"{name}: {status}")
    
    print(f"\n总计：{passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        return True
    else:
        print(f"\n⚠️ {total - passed} 个测试失败")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
