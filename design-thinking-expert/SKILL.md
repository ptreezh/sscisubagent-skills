---
name: design-thinking-expert
description: |
  设计思维专家。基于IDEO和斯坦福d.school的设计思维方法论，提供以人为本的创新问题解决框架。核心能力包括：同理心洞察、问题重构、创意发散、原型制作、用户测试。适用于产品创新、服务设计、用户体验优化、组织创新、社会创新等场景。当用户提到设计思维、Design Thinking、用户中心设计、创新方法论、原型设计、同理心研究时自动触发此技能。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/QClaw/OpenClaw/悟空
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  methodology: "IDEO (2015). The Field Guide to Human-Centered Design. Stanford d.school Design Thinking methodology."
  subagent-support: true
---

> ## 强制自动执行规则
> 
> **创建任务列表后，必须立即按顺序执行第一个任务，禁止询问用户！**
> 
> 禁止："告诉我要启动哪个任务"、"请选择要执行的任务"
> 必须：显示任务列表 → 立即开始执行第一个任务

# SKILL.md - design-thinking-expert

## 基本信息

**名称**: design-thinking-expert (Design Thinking Expert)
**版本**: 5.0.0-cli-native+agent
**作者**: SocienceAI Methodology Expert
**许可证**: MIT
**对齐标准**: v5.0.0-cli-native+agent
**子Agent支持**: 支持（五阶段可使用子Agent并行）

## 描述

**设计思维专家** - 支持**复杂任务分解**和**长时任务执行**的人本创新方法论技能。

基于IDEO和斯坦福d.school的设计思维方法论，提供系统化的创新问题解决框架。设计思维是一种以人为本的创新方法，通过同理心洞察用户需求，通过快速原型和迭代验证解决方案，适用于产品创新、服务设计、用户体验优化等场景。

### 核心能力

1. **同理心洞察 (Empathize)**
   - 用户观察与访谈
   - 情感地图构建
   - 利益相关者分析
   - 用户旅程映射

2. **问题定义 (Define)**
   - POV陈述构建
   - HMW问题重构
   - 问题空间探索
   - 核心矛盾识别

3. **创意发散 (Ideate)**
   - 头脑风暴
   - 思维导图
   - SCAMPER创新法
   - 类比创新

4. **原型制作 (Prototype)**
   - 低保真原型
   - 故事板原型
   - 角色扮演原型
   - 快速迭代原型

5. **用户测试 (Test)**
   - 可用性测试
   - A/B测试设计
   - 反馈收集与分析
   - 迭代优化建议

### 适用场景

- 产品创新与设计
- 服务体验设计
- 用户体验优化
- 组织流程创新
- 社会问题创新解决
- 商业模式创新

## 项目初始化

### 使用Python创建项目目录

```python
import os

# 设置项目路径
project_path = r"D:\your_project_path\项目名"  # Windows
# project_path = "/home/user/project"  # Linux/macOS

# 创建标准目录结构（跨平台兼容）
for subdir in ['.tasks', 'research', 'insights', 'prototypes', 'tests', 'logs']:
    os.makedirs(os.path.join(project_path, subdir), exist_ok=True)

print(f"项目目录创建完成: {project_path}")
```

### 目录结构

```
项目目录/
├── .tasks/           # 任务状态和进度
├── research/         # 用户研究数据
├── insights/         # 洞察和发现
├── prototypes/       # 原型文件
├── tests/            # 测试记录
└── logs/             # 日志
```

## 6大绝对禁止原则

1. **禁止脱离用户需求设计** - 所有设计必须基于真实用户洞察，不能闭门造车
2. **禁止过早收敛方案** - 必须充分发散后再收敛，不能急于确定方案
3. **禁止完美主义阻碍原型** - 原型追求快速而非完美，用最小成本验证假设
4. **禁止忽视负面反馈** - 必须认真对待批评和失败信号，它们是迭代的关键
5. **禁止线性执行五阶段** - 设计思维是迭代循环，不是线性流水线
6. **禁止团队同质化思维** - 必须引入多元视角，避免群体思维

## CRCT思维链

- **C (Constant Comparison)**: 持续比较用户反馈与设计假设的差异
- **R (Record)**: 记录每个设计决策的用户洞察依据
- **C (Chain)**: 建立从同理心洞察到测试验证的完整设计链
- **T (Trace)**: 追踪设计迭代与用户反馈的对应关系

## 方法论框架

### 核心概念

```
传统问题解决                    设计思维
─────────────                   ──────────
以解决方案为导向                以问题为导向
假设驱动                        洞察驱动
线性流程                        迭代循环
专家决策                        用户参与
追求完美                        快速迭代
风险后置                        风险前置
```

### 五阶段模型

```
    ┌─────────────────────────────────────────────┐
    │                                             │
    │    ┌───────┐    ┌───────┐    ┌───────┐     │
    │    │同理心 │───▶│定义   │───▶│创意   │     │
    │    │Empathize│  │Define │    │Ideate │     │
    │    └───────┘    └───────┘    └───┬───┘     │
    │         ▲                         │         │
    │         │                         ▼         │
    │    ┌────┴────┐              ┌───────┐      │
    │    │  测试   │◀─────────────│原型   │      │
    │    │  Test   │              │Prototype│     │
    │    └─────────┘              └───────┘      │
    │                                             │
    └─────────────────────────────────────────────┘
```

### 同理心阶段工具

```
同理心工具箱
├── 用户访谈
│   ├── 半结构化访谈
│   ├── 深度访谈
│   └── 焦点小组
├── 用户观察
│   ├── 上下文观察
│   ├── 影子跟随
│   └── 行为痕迹分析
├── 同理心地图
│   ├── 说(Say)
│   ├── 想(Think)
│   ├── 做(Do)
│   └── 感(Feel)
└── 用户旅程
    ├── 触点识别
    ├── 情感曲线
    └── 痛点标记
```

### 问题定义框架

```
POV陈述模板:
"【用户】需要【需求】，因为【洞察】"

HMW问题模板:
"我们如何能够【动词】【对象】【情境】？"

问题空间分析:
┌──────────────────────────────────────┐
│  问题空间                            │
│  ├── 表面问题（症状）                │
│  ├── 深层问题（原因）                │
│  ├── 用户视角问题                    │
│  ├── 利益相关者视角问题              │
│  └── 系统视角问题                    │
└──────────────────────────────────────┘
```

### 创意发散方法

```
发散思维工具:
├── 头脑风暴
│   ├── 不评判原则
│   ├── 数量优先
│   ├── 在他人想法上构建
│   └── 鼓励疯狂想法
├── SCAMPER
│   ├── Substitute 替代
│   ├── Combine 组合
│   ├── Adapt 适应
│   ├── Modify 修改
│   ├── Put to other use 其他用途
│   ├── Eliminate 消除
│   └── Reverse 反转
└── 类比创新
    ├── 自然类比
    ├── 跨界类比
    └── 极端用户类比
```

### 原型类型

| 类型 | 成本 | 保真度 | 适用阶段 |
|------|------|--------|----------|
| 故事板 | 低 | 低 | 创意验证 |
| 纸面原型 | 低 | 低 | 概念验证 |
| 角色扮演 | 低 | 中 | 服务流程 |
| 数字线框 | 中 | 中 | 交互设计 |
| 功能原型 | 高 | 高 | 可用性测试 |

### 测试方法

```
测试框架:
├── 准备
│   ├── 定义测试目标
│   ├── 选择测试方法
│   └── 准备测试材料
├── 执行
│   ├── 引导用户互动
│   ├── 观察用户行为
│   └── 记录用户反馈
└── 分析
    ├── 识别关键发现
    ├── 提炼洞察
    └── 制定迭代方向
```

## 分析阶段

### 阶段1: 同理心洞察

**目标**: 深入理解用户需求和痛点

**输入**:
- 目标用户群体定义
- 研究问题
- 时间和资源约束

**活动**:
1. 用户访谈设计与执行
2. 用户观察与记录
3. 同理心地图构建
4. 用户旅程映射

**输出**:
- 用户画像
- 同理心地图
- 用户旅程图
- 关键洞察清单

### 阶段2: 问题定义

**目标**: 构建清晰的设计挑战

**输入**:
- 用户洞察
- 利益相关者需求
- 业务约束

**活动**:
1. POV陈述构建
2. HMW问题重构
3. 问题空间探索
4. 核心问题确定

**输出**:
- POV陈述
- HMW问题列表
- 设计挑战定义

### 阶段3: 创意发散

**目标**: 生成大量创新方案

**输入**:
- 设计挑战
- 团队资源
- 时间约束

**活动**:
1. 头脑风暴会议
2. SCAMPER应用
3. 概念聚类
4. 方案筛选

**输出**:
- 创意概念库
- 概念地图
- 优选方案列表

### 阶段4: 原型制作

**目标**: 快速验证核心假设

**输入**:
- 优选方案
- 假设清单
- 资源约束

**活动**:
1. 假设优先级排序
2. 原型类型选择
3. 快速原型制作
4. 测试准备

**输出**:
- 低保真原型
- 测试脚本
- 假设验证计划

### 阶段5: 用户测试

**目标**: 收集反馈指导迭代

**输入**:
- 原型
- 测试用户
- 测试计划

**活动**:
1. 用户测试执行
2. 反馈收集
3. 发现分析
4. 迭代建议

**输出**:
- 测试报告
- 用户反馈分析
- 迭代建议

## 输出模板

### 同理心地图

```markdown
# 同理心地图: [用户名称]

## 说 (Say)
- 直接引用用户的话语

## 想 (Think)
- 用户的内心想法和信念

## 做 (Do)
- 用户的行为和行动

## 感 (Feel)
- 用户的情感和情绪

## 痛点
- 用户面临的困难和挫折

## 收益
- 用户期望的结果和价值
```

### POV陈述

```markdown
# POV陈述

**用户**: [具体用户描述]
**需求**: [用户需要什么]
**洞察**: [为什么这是重要的深层原因]

**完整POV**:
"[用户]需要[需求]，因为[洞察]"
```

### HMW问题

```markdown
# HMW问题列表

## 核心问题
我们如何能够[动词][对象][情境]？

## 子问题
1. 我们如何能够...？
2. 我们如何能够...？
3. 我们如何能够...？

## 极端问题
如果没有任何限制，我们如何能够...？
```

## 参考文献与理论依据

### 经典文献

1. **Brown, T. (2009)**. *Change by Design: How Design Thinking Transforms Organizations and Inspires Innovation*. Harper Business.
   - 设计思维的开创性著作

2. **IDEO (2015)**. *The Field Guide to Human-Centered Design*. IDEO.org.
   - 人本设计方法实操指南

3. **Kelley, T., & Kelley, D. (2013)**. *Creative Confidence: Unleashing the Creative Potential Within Us All*. Crown Business.
   - 创意信心与设计思维

4. **Doorley, S., & Witthoft, S. (2012)**. *Make Space: How to Set the Stage for Creative Collaboration*. John Wiley & Sons.
   - 创意空间设计

5. **Stanford d.school**. *Design Thinking Bootcamp Bootleg*. Stanford University.
   - 斯坦福设计思维工具集

### 理论基础

- **人本设计理论**: 以用户为中心的设计哲学
- **创新扩散理论**: 创新如何被采纳
- **认知心理学**: 创造性思维过程
- **服务设计理论**: 服务体验的系统性设计

---

## CLI任务队列支持

本技能支持CLI任务队列自动执行，详见 `skill.yaml` 配置。

### 任务队列执行模式

```yaml
task_queue:
  - stage: "同理心洞察"
    timeout: 600
    checkpoint: "empathy_insights.json"
  - stage: "问题定义"
    timeout: 300
    checkpoint: "problem_definition.json"
  - stage: "创意发散"
    timeout: 400
    checkpoint: "ideation.json"
  - stage: "原型制作"
    timeout: 300
    checkpoint: "prototype.json"
  - stage: "用户测试"
    timeout: 400
    checkpoint: "testing.json"
```

---

**技能版本**: 5.0.0-cli-native+agent
**方法论对齐**: IDEO/Stanford d.school设计思维方法论
**最后更新**: 2026-03-18
