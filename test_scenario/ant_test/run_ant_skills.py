#!/usr/bin/env python
"""
运行ANT技能测试
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

def test_identify_participants():
    """测试参与者识别脚本"""
    script_path = "ant/scripts/identify_participants.py"
    data_file = "ant_test_data.json"
    
    print("=== 测试identify_participants.py ===")
    
    args = ["--input", data_file, "--output", "participants_output.json"]
    result = run_script(script_path, args)
    
    if result["success"]:
        print("✅ 脚本执行成功")
        print("输出:")
        print(result["stdout"])
        
        # 检查输出文件
        if os.path.exists("participants_output.json"):
            with open("participants_output.json", "r", encoding="utf-8") as f:
                output = json.load(f)
            print("\n生成的JSON输出:")
            print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("❌ 脚本执行失败")
        print(f"错误: {result.get('stderr', 'Unknown error')}")
    
    return result

def test_analyze_network():
    """测试网络分析脚本"""
    script_path = "ant/scripts/analyze_network.py"
    data_file = "ant_test_data.json"
    
    print("\n=== 测试analyze_network.py ===")
    
    args = ["--input", data_file, "--output", "network_output.json"]
    result = run_script(script_path, args)
    
    if result["success"]:
        print("✅ 脚本执行成功")
        print("输出:")
        print(result["stdout"])
        
        # 检查输出文件
        if os.path.exists("network_output.json"):
            with open("network_output.json", "r", encoding="utf-8") as f:
                output = json.load(f)
            print("\n生成的JSON输出:")
            print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("❌ 脚本执行失败")
        print(f"错误: {result.get('stderr', 'Unknown error')}")
    
    return result

def test_trace_translation():
    """测试转译追踪脚本"""
    script_path = "ant/scripts/trace_translation.py"
    data_file = "ant_test_data.json"
    
    print("\n=== 测试trace_translation.py ===")
    
    args = ["--input", data_file, "--output", "translation_output.json"]
    result = run_script(script_path, args)
    
    if result["success"]:
        print("✅ 脚本执行成功")
        print("输出:")
        print(result["stdout"])
        
        # 检查输出文件
        if os.path.exists("translation_output.json"):
            with open("translation_output.json", "r", encoding="utf-8") as f:
                output = json.load(f)
            print("\n生成的JSON输出:")
            print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print("❌ 脚本执行失败")
        print(f"错误: {result.get('stderr', 'Unknown error')}")
    
    return result

def main():
    """主测试函数"""
    print("开始测试ANT技能脚本...")
    print("="*60)
    
    # 切换到测试目录
    test_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(test_dir)
    print(f"测试目录: {test_dir}")
    
    # 检查必要文件
    if not os.path.exists("ant_test_data.json"):
        print("❌ 测试数据文件不存在")
        return
    
    # 运行测试
    results = []
    
    # 测试1: 参与者识别
    results.append(test_identify_participants())
    
    # 测试2: 网络分析
    results.append(test_analyze_network())
    
    # 测试3: 转译追踪
    results.append(test_trace_translation())
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总:")
    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)
    
    print(f"成功: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("✅ 所有ANT技能测试通过！")
    else:
        print("❌ 部分ANT技能测试失败")
        for i, result in enumerate(results, 1):
            status = "✅" if result["success"] else "❌"
            print(f"技能测试{i}: {status}")

if __name__ == "__main__":
    main()