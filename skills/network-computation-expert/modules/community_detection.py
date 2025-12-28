"""
社区检测模块
此模块提供社会网络社区检测的各项功能
"""

from typing import Dict, List, Any
import json


def community_detection(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行网络社区检测
    
    Args:
        data: 包含网络数据的字典
    
    Returns:
        包含社区检测结果的字典
    """
    # 从数据中提取网络信息
    network = data.get('network', {})
    nodes = [node['id'] if isinstance(node, dict) else node for node in network.get('nodes', [])]
    edges = network.get('edges', [])
    is_directed = network.get('type', {}).get('directed', False)
    
    # 构建邻接表
    adj_list = build_adjacency_list(nodes, edges, is_directed)
    
    # 应用社区检测算法（Louvain算法的简化版本）
    communities = detect_communities_louvain(adj_list)
    
    # 验证社区结构
    validation_results = validate_community_structure(nodes, communities, adj_list)
    
    # 分析社区间关系
    inter_community_analysis = analyze_inter_community_relationships(communities, adj_list)
    
    # 计算社区指标
    community_metrics = calculate_community_metrics(communities, adj_list)
    
    return {
        "communities": communities,
        "validation": validation_results,
        "inter_community_analysis": inter_community_analysis,
        "community_metrics": community_metrics,
        "detection_summary": {
            "total_communities": len(communities),
            "largest_community_size": max([len(c) for c in communities.values()], default=0),
            "average_community_size": sum([len(c) for c in communities.values()]) / len(communities) if communities else 0,
            "modularity": validation_results.get('modularity', 0.0)
        }
    }


def build_adjacency_list(nodes: List[str], edges: List[Dict[str, Any]], is_directed: bool) -> Dict[str, List[str]]:
    """
    构建邻接表
    
    Args:
        nodes: 节点列表
        edges: 边列表
        is_directed: 是否为有向图
    
    Returns:
        邻接表
    """
    adj_list = {node: [] for node in nodes}
    
    for edge in edges:
        source = edge['source']
        target = edge['target']
        
        adj_list[source].append(target)
        
        if not is_directed and source != target:
            adj_list[target].append(source)
    
    return adj_list


def detect_communities_louvain(adj_list: Dict[str, List[str]]) -> Dict[int, List[str]]:
    """
    使用Louvain算法检测社区（简化版本）
    
    Args:
        adj_list: 邻接表
    
    Returns:
        社区字典，键为社区ID，值为节点列表
    """
    nodes = list(adj_list.keys())
    n = len(nodes)
    
    if n == 0:
        return {}
    
    # 初始化：每个节点为一个社区
    node_to_community = {node: i for i, node in enumerate(nodes)}
    communities = {i: [node] for node, i in node_to_community.items()}
    
    # 简化的Louvain算法实现
    # 第一阶段：尝试将每个节点移动到邻居社区以优化模块度
    improved = True
    iteration = 0
    max_iterations = 10  # 限制迭代次数
    
    while improved and iteration < max_iterations:
        improved = False
        iteration += 1
        
        for node in nodes:
            current_community = node_to_community[node]
            best_community = current_community
            best_gain = 0
            
            # 检查所有邻居社区，找到移动节点的最佳社区
            neighbor_communities = set()
            for neighbor in adj_list[node]:
                neighbor_communities.add(node_to_community[neighbor])
            
            # 评估移动到每个邻居社区的模块度增益
            for target_community in neighbor_communities:
                if target_community != current_community:
                    gain = calculate_modularity_gain(node, target_community, node_to_community, adj_list)
                    if gain > best_gain:
                        best_gain = gain
                        best_community = target_community
            
            # 如果找到了更好的社区，则移动节点
            if best_community != current_community:
                # 从当前社区移除节点
                communities[current_community].remove(node)
                if not communities[current_community]:  # 如果社区为空，删除它
                    del communities[current_community]
                
                # 添加到新社区
                if best_community not in communities:
                    communities[best_community] = []
                communities[best_community].append(node)
                
                # 更新节点到社区的映射
                node_to_community[node] = best_community
                improved = True
    
    # 重新编号社区，使其从0开始连续
    renumbered_communities = {}
    new_id = 0
    for old_id, community_nodes in communities.items():
        if community_nodes:  # 只有非空社区才保留
            renumbered_communities[new_id] = community_nodes
            # 更新节点到社区的映射
            for node in community_nodes:
                node_to_community[node] = new_id
            new_id += 1
    
    return renumbered_communities


def calculate_modularity_gain(node: str, target_community: int, node_to_community: Dict[str, int], adj_list: Dict[str, List[str]]) -> float:
    """
    计算将节点移动到目标社区的模块度增益
    
    Args:
        node: 节点
        target_community: 目标社区
        node_to_community: 节点到社区的映射
        adj_list: 邻接表
    
    Returns:
        模块度增益
    """
    # 简化的模块度增益计算
    # 在实际实现中，这会涉及更复杂的计算
    internal_connections = 0
    total_connections = len(adj_list[node])
    
    for neighbor in adj_list[node]:
        if node_to_community.get(neighbor) == target_community:
            internal_connections += 1
    
    # 简化的增益计算
    if total_connections > 0:
        return internal_connections / total_connections
    else:
        return 0.0


def validate_community_structure(nodes: List[str], communities: Dict[int, List[str]], adj_list: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    验证社区结构
    
    Args:
        nodes: 节点列表
        communities: 社区字典
        adj_list: 邻接表
    
    Returns:
        验证结果
    """
    # 检查所有节点是否都被分配到社区
    all_community_nodes = []
    for community_nodes in communities.values():
        all_community_nodes.extend(community_nodes)
    
    nodes_assigned = set(all_community_nodes)
    all_nodes = set(nodes)
    
    completeness = len(nodes_assigned.intersection(all_nodes)) / len(all_nodes) if all_nodes else 0
    
    # 计算模块度（简化版本）
    modularity = calculate_modularity(communities, adj_list)
    
    return {
        "completeness": completeness,
        "modularity": modularity,
        "community_count": len(communities),
        "validation_status": "valid" if completeness == 1.0 else "incomplete",
        "node_coverage": f"{len(nodes_assigned)}/{len(nodes)} nodes assigned to communities"
    }


def calculate_modularity(communities: Dict[int, List[str]], adj_list: Dict[str, List[str]]) -> float:
    """
    计算模块度
    
    Args:
        communities: 社区字典
        adj_list: 邻接表
    
    Returns:
        模块度值
    """
    # 简化的模块度计算
    # 在实际实现中，这会使用更精确的公式
    if not communities:
        return 0.0
    
    # 计算内部连接数和总连接数
    total_edges = sum(len(neighbors) for neighbors in adj_list.values()) // 2  # 无向图
    if total_edges == 0:
        return 0.0
    
    internal_edges = 0
    for community_id, community_nodes in communities.items():
        community_set = set(community_nodes)
        for node in community_nodes:
            for neighbor in adj_list[node]:
                if neighbor in community_set:
                    internal_edges += 1
    
    internal_edges //= 2  # 因为无向图中每条边被计算了两次
    
    # 简化的模块度计算
    modularity = internal_edges / total_edges if total_edges > 0 else 0
    
    return modularity


def analyze_inter_community_relationships(communities: Dict[int, List[str]], adj_list: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    分析社区间关系
    
    Args:
        communities: 社区字典
        adj_list: 邻接表
    
    Returns:
        社区间关系分析
    """
    # 构建节点到社区的映射
    node_to_community = {}
    for community_id, nodes in communities.items():
        for node in nodes:
            node_to_community[node] = community_id
    
    # 计算社区间的连接
    inter_community_edges = {}
    for source, neighbors in adj_list.items():
        source_community = node_to_community[source]
        for target in neighbors:
            target_community = node_to_community[target]
            if source_community != target_community:
                edge_key = tuple(sorted([source_community, target_community]))
                if edge_key not in inter_community_edges:
                    inter_community_edges[edge_key] = 0
                inter_community_edges[edge_key] += 1
    
    # 计算社区间的连接密度
    community_pairs = list(inter_community_edges.keys())
    
    return {
        "inter_community_connections": inter_community_edges,
        "inter_community_pairs": len(inter_community_edges),
        "most_connected_communities": find_most_connected_communities(inter_community_edges),
        "community_bridges": find_community_bridges(adj_list, node_to_community)
    }


def find_most_connected_communities(inter_community_edges: Dict[tuple, int]) -> List[tuple]:
    """
    找出连接最多的社区对
    
    Args:
        inter_community_edges: 社区间边的字典
    
    Returns:
        连接最多的社区对列表
    """
    if not inter_community_edges:
        return []
    
    max_connections = max(inter_community_edges.values())
    most_connected = [
        (pair, count) for pair, count in inter_community_edges.items() 
        if count == max_connections
    ]
    
    return most_connected


def find_community_bridges(adj_list: Dict[str, List[str]], node_to_community: Dict[str, int]) -> List[str]:
    """
    找出社区桥接节点
    
    Args:
        adj_list: 邻接表
        node_to_community: 节点到社区的映射
    
    Returns:
        社区桥接节点列表
    """
    bridges = []
    
    for node, neighbors in adj_list.items():
        node_community = node_to_community[node]
        neighbor_communities = set()
        
        for neighbor in neighbors:
            neighbor_communities.add(node_to_community[neighbor])
        
        # 如果节点连接到多个社区，则认为是桥接节点
        if len(neighbor_communities) > 1 and len(neighbor_communities - {node_community}) > 0:
            bridges.append(node)
    
    return bridges


def calculate_community_metrics(communities: Dict[int, List[str]], adj_list: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    计算社区指标
    
    Args:
        communities: 社区字典
        adj_list: 邻接表
    
    Returns:
        社区指标
    """
    metrics = {}
    
    for community_id, nodes in communities.items():
        community_nodes_set = set(nodes)
        
        # 计算社区大小
        size = len(nodes)
        
        # 计算社区内部连接数
        internal_edges = 0
        for node in nodes:
            for neighbor in adj_list[node]:
                if neighbor in community_nodes_set:
                    internal_edges += 1
        internal_edges //= 2  # 无向图
        
        # 计算社区外部连接数
        external_edges = 0
        for node in nodes:
            for neighbor in adj_list[node]:
                if neighbor not in community_nodes_set:
                    external_edges += 1
        
        # 计算社区密度
        max_possible_internal = size * (size - 1) // 2 if size > 1 else 0
        density = internal_edges / max_possible_internal if max_possible_internal > 0 else 0
        
        metrics[community_id] = {
            "size": size,
            "internal_edges": internal_edges,
            "external_edges": external_edges,
            "density": density,
            "conductance": external_edges / (internal_edges + external_edges) if (internal_edges + external_edges) > 0 else 0
        }
    
    return metrics


def detect_communities_other_methods(adj_list: Dict[str, List[str]], method: str = "label_propagation") -> Dict[int, List[str]]:
    """
    使用其他算法检测社区（如标签传播算法）
    
    Args:
        adj_list: 邻接表
        method: 算法方法
    
    Returns:
        社区字典
    """
    if method == "label_propagation":
        return detect_communities_label_propagation(adj_list)
    else:
        # 默认使用Louvain算法
        return detect_communities_louvain(adj_list)


def detect_communities_label_propagation(adj_list: Dict[str, List[str]]) -> Dict[int, List[str]]:
    """
    使用标签传播算法检测社区
    
    Args:
        adj_list: 邻接表
    
    Returns:
        社区字典
    """
    nodes = list(adj_list.keys())
    n = len(nodes)
    
    if n == 0:
        return {}
    
    # 初始化：每个节点有唯一的标签
    node_labels = {node: i for i, node in enumerate(nodes)}
    
    # 迭代更新标签
    for iteration in range(10):  # 限制迭代次数
        updated = False
        for node in nodes:
            # 获取邻居的标签
            neighbor_labels = [node_labels[neighbor] for neighbor in adj_list[node]]
            
            if neighbor_labels:
                # 选择最常见的标签
                from collections import Counter
                label_counts = Counter(neighbor_labels)
                most_common_label = label_counts.most_common(1)[0][0]
                
                if node_labels[node] != most_common_label:
                    node_labels[node] = most_common_label
                    updated = True
        
        if not updated:
            break  # 如果没有更新，算法收敛
    
    # 将相同标签的节点归为同一社区
    label_to_community = {}
    community_id = 0
    communities = {}
    
    for node, label in node_labels.items():
        if label not in label_to_community:
            label_to_community[label] = community_id
            communities[community_id] = []
            community_id += 1
        
        communities[label_to_community[label]].append(node)
    
    return communities