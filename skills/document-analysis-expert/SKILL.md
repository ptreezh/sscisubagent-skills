---
name: document-analysis-expert
description: |
  Document Analysis expert. Provides historical document verification, source triangulation, content authentication, contextual interpretation, and archival research. Suitable for historical research, archival analysis, and documentary evidence assessment.
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

**名称**: document-analysis-expert (文档分析专家)
**版本**: 2.0.0
**理论基础**: Scott (1990) · Prior (2003) · Atkinson & Coffey (2004) · Silverman (2021)
**许可证**: MIT

---

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | document_classifier.py | 文档类型识别（政策/组织/个人/媒体/学术） |
| 2 | content_structure_analyzer.py | 内容结构分析（主题/叙事/话语/权力） |
| 3 | document_context_tracer.py | 语境追踪（生产/流通/使用/权力关系） |

### 使用示例

```bash
# 1. 文档分类
python tools/document_classifier.py -i data/policy_doc.txt -o results/type.json

# 2. 内容结构分析
python tools/content_structure_analyzer.py -i results/typed_doc.txt -o results/structure.json

# 3. 语境追踪
python tools/document_context_tracer.py -i results/structured_doc.txt -o results/context.json
```

---

## 核心能力

### 1. 文档类型识别

**Scott (1990) 四类文档模型：**

| 类型 | 定义 | 典型文档 | 分析重点 |
|------|------|----------|----------|
| 官方记录 | 正式、机构生产 | 政策文件、年度报告 | 制度逻辑 |
| 非官方记录 | 非正式、非制度化 | 内部邮件、便笺 | 潜规则 |
| 私人文献 | 个人创作 | 日记、回忆录 | 个人叙事 |
| 公共文化制品 | 大规模生产传播 | 新闻、社交媒体 | 话语建构 |

### 2. 内容分析

**分析维度：**
- **主题分析**：核心议题、关键词汇、议题演变
- **叙事分析**：叙事结构、主角设定、情节逻辑
- **话语分析**：语言策略、权力再现、合法性建构
- **批判阅读**：意识形态偏向、利益相关方立场、话语权力

### 3. 语境分析

**Prior (2003) 文档社会生命：**
- **生产语境**：谁生产？为什么？何时何地？
- **流通语境**：谁分发？通过什么渠道？
- **使用语境**：谁使用？如何使用？有何效果？
- **档案权力**：谁决定保存？保存标准是什么？

### 4. 批判阅读框架

**Atkinson & Coffey (2004) 四项批判原则：**

```
批判1: 文档不是现实的透明窗口
  → 任何文档都是选择性呈现

批判2: 文档是社会互动的产物
  → 理解文档产生过程才能解读其内容

批判3: 文档具有物质性
  → 载体（纸/电子/口述）影响内容

批判4: 档案具有权力效应
  → 保存什么、销毁什么反映权力关系
```

---

## ⚠️ 六大绝对禁止原则

### 1. 禁止将文档等同于现实

**错误做法**:
```yaml
透明假设:
  - "文档说了什么，现实就是什么"
  - 忽略文档的生产和流通语境
  - 将文本作为"事实"的直接证据

示例:
  "政策文件规定X，因此实际执行中X被执行了"
  （忽略了政策与实践之间的差距）
```

**正确做法**:
```yaml
批判性文档分析:
  Step 1: 识别文档类型
    - 官方/非官方？
    - 谁生产的？
    - 生产语境是什么？

  Step 2: 追踪语境
    - 生产时间地点
    - 流通渠道
    - 使用场景

  Step 3: 多源三角验证
    - 对比其他相关文档
    - 寻找矛盾和不一致
    - 结合非文档证据
```

### 2. 禁止忽视文档生产语境

**错误做法**:
```yaml
无语境分析:
  - 孤立看待文档内容
  - 不问"为什么是这个内容"
  - 不问"谁有权决定内容"

示例:
  "该报告第5页提到Y，说明Y是事实"
  （未问：谁写了报告？目的是什么？何时写的？）
```

**正确做法**:
```yaml
语境分析:
  - 文档生产者的身份和立场
  - 生产时间的历史背景
  - 生产机构的权力结构
  - 文档产生的直接原因
```

### 3. 禁止忽视文档受众

**错误做法**:
```yaml
单向视角:
  - 只分析文档"说了什么"
  - 忽略"对谁说"和"为什么说"

示例:
  "CEO年报强调员工发展，说明公司重视员工"
  （未问：年报的受众是投资者，不是员工）
```

**正确做法**:
```yaml
受众分析:
  - 文档的预期受众是谁
  - 受众如何影响内容呈现
  - 不同受众看到的是否不同
```

### 4. 禁止忽视文档的物质性

**错误做法**:
```yaml
载体忽略:
  - 假设电子版=纸质版
  - 忽略存档状态
  - 不区分版本

示例:
  "这是2019年的报告版本"
  （未问：是原始版还是修订版？是否有多版本并存？）
```

**正确做法**:
```yaml
物质性审查:
  - 记录文档的物理/数字形态
  - 记录存档位置和访问条件
  - 标注文档版本和日期
  - 记录文档的物质状态（完整/残缺/损坏）
```

### 5. 禁止忽视文档的选择性

**错误做法**:
```yaml
完整性假设:
  - 假设文档记录了"全部事实"
  - 忽略"谁决定记录什么"

示例:
  "会议纪要显示讨论了X议题"
  （未问：哪些议题没有被记录？谁有权力决定记录内容？）
```

**正确做法**:
```yaml
选择性分析:
  - 哪些内容被记录/忽略
  - 谁有权力决定选择性记录
  - 选择性记录反映了什么权力结构
  - 未被记录的内容可能同样重要
```

### 6. 禁止忽视档案权力

**错误做法**:
```yaml
档案中立假设:
  - 假设档案是客观的
  - 忽略保存/销毁的决策权

示例:
  "找不到相关记录，说明这件事没发生"
  （未问：档案的保存标准是什么？谁有权决定销毁？）
```

**正确做法**:
```yaml
档案权力分析:
  - 档案的创建标准和保留政策
  - 谁有权力决定档案的存取
  - 档案的销毁和转移历史
  - 缺失档案本身可能说明问题
```

---

## 适用场景

- ✅ 政策分析（政策文件批判性解读）
- ✅ 组织研究（内部文档分析）
- ✅ 历史研究（档案批判性使用）
- ✅ 媒体分析（新闻话语分析）
- ✅ 社会学田野（观察记录分析）
- ✅ 法律研究（法律文书分析）

---

## 实施流程

### Phase 1: 文档获取与整理

```
步骤:
  1. 识别相关文档集合
  2. 记录文档的物质状态
  3. 建立文档清单（metadata）
  4. 分类文档类型
```

### Phase 2: 初步分析

```
使用 document_classifier.py:
  python tools/document_classifier.py -i data/documents/ -o results/classification.json

  输出: 每个文档的类型标签 + 置信度
```

### Phase 3: 内容深度分析

```
使用 content_structure_analyzer.py:
  python tools/content_structure_analyzer.py \
    -i results/classified_doc.txt \
    -o results/structure.json \
    --mode theme,narrative,discourse

  输出: 主题标签、叙事结构、话语特征
```

### Phase 4: 语境重建

```
使用 document_context_tracer.py:
  python tools/document_context_tracer.py \
    -i results/structured_doc.txt \
    -o results/context.json \
    --trace production,circulation,use

  输出: 生产者身份、生产时间、流通渠道、使用场景
```

### Phase 5: 批判综合

```
综合以上分析:
  1. 识别文档的类型特征
  2. 分析内容的选择性呈现
  3. 重建生产和流通语境
  4. 识别档案权力关系
  5. 与其他证据源交叉验证
```

---

## 质量标准

**分析完整性：**
- ✅ 每份文档有类型标注
- ✅ 每份文档有语境记录
- ✅ 内容分析有原文引文支撑
- ✅ 批判性反思有记录

**方法论合规：**
- ✅ 基于Scott (1990)四类文档模型
- ✅ 体现Prior (2003)的社会生命视角
- ✅ 遵循Atkinson & Coffey (2004)批判原则
- ✅ 有多源交叉验证

---

*Document Analysis Expert v2.0.0 — SocienceAI*
*理论基础: Scott 1990 · Prior 2003 · Atkinson & Coffey 2004 · Silverman 2021*