# 开源发布准备清单 / Open Source Release Checklist

本文档提供开源发布的完整检查清单。

This document provides a comprehensive checklist for open source release.

---

## ✅ 文档检查 / Documentation Check

### 必需文档 / Required Documents

- [x] **README.md** - 项目概述和快速开始指南
- [x] **LICENSE** - MIT 开源许可证
- [x] **CONTRIBUTING.md** - 贡献指南
- [x] **requirements.txt** - 生产依赖
- [x] **requirements-dev.txt** - 开发依赖
- [x] **pyproject.toml** - 项目配置
- [x] **.gitignore** - Git 忽略规则

### 推荐文档 / Recommended Documents

- [ ] **CHANGELOG.md** - 版本更新日志
- [ ] **SECURITY.md** - 安全政策
- [ ] **CODE_OF_CONDUCT.md** - 社区行为准则
- [ ] **docs/** - 详细文档目录
  - [ ] API.md - API 文档
  - [ ] CASE_STUDIES.md - 案例研究
  - [ ] TROUBLESHOOTING.md - 故障排除

---

## 🧹 代码清理 / Code Cleanup

### 文件清理 / File Cleanup

- [x] 删除测试输出文件 (JSON, HTML)
- [x] 删除临时脚本和测试文件
- [x] 删除日志文件
- [x] 移动测试脚本到 tests/ 目录
- [ ] 删除 `project_backup/` 目录
- [ ] 清理 `desktop_design/` 临时文件
- [ ] 删除 `archive/skills_copy/` 冗余副本

### 代码质量 / Code Quality

- [ ] 确保所有 Python 文件有类型提示
- [ ] 确保所有函数有文档字符串
- [ ] 运行代码格式化工具 (black, isort)
- [ ] 修复所有 linting 警告
- [ ] 检查是否有硬编码的敏感信息

```bash
# 代码格式化 / Code formatting
black skills/ agents/ tests/
isort skills/ agents/ tests/

# Lint 检查 / Lint check
flake8 skills/ agents/ tests/

# 类型检查 / Type checking
mypy skills/
```

---

## 🔒 安全检查 / Security Check

### 敏感信息 / Sensitive Information

- [ ] 检查是否有 API 密钥
- [ ] 检查是否有密码
- [ ] 检查是否有个人邮箱/电话
- [ ] 检查是否有内部 URL
- [ ] 使用 `git grep` 搜索敏感词:

```bash
# 搜索敏感信息 / Search sensitive info
git grep -i "password"
git grep -i "api_key"
git grep -i "secret"
git grep -i "token"
```

### 依赖安全 / Dependency Security

- [ ] 更新所有依赖到最新稳定版
- [ ] 运行安全扫描工具:

```bash
# 使用 pip-audit 检查依赖漏洞
pip install pip-audit
pip-audit

# 或使用 safety
pip install safety
safety check
```

---

## 🧪 测试检查 / Testing Check

### 测试覆盖率 / Test Coverage

- [ ] 编写核心功能的单元测试
- [ ] 编写集成测试
- [ ] 检查测试覆盖率 (目标: >70%)
- [ ] 确保所有测试通过

```bash
# 运行测试 / Run tests
pytest tests/ -v

# 生成覆盖率报告 / Generate coverage report
pytest tests/ --cov=skills --cov-report=html
```

### 功能验证 / Functionality Verification

- [ ] 验证核心技能可以正常加载
- [ ] 验证示例代码可以运行
- [ ] 测试 CLI 集成
- [ ] 测试跨平台兼容性 (Windows/Linux/Mac)

---

## 📦 打包和分发 / Packaging & Distribution

### 包配置 / Package Configuration

- [x] pyproject.toml 配置完整
- [x] setup.cfg (如果需要)
- [x] MANIFEST.in (如果需要)

### 构建测试 / Build Test

```bash
# 构建源码分发包 / Build source distribution
python -m build

# 检查包内容
tar -tzf dist/ssci_subagent_skills-*.tar.gz

# 测试安装
pip install dist/ssci_subagent_skills-*.tar.gz
```

---

## 📝 版本管理 / Version Management

### 版本号 / Version Number

- [ ] 确认当前版本号 (遵循语义化版本)
- [ ] 创建 git tag:

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### 更新日志 / Changelog

- [ ] 创建 CHANGELOG.md
- [ ] 记录所有重要变更
- [ ] 标注破坏性变更

---

## 🌐 Git 仓库设置 / Git Repository Setup

### GitHub 设置 / GitHub Settings

- [ ] 创建 GitHub 仓库
- [ ] 设置仓库描述
- [ ] 添加 topics 标签
- [ ] 启用 Issues
- [ ] 启用 Discussions
- [ ] 设置分支保护规则 (main 分支)
- [ ] 添加 LICENSE 文件显示
- [ ] 配置自动链接

### GitHub 功能 / GitHub Features

- [ ] 创建 README.md 徽章
- [ ] 设置 GitHub Actions CI/CD
- [ ] 配置 Dependabot
- [ ] 添加 issue 模板
- [ ] 添加 PR 模板

---

## 📢 发布准备 / Release Preparation

### 发布公告 / Release Announcement

- [ ] 准备 GitHub Release 说明
- [ ] 创建 Release Notes
- [ ] 准备演示材料 (截图/GIF)

### 社区准备 / Community Preparation

- [ ] 准备社交媒体发布
- [ ] 准备邮件列表公告
- [ ] 准备技术博客文章
- [ ] 联系相关社区

---

## 🔍 最终检查 / Final Review

### 发布前检查 / Pre-release Check

- [ ] 所有文档完整且准确
- [ ] 所有测试通过
- [ ] 无安全漏洞
- [ ] 无敏感信息
- [ ] 代码格式一致
- [ ] 版本号正确
- [ ] 许可证文件存在

### 回滚计划 / Rollback Plan

- [ ] 准备回滚方案
- [ ] 记录已知问题
- [ ] 准备紧急修复流程

---

## 📋 发布后任务 / Post-release Tasks

- [ ] 监控 Issues 和 PRs
- [ ] 收集用户反馈
- [ ] 修复紧急 bug
- [ ] 规划下一版本
- [ ] 更新文档

---

## 🚀 快速发布命令 / Quick Release Commands

```bash
# 1. 最终代码检查 / Final code check
git status
git diff

# 2. 运行测试 / Run tests
pytest tests/ -v

# 3. 构建包 / Build package
python -m build

# 4. 创建标签 / Create tag
git tag -a v1.0.0 -m "Release v1.0.0"

# 5. 推送到 GitHub / Push to GitHub
git push origin main
git push origin v1.0.0

# 6. 发布到 PyPI (可选) / Publish to PyPI (optional)
twine upload dist/*
```

---

## ✨ 完成标准 / Completion Criteria

当以下所有条件满足时，项目准备好发布：

When all the following conditions are met, the project is ready for release:

- ✅ 所有必需文档完整
- ✅ 代码清理完成
- ✅ 安全检查通过
- ✅ 核心测试通过
- ✅ 版本号正确设置
- ✅ Git 仓库配置完成
- ✅ 发布公告准备完毕

---

**祝发布顺利！ / Good luck with your release!** 🎉
