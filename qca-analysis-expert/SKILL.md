---
name: qca-analysis-expert
description: |
  定性比较分析专家。提供数据校准、真值表构建、一致性分析、必要性/充分性检验功能。适用于比较研究、因果组合分析、中小样本研究场景。
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

# SKILL.md - qca-analysis-expert

---
metadata:
  version: "5.1.0-cli-native+agent"
  methodology: "Qualitative Comparative Analysis (QCA)"
  absolute-prohibitions: true
  task-decomposition-rules: true
  ai-cli-native: true
  task-queue-support: true
  agentskills-io: true
  cross-platform: true
  state-persistence: true
  self-iteration: true
  academic-alignment: true
  subagent-support: true
  graceful-fallback: true
  created: "2026-03-05"
  updated: "2026-03-14"
  author: "SocienceAI Methodology Expert"
  license: "MIT"
  alignment_reference: "grounded-theory-coding (v5.0.0)"

  execution_modes:
    cli_queue: "CLI任务队列（基础）"
    subagent_parallel: "子Agent并行（增强）"

  performance:
    sequential: "60分钟/案例"
    parallel: "65分钟/10案例（9.2x加速）"
---

## 在 AI CLI 中使用

### 方式 1: 在对话中直接使用（推荐）

```
你：使用QCA分析技能分析民主化影响因素

AI: 好的，我将使用QCA分析技能进行分析。
    正在创建任务队列...

    任务清单：
    1. 数据校准 (20 分钟)
    2. 必要性分析 (15 分钟)
    3. 真值表构建 (20 分钟)
    4. 充分性分析 - 复杂解 (20 分钟)
    5. 充分性分析 - 简化解 (20 分钟)
    6. 稳健性检验 (30 分钟)
    7. 案例解释 (15 分钟)

    共 7 个任务，预计 140 分钟。开始执行...
```

### 方式 2: 使用 Python 工具

#### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | analyze.py | 主分析入口，调度各工具 |
| 2 | data_calibrator.py | 校准原始数据为集合 |
| 3 | truth_table_builder.py | 构建真值表 |
| 4 | solution_calculator.py | 计算最小化解 |
| 5 | consistency_analyzer.py | 分析必要性一致性 |
| 6 | set_relation_analyzer.py | 分析集合关系 |
| 7 | planning_integration.py | 任务规划集成 |

#### 使用示例

```bash
# 1. 数据校准
python tools/data_calibrator.py -i data/raw.csv --method fuzzy -o results/calibrated.json

# 2. 构建真值表
python tools/truth_table_builder.py -i results/calibrated.json -o results/truth_table.json

# 3. 计算解
python tools/solution_calculator.py -i results/truth_table.json -o results/solutions.json

# 4. 必要性分析
python tools/consistency_analyzer.py -i results/calibrated.json --outcome outcome -o results/necessity.json

# 5. 集合关系分析
python tools/set_relation_analyzer.py -i results/calibrated.json -o results/set_relations.json
```

## 基本信息

**名称**: qca-analysis-expert (QCA分析专家)
**版本**: 5.0.0-cli-native+agent
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


**QCA分析专家** - 支持**复杂任务分解**和**长时任务执行**的集合论因果分析技能。

基于Ragin (1987, 2008)的定性比较分析方法论，支持**csQCA** (crisp-set)、**mvQCA** (multi-value)、**fsQCA** (fuzzy-set)三种分析方法，通过**集合论**和**布尔代数**分析**因果复杂性**。

### 核心能力

1. **三种QCA方法**
   - **csQCA**: 二元集合分析（清晰集）
   - **mvQCA**: 多值集合分析
   - **fsQCA**: 模糊集分析（最常用）

2. **集合论因果分析**
   - 模糊集校准（连续变量→集合隶属度）
   - 真值表构建（案例→条件组合）
   - 布尔最小化（简化逻辑表达式）

3. **因果复杂性处理**
   - 多重并发因果（多个条件组合导致结果）
   - 非对称因果（X导致Y ≠ Y导致X）
   - 等效性（多条路径导致同一结果）

4. **必要性/充分性分析**
   - 必要条件：结果发生的必要条件
   - 充分条件：导致结果的充分条件
   - 必要且充分条件

5. **稳健性检验**
   - 参数敏感性分析
   - 校准敏感性分析
   - 案例归属检验

### 适用场景

- 中小样本研究（10-200个案例）
- 因果复杂性分析（多重并发、非对称）
- 比较案例分析（跨案例、跨时间）
- 理论检验与发展（从数据到理论）
- 混合方法研究（定量+定性结合）

## 方法论基础

### QCA理论框架

**QCA** 是一种基于**集合论**和**布尔代数**的比较分析方法：

1. **集合论基础**
   - 集合隶属度（0 = 完全不属于，1 = 完全属于）
   - 模糊集（连续隶属度：0.0-1.0）
   - 多值集（超过两个类别）

2. **布尔代数**
   - 逻辑AND（*）：交集
   - 逻辑OR（+）：并集
   - 逻辑NOT（~）：补集

3. **因果复杂性**
   - **多重并发因果** (Conjunctural Causation): 多个条件组合导致结果
   - **非对称因果** (Asymmetric Causality): X导致Y ≠ Y导致X
   - **等效性** (Equifinality): 多条路径导致同一结果

### 核心概念

**校准** (Calibration):
- 将连续变量转化为集合隶属度
- 基于理论和知识设定锚点（完全不属于、交叉点、完全属于）

**真值表** (Truth Table):
- 列出所有可能的条件组合（2^k个，k=条件数）
- 每个组合对应的案例数量和结果一致性

**布尔最小化** (Boolean Minimization):
- 简化逻辑表达式
- 保留核心因果组合
- 识别必要和充分条件

**一致性** (Consistency):
- 充分一致性：条件组合 → 结果的覆盖度
- 必要一致性：结果 → 条件组合的覆盖度

**原始覆盖度** (Raw Coverage):
- 条件组合解释的案例比例

**唯一覆盖度** (Unique Coverage):
- 条件组合独占解释的案例比例

## 六大绝对禁止原则

### 1. 禁止脱离理论校准

**错误做法**:
```yaml
机械校准:
  - 使用统计分位数（33%, 67%）
  - 使用均值、标准差
  - 忽视理论意义
```

**正确做法**:
```yaml
理论指导的校准:
  Step 1: 理论定义
    - "什么是'完全民主'?"（隶属度=1.0）
    - "什么是'完全威权'?"（隶属度=0.0）
    - "什么是'交叉点'?"（隶属度=0.5）

  Step 2: 基于理论的锚点
    - 完全不属于: 0 (完全威权)
    - 交叉点: 0.5 (混合政体)
    - 完全属于: 1.0 (完全民主)

  Step 3: 基于锚点的校准函数
    - 使用对数或 logistic 函数
    - 连接原始值与隶属度
```

**量化标准**:
- 每个条件必须有明确的校准标准
- 锚点必须有理论或实证依据
- 校准依据必须在报告中说明

### 2. 禁止忽略案例独特性

**错误做法**:
```yaml
忽视案例:
  - 只看真值表和逻辑表达式
  - 不回到具体案例
  - "这是统计学方法"

QCA变成黑箱:
  - 不了解每个组合的案例构成
  - 不分析案例的异质性
  - 不做深入的案例研究
```

**正确做法**:
```yaml
案例导向的分析:
  Step 1: 识别关键组合
    - 哪些条件组合最重要?
    - 这些组合包含哪些案例?

  Step 2: 深入案例研究
    - 阅读案例材料
    - 理解因果机制
    - 验证理论解释

  Step 3: 跨案例比较
    - 同一组合内的案例: 共性?
    - 不同组合间的案例: 差异?
    - 残余案例（不一致）: 为什么?
```

**量化标准**:
- 每个关键组合必须回到案例
- 必须报告每个组合的案例列表
- 不一致案例必须深入分析

### 3. 禁止过度简化

**错误做法**:
```yaml
过度最小化:
  - 只报告最简表达式
  - 删除所有"逻辑余项"
  - 损失案例信息

示例:
  原始: A*B + A*C + D
  过度简化: A + D

  问题: 不知道 A*B 还是 A*C
  损失: 不知道具体路径
```

**正确做法**:
```yaml
保守最小化:
  Step 1: 报告所有解
    - 复杂解（最保守）
    - 简化解（中等）
    - 最简解（最激进）

  Step 2: 案例分布检查
    - 每个解的案例分布
    - 案例独占性
    - 案例重叠性

  Step 3: 理论选择
    - 基于理论选择最合适的解
    - 不只选最简的
```

**量化标准**:
- 至少报告2种解（复杂+简化）
- 报告每种解的案例分布
- 基于理论/案例选择解

### 4. 禁止忽视时间维度

**错误做法**:
```yaml
静态快照:
  - 只看某一时刻的数据
  - 忽视因果时序
  - "条件同时发生"

因果倒置风险:
  - 可能是结果导致条件
  - 而非条件导致结果
```

**正确做法**:
```yaml
时间敏感的分析:
  Step 1: 明确时序
    - 条件必须在结果之前
    - 使用T1（条件）→ T2（结果）

  Step 2: 时间序列QCA
    - 多个时间点数据
    - 分析路径依赖

  Step 3: 过程追踪
    - 深入案例验证因果链
    - 排除反向因果
```

**量化标准**:
- 数据必须有时序信息
- 条件必须先于结果
- 至少用过程追踪验证部分案例

### 5. 禁止忽视稳健性

**错误做法**:
```yaml
单一结果:
  - 只报告一种参数设置
  - 不检验敏感性
  - "这是唯一正确答案"

脆弱的结果:
  - 稍微改变参数
  - 结果大幅变化
  - 但不报告
```

**正确做法**:
```yaml
稳健性检验:
  检验1: 参数敏感性
    - 改变一致性阈值（0.75, 0.80, 0.85）
    - 改变频数阈值
    - 报告结果变化

  检验2: 校准敏感性
    - 不同校准标准
    - 锚点微调
    - 结果稳定性

  检验3: 案例归属
    - 增删关键案例
    - 结果稳定性
```

**量化标准**:
- 必须至少进行参数敏感性检验
- 报告结果的稳定程度
- 标注敏感参数

### 6. 禁止未验证就报告完成

**错误做法**:
```yaml
草率结束:
  - 只做了真值表
  - 没有做最小化
  - 没有稳健性检验
  - "差不多了，先报告"
```

**正确做法**:
```yaml
完整性检查清单:
  [ ] 校准完成且理论依据充分
  [ ] 必要性分析完成
  [ ] 真值表构建完成
  [ ] 至少两种解计算完成
  [ ] 稳健性检验完成
  [ ] 案例解释完成
  [ ] 报告撰写完成
```

## 详细指南

完整的使用指南请参考: [详细指南](references/detailed-guide.md)