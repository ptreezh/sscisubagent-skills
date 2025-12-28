#!/usr/bin/env python3
"""
ANT专家分析工具 - 整合参与者识别、网络分析和转译过程追踪功能

此脚本提供全面的行动者网络理论分析功能，整合了原ant、ant-network-analysis、
ant-participant-identification和ant-translation-process技能的功能。
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

from network_analysis import network_analysis, topology_mapping, relationship_analysis, centrality_analysis, dynamics_analysis
from participant_identification import participant_identification, role_analysis, position_mapping
from translation_process import translation_process_analysis, black_boxing_analysis, network_stabilization_analysis


def main():
    parser = argparse.ArgumentParser(
        description='ANT专家分析工具（整合参与者识别、网络分析和转译过程追踪）',
        epilog='示例：python ant_expert_analyzer.py --input data.json --output results.json --method comprehensive'
    )
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON格式）')
    parser.add_argument('--output', '-o', default='ant_expert_results.json', help='输出文件')
    parser.add_argument('--method', '-m', required=True,
                       choices=['participants', 'network', 'translation', 'comprehensive'],
                       help='分析方法')
    parser.add_argument('--analysis-type', '-t', 
                       choices=['actors', 'network', 'translation', 'comprehensive'],
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

    if args.method == 'participants' or args.analysis_type == 'actors':
        # 执行参与者识别分析
        results = {
            'participant_identification': participant_identification(data),
            'role_analysis': role_analysis(data.get('actors', [])),
            'position_mapping': position_mapping(data.get('actors', []))
        }
    elif args.method == 'network' or args.analysis_type == 'network':
        # 执行网络分析
        edges = data.get('edges', [])
        nodes = data.get('nodes', [])
        
        results = {
            'network_analysis': network_analysis(edges, nodes),
            'topology_mapping': topology_mapping(data),
            'relationship_analysis': relationship_analysis(edges),
            'centrality_analysis': centrality_analysis(edges, nodes)
        }
        
        # 如果有时间序列数据，执行动态分析
        if 'edges_over_time' in data:
            results['dynamics_analysis'] = dynamics_analysis(data['edges_over_time'])
    elif args.method == 'translation' or args.analysis_type == 'translation':
        # 执行转译过程分析
        results = {
            'translation_process_analysis': translation_process_analysis(data),
            'black_boxing_analysis': black_boxing_analysis(data),
            'network_stabilization_analysis': network_stabilization_analysis(data)
        }
    elif args.method == 'comprehensive' or args.analysis_type == 'comprehensive':
        # 执行综合分析
        # 1. 参与者识别
        participant_results = participant_identification(data)
        
        # 2. 网络分析
        edges = data.get('edges', [])
        nodes = data.get('nodes', [])
        network_results = {
            'network_analysis': network_analysis(edges, nodes),
            'topology_mapping': topology_mapping(data),
            'relationship_analysis': relationship_analysis(edges),
            'centrality_analysis': centrality_analysis(edges, nodes)
        }
        
        # 3. 转译过程分析
        translation_results = {
            'translation_process_analysis': translation_process_analysis(data),
            'black_boxing_analysis': black_boxing_analysis(data),
            'network_stabilization_analysis': network_stabilization_analysis(data)
        }
        
        # 整合所有结果
        results = {
            'participant_analysis': participant_results,
            'network_analysis': network_results,
            'translation_analysis': translation_results
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
            'skill': 'ant-expert'
        }
    }

    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ ANT专家分析完成")
    print(f"  - 方法: {args.method}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


if __name__ == '__main__':
    main()