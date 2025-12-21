---
name: performing-selective-coding
description: 执行扎根理论的选择式编码过程，包括核心范畴识别、故事线构建、理论框架整合和理论饱和度检验。当需要整合所有范畴构建核心理论，形成完整的故事线和理论模型时使用此技能。
version: 1.0.0
author: chinese-social-sciences-subagents
tags: [grounded-theory, selective-coding, core-category, theory-integration, saturation-assessment]
---

# 选择式编码技能 (Performing Selective Coding)

## Overview
专门用于扎根理论研究的选择式编码阶段，将轴心编码构建的范畴体系整合为系统的理论框架，形成核心理论和故事线。

## When to Use This Skill
Use this skill when the user requests:
- Integration of all categories into a core theory
- Identification of the core category in grounded theory
- Construction of a storyline linking all major categories
- Integration of axial codes into a theoretical framework
- Assessment of theoretical saturation
- Development of theoretical propositions from grounded analysis
- Theory generation and refinement in Chinese research context
- Synthesis of grounded theory findings into coherent whole

## Quick Start
When a user requests selective coding:
1. **Identify** the core category among all categories
2. **Construct** the central storyline linking categories
3. **Integrate** the theory with all components
4. **Validate** the theoretical saturation
5. **Refine** and articulate the complete theory

## Core Functions (Progressive Disclosure)

### Primary Functions
- **Core Category Identification**: Identify the central organizing category among all categories
- **Storyline Construction**: Build the central narrative linking all major categories
- **Basic Integration**: Integrate axial codes into preliminary framework
- **Saturation Assessment**: Evaluate the extent of theoretical saturation

### Secondary Functions
- **Theoretical Proposition Development**: Formulate theoretical propositions from integrated analysis
- **Framework Refinement**: Refine the theoretical framework and its components
- **Relationship Synthesis**: Synthesize relationships across all categories
- **Model Validation**: Validate the emerging theoretical model

### Advanced Functions
- **Complex Theory Integration**: Integrate multiple theoretical perspectives
- **Cross-case Synthesis**: Synthesize findings across multiple cases
- **Advanced Proposition Refinement**: Develop complex theoretical propositions
- **Theory Validation and Testing**: Validate theory against additional data

## Detailed Instructions

### 1. Core Category Selection
   - Apply systematic criteria for core category identification
   - Evaluate the explanatory power of potential core categories
   - Assess the frequency and centrality of categories in data
   - Determine the connection to other categories and concepts
   - Validate the core category's relevance to research questions

### 2. Storyline Construction
   - Develop a coherent narrative that links all major categories
   - Identify the central process or phenomenon in the story
   - Map the temporal sequence of events and processes
   - Establish the relationships between different elements of the story
   - Ensure logical flow and internal consistency

### 3. Theoretical Framework Integration
   - Integrate axial codes into a unified theoretical framework
   - Develop propositions linking major categories
   - Create a coherent model of relationships and processes
   - Ensure theoretical consistency and coherence
   - Consider Chinese cultural and social contexts

### 4. Saturation Verification
   - Assess whether theoretical saturation has been reached
   - Determine if additional data would yield new insights
   - Evaluate the completeness of the theoretical framework
   - Verify that all major relationships are understood
   - Consider whether all relevant contexts have been explored

### 5. Model Refinement
   - Refine theoretical propositions based on synthesis
   - Adjust relationships and connections in the model
   - Address inconsistencies or gaps in the theory
   - Ensure the model is parsimonious yet comprehensive
   - Validate the model against additional data if available

### 6. Validation and Testing
   - Test the theory against alternative explanations
   - Verify the theory's applicability to new cases
   - Assess the theory's predictive and explanatory power
   - Consider the theory's transferability to other contexts
   - Evaluate the theory's contribution to existing knowledge

### 7. Theory Articulation
   - Clearly articulate the core theoretical insights
   - Develop clear and accessible theoretical statements
   - Consider implications for practice and policy
   - Identify areas for future research
   - Ensure the theory addresses the original research questions

## Parameters
- `selection_criteria`: Criteria for selecting the core category (explanatory power, frequency, centrality, etc.)
- `storyline_focus`: Focus of the central narrative (process, relationship, structure, etc.)
- `integration_depth`: Depth of theoretical integration (basic, comprehensive, advanced)
- `saturation_threshold`: Threshold for determining theoretical saturation
- `validation_approach`: Approach to theory validation (empirical, logical, comparative)
- `cultural_context`: Cultural context considerations (especially for Chinese context)
- `methodology`: Approach to selective coding (Straussian, Glaserian, etc.)

## Examples

### Example 1: Educational Research
User: "Integrate my axial coding results into a core theory about student engagement"
Response: Identify core category, construct engagement storyline, integrate into theoretical framework, validate saturation.

### Example 2: Organizational Study
User: "Build a central theory from my organizational change categories"
Response: Identify core change category, construct change process storyline, integrate into theoretical model.

### Example 3: Health Research
User: "Synthesize my categories into a theory about patient care experiences"
Response: Determine core category, build care experience storyline, develop comprehensive theoretical framework.

## Quality Standards

- Apply selective coding principles rigorously
- Ensure the core category truly organizes the theory
- Maintain consistency between categories and storyline
- Validate theoretical saturation appropriately
- Consider Chinese cultural and social contexts

## Output Format

- Complete selective coding report
- Identified core category with justification
- Central storyline narrative
- Integrated theoretical framework
- Saturation assessment and validation
- Theoretical propositions and model
- Recommendations for future research

## Resources
- Grounded theory methodology literature
- Selective coding technique guides
- Examples of theory integration in Chinese context
- Theory validation and testing resources

## Metadata
- Compatibility: Claude 3.5 Sonnet and above
- Domain: Qualitative Research, Grounded Theory
- Language: Optimized for Chinese research context

## 使用时机

当用户提到以下需求时，使用此技能：
- "选择式编码" 或 "执行选择式编码"
- "核心范畴识别" 或 "寻找核心概念"
- "故事线构建" 或 "构建故事线"
- "理论框架" 或 "理论模型"
- "理论饱和度" 或 "饱和度检验"
- 需要整合所有范畴构建核心理论

## 快速开始

### 工具链（4个核心脚本）

```bash
# 第一步：识别核心范畴
python scripts/identify_core_category.py \
  --input categories.json \
  --relations relationships.json \
  --output core_category.json

# 第二步：构建故事线
python scripts/construct_storyline.py \
  --input data.json \
  --categories categories.json \
  --relations relationships.json \
  --output storyline.json

# 第三步：整合理论框架
python scripts/integrate_theory.py \
  --categories categories.json \
  --relations relationships.json \
  --output theory.json

# 第四步：检验饱和度
python scripts/check_saturation.py \
  --existing theory.json \
  --new new_data.json \
  --output saturation.json
```

## 核心流程

### 第一步：核心范畴识别

**使用工具自动评估**：
- 计算解释力（能解释多少数据）
- 计算连接度（与多少范畴相关）
- 计算数据支持（有多少证据）
- 综合评分并排序

**定性验证**：
- 检查是否能统领其他范畴
- 验证与研究问题的契合度

详见：`references/core-category/INDEX.md`

---

### 第二步：故事线构建

**使用工具辅助**：
- 提取时间线和关键事件
- 识别行动者和角色
- 构建因果链条

**人工精炼**：
- 形成连贯的叙述
- 确保逻辑性和说服力

详见：`references/storyline/INDEX.md`

---

### 第三步：理论框架整合

**使用工具生成**：
- 提炼理论命题
- 构建概念框架
- 解释作用机制

**定性完善**：
- 确保逻辑严谨
- 明确理论边界

详见：`references/theory-integration/INDEX.md`

---

### 第四步：理论饱和度检验

**使用工具检验**：
- 检查新概念出现率
- 检查范畴完整性
- 检查关系稳定性
- 评估理论完整性

**判断标准**：
- 新概念率 < 5%
- 范畴完整性 ≥ 90%
- 新关系率 < 10%
- 理论完整性 ≥ 90%

详见：`references/saturation/INDEX.md`

## 输出格式

统一的三层JSON格式：

```json
{
  "summary": {
    "core_category": "学业适应困难",
    "saturation_score": 0.92,
    "propositions_count": 8,
    "is_fully_saturated": true
  },
  "details": {
    "core_category_analysis": {...},
    "storyline": {...},
    "theory_framework": {...},
    "saturation_report": {...}
  }
}
```

## 质量检查标准

在完成选择式编码后，请检查以下项目：

### 核心范畴质量
- [ ] 核心范畴具有最强解释力
- [ ] 核心范畴与多数范畴相关
- [ ] 核心范畴有充分数据支持
- [ ] 核心范畴理论价值明确

### 故事线质量
- [ ] 故事线逻辑清晰连贯
- [ ] 包含所有重要元素
- [ ] 因果关系明确
- [ ] 具有说服力和完整性

### 理论框架质量
- [ ] 理论命题逻辑严谨
- [ ] 概念框架系统完整
- [ ] 作用机制解释清晰
- [ ] 边界条件明确

### 饱和度质量
- [ ] 理论达到充分饱和
- [ ] 数据支持充分
- [ ] 关系识别完整
- [ ] 理论价值明确

## 常见问题

**快速诊断**：
- 难以确定核心范畴 → 使用 `identify_core_category.py` 量化评估
- 故事线不连贯 → 见 `references/storyline/INDEX.md`
- 理论框架复杂 → 见 `references/theory-integration/INDEX.md`
- 理论未达饱和 → 使用 `check_saturation.py` 检验维度

## 深入学习

- **核心范畴理论**：`references/core-category/INDEX.md` - 选择标准详解
- **故事线构建**：`references/storyline/INDEX.md` - 叙事方法
- **理论整合**：`references/theory-integration/INDEX.md` - 命题提炼
- **饱和度检验**：`references/saturation/INDEX.md` - 判断标准

## 完成标志

完成高质量的选择式编码应该产出：
1. 明确的核心范畴
2. 完整的故事线
3. 系统的理论框架
4. 充分的饱和度证明
5. 清晰的理论贡献

---

*此技能为扎根理论研究的选择式编码阶段提供完整指导，确保从范畴体系到核心理论的科学转化和理论建构。*