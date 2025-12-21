---
name: data-analysis
description: 执行数据分析，包括数据清洗、探索性分析、统计建模、可视化和结果解释等。结合定性洞察与定量计算。
license: MIT
compatibility: Python 3.8+, pandas, numpy, matplotlib, seaborn, scikit-learn
metadata:
  domain: data-science
  methodology: mixed-methods
  complexity: advanced
  version: 1.0.0
  integration_type: qualitative_quantitative
  author: zhangshuren@hznu.edu.cn
  website: http://agentpsy.com
allowed-tools: python bash read_file write_file task
---

# 数据分析技能

## 🧠 渐进式披露架构

### Level 1: 核心元数据 (Token: ~100)
- **技能**: 数据分析能力
- **触发**: 需要复杂数据分析时自动激活
- **方法**: 混合方法数据分析

### Level 2: 操作框架 (Token: ~500)
- **五阶段流程**: 数据理解→数据清洗→探索分析→建模→解释
- **AI协作**: 定性洞察 + 定量计算
- **智能决策**: 自动调用适当工具

### Level 3: 专业提示词 (按需加载)
- [数据理解](./prompts/data-understanding.md) | [数据清洗](./prompts/data-cleaning.md) | [探索分析](./prompts/exploratory-analysis.md) | [建模策略](./prompts/modeling-strategy.md) | [结果解释](./prompts/result-interpretation.md)

### Level 4: 计算脚本 (直接调用)
- [数据清洗](./scripts/data_cleaning.py) | [探索分析](./scripts/exploratory_analysis.py) | [统计建模](./scripts/statistical_modeling.py) | [可视化](./scripts/visualization.py) | [集成分析](./scripts/integrated_analysis.py)

## 🔄 定性定量结合机制

### 定性分析 (AI职责)
1. **数据理解** - 业务背景、变量意义 [→ 数据理解提示](./prompts/data-understanding.md)
2. **清洗策略** - 异常值处理、缺失值策略 [→ 数据清洗提示](./prompts/data-cleaning.md)
3. **结果解释** - 统计结果的业务含义 [→ 结果解释提示](./prompts/result-interpretation.md)

### 定量计算 (脚本职责)
1. **数据清洗** - 异常值检测、缺失值处理 (`data_cleaning.py`)
2. **探索分析** - 描述统计、相关分析 (`exploratory_analysis.py`)
3. **统计建模** - 回归、分类、聚类 (`statistical_modeling.py`)
4. **可视化** - 图表生成 (`visualization.py`)

## 📋 五阶段分析流程

1. **数据理解** → AI加载[数据理解提示](./prompts/data-understanding.md)进行业务背景分析
2. **数据清洗** → AI结合[数据清洗提示](./prompts/data-cleaning.md)制定清洗策略，脚本执行
3. **探索分析** → AI基于[探索分析提示](./prompts/exploratory-analysis.md)指导分析方向，脚本执行
4. **建模策略** → AI使用[建模策略提示](./prompts/modeling-strategy.md)选择模型，脚本执行
5. **结果解释** → AI基于[结果解释提示](./prompts/result-interpretation.md)进行深度解读

## 📚 参考资源

- [方法论详解](./references/METHODOLOGY.md) - 数据分析核心概念与步骤
- [最佳实践](./references/BEST_PRACTICES.md) - 数据分析要点
- [报告模板](./assets/templates/report_template.md) - 结果呈现格式

## 🚀 快速开始

```bash
cd data-analysis/
python scripts/integrated_analysis.py
```

---

**AI职责**: 业务理解与结果解释（定性分析） | **脚本职责**: 精确计算（定量分析） | **协作机制**: 智能决策引擎