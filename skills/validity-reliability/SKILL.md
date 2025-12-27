---
name: validity-reliability
description: 当用户需要执行研究信度效度分析，包括内部一致性、重测信度、评分者信度、构念效度、内容效度、效标效度等全面分析时使用此技能
version: 1.0.0
author: chinese-social-sciences-subagents
license: MIT
tags: [reliability, validity, research-methods, psychometrics, measurement, scale-validation]
compatibility: Claude 3.5 Sonnet and above
metadata:
  domain: psychometrics
  methodology: scale-validation
  complexity: advanced
  integration_type: analysis_tool
  last_updated: "2025-12-21"
allowed-tools: [python, bash, read_file, write_file]
---

# 信度效度分析技能 (Validity and Reliability Analysis)

## 概述

为社会科学研究提供全面的测量质量评估，包括信度分析（内部一致性、重测信度、评分者信度）和效度分析（内容效度、构念效度、效标效度），确保研究工具的科学性和有效性。

## 使用时机

当用户请求以下分析时使用此技能：
- 研究工具的信度分析
- 内部一致性评估（Cronbach's Alpha、Omega系数）
- 重测信度评估
- 评分者信度分析
- 测量工具的效度评估
- 内容效度评估
- 构念效度检验（EFA、CFA）
- 效标效度分析
- 量表验证的因子分析
- 量表开发和优化

## 快速开始

当用户请求信度效度评估时：
1. **评估**测量设计和数据质量
2. **评估**使用适当的信度系数
3. **检验**通过因子分析和其他方法验证效度
4. **解释**在测量理论背景下的结果
5. **建议**必要的改进措施

## 核心流程

### 第一阶段：测量设计评估
   - 审查量表结构和项目设计
   - 检查潜在的反应偏差
   - 评估项目措辞和清晰度
   - 验证反应格式的适当性

### 第二阶段：数据质量检查
   - 适当处理缺失值
   - 检测和处理离群值
   - 评估分布特征
   - 验证样本量充足性

### 第三阶段：信度分析
   - 计算各种信度系数
   - 评估置信区间
   - 识别有问题的项目
   - 评估维度性

### 第四阶段：效度验证
   - 进行因子分析（EFA/CFA）
   - 检验聚合和区分效度
   - 评估准则相关效度
   - 评估内容效度证据

### 第五阶段：质量改进建议
   - 提出具体的量表改进建议
   - 建议项目修订或删除
   - 提出额外的验证研究
   - 提供报告指南

## 输出格式

```json
{
  "summary": {
    "cronbach_alpha": 0.87,
    "omega_coefficient": 0.89,
    "ave_convergent": 0.62,
    "discriminant_validity": true,
    "model_fit_cfi": 0.94,
    "model_fit_rmsea": 0.06
  },
  "details": {
    "reliability_analysis": {...},
    "validity_analysis": {...},
    "factor_structure": {...},
    "item_statistics": {...}
  },
  "metadata": {
    "timestamp": "2025-12-21T10:30:00",
    "version": "1.0.0"
  }
}
```

## 质量标准

- 遵循心理测量学最佳实践
- 提供APA格式的统计报告
- 包含效应量和置信区间
- 在适当时候进行多重比较校正
- 验证模型假设条件

## 深入学习

- 心理测量学最佳实践
- 量表开发和验证指南
- 信度效度分析的统计软件语法
- 因子分析和结构方程建模方法

## 完成标志

完成高质量的信度效度分析应包括：
1. 完整的信度和效度分析报告
2. 标准化的统计表格
3. 因子结构可视化
4. 测量模型路径图
5. 可重现的分析代码

---

*此技能为中文社会科学研究提供全面的信度效度分析支持，确保测量工具的科学性和可靠性。*