---
name: checking-theory-saturation
description: 当用户需要检验扎根理论饱和度，包括新概念识别、范畴完善度、关系充分性和理论完整性评估时使用此技能
version: 1.0.0
author: chinese-social-sciences-subagents
tags: [grounded-theory, saturation-analysis, qualitative-research, concept-identification, category-development]
---

# 理论饱和度检验技能 (Checking Theory Saturation)

## Overview
为扎根理论研究提供科学、系统的理论饱和度检验，确保理论构建的完整性和可靠性。

## When to Use This Skill
Use this skill when the user requests:
- Assessment of theoretical saturation in grounded theory
- Determination of whether new concepts are still emerging
- Evaluation of category development completeness
- Checking if sufficient data has been collected
- Validation of theoretical framework completeness
- Decision-making about ending data collection
- Assessment of concept, category, and theory sufficiency
- Evaluation of theoretical explanation adequacy

## Quick Start
When a user requests saturation assessment:
1. **Analyze** new data for emerging concepts
2. **Evaluate** category development completeness
3. **Assess** relationship network stability
4. **Validate** theoretical explanation adequacy
5. **Determine** if additional data is needed

## 使用时机

当用户提到以下需求时，使用此技能：
- "理论饱和度" 或 "饱和度检验"
- "理论是否饱和" 或 "检查饱和度"
- "需要更多数据" 或 "补充数据"
- "可以结束研究" 或 "研究完成度"
- "理论完整性" 或 "理论完善度"
- 需要评估理论构建的充分性

## 快速开始

### 检验流程
1. **概念饱和检验**：分析新数据中是否出现新概念
2. **范畴饱和检验**：评估范畴属性和维度的发展充分性
3. **关系饱和检验**：检查概念间关系的稳定性
4. **理论饱和检验**：验证理论框架的完整性
5. **综合判断**：基于多维度证据做出饱和度判断

### 判断标准
- **概念层面**：连续分析多份数据无新概念出现
- **范畴层面**：范畴属性和维度发展充分
- **关系层面**：关系网络稳定且完整
- **理论层面**：理论能解释所有重要现象

## 核心流程

### 第一步：概念饱和评估
1. **新概念识别**：分析新数据中是否出现新概念
2. **概念重要性评估**：评估新概念对理论的贡献
3. **概念抽象层次检查**：验证概念抽象层次适当性
4. **概念频率统计**：计算新概念出现频率

### 第二步：范畴饱和评估
1. **属性完整性检查**：评估范畴属性发展充分性
2. **维度完整性检查**：评估范畴维度覆盖全面性
3. **范畴间关系稳定性**：检查范畴关系是否稳定
4. **范畴定义清晰度**：验证范畴边界清晰性

### 第三步：关系饱和评估
1. **新关系识别**：检查是否出现新概念关系
2. **关系稳定性**：验证现有关系是否稳定
3. **关系强度评估**：评估关系强度合理性
4. **关系网络完整性**：检查关系网络覆盖完整性

### 第四步：理论饱和评估
1. **解释覆盖度**：验证理论解释现象的全面性
2. **理论一致性**：检查理论内部逻辑一致性
3. **理论贡献度**：评估理论的学术贡献
4. **理论适用性**：验证理论的实践适用性

### 第五步：综合判断
1. **多维度证据整合**：整合各层面饱和度证据
2. **饱和度信心评估**：评估饱和度判断的信心水平
3. **后续步骤建议**：提供是否继续收集数据的建议
4. **质量保证措施**：实施饱和度验证措施

## 输出格式

```json
{
  "summary": {
    "saturation_level": "fully_saturated|partially_saturated|not_saturated",
    "confidence_level": 0.85,
    "concepts_emerging_rate": 0.05,
    "categories_development_score": 0.92
  },
  "details": {
    "concept_saturation": {
      "new_concepts_recent": 2,
      "average_per_data_set": 0.3,
      "significance_level": "low"
    },
    "category_saturation": {
      "attributes_completeness": 0.88,
      "dimensions_coverage": 0.91,
      "relations_stability": 0.94
    },
    "theory_saturation": {
      "explanation_coverage": 0.95,
      "internal_consistency": 0.89,
      "phenomena_explained": 23
    }
  },
  "recommendations": {
    "continue_data_collection": false,
    "focus_areas": ["minor_refinements"],
    "next_steps": ["proceed_to_selective_coding"]
  }
}
```

## 质量标准

- 采用多维度饱和度评估方法
- 基于充分证据进行饱和度判断
- 考虑中国研究语境的特殊性
- 提供明确的后续步骤建议

## 深入学习

- 扎根理论方法论文献
- 理论饱和度评估指南
- 中国语境下的饱和度评估案例
- 质性研究质量评估资源

## 完成标志

完成理论饱和度检验后应产出：
1. 明确的饱和度判断结果
2. 详细的多维度评估报告
3. 基于证据的判断理由
4. 清晰的后续步骤建议

---

*此技能为扎根理论研究提供系统的理论饱和度检验方法，确保理论构建的科学性、完整性和可靠性。*