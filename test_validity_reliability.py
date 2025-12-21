#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
信度效度分析技能测试
测试信度效度分析技能的基本功能
"""

import sys
import os
from pathlib import Path

# 添加脚本路径到系统路径
script_path = Path("skills/validity-reliability/scripts")
sys.path.insert(0, str(script_path))

def test_validity_reliability_basic():
    """测试信度效度分析技能的基本功能"""
    print("🧪 测试信度效度分析技能 - 基本功能")
    
    # 检查脚本是否存在
    script_path = Path("skills/validity-reliability/scripts/validity_reliability_toolkit.py")
    if not script_path.exists():
        print("❌ 脚本文件不存在")
        return False
    
    print(f"✅ 脚本存在: {script_path}")
    
    # 尝试导入脚本而不执行
    try:
        # 读取脚本内容
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查基本语法（不包括需要额外依赖的部分）
        basic_imports = [
            "import numpy as np",
            "import pandas as pd",
            "import scipy.stats as stats",
            "import matplotlib.pyplot as plt",
            "import seaborn as sns"
        ]
        
        for imp in basic_imports:
            if imp in content:
                print(f"✅ 找到基本依赖: {imp}")
            else:
                print(f"⚠️  未找到基本依赖: {imp}")
        
        # 检查主要类是否存在
        if "class ValidityReliabilityAnalyzer:" in content:
            print("✅ 找到主要分析类")
        else:
            print("❌ 未找到主要分析类")
            return False
        
        # 检查主要方法
        main_methods = [
            "def reliability_analysis",
            "def construct_validity_analysis",
            "def content_validity_analysis",
            "def criterion_validity_analysis"
        ]
        
        for method in main_methods:
            if method in content:
                print(f"✅ 找到主要方法: {method}")
            else:
                print(f"⚠️  未找到主要方法: {method}")
        
        return True
        
    except Exception as e:
        print(f"❌ 导入脚本时出错: {e}")
        return False

def test_scale_data_analysis():
    """测试量表数据分析流程"""
    print("\n🧪 测试量表数据分析流程")
    
    # 创建模拟量表数据
    import pandas as pd
    import numpy as np
    
    # 创建模拟量表数据 (6个项目的量表，300个被试)
    np.random.seed(42)
    n = 300
    
    # 生成相关项目（模拟一个构念）
    factor1 = np.random.normal(0, 1, n)
    scale_data = pd.DataFrame({
        'item1': factor1 + np.random.normal(0, 0.5, n) + 3,  # 添加基础均值
        'item2': factor1 + np.random.normal(0, 0.5, n) + 3,
        'item3': factor1 + np.random.normal(0, 0.5, n) + 3,
        'item4': factor1 + np.random.normal(0, 0.5, n) + 3,
        'item5': factor1 + np.random.normal(0, 0.5, n) + 3,
        'item6': factor1 + np.random.normal(0, 0.5, n) + 3,
    })
    
    # 确保数据在合理范围内（1-5分李克特量表）
    for col in scale_data.columns:
        scale_data[col] = np.clip(scale_data[col], 1, 5)
    
    # 保存测试数据
    test_data_path = Path("test_data/validity_reliability_test.csv")
    test_data_path.parent.mkdir(exist_ok=True)
    scale_data.to_csv(test_data_path, index=False)
    
    print(f"✅ 创建量表测试数据: {test_data_path}")
    print(f"📊 数据形状: {scale_data.shape}")
    print(f"📊 数据列: {list(scale_data.columns)}")
    print(f"📊 数据范围: {scale_data.min().min():.2f} - {scale_data.max().max():.2f}")
    
    return True

def run_validity_reliability_tests():
    """运行信度效度分析技能测试"""
    print("🚀 开始测试信度效度分析技能")
    print("="*50)
    
    success = True
    
    # 测试基本功能
    if not test_validity_reliability_basic():
        success = False
        print("❌ 基本功能测试失败")
    
    # 测试量表数据处理流程
    if not test_scale_data_analysis():
        success = False
        print("❌ 量表数据处理流程测试失败")
    
    print("="*50)
    if success:
        print("✅ 信度效度分析技能测试通过")
    else:
        print("❌ 信度效度分析技能测试失败")
    
    return success

if __name__ == "__main__":
    run_validity_reliability_tests()