---
name: network-computation
description: 社会网络计算分析工具，提供网络构建、中心性测量、社区检测、网络可视化等完整的网络分析支持
version: 1.0.0
author: socienceAI.com
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

## 脚本调用时机
当需要执行网络计算分析时，调用 `calculate_centrality.py` 脚本，该脚本整合了网络分析的主要功能。

## 输入格式
```json
{
  "network_data": {
    "nodes": [
      {
        "id": "节点唯一ID",
        "label": "节点标签",
        "attributes": {
          "type": "节点类型",
          "size": "节点大小",
          "group": "节点分组"
        }
      }
    ],
    "edges": [
      {
        "source": "源节点ID",
        "target": "目标节点ID",
        "weight": "边权重",
        "type": "边类型",
        "attributes": {
          "strength": "关系强度",
          "direction": "方向性"
        }
      }
    ]
  },
  "analysis_parameters": {
    "network_type": "directed/undirected",
    "is_weighted": true,
    "centrality_metrics": ["degree", "betweenness", "closeness", "eigenvector"],
    "community_method": "louvain/modularity/greedy",
    "visualization_type": "static/interactive",
    "node_attributes": ["type", "size", "group"],
    "edge_attributes": ["weight", "strength", "direction"]
  },
  "analysis_context": "分析背景和目的",
  "research_questions": ["研究问题列表"]
}
```

## 输出格式
```json
{
  "summary": {
    "network_size": "网络规模（节点数）",
    "network_density": "网络密度",
    "connected_components": "连通分量数",
    "analysis_time": "分析耗时"
  },
  "details": {
    "network_metrics": {
      "density": "网络密度",
      "clustering_coefficient": "聚类系数",
      "average_path_length": "平均路径长度",
      "diameter": "网络直径",
      "components": {
        "number_of_components": "连通分量数",
        "largest_component_size": "最大连通分量规模"
      }
    },
    "centrality_analysis": {
      "degree_centrality": {
        "node_id": "中心度值"
      },
      "betweenness_centrality": {
        "node_id": "中心度值"
      },
      "closeness_centrality": {
        "node_id": "中心度值"
      },
      "eigenvector_centrality": {
        "node_id": "中心度值"
      },
      "top_nodes_by_centrality": {
        "degree": ["按度中心度排序的节点"],
        "betweenness": ["按中介中心度排序的节点"],
        "closeness": ["按接近中心度排序的节点"],
        "eigenvector": ["按特征向量中心度排序的节点"]
      }
    },
    "community_detection": {
      "number_of_communities": "社区数量",
      "communities": [
        {
          "id": "社区ID",
          "size": "社区规模",
          "nodes": ["节点列表"],
          "modularity": "模块度值",
          "description": "社区描述"
        }
      ],
      "node_to_community": {
        "node_id": "社区ID"
      }
    },
    "structural_analysis": {
      "structural_holes": ["结构洞分析结果"],
      "bridges": ["桥接节点"],
      "brokerage_roles": ["中介角色"]
    }
  },
  "visualization": {
    "static_image": "静态图像链接",
    "interactive_graph": "交互图链接",
    "layout": "布局类型",
    "color_scheme": "配色方案"
  },
  "interpretation": {
    "key_findings": ["关键发现"],
    "social_interpretation": "社会学解释",
    "research_insights": ["研究洞察"]
  }
  },
  "metadata": {
    "timestamp": "时间戳",
    "version": "版本号",
    "skill": "network-computation",
    "analysis_parameters": "分析参数"
  }
}
```

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