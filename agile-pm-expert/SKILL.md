---
name: agile-pm-expert
description: |
  敏捷项目管理专家。基于Scrum和Kanban的敏捷方法论，提供Sprint规划、迭代执行、站会管理、回顾改进。核心能力包括：产品待办列表管理、Sprint规划、每日站会、Sprint评审、回顾会议、敏捷度量。适用于软件开发项目、产品迭代、团队协作优化等场景。当用户提到敏捷、Agile、Scrum、Sprint、Kanban、站会、迭代时自动触发此技能。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/QClaw/OpenClaw/悟空
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  methodology: "Schwaber, K. & Sutherland, J. (2020). Scrum Guide."
  subagent-support: true
---

> ## 强制自动执行规则
> 
> **创建任务列表后，必须立即按顺序执行第一个任务，禁止询问用户！**
> 
> 禁止："告诉我要启动哪个任务"、"请选择要执行的任务"
> 必须：显示任务列表 → 立即开始执行第一个任务

# SKILL.md - agile-pm-expert

## 基本信息

**名称**: agile-pm-expert (Agile Project Management Expert)
**版本**: 5.0.0-cli-native+agent
**作者**: SocienceAI Methodology Expert
**许可证**: MIT
**对齐标准**: v5.0.0-cli-native+agent
**子Agent支持**: 支持（多Sprint可并行管理）

## 描述

**敏捷项目管理专家** - 支持**复杂任务分解**和**长时任务执行**的项目管理方法论技能。

基于Scrum和Kanban的敏捷方法论，提供系统化的项目管理框架。敏捷项目管理是一种迭代增量的项目管理方法，通过短周期交付、持续反馈和团队自组织，实现高效的价值交付。

### 核心能力

1. **产品待办列表管理**
   - 用户故事编写
   - 优先级排序
   - 故事点估算
   - 待办列表细化

2. **Sprint规划与执行**
   - Sprint目标设定
   - 任务分解
   - 容量规划
   - Sprint待办列表

3. **Scrum仪式管理**
   - 每日站会
   - Sprint评审
   - Sprint回顾
   - Sprint规划

4. **敏捷度量与可视化**
   - 燃尽图/燃起图
   - 速度追踪
   - 周期时间分析
   - 看板管理

5. **持续改进**
   - 回顾会议引导
   - 改进项追踪
   - 实验设计
   - 团队成熟度评估

### 适用场景

- 软件开发项目
- 产品迭代开发
- 团队协作优化
- 跨职能项目管理
- 创新项目管理
- 运维与支持团队

## 项目初始化

### 使用Python创建项目目录

```python
import os

# 设置项目路径
project_path = r"D:\your_project_path\项目名"  # Windows
# project_path = "/home/user/project"  # Linux/macOS

# 创建标准目录结构（跨平台兼容）
for subdir in ['.tasks', 'product-backlog', 'sprints', 'metrics', 'retrospectives', 'logs']:
    os.makedirs(os.path.join(project_path, subdir), exist_ok=True)

print(f"项目目录创建完成: {project_path}")
```

### 目录结构

```
项目目录/
├── .tasks/           # 任务状态和进度
├── product-backlog/  # 产品待办列表
├── sprints/          # Sprint记录
├── metrics/          # 敏捷度量数据
├── retrospectives/   # 回顾会议记录
└── logs/             # 日志
```

## 6大绝对禁止原则

1. **禁止Sprint中途变更目标** - Sprint开始后不得随意改变Sprint目标
2. **禁止忽视技术债务** - 必须在迭代中安排技术债务处理时间
3. **禁止站会变成汇报会议** - 站会是团队同步，不是向管理者汇报
4. **禁止忽视回顾会议** - 回顾是持续改进的核心，不可省略
5. **禁止管理者分配任务** - 团队成员自主认领任务，自组织是核心
6. **禁止过度承诺** - Sprint规划必须基于团队能力，不可强压

## CRCT思维链

- **C (Constant Comparison)**: 持续比较计划进度与实际进度的差异
- **R (Record)**: 记录每个Sprint的数据和回顾结果
- **C (Chain)**: 建立从产品愿景到用户故事的完整链条
- **T (Trace)**: 追踪每个用户故事的完成路径

## 方法论框架

### 核心概念

```
传统项目管理                  敏捷项目管理
─────────────                 ──────────
预测性规划                    适应性规划
大爆炸交付                    迭代交付
文档驱动                      价值驱动
命令控制                      自组织团队
流程合规                      工作软件
合同谈判                      客户协作
遵循计划                      响应变化
```

### Scrum框架

```
        ┌─────────────────────────────────────────────┐
        │              产品负责人                      │
        │          Product Owner                       │
        └──────────────────┬──────────────────────────┘
                           │
                           ▼
        ┌─────────────────────────────────────────────┐
        │           产品待办列表                       │
        │         Product Backlog                      │
        │  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐            │
        │  │ 1 │ │ 2 │ │ 3 │ │ 4 │ │...│            │
        │  └───┘ └───┘ └───┘ └───┘ └───┘            │
        └──────────────────┬──────────────────────────┘
                           │ Sprint规划
                           ▼
        ┌─────────────────────────────────────────────┐
        │           Sprint待办列表                     │
        │          Sprint Backlog                      │
        │  ┌─────────────────────────────────────┐    │
        │  │  Sprint目标: [目标描述]              │    │
        │  ├─────────────────────────────────────┤    │
        │  │  任务1  ▶ 进行中  ✓ 完成           │    │
        │  │  任务2  □ 待开始                    │    │
        │  │  任务3  ▶ 进行中                    │    │
        │  └─────────────────────────────────────┘    │
        └──────────────────┬──────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
   ┌─────────┐       ┌─────────┐       ┌─────────┐
   │ 每日站会 │       │Sprint评审│       │Sprint回顾│
   │  15分钟  │       │  2小时   │       │ 1.5小时  │
   └─────────┘       └─────────┘       └─────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           ▼
        ┌─────────────────────────────────────────────┐
        │              产品增量                        │
        │           Increment                          │
        │        [可交付的产品增量]                    │
        └─────────────────────────────────────────────┘
```

### Scrum角色

```
Scrum角色:
├── 产品负责人 (Product Owner)
│   - 定义产品愿景
│   - 管理产品待办列表
│   - 决定发布时间和内容
│   - 对产品价值负责
│
├── Scrum Master
│   - 服务型领导
│   - 移除障碍
│   - 促进Scrum实践
│   - 保护团队
│
└── 开发团队 (Development Team)
    - 自组织
    - 跨职能
    - 对Sprint承诺负责
    - 集体责任制
```

### Scrum事件

| 事件 | 时长 | 频率 | 目的 |
|------|------|------|------|
| Sprint规划 | 2-4小时 | Sprint开始 | 规划Sprint工作 |
| 每日站会 | 15分钟 | 每天 | 同步进度和障碍 |
| Sprint评审 | 2小时 | Sprint结束 | 展示产品增量 |
| Sprint回顾 | 1.5小时 | Sprint结束 | 团队改进 |
| Sprint | 1-4周 | 持续 | 迭代周期 |

### Scrum工件

```
Scrum工件:
├── 产品待办列表 (Product Backlog)
│   - 用户故事
│   - 缺陷修复
│   - 技术任务
│   - 优先级排序
│   - 持续细化
│
├── Sprint待办列表 (Sprint Backlog)
│   - 本Sprint承诺
│   - 任务分解
│   - 每日更新
│   - 团队可见
│
└── 产品增量 (Increment)
    - 可交付价值
    - 符合完成定义
    - 可发布状态
```

### 用户故事格式

```
用户故事格式:

作为 [用户角色]
我想要 [功能/目标]
以便于 [价值/原因]

示例:
作为 电商用户
我想要 查看订单历史
以便于 追踪我的购买记录

验收标准:
- [ ] 显示最近30天订单
- [ ] 可按日期筛选
- [ ] 可查看订单详情
- [ ] 支持分页显示
```

### 敏捷度量

```
敏捷度量指标:
├── 速度 (Velocity)
│   - 每Sprint完成的故事点
│   - 用于容量规划
│   - 不用于绩效评估
│
├── 燃尽图 (Burndown Chart)
│   - 剩余工作量追踪
│   - 每日更新
│   - 进度可视化
│
├── 周期时间 (Cycle Time)
│   - 从开始到完成的时间
│   - 流程效率指标
│   - 看板核心指标
│
└── 吞吐量 (Throughput)
    - 单位时间完成的工作项
    - 交付能力指标
    - 预测交付时间
```

## 分析阶段

### 阶段1: 项目启动与团队组建

**目标**: 建立敏捷团队和项目基础

**输入**:
- 项目愿景
- 团队成员
- 约束条件

**活动**:
1. 组建Scrum团队
2. 定义角色职责
3. 建立工作协议
4. 设置工具环境

**输出**:
- 团队章程
- 工作协议
- 工具配置

### 阶段2: 产品待办列表创建

**目标**: 建立初始产品待办列表

**输入**:
- 产品愿景
- 用户需求
- 业务目标

**活动**:
1. 用户故事编写
2. 故事优先级排序
3. 故事点估算
4. 待办列表细化

**输出**:
- 产品待办列表
- 用户故事地图
- 发布规划

### 阶段3: Sprint规划

**目标**: 规划下一个Sprint

**输入**:
- 产品待办列表
- 团队容量
- 速度历史

**活动**:
1. 选择Sprint目标
2. 选择用户故事
3. 任务分解
4. 容量确认

**输出**:
- Sprint待办列表
- Sprint目标
- 任务列表

### 阶段4: Sprint执行

**目标**: 完成Sprint承诺

**输入**:
- Sprint待办列表
- 完成定义

**活动**:
1. 每日站会
2. 任务执行
3. 障碍移除
4. 进度更新

**输出**:
- 产品增量
- 燃尽图
- 障碍清单

### 阶段5: Sprint评审与回顾

**目标**: 交付价值并持续改进

**输入**:
- 产品增量
- 干系人

**活动**:
1. Sprint评审
2. 收集反馈
3. 回顾会议
4. 改进计划

**输出**:
- 验收的产品增量
- 回顾报告
- 改进项列表

## 输出模板

### 产品待办列表模板

```markdown
# 产品待办列表

| ID | 用户故事 | 优先级 | 故事点 | 状态 | 负责人 |
|----|----------|--------|--------|------|--------|
| US-001 | 作为用户... | 高 | 8 | 待开始 | - |
| US-002 | 作为管理员... | 中 | 5 | Sprint中 | 张三 |
| US-003 | 作为用户... | 低 | 3 | 完成 | 李四 |
```

### Sprint规划模板

```markdown
# Sprint [N] 规划

## Sprint信息
- Sprint编号: [N]
- 开始日期: [日期]
- 结束日期: [日期]
- 团队容量: [人天]

## Sprint目标
[一句话描述本Sprint要达成的目标]

## 承诺用户故事
| ID | 用户故事 | 故事点 |
|----|----------|--------|
| US-001 | [描述] | 8 |
| US-002 | [描述] | 5 |

**总故事点**: [点]
```

### 回顾会议模板

```markdown
# Sprint [N] 回顾

## 参与者
[参与者列表]

## 做得好 (Keep)
1. [项目1]
2. [项目2]

## 需要改进 (Problem)
1. [问题1]
   - 原因: [分析]
   - 行动: [建议]
2. [问题2]

## 尝试 (Try)
| 改进项 | 负责人 | 完成日期 |
|--------|--------|----------|
| [改进1] | [人] | [日期] |

## 行动项
- [ ] [行动1] @[负责人] #[截止日期]
- [ ] [行动2] @[负责人] #[截止日期]
```

## 参考文献与理论依据

### 经典文献

1. **Schwaber, K. & Sutherland, J. (2020)**. *The Scrum Guide*. Scrum.org.
   - Scrum方法的权威定义

2. **Schwaber, K. (2004)**. *Agile Project Management with Scrum*. Microsoft Press.
   - Scrum实践指南

3. **Kniberg, H. (2010)**. *Scrum and XP from the Trenches*. InfoQ.
   - 真实项目经验分享

4. **Anderson, D. J. (2010)**. *Kanban: Successful Evolutionary Change for Your Technology Business*. Blue Hole Press.
   - 看板方法论

5. **Cohn, M. (2009)**. *Succeeding with Agile: Software Development Using Scrum*. Addison-Wesley.
   - Scrum成功实践

### 理论基础

- **敏捷宣言**: 敏捷软件开发宣言
- **精益生产**: 丰田生产系统
- **复杂适应系统**: 迭代适应理论
- **团队心理学**: 自组织团队理论

---

## CLI任务队列支持

本技能支持CLI任务队列自动执行，详见 `skill.yaml` 配置。

### 任务队列执行模式

```yaml
task_queue:
  - stage: "项目启动"
    timeout: 300
    checkpoint: "project_init.json"
  - stage: "待办列表创建"
    timeout: 400
    checkpoint: "backlog.json"
  - stage: "Sprint规划"
    timeout: 300
    checkpoint: "sprint_planning.json"
  - stage: "Sprint执行"
    timeout: 600
    checkpoint: "sprint_execution.json"
  - stage: "回顾评审"
    timeout: 300
    checkpoint: "retrospective.json"
```

---

**技能版本**: 5.0.0-cli-native+agent
**方法论对齐**: Scrum Guide/Kanban方法论
**最后更新**: 2026-03-18
