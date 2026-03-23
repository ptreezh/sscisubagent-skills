# Stigmergy 技能使用教程（真实版）

**基于 Stigmergy v1.10.10-beta.5 真实功能**  
**最后更新**: 2026-03-22

---

## ⚠️ 重要说明

**Stigmergy 是什么**:
- ✅ Stigmergy 是**多 AI CLI 工具协同系统**
- ✅ 它协调 Claude、Gemini、Qwen 等 9+ 种 AI CLI 工具
- ✅ 它管理技能，技能安装一次，所有 AI CLI 通用

**Stigmergy 不是什么**:
- ❌ Stigmergy **不是 AI 模型** - 不提供 AI 模型
- ❌ Stigmergy **不是 SocienceAI 的子项目** - 是独立开源项目
- ❌ Stigmergy **不"无需自备算力"** - 用户需要有自己的 AI CLI 工具和 API Key

---

## 📋 前置要求

使用 Stigmergy 前，你需要：

### 1. 安装至少一个 AI CLI 工具

```bash
# Claude CLI（需要 Claude API Key）
npm install -g @anthropic-ai/claude-cli

# Gemini CLI（需要 Gemini API Key）
npm install -g gemini-cli

# Qwen CLI（需要阿里云 API Key）
npm install -g qwen-cli

# 或其他支持的 AI CLI 工具
```

### 2. 配置 AI CLI 工具

```bash
# 配置 Claude
claude config
# 输入你的 Claude API Key

# 配置 Gemini
gemini config
# 输入你的 Gemini API Key

# 配置 Qwen
qwen config
# 输入你的阿里云 API Key
```

### 3. 安装 Node.js

```bash
# 下载并安装 Node.js >= 16.0.0
# https://nodejs.org/
```

---

## 🚀 安装 Stigmergy

```bash
# 安装 Stigmergy（最新 Beta 版）
npm install -g stigmergy@beta

# 验证安装
stigmergy --version
stigmergy --help
```

---

## 📦 安装 SocienceAI 技能

### 方式 1: 从 GitHub 安装（推荐）

```bash
# 安装 SocienceAI 技能包
stigmergy skill install socienceai/agentskills

# 验证技能已安装
stigmergy skill list
```

### 方式 2: Git 克隆

```bash
# 克隆技能仓库
git clone https://github.com/socienceai/agentskills.git
cd agentskills

# 复制到 Stigmergy 技能目录
cp -r grounded-theory-expert ~/.stigmergy/skills/
cp -r social-network-analysis-expert ~/.stigmergy/skills/
# ... 复制其他技能
```

### 方式 3: 手动下载

```bash
# 1. 访问 https://github.com/socienceai/agentskills
# 2. 点击 "Code" → "Download ZIP"
# 3. 解压到本地
# 4. 复制技能到 ~/.stigmergy/skills/
```

---

## 📚 使用技能

### 基本使用

```bash
# 使用特定 AI CLI 工具 + 技能
stigmergy qwen --skill grounded-theory-expert "分析以下访谈数据..."
stigmergy claude --skill social-network-analysis-expert "分析社会网络..."
stigmergy gemini --skill bourdieu-field-analysis-expert "分析场域..."
```

### 智能路由

```bash
# 让 Stigmergy 自动选择最佳 AI 工具
stigmergy call --skill grounded-theory-expert "分析以下访谈数据..."
```

### 交互式模式

```bash
# 启动交互式模式
stigmergy interactive

# 在交互式中加载技能
> use qwen
> load grounded-theory-expert
> 分析以下访谈数据...
> finding: 识别出 4 个初始概念
> decision: 需要进行轴心编码
```

---

## 🤖 多 CLI 协同示例

### 示例：跨学科研究协同

```bash
# 会话 1：使用 Qwen 进行扎根理论分析
stigmergy interactive
> use qwen
> load grounded-theory-expert
> 分析以下访谈数据...
> finding: 识别出 4 个初始概念
> decision: 需要进行轴心编码
> # 会话结束，状态自动保存

# 会话 2：使用 Claude 进行社会网络分析
stigmergy interactive
> status  # 查看之前的状态
> use claude
> load social-network-analysis-expert
> 基于之前的编码结果，分析概念间的关系网络
> finding: 发现核心概念是"工作压力"
> decision: 建议进一步收集数据验证

# 会话 3：使用 Gemini 撰写报告
stigmergy interactive
> status  # 查看所有历史
> use gemini
> load academic-writing-expert
> 基于以上分析，撰写研究报告
```

---

## 📊 技能存储位置

Stigmergy 技能存储位置（优先级从高到低）：

1. `~/.stigmergy/skills/` - Stigmergy 统一存储（**推荐**）
2. `./.agent/skills/` - 项目通用技能
3. `~/.agent/skills/` - 全局通用技能
4. `./.claude/skills/` - 项目 Claude 技能
5. `~/.claude/skills/` - 全局 Claude 技能

**特点**: 技能安装一次，所有 AI CLI 工具通用

---

## 🔧 技能管理

### 查看技能

```bash
# 列出所有技能
stigmergy skill list

# 查看技能详情
stigmergy skill read grounded-theory-expert
```

### 更新技能

```bash
# 更新所有技能
stigmergy skill update

# 更新特定技能
stigmergy skill update grounded-theory-expert
```

### 删除技能

```bash
# 删除技能
stigmergy skill remove grounded-theory-expert
```

---

## 📖 可用技能（12 种）

### 质性研究方法

| 技能 | 对标学者 | 核心功能 |
|------|---------|---------|
| **扎根理论** | Kathy Charmaz | 开放编码、轴心编码、选择式编码 |
| **社会网络分析** | Linton Freeman | 中心性分析、社区检测、结构洞 |
| **行动者网络理论** | Bruno Latour | 行动者识别、转译过程、网络追踪 |
| **布迪厄场域分析** | Pierre Bourdieu | 场域识别、资本分析、习性分析 |

### 定量研究方法

| 技能 | 对标学者 | 核心功能 |
|------|---------|---------|
| **QCA** | Charles Ragin | 模糊集校准、真值表、布尔最小化 |
| **DID** | Angrist & Pischke | 平行趋势检验、双向固定效应 |
| **回归分析** | Ronald Fisher | OLS 估计、假设检验、模型诊断 |
| **问卷设计** | Don A. Dillman | 问题设计、抽样方法、信效度检验 |

### 混合方法与社会理论

| 技能 | 对标学者 | 核心功能 |
|------|---------|---------|
| **混合方法** | John Creswell | 三角验证、互补设计、转换整合 |
| **数字马克思** | David Harvey | 数字劳动、剩余价值、意识形态批判 |
| **数字涂尔干** | Émile Durkheim | 集体意识、社会团结、神圣世俗 |
| **数字韦伯** | Max Weber | 理性化、科层制、祛魅 |

---

## ❓ 常见问题

### Q: Stigmergy 免费吗？

**A**: 
- Stigmergy 本身免费开源（MIT 许可证）
- 但 AI CLI 工具需要 API Key，可能产生费用
- 例如：Claude API、Gemini API、阿里云 API 等

### Q: 我没有 API Key 怎么办？

**A**: 
1. 申请免费 API Key（如 Gemini 有免费额度）
2. 使用本地 AI 模型（如 Ollama、LM Studio）
3. 使用有免费额度的服务

### Q: 技能可以在多个 AI CLI 中使用吗？

**A**: 是的！这是 Stigmergy 的核心优势：
- 技能安装一次
- 所有 AI CLI 工具通用（Claude、Gemini、Qwen 等）
- 无需重复安装

### Q: 如何查看技能内容？

**A**: 
```bash
# 读取技能
stigmergy skill read grounded-theory-expert

# 或查看文件
cat ~/.stigmergy/skills/grounded-theory-expert/SKILL.md
```

### Q: Stigmergy 与 SocienceAI 是什么关系？

**A**: 
- Stigmergy 是独立开源项目（GitHub: ptreezh/stigmergy-CLI-Multi-Agents）
- SocienceAI 是社会科学方法论技能提供者
- SocienceAI 技能遵循 agentskills.io 规范
- Stigmergy 支持 agentskills.io 规范技能
- 两者是**技能分发和使用**的关系

---

## 📖 相关资源

### Stigmergy 资源

- [Stigmergy GitHub](https://github.com/ptreezh/stigmergy-CLI-Multi-Agents)
- [Stigmergy npm](https://www.npmjs.com/package/stigmergy)
- [Stigmergy 文档](https://github.com/ptreezh/stigmergy-CLI-Multi-Agents#readme)

### SocienceAI 资源

- [SocienceAI 技能仓库](https://github.com/socienceai/agentskills)
- [技能包下载](https://github.com/socienceai/agentskills/archive/main.zip)

### AI CLI 工具

- [Claude CLI](https://github.com/anthropics/claude-cli)
- [Gemini CLI](https://github.com/google/gemini-cli)
- [Qwen CLI](https://github.com/QwenLM/qwen-cli)

---

**教程版本**: 1.0（基于真实功能）  
**最后更新**: 2026-03-22  
**维护者**: SocienceAI Team

*基于事实，纠正错误认知*
