#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能调用测试
测试所有技能的调用接口和基本功能
"""

import sys
import subprocess
import json
from pathlib import Path

def test_script_interface(script_path, help_args=['--help']):
    """测试脚本接口"""
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)] + help_args,
            capture_output=True,
            text=True,
            timeout=10
        )
        
        success = result.returncode in [0, 2]  # 0=成功, 2=参数错误但语法正确
        output = result.stdout or result.stderr
        
        return success, output, result.returncode
    except subprocess.TimeoutExpired:
        return False, "Timeout", -1
    except Exception as e:
        return False, str(e), -1

def run_math_stats_invocation_test():
    """运行数学统计技能调用测试"""
    print("🧪 调用测试: 数学统计技能")
    
    script_path = Path("skills/mathematical-statistics/scripts/statistics_toolkit.py")
    if script_path.exists():
        success, output, code = test_script_interface(script_path)
        if success:
            print(f"  ✅ 接口正常 (返回码: {code})")
            if "Social Science Statistics" in output or "statistics" in output.lower():
                print("  ✅ 功能标识正确")
            else:
                print("  ⚠️  未找到功能标识")
        else:
            print(f"  ❌ 接口异常 (返回码: {code}, 错误: {output})")
    else:
        print("  ❌ 脚本不存在")
    
    return True

def run_validity_reliability_invocation_test():
    """运行信度效度技能调用测试"""
    print("🧪 调用测试: 信度效度分析技能")
    
    script_path = Path("skills/validity-reliability/scripts/validity_reliability_toolkit.py")
    if script_path.exists():
        success, output, code = test_script_interface(script_path)
        if success:
            print(f"  ✅ 接口正常 (返回码: {code})")
            if "Validity and Reliability" in output or "reliability" in output.lower():
                print("  ✅ 功能标识正确")
            else:
                print("  ⚠️  未找到功能标识")
        else:
            print(f"  ❌ 接口异常 (返回码: {code}, 错误: {output})")
    else:
        print("  ❌ 脚本不存在")
    
    return True

def run_network_computation_invocation_test():
    """运行网络计算技能调用测试"""
    print("🧪 调用测试: 网络计算分析技能")
    
    script_path = Path("skills/network-computation/scripts/calculate_centrality.py")
    if script_path.exists():
        success, output, code = test_script_interface(script_path)
        if success:
            print(f"  ✅ 接口正常 (返回码: {code})")
            if "中心性" in output or "centrality" in output.lower():
                print("  ✅ 功能标识正确")
            else:
                print("  ⚠️  未找到功能标识")
            
            # 测试使用实际数据
            network_data = Path("test_data/network_test.json")
            if network_data.exists():
                try:
                    result = subprocess.run([
                        sys.executable, str(script_path), 
                        "--input", str(network_data),
                        "--output", "test_output_centrality.json"
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        print("  ✅ 实际数据处理成功")
                        output_file = Path("test_output_centrality.json")
                        if output_file.exists():
                            with open(output_file, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                print(f"    📊 节点数: {data.get('summary', {}).get('total_nodes', 'N/A')}")
                                print(f"    📊 边数: {data.get('summary', {}).get('total_edges', 'N/A')}")
                            output_file.unlink()  # 删除测试输出文件
                        else:
                            print("    ⚠️  未生成输出文件")
                    else:
                        print(f"  ⚠️  实际数据处理失败 (返回码: {result.returncode})")
                        print(f"    错误: {result.stderr[:200]}...")
                except subprocess.TimeoutExpired:
                    print("  ⚠️  实际数据处理超时")
                except Exception as e:
                    print(f"  ⚠️  实际数据处理异常: {e}")
        else:
            print(f"  ❌ 接口异常 (返回码: {code}, 错误: {output})")
    else:
        print("  ❌ 脚本不存在")
    
    return True

def run_skill_documentation_test():
    """测试技能文档完整性"""
    print("🧪 文档测试: 技能文档完整性")
    
    skills_to_test = [
        ("mathematical-statistics", "数学统计"),
        ("validity-reliability", "信度效度"),
        ("network-computation", "网络计算"),
        ("field-analysis", "场域分析"),
        ("ant", "行动者网络理论")
    ]
    
    for skill_dir, skill_name in skills_to_test:
        skill_path = Path(f"skills/{skill_dir}/SKILL.md")
        if skill_path.exists():
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 检查必要部分
            has_name = 'name:' in content
            has_description = 'description:' in content
            has_overview = '## Overview' in content
            has_usage = '## When to Use This Skill' in content
            
            if has_name and has_description and has_overview and has_usage:
                print(f"  ✅ {skill_name} 技能文档完整")
            else:
                missing = []
                if not has_name: missing.append("name")
                if not has_description: missing.append("description") 
                if not has_overview: missing.append("overview")
                if not has_usage: missing.append("usage")
                print(f"  ⚠️  {skill_name} 技能文档缺少: {', '.join(missing)}")
        else:
            print(f"  ❌ {skill_name} 技能文档不存在")
    
    return True

def run_full_invocation_tests():
    """运行完整调用测试"""
    print("🚀 开始执行技能调用测试")
    print("="*50)
    
    # 运行各项测试
    run_math_stats_invocation_test()
    print()
    
    run_validity_reliability_invocation_test()
    print()
    
    run_network_computation_invocation_test()
    print()
    
    run_skill_documentation_test()
    print()
    
    print("="*50)
    print("✅ 技能调用测试完成")

if __name__ == "__main__":
    run_full_invocation_tests()