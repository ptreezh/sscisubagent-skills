---
name: performing-network-computation
description: 执行社会网络计算分析，包括网络构建、基础指标计算、社区检测、网络可视化和高级网络分析。当需要进行复杂的社会网络分析、构建网络模型或计算网络统计指标时使用此技能。
version: 1.0.0
author: chinese-social-sciences-subagents
tags: [social-network-analysis, network-computation, graph-analysis, community-detection, network-visualization]
---

# 网络计算分析技能 (Performing Network Computation)

## Overview
为中文社会科学研究提供全面的社会网络计算分析支持，从网络构建到高级分析的全流程技术实现。

## When to Use This Skill
Use this skill when the user requests:
- Complex social network analysis
- Network model construction
- Network statistical indicators calculation
- Community detection and clustering
- Network visualization and mapping
- Graph-based analysis of social structures
- Analysis of relational data in Chinese context
- Computation of network metrics and indices

## Quick Start
When a user requests network computation:
1. **Construct** network from provided data
2. **Compute** basic network indicators
3. **Analyze** centrality measures
4. **Detect** communities and clusters
5. **Visualize** network structure and patterns

## Core Functions (Progressive Disclosure)

### Primary Functions
- **Network Construction**: Build network from various data formats
- **Basic Indicators**: Calculate fundamental network metrics
- **Centrality Computation**: Compute basic centrality measures (degree, closeness)
- **Simple Visualization**: Generate basic network plots

### Secondary Functions
- **Advanced Centrality**: Compute sophisticated centrality measures (betweenness, eigenvector)
- **Community Detection**: Identify clusters using multiple algorithms
- **Path Analysis**: Analyze shortest paths and distances
- **Network Comparison**: Compare multiple networks

### Advanced Functions
- **Dynamic Analysis**: Analyze network evolution over time
- **Multiplex Networks**: Handle networks with multiple relationship types
- **Large-Scale Computation**: Process large networks efficiently
- **Statistical Testing**: Perform statistical tests on network properties

## Detailed Instructions

### 1. Network Construction
   - Validate input data format and structure
   - Convert data to appropriate network representation
   - Handle missing or inconsistent data
   - Set network attributes (directed/undirected, weighted/unweighted)
   - Verify network integrity and completeness

### 2. Basic Network Metrics
   - Calculate network size (nodes, edges)
   - Compute network density
   - Identify connected components
   - Calculate clustering coefficients
   - Determine network diameter and average path length

### 3. Centrality Analysis
   - Compute degree centrality (direct connections)
   - Calculate closeness centrality (reachability)
   - Determine betweenness centrality (control over flows)
   - Analyze eigenvector centrality (influence through connections)
   - Consider additional measures (Katz, PageRank, etc.)

### 4. Community Detection
   - Apply multiple community detection algorithms
   - Validate community structure significance
   - Assess modularity and cohesion
   - Identify overlapping communities if applicable
   - Map community roles and relationships

### 5. Network Visualization
   - Select appropriate layout algorithms
   - Encode node and edge attributes visually
   - Generate static and interactive visualizations
   - Highlight key network features
   - Ensure visualization clarity and interpretability

### 6. Statistical Analysis
   - Perform significance tests on network metrics
   - Conduct comparative analysis between networks
   - Assess reliability of computed measures
   - Evaluate statistical power for network comparisons
   - Validate results with appropriate statistical tests

### 7. Interpretation and Reporting
   - Integrate computational findings with theoretical understanding
   - Connect network properties to research questions
   - Consider Chinese social network characteristics (guanxi, etc.)
   - Provide actionable insights from network analysis
   - Suggest directions for future research

## Parameters
- `network_type`: Type of network (social, technological, biological, etc.)
- `analysis_depth`: Depth of analysis (basic, intermediate, comprehensive)
- `centrality_measures`: List of centrality measures to compute
- `community_method`: Algorithm for community detection (Louvain, label propagation, etc.)
- `visualization_type`: Type of visualization (static, interactive, animated)
- `data_format`: Expected input data format (edgelist, adjacency matrix, etc.)
- `cultural_context`: Cultural context considerations (especially for Chinese context)

## Examples

### Example 1: Academic Collaboration Network
User: "Analyze the collaboration network among researchers in my department"
Response: Construct collaboration network, compute centrality measures, detect research clusters, visualize network.

### Example 2: Organizational Network
User: "Study the communication network in our organization"
Response: Map communication flows, identify key communicators, detect communication silos, suggest improvements.

### Example 3: Policy Network
User: "Analyze the network of actors involved in a policy domain"
Response: Identify key policy actors, analyze their connections, detect coalitions, assess policy influence patterns.

## Quality Standards

- Apply network analysis principles rigorously
- Use appropriate algorithms for network type and size
- Validate computational results statistically
- Consider cultural and contextual factors
- Provide evidence-based interpretations

## Output Format

- Complete network analysis report
- Computed network metrics and statistics
- Identified communities and key nodes
- Network visualization files (PNG, SVG, interactive HTML)
- Reproducible analysis scripts

## Resources
- Social network analysis literature
- Network computation algorithm guides
- Examples of network analysis in Chinese context
- Software documentation for network analysis tools

## Metadata
- Compatibility: Claude 3.5 Sonnet and above
- Domain: Social Network Analysis, Graph Theory
- Language: Optimized for Chinese research context

## 使用时机

当用户提到以下需求时，使用此技能：
- "网络计算" 或 "网络分析计算"
- "构建社会网络" 或 "网络建模"
- "网络指标计算" 或 "网络统计"
- "社区检测" 或 "聚类分析"
- "网络可视化" 或 "网络绘图"
- 需要进行复杂的社会网络数学计算

## 核心功能模块

### 1. 网络构建模块
- **边列表转换**：将关系数据转换为网络图
- **邻接矩阵处理**：从矩阵形式构建网络
- **多种网络类型**：支持有向图、无向图、加权图
- **数据格式兼容**：处理多种常见数据格式

### 2. 基础指标计算
- **网络规模**：节点数、边数、密度
- **路径分析**：最短路径、直径、半径
- **聚类系数**：局部和全局聚类系数
- **连通性**：连通分量、强连通性

### 3. 高级中心性分析
- **四种经典中心性**：度、接近、介数、特征向量
- **Katz中心性**：考虑路径长度的影响
- **PageRank算法**：网页排名算法应用
- **HITS算法**：权威值和枢纽值

### 4. 社区检测分析
- **模块度优化**：Louvain算法
- **标签传播**：快速社区发现
- **层次聚类**：基于距离的聚类
- **图分割**：谱聚类等方法

### 5. 网络可视化
- **力导向布局**：Fruchterman-Reingold算法
- **层次布局**：树形和 radial 布局
- **多维度展示**：颜色、大小、形状编码
- **交互式可视化**：动态网络展示

## 执行步骤

### 第一步：数据输入和网络构建

1. **识别数据格式**
   - 边列表格式：(node1, node2, weight)
   - 邻接矩阵：方阵形式的连接关系
   - 关系列表：关系类型和强度
   - 混合格式：多种数据源整合

2. **网络参数设置**
   - 确定网络类型（有向/无向）
   - 设置权重处理方式
   - 定义节点属性
   - 处理缺失数据

3. **网络构建**
   - 创建网络对象
   - 添加节点和边
   - 设置属性信息
   - 验证网络完整性

### 第二步：基础网络指标计算

1. **网络规模统计**
   ```python
   # 基础网络指标
   num_nodes = G.number_of_nodes()
   num_edges = G.number_of_edges()
   density = nx.density(G)

   # 连通性分析
   is_connected = nx.is_connected(G)
   components = list(nx.connected_components(G))
   largest_cc = max(components, key=len)
   ```

2. **路径和距离分析**
   ```python
   # 路径统计
   avg_shortest_path = nx.average_shortest_path_length(G)
   diameter = nx.diameter(G)
   radius = nx.radius(G)

   # 聚类系数
   clustering = nx.clustering(G)
   avg_clustering = nx.average_clustering(G)
   ```

### 第三步：中心性分析计算

1. **经典中心性指标**
   ```python
   # 四种基本中心性
   degree_centrality = nx.degree_centrality(G)
   betweenness_centrality = nx.betweenness_centrality(G)
   closeness_centrality = nx.closeness_centrality(G)
   eigenvector_centrality = nx.eigenvector_centrality(G)
   ```

2. **高级中心性指标**
   ```python
   # Katz 中心性和 PageRank
   katz_centrality = nx.katz_centrality(G)
   pagerank = nx.pagerank(G)

   # HITS 算法
   hubs, authorities = nx.hits(G)
   ```

### 第四步：社区检测分析

1. **模块度优化**
   ```python
   # Louvain 社区检测
   import community
   partition = community.best_partition(G)
   modularity = community.modularity(partition, G)
   ```

2. **多种方法对比**
   ```python
   # 标签传播算法
   communities = nx.algorithms.community.label_propagation_communities(G)

   # 层次聚类
   dendrogram = nx.algorithms.community.girvan_newman(G)
   ```

### 第五步：结果可视化和报告

1. **网络可视化**
   ```python
   # 基础可视化
   plt.figure(figsize=(12, 8))
   pos = nx.spring_layout(G)
   nx.draw(G, pos, with_labels=True, node_color=colors,
           node_size=sizes, font_size=8)
   ```

2. **统计报告生成**
   - 创建详细的统计表格
   - 生成可视化图表
   - 撰写分析报告

## 输出格式要求

### 统计报告
- **网络基础指标**表格
- **中心性分析**结果
- **社区结构**统计
- **关键节点**识别

### 可视化成果
- **网络拓扑图**
- **中心性分布图**
- **社区结构图**
- **统计图表**

### 数据文件
- **处理后的网络数据**
- **计算结果文件**
- **可视化源文件**
- **分析脚本**

## 质量控制标准

### 数据质量检查
- [ ] 原始数据格式正确
- [ ] 网络构建无误
- [ ] 缺失数据处理合理
- [ ] 异常值识别准确

### 计算准确性验证
- [ ] 所有指标计算正确
- [ ] 算法参数设置合理
- [ ] 结果验证充分
- [ ] 数值精度符合要求

### 分析深度要求
- [ ] 指标解释准确
- [ ] 结果分析深入
- [ ] 模式识别充分
- [ ] 洞察提炼有价值

### 中文语境适配
- [ ] 术语使用准确
- [ ] 解释符合中文习惯
- [ ] 案例贴切
- [ ] 建议实用

## 常见问题处理

**问题：网络规模过大导致计算缓慢**
- 解决：使用近似算法和抽样方法
- 技术：对超大型网络使用流式算法

**问题：社区检测结果不稳定**
- 解决：多次运行取共识结果
- 方法：使用集成学习思路

**问题：中心性指标解释困难**
- 解决：结合具体应用场景解释
- 策略：使用形象化的比喻说明

**问题：可视化效果不佳**
- 解决：调整布局算法和视觉编码
- 技巧：使用分层展示和交互功能

## 技术工具推荐

### 核心Python库
- **NetworkX**：网络分析核心库
- **igraph**：高性能网络分析
- **python-louvain**：社区检测
- **matplotlib/seaborn**：数据可视化

### 专业软件
- **Gephi**：交互式网络可视化
- **UCINET**：专业社会网络分析
- **Pajek**：大型网络分析

### 数据处理工具
- **Pandas**：数据操作
- **NumPy**：数值计算
- **SciPy**：科学计算

## 完成标准

高质量的网络计算分析应该：
1. 提供准确完整的网络指标计算
2. 生成清晰直观的可视化结果
3. 给出深入合理的分析解释
4. 提供可重现的计算代码

---

*此技能为中文社会科学研究提供全面的网络计算支持，从数据处理到高级分析的技术实现，确保研究的科学性和严谨性。*