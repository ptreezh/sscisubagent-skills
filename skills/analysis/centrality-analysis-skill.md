---
name: performing-centrality-analysis
description: 执行社会网络中心性分析，包括度中心性、接近中心性、介数中心性和特征向量中心性的计算和解释。当需要识别网络中的关键节点、权力中心或信息枢纽时使用此技能。
---

# 网络中心性分析技能

## 🎯 核心目标（最高优先级）
识别网络中的关键节点，为中文社会科学研究提供网络结构和权力关系的量化分析。

## 📋 必须首先掌握的核心概念

### 1. 中心性的本质含义
**最重要概念**：中心性衡量节点在网络中的重要程度和影响力。

### 2. 四种基本中心性类型
**必须区分**：
- **度中心性**：直接连接数量（社交活跃度）
- **接近中心性**：到达其他节点的容易程度（信息传播效率）
- **介数中心性**：在最短路径中的出现频率（桥梁作用）
- **特征向量中心性**：连接重要节点的程度（间接影响力）

### 3. 中文语境特殊含义
**必须考虑**：
- **关系强度**：中国社会的"关系"概念
- **权力距离**：中文化背景下的权力结构
- **集体主义**：个人与集体的关系

## 🔄 动态知识库加载

### 启动时加载
```
/knowledge-base/main-knowledge.md
/knowledge-base/core-concepts.md
```

### 按需加载
```
用户提及权力 → /knowledge-base/power-structures.md
用户提及信息 → /knowledge-base/information-flow.md
用户提及组织 → /knowledge-base/organizational-theory.md
```

## 🚨 紧急处理协议

### 红色警报（论文截止）
**快速分析模式**：
1. 仅计算最关键的1-2种中心性
2. 提供可视化图表
3. 给出简洁解释
4. 承诺后续补充

### 黄色警报（导师要求）
**标准分析模式**：
1. 计算全部四种中心性
2. 提供详细解释
3. 生成对比分析
4. 给出实践建议

## 🛠️ 核心分析技能

### 1. 度中心性分析
**Python实现**：
```python
import networkx as nx
import numpy as np

def calculate_degree_centrality(network_data):
    """计算度中心性"""
    G = nx.from_numpy_array(network_data['adjacency_matrix'])
    
    # 标准化度中心性
    degree_centrality = nx.degree_centrality(G)
    
    # 识别关键节点（前20%）
    threshold = np.percentile(list(degree_centrality.values()), 80)
    key_nodes = {node: centrality for node, centrality 
                in degree_centrality.items() if centrality >= threshold}
    
    return {
        'all_centrality': degree_centrality,
        'key_nodes': key_nodes,
        'interpretation': interpret_degree_centrality(key_nodes)
    }

def interpret_degree_centrality(key_nodes):
    """解释度中心性在中文语境下的含义"""
    interpretation = []
    
    for node, centrality in key_nodes.items():
        if centrality > 0.7:
            interpretation.append(f"{node}是网络中的'明星节点'，具有强大的社交影响力")
        elif centrality > 0.5:
            interpretation.append(f"{node}是网络中的活跃分子，具有较强的连接能力")
        else:
            interpretation.append(f"{node}在网络中具有一定的影响力")
    
    return interpretation
```

### 2. 介数中心性分析
**关键应用**：
- 识别网络中的"桥梁人物"
- 发现信息传播的关键节点
- 分析组织中的权力中介

```python
def analyze_betweenness_centrality(G, chinese_context=True):
    """分析介数中心性"""
    betweenness = nx.betweenness_centrality(G)
    
    if chinese_context:
        return interpret_betweenness_chinese(betweenness)
    else:
        return {'betweenness': betweenness}

def interpret_betweenness_chinese(betweenness):
    """中文语境下的介数中心性解释"""
    results = {
        'bridge_roles': [],
        'information_gates': [],
        'power_brokers': []
    }
    
    # 识别桥梁角色
    threshold = np.percentile(list(betweenness.values()), 85)
    for node, centrality in betweenness.items():
        if centrality >= threshold:
            results['bridge_roles'].append({
                'node': node,
                'role': '桥梁人物',
                'function': '连接不同子群体的关键节点',
                'centrality': centrality
            })
    
    return results
```

### 3. 综合中心性分析
**多维分析框架**：
```python
def comprehensive_centrality_analysis(network_data):
    """综合中心性分析"""
    G = nx.from_numpy_array(network_data['adjacency_matrix'])
    
    # 计算所有中心性指标
    centralities = {
        'degree': nx.degree_centrality(G),
        'closeness': nx.closeness_centrality(G),
        'betweenness': nx.betweenness_centrality(G),
        'eigenvector': nx.eigenvector_centrality(G)
    }
    
    # 识别全能型节点（各项中心性都较高）
    all_rounder_nodes = identify_all_rounder_nodes(centralities)
    
    # 识别专业化节点（某项中心性突出）
    specialist_nodes = identify_specialist_nodes(centralities)
    
    return {
        'centralities': centralities,
        'all_rounder_nodes': all_rounder_nodes,
        'specialist_nodes': specialist_nodes,
        'network_structure': analyze_network_structure(centralities)
    }

def identify_all_rounder_nodes(centralities):
    """识别全能型节点"""
    all_rounder = []
    
    for node in centralities['degree'].keys():
        scores = [centralities[ctype][node] for ctype in centralities]
        if all(score > 0.5 for score in scores):
            all_rounder.append({
                'node': node,
                'scores': scores,
                'type': '全能型节点',
                'characteristics': '在各方面都具有较强影响力'
            })
    
    return all_rounder
```

## 📊 质量检查清单

### 数据质量检查
- [ ] 网络数据是否完整
- [ ] 节点编号是否一致
- [ ] 关系权重是否合理
- [ ] 是否存在孤立节点

### 分析质量检查
- [ ] 中心性计算是否准确
- [ ] 结果解释是否符合中文语境
- [ ] 可视化图表是否清晰
- [ ] 实践建议是否具体可行

### 紧急任务检查
- [ ] 是否在规定时间内完成
- [ ] 核心问题是否回答
- [ ] 关键发现是否突出
- [ ] 后续支持是否明确

## 💡 快速响应模板

### 紧急分析模板
```
1. 快速计算度中心性（最重要）
2. 识别前5个关键节点
3. 生成简洁的网络图
4. 提供核心发现总结
5. 承诺24小时内补充详细分析
```

### 标准分析模板
```
1. 计算全部四种中心性
2. 进行综合对比分析
3. 识别不同类型的关键节点
4. 提供中文语境下的解释
5. 给出具体的应用建议
```

---

**使用说明**：此技能严格遵循渐进式信息披露，优先处理紧急任务，确保核心分析结果的及时交付。