"""
社区检测算法模块
单一职责：检测网络中的社区结构
"""

def find_communities_greedy_modularity(entities, relationships):
    """
    使用贪心模块化算法进行社区检测
    输入: 实体列表、关系列表
    输出: 社区列表，每个社区包含ID和实体列表
    """
    # 尝试使用NetworkX进行更精确的社区检测
    try:
        import networkx as nx
        from networkx.algorithms import community
        
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
                G.add_edge(source, target, weight=rel.get('strength', 1.0))
        
        # 使用NetworkX的社区检测算法
        communities_generator = community.greedy_modularity_communities(G)
        
        # 转换为期望的输出格式
        result_communities = []
        for i, comm in enumerate(communities_generator):
            result_communities.append({
                "id": i,
                "entities": list(comm),
                "size": len(comm)
            })
        
        return result_communities
    
    except ImportError:
        # 如果NetworkX不可用，使用基础实现
        if not entities or not relationships:
            return [{"id": 0, "entities": [e['id'] for e in entities]}] if entities else []
        
        # 构建邻接表
        adj = {}
        for entity in entities:
            adj[entity['id']] = set()
        
        for rel in relationships:
            source = rel.get('source')
            target = rel.get('target')
            if source in adj and target in adj:
                # 添加双向连接（无向图）
                adj[source].add(target)
                adj[target].add(source)
        
        # 初始化：每个节点为一个独立社区
        communities = {entity['id']: entity['id'] for entity in entities}  # node_id -> community_id
        community_members = {entity['id']: {entity['id']} for entity in entities}  # community_id -> set of nodes
        
        # 迭代优化社区结构
        improved = True
        iteration = 0
        max_iterations = 10  # 防止无限循环
        
        while improved and iteration < max_iterations:
            improved = False
            iteration += 1
            
            # 对每个节点尝试移动到相邻节点的社区
            for node in adj:
                current_community = communities[node]
                
                # 统计相邻节点所属的社区
                neighbor_communities = {}
                for neighbor in adj[node]:
                    neighbor_comm = communities[neighbor]
                    neighbor_communities[neighbor_comm] = neighbor_communities.get(neighbor_comm, 0) + 1
                
                # 计算当前社区内外的连接数
                best_community = current_community
                best_gain = 0
                
                # 尝试将节点移动到相邻节点的社区
                for test_community in neighbor_communities:
                    if test_community != current_community:
                        # 使用连接数作为模块化增益的近似
                        gain = neighbor_communities[test_community]
                        if gain > best_gain:
                            best_gain = gain
                            best_community = test_community
                
                # 如果找到更好的社区，则移动
                if best_community != current_community:
                    # 从旧社区移除节点
                    community_members[current_community].discard(node)
                    if len(community_members[current_community]) == 0:
                        del community_members[current_community]
                    
                    # 添加到新社区
                    if best_community not in community_members:
                        community_members[best_community] = set()
                    community_members[best_community].add(node)
                    
                    # 更新节点的社区归属
                    communities[node] = best_community
                    improved = True
        
        # 转换为输出格式
        result_communities = []
        new_id = 0
        
        for members in community_members.values():
            if len(members) > 0:  # 只保留非空社区
                result_communities.append({
                    "id": new_id,
                    "entities": list(members),
                    "size": len(members)
                })
                new_id += 1
        
        return result_communities