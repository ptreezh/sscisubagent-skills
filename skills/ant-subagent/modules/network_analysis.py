"""
ANT Network Analysis Module
Part of the ANT Subagent system
Implements network analysis capabilities from the original ant-network-analysis skill
"""

import networkx as nx
from typing import Dict, List, Any, Tuple
import json


class NetworkAnalyzer:
    """
    Analyzes actor networks using Actor-Network Theory principles
    """
    
    def __init__(self):
        self.graph = nx.Graph()
        
    def create_network_from_data(self, data: Dict[str, Any]) -> nx.Graph:
        """
        Creates a network graph from input data
        """
        self.graph = nx.Graph()
        
        # Add nodes (actors)
        if 'actors' in data:
            for actor in data['actors']:
                actor_type = actor.get('type', 'human')
                self.graph.add_node(
                    actor['id'], 
                    label=actor.get('name', actor['id']),
                    actor_type=actor_type,
                    properties=actor.get('properties', {})
                )
        
        # Add edges (relationships)
        if 'relationships' in data:
            for rel in data['relationships']:
                self.graph.add_edge(
                    rel['source'], 
                    rel['target'], 
                    relationship_type=rel.get('type', 'connection'),
                    strength=rel.get('strength', 1.0),
                    properties=rel.get('properties', {})
                )
        
        return self.graph
    
    def analyze_network_properties(self) -> Dict[str, Any]:
        """
        Analyzes various properties of the network
        """
        if not self.graph.nodes():
            return {}
        
        analysis = {
            'node_count': self.graph.number_of_nodes(),
            'edge_count': self.graph.number_of_edges(),
            'density': nx.density(self.graph),
            'components': nx.number_connected_components(self.graph),
            'diameter': None,
            'avg_clustering': nx.average_clustering(self.graph),
            'centrality_measures': {}
        }
        
        # Calculate centrality measures
        try:
            analysis['centrality_measures']['degree'] = nx.degree_centrality(self.graph)
            analysis['centrality_measures']['betweenness'] = nx.betweenness_centrality(self.graph)
            analysis['centrality_measures']['closeness'] = nx.closeness_centrality(self.graph)
        except:
            # Handle disconnected graphs
            pass
        
        # Calculate diameter if the graph is connected
        if nx.is_connected(self.graph):
            analysis['diameter'] = nx.diameter(self.graph)
        
        return analysis
    
    def identify_key_nodes(self) -> Dict[str, List[str]]:
        """
        Identifies key nodes in the network based on centrality measures
        """
        if not self.graph.nodes():
            return {}
        
        centralities = self.analyze_network_properties()['centrality_measures']
        
        key_nodes = {
            'high_degree': [],
            'high_betweenness': [],
            'high_closeness': []
        }
        
        if 'degree' in centralities:
            sorted_by_degree = sorted(centralities['degree'].items(), key=lambda x: x[1], reverse=True)
            key_nodes['high_degree'] = [node for node, _ in sorted_by_degree[:3]]
        
        if 'betweenness' in centralities:
            sorted_by_betweenness = sorted(centralities['betweenness'].items(), key=lambda x: x[1], reverse=True)
            key_nodes['high_betweenness'] = [node for node, _ in sorted_by_betweenness[:3]]
        
        if 'closeness' in centralities:
            sorted_by_closeness = sorted(centralities['closeness'].items(), key=lambda x: x[1], reverse=True)
            key_nodes['high_closeness'] = [node for node, _ in sorted_by_closeness[:3]]
        
        return key_nodes
    
    def detect_communities(self) -> List[List[str]]:
        """
        Detects communities in the network using modularity-based clustering
        """
        try:
            # Using greedy modularity communities
            communities = nx.community.greedy_modularity_communities(self.graph)
            return [list(community) for community in communities]
        except:
            # Fallback to connected components if community detection fails
            return [list(c) for c in nx.connected_components(self.graph)]
    
    def get_network_summary(self) -> Dict[str, Any]:
        """
        Returns a comprehensive summary of the network analysis
        """
        properties = self.analyze_network_properties()
        key_nodes = self.identify_key_nodes()
        communities = self.detect_communities()
        
        return {
            'network_properties': properties,
            'key_nodes': key_nodes,
            'communities': communities,
            'actor_distribution': self._get_actor_type_distribution()
        }
    
    def _get_actor_type_distribution(self) -> Dict[str, int]:
        """
        Gets the distribution of actor types in the network
        """
        distribution = {}
        for node in self.graph.nodes(data=True):
            actor_type = node[1].get('actor_type', 'unknown')
            distribution[actor_type] = distribution.get(actor_type, 0) + 1
        return distribution