# 回归分析方法论详细指南

## 目录
1. [回归模型选择](#回归模型选择)
2. [OLS回归](#ols回归)
3. [Logistic回归](#logistic回归)
4. [计数数据回归](#计数数据回归)
5. [模型诊断](#模型诊断)
6. [交互与中介效应](#交互与中介效应)

---

## 回归模型选择

### 决策树

```
因变量类型?
├── 连续变量 → OLS回归
│   ├── 正态分布? → 标准OLS
│   ├── 有异常值? → 稳健回归
│   └── 异方差? → WLS或稳健标准误
│
├── 二分类变量 → Logistic回归
│   ├── 样本量充足? → 标准Logistic
│   ├── 稀有事件? → 稀有事件Logistic
│   └── 配对数据? → 条件Logistic
│
├── 计数变量 → Poisson/负二项
│   ├── 均值≈方差? → Poisson回归
│   └── 过离散? → 负二项回归
│
├── 有序变量 → 有序Logistic回归
│
└── 名义变量 → 多项Logistic回归
```

### 样本量要求

| 模型类型 | 最小样本量 | 推荐样本量 |
|---------|-----------|-----------|
| OLS | n ≥ 10k + 50 | n ≥ 20k |
| Logistic | EPV ≥ 10 | EPV ≥ 20 |
| Poisson | n ≥ 100 | n ≥ 200 |

注：k = 预测变量数，EPV = 每个变量的事件数

---

## OLS回归

### 基本公式

$$Y_i = \beta_0 + \beta_1X_{1i} + \beta_2X_{2i} + ... + \beta_kX_{ki} + \varepsilon_i$$

### 核心假设

1. **线性关系**：Y与X之间存在线性关系
2. **独立性**：观测值相互独立
3. **正态性**：残差服从正态分布
4. **同方差性**：残差方差恒定
5. **无多重共线性**：预测变量间无完全共线性

### 系数解释

- **连续预测变量**：β表示X每增加1单位，Y的平均变化量
- **分类预测变量**：β表示参照组与该组的平均差异
- **标准化系数**：β*表示X每增加1个标准差，Y变化的标准差数

### 模型拟合指标

| 指标 | 计算公式 | 理想值 |
|------|---------|--------|
| R² | SS_reg / SS_tot | 越高越好 |
| 调整R² | 1 - (1-R²)(n-1)/(n-k-1) | 考虑变量数 |
| RMSE | √(Σ(y-ŷ)²/n) | 越低越好 |
| AIC | n*ln(SS_res/n) + 2k | 越低越好 |
| BIC | n*ln(SS_res/n) + k*ln(n) | 越低越好 |

---

## Logistic回归

### 基本公式

$$\ln\left(\frac{p}{1-p}\right) = \beta_0 + \beta_1X_1 + ... + \beta_kX_k$$

### 优势比（Odds Ratio）

$$OR = e^{\beta}$$

**解释**：
- OR = 1：无效应
- OR > 1：正效应（风险增加）
- OR < 1：负效应（风险降低）

### 模型拟合指标

| 指标 | 说明 | 理想值 |
|------|------|--------|
| -2LL | -2倍对数似然 | 越低越好 |
| Cox & Snell R² | 伪R² | 越高越好 |
| Nagelkerke R² | 修正伪R² | 越高越好 |
| Hosmer-Lemeshow | 拟合优度检验 | p > 0.05 |

### 分类表

| | 预测=0 | 预测=1 |
|---|--------|--------|
| 实际=0 | TN | FP |
| 实际=1 | FN | TP |

- **灵敏度（Sensitivity）** = TP / (TP + FN)
- **特异度（Specificity）** = TN / (TN + FP)
- **准确率（Accuracy）** = (TP + TN) / Total

---

## 计数数据回归

### Poisson回归

**适用条件**：计数数据，均值 ≈ 方差

$$\ln(\lambda) = \beta_0 + \beta_1X_1 + ... + \beta_kX_k$$

### 负二项回归

**适用条件**：计数数据，过离散（方差 > 均值）

**过离散检验**：
- 离散参数 φ = Var/Mean
- φ ≤ 1.5：Poisson可接受
- φ > 1.5：推荐负二项

### 发生率比（IRR）

$$IRR = e^{\beta}$$

---

## 模型诊断

### 1. 正态性检验

| 检验方法 | 原假设 | 统计量 | p < .05 |
|---------|--------|--------|---------|
| Shapiro-Wilk | 正态分布 | W | 拒绝正态 |
| Kolmogorov-Smirnov | 正态分布 | D | 拒绝正态 |
| Q-Q图 | - | 视觉检验 | 点偏离直线 |

**补救措施**：
- 变量转换（log, sqrt）
- 使用稳健方法
- 增大样本量

### 2. 同方差性检验

| 检验方法 | 原假设 | 适用模型 |
|---------|--------|---------|
| Breusch-Pagan | 同方差 | OLS |
| White | 同方差 | OLS |
| Levene | 同方差 | 分组比较 |

**补救措施**：
- 使用稳健标准误（HC0-HC3）
- 加权最小二乘（WLS）
- 变量转换

### 3. 多重共线性检验

**方差膨胀因子（VIF）**：

$$VIF_j = \frac{1}{1-R_j^2}$$

| VIF值 | 判断 |
|-------|------|
| < 5 | 良好 |
| 5-10 | 中度关注 |
| > 10 | 严重问题 |

**补救措施**：
- 移除冗余变量
- 主成分分析（PCA）
- 岭回归

### 4. 异常值检测

| 统计量 | 阈值 | 说明 |
|--------|------|------|
| 标准化残差 | |z| > 3 | 异常值 |
| 杠杆值 | h > 2(p+1)/n | 高杠杆点 |
| Cook's D | D > 4/n | 强影响点 |

---

## 交互与中介效应

### 交互效应（调节效应）

**模型**：
$$Y = \beta_0 + \beta_1X + \beta_2M + \beta_3(X \times M) + \varepsilon$$

**分析步骤**：
1. 中心化X和M
2. 创建交互项 X×M
3. 检验β₃显著性
4. 进行简单斜率分析

**简单斜率**：
- 在M = Mean - 1SD 处
- 在M = Mean 处
- 在M = Mean + 1SD 处

### 中介效应

**Baron-Kenny三步法**：

1. **总效应**：Y = cX + e₁
2. **路径a**：M = aX + e₂
3. **路径b和直接效应c'**：Y = c'X + bM + e₃

**中介效应** = a × b

**判断标准**：
- 完全中介：间接效应显著，直接效应不显著
- 部分中介：间接效应和直接效应都显著
- 无中介：间接效应不显著

**Bootstrap检验**（推荐）：
- 5000次重抽样
- 95% CI不包含0 → 显著

---

## 参考文献

1. Cohen, J., et al. (2003). *Applied Multiple Regression/Correlation Analysis for the Behavioral Sciences*. 3rd ed.
2. Hosmer, D.W., Lemeshow, S., & Sturdivant, R.X. (2013). *Applied Logistic Regression*. 3rd ed.
3. Cameron, A.C., & Trivedi, P.K. (2013). *Regression Analysis of Count Data*. 2nd ed.
4. Hayes, A.F. (2018). *Introduction to Mediation, Moderation, and Conditional Process Analysis*. 2nd ed.
5. Fox, J. (2016). *Applied Regression Analysis and Generalized Linear Models*. 3rd ed.

---

**版本**: 1.0.0
**更新时间**: 2026-03-15
