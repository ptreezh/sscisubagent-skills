#!/usr/bin/env python
"""
网络可视化工具
生成社会网络的可视化图表
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Tuple
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # 使用非交互式后端
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

def load_centrality_data(centrality_file: str) -> Dict:
    """加载中心性数据"""
    try:
        with open(centrality_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('details', {}).get('centrality_measures', {})
    except:
        return {}

def get_layout_positions(G: nx.Graph, layout_type: str) -> Dict:
    """获取节点布局位置"""
    if layout_type == 'spring':
        return nx.spring_layout(G, k=1, iterations=50)
    elif layout_type == 'circular':
        return nx.circular_layout(G)
    elif layout_type == 'random':
        return nx.random_layout(G)
    elif layout_type == 'shell':
        return nx.shell_layout(G)
    else:
        return nx.spring_layout(G)

def get_node_colors(G: nx.Graph, color_by: str, centrality_data: Dict) -> List:
    """获取节点颜色"""
    n = len(G.nodes())
    
    if color_by == 'centrality' and 'degree' in centrality_data:
        # 使用度中心性着色
        values = [centrality_data['degree'].get(node, 0) for node in G.nodes()]
        return plt.cm.viridis(values)
    elif color_by == 'community':
        # 使用社区信息着色（简化版，基于连通分量）
        communities = list(nx.connected_components(G))
        colors = []
        for node in G.nodes():
            for i, community in enumerate(communities):
                if node in community:
                    colors.append(plt.cm.Set3(i / len(communities)))
                    break
        return colors
    else:
        # 默认颜色
        return ['skyblue'] * n

def get_node_sizes(G: nx.Graph, size_by: str, centrality_data: Dict) -> List:
    """获取节点大小"""
    if size_by == 'centrality' and 'degree' in centrality_data:
        # 基于度中心性
        values = [centrality_data['degree'].get(node, 0) for node in G.nodes()]
        # 归一化到合理范围
        min_val, max_val = min(values), max(values)
        if max_val > min_val:
            normalized = [(v - min_val) / (max_val - min_val) for v in values]
            return [300 + 700 * v for v in normalized]  # 300-1000
        else:
            return [500] * len(values)
    elif size_by == 'degree':
        # 基于实际度数
        degrees = [G.degree(node) for node in G.nodes()]
        max_degree = max(degrees) if degrees else 1
        return [300 + 700 * d / max_degree for d in degrees]
    else:
        # 默认大小
        return [500] * len(G.nodes())

def create_network_visualization(G: nx.Graph, pos: Dict, output_file: str,
                               node_colors: List, node_sizes: List,
                               title: str = "社会网络可视化"):
    """创建网络可视化图"""
    plt.figure(figsize=(12, 10))
    
    # 绘制边
    nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color='gray', width=1)
    
    # 绘制节点
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, 
                          node_size=node_sizes, alpha=0.8)
    
    # 绘制标签
    nx.draw_networkx_labels(G, pos, font_size=10, font_family='SimHei')
    
    plt.title(title, fontsize=16, fontfamily='SimHei')
    plt.axis('off')
    plt.tight_layout()
    
    # 保存图片
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def create_centrality_distribution_plot(centrality_data: Dict, output_file: str):
    """创建中心性分布图"""
    if not centrality_data:
        return
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('网络中心性指标分布', fontsize=16, fontfamily='SimHei')
    
    centrality_types = ['degree', 'betweenness', 'closeness', 'pagerank']
    titles = ['度中心性', '介数中心性', '接近中心性', 'PageRank']
    
    for i, (cent_type, title) in enumerate(zip(centrality_types, titles)):
        ax = axes[i // 2, i % 2]
        
        if cent_type in centrality_data:
            values = list(centrality_data[cent_type].values())
            ax.hist(values, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
            ax.set_title(title, fontfamily='SimHei')
            ax.set_xlabel('中心性值', fontfamily='SimHei')
            ax.set_ylabel('频次', fontfamily='SimHei')
            ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def create_community_visualization(G: nx.Graph, communities: Dict, 
                                 output_file: str):
    """创建社区可视化图"""
    if not communities:
        return
    
    pos = nx.spring_layout(G)
    
    plt.figure(figsize=(12, 10))
    
    # 为每个社区分配颜色
    community_map = communities.get('node_to_community', {})
    n_communities = communities.get('n_communities', 1)
    colors = plt.cm.Set3(np.linspace(0, 1, n_communities))
    
    # 按社区绘制节点
    for i, community_nodes in enumerate(communities.get('communities', [])):
        node_color = colors[i]
        nx.draw_networkx_nodes(G, pos, nodelist=list(community_nodes),
                              node_color=[node_color], node_size=500,
                              alpha=0.8, label=f'社区 {i+1}')
    
    # 绘制边和标签
    nx.draw_networkx_edges(G, pos, alpha=0.3, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, fontfamily='SimHei')
    
    plt.title('网络社区结构', fontsize=16, fontfamily='SimHei')
    plt.legend(prop={'family': 'SimHei'})
    plt.axis('off')
    plt.tight_layout()
    
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    plt.close()

def main():
    parser = argparse.ArgumentParser(
        description='网络可视化工具',
        epilog='示例：python visualize_network.py --input network.json --output network.png'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入网络文件（JSON）')
    parser.add_argument('--output', '-o', default='network_visualization.png', help='输出图片文件')
    parser.add_argument('--layout', '-l',
                       choices=['spring', 'circular', 'random', 'shell'],
                       default='spring',
                       help='布局类型')
    parser.add_argument('--color-by', '-c',
                       choices=['centrality', 'community', 'default'],
                       default='default',
                       help='节点着色依据')
    parser.add_argument('--size-by', '-s',
                       choices=['centrality', 'degree', 'default'],
                       default='default',
                       help='节点大小依据')
    parser.add_argument('--centrality-file',
                       help='中心性数据文件（用于着色和大小）')
    parser.add_argument('--communities-file',
                       help='社区数据文件（用于社区可视化）')
    parser.add_argument('--title', '-t',
                       default='社会网络可视化',
                       help='图表标题')
    
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
    
    # 加载额外数据
    centrality_data = {}
    if args.centrality_file:
        centrality_data = load_centrality_data(args.centrality_file)
    
    # 获取布局和样式
    pos = get_layout_positions(G, args.layout)
    node_colors = get_node_colors(G, args.color_by, centrality_data)
    node_sizes = get_node_sizes(G, args.size_by, centrality_data)
    
    # 创建主网络图
    create_network_visualization(G, pos, args.output, 
                               node_colors, node_sizes, args.title)
    
    # 创建额外的可视化（如果有数据）
    base_name = args.output.rsplit('.', 1)[0]
    
    if centrality_data:
        centrality_output = f"{base_name}_centrality_distribution.png"
        create_centrality_distribution_plot(centrality_data, centrality_output)
        print(f"  - 中心性分布图：{centrality_output}")
    
    if args.communities_file:
        try:
            with open(args.communities_file, 'r', encoding='utf-8') as f:
                communities_data = json.load(f)
            
            communities = communities_data.get('details', {}).get('community_detection', {})
            if communities:
                community_output = f"{base_name}_communities.png"
                create_community_visualization(G, communities, community_output)
                print(f"  - 社区结构图：{community_output}")
        except:
            pass
    
    end_time = datetime.now()
    
    print(f"✓ 网络可视化完成")
    print(f"  - 节点数：{G.number_of_nodes()}")
    print(f"  - 边数：{G.number_of_edges()}")
    print(f"  - 布局：{args.layout}")
    print(f"  - 输出文件：{args.output}")
    print(f"  - 处理时间：{(end_time - start_time).total_seconds():.2f}秒")

if __name__ == '__main__':
    main()