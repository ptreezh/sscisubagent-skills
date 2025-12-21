#!/usr/bin/env python
"""
网络数据处理技能的TDD测试
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

def test_clean_survey_data():
    """测试调查数据清洗功能"""
    print("=== 测试调查数据清洗功能 ===")
    
    script_path = "processing-network-data/scripts/clean_survey_data.py"
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print("❌ clean_survey_data.py 脚本不存在，需要先创建")
        return False
    
    data_file = "survey_data.json"
    
    args = ["--input", data_file, "--output", "cleaned_data.json"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 数据清洗成功")
        
        # 验证输出
        with open("cleaned_data.json", "r", encoding="utf-8") as f:
            output = json.load(f)
        
        summary = output["summary"]
        
        # 断言测试
        assert "n_respondents" in summary, "应包含受访者数量"
        assert "n_valid_respondents" in summary, "应包含有效受访者数量"
        assert summary["n_valid_respondents"] > 0, "有效受访者应大于0"
        
        print(f"  - 原始受访者: {summary.get('n_respondents', 'N/A')} ✓")
        print(f"  - 有效受访者: {summary['n_valid_respondents']} ✓")
        print(f"  - 清洗规则数: {summary.get('n_rules_applied', 'N/A')} ✓")
    else:
        print(f"❌ 数据清洗失败: {result.get('stderr', 'Unknown error')}")
        return False
    
    return True

def test_extract_network_data():
    """测试网络数据提取功能"""
    print("\n=== 测试网络数据提取功能 ===")
    
    script_path = "processing-network-data/scripts/extract_network_data.py"
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print("❌ extract_network_data.py 脚本不存在，需要先创建")
        return False
    
    data_file = "cleaned_data.json"
    
    args = ["--input", data_file, "--output", "network_data.json", "--format", "edgelist"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 网络数据提取成功")
        
        # 验证输出
        with open("network_data.json", "r", encoding="utf-8") as f:
            output = json.load(f)
        
        summary = output["summary"]
        
        # 断言测试
        assert "n_nodes" in summary, "应包含节点数"
        assert "n_edges" in summary, "应包含边数"
        assert summary["n_nodes"] > 0, "节点数应大于0"
        assert summary["n_edges"] > 0, "边数应大于0"
        
        print(f"  - 节点数: {summary['n_nodes']} ✓")
        print(f"  - 边数: {summary['n_edges']} ✓")
        print(f"  - 网络密度: {summary.get('density', 0):.4f} ✓")
    else:
        print(f"❌ 网络数据提取失败: {result.get('stderr', 'Unknown error')}")
        return False
    
    return True

def test_validate_network_data():
    """测试网络数据验证功能"""
    print("\n=== 测试网络数据验证功能 ===")
    
    script_path = "processing-network-data/scripts/validate_network_data.py"
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print("❌ validate_network_data.py 脚本不存在，需要先创建")
        return False
    
    data_file = "network_data.json"
    
    args = ["--input", data_file, "--output", "validation_report.json"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 网络数据验证成功")
        
        # 验证输出
        with open("validation_report.json", "r", encoding="utf-8") as f:
            output = json.load(f)
        
        summary = output["summary"]
        
        # 断言测试
        assert "is_valid" in summary, "应包含有效性标志"
        assert "validation_score" in summary, "应包含验证得分"
        assert "n_checks" in summary, "应包含检查项数"
        
        print(f"  - 有效性: {'是' if summary['is_valid'] else '否'} ✓")
        print(f"  - 验证得分: {summary['validation_score']:.2f} ✓")
        print(f"  - 检查项数: {summary['n_checks']} ✓")
    else:
        print(f"❌ 网络数据验证失败: {result.get('stderr', 'Unknown error')}")
        return False
    
    return True

def test_transform_data_format():
    """测试数据格式转换功能"""
    print("\n=== 测试数据格式转换功能 ===")
    
    script_path = "processing-network-data/scripts/transform_data_format.py"
    
    # 检查脚本是否存在
    if not os.path.exists(script_path):
        print("❌ transform_data_format.py 脚本不存在，需要先创建")
        return False
    
    data_file = "network_data.json"
    
    args = ["--input", data_file, "--output", "adjacency_matrix.json", 
            "--from", "edgelist", "--to", "adjacency"]
    result = run_skill_script(script_path, args)
    
    if result["success"]:
        print("✅ 数据格式转换成功")
        
        # 验证输出
        with open("adjacency_matrix.json", "r", encoding="utf-8") as f:
            output = json.load(f)
        
        summary = output["summary"]
        
        # 断言测试
        assert "matrix_size" in summary, "应包含矩阵大小"
        assert "from_format" in summary, "应包含源格式"
        assert "to_format" in summary, "应包含目标格式"
        assert summary["to_format"] == "adjacency", "目标格式应为adjacency"
        
        print(f"  - 矩阵大小: {summary['matrix_size']}×{summary['matrix_size']} ✓")
        print(f"  - 源格式: {summary['from_format']} ✓")
        print(f"  - 目标格式: {summary['to_format']} ✓")
    else:
        print(f"❌ 数据格式转换失败: {result.get('stderr', 'Unknown error')}")
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
        ("数据清洗", test_clean_survey_data),
        ("网络数据提取", test_extract_network_data),
        ("网络数据验证", test_validate_network_data),
        ("数据格式转换", test_transform_data_format)
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
    print("开始网络数据处理技能TDD测试...")
    print("="*60)
    
    # 切换到测试目录
    test_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(test_dir)
    print(f"测试目录: {test_dir}")
    
    # 检查测试数据
    if not os.path.exists("survey_data.json"):
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
