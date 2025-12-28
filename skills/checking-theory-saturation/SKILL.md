---
name: checking-theory-saturation
description: 当用户需要检验扎根理论饱和度，包括新概念识别、范畴完善度、关系充分性和理论完整性评估时使用此技能
version: 1.0.0
author: socienceAI.com
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

## 脚本调用时机
当需要执行理论饱和度检验时，调用对应的脚本：
- 概念饱和检验：`assess_concept_saturation.py`
- 范畴饱和检验：`assess_category_saturation.py`
- 关系饱和检验：`assess_relationship_saturation.py`
- 理论饱和检验：`assess_theory_saturation.py`
- 综合饱和度判断：`make_saturation_judgment.py`

## 统一输入格式
```json
{
  "saturation_context": {
    "research_topic": "研究主题",
    "current_coding_stage": "当前编码阶段",
    "theoretical_perspective": "理论视角",
    "saturation_purpose": "饱和度检验目的"
  },
  "input_data": {
    "existing_theory": {
      "concepts": [
        {
          "id": "概念ID",
          "name": "概念名称",
          "frequency": "出现频率",
          "last_appearance": "最后出现位置"
        }
      ],
      "categories": [
        {
          "id": "范畴ID",
          "name": "范畴名称",
          "attributes": ["属性列表"],
          "dimensions": ["维度列表"],
          "relationships": ["关系列表"]
        }
      ],
      "relationships": [
        {
          "id": "关系ID",
          "from": "源概念/范畴ID",
          "to": "目标概念/范畴ID",
          "type": "关系类型",
          "strength": "关系强度(0-1)"
        }
      ],
      "theoretical_framework": "理论框架描述"
    },
    "new_data": [
      {
        "id": "新数据ID",
        "content": "新数据内容",
        "type": "数据类型",
        "source": "数据来源"
      }
    ],
    "saturation_criteria": {
      "concept_threshold": 0.05,
      "category_threshold": 0.90,
      "relationship_threshold": 0.10,
      "theory_threshold": 0.90
    }
  },
  "analysis_parameters": {
    "confidence_level": 0.95,
    "statistical_significance": 0.05,
    "minimum_sample_size": 10
  }
}
```

## 统一输出格式
```json
{
  "summary": {
    "saturation_level": "fully_saturated|partially_saturated|not_saturated",
    "overall_saturation_score": "总体饱和度分数(0-1)",
    "confidence_level": "置信度(0-1)",
    "concepts_emerging_rate": "新概念出现率(0-1)",
    "categories_development_score": "范畴发展分数(0-1)",
    "processing_time": "处理时间(秒)"
  },
  "details": {
    "concept_saturation": {
      "new_concepts_identified": [
        {
          "id": "新概念ID",
          "name": "新概念名称",
          "significance": "重要性(0-1)",
          "data_source": "数据来源"
        }
      ],
      "new_concepts_count": "新概念数量",
      "average_per_dataset": "每份数据平均新概念数",
      "significance_level": "重要性水平(high/medium/low)",
      "trend_analysis": "趋势分析"
    },
    "category_saturation": {
      "attributes_completeness": "属性完整度(0-1)",
      "dimensions_coverage": "维度覆盖度(0-1)",
      "relations_stability": "关系稳定性(0-1)",
      "category_maturity_scores": {
        "category_id": "成熟度分数(0-1)"
      }
    },
    "relationship_saturation": {
      "new_relationships_count": "新关系数",
      "relationships_stability": "关系稳定性(0-1)",
      "network_completeness": "网络完整度(0-1)",
      "new_relationships": [
        {
          "id": "新关系ID",
          "from": "源概念/范畴ID",
          "to": "目标概念/范畴ID",
          "type": "关系类型",
          "significance": "重要性(0-1)"
        }
      ]
    },
    "theory_saturation": {
      "explanation_coverage": "解释覆盖度(0-1)",
      "internal_consistency": "内部一致性(0-1)",
      "phenomena_explained_count": "解释现象数",
      "theory_maturity": "理论成熟度(0-1)"
    },
    "statistical_analysis": {
      "confidence_interval": "置信区间",
      "statistical_significance": "统计显著性",
      "sample_size": "样本量",
      "effect_size": "效应量"
    }
  },
  "recommendations": {
    "continue_data_collection": "是否继续收集数据(true/false)",
    "focus_areas": ["需要关注的领域列表"],
    "next_steps": ["下一步建议列表"],
    "data_collection_strategy": "数据收集策略建议"
  },
  "metadata": {
    "timestamp": "时间戳",
    "version": "版本号",
    "skill": "checking-theory-saturation",
    "analysis_method": "分析方法"
  }
}
```

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