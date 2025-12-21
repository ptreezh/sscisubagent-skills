#!/usr/bin/env python
"""
冲突解决技能的TDD测试
基于中文社会科学研究场景的测试驱动开发
"""
import sys
import os
import json
import subprocess
from datetime import datetime

def run_skill_script(script_path, args):
    """运行技能脚本"""
    cmd = [sys.executable, script_path] + args
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30,
            encoding='utf-8'
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
            "error": "脚本执行超时"
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def test_identify_conflicts():
    """测试冲突识别功能"""
    print("=== 测试冲突识别功能 ===")
    
    script_path = "conflict-resolution/scripts/identify_conflicts.py"
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print("❌ identify_conflicts.py 脚本不存在，需要先创建")
        return False
    
    data_file = "research_conflicts.json"
    
    args = ["--input", data_file, "--output", "identified_conflicts.json"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 冲突识别成功")
        
        # 验证输出
        with open("identified_conflicts.json", "r", encoding="utf-8") as f:
            output = json.load(f)
        
        summary = output["summary"]
        
        # 断言测试
        assert "n_conflicts" in summary, "应包含冲突数量"
        assert "conflict_types" in summary, "应包含冲突类型"
        assert summary["n_conflicts"] > 0, "冲突数应大于0"
        
        print(f"  - 识别冲突数: {summary['n_conflicts']} ✓")
        print(f"  - 冲突类型: {summary.get('conflict_types', 'N/A')} ✓")
    else:
        print(f"❌ 冲突识别失败: {result.get('stderr', 'Unknown error')}")
        return False
    
    return True

def test_analyze_conflict_dynamics():
    """测试冲突动态分析功能"""
    print("\n=== 测试冲突动态分析功能 ===")
    
    script_path = "conflict-resolution/scripts/analyze_conflict_dynamics.py"
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print("❌ analyze_conflict_dynamics.py 脚本不存在，需要先创建")
        return False
    
    data_file = "identified_conflicts.json"
    
    args = ["--input", data_file, "--output", "conflict_dynamics.json"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 冲突动态分析成功")
        
        # 验证输出
        with open("conflict_dynamics.json", "r", encoding="utf-8") as f:
            output = json.load(f)
        
        summary = output["summary"]
        
        # 断言测试
        assert "n_analyzed" in summary, "应包含分析数量"
        assert "avg_difficulty" in summary, "应包含解决难度"
        assert summary["n_analyzed"] > 0, "分析的冲突数应大于0"
        
        print(f"  - 分析冲突数: {summary.get('n_analyzed', 'N/A')} ✓")
        print(f"  - 平均强度: {summary.get('avg_intensity', 'N/A')} ✓")
    else:
        print(f"❌ 冲突动态分析失败: {result.get('stderr', 'Unknown error')}")
        return False
    
    return True

def test_generate_resolution_strategies():
    """测试解决策略生成功能"""
    print("\n=== 测试解决策略生成功能 ===")
    
    script_path = "conflict-resolution/scripts/generate_resolution_strategies.py"
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print("❌ generate_resolution_strategies.py 脚本不存在，需要先创建")
        return False
    
    data_file = "conflict_dynamics.json"
    
    # 检查输入文件是否存在
    if not os.path.exists(data_file):
        print(f"❌ 输入文件不存在: {data_file}")
        return False
    
    args = ["--input", data_file, "--output", "resolution_strategies.json"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 解决策略生成成功")
        
        # 验证输出
        with open("resolution_strategies.json", "r", encoding="utf-8") as f:
            output = json.load(f)
        
        summary = output["summary"]
        
        # 断言测试
        assert "n_strategies" in summary, "应包含策略数量"
        assert "strategy_types" in summary, "应包含策略类型"
        assert summary["n_strategies"] > 0, "策略数应大于0"
        
        print(f"  - 生成策略数: {summary['n_strategies']} ✓")
        print(f"  - 策略类型: {summary.get('strategy_types', 'N/A')} ✓")
    else:
        print(f"❌ 解决策略生成失败: {result.get('stderr', 'Unknown error')}")
        return False
    
    return True

def test_facilitate_consensus():
    """测试共识促进功能"""
    print("\n=== 测试共识促进功能 ===")
    
    script_path = "conflict-resolution/scripts/facilitate_consensus.py"
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print("❌ facilitate_consensus.py 脚本不存在，需要先创建")
        return False
    
    data_file = "resolution_strategies.json"
    
    # 检查输入文件是否存在
    if not os.path.exists(data_file):
        print(f"❌ 输入文件不存在: {data_file}")
        return False
    
    args = ["--input", data_file, "--output", "consensus_plan.json"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 共识促进成功")
        
        # 验证输出
        with open("consensus_plan.json", "r", encoding="utf-8") as f:
            output = json.load(f)
        
        summary = output["summary"]
        
        # 断言测试
        assert "consensus_likelihood" in summary, "应包含共识可能性"
        assert "n_steps" in summary, "应包含步骤数"
        assert summary["n_steps"] > 0, "步骤数应大于0"
        
        print(f"  - 共识可能性: {summary.get('consensus_likelihood', 'N/A')} ✓")
        print(f"  - 建议步骤数: {summary['n_steps']} ✓")
    else:
        print(f"❌ 共识促进失败: {result.get('stderr', 'Unknown error')}")
        return False
    
    return True

def generate_report():
    """生成测试报告"""
    print("\n" + "="*60)
    print("测试报告")
    print("="*60)
    
    report = {
        "test_time": datetime.now().isoformat(),
        "test_results": [],
        "summary": {}
    }
    
    # 运行所有测试
    tests = [
        ("冲突识别", test_identify_conflicts),
        ("冲突动态分析", test_analyze_conflict_dynamics),
        ("解决策略生成", test_generate_resolution_strategies),
        ("共识促进", test_facilitate_consensus)
    ]
    
    passed = 0
    for test_name, test_func in tests:
        print(f"\n运行测试: {test_name}")
        try:
            if test_func():
                passed += 1
                report["test_results"].append({
                    "test": test_name,
                    "status": "PASSED",
                    "error": None
                })
            else:
                report["test_results"].append({
                    "test": test_name,
                    "status": "FAILED",
                    "error": "测试执行失败"
                })
        except Exception as e:
            print(f"❌ 测试异常: {e}")
            report["test_results"].append({
                "test": test_name,
                "status": "ERROR",
                "error": str(e)
            })
    
    # 汇总
    total = len(tests)
    report["summary"] = {
        "total": total,
        "passed": passed,
        "failed": total - passed,
        "pass_rate": f"{passed/total*100:.1f}%"
    }
    
    print("\n" + "="*60)
    print("测试汇总:")
    print(f"总测试数: {total}")
    print(f"通过: {passed}")
    print(f"失败: {total - passed}")
    print(f"通过率: {passed/total*100:.1f}%")
    
    # 保存报告
    with open("test_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    return passed == total

def main():
    """主函数"""
    print("开始冲突解决技能TDD测试...")
    print("="*60)
    
    # 切换到测试目录
    test_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(test_dir)
    print(f"测试目录: {test_dir}")
    
    # 检查测试数据
    if not os.path.exists("research_conflicts.json"):
        print("❌ 测试数据文件不存在")
        return
    
    # 生成测试报告
    success = generate_report()
    
    if success:
        print("\n✅ 所有测试通过！")
    else:
        print("\n❌ 部分测试失败，需要完善脚本实现")

if __name__ == "__main__":
    main()