# arXiv论文检索与下载技能

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![arXiv API](https://img.shields.io/badge/arXiv-API-green.svg)](https://arxiv.org/help/api)

**版本**: 1.0.0
**网站**: https://arxiv.org

---

## 快速开始

```bash
# 方法1: 使用 uv（推荐，极快）
uv pip install -r requirements.txt

# 方法2: 使用 pip（传统）
pip install -r requirements.txt

# 运行测试
python scripts/test_arxiv_searcher.py
```

## 基本使用

```python
from skills.arxiv_paper_search.scripts.arxiv_searcher import ArxivPaperSearcher

searcher = ArxivPaperSearcher()

# 搜索论文
results = searcher.search("large language models", max_results=20)

# 保存摘要
searcher.save_abstracts(results, 'abstracts.json')

# 下载PDF
searcher.download_pdf('2312.11805', 'papers/')
```

## 文档

- **[SKILL.md](SKILL.md)** - 技能主控文档（AI入口点）
- **[references/USER_GUIDE.md](references/USER_GUIDE.md)** - 用户指南
- **[references/API_REFERENCE.md](references/API_REFERENCE.md)** - API参考
- **[references/ARXIV_CATEGORIES.md](references/ARXIV_CATEGORIES.md)** - arXiv完整分类列表
- **[references/ADVANCED_USAGE.md](references/ADVANCED_USAGE.md)** - 高级用法

## 核心特性

- **智能论文检索**: 基于arXiv API，支持关键词、分类、日期筛选
- **批量摘要下载**: 支持10/20/50/100篇选项
- **PDF全文下载**: 单篇/批量下载，遵守API频率限制
- **多格式导出**: JSON、CSV格式
- **分类筛选**: 支持cs.AI、cs.LG等arXiv分类

## 使用场景

当用户提到以下需求时，AI应自动调用此技能：

- "搜索英文学术论文/论文"
- "在arXiv搜索..."
- "下载论文摘要/PDF"
- "查找AI/ML/CS领域的最新研究"
- 关键词: **arXiv、paper search、download paper、abstract**

## 数量参数

| 数量 | 适用场景 | 响应时间 |
|------|---------|---------|
| 10篇 | 快速预览 | ~1-2秒 |
| 20篇 | 中等调研（推荐） | ~2-3秒 |
| 50篇 | 深度调研 | ~5-8秒 |
| 100篇 | 全面覆盖 | ~10-15秒 |

## 与其他技能配合

- **pubscholar-auto-search**: 检索中文论文
- **arxiv-paper-search**: 检索英文论文（本技能）
- 两者配合实现中英文文献全覆盖

## 许可

MIT License - 仅用于学术研究和教育目的

---

**维护者**: SSCI Research Tools
**最后更新**: 2025-12-28
