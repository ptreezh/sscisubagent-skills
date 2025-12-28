---
name: network-computation-expert
description: 社会网络计算专家分析技能，整合网络数据处理、网络构建、中心性分析、社区检测和网络可视化功能，提供全面的网络分析框架
version: 1.0.0
author: socienceAI.com
license: MIT
tags: [network-analysis, social-networks, centrality, community-detection, visualization, network-computation]
compatibility: Claude 3.5 Sonnet and above
metadata:
  domain: social-network-analysis
  methodology: network-analysis
  complexity: advanced
  integration_type: analysis_tool
  last_updated: "2025-12-27"
allowed-tools: [python, bash, read_file, write_file]
---

# 社会网络计算专家分析技能 (Network Computation Expert Analysis)

## 概述

社会网络计算专家分析技能整合了网络数据处理、网络构建、中心性分析、社区检测和网络可视化功能，为社会科学研究提供全面的网络分析框架。该技能帮助研究者从原始数据到网络分析结果的全流程处理。

## 使用时机

当用户请求以下分析时使用此技能：
- 社会网络关系的全面分析
- 从原始数据到网络分析的全流程处理
- 网络数据处理、构建、分析和可视化的连续分析
- 网络中心性、社区结构和动态变化的系统分析
- 中文社会网络数据的网络分析

## 快速开始

当用户请求网络分析时：
1. **数据处理**: 清洗和验证网络数据
2. **网络构建**: 从关系数据构建网络
3. **中心性分析**: 计算节点重要性指标
4. **社区检测**: 识别网络中的群组结构
5. **可视化**: 生成网络图和分析图表

## 核心功能（渐进式披露）

### 主要功能
- **网络数据处理**: 从原始数据提取关系信息
- **网络构建**: 构建标准化网络格式
- **中心性分析**: 计算节点重要性指标
- **社区检测**: 识别网络中的群组结构

### 次要功能
- **网络指标计算**: 计算网络基本指标
- **网络可视化**: 生成网络图和分析图表
- **质量检查**: 网络分析的质量控制
- **属性分析**: 节点和边属性的分析

### 高级功能
- **多层网络分析**: 处理多重或多元网络
- **动态网络分析**: 分析网络随时间的变化
- **二模网络分析**: 处理二分网络结构
- **高级布局算法**: 使用专门的布局算法

## 详细指令

### 第一阶段：网络数据处理
   - 识别数据源类型（问卷、访谈、观察、数字痕迹）
   - 从原始数据中提取关系信息
   - 清洗和验证提取的关系
   - 标准化数据格式和表示
   - 检查数据完整性

### 第二阶段：网络构建
   - 创建带有适当标识符的节点列表
   - 构建邻接矩阵（二元、加权、有向）
   - 处理不同网络类型（单模、多模）
   - 处理节点和边属性
   - 创建标准化网络格式

### 第三阶段：中心性分析
   - 计算度中心性（节点的直接连接数）
   - 计算接近中心性（到达其他节点的容易程度）
   - 计算介数中心性（在最短路径中的重要性）
   - 计算特征向量中心性（连接到重要节点的程度）
   - 识别关键节点（枢纽、桥梁、影响者）

### 第四阶段：社区检测
   - 应用适当的聚类算法（Louvain、标签传播等）
   - 验证社区结构
   - 分析社区间关系
   - 解释社区在社会背景中的意义

### 第五阶段：网络可视化
   - 创建清晰的信息网络图
   - 使用视觉属性突出重要特征
   - 生成发布质量的图表
   - 提供交互式可视化（如适用）

### 第六阶段：综合分析与解释
   - 整合所有分析维度的发现
   - 将网络分析与更广泛的研究问题联系起来
   - 考虑中国社会背景和文化特殊性
   - 提供可操作的见解

## 参数
- `network_format`: 输入格式 (edgelist, adjacency matrix, JSON等)
- `directed`: 网络是否有向 (默认: false)
- `weighted`: 网络是否加权 (默认: true)
- `centrality_metrics`: 要计算的中心性指标列表
- `community_method`: 社区检测算法
- `visualization_type`: 可视化类型 (静态, 交互式)
- `node_attributes`: 用于可视化的额外节点属性
- `edge_attributes`: 用于可视化的额外边属性
- `methodology`: 分析方法 (定量, 定性, 混合)
- `cultural_context`: 文化背景考虑 (特别是中文研究背景)

## 示例

### 示例 1: 组织网络分析
User: "分析组织内部的沟通网络"
Response: 处理沟通数据，构建网络，计算中心性指标，检测社区结构，生成可视化。

### 示例 2: 社交网络分析
User: "分析社交媒体中的影响力网络"
Response: 提取关系数据，构建网络，识别关键影响者，检测社区，分析传播路径。

### 示例 3: 合作网络分析
User: "分析学术合作网络的结构"
Response: 处理合作数据，构建网络，计算中心性，检测研究群体，分析合作模式。

## 质量标准

- 应用系统化数据处理程序
- 在整个分析过程中维护数据完整性
- 验证关系提取的准确性
- 记录所有处理步骤和决策
- 考虑中国网络数据的文化背景

## 输出格式

```json
{
  "summary": {
    "total_nodes": 50,
    "total_edges": 120,
    "network_density": 0.098,
    "components": 1,
    "avg_path_length": 2.34,
    "diameter": 6,
    "modularity": 0.72,
    "top_centrality_node": "节点A"
  },
  "details": {
    "network_processing": {...},
    "network_construction": {...},
    "centrality_analysis": {...},
    "community_detection": {...},
    "visualization_data": {...}
  },
  "metadata": {
    "timestamp": "2025-12-27T10:30:00",
    "version": "1.0.0"
  }
}
```

## 资源
- 社会网络分析最佳实践
- 网络可视化指南
- 社区检测算法比较
- 中国社会网络特征（关系等）
- Python工具包: `skills/network-computation-expert/scripts/network_analyzer.py`

## 完成标志

完成高质量的网络分析应包括：
1. 生成准确完整的网络指标
2. 识别清晰的社区结构
3. 提供直观的可视化结果
4. 给出深入的分析解释
5. 考虑中国社会背景的特殊性

---

*此技能为社会科学研究提供专业的综合网络分析框架和工具，确保研究的科学性和严谨性。*