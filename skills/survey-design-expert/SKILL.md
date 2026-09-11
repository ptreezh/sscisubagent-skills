---
name: survey-design-expert
description: |
  问卷设计专家。提供问卷结构设计、信度效度检验、抽样计算、预测试管理功能。适用于调查研究、量表开发、数据收集设计场景。
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

# SKILL.md - survey-design-expert

---
metadata:
  version: "5.1.0-cli-native+agent"
  methodology: "Survey Research Methodology"
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
  created: "2026-03-08"
  updated: "2026-03-08"
  author: "SocienceAI Methodology Expert"
  license: "MIT"
  alignment_reference: "grounded-theory-coding (v5.0.0)"

  execution_modes:
    cli_queue: "CLI任务队列（基础）"
    subagent_parallel: "子Agent并行（增强）"

  performance:
    sequential: "45分钟/问卷"
    parallel: "50分钟/10问卷（9.0x加速）"
---

## 基本信息

**名称**: survey-design-expert (问卷设计专家)
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


**问卷设计专家** - 支持**复杂任务分解**和**长时任务执行**的问卷设计技能。

基于Dillman et al. (2014)的问卷设计方法论，支持从研究问题到高质量问卷的完整设计流程。

涵盖问卷设计、题目编写、量表选择、抽样设计、预测试、信效度检验等。

### 核心能力

1. **问卷设计**
   - 研究问题操作化
   - 题目类型选择
   - 问卷结构设计
   - 逻辑流程设计

2. **题目编写**
   - 清晰无歧义
   - 避免偏见
   - 双向翻译（跨文化研究）
   - 题目优化技术

3. **量表选择**
   - Likert量表
   - 语义差异量表
   - 已验证量表
   - 量表信效度检验

4. **抽样设计**
   - 概率抽样（简单随机、分层、整群）
   - 非概率抽样（配额、方便、滚雪球）
   - 样本量计算
   - 抽样框构建

5. **质量检验**
   - 信度（Cronbach's α、重测信度）
   - 效度（内容效度、构念效度、效标效度）
   - 预测试（认知访谈、试测）
   - 数据质量评估

6. **数据收集**
   - 在线调查工具（Qualtrics、SurveyMonkey）
   - 混合模式调查
   - 提升响应率策略
   - 无应答偏差分析

### 适用场景

- ✅ 量化研究数据收集
- ✅ 混合方法研究
- ✅ 态度与行为测量
- ✅ 满意度调查
- ✅ 市场研究
- ✅ 社会科学调查

## ⚠️ 六大绝对禁止原则

### 1. 禁止脱离理论设计题目

**错误做法**:
```yaml
编造题目:
  - 直接"凭感觉"编写题目
  - 不基于文献或理论
  - 不参考已验证量表
  - 题目无理论依据

示例:
  "我想研究用户满意度，
   所以随便编了几个题目"
```

**正确做法**:
```yaml
基于理论设计:
  Step 1: 文献回顾
    - 查找相关理论
    - 寻找已验证量表
    - 理解构念定义

  Step 2: 量表选择/改编
    - 优先使用已验证量表
    - 改编时说明理由
    - 保持核心题目

  Step 3: 新题目设计
    - 基于理论操作化
    - 专家评审
    - 预测试验证
```

**量化标准**:
- ✅ 题目有理论或文献依据
- ✅ 优先使用已验证量表
- ✅ 新题目经过专家评审
- ✅ 所有题目有来源标注

### 2. 禁止歧义与模糊题目

**错误做法**:
```yaml
模糊题目:
  - 使用模糊词汇
  - 时间范围不清
  - 参照对象不明
  - 多义性问题

示例:
  ❌ "您经常使用社交媒体吗?"
     （"经常"定义模糊）

  ❌ "您对这个产品满意吗?"
     （哪个方面？何时？）

  ❌ "您认为公司政策合理吗?"
     （哪些政策？与什么比？）
```

**正确做法**:
```yaml
清晰题目设计:
  原则1: 具体化
    - 时间明确（"过去7天"）
    - 频率量化（"每天X小时"）
    - 对象明确（"公司HR政策"）

  原则2: 单义性
    - 一题一问
    - 避免双重问题
    - 避免复合概念

  原则3: 参照明确
    - 比较标准清晰
    - 评价对象明确
    - 时间范围清晰

正确示例:
  ✅ "在过去7天，您平均每天
     使用社交媒体多少小时?"

  ✅ "您对公司HR部门在员工
     培训方面的政策满意吗?"

  ✅ "与去年相比，您对公司
     福利政策的满意度如何?"
```

**量化标准**:
- ✅ 每个题目含义清晰
- ✅ 时间范围明确
- ✅ 参照对象明确
- ✅ 通过认知访谈验证

### 3. 禁止引导性与偏见题目

**错误做法**:
```yaml
引导性题目:
  - 暗示"正确"答案
  - 使用情绪化语言
  - 预设立场
  - 社会期望偏见

示例:
  ❌ "您不认为这个政策很糟糕吗?"
     （暗示应该认为糟糕）

  ❌ "专家建议每天运动30分钟，
     您每天运动吗?"
     （权威暗示）

  ❌ "大多数人都支持环保，
     您呢?"
     （从众压力）

  ❌ "您会和你的家人一起犯罪吗?"
     （社会期望偏见）
```

**正确做法**:
```yaml
中性题目设计:
  原则1: 平衡表述
    - 避免倾向性词汇
    - 使用中性语言
    - 提供平衡选项

  原则2: 去偏见化
    - 避免权威引用
    - 避免从众暗示
    - 避免情绪化表述

  原则3: 隐私保护
    - 承诺匿名性
    - 说明无对错
    - 正常化敏感行为
    - 使用投射技术

正确示例:
  ✅ "您对这个政策的看法是?"
     （中性）

  ✅ "您平均每天运动多少分钟?"
     （无权威暗示）

  ✅ "您对环保议题的态度是?"
     （无从众暗示）

  ✅ "人们有时会违反交通规则，
     您过去一年是否有过?"
     （正常化）
```

**量化标准**:
- ✅ 题目表述中性
- ✅ 无引导性语言
- ✅ 选项平衡
- ✅ 通过专家评审验证

### 4. 禁止忽视预测试

**错误做法**:
```yaml
跳过预测试:
  - 问卷设计完直接发放
  - 认为自己没问题
  - 忽视潜在问题
  - 浪费研究资源

示例:
  "问卷设计好了，
   直接发给1000人"
```

**正确做法**:
```yaml
完整预测试流程:
  Phase 1: 专家评审
    - 题目清晰性
    - 内容效度
    - 问卷长度
    - 逻辑流程

  Phase 2: 认知访谈（10-15人）
    - 思考 aloud
    - 理解检查
    - 歧义识别
    - 改进建议

  Phase 3: 试测（50-100人）
    - 完整填写
    - 时间测量
    - 信效度检验
    - 数据质量

  Phase 4: 问卷修改
    - 删除/修改问题题目
    - 调整选项
    - 优化流程
    - 最终版确定


## 详细指南

完整的使用指南请参考: [详细指南](references/detailed-guide.md)