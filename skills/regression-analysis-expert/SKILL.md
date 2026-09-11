---
name: regression-analysis-expert
description: |
  回归分析专家。提供多种回归模型支持（OLS、Logistic、多元回归、层次回归、稳健回归），包括模型诊断、假设检验、变量选择、交互效应分析。适用于量化研究数据分析和因果推断。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/龙虾/QClaw
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0"
  agentskills-io: "true"
  cross-platform: "true"
  category: "quantitative-methods"
  methodology: "Regression Analysis"
  evidence-level: "Level II"
---

# 回归分析专家 (Regression Analysis Expert)

## 概述

回归分析是量化研究中最核心的统计方法，用于探究变量之间的关系、进行预测和因果推断。本技能提供完整的回归分析流程支持。

## 核心功能

### 1. 多种回归模型

| 模型类型 | 适用场景 | 因变量类型 |
|----------|----------|------------|
| OLS回归 | 连续因变量 | 连续 |
| Logistic回归 | 二分类因变量 | 二元 |
| 多项Logistic | 多分类因变量 | 名义 |
| 有序Logistic | 有序分类因变量 | 有序 |
| 泊松回归 | 计数数据 | 计数 |
| 负二项回归 | 过度离散计数 | 计数 |
| 稳健回归 | 异常值存在 | 连续 |

### 2. 模型诊断

- **线性假设**: 残差图、成分+残差图
- **正态性**: Q-Q图、Shapiro-Wilk检验
- **同方差性**: Breusch-Pagan检验、White检验
- **多重共线性**: VIF、条件指数
- **异常值**: Cook's距离、Leverage值
- **独立性**: Durbin-Watson检验

### 3. 变量选择

- 前向选择 (Forward Selection)
- 后向消除 (Backward Elimination)
- 逐步回归 (Stepwise)
- 最佳子集 (Best Subset)
- LASSO/Ridge正则化
- 基于AIC/BIC的选择

### 4. 高级分析

- 交互效应检验
- 中介效应分析
- 调节效应分析
- 非线性关系（多项式、样条）
- 分层回归

## 分析流程

```
数据准备 → 探索性分析 → 模型选择 → 估计与检验 → 诊断验证 → 解释报告
```

## 使用场景

- 社会科学实证研究
- 经济学因果推断
- 医学风险因素分析
- 心理学预测模型
- 教育研究因素分析
- 商业预测建模

## 工具支持

- `model_selector.py`: 模型类型选择
- `diagnostic_tester.py`: 假设检验与诊断
- `variable_selector.py`: 变量选择算法
- `effect_analyzer.py`: 效应分析（交互、中介、调节）

## 报告规范

遵循APA第七版和STROBE声明要求，包括：
- 样本量与缺失数据处理
- 模型拟合指标
- 系数估计与置信区间
- 诊断检验结果
- 效应量报告

## 引用

```bibtex
@book{cohen2003applied,
  title={Applied multiple regression/correlation analysis for the behavioral sciences},
  author={Cohen, Jacob and Cohen, Patricia and West, Stephen G and Aiken, Leona S},
  year={2003},
  publisher={Routledge}
}
```

---

**Version**: 5.0.0  
**Created**: 2026-03-15  
**Author**: SocienceAI Team
