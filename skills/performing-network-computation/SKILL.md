---
name: performing-network-computation
description: 当用户需要执行社会网络计算分析，包括网络构建、基础指标计算、社区检测、网络可视化和高级网络分析时使用此技能
version: 1.0.0
author: chinese-social-sciences-subagents
tags: [social-network-analysis, network-computation, graph-analysis, community-detection, network-visualization]
---

# 网络计算分析技能 (Performing Network Computation)

## Overview
为社会科学研究提供全面的社会网络计算分析支持，从网络构建到高级分析的全流程技术实现。

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

## 使用时机

当用户提到以下需求时，使用此技能：
- "网络计算" 或 "网络分析计算"
- "构建社会网络" 或 "网络建模"
- "网络指标计算" 或 "网络统计"
- "社区检测" 或 "聚类分析"
- "网络可视化" 或 "网络绘图"
- 需要进行复杂的社会网络数学计算

## 快速开始

### 工具链（4个核心脚本）

```bash
# 1. 网络构建
python scripts/build_network.py \
  --input data.json \
  --output network.graphml \
  --type weighted

# 2. 指标计算
python scripts/calculate_metrics.py \
  --input network.graphml \
  --output metrics.json

# 3. 社区检测
python scripts/detect_communities.py \
  --input network.graphml \
  --output communities.json \
  --method louvain

# 4. 网络可视化
python scripts/visualize_network.py \
  --input network.graphml \
  --metrics metrics.json \
  --output network_visualization.png
```

## 核心流程

### 第一步：网络构建

使用工具自动构建网络：
```bash
python scripts/build_network.py --input raw_data.json --output network.graphml
```

**关键要点**：
- 数据格式验证
- 网络类型设置（有向/无向，加权/无权）
- 节点边属性处理
- 网络完整性验证

详见：`references/network-construction/INDEX.md`

---

### 第二步：指标计算

使用工具批量计算指标：
```bash
python scripts/calculate_metrics.py --input network.graphml --output metrics.json
```

**计算指标**：
- 网络规模：节点数、边数、密度
- 路径指标：平均路径长度、直径、半径
- 聚类指标：聚类系数、传递性
- 连通性指标：连通分量、割点、桥

详见：`references/metric-calculations/INDEX.md`

---

### 第三步：社区检测

使用工具识别社区：
```bash
python scripts/detect_communities.py --input network.graphml --output communities.json
```

**检测算法**：
- Louvain模块度优化
- 标签传播算法
- 谱聚类方法
- Girvan-Newman算法

详见：`references/community-detection/INDEX.md`

---

### 第四步：网络可视化

使用工具生成可视化：
```bash
python scripts/visualize_network.py \
  --input network.graphml \
  --metrics metrics.json \
  --communities communities.json \
  --output network.png
```

**可视化元素**：
- 节点：大小编码中心性，颜色编码社区
- 边：粗细编码权重
- 布局：力导向、圆形、层次等

详见：`references/visualization-methods/INDEX.md`

## 输出格式

统一的三层JSON格式：

```json
{
  "summary": {
    "total_nodes": 50,
    "total_edges": 120,
    "network_density": 0.098,
    "components": 1,
    "avg_path_length": 2.34,
    "diameter": 6,
    "modularity": 0.72
  },
  "details": {
    "metrics": {
      "clustering_coefficient": 0.45,
      "transitivity": 0.42,
      "centrality_measures": {...},
      "community_stats": {...}
    },
    "communities": [...],
    "visualization_data": {...}
  }
}
```

## 质量检查清单

在完成网络计算分析后，请检查以下项目：

### 数据质量
- [ ] 原始数据格式正确
- [ ] 网络构建无误
- [ ] 缺失数据处理合理
- [ ] 异常值识别准确

### 计算准确性
- [ ] 所有指标计算正确
- [ ] 算法参数设置合理
- [ ] 结果验证充分
- [ ] 数值精度符合要求

### 分析深度
- [ ] 指标解释准确
- [ ] 结果分析深入
- [ ] 模式识别充分
- [ ] 洞察提炼有价值

### 可视化质量
- [ ] 图形清晰可读
- [ ] 颜色编码合理
- [ ] 布局美观合理
- [ ] 关键信息突出

## 常见问题

**快速诊断**：
- 网络规模过大 → 见 `references/performance-optimization/INDEX.md`
- 社区检测不稳定 → 使用 `detect_communities.py` 多次运行取平均
- 计算结果异常 → 见 `references/troubleshooting/INDEX.md` - 数据验证
- 可视化效果差 → 见 `references/visualization-methods/INDEX.md` - 布局调整

## 深入学习

- **网络构建理论**：`references/network-construction/INDEX.md` - 构建方法详解
- **指标计算**：`references/metric-calculations/INDEX.md` - 算法和公式
- **社区检测**：`references/community-detection/INDEX.md` - 算法比较
- **可视化技术**：`references/visualization-methods/INDEX.md` - 技术和最佳实践

## 完成标志

完成高质量的网络计算分析应该：
1. 生成准确完整的网络指标
2. 识别清晰的社区结构
3. 提供直观的可视化结果
4. 给出深入的分析解释

---

*此技能为中文社会科学研究提供全面的网络计算支持，从数据处理到高级分析的技术实现，确保研究的科学性和严谨性。*