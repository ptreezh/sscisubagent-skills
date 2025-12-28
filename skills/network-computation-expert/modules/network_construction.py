"""
网络构建模块
此模块提供社会网络构建的各项功能
"""

from typing import Dict, List, Any
import json


def network_construction(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行网络构建
    
    Args:
        data: 包含网络数据的字典
    
    Returns:
        包含网络构建结果的字典
    """
    # 从数据中提取相关信息
    nodes = data.get('nodes', [])
    edges = data.get('edges', [])
    node_attributes = data.get('node_attributes', {})
    edge_attributes = data.get('edge_attributes', {})
    network_type = data.get('network_type', 'undirected_unweighted')
    
    # 执行网络格式验证
    format_validation = validate_network_format(nodes, edges, network_type)
    
    # 执行网络构建
    network = construct_network(nodes, edges, network_type)
    
    # 执行网络属性处理
    network_with_attributes = process_network_attributes(network, node_attributes, edge_attributes)
    
    # 执行网络验证
    network_validation = validate_network_properties(network_with_attributes)
    
    # 执行基本网络指标计算
    basic_metrics = calculate_basic_network_metrics(network_with_attributes)
    
    return {
        "format_validation": format_validation,
        "network": network_with_attributes,
        "validation": network_validation,
        "basic_metrics": basic_metrics,
        "construction_summary": {
            "nodes_count": len(network.get('nodes', [])),
            "edges_count": len(network.get('edges', [])),
            "network_type": network_type,
            "density": basic_metrics.get('density', 0.0),
            "connected_components": basic_metrics.get('connected_components', 1)
        }
    }


def validate_network_format(nodes: List[str], edges: List[Dict[str, Any]], network_type: str) -> Dict[str, Any]:
    """
    验证网络格式
    
    Args:
        nodes: 节点列表
        edges: 边列表
        network_type: 网络类型
    
    Returns:
        格式验证结果
    """
    # 检查节点格式
    node_format_valid = all(isinstance(node, str) for node in nodes)
    
    # 检查边格式
    edge_format_valid = True
    for edge in edges:
        if not isinstance(edge, dict) or 'source' not in edge or 'target' not in edge:
            edge_format_valid = False
            break
    
    # 检查节点和边的关联
    all_nodes_in_edges = set()
    for edge in edges:
        all_nodes_in_edges.add(edge['source'])
        all_nodes_in_edges.add(edge['target'])
    
    nodes_in_edges_valid = all_nodes_in_edges.issubset(set(nodes))
    
    return {
        "node_format_valid": node_format_valid,
        "edge_format_valid": edge_format_valid,
        "nodes_edges_consistency": nodes_in_edges_valid,
        "network_type_valid": network_type in ['undirected_unweighted', 'undirected_weighted', 'directed_unweighted', 'directed_weighted'],
        "validation_status": "valid" if all([node_format_valid, edge_format_valid, nodes_in_edges_valid]) else "invalid"
    }


def construct_network(nodes: List[str], edges: List[Dict[str, Any]], network_type: str) -> Dict[str, Any]:
    """
    构建网络
    
    Args:
        nodes: 节点列表
        edges: 边列表
        network_type: 网络类型
    
    Returns:
        构建的网络
    """
    # 根据网络类型构建网络
    is_directed = 'directed' in network_type
    is_weighted = 'weighted' in network_type
    
    # 构建邻接表表示
    adjacency_list = {node: [] for node in nodes}
    
    for edge in edges:
        source = edge['source']
        target = edge['target']
        
        # 添加边到邻接表
        adjacency_list[source].append({
            'target': target,
            'weight': edge.get('weight', 1.0) if is_weighted else 1.0,
            'type': edge.get('type', 'general')
        })
        
        # 如果是无向图，添加反向边
        if not is_directed and source != target:  # 避免自环重复添加
            adjacency_list[target].append({
                'target': source,
                'weight': edge.get('weight', 1.0) if is_weighted else 1.0,
                'type': edge.get('type', 'general')
            })
    
    # 去重（对于无向图，确保每条边只计算一次）
    if not is_directed:
        processed_edges = set()
        unique_edges = []
        for edge in edges:
            # 创建标准化的边表示（对于无向图）
            sorted_edge = tuple(sorted([edge['source'], edge['target']]))
            if sorted_edge not in processed_edges:
                unique_edges.append(edge)
                processed_edges.add(sorted_edge)
        edges = unique_edges
    
    return {
        "nodes": nodes,
        "edges": edges,
        "adjacency_list": adjacency_list,
        "type": {
            "directed": is_directed,
            "weighted": is_weighted
        },
        "node_count": len(nodes),
        "edge_count": len(edges)
    }


def process_network_attributes(network: Dict[str, Any], node_attributes: Dict[str, Any], edge_attributes: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理网络属性
    
    Args:
        network: 网络
        node_attributes: 节点属性
        edge_attributes: 边属性
    
    Returns:
        带属性的网络
    """
    # 添加节点属性
    nodes_with_attributes = []
    for node in network['nodes']:
        node_attr = node_attributes.get(node, {})
        nodes_with_attributes.append({
            'id': node,
            'attributes': node_attr
        })
    
    # 添加边属性
    edges_with_attributes = []
    for edge in network['edges']:
        # 创建边的唯一标识符
        edge_key = f"{edge['source']}-{edge['target']}"
        edge_attr = edge_attributes.get(edge_key, {})
        
        edges_with_attributes.append({
            'source': edge['source'],
            'target': edge['target'],
            'weight': edge.get('weight', 1.0),
            'type': edge.get('type', 'general'),
            'attributes': edge_attr
        })
    
    # 更新网络
    network_with_attributes = network.copy()
    network_with_attributes['nodes'] = nodes_with_attributes
    network_with_attributes['edges'] = edges_with_attributes
    
    return network_with_attributes


def validate_network_properties(network: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证网络属性
    
    Args:
        network: 网络
    
    Returns:
        网络属性验证结果
    """
    nodes = [node['id'] if isinstance(node, dict) else node for node in network['nodes']]
    edges = network['edges']
    
    # 检查网络连通性
    is_connected = check_network_connectivity(nodes, edges, network['type']['directed'])
    
    # 检查自环
    self_loops = [edge for edge in edges if edge['source'] == edge['target']]
    
    # 检查多重边
    edge_set = set()
    multi_edges = []
    for edge in edges:
        edge_tuple = (edge['source'], edge['target'])
        if edge_tuple in edge_set:
            multi_edges.append(edge)
        else:
            edge_set.add(edge_tuple)
    
    return {
        "is_connected": is_connected,
        "self_loops_count": len(self_loops),
        "multi_edges_count": len(multi_edges),
        "node_count": len(nodes),
        "edge_count": len(edges),
        "validation_issues": {
            "self_loops": len(self_loops) > 0,
            "multi_edges": len(multi_edges) > 0,
            "disconnected": not is_connected and len(nodes) > 1
        }
    }


def check_network_connectivity(nodes: List[str], edges: List[Dict[str, Any]], is_directed: bool) -> bool:
    """
    检查网络连通性
    
    Args:
        nodes: 节点列表
        edges: 边列表
        is_directed: 是否为有向图
    
    Returns:
        连通性检查结果
    """
    if len(nodes) <= 1:
        return True
    
    # 构建邻接表
    adj = {node: set() for node in nodes}
    for edge in edges:
        adj[edge['source']].add(edge['target'])
        if not is_directed:
            adj[edge['target']].add(edge['source'])
    
    # 使用广度优先搜索检查连通性
    visited = set()
    queue = [nodes[0]]
    visited.add(nodes[0])
    
    while queue:
        current = queue.pop(0)
        for neighbor in adj[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    # 检查是否所有节点都被访问
    return len(visited) == len(nodes)


def calculate_basic_network_metrics(network: Dict[str, Any]) -> Dict[str, Any]:
    """
    计算基本网络指标
    
    Args:
        network: 网络
    
    Returns:
        基本网络指标
    """
    nodes = [node['id'] if isinstance(node, dict) else node for node in network['nodes']]
    edges = network['edges']
    is_directed = network['type']['directed']
    
    node_count = len(nodes)
    edge_count = len(edges)
    
    # 计算网络密度
    if is_directed:
        max_possible_edges = node_count * (node_count - 1) if node_count > 1 else 0
    else:
        max_possible_edges = node_count * (node_count - 1) // 2 if node_count > 1 else 0
    
    density = edge_count / max_possible_edges if max_possible_edges > 0 else 0.0
    
    # 计算度分布
    degree_dist = calculate_degree_distribution(nodes, edges, is_directed)
    
    # 计算连通分量
    connected_components = calculate_connected_components(nodes, edges, is_directed)
    
    # 计算平均度
    if node_count > 0:
        avg_degree = (2 * edge_count) / node_count if not is_directed else edge_count / node_count
    else:
        avg_degree = 0.0
    
    return {
        "node_count": node_count,
        "edge_count": edge_count,
        "density": density,
        "avg_degree": avg_degree,
        "degree_distribution": degree_dist,
        "connected_components": connected_components,
        "diameter": estimate_diameter(nodes, edges, is_directed),
        "clustering_coefficient": estimate_clustering_coefficient(nodes, edges, is_directed)
    }


def calculate_degree_distribution(nodes: List[str], edges: List[Dict[str, Any]], is_directed: bool) -> Dict[int, int]:
    """
    计算度分布
    
    Args:
        nodes: 节点列表
        edges: 边列表
        is_directed: 是否为有向图
    
    Returns:
        度分布
    """
    # 计算每个节点的度
    degree_count = {node: 0 for node in nodes}
    
    for edge in edges:
        degree_count[edge['source']] += 1
        if not is_directed:
            degree_count[edge['target']] += 1
        # 对于有向图，我们计算的是出度
    
    # 统计度分布
    dist = {}
    for degree in degree_count.values():
        dist[degree] = dist.get(degree, 0) + 1
    
    return dist


def calculate_connected_components(nodes: List[str], edges: List[Dict[str, Any]], is_directed: bool) -> int:
    """
    计算连通分量数量
    
    Args:
        nodes: 节点列表
        edges: 边列表
        is_directed: 是否为有向图
    
    Returns:
        连通分量数量
    """
    if not nodes:
        return 0
    
    # 构建邻接表
    adj = {node: set() for node in nodes}
    for edge in edges:
        adj[edge['source']].add(edge['target'])
        if not is_directed:
            adj[edge['target']].add(edge['source'])
    
    visited = set()
    components = 0
    
    for node in nodes:
        if node not in visited:
            # 发现新连通分量
            components += 1
            # 使用DFS标记所有可达节点
            stack = [node]
            while stack:
                current = stack.pop()
                if current not in visited:
                    visited.add(current)
                    for neighbor in adj[current]:
                        if neighbor not in visited:
                            stack.append(neighbor)
    
    return components


def estimate_diameter(nodes: List[str], edges: List[Dict[str, Any]], is_directed: bool) -> int:
    """
    估算网络直径
    
    Args:
        nodes: 节点列表
        edges: 边列表
        is_directed: 是否为有向图
    
    Returns:
        估算的直径
    """
    # 简化的直径估算 - 在实际应用中，这可能需要更复杂的算法
    if len(nodes) <= 1:
        return 0 if len(nodes) == 0 else 1
    
    # 对于大型网络，返回一个估算值
    if len(nodes) > 100:
        # 使用经验公式估算直径
        import math
        return int(math.log(len(nodes)) / math.log(10) * 3)  # 简化的估算
    
    # 对于小型网络，可以进行精确计算，但这里我们仍使用估算
    return min(len(nodes), 10)  # 限制最大估算值


def estimate_clustering_coefficient(nodes: List[str], edges: List[Dict[str, Any]], is_directed: bool) -> float:
    """
    估算聚类系数
    
    Args:
        nodes: 节点列表
        edges: 边列表
        is_directed: 是否为有向图
    
    Returns:
        估算的聚类系数
    """
    if len(nodes) < 3 or len(edges) < 3:
        return 0.0
    
    # 简化的聚类系数估算
    # 实际计算需要计算每个节点的局部聚类系数，然后取平均值
    # 这化处理：基于网络密度估算
    edge_count = len(edges)
    node_count = len(nodes)
    
    if is_directed:
        max_possible_triangles = node_count * (node_count - 1) * (node_count - 2) / 2
    else:
        max_possible_triangles = node_count * (node_count - 1) * (node_count - 2) / 6
    
    if max_possible_triangles == 0:
        return 0.0
    
    # 简化的估算
    return min(1.0, (edge_count / node_count) / 5)  # 基于平均度的简单估算