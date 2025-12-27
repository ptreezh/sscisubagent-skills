---
name: ant-network-analysis
description: 当用户需要分析行动者网络的结构、动态和稳定性，包括网络拓扑、关系强度、中心性、凝聚力和演化过程时使用此技能
version: 1.0.0
author: chinese-social-sciences-subagents
license: MIT
tags: [actor-network-theory, ANT, network-analysis, topology, stability, dynamics, socio-technical-networks]
compatibility: Claude 3.5 Sonnet and above
metadata:
  domain: science-and-technology-studies
  methodology: actor-network-theory
  complexity: advanced
  integration_type: analysis_tool
  last_updated: "2025-12-21"
allowed-tools: [python, bash, read_file, write_file]
---

# ANT网络分析技能 (ANT Network Analysis)

## 概述

分析行动者网络的结构特征、动态变化和稳定性机制，帮助研究者理解网络的拓扑结构、关系模式、权力分布、稳定化机制以及网络随时间的演化过程。

## 使用时机

当用户请求以下分析时使用此技能：
- 网络拓扑和结构分析
- 关键节点和关键连接识别
- 网络稳定性和鲁棒性评估
- 网络动态和变化过程检查
- 网络凝聚性和碎片化评估
- 网络内权力分布研究
- 网络演化过程追踪
- 网络对干扰的韧性分析

## 快速开始

当用户请求网络分析时：
1. **绘制**网络拓扑和结构
2. **分析**关键关系和连接
3. **识别**中心节点和关键行动者
4. **评估**网络稳定性和脆弱性
5. **追踪**动态变化和演化

## 核心流程

### 第一阶段：网络拓扑映射
   - 创建行动者关系的综合地图
   - 识别行动者之间的连接类型
   - 绘制网络的整体结构
   - 分析连接模式
   - 考虑网络的边界

### 第二阶段：关系分析
   - 评估不同关系的强度
   - 识别连接的性质（支持性、冲突性、中性）
   - 分析关系的方向性
   - 检查连接的质量和持久性
   - 考虑关系的多样性

### 第三阶段：中心性和关键行动者分析
   - 识别网络中的中心行动者
   - 分析关键中介的角色
   - 评估影响力分布
   - 识别潜在瓶颈或脆弱点
   - 考虑连接的冗余性

### 第四阶段：稳定性评估
   - 评估维持网络稳定性的因素
   - 识别不稳定性的潜在来源
   - 评估关键连接的鲁棒性
   - 分析网络稳定化的机制
   - 考虑维持网络连接的成本

### 第五阶段：动态分析
   - 追踪网络结构随时间的变化
   - 识别网络转换的时刻
   - 分析网络变化的原因
   - 评估外部事件对网络的影响
   - 考虑潜在的未来发展

## 输出格式

```json
{
  "summary": {
    "network_type": "socio-technical",
    "node_count": 25,
    "edge_count": 42,
    "network_density": 0.12,
    "stability_score": 0.78
  },
  "details": {
    "topology": {...},
    "relationships": {...},
    "centrality_analysis": {...},
    "stability_assessment": {...},
    "dynamics": {...}
  },
  "metadata": {
    "timestamp": "2025-12-21T10:30:00",
    "version": "1.0.0"
  }
}
```

## 质量标准

- 严格应用网络分析原则
- 考虑结构和动态两个方面
- 评估网络韧性和适应性
- 考虑非人类行动者在网络结构中的作用
- 保持对行动者关系和依赖的关注

## 深入学习

- ANT背景下的网络分析文献
- 社会网络分析方法论
- 复杂系统和网络理论
- 中国背景下网络分析的实例

## 完成标志

完成高质量的ANT网络分析应该：
1. 提供完整的网络拓扑映射
2. 识别关键节点和连接
3. 评估网络稳定性和动态
4. 分析权力分布和影响

---

*此技能为行动者网络理论分析提供专业的网络结构和动态分析支持，确保研究的科学性和严谨性。*