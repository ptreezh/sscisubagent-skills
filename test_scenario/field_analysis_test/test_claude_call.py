#!/usr/bin/env python
"""
测试通过shell调用Claude来执行field-analysis技能
"""
import subprocess
import json
import os
import sys

def run_claude_with_skill(skill_path, prompt):
    """通过shell调用Claude执行技能"""
    # 构建Claude调用命令
    claude_cmd = [
        "claude",
        f"--skill={skill_path}",
        prompt
    ]
    
    try:
        # 执行命令
        result = subprocess.run(
            claude_cmd,
            capture_output=True,
            text=True,
            timeout=60
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
            "error": "Command timed out after 60 seconds"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def test_field_boundary_identification():
    """测试场域边界识别功能"""
    skill_path = "field-analysis"
    prompt = """请分析这个学术场域的边界：
参与者包括教授、副教授、博士后和研究生，来自北京大学和清华大学。
需要识别核心参与者、场域规则和自主性程度。"""
    
    print("=== 测试场域边界识别 ===")
    print(f"技能路径: {skill_path}")
    print(f"提示词: {prompt}\n")
    
    result = run_claude_with_skill(skill_path, prompt)
    
    if result["success"]:
        print("✅ 调用成功")
        print("输出结果:")
        print(result["stdout"])
    else:
        print("❌ 调用失败")
        print(f"错误: {result.get('error', result.get('stderr', 'Unknown error'))}")
    
    return result

def test_capital_distribution():
    """测试资本分布分析功能"""
    skill_path = "field-analysis"
    prompt = """分析这个学术场域的资本分布：
- 张教授：50篇论文，5个项目，20个合作者
- 李副教授：30篇论文，2个项目，15个合作者
- 王博士：10篇论文，0个项目，8个合作者
- 刘硕士：2篇论文，0个项目，3个合作者

请计算文化资本、社会资本和象征资本的分布情况。"""
    
    print("\n=== 测试资本分布分析 ===")
    print(f"技能路径: {skill_path}")
    print(f"提示词: {prompt}\n")
    
    result = run_claude_with_skill(skill_path, prompt)
    
    if result["success"]:
        print("✅ 调用成功")
        print("输出结果:")
        print(result["stdout"])
    else:
        print("❌ 调用失败")
        print(f"错误: {result.get('error', result.get('stderr', 'Unknown error'))}")
    
    return result

def test_autonomy_assessment():
    """测试自主性评估功能"""
    skill_path = "field-analysis"
    prompt = """评估学术场域的自主性：
外部影响包括：
- 经济压力：0.7
- 政治干预：0.3
- 文化因素：0.5

请分析场域相对于外部力量的自主性程度。"""
    
    print("\n=== 测试自主性评估 ===")
    print(f"技能路径: {skill_path}")
    print(f"提示词: {prompt}\n")
    
    result = run_claude_with_skill(skill_path, prompt)
    
    if result["success"]:
        print("✅ 调用成功")
        print("输出结果:")
        print(result["stdout"])
    else:
        print("❌ 调用失败")
        print(f"错误: {result.get('error', result.get('stderr', 'Unknown error'))}")
    
    return result

def main():
    """主测试函数"""
    print("开始测试field-analysis技能的Claude调用...")
    print("="*60)
    
    # 切换到测试目录
    test_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(test_dir)
    print(f"测试目录: {test_dir}")
    
    # 运行测试
    results = []
    
    # 测试1: 场域边界识别
    results.append(test_field_boundary_identification())
    
    # 测试2: 资本分布分析
    results.append(test_capital_distribution())
    
    # 测试3: 自主性评估
    results.append(test_autonomy_assessment())
    
    # 汇总结果
    print("\n" + "="*60)
    print("测试结果汇总:")
    success_count = sum(1 for r in results if r["success"])
    total_count = len(results)
    
    print(f"成功: {success_count}/{total_count}")
    
    if success_count == total_count:
        print("✅ 所有测试通过！")
    else:
        print("❌ 部分测试失败")
        for i, result in enumerate(results, 1):
            status = "✅" if result["success"] else "❌"
            print(f"测试{i}: {status}")

if __name__ == "__main__":
    main()