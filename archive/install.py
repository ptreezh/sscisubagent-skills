#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSCI中文学科研究技能包安装脚本
支持 uv 和 pip 两种安装方式
"""

import subprocess
import sys
import os
from pathlib import Path

def check_command(cmd):
    """检查命令是否可用"""
    try:
        subprocess.run([cmd, "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def install_with_uv():
    """使用uv安装依赖"""
    print("🚀 使用 uv 安装依赖...")
    try:
        # 检查是否已安装uv
        if not check_command("uv"):
            print("📦 正在安装 uv...")
            subprocess.run([sys.executable, "-m", "pip", "install", "uv"], check=True)

        # 使用uv安装
        subprocess.run(["uv", "sync"], check=True)
        print("✅ uv 安装完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ uv 安装失败: {e}")
        return False

def install_with_pip():
    """使用pip安装依赖"""
    print("📦 使用 pip 安装依赖...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ pip 安装完成！")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ pip 安装失败: {e}")
        return False

def verify_installation():
    """验证安装是否成功"""
    print("🔍 验证安装...")

    try:
        # 测试关键依赖
        import jieba
        import networkx
        import pandas
        import numpy

        print("✅ 所有核心依赖导入成功！")

        # 测试技能脚本
        sys.path.insert(0, str(Path(__file__).parent / "skills"))

        # 测试网络分析
        from skills.analysis.centrality_analysis.scripts.centrality import CentralityAnalyzer
        analyzer = CentralityAnalyzer()
        print("✅ 中心性分析工具可用！")

        # 测试理论饱和度
        from skills.coding.theory_saturation.scripts.assess_saturation import TheorySaturationAssessor
        assessor = TheorySaturationAssessor()
        print("✅ 理论饱和度检验工具可用！")

        # 测试开放编码
        from skills.coding.open_coding.scripts.preprocess import TextPreprocessor
        processor = TextPreprocessor()
        print("✅ 开放编码工具可用！")

        return True

    except ImportError as e:
        print(f"❌ 导入失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 验证失败: {e}")
        return False

def main():
    """主安装流程"""
    print("🎯 SSCI中文学科研究技能包安装器")
    print("=" * 50)

    # 检查Python版本
    if sys.version_info < (3, 8):
        print("❌ 需要Python 3.8或更高版本")
        sys.exit(1)

    print(f"✅ Python版本: {sys.version}")

    # 切换到项目目录
    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    # 尝试安装
    if check_command("uv"):
        success = install_with_uv()
    else:
        print("⚠️  uv 未安装，使用 pip 安装...")
        success = install_with_pip()

    if not success:
        print("❌ 安装失败！")
        sys.exit(1)

    # 验证安装
    if verify_installation():
        print("\n🎉 安装成功！")
        print("\n📚 使用方法:")
        print("  1. 将技能文件复制到 Claude Skills 目录")
        print("  2. 或使用 OpenSkills 安装: openskills install .")
        print("  3. 运行测试: python -m pytest tests/")
    else:
        print("\n❌ 安装验证失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()