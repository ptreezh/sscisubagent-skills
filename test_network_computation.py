#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络计算分析技能测试
测试网络计算分析技能的基本功能
"""

import sys
import os
from pathlib import Path

# 添加脚本路径到系统路径
script_path = Path("skills/network-computation/scripts")
sys.path.insert(0, str(script_path))

def test_network_computation_basic():
    """测试网络计算分析技能的基本功能"""
    print("🧪 测试网络计算分析技能 - 基本功能")
    
    # 检查脚本是否存在
    script_path = Path("skills/network-computation/scripts/calculate_centrality.py")
    if not script_path.exists():
        print("❌ 脚本文件不存在")
        return False
    
    print(f"✅ 脚本存在: {script_path}")
    
    # 尝试导入脚本而不执行
    try:
        # 读取脚本内容
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查基本语法
        basic_imports = [
            "import networkx as nx",
            "import argparse",
            "import json"
        ]
        
        for imp in basic_imports:
            if imp in content:
                print(f"✅ 找到基本依赖: {imp}")
            else:
                print(f"⚠️  未找到基本依赖: {imp}")
        
        # 检查主要函数是否存在
        main_functions = [
            "def load_network",
            "def calculate_all_centralities",
            "def rank_nodes",
            "def identify_key_nodes"
        ]
        
        for func in main_functions:
            if func in content:
                print(f"✅ 找到主要函数: {func}")
            else:
                print(f"⚠️  未找到主要函数: {func}")
        
        # 检查主函数
        if "def main():" in content:
            print("✅ 找到主函数")
        else:
            print("❌ 未找到主函数")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ 导入脚本时出错: {e}")
        return False

def test_network_data_creation():
    """测试网络数据创建"""
    print("\n🧪 测试网络数据创建")
    
    import json
    
    # 创建测试网络数据
    test_network = {
        "nodes": ["A", "B", "C", "D", "E", "F", "G", "H"],
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "A", "target": "C"},
            {"source": "B", "target": "C"},
            {"source": "B", "target": "D"},
            {"source": "C", "target": "D"},
            {"source": "D", "target": "E"},
            {"source": "E", "target": "F"},
            {"source": "F", "target": "G"},
            {"source": "G", "target": "H"},
            {"source": "H", "target": "A"},
            {"source": "C", "target": "F"}
        ]
    }
    
    # 保存测试网络数据
    test_data_path = Path("test_data/network_test.json")
    test_data_path.parent.mkdir(exist_ok=True)
    with open(test_data_path, 'w', encoding='utf-8') as f:
        json.dump(test_network, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 创建网络测试数据: {test_data_path}")
    print(f"📊 节点数: {len(test_network['nodes'])}")
    print(f"📊 边数: {len(test_network['edges'])}")
    
    return True

def run_network_computation_tests():
    """运行网络计算分析技能测试"""
    print("🚀 开始测试网络计算分析技能")
    print("="*50)
    
    success = True
    
    # 测试基本功能
    if not test_network_computation_basic():
        success = False
        print("❌ 基本功能测试失败")
    
    # 测试网络数据创建
    if not test_network_data_creation():
        success = False
        print("❌ 网络数据创建测试失败")
    
    print("="*50)
    if success:
        print("✅ 网络计算分析技能测试通过")
    else:
        print("❌ 网络计算分析技能测试失败")
    
    return success

if __name__ == "__main__":
    run_network_computation_tests()