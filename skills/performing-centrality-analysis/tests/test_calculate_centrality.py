"""
中心性计算工具的单元测试
"""

import sys
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

import networkx as nx
from calculate_centrality import (
    calculate_all_centralities,
    rank_nodes,
    identify_key_nodes
)


class TestCalculateAllCentralities:
    """测试中心性计算"""
    
    def test_basic_network(self):
        """测试基本网络的中心性计算"""
        # 创建简单网络：A-B-C-D（线性）
        G = nx.Graph()
        G.add_edges_from([('A', 'B'), ('B', 'C'), ('C', 'D')])
        
        centralities = calculate_all_centralities(G)
        
        # 验证所有节点都有中心性值
        assert len(centralities) == 4
        assert 'A' in centralities
        
        # 验证中心性类型
        assert 'degree' in centralities['A']
        assert 'closeness' in centralities['A']
        assert 'betweenness' in centralities['A']
        assert 'eigenvector' in centralities['A']
        
        # B和C应该有最高的介数中心性（在中间）
        assert centralities['B']['betweenness'] > 0
        assert centralities['C']['betweenness'] > 0
    
    def test_star_network(self):
        """测试星形网络（中心节点连接所有其他节点）"""
        G = nx.Graph()
        G.add_edges_from([('Center', 'A'), ('Center', 'B'), 
                         ('Center', 'C'), ('Center', 'D')])
        
        centralities = calculate_all_centralities(G)
        
        # 中心节点应该有最高的度中心性
        assert centralities['Center']['degree'] == 1.0
        
        # 中心节点应该有最高的介数中心性
        assert centralities['Center']['betweenness'] > centralities['A']['betweenness']
    
    def test_complete_network(self):
        """测试完全网络（所有节点互相连接）"""
        G = nx.complete_graph(5)
        
        centralities = calculate_all_centralities(G)
        
        # 在完全网络中，所有节点的中心性应该相等
        degree_values = [c['degree'] for c in centralities.values()]
        assert len(set(degree_values)) == 1  # 所有值相同
        
        # 度中心性应该是1.0（连接到所有其他节点）
        assert degree_values[0] == 1.0


class TestRankNodes:
    """测试节点排序"""
    
    def test_rank_by_degree(self):
        """测试按度中心性排序"""
        centralities = {
            'A': {'node': 'A', 'degree': 0.8, 'betweenness': 0.3},
            'B': {'node': 'B', 'degree': 0.5, 'betweenness': 0.7},
            'C': {'node': 'C', 'degree': 0.9, 'betweenness': 0.2}
        }
        
        result = rank_nodes(centralities, metric='degree', top_n=2)
        
        assert len(result) == 2
        assert result[0]['node'] == 'C'  # 最高度中心性
        assert result[1]['node'] == 'A'
    
    def test_rank_by_betweenness(self):
        """测试按介数中心性排序"""
        centralities = {
            'A': {'node': 'A', 'degree': 0.8, 'betweenness': 0.3},
            'B': {'node': 'B', 'degree': 0.5, 'betweenness': 0.7},
            'C': {'node': 'C', 'degree': 0.9, 'betweenness': 0.2}
        }
        
        result = rank_nodes(centralities, metric='betweenness', top_n=3)
        
        assert result[0]['node'] == 'B'  # 最高介数中心性
        assert result[1]['node'] == 'A'
        assert result[2]['node'] == 'C'
    
    def test_top_n_limit(self):
        """测试top_n限制"""
        centralities = {
            'A': {'node': 'A', 'degree': 0.8},
            'B': {'node': 'B', 'degree': 0.5},
            'C': {'node': 'C', 'degree': 0.9},
            'D': {'node': 'D', 'degree': 0.7}
        }
        
        result = rank_nodes(centralities, metric='degree', top_n=2)
        
        assert len(result) == 2


class TestIdentifyKeyNodes:
    """测试关键节点识别"""
    
    def test_identify_hubs(self):
        """测试识别hubs（度中心性高的节点）"""
        centralities = {
            'A': {'degree': 0.6, 'betweenness': 0.1, 'eigenvector': 0.2},
            'B': {'degree': 0.3, 'betweenness': 0.1, 'eigenvector': 0.2},
            'C': {'degree': 0.8, 'betweenness': 0.1, 'eigenvector': 0.2}
        }
        
        thresholds = {'degree': 0.5, 'betweenness': 0.1, 'eigenvector': 0.3}
        result = identify_key_nodes(centralities, thresholds)
        
        # A和C的度中心性≥0.5，应该被识别为hubs
        assert len(result['hubs']) == 2
        assert 'A' in result['hubs']
        assert 'C' in result['hubs']
    
    def test_identify_bridges(self):
        """测试识别bridges（介数中心性高的节点）"""
        centralities = {
            'A': {'degree': 0.3, 'betweenness': 0.15, 'eigenvector': 0.2},
            'B': {'degree': 0.3, 'betweenness': 0.05, 'eigenvector': 0.2},
            'C': {'degree': 0.3, 'betweenness': 0.20, 'eigenvector': 0.2}
        }
        
        thresholds = {'degree': 0.5, 'betweenness': 0.1, 'eigenvector': 0.3}
        result = identify_key_nodes(centralities, thresholds)
        
        # A和C的介数中心性≥0.1，应该被识别为bridges
        assert len(result['bridges']) == 2
        assert 'A' in result['bridges']
        assert 'C' in result['bridges']
    
    def test_identify_influencers(self):
        """测试识别influencers（特征向量中心性高的节点）"""
        centralities = {
            'A': {'degree': 0.3, 'betweenness': 0.05, 'eigenvector': 0.4},
            'B': {'degree': 0.3, 'betweenness': 0.05, 'eigenvector': 0.2},
            'C': {'degree': 0.3, 'betweenness': 0.05, 'eigenvector': 0.5}
        }
        
        thresholds = {'degree': 0.5, 'betweenness': 0.1, 'eigenvector': 0.3}
        result = identify_key_nodes(centralities, thresholds)
        
        # A和C的特征向量中心性≥0.3，应该被识别为influencers
        assert len(result['influencers']) == 2
        assert 'A' in result['influencers']
        assert 'C' in result['influencers']
    
    def test_default_thresholds(self):
        """测试默认阈值"""
        centralities = {
            'A': {'degree': 0.6, 'betweenness': 0.15, 'eigenvector': 0.4}
        }
        
        result = identify_key_nodes(centralities)  # 使用默认阈值
        
        # 使用默认阈值，A应该被识别为所有三种类型
        assert 'A' in result['hubs']
        assert 'A' in result['bridges']
        assert 'A' in result['influencers']


class TestNetworkProperties:
    """测试网络属性计算"""
    
    def test_empty_network(self):
        """测试空网络"""
        G = nx.Graph()
        
        centralities = calculate_all_centralities(G)
        
        assert len(centralities) == 0
    
    def test_single_node(self):
        """测试单节点网络"""
        G = nx.Graph()
        G.add_node('A')
        
        centralities = calculate_all_centralities(G)
        
        assert len(centralities) == 1
        # networkx对单节点的度中心性定义为1.0
        assert centralities['A']['degree'] == 1.0
    
    def test_disconnected_network(self):
        """测试非连通网络"""
        G = nx.Graph()
        G.add_edges_from([('A', 'B'), ('C', 'D')])  # 两个独立的组件
        
        centralities = calculate_all_centralities(G)
        
        assert len(centralities) == 4
        # 接近中心性可能为0（无法到达其他组件）
        # 但不应该报错


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
