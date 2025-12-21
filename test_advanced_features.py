#!/usr/bin/env python3
"""
测试高级功能和降级机制

验证脚本：
1. 高级统计分析功能
2. 高级行动者分析功能  
3. 高级引用处理功能
4. 依赖管理器功能
"""

import json
import tempfile
import os
from pathlib import Path


def create_test_data():
    """创建测试数据"""
    # 统计分析测试数据
    stats_data = {
        "variable1": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        "variable2": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
        "group": ["A", "A", "B", "B", "A", "B", "A", "B", "A", "B"]
    }
    
    # 行动者分析测试数据
    ant_data = {
        "text": "张三支持人工智能技术发展，李四与王五合作开发新系统，新技术影响了整个组织。"
    }
    
    # 引用处理测试数据
    citation_data = {
        "citations": [
            "张三. (2020). 人工智能研究. 计算机学报, 43(5): 123-135.",
            "李四. (2021). 机器学习方法. 软件学报, 32(3): 456-468.",
            "张三. (2020). 人工智能研究. 计算机学报, 43(5): 123-135.",  # 重复
            "王五. (2019). 数据分析技术. 统计研究, 36(2): 78-89."
        ]
    }
    
    return stats_data, ant_data, citation_data


def test_statistical_analysis():
    """测试统计分析功能"""
    print("=== 测试统计分析功能 ===")
    
    stats_data, _, _ = create_test_data()
    
    # 创建临时输入文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(stats_data, f, ensure_ascii=False, indent=2)
        input_file = f.name
    
    try:
        # 测试描述性统计
        output_file = input_file.replace('.json', '_desc_output.json')
        cmd = f'python advanced_statistical_analysis.py --input {input_file} --output {output_file} --analysis descriptive --x-column variable1'
        print(f"执行命令: {cmd}")
        os.system(cmd)
        
        # 读取并验证输出
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                print(f"  描述性统计结果: {result['summary']['processing_time']}秒处理时间")
                print(f"  使用高级功能: {result['details'].get('using_advanced', 'N/A')}")
        else:
            print("  错误: 输出文件未生成")
        
        # 测试t检验
        output_file = input_file.replace('.json', '_ttest_output.json')
        cmd = f'python advanced_statistical_analysis.py --input {input_file} --output {output_file} --analysis t_test --x-column variable1 --group-column group'
        print(f"执行命令: {cmd}")
        os.system(cmd)
        
        # 读取并验证输出
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                print(f"  t检验结果: {result['summary']['processing_time']}秒处理时间")
                print(f"  使用高级功能: {result['details'].get('using_advanced', 'N/A')}")
        else:
            print("  错误: t检验输出文件未生成")
    
    finally:
        # 清理临时文件
        os.unlink(input_file)
        for ext in ['_desc_output.json', '_ttest_output.json']:
            output_path = input_file.replace('.json', ext)
            if os.path.exists(output_path):
                os.unlink(output_path)


def test_ant_analysis():
    """测试行动者分析功能"""
    print("\n=== 测试行动者分析功能 ===")
    
    _, ant_data, _ = create_test_data()
    
    # 创建临时输入文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(ant_data, f, ensure_ascii=False, indent=2)
        input_file = f.name
    
    try:
        # 测试行动者识别
        output_file = input_file.replace('.json', '_output.json')
        cmd = f'python advanced_identify_actors.py --input {input_file} --output {output_file}'
        print(f"执行命令: {cmd}")
        os.system(cmd)
        
        # 读取并验证输出
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                print(f"  行动者识别结果: {result['summary']['processing_time']}秒处理时间")
                print(f"  总行动者数: {result['summary']['n_actors']}")
                print(f"  使用高级分析: {result['summary']['using_advanced']}")
        else:
            print("  错误: 输出文件未生成")
    
    finally:
        # 清理临时文件
        os.unlink(input_file)
        output_path = input_file.replace('.json', '_output.json')
        if os.path.exists(output_path):
            os.unlink(output_path)


def test_citation_processing():
    """测试引用处理功能"""
    print("\n=== 测试引用处理功能 ===")
    
    _, _, citation_data = create_test_data()
    
    # 创建临时输入文件
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
        json.dump(citation_data, f, ensure_ascii=False, indent=2)
        input_file = f.name
    
    try:
        # 测试引用处理
        output_file = input_file.replace('.json', '_output.json')
        cmd = f'python advanced_format_citations.py --input {input_file} --output {output_file} --action all'
        print(f"执行命令: {cmd}")
        os.system(cmd)
        
        # 读取并验证输出
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                result = json.load(f)
                print(f"  引用处理结果: {result['summary']['processing_time']}秒处理时间")
                print(f"  总引用数: {result['summary']['total_citations']}")
                print(f"  使用高级分析: {result['summary']['using_advanced']}")
                print(f"  重复引用数: {len(result['details']['duplicates'])}")
        else:
            print("  错误: 输出文件未生成")
    
    finally:
        # 清理临时文件
        os.unlink(input_file)
        output_path = input_file.replace('.json', '_output.json')
        if os.path.exists(output_path):
            os.unlink(output_path)


def test_dependency_manager():
    """测试依赖管理器功能"""
    print("\n=== 测试依赖管理器功能 ===")
    
    # 导入依赖管理器
    import sys
    sys.path.append('D:/stigmergy-CLI-Multi-Agents/sscisubagent-skills/archive/skills/common')
    
    try:
        from dependency_manager import (
            DependencyManager, 
            install_required_packages, 
            get_package_availability,
            install_skill_packages
        )
        
        # 创建依赖管理器实例
        dm = DependencyManager()
        
        # 测试单个包安装
        print("  测试安装numpy:")
        numpy_result = dm.check_and_install('numpy', 'numpy')
        print(f"    numpy安装结果: {'成功' if numpy_result else '失败'}")
        
        # 测试批量包安装
        print("  测试批量安装:")
        packages_to_install = [
            ('pandas', 'pandas'),
            ('requests', 'requests')
        ]
        batch_results = dm.require_packages(packages_to_install)
        for pkg, result in batch_results.items():
            print(f"    {pkg}: {'成功' if result else '失败'}")
        
        # 测试技能包安装
        print("  测试统计技能包安装:")
        stats_results = install_skill_packages('statistics')
        for pkg, result in stats_results.items():
            print(f"    {pkg}: {'成功' if result else '失败'}")
        
        # 显示所有包的可用性
        print("  所有包的可用性:")
        availability = get_package_availability()
        for pkg, available in availability.items():
            print(f"    {pkg}: {'可用' if available else '不可用'}")
    
    except ImportError as e:
        print(f"  无法导入依赖管理器: {e}")
    except Exception as e:
        print(f"  测试依赖管理器时出错: {e}")


def main():
    """主测试函数"""
    print("开始测试高级功能和降级机制...")

    # 更改到适当的目录
    script_dir = Path(__file__).parent
    skills_dir = script_dir / "archive" / "skills"

    # 测试统计分析
    stats_dir = skills_dir / "mathematical-statistics" / "scripts"
    if stats_dir.exists():
        original_dir = os.getcwd()
        os.chdir(stats_dir)
        try:
            test_statistical_analysis()
        finally:
            os.chdir(original_dir)
    else:
        print(f"统计分析脚本目录不存在: {stats_dir}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"尝试的路径: {stats_dir}")

    # 测试行动者分析
    ant_dir = skills_dir / "ant" / "scripts"
    if ant_dir.exists():
        original_dir = os.getcwd()
        os.chdir(ant_dir)
        try:
            test_ant_analysis()
        finally:
            os.chdir(original_dir)
    else:
        print(f"行动者分析脚本目录不存在: {ant_dir}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"尝试的路径: {ant_dir}")

    # 测试引用处理
    writing_dir = skills_dir / "writing" / "scripts"
    if writing_dir.exists():
        original_dir = os.getcwd()
        os.chdir(writing_dir)
        try:
            test_citation_processing()
        finally:
            os.chdir(original_dir)
    else:
        print(f"引用处理脚本目录不存在: {writing_dir}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"尝试的路径: {writing_dir}")

    # 测试依赖管理器
    common_dir = script_dir / "archive" / "skills" / "common"  # 修正路径
    if common_dir.exists():
        original_dir = os.getcwd()
        os.chdir(common_dir)
        try:
            test_dependency_manager()
        finally:
            os.chdir(original_dir)
    else:
        print(f"通用工具目录不存在: {common_dir}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"尝试的路径: {common_dir}")

    print("\n测试完成！")


if __name__ == "__main__":
    main()