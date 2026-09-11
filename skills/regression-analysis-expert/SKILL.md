---
name: regression-analysis-expert
description: |
  Regression Analysis expert. Provides linear/logistic regression modeling, assumption checking, variable selection, prediction validation, and regression diagnostics. Suitable for statistical modeling, predictive analysis, and quantitative research.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

## 概述

回归分析是量化研究中最核心、最广泛应用统计方法，用于探究变量之间的关系、进行预测建模和因果推断。自Francis Galton在19世纪末发明回归概念以来，回归分析已经发展成为包含多种模型和技术方法的完整体系。

本技能提供完整的回归分析流程支持，涵盖从模型选择、数据诊断、参数估计、假设检验到结果解释的全过程。支持的回归模型包括：普通最小二乘法(OLS)、Logistic回归、多项Logistic回归、有序Logistic回归、泊松回归、负二项回归、稳健回归等多种类型。

回归分析的应用场景极为广泛，包括：社会科学实证研究（教育、心理、管理）、经济学因果推断和政策评估、医学临床研究中的风险因素分析、商业领域的预测建模和市场分析等。本技能特别强调模型假设的检验和诊断，确保分析结果的可靠性和可解释性。

---


## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | diagnostic_tester.py | Regressiondiagnostic |
| 2 | effect_analyzer.py | Effectanalyzer |
| 3 | model_selector.py | Regressionmodelselector |

### CLI用法

```bash
# 列出可用工具
ls tools/

# 运行主分析（根据具体工具调整）
python tools/analysis.py --input data.csv
```

## 理论基础

### 经典理论家与贡献

| 理论家 | 年份 | 核心贡献 |
|--------|------|----------|
| **Francis Galton** | 1885 | 发明回归概念，首次提出"回归到平均值"理论 |
| **Karl Pearson** | 1900s | 发展皮尔逊相关系数，完善线性回归理论 |
| **Ronald Fisher** | 1920s | 提出最大似然估计，发展方差分析框架 |
| **Jerzy Neyman & Egon Pearson** | 1930s | 建立假设检验的统计框架 |
| **Cohen, Cohen & West** | 2003 | 《应用多元回归》，成为社会科学标准教材 |
| **Fox** | 2000s | 发展稳健回归和诊断技术 |

### 回归模型分类体系

```
回归模型
├── 线性回归
│   ├── 普通最小二乘回归 (OLS)
│   ├── 加权最小二乘回归 (WLS)
│   ├── 广义最小二乘回归 (GLS)
│   └── 稳健回归 (Robust)
│
├── 广义线性模型 (GLM)
│   ├── Logistic回归 (Binary)
│   ├── 多项Logistic回归 (Multinomial)
│   ├── 有序Logistic回归 (Ordinal)
│   ├── 泊松回归 (Poisson Count)
│   └── 负二项回归 (NB Count)
│
└── 特殊回归
    ├── 分层回归 (Hierarchical)
    ├── 调节回归 (Moderation)
    ├── 中介回归 (Mediation)
    ├── 非线性回归 (Polynomial/Spline)
    ├── 岭回归/LASSO (Regularized)
    └── 分位数回归 (Quantile)
```

---

## 🖥️ Python 工具

### model_selector.py - 模型选择器

根据因变量特性和数据质量自动推荐最合适的回归模型。

| 类/函数 | 功能 | CLI用法示例 |
|---------|------|------------|
| `RegressionModelSelector` | 模型选择主类 | `selector = RegressionModelSelector()` |
| `analyze_dependent_variable()` | 分析因变量特征 | `analysis = selector.analyze_dependent_variable(y)` |
| `recommend_model()` | 推荐模型并说明理由 | `rec = selector.recommend_model(y, X)` |
| `get_model_syntax()` | 生成statsmodels语法 | `syntax = selector.get_model_syntax('ols', 'y', ['x1','x2'])` |

**因变量类型识别：**

```python
from tools.model_selector import RegressionModelSelector
import numpy as np

selector = RegressionModelSelector()

# 连续变量
y_continuous = np.random.normal(100, 15, 200)
rec = selector.recommend_model(y_continuous)
# → 推荐: OLS Regression

# 二分类变量
y_binary = np.random.binomial(1, 0.3, 200)
rec = selector.recommend_model(y_binary)
# → 推荐: Logistic Regression

# 计数变量
y_count = np.random.poisson(5, 200)
rec = selector.recommend_model(y_count)
# → 推荐: Poisson Regression (或 Negative Binomial)
```

### diagnostic_tester.py - 回归诊断测试器

全面测试回归假设，包括正态性、同方差性、线性、多重共线性和异常值。

| 类/函数 | 功能 | CLI用法示例 |
|---------|------|------------|
| `RegressionDiagnostic` | 诊断主类 | `diag = RegressionDiagnostic()` |
| `run_all_diagnostics()` | 运行全部诊断测试 | `results = diag.run_all_diagnostics(y, y_pred, residuals, X)` |
| `test_normality()` | 正态性检验 (Shapiro-Wilk) | `results['normality']` |
| `test_homoscedasticity()` | 同方差检验 (Breusch-Pagan, White) | `results['homoscedasticity']` |
| `test_linearity()` | 线性检验 (Ramsey RESET) | `results['linearity']` |
| `test_multicollinearity()` | 多重共线性 (VIF) | `results['multicollinearity']` |
| `test_independence()` | 独立性检验 (Durbin-Watson) | `results['independence']` |
| `detect_outliers()` | 异常值检测 (Cook's D, Leverage) | `results['outliers']` |

**诊断阈值设置：**

```python
from tools.diagnostic_tester import RegressionDiagnostic
import numpy as np
from numpy.linalg import lstsq

diag = RegressionDiagnostic()

# 模拟OLS回归
np.random.seed(42)
n, k = 200, 3
X = np.random.randn(n, k)
X_const = np.column_stack([np.ones(n), X])
y = 2 + 1.5*X[:,0] + 0.5*X[:,1] + np.random.randn(n)*2

# OLS拟合
coeffs, _, _, _ = lstsq(X_const, y, rcond=None)
y_pred = X_const @ coeffs
residuals = y - y_pred

# 运行全部诊断
results = diag.run_all_diagnostics(y, y_pred, residuals, X, X_const)

# 查看结果摘要
print(f"状态: {results['summary']['status']}")
print(f"假设满足: {results['summary']['assumptions_met']}/{results['summary']['assumptions_total']}")

# 异常值检测
print(f"异常值数量: {results['details']['outliers']['summary']['n_outliers']}")

# 建议
for rec in results['recommendations']:
    print(f"  - {rec}")
```

### effect_analyzer.py - 效应分析器

分析交互效应、中介效应和调节效应。

| 类/函数 | 功能 | CLI用法示例 |
|---------|------|------------|
| `EffectAnalyzer` | 效应分析主类 | `analyzer = EffectAnalyzer()` |
| `test_interaction()` | 交互效应检验 | `result = analyzer.test_interaction(y, x1, x2)` |
| `simple_slopes_analysis()` | 简单斜率分析 | `result['simple_slopes']` |
| `mediation_analysis()` | 中介效应分析 | `result = analyzer.mediation_analysis(y, X, M)` |
| `moderation_analysis()` | 调节效应分析 | `result = analyzer.moderation_analysis(y, x, m)` |

**中介效应分析示例：**

```python
from tools.effect_analyzer import EffectAnalyzer
import numpy as np

analyzer = EffectAnalyzer()

# 数据：X → M → Y 的中介模型
np.random.seed(42)
n = 200
X = np.random.randn(n)              # 自变量
M = 0.5*X + np.random.randn(n)*0.5  # 中介变量
Y = 0.3*X + 0.4*M + np.random.randn(n)*0.5  # 因变量

# 中介效应分析
result = analyzer.mediation_analysis(Y, X, M, method='sobel')

print(f"路径 a (X→M): {result['paths']['a']['coefficient']:.3f}, p={result['paths']['a']['p_value']:.4f}")
print(f"路径 b (M→Y): {result['paths']['b']['coefficient']:.3f}, p={result['paths']['b']['p_value']:.4f}")
print(f"间接效应 (a×b): {result['indirect_effect']['coefficient']:.3f}")
print(f"中介类型: {result['mediation_type']}")
```

---

## 🚫 绝对禁止原则

回归分析必须遵循以下绝对禁止原则，任何违反都将严重影响分析质量：

1. **禁止忽略模型假设** - 必须检验线性、独立性、正态性、同方差性假设
2. **禁止忽视多重共线性** - VIF>10的变量必须处理，否则系数估计不稳定
3. **禁止忽视异常值** - 必须识别并报告Cook's距离和杠杆值高的问题观测
4. **禁止盲目追求显著** - 不应为了p<0.05而选择性报告或数据操纵
5. **禁止混淆相关与因果** - 回归系数不能直接解释为因果效应
6. **禁止忽视样本量要求** - 样本量必须满足10-20倍于自变量数的要求
7. **禁止忽视变量尺度** - 系数大小受变量尺度影响，必须标准化比较
8. **禁止忽略遗漏变量偏误** - 必须讨论潜在遗漏变量及其影响方向

---

## 5️⃣ 五阶段实施流程

### 阶段1：数据准备 (Data Preparation)

**目标**：确保数据质量，进行探索性分析

**关键任务：**
- 缺失值处理策略（删除、多重插补、EM算法）
- 异常值初步识别和处理
- 变量类型确认（连续、二分、计数、分类）
- 描述性统计和分布检验
- 相关矩阵和初步相关分析
- 数据分布转换判断

**缺失数据处理策略对比：**

| 方法 | 适用场景 | 优点 | 缺点 |
|------|----------|------|------|
| 列表删除 | 缺失比例<5% | 简单 | 丢失信息 |
| 均值填补 | 连续变量少量缺失 | 保持均值 | 降低方差 |
| 回归填补 | 有预测变量 | 保持关系 | 标准误低估 |
| 多重插补 | 随机缺失 | 无偏估计 | 复杂计算 |

### 阶段2：探索性分析 (Exploratory Analysis)

**目标**：理解数据结构，验证分析前提

**关键任务：**
- 绘制散点图矩阵，检查非线性关系
- 相关系数矩阵，识别高度相关变量
- 箱线图，检查异常值和分布
- 分布检验，正态性评估
- 交叉表，对分类变量的初步探索
- 功效分析，确定所需样本量

**模型选择决策树：**

```
因变量类型
│
├─ 连续
│   ├─ 样本量充足，无异常值 → OLS回归
│   ├─ 存在异常值 → 稳健回归
│   ├─ 需要正则化 → Ridge/LASSO回归
│   └─ 需要分位数估计 → 分位数回归
│
├─ 二分类
│   └─ Logistic回归
│
├─ 有序多分类
│   └─ 有序Logistic回归
│
├─ 名义多分类
│   └─ 多项Logistic回归
│
└─ 计数
    ├─ 方差≈均值 → 泊松回归
    └─ 方差>均值 → 负二项回归
```

### 阶段3：模型选择与估计 (Model Selection & Estimation)

**目标**：选择最优模型，估算参数

**关键任务：**
- 基于因变量类型选择模型族
- 变量选择（前向/后向/逐步/正则化）
- 交互项和二次项的添加
- 共线性检验和变量处理
- 模型估计和系数解释
- 伪R²/调整R²计算
- 信息准则（AIC、BIC）比较

**变量选择方法对比：**

| 方法 | 描述 | 适用场景 |
|------|------|----------|
| 前向选择 | 从空模型逐步加入变量 | 候选变量多，样本有限 |
| 后向消除 | 从全模型逐步剔除变量 | 变量数量适中 |
| 逐步回归 | 结合前向和后向 | 平衡效率和精度 |
| LASSO | L1正则化同时做变量选择 | 高维数据 |
| Ridge | L2正则化处理共线性 | 强共线性存在 |
| 最佳子集 | 遍历所有可能组合 | 变量数<15 |

### 阶段4：诊断验证 (Diagnostic Validation)

**目标**：检验模型假设，评估模型质量

**关键任务：**
- 正态性检验（Shapiro-Wilk, K-S）
- 同方差性检验（Breusch-Pagan, White）
- 线性假设检验（RESET检验、成分残差图）
- 多重共线性检验（VIF > 10 为问题阈值）
- 独立性检验（Durbin-Watson）
- 异常值检验（Cook's D > 4/n, Leverage > 2k/n）
- 预测值范围检查

**诊断决策表：**

| 诊断项 | 检验方法 | 拒绝标准 | 补救措施 |
|--------|----------|----------|----------|
| 正态性 | Shapiro-Wilk | p < 0.05 | 数据变换、稳健标准误 |
| 同方差 | Breusch-Pagan | p < 0.05 | 稳健标准误、WLS |
| 线性 | Ramsey RESET | p < 0.05 | 多项式、样条、变换 |
| 共线性 | VIF | VIF > 10 | 删除、合并、PCA |
| 异常值 | Cook's D | D > 4/n | 检查、删除、稳健 |
| 自相关 | D-W | 远离2.0 | GLS、时间序列 |

### 阶段5：解释报告 (Interpretation & Reporting)

**目标**：清晰报告结果，提供可操作的洞察

**关键任务：**
- 标准化系数计算和比较
- 交互效应的简单斜率分析
- 中介效应的Sobel检验或Bootstrap
- 效应量和置信区间报告
- 结果可视化（森林图、系数图）
- APA格式结果报告
- 研究局限性讨论

---

## ✅ 质量标准

### 完整性标准

| 要素 | 最低要求 | 优秀标准 |
|------|----------|----------|
| 模型报告 | 系数、标准误、p值 | 含置信区间、效应量 |
| 假设检验 | 主要假设检验 | 完整诊断报告 |
| 模型比较 | 单模型报告 | 多模型比较表 |
| 效应报告 | 原始系数 | 标准化系数+Cohen's d |

### 方法论标准

| 要素 | 要求 |
|------|------|
| 理论基础 | 有理论依据的变量选择 |
| 模型假设 | 明确的假设检验和补救 |
| 估计方法 | 适当的估计方法选择 |
| 推断有效性 | 报告置信区间而非仅p值 |

### 深度标准

| 层次 | 描述 |
|------|------|
| 基础分析 | 系数解释和显著性 |
| 诊断分析 | 假设检验和诊断 |
| 高级分析 | 交互、中介、调节效应 |
| 稳健分析 | 多重稳健性检验 |

---

## 分析流程

```
数据准备 → 探索性分析 → 模型选择 → 估计与检验 → 诊断验证 → 解释报告
    │            │             │          │           │           │
    ▼            ▼             ▼          ▼           ▼           ▼
 缺失处理     相关分析     因变量类型   参数估计    假设检验    效应解释
 异常识别     分布检验     模型族选择   假设检验    诊断补救    可视化
 数据清洗     可视化       变量选择     拟合度      异常值      报告撰写
```

---

## 效应量解释标准

### Cohen's d 效应量标准

| 效应量 | 小 | 中 | 大 |
|--------|----|----|-----|
| d | 0.2 | 0.5 | 0.8 |
| r | 0.1 | 0.3 | 0.5 |
| f² | 0.02 | 0.15 | 0.35 |

### R² 解释标准

| R²值 | 解释 |
|------|------|
| < 0.10 | 弱解释力 |
| 0.10-0.30 | 中等解释力 |
| 0.30-0.50 | 较强解释力 |
| > 0.50 | 强解释力 |

---

## 报告规范

遵循APA第七版要求，回归分析报告应包括：

1. **样本描述**：样本量、有效样本、缺失数据处理
2. **模型拟合指标**：R²、调整R²、F变化量
3. **系数估计表**：B、SE、β、t、p、95%CI
4. **诊断检验结果**：主要假设检验结论
5. **效应量报告**：标准化系数或Cohen's d
6. **稳健性检验**：替代模型结果比较

---

## 引用

```bibtex
@book{cohen2003applied,
  title={Applied multiple regression/correlation analysis for the behavioral sciences},
  author={Cohen, Jacob and Cohen, Patricia and West, Stephen G and Aiken, Leona S},
  year={2003},
  publisher={Routledge}
}

@book{fox2000nonparametric,
  title={Nonparametric Simple Regression: Smoothing Scatterplots},
  author={Fox, John},
  year={2000},
  publisher={Sage}
}

@book{harrell2015regression,
  title={Regression Modeling Strategies},
  author={Harrell Jr, Frank E},
  year={2015},
  publisher={Springer}
}
```

---

**Version**: 5.0.0
**Created**: 2026-03-15
**Author**: SocienceAI Team