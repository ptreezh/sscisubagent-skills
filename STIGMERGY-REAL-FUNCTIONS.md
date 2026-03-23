# Stigmergy 真实功能分析报告

**分析日期**: 2026-03-22  
**信息来源**: npm + GitHub README  
**版本**: stigmergy@1.10.10-beta.5

---

## 🎯 Stigmergy 是什么？

**Stigmergy CLI** 是一个**多 AI CLI 工具协同系统**，不是 AI 模型本身，而是 AI CLI 工具之间的协调层。

**核心定位**:
- ✅ **AI CLI 工具协调器** - 协调 Claude、Gemini、Qwen 等 9+ 种 AI CLI 工具
- ✅ **技能管理器** - 从 GitHub 安装和管理技能，技能安装一次，所有 AI CLI 通用
- ✅ **跨 CLI 通信** - 实现不同 AI CLI 工具之间的无缝协作
- ✅ **智能任务路由** - 自动选择最适合的 AI 工具处理任务
- ✅ **会话恢复** - 跨 CLI 会话恢复和记忆共享

**重要澄清**:
- ❌ **Stigmergy 不是 AI 模型** - 它不提供 AI 模型
- ❌ **Stigmergy 不是 SocienceAI 的子项目** - 它是独立的开源项目
- ❌ **Stigmergy 需要自备 AI 算力** - 用户需要有自己的 AI CLI 工具（Claude、Gemini、Qwen 等）

---

## 📦 安装方法

```bash
# 从 npm 安装（最新 Beta 版）
npm install -g stigmergy@beta

# Windows（PowerShell 管理员）
npm install -g stigmergy@beta

# macOS/Linux
sudo npm install -g stigmergy@beta

# 验证安装
stigmergy --version
stigmergy --help
```

**前置要求**: Node.js >= 16.0.0

---

## 🔧 核心功能

### 1. 多 AI CLI 支持

支持 9+ 种 AI CLI 工具：
- claude-cli
- gemini-cli
- qwen-cli
- iflow-cli
- qoder-cli
- codebuddy-cli
- copilot-cli
- codex-cli
- kilocode-cli

### 2. 智能任务路由

```bash
# 使用特定 AI 工具
stigmergy claude "write a Python function"
stigmergy gemini "translate this text"
stigmergy qwen "analyze this code"

# 智能路由（自动选择最佳工具）
stigmergy call "create a React component"
```

### 3. 技能管理器

```bash
# 从 GitHub 安装技能
stigmergy skill install vercel-labs/agent-skills
stigmergy skill install anthropics/skills
stigmergy skill install owner/repo

# 管理技能
stigmergy skill list      # 列出所有技能
stigmergy skill read pdf  # 读取技能内容
stigmergy skill remove pdf # 删除技能
```

**技能存储位置**（优先级顺序）:
1. `~/.stigmergy/skills/` - Stigmergy 统一存储
2. `./.agent/skills/` - 项目通用技能
3. `~/.agent/skills/` - 全局通用技能
4. `./.claude/skills/` - 项目 Claude 技能
5. `~/.claude/skills/` - 全局 Claude 技能

**特点**: 技能安装一次，所有 AI CLI 工具通用

### 4. 跨会话协作

**项目状态看板**（Project Status Board）:
- 每个项目目录有独立的状态看板
- 存储在 `.stigmergy/status/PROJECT_STATUS.md`
- 跟踪任务、发现、决策和协作历史
- 不同 CLI 会话自动基于状态板协作

```bash
stigmergy interactive
> status      # 查看项目状态
> context     # 显示所有 CLI 工具的上下文
> use qwen    # 切换到特定 CLI
> finding: xxx  # 记录发现
> decision: xxx # 记录决策
```

### 5. Stigmergy Gateway

通过飞书/Telegram/Slack/Discord 远程控制 AI CLI：

```bash
# 启动 Gateway
stigmergy gateway --feishu --port 3000
```

### 6. 12 种语言支持

支持中文、英文、日文、德文、法文、西班牙文等 12 种语言。

---

## 🤖 多智能体协同机制

### 协同方式

Stigmergy 的多智能体协同**不是**多个 AI 模型同时处理一个任务，而是：

1. **任务路由协同**
   - 根据任务类型自动选择最佳 AI CLI 工具
   - 例如：代码任务 → Claude，翻译 → Gemini，分析 → Qwen

2. **跨会话协同**
   - 不同 AI CLI 会话共享项目状态看板
   - 每个会话记录发现和决策
   - 后续会话基于之前的状态继续工作

3. **技能共享协同**
   - 技能安装一次，所有 AI CLI 通用
   - 不同 AI CLI 可以使用相同的技能

### 协同示例

```bash
# 会话 1：使用 Claude 写代码
stigmergy interactive
> use claude
> 写一个 Python 函数，用于数据清洗
> finding: 创建了 data_cleaning.py
> decision: 使用 pandas 库

# 会话 2：使用 Qwen 分析代码
stigmergy interactive
> status  # 查看之前的状态
> use qwen
> 分析 data_cleaning.py 的代码质量
> finding: 代码质量良好，但缺少异常处理
> decision: 建议添加 try-except 块

# 会话 3：使用 Gemini 写文档
stigmergy interactive
> status  # 查看所有历史
> use gemini
> 为 data_cleaning.py 写文档
```

---

## 💡 重要澄清

### Stigmergy 不是什么

❌ **Stigmergy 不是 AI 模型**
- 它不提供 AI 模型
- 它需要用户有自己的 AI CLI 工具（Claude、Gemini、Qwen 等）
- 它不提供云端 AI 服务

❌ **Stigmergy 不是 SocienceAI 的子项目**
- 它是独立的开源项目（GitHub: ptreezh/stigmergy-CLI-Multi-Agents）
- 维护者：niuxiaozhang <shurenzhang631@gmail.com>
- 与 SocienceAI 没有直接关系

❌ **Stigmergy 不"无需自备算力"**
- 用户需要有自己的 AI CLI 工具
- 这些 AI CLI 工具需要 API Key（如 Claude API、Gemini API 等）
- 或者需要本地 AI 模型（如 Ollama、LM Studio 等）

### Stigmergy 是什么

✅ **Stigmergy 是 AI CLI 协调器**
- 协调多个 AI CLI 工具
- 提供统一的技能管理
- 实现跨 CLI 通信

✅ **Stigmergy 是技能管理器**
- 从 GitHub 安装技能
- 技能安装一次，所有 AI CLI 通用
- 支持 agentskills.io 规范技能

✅ **Stigmergy 是会话管理器**
- 跨会话恢复
- 项目状态看板
- 记忆共享

---

## 📊 与 SocienceAI 技能的关系

### 技能兼容

SocienceAI 的社会科学方法论技能可以通过 Stigmergy 加载：

```bash
# 安装 SocienceAI 技能
stigmergy skill install socienceai/agentskills

# 使用技能
stigmergy qwen --skill grounded-theory-expert "分析访谈数据"
stigmergy claude --skill social-network-analysis-expert "分析社会网络"
```

### 技能位置

SocienceAI 技能可以放在：
- `~/.stigmergy/skills/` - Stigmergy 统一存储
- `~/.claude/skills/` - Claude 技能
- `~/.qwen/skills/` - Qwen 技能

---

## 🎯 正确使用方式

### 前提条件

使用 Stigmergy 前，用户需要：
1. **安装至少一个 AI CLI 工具**
   - claude-cli（需要 Claude API Key）
   - gemini-cli（需要 Gemini API Key）
   - qwen-cli（需要阿里云 API Key）
   - 或其他支持的 AI CLI 工具

2. **配置 AI CLI 工具**
   ```bash
   claude config  # 配置 Claude API Key
   gemini config  # 配置 Gemini API Key
   qwen config    # 配置阿里云 API Key
   ```

### 使用流程

```bash
# 1. 安装 Stigmergy
npm install -g stigmergy@beta

# 2. 安装 SocienceAI 技能
stigmergy skill install socienceai/agentskills

# 3. 使用技能（需要有自己的 AI CLI 工具）
stigmergy qwen --skill grounded-theory-expert "分析访谈数据"
```

---

## 📋 战略调整建议

### 之前的错误

❌ 错误 1: "Stigmergy 是本平台的多智能体系统"
- 事实：Stigmergy 是独立开源项目，与 SocienceAI 无直接关系

❌ 错误 2: "无需自备 AI 模型算力"
- 事实：用户需要有自己的 AI CLI 工具和 API Key

❌ 错误 3: "多 Agent 协同进化"
- 事实：Stigmergy 的协同是任务路由和会话共享，不是多个 AI 同时处理一个任务

### 正确定位

✅ **Stigmergy 是技能分发渠道**
- SocienceAI 技能可以通过 Stigmergy 分发
- 技能安装一次，所有 AI CLI 通用

✅ **Stigmergy 是协同工具**
- 协调多个 AI CLI 工具
- 跨会话协作
- 项目状态管理

✅ **SocienceAI 技能兼容 Stigmergy**
- 遵循 agentskills.io 规范
- 可以在 Stigmergy 中使用
- 可以在所有 AI CLI 中使用

---

**分析完成日期**: 2026-03-22  
**分析师**: SocienceAI Team  
**信息来源**: npm + GitHub README  
**版本**: stigmergy@1.10.10-beta.5

*基于事实，纠正错误认知*
