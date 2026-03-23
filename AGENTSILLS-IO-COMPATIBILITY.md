# agentskills.io 规范兼容分析报告

**分析日期**: 2026-03-22  
**兼容平台**: OpenClaw（小龙虾）、Claude Code  
**规范版本**: agentskills.io v1.0

---

## 📋 agentskills.io 技能规范

### 技能包结构

```
skill-name/
├── SKILL.md              # 技能定义（必需）
├── skill.yaml            # 技能配置（必需）
├── tools/                # 工具模块（可选）
│   ├── __init__.py
│   └── tool_name.py
├── templates/            # 模板文件（可选）
├── examples/             # 使用示例（可选）
└── README.md             # 使用说明（推荐）
```

### SKILL.md 格式

```markdown
---
name: skill-name
description: |
  技能的触发描述和使用场景。
  当用户想要做 X 时使用此技能。
  触发条件：[具体触发场景]
---

# 技能正文

## 角色定义
你是 XXX 专家，专注于...

## 工作流程
1. 第一步...
2. 第二步...

## 输出规范
- 必须...
- 禁止...
```

### skill.yaml 格式

```yaml
---
name: skill-name
version: 1.0.0
description: |
  技能的详细描述

author: Author Name
license: MIT

metadata:
  version: "1.0.0"
  type: "methodology"
  category: "social-science"

inputs:
  task:
    type: string
    required: true
    description: 任务描述

outputs:
  result:
    type: object
    description: 执行结果

prompts:
  system: SKILL.md

tools:
  - name: tool-name
    description: 工具描述
    module: tool_module

quality_checks:
  - name: check-name
    description: 检查说明
    rule: "检查规则"

compatibility:
  - agentskills.io
  - openclaw
  - claude-code

allowed-tools: Read Write Bash --allow
---
```

---

## 🔌 OpenClaw（小龙虾）兼容性

### OpenClaw 技能规范

**技能位置**: `~/.qwen/skills/skill-name/`

**加载方式**:
```bash
# 自动加载（技能在技能目录）
qwen "任务描述"

# 手动指定
qwen --skill skill-name "任务描述"

# 环境变量
export QWEN_SKILL_PATH=/path/to/skills
qwen "任务描述"
```

### 兼容性分析

| 规范要素 | agentskills.io | OpenClaw | 兼容性 |
|---------|---------------|---------|--------|
| SKILL.md | ✅ 必需 | ✅ 必需 | ✅ 完全兼容 |
| skill.yaml | ✅ 必需 | ✅ 必需 | ✅ 完全兼容 |
| tools/ | ✅ 可选 | ✅ 可选 | ✅ 完全兼容 |
| templates/ | ✅ 可选 | ✅ 可选 | ✅ 完全兼容 |
| 跨平台要求 | ✅ 必须 | ✅ 必须 | ✅ 完全兼容 |

### OpenClaw 特定要求

**Soul Agent 规范**:
```yaml
# skill.yaml 额外字段
soul:
  name: grounded-theory-expert
  role: 扎根理论分析专家
  personality: 严谨、系统、深入
  values:
    - 方法论严谨性第一
    - 权威理论对齐
```

**Hooks 配置**:
```yaml
# skill-hooks.yaml（可选）
hooks:
  on_cli_start:
    enabled: true
    action: load_soul
  on_session_start:
    enabled: true
    actions:
      - load_state
```

---

## 🤖 Claude Code 兼容性

### Claude Code 技能规范

**技能位置**: `~/.claude/skills/skill-name/` 或项目 `.claude/skills/`

**加载方式**:
```bash
# 自动加载（技能在技能目录）
claude "任务描述"

# 项目级别
# 在项目 .claude/skills/ 中创建技能
# Claude Code 自动加载
```

### 兼容性分析

| 规范要素 | agentskills.io | Claude Code | 兼容性 |
|---------|---------------|------------|--------|
| SKILL.md | ✅ 必需 | ✅ 必需 | ✅ 完全兼容 |
| skill.yaml | ✅ 必需 | ✅ 必需 | ✅ 完全兼容 |
| tools/ | ✅ 可选 | ✅ 可选 | ✅ 完全兼容 |
| templates/ | ✅ 可选 | ✅ 可选 | ✅ 完全兼容 |
| 跨平台要求 | ✅ 必须 | ✅ 必须 | ✅ 完全兼容 |

### Claude Code 特定要求

**技能描述优化**:
```markdown
# SKILL.md 开头部分需要更"pushy"的描述

description: |
  创建新技能时使用此技能。
  当用户提到"创建技能"、"编辑技能"、"优化技能"时务必使用。
  即使没有明确请求，只要涉及技能相关工作就应触发。
```

**工具权限声明**:
```yaml
# skill.yaml
allowed-tools:
  - Read
  - Write
  - Bash(git:*)
  - Bash(python:*)
  - --allow
```

---

## 📦 统一技能包结构

### 推荐结构（兼容双平台）

```
skill-package/
├── SKILL.md                    # 技能定义（双平台兼容）
├── skill.yaml                  # 技能配置（双平台兼容）
├── tools/                      # 工具模块（双平台兼容）
│   ├── __init__.py
│   ├── tool1.py
│   └── tool2.py
├── templates/                  # 模板文件（双平台兼容）
│   ├── template1.md
│   └── template2.md
├── examples/                   # 使用示例
│   ├── openclaw-examples.md    # OpenClaw 示例
│   └── claude-examples.md      # Claude Code 示例
├── docs/                       # 文档
│   ├── openclaw-guide.md       # OpenClaw 使用指南
│   ├── claude-guide.md         # Claude Code 使用指南
│   └── troubleshooting.md      # 故障排查
└── README.md                   # 总说明
```

### 平台适配层（可选）

```
adapters/
├── openclaw/
│   └── adapter.yaml
└── claude/
    └── adapter.yaml
```

**OpenClaw 适配器**:
```yaml
# adapters/openclaw/adapter.yaml
platform: openclaw
skill_path: ~/.qwen/skills/{{skill_name}}
load_command: qwen --skill {{skill_name}}
config_files:
  - SKILL.md
  - skill.yaml
  - skill-hooks.yaml (可选)
```

**Claude Code 适配器**:
```yaml
# adapters/claude/adapter.yaml
platform: claude-code
skill_path: ~/.claude/skills/{{skill_name}}
load_command: claude --skill {{skill_name}}
config_files:
  - SKILL.md
  - skill.yaml
```

---

## 🚀 技能分发流程

### 1. 开发技能

```bash
# 创建技能目录
mkdir -p grounded-theory-expert
cd grounded-theory-expert

# 创建 SKILL.md
# 创建 skill.yaml
# 创建 tools/
# 创建 templates/
```

### 2. 测试技能

**OpenClaw 测试**:
```bash
# 复制到 OpenClaw 技能目录
cp -r grounded-theory-expert ~/.qwen/skills/

# 测试
qwen --skill grounded-theory-expert "任务描述"
```

**Claude Code 测试**:
```bash
# 复制到 Claude Code 技能目录
cp -r grounded-theory-expert ~/.claude/skills/

# 测试
claude --skill grounded-theory-expert "任务描述"
```

### 3. 打包技能

```bash
# 打包为 ZIP
zip -r grounded-theory-expert.zip grounded-theory-expert/

# 或发布到 GitHub
git init
git add .
git commit -m "Initial release"
git push origin main
```

### 4. 分发技能

**GitHub 发布**:
```
仓库：github.com/socienceai/agentskills
路径：/grounded-theory-expert/
发布：GitHub Release
```

**agentskills.io 发布**:
```
提交到 agentskills.io 技能市场
遵循 agentskills.io 审核流程
```

---

## 📚 用户使用流程

### OpenClaw 用户

**步骤 1: 安装 OpenClaw**
```bash
npm install -g openclaw
# 或
pip install openclaw
```

**步骤 2: 下载技能**
```bash
# 方式 1: Git 克隆
git clone https://github.com/socienceai/agentskills.git
cd agentskills

# 方式 2: 下载 ZIP
# 访问 GitHub 下载并解压
```

**步骤 3: 加载技能**
```bash
# 复制到技能目录
cp -r grounded-theory-expert ~/.qwen/skills/

# 使用技能
qwen --skill grounded-theory-expert "使用扎根理论分析以下访谈数据..."
```

### Claude Code 用户

**步骤 1: 安装 Claude Code**
```bash
# 按照官方文档安装
```

**步骤 2: 下载技能**
```bash
# 方式 1: Git 克隆
git clone https://github.com/socienceai/agentskills.git
cd agentskills

# 方式 2: 下载 ZIP
# 访问 GitHub 下载并解压
```

**步骤 3: 加载技能**
```bash
# 复制到技能目录
cp -r grounded-theory-expert ~/.claude/skills/

# 使用技能
claude --skill grounded-theory-expert "使用扎根理论分析以下访谈数据..."
```

---

## ✅ 兼容性检查清单

### 技能开发检查

- [ ] SKILL.md 格式正确
- [ ] skill.yaml 格式正确
- [ ] tools/ 模块跨平台兼容
- [ ] templates/ 模板可用
- [ ] 无 Linux 特定命令
- [ ] 使用 Python 跨平台 API

### 测试检查

- [ ] OpenClaw 测试通过
- [ ] Claude Code 测试通过
- [ ] Windows 测试通过
- [ ] macOS 测试通过
- [ ] Linux 测试通过

### 分发检查

- [ ] README.md 完整
- [ ] 使用文档完整
- [ ] GitHub 仓库创建
- [ ] 许可证正确（MIT）
- [ ] agentskills.io 提交

---

## 🎯 最佳实践

### 1. SKILL.md 编写

**推荐**:
```markdown
---
name: grounded-theory-expert
description: |
  扎根理论分析专家 - 用于质性数据分析。
  当用户需要分析访谈数据、进行编码时使用。
  触发场景：访谈分析、编码、理论建构
---

# 角色
你是扎根理论分析专家...
```

**避免**:
```markdown
# 避免模糊描述
description: 一个有用的技能

# 避免平台特定
description: 仅适用于 OpenClaw
```

### 2. skill.yaml 编写

**推荐**:
```yaml
---
name: grounded-theory-expert
version: 1.0.0
description: 扎根理论分析专家
compatibility:
  - agentskills.io
  - openclaw
  - claude-code
---
```

**避免**:
```yaml
# 避免缺少版本
version: 

# 避免缺少兼容性声明
compatibility: []
```

### 3. 工具开发

**推荐**:
```python
# 使用 pathlib 跨平台
from pathlib import Path
path = Path.home() / '.qwen' / 'skills'

# 使用 subprocess 跨平台
import subprocess
subprocess.run(['git', 'clone', url])
```

**避免**:
```python
# 避免 Linux 特定路径
path = '/tmp/skills'

# 避免 shell 特定命令
os.system('rm -rf /tmp/skills')
```

---

**分析完成日期**: 2026-03-22  
**分析师**: SocienceAI Team  
**兼容平台**: OpenClaw、Claude Code  
**规范版本**: agentskills.io v1.0

*让社会科学研究人人可为*
