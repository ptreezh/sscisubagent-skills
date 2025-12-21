#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试网络分析技能的真实数据
"""

import sys
import json
from pathlib import Path

# Add skills path
sys.path.insert(0, str(Path(__file__).parent / "skills" / "analysis" / "centrality-analysis" / "scripts"))

try:
    from centrality import CentralityAnalyzer

    # Test with real network data
    analyzer = CentralityAnalyzer()

    # Test with small network
    print("Testing with small network...")
    analyzer.load_network('test_data/real/network_analysis/small_network.json', format='json')
    results = analyzer.calculate_all_centralities()

    print('Network Analysis Results:')
    print(f'Nodes: {results["basic_statistics"]["nodes"]}')
    print(f'Edges: {results["basic_statistics"]["edges"]}')
    print(f'Density: {results["basic_statistics"]["density"]:.3f}')
    print(f'Connected: {results["basic_statistics"]["is_connected"]}')

    # Show top nodes by degree centrality
    centrality_df = results['centrality_dataframe']
    print('\nTop 3 nodes by degree centrality:')
    for node, centrality in list(centrality_df.items())[:3]:
        print(f'{node}: {centrality["degree_centrality"]:.3f}')

    print("\n✅ Centrality analysis with real data successful!")

except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)