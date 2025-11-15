# Network Computation Skill

## 技能概述

社会网络计算分析技能，提供全面的社会网络分析计算支持，包括网络构建、中心性测量、社区检测、网络可视化等，并提供完整的Python编程脚本实现。

## 核心功能

### 1. 网络构建与基础分析
```python
# 社会网络分析基础脚本
import networkx as nx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Dict, List, Tuple, Any, Optional
from community import community_louvain
import igraph as ig

class NetworkBuilder:
    """网络构建器"""
    
    def __init__(self):
        self.graph = None
        self.directed = False
        self.weighted = False
    
    def create_network_from_edgelist(self, edgelist: List[Tuple], 
                                   directed: bool = False, 
                                   weighted: bool = False) -> nx.Graph:
        """从边列表创建网络"""
        self.directed = directed
        self.weighted = weighted
        
        if directed:
            if weighted:
                self.graph = nx.DiGraph()
            else:
                self.graph = nx.DiGraph()
        else:
            if weighted:
                self.graph = nx.Graph()
            else:
                self.graph = nx.Graph()
        
        # 添加边和权重
        for edge in edgelist:
            if len(edge) == 2:
                self.graph.add_edge(edge[0], edge[1])
            elif len(edge) == 3:
                self.graph.add_edge(edge[0], edge[1], weight=edge[2])
        
        return self.graph
    
    def create_network_from_adjacency(self, adjacency_matrix: np.ndarray, 
                                    node_labels: List[str] = None) -> nx.Graph:
        """从邻接矩阵创建网络"""
        if node_labels is None:
            node_labels = [str(i) for i in range(adjacency_matrix.shape[0])]
        
        self.graph = nx.from_numpy_array(adjacency_matrix)
        mapping = {i: node_labels[i] for i in range(len(node_labels))}
        self.graph = nx.relabel_nodes(self.graph, mapping)
        
        return self.graph
    
    def create_network_from_data(self, data: pd.DataFrame, 
                               source_col: str, target_col: str, 
                               weight_col: str = None) -> nx.Graph:
        """从数据框创建网络"""
        self.graph = nx.from_pandas_edgelist(
            data, source=source_col, target=target_col, 
            edge_attr=weight_col, create_using=nx.Graph()
        )
        
        if weight_col:
            self.weighted = True
        
        return self.graph
    
    def network_basic_stats(self) -> Dict[str, Any]:
        """计算网络基础统计"""
        if self.graph is None:
            raise ValueError("网络尚未创建")
        
        stats = {
            'basic_info': {
                'num_nodes': self.graph.number_of_nodes(),
                'num_edges': self.graph.number_of_edges(),
                'is_directed': self.graph.is_directed(),
                'is_weighted': nx.is_weighted(self.graph),
                'density': nx.density(self.graph)
            },
            'connectivity': {
                'is_connected': nx.is_connected(self.graph),
                'num_components': nx.number_connected_components(self.graph),
                'largest_component_size': len(max(nx.connected_components(self.graph), key=len))
            },
            'degree_stats': self._calculate_degree_stats()
        }
        
        return stats
    
    def _calculate_degree_stats(self) -> Dict[str, float]:
        """计算度统计"""
        degrees = dict(self.graph.degree())
        degree_values = list(degrees.values())
        
        return {
            'mean_degree': np.mean(degree_values),
            'std_degree': np.std(degree_values),
            'min_degree': min(degree_values),
            'max_degree': max(degree_values),
            'degree_assortativity': nx.degree_assortativity_coefficient(self.graph)
        }

class NetworkCentrality:
    """网络中心性分析器"""
    
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.centrality_measures = {}
    
    def calculate_all_centralities(self) -> Dict[str, Dict[str, float]]:
        """计算所有中心性指标"""
        centralities = {
            'degree_centrality': nx.degree_centrality(self.graph),
            'betweenness_centrality': nx.betweenness_centrality(self.graph),
            'closeness_centrality': nx.closeness_centrality(self.graph),
            'eigenvector_centrality': nx.eigenvector_centrality(self.graph, max_iter=1000),
            'pagerank': nx.pagerank(self.graph),
            'katz_centrality': nx.katz_centrality(self.graph),
            'load_centrality': nx.load_centrality(self.graph)
        }
        
        # 如果有权重，计算加权中心性
        if nx.is_weighted(self.graph):
            centralities.update({
                'weighted_betweenness': nx.betweenness_centrality(self.graph, weight='weight'),
                'weighted_closeness': nx.closeness_centrality(self.graph, distance='weight'),
                'weighted_degree': dict(self.graph.degree(weight='weight'))
            })
        
        self.centrality_measures = centralities
        return centralities
    
    def centrality_correlation_analysis(self) -> pd.DataFrame:
        """中心性指标相关性分析"""
        if not self.centrality_measures:
            self.calculate_all_centralities()
        
        # 创建中心性数据框
        centrality_df = pd.DataFrame(self.centrality_measures)
        
        # 计算相关性矩阵
        correlation_matrix = centrality_df.corr()
        
        return correlation_matrix
    
    def identify_key_players(self, top_k: int = 5) -> Dict[str, List[Tuple[str, float]]]:
        """识别关键节点"""
        if not self.centrality_measures:
            self.calculate_all_centralities()
        
        key_players = {}
        for measure, values in self.centrality_measures.items():
            sorted_nodes = sorted(values.items(), key=lambda x: x[1], reverse=True)
            key_players[measure] = sorted_nodes[:top_k]
        
        return key_players
    
    def centrality_distribution_analysis(self) -> Dict[str, Dict[str, float]]:
        """中心性分布分析"""
        if not self.centrality_measures:
            self.calculate_all_centralities()
        
        distribution_stats = {}
        for measure, values in self.centrality_measures.items():
            value_list = list(values.values())
            distribution_stats[measure] = {
                'mean': np.mean(value_list),
                'std': np.std(value_list),
                'min': min(value_list),
                'max': max(value_list),
                'skewness': self._calculate_skewness(value_list),
                'gini_coefficient': self._calculate_gini(value_list)
            }
        
        return distribution_stats
    
    def _calculate_skewness(self, values: List[float]) -> float:
        """计算偏度"""
        from scipy.stats import skew
        return skew(values)
    
    def _calculate_gini(self, values: List[float]) -> float:
        """计算基尼系数"""
        sorted_values = sorted(values)
        n = len(values)
        cumsum = np.cumsum(sorted_values)
        return (n + 1 - 2 * np.sum(cumsum) / cumsum[-1]) / n
```

### 2. 社区检测与分析
```python
# 社区检测脚本
class CommunityDetection:
    """社区检测分析器"""
    
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.communities = {}
        self.community_stats = {}
    
    def detect_communities(self, method: str = 'louvain') -> Dict[str, Any]:
        """检测社区"""
        if method == 'louvain':
            return self._louvain_detection()
        elif method == 'girvan_newman':
            return self._girvan_newman_detection()
        elif method == 'label_propagation':
            return self._label_propagation_detection()
        elif method == 'modularity':
            return self._modularity_detection()
        else:
            raise ValueError(f"未知的社区检测方法: {method}")
    
    def _louvain_detection(self) -> Dict[str, Any]:
        """Louvain社区检测"""
        partition = community_louvain.best_partition(self.graph)
        
        # 统计信息
        communities = {}
        for node, comm_id in partition.items():
            if comm_id not in communities:
                communities[comm_id] = []
            communities[comm_id].append(node)
        
        modularity = community_louvain.modularity(partition, self.graph)
        
        result = {
            'method': 'Louvain',
            'partition': partition,
            'communities': communities,
            'num_communities': len(communities),
            'modularity': modularity,
            'community_sizes': {comm: len(members) for comm, members in communities.items()}
        }
        
        self.communities[('louvain', len(communities))] = result
        return result
    
    def _girvan_newman_detection(self) -> Dict[str, Any]:
        """Girvan-Newman社区检测"""
        communities_generator = nx.community.girvan_newman(self.graph)
        
        # 获取第一层社区划分
        first_level_communities = next(communities_generator)
        
        communities = [list(community) for community in first_level_communities]
        modularity = nx.community.modularity(self.graph, communities)
        
        # 创建节点到社区的映射
        partition = {}
        for i, community in enumerate(communities):
            for node in community:
                partition[node] = i
        
        result = {
            'method': 'Girvan-Newman',
            'partition': partition,
            'communities': {i: community for i, community in enumerate(communities)},
            'num_communities': len(communities),
            'modularity': modularity,
            'community_sizes': {i: len(community) for i, community in enumerate(communities)}
        }
        
        self.communities[('girvan_newman', len(communities))] = result
        return result
    
    def _label_propagation_detection(self) -> Dict[str, Any]:
        """标签传播社区检测"""
        communities = nx.community.label_propagation_communities(self.graph)
        communities = [list(community) for community in communities]
        modularity = nx.community.modularity(self.graph, communities)
        
        partition = {}
        for i, community in enumerate(communities):
            for node in community:
                partition[node] = i
        
        result = {
            'method': 'Label Propagation',
            'partition': partition,
            'communities': {i: community for i, community in enumerate(communities)},
            'num_communities': len(communities),
            'modularity': modularity,
            'community_sizes': {i: len(community) for i, community in enumerate(communities)}
        }
        
        self.communities[('label_propagation', len(communities))] = result
        return result
    
    def analyze_community_structure(self, partition: Dict) -> Dict[str, Any]:
        """分析社区结构"""
        # 计算社区内部密度
        internal_densities = {}
        external_densities = {}
        
        for comm_id, nodes in partition.items():
            subgraph = self.graph.subgraph(nodes)
            internal_densities[comm_id] = nx.density(subgraph)
            
            # 计算外部连接
            external_edges = 0
            for node in nodes:
                for neighbor in self.graph.neighbors(node):
                    if neighbor not in nodes:
                        external_edges += 1
            
            possible_external = len(nodes) * (self.graph.number_of_nodes() - len(nodes))
            external_densities[comm_id] = external_edges / possible_external if possible_external > 0 else 0
        
        return {
            'internal_densities': internal_densities,
            'external_densities': external_densities,
            'conductance': {comm_id: external_densities[comm_id] / (internal_densities[comm_id] + external_densities[comm_id]) 
                           for comm_id in partition.keys()}
        }
    
    def inter_community_analysis(self, result: Dict) -> Dict[str, Any]:
        """社区间分析"""
        communities = result['communities']
        inter_community_edges = {}
        
        for comm1_id, comm1_nodes in communities.items():
            for comm2_id, comm2_nodes in communities.items():
                if comm1_id < comm2_id:  # 避免重复计算
                    edge_count = 0
                    for node1 in comm1_nodes:
                        for node2 in comm2_nodes:
                            if self.graph.has_edge(node1, node2):
                                edge_count += 1
                    
                    if edge_count > 0:
                        inter_community_edges[(comm1_id, comm2_id)] = edge_count
        
        return {
            'inter_community_edges': inter_community_edges,
            'bridge_nodes': self._identify_bridge_nodes(communities)
        }
    
    def _identify_bridge_nodes(self, communities: Dict) -> Dict[str, List[str]]:
        """识别桥梁节点"""
        bridge_nodes = {comm_id: [] for comm_id in communities.keys()}
        
        for node in self.graph.nodes():
            node_communities = []
            for comm_id, nodes in communities.items():
                if node in nodes:
                    node_communities.append(comm_id)
            
            # 如果节点连接到多个社区
            neighbors = list(self.graph.neighbors(node))
            neighbor_communities = set()
            for neighbor in neighbors:
                for comm_id, nodes in communities.items():
                    if neighbor in nodes:
                        neighbor_communities.add(comm_id)
            
            if len(neighbor_communities) > 1:
                for comm_id in node_communities:
                    bridge_nodes[comm_id].append(node)
        
        return bridge_nodes

class NetworkVisualization:
    """网络可视化器"""
    
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.pos = None
    
    def calculate_layout(self, layout_type: str = 'spring') -> Dict[str, Tuple[float, float]]:
        """计算节点布局"""
        if layout_type == 'spring':
            self.pos = nx.spring_layout(self.graph, k=1, iterations=50)
        elif layout_type == 'circular':
            self.pos = nx.circular_layout(self.graph)
        elif layout_type == 'random':
            self.pos = nx.random_layout(self.graph)
        elif layout_type == 'kamada_kawai':
            self.pos = nx.kamada_kawai_layout(self.graph)
        elif layout_type == 'shell':
            self.pos = nx.shell_layout(self.graph)
        
        return self.pos
    
    def draw_network(self, node_attributes: Dict = None, 
                    edge_attributes: Dict = None,
                    community_partition: Dict = None,
                    save_path: str = None) -> None:
        """绘制网络图"""
        plt.figure(figsize=(12, 8))
        
        if self.pos is None:
            self.calculate_layout()
        
        # 节点颜色
        node_colors = []
        if community_partition:
            max_comm = max(community_partition.values()) if community_partition else 0
            colors = plt.cm.Set3(np.linspace(0, 1, max_comm + 1))
            for node in self.graph.nodes():
                comm_id = community_partition.get(node, 0)
                node_colors.append(colors[comm_id])
        else:
            node_colors = 'lightblue'
        
        # 节点大小（基于度中心性）
        degree_centralities = nx.degree_centrality(self.graph)
        node_sizes = [degree_centralities[node] * 2000 + 100 for node in self.graph.nodes()]
        
        # 边宽度（基于权重）
        edge_widths = []
        if nx.is_weighted(self.graph):
            for edge in self.graph.edges():
                weight = self.graph[edge[0]][edge[1]].get('weight', 1)
                edge_widths.append(weight * 2)
        else:
            edge_widths = 1
        
        # 绘制网络
        nx.draw_networkx_nodes(self.graph, self.pos, 
                              node_color=node_colors,
                              node_size=node_sizes,
                              alpha=0.7)
        
        nx.draw_networkx_edges(self.graph, self.pos,
                              width=edge_widths,
                              alpha=0.5,
                              edge_color='gray')
        
        # 绘制标签（仅对小网络）
        if self.graph.number_of_nodes() <= 50:
            nx.draw_networkx_labels(self.graph, self.pos, 
                                   font_size=8,
                                   font_weight='bold')
        
        plt.title("Social Network Analysis")
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def draw_centrality_comparison(self, centralities: Dict[str, Dict[str, float]],
                                 save_path: str = None) -> None:
        """绘制中心性比较图"""
        centrality_df = pd.DataFrame(centralities)
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Centrality Measures Comparison')
        
        # 度中心性
        axes[0, 0].bar(range(len(centrality_df)), 
                      centrality_df['degree_centrality'].sort_values(ascending=False))
        axes[0, 0].set_title('Degree Centrality')
        axes[0, 0].set_xlabel('Nodes')
        axes[0, 0].set_ylabel('Centrality')
        
        # 介数中心性
        axes[0, 1].bar(range(len(centrality_df)), 
                      centrality_df['betweenness_centrality'].sort_values(ascending=False))
        axes[0, 1].set_title('Betweenness Centrality')
        axes[0, 1].set_xlabel('Nodes')
        axes[0, 1].set_ylabel('Centrality')
        
        # 接近中心性
        axes[1, 0].bar(range(len(centrality_df)), 
                      centrality_df['closeness_centrality'].sort_values(ascending=False))
        axes[1, 0].set_title('Closeness Centrality')
        axes[1, 0].set_xlabel('Nodes')
        axes[1, 0].set_ylabel('Centrality')
        
        # 特征向量中心性
        axes[1, 1].bar(range(len(centrality_df)), 
                      centrality_df['eigenvector_centrality'].sort_values(ascending=False))
        axes[1, 1].set_title('Eigenvector Centrality')
        axes[1, 1].set_xlabel('Nodes')
        axes[1, 1].set_ylabel('Centrality')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
    
    def draw_community_network(self, community_result: Dict, save_path: str = None) -> None:
        """绘制社区网络"""
        if self.pos is None:
            self.calculate_layout()
        
        plt.figure(figsize=(12, 8))
        
        communities = community_result['communities']
        partition = community_result['partition']
        
        # 为每个社区分配颜色
        colors = plt.cm.Set3(np.linspace(0, 1, len(communities)))
        
        # 绘制每个社区
        for comm_id, nodes in communities.items():
            subgraph = self.graph.subgraph(nodes)
            node_color = [colors[comm_id]]
            
            nx.draw_networkx_nodes(subgraph, self.pos,
                                  node_color=node_color,
                                  node_size=300,
                                  alpha=0.7,
                                  label=f'Community {comm_id}')
        
        # 绘制所有边
        nx.draw_networkx_edges(self.graph, self.pos, alpha=0.3)
        
        # 绘制标签
        if self.graph.number_of_nodes() <= 30:
            nx.draw_networkx_labels(self.graph, self.pos, font_size=8)
        
        plt.title(f"Community Detection - {community_result['method']}")
        plt.legend()
        plt.axis('off')
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        
        plt.show()
```

### 3. 高级网络分析
```python
# 高级网络分析脚本
class AdvancedNetworkAnalysis:
    """高级网络分析器"""
    
    def __init__(self, graph: nx.Graph):
        self.graph = graph
    
    def structural_holes_analysis(self) -> Dict[str, Dict[str, float]]:
        """结构洞分析"""
        # 计算约束系数
        constraints = nx.constraint(self.graph)
        
        # 计算有效规模
        effective_sizes = {}
        for node in self.graph.nodes():
            neighbors = list(self.graph.neighbors(node))
            effective_size = 0
            
            for neighbor in neighbors:
                # 计算邻居之间的连接数
                neighbor_connections = 0
                for other_neighbor in neighbors:
                    if other_neighbor != neighbor and self.graph.has_edge(neighbor, other_neighbor):
                        neighbor_connections += 1
                
                # 有效规模 = 邻居数 - 邻居间连接数/邻居数
                effective_size += 1 - neighbor_connections / (len(neighbors) - 1) if len(neighbors) > 1 else 1
            
            effective_sizes[node] = effective_size
        
        return {
            'constraints': constraints,
            'effective_sizes': effective_sizes,
            'brokerage_scores': {node: 1 - constraints[node] for node in constraints.keys()}
        }
    
    def small_world_analysis(self) -> Dict[str, float]:
        """小世界网络分析"""
        # 计算聚类系数
        clustering_coefficient = nx.average_clustering(self.graph)
        
        # 计算平均路径长度
        if nx.is_connected(self.graph):
            avg_path_length = nx.average_shortest_path_length(self.graph)
        else:
            # 对于不连通的网络，计算最大连通分量的平均路径长度
            largest_cc = max(nx.connected_components(self.graph), key=len)
            subgraph = self.graph.subgraph(largest_cc)
            avg_path_length = nx.average_shortest_path_length(subgraph)
        
        # 生成随机网络进行比较
        n = self.graph.number_of_nodes()
        m = self.graph.number_of_edges()
        random_graph = nx.erdos_renyi_graph(n, m / (n * (n - 1) / 2))
        
        random_clustering = nx.average_clustering(random_graph)
        random_path_length = nx.average_shortest_path_length(random_graph) if nx.is_connected(random_graph) else float('inf')
        
        # 计算小世界系数
        clustering_ratio = clustering_coefficient / random_clustering if random_clustering > 0 else float('inf')
        path_ratio = avg_path_length / random_path_length if random_path_length > 0 else float('inf')
        small_world_coefficient = clustering_ratio / path_ratio if path_ratio > 0 else float('inf')
        
        return {
            'clustering_coefficient': clustering_coefficient,
            'avg_path_length': avg_path_length,
            'random_clustering': random_clustering,
            'random_path_length': random_path_length,
            'clustering_ratio': clustering_ratio,
            'path_ratio': path_ratio,
            'small_world_coefficient': small_world_coefficient
        }
    
    def network_resilience_analysis(self) -> Dict[str, Any]:
        """网络韧性分析"""
        original_components = nx.number_connected_components(self.graph)
        original_size = len(max(nx.connected_components(self.graph), key=len))
        
        # 节点移除分析
        node_removal_effects = {}
        centrality_measures = nx.degree_centrality(self.graph)
        sorted_nodes = sorted(centrality_measures.items(), key=lambda x: x[1], reverse=True)
        
        for node, _ in sorted_nodes[:10]:  # 分析前10个重要节点
            temp_graph = self.graph.copy()
            temp_graph.remove_node(node)
            
            new_components = nx.number_connected_components(temp_graph)
            new_size = len(max(nx.connected_components(temp_graph), key=len)) if temp_graph.nodes() else 0
            
            node_removal_effects[node] = {
                'components_change': new_components - original_components,
                'largest_component_size_change': original_size - new_size,
                'fragmentation_ratio': new_size / original_size if original_size > 0 else 0
            }
        
        # 边移除分析
        edge_removal_effects = {}
        betweenness = nx.edge_betweenness_centrality(self.graph)
        sorted_edges = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)
        
        for edge, _ in sorted_edges[:10]:  # 分析前10条重要边
            temp_graph = self.graph.copy()
            temp_graph.remove_edge(edge[0], edge[1])
            
            new_components = nx.number_connected_components(temp_graph)
            new_size = len(max(nx.connected_components(temp_graph), key=len)) if temp_graph.nodes() else 0
            
            edge_removal_effects[f"{edge[0]}-{edge[1]}"] = {
                'components_change': new_components - original_components,
                'largest_component_size_change': original_size - new_size,
                'fragmentation_ratio': new_size / original_size if original_size > 0 else 0
            }
        
        return {
            'node_removal_effects': node_removal_effects,
            'edge_removal_effects': edge_removal_effects,
            'network_fragility': self._calculate_fragility(node_removal_effects)
        }
    
    def _calculate_fragility(self, removal_effects: Dict) -> float:
        """计算网络脆弱性"""
        total_fragmentation = sum(effect['fragmentation_ratio'] for effect in removal_effects.values())
        return total_fragmentation / len(removal_effects) if removal_effects else 0
    
    def motif_analysis(self) -> Dict[str, int]:
        """网络模体分析"""
        # 使用三角模体作为示例
        triangles = sum(nx.triangles(self.graph).values()) // 3
        
        # 计算所有可能的三元组
        total_triplets = 0
        for node in self.graph.nodes():
            neighbors = list(self.graph.neighbors(node))
            total_triplets += len(neighbors) * (len(neighbors) - 1) / 2
        
        clustering_coefficient = (3 * triangles) / total_triplets if total_triplets > 0 else 0
        
        return {
            'triangles': triangles,
            'total_triplets': total_triplets,
            'clustering_coefficient': clustering_coefficient,
            'transitivity': nx.transitivity(self.graph)
        }
    
    def network_dynamics_simulation(self, steps: int = 100, 
                                 attachment_rule: str = 'preferential') -> Dict[str, List]:
        """网络动态模拟"""
        # 从初始网络开始模拟增长
        dynamic_network = self.graph.copy()
        metrics_history = {
            'nodes': [],
            'edges': [],
            'density': [],
            'clustering': [],
            'avg_path_length': []
        }
        
        for step in range(steps):
            # 添加新节点
            new_node = f"new_node_{step}"
            dynamic_network.add_node(new_node)
            
            # 根据规则添加连接
            if attachment_rule == 'preferential':
                # 优先连接
                degrees = dict(dynamic_network.degree())
                total_degree = sum(degrees.values())
                
                if total_degree > 0:
                    # 基于度分布选择连接目标
                    probabilities = [degrees[node] / total_degree for node in degrees.keys()]
                    target_nodes = np.random.choice(
                        list(degrees.keys()), 
                        size=min(3, len(degrees)), 
                        replace=False,
                        p=probabilities
                    )
                    
                    for target in target_nodes:
                        dynamic_network.add_edge(new_node, target)
            
            # 记录网络指标
            metrics_history['nodes'].append(dynamic_network.number_of_nodes())
            metrics_history['edges'].append(dynamic_network.number_of_edges())
            metrics_history['density'].append(nx.density(dynamic_network))
            metrics_history['clustering'].append(nx.average_clustering(dynamic_network))
            
            if nx.is_connected(dynamic_network):
                metrics_history['avg_path_length'].append(nx.average_shortest_path_length(dynamic_network))
            else:
                metrics_history['avg_path_length'].append(float('inf'))
        
        return {
            'final_network': dynamic_network,
            'metrics_history': metrics_history
        }

# R语言网络分析脚本
r_network_script = '''
# 社会网络分析 - R脚本
library(igraph)
library(tidygraph)
library(ggraph)
library(networkD3)

# 创建网络对象
create_network <- function(edgelist, directed = FALSE, weighted = FALSE) {
  if (weighted) {
    graph <- graph_from_data_frame(edgelist, directed = directed)
  } else {
    graph <- graph_from_data_frame(edgelist[, 1:2], directed = directed)
  }
  
  return(graph)
}

# 计算中心性指标
calculate_centralities <- function(graph) {
  centralities <- list(
    degree = centrality_degree(graph, mode = "all"),
    betweenness = centrality_betweenness(graph),
    closeness = centrality_closeness(graph),
    eigenvector = centrality_eigen(graph),
    pagerank = centrality_pagerank(graph),
    authority = centrality_authority(graph),
    hub = centrality_hub(graph)
  )
  
  return(centralities)
}

# 社区检测
detect_communities <- function(graph, method = "louvain") {
  if (method == "louvain") {
    communities <- cluster_louvain(graph)
  } else if (method == "walktrap") {
    communities <- cluster_walktrap(graph)
  } else if (method == "edge_betweenness") {
    communities <- cluster_edge_betweenness(graph)
  } else if (method == "fast_greedy") {
    communities <- cluster_fast_greedy(graph)
  }
  
  return(communities)
}

# 网络可视化
visualize_network <- function(graph, layout = "fr", 
                            node_size = NULL, 
                            node_color = NULL,
                            save_path = NULL) {
  # 计算布局
  if (layout == "fr") {
    layout_coords <- layout_with_fr(graph)
  } else if (layout == "kk") {
    layout_coords <- layout_with_kk(graph)
  } else if (layout == "circle") {
    layout_coords <- layout_in_circle(graph)
  }
  
  # 创建可视化
  p <- ggraph(graph, layout = layout_coords) +
    geom_edge_link(alpha = 0.5) +
    geom_node_point(aes(size = node_size, color = node_color)) +
    geom_node_text(aes(label = name), repel = TRUE) +
    theme_void()
  
  if (!is.null(save_path)) {
    ggsave(save_path, p, width = 10, height = 8, dpi = 300)
  }
  
  return(p)
}

# 网络统计分析
network_statistics <- function(graph) {
  stats <- list(
    basic_info = list(
      n_nodes = vcount(graph),
      n_edges = ecount(graph),
      is_directed = is_directed(graph),
      is_weighted = is_weighted(graph),
      density = edge_density(graph)
    ),
    connectivity = list(
      is_connected = is_connected(graph),
      n_components = count_components(graph),
      diameter = diameter(graph),
      avg_path_length = mean_distance(graph)
    ),
    clustering = list(
      transitivity = transitivity(graph),
      avg_clustering = transitivity(graph, type = "average")
    )
  )
  
  return(stats)
}

# 结构洞分析
structural_holes <- function(graph) {
  constraints <- constraint(graph)
  effective_size <- effective.size(graph)
  
  return(list(
    constraint = constraints,
    effective_size = effective_size,
    brokerage = 1 - constraints
  ))
}
'''
```

### 4. 网络统计检验
```python
# 网络统计检验脚本
class NetworkStatisticalTests:
    """网络统计检验器"""
    
    def __init__(self, observed_graph: nx.Graph):
        self.observed_graph = observed_graph
        self.random_graphs = []
    
    def generate_random_graphs(self, n: int = 1000, model: str = 'configuration') -> List[nx.Graph]:
        """生成随机网络"""
        self.random_graphs = []
        
        if model == 'configuration':
            # 配置模型（保持度分布）
            degree_sequence = [d for n, d in self.observed_graph.degree()]
            for _ in range(n):
                random_graph = nx.configuration_model(degree_sequence)
                # 转换为简单图
                random_graph = nx.Graph(random_graph)
                random_graph.remove_edges_from(nx.selfloop_edges(random_graph))
                self.random_graphs.append(random_graph)
        
        elif model == 'erdos_renyi':
            # ER随机图
            p = nx.density(self.observed_graph)
            for _ in range(n):
                random_graph = nx.erdos_renyi_graph(
                    self.observed_graph.number_of_nodes(), 
                    p
                )
                self.random_graphs.append(random_graph)
        
        return self.random_graphs
    
    def test_network_properties(self, property_name: str) -> Dict[str, Any]:
        """检验网络属性"""
        if not self.random_graphs:
            self.generate_random_graphs()
        
        # 计算观测网络的属性值
        observed_value = self._calculate_property(self.observed_graph, property_name)
        
        # 计算随机网络的属性分布
        random_values = []
        for graph in self.random_graphs:
            try:
                value = self._calculate_property(graph, property_name)
                random_values.append(value)
            except:
                continue
        
        # 统计检验
        random_values = np.array(random_values)
        mean_random = np.mean(random_values)
        std_random = np.std(random_values)
        
        # Z-score
        z_score = (observed_value - mean_random) / std_random if std_random > 0 else 0
        
        # p值（双尾检验）
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score))) if len(random_values) > 0 else 1
        
        # 置信区间
        ci_lower = np.percentile(random_values, 2.5)
        ci_upper = np.percentile(random_values, 97.5)
        
        return {
            'property': property_name,
            'observed_value': observed_value,
            'random_mean': mean_random,
            'random_std': std_random,
            'z_score': z_score,
            'p_value': p_value,
            'confidence_interval': (ci_lower, ci_upper),
            'significant': p_value < 0.05,
            'random_values': random_values.tolist()
        }
    
    def _calculate_property(self, graph: nx.Graph, property_name: str) -> float:
        """计算网络属性"""
        if property_name == 'density':
            return nx.density(graph)
        elif property_name == 'clustering':
            return nx.average_clustering(graph)
        elif property_name == 'avg_path_length':
            if nx.is_connected(graph):
                return nx.average_shortest_path_length(graph)
            else:
                return float('inf')
        elif property_name == 'diameter':
            if nx.is_connected(graph):
                return nx.diameter(graph)
            else:
                return float('inf')
        elif property_name == 'transitivity':
            return nx.transitivity(graph)
        elif property_name == 'assortativity':
            return nx.degree_assortativity_coefficient(graph)
        else:
            raise ValueError(f"未知的网络属性: {property_name}")
    
    def qap_test(self, matrix1: np.ndarray, matrix2: np.ndarray, 
                permutations: int = 1000) -> Dict[str, Any]:
        """QAP检验（二次分配程序）"""
        # 计算观测相关性
        observed_correlation = np.corrcoef(matrix1.flatten(), matrix2.flatten())[0, 1]
        
        # 随机置换检验
        random_correlations = []
        for _ in range(permutations):
            # 随机置换矩阵的行列
            permuted_indices = np.random.permutation(matrix1.shape[0])
            permuted_matrix1 = matrix1[permuted_indices, :][:, permuted_indices]
            
            correlation = np.corrcoef(permuted_matrix1.flatten(), matrix2.flatten())[0, 1]
            random_correlations.append(correlation)
        
        random_correlations = np.array(random_correlations)
        
        # 计算p值
        p_value = (np.sum(np.abs(random_correlations) >= np.abs(observed_correlation)) + 1) / (permutations + 1)
        
        return {
            'observed_correlation': observed_correlation,
            'random_mean': np.mean(random_correlations),
            'random_std': np.std(random_correlations),
            'p_value': p_value,
            'significant': p_value < 0.05,
            'random_correlations': random_correlations.tolist()
        }

# 使用示例
def main():
    """主函数示例"""
    # 创建示例网络
    edges = [
        ('A', 'B'), ('A', 'C'), ('A', 'D'),
        ('B', 'C'), ('B', 'E'),
        ('C', 'D'), ('C', 'E'),
        ('D', 'E'), ('D', 'F'),
        ('E', 'F'), ('E', 'G'),
        ('F', 'G')
    ]
    
    # 构建网络
    builder = NetworkBuilder()
    graph = builder.create_network_from_edgelist(edges)
    
    # 基础统计分析
    basic_stats = builder.network_basic_stats()
    print("=== 网络基础统计 ===")
    print(f"节点数: {basic_stats['basic_info']['num_nodes']}")
    print(f"边数: {basic_stats['basic_info']['num_edges']}")
    print(f"密度: {basic_stats['basic_info']['density']:.3f}")
    
    # 中心性分析
    centrality_analyzer = NetworkCentrality(graph)
    centralities = centrality_analyzer.calculate_all_centralities()
    key_players = centrality_analyzer.identify_key_players(top_k=3)
    
    print("\n=== 关键节点 (度中心性) ===")
    for node, score in key_players['degree_centrality']:
        print(f"{node}: {score:.3f}")
    
    # 社区检测
    community_detector = CommunityDetection(graph)
    communities = community_detector.detect_communities(method='louvain')
    
    print(f"\n=== 社区检测 ===")
    print(f"社区数量: {communities['num_communities']}")
    print(f"模块度: {communities['modularity']:.3f}")
    
    # 可视化
    visualizer = NetworkVisualization(graph)
    visualizer.draw_network(community_partition=communities['partition'])
    visualizer.draw_community_network(communities)
    
    # 高级分析
    advanced_analyzer = AdvancedNetworkAnalysis(graph)
    small_world = advanced_analyzer.small_world_analysis()
    
    print(f"\n=== 小世界分析 ===")
    print(f"聚类系数: {small_world['clustering_coefficient']:.3f}")
    print(f"平均路径长度: {small_world['avg_path_length']:.3f}")
    print(f"小世界系数: {small_world['small_world_coefficient']:.3f}")
    
    # 统计检验
    statistical_tests = NetworkStatisticalTests(graph)
    density_test = statistical_tests.test_network_properties('density')
    
    print(f"\n=== 密度检验 ===")
    print(f"观测密度: {density_test['observed_value']:.3f}")
    print(f"随机网络平均密度: {density_test['random_mean']:.3f}")
    print(f"p值: {density_test['p_value']:.3f}")

if __name__ == "__main__":
    main()
```

## 实施指南

### 1. 数据准备
- 收集关系数据（边列表、邻接矩阵等）
- 清洗和标准化数据格式
- 验证数据完整性和准确性
- 确定网络类型（有向/无向，加权/无权）

### 2. 网络构建
- 选择合适的网络表示方法
- 处理缺失值和异常值
- 验证网络连接性
- 计算基础网络统计

### 3. 分析执行
- 根据研究问题选择分析方法
- 计算相关网络指标
- 进行统计检验和验证
- 可视化分析结果

### 4. 结果解释
- 结合理论背景解释结果
- 考虑网络分析的局限性
- 提供实践建议
- 制定后续研究计划

## 质量标准

### 1. 数据质量
- 关系数据准确完整
- 节点和边定义清晰
- 时间和边界条件明确
- 数据来源可靠

### 2. 分析准确性
- 使用正确的分析方法
- 准确计算网络指标
- 正确进行统计检验
- 避免分析偏差

### 3. 结果可靠性
- 进行稳健性检验
- 验证分析结果
- 考虑替代解释
- 报告分析局限性

## 应用场景

### 1. 组织网络分析
- 组织结构和沟通网络
- 知识分享和创新网络
- 权力和影响力网络
- 团队合作网络

### 2. 社会网络分析
- 社交媒体网络
- 社区关系网络
- 家庭和亲缘网络
- 社会支持网络

### 3. 学术网络分析
- 合作网络
- 引用网络
- 知识传播网络
- 学科交叉网络

## 评估指标

### 1. 网络指标
- 中心性指标分布
- 社区划分质量
- 网络韧性程度
- 小世界特性

### 2. 分析指标
- 统计显著性
- 效应量大小
- 模型拟合度
- 预测准确性

### 3. 实用指标
- 分析效率
- 结果可解释性
- 决策支持价值
- 实际应用效果