---
name: bibliometric-analysis-expert
description: |
  Bibliometric analysis expert. Provides citation network analysis, publication trend mapping, co-authorship patterns, h-index calculation, and research impact assessment. Suitable for scientometrics, literature review, and research evaluation.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

-----|----------|------|
| Web of Science | 全球核心期刊 | 引文数据完整 |
| Scopus | 全面学术资源 | 期刊覆盖广 |
| Google Scholar | 全面网络资源 | 免费开放 |
| CNKI | 中文学术资源 | 中文文献全 |

### 数据字段

```
文献记录字段:
├── 标题(Title)
├── 作者(Authors)
├── 摘要(Abstract)
├── 关键词(Keywords)
├── 期刊(Source)
├── 年份(Year)
├── 卷期(Volume, Issue)
├── 页码(Pages)
├── DOI
├── 参考文献(References)
└── 被引次数(Citations)
```

## 描述性分析

### 基础指标

| 指标 | 计算方式 | 含义 |
|------|----------|------|
| 发文量 | 文献计数 | 学术产出规模 |
| 被引次数 | 引用计数 | 学术影响力 |
| 篇均被引 | 总被引/发文量 | 平均影响力 |
| H指数 | h篇≥h次被引 | 持续影响力 |
| 期刊影响因子 | 期刊前两年被引/发文 | 期刊影响力 |

### 时间趋势分析

```
发文量趋势:
年 │
份 │           ████
↑  │       ████████
   │   ████████████
   │ ████████████████
   └─────────────────→ 年份
     2018 2019 2020 2021 2022 2023
```

## 共引分析

### 原理

```
共引关系:
文献A ──→ 被引用 ──→ 文献C
文献B ──→ 被引用 ──→ 文献C

文献A和B的共引强度 = 同时引用A和B的文献数

解读:
- 共引强度高 → 文献研究主题相似
- 聚类分析 → 发现研究群体/主题
```

### 聚类算法

| 算法 | 特点 | 适用场景 |
|------|------|----------|
| VOS聚类 | 基于相似性 | VOSviewer默认 |
| Louvain | 模块度优化 | 大规模网络 |
| Leiden | 改进Louvain | 高质量聚类 |

## 文献耦合

### 原理

```
文献耦合:
文献A ──→ 引用 ──→ 文献X
文献A ──→ 引用 ──→ 文献Y
文献B ──→ 引用 ──→ 文献X
文献B ──→ 引用 ──→ 文献Y

文献A和B的耦合强度 = 共同参考文献数

解读:
- 耦合强度高 → 文献研究方法/主题相似
- 用于发现研究前沿
```

## 作者合作分析

### 合作网络

```
作者合作网络:
      ┌── 作者A ──┐
      │           │
作者C ──┤           ├── 作者B
      │           │
      └── 作者D ──┘

边权重 = 合作发文数
节点大小 = 发文量/被引量
```

### 合作指标

| 指标 | 含义 |
|------|------|
| 合作率 | 合作论文/总论文 |
| 合作广度 | 平均合作人数 |
| 国际合作率 | 国际合作论文比例 |
| 网络中心性 | 在合作网络中的位置 |

## 科学知识图谱

### 图谱类型

| 类型 | 节点 | 边 | 用途 |
|------|------|-----|------|
| 共引图谱 | 文献/作者 | 共引关系 | 发现学科结构 |
| 耦合图谱 | 文献 | 耦合关系 | 发现研究前沿 |
| 合作图谱 | 作者/机构 | 合作关系 | 发现研究团队 |
| 关键词图谱 | 关键词 | 共现关系 | 发现研究主题 |

### VOSviewer可视化

```python
# 从Web of Science导出数据
# 使用VOSviewer创建知识图谱

步骤:
1. 导入文献数据
2. 选择分析类型(共引/耦合/共现)
3. 设定阈值(最小被引/发文量)
4. 聚类分析
5. 可视化调整
```

## 研究前沿识别

### 方法

| 方法 | 原理 | 优势 |
|------|------|------|
| 突发检测 | Kleinberg算法 | 识别新兴热点 |
| 引文突增 | 被引增速 | 发现高影响力文献 |
| 文献耦合聚类 | 前沿主题聚类 | 发现研究群体 |
| 关键词时序分析 | 词频变化 | 追踪主题演变 |

### 突发词检测

```
突发词检测:
词频
  │
  │     ████
  │  ████  ████
  │██          ████
  └────────────────→ 时间
    开始  结束

突发强度 = 词频突增幅度
突发持续时间 = 热点周期
```

## 引文分析指标

### 期刊指标

| 指标 | 公式 | 含义 |
|------|------|------|
| 影响因子(IF) | 前两年被引/发文 | 期刊平均影响力 |
| 5年影响因子 | 前5年被引/发文 | 长期影响力 |
| 即年指数 | 当年被引/发文 | 时效性 |
| SJR | 基于PageRank | 声誉加权影响 |
| SNIP | 标准化影响因子 | 领域可比 |

### 作者指标

| 指标 | 公式 | 含义 |
|------|------|------|
| H指数 | h篇≥h次被引 | 持续影响力 |
| G指数 | 引文累计平方根 | 高被引加权 |
| i10指数 | ≥10次被引论文数 | 高影响力产出 |
| M指数 | H指数/学术年龄 | 年均产出效率 |

## 软件工具

| 工具 | 功能 | 特点 |
|------|------|------|
| VOSviewer | 可视化分析 | 免费、易用 |
| CiteSpace | 时序分析 | 突发检测 |
| BibExcel | 数据处理 | 灵活 |
| bibliometrix(R) | 全面分析 | 编程灵活 |
| CitNetExplorer | 引文网络 | 网络分析 |

## 使用示例

```
用户: 分析人工智能在教育领域的研究热点

AI: 我将执行完整的文献计量分析：

## 数据概况
- 数据库: Web of Science
- 检索式: TS=("artificial intelligence" OR "AI" OR "machine learning") 
          AND TS=("education" OR "learning")
- 时间范围: 2018-2023
- 文献量: 5,234篇

## 描述性分析
| 年份 | 发文量 | 增长率 |
|------|--------|--------|
| 2018 | 456    | -      |
| 2019 | 582    | 28%    |
| 2020 | 789    | 36%    |
| 2021 | 1023   | 30%    |
| 2022 | 1245   | 22%    |
| 2023 | 1139   | -8%    |

## 研究热点(关键词聚类)
聚类1(35%): 个性化学习
  - adaptive learning, personalization, learner modeling

聚类2(28%): 智能教学系统
  - intelligent tutoring, chatbot, virtual assistant

聚类3(22%): 学习分析
  - learning analytics, prediction, early warning

聚类4(15%): 自动评估
  - automated scoring, essay evaluation, feedback

## 高被引文献(Top 5)
1. Holmes et al. (2019) - AI in Education: 856次
2. Luckin et al. (2020) - AI for Good Education: 623次
3. Zawacki-Richter et al. (2019) - AI in HE: 512次

## 研究前沿(突发检测)
- generative AI (2022-2023, 强度: 8.5)
- ChatGPT (2023, 强度: 15.2)
- large language model (2023, 强度: 12.1)
```

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | co_citation_analyzer.py | 共引分析，构建文献共引网络并聚类 |
| 2 | keyword_cooccurrence.py | 关键词共现分析，识别研究热点主题 |
| 3 | author_network.py | 作者合作网络分析，评估学术影响力 |

### CLI用法

```bash
python tools/co_citation_analyzer.py --input papers.json --output citations
python tools/keyword_cooccurrence.py --input abstracts.csv --min-freq 5
python tools/author_network.py --input authors.json --visualize
```

## 🚫 绝对禁止原则

> **使用前必读**：以下原则是不可逾越的红线，违反将导致文献计量分析结论失效。

1. **禁止脱离数据来源空谈结论** — 未明确说明数据来源（WoS/Scopus/CNKI）即进行指标计算，导致结果无法验证和复现
2. **禁止忽视数据清洗** — 跳过去重、标准化、字段补全等清洗步骤，导致计数偏差和虚假关联
3. **禁止只看单一指标** — 仅凭发文量或被引量下结论，忽略H指数、期刊影响因子等多维指标综合评估
4. **禁止混淆相关与因果** — 将共引关系、共现关系解读为因果关系，误导学科发展判断
5. **禁止忽视时间维度** — 将历史文献与近期文献同等对待，忽略引文网络的时间衰减效应
6. **禁止脱离领域语境** — 机械套用通用阈值（如H指数≥5）而不考虑学科差异，导致学科内不公平比较

## ✅ 质量标准

### 完整性
- 必做项清单完成度 ≥ 90%
- 数据来源说明完整（数据库、时间范围、检索式）
- 分析步骤可追溯

### 方法论
- 理论框架与数据一致性 ≥ 90%
- 分析步骤可复现性高
- 指标选择有学科依据

### 深度
- 核心维度覆盖 ≥ 80%
- 多指标综合评估
- 历史演变分析

## 参考文献

1. van Eck, N.J., & Waltman, L. (2014). Visualizing bibliometric networks. In *Measuring Scholarly Impact*, 285-320.
2. Donthu, N., et al. (2021). How to conduct a bibliometric analysis. *International Journal of Research in Marketing*, 38(2), 285-309.
3. Chen, C. (2006). CiteSpace II: Detecting and visualizing emerging trends. *JASIST*, 57(3), 359-377.
4. Aria, M., & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive science mapping analysis. *Journal of Informetrics*, 11(4), 959-975.

---

**技能版本**: 5.0.0  
**方法论标准**: van Eck & Waltman (2014)  
**创建时间**: 2026-03-15