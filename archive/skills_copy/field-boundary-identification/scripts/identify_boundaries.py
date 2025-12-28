#!/usr/bin/env python3
"""
场域边界识别工具 - 智能依赖管理和功能降级系统

此脚本专门用于识别和分析社会场域的边界，优先使用高级功能，如不可用则降级到基础实现
"""

import argparse
import json
import sys
import importlib
import subprocess
import re
from datetime import datetime
from typing import Dict, List, Any, Optional


def install_package(package_name: str) -> bool:
    """尝试安装包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return True
    except subprocess.CalledProcessError:
        return False


def check_and_import(module_name: str, package_name: Optional[str] = None) -> Any:
    """检查并导入模块，如失败则返回None"""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        if package_name:
            print(f"模块 {module_name} 未找到，正在尝试安装 {package_name}...")
            if install_package(package_name):
                try:
                    return importlib.import_module(module_name)
                except ImportError:
                    print(f"安装后仍然无法导入 {module_name}")
                    return None
            else:
                print(f"无法安装 {package_name}")
                return None
        return None


# 尝试导入高级包
np = check_and_import("numpy")
pd = check_and_import("pandas")
nx = check_and_import("networkx", "networkx")
sns = check_and_import("seaborn", "seaborn")
plt = check_and_import("matplotlib.pyplot", "matplotlib")

# 检查高级功能是否可用
ADVANCED_AVAILABLE = all([np, pd])


def identify_field_boundaries(text: str) -> List[Dict[str, Any]]:
    """识别场域边界"""
    # 场域边界通常涉及界限、范围、排除、规则等概念
    boundary_patterns = [
        r'范围.*?包括|涵盖',
        r'界限.*?划定|确定',
        r'边界.*?设置|定义',
        r'排除.*?标准|机制',
        r'准入.*?条件|资格',
        r'规则.*?制定|执行',
        r'领域.*?划分|界定',
        r'范围.*?界定|限制',
        r'field.*?boundaries|scope|limits',
        r'exclusion.*?criteria|mechanisms',
        r'access.*?conditions|qualification',
        r'rules.*?established|enforced'
    ]

    boundaries = []
    sentences = re.split(r'[。！？\\n]', text)
    for sentence in sentences:
        for pattern in boundary_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                boundaries.append({
                    'boundary_type': 'potential_boundary',
                    'evidence': sentence.strip(),
                    'context': text[max(0, text.find(sentence)-100):text.find(sentence)+len(sentence)+100].strip()
                })
                break  # 找到一个匹配就跳出

    return boundaries


def identify_inclusion_exclusion_mechanisms(text: str) -> Dict[str, List[Dict[str, Any]]]:
    """识别包含和排除机制"""
    inclusion_patterns = [
        r'纳入.*?标准|条件',
        r'接受.*?条件|机制',
        r'加入.*?途径|方式',
        r'准入.*?门槛|要求',
        r'include.*?criteria|standards',
        r'accept.*?conditions|mechanisms',
        r'admit.*?pathways|methods'
    ]

    exclusion_patterns = [
        r'排除.*?标准|机制',
        r'拒绝.*?条件|理由',
        r'限制.*?进入|参与',
        r'禁止.*?加入|参与',
        r'exclude.*?criteria|mechanisms',
        r'reject.*?conditions|reasons',
        r'prohibit.*?joining|participating'
    ]

    inclusions = []
    exclusions = []

    sentences = re.split(r'[。！？\\n]', text)
    for sentence in sentences:
        for pattern in inclusion_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                inclusions.append({
                    'type': 'inclusion',
                    'evidence': sentence.strip(),
                    'context': text[max(0, text.find(sentence)-100):text.find(sentence)+len(sentence)+100].strip()
                })
                break

        for pattern in exclusion_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                exclusions.append({
                    'type': 'exclusion',
                    'evidence': sentence.strip(),
                    'context': text[max(0, text.find(sentence)-100):text.find(sentence)+len(sentence)+100].strip()
                })
                break

    return {
        'inclusion_mechanisms': inclusions,
        'exclusion_mechanisms': exclusions
    }


def analyze_field_specific_rules(text: str) -> List[Dict[str, Any]]:
    """分析场域特定规则"""
    rule_patterns = [
        r'规则.*?制定|规定',
        r'准则.*?设立|确立',
        r'标准.*?设定|确定',
        r'原则.*?遵循|坚持',
        r'惯例.*?形成|建立',
        r'norms.*?established|followed',
        r'rules.*?defined|implemented',
        r'standards.*?set|determined',
        r'principles.*?followed|maintained'
    ]

    rules = []
    sentences = re.split(r'[。！？\\n]', text)
    for sentence in sentences:
        for pattern in rule_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                rules.append({
                    'rule_type': 'potential_field_rule',
                    'evidence': sentence.strip(),
                    'context': text[max(0, text.find(sentence)-100):text.find(sentence)+len(sentence)+100].strip()
                })
                break  # 找到一个匹配就跳出

    return rules


def identify_field_relationships(text: str) -> List[Dict[str, Any]]:
    """识别场域间关系"""
    relationship_patterns = [
        r'与其他.*?关系|关联',
        r'跨.*?领域|场域|学科',
        r'多.*?领域|场域|学科',
        r'inter.*?field|domain|sector',
        r'cross.*?field|domain|sector',
        r'multi.*?field|domain|sector'
    ]

    relationships = []
    sentences = re.split(r'[。！？\\n]', text)
    for sentence in sentences:
        for pattern in relationship_patterns:
            if re.search(pattern, sentence, re.IGNORECASE):
                relationships.append({
                    'relationship_type': 'field_interaction',
                    'evidence': sentence.strip(),
                    'context': text[max(0, text.find(sentence)-100):text.find(sentence)+len(sentence)+100].strip()
                })
                break  # 找到一个匹配就跳出

    return relationships


def calculate_boundary_metrics(boundaries: List[Dict], mechanisms: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """计算边界指标"""
    if ADVANCED_AVAILABLE:
        try:
            import pandas as pd
            import numpy as np

            # 使用高级统计方法分析边界特征
            metrics = {
                'n_boundaries': len(boundaries),
                'n_inclusion_mechanisms': len(mechanisms['inclusion_mechanisms']),
                'n_exclusion_mechanisms': len(mechanisms['exclusion_mechanisms']),
                'boundary_clarity': len(boundaries) / max(1, len(text.split())),  # 简单的边界清晰度指标
                'inclusion_exclusion_balance': len(mechanisms['inclusion_mechanisms']) / max(1, len(mechanisms['exclusion_mechanisms']))  # 包含/排除平衡
            }

            return metrics
        except Exception as e:
            print(f"高级边界分析失败: {e}，使用基础分析")

    # 降级到基础实现
    return {
        'n_boundaries': len(boundaries),
        'n_inclusion_mechanisms': len(mechanisms['inclusion_mechanisms']),
        'n_exclusion_mechanisms': len(mechanisms['exclusion_mechanisms']),
        'boundaries': [b['evidence'] for b in boundaries],
        'inclusion_mechanisms': [im['evidence'] for im in mechanisms['inclusion_mechanisms']],
        'exclusion_mechanisms': [em['evidence'] for em in mechanisms['exclusion_mechanisms']]
    }


def main():
    parser = argparse.ArgumentParser(
        description='场域边界识别工具（支持高级功能，提供优雅降级）',
        epilog='示例：python field_boundary_identification.py --input data.json --output results.json'
    )
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON格式）')
    parser.add_argument('--output', '-o', default='field_boundaries.json', help='输出文件')

    args = parser.parse_args()

    start_time = datetime.now()

    # 读取输入数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)

    # 确定要分析的文本
    if isinstance(data, dict):
        if 'text' in data:
            text = data['text']
        elif 'content' in data:
            text = data['content']
        else:
            text = json.dumps(data, ensure_ascii=False)
    elif isinstance(data, list):
        text = ' '.join(str(item) for item in data)
    elif isinstance(data, str):
        text = data
    else:
        text = str(data)

    # 识别场域边界
    boundaries = identify_field_boundaries(text)

    # 识别包含和排除机制
    mechanisms = identify_inclusion_exclusion_mechanisms(text)

    # 分析场域特定规则
    rules = analyze_field_specific_rules(text)

    # 识别场域间关系
    relationships = identify_field_relationships(text)

    # 计算边界指标
    metrics = calculate_boundary_metrics(boundaries, mechanisms)

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'n_boundaries': len(boundaries),
            'n_inclusion_mechanisms': len(mechanisms['inclusion_mechanisms']),
            'n_exclusion_mechanisms': len(mechanisms['exclusion_mechanisms']),
            'n_rules': len(rules),
            'n_relationships': len(relationships),
            'processing_time': round((end_time - start_time).total_seconds(), 2),
            'using_advanced': ADVANCED_AVAILABLE
        },
        'details': {
            'boundaries': boundaries,
            'inclusion_exclusion_mechanisms': mechanisms,
            'field_rules': rules,
            'inter_field_relationships': relationships,
            'boundary_metrics': metrics
        },
        'metadata': {
            'input_file': args.input,
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'field-boundary-identification'
        }
    }

    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ 场域边界识别完成")
    print(f"  - 识别边界: {len(boundaries)} 个")
    print(f"  - 包含机制: {len(mechanisms['inclusion_mechanisms'])} 个")
    print(f"  - 排除机制: {len(mechanisms['exclusion_mechanisms'])} 个")
    print(f"  - 场域规则: {len(rules)} 个")
    print(f"  - 场域关系: {len(relationships)} 个")
    print(f"  - 使用高级功能: {output['summary']['using_advanced']}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()