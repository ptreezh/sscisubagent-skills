---
name: mathematical-statistics
description: 当用户需要执行社会科学研究的数理统计分析，包括描述性统计、推断统计、回归分析、方差分析、因子分析等时使用此技能
version: 1.0.0
author: socienceAI.com
tags: [statistics, social-sciences, data-analysis, research-methods, descriptive-stats, inferential-stats, regression-analysis]
---

# 数理统计分析技能 (Mathematical Statistics Analysis)

## Overview
为社会科学研究提供全面的数理统计分析支持，包括描述性统计、推断统计、回归分析、方差分析、因子分析等，确保研究数据分析的科学性和准确性。

## When to Use This Skill
Use this skill when the user requests:
- Statistical analysis of social science data
- Descriptive statistics (means, standard deviations, distributions)
- Inferential statistics (t-tests, ANOVA, chi-square tests)
- Regression analysis (linear, logistic, multiple)
- Factor analysis or other multivariate techniques
- Reliability and validity analysis
- Data visualization for statistical results
- Interpretation of statistical outputs

## Quick Start
When a user requests statistical analysis:
1. **Understand** the research question and data structure
2. **Select** appropriate statistical methods based on data and question
3. **Execute** analysis with proper diagnostics
4. **Interpret** results in the context of the research question
5. **Visualize** findings appropriately

## 使用时机

当用户提到以下需求时，使用此技能：
- "数理统计" 或 "统计分析"
- "描述性统计" 或 "数据概览"
- "推断统计" 或 "假设检验"
- "回归分析" 或 "相关分析"
- "方差分析" 或 "ANOVA"
- "因子分析" 或 "主成分分析"
- 需要进行定量数据分析

## 快速开始

### 工具链（3个核心脚本）

```bash
# 1. 描述性统计
python scripts/descriptive_statistics.py \
  --input data.csv \
  --output descriptive_stats.json

# 2. 推断统计
python scripts/inferential_statistics.py \
  --input data.csv \
  --test t-test \
  --output inferential_results.json

# 3. 回归分析
python scripts/regression_analysis.py \
  --input data.csv \
  --dependent var1 \
  --independent var2,var3,var4 \
  --output regression_results.json
```

## 核心流程

### 第一步：数据预处理

使用预处理工具清洗数据：
```bash
python scripts/preprocess_data.py --input raw_data.csv --output clean_data.csv
```

**关键要点**：
- 数据质量检查
- 缺失值处理
- 异常值检测
- 数据分布验证

详见：`references/data-preparation.md`

### 第二步：描述性统计

使用统计工具计算基础指标：
```bash
python scripts/descriptive_statistics.py --input clean_data.csv --output desc_stats.json
```

**计算指标**：
- 集中趋势：均值、中位数、众数
- 离散程度：标准差、方差、范围
- 分布形状：偏度、峰度
- 频数分布：计数、百分比

详见：`references/descriptive-statistics.md`

### 第三步：推断统计

根据数据特征选择合适的推断统计方法：
```bash
python scripts/inferential_statistics.py --input clean_data.csv --output inference.json
```

**分析类型**：
- 参数检验：t检验、ANOVA、相关分析
- 非参数检验：Mann-Whitney U、Kruskal-Wallis
- 关联分析：卡方检验、Fisher精确检验

详见：`references/inferential-statistics.md`

### 第四步：回归分析

建立变量间的关系模型：
```bash
python scripts/regression_analysis.py --input clean_data.csv --output regression.json
```

**回归类型**：
- 线性回归：简单线性、多元线性
- 逻辑回归：二元、多项
- 高级回归：岭回归、LASSO、分位数回归

详见：`references/regression-analysis.md`

### 第五步：多变量分析

进行高级统计分析：
```bash
python scripts/multivariate_analysis.py --input clean_data.csv --output multivariate.json
```

**分析方法**：
- 因子分析：探索性、验证性
- 聚类分析：K均值、层次聚类
- 主成分分析：降维、变量选择

详见：`references/multivariate-analysis.md`

### 第六步：结果可视化

生成统计图表：
```bash
python scripts/visualize_statistics.py \
  --input clean_data.csv \
  --stats desc_stats.json \
  --output statistical_plots.png
```

**可视化类型**：
- 分布图：直方图、箱线图、密度图
- 关系图：散点图、相关矩阵热图
- 比较图：柱状图、误差条图
- 模型图：回归线、残差图

详见：`references/statistical-visualization.md`

## 输出格式

统一的三层JSON格式：

```json
{
  "summary": {
    "sample_size": 200,
    "variables_count": 8,
    "analysis_type": "multiple_regression",
    "significant_findings": 3,
    "model_fit": 0.72,
    "assumptions_met": true
  },
  "details": {
    "descriptive_stats": {...},
    "inferential_results": {...},
    "regression_output": {...},
    "model_diagnostics": {...}
  },
  "metadata": {
    "timestamp": "2025-12-21T10:30:00",
    "version": "1.0.0"
  }
}
```

详见：`references/output-format.md`

## 质量检查清单

在完成统计分析后，请检查以下项目：

- [ ] 数据质量检查完成（缺失值、异常值、分布）
- [ ] 统计方法选择合适（符合数据特征和研究问题）
- [ ] 统计假设验证通过（正态性、方差齐性等）
- [ ] 效应量和置信区间报告完整
- [ ] 结果解释准确（统计显著性与实际意义区分）
- [ ] 可视化清晰（图表标题、坐标轴、图例完整）

详见：`references/quality-checklist.md`

## 常见问题

**快速诊断**：
- 数据格式问题 → 见 `references/troubleshooting.md` - 数据预处理
- 统计方法选择困难 → 使用 `method_selector.py` 辅助选择
- 结果解释困难 → 见 `references/interpretation-guide.md`
- 假设检验失败 → 见 `references/nonparametric-alternatives.md`

## 深入学习

- **统计理论**：`references/statistical-theory.md` - 方法原理和公式
- **实践案例**：`references/case-studies.md` - 完整分析示例
- **故障排除**：`references/troubleshooting.md` - 问题诊断和解决
- **中文语境**：`references/chinese-context.md` - 数据和解释特点

## 完成标志

完成高质量的统计分析应该：
1. 提供准确完整的统计指标
2. 选择合适的统计方法
3. 验证统计假设
4. 给出清晰的解释和建议

---

*此技能为中文社会科学研究提供全面的数理统计支持，从数据预处理到高级分析的技术实现，确保研究的科学性和严谨性。*