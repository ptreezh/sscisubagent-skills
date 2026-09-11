# Soul Agent Creator - 灵魂分身创建专家

> 通过自然语言对话创建社会科学方法论专家分身

**版本**: 1.0.0
**作者**: SocienceAI
**许可**: MIT

---

## 📋 概述

**Soul Agent Creator** 是一个专门的 skill，用于通过自然语言对话帮助用户创建自己的社会科学方法论专家分身。

### 核心能力

- ✅ **需求澄清** - 通过对话了解用户的研究领域、方法论偏好、使用场景
- ✅ **技能匹配** - 推荐最适合的方法论技能（10+ 种可选）
- ✅ **配置生成** - 自动生成 SOUL.md、SOUL_CONFIG.yaml、METHODOLOGY.md
- ✅ **目录创建** - 建立完整的分身目录结构（记忆、案例、进化日志）
- ✅ **个性化定制** - 支持自定义分身名称、对话风格、输出偏好

### 支持的创建方式

| 方式 | 描述 | 适用场景 |
|------|------|---------|
| 直接创建 | 用户明确知道要创建什么 | "我想创建一个扎根理论分身" |
| 探索式创建 | 用户需要推荐和引导 | "我是管理学研究生，需要什么方法？" |
| 快速创建 | 用户使用默认配置 | "帮我快速创建一个 SNA 分身" |

---

## 🚀 快速开始

### 方式 1: 在 CLI 中使用

```bash
# 启动 CLI
qwen

# 直接表达需求
"我想创建一个扎根理论的分身，用于分析访谈数据"
```

### 方式 2: 使用 Stigmergy 调用

```bash
stigmergy use qwen skill soul-agent-creator "帮我创建一个社会网络分析分身"
```

### 方式 3: 作为技能自动触发

当用户输入包含以下关键词时，自动触发：
- "创建分身"
- "定制方法论"
- "Soul Agent"
- "学术 AI 助手"

---

## 📖 使用示例

### 示例 1: 直接创建

**用户**: 我想创建一个扎根理论的分身，用于分析访谈数据

**Soul Agent Creator**:
```
好的！我来帮你创建一个扎根理论专家分身。

在开始之前，我需要了解几个问题：

1. 自定义名称：你希望分身叫什么名字？（默认："扎根理论专家"）
2. 对标学者：你更倾向于哪位学者的方法？
   - Kathy Charmaz（建构主义扎根理论）
   - Strauss & Corbin（程序化扎根理论）
   - Glaser & Strauss（经典扎根理论）
3. 主要用途：除了访谈数据分析，还需要其他功能吗？
   - 文献综述
   - 理论建构
   - 论文写作辅助

请告诉我你的偏好，我将为你定制专属分身！
```

### 示例 2: 探索式创建

**用户**: 我是管理学研究生，想定制一个方法论 AI 助手，但不知道有哪些选择

**Soul Agent Creator**:
```
欢迎！我来帮你选择最适合的方法论分身。

作为管理学研究生，你可能研究方向包括：
- 组织行为/人力资源 → 适合质性方法（扎根理论、现象学）
- 战略管理/创新研究 → 适合混合方法或社会网络分析
- 市场营销/消费者行为 → 适合质性方法（内容分析、叙事分析）

请告诉我：
1. 你的具体研究方向是什么？
2. 你主要收集什么类型的数据？（访谈/问卷/二手数据/观察）
3. 你希望分身帮你解决什么问题？（数据分析/方法学习/论文写作）

根据你的回答，我会推荐最合适的方法论分身！
```

### 示例 3: 快速创建

**用户**: 帮我快速创建一个社会网络分析分身，默认配置就行

**Soul Agent Creator**:
```
好的！我将为你创建一个社会网络分析分身，使用默认配置：

- 分身名称：社会网络分析专家
- 对标学者：Linton Freeman / Stanley Wasserman
- 核心能力：中心性分析、社区检测、结构洞分析
- 对话风格：学术严谨
- 存储位置：~/.stigmergy/soul-agents/soul_sna_20260322/

确认创建？(回复"确认"或"y"即可)
```

---

## 🎯 支持的方法论技能

### 📖 质性研究方法

| 技能 ID | 名称 | 对标学者 | 核心概念 |
|--------|------|---------|---------|
| grounded-theory | 扎根理论专家 | Kathy Charmaz | 开放编码/轴心编码/选择式编码 |
| actor-network-theory | 行动者网络理论专家 | Bruno Latour | 行动者识别/转译过程/网络稳定化 |
| bourdieu-field-analysis | 布迪厄场域分析专家 | Pierre Bourdieu | 场域/资本/习性 |

### 📊 定量研究方法

| 技能 ID | 名称 | 对标学者 | 核心概念 |
|--------|------|---------|---------|
| social-network-analysis | 社会网络分析专家 | Linton Freeman | 中心性/社区检测/结构洞 |
| qca-analysis | 定性比较分析专家 | Charles Ragin | 模糊集校准/真值表/布尔最小化 |
| did-analysis | 双重差分分析专家 | Angrist & Pischke | 平行趋势/双向固定效应 |
| regression-analysis | 回归分析专家 | Ronald Fisher | OLS 估计/假设检验/模型诊断 |
| survey-design | 问卷设计专家 | Don A. Dillman | 问题设计/抽样方法/信效度 |

### 🔄 混合研究方法

| 技能 ID | 名称 | 对标学者 | 核心概念 |
|--------|------|---------|---------|
| mixed-methods | 混合方法研究专家 | John Creswell | 三角验证/互补设计/转换整合 |

### 🧠 社会理论视角

| 技能 ID | 名称 | 对标学者 | 核心概念 |
|--------|------|---------|---------|
| digital-marxism | 数字马克思分析专家 | David Harvey | 数字劳动/剩余价值/意识形态批判 |
| digital-durkheim | 数字涂尔干分析专家 | Émile Durkheim | 集体意识/社会团结/神圣世俗 |
| digital-weber | 数字韦伯分析专家 | Max Weber | 理性化/科层制/祛魅 |

---

## 📁 生成的文件结构

创建完成后，会在 `~/.stigmergy/soul-agents/[soul_id]/` 生成以下结构：

```
[soul_id]/
├── SOUL.md              # 灵魂身份定义（角色、价值观、工作方式）
├── SOUL_CONFIG.yaml     # 运行时配置（对话风格、质量控制、进化设置）
├── METHODOLOGY.md       # 方法论详解（学派、概念、操作步骤）
├── README.md            # 使用说明
├── metadata.json        # 元数据
├── memory/
│   ├── lessons/         # 教训记忆
│   │   └── README.md    # 教训记录模板
│   └── patterns/        # 成功模式
│       └── README.md    # 模式记录模板
├── evolution/           # 进化记录
│   └── log.md           # 进化日志
├── cases/
│   ├── positive/        # 正面案例
│   └── negative/        # 负面案例
├── templates/           # 工作模板
├── logs/               # 日志
├── data/               # 数据
└── results/            # 结果
```

---

## 🔧 工具模块

### list_skills

列出所有可用的方法论技能。

```python
from tools import list_skills

# 列出所有技能
skills = list_skills.list_all()

# 按类别列出
qualitative = list_skills.list_by_category("qualitative")

# 获取单个技能
gt = list_skills.get_skill("grounded-theory")

# 格式化显示
print(list_skills.format_display())
```

### generate_soul_config

生成 Soul Agent 配置文件。

```python
from tools import generate_soul_config

# 创建分身
result = generate_soul_config.create(
    skill_id="grounded-theory",
    custom_name="我的扎根理论助手",
    output_dir="~/.stigmergy/soul-agents/",
    verbose=True
)

print(f"Soul ID: {result['soul_id']}")
print(f"路径：{result['output_dir']}")
```

---

## ✅ 质量保证

每次创建完成后，自动执行以下检查：

- [ ] SOUL.md 文件存在且包含完整角色定义
- [ ] SOUL_CONFIG.yaml 文件存在且 YAML 格式有效
- [ ] METHODOLOGY.md 文件存在且包含方法论详解
- [ ] 目录结构完整（memory/、evolution/、cases/等）
- [ ] metadata.json 包含正确的元数据
- [ ] README.md 包含清晰的激活说明

---

## ⚠️ 禁忌事项

以下行为严格禁止：

❌ **禁止**在用户未确认配置前直接生成分身
❌ **禁止**推荐用户未提及的方法论技能（除非用户明确要求推荐）
❌ **禁止**使用过于技术化的术语（除非用户显示熟悉）
❌ **禁止**忽略用户的个性化需求（必须支持定制）
❌ **禁止**创建后不提供激活说明

---

## 🚀 激活分身

创建完成后，有 3 种方式激活分身：

### 方式 1: 环境变量

```bash
export SOUL_AGENT_ID="soul_groundedtheory_20260322"
```

### 方式 2: 直接指定配置

```bash
opencode --soul-config ~/.stigmergy/soul-agents/soul_groundedtheory_20260322/SOUL.md
```

### 方式 3: Stigmergy 调用

```bash
stigmergy use soul soul_groundedtheory_20260322
```

---

## 📚 相关文档

- [SKILL.md](SKILL.md) - 完整的角色定义和工作流程
- [skill.yaml](skill.yaml) - 配置和工具定义
- [templates/](templates/) - 模板文件
- [tools/](tools/) - 工具模块

---

## 🔄 更新日志

### v1.0.0 (2026-03-22)

- ✅ 初始版本发布
- ✅ 支持 12 种方法论技能
- ✅ 完整的对话引导流程
- ✅ 自动生成配置文件
- ✅ 完整的目录结构创建

---

## 📞 支持和反馈

**项目位置**: `D:\socienceAI\agentskills\soul-agent-creator\`

**问题反馈**: 请提交 issue 或直接联系 SocienceAI 团队

---

*由 SocienceAI Soul Agent System 提供支持*
