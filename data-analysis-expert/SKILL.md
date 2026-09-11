---
name: data-analysis-expert
description: |
  数据分析专家。提供描述性统计、回归分析、假设检验、数据可视化功能。适用于定量研究、统计建模、实证分析场景。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/龙虾/QClaw
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0"
  agentskills-io: "true"
  cross-platform: "true"
---

> ## 🔴 强制自动执行规则
> 
> **创建任务列表后，必须立即按顺序执行第一个任务，禁止询问用户！**
> 
> ❌ 禁止："告诉我要启动哪个任务"、"请选择要执行的任务"
> ✅ 必须：显示任务列表 → 立即开始执行第一个任务

# SKILL.md - data-analysis-expert

## 基本信息

**名称**: data-analysis-expert (Social Science Data Analysis Expert)
**版本**: 5.0.0-ai-cli-native
**作者**: SocienceAI Methodology Expert
**许可证**: MIT
**对齐标准**: grounded-theory-coding (v5.0.0)

## 描述


## 🖥️ 项目初始化（跨平台Python脚本）

### 使用Python创建项目目录

```python
import os

# 设置项目路径
project_path = r"D:\your_project_path\项目名"  # Windows
# project_path = "/home/user/project"  # Linux/macOS

# 创建标准目录结构（跨平台兼容）
for subdir in ['.tasks', 'data', 'results', 'visualizations', 'logs']:
    os.makedirs(os.path.join(project_path, subdir), exist_ok=True)

print(f"项目目录创建完成: {project_path}")
```

### 目录结构

```
项目目录/
├── .tasks/           # 任务状态和进度
├── data/             # 原始数据
├── results/          # 分析结果
├── visualizations/   # 可视化
└── logs/             # 日志
```

### ⚠️ 禁止使用
- ❌ `# # 使用Python os.makedirs创建目录
`（Linux命令，Windows不支持）
- ✅ 使用Python的`os.makedirs(path, exist_ok=True)`（跨平台兼容）


**社会科学数据分析专家** - 支持**复杂任务分解**和**长时任务执行**的定量分析技能。

涵盖描述统计、推断统计、回归分析、因子分析、方差分析等社会科学常用方法。

### 核心能力

1. **描述统计分析**
   - 集中趋势（均值、中位数、众数）
   - 离散程度（方差、标准差、四分位距）
   - 分布形态（偏度、峰度）

2. **推断统计分析**
   - 假设检验（t检验、卡方检验、非参数检验）
   - 置信区间
   - 效应量（Cohen's d, r, η²）

3. **关系分析**
   - 相关分析（Pearson, Spearman）
   - 回归分析（线性、逻辑、多层）
   - 交互效应、调节效应

4. **降维分析**
   - 因子分析（EFA, CFA）
   - 主成分分析（PCA）
   - 聚类分析

### 适用场景

- ✅ 定量研究设计
- ✅ 问卷调查分析
- ✅ 实验数据分析
- ✅ 二次数据分析
PZ|
## 🔧 Python 工具

python tools:

#### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | analyze.py | 主分析入口，调度各工具 |
| 2 | prepare-data.py | 数据准备与清洗 |
| 3 | calculate-descriptive.py | 描述性统计计算 |
| 4 | data_quality_checker.py | 数据质量检查 |
| 5 | run-regression.py | 回归分析 |
| 6 | run-inferential.py | 推断统计检验 |
| 7 | generate-visualization.py | 生成可视化图表 |
| 8 | planning-integration.py | 任务规划集成 |

#### 使用示例

```bash
# 1. 数据准备
python tools/prepare-data.py -i data/raw.csv -o results/cleaned.csv

# 2. 描述统计
python tools/calculate-descriptive.py -i results/cleaned.csv -o results/descriptive.json

# 3. 数据质量检查
python tools/data_quality_checker.py -i results/cleaned.csv -o results/quality.json

# 4. 回归分析
python tools/run-regression.py -i results/cleaned.csv --model linear -o results/regression.json

# 5. 推断统计
python tools/run-inferential.py -i results/cleaned.csv --test ttest -o results/inferential.json

# 6. 可视化
python tools/generate-visualization.py -i results/cleaned.csv --type histogram -o results/plots/
```

JK|## ⚠️ 六大绝对禁止原则
## ⚠️ 六大绝对禁止原则

### 1. 禁止脱离分析数据

**错误做法**:
```yaml
不看数据就跑模型:
  - 不检查分布
  - 不检查异常值
  - 不检查缺失值
  - 直接运行回归
```

**正确做法**:
```yaml
数据探索优先:
  Step 1: 描述统计
    - 分布形态（直方图、Q-Q图）
    - 异常值（箱线图、Z分数）
    - 缺失值模式

  Step 2: 数据清洗
    - 处理异常值
    - 处理缺失值
    - 变量转换

  Step 3: 假设检验
    - 正态性检验（Shapiro-Wilk）
    - 方差齐性检验（Levene）
    - 线性检验
```

**量化标准**:
- ✅ 任何分析前必须先探索数据
- ✅ 报告描述统计（N, M, SD, 范围）
- ✅ 报告假设检验结果

### 2. 禁止p值崇拜

**错误做法**:
```yaml
只关注p值:
  - "p<0.05，显著！"
  - "p>0.05，不显著，没用"
  - 忽视效应量
  - 忽视置信区间

p-hacking:
  - 尝试多种分析直到p<0.05
  - 选择性报告结果
  - HARKing (Hypothesizing After Results are Known)
```

**正确做法**:
```yaml
全面报告:
  1. 效应量（Effect Size）
     - Cohen's d（t检验）
     - r（相关）
     - η²（ANOVA）
     - OR/RR（比值比/相对风险）

  2. 置信区间（Confidence Interval）
     - 95% CI
     - 精确性指示

  3. 实际显著性（Practical Significance）
     - 不只统计显著性
     - 考虑实际意义

  4. 透明性
     - 报告所有分析（包括不显著的）
     - 不p-hacking
     - 预注册研究设计
```

**量化标准**:
- ✅ 总是报告效应量
- ✅ 总是报告置信区间
- ✅ 讨论实际意义

### 3. 禁止忽视假设违反

**错误做法**:
```yaml
忽视假设违反:
  - 数据不正态但用t检验
  - 方差不齐但用ANOVA
  - 线性不存在但用线性回归
  - "没关系，样本大"

结果:
  - 第一类错误（假阳性）
  - 第二类错误（假阴性）
  - 效应量估计偏差
```

**正确做法**:
```yaml
检验并处理假设违反:
  1. 正态性检验
     - Shapiro-Wilk test
     - Q-Q plot
     - 如违反：转换数据或用非参数检验

  2. 方差齐性检验
     - Levene's test
     - 如违反：用Welch's t检验或非参数

  3. 线性检验
     - Scatterplot
     - 如违反：非线性模型

  4. 多重共线性检验
     - VIF (Variance Inflation Factor)
     - 如违反：删除变量或正则化
```

**量化标准**:
- ✅ 每个分析前检验假设
- ✅ 报告假设检验结果
- ✅ 如违反，使用替代方法

### 4. 禁止混淆相关与因果

**错误做法**:
```yaml
相关=因果:
  - "X与Y相关，所以X导致Y"
  - 忽视混淆变量
  - 忽视反向因果
  - 过度推断

示例:
  "冰淇淋销量与溺水人数相关（r=0.8），
   所以冰淇淋导致溺水"
   （混淆变量：气温）
```

**正确做法**:
```yaml
谨慎推断因果:
  1. 识别混淆变量
     - 统计控制（回归中的控制变量）
     - 匹配（ propensity score matching）
     - 实验设计（随机对照）

  2. 考虑反向因果
     - X→Y 还是 Y→X?
     - 使用滞后变量
     - 使用工具变量

  3. 谨慎表述
     - ❌ "X导致Y"
     - ✅ "X与Y相关，控制Z后仍显著"
     - ✅ "结果与X的因果效应一致，但..."
```

**量化标准**:
- ✅ 区分观察研究与实验研究
- ✅ 观察研究用谨慎语言
- ✅ 讨论局限性

### 5. 禁止多重比较忽视

**错误做法**:
```yaml
忽视多重比较问题:
  - 运行10个t检验，不校正
  - p<0.05就显著
  - 第一类错误累积

问题:
  - 单次检验α=0.05
  - 10次检验→α=1-(1-0.05)^10 ≈ 0.40
  - 假阳性率40%！
```

**正确做法**:
```yaml
多重比较校正:
  方法1: Bonferroni校正
    - α' = α / k （k=比较次数）
    - 保守但简单

  方法2: Holm-Bonferroni
    - 逐步校正
    - 比Bonferroni不保守

  方法3: FDR (False Discovery Rate)
    - Benjamini-Hochberg
    - 平衡发现与错误

  方法4: 事先计划
    - 限制比较次数
    - 预注册假设
```

**量化标准**:
- ✅ 多次比较必须校正
- ✅ 报告校正方法
- ✅ 区分探索性与验证性分析

### 6. 禁止不透明的分析

**错误做法**:
```yaml
黑箱分析:
  - 不报告具体方法
  - 不报告参数设置
  - 不报告数据处理步骤
  - 无法复现

示例:
  "使用回归分析，结果显示X影响Y（p<0.05）"

问题:
  - 哪种回归？
  - 有哪些控制变量？
  - 数据如何处理？
  - 无法评估和复现
```

**正确做法**:
```yaml
完全透明:
  报告所有细节:
    1. 数据来源
    2. 样本大小
    3. 变量操作化
    4. 分析方法（包括参数）
    5. 软件和版本
    6. 完整结果（包括不显著的）
    7. 数据和代码共享

  示例:
    "使用OLS回归分析，
    因变量：Y（定义...）
    自变量：X（定义...）
    控制变量：Z1, Z2（定义...）
    样本：N=200
    软件：R 4.3.0, lm()函数
    结果：β=0.35, SE=0.12, t=2.92, p=0.004, 95%CI[0.11,0.59]"
```

**量化标准**:
- ✅ 任何可复现的研究都能复现
- ✅ 报告所有分析决策
- ✅ 共享数据和代码

## 📋 任务分解规则

### 四大原则



## 详细指南

完整的使用指南请参考: [详细指南](references/detailed-guide.md)