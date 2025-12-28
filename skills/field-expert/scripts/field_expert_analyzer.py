#!/usr/bin/env python3
"""
场域专家分析工具 - 整合场域边界识别、资本分析和习性分析功能

此脚本提供全面的布迪厄场域理论分析功能，整合了原field-analysis、
field-boundary-identification、field-capital-analysis和
field-habitus-analysis技能的功能。
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

from boundary_analysis import field_boundary_identification, analyze_boundary_dynamics
from capital_analysis import field_capital_analysis
from habitus_analysis import field_habitus_analysis, analyze_symbolic_violence, analyze_cross_field_analysis


def main():
    parser = argparse.ArgumentParser(
        description='场域专家分析工具（整合边界识别、资本分析和习性分析）',
        epilog='示例：python field_expert_analyzer.py --input data.json --output results.json --method comprehensive'
    )
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON格式）')
    parser.add_argument('--output', '-o', default='field_expert_results.json', help='输出文件')
    parser.add_argument('--method', '-m', required=True,
                       choices=['boundary', 'capital', 'habitus', 'comprehensive'],
                       help='分析方法')
    parser.add_argument('--field-type', '-f', 
                       choices=['educational', 'political', 'cultural', 'economic', 'academic', 'artistic'],
                       help='场域类型')

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

    if args.method == 'boundary':
        # 执行边界分析
        results = {
            'field_boundary_analysis': field_boundary_identification(data),
            'boundary_dynamics_analysis': analyze_boundary_dynamics(data)
        }
    elif args.method == 'capital':
        # 执行资本分析
        results = {
            'field_capital_analysis': field_capital_analysis(data)
        }
    elif args.method == 'habitus':
        # 执行习性分析
        results = {
            'field_habitus_analysis': field_habitus_analysis(data),
            'symbolic_violence_analysis': analyze_symbolic_violence(data),
            'cross_field_analysis': analyze_cross_field_analysis(data)
        }
    elif args.method == 'comprehensive':
        # 执行综合分析
        # 1. 边界分析
        boundary_results = {
            'field_boundary_analysis': field_boundary_identification(data),
            'boundary_dynamics_analysis': analyze_boundary_dynamics(data)
        }
        
        # 2. 资本分析
        capital_results = {
            'field_capital_analysis': field_capital_analysis(data)
        }
        
        # 3. 习性分析
        habitus_results = {
            'field_habitus_analysis': field_habitus_analysis(data),
            'symbolic_violence_analysis': analyze_symbolic_violence(data),
            'cross_field_analysis': analyze_cross_field_analysis(data)
        }
        
        # 整合所有结果
        results = {
            'boundary_analysis': boundary_results,
            'capital_analysis': capital_results,
            'habitus_analysis': habitus_results
        }

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'method': args.method,
            'field_type': args.field_type or data.get('field_type', 'unknown'),
            'input_file': args.input,
            'processing_time': round((end_time - start_time).total_seconds(), 2),
            'analysis_components': list(results.keys())
        },
        'details': results,
        'metadata': {
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'field-expert'
        }
    }

    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ 场域专家分析完成")
    print(f"  - 方法: {args.method}")
    print(f"  - 场域类型: {args.field_type or data.get('field_type', 'unknown')}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()