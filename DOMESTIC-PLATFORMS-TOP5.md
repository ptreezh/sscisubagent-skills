# 国内 AI 平台技能加载指南（首推版）

**分析日期**: 2026-03-22  
**覆盖平台**: 8 个国内主流平台  
**规范标准**: agentskills.io v1.0  
**首推平台**: WorkBuddy、Stigmergy、Coze、钉钉、Qwen

---

## 🎯 首推平台（5 个）

| 平台 | 类型 | 获取难度 | 用户群体 | 特点 | 推荐度 |
|------|------|---------|---------|------|--------|
| **WorkBuddy** ⭐ | CLI 工具 | ⭐ 极易 | 研究者、开发者 | 本地部署，兼容性好，研究者首选 | ⭐⭐⭐⭐⭐ |
| **Stigmergy** ⭐ | CLI 协调器 | ⭐ 极易 | 研究者 | 多 CLI 协同，技能通用，跨平台协作 | ⭐⭐⭐⭐⭐ |
| **Coze 编程** ⭐ | 云端 Bot | ⭐ 极易 | 所有人 | 网页访问，免费额度，无需安装 | ⭐⭐⭐⭐⭐ |
| **钉钉悟空** ⭐ | 企业 Bot | ⭐ 极易 | 企业用户 | 钉钉内置，企业集成，免费使用 | ⭐⭐⭐⭐⭐ |
| **Qwen** ⭐ | CLI/API | ⭐ 极易 | 开发者、研究者 | 中文能力强，有免费额度 | ⭐⭐⭐⭐⭐ |

---

## 🌟 WorkBuddy（首推 - 研究者首选）

### 核心优势

**WorkBuddy** 是本地部署的 AI 助手 CLI 工具，完全兼容 agentskills.io 规范。

**特点**:
- ✅ **本地部署，数据安全** - 数据不出本地，适合敏感研究
- ✅ **兼容 agentskills.io 规范** - 技能安装一次，多平台通用
- ✅ **研究者友好** - 专为社会科学研究设计
- ✅ **中文支持好** - 中文文档和社区
- ✅ **npm/pip 安装** - 一键安装，开箱即用

### 安装 WorkBuddy

```bash
# npm 安装（推荐）
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
workbuddy --skill grounded-theory-expert "使用扎根理论分析以下访谈数据..."
```

### 使用示例

```bash
# 加载扎根理论技能
workbuddy --skill grounded-theory-expert

# 输入任务
请对以下访谈数据进行开放编码：

"我觉得工作压力很大，每天都要加班，
但是没有明确的晋升通道，感觉很迷茫。"
```

**详细教程**: [WorkBuddy 使用教程](/tutorials/workbuddy/)

---

## 🌟 Stigmergy（首推 - 多 CLI 协同）

### 核心优势

**Stigmergy** 是多 AI CLI 工具协同系统，协调 Claude、Gemini、Qwen 等 9+ 种 AI CLI 工具。

**特点**:
- ✅ **技能安装一次，所有 AI CLI 通用** - 最大优势
- ✅ **跨 CLI 通信** - 不同 AI CLI 工具之间无缝协作
- ✅ **智能任务路由** - 自动选择最佳 AI 工具
- ✅ **会话恢复和记忆共享** - 跨会话协作
- ✅ **npm 安装** - 一键安装

**重要说明**:
- ⚠️ Stigmergy 不是 AI 模型，需要自备 AI CLI 工具
- ⚠️ 需要至少一个 AI CLI 工具（Claude、Gemini、Qwen 等）
- ⚠️ 需要 API Key（或使用免费额度的服务）

### 安装 Stigmergy

```bash
# 安装 Stigmergy
npm install -g stigmergy@beta

# 验证安装
stigmergy --version
```

### 前置要求

使用 Stigmergy 前，需要先安装至少一个 AI CLI 工具：
```bash
# 选择安装（至少一个）
npm install -g @anthropic-ai/claude-cli  # Claude（需要 API Key）
npm install -g gemini-cli                # Gemini（有免费额度）
npm install -g qwen-cli                  # Qwen（有免费额度）
```

### 加载技能

```bash
# 安装 SocienceAI 技能
stigmergy skill install socienceai/agentskills

# 使用技能（会自动选择已安装的 AI CLI 工具）
stigmergy call --skill grounded-theory-expert "分析访谈数据"

# 或指定 AI CLI 工具
stigmergy qwen --skill grounded-theory-expert "分析访谈数据"
```

### 多 CLI 协同示例

```bash
# 会话 1：使用 Qwen 进行扎根理论分析
stigmergy interactive
> use qwen
> load grounded-theory-expert
> 分析以下访谈数据...
> finding: 识别出 4 个初始概念

# 会话 2：使用 Claude 进行社会网络分析
stigmergy interactive
> status  # 查看之前的状态
> use claude
> load social-network-analysis-expert
> 基于之前的编码结果，分析概念间的关系网络
```

**详细教程**: [Stigmergy 真实使用教程](/tutorials/stigmergy-real/)

---

## 🌟 Coze 编程（首推 - 免费云端）

### 核心优势

**Coze 编程**是字节跳动推出的 AI 编程助手，支持技能/插件导入。

**特点**:
- ✅ **无需部署，开箱即用** - 网页访问
- ✅ **可视化配置** - 无需编程
- ✅ **免费额度** - 有免费使用额度
- ✅ **支持插件扩展** - 丰富的插件生态

### 使用方式

1. 访问 https://www.coze.cn/
2. 注册/登录
3. 创建 Bot
4. 配置人设（复制 SKILL.md 内容）
5. 添加插件（对应 tools/）
6. 上传知识库（对应 templates/）
7. 发布 Bot

**详细教程**: [Coze 使用教程](/tutorials/coze/)

---

## 🌟 钉钉悟空（首推 - 企业免费）

### 核心优势

**钉钉悟空**是阿里巴巴推出的企业级 AI 助手，集成在钉钉中。

**特点**:
- ✅ **企业用户直接可用** - 钉钉内置
- ✅ **集成钉钉生态** - 与企业微信、钉钉应用无缝集成
- ✅ **免费使用** - 企业版免费
- ✅ **数据安全** - 企业级数据安全

### 使用方式

1. 打开钉钉
2. 搜索"悟空助手"
3. 添加到工作台
4. 配置使用

**详细教程**: [钉钉悟空使用教程](/tutorials/dingtalk/)

---

## 🌟 Qwen（首推 - 中文能力强）

### 核心优势

**Qwen** 是阿里云推出的通义千问系列，包括 CLI 和 API。

**特点**:
- ✅ **中文能力强** - 中文理解和生成能力强
- ✅ **支持 CLI 和 API** - 多种使用方式
- ✅ **有免费额度** - 新用户有免费 API 额度
- ✅ **技能兼容性好** - 支持 agentskills.io 规范

### 安装 Qwen CLI

```bash
# npm 安装
npm install -g qwen-cli

# 配置 API Key（新用户有免费额度）
qwen config --api-key YOUR_API_KEY

# 使用技能
qwen --skill grounded-theory-expert "任务描述"
```

**详细教程**: [Qwen 使用教程](/tutorials/qwen/)

---

## 📊 首推平台对比

| 平台 | 类型 | 安装方式 | 技能格式 | 数据位置 | 算力需求 | 免费额度 | 推荐场景 |
|------|------|---------|---------|---------|---------|---------|---------|
| **WorkBuddy** ⭐ | CLI 工具 | npm/pip | agentskills.io | 本地 | 需自备 | ❌ | 研究者首选，数据安全 |
| **Stigmergy** ⭐ | CLI 协调器 | npm | agentskills.io | 本地 | 需自备 AI CLI | ❌ | 多 CLI 协同，技能通用 |
| **Coze 编程** ⭐ | 云端 Bot | 网页 | Bot 配置 | 云端 | 云端 | ✅ | 快速上手，免费额度 |
| **钉钉悟空** ⭐ | 企业 Bot | 钉钉内置 | 企业 Bot | 云端 | 云端 | ✅ | 企业用户，企业集成 |
| **Qwen** ⭐ | CLI/API | npm/pip | agentskills.io | 云端/本地 | 需自备 | ✅ | 中文研究，API 调用 |

---

## 🚀 快速选择指南

### 根据用户类型选择

**研究者（首选）**:
1. **WorkBuddy** ⭐⭐⭐⭐⭐ - 研究者友好，本地部署
2. **Stigmergy** ⭐⭐⭐⭐⭐ - 多 CLI 协同，技能通用
3. **Qwen** ⭐⭐⭐⭐⭐ - 中文能力强

**企业用户**:
1. **钉钉悟空** ⭐⭐⭐⭐⭐ - 企业集成
2. **Coze 编程** ⭐⭐⭐⭐⭐ - 快速部署
3. **Qwen** ⭐⭐⭐⭐⭐ - 企业 API

**开发者**:
1. **Stigmergy** ⭐⭐⭐⭐⭐ - 多 CLI 协同
2. **WorkBuddy** ⭐⭐⭐⭐⭐ - 本地部署
3. **OpenCode** - 开源编程

**学生/个人用户**:
1. **Coze 编程** ⭐⭐⭐⭐⭐ - 免费额度
2. **Qwen** ⭐⭐⭐⭐⭐ - 免费 API 额度
3. **WorkBuddy** - 本地免费

### 根据需求选择

**数据安全优先**:
1. **WorkBuddy** - 本地部署，数据不出本地
2. **OpenClaw** - 本地部署
3. **OpenCode** - 本地部署

**免费额度优先**:
1. **Coze 编程** - 免费额度
2. **钉钉悟空** - 企业免费
3. **Qwen** - 免费 API 额度

**多 CLI 协同**:
1. **Stigmergy** - 多 CLI 协同，技能通用
2. **WorkBuddy** - 兼容性好

**快速上手**:
1. **Coze 编程** - 网页访问，无需安装
2. **钉钉悟空** - 钉钉内置
3. **WorkBuddy** - npm 一键安装

---

## 📚 教程资源

### 首推平台教程

| 教程 | 文件 | 说明 |
|------|------|------|
| WorkBuddy 教程 | `tutorial-workbuddy.md` | WorkBuddy 详细使用教程 |
| Stigmergy 教程 | `tutorial-stigmergy-real.md` | Stigmergy 真实使用教程 |
| Coze 教程 | `tutorial-coze.md` | Coze 详细使用教程 |
| 钉钉悟空教程 | `tutorial-dingtalk.md` | 钉钉悟空使用教程 |
| Qwen 教程 | `tutorial-qwen.md` | Qwen 详细使用教程 |

### 其他平台教程

| 教程 | 文件 | 说明 |
|------|------|------|
| OpenCode 教程 | `tutorial-opencode.md` | OpenCode 使用教程 |
| KiloCode 教程 | `tutorial-kilocode.md` | KiloCode 使用教程 |
| OpenClaw 教程 | `tutorial-openclaw.md` | OpenClaw 使用教程 |

---

## 📖 相关资源

### 平台文档

- [WorkBuddy 文档](https://github.com/workbuddy/workbuddy)
- [Stigmergy 文档](https://github.com/ptreezh/stigmergy-CLI-Multi-Agents)
- [Coze 文档](https://www.coze.cn/docs)
- [钉钉悟空文档](https://open.dingtalk.com/document/)
- [Qwen 文档](https://help.aliyun.com/product/42154.html)

### 技能仓库

- [SocienceAI 技能仓库](https://github.com/socienceai/agentskills)
- [技能包下载](https://github.com/socienceai/agentskills/archive/main.zip)

---

**分析完成日期**: 2026-03-22  
**分析师**: SocienceAI Team  
**首推平台**: WorkBuddy、Stigmergy、Coze、钉钉悟空、Qwen

*让社会科学研究人人可为*
