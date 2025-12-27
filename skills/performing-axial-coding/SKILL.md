---
name: performing-axial-coding
description: 当用户需要执行扎根理论的轴心编码，包括范畴识别、属性维度分析、关系建立和Paradigm模型构建时使用此技能
version: 1.0.0
author: chinese-social-sciences-subagents
tags: [grounded-theory, axial-coding, category-analysis, paradigm-model, qualitative-research]
---

# 轴心编码技能 (Performing Axial Coding)

## Overview
专门用于扎根理论研究的轴心编码阶段，将开放编码产生的概念整合为系统性的范畴体系，并建立范畴间的逻辑关系。

## When to Use This Skill
Use this skill when the user requests:
- Integration of open coding concepts into categories
- Identification of category properties and dimensions
- Establishment of relationships between categories
- Construction of paradigm models (conditions-context-actions-outcomes)
- Development of theoretical frameworks from coded data
- Systematic approach to mid-stage qualitative analysis
- Chinese qualitative data analysis following grounded theory principles

## Quick Start
When a user requests axial coding:
1. **Group** related concepts from open coding into categories
2. **Analyze** properties and dimensions of each category
3. **Establish** relationships between categories
4. **Construct** paradigm models linking categories
5. **Validate** the coherence of the category system

## 使用时机

当用户提到以下需求时，使用此技能：
- "轴心编码" 或 "执行轴心编码"
- "范畴构建" 或 "概念归类"
- "属性维度分析" 或 "维度分析"
- "范畴关系" 或 "概念关系"
- "Paradigm构建" 或 "范式构建"
- 需要将开放编码结果整合为理论框架

## 快速开始

### 工具链（4个核心脚本）

```bash
# 1. 范畴识别（从开放编码结果）
python scripts/identify_categories.py --input codes.json --output categories.json

# 2. 属性分析（可选）
python scripts/analyze_properties.py --input categories.json --output properties.json

# 3. 关系建立
python scripts/build_relationships.py --input categories.json --output relationships.json

# 4. Paradigm构建
python scripts/construct_paradigm.py --input relationships.json --output paradigm.json
```

## 核心流程

### 第一步：范畴识别

**使用工具自动聚类**：
```bash
python scripts/identify_categories.py --input codes.json --output categories.json
```

**定性精炼**：
- 检查范畴内部一致性
- 调整范畴命名（行动导向）
- 完善范畴定义
- 建立层级结构（核心/次要）

详见：`references/category-examples.md`

### 第二步：属性维度分析（可选）

**使用工具分析属性**：
```bash
python scripts/analyze_properties.py --input categories.json --output properties.json
```

**定性分析**：
- 识别范畴的核心属性
- 定义属性的变化维度
- 在维度上定位案例

详见：`references/paradigm-theory.md` - 属性维度理论

### 第三步：关系建立

**使用工具识别关系**：
```bash
python scripts/build_relationships.py --input categories.json --output relationships.json
```

**关系类型**：
- 因果关系：A导致B
- 条件关系：当A时B发生
- 策略关系：通过A达成B
- 互动关系：A与B相互影响

**定性判断**：
- 验证关系的证据充分性
- 确定关系的方向和强度
- 分析关系的理论意义

详见：`references/relationship-types.md` - 关系类型详解

### 第四步：Paradigm构建

**使用工具构建模型**：
```bash
python scripts/construct_paradigm.py --input relationships.json --output paradigm.json
```

**Paradigm组件**：
- 现象：核心研究现象
- 条件：导致现象的因素
- 行动：应对现象的策略
- 结果：行动的后果

**定性整合**：
- 验证逻辑链条完整性
- 确认模型理论意义
- 撰写理论备忘录

详见：`references/paradigm-theory.md` - Paradigm模型详解

## 输出格式

统一的三层JSON格式：
```json
{
  "summary": {
    "total_categories": 8,
    "core_categories": 3,
    "total_relations": 12,
    "paradigm_completeness": 0.85
  },
  "details": {
    "categories": [...],
    "relationships": [...],
    "paradigm": {...}
  }
}
```

## 质量检查标准

在完成轴心编码后，请检查以下项目：

### 范畴构建质量
- [ ] 范畴命名准确且有意义
- [ ] 范畴定义清晰完整
- [ ] 概念归类合理有据
- [ ] 范畴层级结构清晰
- [ ] 范畴间区分度明确

### 属性维度质量
- [ ] 属性识别全面准确
- [ ] 维度定义合理
- [ ] 维度范围适当
- [ ] 案例定位准确
- [ ] 分布分析科学

### 关系建立质量
- [ ] 关系类型判断准确
- [ ] 关系强度评估合理
- [ ] 关系证据充分
- [ ] 关系方向正确
- [ ] 关系网络完整

### Paradigm构建质量
- [ ] 条件识别完整
- [ ] 行动描述准确
- [ ] 结果分析全面
- [ ] 逻辑链条清晰
- [ ] 理论意义明确

## 常见问题

**快速诊断**：
- 范畴过于宽泛 → 使用 `identify_categories.py` 增加聚类数
- 概念归属不明确 → 见 `references/troubleshooting.md`
- 关系论证不充分 → 使用 `build_relationships.py` 查看证据计数
- Paradigm不完整 → 使用 `construct_paradigm.py` 检查完整度

## 深入学习

- **Paradigm理论**：`references/paradigm-theory.md` - Strauss模型详解
- **范畴案例**：`references/category-examples.md` - 完整构建过程
- **关系类型**：`references/relationship-types.md` - 四种关系详解
- **故障排除**：`references/troubleshooting.md` - 问题诊断

## 完成标志

完成轴心编码后应该产出：
1. 系统性的范畴体系
2. 详细的属性维度分析
3. 完整的范畴关系网络
4. 清晰的Paradigm理论模型

---

*此技能为中文扎根理论研究的轴心编码阶段提供完整指导，确保从概念到范畴的科学转化和理论建构。*