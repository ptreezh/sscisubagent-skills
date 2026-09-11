# 时间序列SNA分析 - 子Agent并行示例

**使用子Agent并行分析多个时间点的社会网络演化**

---

## 📋 场景描述

**任务**: 分析20个时间点的科研合作网络演化

**时间点**: 2000-2019，每年一个时间点

**数据**: `data/temporal_networks/year_*.csv`

---

## 🚀 两种执行方式对比

### 方式A: CLI任务队列（串行）

```yaml
用户请求: "分析2000-2019年的科研合作网络演化"

系统行为:
  模式: CLI队列（自动选择？不，时间点太多应使用并行）

  执行流程:
    Task 1: 分析year_2000.csv (15分钟)
    Task 2: 分析year_2001.csv (15分钟)
    ...
    Task 20: 分析year_2019.csv (15分钟)

  总时间: 300分钟（5小时）

  用户看到:
    ✅ 正在分析 year_2000.csv...
    ✅ 正在分析 year_2001.csv...
    ...
    ✅ 完成！总时间: 5小时
```

### 方式B: 子Agent并行（推荐）

```yaml
用户请求: "分析2000-2019年的科研合作网络演化"

系统行为:
  模式: 子Agent并行（自动选择）

  友好提示:
    ℹ️  检测到时序分析任务（20个时间点）
    ℹ️  将使用并行处理以提升效率
    ℹ️  预计时间: 约20分钟（而非5小时）
    ℹ️  加速比: 15x ⚡

  执行流程:
    启动20个sna-analyzer子Agent
    ├── 子Agent1: 分析year_2000.csv
    ├── 子Agent2: 分析year_2001.csv
    ├── ...
    └── 子Agent20: 分析year_2019.csv

    所有子Agent并行执行 ⚡

  总时间: 20分钟
  加速比: 15x ⚡

  用户看到:
    ✅ 正在并行处理20个时间点...
    ✅ year_2000.csv 完成 ✅
    ✅ year_2001.csv 完成 ✅
    ...
    ✅ 所有时间点完成！总时间: 20分钟
    ✅ 加速: 15x ⚡
```

---

## 📊 分析结果示例

### 每个时间点的分析

```json
{
  "time_point": "year_2010",
  "nodes": 156,
  "edges": 342,
  "density": 0.028,

  "centrality": {
    "top_nodes": [
      {"node": "Researcher_A", "degree": 18, "betweenness": 245},
      {"node": "Researcher_B", "degree": 15, "betweenness": 189},
      {"node": "Researcher_C", "degree": 12, "betweenness": 156}
    ]
  },

  "communities": {
    "modularity": 0.34,
    "num_communities": 6,
    "largest_community_size": 28
  },

  "structural_holes": {
    "brokerage_nodes": [
      {"node": "Researcher_D", "constraint": 0.23}
    ]
  }
}
```

### 整合的演化分析

```json
{
  "analysis_type": "temporal_sna",
  "time_points": 20,
  "time_range": "2000-2019",

  "network_growth": {
    "nodes": [120, 125, 130, ..., 156],
    "edges": [245, 256, 268, ..., 342],
    "density": [0.034, 0.033, 0.032, ..., 0.028]
  },

  "key_findings": {
    "growth_pattern": "稳定增长",
    "centralization_trend": "下降（网络去中心化）",
    "community_evolution": "社群数量增加，规模缩小"
  },

  "dominant_players": {
    "persistent": ["Researcher_A", "Researcher_B"],
    "emerging": ["Researcher_X", "Researcher_Y"],
    "declining": ["Researcher_Z"]
  },

  "structural_evolution": {
    "brokerage_trend": "经纪能力增强",
    "bridging_trend": "桥接节点增多",
    "clustering_trend": "聚类系数稳定"
  }
}
```

---

## 🎯 使用方式

### 自动模式（推荐）

```
你: "分析data/temporal_networks/下所有年份的网络演化"

系统:
  - 检测到20个时间点文件
  - 自动选择子Agent并行模式
  - 显示友好提示
  - 20分钟后完成演化分析
```

### 手动指定

```
你: "使用子Agent并行分析这20个时间点的网络"

系统:
  - 强制使用子Agent并行
  - 20分钟后完成
```

---

## ✅ 完成后的下一步

演化分析完成后，可以进一步：

```yaml
阶段2: 演化模式识别
  - 识别关键演化事件
  - 分析结构变化
  - 预测未来趋势

阶段3: 可视化
  - 绘制演化图
  - 动画展示网络变化
  - 交互式可视化

阶段4: 报告生成
  - 生成演化分析报告
  - 识别关键洞察
  - 提供政策建议
```

---

## 💡 关键洞察

### 1. 并行分析的优势

```yaml
传统方式（CLI队列）:
  - 依次分析每个时间点
  - 总时间: 5小时
  - 优点: 简单
  - 缺点: 慢

并行方式（子Agent）:
  - 同时分析所有时间点
  - 总时间: 20分钟
  - 优点: 快（15x加速）
  - 缺点: 无
```

### 2. 时序分析的特殊性

```yaml
时序SNA的特点:
  ✅ 时间点相互独立
  ✅ 每个时间点分析相同
  ✅ 结果可以并行整合
  ✅ 最适合子Agent并行

不适合的场景:
  ❌ 单个网络分析
  ❌ 复杂的动态网络模型
  ❌ 需要迭代的分析
```

### 3. 降级保证

```yaml
如果子Agent不可用:
  → 自动降级到CLI队列
  → 依次分析每个时间点
  → 所有分析都能完成
  → 只是时间更长（5小时 vs 20分钟）

用户知道:
  ℹ️  "子Agent不可用，使用CLI队列模式"
  ℹ️  "预计时间: 5小时"
```

---

## 🎉 总结

**使用子Agent进行时序SNA分析**:
- ⚡ 15x加速（20个时间点：5小时→20分钟）
- ✅ 自动演化模式识别
- 🎯 关键事件检测
- 🛡️ 优雅降级保证
- 💡 用户友好提示

**时序SNA分析的最佳选择！** ⚡
