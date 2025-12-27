# 研究设计技能 (Research Design Skill)

## 概述

研究设计技能是一个综合性的研究方法论工具，旨在帮助研究人员从问题定义到设计评估的整个研究设计过程中提供专业指导。该技能结合了定性理论分析与定量计算，确保研究设计的科学性、可行性和伦理性。

## 功能特性

### 1. 文献分析
- 分析出版趋势和研究主题
- 识别知识缺口和研究机会
- 生成文献分析报告

### 2. 方法匹配
- 基于研究目的匹配最适合的研究方法
- 评估不同设计的适用性
- 提供方法选择建议

### 3. 设计评估
- 评估研究设计的各个方面（科学严谨性、可行性、伦理完整性等）
- 识别设计中的优势和劣势
- 提供改进建议

### 4. 综合分析
- 集成所有分析结果
- 提供完整的研究设计建议
- 生成详细的实施计划

## 依赖管理

本技能使用uv进行依赖管理。所有依赖都已在pyproject.toml中明确定义。

### 安装依赖
```bash
# 使用uv安装依赖
uv sync
```

### 依赖说明
- **必需依赖**: pandas, numpy (用于数据处理和数值计算)
- **可选依赖**: pytest, black, mypy (用于开发和测试)

## 使用方法

### 基本用法
```python
from scripts.integrated_analysis import IntegratedResearchDesigner

# 创建设计师实例
designer = IntegratedResearchDesigner()

# 准备文献数据
literature_data = pd.DataFrame({...})

# 定义研究上下文
research_context = {
    'research_topic': '研究主题',
    'research_purpose': '探索和解释',
    'target_population': '目标人群',
    'target_sample_size': 300,
    'time_constraint': 'medium',
    'resource_level': 'adequate',
    'ethical_sensitivity': True,
    'research_questions': ['研究问题1', '研究问题2']
}

# 定义设计元素
design_elements = {
    'theoretical_framework': '理论框架',
    'research_hypotheses': ['假设1', '假设2'],
    'sampling_strategy': '抽样策略',
    # ... 更多设计元素
}

# 执行完整分析
results = designer.execute_complete_analysis(
    literature_data,
    research_context,
    design_elements
)

# 获取最终推荐
recommendation = results['final_recommendation']
```

## 模块说明

### scripts/
- `literature_analysis.py`: 文献分析模块
- `method_matching.py`: 方法匹配模块
- `design_evaluation.py`: 设计评估模块
- `integrated_analysis.py`: 集成分析模块

### prompts/ - 专业提示词（按需加载）
- `problem-definition.md`: [问题定义专家提示](./prompts/problem-definition.md) | [详纲](./prompts/problem-definition-outline.md)
- `method-selection.md`: [方法选择专家提示](./prompts/method-selection.md) | [详纲](./prompts/method-selection-outline.md)
- `data-planning.md`: [数据计划专家提示](./prompts/data-planning.md) | [详纲](./prompts/data-planning-outline.md)
- `analysis-strategy.md`: [分析策略专家提示](./prompts/analysis-strategy.md) | [详纲](./prompts/analysis-strategy-outline.md)
- `ethics-review.md`: [伦理审查专家提示](./prompts/ethics-review.md) | [详纲](./prompts/ethics-review-outline.md)

### references/
- `methodology.md`: [研究方法论详解](./references/methodology.md) | [详纲](./references/methodology-outline.md)
- `best-practices.md`: [研究设计最佳实践](./references/best-practices.md) | [详纲](./references/best-practices-outline.md)

### assets/templates/
- `research_design_template.md`: 研究设计模板

## 渐进式披露架构

### Level 1: 核心元数据 (~100 tokens)
- **技能**: 研究设计能力
- **触发**: 需要系统化研究设计时
- **方法**: 混合方法研究设计

### Level 2: 操作框架 (~500 tokens)
- **六阶段流程**: 问题定义→文献综述→方法选择→数据计划→分析策略→伦理审查
- **AI协作**: 定性思考 + 定量计算
- **智能决策**: 自动调用适当工具

### Level 3: 专业提示词 (按需加载)
- [问题定义](./prompts/problem-definition.md) | [方法选择](./prompts/method-selection.md) | [数据计划](./prompts/data-planning.md) | [分析策略](./prompts/analysis-strategy.md) | [伦理审查](./prompts/ethics-review.md)

### Level 4: 计算脚本 (直接调用)
- [文献分析](./scripts/literature_analysis.py) | [方法匹配](./scripts/method_matching.py) | [设计评估](./scripts/design_evaluation.py) | [集成分析](./scripts/integrated_analysis.py)

## 定性定量结合机制

### 定性分析 (AI职责)
1. **问题构建** - 研究问题定义 [→ 问题定义提示](./prompts/problem-definition.md)
2. **方法选择** - 研究方法匹配 [→ 方法选择提示](./prompts/method-selection.md)
3. **数据计划** - 数据收集策略 [→ 数据计划提示](./prompts/data-planning.md)
4. **分析策略** - 分析计划制定 [→ 分析策略提示](./prompts/analysis-strategy.md)
5. **伦理审查** - 伦理风险评估 [→ 伦理审查提示](./prompts/ethics-review.md)

### 定量计算 (脚本职责)
1. **文献分析** - 趋势、主题、知识缺口分析 (`literature_analysis.py`)
2. **方法匹配** - 研究目的与设计匹配 (`method_matching.py`)
3. **设计评估** - 质量、可行性、伦理评估 (`design_evaluation.py`)
4. **集成分析** - 综合分析与推荐 (`integrated_analysis.py`)

## 应用场景

1. **学术研究**: 为学者提供系统的研究设计指导
2. **政策分析**: 为政策制定者提供实证研究设计
3. **商业调研**: 为企业提供市场研究设计
4. **社会调查**: 为社会科学研究提供方法论支持

## 技术特点

- **渐进式披露**: 四层架构，按需加载最小上下文
- **定性定量结合**: AI负责定性分析，脚本负责定量计算
- **模块化设计**: 各模块功能独立，便于维护和扩展
- **健壮性**: 处理各种边界情况和错误，避免运行时警告
- **依赖管理**: 使用uv进行依赖管理，明确依赖范围

## 许可证

MIT License