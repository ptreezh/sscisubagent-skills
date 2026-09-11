---
name: multilevel-modeling-expert
description: |
  多层模型分析专家。提供系统化多层/分层线性模型分析，支持随机截距模型、
  随机斜率模型、跨层交互、增长曲线模型。核心能力包括：组内相关计算、
  模型构建策略、效应分解、模型比较、诊断检验。
  遵循Raudenbush & Bryk (2002)和Hox et al. (2018)标准。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/龙虾/QClaw
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0"
  agentskills-io: "true"
  cross-platform: "true"
  methodology: "Raudenbush & Bryk (2002), Hox et al. (2018), Snijders & Bosker (2012)"
---

# 多层模型分析专家 (Multilevel Modeling Expert)

## 概述

多层模型(也称分层线性模型HLM、混合效应模型)用于分析嵌套数据结构，正确处理组内相关和效应分解。

## 为什么需要多层模型？

### 嵌套数据问题

```
传统回归假设:
- 观测独立
- 同质方差

嵌套数据现实:
学生 ──┬── 班级A (共享环境)
       ├── 班级A (非独立)
       └── 班级A (组内相关)

问题:
- 低估标准误
- 假阳性风险
- 错误推断
```

### 组内相关(ICC)

```
ICC = 组间方差 / 总方差

ICC解释:
ICC = 0.00 → 无组效应，可用传统回归
ICC = 0.05 → 弱组效应
ICC = 0.15 → 中等组效应
ICC = 0.30 → 强组效应

设计效应: DEFF = 1 + (n̄ - 1) × ICC
DEFF > 1.1 → 需要多层模型
```

## 模型结构

### 两层模型

```
层1(个体层): 
Yij = β0j + β1jXij + rij

层2(组层):
β0j = γ00 + γ01Wj + u0j  (随机截距)
β1j = γ10 + γ11Wj + u1j  (随机斜率)

合并模型:
Yij = γ00 + γ01Wj + γ10Xij + γ11WjXij + u0j + u1jXij + rij
```

### 模型组成部分

| 成分 | 符号 | 含义 |
|------|------|------|
| 固定效应 | γ | 总体平均效应 |
| 随机效应 | u | 组间变异 |
| 残差 | r | 个体层误差 |
| 方差成分 | τ², σ² | 随机效应方差 |

## 模型构建策略

### 自下而上策略

```
步骤1: 空模型(Null Model)
Yij = γ00 + u0j + rij
├── 计算ICC
├── 评估组效应
└── 决定是否需要多层模型

步骤2: 随机截距模型
Yij = γ00 + γ10Xij + u0j + rij
├── 加入层1预测变量
├── 组均值中心化
└── 评估固定效应

步骤3: 随机斜率模型
Yij = γ00 + γ10Xij + u0j + u1jXij + rij
├── 检验斜率方差
├── χ²检验或LR检验
└── 决定是否保留随机斜率

步骤4: 跨层交互模型
β1j = γ10 + γ11Wj + u1j
├── 加入层2预测变量
├── 检验跨层交互
└── 解释调节效应
```

## 中心化策略

### 三种中心化选择

| 策略 | 公式 | 效果 |
|------|------|------|
| 原始尺度 | Xij | 组间+组内混合效应 |
| 组均值中心化 | Xij - X̄j | 纯组内效应 |
| 总均值中心化 | Xij - X̄ | 减少共线性 |

### 最佳实践
```
场景: 研究学生努力(X)对成绩(Y)的影响

1. 学生努力(Xij) → 组均值中心化
   → "班级内相对努力程度"

2. 班级平均努力(X̄j) → 总均值中心化
   → "班级整体努力水平(情境效应)"

3. 两个变量同时纳入:
   Yij = γ00 + γ10(Xij-X̄j) + γ01(X̄j-X̄) + ...
   → 分解组内效应(γ10)和组间效应(γ01)
```

## 模型比较

### 信息准则

| 指标 | 原则 | 说明 |
|------|------|------|
| AIC | 越小越好 | 惩罚复杂度 |
| BIC | 越小越好 | 更严格惩罚 |
| -2LL | 越小越好 | 似然比检验 |

### 似然比检验
```
模型比较: 
-2ΔLL = -2(LL_reduced - LL_full)

χ²检验:
df = df_full - df_reduced
p < .05 → 完整模型更优
```

## 增长曲线模型

### 纵向数据多层模型

```
层1(时间层):
Yti = π0i + π1i(Time)ti + π2i(Time²)ti + eti

层2(个体层):
π0i = β00 + β01Zi + r0i  (初始状态)
π1i = β10 + β11Zi + r1i  (线性变化率)
π2i = β20 + β21Zi + r2i  (二次变化率)

时间编码:
- 年龄编码: 实际年龄
- 事件编码: 相对于事件时间
- 0点编码: 有意义的时间零点
```

## 软件实现

### R语言
```r
library(lme4)
# 随机截距模型
model1 <- lmer(Y ~ X + (1|group), data)

# 随机斜率模型
model2 <- lmer(Y ~ X + (X|group), data)

# 跨层交互
model3 <- lmer(Y ~ X*W + (X|group), data)
```

### 模型诊断

| 诊断项 | 方法 | 问题 |
|--------|------|------|
| 正态性 | Q-Q图 | 随机效应/残差分布 |
| 异方差 | 残差vs拟合值 | 方差齐性 |
| 影响点 | Cook's D | 异常值影响 |
| 多重共线性 | VIF | 预测变量相关性 |

## 效应量

### 方差解释

```
条件R² = (固定效应方差 + 随机效应方差) / 总方差

伪R²(Proportional Reduction in Variance):
伪R² = (τ²_null - τ²_model) / τ²_null

解释:
- 层1伪R²: 层1方差减少比例
- 层2伪R²: 层2方差减少比例
```

## 使用示例

```
用户: 研究学校氛围对学生成绩的影响

AI: 我将构建多层模型：

## 数据结构
层1: 学生(n=2000)
层2: 学校(n=50)

## 空模型
Yij = γ00 + u0j + rij
ICC = 0.18 (18%方差在学校层)
→ 需要多层模型

## 模型构建
模型1(随机截距):
成绩ij = γ00 + γ10(努力ij) + u0j + rij

模型2(随机斜率):
成绩ij = γ00 + γ10(努力ij) + u0j + u1j(努力ij) + rij
χ²检验: p < .05 → 保留随机斜率

模型3(跨层交互):
β1j = γ10 + γ11(学校氛围j) + u1j
γ11 = 0.25, p < .05
→ 学校氛围调节努力对成绩的影响

## 结果解释
在积极氛围学校，努力对成绩的影响更强
```

## 工具函数

| 工具 | 功能 |
|------|------|
| `icc_calculator.py` | 组内相关计算 |
| `model_builder.py` | 模型构建辅助 |
| `effect_decomposer.py` | 效应分解分析 |

## 参考文献

1. Raudenbush, S.W., & Bryk, A.S. (2002). *Hierarchical Linear Models*. 2nd ed.
2. Hox, J.J., Moerbeek, M., & van de Schoot, R. (2018). *Multilevel Analysis*. 3rd ed.
3. Snijders, T.A.B., & Bosker, R.J. (2012). *Multilevel Analysis*. 2nd ed.
4. Gelman, A., & Hill, J. (2007). *Data Analysis Using Regression and Multilevel Models*.

---

**技能版本**: 5.0.0  
**方法论标准**: Raudenbush & Bryk (2002)  
**创建时间**: 2026-03-15
