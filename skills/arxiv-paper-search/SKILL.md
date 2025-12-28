---
name: arxiv-paper-search
description: 在arXiv学术平台检索、下载论文摘要和全文PDF，支持批量下载和智能筛选。当用户需要搜索英文学术论文、下载论文摘要或获取PDF全文时使用此技能。
version: 1.0.0
author: socienceAI.com
license: MIT
tags: [literature-search, arxiv, paper-download, academic-search, pdf-download]
compatibility: Claude 3.5 Sonnet and above
metadata:
  domain: literature-search
  methodology: api-based
  complexity: intermediate
  integration_type: api-integration
  last_updated: "2025-12-28"
  website: https://arxiv.org
  language: bilingual
allowed-tools: [python, requests, urllib]
---

# arXiv论文检索与下载技能 (arXiv Paper Search & Download)

## Overview

在arXiv学术平台（https://arxiv.org/）自动检索英文学术论文，支持批量下载摘要和PDF全文，提供智能筛选和多数量选项。

## When to Use This Skill

Use this skill when the user requests:
- 搜索英文学术论文 ("搜索关于...的论文")
- 在arXiv查找学术论文
- 下载论文摘要或全文
- 批量获取arXiv论文
- 查找AI/CS/物理等领域的最新研究
- 论文文献调研
- 检索arXiv论文、查找学术论文、下载英文文献

## Quick Start

When user needs arXiv paper search:
1. **识别**搜索关键词和领域
2. **执行**arXiv API搜索
3. **选择**返回数量（10/20/50/100篇）
4. **提取**论文摘要和元数据
5. **下载**PDF全文（可选）
6. **返回**结构化结果列表

## 使用时机

当用户提到以下需求时，使用此技能：
- "搜索" + "论文" / "学术论文" / "英文学术论文" / "英文文献"
- "在arXiv" / "arxiv" / "arXiv平台" 搜索
- "下载论文" / "获取论文PDF" / "下载全文"
- "论文摘要" / "abstract" / "论文摘要"
- "批量下载" + "论文" / "文献"
- 查找特定领域（AI、ML、CS、深度学习等）的最新研究
- "arXiv检索" / "文献检索" / "学术论文检索"
- "查找英文论文" / "搜索国外论文"

**关键词触发（中文）**:
- arXiv检索、arXiv搜索、arXiv论文
- 英文论文、英文学术论文、英文文献
- 论文检索、文献检索、学术论文搜索
- 下载论文、论文下载、PDF下载
- 论文摘要、摘要下载
- 批量下载、批量获取论文
- AI论文、机器学习论文、深度学习论文
- 国外论文、外文论文

**关键词触发（英文）**:
- arXiv、arxiv search
- paper search、paper download
- academic paper、research paper
- download paper、PDF download
- abstract、paper abstract
- AI papers、ML papers

## 核心功能

### 1. 智能论文检索

**支持功能**:
- 关键词搜索（标题、摘要、作者）
- 分类筛选（cs.AI, cs.LG, stat.ML等）
- 时间范围筛选
- 排序方式（相关性/最新/引用数）

### 2. 摘要批量下载

**支持数量选项**:
- 10篇（快速预览）
- 20篇（中等调研）
- 50篇（深度调研）
- 100篇（全面覆盖）

**提取信息**:
- 标题 (title)
- 作者列表 (authors)
- 摘要 (abstract)
- 发表时间 (published)
- arXiv ID
- PDF链接 (pdf_url)
- 分类标签 (categories)
- DOI（如果有）

### 3. PDF全文下载

**下载功能**:
- 单篇PDF下载
- 批量PDF下载
- 断点续传
- 下载进度显示

## 脚本调用

```python
from skills.arxiv_paper_search.scripts.arxiv_searcher import ArxivPaperSearcher

# 初始化
searcher = ArxivPaperSearcher()

# 搜索论文（获取摘要）
results = searcher.search(
    query="large language models",
    max_results=20,        # 可选: 10, 20, 50, 100
    sort_by="relevance"    # relevance, lastUpdatedDate, submittedDate
)

# 下载单篇PDF
searcher.download_pdf(
    arxiv_id="2312.11805",
    output_dir="papers/"
)

# 批量下载PDF
searcher.batch_download_pdfs(
    results=results,
    output_dir="papers/",
    max_papers=10
)
```

**参数说明**:
- `query`: 搜索关键词（必需）
- `max_results`: 返回结果数（默认20，可选10/20/50/100）
- `sort_by`: 排序方式（默认relevance）
- `categories`: arXiv分类筛选（可选）
- `filters`: 额外筛选条件（可选）

## 统一输入格式

```json
{
  "search_request": {
    "query": "搜索关键词（必需）",
    "max_results": 20,
    "sort_by": "relevance",
    "categories": ["cs.AI", "cs.LG"],
    "date_range": {
      "start": "2024-01-01",
      "end": "2024-12-31"
    }
  },
  "download_request": {
    "arxiv_id": "2312.11805",
    "output_dir": "papers/",
    "download_abstract": true,
    "download_pdf": false
  }
}
```

## 统一输出格式

```json
{
  "search_summary": {
    "query": "large language models",
    "total_results": 20,
    "search_time_seconds": 2.3
  },
  "papers": [
    {
      "index": 1,
      "title": "Attention Is All You Need",
      "authors": ["Vaswani, A.", "Shazeer, N.", "Parmar, N."],
      "summary": "The dominant sequence transduction models...",
      "published": "2017-06-12",
      "updated": "2017-06-12",
      "arxiv_id": "1706.03762",
      "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
      "categories": ["cs.CL", "cs.LG"],
      "doi": "10.1234/arxiv.1706.03762",
      "comment": "8 pages, 5 figures",
      "journal_ref": "NIPS 2017"
    }
  ]
}
```

## 数量参数映射

| 数量 | 适用场景 | 响应时间 | 数据量 |
|------|---------|---------|--------|
| 10篇 | 快速预览、初步调研 | ~1-2秒 | ~50KB |
| 20篇 | 中等调研（推荐） | ~2-3秒 | ~100KB |
| 50篇 | 深度调研 | ~5-8秒 | ~250KB |
| 100篇 | 全面覆盖、批量分析 | ~10-15秒 | ~500KB |

## arXiv分类参考

### 计算机科学 (cs)
- `cs.AI` - 人工智能
- `cs.CL` - 计算语言学
- `cs.CV` - 计算机视觉
- `cs.LG` - 机器学习
- `cs.NE` - 神经网络
- `cs.CR` - 加密学

### 数学 (math)
- `math.OC` - 优化与控制
- `math.ST` - 统计理论

### 物理学 (physics)
- `physics.comp-ph` - 计算物理
- `quant-ph` - 量子物理

### 统计学 (stat)
- `stat.ML` - 机器学习统计

## 参考文档

详细文档请查看：
- `references/USER_GUIDE.md` - 完整使用指南
- `references/API_REFERENCE.md` - API参考
- `references/ARXIV_CATEGORIES.md` - arXiv完整分类列表
- `references/ADVANCED_USAGE.md` - 高级用法和最佳实践

## 依赖要求

**最小依赖**（只包含必需的2个库）:
```bash
# 方法1: 使用 uv（推荐，极快）
uv pip install -r requirements.txt

# 方法2: 使用 pip（传统）
pip install -r requirements.txt
```

**依赖列表**:
- `requests>=2.31.0` - HTTP请求
- `feedparser>=6.0.10` - 解析arXiv API响应

**安装说明**:
- 总大小: ~300 KB（优化前 5 MB）
- 安装时间: ~1秒（uv）或 ~10秒（pip）
- Python版本要求: >=3.8

**测试**:
```bash
python scripts/test_arxiv_searcher.py
```

## 示例用法

### 示例1: 基本搜索
```python
# 用户: "在arXiv搜索关于LLM的论文"
searcher = ArxivPaperSearcher()
results = searcher.search("large language models", max_results=20)

for paper in results[:5]:
    print(f"{paper['title']}")
    print(f"{paper['summary'][:100]}...")
```

### 示例2: 下载摘要
```python
# 用户: "下载50篇GPT相关论文的摘要"
results = searcher.search("GPT", max_results=50)
searcher.save_abstracts(results, 'gpt_abstracts.json')
```

### 示例3: 批量下载PDF
```python
# 用户: "下载10篇最新AI论文的PDF"
results = searcher.search(
    "artificial intelligence",
    categories=["cs.AI"],
    sort_by="lastUpdatedDate",
    max_results=10
)
searcher.batch_download_pdfs(results, 'ai_papers/')
```

## 注意事项

⚠️ **重要声明**:
- 仅用于学术研究和教育目的
- 遵守arXiv API使用条款（每3秒最多1次请求）
- 尊重论文作者版权
- 批量下载时建议添加延迟避免过载
- PDF仅供个人学习使用

✅ **最佳实践**:
- 建议单次搜索不超过100篇论文
- 使用具体关键词提高搜索精度
- 优先使用摘要筛选，再下载PDF
- 批量下载时每次间隔2-3秒
- 正确引用原始论文（包含arXiv ID）

## 与其他技能的配合

- **pubscholar-auto-search**: 检索中文论文
- **arxiv-paper-search**: 检索英文论文（本技能）
- 两者配合实现中英文文献全覆盖

---

**版本**: 1.0.0
**最后更新**: 2025-12-28
**维护者**: SSCI Research Tools
