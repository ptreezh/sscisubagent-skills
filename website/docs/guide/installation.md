# 安装

## 环境要求

- **Claude Code**: 最新版本
- **Python 3.8+**: 用于验证脚本（可选）
- **操作系统**: Windows / macOS / Linux

## 安装步骤

### 1. 获取技能包

```bash
# 克隆仓库
git clone https://github.com/socienceai/agentskills.git
cd agentskills
```

### 2. 安装到 Claude Code

将技能目录复制到 Claude Code 的 skills 目录：

```bash
# 复制技能到全局目录
cp -r <skill-name>-expert ~/.claude/skills/
```

### 3. 验证安装

```bash
# 验证所有技能
python scripts/validate_all_skills.py
```

## 技能目录结构

每个技能包含：

```
<skill-name>-expert/
├── SKILL.md          # 技能定义（必需）
├── examples/         # 示例数据（推荐）
│   └── *.md
└── README.md         # 说明文档（可选）
```

---

[← 返回使用指南](/guide/)

*由 SocienceAI 提供*
