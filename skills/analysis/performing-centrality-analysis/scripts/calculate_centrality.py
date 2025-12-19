#!/usr/bin/env python3
"""
中心性计算工具

功能：
1. 计算度中心性（Degree Centrality）
2. 计算接近中心性（Closeness Centrality）
3. 计算中介中心性（Betweenness Centrality）
4. 计算特征向量中心性（Eigenvector Centrality）
5. 综合排序和分析

标准化接口：argparse + 三层JSON输出
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict

import networkx as nx


def load_network(file_path: str) -> nx.Graph:
    """加载网络数据"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 支持多种格式
        if 'edges' in data:
            edges = data['edges']
        elif 'links' in data:
            edges = data['links']
        else:
            edges = data
        
        G = nx.Graph()
        for edge in edges:
            source = edge.get('source') or edge.get('from')
            target = edge.get('target') or edge.get('to')
            weight = edge.get('weight', 1.0)
            G.add_edge(source, target, weight=weight)
        
        return G
    
    except Exception as e:
        print(f"错误：无法加载网络文件 - {e}", file=sys.stderr)
        sys.exit(1)


def calculate_all_centralities(G: nx.Graph) -> Dict:
    """计算所有中心性指标"""
    
    # 度中心性
    degree_cent = nx.degree_centrality(G)
    
    # 接近中心性
    try:
        closeness_cent = nx.closeness_centrality(G)
    except:
        closeness_cent = {node: 0.0 for node in G.nodes()}
    
    # 中介中心性
    betweenness_cent = nx.betweenness_centrality(G)
    
    # 特征向量中心性
    try:
        eigenvector_cent = nx.eigenvector_centrality(G, max_iter=1000)
    except:
        eigenvector_cent = {node: 0.0 for node in G.nodes()}
    
    # 整合结果
    centralities = {}
    for node in G.nodes():
        centralities[node] = {
            'node': node,
            'degree': round(degree_cent.get(node, 0), 4),
            'closeness': round(closeness_cent.get(node, 0), 4),
            'betweenness': round(betweenness_cent.get(node, 0), 4),
            'eigenvector': round(eigenvector_cent.get(node, 0), 4)
        }
    
    return centralities


def rank_nodes(centralities: Dict, metric: str = 'degree', top_n: int = 10) -> list:
    """按指定指标排序节点"""
    sorted_nodes = sorted(
        centralities.values(),
        key=lambda x: x[metric],
        reverse=True
    )
    return sorted_nodes[:top_n]


def identify_key_nodes(centralities: Dict, thresholds: Dict = None) -> Dict:
    """识别关键节点"""
    if thresholds is None:
        thresholds = {
            'degree': 0.5,
            'betweenness': 0.1,
            'eigenvector': 0.3
        }
    
    hubs = []  # 度中心性高的节点
    bridges = []  # 中介中心性高的节点
    influencers = []  # 特征向量中心性高的节点
    
    for node, scores in centralities.items():
        if scores['degree'] >= thresholds['degree']:
            hubs.append(node)
        if scores['betweenness'] >= thresholds['betweenness']:
            bridges.append(node)
        if scores['eigenvector'] >= thresholds['eigenvector']:
            influencers.append(node)
    
    return {
        'hubs': hubs,
        'bridges': bridges,
        'influencers': influencers
    }


def main():
    parser = argparse.ArgumentParser(
        description='中心性计算工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例用法:
  python calculate_centrality.py --input network.json
  python calculate_centrality.py -i network.json -m betweenness --top 20
  python calculate_centrality.py -i network.json -o centrality.json
        '''
    )
    
    parser.add_argument('--input', '-i', required=True,
                       help='输入的网络文件（JSON格式）')
    parser.add_argument('--output', '-o', default='centrality.json',
                       help='输出文件名（默认：centrality.json）')
    parser.add_argument('--metric', '-m', default='degree',
                       choices=['degree', 'closeness', 'betweenness', 'eigenvector'],
                       help='排序指标（默认：degree）')
    parser.add_argument('--top', '-t', type=int, default=10,
                       help='输出前N个节点（默认：10）')
    
    args = parser.parse_args()
    
    start_time = datetime.now()
    
    # 加载网络
    G = load_network(args.input)
    
    # 计算中心性
    centralities = calculate_all_centralities(G)
    
    # 排序节点
    top_nodes = rank_nodes(centralities, args.metric, args.top)
    
    # 识别关键节点
    key_nodes = identify_key_nodes(centralities)
    
    end_time = datetime.now()
    processing_time = (end_time - start_time).total_seconds()
    
    # 标准化输出
    output = {
        'summary': {
            'total_nodes': G.number_of_nodes(),
            'total_edges': G.number_of_edges(),
            'network_density': round(nx.density(G), 4),
            'top_node': top_nodes[0]['node'] if top_nodes else None,
            'top_score': top_nodes[0][args.metric] if top_nodes else 0,
            'hubs_count': len(key_nodes['hubs']),
            'bridges_count': len(key_nodes['bridges']),
            'influencers_count': len(key_nodes['influencers']),
            'processing_time': round(processing_time, 2)
        },
        'details': {
            'centralities': list(centralities.values()),
            'top_nodes': top_nodes,
            'key_nodes': key_nodes
        },
        'metadata': {
            'input_file': args.input,
            'output_file': args.output,
            'metric_used': args.metric,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'performing-centrality-analysis'
        }
    }
    
    # 写入输出文件
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 中心性计算完成")
        print(f"  - 节点数：{G.number_of_nodes()}")
        print(f"  - 边数：{G.number_of_edges()}")
        print(f"  - 网络密度：{output['summary']['network_density']:.4f}")
        print(f"  - 最高{args.metric}节点：{output['summary']['top_node']}")
        print(f"  - 输出文件：{args.output}")
    
    except Exception as e:
        print(f"错误：无法写入输出文件 - {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
