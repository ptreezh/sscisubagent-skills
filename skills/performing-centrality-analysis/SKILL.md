---
name: performing-centrality-analysis
description: 当用户需要执行社会网络中心性分析，包括度中心性、接近中心性、介数中心性和特征向量中心性的计算和解释时使用此技能
version: 1.0.0
author: chinese-social-sciences-subagents
tags: [social-network-analysis, centrality-measures, network-analysis, graph-theory, node-importance]
---

# 网络中心性分析技能 (Performing Centrality Analysis)

## Overview
识别网络中的关键节点，为中文社会科学研究提供网络结构和权力关系的量化分析。

## When to Use This Skill
Use this skill when the user requests:
- Calculation of network centrality measures (degree, closeness, betweenness, eigenvector)
- Identification of key nodes or influential actors in a network
- Analysis of power distribution and influence in social networks
- Detection of bridges or brokers in information flow
- Assessment of node importance and connectivity
- Understanding of network structure and key positions
- Analysis of social network data in Chinese context

## Quick Start
When a user requests centrality analysis:
1. **Calculate** all four main centrality measures
2. **Compare** different centrality indicators
3. **Identify** key influential nodes (hubs, bridges, influencers)
4. **Analyze** the relationship between different centrality measures
5. **Interpret** results in Chinese social network context

## 使用时机

当用户提到以下需求时，使用此技能：
- "中心性分析" 或 "计算中心性"
- "关键节点识别" 或 "找出重要节点"
- "权力中心" 或 "影响力分析"
- "社会网络分析" 或 "网络结构"
- "信息枢纽" 或 "信息传播"
- 需要量化分析网络中节点的重要性

## 快速开始

### 工具链（5个核心脚本）

```bash
# 1. 计算所有中心性指标
python scripts/calculate_centrality.py \
  --input network.json \
  --output centrality.json

# 2. 按特定指标排序
python scripts/calculate_centrality.py \
  --input network.json \
  --metric betweenness \
  --top 20

# 3. 识别关键节点
python scripts/identify_key_nodes.py \
  --input centrality.json \
  --output key_nodes.json

# 4. 比较不同中心性
python scripts/compare_centralities.py \
  --input centrality.json \
  --output comparison.json

# 5. 网络可视化
python scripts/visualize_centrality.py \
  --input network.json \
  --centrality centrality.json \
  --output network_viz.png
```

## 核心流程

### 第一步：数据预处理

使用预处理工具清洗网络数据：
```bash
python scripts/preprocess_network_data.py --input raw_data.json --output clean_network.json
```

**关键要点**：
- 网络格式验证
- 缺失值处理
- 异常值检测

详见：`references/data-preparation.md`

### 第二步：中心性计算

使用计算工具获得四种中心性指标：
```bash
python scripts/calculate_centrality.py --input clean_network.json --output centrality_measures.json
```

**计算指标**：
- 度中心性：节点的直接连接数
- 接近中心性：到达其他节点的容易程度
- 介数中心性：在最短路径中的重要性
- 特征向量中心性：连接到重要节点的程度

详见：`references/centrality-theory.md`

### 第三步：关键节点识别

使用分类工具识别不同类型的节点：
```bash
python scripts/identify_key_nodes.py --input centrality_measures.json --output node_classifications.json
```

**节点类型**：
- Hubs（枢纽节点）：度中心性高
- Bridges（桥接节点）：介数中心性高
- Influencers（影响者）：特征向量中心性高

详见：`references/node-classification.md`

### 第四步：中心性比较分析

使用比较工具分析不同中心性指标的关系：
```bash
python scripts/compare_centralities.py --input centrality_measures.json --output comparison_report.json
```

**比较维度**：
- 相关性分析
- 排名差异
- 一致性检验

详见：`references/centrality-comparison.md`

### 第五步：结果解释

结合社会背景解释中心性结果：
- 识别权力结构
- 分析信息流动
- 理解网络功能

详见：`references/social-interpretation.md`

## 输出格式

统一的三层JSON格式：

```json
{
  "summary": {
    "total_nodes": 50,
    "total_edges": 120,
    "network_density": 0.098,
    "top_node": "节点A",
    "hubs_count": 5,
    "bridges_count": 3,
    "influencers_count": 4
  },
  "details": {
    "centralities": {
      "degree": [...],
      "closeness": [...],
      "betweenness": [...],
      "eigenvector": [...]
    },
    "top_nodes": [...],
    "key_nodes": {
      "hubs": [...],
      "bridges": [...],
      "influencers": [...]
    }
  },
  "metadata": {
    "timestamp": "2025-12-21T10:30:00",
    "version": "1.0.0"
  }
}
```

详见：`references/output-format.md`

## 质量检查清单

在完成中心性分析后，请检查以下项目：

- [ ] 网络数据格式正确，节点边信息完整
- [ ] 所有4种中心性指标计算正确
- [ ] 关键节点识别合理（hubs/bridges/influencers）
- [ ] 结果解释准确，考虑中国"关系"网络特点
- [ ] 可视化清晰，突出关键节点

详见：`references/quality-checklist.md`

## 深入学习

- **中心性理论**：`references/centrality-theory.md` - 公式和算法
- **中国社会网络**：`references/chinese-network-characteristics.md` - 关系网络特点
- **实践案例**：`references/case-studies.md` - 完整分析案例
- **故障排除**：`references/troubleshooting.md` - 问题诊断

## 完成标志

完成高质量的中心性分析应该：
1. 提供准确的四种中心性指标
2. 深入解释各种中心性的含义
3. 识别网络中的关键节点
4. 给出符合中文语境的解释和建议

---

*此技能为中文社会科学研究提供全面的网络中心性分析支持，帮助研究者深入理解网络结构和权力关系。*