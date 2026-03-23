# 社会科学方法论技能使用教程

**兼容平台**: OpenClaw（小龙虾）、Claude Code  
**规范版本**: agentskills.io v1.0  
**最后更新**: 2026-03-22

---

## 🎯 什么是方法论技能

**方法论技能**是遵循 agentskills.io 规范的专业能力包，可在 OpenClaw 和 Claude Code 中加载使用。

**核心特点**:
- ✅ 遵循 agentskills.io 规范
- ✅ 兼容 OpenClaw 和 Claude Code
- ✅ 跨平台兼容（Windows/Linux/macOS）
- ✅ 学术规范性强

**技能包结构**:
```
skill-name/
├── SKILL.md              # 技能定义
├── skill.yaml            # 技能配置
├── tools/                # 工具模块
├── templates/            # 模板文件
└── README.md             # 使用说明
```

---

## 📦 可用技能（12 种）

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

## 🚀 快速开始（5 分钟）

### 步骤 1: 选择你的平台

**OpenClaw（小龙虾）**:
- 本地部署，数据不出本地
- 支持 Soul Agent 规范
- 适合社会科学研究

**Claude Code**:
- Claude 原生技能
- 代码能力强
- 适合编程相关任务

### 步骤 2: 下载技能包

**方式 1: Git 克隆（推荐）**:
```bash
git clone https://github.com/socienceai/agentskills.git
cd agentskills
```

**方式 2: 下载 ZIP**:
1. 访问 https://github.com/socienceai/agentskills
2. 点击 "Code" → "Download ZIP"
3. 解压到本地

### 步骤 3: 加载技能

**OpenClaw 用户**: 跳转到 [OpenClaw 教程](#openclaw-教程)  
**Claude Code 用户**: 跳转到 [Claude Code 教程](#claude-code-教程)

---

## 📚 OpenClaw 教程

### 安装 OpenClaw

```bash
# 方式 1: npm 安装
npm install -g openclaw

# 方式 2: pip 安装
pip install openclaw

# 验证安装
openclaw --version
```

### 配置技能路径

**方式 1: 复制到技能目录**:
```bash
# 创建技能目录
mkdir -p ~/.qwen/skills

# 复制技能
cp -r grounded-theory-expert ~/.qwen/skills/
```

**方式 2: 环境变量**:
```bash
# Windows (PowerShell)
$env:QWEN_SKILL_PATH="D:\socienceAI\agentskills"

# Linux/Mac
export QWEN_SKILL_PATH="/path/to/agentskills"
```

### 使用技能

**方式 1: 自动加载**:
```bash
# 技能在~/.qwen/skills/目录时自动加载
openclaw "使用扎根理论分析以下访谈数据..."
```

**方式 2: 手动指定**:
```bash
openclaw --skill grounded-theory-expert "使用扎根理论分析以下访谈数据..."
```

### 使用示例

**示例 1: 扎根理论分析**:
```bash
openclaw --skill grounded-theory-expert "
请对以下访谈数据进行开放编码：

'我觉得工作压力很大，每天都要加班，
但是没有明确的晋升通道，感觉很迷茫。'
"
```

**预期输出**:
```
## 开放编码结果

### 初始概念
1. 工作压力 - "我觉得工作压力很大"
2. 加班现象 - "每天都要加班"
3. 晋升困境 - "没有明确的晋升通道"
4. 迷茫情绪 - "感觉很迷茫"

### 下一步建议
1. 进行轴心编码，建立概念间关系
2. 收集更多数据进行持续比较
```

**示例 2: 社会网络分析**:
```bash
openclaw --skill social-network-analysis-expert "
请分析以下社会网络：
节点：A, B, C, D, E
关系：A-B, A-C, B-C, B-D, C-E, D-E
"
```

---

## 📚 Claude Code 教程

### 安装 Claude Code

```bash
# 按照官方文档安装
# https://github.com/anthropics/claude-code
```

### 配置技能路径

**方式 1: 复制到技能目录**:
```bash
# 创建技能目录
mkdir -p ~/.claude/skills

# 复制技能
cp -r grounded-theory-expert ~/.claude/skills/
```

**方式 2: 项目级别**:
```bash
# 在项目目录创建.claude/skills/
mkdir -p .claude/skills
cp -r grounded-theory-expert .claude/skills/
```

### 使用技能

**方式 1: 自动加载**:
```bash
# 技能在~/.claude/skills/目录时自动加载
claude "使用扎根理论分析以下访谈数据..."
```

**方式 2: 手动指定**:
```bash
claude --skill grounded-theory-expert "使用扎根理论分析以下访谈数据..."
```

### 使用示例

**示例 1: 扎根理论分析**:
```bash
claude --skill grounded-theory-expert "
请对以下访谈数据进行开放编码：

'我觉得工作压力很大，每天都要加班，
但是没有明确的晋升通道，感觉很迷茫。'
"
```

**示例 2: 技能创建**:
```bash
claude --skill skill-creator "
我想创建一个用于分析社交媒体数据的技能，
应该包含哪些内容？
"
```

---

## 🔧 高级用法

### 技能组合使用

**OpenClaw**:
```bash
# 同时加载多个技能
openclaw --skill grounded-theory-expert --skill social-network-analysis-expert "
请先用扎根理论编码访谈数据，
然后用社会网络分析分析编码结果的关系网络。
"
```

**Claude Code**:
```bash
# 在对话中切换技能
claude "加载 grounded-theory-expert 技能"
claude "现在切换到 social-network-analysis-expert 技能"
```

### 自定义配置

**编辑 skill.yaml**:
```bash
# 查看技能配置
cat ~/.qwen/skills/grounded-theory-expert/skill.yaml

# 编辑配置
nano ~/.qwen/skills/grounded-theory-expert/skill.yaml
```

### 技能开发

**创建新技能**:
```bash
# 使用 skill-creator 技能
claude --skill skill-creator "
帮我创建一个新的技能，用于分析政策文本。
"
```

---

## ❓ 常见问题

### Q: 技能加载失败

**问题**: `Error: Skill not found`

**解决方案**:
```bash
# 1. 检查技能路径
ls ~/.qwen/skills/  # OpenClaw
ls ~/.claude/skills/  # Claude Code

# 2. 确认技能名称
openclaw --list-skills  # OpenClaw

# 3. 重新复制技能
cp -r grounded-theory-expert ~/.qwen/skills/
```

### Q: 技能执行报错

**问题**: `Error: Tool not found`

**解决方案**:
```bash
# 1. 检查工具依赖
cd ~/.qwen/skills/grounded-theory-expert
pip install -r requirements.txt

# 2. 检查 Python 版本
python --version  # 需要 Python 3.8+
```

### Q: 如何更新技能

**解决方案**:
```bash
# Git 拉取更新
cd ~/agentskills
git pull

# 或重新下载
rm -rf ~/agentskills
git clone https://github.com/socienceai/agentskills.git
```

### Q: 技能在两个平台都能用吗

**回答**: 是的！我们的技能遵循 agentskills.io 规范，兼容 OpenClaw 和 Claude Code 两个平台。

---

## 📖 相关资源

### 规范文档

- [agentskills.io 规范](https://agentskills.io/spec)
- [OpenClaw 技能规范](https://github.com/openclaw/openclaw)
- [Claude Code 技能规范](https://github.com/anthropics/claude-code)

### 技能仓库

- [SocienceAI 技能仓库](https://github.com/socienceai/agentskills)
- [技能包下载](https://github.com/socienceai/agentskills/archive/main.zip)

### 社区支持

- [GitHub Discussions](https://github.com/socienceai/agentskills/discussions)
- [Issues](https://github.com/socienceai/agentskills/issues)

---

## 🎯 下一步学习

### 入门教程

1. ✅ 完成本教程
2. [OpenClaw 详细教程](/tutorials/openclaw/)
3. [Claude Code 详细教程](/tutorials/claude-code/)

### 进阶教程

1. [技能开发与定制](/tutorials/skill-development/)
2. [多技能组合使用](/tutorials/skill-combination/)
3. [技能性能优化](/tutorials/skill-optimization/)

### 专业教程

1. [扎根理论实操指南](/skills/grounded-theory/tutorial/)
2. [社会网络分析实战](/skills/social-network-analysis/tutorial/)
3. [布迪厄场域分析案例](/skills/bourdieu-field-analysis/tutorial/)

---

**教程版本**: 1.0  
**最后更新**: 2026-03-22  
**维护者**: SocienceAI Team

*让社会科学研究人人可为*
