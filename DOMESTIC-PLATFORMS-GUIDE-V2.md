# 国内 AI 平台技能加载指南

**分析日期**: 2026-03-22  
**覆盖平台**: 8 个国内主流平台  
**规范标准**: agentskills.io v1.0 + 各平台规范

---

## 🎯 平台总览

### 第一梯队（最易获得 + 本平台推荐）

| 平台 | 类型 | 获取难度 | 用户群体 | 特点 |
|------|------|---------|---------|------|
| **Stigmergy** ⭐ | 多 Agent 协同 | ⭐ 极易 | 研究者 | **本平台多智能体系统，无需自备算力** |
| **WorkBuddy** | CLI 工具 | ⭐ 极易 | 研究者、开发者 | 本地部署，兼容性好 |
| **Coze 编程** | 云端 Bot | ⭐ 极易 | 所有人 | 网页访问，无需安装 |
| **钉钉悟空** | 企业 Bot | ⭐ 极易 | 企业用户 | 钉钉内置，企业集成 |
| **Qwen** | CLI/API | ⭐ 极易 | 开发者、研究者 | 中文能力强 |

### 第二梯队（易于获得）

| 平台 | 类型 | 获取难度 | 用户群体 |
|------|------|---------|---------|
| **OpenCode** | CLI 工具 | ⭐ 易 | 开发者 |
| **KiloCode** | CLI 工具 | ⭐ 易 | 开发者 |
| **OpenClaw** | CLI 工具 | ⭐ 中 | 研究者 |

---

## 🌟 Stigmergy - 本平台多智能体系统（首推）

### 核心优势

**Stigmergy** 是 SocienceAI 平台的多智能体协同系统，具有以下独特优势：

1. **无需自备 AI 模型算力** ✅
   - 使用云端 AI 模型（通义千问、Coze 等）
   - 无需购买 GPU、无需配置本地模型
   - 按使用量付费，成本低

2. **多 Agent 协同** ✅
   - 多个专家 Agent 协同工作
   - 跨学科研究支持
   - 自动任务分配

3. **自动进化** ✅
   - Agent 间相互学习
   - 协同进化新能力
   - 持续改进

4. **npm 安装** ✅
   ```bash
   npm install -g stigmergy
   ```

5. **技能兼容** ✅
   - 支持 agentskills.io 规范
   - 兼容所有社会科学方法论技能

### 安装 Stigmergy

```bash
# npm 安装（推荐）
npm install -g stigmergy

# 验证安装
stigmergy --version
```

### 配置（无需自备算力）

```bash
# 配置使用云端 AI（默认，无需自备算力）
stigmergy config --use-cloud

# 或配置具体 AI 服务
stigmergy config --ai-provider qwen  # 通义千问
stigmergy config --ai-provider coze   # Coze
```

### 使用示例

```bash
# 加载多个专家 Agent
stigmergy load grounded-theory-expert
stigmergy load social-network-analysis-expert

# 多 Agent 协同分析
stigmergy use grounded-theory-expert,social-network-analysis-expert "
请对以下研究进行协同分析...
"
```

**详细教程**: [Stigmergy 使用教程](/tutorials/stigmergy/)

---

## 1️⃣ WorkBuddy 教程

### 平台介绍

**WorkBuddy** 是本地部署的 AI 助手 CLI 工具，完全兼容 agentskills.io 规范。

**特点**:
- ✅ 本地部署，数据安全
- ✅ 兼容 agentskills.io 规范
- ✅ 与 Stigmergy 技能通用
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

1. 创建 Bot
2. 配置人设（复制 SKILL.md 内容）
3. 添加插件（对应 tools/）
4. 上传知识库（对应 templates/）
5. 发布 Bot

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

1. 进入钉钉开放平台
2. 创建企业 Bot
3. 配置 Bot 人设
4. 添加能力
5. 发布 Bot

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

# 配置 API Key
qwen config --api-key YOUR_API_KEY

# 使用技能
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

# 加载技能
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

# 加载技能
kilocode --skill grounded-theory-expert "任务描述"
```

---

## 7️⃣ OpenClaw 教程

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

# 加载技能
openclaw --skill grounded-theory-expert "任务描述"
```

---

## 📊 平台对比

| 平台 | 获取难度 | 安装方式 | 技能格式 | 数据位置 | 算力需求 |
|------|---------|---------|---------|---------|---------|
| **Stigmergy** ⭐ | ⭐⭐⭐⭐⭐ | npm | agentskills.io | 云端 | **无需自备** |
| WorkBuddy | ⭐⭐⭐⭐⭐ | npm/pip | agentskills.io | 本地 | 需自备 |
| Coze 编程 | ⭐⭐⭐⭐⭐ | 网页 | Bot 配置 | 云端 | 无需自备 |
| 钉钉悟空 | ⭐⭐⭐⭐⭐ | 钉钉内置 | 企业 Bot | 云端 | 无需自备 |
| Qwen | ⭐⭐⭐⭐⭐ | npm/pip | agentskills.io | 云端/本地 | 可选 |
| OpenCode | ⭐⭐⭐⭐ | npm | agentskills.io | 本地 | 需自备 |
| KiloCode | ⭐⭐⭐⭐ | npm | agentskills.io | 本地 | 需自备 |
| OpenClaw | ⭐⭐⭐ | npm/pip | Soul Agent | 本地 | 需自备 |

---

## 🚀 快速选择指南

### 根据需求选择

**研究者首选**:
1. **Stigmergy** ⭐ - 多 Agent 协同，无需自备算力
2. WorkBuddy - 研究者友好，本地部署
3. OpenClaw - 社会科学友好

**企业用户首选**:
1. 钉钉悟空 - 企业集成
2. Coze 编程 - 快速部署
3. Qwen - 企业 API

**开发者首选**:
1. OpenCode - 开源编程
2. KiloCode - 轻量快速
3. Qwen - API 友好

### 根据算力需求选择

**无需自备算力**:
- **Stigmergy** ⭐ - 云端 AI，多 Agent 协同
- Coze 编程 - 云端 Bot
- 钉钉悟空 - 云端服务
- Qwen - 云端 API

**本地部署**（需自备算力）:
- WorkBuddy
- OpenCode
- KiloCode
- OpenClaw

---

## 📖 相关资源

### 平台文档

- [Stigmergy 文档](https://github.com/stigmergy/stigmergy)
- [WorkBuddy 文档](https://github.com/workbuddy/workbuddy)
- [Coze 文档](https://www.coze.cn/docs)
- [Qwen 文档](https://help.aliyun.com/product/42154.html)

### 技能仓库

- [SocienceAI 技能仓库](https://github.com/socienceai/agentskills)
- [技能包下载](https://github.com/socienceai/agentskills/archive/main.zip)

### 教程

- [Stigmergy 教程](/tutorials/stigmergy/)
- [WorkBuddy 教程](/tutorials/workbuddy/)
- [Coze 教程](/tutorials/coze/)
- [Qwen 教程](/tutorials/qwen/)

---

**分析完成日期**: 2026-03-22  
**分析师**: SocienceAI Team  
**覆盖平台**: 8 个国内主流平台  
**首推平台**: Stigmergy（本平台多智能体系统）

*让社会科学研究人人可为*
