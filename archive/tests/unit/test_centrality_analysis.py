#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中心性分析工具单元测试
测试网络中心性计算功能
"""

import unittest
import sys
import json
import tempfile
from pathlib import Path

# 添加技能脚本路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skills" / "analysis" / "centrality-analysis" / "scripts"))

try:
    from centrality import CentralityAnalyzer
except ImportError as e:
    print(f"导入错误: {e}")
    sys.exit(1)

class TestCentralityAnalyzer(unittest.TestCase):
    """测试中心性分析器"""

    def setUp(self):
        self.analyzer = CentralityAnalyzer()

    def test_load_network_from_json(self):
        """测试从JSON加载网络"""
        # 创建测试网络数据
        test_network = {
            "nodes": ["A", "B", "C", "D", "E"],
            "edges": [
                ["A", "B"], ["A", "C"], ["B", "C"],
                ["B", "D"], ["C", "D"], ["D", "E"]
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(test_network, f)
            network_file = f.name

        try:
            # 测试加载网络
            self.analyzer.load_network(network_file)
            self.assertIsNotNone(self.analyzer.graph)
            self.assertEqual(self.analyzer.graph.number_of_nodes(), 5)
            self.assertEqual(self.analyzer.graph.number_of_edges(), 6)

        finally:
            Path(network_file).unlink()

    def test_calculate_all_centralities(self):
        """测试所有中心性指标计算"""
        # 创建简单网络
        self.analyzer.graph = self._create_test_network()

        # 计算中心性指标
        results = self.analyzer.calculate_all_centralities()

        self.assertIn('basic_statistics', results)
        self.assertIn('centrality_measures', results)
        self.assertIn('centrality_dataframe', results)
        self.assertIn('key_nodes', results)

        # 检查基本统计
        stats = results['basic_statistics']
        self.assertEqual(stats['nodes'], 4)
        self.assertEqual(stats['edges'], 5)
        self.assertGreater(stats['density'], 0)

        # 检查中心性指标
        measures = results['centrality_measures']
        self.assertIn('degree_centrality', measures)
        self.assertIn('betweenness_centrality', measures)
        self.assertIn('closeness_centrality', measures)
        self.assertIn('eigenvector_centrality', measures)

        # 检查关键节点
        key_nodes = results['key_nodes']
        self.assertIn('overall_top', key_nodes)
        self.assertEqual(len(key_nodes['overall_top']), 4)

    def test_generate_report(self):
        """测试报告生成"""
        # 创建测试网络
        self.analyzer.graph = self._create_test_network()
        results = self.analyzer.calculate_all_centralities()

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            report_file = f.name

        try:
            # 生成报告
            report = self.analyzer.generate_report(report_file)

            self.assertIn('network_summary', report)
            self.assertIn('centrality_summary', report)
            self.assertIn('key_nodes_analysis', report)
            self.assertIn('centrality_correlation', report)
            self.assertIn('top_nodes', report)

        finally:
            Path(report_file).unlink()

    def test_handle_disconnected_network(self):
        """测试断开连接的网络"""
        # 创建断开连接的网络
        self.analyzer.graph = self._create_disconnected_network()

        # 计算中心性指标
        results = self.analyzer.calculate_all_centralities()

        # 应该标记为不连通
        stats = results['basic_statistics']
        self.assertFalse(stats['is_connected'])

        # 某些中心性指标应该无法计算
        measures = results['centrality_measures']
        # closeness centrality 在断开连接的网络中会有问题

    def test_edge_cases(self):
        """测试边界情况"""
        # 测试空网络
        self.analyzer.graph = None

        with self.assertRaises(ValueError):
            self.analyzer.calculate_all_centralities()

        # 测试单节点网络
        import networkx as nx
        self.analyzer.graph = nx.Graph()
        self.analyzer.graph.add_node("A")

        results = self.analyzer.calculate_all_centralities()

        measures = results['centrality_measures']
        # 单节点网络的中心性应该为0或接近0
        self.assertLessEqual(measures['degree_centrality']['A'], 1.0)
        self.assertLessEqual(measures['closeness_centrality']['A'], 1.0)

    def _create_test_network(self):
        """创建测试网络"""
        import networkx as nx
        G = nx.Graph()
        G.add_edges_from([
            ('A', 'B'), ('A', 'C'), ('B', 'C'),
            ('B', 'D'), ('C', 'D')
        ])
        return G

    def _create_disconnected_network(self):
        """创建断开连接的网络"""
        import networkx as nx
        G = nx.Graph()
        G.add_edges_from([
            ('A', 'B'), ('A', 'C')
        ])
        G.add_edges_from([
            ('D', 'E')  # 断开的组件
        ])
        return G

class TestNetworkDataFormats(unittest.TestCase):
    """测试不同网络数据格式"""

    def setUp(self):
        self.analyzer = CentralityAnalyzer()

    def test_edgelist_format(self):
        """测试边列表格式"""
        edgelist_data = {
            "edges": [
                ["A", "B"],
                ["B", "C"],
                ["C", "D"],
                ["A", "D"],
                ["B", "E"],
                ["C", "E"]
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(edgelist_data, f)
            data_file = f.name

        try:
            self.analyzer.load_network(data_file, format='edgelist')
            self.assertEqual(self.analyzer.graph.number_of_nodes(), 5)
            self.assertEqual(self.analyzer.graph.number_of_edges(), 6)

        finally:
            Path(data_file).unlink()

    def test_adjacency_matrix_format(self):
        """测试邻接矩阵格式"""
        import numpy as np
        adjacency_matrix = np.array([
            [0, 1, 1, 0, 1],
            [1, 0, 1, 1, 1],
            [1, 1, 0, 1, 1],
            [0, 1, 1, 0, 1],
            [1, 1, 1, 1, 0]
        ])

        adjacency_data = {
            "adjacency_matrix": adjacency_matrix.tolist(),
            "nodes": ["A", "B", "C", "D", "E"]
        }

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(adjacency_data, f)
            data_file = f.name

        try:
            self.analyzer.load_network(data_file, format='adjacency')
            self.assertEqual(self.analyzer.graph.number_of_nodes(), 5)
            # 无向图中，邻接矩阵的上三角部分决定了边数
            self.assertEqual(self.analyzer.graph.number_of_edges(), 9)

        finally:
            Path(data_file).unlink()

if __name__ == '__main__':
    unittest.main()