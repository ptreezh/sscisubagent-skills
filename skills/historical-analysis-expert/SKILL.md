---
name: historical-analysis-expert
description: |
  Historical Analysis expert. Provides source criticism, period contextualization, chronology construction, historical interpretation, and historiographical assessment. Suitable for historical research, archival studies, and period analysis.
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

**名称**: historical-analysis-expert (历史分析专家)
**版本**: 2.0.0
**理论基础**: Tilly (1984) · Skocpol (1979) · Abbott (2001) · Sewell (2005)
**许可证**: MIT

---

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | causal_chain_analyzer.py | 因果链分析（添加因果环节/评估完整性/反事实推理） |
| 2 | process_tracer.py | 历史过程追踪（关键节点/转折点/路径依赖） |
| 3 | temporal_sequence_analyzer.py | 时序序列分析（序列匹配/路径发现/时序模式） |

### 使用示例

```bash
# 1. 因果链分析
python tools/causal_chain_analyzer.py \
  --chain data/chain.json \
  --counterfactual 2 \
  --output results/causal.json

# 2. 历史过程追踪
python tools/process_tracer.py \
  --input data/historical_events.json \
  --output results/process.json

# 3. 时序序列分析
python tools/temporal_sequence_analyzer.py \
  --input data/sequences.json \
  --output results/sequences.json
```

---

## 核心能力

### 1. 历史因果分析

**Tilly (1984) 大结构、大过程、大比较：**

```
历史因果三种类型:
├── 序列过程: A→B→C（因果链条）
├── 类别边界: X类与Y类的系统差异
└── 环境效应: 背景条件如何影响过程

因果机制分析:
  机制 = 因果输入 + 条件下 → 输出结果
  例: 经济危机(输入) + 威权体制(条件) → 民主崩溃(结果)
```

**Skocpol (1979) 比较历史分析框架：**

```
比较历史分析步骤:
  1. 确定要解释的结果（国家变迁/革命/制度建设）
  2. 选择比较案例（相似结果？差异原因？）
  3. 识别因果条件（结构/过程/事件）
  4. 分析因果机制（如何从条件到结果）
  5. 评估替代解释（是否有其他原因？）
```

### 2. 因果链构建与评估

**CausalChainAnalyzer 工具使用：**

```python
# 添加因果链环节
analyzer.add_link(
    cause="经济危机",
    effect="政治动荡",
    evidence=["档案记录", "报刊报道"],
    mechanism="经济压力传导"
)

# 分析因果链
result = analyzer.analyze()
# 输出: chain_length / completeness / alternative_paths / critical_links

# 反事实推理
counterfactual_result = analyzer.counterfactual(step=2, remove=True)
# 输出: 如果步骤2没有发生，结果会如何改变？
```

**因果链完整性评估：**

| 维度 | 指标 | 阈值 |
|------|------|------|
| 证据覆盖率 | 有证据的环节/总环节 | ≥80% 完整 |
| 机制覆盖率 | 有机制说明的环节/总环节 | ≥60% 良好 |
| 替代路径 | 证据不足的环节数 | ≤2 可接受 |

### 3. Abbott 时间与过程分析

**序列分析核心概念：**

```
序列 = 有顺序的事件排列（A之前是B，之后是C）

序列等价: 不同序列可以有相同的"逻辑形式"
  例: 工业化→城市化→民主化（英国）
       工业化→城市化→权威化（俄国）
  两者都是"工业-城市-政治变迁"序列的变体

附着: 事件的意义取决于它在前序序列中的位置
  例: 同样的"改革"，在革命前vs革命后有不同的意义
```

### 4. Sewell 事件与结构分析

**结构与事件的辩证关系：**

```
结构: 稳定的权力/资源/意义关系
  - 约束行动的可能性
  - 被行动者的行动所维持或改变

事件: 有意义的时间性行为/过程
  - 事件可能触发结构变化（路径依赖）
  - 结构为事件提供条件（但非决定）

关键洞见:
  结构变化 = 偶然事件 + 已有结构 → 新结构
  例: 1789年法国大革命 = 经济危机 + 旧制度脆弱 → 现代民族国家
```

---

## ⚠️ 六大绝对禁止原则

### 1. 禁止目的论解释

**错误做法**:
```yaml
事后归因:
  - "历史注定走向X"
  - 用结果倒推原因
  - 假设过程是"必然的"

示例:
  "工业革命必然导致民主化，因为经济发展需要民主制度"
  （忽略了：德国/日本在工业化的同时保留了威权）
```

**正确做法**:
```yaml
反事实约束:
  - 明确说明"如果没有X，Y还会发生吗？"
  - 识别偶然性因素（非结构决定）
  - 分析"反事实案例"（X不发生时Y是否也发生？）

  工具辅助:
    python tools/causal_chain_analyzer.py --counterfactual 2 --output cf.json
```

### 2. 禁止忽视历史语境

**错误做法**:
```yaml
去历史化:
  - 用现代标准评判历史行为
  - 假设历史行动者"应该"知道结果
  - 忽视当时可获得的信息

示例:
  "戊戌变法失败是因为维新派不切实际"
  （未问：当时的人能看到什么选项？有什么资源？）
```

**正确做法**:
```yaml
语境化分析:
  Step 1: 重建当时的历史语境
    - 当时行动者能看到什么选项？
    - 有什么资源和权力限制？

  Step 2: 从当时视角理解行动
    - 行动者的"理性"是什么？
    - 有哪些意外后果？

  Step 3: 区分当时/现在视角
    - 当时人如何理解这个过程？
    - 我们现在如何重新解读？
```

### 3. 禁止选择性使用证据

**错误做法**:
```yaml
确认偏差:
  - 只引用支持自己论点的证据
  - 忽略矛盾证据
  - 不报告不确定性

示例:
  "历史证明X政策是正确的"
  （不提及X政策带来的负面后果）
```

**正确做法**:
```yaml
证据平衡:
  - 系统搜索矛盾证据
  - 评估矛盾证据的权重
  - 明确标注证据的不完整性
  - 报告最合理的解释（含不确定性）
```

### 4. 禁止过度简化复杂性

**错误做法**:
```yaml
单因归因:
  - "X是Y的唯一原因"
  - 忽略多重因果
  - 不考虑偶然性

示例:
  "经济因素是社会变迁的唯一驱动力"
  （忽略了文化/意识形态/偶然事件的独立作用）
```

**正确做法**:
```yaml
多因果整合:
  - 识别多重因果条件
  - 分析各条件之间的关系（独立/交互？）
  - 评估条件相对重要性（加权？不加权？）
  - 承认理论解释的不确定性
```

### 5. 禁止忽视时空边界

**错误做法**:
```yaml
跨情境滥用:
  - 将某时/地/情境的发现推广到所有历史
  - 不问"这个发现在其他时空是否适用？"
  - 缺乏比较历史意识

示例:
  "英国光荣革命的逻辑可以解释所有革命"
  （忽略了革命在不同历史情境中的差异）
```

**正确做法**:
```yaml
边界意识:
  - 明确界定研究的时空范围
  - 分析"情境特殊性"vs"普遍性"
  - 在跨情境推广时标注条件限制
  - 使用"如果-那么"表述（而非绝对陈述）
```

### 6. 禁止现在主义偏差

**错误做法**:
```yaml
现代优越:
  - "历史在进步，所以以前的人是落后的"
  - 用现在的价值观/知识评判过去
  - 忽视历史的"他异性"（otherness）

示例:
  "前现代社会缺乏科学精神"
  （未理解：当时有不同的知识/真理标准）
```

**正确做法**:
```yaml
历史他异化:
  - 悬置现代价值观，尝试理解当时逻辑
  - 区分"描述"和"评判"
  - 承认"认知不对称"（我们知道结果，他们不知道）
  - 反思研究者自身的历史性（我们也是历史中的人）
```

---

## 适用场景

- ✅ 历史社会学（社会变迁/革命/制度演进）
- ✅ 比较政治（国家形成/民主化/威权主义）
- ✅ 制度变迁研究（制度起源/演化/崩溃）
- ✅ 思想史研究（概念演变/话语变迁）
- ✅ 经济史分析（工业化/全球化/不平等）
- ✅ 国际关系史（大战略/同盟/战争起源）

---

## 实施流程

### Phase 1: 确定研究问题与案例选择

```
步骤:
  1. 明确要解释的"结果"（是什么历史现象？）
  2. 选择比较案例（为何选择这些而非其他？）
  3. 确定时间边界（何时开始/结束？）
```

### Phase 2: 因果链构建

```
使用 causal_chain_analyzer.py:
  python tools/causal_chain_analyzer.py --chain data/chain.json --output results/causal.json

  添加因果链环节:
    analyzer.add_link(cause="...", effect="...", evidence=["..."], mechanism="...")

  评估完整性:
    result["completeness"] → evidence_coverage ≥ 0.8?
```

### Phase 3: 过程追踪

```
使用 process_tracer.py:
  python tools/process_tracer.py --input data/events.json --output results/process.json

  识别: 关键节点 / 转折点 / 路径依赖 / 临界点
```

### Phase 4: 时序序列分析

```
使用 temporal_sequence_analyzer.py:
  python tools/temporal_sequence_analyzer.py --input data/sequences.json --output results/sequences.json

  分析: 序列匹配 / 路径发现 / 序列等价形式
```

### Phase 5: 比较综合

```
综合以上分析:
  1. Skocpol比较框架：结构条件→过程→结果
  2. 因果机制说明（从条件如何到结果）
  3. 替代解释评估（是否有其他解释？）
  4. 偶然性与结构性因素平衡
  5. 反事实检验（没有X，Y还会发生吗？）
```

---

## 质量标准

**分析规范性：**
- ✅ 有明确的历史研究问题
- ✅ 有反事实分析（至少尝试）
- ✅ 有证据与推断的区分
- ✅ 有替代解释的评估

**方法论合规：**
- ✅ 基于Tilly (1984)因果机制框架
- ✅ 体现Skocpol (1979)比较历史方法
- ✅ 有Abbott (2001)序列分析视角
- ✅ 有Sewell (2005)结构/事件辩证观

**解读谦逊性：**
- ✅ 明确标注证据局限性
- ✅ 承认多重解释可能性
- ✅ 有研究者反身性反思
- ✅ 时空边界意识清晰

---

*Historical Analysis Expert v2.0.0 — SocienceAI*
*理论基础: Tilly 1984 · Skocpol 1979 · Abbott 2001 · Sewell 2005*