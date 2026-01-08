---
name: field-expert
description: 布迪厄场域理论专家分析技能，整合场域边界识别、资本分析、习性分析和场域动力学分析功能，基于渐进式信息披露原则支持宿主agent动态加载提示词模板。
version: 2.0.0
author: socienceAI.com
license: MIT
tags: [field-analysis, bourdieu, social-structure, cultural-capital, power-relations, boundary-identification, capital-analysis, habitus-analysis]
compatibility: Claude 3.5 Sonnet and above, iFlow CLI
metadata:
  domain: sociology
  methodology: field-theory
  complexity: advanced
  last_updated: "2026-01-06"
allowed-tools: [python, bash, read_file, write_file, glob]
workflow:
  type: sequential
  steps: 6
prompt_templates:
  directory: prompts/
  templates:
    - boundary_analysis
    - capital_analysis
    - habitus_analysis
    - dynamics_analysis
agent_integration:
  agent: field-analysis-expert
  core_skills:
    - field-analysis
    - field-boundary-identification
    - field-capital-analysis
    - field-habitus-analysis
---

# 布迪厄场域理论专家分析技能 (Field Expert Analysis)

## 概述

布迪厄场域理论专家分析技能整合了场域边界识别、资本分析、习性分析和场域动力学分析功能。该技能遵循渐进式信息披露原则，定义标准化的分析流程，支持宿主agent动态加载提示词模板。

## 使用时机

当用户请求以下分析时使用此技能：
- 分析社会场域或领域（教育、政治、文化等）
- 识别场域边界和游戏规则
- 分析资本分布和权力关系
- 理解习性及其与场域结构的关系
- 调查场域内的斗争和权力动态
- 分析场域的历史演变与发展趋势

## 输入规范

### 用户输入格式
用户应提供分析文本的路径：
```json
{
  "input_path": "文本目录路径",
  "field_type": "场域类型（可选，如educational, cultural, political）"
}
```

### 预期输入文件
技能自动扫描输入目录中的以下文件类型：
- **扎根理论数据**: `*开放编码*`, `*选择性编码*`, `*饱和度检验*`
- **社会网络数据**: `*社会网络*`, `*network*`
- **理论框架**: `*ESOC*`, `*理论框架*`

## 工作流程（6步骤）

### 步骤1: 数据准备
**操作类型**: 执行脚本（定量处理）
**脚本路径**: `scripts/prepare_data.py`
**输入**: 自动扫描输入目录中的文本文件
**输出**: `input/processed/combined_input.json`

**执行命令**:
```bash
python scripts/prepare_data.py --input <用户输入路径> --output input/processed/combined_input.json
```

**输出格式**:
```json
{
  "metadata": {
    "input_path": "原始数据路径",
    "prepared_at": "时间戳",
    "sources": ["grounded_theory", "social_network", "esoc_framework"]
  },
  "grounded_theory": {...},
  "social_network": {...},
  "esoc_framework": {...}
}
```

---

### 步骤2: 边界分析
**操作类型**: 动态加载提示词 → 宿主LLM分析
**提示词模板**: `prompts/boundary_analysis.txt`
**输入**: `input/processed/combined_input.json`
**输出**: `intermediate/01_boundary/boundary_results.json`

**[PROMPT:boundary_analysis]**
你是布迪厄场域理论专家。请基于以下扎根理论分析数据，识别和界定分析文本中的场域边界。

### 输入数据
{context:input/processed/combined_input.json}

### 分析任务

请从以下四个维度进行场域边界分析：

#### 1. 场域识别
识别文本中描述的各个社会场域，包括场域名称、核心行动者、边界标识和场域间的区分原则。

#### 2. 边界确定
分析每个场域的边界特征：进入场域的条件、场域内部的排斥机制、场域边界的标识物。

#### 3. 守门人识别
识别场域边界的守门人角色：谁控制场域入口、谁维护场域规则、谁有权决定场域内外。

#### 4. 边界动态
分析场域边界的动态变化：边界的稳定性、边界渗透性、边界变迁的触发因素。

### 输出格式

请以JSON格式输出分析结果：
```json
{
  "fields": [
    {
      "name": "场域名称",
      "core_actors": ["行动者1", "行动者2"],
      "boundary_markers": ["标识1", "标识2"],
      "entry_conditions": ["条件1", "条件2"],
      "exclusion_mechanisms": ["机制1", "机制2"]
    }
  ],
  "gatekeepers": [
    {
      "actor": "守门人名称",
      "fields": ["场域1", "场域2"],
      "role": "守门角色描述"
    }
  ],
  "boundary_dynamics": {
    "stability": "稳定/变化中",
    "permeability": "高/中/低",
    "change_triggers": ["触发因素1", "触发因素2"]
  }
}
```
[/PROMPT]

---

### 步骤3: 资本分析
**操作类型**: 动态加载提示词 → 宿主LLM分析
**提示词模板**: `prompts/capital_analysis.txt`
**输入**: `input/processed/combined_input.json`
**输出**: `intermediate/02_capital/capital_results.json`

**[PROMPT:capital_analysis]**
你是布迪厄场域理论专家。请基于以下扎根理论分析数据，分析各场域中的资本类型与分布。

### 输入数据
{context:input/processed/combined_input.json}

### 分析任务

请从以下四个维度进行资本分布分析：

#### 1. 资本类型识别
识别分析文本中出现的各类资本：经济资本、社会资本、文化资本、符号资本。

#### 2. 资本分布分析
分析各类资本在不同行动者/场域间的分布：资本持有量排名、分布的不平等程度、资本占有的合法性来源。

#### 3. 资本转换路径
分析资本之间的转换关系：经济→社会、社会→文化、文化→符号，转换的条件和代价。

#### 4. 资本与位置关系
分析资本占有与场域位置的关系：资本多寡如何决定场域位置、位置如何影响资本获取。

### 输出格式

请以JSON格式输出分析结果：
```json
{
  "capital_types": {
    "economic": {"description": "...", "manifestations": [...]},
    "social": {"description": "...", "manifestations": [...]},
    "cultural": {"description": "...", "manifestations": [...]},
    "symbolic": {"description": "...", "manifestations": [...]}
  },
  "capital_distribution": {
    "ranking": [...],
    "inequality_level": "高/中/低"
  },
  "conversion_paths": [...]
}
```
[/PROMPT]

---

### 步骤4: 习性分析
**操作类型**: 动态加载提示词 → 宿主LLM分析
**提示词模板**: `prompts/habitus_analysis.txt`
**输入**: `input/processed/combined_input.json`
**输出**: `intermediate/03_habitus/habitus_results.json`

**[PROMPT:habitus_analysis]**
你是布迪厄场域理论专家。请基于以下扎根理论分析数据，分析各场域行动者的习性模式。

### 输入数据
{context:input/processed/combined_input.json}

### 分析任务

请从以下四个维度进行习性模式分析：

#### 1. 行动者习性识别
识别各主要行动者的习性特征：行为模式、认知结构、实践倾向。

#### 2. 习性与场域关系
分析习性如何与场域结构相互作用：场域如何塑造习性、习性如何影响场域实践。

#### 3. 符号暴力机制
分析场域中的符号暴力：支配者实施的符号暴力形式、被支配者的接受与内化。

#### 4. 跨场域分析
分析习性的跨场域作用：场域转换时的习性调适、跨场域策略。

### 输出格式

请以JSON格式输出分析结果：
```json
{
  "actors_habitus": [
    {
      "actor": "行动者名称",
      "behavior_patterns": {...},
      "cognitive_structure": {...},
      "practical_dispositions": {...}
    }
  ],
  "habitus_field_relationship": {...},
  "symbolic_violence": {...},
  "cross_field_analysis": {...}
}
```
[/PROMPT]

---

### 步骤5: 动力学分析
**操作类型**: 动态加载提示词 → 宿主LLM分析
**提示词模板**: `prompts/dynamics_analysis.txt`
**输入**: `combined_input.json` + `boundary_results.json` + `capital_results.json` + `habitus_results.json`
**输出**: `intermediate/04_dynamics/dynamics_results.json`

**[PROMPT:dynamics_analysis]**
你是布迪厄场域理论专家。请基于以下前期分析结果，进行场域动力学分析。

### 输入数据
{context:intermediate_results}

其中 intermediate_results 包含：
- 边界分析结果: intermediate/01_boundary/boundary_results.json
- 资本分析结果: intermediate/02_capital/capital_results.json  
- 习性分析结果: intermediate/03_habitus/habitus_results.json

### 分析任务

请从以下四个维度进行场域动力学分析：

#### 1. 场域竞争分析
分析场域内的竞争格局：竞争主体、竞争资源、竞争策略、竞争结果。

#### 2. 权力关系分析
分析场域内的权力结构与运作：权力来源、权力结构、权力运作、权力抵抗。

#### 3. 场域演变趋势
分析场域的历史演变与未来趋势：发展阶段、演变动力、演变阻力、未来趋势。

#### 4. 综合理论建构
基于以上分析，提炼理论命题。

### 输出格式

请以JSON格式输出分析结果：
```json
{
  "competition_analysis": {...},
  "power_relations": {...},
  "field_evolution": {...},
  "theory_construction": {
    "core_findings": [...],
    "theoretical_propositions": [...]
  }
}
```
[/PROMPT]

---

### 步骤6: 报告生成
**操作类型**: 执行脚本（定量处理）
**脚本路径**: `scripts/generate_report.py`
**输入**: 所有中间结果文件
**输出**: 
- `output/reports/field_analysis_report.html`
- `output/json/comprehensive_analysis.json`
- `output/executive_summary.txt`

**执行命令**:
```bash
python scripts/generate_report.py \
  --input input/processed/combined_input.json \
  --boundary intermediate/01_boundary/boundary_results.json \
  --capital intermediate/02_capital/capital_results.json \
  --habitus intermediate/03_habitus/habitus_results.json \
  --dynamics intermediate/04_dynamics/dynamics_results.json \
  --output output/
```

---

## 目录结构

```
field-expert/
├── SKILL.md                    # 技能定义 + 工作流程
├── prompts/                    # 提示词模板目录
│   ├── boundary_analysis.txt   # 边界分析提示词
│   ├── capital_analysis.txt    # 资本分析提示词
│   ├── habitus_analysis.txt    # 习性分析提示词
│   └── dynamics_analysis.txt   # 动力学分析提示词
├── scripts/                    # 脚本目录（定量处理）
│   ├── prepare_data.py         # 数据准备脚本
│   └── generate_report.py      # 报告生成脚本
├── modules/                    # 分析模块
└── tests/                      # 测试文件
```

## 数据流规范

| 步骤 | 操作 | 输入 | 输出 |
|------|------|------|------|
| 1 | 脚本 | 源文件 | `input/processed/combined_input.json` |
| 2 | LLM | combined_input | `intermediate/01_boundary/boundary_results.json` |
| 3 | LLM | combined_input | `intermediate/02_capital/capital_results.json` |
| 4 | LLM | combined_input | `intermediate/03_habitus/habitus_results.json` |
| 5 | LLM | 步骤2-4结果 | `intermediate/04_dynamics/dynamics_results.json` |
| 6 | 脚本 | 所有结果 | `output/reports/*.html`, `output/json/*.json` |

## 宿主Agent集成指南

宿主agent调用此技能时应：

1. **解析SKILL.md** - 读取工作流程定义
2. **按步骤执行** - 按顺序执行6个步骤
3. **动态加载提示词** - 识别 `[PROMPT:name]` 标记，加载对应模板
4. **注入上下文** - 替换 `{context:filepath}` 为实际文件内容
5. **发送LLM** - 将提示词发送给宿主LLM执行
6. **写入结果** - 将LLM输出写入指定的JSON文件

### 伪代码示例

```python
def run_field_analysis_skill(input_path):
    # 步骤1: 数据准备
    run_script("scripts/prepare_data.py", f"--input {input_path}")
    
    # 步骤2: 边界分析
    prompt = load_prompt("prompts/boundary_analysis.txt")
    context = read_file("input/processed/combined_input.json")
    result = llm_analyze(prompt.replace("{context}", context))
    write_file("intermediate/01_boundary/boundary_results.json", result)
    
    # 步骤3: 资本分析
    prompt = load_prompt("prompts/capital_analysis.txt")
    result = llm_analyze(prompt.replace("{context}", context))
    write_file("intermediate/02_capital/capital_results.json", result)
    
    # ... 步骤4-6
    
    return {"report": "output/reports/field_analysis_report.html"}
```

## 输出格式标准

所有LLM分析步骤必须输出JSON格式，确保：
- 键使用小写字母+下划线
- 值类型一致
- 包含timestamp元数据
- 数组元素类型一致

## 质量标准

- 严格应用布迪厄理论框架
- 保持关系分析的核心关注点
- 考虑历史和文化背景
- 平衡结构和能动性视角
- 提供基于证据的解释

---

*此技能遵循agentskills.io标准，支持渐进式信息披露和动态提示词加载。*
