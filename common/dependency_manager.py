#!/usr/bin/env python3
"""
智能体依赖管理器

此脚本提供以下功能：
1. 检查并自动安装高级依赖包
2. 在高级包不可用时提供优雅降级
3. 为智能体提供动态功能切换
"""

import argparse
import json
import subprocess
import sys
import importlib
from pathlib import Path
from typing import Dict, List, Tuple, Optional
from datetime import datetime


def check_package_availability(package_name: str) -> bool:
    """检查包是否可用"""
    try:
        importlib.import_module(package_name)
        return True
    except ImportError:
        return False


def install_package(package_name: str) -> bool:
    """安装包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False


def get_available_features() -> Dict[str, Dict[str, bool]]:
    """获取可用的功能包"""
    return {
        'statistics': {
            'statsmodels': check_package_availability('statsmodels'),
            'pingouin': check_package_availability('pingouin'),
            'scikit_learn': check_package_availability('sklearn'),
        },
        'network_analysis': {
            'networkx': check_package_availability('networkx'),
            'igraph': check_package_availability('igraph'),
            'community': check_package_availability('community'),
        },
        'nlp': {
            'jieba': check_package_availability('jieba'),
            'nltk': check_package_availability('nltk'),
            'spacy': check_package_availability('spacy'),
        },
        'psychometrics': {
            'factor_analyzer': check_package_availability('factor_analyzer'),
        }
    }


def install_feature_group(feature_group: str) -> Dict[str, bool]:
    """安装特定功能组的包"""
    packages = {
        'statistics': ['statsmodels', 'pingouin', 'scikit-learn'],
        'network_analysis': ['networkx', 'python-igraph', 'python-louvain'],
        'nlp': ['jieba', 'nltk', 'spacy'],
        'psychometrics': ['factor-analyzer', 'pingouin', 'statsmodels']
    }
    
    if feature_group not in packages:
        return {}
    
    results = {}
    for package in packages[feature_group]:
        print(f"正在安装 {package}...")
        success = install_package(package)
        results[package] = success
        if success:
            print(f"✓ {package} 安装成功")
        else:
            print(f"✗ {package} 安装失败")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='智能体依赖管理器 - 支持高级功能和优雅降级',
        epilog='示例：python dependency_manager.py --check-all 或 python dependency_manager.py --install statistics'
    )
    parser.add_argument('--check-all', action='store_true', help='检查所有功能包的可用性')
    parser.add_argument('--install', choices=['statistics', 'network_analysis', 'nlp', 'psychometrics', 'all'], 
                       help='安装特定功能组的包')
    parser.add_argument('--list-available', action='store_true', help='列出所有可用功能')
    parser.add_argument('--output', '-o', default='dependency_report.json', help='输出报告文件')
    
    args = parser.parse_args()

    if args.check_all or args.list_available:
        available_features = get_available_features()
        
        # 创建报告
        report = {
            'summary': {
                'check_timestamp': datetime.now().isoformat(),
                'total_feature_groups': len(available_features),
                'features_checked': list(available_features.keys())
            },
            'details': {
                'available_features': available_features
            },
            'recommendations': []
        }
        
        # 添加建议
        for group, packages in available_features.items():
            unavailable = [pkg for pkg, available in packages.items() if not available]
            if unavailable:
                report['recommendations'].append({
                    'feature_group': group,
                    'missing_packages': unavailable,
                    'install_command': f"python dependency_manager.py --install {group}"
                })
        
        # 保存报告
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print("✓ 依赖检查完成")
        print(f"  - 报告已保存至: {args.output}")
        
        for group, packages in available_features.items():
            available_count = sum(1 for available in packages.values() if available)
            total_count = len(packages)
            print(f"  - {group}: {available_count}/{total_count} 包可用")
    
    elif args.install:
        if args.install == 'all':
            all_results = {}
            for group in ['statistics', 'network_analysis', 'nlp', 'psychometrics']:
                print(f"\n--- 安装 {group} 功能组 ---")
                results = install_feature_group(group)
                all_results[group] = results
        else:
            print(f"--- 安装 {args.install} 功能组 ---")
            all_results = {args.install: install_feature_group(args.install)}
        
        # 保存安装结果
        results_file = args.output.replace('.json', '_install_results.json')
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump({
                'installation_results': all_results,
                'timestamp': datetime.now().isoformat(),
                'requested_installation': args.install
            }, f, ensure_ascii=False, indent=2)
        
        print(f"\n✓ 安装完成 - 结果已保存至: {results_file}")
        
        # 检查安装后的可用性
        print("\n重新检查功能可用性:")
        updated_features = get_available_features()
        for group, packages in updated_features.items():
            if args.install == 'all' or group == args.install.replace('_', '-'):
                available_count = sum(1 for available in packages.values() if available)
                total_count = len(packages)
                print(f"  - {group}: {available_count}/{total_count} 包可用")
    
    else:
        print("请使用 --check-all 检查功能或 --install [功能组] 安装功能包")


if __name__ == '__main__':
    main()