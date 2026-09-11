---
name: discourse-analysis-expert
description: |
  Discourse Analysis expert. Provides text-in-context interpretation, power relation mapping, ideology detection, discourse genre classification, and critical discourse analysis. Suitable for linguistics, media studies, and critical social research.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

---|---------|------|
| 词汇选择 | 用词倾向 | "非法移民"vs"无证移民" |
| 分类系统 | 命名与分类 | 职业称谓的性别化 |
| 价值负载 | 评价性词汇 | 褒贬色彩词 |
| 隐喻 | 概念隐喻 | "疾病即战争" |

### 语法层面
| 维度 | 分析要点 | 功能 |
|------|---------|------|
| 及物性 | 过程类型 | 物质/心理/关系过程 |
| 情态 | 确定性程度 | 认识/道义情态 |
| 转换 | 主动/被动 | 施事隐藏 |
| 名词化 | 过程名词化 | 去历史化 |

### 文本结构
| 维度 | 分析要点 |
|------|---------|
| 体裁结构 | 文本的组织模式 |
| 信息结构 | 已知/新信息分布 |
| 连贯性 | 语义连接 |
| 衔接手段 | 词汇/语法衔接 |

## 话语策略(Wodak)

| 策略 | 定义 | 示例 |
|------|------|------|
| 指称策略 | 社会行动者的命名 | "我们"vs"他们" |
| 谓语策略 | 特质的赋予 | 正面/负面定性 |
| 论证策略 | 论点的正当化 | 诉诸权威、因果 |
| 视角策略 | 观点的表达 | 显性/隐性立场 |
| 强化/弱化 | 话语的强化或缓和 | 强调词、模糊语 |

## van Dijk社会认知方法

### 宏观结构分析
- **主题**: 话语的语义宏观结构
- **图式**: 话语的修辞组织

### 微观结构分析
- **局部语义**: 命题、连贯
- **局部语法**: 句法、词序
- **修辞**: 隐喻、夸张

### 认知维度
- **心智模型**: 情境的心理表征
- **知识结构**: 社会共享知识
- **意识形态**: 基本社会信念

## 使用示例

```
用户: 分析这篇政治演讲中的话语策略

AI: 我将采用批判话语分析方法，从三个维度分析：

## 一、文本层面分析

### 词汇分析
- 指称策略："我们人民"vs"那些政客"
- 谓语策略：正面定性本国，负面定性他者
- 隐喻系统：疾病隐喻("国家生病")、战争隐喻("抗击通胀")

### 语法分析
- 及物性：物质过程主导，突出行动
- 情态：高确定性情态("必须""一定")
- 被动语态：隐藏施事("问题被解决")

## 二、话语实践层面
- 互文性：引用历史人物、经典文献
- 话语消费：预设听众认同

## 三、社会实践层面
- 意识形态：民族主义、民粹主义
- 权力关系：建构二元对立
[继续详细分析...]
```

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | text_analyzer.py | 文本层面语言学分析，支持词汇/语法/结构多维度分析 |
| 2 | discourse_strategy.py | 话语策略识别，Wodak五话语策略框架分析 |
| 3 | power_analyzer.py | 权力关系与意识形态分析，van Dijk社会认知方法 |

### CLI用法

```bash
python tools/text_analyzer.py --input speech.txt --level lexical,grammatical
python tools/discourse_strategy.py --input discourse.txt --framework wodaK
python tools/power_analyzer.py --input text.json --model vandijk
```

## 🚫 绝对禁止原则

> **使用前必读**：以下原则是不可逾越的红线，违反将导致话语分析结论无效。

1. **禁止脱离社会语境分析话语** — 仅做词汇/语法层面的文本分析，不联系社会权力关系和意识形态背景
2. **禁止忽视互文性** — 不分析文本对已有话语的引用、改写、挪用，丢失话语的历史和权力维度
3. **禁止将话语等同于现实** — 将话语建构误认为客观现实，忽略话语背后的权力运作和利益诉求
4. **禁止单一方法论框架混用** — 同时使用CDA和会话分析而不说明差异，两者有不同的本体论和认识论假设
5. **禁止忽视话语策略的效果** — 仅识别话语策略而不评估其在特定社会语境中的效果和功能
6. **禁止用研究者自己的立场代替分析对象** — 将主观判断当作"客观"分析结论，违反批判话语分析的价值反思要求

## ✅ 质量标准

### 完整性
- 必做项清单完成度 ≥ 90%
- 话语策略识别完整
- 语境分析有深度

### 方法论
- 理论框架与数据一致性 ≥ 90%
- 分析步骤可复现性高
- 框架选择有明确依据

### 深度
- 核心维度覆盖 ≥ 80%
- Fairclough三维模型完整应用
- 权力关系和意识形态分析深入

## 参考文献

1. Fairclough, N. (2010). *Critical Discourse Analysis: The Critical Study of Language*. 2nd ed. Routledge.
2. van Dijk, T.A. (2008). *Discourse and Power*. Palgrave.
3. Wodak, R. (2015). *The Discourse Studies Reader*. Routledge.
4. Gee, J.P. (2011). *An Introduction to Discourse Analysis*. 3rd ed. Routledge.
5. Potter, J., & Wetherell, M. (1987). *Discourse and Social Psychology*. Sage.

---

**技能版本**: 5.0.0  
**方法论标准**: Fairclough三维模型, van Dijk社会认知方法  
**创建时间**: 2026-03-15