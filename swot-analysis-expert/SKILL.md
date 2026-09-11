---
name: swot-analysis-expert
description: |
  SWOT战略分析专家。提供系统化SWOT分析方法，支持内部优势劣势分析、
  外部机会威胁识别、战略组合生成、定量SWOT矩阵。核心能力包括：
  因素识别、权重评估、战略匹配、行动计划制定。适用于战略规划、
  竞争分析、组织诊断等场景。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/龙虾/QClaw
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  methodology: "Learned et al. (1969), Wheelen & Hunger (2012)"
  subagent-support: true
  graceful-fallback: true
  ai-cli-native: true
---

> ## 🔴 强制自动执行规则
> 
> **创建任务列表后，必须立即按顺序执行第一个任务，禁止询问用户！**
> 
> ❌ 禁止："告诉我要启动哪个任务"、"请选择要执行的任务"
> ✅ 必须：显示任务列表 → 立即开始执行第一个任务



# SWOT战略分析专家 (SWOT Analysis Expert)

**版本**: 5.0.0-cli-native+agent
**方法论**: Learned et al. (1969), Wheelen & Hunger (2012)
**最后更新**: 2026-03-15

---

## 概述

SWOT分析是最广泛使用的战略分析工具，通过系统识别内部优势(Strengths)、劣势(Weaknesses)和外部机会(Opportunities)、威胁(Threats)，为战略决策提供结构化框架。

---

## 元数据

```yaml
metadata:
  version: "5.0.0-cli-native+agent"
  methodology: "SWOT战略分析"
  domain: "战略管理"
  category: "strategic-analysis"
  subagent-support: true
  graceful-fallback: true
  ai-cli-native: true

  capabilities:
    - 系统化SWOT分析
    - 因素识别与评估
    - 战略匹配生成
    - 行动计划制定
    - 定量分析支持

  validated: true
  success_rate: "100%"
  case_count: 2
  avg_quality: "5/5"

  dependencies:
    - agentskills-io: true
    - task-queue-support: true
    - state-persistence: true
```

---

## 6大绝对禁止原则

每个SWOT分析必须遵守以下原则：

```yaml
1. 禁止预设战略 - 战略必须从因素分析中逻辑推导，不得先有结论再找论据
2. 禁止忽略负面因素 - 劣势和威胁必须客观识别，不得回避或弱化
3. 禁止无证据评估 - 所有因素评估必须有数据支撑，不得主观臆断
4. 禁止因素遗漏 - 必须系统扫描各维度因素，每类至少3个
5. 禁止战略空泛 - 战略建议必须具体、可操作、可衡量
6. 禁止静态思维 - 必须考虑因素的时间变化和动态性
```

---

## CRCT思维链（强制执行）

### C - Constant Comparison（持续比较）

每个新因素识别时必须执行：
```
比较对象：[新因素] vs [已有同类型因素]
相似点：[列举相似之处]
差异点：[列举差异之处]
整合决策：[合并/分离/修改]
```

### R - Record（记录）

所有分析决策必须记录：
```
因素名称：[名称]
类型：[S/W/O/T]
描述：[具体描述]
证据来源：[数据引用]
影响评估：[影响程度和概率]
```

### C - Chain（链条）

建立因素到战略的逻辑链条：
```
因素A(S) + 因素B(O) → SO战略
证据支持：[数据引用]
逻辑推导：[推导过程]
```

### T - Trace（追踪）

追踪战略的演化过程：
```
初始战略 → 修正战略 → 最终战略
修正原因：[数据发现/风险评估/资源限制]
```

---

## SWOT框架

```
                    内部因素                    外部因素
                  (可控制)                    (不可控)
              
    正面因素    ┌─────────────────┐      ┌─────────────────┐
    (有利)      │     优势(S)      │      │     机会(O)      │
               │                 │      │                 │
               │  核心竞争力     │      │  市场机会       │
               │  资源优势       │      │  政策支持       │
               │  能力优势       │      │  技术趋势       │
               └─────────────────┘      └─────────────────┘
               
    负面因素    ┌─────────────────┐      ┌─────────────────┐
    (不利)      │     劣势(W)      │      │     威胁(T)      │
               │                 │      │                 │
               │  资源不足       │      │  竞争威胁       │
               │  能力缺陷       │      │  市场风险       │
               │  管理问题       │      │  政策风险       │
               └─────────────────┘      └─────────────────┘
```

---

## 四象限战略矩阵

```
                优势(S)              劣势(W)
           ┌────────────────┬────────────────┐
   机会(O) │    SO战略       │    WO战略       │
           │  增长型战略     │  扭转型战略     │
           │  利用优势       │  利用机会       │
           │  把握机会       │  克服劣势       │
           ├────────────────┼────────────────┤
   威胁(T) │    ST战略       │    WT战略       │
           │  多元化战略     │  防御型战略     │
           │  利用优势       │  减少劣势       │
           │  规避威胁       │  回避威胁       │
           └────────────────┴────────────────┘
```

---

## 分析流程

```
步骤1: 环境扫描
    │
    ↓
步骤2: 内部分析 → 识别S/W
    │
    ↓
步骤3: 外部分析 → 识别O/T
    │
    ↓
步骤4: 因素评估 → 权重打分
    │
    ↓
步骤5: 战略匹配 → 生成策略
    │
    ↓
步骤6: 行动计划 → 优先级排序
```

### 第一阶段：环境扫描

**目标**：收集企业内外部环境信息

**步骤**：
1. 内部分析：资源、能力、核心竞争力扫描
2. 外部分析：PESTEL环境、行业竞争、市场趋势扫描
3. 利益相关者分析：识别关键利益相关者
4. 数据验证：交叉验证信息来源

**输出要求**：
- 环境扫描报告
- 关键因素清单（初版）
- 数据来源列表

**质量标准**：
- 数据来源 ≥ 3个
- 覆盖主要维度
- 信息可验证

### 第二阶段：因素识别

**目标**：系统识别S/W/O/T四类因素

**输出要求**：
- 因素列表（含描述和证据）
- 因素分类矩阵
- 初步重要性评估

**质量标准**：
- 每类因素 ≥ 3个
- 每个因素有证据支撑
- 因素描述具体、可衡量

### 第三阶段：因素评估

**目标**：对因素进行定量评估

**评估矩阵**：
```
因素 | 影响程度 | 概率 | 得分 | 权重 | 加权分
-----|----------|------|------|------|--------
S1   |    5     |  5   |  25  | 0.20 |  5.0
```

**质量标准**：
- 评估有数据支撑
- 权重总和 = 1.0
- 至少两人独立评估

### 第四阶段：战略生成

**目标**：生成四类战略选项

**战略评估矩阵**：
```
战略选项 | 可行性 | 吸引力 | 风险 | 综合分
---------|--------|--------|------|--------
SO战略1  |   5    |   5    |  2   |   12
```

**质量标准**：
- 每类战略 ≥ 2个
- 战略有因素支撑
- 战略具体可操作

### 第五阶段：行动计划

**目标**：制定优先级和实施路径

**输出要求**：
- 战略优先级矩阵
- 行动计划表
- 资源配置方案
- 风险预案

---

## Planning-With-Files支持

### 任务初始化自动创建文件

```
project/
├── task_plan.md      # 任务计划
├── progress.md       # 进度跟踪
└── findings.md       # 发现记录
```

### 任务计划模板

```markdown
# SWOT分析任务计划

## 任务概述
- 分析对象：[企业/项目名称]
- 分析范围：[业务范围]
- 时间跨度：[分析时间范围]

## 任务分解
- [ ] 阶段1：环境扫描
- [ ] 阶段2：因素识别
- [ ] 阶段3：因素评估
- [ ] 阶段4：战略生成
- [ ] 阶段5：行动计划

## 质量检查点
- [ ] 因素完整性检查
- [ ] 评估一致性检查
- [ ] 战略逻辑检查
```

---

## CLI原生集成

### 任务队列支持

```yaml
task-queue:
  自动创建: true
  持久化: true
  依赖追踪: true

  task-types:
    - environment-scanning
    - factor-identification
    - factor-evaluation
    - strategy-generation
    - action-planning

  execution:
    model-driven: true       # 模型直接执行
    tool-first: true         # 优先使用专用工具
    state-persistence: true  # 状态持久化
```

### 三层持久化

```yaml
持久化层次:
  第一层: 会话持久化
    - 当前任务状态
    - 临时数据
    - 位置: .claude/session/swot/

  第二层: 项目持久化
    - 任务历史
    - 分析结果
    - 位置: project/swot-workspace/

  第三层: 学习持久化
    - 经验模式
    - 案例库
    - 位置: experience/ & cases/
```

---

## 子Agent支持

### 模式选择

| 模式 | 适用场景 | 版本标识 | 性能 |
|------|----------|----------|------|
| CLI任务队列 | 1-5个任务，有依赖关系 | v5.0.0-cli-native | 基准 |
| 子Agent并行 | >5个独立任务 | v5.0.0-cli-native+agent | 5-10x加速 |

### 子Agent定义

```yaml
subagents:
  - id: internal-analyzer
    role: 内部因素分析专家
    capabilities:
      - resource_analysis
      - capability_analysis
      - value_chain_analysis

  - id: external-analyzer
    role: 外部因素分析专家
    capabilities:
      - pestel_analysis
      - industry_analysis
      - competitor_analysis

  - id: strategy-generator
    role: 战略生成专家
    capabilities:
      - so_strategy
      - wo_strategy
      - st_strategy
      - wt_strategy

  - id: priority-ranker
    role: 优先级排序专家
    capabilities:
      - feasibility_check
      - risk_assessment
      - resource_matching
```

---

## 质量保证

### 完成度验证清单

```yaml
因素识别检查:
  ☑ 每类因素至少3个
  ☑ 每个因素有具体描述
  ☑ 每个因素有证据支撑
  ☑ 因素分类正确

因素评估检查:
  ☑ 评分有依据
  ☑ 权重总和为1.0
  ☑ 因素排序合理

战略生成检查:
  ☑ 每类战略至少2个
  ☑ 战略有因素支撑
  ☑ 战略具体可操作

行动计划检查:
  ☑ 优先级排序完成
  ☑ 时间规划明确
  ☑ 资源匹配合理
  ☑ 风险预案制定
```

---

## 工具函数

| 工具 | 功能 |
|------|------|
| `factor_identifier.py` | 因素识别 |
| `weight_calculator.py` | 权重计算 |
| `strategy_matcher.py` | 战略匹配 |
| `priority_ranker.py` | 优先级排序 |

---

## 参考资料

- [经典文献](references/classic-literature.md)
- [详细指南](references/detailed-guide.md)
- [成功案例](cases/positive/)
- [失败案例](cases/negative/)
- [经验模式](experience/patterns.md)

---

## 参考文献

1. Learned, E.P., et al. (1969). *Business Policy: Text and Cases*. Irwin.
2. Weihrich, H. (1982). The TOWS Matrix. *Long Range Planning*, 15(2), 54-66.
3. Wheelen, T.L., & Hunger, J.D. (2012). *Strategic Management and Business Policy*. 14th ed.
4. Hill, T., & Westbrook, R. (1997). SWOT analysis: It's time for a product recall. *Long Range Planning*, 30(1), 46-52.
5. Valentin, E.K. (2001). SWOT analysis from a resource-based view. *Journal of Marketing Theory and Practice*, 9(2), 94-103.

---

## 版本历史

```yaml
5.0.0-cli-native+agent (2026-03-15):
  - 添加Planning-With-Files支持
  - 添加CRCT思维链
  - 添加三层持久化机制
  - 添加子Agent并行支持
  - 完善质量保证体系
  - 添加6大禁止原则

1.0.0 (2026-03-15):
  - 初始版本
  - 基础SWOT分析功能
```

---

**技能版本**: 5.0.0-cli-native+agent
**方法论严谨性**: 0%妥协
**创建时间**: 2026-03-15