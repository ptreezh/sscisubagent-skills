---
name: grounded-theory-expert
description: 扎根理论专家分析技能，整合开放编码、轴心编码、选择式编码、备忘录撰写和理论饱和度检验功能，提供完整的扎根理论分析框架
version: 1.0.0
author: socienceAI.com
license: MIT
tags: [grounded-theory, open-coding, axial-coding, selective-coding, memo-writing, saturation-analysis, qualitative-research]
compatibility: Claude 3.5 Sonnet and above
metadata:
  domain: qualitative-research
  methodology: grounded-theory
  complexity: advanced
  integration_type: analysis_tool
  last_updated: "2025-12-27"
allowed-tools: [python, bash, read_file, write_file]
---

# 扎根理论专家分析技能 (Grounded Theory Expert Analysis)

## 概述

扎根理论专家分析技能整合了开放编码、轴心编码、选择式编码、备忘录撰写和理论饱和度检验功能，为质性研究提供完整的扎根理论分析框架。该技能帮助研究者从原始数据中系统性地构建理论。

## 使用时机

当用户请求以下分析时使用此技能：
- 扎根理论研究的完整流程
- 从原始数据到理论构建的全过程
- 开放编码、轴心编码、选择式编码的连续分析
- 理论饱和度的系统检验
- 扎根理论备忘录的撰写和管理
- 中文质性数据的扎根理论分析

## 快速开始

当用户请求扎根理论分析时：
1. **开放编码**：概念识别和初始编码
2. **轴心编码**：范畴构建和关系建立
3. **选择式编码**：核心范畴和理论构建
4. **饱和度检验**：理论完整性的验证
5. **备忘录撰写**：过程记录和理论反思

## 核心功能（渐进式披露）

### 主要功能
- **开放编码**: 概念识别和初始编码
- **轴心编码**: 范畴构建和关系建立
- **选择式编码**: 核心范畴和理论构建
- **饱和度检验**: 理论完整性的验证

### 次要功能
- **备忘录撰写**: 过程记录和理论反思
- **数据管理**: 质性数据的组织和管理
- **质量检查**: 扎根理论分析的质量控制
- **理论评估**: 构建理论的有效性评估

### 高级功能
- **跨阶段整合**: 不同编码阶段的整合分析
- **理论验证**: 构建理论的验证和修正
- **多数据源分析**: 多个数据源的整合分析
- **理论比较**: 不同理论框架的比较分析

## 详细指令

### 第一阶段：开放编码
   - 准备质性数据进行编码
   - 识别初始概念和现象
   - 逐行或逐段编码数据
   - 在不同数据段间进行持续比较
   - 开发初始理论概念并撰写备忘录

### 第二阶段：轴心编码
   - 将开放编码的概念整合为范畴
   - 分析每个范畴的属性和维度
   - 建立范畴间的逻辑关系
   - 构建Paradigm模型（条件-情境-行动-结果）
   - 验证范畴系统的连贯性

### 第三阶段：选择式编码
   - 从所有范畴中识别核心范畴
   - 构建连接所有主要范畴的中心故事线
   - 将轴心编码构建的范畴体系整合为理论框架
   - 评估理论饱和度
   - 提炼理论命题并完善理论

### 第四阶段：饱和度检验
   - 分析新数据中是否出现新概念
   - 评估范畴发展的完整性
   - 检查概念关系的稳定性
   - 验证理论解释的充分性
   - 确定是否需要更多数据

### 第五阶段：备忘录撰写
   - 记录编码过程和思考
   - 进行理论反思和分析
   - 撰写理论备忘录
   - 记录研究发现和洞察
   - 保存研究过程的思考

### 第六阶段：综合与解释
   - 整合所有阶段的发现
   - 将扎根理论与更广泛的研究问题联系
   - 考虑中国研究背景和文化特殊性
   - 提供可操作的理论见解

## 参数
- `coding_stage`: 编码阶段 (open, axial, selective, saturation, memo)
- `data_source`: 数据来源 (interviews, observations, documents)
- `analysis_scope`: 分析范围 (narrow, medium, broad)
- `saturation_level`: 饱和度水平 (low, medium, high)
- `memo_type`: 备忘录类型 (process, theory, reflection, operational)
- `methodology`: 分析方法 (qualitative, mixed)
- `cultural_context`: 文化背景考虑 (特别是中文研究背景)

## 示例

### 示例 1: 教育研究
User: "分析中国大学生学习适应的扎根理论"
Response: 执行开放编码识别概念，轴心编码构建范畴，选择式编码形成核心理论，检验理论饱和度。

### 示例 2: 组织研究
User: "研究中国企业数字化转型的扎根理论"
Response: 概念识别，范畴构建，核心理论形成，饱和度验证，理论备忘录撰写。

### 示例 3: 社会现象研究
User: "探索中国城市社区治理的扎根理论"
Response: 开放编码，轴心编码，选择式编码，饱和度检验，完整理论框架构建。

## 质量标准

- 严格应用扎根理论方法论
- 保持编码的系统性和一致性
- 考虑中国研究语境的特殊性
- 提供基于证据的理论构建
- 确保理论的饱和度和完整性

## 输出格式

```json
{
  "summary": {
    "coding_stage": "selective",
    "concepts_identified": 45,
    "categories_developed": 8,
    "core_category": "Academic Adaptation Challenges",
    "saturation_level": 0.92,
    "theoretical_propositions": 6
  },
  "details": {
    "open_coding": {...},
    "axial_coding": {...},
    "selective_coding": {...},
    "saturation_analysis": {...},
    "memo_analysis": {...}
  },
  "metadata": {
    "timestamp": "2025-12-27T10:30:00",
    "version": "1.0.0"
  }
}
```

## 资源
- 扎根理论方法论文献
- 扎根理论分析指南
- 中国语境下的质性研究文献
- 扎根理论分析示例

## 完成标志

完成高质量的扎根理论分析应包括：
1. 完整的三级编码过程
2. 系统的理论构建
3. 充分的饱和度证明
4. 详细的备忘录记录
5. 清晰的理论贡献

---

*此技能为质性研究提供专业的综合扎根理论分析框架和工具，确保研究的科学性和严谨性。*