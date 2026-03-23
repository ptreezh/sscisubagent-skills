---
name: meta-analysis-expert
description: |
  元分析专家。提供系统性文献综述和元分析全流程支持，包括文献检索策略、研究质量评估、效应量计算、异质性检验、发表偏倚检测和亚组分析。适用于循证研究、证据合成和研究综合。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/龙虾/QClaw
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0"
  agentskills-io: "true"
  cross-platform: "true"
  methodology: "Meta-Analysis"
  evidence-level: "Level I (Highest)"
---

# Meta-Analysis Expert | 元分析专家

## 概述

元分析专家是一个专门支持系统性文献综述和元分析的研究方法技能。元分析是证据等级金字塔的顶端方法，通过统计合成多个研究结果来提供最强有力的证据。

## 核心能力

### 1. 文献综述阶段
- PRISMA流程图生成
- 文献检索策略设计
- 纳入/排除标准制定
- 研究筛选记录

### 2. 数据提取阶段
- 效应量计算（d, g, r, OR, RR等）
- 研究特征编码
- 质量评估工具（Cochrane RoB, NOS, Newcastle-Ottawa等）

### 3. 统计分析阶段
- 固定效应模型
- 随机效应模型
- 异质性检验（Q检验, I², Tau²）
- 发表偏倚检测（漏斗图, Egger检验, Trim-and-fill）

### 4. 高级分析
- 亚组分析
- 元回归
- 敏感性分析
- 累积元分析

## 支持的效应量类型

| 类型 | 符号 | 适用场景 |
|------|------|----------|
| 标准化均差 | d, g | 连续变量，组间比较 |
| 相关系数 | r | 关联研究 |
| 优势比 | OR | 二分类变量 |
| 相对风险 | RR | 二分类变量 |
| 风险差 | RD | 二分类变量 |
| 发生率比 | IRR | 计数数据 |

## 分析流程

```
研究问题 → 检索策略 → 文献筛选 → 数据提取 → 
质量评估 → 效应量计算 → 模型选择 → 异质性分析 → 
发表偏倚检验 → 亚组分析 → 结果解释 → 报告撰写
```

## 质量标准

### PRISMA 2020 检查清单
- 标题标识
- 摘要结构化
- 研究问题（PICO）
- 检索策略
- 筛选流程
- 数据提取
- 质量评估
- 统计方法
- 结果报告
- 讨论局限

### 方法质量评估
- AMSTAR 2（系统性综述）
- Cochrane RoB 2（RCT）
- ROBINS-I（非随机研究）
- Newcastle-Ottawa Scale（观察性研究）

## 使用场景

1. **循证医学**：治疗效果综合评估
2. **心理学研究**：效应大小估计
3. **教育研究**：干预效果评估
4. **社会科学**：研究综合与证据合成
5. **政策评估**：项目效果元分析

## 工具函数

### Python工具

- `effect_size_calculator.py` - 效应量计算
- `heterogeneity_analyzer.py` - 异质性分析
- `publication_bias_tester.py` - 发表偏倚检测
- `subgroup_analyzer.py` - 亚组分析
- `forest_plot_generator.py` - 森林图生成

### 子智能体

- 文献筛选智能体
- 数据提取智能体
- 质量评估智能体
- 统计分析智能体
- 报告撰写智能体

## 报告输出

1. **PRISMA流程图**：文献筛选可视化
2. **森林图**：效应量及其置信区间
3. **漏斗图**：发表偏倚可视化
4. **异质性报告**：Q, I², Tau²统计
5. **敏感性分析表**：逐一排除结果

## 方法论参考

### 核心文献

1. Borenstein, M., et al. (2021). *Introduction to Meta-Analysis*. 2nd Ed.
2. Higgins, J. P. T., et al. (2019). *Cochrane Handbook for Systematic Reviews*.
3. Lipsey, M. W., & Wilson, D. B. (2001). *Practical Meta-Analysis*.
4. Cooper, H., et al. (2019). *The Handbook of Research Synthesis and Meta-Analysis*. 3rd Ed.

### 报告标准

- PRISMA 2020
- MOOSE（观察性研究）
- Cochrane手册

---

**版本**: 5.0.0  
**创建时间**: 2026-03-15  
**证据等级**: Level I（最高等级）
