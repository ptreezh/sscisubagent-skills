---
name: fsqca-analysis
description: 执行模糊集定性比较分析(fsQCA)，结合定性理论分析与定量计算。包含理论分析、校准指导、定量计算、结果解释四个阶段。
license: MIT
compatibility: Python 3.8+, pandas, numpy
metadata:
  domain: qualitative-comparative-analysis
  methodology: fsQCA
  complexity: advanced
  version: 1.0.0
  integration_type: qualitative_quantitative
  author: socienceAI.com
  website: http://agentpsy.com
allowed-tools: python bash read_file write_file task
---

# fsQCA分析技能

## 🧠 渐进式披露架构

### Level 1: 核心元数据 (Token: ~100)
- **技能**: fsQCA分析能力
- **触发**: 复杂因果机制分析
- **方法**: 模糊集定性比较分析

### Level 2: 操作框架 (Token: ~500)
- **四阶段流程**: 理论→校准→定量→解释
- **AI协作**: 定性思考 + 定量计算
- **智能决策**: 自动调用适当工具

### Level 3: 专业提示词 (按需加载)
- [理论分析](./prompts/theoretical-analysis.md) | [校准指导](./prompts/calibration-guidance.md) | [结果解释](./prompts/result-interpretation.md)

### Level 4: 计算脚本 (直接调用)
- [校准](./scripts/calibration.py) | [真值表](./scripts/truth_table.py) | [最小化](./scripts/minimization.py) | [集成分析](./scripts/integrated_analysis.py)

## 🔄 定性定量结合机制

### 定性分析 (AI职责)
1. **理论构建** - 概念定义、条件选择 [→ 理论分析提示](./prompts/theoretical-analysis.md)
2. **校准策略** - 隶属度函数选择 [→ 校准指导提示](./prompts/calibration-guidance.md)
3. **结果阐释** - 因果机制解释 [→ 结果解释提示](./prompts/result-interpretation.md)

### 定量计算 (脚本职责)
1. **模糊集校准** - 隶属度计算 (`calibration.py`)
2. **真值表构建** - 一致性与覆盖度 (`truth_table.py`)
3. **逻辑最小化** - 解生成与评估 (`minimization.py`)

## 📋 四阶段分析流程

1. **理论构建** → AI加载[理论分析提示](./prompts/theoretical-analysis.md)进行深度理论分析
2. **校准规划** → AI结合数据特征与[校准指导提示](./prompts/calibration-guidance.md)制定校准方案
3. **定量分析** → 脚本执行确定性计算（校准→真值表→最小化）
4. **结果解释** → AI基于定量结果和[结果解释提示](./prompts/result-interpretation.md)进行深度阐释

## 📚 参考资源

- [方法论详解](./references/METHODOLOGY.md) - fsQCA核心概念与步骤
- [最佳实践](./references/BEST_PRACTICES.md) - 研究设计与分析要点
- [报告模板](./assets/templates/report_template.md) - 结果呈现格式

## 🚀 快速开始

```bash
cd fsqca-analysis/
python scripts/integrated_analysis.py
```

---

**AI职责**: 理论思考与结果解释（定性分析） | **脚本职责**: 精确计算（定量分析） | **协作机制**: 智能决策引擎