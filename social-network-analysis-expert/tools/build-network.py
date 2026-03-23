"""
网络构建工具
从边列表构建 NetworkX 网络对象
"""

import networkx as nx
from typing import List, Dict, Tuple, Optional


def build_network(edges: List[Tuple[str, str]], 
                  directed: bool = False,
                  weighted: bool = False,
                  edge_weights: Optional[List[float]] = None) -> nx.Graph:
    """
    从边列表构建网络
    
    参数:
        edges: 边列表 [(node1, node2), ...]
        directed: 是否是有向网络
        weighted: 是否是加权网络
        edge_weights: 边权重列表
    
    返回:
        NetworkX 网络对象
    """
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    
    # 添加边
    if weighted and edge_weights:
        for (u, v), w in zip(edges, edge_weights):
            G.add_edge(u, v, weight=w)
    else:
        G.add_edges_from(edges)
    
    return G


def calculate_basic_metrics(G: nx.Graph) -> Dict:
    """
    计算基础网络指标
    
    参数:
        G: NetworkX 网络对象
    
    返回:
        基础指标字典
    """
    metrics = {
        'num_nodes': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
        'density': nx.density(G),
        'is_directed': G.is_directed(),
        'is_connected': nx.is_connected(G) if not G.is_directed() else nx.is_weakly_connected(G),
    }
    
    # 连通分量
    if G.is_directed():
        metrics['num_weakly_components'] = nx.number_weakly_connected_components(G)
    else:
        metrics['num_components'] = nx.number_connected_components(G)
    
    # 平均度数
    if G.number_of_nodes() > 0:
        metrics['avg_degree'] = 2 * G.number_of_edges() / G.number_of_nodes()
    
    return metrics


def validate_network(edges: List[Tuple[str, str]]) -> Dict:
    """
    验证网络数据
    
    参数:
        edges: 边列表
    
    返回:
        验证结果
    """
    issues = []
    
    # 检查边列表是否为空
    if not edges:
        issues.append({
            'code': 'EMPTY_NETWORK',
            'message': '网络数据为空',
            'severity': 'error'
        })
        return {'valid': False, 'issues': issues}
    
    # 检查边格式
    for i, edge in enumerate(edges):
        if not isinstance(edge, (list, tuple)) or len(edge) != 2:
            issues.append({
                'code': 'INVALID_EDGE_FORMAT',
                'message': f'边 {i} 格式错误, 应该是 (node1, node2)',
                'severity': 'error'
            })
    
    # 检查节点数量
    nodes = set()
    for edge in edges:
        nodes.add(edge[0])
        nodes.add(edge[1])
    
    if len(nodes) < 3:
        issues.append({
            'code': 'NETWORK_TOO_SMALL',
            'message': '网络太小, 至少需要 3 个节点',
            'severity': 'warning'
        })
    
    if len(edges) < 2:
        issues.append({
            'code': 'TOO_FEW_EDGES',
            'message': '边太少, 至少需要 2 条边',
            'severity': 'warning'
        })
    
    return {
        'valid': len([i for i in issues if i['severity'] == 'error']) == 0,
        'issues': issues,
        'num_nodes': len(nodes),
        'num_edges': len(edges)
    }


def build_network_from_adjacency_matrix(matrix: List[List[float]], 
                                        node_names: Optional[List[str]] = None) -> nx.Graph:
    """
    从邻接矩阵构建网络
    
    参数:
        matrix: 邻接矩阵
        node_names: 节点名称列表
    
    返回:
        NetworkX 网络对象
    """
    import numpy as np
    
    matrix = np.array(matrix)
    
    if node_names is None:
        node_names = [f'Node_{i}' for i in range(matrix.shape[0])]
    
    G = nx.from_numpy_array(matrix)
    
    # 重命名节点
    mapping = {i: name for i, name in enumerate(node_names)}
    G = nx.relabel_nodes(G, mapping)
    
    return G


if __name__ == '__main__':
    # 测试
    edges = [('A', 'B'), ('B', 'C'), ('C', 'D'), ('D', 'E')]
    
    # 验证
    validation = validate_network(edges)
    print(f"验证结果：{validation}")
    
    # 构建网络
    G = build_network(edges)
    print(f"网络：{G.number_of_nodes()} 节点, {G.number_of_edges()} 边")
    
    # 基础指标
    metrics = calculate_basic_metrics(G)
    print(f"基础指标：{metrics}")
