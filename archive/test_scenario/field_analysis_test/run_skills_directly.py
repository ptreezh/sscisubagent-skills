#!/usr/bin/env python
"""
直接运行field-analysis技能脚本进行测试
"""
import sys
import os
import json
import subprocess

def run_script(script_path, args):
    """运行Python脚本"""
    cmd = [sys.executable, script_path] + args
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": "Script timed out after 30 seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def test_identify_field_boundary():
    """测试场域边界识别脚本"""
    script_path = "field-analysis/scripts/identify_field_boundary.py"
    data_file_fixed = "test_data_fixed.json"
    
    print("=== 测试identify_field_boundary.py ===")
    
    # 测试基本功能
    args = ["--input", data_file_fixed, "--output", "boundary_output.json"]
    result = run_script(script_path, args)
    
    if result["success"]:
        print("✅ 脚本执行成功")
        print("输出:")
        print(result["stdout"])
        
        # 检查输出文件
        if os.path.exists("boundary_output.json"):
            with open("boundary_output.json", "r", encoding="utf-8") as f:
                output = json.load(f)
            print("\n生成的JSON输出:")
            print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("❌ 脚本执行失败")
        print(f"错误: {result.get('stderr', 'Unknown error')}")
    
    return result

def test_analyze_capital_distribution():
    """测试资本分布分析脚本"""
    script_path = "field-analysis/scripts/analyze_capital_distribution.py"
    data_file_fixed = "test_data_fixed.json"
    
    print("\n=== 测试analyze_capital_distribution.py ===")
    
    args = ["--input", data_file_fixed, "--output", "capital_output.json"]
    result = run_script(script_path, args)
    
    if result["success"]:
        print("✅ 脚本执行成功")
        print("输出:")
        print(result["stdout"])
        
        # 检查输出文件
        if os.path.exists("capital_output.json"):
            with open("capital_output.json", "r", encoding="utf-8") as f:
                output = json.load(f)
            print("\n生成的JSON输出:")
            print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("❌ 脚本执行失败")
        print(f"错误: {result.get('stderr', 'Unknown error')}")
    
    return result

def test_assess_autonomy():
    """测试自主性评估脚本"""
    script_path = "field-analysis/scripts/assess_autonomy.py"
    data_file_fixed = "test_data_fixed.json"
    
    print("\n=== 测试assess_autonomy.py ===")
    
    args = ["--input", data_file_fixed, "--output", "autonomy_output.json"]
    result = run_script(script_path, args)
    
    if result["success"]:
        print("✅ 脚本执行成功")
        print("输出:")
        print(result["stdout"])
        
        # 检查输出文件
        if os.path.exists("autonomy_output.json"):
            with open("autonomy_output.json", "r", encoding="utf-8") as f:
                output = json.load(f)
            print("\n生成的JSON输出:")
            print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("❌ 脚本执行失败")
        print(f"错误: {result.get('stderr', 'Unknown error')}")
    
    return result

def main():
    """主测试函数"""
    print("开始直接测试field-analysis脚本...")
    print("="*60)
    
    # 切换到测试目录
    test_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(test_dir)
    print(f"测试目录: {test_dir}")
    
    # 检查必要文件
    if not os.path.exists("test_data_fixed.json"):
        print("❌ 测试数据文件不存在")
        return
    
    # 运行测试
    results = []
    
    # 测试1: 场域边界识别
    results.append(test_identify_field_boundary())
    
    # 测试2: 资本分布分析
    results.append(test_analyze_capital_distribution())
    
    # 测试3: 自主性评估
    results.append(test_assess_autonomy())
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总:")
    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)
    
    print(f"成功: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("✅ 所有脚本测试通过！")
    else:
        print("❌ 部分脚本测试失败")
        for i, result in enumerate(results, 1):
            status = "✅" if result["success"] else "❌"
            print(f"脚本测试{i}: {status}")

if __name__ == "__main__":
    main()