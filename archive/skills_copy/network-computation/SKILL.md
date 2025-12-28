---
name: network-computation
description: 社会网络计算分析工具，提供网络构建、中心性测量、社区检测、网络可视化等完整的网络分析支持
version: 1.0.0
author: chinese-social-sciences-subagents
tags: [network-analysis, social-networks, centrality, community-detection, visualization]
---

# Network Computation Analysis Skill

## Overview
社会网络计算分析技能为社会科学研究提供全面的网络分析支持，包括网络构建、中心性测量、社区检测、网络可视化等，帮助研究者深入理解社会关系结构和动态。

## When to Use This Skill
Use this skill when the user requests:
- Social network analysis of relationships
- Network construction from relational data
- Centrality analysis (degree, betweenness, closeness, eigenvector)
- Community detection and clustering
- Network visualization and mapping
- Structural hole analysis
- Brokerage and mediation analysis
- Network density and cohesion measures
- Network evolution and change analysis
- Two-mode network analysis

## Quick Start
When a user requests network analysis:
1. **Prepare** network data in appropriate format
2. **Construct** the network from relational data
3. **Analyze** key properties (centrality, communities, etc.)
4. **Visualize** the network structure
5. **Interpret** findings in social context

## Core Functions (Progressive Disclosure)

### Primary Functions
- **Network Construction**: Create networks from edgelist or matrix data
- **Centrality Analysis**: Calculate degree, betweenness, and closeness centrality
- **Basic Visualization**: Generate network diagrams with standard layouts
- **Network Metrics**: Compute density, clustering coefficient, path length

### Secondary Functions
- **Community Detection**: Identify clusters using modularity-based methods
- **Advanced Centrality**: Calculate eigenvector centrality, PageRank
- **Structural Analysis**: Identify structural holes, components
- **Interactive Visualization**: Create interactive network diagrams

### Advanced Functions
- **Multi-layer Networks**: Handle networks with multiple relationship types
- **Dynamic Networks**: Analyze network evolution over time
- **Two-mode Networks**: Handle bipartite network structures
- **Advanced Layouts**: Use specialized layout algorithms for large networks

## Detailed Instructions

### 1. Network Data Preparation
   - Validate network data format (edgelist, adjacency matrix, etc.)
   - Clean and preprocess relational data
   - Identify and handle missing or anomalous connections
   - Determine appropriate network type (directed/undirected, weighted/unweighted)

### 2. Network Construction
   - Create network object from data
   - Validate network properties (connectedness, size, etc.)
   - Compute basic network metrics (nodes, edges, density)
   - Visualize initial network structure

### 3. Centrality Analysis
   - Calculate multiple centrality measures
   - Rank nodes by different centrality indicators
   - Identify key players, bridges, and influencers
   - Interpret centrality in social context

### 4. Community Detection
   - Apply appropriate clustering algorithms
   - Validate community structure
   - Analyze inter-community relationships
   - Interpret community meaning in social context

### 5. Network Visualization
   - Create clear, informative network diagrams
   - Use visual attributes to highlight important features
   - Generate publication-quality figures
   - Provide interactive visualization when appropriate

### 6. Interpretation and Reporting
   - Explain findings in social science terms
   - Connect network properties to research questions
   - Consider Chinese social context (guanxi, mianzi, etc.)
   - Provide actionable insights

## Parameters
- `network_format`: Input format (edgelist, adjacency matrix, JSON, etc.)
- `directed`: Whether the network is directed (default: false)
- `weighted`: Whether the network is weighted (default: true)
- `centrality_metrics`: List of centrality measures to compute
- `community_method`: Community detection algorithm to use
- `visualization_type`: Type of visualization (static, interactive)
- `node_attributes`: Additional node properties to visualize
- `edge_attributes`: Additional edge properties to visualize

## Examples

### Example 1: Centrality Analysis
User: "Analyze this social network and identify the most important actors"
Response: Calculate all centrality measures, identify key nodes, interpret in social context.

### Example 2: Community Detection
User: "Find communities within this organization's communication network"
Response: Apply community detection algorithms, validate structure, interpret meaning.

### Example 3: Network Visualization
User: "Create a visualization of this collaboration network"
Response: Generate network diagram with appropriate layout, highlight important nodes.

## Quality Assurance

- Verify network data integrity before analysis
- Use multiple algorithms when possible for validation
- Consider social context in interpretation
- Ensure visualizations are clear and informative
- Validate community detection results

## Output Format

- Complete network analysis report
- Standardized network metrics tables
- Network visualization files (PNG, SVG, interactive HTML)
- Network data files in various formats
- Reproducible analysis code

## Resources
- Social network analysis best practices
- Network visualization guidelines
- Community detection algorithm comparisons
- Chinese social network characteristics (guanxi, etc.)
- Python toolkit: `skills/network-computation/scripts/calculate_centrality.py`

## Metadata
- Compatibility: Claude 3.5 Sonnet and above
- Domain: Social Network Analysis
- Language: Optimized for Chinese research context