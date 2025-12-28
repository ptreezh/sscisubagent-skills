"""
ANT网络分析模块
此模块提供行动者网络的结构、动态和稳定性分析功能
"""

from typing import Dict, List, Any, Tuple
import json


def network_analysis(edges: List[Tuple], nodes: List[str] = None) -> Dict[str, Any]:
    """
    分析行动者网络的结构特征、动态变化和稳定性机制
    
    Args:
        edges: 网络边的列表，每条边为(源节点, 目标节点)的元组
        nodes: 节点列表（可选）
    
    Returns:
        包含网络分析结果的字典
    """
    # 基础网络指标计算
    node_set = set()
    for edge in edges:
        node_set.add(edge[0])
        node_set.add(edge[1])

    if nodes:
        node_set.update(nodes)

    # 计算网络基本属性
    num_nodes = len(node_set)
    num_edges = len(edges)
    
    # 计算网络密度（如果节点数大于1）
    density = 0
    if num_nodes > 1:
        max_possible_edges = num_nodes * (num_nodes - 1) / 2  # 无向图
        density = num_edges / max_possible_edges if max_possible_edges > 0 else 0

    # 计算连接度分布（基础版本）
    degree_dist = {}
    for node in node_set:
        degree = sum(1 for edge in edges if node in edge)
        if degree in degree_dist:
            degree_dist[degree] += 1
        else:
            degree_dist[degree] = 1

    # 识别中心节点（基础版本：度数最高的节点）
    central_nodes = []
    if edges:
        node_degrees = {}
        for node in node_set:
            node_degrees[node] = sum(1 for edge in edges if node in edge)
        
        max_degree = max(node_degrees.values()) if node_degrees else 0
        central_nodes = [node for node, degree in node_degrees.items() if degree == max_degree]

    # 稳定性评估（基础版本）
    stability_score = calculate_stability_score(edges, node_set)

    return {
        "network_type": "socio-technical",
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "density": density,
        "nodes": list(node_set),
        "edges": edges,
        "degree_distribution": degree_dist,
        "central_nodes": central_nodes,
        "stability_score": stability_score,
        "components": 1,  # 基础版本，假设网络连通
        "avg_clustering": 0,  # 基础版本
        "avg_shortest_path": float('inf')  # 基础版本
    }


def calculate_stability_score(edges: List[Tuple], nodes: set) -> float:
    """
    计算网络稳定性得分（基础版本）
    
    Args:
        edges: 网络边的列表
        nodes: 节点集合
    
    Returns:
        稳定性得分（0-1之间的浮点数）
    """
    if not nodes:
        return 0
    
    if not edges:
        # 无连接的网络，稳定性较低
        return 0.2 if len(nodes) > 1 else 1.0
    
    # 计算平均连接度
    total_degree = sum(2 for _ in edges)  # 每条边贡献2度
    avg_degree = total_degree / len(nodes) if nodes else 0
    
    # 基于平均连接度和网络密度计算稳定性
    # 连接度适中且密度适中的网络更稳定
    ideal_avg_degree = min(5, len(nodes) / 2)  # 理想平均度数
    degree_stability = 1 - abs(avg_degree - ideal_avg_degree) / ideal_avg_degree if ideal_avg_degree > 0 else 0
    degree_stability = max(0, min(1, degree_stability))  # 限制在0-1之间
    
    # 网络密度对稳定性的影响
    density = len(edges) / (len(nodes) * (len(nodes) - 1) / 2) if len(nodes) > 1 else 0
    density_stability = 1 - abs(density - 0.5) * 2  # 密度为0.5时最稳定
    density_stability = max(0, min(1, density_stability))
    
    # 综合稳定性得分
    stability_score = (degree_stability * 0.6 + density_stability * 0.4)
    
    return stability_score


def topology_mapping(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    创建行动者关系的综合地图
    
    Args:
        data: 包含网络数据的字典
    
    Returns:
        包含拓扑映射结果的字典
    """
    edges = data.get('edges', [])
    nodes = data.get('nodes', [])
    
    # 生成拓扑映射
    topology = {
        "node_count": len(set(node for edge in edges for node in edge) | set(nodes)),
        "edge_count": len(edges),
        "connection_types": identify_connection_types(edges),
        "boundary_nodes": identify_boundary_nodes(edges, nodes),
        "subnetworks": identify_subnetworks(edges)
    }
    
    return topology


def identify_connection_types(edges: List[Tuple]) -> Dict[str, int]:
    """识别连接类型"""
    # 基础实现：统计连接数量
    return {"associative": len(edges)}


def identify_boundary_nodes(edges: List[Tuple], nodes: List[str]) -> List[str]:
    """识别边界节点"""
    # 基础实现：返回度数为1的节点
    boundary_nodes = []
    for node in nodes:
        degree = sum(1 for edge in edges if node in edge)
        if degree <= 1:
            boundary_nodes.append(node)
    return boundary_nodes


def identify_subnetworks(edges: List[Tuple]) -> List[List[Tuple]]:
    """识别子网络"""
    # 基础实现：返回所有边作为一个子网络
    return [edges] if edges else []


def relationship_analysis(edges: List[Tuple]) -> Dict[str, Any]:
    """
    分析关系强度和性质
    
    Args:
        edges: 网络边的列表
    
    Returns:
        包含关系分析结果的字典
    """
    # 基础关系分析
    relationships = {
        "total_relationships": len(edges),
        "relationship_strength_distribution": {},  # 基础版本
        "relationship_types": {"associative": len(edges)},
        "directionality": "undirected",  # 基础版本
        "quality_indicators": {"average": len(edges)}  # 基础版本
    }
    
    return relationships


def centrality_analysis(edges: List[Tuple], nodes: List[str] = None) -> Dict[str, Any]:
    """
    中心性分析
    
    Args:
        edges: 网络边的列表
        nodes: 节点列表（可选）
    
    Returns:
        包含中心性分析结果的字典
    """
    if nodes is None:
        nodes = list(set(node for edge in edges for node in edge))
    
    # 计算度中心性
    degree_centrality = {}
    for node in nodes:
        degree = sum(1 for edge in edges if node in edge)
        degree_centrality[node] = degree / (len(nodes) - 1) if len(nodes) > 1 else 0
    
    # 找出中心节点
    max_centrality = max(degree_centrality.values()) if degree_centrality else 0
    central_nodes = [node for node, centrality in degree_centrality.items() 
                     if centrality == max_centrality]
    
    return {
        "degree_centrality": degree_centrality,
        "central_nodes": central_nodes,
        "max_centrality": max_centrality,
        "influence_distribution": degree_centrality  # 基础版本
    }


def dynamics_analysis(edges_over_time: List[List[Tuple]]) -> Dict[str, Any]:
    """
    动态分析
    
    Args:
        edges_over_time: 不同时刻的边列表
    
    Returns:
        包含动态分析结果的字典
    """
    if not edges_over_time:
        return {"change_points": [], "evolution_pattern": "static"}
    
    # 基础动态分析
    changes = []
    for i in range(1, len(edges_over_time)):
        prev_nodes = set(node for edge in edges_over_time[i-1] for node in edge)
        curr_nodes = set(node for edge in edges_over_time[i] for node in edge)
        
        new_nodes = curr_nodes - prev_nodes
        removed_nodes = prev_nodes - curr_nodes
        
        changes.append({
            "time_step": i,
            "new_nodes": list(new_nodes),
            "removed_nodes": list(removed_nodes),
            "net_change": len(new_nodes) - len(removed_nodes)
        })
    
    return {
        "change_points": changes,
        "evolution_pattern": "evolving" if changes else "static",
        "total_changes": len(changes)
    }