"""
社群检测工具
Louvain/Leiden算法实现
"""

import networkx as nx
import community.community_louvain as community_louvain
from typing import Dict, List, Optional


def detect_communities_louvain(G: nx.Graph,
                               resolution: float = 1.0,
                               random_state: Optional[int] = None) -> Dict:
    """
    使用 Louvain 算法进行社群检测
    
    参数:
        G: NetworkX 网络对象
        resolution: 分辨率参数
        random_state: 随机种子
    
    返回:
        社群检测结果
    """
    # 执行 Louvain 算法
    partition = community_louvain.best_partition(G, 
                                                  resolution=resolution,
                                                  random_state=random_state)
    
    # 计算模块化
    modularity = community_louvain.modularity(partition, G)
    
    # 整理社群
    communities = {}
    for node, comm_id in partition.items():
        if comm_id not in communities:
            communities[comm_id] = []
        communities[comm_id].append(node)
    
    # 社群统计
    community_stats = {
        'num_communities': len(communities),
        'modularity': modularity,
        'avg_size': len(G.nodes()) / len(communities) if communities else 0,
        'max_size': max(len(members) for members in communities.values()) if communities else 0,
        'min_size': min(len(members) for members in communities.values()) if communities else 0
    }
    
    return {
        'communities': communities,
        'partition': partition,
        'modularity': modularity,
        'stats': community_stats,
        'algorithm': 'louvain'
    }


def detect_communities_leiden(G: nx.Graph,
                              resolution: float = 1.0,
                              max_iter: int = -1) -> Dict:
    """
    使用 Leiden 算法进行社群检测
    
    参数:
        G: NetworkX 网络对象
        resolution: 分辨率参数
        max_iter: 最大迭代次数
    
    返回:
        社群检测结果
    """
    try:
        # 需要 leidenalg 包
        import leidenalg
        
        # 转换为 igraph 格式
        import igraph as ig
        g = ig.Graph.from_networkx(G)
        
        # 执行 Leiden 算法
        partition = leidenalg.find_partition(g, 
                                             leidenalg.ModularityVertexPartition,
                                             resolution_parameter=resolution,
                                             max_iters=max_iter)
        
        # 整理社群
        communities = {i: list(members) for i, members in enumerate(partition)}
        
        # 计算模块化
        modularity = G.modularity()
        
        return {
            'communities': communities,
            'modularity': modularity,
            'algorithm': 'leiden'
        }
    except ImportError:
        # 如果没有 leidenalg, 回退到 Louvain
        return detect_communities_louvain(G, resolution)


def calculate_community_stats(G: nx.Graph, 
                             communities: Dict) -> Dict:
    """
    计算社群统计信息
    
    参数:
        G: NetworkX 网络对象
        communities: 社群字典 {comm_id: [nodes]}
    
    返回:
        社群统计信息
    """
    stats = {
        'num_communities': len(communities),
        'total_nodes': len(G.nodes()),
        'communities': []
    }
    
    for comm_id, members in communities.items():
        # 子图
        subgraph = G.subgraph(members)
        
        comm_stats = {
            'id': comm_id,
            'size': len(members),
            'density': nx.density(subgraph),
            'num_edges': subgraph.number_of_edges(),
            'members': members
        }
        
        stats['communities'].append(comm_stats)
    
    return stats


def validate_communities(communities: Dict, 
                        modularity: float) -> Dict:
    """
    验证社群检测结果
    
    参数:
        communities: 社群字典
        modularity: 模块化值
    
    返回:
        验证结果
    """
    issues = []
    
    # 检查模块化值
    if modularity < 0.3:
        issues.append({
            'code': 'LOW_MODULARITY',
            'message': f'模块化 Q 值 ({modularity:.3f}) 较低, 社群结构不明显',
            'severity': 'warning'
        })
    
    # 检查社群大小
    for comm_id, members in communities.items():
        if len(members) == 1:
            issues.append({
                'code': 'SINGLE_NODE_COMMUNITY',
                'message': f'社群 {comm_id} 只有一个节点',
                'severity': 'info'
            })
    
    return {
        'valid': len([i for i in issues if i['severity'] == 'error']) == 0,
        'issues': issues,
        'modularity_quality': 'good' if modularity > 0.5 else 'moderate' if modularity > 0.3 else 'poor'
    }


if __name__ == '__main__':
    # 测试
    import networkx as nx
    
    # 创建测试网络
    G = nx.karate_club_graph()
    
    # 社群检测
    result = detect_communities_louvain(G)
    
    print(f"社群检测结果:")
    print(f"  社群数：{result['stats']['num_communities']}")
    print(f"  模块化 Q 值：{result['modularity']:.3f}")
    print(f"  平均大小：{result['stats']['avg_size']:.1f}")
    
    # 验证
    validation = validate_communities(result['communities'], result['modularity'])
    print(f"  验证结果：{validation['modularity_quality']}")
