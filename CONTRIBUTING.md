# 贡献指南 / Contributing Guide

感谢您考虑为 SSCI Subagent Skills 项目做出贡献！

Thank you for considering contributing to SSCI Subagent Skills!

---

## 如何贡献 / How to Contribute

### 报告问题 / Reporting Issues

如果您发现了bug或有功能建议：

If you found a bug or have a feature request:

1. 检查 [Issues](https://github.com/yourusername/sscisubagent-skills/issues) 确保问题未被报告
   Check existing issues to avoid duplicates
2. 创建新Issue，使用清晰的标题和详细描述
   Create a new issue with a clear title and detailed description
3. 提供重现步骤、预期行为和实际行为
   Include steps to reproduce, expected behavior, and actual behavior
4. 如果可能，添加截图或代码示例
   Add screenshots or code examples if applicable

### 提交代码 / Submitting Code

#### 1. Fork 仓库 / Fork the Repository

```bash
# Fork 项目到您的 GitHub 账户
# Fork the project to your GitHub account
git clone https://github.com/ptreezh/sscisubagent-skills.git
cd sscisubagent-skills
```

#### 2. 创建分支 / Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

#### 3. 进行修改 / Make Changes

遵循以下规范：

Follow these guidelines:

- **代码风格 / Code Style**:
  - Python: 遵循 PEP 8
  - 使用 `black` 格式化代码
  - 使用 `isort` 排序导入

- **提交信息 / Commit Messages**:
  ```
  feat: 添加新技能功能
  fix: 修复网络分析中的bug
  docs: 更新README文档
  test: 添加单元测试
  refactor: 重构代码结构
  ```

#### 4. 编写测试 / Write Tests

```bash
# 为新功能编写测试
# Write tests for new features
pytest tests/your_new_test.py

# 确保所有测试通过
# Ensure all tests pass
pytest tests/
```

#### 5. 提交 Pull Request / Submit a Pull Request

```bash
git add .
git commit -m "feat: 添加您的功能描述"
git push origin feature/your-feature-name
```

然后到 GitHub 创建 Pull Request。

Then create a Pull Request on GitHub.

---

## 开发规范 / Development Standards

### 技能开发 / Skill Development

#### 技能结构 / Skill Structure

每个技能必须遵循以下结构：

Each skill must follow this structure:

```
skill-name/
├── SKILL.md              # 技能定义文件（包含YAML frontmatter）
├── scripts/              # Python实现脚本
│   └── analyzer.py
├── references/           # 参考资料
│   ├── theory.md
│   ├── examples.md
│   └── troubleshooting.md
└── algorithms/           # 可选：算法实现
    └── advanced_method.py
```

#### SKILL.md 模板 / SKILL.md Template

```markdown
---
name: skill-name
description: 技能的简短描述
version: 1.0.0
author: your-name
license: MIT
tags: [tag1, tag2, tag3]
compatibility: Claude 3.5 Sonnet and above
metadata:
  domain: research-domain
  methodology: method-name
  complexity: intermediate
  integration_type: analysis_tool
  last_updated: "2025-12-28"
allowed-tools: [python, bash, read_file, write_file]
---

# 技能名称 / Skill Name

## 概述 / Overview

简要描述技能的功能和用途。

Brief description of the skill's functionality.

## 使用时机 / When to Use

描述何时应该使用此技能。

Describe when this skill should be used.

## 核心功能 / Core Features

- 功能1
- 功能2
- 功能3
```

#### 代码规范 / Code Standards

1. **类型提示 / Type Hints**:
   ```python
   def analyze_data(data: List[Dict]) -> Dict[str, Any]:
       """分析数据并返回结果"""
       pass
   ```

2. **文档字符串 / Docstrings**:
   ```python
   def process_network(network_data: Dict) -> Dict:
       """
       处理网络数据

       Args:
           network_data: 网络数据字典

       Returns:
           处理后的网络数据

       Raises:
           ValueError: 当数据格式不正确时
       """
       pass
   ```

3. **错误处理 / Error Handling**:
   ```python
   try:
       result = process_data(data)
   except ValueError as e:
       logger.error(f"数据处理失败: {e}")
       raise
   ```

---

## 测试要求 / Testing Requirements

### 测试覆盖率 / Test Coverage

- 新代码的测试覆盖率应至少达到 80%
- Test coverage for new code should be at least 80%

### 测试类型 / Test Types

1. **单元测试 / Unit Tests**:
   ```python
   def test_open_coding():
       expert = GroundedTheoryExpert()
       concepts = expert.perform_open_coding(test_data)
       assert len(concepts) > 0
   ```

2. **集成测试 / Integration Tests**:
   ```python
   def test_full_analysis_pipeline():
       result = run_complete_analysis(sample_data)
       assert 'theory' in result
   ```

3. **端到端测试 / End-to-End Tests**:
   ```python
   def test_real_world_scenario():
       # 使用真实数据测试
       # Test with real data
       pass
   ```

---

## 文档要求 / Documentation Requirements

### 必需文档 / Required Documentation

1. **SKILL.md**: 技能的主要文档
2. **API文档**: 函数和类的详细说明
3. **使用示例**: 实际使用案例
4. **参考资料**: 理论背景和方法说明

### 文档语言 / Documentation Language

- 主要使用中文
- 关键术语提供英文翻译
- 代码注释使用英文

---

## 代码审查流程 / Code Review Process

1. **自动检查 / Automated Checks**:
   - 代码格式化检查
   - 类型检查 (mypy)
   - 测试覆盖率检查

2. **人工审查 / Manual Review**:
   - 代码质量评估
   - 最佳实践检查
   - 文档完整性验证

3. **审查标准 / Review Criteria**:
   - ✅ 代码符合项目规范
   - ✅ 测试充分且通过
   - ✅ 文档完整清晰
   - ✅ 没有引入新的警告
   - ✅ 向后兼容性良好

---

## 社区规范 / Community Guidelines

### 行为准则 / Code of Conduct

- 尊重所有贡献者
- Constructive feedback
- 包容和欢迎的态度
- 专注于技术讨论

### 沟通渠道 / Communication Channels

- GitHub Issues: 问题报告和功能讨论
- GitHub Discussions: 一般讨论和问答
- Pull Requests: 代码审查和技术讨论

---

## 获得帮助 / Getting Help

如果您需要帮助：

If you need help:

1. 查看 [README.md](README.md)
2. 浏览现有 Issues
3. 在 GitHub Discussions 提问
4. 联系维护者

---

## 许可证 / License

通过贡献代码，您同意您的贡献将在与项目相同的 MIT 许可证下发布。

By contributing code, you agree that your contributions will be licensed under the same MIT License as the project.

---

## 致谢 / Acknowledgments

感谢所有贡献者的努力！

Thank you to all contributors for your efforts!
