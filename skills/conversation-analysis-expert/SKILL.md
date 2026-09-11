---
name: conversation-analysis-expert
description: |
  Conversation Analysis expert. Provides turn-taking analysis, sequential organization, repair mechanisms, interactional competence assessment, and discourse pattern identification. Suitable for linguistics, communication studies, and interactional sociology.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

## 概述

会话分析（Conversation Analysis，简称 CA）是一门以经验研究为基础的社会学分支学科，起源于 Harvey Sacks 在 1960 年代的开创性工作，并与 Emanuel Schegloff 和 Gail Jefferson 共同发展成熟。CA 的核心方法论原则是：**以参与者自身的行为组织和推理为分析对象**，而非从外部强加理论框架。

本技能提供基于 CA 传统的系统化会话分析能力，涵盖话轮转换系统（Turn-Taking System）、序列组织（Sequence Organization）、修复机制（Repair）以及机构互动（Institutional Interaction）四大核心领域。适用于医患沟通研究、课堂教学分析、客服对话优化、法庭互动研究、日常会话研究等多种场景。

使用本技能时，分析师必须坚持"描述先于解释"的基本立场，即首先详尽描述会话参与者实际上做了什么，再探讨其背后的社会意义和机制，而非以先入为主的理论预设代替细致的观察描述。

---

## 理论基础

### 经典理论家与核心贡献

**Harvey Sacks (1931-1975)**
美国社会学家，CA 创始人。Sacks 的核心贡献包括：（1）话轮转换系统理论，提出话轮分配的基本规则和选项；（2）成员类属分析（Membership Categorization Analysis, MCA），探讨人们如何运用社会类别组织描述；（3）会话材料的"录音/转写"方法论革命，使细致分析日常对话成为可能。Sacks 的遗著《会话分析讲演集》（Lectures on Conversation, 1992）是该领域的奠基文献。

**Emanuel A. Schegloff (1934-2024)**
美国 UCLA 社会学教授，CA 领域最具影响力的理论家之一。Schegloff 系统发展了序列组织理论，提出邻接对（Adjacency Pair）、扩展序列（Sequence Expansion）和优先解读（Preferred Interpretation）等核心概念。其著作《序列分析导论》（Sequence Analysis, 2007）系统阐述了 CA 的分析单位和方法论原则。Schegloff 还对界面互动（interactions at interface）、电话会话和会话中的索引性（indexicality）进行了深入研究。

**Gail Jefferson (1938-2007)**
英国兰卡斯特大学荣誉研究员，CA 转写体系的主要设计者。Jefferson 创建了至今仍在全球广泛使用的 CA 转写规范，包括话轮重叠标记、停顿计时、笑声编码、语速变化标注等。她的研究涵盖错误和修复、笑话与幽默、会话中的情感表达等主题。《转写手册》（Jefferson, 2004）已成为该领域的标准参考文献。

**John Heritage (1947-)**
英国 UCLA 社会学教授，CA 在机构互动研究领域的主要推手。Heritage 将 CA 方法论系统引入对医疗机构、法庭审讯、新闻采访和客户服务等机构场景的分析，揭示了机构互动中权力不对称、任务导向和身份建构的会话机制。其著作《机构互动》（Interactional Constitution of Institutions, 2012）与 Steven Clayman 合著的《新闻采访中的会话》（Craft of Interviewing）均是该领域的权威文献。

**Jeff Sidnell (1961-)**
多伦多大学社会学教授，《会话分析手册》（The Handbook of Conversation Analysis, 2012）主编之一。Sidnell 的研究涵盖法庭互动、跨文化比较会话分析以及 CA 的认识论和方法论基础，其工作促进了 CA 与语言人类学的深度对话。

---

## 理论框架总览

```
┌─────────────────────────────────────────────────────────────────┐
│                    会话分析 (CA) 理论框架                         │
├─────────────────┬───────────────────────────────────────────────┤
│ 话轮转换系统     │ 话轮构建、话轮分配、转换相关位置 (TRP)           │
│ (Turn-Taking)   │ Sacks, Schegloff & Jefferson (1974)             │
├─────────────────┼───────────────────────────────────────────────┤
│ 序列组织         │ 邻接对、扩展序列、优先/非优先回应                 │
│ (Sequence Org.) │ Schegloff (2007)                                │
├─────────────────┼───────────────────────────────────────────────┤
│ 修复机制         │ 自我/他人发起的 × 自我/他人完成的 修复组合        │
│ (Repair)        │ Jefferson et al.                                │
├─────────────────┼───────────────────────────────────────────────┤
│ 机构互动         │ 医患、课堂、法庭、新闻采访、客服等场景             │
│ (Institutional)  │ Heritage (2012)                                 │
├─────────────────┼───────────────────────────────────────────────┤
│ 多模态分析       │ 手势、注视、空间配置、身体姿态的协调组织           │
│ (Multimodal)    │ Mondada (2019), Goodwin (2000)                  │
└─────────────────┴───────────────────────────────────────────────┘
```

---

## 🖥️ Python 工具

### 工具总览

| 工具文件 | 功能描述 | 核心方法 | CLI 用法示例 |
|---------|---------|---------|------------|
| `turn_taker.py` | 话轮转换分析 | `identify_trp()`, `analyze_turn_allocation()` | `python tools/turn_taker.py --input data/transcript.json --output results/trp.json` |
| `sequence_analyzer.py` | 序列组织分析 | `identify_adjacency_pairs()`, `analyze_preference()` | `python tools/sequence_analyzer.py --input data/transcript.json --output results/sequences.json` |
| `repair_detector.py` | 修复机制识别 | `detect_repairs()`, `classify_repair_type()` | `python tools/repair_detector.py --input data/transcript.json --output results/repairs.json` |

### 转写数据格式要求

所有工具均要求输入 JSON 格式的会话转写文件，格式规范如下：

```json
[
  {
    "speaker": "A",
    "text": "你好，请问今天有什么不舒服？",
    "start_time": 0.0,
    "end_time": 3.5
  },
  {
    "speaker": "B",
    "text": "我这两天一直头疼。",
    "start_time": 3.8,
    "end_time": 6.2
  }
]
```

字段说明：
- `speaker`: 说话人标识符（字符串，不可为空）
- `text`: 话语内容（字符串，不可为空）
- `start_time`: 开始时间（浮点数，单位秒，可选）
- `end_time`: 结束时间（浮点数，单位秒，可选）

### turn_taker.py 详细用法

```bash
# 标准调用
python tools/turn_taker.py --input data/consultation.json --output results/trp_analysis.json

# 输出结构
{
  "trps": [
    {
      "turn_index": 2,
      "position": "end",
      "type": "possible_trp"
    }
  ],
  "allocation": {
    "current_selects_next": 5,
    "next_self_selects": 12,
    "current_continues": 2
  }
}
```

**话轮分配类型说明**：
- `current_selects_next`: 当前说话人通过称呼语或专有名词指定下一说话人
- `next_self_selects`: 无人指定，下一说话人主动接话
- `current_continues`: 当前说话人在转换相关位置继续说话（不构成话轮转换）

### sequence_analyzer.py 详细用法

```bash
python tools/sequence_analyzer.py --input data/interview.json --output results/sequences.json

# 邻接对类型预定义
ADJACENCY_PAIRS = {
    'question-answer': {'first': ['?', '吗', '什么'], 'second': ['是', '不是', '好']},
    'greeting-greeting': {'first': ['你好', '早', 'hi'], 'second': ['你好', '早', 'hi']},
    'request-accept/reject': {'first': ['请', '能', '可以'], 'second': ['好', '行', '不行']}
}
```

**偏好组织分析**：在请求-接受/拒绝邻接对中，直接回应（如"好"、"行"）为优先回应（preferred response）；含延迟标记（如"但是"、"不过"）或解释的回应为非优先回应（dispreferred response）。

### repair_detector.py 详细用法

```bash
python tools/repair_detector.py --input data/therapy.json --output results/repairs.json

# 修复类型四象限
# 自我发起-自我完成 (self-initiated, self-repair)
# 自我发起-他人完成 (self-initiated, other-repair)
# 他人发起-自我完成 (other-initiated, self-repair)
# 他人发起-他人完成 (other-initiated, other-repair)
```

---

## 🚫 绝对禁止原则

> **核心原则**：会话分析强调"描述先于解释"，分析者必须忠实呈现参与者的行为组织，而非以理论预设代替细致观察。

### 六条绝对禁止原则

1. **禁止脱离语境解释话语**
   会话意义具有强烈的情境依赖性。任何话语的解释必须基于其在特定序列位置中的实际使用，而非词典意义或说话人事后的陈述。脱离语境的解释即使在直觉上合理，也与方法论文则相悖。

2. **禁止预设参与者意图**
   CA 分析关注参与者实际上做了什么（what they do），而非他们意图做什么。意图属于参与者的主观心理状态，无法从会话行为本身直接推知。声称某话语反映了某意图需要额外的论证，而非不言自明。

3. **禁止忽视话轮转换细节**
   话轮边界、转换时机、重叠话语、停顿时长等细节本身就构成有组织的行为模式。忽略这些细节意味着忽略会话的核心组织机制。TRP（转换相关位置）的识别是一切后续分析的基础。

4. **禁止跳过转写验证**
   转写是 CA 分析的核心前提。未经良好转写的会话数据无法支持可靠的 CA 分析。转写过程本身即是分析过程，包含对声音、节奏、语调、停顿等副语言特征的系统记录。

5. **禁止过度理论化**
   CA 的核心洞见来自对日常互动的细致描述，而非套用宏观社会学理论。在尚未充分描述参与者的实际行为之前，不应引入功能主义解释、权力分析或意识形态批判等高层次理论框架。

6. **禁止忽视参与者视角**
   CA 方法论的基石之一是"成员方法论"（member's method）：参与者自身运用哪些组织资源来生产可理解的行为？分析者必须从参与者的内部视角（emic perspective）来理解会话，而非从分析者的外部视角（etic perspective）强加解读。

---

## 5️⃣ 五阶段实施流程

### 阶段一：识别（Identify）

**目标**：获取原始会话数据，确定分析边界和场景类型。

**操作步骤**：
1. 收集录音/录像数据，确保获得所有参与者的知情同意
2. 进行完整转写（参照 Jefferson CA 转写规范）
3. 识别会话类型（日常对话、机构对话、多方互动等）
4. 标注说话人、话轮边界和时间戳
5. 确定分析焦点（如特定序列、话轮转换模式或修复机制）

**输入**：原始录音/录像文件，或初步转写稿
**输出**：规范转写文本（含时间标注和副语言特征）

---

### 阶段二：分析（Analyze）

**目标**：运用 CA 核心工具对转写数据进行系统分析。

**操作步骤**：
1. 运行 `turn_taker.py` 识别转换相关位置（TRP）和话轮分配模式
2. 运行 `sequence_analyzer.py` 识别邻接对和序列扩展模式
3. 运行 `repair_detector.py` 识别修复序列及其类型分布
4. 对关键序列进行手动深度标注（如重叠、停顿语调、笑声等）
5. 识别机构互动中的任务导向结构和身份建构机制

**分析工具对照表**：
| 分析维度 | 主要工具 | 补充工具 |
|---------|---------|---------|
| 话轮转换 | turn_taker.py | 手动标注 TRP |
| 序列组织 | sequence_analyzer.py | 手动标注扩展 |
| 修复机制 | repair_detector.py | 四象限分类 |
| 多模态 | — | Goodwin (2000) 框架 |

**输入**：规范转写文本
**输出**：结构化分析结果（JSON 格式，含索引、类型和位置信息）

---

### 阶段三：执行（Execute）

**目标**：将分析结果转化为可理解的研究发现。

**操作步骤**：
1. 解读 TRP 分布模式，联系话轮分配规则进行说明
2. 分析邻接对的优先/非优先回应模式及其社会意义
3. 统计修复类型分布，讨论修复机制在维持互动秩序中的作用
4. 提炼关键发现，选择代表性序列片段作为证据
5. 将技术分析结果转化为非技术受众可理解的语言
6. 生成可视化的序列图（sequence diagram）辅助呈现

**输出**：分析备忘录或初步研究发现报告

---

### 阶段四：验证（Verify）

**目标**：确保分析结果的可靠性和可重复性。

**操作步骤**：
1. 复核所有 JSON 输出文件，确认数据完整性
2. 交叉检查工具输出与手动转写的一致性
3. 对关键发现进行独立复核（同伴验证）
4. 确认分析解释与转写证据的一致性
5. 检查是否存在选择性地忽略不符合预期模式的数据
6. 验证序列解读是否符合 CA 学术规范

**验证清单**：
- [ ] 转写文本已按 Jefferson 规范完成
- [ ] 所有话轮均已标注，无遗漏
- [ ] 工具输出文件大小合理（>1KB）
- [ ] 邻接对识别结果与人工判断一致
- [ ] 修复类型分类逻辑正确
- [ ] 分析解读有转写证据支撑

---

### 阶段五：归档（Archive）

**目标**：规范存储分析过程和结果，支持后续研究复用。

**操作步骤**：
1. 以标准命名规范存储转写文件：`{project}_{date}_{scene}.json`
2. 保存分析结果文件至 `results/` 目录
3. 生成分析日志，记录分析决策过程
4. 编写数据字典，说明字段含义和编码规则
5. 如涉及机构数据，确认脱敏处理和伦理审批记录
6. 撰写分析报告，包含方法、发现和局限性说明

**输出**：归档数据包（含原始数据、转写、分析结果、报告）

---

## ✅ 质量标准

### 完整性标准

| 检查项 | 最低要求 | 理想标准 |
|--------|---------|---------|
| 转写覆盖率 | 所有话轮100%转写 | 含副语言特征完整标注 |
| TRP 识别 | 所有潜在 TRP 标注 | 区分强/弱 TRP |
| 邻接对识别 | 主要类型全覆盖 | 考虑语境细分 |
| 修复分析 | 类型四象限均有覆盖 | 含频率统计 |
| 机构分析 | 识别任务结构 | 揭示权力不对称 |

### 方法论标准

1. **忠实性**：分析解释必须忠实于转写证据，禁止脱离语境地解读
2. **系统性**：运用 CA 核心概念（Sacks 等人传统）而非替代性理论框架
3. **可重复性**：分析过程和结果必须可被其他受过训练的分析师复现
4. **描述优先**：坚持"先描述、后解释"的基本立场
5. **成员视角**：从参与者内部视角理解行为，而非从外部强加判断

### 深度标准

- **基础层**：完成转写、识别 TRP、标注邻接对
- **进阶层**：分析偏好组织、修复机制类型分布、序列扩展模式
- **深度层**：揭示机构互动中的权力不对称和身份建构机制
- **综合层**：将微观会话分析与宏观社会理论对话

---

**技能版本**: 5.0.0-cli-native+agent
**方法论严谨性**: 0%妥协
**最后更新**: 2026-04-04