# 敏捷项目管理经典文献

## 核心文献

### 1. Agile Manifesto (2001)
**《敏捷软件开发宣言》**

核心价值观：
1. **个体和互动** 高于流程和工具
2. **工作的软件** 高于详尽的文档
3. **客户合作** 高于合同谈判
4. **响应变化** 高于遵循计划

> "While there is value in the items on the right, we value the items on the left more."

### 2. Ken Schwaber & Jeff Sutherland - Scrum Guide (2020)
**《Scrum指南》**

Scrum框架三大支柱：
- **透明性 (Transparency)**
- **检视 (Inspection)**
- **适应 (Adaptation)**

### 3. Jeff Sutherland - Scrum: The Art of Doing Twice the Work in Half the Time (2014)
**《Scrum：用一半的时间做两倍的事》**

关键概念：
- Sprint周期
- 每日站会
- 回顾会议

## Scrum框架详解

### 角色 (Roles)

| 角色 | 职责 |
|------|------|
| Product Owner | 产品价值最大化，管理产品待办列表 |
| Scrum Master | 过程促进者，消除障碍 |
| Development Team | 自组织、跨功能团队 |

### 事件 (Events)

| 事件 | 时长 | 目的 |
|------|------|------|
| Sprint Planning | 2-4小时 | 确定Sprint目标和待办事项 |
| Daily Scrum | 15分钟 | 同步进度和障碍 |
| Sprint Review | 1-2小时 | 展示成果，收集反馈 |
| Sprint Retrospective | 1-1.5小时 | 反思改进 |

### 工件 (Artifacts)

1. **Product Backlog**：产品待办列表（有序优先级）
2. **Sprint Backlog**：Sprint待办列表（当前迭代）
3. **Increment**：产品增量（可交付成果）

## 用户故事 (User Stories)

### 格式

```
作为 <角色>
我想要 <功能>
以便于 <价值>
```

### INVEST原则

| 原则 | 含义 | 检查 |
|------|------|------|
| I - Independent | 独立的 | 可以单独开发吗？ |
| N - Negotiable | 可协商的 | 细节可以讨论吗？ |
| V - Valuable | 有价值的 | 对用户有价值吗？ |
| E - Estimable | 可估算的 | 能估算工作量吗？ |
| S - Small | 足够小 | 能在一个Sprint完成吗？ |
| T - Testable | 可测试的 | 有明确的验收标准吗？ |

## 敏捷度量

### 速度 (Velocity)

```
速度 = 一个Sprint完成的用户故事点数总和
```

用途：
- Sprint规划参考
- 发布预测
- 不用于绩效考核

### 燃尽图 (Burndown Chart)

```
剩余工作量
    |
    |\
    | \
    |  \_____  实际进度
    |        \
    |________\____ Sprint结束
    理想进度线
```

### 周期时间 (Cycle Time)

```
周期时间 = 完成时间 - 开始时间
```

## Kanban方法

### 核心原则

1. **可视化工作流程**
2. **限制在制品数量 (WIP Limits)**
3. **管理流动**
4. **显式流程政策**
5. **实施反馈环**
6. **协作改进**

### 看板列

```
待办 → 进行中(WIP:3) → 测试(WIP:2) → 完成
```

## 定义完成 (Definition of Done)

示例清单：
- [ ] 代码已审查
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 文档已更新
- [ ] 产品负责人验收
- [ ] 已部署到测试环境

## 参考资源

- Scrum.org: https://www.scrum.org/
- Agile Alliance: https://www.agilealliance.org/
- Atlassian Agile: https://www.atlassian.com/agile
