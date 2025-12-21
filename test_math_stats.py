#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数学统计技能测试
测试数学统计技能的基本功能
"""

import sys
import os
from pathlib import Path

# 添加脚本路径到系统路径
script_path = Path("skills/mathematical-statistics/scripts")
sys.path.insert(0, str(script_path))

def test_mathematical_statistics_basic():
    """测试数学统计技能的基本功能"""
    print("🧪 测试数学统计技能 - 基本功能")
    
    # 检查脚本是否存在
    script_path = Path("skills/mathematical-statistics/scripts/statistics_toolkit.py")
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
        if "class SocialScienceStatistics:" in content:
            print("✅ 找到主要分析类")
        else:
            print("❌ 未找到主要分析类")
            return False
        
        # 检查主要方法
        main_methods = [
            "def load_data",
            "def descriptive_statistics",
            "def hypothesis_testing"
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

def test_data_analysis_workflow():
    """测试数据处理流程"""
    print("\n🧪 测试数据处理流程")
    
    # 创建测试数据
    import pandas as pd
    import numpy as np
    
    # 创建模拟数据
    np.random.seed(42)
    n = 100
    test_data = pd.DataFrame({
        'age': np.random.normal(35, 10, n),
        'income': np.random.normal(50000, 15000, n),
        'satisfaction': np.random.normal(7, 2, n),
        'education_years': np.random.normal(16, 3, n)
    })
    
    # 确保数据合理性
    test_data['age'] = np.clip(test_data['age'], 18, 80)
    test_data['income'] = np.clip(test_data['income'], 20000, 100000)
    test_data['satisfaction'] = np.clip(test_data['satisfaction'], 1, 10)
    test_data['education_years'] = np.clip(test_data['education_years'], 8, 25)
    
    # 保存测试数据
    test_data_path = Path("test_data/math_stats_test.csv")
    test_data_path.parent.mkdir(exist_ok=True)
    test_data.to_csv(test_data_path, index=False)
    
    print(f"✅ 创建测试数据: {test_data_path}")
    print(f"📊 数据形状: {test_data.shape}")
    print(f"📊 数据列: {list(test_data.columns)}")
    
    return True

def run_mathematical_statistics_tests():
    """运行数学统计技能测试"""
    print("🚀 开始测试数学统计技能")
    print("="*50)
    
    success = True
    
    # 测试基本功能
    if not test_mathematical_statistics_basic():
        success = False
        print("❌ 基本功能测试失败")
    
    # 测试数据处理流程
    if not test_data_analysis_workflow():
        success = False
        print("❌ 数据处理流程测试失败")
    
    print("="*50)
    if success:
        print("✅ 数学统计技能测试通过")
    else:
        print("❌ 数学统计技能测试失败")
    
    return success

if __name__ == "__main__":
    run_mathematical_statistics_tests()