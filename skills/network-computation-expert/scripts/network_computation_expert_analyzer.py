#!/usr/bin/env python3
"""
网络计算专家分析工具 - 整合网络数据处理、网络构建、中心性分析和社区检测功能

此脚本提供全面的社会网络分析功能，整合了原network-computation、
performing-network-computation、performing-centrality-analysis、
processing-network-data等技能的功能。
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

from data_processing import network_data_processing
from network_construction import network_construction
from centrality_analysis import centrality_analysis
from community_detection import community_detection


def main():
    parser = argparse.ArgumentParser(
        description='网络计算专家分析工具（整合数据处理、网络构建、中心性分析和社区检测）',
        epilog='示例：python network_computation_expert_analyzer.py --input data.json --output results.json --method comprehensive'
    )
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON格式）')
    parser.add_argument('--output', '-o', default='network_computation_expert_results.json', help='输出文件')
    parser.add_argument('--method', '-m', required=True,
                       choices=['data-processing', 'construction', 'centrality', 'community', 'comprehensive'],
                       help='分析方法')
    parser.add_argument('--network-type', '-n', 
                       choices=['undirected-unweighted', 'undirected-weighted', 'directed-unweighted', 'directed-weighted'],
                       help='网络类型')

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

    if args.method == 'data-processing':
        # 执行网络数据处理
        results = {
            'network_data_processing': network_data_processing(data)
        }
    elif args.method == 'construction':
        # 执行网络构建
        results = {
            'network_construction': network_construction(data)
        }
    elif args.method == 'centrality':
        # 执行中心性分析
        results = {
            'centrality_analysis': centrality_analysis(data)
        }
    elif args.method == 'community':
        # 执行社区检测
        results = {
            'community_detection': community_detection(data)
        }
    elif args.method == 'comprehensive':
        # 执行综合分析
        # 准备网络数据处理的输入
        processing_input = {
            'raw_data': data.get('raw_data', []),
            'data_source_type': data.get('data_source_type', 'survey'),
            'node_attributes': data.get('node_attributes', {}),
            'edge_attributes': data.get('edge_attributes', {})
        }

        # 1. 网络数据处理
        processing_results = network_data_processing(processing_input)

        # 2. 网络构建 - 使用直接提供的节点和边数据
        construction_input = {
            'nodes': data.get('nodes', []),
            'edges': data.get('edges', []),
            'node_attributes': data.get('node_attributes', {}),
            'edge_attributes': data.get('edge_attributes', {}),
            'network_type': data.get('network_type', 'undirected_weighted')
        }
        construction_results = network_construction(construction_input)

        # 3. 中心性分析
        centrality_input = {
            'network': construction_results['network']
        }
        centrality_results = centrality_analysis(centrality_input)

        # 4. 社区检测
        community_input = {
            'network': construction_results['network']
        }
        community_results = community_detection(community_input)

        # 整合所有结果
        results = {
            'network_data_processing': processing_results,
            'network_construction': construction_results,
            'centrality_analysis': centrality_results,
            'community_detection': community_results,
            'comprehensive_analysis': {
                'network_summary': {
                    'nodes_count': construction_results['construction_summary']['nodes_count'],
                    'edges_count': construction_results['construction_summary']['edges_count'],
                    'network_type': construction_results['construction_summary']['network_type'],
                    'density': construction_results['basic_metrics']['density']
                },
                'centrality_summary': centrality_results['analysis_summary'],
                'community_summary': community_results['detection_summary'],
                'key_findings': generate_key_findings(
                    construction_results, centrality_results, community_results
                )
            }
        }

    end_time = datetime.now()

    # 标准化输出
    output = {
        'summary': {
            'method': args.method,
            'network_type': args.network_type or data.get('network_type', 'unknown'),
            'input_file': args.input,
            'processing_time': round((end_time - start_time).total_seconds(), 2),
            'analysis_components': list(results.keys())
        },
        'details': results,
        'metadata': {
            'output_file': args.output,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'network-computation-expert'
        }
    }

    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✓ 网络计算专家分析完成")
    print(f"  - 方法: {args.method}")
    print(f"  - 网络类型: {args.network_type or data.get('network_type', 'unknown')}")
    print(f"  - 处理时间: {output['summary']['processing_time']} 秒")
    print(f"  - 输出文件: {args.output}")


def generate_key_findings(construction: Dict[str, Any], centrality: Dict[str, Any], community: Dict[str, Any]) -> List[str]:
    """
    生成关键发现
    
    Args:
        construction: 网络构建结果
        centrality: 中心性分析结果
        community: 社区检测结果
    
    Returns:
        关键发现列表
    """
    findings = []
    
    # 网络结构发现
    density = construction['basic_metrics']['density']
    if density > 0.5:
        findings.append("网络密度较高，表明节点间连接紧密")
    elif density < 0.1:
        findings.append("网络密度较低，表明节点间连接稀疏")
    else:
        findings.append("网络密度中等，连接模式适中")
    
    # 中心性发现
    top_by_degree = centrality['analysis_summary'].get('top_node_by_degree', 'unknown')
    if top_by_degree:
        findings.append(f"节点 {top_by_degree} 在度中心性上表现突出，是网络中的关键连接点")
    
    # 社区结构发现
    modularity = community['detection_summary'].get('modularity', 0.0)
    if modularity > 0.7:
        findings.append("社区结构明显，模块度较高")
    elif modularity < 0.3:
        findings.append("社区结构不明显，模块度较低")
    else:
        findings.append("社区结构中等，存在一定的群组划分")
    
    return findings


if __name__ == '__main__':
    main()