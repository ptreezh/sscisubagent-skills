#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社会网络分析器
分析个体的社会关系网络质量和连接状况
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional, Set
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict, Counter
import json


@dataclass
class SocialNetworkMetrics:
    """社会网络指标数据类"""
    network_size: float              # 网络规模
    network_density: float           # 网络密度
    tie_strength: float              # 连接强度
    structural_holes: float          # 结构洞数量
    betweenness_centrality: float    # 介数中心性
    closeness_centrality: float      # 接近中心性
    eigenvector_centrality: float    # 特征向量中心性
    reciprocity: float               # 互惠性
    transitivity: float              # 传递性
    diversity_index: float           # 多样性指数


class SocialNetworkAnalyzer:
    """社会网络分析器"""
    
    def __init__(self):
        self.network_weights = {
            'network_size': 0.15,
            'network_density': 0.12,
            'tie_strength': 0.15,
            'structural_holes': 0.10,
            'betweenness_centrality': 0.12,
            'closeness_centrality': 0.10,
            'eigenvector_centrality': 0.08,
            'reciprocity': 0.08,
            'transitivity': 0.05,
            'diversity_index': 0.05
        }
        
        self.network_thresholds = {
            'excellent': 0.80,
            'good': 0.65,
            'satisfactory': 0.50,
            'needs_improvement': 0.35,
            'poor': 0.20
        }
        
        self.relationship_types = [
            'family', 'friends', 'colleagues', 'neighbors', 
            'acquaintances', 'online_connections', 'professional_contacts'
        ]
    
    def analyze_social_network(self, network_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        分析社会网络
        
        Args:
            network_data: 社会网络数据字典
            
        Returns:
            分析结果字典
        """
        # 解析网络数据
        edges = network_data.get('edges', [])
        nodes = network_data.get('nodes', [])
        relationship_data = network_data.get('relationship_data', {})
        
        # 计算网络指标
        metrics = self._calculate_network_metrics(nodes, edges, relationship_data)
        
        # 分析网络结构
        network_structure = self._analyze_network_structure(metrics)
        
        # 评估网络质量
        network_quality = self._assess_network_quality(metrics)
        
        # 识别网络角色
        network_roles = self._identify_network_roles(metrics)
        
        # 分析关系质量
        relationship_quality = self._analyze_relationship_quality(relationship_data)
        
        # 评估社会支持
        social_support = self._assess_social_support(metrics, relationship_data)
        
        # 预测网络发展
        network_evolution = self._predict_network_evolution(metrics)
        
        # 评估异化相关性
        alienation_correlation = self._assess_alienation_correlation(metrics)
        
        return {
            'network_metrics': metrics,
            'network_structure': network_structure,
            'network_quality': network_quality,
            'network_roles': network_roles,
            'relationship_quality': relationship_quality,
            'social_support': social_support,
            'network_evolution': network_evolution,
            'alienation_correlation': alienation_correlation,
            'improvement_suggestions': self._generate_improvement_suggestions(metrics),
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _calculate_network_metrics(self, nodes: List[str], edges: List[Tuple[str, str]], 
                                 relationship_data: Dict[str, Dict]) -> SocialNetworkMetrics:
        """计算网络指标"""
        if not nodes:
            # 返回默认指标
            return SocialNetworkMetrics(
                network_size=0.1, network_density=0.1, tie_strength=0.1,
                structural_holes=0.1, betweenness_centrality=0.1,
                closeness_centrality=0.1, eigenvector_centrality=0.1,
                reciprocity=0.1, transitivity=0.1, diversity_index=0.1
            )
        
        # 网络规模
        network_size = min(1.0, len(nodes) / 50)  # 假设50为理想网络规模
        
        # 网络密度
        max_edges = len(nodes) * (len(nodes) - 1) / 2
        network_density = min(1.0, len(edges) / max_edges) if max_edges > 0 else 0
        
        # 连接强度
        tie_strength = self._calculate_average_tie_strength(edges, relationship_data)
        
        # 结构洞 (使用Burt's constraint简化计算)
        structural_holes = self._calculate_structural_holes(nodes, edges)
        
        # 中心性指标
        betweenness_centrality = self._calculate_betweenness_centrality(nodes, edges)
        closeness_centrality = self._calculate_closeness_centrality(nodes, edges)
        eigenvector_centrality = self._calculate_eigenvector_centrality(nodes, edges)
        
        # 互惠性
        reciprocity = self._calculate_reciprocity(edges)
        
        # 传递性
        transitivity = self._calculate_transitivity(nodes, edges)
        
        # 多样性指数
        diversity_index = self._calculate_diversity_index(relationship_data)
        
        return SocialNetworkMetrics(
            network_size=network_size,
            network_density=network_density,
            tie_strength=tie_strength,
            structural_holes=structural_holes,
            betweenness_centrality=betweenness_centrality,
            closeness_centrality=closeness_centrality,
            eigenvector_centrality=eigenvector_centrality,
            reciprocity=reciprocity,
            transitivity=transitivity,
            diversity_index=diversity_index
        )
    
    def _calculate_average_tie_strength(self, edges: List[Tuple[str, str]], 
                                      relationship_data: Dict[str, Dict]) -> float:
        """计算平均连接强度"""
        if not edges or not relationship_data:
            return 0.5
        
        total_strength = 0
        valid_edges = 0
        
        for edge in edges:
            edge_key = f"{edge[0]}-{edge[1]}"
            reverse_key = f"{edge[1]}-{edge[0]}"
            
            strength = 0
            if edge_key in relationship_data:
                strength = relationship_data[edge_key].get('strength', 0.5)
            elif reverse_key in relationship_data:
                strength = relationship_data[reverse_key].get('strength', 0.5)
            
            total_strength += strength
            valid_edges += 1
        
        return total_strength / valid_edges if valid_edges > 0 else 0.5
    
    def _calculate_structural_holes(self, nodes: List[str], edges: List[Tuple[str, str]]) -> float:
        """计算结构洞 (简化版本)"""
        if len(nodes) < 3:
            return 0.1
        
        # 构建邻接矩阵
        adjacency = defaultdict(set)
        for edge in edges:
            adjacency[edge[0]].add(edge[1])
            adjacency[edge[1]].add(edge[0])
        
        # 计算每个节点的结构洞
        total_holes = 0
        for node in nodes:
            neighbors = adjacency[node]
            if len(neighbors) < 2:
                continue
            
            # 简化的结构洞计算：考虑非连接邻居对
            non_connections = 0
            total_pairs = 0
            neighbor_list = list(neighbors)
            
            for i in range(len(neighbor_list)):
                for j in range(i + 1, len(neighbor_list)):
                    total_pairs += 1
                    if neighbor_list[j] not in adjacency[neighbor_list[i]]:
                        non_connections += 1
            
            if total_pairs > 0:
                node_holes = non_connections / total_pairs
                total_holes += node_holes
        
        # 标准化
        max_possible_holes = len(nodes) * (len(nodes) - 1) / 2
        return min(1.0, total_holes / max_possible_holes) if max_possible_holes > 0 else 0
    
    def _calculate_betweenness_centrality(self, nodes: List[str], edges: List[Tuple[str, str]]) -> float:
        """计算介数中心性 (简化版本)"""
        if len(nodes) < 3:
            return 0.5
        
        # 构建图
        graph = defaultdict(set)
        for edge in edges:
            graph[edge[0]].add(edge[1])
            graph[edge[1]].add(edge[0])
        
        # 计算每个节点作为中间节点的重要性
        total_betweenness = 0
        for start_node in nodes:
            # 简化的最短路径计算
            paths = self._find_shortest_paths(graph, start_node, nodes)
            betweenness = 0
            for end_node in paths:
                if end_node != start_node:
                    # 简化：使用路径长度作为介数指标
                    betweenness += 1 / len(paths[end_node])
            total_betweenness += betweenness
        
        # 标准化
        max_betweenness = len(nodes) * (len(nodes) - 1) / 2
        return min(1.0, total_betweenness / max_betweenness) if max_betweenness > 0 else 0.5
    
    def _find_shortest_paths(self, graph: Dict[str, Set[str]], start: str, all_nodes: List[str]) -> Dict[str, List[str]]:
        """找到从起始节点到其他节点的最短路径"""
        paths = {start: [start]}
        visited = {start}
        queue = [start]
        
        while queue:
            current = queue.pop(0)
            for neighbor in graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    # 简化的路径记录
                    paths[neighbor] = paths[current] + [neighbor]
        
        return paths
    
    def _calculate_closeness_centrality(self, nodes: List[str], edges: List[Tuple[str, str]]) -> float:
        """计算接近中心性 (简化版本)"""
        if len(nodes) < 2:
            return 0.5
        
        # 构建图
        graph = defaultdict(set)
        for edge in edges:
            graph[edge[0]].add(edge[1])
            graph[edge[1]].add(edge[0])
        
        # 计算平均最短路径长度
        total_distance = 0
        path_count = 0
        
        for i, start_node in enumerate(nodes):
            for j, end_node in enumerate(nodes):
                if i != j:
                    distance = self._shortest_path_length(graph, start_node, end_node)
                    if distance > 0:
                        total_distance += distance
                        path_count += 1
        
        if path_count > 0:
            avg_distance = total_distance / path_count
            # 转换为中心性分数（距离越短，中心性越高）
            return min(1.0, 1.0 / avg_distance) if avg_distance > 0 else 0.5
        else:
            return 0.5
    
    def _shortest_path_length(self, graph: Dict[str, Set[str]], start: str, end: str) -> int:
        """计算两点间最短路径长度"""
        if start == end:
            return 0
        
        visited = {start}
        queue = [(start, 0)]
        
        while queue:
            current, distance = queue.pop(0)
            
            for neighbor in graph[current]:
                if neighbor == end:
                    return distance + 1
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, distance + 1))
        
        return float('inf')  # 无法到达
    
    def _calculate_eigenvector_centrality(self, nodes: List[str], edges: List[Tuple[str, str]]) -> float:
        """计算特征向量中心性 (简化版本)"""
        if not edges:
            return 0.1
        
        # 计算每个节点的连接度
        connections = {}
        for node in nodes:
            connections[node] = 0
        
        for edge in edges:
            connections[edge[0]] += 1
            connections[edge[1]] += 1
        
        # 标准化
        max_connections = max(connections.values()) if connections.values() else 1
        avg_centrality = sum(connections.values()) / len(connections) / max_connections if connections else 0
        
        return avg_centrality
    
    def _calculate_reciprocity(self, edges: List[Tuple[str, str]]) -> float:
        """计算互惠性"""
        if not edges:
            return 0.1
        
        reciprocal_edges = 0
        edge_set = set(edges)
        
        for edge in edges:
            reverse_edge = (edge[1], edge[0])
            if reverse_edge in edge_set:
                reciprocal_edges += 1
        
        return reciprocal_edges / len(edges) if edges else 0.1
    
    def _calculate_transitivity(self, nodes: List[str], edges: List[Tuple[str, str]]) -> float:
        """计算传递性"""
        if len(nodes) < 3:
            return 0.1
        
        # 构建邻接集
        adjacency = defaultdict(set)
        for edge in edges:
            adjacency[edge[0]].add(edge[1])
            adjacency[edge[1]].add(edge[0])
        
        triangles = 0
        triples = 0
        
        # 简化的传递性计算
        for i, node1 in enumerate(nodes):
            for j, node2 in enumerate(nodes):
                if i >= j:
                    continue
                
                for k, node3 in enumerate(nodes):
                    if j >= k:
                        continue
                    
                    # 检查是否形成三角形
                    if (node2 in adjacency[node1] and 
                        node3 in adjacency[node2] and 
                        node3 in adjacency[node1]):
                        triangles += 1
                    
                    triples += 1
        
        return triangles / triples if triples > 0 else 0.1
    
    def _calculate_diversity_index(self, relationship_data: Dict[str, Dict]) -> float:
        """计算多样性指数"""
        if not relationship_data:
            return 0.5
        
        # 统计关系类型分布
        type_counts = Counter()
        for edge_data in relationship_data.values():
            rel_type = edge_data.get('type', 'unknown')
            type_counts[rel_type] += 1
        
        # 计算香农多样性指数
        total = sum(type_counts.values())
        if total == 0:
            return 0.1
        
        diversity = 0
        for count in type_counts.values():
            p = count / total
            if p > 0:
                diversity -= p * np.log(p)
        
        # 标准化 (假设最大多样性为ln(7) = 1.945)
        max_diversity = np.log(len(self.relationship_types))
        return diversity / max_diversity if max_diversity > 0 else 0.5
    
    def _analyze_network_structure(self, metrics: SocialNetworkMetrics) -> Dict[str, Any]:
        """分析网络结构"""
        return {
            'network_type': self._classify_network_type(metrics),
            'structural_characteristics': {
                'size_adequacy': 'adequate' if 0.4 <= metrics.network_size <= 0.8 else 'inadequate',
                'density_level': self._classify_density_level(metrics.network_density),
                'centralization': 'high' if metrics.betweenness_centrality > 0.7 else 'moderate',
                'clustering': 'high' if metrics.transitivity > 0.5 else 'low'
            },
            'structural_assessment': self._assess_structural_health(metrics)
        }
    
    def _assess_network_quality(self, metrics: SocialNetworkMetrics) -> Dict[str, Any]:
        """评估网络质量"""
        overall_quality = self._calculate_overall_quality(metrics)
        
        return {
            'overall_quality_score': overall_quality,
            'quality_level': self._determine_quality_level(overall_quality),
            'quality_dimensions': {
                'connectivity': (metrics.network_density + metrics.tie_strength) / 2,
                'influence': (metrics.betweenness_centrality + metrics.eigenvector_centrality) / 2,
                'support': (metrics.closeness_centrality + metrics.reciprocity) / 2,
                'diversity': metrics.diversity_index
            },
            'quality_indicators': self._generate_quality_indicators(metrics)
        }
    
    def _identify_network_roles(self, metrics: SocialNetworkMetrics) -> Dict[str, Any]:
        """识别网络角色"""
        return {
            'primary_role': self._determine_primary_role(metrics),
            'role_characteristics': self._analyze_role_characteristics(metrics),
            'network_position': self._assess_network_position(metrics)
        }
    
    def _analyze_relationship_quality(self, relationship_data: Dict[str, Dict]) -> Dict[str, Any]:
        """分析关系质量"""
        if not relationship_data:
            return {'error': '关系数据缺失'}
        
        # 分析不同类型关系的质量
        type_quality = {}
        for rel_type in self.relationship_types:
            type_edges = [data for data in relationship_data.values() 
                         if data.get('type') == rel_type]
            if type_edges:
                avg_quality = np.mean([edge.get('quality', 0.5) for edge in type_edges])
                type_quality[rel_type] = avg_quality
        
        return {
            'relationship_type_quality': type_quality,
            'overall_relationship_quality': np.mean(list(type_quality.values())) if type_quality else 0.5,
            'relationship_distribution': self._analyze_relationship_distribution(relationship_data)
        }
    
    def _assess_social_support(self, metrics: SocialNetworkMetrics, 
                             relationship_data: Dict[str, Dict]) -> Dict[str, Any]:
        """评估社会支持"""
        # 基于网络指标评估社会支持水平
        support_score = (
            metrics.tie_strength * 0.3 +
            metrics.network_size * 0.2 +
            metrics.diversity_index * 0.2 +
            metrics.reciprocity * 0.15 +
            metrics.closeness_centrality * 0.15
        )
        
        return {
            'support_score': support_score,
            'support_level': self._determine_support_level(support_score),
            'support_sources': self._identify_support_sources(relationship_data),
            'support_gaps': self._identify_support_gaps(metrics)
        }
    
    def _predict_network_evolution(self, metrics: SocialNetworkMetrics) -> Dict[str, Any]:
        """预测网络发展"""
        # 基于当前指标预测网络发展趋势
        evolution_trend = self._calculate_evolution_trend(metrics)
        
        return {
            'evolution_trend': evolution_trend,
            'predicted_changes': self._predict_network_changes(metrics),
            'evolution_factors': self._identify_evolution_factors(metrics)
        }
    
    def _assess_alienation_correlation(self, metrics: SocialNetworkMetrics) -> Dict[str, float]:
        """评估与社会异化的相关性"""
        # 社会网络薄弱与社会异化的相关性
        alienation_correlation = 1 - (
            metrics.network_size * 0.25 +
            metrics.tie_strength * 0.25 +
            metrics.diversity_index * 0.2 +
            metrics.reciprocity * 0.15 +
            metrics.closeness_centrality * 0.15
        )
        
        return {
            'social_alienation_correlation': max(0, min(1, alienation_correlation)),
            'alienation_risk_level': self._determine_risk_level(alienation_correlation),
            'isolation_indicators': self._identify_isolation_indicators(metrics)
        }
    
    # 辅助方法
    def _classify_network_type(self, metrics: SocialNetworkMetrics) -> str:
        """分类网络类型"""
        if metrics.network_size < 0.3:
            return '小型网络'
        elif metrics.network_density > 0.7:
            return '密集网络'
        elif metrics.structural_holes > 0.6:
            return '结构洞网络'
        elif metrics.diversity_index > 0.7:
            return '多样化网络'
        else:
            return '标准网络'
    
    def _classify_density_level(self, density: float) -> str:
        """分类密度等级"""
        if density > 0.7:
            return '高密度'
        elif density > 0.4:
            return '中等密度'
        else:
            return '低密度'
    
    def _assess_structural_health(self, metrics: SocialNetworkMetrics) -> str:
        """评估结构健康度"""
        health_score = (
            metrics.network_size * 0.2 +
            metrics.network_density * 0.2 +
            metrics.tie_strength * 0.2 +
            metrics.structural_holes * 0.2 +
            metrics.diversity_index * 0.2
        )
        
        if health_score > 0.7:
            return '健康'
        elif health_score > 0.5:
            return '一般'
        else:
            return '不健康'
    
    def _calculate_overall_quality(self, metrics: SocialNetworkMetrics) -> float:
        """计算总体质量分数"""
        weights = self.network_weights
        values = [
            metrics.network_size * weights['network_size'],
            metrics.network_density * weights['network_density'],
            metrics.tie_strength * weights['tie_strength'],
            metrics.structural_holes * weights['structural_holes'],
            metrics.betweenness_centrality * weights['betweenness_centrality'],
            metrics.closeness_centrality * weights['closeness_centrality'],
            metrics.eigenvector_centrality * weights['eigenvector_centrality'],
            metrics.reciprocity * weights['reciprocity'],
            metrics.transitivity * weights['transitivity'],
            metrics.diversity_index * weights['diversity_index']
        ]
        
        return sum(values)
    
    def _determine_quality_level(self, quality: float) -> str:
        """确定质量等级"""
        if quality >= self.network_thresholds['excellent']:
            return '优秀'
        elif quality >= self.network_thresholds['good']:
            return '良好'
        elif quality >= self.network_thresholds['satisfactory']:
            return '满意'
        elif quality >= self.network_thresholds['needs_improvement']:
            return '需要改进'
        else:
            return '较差'
    
    def _generate_quality_indicators(self, metrics: SocialNetworkMetrics) -> List[str]:
        """生成质量指标"""
        indicators = []
        
        if metrics.network_size > 0.7:
            indicators.append('网络规模适中')
        if metrics.tie_strength > 0.7:
            indicators.append('关系连接强度高')
        if metrics.diversity_index > 0.6:
            indicators.append('关系类型多样化')
        if metrics.betweenness_centrality > 0.6:
            indicators.append('在网络中具有重要影响力')
        if metrics.reciprocity > 0.6:
            indicators.append('关系互惠性良好')
        
        return indicators
    
    def _determine_primary_role(self, metrics: SocialNetworkMetrics) -> str:
        """确定主要网络角色"""
        if metrics.betweenness_centrality > 0.7:
            return '中介者'
        elif metrics.eigenvector_centrality > 0.7:
            return '影响者'
        elif metrics.network_size > 0.8:
            return '连接者'
        elif metrics.tie_strength > 0.7:
            return '紧密关系维护者'
        else:
            return '普通参与者'
    
    def _analyze_role_characteristics(self, metrics: SocialNetworkMetrics) -> Dict[str, str]:
        """分析角色特征"""
        return {
            'influence_level': 'high' if metrics.betweenness_centrality > 0.6 else 'moderate',
            'connectivity': 'strong' if metrics.network_size > 0.6 else 'moderate',
            'relationship_quality': 'strong' if metrics.tie_strength > 0.6 else 'moderate',
            'network_position': 'central' if metrics.closeness_centrality > 0.6 else 'peripheral'
        }
    
    def _assess_network_position(self, metrics: SocialNetworkMetrics) -> str:
        """评估网络位置"""
        centrality_score = (metrics.betweenness_centrality + 
                          metrics.closeness_centrality + 
                          metrics.eigenvector_centrality) / 3
        
        if centrality_score > 0.7:
            return '中心位置'
        elif centrality_score > 0.4:
            return '半中心位置'
        else:
            return '边缘位置'
    
    def _analyze_relationship_distribution(self, relationship_data: Dict[str, Dict]) -> Dict[str, int]:
        """分析关系分布"""
        distribution = Counter()
        for data in relationship_data.values():
            rel_type = data.get('type', 'unknown')
            distribution[rel_type] += 1
        return dict(distribution)
    
    def _determine_support_level(self, support_score: float) -> str:
        """确定支持水平"""
        if support_score > 0.7:
            return '高支持'
        elif support_score > 0.5:
            return '中等支持'
        elif support_score > 0.3:
            return '低支持'
        else:
            return '缺乏支持'
    
    def _identify_support_sources(self, relationship_data: Dict[str, Dict]) -> List[str]:
        """识别支持来源"""
        sources = []
        for data in relationship_data.values():
            rel_type = data.get('type', 'unknown')
            quality = data.get('quality', 0)
            if quality > 0.6:
                sources.append(rel_type)
        return sources
    
    def _identify_support_gaps(self, metrics: SocialNetworkMetrics) -> List[str]:
        """识别支持缺口"""
        gaps = []
        
        if metrics.network_size < 0.4:
            gaps.append('网络规模不足')
        if metrics.diversity_index < 0.4:
            gaps.append('关系类型单一')
        if metrics.tie_strength < 0.4:
            gaps.append('关系深度不足')
        if metrics.reciprocity < 0.4:
            gaps.append('互惠关系不足')
        
        return gaps
    
    def _calculate_evolution_trend(self, metrics: SocialNetworkMetrics) -> str:
        """计算发展趋势"""
        trend_score = (
            metrics.network_size * 0.3 +
            metrics.tie_strength * 0.3 +
            metrics.diversity_index * 0.2 +
            metrics.structural_holes * 0.2
        )
        
        if trend_score > 0.6:
            return '增长趋势'
        elif trend_score > 0.4:
            return '稳定趋势'
        else:
            return '衰退趋势'
    
    def _predict_network_changes(self, metrics: SocialNetworkMetrics) -> List[str]:
        """预测网络变化"""
        changes = []
        
        if metrics.network_size < 0.4:
            changes.append('网络规模可能扩大')
        if metrics.tie_strength < 0.4:
            changes.append('关系强度可能提升')
        if metrics.diversity_index < 0.4:
            changes.append('关系类型可能多样化')
        if metrics.structural_holes > 0.7:
            changes.append('结构洞位置可能保持')
        
        return changes
    
    def _identify_evolution_factors(self, metrics: SocialNetworkMetrics) -> List[str]:
        """识别发展因素"""
        factors = []
        
        if metrics.tie_strength > 0.6:
            factors.append('强关系纽带有利于网络稳定')
        if metrics.diversity_index > 0.6:
            factors.append('多样化关系有利于网络扩展')
        if metrics.structural_holes > 0.6:
            factors.append('结构洞位置有利于信息获取')
        if metrics.reciprocity > 0.6:
            factors.append('互惠关系有利于长期发展')
        
        return factors
    
    def _determine_risk_level(self, risk: float) -> str:
        """确定风险等级"""
        if risk >= 0.7:
            return '高风险'
        elif risk >= 0.5:
            return '中等风险'
        elif risk >= 0.3:
            return '低风险'
        else:
            return '极低风险'
    
    def _identify_isolation_indicators(self, metrics: SocialNetworkMetrics) -> List[str]:
        """识别孤立指标"""
        indicators = []
        
        if metrics.network_size < 0.3:
            indicators.append('网络规模过小')
        if metrics.tie_strength < 0.3:
            indicators.append('关系连接薄弱')
        if metrics.diversity_index < 0.3:
            indicators.append('关系类型单一')
        if metrics.closeness_centrality < 0.3:
            indicators.append('网络位置边缘化')
        
        return indicators
    
    def _generate_improvement_suggestions(self, metrics: SocialNetworkMetrics) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if metrics.network_size < 0.5:
            suggestions.append('扩大社交网络，增加新的关系连接')
        if metrics.tie_strength < 0.5:
            suggestions.append('深化现有关系，提高连接质量')
        if metrics.diversity_index < 0.5:
            suggestions.append('拓展关系类型，建立多样化社交圈')
        if metrics.reciprocity < 0.5:
            suggestions.append('增强关系互惠性，建立双向支持')
        if metrics.closeness_centrality < 0.5:
            suggestions.append('提高网络中心性，增强影响力')
        
        return suggestions


def main():
    """主函数 - 用于测试"""
    analyzer = SocialNetworkAnalyzer()
    
    # 测试数据
    test_data = {
        'nodes': ['A', 'B', 'C', 'D', 'E'],
        'edges': [('A', 'B'), ('B', 'C'), ('C', 'D'), ('A', 'C'), ('B', 'D')],
        'relationship_data': {
            'A-B': {'type': 'friends', 'strength': 0.8, 'quality': 0.7},
            'B-C': {'type': 'colleagues', 'strength': 0.6, 'quality': 0.6},
            'C-D': {'type': 'family', 'strength': 0.9, 'quality': 0.8},
            'A-C': {'type': 'acquaintances', 'strength': 0.4, 'quality': 0.5},
            'B-D': {'type': 'neighbors', 'strength': 0.5, 'quality': 0.5}
        }
    }
    
    # 分析社会网络
    result = analyzer.analyze_social_network(test_data)
    
    # 打印结果
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()