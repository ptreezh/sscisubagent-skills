---
name: meta-analysis-expert
description: |
  Meta-Analysis expert. Provides effect size pooling, heterogeneity assessment, publication bias testing, subgroup analysis, and meta-regression modeling. Suitable for systematic review, evidence synthesis, and quantitative literature review.
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

元分析(Meta-Analysis)专家是专门支持系统性文献综述和统计合成研究的循证方法技能。元分析是循证医学和循证实践金字塔中证据等级最高的方法，通过系统化检索、严格筛选、量化综合多个独立研究的结果，得出更加精确和可靠的总效应估计。

元分析的核心价值在于：它能够通过统计方法合成多项研究的结果，解决单项研究样本量有限、结果不一致的问题；它能够量化异质性，探究研究间差异的来源；它能够通过发表偏倚检测，评估现有证据的完整性；它能够通过亚组分析和元回归，探索调节变量的影响。

本技能提供从研究问题界定到最终报告撰写的全流程支持，涵盖：系统检索策略设计、PRISMA流程报告、研究质量评估(Cochrane RoB、NOS)、多种效应量计算(d、Cohen's g、Pearson r、OR、RR)、固定效应与随机效应模型、异质性统计检验(Q、I²、Tau²)、发表偏倚检测(Egger、Begg、Trim-and-fill)、亚组分析和元回归、森林图和漏斗图可视化。

元分析适用于：循证医学的治疗效果评估、心理学研究的效应大小估计、教育干预效果评估、社会科学的证据综合、政策制定的实证基础构建等场景。

---


## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | effect_size_calculator.py | Effect Size Calculator |
| 2 | heterogeneity_analyzer.py | Heterogeneity Analyzer |
| 3 | publication_bias_tester.py | Publication Bias Tester |

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
| **Karl Pearson** | 1904 | 首次提出合并传染病死亡率的想法 |
| **Gene Glass** | 1976 | 首创"meta-analysis"术语 |
| **Jacob Cohen** | 1977 | 提出效应量d和统计检验力分析 |
| **Rosenthal** | 1979 | 开发Fail-safe N和文件抽屉方法 |
| **Hunter, Schmidt & Jackson** | 1980s | 发展认知类方法学(meta for correlations) |
| **DerSimonian & Laird** | 1986 | 提出随机效应模型D-L估计法 |
| **Borenstein et al.** | 2009 | 系统化元分析教科书 |
| **Higgins & Thompson** | 2002 | I²置信区间和异质性度量 |
| **Egger et al.** | 1997 | Egger发表偏倚检验 |
| **Duval & Tweedie** | 2000 | Trim-and-fill发表偏倚校正 |

### 元分析模型体系

```
元分析模型
│
├── 固定效应模型 (Fixed-Effect Model)
│   │
│   假设：所有研究共享同一真实效应量
│   权重：逆方差加权 (w_i = 1/v_i)
│   适用：研究间异质性极低 (I² < 25%)
│   方法：逆方差合并法 (Inverse-Variance Method)
│
└── 随机效应模型 (Random-Effects Model)
    │
    假设：真实效应量随研究变化，存在研究间方差
    权重：调整逆方差加权 [w_i* = 1/(v_i + Tau²)]
    适用：研究间存在真实异质性
    方法：
    ├─ DerSimonian-Laird (D-L) - 最常用
    ├─ REML (Restricted Maximum Likelihood)
    ├─ ML (Maximum Likelihood)
    └─ Paule-Mandel
```

### 异质性统计量体系

```
异质性度量
│
├── Q统计量 (Cochran's Q)
│   │
│   Q = Σw_i(Y_i - Y_bar)²
│   检验：Q服从df=k-1的卡方分布
│   问题：对研究数量敏感，小样本不可靠
│
├── I²统计量 (Higgins & Thompson, 2002)
│   │
│   I² = max{0, (Q-df)/Q × 100%}
│   解释标准：
│   ├─ 0-25%: 低异质性
│   ├─ 25-50%: 中等异质性
│   ├─ 50-75%: 较高异质性
│   └─ 75-100%: 高异质性
│   优势：不受研究数量影响
│
└── Tau²和Tau
    │
    Tau²：研究间真实效应的方差
    Tau：研究间标准差
    解释：Tau²越大，研究间差异越大
```

---

## 🖥️ Python 工具

### effect_size_calculator.py - 效应量计算器

计算多种效应量类型并进行转换。

| 类/函数 | 功能 | CLI用法示例 |
|---------|------|------------|
| `EffectSizeCalculator` | 效应量计算主类 | `calc = EffectSizeCalculator(confidence_level=0.95)` |
| `cohen_d()` | Cohen's d计算 | `result = calc.cohen_d(85.2, 78.5, 12.3, 11.8, 50, 45)` |
| `hedges_g()` | Hedges' g计算 | `result = calc.hedges_g(mean1, mean2, sd1, sd2, n1, n2)` |
| `pearson_r()` | Pearson r计算 | `result = calc.pearson_r(r=0.35, n=100)` |
| `odds_ratio()` | 优势比计算 | `result = calc.odds_ratio(45, 55, 30, 70)` |
| `risk_ratio()` | 风险比计算 | `result = calc.risk_ratio(45, 55, 30, 70)` |
| `d_to_r()` | d转换为r | `r = calc.d_to_r(0.5)` |
| `interpret_effect_size()` | 效应量解释 | `size = interpret_effect_size(0.5)` |

**效应量计算示例：**

```python
from tools.effect_size_calculator import EffectSizeCalculator, interpret_effect_size

calc = EffectSizeCalculator(confidence_level=0.95)

# 1. Cohen's d - 连续变量
d_result = calc.cohen_d(
    mean1=85.2, mean2=78.5,
    sd1=12.3, sd2=11.8,
    n1=50, n2=45
)
print(f"Cohen's d = {d_result.effect_size:.3f}")
print(f"95% CI: [{d_result.confidence_interval[0]:.3f}, {d_result.confidence_interval[1]:.3f}]")
print(f"解释: {interpret_effect_size(d_result.effect_size)}")

# 2. Hedges' g - 小样本校正
g_result = calc.hedges_g(
    mean1=85.2, mean2=78.5,
    sd1=12.3, sd2=11.8,
    n1=50, n2=45
)
print(f"Hedges' g = {g_result.effect_size:.3f}")

# 3. Odds Ratio - 二分类变量
or_result = calc.odds_ratio(
    a=45, b=55,   # 干预组: 事件/非事件
    c=30, d=70    # 对照组: 事件/非事件
)
print(f"OR = {or_result.effect_size:.3f}")
print(f"95% CI: [{or_result.confidence_interval[0]:.3f}, {or_result.confidence_interval[1]:.3f}]")

# 4. 批量计算
studies = [
    {'study_id': 'S1', 'study_name': '研究1', 'mean1': 85, 'mean2': 78, 'sd1': 12, 'sd2': 11, 'n1': 50, 'n2': 45},
    {'study_id': 'S2', 'study_name': '研究2', 'mean1': 82, 'mean2': 76, 'sd1': 10, 'sd2': 9, 'n1': 60, 'n2': 58},
]
results = calc.calculate_from_studies(studies, 'g')
```

### heterogeneity_analyzer.py - 异质性分析器

Q检验、I²、Tau²计算和模型选择建议。

| 类/函数 | 功能 | CLI用法示例 |
|---------|------|------------|
| `HeterogeneityAnalyzer` | 异质性分析主类 | `analyzer = HeterogeneityAnalyzer()` |
| `analyze()` | 执行完整异质性分析 | `result = analyzer.analyze(effect_sizes, variances)` |
| `tau_squared_reml()` | REML法估计Tau² | `tau2 = analyzer.tau_squared_reml(es, var)` |
| `compare_models()` | 比较固定/随机效应模型 | `comp = analyzer.compare_models(es, var)` |
| `generate_report()` | 生成异质性报告 | `report = analyzer.generate_report(result)` |

**异质性分析示例：**

```python
from tools.heterogeneity_analyzer import HeterogeneityAnalyzer

analyzer = HeterogeneityAnalyzer()

# 模拟10个研究的效应量和方差
effect_sizes = [0.45, 0.62, 0.38, 0.55, 0.48, 0.72, 0.41, 0.58, 0.52, 0.49]
variances = [0.04, 0.03, 0.05, 0.04, 0.03, 0.04, 0.06, 0.03, 0.04, 0.05]

# 执行异质性分析
result = analyzer.analyze(effect_sizes, variances)

print(f"Q统计量: {result.q_statistic:.3f} (df={result.q_df}, p={result.q_pvalue:.4f})")
print(f"I²: {result.i_squared:.1f}%")
print(f"Tau²: {result.tau_squared:.4f}")
print(f"异质性水平: {result.heterogeneity_level}")
print(f"模型建议: {result.model_recommendation}")

# 模型比较
comparison = analyzer.compare_models(effect_sizes, variances)
print(f"\n固定效应估计: {comparison['fixed_effect']['estimate']:.3f}")
print(f"随机效应估计: {comparison['random_effects']['estimate']:.3f}")

# 生成报告
print(analyzer.generate_report(result))
```

### publication_bias_tester.py - 发表偏倚检测器

Egger检验、Begg检验、Fail-safe N、Trim-and-fill。

| 类/函数 | 功能 | CLI用法示例 |
|---------|------|------------|
| `PublicationBiasTester` | 发表偏倚检测主类 | `tester = PublicationBiasTester()` |
| `egger_test()` | Egger回归检验 | `result = tester.egger_test(effect_sizes, standard_errors)` |
| `begg_test()` | Begg秩相关检验 | `result = tester.begg_test(effect_sizes, variances)` |
| `fail_safe_n()` | Rosenthal Fail-safe N | `result = tester.fail_safe_n(es, var)` |
| `trim_and_fill()` | Duval-Tweedie Trim-and-fill | `result = tester.trim_and_fill(es, var)` |
| `comprehensive_analysis()` | 综合发表偏倚分析 | `analysis = tester.comprehensive_analysis(es, var)` |

**发表偏倚检测示例：**

```python
from tools.publication_bias_tester import PublicationBiasTester

tester = PublicationBiasTester()

# 模拟存在潜在发表偏倚的数据
effect_sizes = [0.85, 0.72, 0.68, 0.55, 0.52, 0.45, 0.42, 0.38]
variances = [0.03, 0.04, 0.05, 0.06, 0.04, 0.08, 0.07, 0.09]

# 综合分析
analysis = tester.comprehensive_analysis(effect_sizes, variances)

# Egger检验
print(f"Egger检验: t={analysis['egger_test']['statistic']:.3f}, p={analysis['egger_test']['p_value']:.4f}")
print(f"  {analysis['egger_test']['interpretation']}")

# Fail-safe N
print(f"Fail-safe N: {analysis['fail_safe_n']['fail_safe_n']}")
print(f"  {analysis['fail_safe_n']['interpretation']}")

# Trim-and-fill
print(f"Trim-and-fill估计缺失研究: {analysis['trim_and_fill']['trimmed_studies']}")
print(f"原始效应量: {analysis['trim_and_fill']['original_estimate']:.3f}")
print(f"校正后效应量: {analysis['trim_and_fill']['adjusted_estimate']:.3f}")

# 综合评估
print(f"\n综合评估: {analysis['overall_assessment']}")

# 生成报告
print(tester.generate_report(analysis))
```

---

## 🚫 绝对禁止原则

元分析必须遵循以下绝对禁止原则，任何违反都将严重影响证据质量：

1. **禁止不完整检索** - 必须系统检索多个数据库，未检索=选择性报告
2. **禁止不明确纳入标准** - 必须预先定义PICO和纳入排除标准
3. **禁止忽视质量评估** - 必须对每项研究进行质量/偏倚风险评估
4. **禁止混用效应量** - 不同效应量类型需转换后才能合并
5. **禁止忽视异质性** - 高异质性(I²>75%)时必须探索来源
6. **禁止忽视发表偏倚** - 必须检测并讨论发表偏倚风险
7. **禁止不报告敏感性分析** - 必须验证结果稳健性
8. **禁止不遵循PRISMA** - 必须使用PRISMA流程图报告筛选过程

---

## 5️⃣ 五阶段实施流程

### 阶段1：研究问题与方案 (Protocol)

**目标**：明确研究问题，制定系统综述方案

**关键任务：**
- 构建PICOs问题框架
- 注册系统综述方案(Cochrane, PROSPERO)
- 制定检索策略
- 确定纳入排除标准
- 选择效应量类型
- 确定分析模型
- 准备数据提取表

**PICOs框架：**

```
P - Population (研究对象)
    └─ 目标人群特征、诊断标准

I - Intervention (干预措施)
    └─ 实验组处理方式

C - Comparison (对照)
    └─ 对照组处理方式(安慰剂/标准治疗/无处理)

O - Outcome (结局指标)
    └─ 主要/次要结局指标定义

S - Study design (研究设计)
    └─ RCT、队列、病例对照、横断面
```

### 阶段2：文献筛选 (Study Selection)

**目标**：系统检索和筛选文献

**关键任务：**
- 多数据库系统检索(Cochrane, PubMed, EMBASE, PsycINFO, Web of Science)
- 灰色文献检索(会议论文、学位论文、预印本)
- 导入文献管理软件(EndNote, Zotero, Rayyan)
- 标题摘要筛选(两人独立)
- 全文筛选和理由记录
- PRISMA流程图绘制
- 纳入研究特征编码

**数据库检索策略示例：**

```boolean
# PubMed检索式示例 (心理干预对抑郁的效果)
(("cognitive therapy"[Title/Abstract] OR "behavioral therapy"[Title/Abstract])
  AND ("depression"[MeSH Terms] OR "depressive disorder"[MeSH Terms]))
  AND (randomized controlled trial[Publication Type]
       OR "random*"[Title/Abstract]))
```

### 阶段3：数据提取 (Data Extraction)

**目标**：从每项研究中提取效应量和特征数据

**关键任务：**
- 设计标准化数据提取表
- 培训数据提取员
- 提取研究基本特征(作者、年份、样本量、设计)
- 提取效应量数据(均值、标准差、事件数、相关系数)
- 提取亚组和协变量信息
- 质量评估(Cochrane RoB 2, NOS, Newcastle-Ottawa)
- 交叉核验和争议解决

**质量评估工具对比：**

| 工具 | 适用研究 | 评估维度 |
|------|----------|----------|
| Cochrane RoB 2 | RCT | 选择性偏倚、实施偏倚、随访偏倚、测量偏倚、报告偏倚 |
| ROBINS-I | 非随机干预研究 | 混杂、选择、分类、实施、随访、报告、其他 |
| Newcastle-Ottawa | 观察性研究(队列/病例对照) | 选择、可比性、结局 |
| JBI Checklist | 流行病学研究 | 评价标准因研究类型而异 |

### 阶段4：统计分析 (Statistical Analysis)

**目标**：合并效应量，评估异质性和偏倚

**关键任务：**
- 计算或提取效应量(如需要则转换)
- 选择合并模型(固定/随机)
- 执行异质性检验(Q, I², Tau²)
- 处理高异质性(亚组分析、元回归)
- 发表偏倚检测和校正
- 敏感性分析(剔除高风险研究)
- 累积元分析(按时间顺序)
- 生成森林图和漏斗图

**效应量转换规则：**

```
d ↔ r:  d = 2r/√(1-r²),  r = d/√(d²+4)
d ↔ OR: d = ln(OR)×(√3/π),  OR = exp(d×π/√3)
r ↔ OR: 先转d再转OR，或使用 exp(1.81r)
g → d:  g已做小样本校正，直接使用或转r
```

### 阶段5：报告撰写 (Report Writing)

**目标**：遵循PRISMA标准撰写完整报告

**关键任务：**
- PRISMA 2020清单核对
- 撰写方法部分(检索、筛选、质量评估、分析)
- 报告结果(森林图、异质性、偏倚、亚组)
- 撰写讨论(证据质量、局限性、临床意义)
- 证据质量评级(GRADE)
- 补充材料整理
- 投稿和传播

**PRISMA 2020核心条目：**

| 章节 | 关键条目 |
|------|----------|
| 标题 | 明确标识为系统综述和元分析 |
| 摘要 | 结构化摘要(背景、目的、数据来源、研究纳入、评估偏倚方法等) |
| 引言 | 研究问题PICO化和理由 |
| 方法 | 检索策略、纳入标准、研究选择、数据提取、偏倚风险评估、综合方法 |
| 结果 | 研究选择流程图、研究特征、偏倚风险、结局数据、异质性分析 |
| 讨论 | 证据总结、局限性、结论 |

---

## ✅ 质量标准

### 完整性标准

| 要素 | 最低要求 | 优秀标准 |
|------|----------|----------|
| 检索 | 2个以上数据库 | 多数据库+灰色文献+追踪引用 |
| 筛选 | 明确纳排标准 | 预注册+双盲筛选 |
| 质量评估 | 简要报告 | 使用标准化工具+敏感性分析 |
| 效应量 | 每项研究提取 | 含标准误和置信区间 |
| 偏倚检测 | 一种方法 | 多种方法+校正 |

### 方法论标准

| 要素 | 要求 |
|------|------|
| 方案预注册 | 注册于PROSPERO或Cochrane |
| 效应量计算 | 使用原始数据而非报告值 |
| 模型选择 | 基于异质性检验选择 |
| 异质性处理 | 高异质性时探索来源 |
| 偏倚评估 | 系统性发表偏倚讨论 |

### 深度标准

| 层次 | 描述 |
|------|------|
| 基础报告 | 合并效应量和置信区间 |
| 完整报告 | 含异质性分析和偏倚检测 |
| 高级报告 | 亚组分析+元回归+累积元分析 |
| 最佳报告 | GRADE评级+决策曲线分析 |

---

## 分析流程

```
研究问题 → 检索策略 → 文献筛选 → 数据提取 →
质量评估 → 效应量计算 → 模型选择 → 异质性分析 →
发表偏倚检验 → 亚组分析 → 结果解释 → 报告撰写
    │          │           │          │           │
    ▼          ▼           ▼          ▼           ▼
  PICOs定义  数据库选择   流程图    质量工具   PRISMA清单
  方案注册    检索式构建   双盲筛选  偏倚评估   GRADE评级
```

---

## 效应量解释标准

### Cohen's d 效应量标准

| 效应量 | 小效应 | 中效应 | 大效应 |
|--------|--------|--------|--------|
| d | 0.2 | 0.5 | 0.8 |
| r | 0.1 | 0.3 | 0.5 |
| OR | 1.44 | 2.48 | 4.26 |

### I² 异质性解释标准

| I²范围 | 解释 | 处理建议 |
|--------|------|----------|
| 0-25% | 低异质性 | 固定效应模型足够 |
| 25-50% | 中等异质性 | 考虑随机效应 |
| 50-75% | 较高异质性 | 必须探索异质性来源 |
| 75-100% | 高异质性 | 亚组分析+报告预测区间 |

---

## 方法论参考

### 核心文献

1. Borenstein, M., et al. (2021). *Introduction to Meta-Analysis*. 2nd Ed. Wiley.
2. Higgins, J. P. T., et al. (2019). *Cochrane Handbook for Systematic Reviews*. Cochrane.
3. Lipsey, M. W., & Wilson, D. B. (2001). *Practical Meta-Analysis*. Sage.
4. Cooper, H., et al. (2019). *The Handbook of Research Synthesis and Meta-Analysis*. 3rd Ed.

### 报告标准

- **PRISMA 2020** - 系统综述和元分析报告规范
- **MOOSE** - 观察性研究的元分析报告
- **QUORUM** - 元分析报告质量规范

---

**版本**: 5.0.0
**创建时间**: 2026-03-15
**证据等级**: Level I（最高等级）