#!/usr/bin/env python3
"""
扎根理论专家分析工具 - 整合开放编码、轴心编码、选择式编码、饱和度检验和备忘录撰写功能

此脚本提供全面的扎根理论分析功能，整合了原performing-open-coding、
performing-axial-coding、performing-selective-coding、
checking-theory-saturation和writing-grounded-theory-memos技能的功能。
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
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'stages'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools'))

from open_coding import open_coding
from axial_coding import axial_coding
from selective_coding import selective_coding
from saturation_checker import saturation_check
from memo_writer import memo_writing


def main():
    parser = argparse.ArgumentParser(
        description='扎根理论专家分析工具（整合开放编码、轴心编码、选择式编码、饱和度检验和备忘录撰写）',
        epilog='示例：python gt_expert_analyzer.py --input data.json --output results.json --method comprehensive'
    )
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON格式）')
    parser.add_argument('--output', '-o', default='gt_expert_results.json', help='输出文件')
    parser.add_argument('--method', '-m', required=True,
                       choices=['open', 'axial', 'selective', 'saturation', 'memo', 'comprehensive'],
                       help='分析方法')
    parser.add_argument('--coding-stage', '-s', 
                       choices=['open', 'axial', 'selective'],
                       help='编码阶段')

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

    if args.method == 'open':
        # 执行开放编码
        results = {
            'open_coding': open_coding(data),
            'memo_notes': memo_writing({
                'coding_stage': 'open',
                'process_info': data.get('process_info', {}),
                'analysis_results': open_coding(data)
            })['memos']
        }
    elif args.method == 'axial':
        # 执行轴心编码
        results = {
            'axial_coding': axial_coding(data),
            'memo_notes': memo_writing({
                'coding_stage': 'axial',
                'process_info': data.get('process_info', {}),
                'analysis_results': axial_coding(data)
            })['memos']
        }
    elif args.method == 'selective':
        # 执行选择式编码
        results = {
            'selective_coding': selective_coding(data),
            'memo_notes': memo_writing({
                'coding_stage': 'selective',
                'process_info': data.get('process_info', {}),
                'analysis_results': selective_coding(data)
            })['memos']
        }
    elif args.method == 'saturation':
        # 执行饱和度检验
        results = {
            'saturation_analysis': saturation_check(data)
        }
    elif args.method == 'memo':
        # 执行备忘录撰写
        results = {
            'memo_writing': memo_writing(data)
        }
    elif args.method == 'comprehensive':
        # 执行综合分析
        # 1. 开放编码
        open_results = open_coding(data)
        
        # 2. 轴心编码
        axial_input = {
            'concepts': open_results['concepts']
        }
        axial_results = axial_coding(axial_input)
        
        # 3. 选择式编码
        selective_input = {
            'categories': axial_results['categories'],
            'relationships': axial_results['relationships']
        }
        selective_results = selective_coding(selective_input)
        
        # 4. 饱和度检验
        saturation_input = {
            'existing_theory': {
                'open_coding': open_results,
                'axial_coding': axial_results,
                'selective_coding': selective_results
            },
            'new_data': data.get('new_data', [])
        }
        saturation_results = saturation_check(saturation_input)
        
        # 5. 备忘录撰写
        memo_results = memo_writing({
            'coding_stage': 'selective',
            'process_info': data.get('process_info', {}),
            'analysis_results': selective_results
        })
        
        # 整合所有结果
        results = {
            'open_coding': open_results,
            'axial_coding': axial_results,
            'selective_coding': selective_results,
            'saturation_analysis': saturation_results,
            'memo_writing': memo_results,
            'comprehensive_theory': {
                'core_category': selective_results.get('core_category', {}),
                'storyline': selective_results.get('storyline', {}),
                'theory_framework': selective_results.get('theory_framework', {}),
                'saturation_level': saturation_results.get('overall_saturation', {}).get('level', 'unknown')
            }
        }

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'method': args.method,
            'coding_stage': args.method if args.method in ['open', 'axial', 'selective'] else args.coding_stage,
            'input_file': args.input,
            'processing_time': round((end_time - start_time).total_seconds(), 2),
            'analysis_components': list(results.keys())
        },
        'details': results,
        'metadata': {
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'grounded-theory-expert'
        }
    }

    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ 扎根理论专家分析完成")
    print(f"  - 方法: {args.method}")
    print(f"  - 编码阶段: {args.method if args.method in ['open', 'axial', 'selective'] else (args.coding_stage or 'N/A')}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()