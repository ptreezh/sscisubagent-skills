---
name: longitudinal-analysis-expert
description: |
  Longitudinal Analysis expert. Provides panel data modeling, growth curve estimation, time-series analysis, attrition handling, and repeated measures design. Suitable for developmental research, panel studies, and temporal trend analysis.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

---|--------|------|
| 因果推断 | 弱 | 强 |
| 变化测量 | 无 | 有 |
| 个体差异 | 无法控制 | 可控制 |
| 成本 | 低 | 高 |
| 样本流失 | 无 | 有 |

### 纵向数据类型

```
类型1: 面板数据
时间点固定 → 相同间隔测量

类型2: 加速纵向设计
不同年龄队列 → 重叠部分连接

类型3: 事件史数据
事件发生时间 → 持续时间分析

类型4: 强度数据
观察间隔不等 → 连续时间建模
```

## 核心分析方法

### 1. 重复测量ANOVA

```
模型: Yij = μ + αi + βj + (αβ)ij + εij

问题:
- 球形假设(sphericity)
- 缺失数据敏感性
- 假设过多

适用: 少量时间点、完整数据
```

### 2. 潜在增长模型(LGM)

```
基本模型:
Yti = π0i + π1i(Time)ti + π2i(Time²)ti + εti

个体参数:
π0i = β00 + β01Zi + ζ0i  (截距因子)
π1i = β10 + β11Zi + ζ1i  (斜率因子)
π2i = β20 + β21Zi + ζ2i  (曲线因子)

解释:
- 截距因子: 初始状态
- 斜率因子: 变化速度
- 曲线因子: 非线性变化
```

### 3. 交叉滞后模型

```
时间点1         时间点2         时间点3
   X1 ───────────→ X2 ───────────→ X3
   │              │               │
   ↓              ↓               ↓
   Y1 ←─────────── Y2 ←─────────── Y3
   │              │
   └───→ Y2       └───→ Y3

路径含义:
- 自回归: X1→X2, Y1→Y2 (稳定性)
- 交叉滞后: X1→Y2, Y1→X2 (因果关系)
- 同期相关: X1↔Y1 (共享方差)
```

### 4. 事件史分析

```
风险函数: h(t) = lim[Pr(t ≤ T < t+Δt | T ≥ t)/Δt]

生存函数: S(t) = Pr(T ≥ t)

Cox比例风险模型:
h(t|X) = h0(t) × exp(β'X)

解释:
- h(t): 在时间t发生事件的瞬时风险
- h0(t): 基线风险函数
- exp(β): 风险比(HR)
```

## 时间效应建模

### 时间编码策略

| 编码方式 | 特点 | 适用场景 |
|---------|------|---------|
| 原始时间 | 实际测量时间 | 发展研究 |
| 0起点 | 有意义的起点 | 干预研究 |
| 中心化 | 减少共线性 | 多项式模型 |
| 年龄基准 | 生物年龄 | 发展心理学 |

### 轨迹形状

```
线性: Y = π0 + π1t
      ↓
单调增/减

二次: Y = π0 + π1t + π2t²
      ↓
先增后减/先减后增

分段: Y = π0 + π1t1 + π2t2
      ↓
不同阶段不同斜率

渐近: Y = α - (α-π0)e^{-βt}
      ↓
趋近渐近线
```

## 缺失数据处理

### 缺失数据机制

| 类型 | 符号 | 特点 | 处理方法 |
|------|------|------|---------|
| 完全随机 | MCAR | 与所有变量无关 | 可忽略 |
| 随机 | MAR | 与观测变量相关 | FIML/MI |
| 非随机 | MNAR | 与未观测变量相关 | 模式混合 |

### 处理方法

```
方法1: 全信息最大似然(FIML)
- 使用所有可用数据
- 适合MAR
- SEM软件默认

方法2: 多重插补(MI)
- 生成多个完整数据集
- 合并分析结果
- 灵活性高

方法3: 模式混合模型
- 对MNAR建模
- 敏感性分析
- 模型依赖性强
```

## 软件实现

### R语言示例

```r
# 潜在增长模型(lavaan)
library(lavaan)
model <- '
  i =~ 1*t1 + 1*t2 + 1*t3
  s =~ 0*t1 + 1*t2 + 2*t3
  i ~ predictor
  s ~ predictor
'
fit <- growth(model, data)

# Cox回归(survival)
library(survival)
cox_model <- coxph(Surv(time, event) ~ X, data)
```

## 质量控制

### 样本流失分析

```
流失模式分析:
1. 比较流失者vs保留者
   - 基线特征比较
   - t检验/卡方检验

2. 流失预测模型
   - 流失与变量的关系
   - 判断MAR vs MNAR

3. 敏感性分析
   - 最佳/最差情景
   - 估计稳健性
```

### 检验力分析

```
纵向设计检验力:
- 时间点数量
- 样本规模
- 效应量大小
- 相关性结构

经验法则:
时间点 ≥ 3 → 可估计斜率
时间点 ≥ 4 → 可估计曲率
样本量 ≥ 10N参数
```

## 使用示例

```
用户: 分析学生学业成绩3年追踪数据

AI: 我建议采用潜在增长模型：

## 数据特征
- 时间点: 3年(6、7、8年级)
- 样本: N=500学生
- 变量: 数学成绩、社会经济地位

## 模型构建
模型1: 无条件增长模型
Yti = π0i + π1i(Time)ti + εti

结果:
- 截距均值 β00 = 70 (初始水平)
- 斜率均值 β10 = 3 (年均增长)
- 截距方差 τ00 = 45 (个体差异显著)
- 斜率方差 τ11 = 4 (增长差异显著)

模型2: 条件增长模型
π0i = β00 + β01(SES)i + ζ0i
π1i = β10 + β11(SES)i + ζ1i

结果:
- SES对初始水平: β01 = 5.2***
- SES对增长速度: β11 = 0.8(n.s.)

结论:
高SES学生起点更高，但增长速度无差异
```

## 🚫 绝对禁止原则

> **使用前必读**：以下原则是不可逾越的红线，违反将导致纵向研究结论失效。

1. **禁止忽视缺失数据机制** — 不检验MCAR/MAR/MNAR，直接删除缺失值或使用不恰当的处理方法，导致估计偏倚
2. **禁止混淆相关与因果** — 将时间上的前后顺序等同于因果关系，忽略遗漏变量偏倚和反向因果
3. **禁止忽视时间编码** — 不说明时间变量的编码方式（原始/0起点/中心化），导致模型不可复现
4. **禁止只看均值轨迹** — 仅报告组均值变化而忽视个体差异轨迹（离散性），导致个体异质性被掩盖
5. **禁止忽视样本流失分析** — 不检验流失者与保留者的基线差异，导致结论无法推广
6. **禁止时间点不足仍建模变化** — 时间点<3时声称分析"变化轨迹"或"发展趋势"，导致模型过度拟合

## ✅ 质量标准

### 完整性
- 必做项清单完成度 ≥ 90%
- 缺失数据机制检验报告完整
- 样本流失分析完整

### 方法论
- 理论框架与数据一致性 ≥ 90%
- 分析步骤可复现性高（含时间编码说明）
- 模型比较有据可查

### 深度
- 核心维度覆盖 ≥ 80%
- 个体差异轨迹分析（不仅是均值）
- 敏感性分析完整

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | lgm_analyzer.py | 潜在增长模型，支持无条件/条件增长模型、轨迹形状检验 |
| 2 | cross_lag_analyzer.py | 交叉滞后模型，支持随机截距交叉滞后面板模型(RICLPM) |
| 3 | survival_analyzer.py | 事件史分析，支持Kaplan-Meier、Cox回归、风险比计算 |
| 4 | missing_data_handler.py | 缺失数据处理，支持MCAR/MAR/MNAR检验、FIML、多重插补 |

### CLI用法

```bash
python tools/lgm_analyzer.py --input panel_data.csv --time t1,t2,t3 --output growth_model.json
python tools/cross_lag_analyzer.py --input data.csv --variables X,Y --output cross_lag.json
python tools/survival_analyzer.py --input event_data.csv --time time --event status --output survival.json
```

## 参考文献

1. Singer, J.D., & Willett, J.B. (2003). *Applied Longitudinal Data Analysis*.
2. Bollen, K.A., & Curran, P.J. (2006). *Latent Curve Models*.
3. Little, T.D. (2013). *Longitudinal Structural Equation Modeling*.
4. Allison, P.D. (2014). *Event History and Survival Analysis*. 2nd ed.

---

**技能版本**: 5.0.0  
**方法论标准**: Singer & Willett (2003)  
**创建时间**: 2026-03-15