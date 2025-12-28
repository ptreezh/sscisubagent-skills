"""
网络分析算法模块
单一职责：执行网络拓扑分析和中心性计算
"""

def calculate_network_topology(entities, relationships):
    """
    计算网络拓扑属性
    输入: 实体列表、关系列表
    输出: 包含拓扑属性的字典
    """
    entity_count = len(entities)
    relationship_count = len(relationships)
    
    # 计算网络密度
    if entity_count > 1:
        # 对于有向图，最大可能边数是 n*(n-1)
        max_possible_relationships = entity_count * (entity_count - 1)
        network_density = relationship_count / max_possible_relationships if max_possible_relationships > 0 else 0
    else:
        network_density = 0
    
    return {
        "entityCount": entity_count,
        "relationshipCount": relationship_count,
        "density": network_density,
        "averageDegree": 0  # 将在中心性计算中更新
    }


def calculate_degree_centrality(entities, relationships):
    """
    计算度中心性（出度和入度的总和）
    输入: 实体列表、关系列表
    输出: 度中心性字典，键为实体ID，值为度数
    """
    # 尝试使用NetworkX进行更精确的计算
    try:
        import networkx as nx
        
        # 构建NetworkX图
        G = nx.Graph()
        
        # 添加节点
        for entity in entities:
            G.add_node(entity['id'])
        
        # 添加边
        for rel in relationships:
            source = rel.get('source')
            target = rel.get('target')
            if source and target and source in G.nodes and target in G.nodes:
                G.add_edge(source, target)
        
        # 使用NetworkX计算度中心性
        degree_centrality = nx.degree_centrality(G)
        
        return degree_centrality
    
    except ImportError:
        # 如果NetworkX不可用，使用基础实现
        degree_centrality = {}
        for entity in entities:
            entity_id = entity.get('id', '')
            # 计算该实体作为源或目标出现的次数
            degree = sum(1 for rel in relationships if rel.get('source') == entity_id or rel.get('target') == entity_id)
            degree_centrality[entity_id] = degree
        
        return degree_centrality


def calculate_closeness_centrality(entities, relationships, degree_centrality):
    """
    计算接近中心性
    输入: 实体列表、关系列表、度中心性字典
    输出: 接近中心性字典
    """
    # 尝试使用NetworkX进行更精确的计算
    try:
        import networkx as nx
        
        # 构建NetworkX图
        G = nx.Graph()
        
        # 添加节点
        for entity in entities:
            G.add_node(entity['id'])
        
        # 添加边
        for rel in relationships:
            source = rel.get('source')
            target = rel.get('target')
            if source and target and source in G.nodes and target in G.nodes:
                G.add_edge(source, target)
        
        # 使用NetworkX计算接近中心性
        closeness_centrality = nx.closeness_centrality(G)
        
        return closeness_centrality
    
    except ImportError:
        # 如果NetworkX不可用，使用基础实现
        closeness_centrality = {}
        entity_count = len(entities)
        
        if entity_count > 1:
            for entity_id in degree_centrality:
                if degree_centrality[entity_id] > 0:
                    # 简化：基于度中心性进行归一化
                    max_degree = max(degree_centrality.values()) if degree_centrality else 1
                    closeness_centrality[entity_id] = degree_centrality[entity_id] / max_degree if max_degree > 0 else 0
                else:
                    closeness_centrality[entity_id] = 0
        else:
            for entity_id in degree_centrality:
                closeness_centrality[entity_id] = 0
        
        return closeness_centrality


def calculate_betweenness_centrality(entities, relationships, degree_centrality):
    """
    计算中介中心性（简化版本）
    输入: 实体列表、关系列表、度中心性字典
    输出: 中介中心性字典
    """
    # 尝试使用NetworkX进行更精确的计算
    try:
        import networkx as nx
        
        # 构建NetworkX图
        G = nx.Graph()
        
        # 添加节点
        for entity in entities:
            G.add_node(entity['id'])
        
        # 添加边
        for rel in relationships:
            source = rel.get('source')
            target = rel.get('target')
            if source and target and source in G.nodes and target in G.nodes:
                G.add_edge(source, target)
        
        # 使用NetworkX计算中介中心性
        betweenness_centrality = nx.betweenness_centrality(G)
        
        return betweenness_centrality
    
    except ImportError:
        # 如果NetworkX不可用，使用基础实现
        betweenness_centrality = {}
        entity_count = len(entities)
        
        for entity in entities:
            entity_id = entity.get('id', '')
            # 基于该节点的度和在网络中的位置
            connections = degree_centrality[entity_id]
            # 估算中介中心性：高度节点通常在路径中出现更频繁
            if entity_count > 2 and connections > 0:
                betweenness_centrality[entity_id] = (connections * (connections - 1)) / ((entity_count - 1) * (entity_count - 2)) if entity_count > 2 else 0
            else:
                betweenness_centrality[entity_id] = 0
        
        # 正常化中介中心性
        if betweenness_centrality and max(betweenness_centrality.values()) > 0:
            max_bc = max(betweenness_centrality.values())
            for entity_id in betweenness_centrality:
                betweenness_centrality[entity_id] = betweenness_centrality[entity_id] / max_bc
        
        return betweenness_centrality