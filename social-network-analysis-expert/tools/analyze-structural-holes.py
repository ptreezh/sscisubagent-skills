"""
结构洞分析工具
基于 Burt (1992) 的结构洞理论
"""

import networkx as nx
import numpy as np
from typing import Dict, List


def calculate_constraint(G: nx.Graph, 
                         nodes: List[str] = None) -> Dict[str, float]:
    """
    计算约束指标 (Constraint)
    
    参数:
        G: NetworkX 网络对象
        nodes: 节点列表
    
    返回:
        约束指标字典
    """
    constraint = nx.constraint(G, nodes=nodes)
    return constraint


def calculate_effective_size(G: nx.Graph,
                             nodes: List[str] = None) -> Dict[str, float]:
    """
    计算有效规模 (Effective Size)
    
    参数:
        G: NetworkX 网络对象
        nodes: 节点列表
    
    返回:
        有效规模字典
    """
    effective_size = nx.effective_size(G, nodes=nodes)
    return effective_size


def calculate_hierarchy(G: nx.Graph,
                        nodes: List[str] = None) -> Dict[str, float]:
    """
    计算层级性 (Hierarchy)
    
    参数:
        G: NetworkX 网络对象
        nodes: 节点列表
    
    返回:
        层级性字典
    """
    # 简化版层级性计算 - 使用聚类系数
    hierarchy = {node: nx.clustering(G, node) for node in nodes}
    return hierarchy
    return hierarchy


def analyze_structural_holes(G: nx.Graph) -> Dict:
    """
    完整的结构洞分析
    
    参数:
        G: NetworkX 网络对象
    
    返回:
        结构洞分析结果
    """
    nodes = list(G.nodes())
    
    # 计算所有指标
    constraint = calculate_constraint(G, nodes)
    effective_size = calculate_effective_size(G, nodes)
    hierarchy = calculate_hierarchy(G, nodes)
    
    # 识别结构洞位置(低约束的节点)
    avg_constraint = np.mean(list(constraint.values()))
    structural_holes = [
        node for node in nodes 
        if constraint[node] < avg_constraint
    ]
    
    # 网络效率
    efficiency = {
        node: effective_size[node] / len(list(G.neighbors(node)))
        for node in nodes
        if len(list(G.neighbors(node))) > 0
    }
    
    return {
        'constraint': constraint,
        'effective_size': effective_size,
        'hierarchy': hierarchy,
        'efficiency': efficiency,
        'structural_holes': structural_holes,
        'avg_constraint': avg_constraint,
        'num_structural_holes': len(structural_holes)
    }


def identify_brokers(G: nx.Graph,
                     constraint: Dict[str, float],
                     threshold: float = None) -> List[str]:
    """
    识别网络经纪人(占据结构洞位置的节点)
    
    参数:
        G: NetworkX 网络对象
        constraint: 约束指标字典
        threshold: 阈值(默认使用平均值)
    
    返回:
        经纪人节点列表
    """
    if threshold is None:
        threshold = np.mean(list(constraint.values()))
    
    # 低约束的节点是经纪人
    brokers = [node for node in G.nodes() if constraint[node] < threshold]
    
    return brokers


def validate_structural_holes_results(results: Dict) -> Dict:
    """
    验证结构洞分析结果
    
    参数:
        results: 分析结果字典
    
    返回:
        验证结果
    """
    issues = []
    
    # 检查约束指标范围
    for node, value in results['constraint'].items():
        if value < 0 or value > 1:
            issues.append({
                'code': 'CONSTRAINT_OUT_OF_RANGE',
                'message': f'节点 {node} 的约束指标 {value} 超出 0-1 范围',
                'severity': 'error'
            })
    
    # 检查有效规模
    for node, value in results['effective_size'].items():
        if value < 0:
            issues.append({
                'code': 'NEGATIVE_EFFECTIVE_SIZE',
                'message': f'节点 {node} 的有效规模 {value} 为负数',
                'severity': 'warning'
            })
    
    return {
        'valid': len([i for i in issues if i['severity'] == 'error']) == 0,
        'issues': issues
    }


if __name__ == '__main__':
    # 测试
    import networkx as nx
    
    # 创建测试网络
    G = nx.karate_club_graph()
    
    # 结构洞分析
    results = analyze_structural_holes(G)
    
    print(f"结构洞分析结果:")
    print(f"  平均约束：{results['avg_constraint']:.3f}")
    print(f"  结构洞位置数：{results['num_structural_holes']}")
    print(f"\n前 5 个经纪人节点:")
    
    # 按约束排序
    sorted_nodes = sorted(results['constraint'].items(), key=lambda x: x[1])
    for node, constraint in sorted_nodes[:5]:
        print(f"  {node}: 约束={constraint:.3f}, 有效规模={results['effective_size'][node]:.2f}")
