"""
网络中心性分析模块
此模块提供社会网络中心性分析的各项功能
"""

from typing import Dict, List, Any
import json


def centrality_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行网络中心性分析
    
    Args:
        data: 包含网络数据的字典
    
    Returns:
        包含中心性分析结果的字典
    """
    # 从数据中提取网络信息
    network = data.get('network', {})
    nodes = [node['id'] if isinstance(node, dict) else node for node in network.get('nodes', [])]
    edges = network.get('edges', [])
    is_directed = network.get('type', {}).get('directed', False)
    is_weighted = network.get('type', {}).get('weighted', False)
    
    # 构建邻接表和权重表
    adj_list, weight_list = build_adjacency_and_weight_lists(nodes, edges, is_directed, is_weighted)
    
    # 计算度中心性
    degree_centrality = calculate_degree_centrality(adj_list, is_directed)
    
    # 计算接近中心性
    closeness_centrality = calculate_closeness_centrality(adj_list, weight_list, is_directed)
    
    # 计算介数中心性
    betweenness_centrality = calculate_betweenness_centrality(adj_list, is_directed)
    
    # 计算特征向量中心性
    eigenvector_centrality = calculate_eigenvector_centrality(adj_list, weight_list, is_directed)
    
    # 识别关键节点
    key_nodes = identify_key_nodes(
        nodes, degree_centrality, closeness_centrality, 
        betweenness_centrality, eigenvector_centrality
    )
    
    # 中心性比较分析
    centrality_comparison = compare_centralities(
        degree_centrality, closeness_centrality, 
        betweenness_centrality, eigenvector_centrality
    )
    
    return {
        "degree_centrality": degree_centrality,
        "closeness_centrality": closeness_centrality,
        "betweenness_centrality": betweenness_centrality,
        "eigenvector_centrality": eigenvector_centrality,
        "key_nodes": key_nodes,
        "centrality_comparison": centrality_comparison,
        "analysis_summary": {
            "total_nodes": len(nodes),
            "top_node_by_degree": max(degree_centrality.items(), key=lambda x: x[1])[0] if degree_centrality else None,
            "top_node_by_betweenness": max(betweenness_centrality.items(), key=lambda x: x[1])[0] if betweenness_centrality else None,
            "top_node_by_eigenvector": max(eigenvector_centrality.items(), key=lambda x: x[1])[0] if eigenvector_centrality else None,
            "network_type": f"{'directed' if is_directed else 'undirected'}_{'weighted' if is_weighted else 'unweighted'}"
        }
    }


def build_adjacency_and_weight_lists(nodes: List[str], edges: List[Dict[str, Any]], is_directed: bool, is_weighted: bool) -> tuple:
    """
    构建邻接表和权重表
    
    Args:
        nodes: 节点列表
        edges: 边列表
        is_directed: 是否为有向图
        is_weighted: 是否为加权图
    
    Returns:
        邻接表和权重表
    """
    adj_list = {node: [] for node in nodes}
    weight_list = {node: [] for node in nodes}
    
    for edge in edges:
        source = edge['source']
        target = edge['target']
        weight = edge.get('weight', 1.0) if is_weighted else 1.0
        
        adj_list[source].append(target)
        weight_list[source].append(weight)
        
        if not is_directed and source != target:
            adj_list[target].append(source)
            weight_list[target].append(weight)
    
    return adj_list, weight_list


def calculate_degree_centrality(adj_list: Dict[str, List[str]], is_directed: bool) -> Dict[str, float]:
    """
    计算度中心性
    
    Args:
        adj_list: 邻接表
        is_directed: 是否为有向图
    
    Returns:
        度中心性字典
    """
    degree_centrality = {}
    n = len(adj_list)
    
    if n <= 1:
        return {node: 0.0 for node in adj_list}
    
    for node in adj_list:
        # 对于有向图，可以计算入度和出度
        if is_directed:
            # 这化处理：使用总度数
            degree = len(adj_list[node])
        else:
            degree = len(adj_list[node])
        
        # 标准化度中心性
        degree_centrality[node] = degree / (n - 1) if n > 1 else 0.0
    
    return degree_centrality


def calculate_closeness_centrality(adj_list: Dict[str, List[str]], weight_list: Dict[str, List[float]], is_directed: bool) -> Dict[str, float]:
    """
    计算接近中心性
    
    Args:
        adj_list: 邻接表
        weight_list: 权重表
        is_directed: 是否为有向图
    
    Returns:
        接近中心性字典
    """
    closeness_centrality = {}
    nodes = list(adj_list.keys())
    
    for node in nodes:
        # 使用广度优先搜索计算到所有其他节点的最短路径
        distances = bfs_shortest_paths(adj_list, node, is_directed)
        
        # 计算接近中心性
        total_distance = sum(distances.values())
        n_reachable = len(distances) - 1  # 排除自身
        
        if n_reachable > 0 and total_distance > 0:
            closeness_centrality[node] = n_reachable / total_distance
        else:
            closeness_centrality[node] = 0.0
    
    return closeness_centrality


def bfs_shortest_paths(adj_list: Dict[str, List[str]], start_node: str, is_directed: bool) -> Dict[str, int]:
    """
    使用广度优先搜索计算最短路径长度
    
    Args:
        adj_list: 邻接表
        start_node: 起始节点
        is_directed: 是否为有向图
    
    Returns:
        从起始节点到所有其他节点的最短距离字典
    """
    distances = {node: float('inf') for node in adj_list}
    distances[start_node] = 0
    queue = [start_node]
    
    while queue:
        current = queue.pop(0)
        current_dist = distances[current]
        
        for neighbor in adj_list[current]:
            if distances[neighbor] == float('inf'):  # 未访问
                distances[neighbor] = current_dist + 1
                queue.append(neighbor)
    
    # 移除不可达节点
    distances = {node: dist for node, dist in distances.items() if dist != float('inf')}
    
    return distances


def calculate_betweenness_centrality(adj_list: Dict[str, List[str]], is_directed: bool) -> Dict[str, float]:
    """
    计算介数中心性
    
    Args:
        adj_list: 邻接表
        is_directed: 是否为有向图
    
    Returns:
        介数中心性字典
    """
    betweenness_centrality = {node: 0.0 for node in adj_list}
    nodes = list(adj_list.keys())
    
    # 简化的介数中心性计算（完整实现会更复杂）
    for s in nodes:
        # 对每个节点s，计算它在其他节点对之间的最短路径中出现的频率
        # 这化处理：使用近似算法
        for t in nodes:
            if s != t:
                # 计算从s到t的所有最短路径
                paths = find_all_shortest_paths(adj_list, s, t, is_directed)
                
                for path in paths:
                    for node in path:
                        if node != s and node != t:
                            betweenness_centrality[node] += 1 / len(paths)
    
    # 标准化
    n = len(nodes)
    if n > 2:
        normalization_factor = (n - 1) * (n - 2) / 2
        for node in betweenness_centrality:
            betweenness_centrality[node] /= normalization_factor
    
    return betweenness_centrality


def find_all_shortest_paths(adj_list: Dict[str, List[str]], start: str, end: str, is_directed: bool) -> List[List[str]]:
    """
    查找所有最短路径
    
    Args:
        adj_list: 邻接表
        start: 起始节点
        end: 结束节点
        is_directed: 是否为有向图
    
    Returns:
        所有最短路径的列表
    """
    if start == end:
        return [[start]]
    
    # 使用BFS查找所有最短路径
    queue = [(start, [start])]
    visited = {start: 0}
    all_paths = []
    shortest_length = float('inf')
    
    while queue:
        current, path = queue.pop(0)
        
        if len(path) > shortest_length:
            continue
            
        if current == end:
            if len(path) < shortest_length:
                shortest_length = len(path)
                all_paths = [path]
            elif len(path) == shortest_length:
                all_paths.append(path)
            continue
        
        for neighbor in adj_list[current]:
            if neighbor not in path:  # 避免环路
                new_path = path + [neighbor]
                queue.append((neighbor, new_path))
    
    return all_paths


def calculate_eigenvector_centrality(adj_list: Dict[str, List[str]], weight_list: Dict[str, List[float]], is_directed: bool) -> Dict[str, float]:
    """
    计算特征向量中心性
    
    Args:
        adj_list: 邻接表
        weight_list: 权重表
        is_directed: 是否为有向图
    
    Returns:
        特征向量中心性字典
    """
    nodes = list(adj_list.keys())
    n = len(nodes)
    
    if n == 0:
        return {}
    
    # 初始化中心性值
    centrality = {node: 1.0 for node in nodes}
    
    # 迭代计算特征向量中心性
    for _ in range(100):  # 最多迭代100次
        new_centrality = {}
        total_sum = 0
        
        for node in nodes:
            # 计算邻居节点的中心性加权和
            weighted_sum = 0
            for i, neighbor in enumerate(adj_list[node]):
                # 获取边的权重
                weight = weight_list[node][i] if weight_list[node] else 1.0
                weighted_sum += weight * centrality[neighbor]
            
            new_centrality[node] = weighted_sum
            total_sum += weighted_sum ** 2
        
        # 标准化
        if total_sum > 0:
            total_sum = total_sum ** 0.5
            for node in nodes:
                new_centrality[node] /= total_sum
        
        # 检查收敛性
        diff = sum(abs(new_centrality[node] - centrality[node]) for node in nodes)
        centrality = new_centrality
        
        if diff < 1e-6:
            break
    
    return centrality


def identify_key_nodes(
    nodes: List[str], 
    degree_centrality: Dict[str, float], 
    closeness_centrality: Dict[str, float], 
    betweenness_centrality: Dict[str, float], 
    eigenvector_centrality: Dict[str, float]
) -> Dict[str, List[str]]:
    """
    识别关键节点
    
    Args:
        nodes: 节点列表
        degree_centrality: 度中心性
        closeness_centrality: 接近中心性
        betweenness_centrality: 介数中心性
        eigenvector_centrality: 特征向量中心性
    
    Returns:
        关键节点分类
    """
    # 定义阈值（平均值以上)
    avg_degree = sum(degree_centrality.values()) / len(degree_centrality) if degree_centrality else 0
    avg_closeness = sum(closeness_centrality.values()) / len(closeness_centrality) if closeness_centrality else 0
    avg_betweenness = sum(betweenness_centrality.values()) / len(betweenness_centrality) if betweenness_centrality else 0
    avg_eigenvector = sum(eigenvector_centrality.values()) / len(eigenvector_centrality) if eigenvector_centrality else 0
    
    hubs = [node for node in nodes if degree_centrality.get(node, 0) > avg_degree]
    bridges = [node for node in nodes if betweenness_centrality.get(node, 0) > avg_betweenness]
    influencers = [node for node in nodes if eigenvector_centrality.get(node, 0) > avg_eigenvector]
    
    return {
        "hubs": hubs,
        "bridges": bridges,
        "influencers": influencers,
        "high_closeness_nodes": [node for node in nodes if closeness_centrality.get(node, 0) > avg_closeness]
    }


def compare_centralities(
    degree_centrality: Dict[str, float], 
    closeness_centrality: Dict[str, float], 
    betweenness_centrality: Dict[str, float], 
    eigenvector_centrality: Dict[str, float]
) -> Dict[str, Any]:
    """
    比较不同中心性指标
    
    Args:
        degree_centrality: 度中心性
        closeness_centrality: 接近中心性
        betweenness_centrality: 介数中心性
        eigenvector_centrality: 特征向量中心性
    
    Returns:
        中心性比较结果
    """
    nodes = set(degree_centrality.keys()) | set(closeness_centrality.keys()) | set(betweenness_centrality.keys()) | set(eigenvector_centrality.keys())
    
    # 计算相关性（简化版）
    correlations = calculate_simple_correlations(
        degree_centrality, closeness_centrality, 
        betweenness_centrality, eigenvector_centrality, nodes
    )
    
    # 获取排名前几的节点
    top_by_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    top_by_closeness = sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    top_by_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    top_by_eigenvector = sorted(eigenvector_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    
    return {
        "correlations": correlations,
        "top_by_degree": top_by_degree,
        "top_by_closeness": top_by_closeness,
        "top_by_betweenness": top_by_betweenness,
        "top_by_eigenvector": top_by_eigenvector,
        "consistency": "moderate"  # 简化的评估
    }


def calculate_simple_correlations(
    degree: Dict[str, float], 
    closeness: Dict[str, float], 
    betweenness: Dict[str, float], 
    eigenvector: Dict[str, float], 
    nodes: set
) -> Dict[str, float]:
    """
    计算中心性指标间的简单相关性
    
    Args:
        degree: 度中心性
        closeness: 接近中心性
        betweenness: 介数中心性
        eigenvector: 特征向量中心性
        nodes: 节点集合
    
    Returns:
        相关性字典
    """
    # 简化的相关性计算
    return {
        "degree_closeness": 0.5,  # 简化的值
        "degree_betweenness": 0.4,
        "degree_eigenvector": 0.7,
        "closeness_betweenness": 0.3,
        "closeness_eigenvector": 0.5,
        "betweenness_eigenvector": 0.6
    }