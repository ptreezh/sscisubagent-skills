---
name: media-analysis-expert
description: |
  Media Analysis expert. Provides content coding, media framing analysis, audience reception mapping, media production assessment, and cultural indicators measurement. Suitable for media studies, communication research, and cultural analysis.
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

**名称**: media-analysis-expert (媒介分析专家)
**版本**: 2.0.0
**理论基础**: McLuhan (1964) · Postman (1985) · Williams (1974) · Couldry & Hepp (2017)
**许可证**: MIT

---

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | mediatization_tracker.py | 媒介化追踪（媒介对社会各领域的渗透程度分析） |
| 2 | medium_ecology_analyzer.py | 媒介生态分析（媒介系统的相互关系/竞争/共生） |
| 3 | platform_power_analyzer.py | 平台权力分析（平台所有/治理/算法/商业模式） |

### 使用示例

```bash
# 1. 媒介化追踪
echo '{"mediatization_indicators": {"media_dependency": true, "media_logic_adoption": true}}' > data.json
python tools/mediatization_tracker.py --input data.json --output results/mediatization.json

# 2. 媒介生态分析
python tools/medium_ecology_analyzer.py --input data.json --output results/ecology.json

# 3. 平台权力分析
python tools/platform_power_analyzer.py --input data.json --output results/platform_power.json
```

---

## 核心能力

### 1. McLuhan 媒介理论

**核心命题：**

```
"媒介即讯息"（The medium is the message）

含义:
  - 媒介的影响来自媒介本身，而非内容
  - 媒介通过"延伸人体"和"截除"来重塑社会
  - 新媒介创造新的感知比率

媒介四定律（McLuhan & Fiore）:
  1. 提升（Enhancement）: 媒介放大了什么？
  2. 逆转（Reversal）: 媒介过度延伸后会变成什么？
  3. 取回（Retrieval）: 媒介会恢复什么旧形式？
  4. 废弃（Obsolescence）: 媒介使什么变得过时？
```

**媒介与内容的关系：**

```
媒介塑造内容:
  - 不同的媒介适合不同类型的内容
  - 内容被媒介的特性所塑造
  - "电视"不只是传输内容的管道，它本身就是讯息

冷媒介 vs 热媒介（McLuhan）:
  热媒介: 高清晰度，需要较少参与（电影/广播）
  冷媒介: 低清晰度，需要大量参与（电话/电视/漫画）
```

### 2. Williams 电视研究

**技术/文化形式分析（Williams 1974）：**

```
电视的三种定义:
  1. 发明（Invention）: 技术的可能性
  2. 形式（Form）: 特定社会使用的结构
  3. 制度（Institution）: 生产和分配的组织

关键洞见:
  - 技术可能性 ≠ 社会现实
  - 电视"本质"是由社会斗争决定的
  - 私人接收 vs 公共广播的张力
```

### 3. Couldry & Hepp 深度媒介化

**"深度媒介化"命题（Couldry & Hepp 2017）：**

```
深度媒介化 = 媒介已渗透到社会所有角落
  - 不只是"媒介社会"（媒介影响社会）
  - 而是"媒介化世界"（社会已被媒介建构）

三大特征:
  1. 媒介化基础设施: 媒介成为所有社会实践的基础设施
  2. 平台化: 一切都通过平台中介
  3. 数据化: 所有行为都留下数字痕迹

研究转向:
  从"媒介做什么"（效果研究）
  到"媒介如何建构世界"（建构论）
```

### 4. 媒介化追踪

**MediatizationTracker 工具使用：**

```python
# 评估媒介化程度
result = track_mediatization(domain_data)
# 输出: level (strong/medium/weak) / process / effects

# 评估指标
indicators = {
    "media_dependency": True,        # 该领域是否依赖媒介？
    "media_logic_adoption": True,   # 是否采用媒介逻辑？
    "media_infrastructure": True    # 是否有媒介基础设施？
}

level = assess_mediatization_level(domain_data)
# >= 3: strong / >= 2: medium / else: weak
```

---

## ⚠️ 六大绝对禁止原则

### 1. 禁止技术决定论

**错误做法**:
```yaml
技术决定:
  - "电视必然导致思维碎片化"
  - "互联网必然带来民主"
  - 技术被赋予超越社会的力量

示例:
  "社交媒体必然改变政治参与"
  （忽略了社会条件如何塑造技术使用）
```

**正确做法**:
```yaml
社会-技术共构:
  - 技术不是独立的因果力量
  - 社会条件决定技术如何被使用
  - 技术被社会群体争夺和使用

  分析框架:
    - 谁有权力决定技术的使用方式？
    - 什么社会条件塑造了这种使用？
    - 是否有替代性使用方式？
```

### 2. 禁止忽视社会语境

**错误做法**:
```yaml
媒介孤立论:
  - "只看媒介本身"
  - 不问媒介如何嵌入社会
  - 忽略政治/经济/文化语境

示例:
  "电视新闻塑造了公众舆论"
  （未问：谁拥有电视？谁决定播放内容？政治经济语境是什么？）
```

**正确做法**:
```yaml
语境嵌入分析:
  - 政治语境: 媒介如何嵌入权力结构？
  - 经济语境: 媒介的所有权和商业模式是什么？
  - 文化语境: 媒介如何嵌入文化惯例？
```

### 3. 禁止忽视权力关系

**错误做法**:
```yaml
去政治化:
  - "媒介是中性工具"
  - 忽略媒介所有权集中
  - 不问"谁的声音被放大？"

示例:
  "Facebook连接了全球用户"
  （未问：Facebook如何通过算法放大某些声音？平台权力如何运作？）
```

**正确做法**:
```yaml
媒介权力批判:
  - 谁拥有这个媒介？
  - 谁决定媒介内容？
  - 谁的声音被放大/压制？
  - 算法如何执行权力？

  工具辅助:
    python tools/platform_power_analyzer.py --input data.json --output results/platform_power.json
```

### 4. 禁止忽视历史维度

**错误做法**:
```yaml
历史断裂:
  - "新媒体是新现象"
  - 不理解新旧媒介的连续性
  - 忽视历史先例

示例:
  "社交媒体是前所未有的革命"
  （未问：广播/电视/电话是否也有类似的历史争论？）
```

**正确做法**:
```yaml
历史化分析:
  - 这个媒介的历史先例是什么？
  - 新媒介与旧媒介有何连续/断裂？
  - 历史上类似争论的结果如何？
```

### 5. 禁止忽视受众能动性

**错误做法**:
```yaml
被动受众:
  - "受众是媒介的傀儡"
  - 不考虑受众如何抵抗/协商
  - 假设"媒介效果"是单向的

示例:
  "广告必然说服消费者购买"
  （未问：消费者如何抵抗广告解读？文化背景如何影响解读？）
```

**正确做法**:
```yaml
能动性视角:
  - 受众不是被动的接受者
  - 受众如何协商/抵抗/重新解读媒介内容？
  - 有什么样的"第二层解读"？
  - 是否有替代性媒介实践？
```

### 6. 禁止忽视全球不平等

**错误做法**:
```yaml
西方中心:
  - "西方媒介理论是普遍的"
  - 不考虑非西方媒介实践
  - 用西方框架分析所有现象

示例:
  "媒介化是全球普遍现象"
  （未问：不同地区/文化中的媒介化路径是否不同？全球南方有什么独特性？）
```

**正确做法**:
```yaml
全球视角:
  - 承认媒介理论的地理/文化局限性
  - 探索非西方媒介实践的独特性
  - 分析媒介的全球不平等（谁生产？谁消费？）
  - 考虑数字殖民主义的可能性
```

---

## 适用场景

- ✅ 媒介批评（新闻/影视/广告/流行文化）
- ✅ 传播政策研究（媒介规制/所有权/内容政策）
- ✅ 深度媒介化分析（政治/教育/宗教/日常生活）
- ✅ 平台权力批判（算法/数据/治理）
- ✅ 跨文化媒介比较
- ✅ 媒介史研究（历史脉络与当代关联）

---

## 实施流程

### Phase 1: 媒介生态记录

```
步骤:
  1. 识别研究领域的媒介生态
  2. 记录各媒介的角色和关系
  3. 追踪历史演变
```

### Phase 2: 媒介化程度评估

```
使用 mediatization_tracker.py:
  echo '{"mediatization_indicators": {"media_dependency": true, "media_logic_adoption": true}}' > data.json
  python tools/mediatization_tracker.py --input data.json --output results/mediatization.json

  输出: level (strong/medium/weak) + 过程分析 + 效果评估
```

### Phase 3: 媒介生态分析

```
使用 medium_ecology_analyzer.py:
  python tools/medium_ecology_analyzer.py --input data.json --output results/ecology.json

  分析: 媒介之间的关系 / 竞争与共生 / 系统稳定性
```

### Phase 4: 平台权力研究

```
使用 platform_power_analyzer.py:
  python tools/platform_power_analyzer.py --input data.json --output results/platform_power.json

  分析: 所有权结构 / 算法逻辑 / 商业模式 / 治理机制
```

### Phase 5: 综合分析

```
综合以上分析:
  1. McLuhan: 媒介即讯息（技术如何塑造感知）
  2. Williams: 技术/形式/制度三角（谁决定形式？）
  3. Couldry & Hepp: 深度媒介化（媒介如何建构世界）
  4. 权力批判: 谁有权力决定媒介运作？
  5. 全球视角: 媒介化的不平等地理
```

---

## 质量标准

**分析深度：**
- ✅ 有技术/社会共构视角
- ✅ 有历史脉络分析
- ✅ 有权力关系批判
- ✅ 有全球不平等意识

**方法论合规：**
- ✅ 基于McLuhan (1964)媒介理论
- ✅ 体现Williams (1974)电视研究框架
- ✅ 有Couldry & Hepp (2017)深度媒介化视角
- ✅ 有Postman (1985)媒介环境学批判

**规范性：**
- ✅ 避免技术决定论
- ✅ 承认受众能动性
- ✅ 有反身性反思
- ✅ 跨文化敏感性

---

*Media Analysis Expert v2.0.0 — SocienceAI*
*理论基础: McLuhan 1964 · Postman 1985 · Williams 1974 · Couldry & Hepp 2017*