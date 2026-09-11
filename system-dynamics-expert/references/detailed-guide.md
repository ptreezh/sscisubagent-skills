6. **绝不忽视校准验证**
   - 与历史数据对比
   - 检验模型有效性
   - 报告拟合度

---

**使用方式**:
- 对话中直接使用："使用系统动力学建模分析XX"
- 长时研究：技能会自动分解任务
- 质量保证：六大禁止原则+完成度清单

## 🔄 CLI任务队列自动执行

### 自动激活条件

当满足以下任一条件时，技能自动激活任务队列模式：

```yaml
激活条件:
  - 任务估计时间 > 3小时
  - 包含3个以上独立子任务
  - 需要多阶段验证
  - 用户明确要求"分解任务"
```

### 自动分解流程

```yaml
Step 1: 任务分析
  - 识别SD建模类型（流行病/供应链/环境）
  - 估计系统复杂度
  - 判断所需数据和方法

Step 2: 方法论匹配
  - 匹配标准建模流程模板
  - 根据问题特点调整
  - 确定质量验证点

Step 3: 任务队列生成
  - 创建结构化任务列表
  - 建立任务依赖关系
  - 设置时间估计

Step 4: 执行计划展示
  - 展示完整任务清单
  - 说明预计总时间
  - 等待用户确认
```

### 流行病建模自动分解示例

```yaml
用户请求: "建立COVID-19传播动力学模型"

自动分解为:

Phase 1: 问题界定 (4小时)
  Task 1.1: 问题边界定义 (1小时)
    - 输出: 问题陈述文档
    - 验证: 时空边界清晰

  Task 1.2: 关键变量识别 (1.5小时)
    - 输出: 变量清单（易感/感染/康复/死亡）
    - 验证: Stock/Flow区分明确

  Task 1.3: 参考模式绘制 (1.5小时)
    - 输出: 历史感染曲线图
    - 验证: 行为模式识别准确

Phase 2: 系统建模 (1周)
  Task 2.1: 因果回路图CLD (2天)
    - 输出: 完整CLD图
    - 验证: 反馈回路识别完整

  Task 2.2: Stock & Flow图SFD (2天)
    - 输出: SFD图文档
    - 验证: 存量流量结构正确

  Task 2.3: 方程与参数 (2天)
    - 输出: 完整方程清单
    - 验证: 单位一致、逻辑正确

Phase 3: 仿真与校准 (1周)
  Task 3.1: 基准模型实现 (2天)
    - 输出: 可运行模型
    - 验证: 无语法错误、可仿真

  Task 3.2: 模型校准 (2天)
    - 输出: 校准后参数
    - 验证: 与历史数据拟合（R²>0.8）

  Task 3.3: 敏感性分析 (2天)
    - 输出: 敏感性报告
    - 验证: 关键参数识别

Phase 4: 政策分析 (4天)
  Task 4.1: 基准情景 (1天)
    - 输出: 无干预情景仿真
    - 验证: 基准行为合理

  Task 4.2: 干预情景 (2天)
    - 输出: 多情景对比（口罩/隔离/疫苗）
    - 验证: 情景差异清晰

  Task 4.3: 杠杆点分析 (1天)
    - 输出: 杠杆点识别报告
    - 验证: 干预建议可行性

总估计时间: 3周
```

## 💾 任务状态持久化

### 持久化架构

```yaml
存储位置:
  Level 1: .tasks/session-{uuid}.yaml
    - 会话级状态
    - 生命周期: 会话结束

  Level 2: .tasks/project-state.yaml
    - 项目级状态
    - 生命周期: 项目完成

  Level 3: experience/patterns.md
    - 学习级知识
    - 生命周期: 永久
```

### 状态文件示例

```yaml
# .tasks/session-abc123.yaml

session:
  id: "abc123"
  skill: "system-dynamics-expert"
  start_time: "2026-03-08T10:00:00Z"
  last_update: "2026-03-08T14:30:00Z"

user_request:
  original: "建立COVID-19传播动力学模型"
  interpreted: "使用SEIR模型建模传染病传播"

task_queue:
  - id: "1.1"
    name: "问题边界定义"
    status: "completed"
    output: "docs/problem_statement.md"
    validation: "passed"
    timestamp: "2026-03-08T11:00:00Z"

  - id: "2.1"
    name: "因果回路图CLD"
    status: "in_progress"
    started_at: "2026-03-08T13:00:00Z"

progress:
  total_tasks: 13
  completed: 4
  in_progress: 1
  pending: 8
  percentage: 31

model_artifacts:
  cld: "models/cld_v1.png"
  sfd: "models/sfd_draft.png"
  equations: "models/equations.md"
```

## 🎯 CLI模型驱动执行

### 核心原则

```yaml
✅ 正确做法 - 直接使用建模工具:
  - "使用Vensim建立SIR模型"
  - "使用PySD运行敏感性分析"
  - "使用Insight Maker创建CLD图"

❌ 错误做法 - 生成脚本:
  - "生成model.py脚本"
  - "创建build_model.py并执行"
```

### 系统动力学工具链

```yaml
专业工具:
  - Vensim: 专业SD建模
  - Stella: 教育与研究
  - Insight Maker: 在线建模
  - AnyLogic: 多方法仿真

Python工具:
  - PySD: Python SD库
  - BPTK_Py: 政策仿真
  - pysd: 模型转换

CLI集成:
  - 直接调用工具
  - 通过命令执行
  - 结果直接返回
  - 模型可复现
```

## 🧠 自迭代与学习机制

### 经验记录

每次建模任务完成后自动记录：

```yaml
session:
  id: "uuid"
  date: "2026-03-08"
  task_type: "流行病建模"
  duration: "3 weeks"
  success: true

approach:
  task_breakdown: "使用的任务分解"
  methods: "使用的SD方法"
  tools: "Vensim, PySD"

results:
  model_quality: "模型质量评分 (1-5)"
  calibration: "校准拟合度"
  validation: "验证结果"

issues:
  - issue: "参数不确定性"
    resolution: "贝叶斯校准"

lessons:
  successful_patterns: "成功模式"
  improvement_areas: "改进空间"
  effectiveness_score: 4.5
```

---

**版本**: 5.0.0-cli-native
**完成度**: 100%

## 核心概念

**Stock (存量)**: 系统中积累的量（人口、财富、知识）
**Flow (流量)**: 改变存量的速率（出生/死亡、收入/支出）
**反馈回路**:
- 正反馈 (R): 增强回路、增长引擎
- 负反馈 (B): 平衡回路、目标 seeking

**延迟**:
- 物质延迟: 物质流动的时间
- 信息延迟: 信息感知和决策的时间

**参考模式**: 系统行为的时间模式（增长、振荡、S形、崩溃、超调）

## 🔄 子Agent支持

本技能支持调用其他专门技能进行协作分析：

```yaml
问题界定阶段:
  - grounded-theory-expert: 提取关键变量
  - survey-design-expert: 设计测量方案

系统建模阶段:
  - social-network-analysis-expert: 分析网络结构
  - data-analysis-expert: 时间序列分析

政策分析阶段:
  - qca-analysis-expert: 识别政策构型
  - business-ecosystem-expert: 评估系统影响
```

详见 SUBAGENT_EXAMPLE.md 获取完整示例。

## 相关工具

- Vensim
- Stella
- AnyLogic
- Insight Maker
- Python (PySD)
