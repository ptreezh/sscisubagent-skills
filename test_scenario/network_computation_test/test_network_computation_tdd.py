#!/usr/bin/env python
"""
网络计算技能的TDD测试
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

def test_build_network():
    """测试网络构建功能"""
    print("=== 测试网络构建功能 ===")
    
    script_path = "performing-network-computation/scripts/build_network.py"
    data_file = "social_network_data.json"
    
    # 测试1: 边列表构建
    print("\n测试1.1: 边列表构建网络")
    args = ["--input", data_file, "--output", "network_edgelist.json", "--type", "edgelist"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 边列表构建成功")
        
        # 验证输出
        with open("network_edgelist.json", "r", encoding="utf-8") as f:
            output = json.load(f)
        
        summary = output["summary"]
        details = output["details"]
        
        # 断言测试
        assert summary["n_nodes"] == 11, f"节点数应为11，实际为{summary['n_nodes']}"
        assert summary["n_edges"] == 14, f"边数应为14（去重后），实际为{summary['n_edges']}"
        assert summary["density"] > 0, "网络密度应大于0"
        assert details["validation"]["is_valid"], "网络应该是有效的"
        
        print(f"  - 节点数: {summary['n_nodes']} ✓")
        print(f"  - 边数: {summary['n_edges']} ✓")
        print(f"  - 密度: {summary['density']:.4f} ✓")
    else:
        print(f"❌ 边列表构建失败: {result.get('stderr', 'Unknown error')}")
        return False
    
    # 测试2: 带清理的网络构建
    print("\n测试1.2: 带清理的网络构建")
    args = ["--input", data_file, "--output", "network_cleaned.json", 
            "--type", "edgelist", "--remove-isolates", "--remove-self-loops"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 网络清理成功")
    else:
        print(f"❌ 网络清理失败: {result.get('stderr', 'Unknown error')}")
        return False
    
    return True

def test_calculate_metrics():
    """测试网络指标计算"""
    print("\n=== 测试网络指标计算 ===")
    
    # 先创建指标计算脚本
    script_path = "performing-network-computation/scripts/calculate_metrics.py"
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print("❌ calculate_metrics.py 脚本不存在，需要先创建")
        return False
    
    data_file = "network_edgelist.json"
    
    args = ["--input", data_file, "--output", "metrics.json"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 指标计算成功")
        
        # 验证输出
        with open("metrics.json", "r", encoding="utf-8") as f:
            output = json.load(f)
        
        summary = output["summary"]
        
        # 断言关键指标
        assert "basic_metrics" in summary, "应包含基础指标"
        assert "centrality_metrics" in summary, "应包含中心性指标"
        assert summary["n_nodes"] > 0, "节点数应大于0"
        
        print(f"  - 基础指标: 已计算 ✓")
        print(f"  - 中心性指标: 已计算 ✓")
        print(f"  - 处理节点数: {summary['n_nodes']} ✓")
    else:
        print(f"❌ 指标计算失败: {result.get('stderr', 'Unknown error')}")
        return False
    
    return True

def test_detect_communities():
    """测试社区检测"""
    print("\n=== 测试社区检测 ===")
    
    script_path = "performing-network-computation/scripts/detect_communities.py"
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print("❌ detect_communities.py 脚本不存在，需要先创建")
        return False
    
    data_file = "network_edgelist.json"
    
    args = ["--input", data_file, "--output", "communities.json", "--method", "louvain"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 社区检测成功")
        
        # 验证输出
        with open("communities.json", "r", encoding="utf-8") as f:
            output = json.load(f)
        
        summary = output["summary"]
        
        # 断言社区检测结果
        assert "n_communities" in summary, "应包含社区数量"
        assert "modularity" in summary, "应包含模块度"
        assert summary["n_communities"] > 0, "社区数量应大于0"
        
        print(f"  - 检测到社区数: {summary['n_communities']} ✓")
        print(f"  - 模块度: {summary.get('modularity', 0):.4f} ✓")
    else:
        print(f"❌ 社区检测失败: {result.get('stderr', 'Unknown error')}")
        return False
    
    return True

def test_visualize_network():
    """测试网络可视化"""
    print("\n=== 测试网络可视化 ===")
    
    script_path = "performing-network-computation/scripts/visualize_network.py"
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print("❌ visualize_network.py 脚本不存在，需要先创建")
        return False
    
    data_file = "network_edgelist.json"
    
    args = ["--input", data_file, "--output", "network_visualization.png", 
            "--layout", "spring", "--color-by", "centrality"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 网络可视化成功")
        
        # 检查输出文件
        if os.path.exists("network_visualization.png"):
            print("  - 可视化文件已生成 ✓")
        else:
            print("⚠️ 可视化文件未找到")
    else:
        print(f"❌ 网络可视化失败: {result.get('stderr', 'Unknown error')}")
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
        ("网络构建", test_build_network),
        ("指标计算", test_calculate_metrics),
        ("社区检测", test_detect_communities),
        ("网络可视化", test_visualize_network)
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
    print("开始网络计算技能TDD测试...")
    print("="*60)
    
    # 切换到测试目录
    test_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(test_dir)
    print(f"测试目录: {test_dir}")
    
    # 检查测试数据
    if not os.path.exists("social_network_data.json"):
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