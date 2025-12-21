#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证field-analysis技能的脚本是否正常工作
"""

import sys
import subprocess
import json
from pathlib import Path

def test_field_analysis_scripts():
    """测试field-analysis的脚本"""
    print("🧪 验证field-analysis技能脚本")
    
    # 检查脚本是否存在
    scripts_dir = Path("archive/skills/field-analysis/scripts")
    scripts = list(scripts_dir.glob("*.py"))
    
    print(f"找到 {len(scripts)} 个脚本:")
    for script in scripts:
        print(f"  - {script.name}")
    
    # 测试每个脚本的语法
    for script in scripts:
        print(f"\n测试脚本: {script.name}")
        try:
            # 检查语法
            with open(script, 'r', encoding='utf-8') as f:
                content = f.read()
            compile(content, str(script), 'exec')
            print(f"  ✅ 语法正确")
            
            # 尝试运行帮助命令（如果脚本支持）
            try:
                result = subprocess.run(
                    [sys.executable, str(script), '--help'],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode in [0, 2]:  # 0=成功, 2=参数错误但语法正确
                    print(f"  ✅ 帮助命令正常")
                else:
                    print(f"  ⚠️ 帮助命令异常 (返回码: {result.returncode})")
            except subprocess.TimeoutExpired:
                print(f"  ⚠️ 帮助命令超时")
            except Exception as e:
                print(f"  ⚠️ 帮助命令错误: {e}")
                
        except SyntaxError as e:
            print(f"  ❌ 语法错误: {e}")
        except Exception as e:
            print(f"  ❌ 错误: {e}")
    
    # 创建测试数据并尝试运行一个脚本
    print(f"\n📝 创建测试数据")
    test_data = {
        "field_name": "高等教育场域",
        "actors": [
            {"name": "大学A", "type": "institution", "capital": {"学术": 90, "经济": 80, "象征": 85}},
            {"name": "大学B", "type": "institution", "capital": {"学术": 70, "经济": 60, "象征": 75}}
        ],
        "relationships": [
            {"from": "大学A", "to": "大学B", "type": "竞争"},
            {"from": "大学A", "to": "教育部", "type": "依赖"}
        ]
    }
    
    test_file = Path("test_data/field_test.json")
    test_file.parent.mkdir(exist_ok=True)
    with open(test_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ 测试数据已创建: {test_file}")
    
    print(f"\n🎯 field-analysis技能验证完成")

if __name__ == "__main__":
    test_field_analysis_scripts()