---
name: research-design
description: 执行研究设计，包括问题定义、方法选择、数据收集计划、分析策略和伦理考虑等
license: MIT
compatibility: Python 3.8+
dependencies:
  required:
    - pandas>=1.5.0,<3.0.0
    - numpy>=1.21.0,<2.0.0
  optional:
    - pytest>=7.0.0 (for testing)
    - black>=22.0.0 (for formatting)
    - mypy>=0.950 (for type checking)
dependency-manager: uv
metadata:
  domain: research-methodology
  methodology: mixed-methods
  complexity: advanced
  version: 1.0.0
  integration_type: qualitative_quantitative
  author: zhangshuren@hznu.edu.cn
  website: http://agentpsy.com
allowed-tools: python bash read_file write_file task
---

# 研究设计技能

## 🧠 渐进式披露架构

### Level 1: 核心元数据 (Token: ~100)
- **技能**: 研究设计能力
- **触发**: 需要系统化研究设计时自动激活
- **方法**: 混合方法研究设计

### Level 2: 操作框架 (Token: ~500)
- **六阶段流程**: 问题定义→文献综述→方法选择→数据计划→分析策略→伦理审查
- **AI协作**: 定性思考 + 定量规划
- **智能决策**: 自动调用适当工具

### Level 3: 专业提示词 (按需加载)
- [问题定义](./prompts/problem-definition.md) | [方法选择](./prompts/method-selection.md) | [数据计划](./prompts/data-planning.md) | [分析策略](./prompts/analysis-strategy.md) | [伦理审查](./prompts/ethics-review.md)

### Level 4: 计算脚本 (直接调用)
- [文献分析](./scripts/literature_analysis.py) | [方法匹配](./scripts/method_matching.py) | [设计评估](./scripts/design_evaluation.py) | [集成分析](./scripts/integrated_analysis.py)

## 🔄 定性定量结合机制

### 定性分析 (AI职责)
1. **问题定义** - 研究问题构建 [→ 问题定义提示](./prompts/problem-definition.md)
2. **方法选择** - 研究方法匹配 [→ 方法选择提示](./prompts/method-selection.md)
3. **伦理审查** - 伦理风险评估 [→ 伦理审查提示](./prompts/ethics-review.md)

### 定量规划 (脚本职责)
1. **样本计算** - 样本量确定 (`sample_size_calculation.py`)
2. **统计功效** - 效力分析 (`power_analysis.py`)
3. **设计评估** - 设计质量评估 (`design_evaluation.py`)

## 📋 六阶段分析流程

1. **问题定义** → AI加载[问题定义提示](./prompts/problem-definition.md)进行研究问题构建
2. **文献综述** → AI结合[文献分析脚本](./scripts/literature_analysis.py)进行理论基础构建
3. **方法选择** → AI基于研究问题与[方法选择提示](./prompts/method-selection.md)匹配合适方法
4. **数据计划** → AI使用[数据计划提示](./prompts/data-planning.md)制定数据收集策略
5. **分析策略** → AI根据数据特征与[分析策略提示](./prompts/analysis-strategy.md)制定分析计划
6. **伦理审查** → AI基于[伦理审查提示](./prompts/ethics-review.md)进行伦理风险评估

## 📚 参考资源

- [方法论详解](./references/methodology.md) - 研究设计核心概念与步骤
- [最佳实践](./references/best-practices.md) - 研究设计要点
- [报告模板](./assets/templates/research_design_template.md) - 设计文档格式

## 🚀 快速开始

```bash
cd research-design/
python scripts/integrated_analysis.py
```

---

**AI职责**: 研究问题构建与方法选择（定性分析） | **脚本职责**: 统计计算与设计评估（定量规划） | **协作机制**: 智能决策引擎