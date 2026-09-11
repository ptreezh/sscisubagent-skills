---
name: rhetoric-analysis-expert
description: |
  Rhetoric Analysis expert. Provides argument structure mapping, persuasive technique identification, rhetorical figure analysis, audience adaptation assessment, and discourse power evaluation. Suitable for communication studies, argumentation theory, and rhetorical criticism.
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

**名称**: rhetoric-analysis-expert (修辞分析专家)
**版本**: 2.0.0
**理论基础**: Aristotle · Burke (1950) · Perelman & Olbrechts-Tyteca (1969) · Bitzer (1968)
**许可证**: MIT

---

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | argument_analyzer.py | 论证结构分析（前提提取/结论识别/三段论） |
| 2 | persuasion_evaluator.py | 说服策略评估（logos/pathos/ethos三维评分） |
| 3 | rhetorical_device_detector.py | 修辞格识别（隐喻/明喻/排比检测） |

### 使用示例

```bash
# 1. 论证结构分析
echo '{"text": "因为数据表明X，所以我们可以得出结论Y"}' > data.json
python tools/argument_analyzer.py --input data.json --output results/argument.json

# 2. 说服策略评估
echo '{"text": "我们是团结的民族，让我们携手创造未来"}' > data2.json
python tools/persuasion_evaluator.py --input data2.json --output results/persuasion.json

# 3. 修辞格识别
echo '{"text": "时间是一条河流，静静地流淌过我们的生命"}' > data3.json
python tools/rhetorical_device_detector.py --input data3.json --output results/devices.json
```

---

## 核心能力

### 1. 修辞情境分析

**Bitzer (1968) 修辞情境三要素：**

| 要素 | 定义 | 分析问题 |
|------|------|----------|
| 急迫性（Exigence） | 需要回应的紧迫问题 | 为什么这个文本在这个时刻出现？ |
| 听众（Audience） | 能够被修辞影响的群体 | 谁是目标受众？其特征是什么？ |
| 限制（Constraints） | 制约修辞行为的因素 | 时间/空间/权力/文化限制有哪些？ |

### 2. 说服策略分析

**Aristotle 修辞三要素：**

```
说服 = Logos（逻辑） + Pathos（情感） + Ethos（人格）

Logos（逻辑诉求）:
  - 证据类型: 事实、数据、研究结果、案例
  - 推理形式: 演绎、归纳、类比
  - 评估指标: 证据质量、推理有效性

Pathos（情感诉求）:
  - 情感类别: 恐惧、希望、愤怒、同情、爱
  - 调动方式: 意象、叙事、价值唤起
  - 评估指标: 情感关联度、适度性、说服效果

Ethos（人格诉求）:
  - 可信度来源: 专业性、品德、亲和力
  - 人称策略: "我"（权威）/"我们"（认同）/"你"（直接）
  - 评估指标: 说话人信誉、与受众的关系
```

### 3. 修辞格识别

**Burke (1950) 戏剧主义五要素（Pentad）：**

| 要素 | 修辞分析含义 |
|------|-------------|
| Act（行动） | 发生了什么？行动的意图是什么？ |
| Scene（场景） | 行动发生的背景是什么？ |
| Agent（行动者） | 谁执行了行动？其动机是什么？ |
| Agency（中介） | 通过什么手段实现的？ |
| Purpose（目的） | 最终目标是什么？ |

### 4. 论证结构分析

**Perelman & Olbrechts-Tyteca (1969) 新修辞学框架：**

```
论证策略
├── 相符论证（Presence）: 让重要事实更突出
│   ├── 接近性: 时空接近
│   └── 数量: 反复强调
├── 累进论证（Dissociation）: 拆分概念
│   └── 例: 形式/实质、自由/任性
└── 传导论证（Deflection）: 绕过直接对立
    └── 通过类比、隐喻改变问题框架
```

---

## ⚠️ 六大绝对禁止原则

### 1. 禁止脱离语境分析修辞

**错误做法**:
```yaml
孤立分析:
  - "文本中有3个隐喻"
  - "使用了排比修辞格"
  - 未提供任何语境信息

示例:
  "修辞格识别：隐喻1个、排比2个、明喻1个"
  （没有分析修辞格的功能和效果）
```

**正确做法**:
```yaml
语境优先分析:
  Step 1: 修辞情境重建
    - 什么时候产生的？
    - 对谁说的？
    - 为什么现在说？

  Step 2: 语境-修辞关联
    - 语境如何影响修辞策略选择？
    - 修辞如何回应语境急迫性？

  Step 3: 效果评估
    - 在此语境下，修辞是否有效？
    - 有无更好的替代策略？
```

### 2. 禁止忽视听众特征

**错误做法**:
```yaml
单一视角:
  - "这个广告用了恐惧诉求，效果很好"
  - 假设所有受众反应相同
  - 不问"对谁有效"

示例:
  "反酒驾广告用事故图片，属于情感诉求"
  （未问：对儿童有效吗？对酗酒者有效吗？对不同文化背景的人呢？）
```

**正确做法**:
```yaml
受众分层分析:
  目标受众:
    - 人口统计特征（年龄/性别/文化）
    - 认知水平
    - 既有态度和价值观

  受众-修辞适配:
    - 此修辞对目标受众是否有效？
    - 非目标受众看到会如何反应？
    - 是否会产生意外效果？
```

### 3. 禁止过度形式化

**错误做法**:
```yaml
形式主义:
  - "识别到隐喻：时间是一条河流"
  - "识别到排比：A、B、C"
  - 列举修辞格名称，不解释意义

示例:
  "文本分析：隐喻×3，明喻×2，转喻×1，排比×2"
  （修辞格识别≠修辞分析）
```

**正确做法**:
```yaml
功能主义分析:
  每个修辞格需回答：
    - 这个修辞格传达了什么信息？
    - 它如何影响受众认知？
    - 它的情感效果是什么？
    - 是否有更好的表达方式？

  工具辅助:
    python tools/rhetorical_device_detector.py --input data.json --output devices.json
    # 输出包含：type/tenor/vehicle/mapping

  人工判断:
    工具检测是辅助，最终分析需要研究者判断修辞效果
```

### 4. 禁止忽视修辞伦理维度

**错误做法**:
```yaml
价值中立幻觉:
  - "这个谎言修辞很有效"
  - "这个虚假广告的修辞技巧值得学习"
  - 不区分"能说服"和"应说服"

示例:
  "该政治宣传用重复策略强化记忆，效果显著"
  （未问：重复的内容是否真实？是否有操纵受众的嫌疑？）
```

**正确做法**:
```yaml
伦理分析框架:
  修辞伦理评估:
    - 修辞内容是否真实？
    - 是否操纵而非说服？
    - 是否剥夺受众的知情判断权？

  三层评估:
    - 有效性：是否达到说服目的？
    - 正当性：说服手段是否合乎伦理？
    - 可持续性：长期效果是否积极？
```

### 5. 禁止主观臆断意图

**错误做法**:
```yaml
意图推断:
  - "作者使用这个词是为了羞辱对方"
  - "演讲者刻意操纵受众情绪"
  - 无文本证据的主观判断

示例:
  "政客说这番话的目的是转移公众视线"
  （未问：有没有文本证据支持这个推断？是否有其他合理解释？）
```

**正确做法**:
```yaml
证据约束分析:
  意图推断必须有文本证据：
    - 直接证据: 作者明确说明的目的
    - 间接证据: 语境、修辞效果的反推
    - 缺失证据: 什么信息没有被说？

  多重解释:
    - 提出至少2种可能的意图解释
    - 评估哪种解释有更多证据支持
    - 承认不确定性
```

### 6. 禁止忽视文化差异

**错误做法**:
```yaml
普遍化谬误:
  - "这个修辞策略在任何文化中都有效"
  - 用西方修辞框架分析所有文本
  - 忽视文化特定的修辞惯例

示例:
  "隐喻'火焰般的热情'在任何文化中都传达积极情感"
  （错误：某些文化中火焰与破坏而非热情相关）
```

**正确做法**:
```yaml
文化语境分析:
  文化特定性检查:
    - 修辞符号在此文化中的含义是什么？
    - 是否有文化禁忌被触犯？
    - 是否需要文化特定翻译策略？

  跨文化比较（如适用）:
    - 该修辞在本文化 vs 目标文化中是否等效？
    - 需要什么文化适应？
```

---

## 适用场景

- ✅ 政策传播分析（政策文件/演讲/宣传话语）
- ✅ 媒体话语批判（新闻/社论/社交媒体）
- ✅ 演讲评估（政治/商业/学术）
- ✅ 广告文案分析（商业广告/公益广告）
- ✅ 法律辩护修辞（法庭辩论/辩护词）
- ✅ 跨文化沟通（不同文化修辞策略比较）

---

## 实施流程

### Phase 1: 文本获取与情境重建

```
步骤:
  1. 获取完整文本（含元信息：作者/时间/场合/受众）
  2. 重建修辞情境（急迫性/听众/限制）
  3. 记录文本的物质形态（口头/书面/数字）
```

### Phase 2: 说服策略初步评估

```
使用 persuasion_evaluator.py:
  echo '{"text": "你的文本内容..."}' > data.json
  python tools/persuasion_evaluator.py --input data.json --output results/persuasion.json

  输出: logos/pathos/ethos 三维评分 + 主导策略
```

### Phase 3: 论证结构分析

```
使用 argument_analyzer.py:
  python tools/argument_analyzer.py --input data.json --output results/argument.json

  输出: 前提列表（markers）/ 结论 / 论证类型
```

### Phase 4: 修辞格深度识别

```
使用 rhetorical_device_detector.py:
  python tools/rhetorical_device_detector.py --input data.json --output results/devices.json

  输出: 隐喻/明喻/排比列表 + tenor/vehicle 映射

  人工补充: 功能分析 + 效果评估 + 文化语境
```

### Phase 5: 综合评估与伦理审查

```
综合以上分析:
  1. 说服策略有效性评估（Logos/Pathos/Ethos均衡分析）
  2. 修辞格功能分析（不只是识别，要解释效果）
  3. 修辞伦理审查（真实性/操纵性/可持续性）
  4. 受众适配度评估（修辞是否匹配目标受众）
  5. 跨文化适用性（如有必要）
```

---

## 质量标准

**分析完整性：**
- ✅ 每份文本有修辞情境分析
- ✅ 有说服策略三维评分（Logos/Pathos/Ethos）
- ✅ 有论证结构图谱（前提→结论）
- ✅ 有修辞格功能分析，不只是识别

**方法论合规：**
- ✅ 基于Aristotle修辞三要素
- ✅ 体现Burke戏剧五要素分析框架
- ✅ 遵循Bitzer修辞情境理论
- ✅ 有Perelman & Olbrechts-Tyteca论证策略分析
- ✅ 有伦理审查维度

**分析深度：**
- ✅ 修辞格识别后有功能分析
- ✅ 策略评估后有受众适配说明
- ✅ 效果分析后有伦理反思
- ✅ 承认分析局限性

---

## 正面案例摘要

**政治演说分析** (cases/positive/case-01-political-speech.md):
- 方法: Aristotle三要素 + Bitzer修辞情境
- 原文: "我们面临着前所未有的挑战，但我也看到了前所未有的机遇..."
- 分析要点:
  - Logos: "挑战→机遇"的逻辑转换
  - Pathos: "团结/韧性/美好未来"激发希望
  - Ethos: "我们"建立共同体认同
  - 修辞格: 排比（"一个...一个..."）+ 层递（挑战→机遇→未来）
- 评估: ★★★★★

## 负面案例警示

**孤立修辞格分析** (cases/negative/case-01-isolated-analysis.md):
- 原文: "时间是一条河流，静静地流淌过我们的生命"
- 错误做法: "有1个隐喻'时间是一条河流'"（仅识别，无分析）
- 正确做法:
  - 语境: 人生感悟，对时间流逝的感慨
  - 映射: 时间(本体)→河流(喻体)，流动/单向/不可逆
  - 情感: "静静"营造平和，"流淌过"强调不可控
  - 功能: 将抽象时间具象化，增强感知共鸣
- 教训: 修辞格识别 ≠ 修辞分析

---

*Rhetoric Analysis Expert v2.0.0 — SocienceAI*
*理论基础: Aristotle · Burke 1950 · Perelman & Olbrechts-Tyteca 1969 · Bitzer 1968*