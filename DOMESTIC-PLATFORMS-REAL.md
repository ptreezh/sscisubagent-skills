# 国内 AI 平台技能加载指南（真实版）

**分析日期**: 2026-03-22  
**覆盖平台**: 8 个国内主流平台  
**规范标准**: agentskills.io v1.0

---

## 🎯 平台总览

### 第一梯队（最易获得）

| 平台 | 类型 | 获取难度 | 用户群体 | 算力需求 |
|------|------|---------|---------|---------|
| **Coze 编程** | 云端 Bot | ⭐ 极易 | 所有人 | 云端（免费） |
| **钉钉悟空** | 企业 Bot | ⭐ 极易 | 企业用户 | 云端（免费） |
| **WorkBuddy** | CLI 工具 | ⭐ 极易 | 研究者、开发者 | 需自备 |
| **Qwen** | CLI/API | ⭐ 极易 | 开发者、研究者 | 需自备 |
| **Stigmergy** | CLI 协调器 | ⭐ 极易 | 研究者 | 需自备 AI CLI |

### 第二梯队（易于获得）

| 平台 | 类型 | 获取难度 | 用户群体 | 算力需求 |
|------|------|---------|---------|---------|
| **OpenCode** | CLI 工具 | ⭐ 易 | 开发者 | 需自备 |
| **KiloCode** | CLI 工具 | ⭐ 易 | 开发者 | 需自备 |
| **OpenClaw** | CLI 工具 | ⭐ 中 | 研究者 | 需自备 |

---

## ⚠️ Stigmergy 重要说明

**Stigmergy 是什么**:
- ✅ **多 AI CLI 工具协同系统** - 协调 Claude、Gemini、Qwen 等 9+ 种 AI CLI 工具
- ✅ **技能管理器** - 技能安装一次，所有 AI CLI 通用
- ✅ **跨 CLI 通信** - 实现不同 AI CLI 工具之间的协作

**Stigmergy 不是什么**:
- ❌ **不是 AI 模型** - 不提供 AI 模型
- ❌ **不是 SocienceAI 的子项目** - 是独立开源项目（GitHub: ptreezh/stigmergy-CLI-Multi-Agents）
- ❌ **不"无需自备算力"** - 用户需要有自己的 AI CLI 工具和 API Key

**正确使用 Stigmergy**:
```bash
# 1. 先安装至少一个 AI CLI 工具
npm install -g @anthropic-ai/claude-cli  # 需要 Claude API Key
npm install -g gemini-cli                # 需要 Gemini API Key
npm install -g qwen-cli                  # 需要阿里云 API Key

# 2. 安装 Stigmergy
npm install -g stigmergy@beta

# 3. 安装 SocienceAI 技能
stigmergy skill install socienceai/agentskills

# 4. 使用技能（需要有自己的 AI CLI 工具）
stigmergy qwen --skill grounded-theory-expert "分析访谈数据"
```

**详细教程**: [Stigmergy 真实使用教程](/tutorials/stigmergy-real/)

---

## 1️⃣ Coze 编程教程（首推 - 免费）

### 平台介绍

**Coze 编程**是字节跳动推出的 AI 编程助手，支持技能/插件导入。

**特点**:
- ✅ 无需部署，开箱即用
- ✅ 可视化配置
- ✅ 支持插件扩展
- ✅ **免费使用**（有免费额度）

### 注册 Coze

1. 访问 https://www.coze.cn/
2. 点击"登录/注册"
3. 使用抖音/头条/邮箱注册

### 导入技能

1. 创建 Bot
2. 配置人设（复制 SKILL.md 内容）
3. 添加插件（对应 tools/）
4. 上传知识库（对应 templates/）
5. 发布 Bot

---

## 2️⃣ 钉钉悟空教程（首推 - 企业免费）

### 平台介绍

**钉钉悟空**是阿里巴巴推出的企业级 AI 助手，集成在钉钉中。

**特点**:
- ✅ 企业用户直接可用
- ✅ 集成钉钉生态
- ✅ 支持企业定制
- ✅ **免费使用**（企业版）

### 访问悟空

1. 打开钉钉
2. 搜索"悟空助手"
3. 添加到工作台

### 加载技能

1. 进入钉钉开放平台
2. 创建企业 Bot
3. 配置 Bot 人设
4. 添加能力
5. 发布 Bot

---

## 3️⃣ WorkBuddy 教程

### 平台介绍

**WorkBuddy** 是本地部署的 AI 助手 CLI 工具，完全兼容 agentskills.io 规范。

**特点**:
- ✅ 本地部署，数据安全
- ✅ 兼容 agentskills.io 规范
- ✅ 中文支持好

### 安装 WorkBuddy

```bash
# npm 安装
npm install -g workbuddy

# 或 pip 安装
pip install workbuddy-cli

# 验证安装
workbuddy --version
```

### 加载技能

```bash
# 创建技能目录
mkdir -p ~/.workbuddy/skills

# 复制技能
cp -r grounded-theory-expert ~/.workbuddy/skills/

# 使用技能
workbuddy --skill grounded-theory-expert "任务描述"
```

---

## 4️⃣ Qwen 教程

### 平台介绍

**Qwen** 是阿里云推出的通义千问系列，包括 CLI 和 API。

**特点**:
- ✅ 中文能力强
- ✅ 支持 CLI 和 API
- ✅ 技能兼容性好
- ✅ **有免费额度**

### 安装 Qwen CLI

```bash
# npm 安装
npm install -g qwen-cli

# 配置 API Key（有免费额度）
qwen config --api-key YOUR_API_KEY

# 使用技能
qwen --skill grounded-theory-expert "任务描述"
```

---

## 5️⃣ Stigmergy 教程

### 平台介绍

**Stigmergy** 是多 AI CLI 工具协同系统，协调 Claude、Gemini、Qwen 等 9+ 种 AI CLI 工具。

**特点**:
- ✅ 技能安装一次，所有 AI CLI 通用
- ✅ 跨 CLI 通信
- ✅ 智能任务路由
- ⚠️ **需要自备 AI CLI 工具和 API Key**

### 安装 Stigmergy

```bash
# 安装 Stigmergy
npm install -g stigmergy@beta

# 验证安装
stigmergy --version
```

### 前置要求

使用 Stigmergy 前，需要先安装至少一个 AI CLI 工具：
- claude-cli（需要 Claude API Key）
- gemini-cli（需要 Gemini API Key）
- qwen-cli（需要阿里云 API Key）

### 加载技能

```bash
# 安装 SocienceAI 技能
stigmergy skill install socienceai/agentskills

# 使用技能（需要有自己的 AI CLI 工具）
stigmergy qwen --skill grounded-theory-expert "任务描述"
```

**详细教程**: [Stigmergy 真实使用教程](/tutorials/stigmergy-real/)

---

## 6️⃣ OpenCode 教程

### 平台介绍

**OpenCode** 是开源的 AI 编程助手 CLI 工具。

**特点**:
- ✅ 开源免费
- ✅ 兼容 agentskills.io
- ✅ 社区活跃

### 安装 OpenCode

```bash
# npm 安装
npm install -g opencode-cli

# 加载技能
opencode --skill grounded-theory-expert "任务描述"
```

---

## 7️⃣ KiloCode 教程

### 平台介绍

**KiloCode** 是轻量级 AI 编程助手。

**特点**:
- ✅ 轻量快速
- ✅ 支持技能扩展
- ✅ 免费使用

### 安装 KiloCode

```bash
# npm 安装
npm install -g kilocode

# 加载技能
kilocode --skill grounded-theory-expert "任务描述"
```

---

## 8️⃣ OpenClaw 教程

### 平台介绍

**OpenClaw**（小龙虾）是本地部署的 AI 智能体 CLI 工具。

**特点**:
- ✅ 本地部署，数据安全
- ✅ Soul Agent 规范
- ✅ 社会科学友好

### 安装 OpenClaw

```bash
# npm 安装
npm install -g openclaw

# 加载技能
openclaw --skill grounded-theory-expert "任务描述"
```

---

## 📊 平台对比（真实版）

| 平台 | 获取难度 | 安装方式 | 技能格式 | 数据位置 | 算力需求 | 免费额度 |
|------|---------|---------|---------|---------|---------|---------|
| **Coze 编程** | ⭐⭐⭐⭐⭐ | 网页 | Bot 配置 | 云端 | 云端 | ✅ 有 |
| **钉钉悟空** | ⭐⭐⭐⭐⭐ | 钉钉内置 | 企业 Bot | 云端 | 云端 | ✅ 企业免费 |
| **WorkBuddy** | ⭐⭐⭐⭐⭐ | npm/pip | agentskills.io | 本地 | 需自备 | ❌ |
| **Qwen** | ⭐⭐⭐⭐⭐ | npm/pip | agentskills.io | 云端/本地 | 需自备 | ✅ 有 |
| **Stigmergy** | ⭐⭐⭐⭐ | npm | agentskills.io | 本地 | 需自备 AI CLI | ❌ |
| **OpenCode** | ⭐⭐⭐⭐ | npm | agentskills.io | 本地 | 需自备 | ❌ |
| **KiloCode** | ⭐⭐⭐⭐ | npm | agentskills.io | 本地 | 需自备 | ❌ |
| **OpenClaw** | ⭐⭐⭐ | npm/pip | Soul Agent | 本地 | 需自备 | ❌ |

---

## 🚀 快速选择指南

### 根据算力需求选择

**无需自备算力（免费额度）**:
- **Coze 编程** ⭐⭐⭐⭐⭐ - 网页访问，免费额度
- **钉钉悟空** ⭐⭐⭐⭐⭐ - 企业用户，免费使用
- **Qwen** ⭐⭐⭐⭐⭐ - 有免费 API 额度

**需要自备算力**:
- WorkBuddy - 本地部署
- OpenCode - 本地部署
- KiloCode - 本地部署
- OpenClaw - 本地部署
- Stigmergy - 需要自备 AI CLI 工具

### 根据使用场景选择

**企业用户**:
1. 钉钉悟空 - 企业集成
2. Coze 编程 - 快速部署
3. Qwen - 企业 API

**研究者**:
1. WorkBuddy - 研究者友好
2. OpenClaw - 社会科学友好
3. Stigmergy - 多 CLI 协同（需自备 AI CLI）

**开发者**:
1. OpenCode - 开源编程
2. KiloCode - 轻量快速
3. Qwen - API 友好

---

## 📖 相关资源

### 平台文档

- [Coze 文档](https://www.coze.cn/docs)
- [钉钉悟空文档](https://open.dingtalk.com/document/)
- [WorkBuddy 文档](https://github.com/workbuddy/workbuddy)
- [Qwen 文档](https://help.aliyun.com/product/42154.html)
- [Stigmergy 文档](https://github.com/ptreezh/stigmergy-CLI-Multi-Agents)
- [OpenCode 文档](https://github.com/opencode/opencode)
- [KiloCode 文档](https://github.com/kilocode/kilocode)
- [OpenClaw 文档](https://github.com/openclaw/openclaw)

### 技能仓库

- [SocienceAI 技能仓库](https://github.com/socienceai/agentskills)
- [技能包下载](https://github.com/socienceai/agentskills/archive/main.zip)

### 教程

- [Coze 教程](/tutorials/coze/)
- [钉钉悟空教程](/tutorials/dingtalk/)
- [WorkBuddy 教程](/tutorials/workbuddy/)
- [Qwen 教程](/tutorials/qwen/)
- [Stigmergy 真实教程](/tutorials/stigmergy-real/)
- [OpenCode 教程](/tutorials/opencode/)
- [KiloCode 教程](/tutorials/kilocode/)
- [OpenClaw 教程](/tutorials/openclaw/)

---

**分析完成日期**: 2026-03-22  
**分析师**: SocienceAI Team  
**覆盖平台**: 8 个国内主流平台  
**首推平台**: Coze 编程、钉钉悟空、Qwen（有免费额度）

*基于事实，纠正错误认知*
