---
name: performing-centrality-analysis
description: 执行社会网络中心性分析，包括度中心性、接近中心性、介数中心性和特征向量中心性的计算和解释。当需要识别网络中的关键节点、权力中心或信息枢纽时使用此技能。
---

# 网络中心性分析技能 (Performing Centrality Analysis)

识别网络中的关键节点，为中文社会科学研究提供网络结构和权力关系的量化分析。

## 使用时机

当用户提到以下需求时，使用此技能：
- "中心性分析" 或 "计算中心性"
- "关键节点识别" 或 "找出重要节点"
- "权力中心" 或 "影响力分析"
- "社会网络分析" 或 "网络结构"
- "信息枢纽" 或 "信息传播"
- 需要量化分析网络中节点的重要性

## 四种中心性类型

| 类型 | 含义 | 应用场景 |
|-----|------|---------|
| **度中心性** | 直接连接数量 | 识别活跃节点 |
| **接近中心性** | 到达其他节点的容易程度 | 识别信息传播效率高的节点 |
| **介数中心性** | 最短路径中出现频率 | 识别桥梁和中介节点 |
| **特征向量中心性** | 连接到重要节点的程度 | 识别具有间接影响力的节点 |

详见：`references/centrality-theory/INDEX.md`

---

## 快速开始

### 工具链

```bash
# 计算所有中心性指标
python scripts/calculate_centrality.py \
  --input network.json \
  --output centrality.json

# 按特定指标排序
python scripts/calculate_centrality.py \
  --input network.json \
  --metric betweenness \
  --top 20

# 识别关键节点
python scripts/identify_key_nodes.py \
  --input centrality.json \
  --output key_nodes.json

# 比较不同中心性
python scripts/compare_centralities.py \
  --input centrality.json \
  --output comparison.json

# 可视化
python scripts/visualize_centrality.py \
  --input network.json \
  --centrality centrality.json \
  --output network_viz.png
```

---

## 核心流程

### 第一步：计算中心性

**使用工具自动计算**：
- 4种中心性一次性计算
- 自动识别关键节点（hubs, bridges, influencers）
- 输出标准化JSON格式

**定性解释**：
- 结合研究问题解释中心性含义
- 考虑中国社会网络的"关系"特点

详见：`references/centrality-theory/INDEX.md`

---

### 第二步：识别关键节点

**使用工具分类**：
- Hubs：度中心性高（≥0.5）
- Bridges：介数中心性高（≥0.1）
- Influencers：特征向量中心性高（≥0.3）

**定性分析**：
- 验证关键节点的实际影响力
- 分析节点角色和功能

详见：`references/examples/INDEX.md`

---

### 第三步：比较和解释

**使用工具对比**：
- 计算不同中心性的相关性
- 识别中心性差异大的节点

**定性解释**：
- 解释为什么某些节点在不同中心性上表现不同
- 结合中国文化背景（关系网络、面子文化）

详见：`references/chinese-context/INDEX.md`

---

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
    "centralities": [...],
    "top_nodes": [...],
    "key_nodes": {...}
  }
}
```

## 质量检查清单

- [ ] 网络数据格式正确，节点边信息完整
- [ ] 所有4种中心性指标计算正确
- [ ] 关键节点识别合理（hubs/bridges/influencers）
- [ ] 结果解释准确，考虑中国"关系"网络特点
- [ ] 可视化清晰，突出关键节点

---

## 常见问题

**快速诊断**：
- 网络规模过大 → 见 `references/troubleshooting/INDEX.md` - 性能优化
- 中心性结果矛盾 → 使用 `compare_centralities.py` 分析差异
- 可视化不清晰 → 见 `references/examples/INDEX.md` - 可视化方法

---

## 深入学习

- **中心性理论**：`references/centrality-theory/INDEX.md` - 公式和算法
- **中国社会网络**：`references/chinese-context/INDEX.md` - 关系网络特点
- **实践案例**：`references/examples/INDEX.md` - 完整分析案例
- **故障排除**：`references/troubleshooting/INDEX.md` - 问题诊断

**问题：中心性分布极不均匀**
- 解决：检查网络结构和数据质量
- 方法：分析网络的基本结构特征

**问题：中文语境下的解释困难**
- 解决：结合中国文化和社会背景
- 策略：使用贴近中文研究者理解的表达方式

## 技术工具建议

**Python库推荐**：
- **NetworkX**：网络分析的核心库
- **Matplotlib/Seaborn**：可视化
- **Pandas**：数据处理
- **NumPy**：数值计算

**其他工具**：
- **Gephi**：交互式网络可视化
- **UCINET**：专业社会网络分析软件
- **R语言的igraph包**：网络分析

## 完成标志

完成高质量的中心性分析应该：
1. 提供准确的四种中心性指标
2. 深入解释各种中心性的含义
3. 识别网络中的关键节点
4. 给出符合中文语境的解释和建议

---

*此技能专为中文社会科学研究设计，提供全面的网络中心性分析支持，帮助研究者深入理解网络结构和权力关系。*