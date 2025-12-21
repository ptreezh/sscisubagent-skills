#!/usr/bin/env python
"""
网络构建工具
将各种格式的数据转换为网络图结构
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Tuple
import networkx as nx

def build_from_edgelist(edges: List[Dict]) -> nx.Graph:
    """从边列表构建网络"""
    G = nx.Graph()
    
    for edge in edges:
        source = edge.get('source', '')
        target = edge.get('target', '')
        weight = edge.get('weight', 1.0)
        
        if source and target:
            G.add_edge(source, target, weight=weight)
    
    return G

def build_from_adjacency_matrix(matrix: List[List[float]], node_labels: List[str]) -> nx.Graph:
    """从邻接矩阵构建网络"""
    G = nx.Graph()
    
    # 添加节点
    for i, label in enumerate(node_labels):
        G.add_node(label)
    
    # 添加边
    n = len(matrix)
    for i in range(n):
        for j in range(i+1, n):
            if matrix[i][j] > 0:
                G.add_edge(node_labels[i], node_labels[j], weight=matrix[i][j])
    
    return G

def build_from_survey(survey_data: List[Dict]) -> nx.Graph:
    """从调查数据构建网络"""
    G = nx.Graph()
    
    # 假设调查数据包含关系信息
    for record in survey_data:
        respondent = record.get('respondent', '')
        connections = record.get('connections', [])
        
        if respondent:
            G.add_node(respondent)
            
            for connection in connections:
                target = connection.get('target', '')
                strength = connection.get('strength', 1.0)
                
                if target:
                    G.add_edge(respondent, target, weight=strength)
    
    return G

def add_node_attributes(G: nx.Graph, attributes: Dict[str, Dict]) -> nx.Graph:
    """添加节点属性"""
    for node, attrs in attributes.items():
        if node in G.nodes:
            G.nodes[node].update(attrs)
    
    return G

def add_edge_weights(G: nx.Graph, weights: Dict[Tuple[str, str], float]) -> nx.Graph:
    """添加边权重"""
    for (source, target), weight in weights.items():
        if G.has_edge(source, target):
            G.edges[source, target]['weight'] = weight
    
    return G

def validate_network(G: nx.Graph) -> Dict:
    """验证网络结构"""
    validation = {
        'is_valid': True,
        'warnings': [],
        'errors': []
    }
    
    # 检查节点数
    n_nodes = G.number_of_nodes()
    if n_nodes == 0:
        validation['errors'].append('网络没有节点')
        validation['is_valid'] = False
    elif n_nodes == 1:
        validation['warnings'].append('网络只有一个节点')
    
    # 检查边数
    n_edges = G.number_of_edges()
    if n_edges == 0 and n_nodes > 1:
        validation['warnings'].append('网络有多个节点但没有边')
    
    # 检查连通性
    if not nx.is_connected(G):
        validation['warnings'].append('网络不连通')
        components = list(nx.connected_components(G))
        validation['n_components'] = len(components)
    
    # 检查权重
    has_weights = any('weight' in G.edges[edge] for edge in G.edges)
    if not has_weights and n_edges > 0:
        validation['warnings'].append('边没有权重信息')
    
    return validation

def clean_network(G: nx.Graph, remove_isolates: bool = True, 
                  remove_self_loops: bool = True) -> nx.Graph:
    """清理网络"""
    # 移除自环
    if remove_self_loops:
        G.remove_edges_from(nx.selfloop_edges(G))
    
    # 移除孤立节点
    if remove_isolates:
        G.remove_nodes_from(list(nx.isolates(G)))
    
    return G

def get_network_summary(G: nx.Graph) -> Dict:
    """获取网络摘要信息"""
    summary = {
        'n_nodes': G.number_of_nodes(),
        'n_edges': G.number_of_edges(),
        'density': nx.density(G),
        'is_directed': G.is_directed(),
        'is_multigraph': G.is_multigraph()
    }
    
    # 连通性信息
    if G.number_of_nodes() > 0:
        summary['is_connected'] = nx.is_connected(G)
        if not summary['is_connected']:
            summary['n_components'] = nx.number_connected_components(G)
        
        # 路径信息（仅对连通图）
        if summary['is_connected']:
            summary['diameter'] = nx.diameter(G)
            summary['average_shortest_path_length'] = nx.average_shortest_path_length(G)
            summary['radius'] = nx.radius(G)
    
    return summary

def main():
    parser = argparse.ArgumentParser(
        description='网络构建工具',
        epilog='示例：python build_network.py --input data.json --output network.json --type edgelist'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--output', '-o', default='network.json', help='输出文件')
    parser.add_argument('--type', '-t', 
                       choices=['edgelist', 'matrix', 'survey'],
                       default='edgelist',
                       help='输入数据类型')
    parser.add_argument('--remove-isolates', action='store_true',
                       help='移除孤立节点')
    parser.add_argument('--remove-self-loops', action='store_true',
                       help='移除自环')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 构建网络
    try:
        if args.type == 'edgelist':
            edges = data if isinstance(data, list) else data.get('edges', [])
            G = build_from_edgelist(edges)
        elif args.type == 'matrix':
            matrix = data.get('matrix', [])
            labels = data.get('node_labels', [])
            G = build_from_adjacency_matrix(matrix, labels)
        elif args.type == 'survey':
            survey_data = data if isinstance(data, list) else data.get('survey_data', [])
            G = build_from_survey(survey_data)
    except Exception as e:
        print(f"错误：网络构建失败 - {e}", file=sys.stderr)
        sys.exit(1)
    
    # 添加属性（如果有）
    if 'node_attributes' in data:
        G = add_node_attributes(G, data['node_attributes'])
    
    # 清理网络
    G = clean_network(G, args.remove_isolates, args.remove_self_loops)
    
    # 验证网络
    validation = validate_network(G)
    
    # 获取摘要
    summary = get_network_summary(G)
    
    end_time = datetime.now()
    
    # 准备输出
    output = {
        'summary': {
            'network_type': args.type,
            'n_nodes': summary['n_nodes'],
            'n_edges': summary['n_edges'],
            'density': round(summary['density'], 4),
            'is_valid': validation['is_valid'],
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'network_summary': summary,
            'validation': validation,
            'nodes': list(G.nodes()),
            'edges': [(u, v, G.edges[u, v]) for u, v in G.edges()]
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
        
        print(f"✓ 网络构建完成")
        print(f"  - 节点数：{summary['n_nodes']}")
        print(f"  - 边数：{summary['n_edges']}")
        print(f"  - 密度：{summary['density']:.4f}")
        print(f"  - 有效性：{'是' if validation['is_valid'] else '否'}")
        print(f"  - 输出文件：{args.output}")
        
        # 显示警告
        if validation['warnings']:
            print("\n警告：")
            for warning in validation['warnings']:
                print(f"  - {warning}")
        
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()