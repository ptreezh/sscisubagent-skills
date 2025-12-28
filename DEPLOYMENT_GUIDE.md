# 部署指南 / Deployment Guide

**作者**: socienceAI.com
**联系**: zhangshuren@freeagentskills.com
**版本**: 1.0.0
**最后更新**: 2025-12-28

---

## 目录 / Table of Contents

1. [快速开始](#快速开始)
2. [基础部署](#基础部署)
3. [CI/CD自动化](#cicd自动化)
4. [发布到AgentSkills.io](#发布到agentskillsio)
5. [故障排查](#故障排查)

---

## 快速开始

### 方式1: 使用部署脚本（推荐）

**Linux/macOS**:
```bash
./scripts/deploy.sh
```

**Windows**:
```cmd
scripts\deploy.bat
```

### 方式2: 手动Git命令

```bash
# 1. 添加所有更改
git add .

# 2. 创建提交
git commit -m "feat: 更新技能和文档

- 更新作者信息
- 优化技能结构
- 添加新功能

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"

# 3. 推送到远程
git push origin main
```

---

## 基础部署

### Git工作流

#### 1. 检查状态

```bash
git status
```

#### 2. 查看更改

```bash
git diff
```

#### 3. 添加文件

```bash
# 添加所有更改
git add .

# 或添加特定文件
git add agents/ skills/
```

#### 4. 创建提交

```bash
git commit -m "type: description"
```

**提交类型（type）**:
- `feat`: 新功能
- `fix`: 修复bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

#### 5. 推送到远程

```bash
git push origin main
```

### 部署脚本详解

#### Linux/macOS (deploy.sh)

**基本使用**:
```bash
# 默认部署（包含测试）
./scripts/deploy.sh

# 跳过测试
./scripts/deploy.sh --skip-tests

# 自定义提交信息
./scripts/deploy.sh -m "feat: 添加新技能"

# 创建版本标签
./scripts/deploy.sh -t v1.0.0
```

**参数说明**:
- `--skip-tests`: 跳过Python语法检查
- `--message, -m`: 自定义提交信息
- `--tag, -t`: 创建版本标签
- `--help, -h`: 显示帮助信息

#### Windows (deploy.bat)

**基本使用**:
```cmd
REM 默认部署
scripts\deploy.bat

REM 跳过测试
scripts\deploy.bat --skip-tests

REM 自定义提交信息
scripts\deploy.bat -m "feat: 添加新技能"

REM 创建版本标签
scripts\deploy.bat -t v1.0.0
```

---

## CI/CD自动化

### GitHub Actions工作流

项目配置了完整的CI/CD管道，位于 `.github/workflows/ci-cd.yml`

#### 触发条件

- **Push到main/develop分支**
- **Pull Request到main/develop分支**
- **创建Release**

#### 工作流程

```
┌─────────────────────────────────────┐
│  1. 代码质量检查 (lint)              │
│     - Black (代码格式)               │
│     - isort (导入排序)               │
│     - Flake8 (代码检查)             │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  2. Python语法检查 (syntax-check)    │
│     - 编译所有.py文件                │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  3. 技能验证 (skills-validation)     │
│     - SKILL.md格式检查              │
│     - YAML frontmatter验证          │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  4. 作者信息检查 (author-check)      │
│     - 统一作者和联系信息             │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  5. 构建和测试 (build-and-test)      │
│     - 多OS测试 (Ubuntu/Windows/MacOS)│
│     - 多Python版本 (3.8-3.11)       │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  6. 文档生成 (docs)                  │
│     - 技能清单                       │
│     - 自动生成文档                   │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  7. 发布到AgentSkills.io             │
│     - (仅在Release时触发)            │
└────────────┬────────────────────────┘
             ↓
┌─────────────────────────────────────┐
│  8. 更新Changelog (changelog)        │
│     - (仅在Release时触发)            │
└─────────────────────────────────────┘
```

### 本地测试CI/CD

使用 `act` 在本地运行GitHub Actions:

```bash
# 安装act (macOS/Linux)
brew install act

# 运行所有job
act push

# 运行特定job
act -j lint
act -j syntax-check
```

### CI/CD Secrets配置

需要在GitHub仓库中配置以下Secrets:

#### 1. AGENTSKILLS_API_KEY

**用途**: 发布技能到AgentSkills.io的API密钥

**获取方式**:
1. 访问 https://agentskills.io/developer
2. 注册/登录账户
3. 创建新的API密钥
4. 复制密钥

**配置步骤**:
1. 进入GitHub仓库设置
2. Secrets and variables → Actions
3. 点击 "New repository secret"
4. Name: `AGENTSKILLS_API_KEY`
5. Value: `your-api-key-here`
6. 点击 "Add secret"

---

## 发布到AgentSkills.io

### 自动发布（推荐）

通过GitHub Release触发自动发布:

```bash
# 1. 创建并推送标签
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 2. 在GitHub上创建Release
# - 访问仓库页面
# - 点击 "Releases" → "Draft a new release"
# - 选择标签 v1.0.0
# - 填写Release说明
# - 点击 "Publish release"
```

GitHub Actions会自动:
1. 运行所有测试
2. 生成文档
3. 发布技能到AgentSkills.io
4. 更新Changelog

### 手动发布

使用发布脚本:

```bash
# 设置API密钥
export AGENTSKILLS_API_KEY="your-api-key-here"

# 运行发布脚本
python .github/scripts/publish_to_agentskills.py
```

### 发布配置

编辑 `.agentskills/config.yml` 来自定义发布配置:

```yaml
# 项目信息
project:
  name: "sscisubagent-skills"
  version: "1.0.0"
  author: "socienceAI.com"
  email: "zhangshuren@freeagentskills.com"

# 技能映射
skills_mapping:
  - source: "skills/arxiv-paper-search/SKILL.md"
    target: "literature/arxiv-search"
    name: "arXiv Paper Search"
    description: "arXiv论文检索和下载"
    dependencies:
      - "requests>=2.31.0"
      - "feedparser>=6.0.10"
```

---

## 故障排查

### 常见问题

#### 1. Git推送失败

**错误**:
```
error: failed to push some refs to 'https://github.com/...'
```

**解决方案**:
```bash
# 拉取远程更改
git pull origin main --rebase

# 解决冲突后
git push origin main
```

#### 2. Python语法检查失败

**错误**:
```
SyntaxError: invalid syntax
```

**解决方案**:
```bash
# 本地检查Python语法
python -m py_compile your_file.py

# 查看详细错误
python -m py_compile your_file.py -v
```

#### 3. CI/CD工作流失败

**查看失败原因**:
1. 访问GitHub仓库
2. 点击 "Actions" 标签
3. 选择失败的工作流运行
4. 查看详细日志

**常见失败原因**:
- Python语法错误
- YAML格式错误
- 缺少依赖
- 测试失败
- Secret未配置

#### 4. AgentSkills.io发布失败

**错误**:
```
错误: 未设置AGENTSKILLS_API_KEY环境变量
```

**解决方案**:
1. 检查GitHub Secret是否配置
2. 确认Secret名称为 `AGENTSKILLS_API_KEY`
3. 重新触发工作流

#### 5. 技能验证失败

**错误**:
```
❌ 错误: 缺少YAML frontmatter
```

**解决方案**:
确保SKILL.md文件格式正确:

```markdown
---
name: skill-name
description: Skill description
tags: [tag1, tag2]
---

# Skill Title

Skill content here...
```

### 获取帮助

**文档**:
- README.md
- CONTRIBUTING.md
- RELEASE_CHECKLIST.md

**联系方式**:
- 作者: socienceAI.com
- 邮箱: zhangshuren@freeagentskills.com
- GitHub Issues: https://github.com/ptreezh/sscisubagent-skills/issues

---

## 最佳实践

### 1. 提交规范

**好的提交**:
```
feat: 添加arXiv论文检索技能

- 实现API检索功能
- 支持批量下载
- 添加完整文档

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**不好的提交**:
```
update
fix bug
添加功能
```

### 2. 版本管理

**语义化版本**:
- `MAJOR.MINOR.PATCH` (如: 1.0.0)
- MAJOR: 不兼容的API更改
- MINOR: 向后兼容的新功能
- PATCH: 向后兼容的bug修复

**发布流程**:
```bash
# 1. 更新版本号
# 2. 更新CHANGELOG.md
# 3. 创建提交
git commit -m "chore: bump version to 1.0.0"

# 4. 创建标签
git tag -a v1.0.0 -m "Release v1.0.0"

# 5. 推送
git push origin main
git push origin v1.0.0

# 6. 在GitHub创建Release
```

### 3. 分支管理

**推荐分支策略**:
- `main`: 生产环境（稳定）
- `develop`: 开发环境
- `feature/*`: 功能分支
- `hotfix/*`: 紧急修复

**工作流**:
```bash
# 创建功能分支
git checkout -b feature/new-skill

# 开发和提交
git add .
git commit -m "feat: add new skill"

# 合并到develop
git checkout develop
git merge feature/new-skill

# 删除功能分支
git branch -d feature/new-skill
```

### 4. 测试要求

**本地测试**:
```bash
# Python语法检查
python -m py_compile agents/*.py skills/*/*.py

# 技能验证
python .github/scripts/validate_skills.py

# 作者信息检查
python .github/scripts/check_author_info.py
```

**CI/CD测试**:
- 自动运行在每次push和PR
- 必须通过所有检查才能合并
- 包括多OS和多Python版本测试

---

## 相关文档

- [README.md](README.md) - 项目概述
- [CONTRIBUTING.md](CONTRIBUTING.md) - 贡献指南
- [CHANGELOG.md](CHANGELOG.md) - 变更日志
- [LICENSE](LICENSE) - 许可证

---

**维护者**: socienceAI.com
**最后更新**: 2025-12-28
**版本**: 1.0.0
