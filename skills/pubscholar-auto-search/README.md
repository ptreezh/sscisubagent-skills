# PubScholar自动搜索技能

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/Playwright-1.40+-green.svg)](https://playwright.dev/)

**版本**: 1.0.0
**网站**: https://pubscholar.cn

---

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt
playwright install chromium

# 运行测试
python scripts/test_pubscholar_search.py
```

## 基本使用

```python
from skills.pubscholar_auto_search.scripts.pubscholar_searcher import SynchronousPubScholarSearcher

searcher = SynchronousPubScholarSearcher()
results = searcher.search("数字鸿沟")

# 导出结果
searcher.export_to_csv(results, 'results.csv')
```

## 文档

- **[SKILL.md](SKILL.md)** - 技能主控文档（AI入口点）
- **[references/USER_GUIDE.md](references/USER_GUIDE.md)** - 用户指南
- **[references/API_REFERENCE.md](references/API_REFERENCE.md)** - API参考
- **[references/DEVELOPMENT.md](references/DEVELOPMENT.md)** - 开发文档
- **[references/EXTENSION_STRATEGIES.md](references/EXTENSION_STRATEGIES.md)** - 扩展策略详解

## 核心特性

- **智能双阶段搜索**: 精准搜索 + 自动扩展
- **自适应扩展**: 结果<5篇时自动添加相关词
- **完整元数据提取**: 标题、作者、期刊、摘要、关键词
- **多格式导出**: JSON、CSV、GB/T 7714引用格式

## 使用场景

当用户提到以下需求时，AI应自动调用此技能：

- "搜索中文论文/文献/专利"
- "在PubScholar搜索..."
- "查找中文学术资源"
- "文献检索（中文）"

## 许可

MIT License - 仅用于学术研究和教育目的

---

**维护者**: SSCI Research Tools
**最后更新**: 2025-12-28
