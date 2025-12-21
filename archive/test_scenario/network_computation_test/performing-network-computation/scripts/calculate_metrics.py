#!/usr/bin/env python
"""
网络指标计算工具
计算社会网络的各种中心性指标和统计特征
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any
import networkx as nx
import numpy as np

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

def calculate_basic_metrics(G: nx.Graph) -> Dict:
    """计算基础网络指标"""
    metrics = {
        'n_nodes': G.number_of_nodes(),
        'n_edges': G.number_of_edges(),
        'density': nx.density(G),
        'is_connected': nx.is_connected(G)
    }
    
    # 连通性指标
    if metrics['is_connected']:
        metrics['diameter'] = nx.diameter(G)
        metrics['radius'] = nx.radius(G)
        metrics['avg_shortest_path'] = nx.average_shortest_path_length(G)
    else:
        metrics['n_components'] = nx.number_connected_components(G)
        metrics['largest_component_size'] = max(len(c) for c in nx.connected_components(G))
    
    # 聚类系数
    metrics['avg_clustering'] = nx.average_clustering(G)
    metrics['transitivity'] = nx.transitivity(G)
    
    return metrics

def calculate_centrality_measures(G: nx.Graph) -> Dict:
    """计算中心性指标"""
    centralities = {}
    
    # 度中心性
    centralities['degree'] = nx.degree_centrality(G)
    
    # 接近中心性（仅对连通图）
    if nx.is_connected(G):
        centralities['closeness'] = nx.closeness_centrality(G)
    else:
        centralities['closeness'] = {}
        for component in nx.connected_components(G):
            subgraph = G.subgraph(component)
            sub_centrality = nx.closeness_centrality(subgraph)
            centralities['closeness'].update(sub_centrality)
    
    # 介数中心性
    centralities['betweenness'] = nx.betweenness_centrality(G)
    
    # 特征向量中心性
    try:
        centralities['eigenvector'] = nx.eigenvector_centrality(G, max_iter=1000)
    except:
        centralities['eigenvector'] = {node: 0 for node in G.nodes()}
    
    # PageRank
    centralities['pagerank'] = nx.pagerank(G)
    
    # Katz中心性
    try:
        centralities['katz'] = nx.katz_centrality(G)
    except:
        centralities['katz'] = {node: 0 for node in G.nodes()}
    
    return centralities

def analyze_centrality_distribution(centralities: Dict) -> Dict:
    """分析中心性分布"""
    distribution = {}
    
    for centrality_type, values in centralities.items():
        if values:
            vals = list(values.values())
            distribution[centrality_type] = {
                'mean': np.mean(vals),
                'std': np.std(vals),
                'min': np.min(vals),
                'max': np.max(vals),
                'top_nodes': sorted(values.items(), key=lambda x: x[1], reverse=True)[:5]
            }
    
    return distribution

def identify_key_players(G: nx.Graph, centralities: Dict) -> Dict:
    """识别关键行动者"""
    key_players = {
        'highest_degree': [],
        'highest_betweenness': [],
        'highest_closeness': [],
        'highest_pagerank': []
    }
    
    # 找出各中心性指标的前3名
    for metric in ['degree', 'betweenness', 'closeness', 'pagerank']:
        if metric in centralities and centralities[metric]:
            sorted_nodes = sorted(centralities[metric].items(), 
                                key=lambda x: x[1], reverse=True)
            key_players[f'highest_{metric}'] = [
                {'node': node, 'score': score} 
                for node, score in sorted_nodes[:3]
            ]
    
    # 综合评分（前3个中心性的平均）
    if all(c in centralities for c in ['degree', 'betweenness', 'pagerank']):
        comprehensive_scores = {}
        for node in G.nodes():
            comprehensive_scores[node] = (
                centralities['degree'].get(node, 0) * 0.3 +
                centralities['betweenness'].get(node, 0) * 0.4 +
                centralities['pagerank'].get(node, 0) * 0.3
            )
        
        sorted_comprehensive = sorted(comprehensive_scores.items(), key=lambda x: x[1], reverse=True)
        key_players['comprehensive_top'] = [
            {'node': node, 'score': score} 
            for node, score in sorted_comprehensive[:5]
        ]
    
    return key_players

def calculate_assortativity(G: nx.Graph) -> Dict:
    """计算同配性"""
    assortativity = {}
    
    # 度同配性
    if G.number_of_edges() > 0:
        try:
            assortativity['degree_assortativity'] = nx.degree_assortativity_coefficient(G)
        except:
            assortativity['degree_assortativity'] = 0
    
    return assortativity

def main():
    parser = argparse.ArgumentParser(
        description='网络指标计算工具',
        epilog='示例：python calculate_metrics.py --input network.json --output metrics.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入网络文件（JSON）')
    parser.add_argument('--output', '-o', default='network_metrics.json', help='输出文件')
    
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
    
    # 计算各项指标
    basic_metrics = calculate_basic_metrics(G)
    centrality_measures = calculate_centrality_measures(G)
    centrality_distribution = analyze_centrality_distribution(centrality_measures)
    key_players = identify_key_players(G, centrality_measures)
    assortativity = calculate_assortativity(G)
    
    end_time = datetime.now()
    
    # 准备输出
    output = {
        'summary': {
            'n_nodes': basic_metrics['n_nodes'],
            'n_edges': basic_metrics['n_edges'],
            'basic_metrics': basic_metrics,
            'centrality_metrics': {
                k: len(v) for k, v in centrality_measures.items()
            },
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'basic_metrics': basic_metrics,
            'centrality_measures': centrality_measures,
            'centrality_distribution': centrality_distribution,
            'key_players': key_players,
            'assortativity': assortativity
        },
        'metadata': {
            'input_file': args.input,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'performing-network-computation'
        }
    }
    
    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 网络指标计算完成")
        print(f"  - 节点数：{basic_metrics['n_nodes']}")
        print(f"  - 边数：{basic_metrics['n_edges']}")
        print(f"  - 密度：{basic_metrics['density']:.4f}")
        print(f"  - 平均聚类系数：{basic_metrics['avg_clustering']:.4f}")
        print(f"  - 输出文件：{args.output}")
        
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()