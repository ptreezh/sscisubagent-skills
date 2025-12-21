#!/usr/bin/env python
"""
社区检测工具
使用多种算法检测网络中的社区结构
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any
import networkx as nx
import numpy as np
from collections import defaultdict

def load_network_from_json(file_path: str) -> nx.Graph:
    """从JSON文件加载网络"""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 从edges列表重建网络
    G = nx.Graph()
    edges = data.get('details', {}).get('edges', [])
    
    for edge in edges:
        if len(edge) >= 2:
            source, target = edge[0], edge[1]
            weight = edge[2].get('weight', 1.0) if len(edge) > 2 else 1.0
            G.add_edge(source, target, weight=weight)
    
    return G

def detect_communities_louvain(G: nx.Graph) -> Dict:
    """使用Louvain算法检测社区（简化实现）"""
    # 简化的Louvain实现，使用模块度优化
    communities = list(nx.algorithms.community.greedy_modularity_communities(G))
    
    # 转换为节点到社区的映射
    node_to_community = {}
    for i, community in enumerate(communities):
        for node in community:
            node_to_community[node] = i
    
    # 计算模块度
    modularity = nx.algorithms.community.modularity(G, communities)
    
    return {
        'communities': [list(c) for c in communities],  # 转换frozenset为list
        'node_to_community': node_to_community,
        'n_communities': len(communities),
        'modularity': modularity,
        'method': 'louvain'
    }

def detect_communities_label_propagation(G: nx.Graph) -> Dict:
    """使用标签传播算法检测社区"""
    communities = list(nx.algorithms.community.label_propagation_communities(G))
    
    # 转换为节点到社区的映射
    node_to_community = {}
    for i, community in enumerate(communities):
        for node in community:
            node_to_community[node] = i
    
    # 计算模块度
    modularity = nx.algorithms.community.modularity(G, communities)
    
    return {
        'communities': [list(c) for c in communities],  # 转换frozenset为list
        'node_to_community': node_to_community,
        'n_communities': len(communities),
        'modularity': modularity,
        'method': 'label_propagation'
    }

def detect_communities_girvan_newman(G: nx.Graph) -> Dict:
    """使用Girvan-Newman算法检测社区（适用于小网络）"""
    if G.number_of_nodes() > 50:
        # 大网络使用其他方法
        return detect_communities_louvain(G)
    
    # Girvan-Newman算法
    communities_generator = nx.algorithms.community.girvan_newman(G)
    communities = next(communities_generator)
    
    # 转换为节点到社区的映射
    node_to_community = {}
    for i, community in enumerate(communities):
        for node in community:
            node_to_community[node] = i
    
    # 计算模块度
    modularity = nx.algorithms.community.modularity(G, communities)
    
    return {
        'communities': [list(c) for c in communities],  # 转换frozenset为list
        'node_to_community': node_to_community,
        'n_communities': len(communities),
        'modularity': modularity,
        'method': 'girvan_newman'
    }

def analyze_community_structure(G: nx.Graph, result: Dict) -> Dict:
    """分析社区结构特征"""
    communities = result['communities']
    node_to_community = result['node_to_community']
    
    analysis = {
        'community_sizes': [len(c) for c in communities],
        'largest_community_size': max(len(c) for c in communities),
        'smallest_community_size': min(len(c) for c in communities),
        'avg_community_size': np.mean([len(c) for c in communities]),
        'size_std': np.std([len(c) for c in communities])
    }
    
    # 计算社区内部和外部连接比例
    internal_edges = 0
    external_edges = 0
    
    for u, v in G.edges():
        if node_to_community.get(u) == node_to_community.get(v):
            internal_edges += 1
        else:
            external_edges += 1
    
    total_edges = G.number_of_edges()
    if total_edges > 0:
        analysis['internal_edge_ratio'] = internal_edges / total_edges
        analysis['external_edge_ratio'] = external_edges / total_edges
    
    # 识别关键节点（社区间的桥梁）
    bridge_nodes = []
    for node in G.nodes():
        community = node_to_community.get(node)
        neighbors = list(G.neighbors(node))
        neighbor_communities = set(node_to_community.get(n) for n in neighbors)
        
        # 如果连接到多个社区，则是桥梁节点
        if len(neighbor_communities) > 1:
            bridge_nodes.append({
                'node': node,
                'community': community,
                'connected_communities': len(neighbor_communities),
                'neighbors': neighbors
            })
    
    # 按连接的社区数排序
    bridge_nodes.sort(key=lambda x: x['connected_communities'], reverse=True)
    analysis['bridge_nodes'] = bridge_nodes[:5]  # 前5个最重要的桥梁节点
    
    return analysis

def compare_community_methods(G: nx.Graph) -> Dict:
    """比较不同社区检测方法"""
    methods = {
        'louvain': detect_communities_louvain(G),
        'label_propagation': detect_communities_label_propagation(G)
    }
    
    # 如果网络较小，也运行Girvan-Newman
    if G.number_of_nodes() <= 30:
        methods['girvan_newman'] = detect_communities_girvan_newman(G)
    
    comparison = {
        'method_results': methods,
        'best_method': None,
        'best_modularity': -1
    }
    
    # 找出模块度最高的方法
    for method, result in methods.items():
        modularity = result['modularity']
        if modularity > comparison['best_modularity']:
            comparison['best_modularity'] = modularity
            comparison['best_method'] = method
    
    return comparison

def main():
    parser = argparse.ArgumentParser(
        description='社区检测工具',
        epilog='示例：python detect_communities.py --input network.json --output communities.json --method louvain'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入网络文件（JSON）')
    parser.add_argument('--output', '-o', default='communities.json', help='输出文件')
    parser.add_argument('--method', '-m', 
                       choices=['louvain', 'label_propagation', 'girvan_newman', 'compare'],
                       default='louvain',
                       help='社区检测方法')
    
    args = parser.parse_args()
    
    # 读取网络
    try:
        G = load_network_from_json(args.input)
    except Exception as e:
        print(f"错误：无法读取网络文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    if G.number_of_nodes() == 0:
        print("错误：网络没有节点", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 执行社区检测
    if args.method == 'compare':
        result = compare_community_methods(G)
        summary = {
            'n_nodes': G.number_of_nodes(),
            'n_edges': G.number_of_edges(),
            'methods_compared': list(result['method_results'].keys()),
            'best_method': result['best_method'],
            'best_modularity': result['best_modularity']
        }
        details = result
    else:
        # 单一方法检测
        if args.method == 'louvain':
            result = detect_communities_louvain(G)
        elif args.method == 'label_propagation':
            result = detect_communities_label_propagation(G)
        elif args.method == 'girvan_newman':
            result = detect_communities_girvan_newman(G)
        
        # 分析社区结构
        analysis = analyze_community_structure(G, result)
        
        summary = {
            'n_nodes': G.number_of_nodes(),
            'n_edges': G.number_of_edges(),
            'n_communities': result['n_communities'],
            'modularity': result['modularity'],
            'method': result['method']
        }
        
        details = {
            'community_detection': result,
            'community_analysis': analysis
        }
    
    end_time = datetime.now()
    
    # 准备输出
    output = {
        'summary': summary,
        'details': details,
        'metadata': {
            'input_file': args.input,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'performing-network-computation'
        }
    }
    
    # 添加处理时间
    output['summary']['processing_time'] = round((end_time - start_time).total_seconds(), 2)
    
    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 社区检测完成")
        if args.method == 'compare':
            print(f"  - 比较方法数：{len(summary['methods_compared'])}")
            print(f"  - 最佳方法：{summary['best_method']}")
            print(f"  - 最高模块度：{summary['best_modularity']:.4f}")
        else:
            print(f"  - 检测方法：{summary['method']}")
            print(f"  - 社区数量：{summary['n_communities']}")
            print(f"  - 模块度：{summary['modularity']:.4f}")
        print(f"  - 输出文件：{args.output}")
        
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()