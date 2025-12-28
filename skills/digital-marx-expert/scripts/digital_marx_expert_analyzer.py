#!/usr/bin/env python3
"""
数字马克思专家分析工具 - 整合历史唯物主义分析、阶级分析、资本分析和意识形态批判功能

此脚本提供全面的马克思主义分析功能，整合了原digital-marx、
historical-materialist-analysis、class-structure-analysis等技能的功能。
"""

import argparse
import json
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

# 导入内部模块
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'modules'))

from historical_materialism import historical_materialist_analysis
from class_analysis import class_structure_analysis
from capital_analysis import capital_analysis, ideology_analysis


def main():
    parser = argparse.ArgumentParser(
        description='数字马克思专家分析工具（整合历史唯物主义、阶级分析、资本分析和意识形态批判）',
        epilog='示例：python digital_marx_expert_analyzer.py --input data.json --output results.json --method comprehensive'
    )
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON格式）')
    parser.add_argument('--output', '-o', default='digital_marx_expert_results.json', help='输出文件')
    parser.add_argument('--method', '-m', required=True,
                       choices=['historical-materialism', 'class', 'capital', 'ideology', 'comprehensive'],
                       help='分析方法')
    parser.add_argument('--analysis-type', '-t', 
                       choices=['historical-materialism', 'class', 'capital', 'ideology', 'comprehensive'],
                       help='分析类型（兼容旧参数）')

    args = parser.parse_args()

    start_time = datetime.now()

    # 读取输入数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)

    results = {}

    if args.method == 'historical-materialism' or args.analysis_type == 'historical-materialism':
        # 执行历史唯物主义分析
        results = {
            'historical_materialism_analysis': historical_materialist_analysis(data)
        }
    elif args.method == 'class' or args.analysis_type == 'class':
        # 执行阶级分析
        results = {
            'class_analysis': class_structure_analysis(data)
        }
    elif args.method == 'capital' or args.analysis_type == 'capital':
        # 执行资本分析
        results = {
            'capital_analysis': capital_analysis(data)
        }
    elif args.method == 'ideology' or args.analysis_type == 'ideology':
        # 执行意识形态分析
        results = {
            'ideology_analysis': ideology_analysis(data)
        }
    elif args.method == 'comprehensive' or args.analysis_type == 'comprehensive':
        # 执行综合分析
        # 1. 历史唯物主义分析
        historical_results = historical_materialist_analysis(data)
        
        # 2. 阶级分析
        class_results = class_structure_analysis(data)
        
        # 3. 资本分析
        capital_results = capital_analysis(data)
        
        # 4. 意识形态分析
        ideology_results = ideology_analysis(data)
        
        # 整合所有结果
        results = {
            'historical_materialism_analysis': historical_results,
            'class_analysis': class_results,
            'capital_analysis': capital_results,
            'ideology_analysis': ideology_results,
            'comprehensive_synthesis': {
                'material_basis_synthesis': {
                    'productive_forces': historical_results['historical_materialist_overview']['development_level'],
                    'production_relations': 'To be integrated from class and capital analysis'
                },
                'class_synthesis': class_results['class_structure_overview'],
                'capital_synthesis': capital_results['capital_overview'],
                'ideology_synthesis': ideology_results['ideology_overview'],
                'main_contradiction': identify_main_contradiction(
                    historical_results, class_results, capital_results
                ),
                'revolutionary_potential': assess_revolutionary_potential(
                    class_results, capital_results
                )
            }
        }

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'method': args.method,
            'input_file': args.input,
            'processing_time': round((end_time - start_time).total_seconds(), 2),
            'analysis_components': list(results.keys())
        },
        'details': results,
        'metadata': {
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'digital-marx-expert'
        }
    }

    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ 数字马克思专家分析完成")
    print(f"  - 方法: {args.method}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


def identify_main_contradiction(historical: Dict[str, Any], class_analysis: Dict[str, Any], capital: Dict[str, Any]) -> str:
    """
    识别主要矛盾
    
    Args:
        historical: 历史唯物主义分析结果
        class_analysis: 阶级分析结果
        capital: 资本分析结果
    
    Returns:
        主要矛盾描述
    """
    # 简化的矛盾识别逻辑
    main_contradiction = historical['historical_materialist_overview'].get('main_contradiction', 'unknown')
    if main_contradiction == 'unknown':
        main_contradiction = class_analysis['class_structure_overview'].get('main_contradiction', 'capital_vs_labor')
    
    return main_contradiction


def assess_revolutionary_potential(class_analysis: Dict[str, Any], capital: Dict[str, Any]) -> float:
    """
    评估革命潜力
    
    Args:
        class_analysis: 阶级分析结果
        capital: 资本分析结果
    
    Returns:
        革命潜力评估（0-1之间的浮点数）
    """
    # 简化的革命潜力评估
    class_consciousness = class_analysis['class_structure_overview'].get('consciousness_level', 'low')
    surplus_value_rate = capital['capital_overview'].get('surplus_value_rate', 0)
    
    # 基于阶级意识和剩余价值率评估革命潜力
    if class_consciousness == 'high' and surplus_value_rate > 100:
        return 0.8
    elif class_consciousness == 'medium' and surplus_value_rate > 50:
        return 0.5
    else:
        return 0.2


if __name__ == '__main__':
    main()