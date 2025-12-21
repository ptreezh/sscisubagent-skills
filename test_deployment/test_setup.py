"""
测试脚本，用于模拟真实场景进行项目级的技能部署和测试
该脚本将验证dist目录下的所有技能是否可以正确加载和运行
"""

import os
import sys
import json
import shutil
from pathlib import Path

def setup_test_environment():
    """创建测试环境"""
    print("Setting up test environment...")
    
    # 创建临时目录用于测试
    test_dir = Path("temp_test_env")
    if test_dir.exists():
        shutil.rmtree(test_dir)
    
    test_dir.mkdir(exist_ok=True)
    print(f"Created test directory: {test_dir.absolute()}")
    
    return test_dir

def discover_skills(dist_path):
    """发现dist目录下的所有技能"""
    skills = []
    
    # 遍历dist目录寻找技能定义文件
    dist_dir = Path(dist_path)
    
    # 查找所有可能的技能定义
    for item in dist_dir.iterdir():
        if item.is_dir():
            # 检查目录中是否有SKILL.md或相关的技能定义文件
            skill_files = list(item.glob("*.md")) + list(item.glob("*.py")) + list(item.glob("*.json"))
            if skill_files:
                skills.append({
                    'name': item.name,
                    'path': item,
                    'files': skill_files
                })
                
    # 特别检查新移动过来的skills子目录
    skills_dir = dist_dir / "skills"
    if skills_dir.exists() and skills_dir.is_dir():
        for item in skills_dir.iterdir():
            if item.is_dir():
                skill_files = list(item.glob("*.md")) + list(item.glob("*.py")) + list(item.glob("*.json"))
                if skill_files:
                    skills.append({
                        'name': f"skills/{item.name}",
                        'path': item,
                        'files': skill_files
                    })
    
    return skills

def test_skill_loading(skill_info):
    """测试单个技能的加载能力"""
    print(f"Testing skill: {skill_info['name']}")
    
    try:
        # 检查主要的技能定义文件
        for file_path in skill_info['files']:
            if file_path.suffix == '.md':
                # 尝试读取MD文件
                content = file_path.read_text(encoding='utf-8')
                print(f"  ✓ Loaded {file_path.name}: {len(content)} characters")
            
            elif file_path.suffix == '.py':
                # 尝试导入PY文件
                import importlib.util
                spec = importlib.util.spec_from_file_location(file_path.stem, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                print(f"  ✓ Imported {file_path.name}")
                
        print(f"  Skill {skill_info['name']} loaded successfully!\n")
        return True
        
    except Exception as e:
        print(f"  ✗ Failed to load {skill_info['name']}: {str(e)}\n")
        return False

def run_tests():
    """运行所有测试"""
    print("=" * 60)
    print("Starting comprehensive skill deployment and testing")
    print("=" * 60)
    
    # 设置测试环境
    test_dir = setup_test_environment()
    
    # 发现所有技能
    dist_path = "../dist"
    skills = discover_skills(dist_path)
    
    print(f"\nFound {len(skills)} skills in dist directory:")
    for i, skill in enumerate(skills, 1):
        print(f"  {i}. {skill['name']}")
    
    print("\n" + "=" * 40)
    print("Testing skill loading...")
    print("=" * 40)
    
    # 测试每个技能的加载
    success_count = 0
    total_count = len(skills)
    
    for skill in skills:
        if test_skill_loading(skill):
            success_count += 1
    
    # 总结测试结果
    print("=" * 40)
    print("Test Summary:")
    print(f"  Total skills tested: {total_count}")
    print(f"  Successfully loaded: {success_count}")
    print(f"  Failed to load: {total_count - success_count}")
    print(f"  Success rate: {success_count/total_count*100:.2f}%")
    print("=" * 40)
    
    # 清理测试环境
    if test_dir.exists():
        shutil.rmtree(test_dir)
        print(f"Cleaned up test directory: {test_dir.absolute()}")
    
    print("\nTesting completed!")

if __name__ == "__main__":
    run_tests()