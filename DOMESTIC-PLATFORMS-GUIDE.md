# 国内 AI 平台技能加载指南

**分析日期**: 2026-03-22  
**覆盖平台**: 8 个国内主流 AI 平台  
**规范标准**: agentskills.io v1.0 + 各平台规范

---

## 🎯 平台总览

### 第一梯队（最易获得）

| 平台 | 类型 | 获取难度 | 用户群体 |
|------|------|---------|---------|
| **WorkBuddy** | CLI 工具 | ⭐ 极易 | 研究者、开发者 |
| **Coze 编程** | 云端 Bot | ⭐ 极易 | 所有人 |
| **钉钉悟空** | 企业 Bot | ⭐ 极易 | 企业用户 |
| **Qwen** | CLI/API | ⭐ 极易 | 开发者、研究者 |
| **OpenCode** | CLI 工具 | ⭐ 易 | 开发者 |
| **KiloCode** | CLI 工具 | ⭐ 易 | 开发者 |
| **Stigmergy** | 协同框架 | ⭐ 中 | 研究者 |
| **OpenClaw** | CLI 工具 | ⭐ 中 | 研究者 |

---

## 📦 技能包结构（通用）

```
skill-package/
├── SKILL.md              # 技能定义（通用）
├── skill.yaml            # 技能配置（通用）
├── tools/                # 工具模块（通用）
├── templates/            # 模板文件（通用）
├── adapters/             # 平台适配器
│   ├── workbuddy/
│   ├── coze/
│   ├── dingtalk/
│   ├── qwen/
│   ├── opencode/
│   ├── kilocode/
│   ├── stigmergy/
│   └── openclaw/
└── README.md             # 使用说明
```

---

## 1️⃣ WorkBuddy 教程

### 平台介绍

**WorkBuddy** 是本地部署的 AI 助手 CLI 工具，完全兼容 agentskills.io 规范。

**特点**:
- ✅ 本地部署，数据安全
- ✅ 兼容 agentskills.io 规范
- ✅ 与 OpenClaw 技能通用
- ✅ 中文支持好

### 安装 WorkBuddy

```bash
# 方式 1: npm 安装
npm install -g workbuddy

# 方式 2: pip 安装
pip install workbuddy-cli

# 验证安装
workbuddy --version
```

### 加载技能

**方式 1: 复制到技能目录**:
```bash
# 创建技能目录
mkdir -p ~/.workbuddy/skills

# 复制技能
cp -r grounded-theory-expert ~/.workbuddy/skills/
```

**方式 2: 配置文件**:
```yaml
# ~/.workbuddy/config.yaml
skill_paths:
  - ~/.workbuddy/skills
  - /path/to/agentskills
```

**方式 3: 命令行指定**:
```bash
workbuddy --skill /path/to/grounded-theory-expert "任务描述"
```

### 使用示例

```bash
# 加载技能
workbuddy --skill grounded-theory-expert

# 输入任务
请对以下访谈数据进行开放编码：

"我觉得工作压力很大，每天都要加班，
但是没有明确的晋升通道，感觉很迷茫。"
```

---

## 2️⃣ Coze 编程教程

### 平台介绍

**Coze 编程**是字节跳动推出的 AI 编程助手，支持技能/插件导入。

**特点**:
- ✅ 无需部署，开箱即用
- ✅ 可视化配置
- ✅ 支持插件扩展
- ✅ 免费使用

### 注册 Coze

1. 访问 https://www.coze.cn/
2. 点击"登录/注册"
3. 使用抖音/头条/邮箱注册

### 导入技能

**方式 1: Bot 配置导入**:

1. 创建 Bot
2. 配置人设（复制 SKILL.md 内容）
3. 添加插件（对应 tools/）
4. 上传知识库（对应 templates/）
5. 发布 Bot

**方式 2: 工作流导入**:

1. 创建工作流
2. 配置节点（对应技能工作流程）
3. 测试工作流
4. 发布工作流

### 技能转换

**SKILL.md → Coze 人设**:
```markdown
# SKILL.md 内容
---
name: grounded-theory-expert
description: 扎根理论分析专家
---

# 角色
你是扎根理论分析专家...

# Coze 人设配置
角色：扎根理论分析专家
简介：专注于质性数据分析的 AI 助手
功能：开放编码、轴心编码、选择式编码
```

**tools/ → Coze 插件**:
```
扎根理论工具 → 文本分析插件
编码工具 → 数据处理插件
模板工具 → 文档生成插件
```

---

## 3️⃣ 钉钉悟空教程

### 平台介绍

**钉钉悟空**是阿里巴巴推出的企业级 AI 助手，集成在钉钉中。

**特点**:
- ✅ 企业用户直接可用
- ✅ 集成钉钉生态
- ✅ 支持企业定制
- ✅ 数据安全

### 访问悟空

1. 打开钉钉
2. 搜索"悟空助手"
3. 添加到工作台

### 加载技能

**方式 1: 企业 Bot 配置**:

1. 进入钉钉开放平台
2. 创建企业 Bot
3. 配置 Bot 人设（复制 SKILL.md）
4. 添加能力（对应 tools/）
5. 发布 Bot

**方式 2: 钉钉应用市场**:

1. 访问钉钉应用市场
2. 搜索"AI 助手"
3. 安装应用
4. 配置使用

### 企业定制

**配置企业知识库**:
```
1. 准备企业文档
2. 上传到悟空知识库
3. 配置知识检索
4. 测试效果
```

---

## 4️⃣ Qwen 教程

### 平台介绍

**Qwen** 是阿里云推出的通义千问系列，包括 CLI 和 API。

**特点**:
- ✅ 中文能力强
- ✅ 支持 CLI 和 API
- ✅ 技能兼容性好
- ✅ 免费额度

### 安装 Qwen CLI

```bash
# npm 安装
npm install -g qwen-cli

# 或 pip 安装
pip install qwen-cli

# 验证安装
qwen --version
```

### 配置 Qwen

**获取 API Key**:
1. 访问 https://dashscope.console.aliyun.com/
2. 登录/注册阿里云账号
3. 创建 API Key
4. 复制保存

**配置 CLI**:
```bash
# 配置 API Key
qwen config --api-key YOUR_API_KEY

# 或编辑配置文件
# ~/.qwen/config.yaml
api_key: YOUR_API_KEY
```

### 加载技能

**方式 1: 技能目录**:
```bash
# 创建技能目录
mkdir -p ~/.qwen/skills

# 复制技能
cp -r grounded-theory-expert ~/.qwen/skills/
```

**方式 2: 项目级别**:
```bash
# 在项目目录创建.qwen/skills/
mkdir -p .qwen/skills
cp -r grounded-theory-expert .qwen/skills/
```

### 使用技能

```bash
# 自动加载
qwen "使用扎根理论分析以下访谈数据..."

# 手动指定
qwen --skill grounded-theory-expert "任务描述"
```

---

## 5️⃣ OpenCode 教程

### 平台介绍

**OpenCode** 是开源的 AI 编程助手 CLI 工具。

**特点**:
- ✅ 开源免费
- ✅ 兼容 agentskills.io
- ✅ 社区活跃
- ✅ 跨平台

### 安装 OpenCode

```bash
# npm 安装
npm install -g opencode-cli

# 或从 GitHub 下载
git clone https://github.com/opencode/opencode.git
cd opencode
npm install
```

### 加载技能

```bash
# 创建技能目录
mkdir -p ~/.opencode/skills

# 复制技能
cp -r grounded-theory-expert ~/.opencode/skills/

# 使用技能
opencode --skill grounded-theory-expert "任务描述"
```

---

## 6️⃣ KiloCode 教程

### 平台介绍

**KiloCode** 是轻量级 AI 编程助手。

**特点**:
- ✅ 轻量快速
- ✅ 支持技能扩展
- ✅ 免费使用
- ✅ 中文支持

### 安装 KiloCode

```bash
# npm 安装
npm install -g kilocode

# 验证安装
kilocode --version
```

### 加载技能

```bash
# 创建技能目录
mkdir -p ~/.kilocode/skills

# 复制技能
cp -r grounded-theory-expert ~/.kilocode/skills/

# 使用技能
kilocode --skill grounded-theory-expert "任务描述"
```

---

## 7️⃣ Stigmergy 教程

### 平台介绍

**Stigmergy** 是协同智能体框架，支持多 Agent 协作。

**特点**:
- ✅ 多 Agent 协同
- ✅ 支持技能共享
- ✅ 研究者友好
- ✅ 开源

### 安装 Stigmergy

```bash
# pip 安装
pip install stigmergy

# 或从 GitHub 下载
git clone https://github.com/stigmergy/stigmergy.git
cd stigmergy
pip install -e .
```

### 配置 Stigmergy

```bash
# 初始化配置
stigmergy init

# 配置技能路径
stigmergy config --skill-path /path/to/agentskills
```

### 加载技能

```bash
# 加载技能
stigmergy load grounded-theory-expert

# 使用技能
stigmergy use grounded-theory-expert "任务描述"

# 多 Agent 协同
stigmergy use grounded-theory-expert,sna-expert "任务描述"
```

---

## 8️⃣ OpenClaw 教程

### 平台介绍

**OpenClaw**（小龙虾）是本地部署的 AI 智能体 CLI 工具。

**特点**:
- ✅ 本地部署，数据安全
- ✅ Soul Agent 规范
- ✅ 社会科学友好
- ✅ 开源免费

### 安装 OpenClaw

```bash
# npm 安装
npm install -g openclaw

# 或 pip 安装
pip install openclaw

# 验证安装
openclaw --version
```

### 加载技能

```bash
# 创建技能目录
mkdir -p ~/.openclaw/skills

# 复制技能
cp -r grounded-theory-expert ~/.openclaw/skills/

# 使用技能
openclaw --skill grounded-theory-expert "任务描述"
```

---

## 📊 平台对比

| 平台 | 获取难度 | 安装方式 | 技能格式 | 数据位置 |
|------|---------|---------|---------|---------|
| WorkBuddy | ⭐⭐⭐⭐⭐ | npm/pip | agentskills.io | 本地 |
| Coze 编程 | ⭐⭐⭐⭐⭐ | 网页 | Bot 配置 | 云端 |
| 钉钉悟空 | ⭐⭐⭐⭐⭐ | 钉钉内置 | 企业 Bot | 云端 |
| Qwen | ⭐⭐⭐⭐⭐ | npm/pip | agentskills.io | 云端/本地 |
| OpenCode | ⭐⭐⭐⭐ | npm | agentskills.io | 本地 |
| KiloCode | ⭐⭐⭐⭐ | npm | agentskills.io | 本地 |
| Stigmergy | ⭐⭐⭐ | pip | 协同框架 | 本地 |
| OpenClaw | ⭐⭐⭐ | npm/pip | Soul Agent | 本地 |

---

## 🚀 快速选择指南

### 根据需求选择

**研究者首选**:
1. WorkBuddy - 研究者友好
2. OpenClaw - 社会科学友好
3. Stigmergy - 多 Agent 协同

**企业用户首选**:
1. 钉钉悟空 - 企业集成
2. Coze 编程 - 快速部署
3. Qwen - 企业 API

**开发者首选**:
1. OpenCode - 开源编程
2. KiloCode - 轻量快速
3. Qwen - API 友好

### 根据数据敏感性选择

**数据不出本地**:
- WorkBuddy
- OpenClaw
- OpenCode
- KiloCode
- Stigmergy

**可接受云端**:
- Coze 编程
- 钉钉悟空
- Qwen（云端模式）

---

## 📚 技能分发策略

### GitHub 统一分发

```
仓库：github.com/socienceai/agentskills

下载方式:
1. Git 克隆
   git clone https://github.com/socienceai/agentskills.git

2. 下载 ZIP
   访问 GitHub → Code → Download ZIP

3. 单个技能下载
   git clone https://github.com/socienceai/agentskills.git grounded-theory-expert
```

### 平台技能市场

**已上架**:
- WorkBuddy 技能市场
- OpenClaw 技能市场
- OpenCode 技能市场

**计划上架**:
- Coze 技能商店
- 钉钉悟空应用市场
- Qwen 技能中心

---

## ❓ 常见问题

### Q: 哪个平台最容易获得？

**A**: 
1. **Coze 编程** - 网页访问，无需安装
2. **钉钉悟空** - 钉钉内置，企业用户直接可用
3. **WorkBuddy** - npm/pip 一键安装
4. **Qwen** - npm/pip 一键安装

### Q: 技能可以在多个平台使用吗？

**A**: 是的！我们的技能遵循 agentskills.io 规范，通过平台适配器可以在所有 8 个平台使用。

### Q: 如何选择平台？

**A**: 
- 研究者：WorkBuddy、OpenClaw
- 企业用户：钉钉悟空、Coze
- 开发者：OpenCode、KiloCode、Qwen
- 多 Agent：Stigmergy

### Q: 数据安全性如何？

**A**: 
- 本地部署平台（WorkBuddy、OpenClaw 等）：数据不出本地
- 云端平台（Coze、钉钉悟空）：数据在云端，遵循平台隐私政策

---

**分析完成日期**: 2026-03-22  
**分析师**: SocienceAI Team  
**覆盖平台**: 8 个国内主流平台

*让社会科学研究人人可为*
