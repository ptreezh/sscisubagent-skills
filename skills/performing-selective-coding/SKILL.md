---
name: performing-selective-coding
description: 当用户需要执行扎根理论的选择式编码，包括核心范畴识别、故事线构建、理论框架整合和理论饱和度检验时使用此技能
version: 1.0.0
author: socienceAI.com
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

## 使用时机

当用户提到以下需求时，使用此技能：
- "选择式编码" 或 "执行选择式编码"
- "核心范畴识别" 或 "寻找核心概念"
- "故事线构建" 或 "构建故事线"
- "理论框架" 或 "理论模型"
- "理论饱和度" 或 "饱和度检验"
- 需要整合所有范畴构建核心理论

## 脚本调用时机
当需要执行选择式编码的不同阶段时，调用对应的脚本：
- 核心范畴识别：调用 `identify_core_category.py`
- 故事线构建：调用 `construct_storyline.py`
- 理论框架整合：调用 `integrate_theory.py`
- 理论饱和度检验：调用 `check_saturation.py`

## 统一输入格式
```json
{
  "coding_context": {
    "research_topic": "研究主题",
    "previous_coding_stages": ["开放编码", "轴心编码"],
    "theoretical_perspective": "理论视角",
    "coding_purpose": "编码目的"
  },
  "input_data": {
    "categories": [
      {
        "id": "范畴ID",
        "name": "范畴名称",
        "definition": "范畴定义",
        "type": "范畴类型(核心/次要)",
        "concepts": ["概念ID列表"],
        "properties": "范畴属性"
      }
    ],
    "relationships": [
      {
        "id": "关系ID",
        "from_category": "源范畴ID",
        "to_category": "目标范畴ID",
        "type": "关系类型",
        "strength": "关系强度(0-1)"
      }
    ],
    "axial_codes": "轴心编码结果",
    "paradigm_models": ["Paradigm模型列表"]
  },
  "coding_parameters": {
    "core_category_criteria": {
      "explanatory_power": "解释力权重",
      "connectivity": "连接度权重",
      "data_support": "数据支持权重"
    },
    "saturation_thresholds": {
      "new_concept_rate": 0.05,
      "category_completion": 0.90,
      "relationship_rate": 0.10,
      "theory_completion": 0.90
    }
  }
}
```

## 统一输出格式
```json
{
  "summary": {
    "core_category": "核心范畴名称",
    "saturation_score": "饱和度分数(0-1)",
    "propositions_count": "理论命题数量",
    "is_fully_saturated": "是否完全饱和",
    "processing_time": "处理时间(秒)"
  },
  "details": {
    "core_category_analysis": {
      "id": "核心范畴ID",
      "name": "核心范畴名称",
      "definition": "核心范畴定义",
      "explanatory_power": "解释力(0-1)",
      "connectivity": "连接度(0-1)",
      "data_support": "数据支持度(0-1)",
      "rationale": "选择理由",
      "related_categories": ["相关范畴ID列表"]
    },
    "storyline": {
      "central_narrative": "中心叙事",
      "key_elements": {
        "actors": ["主要行动者"],
        "events": ["关键事件"],
        "processes": ["核心过程"],
        "outcomes": ["结果"]
      },
      "causal_chains": ["因果链条"],
      "chronological_order": "时间顺序"
    },
    "theory_framework": {
      "theoretical_propositions": [
        {
          "id": "命题ID",
          "statement": "命题陈述",
          "categories_involved": ["涉及范畴"],
          "mechanism": "作用机制"
        }
      ],
      "conceptual_model": "概念模型描述",
      "boundary_conditions": "边界条件",
      "scope": "理论适用范围"
    },
    "saturation_report": {
      "new_concept_rate": "新概念率",
      "category_completion": "范畴完成度",
      "new_relationship_rate": "新关系率",
      "theory_completion": "理论完成度",
      "saturation_status": "饱和状态评估",
      "additional_data_needed": "是否需要更多数据"
    },
    "statistics": {
      "theoretical_integration": "理论整合度",
      "framework_coherence": "框架一致性",
      "conceptual_density": "概念密度"
    }
  },
  "metadata": {
    "timestamp": "时间戳",
    "version": "版本号",
    "skill": "performing-selective-coding",
    "processing_stage": "处理阶段"
  }
}
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