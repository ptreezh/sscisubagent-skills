"""
端到端测试脚本

验证所有高级功能和降级机制的完整工作流程
"""

import json
import tempfile
import os
from pathlib import Path
import subprocess
import sys


def test_end_to_end():
    """端到端测试"""
    print("=== 端到端测试开始 ===")

    script_dir = Path(__file__).parent

    # 1. 测试高级统计分析
    print("\n1. 测试高级统计分析功能:")

    # 创建测试数据
    stats_data = {
        "variable1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "variable2": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
        "group": ["A", "A", "B", "B", "A", "B", "A", "B", "A", "B"]
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(stats_data, f, ensure_ascii=False, indent=2)
        stats_input = f.name

    stats_output = stats_input.replace('.json', '_output.json')

    # 切换到统计分析脚本目录并执行
    stats_script_dir = script_dir / "archive" / "skills" / "mathematical-statistics" / "scripts"
    original_dir = os.getcwd()
    os.chdir(stats_script_dir)

    cmd = f'python advanced_statistical_analysis.py --input {Path(stats_input).name} --output {Path(stats_output).name} --analysis descriptive --x-column variable1'
    print(f"   执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # 检查结果
    os.chdir(original_dir)  # 切换回原目录以访问输出文件
    if os.path.exists(stats_output):
        with open(stats_output, 'r', encoding='utf-8') as f:
            result_data = json.load(f)
            print(f"   ✓ 统计分析成功 - 使用高级功能: {result_data['details'].get('using_advanced', False)}")
            print(f"   ✓ 处理时间: {result_data['summary']['processing_time']}秒")
    else:
        print("   ✗ 统计分析失败 - 输出文件未生成")
        print(f"   命令输出: {result.stdout}")
        print(f"   命令错误: {result.stderr}")

    # 2. 测试行动者分析
    print("\n2. 测试行动者分析功能:")

    ant_data = {
        "text": "张三支持人工智能技术发展，李四与王五合作开发新系统，新技术影响了整个组织。"
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(ant_data, f, ensure_ascii=False, indent=2)
        ant_input = f.name

    ant_output = ant_input.replace('.json', '_output.json')

    # 切换到行动者分析脚本目录并执行
    ant_script_dir = script_dir / "archive" / "skills" / "ant" / "scripts"
    os.chdir(ant_script_dir)

    cmd = f'python advanced_identify_actors.py --input {Path(ant_input).name} --output {Path(ant_output).name}'
    print(f"   执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # 检查结果
    os.chdir(original_dir)  # 切换回原目录以访问输出文件
    if os.path.exists(ant_output):
        with open(ant_output, 'r', encoding='utf-8') as f:
            result_data = json.load(f)
            print(f"   ✓ 行动者分析成功 - 使用高级分析: {result_data['summary']['using_advanced']}")
            print(f"   ✓ 总行动者数: {result_data['summary']['n_actors']}")
            print(f"   ✓ 处理时间: {result_data['summary']['processing_time']}秒")
    else:
        print("   ✗ 行动者分析失败 - 输出文件未生成")
        print(f"   命令输出: {result.stdout}")
        print(f"   命令错误: {result.stderr}")

    # 3. 测试引用处理
    print("\n3. 测试引用处理功能:")

    citation_data = {
        "citations": [
            "张三. (2020). 人工智能研究. 计算机学报, 43(5): 123-135.",
            "李四. (2021). 机器学习方法. 软件学报, 32(3): 456-468.",
            "张三. (2020). 人工智能研究. 计算机学报, 43(5): 123-135.",  # 重复
            "王五. (2019). 数据分析技术. 统计研究, 36(2): 78-89."
        ]
    }

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(citation_data, f, ensure_ascii=False, indent=2)
        cit_input = f.name

    cit_output = cit_input.replace('.json', '_output.json')

    # 切换到引用处理脚本目录并执行
    cit_script_dir = script_dir / "archive" / "skills" / "writing" / "scripts"
    os.chdir(cit_script_dir)

    cmd = f'python advanced_format_citations.py --input {Path(cit_input).name} --output {Path(cit_output).name} --action all'
    print(f"   执行: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    # 检查结果
    os.chdir(original_dir)  # 切换回原目录以访问输出文件
    if os.path.exists(cit_output):
        with open(cit_output, 'r', encoding='utf-8') as f:
            result_data = json.load(f)
            print(f"   ✓ 引用处理成功 - 使用高级分析: {result_data['summary']['using_advanced']}")
            print(f"   ✓ 总引用数: {result_data['summary']['total_citations']}")
            print(f"   ✓ 重复引用数: {len(result_data['details']['duplicates'])}")
            print(f"   ✓ 处理时间: {result_data['summary']['processing_time']}秒")
    else:
        print("   ✗ 引用处理失败 - 输出文件未生成")
        print(f"   命令输出: {result.stdout}")
        print(f"   命令错误: {result.stderr}")

    # 4. 测试依赖管理器
    print("\n4. 测试依赖管理器功能:")

    # 切换到依赖管理器目录
    dep_manager_dir = script_dir / "archive" / "skills" / "common"
    os.chdir(dep_manager_dir)

    try:
        sys.path.insert(0, str(dep_manager_dir))
        from dependency_manager import DependencyManager, with_fallback, requires_dependencies

        # 创建依赖管理器实例
        dm = DependencyManager()

        # 测试包安装
        numpy_ok = dm.check_and_install('numpy', 'numpy')
        pandas_ok = dm.check_and_install('pandas', 'pandas')

        print(f"   ✓ NumPy 可用: {numpy_ok}")
        print(f"   ✓ Pandas 可用: {pandas_ok}")

        # 测试装饰器功能
        def basic_sum(data):
            return sum(data) if data else 0

        @requires_dependencies('numpy')
        def advanced_sum(data):
            import numpy as np
            return float(np.sum(data))

        @with_fallback(basic_sum)
        def smart_sum(data):
            return advanced_sum(data)

        # 测试智能函数
        test_data = [1, 2, 3, 4, 5]
        result = smart_sum(test_data)
        expected = sum(test_data)
        print(f"   ✓ 智能求和函数: {result} (期望: {expected}) - {'正确' if result == expected else '错误'}")

    except Exception as e:
        print(f"   ✗ 依赖管理器测试失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        os.chdir(original_dir)

    # 清理临时文件
    for file_path in [stats_input, stats_output, ant_input, ant_output, cit_input, cit_output]:
        if os.path.exists(file_path):
            os.unlink(file_path)

    print("\n=== 端到端测试完成 ===")


if __name__ == "__main__":
    # 执行测试
    test_end_to_end()