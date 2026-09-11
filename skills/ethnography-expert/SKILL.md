---
name: ethnography-expert
description: |
  Ethnography expert. Provides participant observation, field note writing, cultural immersion assessment, thematic analysis, and ethnographic validity checking. Suitable for anthropological research, cultural studies, and qualitative field work.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

---|------|---------|
| 传统民族志 | 长期、深入、单一地点 | 12-24个月 |
| 快速民族志 | 聚焦特定问题 | 2-6个月 |
| 多点民族志 | 跨地点追踪 | 6-18个月 |
| 数字民族志 | 在线社区研究 | 3-12个月 |
| 自传民族志 | 研究者自身经验 | 灵活 |

## 田野工作流程

```
准备阶段
├── 文献回顾
├── 研究问题
├── 进入策略
└── 伦理审批
    ↓
进入田野
├── 建立信任
├── 寻找关键报道人
├── 学习地方知识
└── 适应环境
    ↓
深度田野
├── 参与观察
├── 深度访谈
├── 田野笔记
├── 文献收集
└── 持续反思
    ↓
离开田野
├── 逐步退出
├── 资料整理
├── 补充访谈
└── 关系维护
    ↓
写作阶段
├── 资料分析
├── 文化描述
├── 理论建构
└── 民族志写作
```

## 数据收集方法

### 参与观察

| 观察类型 | 研究者角色 | 适用场景 |
|---------|-----------|---------|
| 完全观察者 | 不参与 | 公共场所 |
| 观察者即参与者 | 有限参与 | 特定活动 |
| 参与者即观察者 | 主要参与 | 社区成员 |
| 完全参与者 | 深度融入 | 长期田野 |

### 深度访谈
- **半结构化**: 有框架但灵活
- **口述史**: 生命历程叙事
- **焦点小组**: 群体互动视角
- **关键报道人**: 深入了解文化

### 田野笔记类型

| 类型 | 内容 | 时机 |
|------|------|------|
| 描述性笔记 | 事实记录 | 即时 |
| 方法论笔记 | 研究过程 | 即时 |
| 理论笔记 | 分析思考 | 反思 |
| 情感笔记 | 个人感受 | 反思 |

## 分析框架

### 主位/客位分析
- **主位(Emic)**: 当地人视角的意义系统
- **客位(Etic)**: 分析者视角的理论框架
- **对话**: 两种视角的互动理解

### 文化模式分析
1. **识别**: 反复出现的模式
2. **描述**: 模式的具体表现
3. **解释**: 模式的文化意义
4. **联系**: 与更大社会结构的关联

### 深描示例

```
薄描: 两个男孩快速眨眼
深描: 这是在特定文化情境下的眨眼实践——
      一场具有意义的社交表演，可能传递着
      密谋的信号、讽刺的姿态或求爱的暗示，
      其意义取决于文化背景和情境理解。
```

## 质量标准

| 标准 | 说明 | 实现方式 |
|------|------|---------|
| 可信性 | 真实呈现 | 三角验证、成员检验 |
| 可转移性 | 可应用他处 | 深描、情境描述 |
| 可依赖性 | 过程一致 | 审计追踪 |
| 可确认性 | 相对客观 | 反思性、透明度 |

## 使用示例

```
用户: 我要研究一个乡村社区的社会支持网络

AI: 我将为您设计一个系统化的民族志研究方案：

## 研究设计

### 进入策略
- 通过村干部或社区领袖介绍
- 参与社区活动建立信任
- 初期以"学习者"身份进入

### 关键报道人选择
- 社区 elders（了解历史）
- 社区活跃分子（了解网络）
- 边缘群体（了解差异）

### 数据收集计划
1. 参与观察（日常互动、节庆活动）
2. 深度访谈（生命史、支持经验）
3. 社会网络映射（支持关系图）

### 分析框架
- 主位视角：社区成员如何理解"互助"
- 客位视角：社会支持的理论概念
- 深描：关键事件的详细描述

[继续详细设计...]
```

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | fieldnote_manager.py | 田野笔记管理与编码，支持描述性/方法论/理论/情感四类笔记 |
| 2 | cultural_pattern_analyzer.py | 文化模式识别与分析，支持主位/客位双视角分析 |
| 3 | key_informant_tracker.py | 关键报道人管理，追踪访谈记录与关系网络 |

### CLI用法

```bash
python tools/fieldnote_manager.py --add --type descriptive --note "田野记录"
python tools/cultural_pattern_analyzer.py --input patterns.json --perspective emic
python tools/key_informant_tracker.py --track --informant "报道人A"
```


## 🚫 绝对禁止原则

> **使用前必读**：以下原则是不可逾越的红线，违反将导致研究结论无效。

1. **禁止跳过研究伦理审查** — 未获IRB批准的实证研究不得用于发表
2. **禁止捏造或篡改数据** — 任何形式的数据造假均违反学术伦理
3. **禁止忽视研究局限性** — 必须在论文中诚实报告研究局限
4. **禁止剽窃他人研究成果** — 必须正确引用所有参考来源
5. **禁止选择性报告结果** — 阴性结果同样需要报告
6. **禁止使用不匹配的分析方法** — 必须根据研究问题选择合适方法

## 参考文献

1. Geertz, C. (1973). *The Interpretation of Cultures*. Basic Books.
2. Malinowski, B. (1922). *Argonauts of the Western Pacific*.
3. Hammersley, M., & Atkinson, P. (2007). *Ethnography: Principles in Practice*. 3rd ed.
4. Emerson, R.M., Fretz, R.I., & Shaw, L.L. (2011). *Writing Ethnographic Fieldnotes*. 2nd ed.
5. Marcus, G.E. (1998). *Ethnography through Thick and Thin*. Princeton.

---

**技能版本**: 5.0.0  
**方法论标准**: Geertz解释性方法  
**创建时间**: 2026-03-15