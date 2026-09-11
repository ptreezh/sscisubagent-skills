---
name: semiotics-analysis-expert
description: |
  Semiotics Analysis expert. Provides sign/signifier/signified decomposition, denotation/connotation mapping, codes and conventions analysis, and semiotic triangle construction. Suitable for cultural studies, media analysis, and sign theory research.
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

**名称**: semiotics-analysis-expert (符号学分析专家)
**版本**: 2.0.0
**理论基础**: Saussure (1916) · Peirce · Barthes (1964) · Eco (1976)
**许可证**: MIT

---

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | sign_identifier.py | 符号类型识别（图像符号/指示符号/象征符号） |
| 2 | meaning_layer_analyzer.py | 意义层次分析（表层义/深层义/神话义） |
| 3 | myth_decoder.py | 神话解码（第一序/第二序意义） |

### 使用示例

```bash
# 1. 符号类型识别
echo '{"text": "香水广告中的女性优雅形象"}' > data.json
python tools/sign_identifier.py --input data.json --output results/sign_type.json

# 2. 意义层次分析
echo '{"text": "香水广告中展示的优雅女性形象..."}' > data2.json
python tools/meaning_layer_analyzer.py --input data2.json --output results/meaning.json

# 3. 神话解码
python tools/myth_decoder.py --input results/meaning.json --output results/myth.json
```

---

## 核心能力

### 1. 符号类型识别

**Peirce 符号三元组：**

```
            解释项 (Interpretant)
                 ↑
                /
               /
            符号 (Sign) ────→ 对象 (Object)
```

| 符号类型 | 关系定义 | 典型示例 | 分析重点 |
|---------|---------|---------|---------|
| 图像符号 (Icon) | 相似性关系 | 照片、地图、漫画 | 相似程度、选择特征 |
| 指示符号 (Index) | 因果/邻近关系 | 烟→火、脚印、疾病症状 | 物理/因果联系 |
| 象征符号 (Symbol) | 约定俗成 | 文字、国旗、十字架 | 文化规约、历史形成 |

### 2. Saussure 符号结构

**能指 (Signifier) / 所指 (Signified)：**

```
符号 = 能指 (声音/图像/物质形式) + 所指 (概念/意义)

关键特性:
├── 任意性: 符号与意义之间无自然联系
├── 差异性: 符号意义由差异产生（非本质存在）
├── 组合关系: 符号在句段（序列）中的排列
└── 聚合关系: 符号在联想（选择）集中的替代
```

### 3. Barthes 神话学

**两层符号系统：**

```
第一层（语言系统）:
  能指（形式） + 所指（概念） = 符号

第二层（神话系统）:
  第一层符号（作为能指）+ 神话所指（意识形态意义）= 神话

神话的功能: 将历史自然化、将偶然普遍化
```

### 4. 意义层次分析

| 层次 | 定义 | 分析问题 |
|------|------|---------|
| 表层义 (Denotation) | 直接、字面的意义 | 符号"表面"说了什么？ |
| 深层义 (Connotation) | 隐含、联想的意义 | 符号唤起了什么联想？ |
| 神话义 (Myth) | 文化意识形态意义 | 符号如何服务于特定意识形态？ |

---

## ⚠️ 六大绝对禁止原则

### 1. 禁止脱离文化语境解读

**错误做法**:
```yaml
普遍化谬误:
  - "红色在所有文化中都代表热情"
  - 用单一文化框架分析所有符号
  - 忽视符号的文化特殊性

示例:
  "红色符号传达'热情'或'革命'的意义"
  （未问：红色在中国文化中也有"吉祥/喜庆"含义）
```

**正确做法**:
```yaml
文化语境分析:
  Step 1: 确定符号产生的文化语境
    - 这是哪个文化/社群产生的？
    - 生产时间是哪个历史时期？

  Step 2: 追踪意义的历史变迁
    - 这个符号在该文化中意义是否发生过变化？
    - 是否有被"劫持"或意义反转的情况？

  Step 3: 评估文化特殊性
    - 这个符号是否可以跨文化等效传递？
    - 需要什么文化适应？
```

### 2. 禁止忽视符号的历史变迁

**错误做法**:
```yaml
静态分析:
  - "这个符号一直就是这个意义"
  - 不追踪符号的历史演变
  - 假设符号意义不变

示例:
  "十字架作为宗教符号，意义是永恒的"
  （错误：十字架经历了从刑具→殉道象征→时尚符号的演变）
```

**正确做法**:
```yaml
历史符号学分析:
  - 追溯符号的历史起源
  - 追踪意义的关键转折点
  - 记录当前语境中的意义
  - 预测可能的未来演变
```

### 3. 禁止过度解读（主观臆断）

**错误做法**:
```yaml
主观臆断:
  - "这个符号代表X"（无证据）
  - 过度分析细节
  - 用研究者的文化背景替代被分析对象的语境

示例:
  "广告中的蓝色代表忧郁，因此该广告表达了消极情绪"
  （未问：是否只是品牌色彩选择？）
```

**正确做法**:
```yaml
证据约束分析:
  符号解读必须有证据支撑：
    - 直接证据: 创作者/受众的明确说明
    - 间接证据: 历史/文化语境支持
    - 缺失证据: 什么信息未被确认？

  适度解读原则:
    - 先提供最直接的意义解读
    - 再提供可能的深层解读
    - 承认解读的多重可能性
```

### 4. 禁止忽视符号的多义性

**错误做法**:
```yaml
单义假设:
  - "这个符号只有一个正确意义"
  - 忽略符号的模糊性和开放性
  - 强制唯一解释

示例:
  "这个logo只有一个'创新'的意义"
  （实际上logo可能有多个并存的意义层次）
```

**正确做法**:
```yaml
多义性分析:
  识别并报告:
    - 符号有哪些可能的（合理）意义？
    - 哪些意义是主要的？哪些是次要的？
    - 不同受众可能如何解读？

  使用工具辅助:
    python tools/meaning_layer_analyzer.py --input data.json --output meaning.json
    # 输出: denotation + connotation + mythological layers
```

### 5. 禁止忽视符号的物质性

**错误做法**:
```yaml
抽象符号观:
  - 只分析文本/图像内容
  - 忽略符号的物质载体
  - 忽略使用场景

示例:
  "网页上的标志符号..."
  （未问：这个符号是以什么介质呈现的？尺寸/颜色/位置有何影响？）
```

**正确做法**:
```yaml
物质性审查:
  - 符号的物质载体是什么？（纸/屏幕/声音/空间）
  - 物质形态如何影响意义？
  - 使用场景（私密/公开/仪式化）如何影响符号效果？
```

### 6. 禁止忽视互文关系

**错误做法**:
```yaml
孤立分析:
  - 单独分析一个符号
  - 忽略符号与其他符号的关系
  - 忽略符号与类型（genre）的关系

示例:
  "分析这则广告中的女性形象"
  （未问：广告的整体叙事结构是什么？这个形象与其他形象的关系？）
```

**正确做法**:
```yaml
互文分析:
  - 这个符号与哪些其他符号构成整体？
  - 符号之间的关系是什么？（对比/类比/补充/矛盾）
  - 这个符号是否引用/戏仿了其他文本？
  - 是否存在符号聚合关系（可以选择的不同表达）？
```

---

## 适用场景

- ✅ 媒体文化分析（新闻/广告/影视符号）
- ✅ 品牌符号学（logo/视觉识别/品牌故事）
- ✅ 广告批判（消费主义意识形态解码）
- ✅ 文化研究（流行文化/亚文化符号）
- ✅ 视觉分析（图像/摄影/设计符号）
- ✅ 品牌话语分析（品牌叙事/文化编码）

---

## 实施流程

### Phase 1: 符号获取与记录

```
步骤:
  1. 确定分析对象（文本/图像/物体/事件）
  2. 记录符号的物质形态（载体/尺寸/场景）
  3. 建立符号清单（每个符号的ID/位置/形式）
```

### Phase 2: 符号类型识别

```
使用 sign_identifier.py:
  echo '{"text": "你的符号描述..."}' > data.json
  python tools/sign_identifier.py --input data.json --output results/sign_type.json

  输出: iconic (图像) / indexical (指示) / symbolic (象征) + 置信度
```

### Phase 3: 意义层次分析

```
使用 meaning_layer_analyzer.py:
  python tools/meaning_layer_analyzer.py --input data.json --output results/meaning.json

  输出: denotation / connotation / mythological layers
  注意: 工具提供表层分析，深层义和神话义需人工补充
```

### Phase 4: 神话解码

```
使用 myth_decoder.py:
  python tools/myth_decoder.py --input results/meaning.json --output results/myth.json

  输出: 第一序意义 + 第二序神话意义
  Barthes神话分析框架:
    1. 识别第一序符号（语言系统）
    2. 将第一序符号作为第二序能指
    3. 解码第二序神话所指（意识形态）
```

### Phase 5: 互文与文化语境整合

```
综合以上分析:
  1. 建立符号之间的互文关系图
  2. 补充文化历史语境
  3. 评估多义性（承认多种合理解读）
  4. 揭示意识形态功能（符号如何服务特定权力关系）
```

---

## 质量标准

**分析完整性：**
- ✅ 每个符号有类型标注（图像/指示/象征）
- ✅ 每层意义有分析记录（表层/深层/神话）
- ✅ 语境信息有记录（文化/历史/物质）

**方法论合规：**
- ✅ 基于Saussure能指/所指框架
- ✅ 体现Peirce符号三元组
- ✅ 遵循Barthes神话学两层分析
- ✅ 有Eco符号生产视角

**分析深度：**
- ✅ 工具辅助 + 人工判断结合
- ✅ 神话解码有意识形态分析
- ✅ 承认多义性和语境依赖
- ✅ 有文化历史维度

---

## 正面案例摘要

**香水广告神话解码** (cases/positive/case-01-advertisement.md):

- **表层分析**: 女性形象 + 香水产品 + 品牌文字
- **深层分析**:
  - 美丽代码: 优雅/魅力/吸引力
  - 性别代码: 女性气质规范
  - 阶级代码: 中产阶级消费品味
- **神话解码**:
  - 能指: 优雅女性使用香水
  - 所指: 使用此香水 = 成为优雅女性
  - 神话义: 消费主义意识形态（商品 = 身份认同）
- **评估**: ★★★★★

## 负面案例警示

**脱离语境的过度解读** (cases/negative/case-01-overinterpretation.md):

- 错误: "红色符号代表'革命'"（无文化语境支撑）
- 正确做法:
  1. 考察符号使用语境（是哪个文化/时期？）
  2. 追溯历史演变（红色在不同时期/文化有不同含义）
  3. 考虑多种可能解释（吉祥/警示/热情 + 革命）
  4. 提供证据支持（创作者意图/受众反应）

- 教训: 符号解读必须有文化历史证据支撑，不能主观臆断

---

*Semiotics Analysis Expert v2.0.0 — SocienceAI*
*理论基础: Saussure 1916 · Peirce · Barthes 1964 · Eco 1976*