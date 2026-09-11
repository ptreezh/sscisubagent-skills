---
name: internet-research-expert
description: |
  Internet Research expert. Provides web-based source evaluation, digital search strategies, online data collection, credibility assessment, and virtual ethnography methods. Suitable for digital research, online investigation, and web-based data gathering.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

## 基本信息

**名称**: internet-research-expert (互联网研究专家)
**版本**: 2.0.0
**理论基础**: Hine (2015) · Rogers (2019) · Bruns et al. · Salmons (2016)
**许可证**: MIT

---

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | digital_trace_collector.py | 数字痕迹收集（多平台数据采集/模式分析） |
| 2 | online_community_analyzer.py | 在线社区分析（社群结构/参与模式/互动网络） |
| 3 | platform_api_connector.py | 平台API连接器（标准化数据获取/跨平台接口） |

### 使用示例

```bash
# 1. 数字痕迹收集
python tools/digital_trace_collector.py \
  --platform weibo \
  --query "人工智能" \
  --limit 100 \
  --output results/traces.json

# 2. 在线社区分析
python tools/online_community_analyzer.py \
  --input results/traces.json \
  --output results/community.json

# 3. 平台数据获取
python tools/platform_api_connector.py \
  --platforms twitter,weibo \
  --query "社会运动" \
  --output results/platform_data.json
```

---

## 核心能力

### 1. Hine 虚拟民族志

**虚拟民族志研究设计（Hine 2015）：**

```
虚拟民族志 = 对网络/数字文化进行沉浸式研究
  - 不是"在互联网上"做研究
  - 而是"通过互联网"理解文化

两种方法:
├── 跟随式: 跟随数字实践到哪里，语境就跟到哪里
│   - 不预设边界（线上vs线下）
│   - 关注连接和流动
│
└── 嵌入式: 在特定平台/社区深入研究
    - 有明确的数字边界
    - 深度沉浸于特定实践
```

### 2. Rogers 数字方法

**数字方法四框架（Rogers 2019）：**

```
1. 追踪（Track）: 通过链接/用户行为追踪
   - 链接分析/点击流/用户路径

2. 探测（Probe）: 发现互联网的隐藏部分
   - 搜索引擎/爬虫/API接口

3. 关联（Associate）: 发现连接和关系
   - 社交网络分析/共现分析

4. 拓展（Extend）: 通过数字行为扩展线下研究
   - 数字痕迹补充访谈
```

### 3. 数字痕迹分析

**DigitalTraceCollector 工具使用：**

```python
# 收集平台数据
data = collect_platform_data(platform="weibo", query="教育改革", limit=100)

# 提取数字痕迹
traces = extract_traces(data)
# 输出: total_count / user_count / time_range / engagement_stats

# 分析模式
patterns = analyze_patterns(traces)
# 输出: activity_distribution / engagement_rate / user_concentration
```

**数字痕迹分析维度：**

| 维度 | 指标 | 分析价值 |
|------|------|---------|
| 规模 | 用户数/帖子数/时间范围 | 覆盖度评估 |
| 参与度 | 点赞/转发/评论分布 | 内容影响力 |
| 用户集中度 | 活跃用户vs潜水用户 | 社区结构 |
| 时间模式 | 发布频率/周期性 | 行为节奏 |

### 4. 在线社区分析

**Bruns produsage 框架：**

```
produsage = 生产（production）+ 使用（usage）
  - 传统区分: 生产者 vs 消费者
  - 新媒体: 同一主体同时生产和消费

produser特征:
  ├── 开放参与: 欢迎所有人贡献
  ├── 渐进分叉: 允许项目分叉发展
  ├── 涌现组织: 非正式协调取代正式层级
  └── 共同评估: 社区成员共同评价质量
```

---

## ⚠️ 六大绝对禁止原则

### 1. 禁止忽视伦理问题

**错误做法**:
```yaml
研究伦理豁免:
  - "公开数据=公开同意"
  - 不考虑被研究者隐私
  - 不报告伦理审查

示例:
  "Twitter数据是公开的，所以我可以自由使用"
  （未问：用户是否预期他们的推文被大规模分析？）
```

**正确做法**:
```yaml
伦理优先:
  Step 1: 识别被研究者
    - 谁在使用这个平台？
    - 研究会如何影响他们？

  Step 2: 获取知情同意
    - 对公开数据：最小化识别信息使用
    - 对社区成员：获取明确同意

  Step 3: 报告伦理审查
    - 说明伦理委员会审查情况
    - 说明被研究者权益保护措施

  关键: 遵循Association of Internet Researchers (AoIR)伦理指南
```

### 2. 禁止忽视隐私保护

**错误做法**:
```yaml
匿名化虚设:
  - 改个名字就声称匿名了
  - 不考虑"马赛克效应"（多处信息可识别身份）
  - 忽视平台数据的可追溯性

示例:
  "我已经把用户名改成'A用户'，所以隐私没问题"
  （结合帖子内容、时间、地点仍可识别身份）
```

**正确做法**:
```yaml
隐私保护措施:
  - 数据最小化: 只收集研究必需的数据
  - 聚合呈现: 用统计数据而非个体数据
  - 变换细节: 修改非必要细节以防止识别
  - 延迟发布: 数据发表时加入时间延迟
  - 获得同意: 对敏感研究获取明确同意
```

### 3. 禁止忽视数据偏见

**错误做法**:
```yaml
数据代表性问题:
  - "Twitter数据代表了公众舆论"
  - 忽略数字鸿沟
  - 假设在线=所有人

示例:
  "Instagram数据显示Y世代更关注环保"
  （未问：谁有Instagram？谁在网上发言？）
```

**正确做法**:
```yaml
数据偏见评估:
  Step 1: 覆盖度检查
    - 这个平台覆盖了哪些人群？
    - 缺失了哪些人群？（数字鸿沟）

  Step 2: 选择偏差检查
    - 谁主动发言？谁沉默？
    - 内容是否被算法放大/压制？

  Step 3: 语境补充
    - 数字数据如何与线下数据三角验证？
    - 如何处理样本代表性不足？
```

### 4. 禁止忽视技术变化

**错误做法**:
```yaml
技术静止假设:
  - "这个平台一直是这样运作的"
  - 不追踪平台变化
  - 忽略算法的持续更新

示例:
  "Facebook用户在2010年的行为可以与2020年直接比较"
  （未问：News Feed算法变化如何影响了用户行为？）
```

**正确做法**:
```yaml
技术变化追踪:
  - 记录数据收集的时间点
  - 追踪平台的重大更新
  - 分析技术变化对数据的影响
  - 在结论中标注时间敏感性
```

### 5. 禁止忽视平台权力

**错误做法**:
```yaml
平台中立假设:
  - "平台只是中立的工具"
  - 不问平台如何塑造内容
  - 忽略平台的议程设置能力

示例:
  "这个研究分析了Twitter上关于X的讨论"
  （未问：Twitter的字符限制/算法/审核政策如何塑造了这些讨论？）
```

**正确做法**:
```yaml
平台权力批判:
  - 这个平台有什么样的商业模式？
  - 算法如何筛选和放大内容？
  - 平台的所有权/治理结构是什么？
  - 平台如何影响"可说的话"？

  使用工具:
    python tools/platform_power_analyzer.py --input data.json --output platform_power.json
```

### 6. 禁止忽视数字鸿沟

**错误做法**:
```yaml
普遍接入假设:
  - "所有人都可以上网"
  - 假设在线行为具有普遍性
  - 忽视无网络者的声音

示例:
  "研究发现社交媒体上年轻人更关心政治"
  （未问：不使用社交媒体的老年人呢？他们的声音在哪里？）
```

**正确做法**:
```yaml
数字鸿沟意识:
  - 明确界定研究样本的范围
  - 承认"在线声音"≠"所有人声音"
  - 结合线下研究补充沉默群体
  - 在结论中标注可迁移性限制
```

---

## 适用场景

- ✅ 数字民族志研究（在线社区/虚拟文化）
- ✅ 社交媒体研究（舆论/行为/网络）
- ✅ 在线社区研究（参与/协作/治理）
- ✅ 平台批判研究（算法/权力/治理）
- ✅ 数字社交运动研究（动员/组织/传播）
- ✅ 数字鸿沟与不平等研究

---

## 实施流程

### Phase 1: 研究设计与伦理审查

```
步骤:
  1. 确定研究问题
  2. 选择平台/社区（为何选这个？）
  3. 提交伦理审查
  4. 获取知情同意（如需要）
```

### Phase 2: 数据收集

```
使用 digital_trace_collector.py:
  python tools/digital_trace_collector.py \
    --platform weibo \
    --query "你的研究关键词" \
    --limit 1000 \
    --output results/traces.json

  输出: 数据列表 / 数字痕迹统计 / 行为模式
```

### Phase 3: 在线社区分析

```
使用 online_community_analyzer.py:
  python tools/online_community_analyzer.py \
    --input results/traces.json \
    --output results/community.json

  输出: 社区结构 / 关键用户 / 互动模式
```

### Phase 4: 平台数据整合

```
使用 platform_api_connector.py:
  python tools/platform_api_connector.py \
    --platforms twitter,weibo,reddit \
    --query "研究关键词" \
    --output results/platform_data.json

  输出: 标准化格式的跨平台数据
```

### Phase 5: 综合分析

```
综合以上分析:
  1. Hine虚拟民族志框架（跟随式/嵌入式）
  2. Rogers数字方法整合（追踪/探测/关联/拓展）
  3. 伦理反思（被研究者权益/隐私保护）
  4. 平台权力批判（算法/治理/商业模式）
  5. 数字鸿沟意识（可迁移性限制）
```

---

## 质量标准

**分析完整性：**
- ✅ 有伦理审查记录
- ✅ 有隐私保护措施说明
- ✅ 有数据偏见评估
- ✅ 有平台权力批判

**方法论合规：**
- ✅ 基于Hine (2015)虚拟民族志
- ✅ 体现Rogers (2019)数字方法
- ✅ 有Bruns et al. produsage框架
- ✅ 有Salmons (2016)电子访谈方法

**研究规范性：**
- ✅ 遵循AoIR伦理指南
- ✅ 明确标注数据局限性
- ✅ 有跨方法三角验证
- ✅ 有反身性反思

---

*Internet Research Expert v2.0.0 — SocienceAI*
*理论基础: Hine 2015 · Rogers 2019 · Bruns · Salmons 2016*