---
name: okr-expert
description: |
  OKR目标管理专家。基于Intel和Google的OKR方法论，提供目标设定、关键结果设计、对齐检查、执行追踪、复盘优化。核心能力包括：O目标制定、KR关键结果设计、对齐检查、进度追踪、复盘改进。适用于战略执行、团队目标管理、个人成长规划等场景。当用户提到OKR、目标关键结果、Objectives and Key Results、目标管理、绩效管理时自动触发此技能。
license: MIT
compatibility: |
  Python 3.8+
  AI CLI: Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/Cursor/Windsurf/QClaw/OpenClaw/悟空
  agentskills.io: v1.0 compliant
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  methodology: "Doerr, J. (2018). Measure What Matters. Portfolio."
  subagent-support: true
---

> ## 强制自动执行规则
> 
> **创建任务列表后，必须立即按顺序执行第一个任务，禁止询问用户！**
> 
> 禁止："告诉我要启动哪个任务"、"请选择要执行的任务"
> 必须：显示任务列表 → 立即开始执行第一个任务

# SKILL.md - okr-expert

## 基本信息

**名称**: okr-expert (OKR Expert)
**版本**: 5.0.0-cli-native+agent
**作者**: SocienceAI Methodology Expert
**许可证**: MIT
**对齐标准**: v5.0.0-cli-native+agent
**子Agent支持**: 支持（多团队OKR对齐可并行）

## 描述

**OKR目标管理专家** - 支持**复杂任务分解**和**长时任务执行**的目标管理方法论技能。

基于Intel和Google推广的OKR（Objectives and Key Results）方法论，提供系统化的目标设定与执行追踪框架。OKR是一种简单而强大的目标管理方法，通过设定有挑战性的目标（O）和可衡量的关键结果（KR），实现战略对齐和执行聚焦。

### 核心能力

1. **目标(O)制定**
   - 目标设计原则
   - 挑战性目标设定
   - 目标对齐检查
   - 目标优先级排序

2. **关键结果(KR)设计**
   - KR设计原则
   - 量化指标选择
   - KR平衡设计
   - 进度度量方法

3. **对齐与沟通**
   - 上下对齐检查
   - 横向协同对齐
   - OKR公开透明
   - 定期沟通机制

4. **执行与追踪**
   - 周进度检查
   - 月度复盘
   - 季度评估
   - 调整优化

5. **复盘与改进**
   - OKR评分
   - 复盘方法论
   - 经验提取
   - 下周期优化

### 适用场景

- 企业战略执行
- 团队目标管理
- 个人成长规划
- 项目目标管理
- 跨部门协同
- 创业公司管理

## 项目初始化

### 使用Python创建项目目录

```python
import os

# 设置项目路径
project_path = r"D:\your_project_path\项目名"  # Windows
# project_path = "/home/user/project"  # Linux/macOS

# 创建标准目录结构（跨平台兼容）
for subdir in ['.tasks', 'objectives', 'key-results', 'tracking', 'reviews', 'logs']:
    os.makedirs(os.path.join(project_path, subdir), exist_ok=True)

print(f"项目目录创建完成: {project_path}")
```

### 目录结构

```
项目目录/
├── .tasks/           # 任务状态和进度
├── objectives/       # 目标记录
├── key-results/      # 关键结果追踪
├── tracking/         # 进度追踪数据
├── reviews/          # 复盘记录
└── logs/             # 日志
```

## 6大绝对禁止原则

1. **禁止将OKR与绩效薪酬直接挂钩** - OKR是管理工具，不是考核工具
2. **禁止设定过多目标** - 每个周期不超过3-5个目标，保持聚焦
3. **禁止目标缺乏挑战性** - OKR追求"不可能完成但值得追求"的目标
4. **禁止KR不可衡量** - 关键结果必须是可量化的，不能模糊
5. **禁止设置后不追踪** - OKR需要定期检查，不能"设而不管"
6. **禁止自上而下强制摊派** - OKR需要团队参与制定，而非命令式分配

## CRCT思维链

- **C (Constant Comparison)**: 持续比较目标与实际进展的差距
- **R (Record)**: 记录每个OKR周期的执行情况和复盘结果
- **C (Chain)**: 建立从战略目标到个人行动的完整链条
- **T (Trace)**: 追踪每个关键结果的达成路径

## 方法论框架

### 核心概念

```
传统目标管理                    OKR方法
─────────────                   ──────────
自上而下指令                    上下对齐协同
安全可达目标                    挑战性目标
与薪酬挂钩                      独立于薪酬
年度设定                        季度迭代
秘密执行                        公开透明
完成率100%为成功                70%为理想状态
考核工具                        管理工具
```

### OKR结构

```
Objective (目标)
"What we want to accomplish"
- 定性描述
- 有挑战性
- 鼓舞人心
- 与战略对齐

├── Key Result 1 (关键结果1)
│   "How we measure success"
│   - 可量化
│   - 有截止日期
│   - 可达成
│
├── Key Result 2 (关键结果2)
│   - 可量化
│   - 有截止日期
│   - 可达成
│
└── Key Result 3 (关键结果3)
    - 可量化
    - 有截止日期
    - 可达成
```

### OKR设计原则

**目标(O)设计原则**:
```
1. 定性描述 - 描述"要达成什么"
2. 有挑战性 - 理想完成率60-70%
3. 鼓舞人心 - 激发团队热情
4. 可理解 - 清晰明确
5. 可行动 - 团队可以采取行动
6. 数量限制 - 每周期3-5个
```

**关键结果(KR)设计原则**:
```
1. 可量化 - 必须能用数字衡量
2. 有时限 - 明确截止日期
3. 可达成 - 经过努力可以完成
4. 结果导向 - 关注产出而非投入
5. 独立性 - KR之间相互独立
6. 数量限制 - 每个O对应3-5个KR
```

### OKR对齐模型

```
           公司战略OKR
               │
        ┌──────┼──────┐
        │      │      │
     部门OKR 部门OKR 部门OKR
        │      │      │
    ┌───┼───┐  │  ┌───┼───┐
    │   │   │  │  │   │   │
  团队OKR  团队OKR  团队OKR
    │       │       │
  个人OKR 个人OKR 个人OKR
```

### OKR生命周期

```
OKR周期（通常为季度）:

第1周: OKR制定
├── 回顾上周期OKR
├── 分析战略重点
├── 团队讨论制定
└── 对齐确认

第2-11周: 执行与追踪
├── 周检查（15分钟）
├── 月度复盘（1小时）
└── 中期调整

第12周: 复盘与评分
├── OKR评分
├── 复盘会议
├── 经验总结
└── 下周期规划
```

### OKR评分标准

| 分数 | 含义 | 判断 |
|------|------|------|
| 0.0-0.3 | 未达预期 | 目标设定可能太高或执行不力 |
| 0.4-0.6 | 接近达成 | 正常范围，有进步 |
| 0.7-1.0 | 超出预期 | 目标可能设定太低 |

**理想状态**: OKR平均分在0.6-0.7

## 分析阶段

### 阶段1: 战略理解与目标定位

**目标**: 理解战略方向，确定OKR定位

**输入**:
- 公司/部门战略
- 上级OKR
- 业务现状

**活动**:
1. 分析战略重点
2. 识别关键挑战
3. 确定OKR范围
4. 与上级对齐

**输出**:
- 战略理解文档
- OKR定位说明
- 对齐关系图

### 阶段2: 目标(O)设计

**目标**: 设计有挑战性的目标

**输入**:
- 战略重点
- 业务痛点
- 团队能力

**活动**:
1. 目标头脑风暴
2. 挑战性评估
3. 对齐检查
4. 优先级排序

**输出**:
- 目标清单
- 目标描述
- 优先级矩阵

### 阶段3: 关键结果(KR)设计

**目标**: 设计可衡量的关键结果

**输入**:
- 确定的目标
- 历史数据
- 资源情况

**活动**:
1. 指标选择
2. 基准线确定
3. 目标值设定
4. KR验证

**输出**:
- KR清单
- 量化指标
- 目标值

### 阶段4: 对齐与沟通

**目标**: 确保OKR上下左右对齐

**输入**:
- 团队OKR
- 上级OKR
- 协作方OKR

**活动**:
1. 向上对齐检查
2. 向下传达
3. 横向协同
4. 公开透明

**输出**:
- 对齐关系图
- 协同协议
- 公开OKR

### 阶段5: 执行追踪与复盘

**目标**: 确保OKR有效执行

**输入**:
- OKR文档
- 执行进度

**活动**:
1. 周进度检查
2. 月度复盘
3. 季度评分
4. 经验总结

**输出**:
- 进度报告
- 评分结果
- 复盘报告

## 输出模板

### OKR文档模板

```markdown
# OKR文档 - [周期]

## 目标1: [目标描述]

**为什么重要**: [战略关联说明]

### 关键结果
| KR | 描述 | 目标值 | 当前值 | 进度 |
|----|------|--------|--------|------|
| KR1.1 | [描述] | [值] | [值] | [%] |
| KR1.2 | [描述] | [值] | [值] | [%] |
| KR1.3 | [描述] | [值] | [值] | [%] |

## 目标2: [目标描述]

**为什么重要**: [战略关联说明]

### 关键结果
| KR | 描述 | 目标值 | 当前值 | 进度 |
|----|------|--------|--------|------|
| KR2.1 | [描述] | [值] | [值] | [%] |
| KR2.2 | [描述] | [值] | [值] | [%] |
```

### 周检查模板

```markdown
# OKR周检查 - 第[X]周

## 进度更新
| OKR | 上周进度 | 本周进度 | 变化 |
|-----|----------|----------|------|
| O1 | [%] | [%] | [+/-] |
| O2 | [%] | [%] | [+/-] |

## 本周亮点
- [亮点1]
- [亮点2]

## 本周问题
- [问题1]
- [问题2]

## 下周重点
- [ ] [重点1]
- [ ] [重点2]
```

### 复盘报告模板

```markdown
# OKR复盘报告 - [周期]

## OKR评分

| 目标 | KR | 目标值 | 实际值 | 分数 |
|------|-----|--------|--------|------|
| O1 | KR1.1 | [值] | [值] | [分] |
| O1 | KR1.2 | [值] | [值] | [分] |

**平均分**: [分]

## 完成情况分析
- 成功的OKR: [列表]
- 未达成的OKR: [列表]

## 经验总结
### 做得好的
1. [经验1]
2. [经验2]

### 需要改进的
1. [改进点1]
2. [改进点2]

## 下周期建议
1. [建议1]
2. [建议2]
```

## 参考文献与理论依据

### 经典文献

1. **Doerr, J. (2018)**. *Measure What Matters: How Google, Bono, and the Gates Foundation Rock the World with OKRs*. Portfolio.
   - OKR方法论的权威著作

2. **Wodtke, C. (2016)**. *Radical Focus: Achieving Your Most Important Goals with Objectives and Key Results*. Cucina Media.
   - OKR实践指南

3. **Niven, P. R., & Lamorte, B. (2016)**. *Objectives and Key Results: Driving Focus, Alignment, and Engagement with OKRs*. Wiley.
   - OKR实施手册

4. **Grove, A. (1983)**. *High Output Management*. Random House.
   - Intel的管理哲学，OKR起源

### 理论基础

- **目标设定理论**: Locke & Latham的目标设定研究
- **管理控制系统**: 战略执行的控制机制
- **组织行为学**: 目标一致性与动机理论
- **绩效管理**: 目标导向的绩效体系

---

## CLI任务队列支持

本技能支持CLI任务队列自动执行，详见 `skill.yaml` 配置。

### 任务队列执行模式

```yaml
task_queue:
  - stage: "战略理解与目标定位"
    timeout: 300
    checkpoint: "strategy_alignment.json"
  - stage: "目标设计"
    timeout: 300
    checkpoint: "objectives.json"
  - stage: "关键结果设计"
    timeout: 300
    checkpoint: "key_results.json"
  - stage: "对齐与沟通"
    timeout: 200
    checkpoint: "alignment.json"
  - stage: "复盘评估"
    timeout: 300
    checkpoint: "review.json"
```

---

**技能版本**: 5.0.0-cli-native+agent
**方法论对齐**: Intel/Google OKR方法论
**最后更新**: 2026-03-18
