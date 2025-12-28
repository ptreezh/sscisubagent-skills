# arXiv论文检索技能 - 用户指南

**版本**: 1.0.0
**更新日期**: 2025-12-28

---

## 目录

1. [快速开始](#快速开始)
2. [基本用法](#基本用法)
3. [高级用法](#高级用法)
4. [搜索技巧](#搜索技巧)
5. [结果处理](#结果处理)
6. [常见问题](#常见问题)
7. [最佳实践](#最佳实践)

---

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 验证安装

```bash
python scripts/test_arxiv_searcher.py
```

---

## 基本用法

### 1. 搜索论文

```python
from skills.arxiv_paper_search.scripts.arxiv_searcher import ArxivPaperSearcher

searcher = ArxivPaperSearcher()

# 基本搜索
results = searcher.search("large language models", max_results=20)

# 查看结果
for paper in results[:5]:
    print(f"标题: {paper['title']}")
    print(f"作者: socienceAI.com
    print(f"摘要: {paper['summary'][:100]}...")
    print()
```

### 2. 下载摘要

```python
# 搜索并保存摘要
results = searcher.search("GPT", max_results=50)
searcher.save_abstracts(results, 'gpt_abstracts.json')
```

### 3. 下载PDF

```python
# 单篇下载
searcher.download_pdf('2312.11805', 'papers/')

# 批量下载
searcher.batch_download_pdfs(results[:10], 'papers/')
```

---

## 高级用法

### 1. 分类筛选

```python
# 只搜索AI和机器学习分类
results = searcher.search(
    "deep learning",
    categories=["cs.AI", "cs.LG"],
    max_results=20
)

# 查看分类分布
from collections import Counter
all_cats = []
for paper in results:
    all_cats.extend(paper['categories'])

print(Counter(all_cats))
```

### 2. 日期范围筛选

```python
# 搜索2024年的论文
results = searcher.search(
    "transformer",
    date_range={
        "start": "2024-01-01",
        "end": "2024-12-31"
    },
    max_results=50
)
```

### 3. 排序选项

```python
# 按相关性排序（默认）
results = searcher.search("attention", sort_by="relevance")

# 按最新提交排序
results = searcher.search("attention", sort_by="submittedDate")

# 按最后更新排序
results = searcher.search("attention", sort_by="lastUpdatedDate")
```

### 4. 获取最新AI论文

```python
# 最近7天的AI论文
recent = searcher.get_recent_ai_papers(days=7, max_results=20)

for paper in recent:
    print(f"{paper['title'][:60]}")
    print(f"日期: {paper['published'][:10]}")
    print()
```

---

## 搜索技巧

### 1. 使用具体关键词

```python
# ✅ 好：具体
results = searcher.search("BERT pre-training language model")

# ❌ 差：太宽泛
results = searcher.search("model")
```

### 2. 组合搜索

```python
# 使用AND/OR逻辑（arXiv API支持）
results = searcher.search("all:transformer AND all:attention")
```

### 3. 字段限定

```python
# 在标题中搜索
results = searcher.search("ti:large language models")

# 在摘要中搜索
results = searcher.search("abs:fine-tuning")

# 在作者中搜索
results = searcher.search("au:Hinton")
```

### 4. 分类聚焦

```python
# 聚焦特定领域
ai_papers = searcher.search("RL", categories=["cs.AI"])
ml_papers = searcher.search("optimization", categories=["cs.LG", "stat.ML"])
nlp_papers = searcher.search("embedding", categories=["cs.CL"])
```

---

## 结果处理

### 1. JSON导出

```python
results = searcher.search("GAN", max_results=50)

# 保存完整数据
searcher.save_abstracts(results, 'gan_papers.json')

# 加载并分析
import json
with open('gan_papers.json', 'r') as f:
    papers = json.load(f)

print(f"共保存 {len(papers)} 篇论文")
```

### 2. CSV导出

```python
# 导出为CSV
searcher.export_to_csv(results, 'gan_papers.csv')

# 在Excel中打开分析
```

### 3. 自定义筛选

```python
# 筛选有DOI的论文
papers_with_doi = [p for p in results if p['doi']]

# 筛选特定作者
hinton_papers = [p for p in results if any('Hinton' in auth for auth in p['authors'])]

# 筛选长摘要
detailed_papers = [p for p in results if len(p['summary']) > 500]
```

---

## 常见问题

### Q: 为什么搜索结果少于指定数量？

A: 可能原因：
1. arXiv上该主题的论文确实很少
2. 搜索条件过于严格
3. 分类筛选限制了结果

解决方案：
- 使用更宽泛的关键词
- 移除分类筛选
- 增加时间范围

### Q: 下载PDF失败？

A: 可能原因：
1. 网络连接问题
2. 论文尚未发布PDF
3. arXiv ID不正确

解决方案：
- 检查网络连接
- 使用`paper['pdf_url']`在浏览器中验证
- 确认arXiv ID格式正确（如"2312.11805"）

### Q: 搜索速度慢？

A: 这是正常的，因为：
- API请求延迟（遵守每3秒1次的限制）
- 数据传输时间
- 大量结果时的解析时间

优化建议：
- 使用更小的`max_results`
- 添加分类筛选减少无关结果
- 批量操作时一次性搜索多个关键词

### Q: 如何只下载开源论文？

A: arXiv本身都是开源的，但部分论文可能同时发表在期刊上。建议：
- 优先使用arXiv版本
- 检查`paper['journal_ref']`字段
- 尊重期刊版权政策

---

## 最佳实践

### 1. 分阶段搜索策略

```python
# 第一阶段：快速预览（10篇）
preview = searcher.search("topic", max_results=10)

# 根据预览结果调整关键词
# 第二阶段：深度搜索（50篇）
deep = searcher.search("refined topic", max_results=50)

# 第三阶段：下载重要论文
searcher.batch_download_pdfs(deep[:10], 'papers/')
```

### 2. 批量操作优化

```python
keywords = ["GAN", "VAE", "diffusion model"]

all_results = []
for kw in keywords:
    results = searcher.search(kw, max_results=20)
    all_results.extend(results)

# 去重（基于arXiv ID）
seen = set()
unique_results = []
for paper in all_results:
    if paper['arxiv_id'] not in seen:
        seen.add(paper['arxiv_id'])
        unique_results.append(paper)

print(f"去重后: {len(unique_results)} 篇")
```

### 3. 元数据管理

```python
# 添加搜索时间戳
from datetime import datetime

search_metadata = {
    "query": "transformer",
    "search_date": datetime.now().isoformat(),
    "total_results": len(results),
    "papers": results
}

with open('search_results.json', 'w') as f:
    json.dump(search_metadata, f, indent=2)
```

### 4. 进度跟踪

```python
# 批量下载时显示进度
papers = results[:20]

for i, paper in enumerate(papers, 1):
    print(f"\n[{i}/{len(papers)}] 下载: {paper['title'][:40]}")
    searcher.download_pdf(paper['arxiv_id'], 'papers/')
```

---

## 许可和免责

- ✅ 仅用于学术研究和教育目的
- ✅ 遵守arXiv API使用条款
- ✅ 尊重论文作者版权
- ❌ 不用于商业用途
- ❌ 不用于大规模数据采集
- ✅ 正确引用原始论文

---

**文档版本**: 1.0.0
**最后更新**: 2025-12-28
