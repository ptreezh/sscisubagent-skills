---
name: sem-analysis-expert
description: |
  结构方程模型专家。提供SEM全流程支持，包括模型构建、测量模型分析（CFA）、结构模型分析、路径分析、模型拟合评估、修正指数分析、多群组比较和中介效应检验。适用于社会科学量化研究、问卷数据分析、理论验证和潜变量建模。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/龙虾/QClaw
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0"
  agentskills-io: "true"
  cross-platform: "true"
  methodology: "Structural Equation Modeling"
  software: "lavaan/Mplus/AMOS/semopy"
---

# SEM Analysis Expert | 结构方程模型专家

## 概述

结构方程模型专家是一个专门支持SEM分析的研究方法技能。SEM是社会科学领域最常用的高级统计方法，融合了因子分析和回归分析，能够同时处理测量误差和估计路径系数。

## 核心能力

### 1. 模型构建
- 概念模型转化为统计模型
- 潜变量定义与指标选择
- 路径关系设定
- 模型语法生成

### 2. 测量模型分析 (CFA)
- 验证性因子分析
- 因子载荷评估
- 测量误差估计
- 构念信效度检验

### 3. 结构模型分析
- 路径系数估计
- 直接效应与间接效应
- 总效应分解
- 假设检验

### 4. 模型拟合评估
- 绝对拟合指标（χ², RMSEA, SRMR）
- 相对拟合指标（CFI, TLI, NFI）
- 简约拟合指标（AIC, BIC）
- 拟合指标解释标准

### 5. 模型修正
- 修正指数(MI)分析
- 残差分析
- 模型修正建议
- 修正合理性评估

### 6. 高级分析
- 多群组比较
- 中介效应检验（Bootstrap）
- 调节效应分析
- 潜变量交互

## 模型拟合指标标准

| 指标 | 可接受 | 良好 | 优秀 |
|------|--------|------|------|
| χ²/df | < 5 | < 3 | < 2 |
| RMSEA | < 0.10 | < 0.08 | < 0.06 |
| CFI | > 0.90 | > 0.95 | > 0.97 |
| TLI | > 0.90 | > 0.95 | > 0.97 |
| SRMR | < 0.10 | < 0.08 | < 0.05 |

## 分析流程

```
理论模型 → 模型设定 → 数据准备 → 测量模型检验 → 
结构模型分析 → 模型拟合评估 → 模型修正 → 
结果解释 → 假设检验 → 报告撰写
```

## 信效度标准

### 信度指标
- **Cronbach's α**: > 0.70 可接受, > 0.80 良好
- **组合信度(CR)**: > 0.70 可接受
- **平均方差萃取(AVE)**: > 0.50 可接受

### 效度指标
- **收敛效度**: AVE > 0.50, 因子载荷 > 0.50
- **区分效度**: √AVE > 构念间相关系数

## 使用场景

1. **理论验证**：验证已建立的理论模型
2. **量表开发**：开发和验证测量工具
3. **中介效应**：检验复杂的中介机制
4. **潜变量建模**：处理不可直接观测的构念
5. **多群组比较**：检验模型跨群组稳定性

## 工具函数

### Python工具

- `model_builder.py` - 模型构建工具
- `cfa_analyzer.py` - 验证性因子分析
- `sem_estimator.py` - 结构方程估计
- `fit_evaluator.py` - 拟合指标评估
- `mediation_tester.py` - 中介效应检验
- `multigroup_analyzer.py` - 多群组分析

### 子智能体

- 模型构建智能体
- 测量模型智能体
- 结构模型智能体
- 拟合评估智能体
- 中介检验智能体

## 报告输出

1. **模型图**：路径图可视化
2. **测量模型表**：因子载荷、信效度
3. **结构模型表**：路径系数、假设检验
4. **拟合指标表**：各项拟合指标汇总
5. **中介效应表**：直接、间接、总效应

## 方法论参考

### 核心文献

1. Kline, R. B. (2016). *Principles and Practice of Structural Equation Modeling*. 4th Ed.
2. Hair, J. F., et al. (2019). *Multivariate Data Analysis*. 8th Ed.
3. Byrne, B. M. (2016). *Structural Equation Modeling with AMOS*. 3rd Ed.
4. Hu, L., & Bentler, P. M. (1999). Cutoff criteria for fit indexes. *Psychological Methods*.

### 软件支持

- **R/lavaan**: 开源SEM分析
- **Mplus**: 专业SEM软件
- **AMOS**: 图形化SEM分析
- **Python/semopy**: Python SEM库

---

**版本**: 5.0.0  
**创建时间**: 2026-03-15  
**方法类型**: 高级统计方法
