#!/usr/bin/env python3
"""
社会网络中心性计算脚本
计算度中心性、接近中心性和中介中心性
"""

import json
import networkx as nx
import sys

def calculate_centralities():
    # 读取测试网络数据
    with open('test_data/test_network.json', 'r', encoding='utf-8') as f:
        network_data = json.load(f)
    
    # 创建网络图
    G = nx.Graph()
    
    # 添加边
    for edge in network_data['edges']:
        G.add_edge(edge[0], edge[1])
    
    print("=" * 50)
    print("社会网络中心性分析结果")
    print("=" * 50)
    print(f"网络节点数: {G.number_of_nodes()}")
    print(f"网络边数: {G.number_of_edges()}")
    print(f"网络密度: {nx.density(G):.4f}")
    print()
    
    # 计算各种中心性
    degree_cent = nx.degree_centrality(G)
    closeness_cent = nx.closeness_centrality(G)
    betweenness_cent = nx.betweenness_centrality(G)
    
    # 按度中心性排序显示结果
    sorted_nodes = sorted(degree_cent.keys(), key=lambda x: degree_cent[x], reverse=True)
    
    print("节点中心性指标:")
    print("-" * 50)
    print(f"{'节点':<6} {'度中心性':<10} {'接近中心性':<12} {'中介中心性':<12}")
    print("-" * 50)
    
    for node in sorted_nodes:
        print(f"{node:<6} {degree_cent[node]:<10.4f} {closeness_cent[node]:<12.4f} {betweenness_cent[node]:<12.4f}")
    
    print()
    print("关键节点分析:")
    print("-" * 30)
    
    # 找出各种中心性最高的节点
    max_degree_node = max(degree_cent, key=degree_cent.get)
    max_closeness_node = max(closeness_cent, key=closeness_cent.get)
    max_betweenness_node = max(betweenness_cent, key=betweenness_cent.get)
    
    print(f"度中心性最高节点: {max_degree_node} ({degree_cent[max_degree_node]:.4f})")
    print(f"接近中心性最高节点: {max_closeness_node} ({closeness_cent[max_closeness_node]:.4f})")
    print(f"中介中心性最高节点: {max_betweenness_node} ({betweenness_cent[max_betweenness_node]:.4f})")
    
    print()
    print("中心性解释:")
    print("-" * 30)
    print("• 度中心性: 节点的直接连接数量，反映活跃程度")
    print("• 接近中心性: 节点到其他节点的平均距离，反映信息传播效率")
    print("• 中介中心性: 节点在最短路径中出现的频率，反映桥梁作用")
    
    # 保存结果到JSON文件
    results = {
        'network_info': {
            'nodes': G.number_of_nodes(),
            'edges': G.number_of_edges(),
            'density': nx.density(G)
        },
        'centralities': {
            'degree': degree_cent,
            'closeness': closeness_cent,
            'betweenness': betweenness_cent
        },
        'top_nodes': {
            'degree': max_degree_node,
            'closeness': max_closeness_node,
            'betweenness': max_betweenness_node
        }
    }
    
    with open('centrality_analysis_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n分析结果已保存到: centrality_analysis_results.json")

if __name__ == '__main__':
    calculate_centralities()
