"""
健康度评估算法模块
单一职责：评估生态系统的健康状况
"""

def assess_ecosystem_health(network_topology, centralities, communities, relationships):
    """
    评估生态系统健康度
    输入: 网络拓扑信息、中心性数据、社区信息、关系列表
    输出: 健康度评估结果
    """
    entity_count = network_topology['entityCount']
    relationship_count = network_topology['relationshipCount']
    network_density = network_topology['density']
    
    if entity_count == 0:
        return {
            "score": 0,
            "indicators": {
                "density": 0,
                "connectivity": 0,
                "diversity": 0,
                "averageDegree": 0
            },
            "assessment": "生态系统健康度无法评估（无实体）"
        }
    
    # 计算平均度
    avg_degree = sum(centralities['degree'].values()) / entity_count if entity_count > 0 else 0
    max_possible_degree = entity_count - 1 if entity_count > 0 else 1
    avg_connectivity = avg_degree / max_possible_degree if max_possible_degree > 0 else 0
    
    # 社区多样性
    community_diversity = len(communities) / entity_count if entity_count > 0 else 0
    
    # 基于多个因素计算健康度
    # 网络密度占30%，连通性占35%，社区多样性占35%
    network_health = network_density * 30
    connectivity_health = avg_connectivity * 35
    diversity_health = min(community_diversity * 100, 35)  # 限制多样性影响不超过35分
    
    health_score = min(100, max(0, int(network_health + connectivity_health + diversity_health)))
    
    return {
        "score": health_score,
        "indicators": {
            "density": network_density,
            "connectivity": avg_connectivity,
            "diversity": community_diversity,
            "averageDegree": avg_degree
        },
        "assessment": f"生态系统健康度{'优秀' if health_score >= 80 else '良好' if health_score >= 70 else '一般' if health_score >= 50 else '需要关注'}"
    }