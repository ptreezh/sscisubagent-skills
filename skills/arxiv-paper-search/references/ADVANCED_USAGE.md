# arXiv论文检索技能 - 高级用法

**版本**: 1.0.0
**更新日期**: 2025-12-28

---

## 目录

1. [批量搜索策略](#批量搜索策略)
2. [结果去重与合并](#结果去重与合并)
3. [自定义筛选器](#自定义筛选器)
4. [性能优化](#性能优化)
5. [集成示例](#集成示例)
6. [自动化工作流](#自动化工作流)

---

## 批量搜索策略

### 1. 多关键词并行搜索

```python
from skills.arxiv_paper_search.scripts.arxiv_searcher import ArxivPaperSearcher
import time

searcher = ArxivPaperSearcher(debug=False)

keywords = ["GAN", "VAE", "diffusion model", "normalizing flow"]

all_results = {}

for i, keyword in enumerate(keywords, 1):
    print(f"\n[{i}/{len(keywords)}] 搜索: {keyword}")

    results = searcher.search(keyword, max_results=20)
    all_results[keyword] = results

    print(f"  找到 {len(results)} 篇")

    # 遵守API限制（内置延迟会自动处理）
    if i < len(keywords):
        time.sleep(1)

# 合并所有结果
combined = []
for results in all_results.values():
    combined.extend(results)

print(f"\n总计: {len(combined)} 篇论文")
```

### 2. 渐进式搜索策略

```python
# 第一阶段：广泛搜索
print("阶段1: 广泛搜索")
broad_results = searcher.search(
    "machine learning",
    max_results=10
)

# 分析结果，调整关键词
# ...

# 第二阶段：精准搜索
print("\n阶段2: 精准搜索")
focused_results = searcher.search(
    "transformer architecture vision",
    categories=["cs.CV", "cs.AI"],
    max_results=50
)

# 第三阶段：特定主题
print("\n阶段3: 特定主题")
specific_results = searcher.search(
    "vision transformer",
    categories=["cs.CV"],
    max_results=100
)
```

---

## 结果去重与合并

### 1. 基于arXiv ID去重

```python
def deduplicate_papers(papers):
    """去除重复论文（基于arXiv ID）"""
    seen = set()
    unique = []

    for paper in papers:
        arxiv_id = paper['arxiv_id']

        if arxiv_id not in seen:
            seen.add(arxiv_id)
            unique.append(paper)
        else:
            print(f"重复: {arxiv_id} - {paper['title'][:40]}")

    return unique

# 使用
combined = results1 + results2 + results3
unique_papers = deduplicate_papers(combined)

print(f"去重前: {len(combined)}, 去重后: {len(unique_papers)}")
```

### 2. 智能合并（保留最新版本）

```python
def merge_papers(paper_lists):
    """合并多个搜索结果，保留最新版本"""
    from collections import defaultdict

    # 按arXiv ID分组
    papers_by_id = defaultdict(list)

    for papers in paper_lists:
        for paper in papers:
            papers_by_id[paper['arxiv_id']].append(paper)

    # 选择最新版本
    merged = []
    for arxiv_id, versions in papers_by_id.items():
        # 按更新时间排序
        latest = max(versions, key=lambda p: p['updated'])
        merged.append(latest)

    return merged

# 使用
merged = merge_papers([results1, results2, results3])
```

### 3. 结果排序

```python
# 按发表时间排序
from datetime import datetime

def sort_by_date(papers, reverse=True):
    """按发表时间排序"""
    return sorted(
        papers,
        key=lambda p: p['published'],
        reverse=reverse
    )

# 按作者数量排序
def sort_by_author_count(papers):
    """按作者数量排序"""
    return sorted(
        papers,
        key=lambda p: len(p['authors']),
        reverse=True
    )

# 使用
sorted_papers = sort_by_date(results)
print("最新论文:")
for paper in sorted_papers[:5]:
    print(f"  {paper['published'][:10]} - {paper['title'][:50]}")
```

---

## 自定义筛选器

### 1. 按作者筛选

```python
def filter_by_author(papers, author_name):
    """筛选特定作者的论文"""
    filtered = []

    for paper in papers:
        if any(author_name.lower() in auth.lower()
               for auth in paper['authors']):
            filtered.append(paper)

    return filtered

# 使用
hinton_papers = filter_by_author(results, "Hinton")
print(f"Hinton的论文: {len(hinton_papers)} 篇")
```

### 2. 按分类筛选

```python
def filter_by_categories(papers, categories):
    """筛选特定分类的论文"""
    filtered = []

    for paper in papers:
        if any(cat in paper['categories'] for cat in categories):
            filtered.append(paper)

    return filtered

# 使用
ai_papers = filter_by_categories(results, ["cs.AI", "cs.LG"])
print(f"AI论文: {len(ai_papers)} 篇")
```

### 3. 按摘要长度筛选

```python
def filter_by_abstract_length(papers, min_length=200):
    """筛选摘要长度（更详细的论文）"""
    return [
        p for p in papers
        if len(p['summary']) > min_length
    ]

# 使用
detailed_papers = filter_by_abstract_length(results, min_length=500)
print(f"详细论文: {len(detailed_papers)} 篇")
```

### 4. 按关键词筛选

```python
def filter_by_keywords(papers, keywords, field='summary'):
    """在摘要/标题中筛选关键词"""
    filtered = []

    for paper in papers:
        text = paper[field].lower()

        if all(kw.lower() in text for kw in keywords):
            filtered.append(paper)

    return filtered

# 使用
transformer_papers = filter_by_keywords(
    results,
    ["transformer", "attention"],
    field='summary'
)
```

### 5. 组合筛选器

```python
def apply_filters(papers, filters):
    """应用多个筛选器"""
    result = papers

    for filter_func, filter_name in filters:
        before = len(result)
        result = filter_func(result)
        after = len(result)

        print(f"{filter_name}: {before} -> {after}")

    return result

# 使用
filters = [
    (lambda p: filter_by_categories(p, ["cs.AI"]), "分类筛选"),
    (lambda p: filter_by_abstract_length(p, 300), "摘要长度筛选"),
    (lambda p: [paper for paper in p if paper['doi']], "DOI筛选"),
]

filtered = apply_filters(results, filters)
```

---

## 性能优化

### 1. 缓存搜索结果

```python
import pickle
from pathlib import Path

class CachedArxivSearcher(ArxivPaperSearcher):
    """带缓存的搜索器"""

    def __init__(self, cache_dir='arxiv_cache'):
        super().__init__()
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def search(self, query, **kwargs):
        # 生成缓存键
        cache_key = f"{query}_{kwargs.get('max_results', 20)}"
        cache_file = self.cache_dir / f"{cache_key}.pkl"

        # 检查缓存
        if cache_file.exists():
            print(f"从缓存加载: {cache_key}")
            with open(cache_file, 'rb') as f:
                return pickle.load(f)

        # 执行搜索
        results = super().search(query, **kwargs)

        # 保存缓存
        with open(cache_file, 'wb') as f:
            pickle.dump(results, f)

        return results

# 使用
searcher = CachedArxivSearcher()
results = searcher.search("transformer")  # 第一次：搜索
results = searcher.search("transformer")  # 第二次：从缓存加载
```

### 2. 批量操作优化

```python
def batch_search_keywords(searcher, keywords, max_results=20):
    """批量搜索优化版"""
    all_results = []

    for i, keyword in enumerate(keywords, 1):
        print(f"[{i}/{len(keywords)}] {keyword}")

        results = searcher.search(keyword, max_results=max_results)
        all_results.extend(results)

        # 内置延迟已经遵守API限制
        # 但可以添加额外延迟以降低负载
        if i < len(keywords):
            time.sleep(2)

    return all_results

# 使用
keywords = ["GAN", "VAE", "diffusion"]
results = batch_search_keywords(searcher, keywords, max_results=20)
```

### 3. 内存管理（大结果集）

```python
def search_in_batches(searcher, query, total=100, batch_size=20):
    """分批搜索大量结果"""
    all_results = []

    for offset in range(0, total, batch_size):
        print(f"搜索 {offset+1}-{min(offset+batch_size, total)} 篇")

        # arXiv API支持start参数
        # 这里简化为多次搜索不同关键词
        batch_results = searcher.search(
            query,
            max_results=batch_size
        )

        if not batch_results:
            break

        all_results.extend(batch_results)

        # 处理当前批次
        # ...
        time.sleep(3)

    return all_results
```

---

## 集成示例

### 1. 与文献管理集成

```python
def create_bibtex(paper):
    """生成BibTeX条目"""
    authors = " and ".join(paper['authors'])

    bibtex = f"""@article{{{paper['arxiv_id']},
  title={{{{paper['title']}}}},
  author={{{authors}}},
  year={{{paper['published'][:4]}}}},
  eprint={{{paper['arxiv_id']}}},
  archivePrefix={{arXiv}},
  primaryClass={{{paper['categories'][0] if paper['categories'] else 'cs.AI'}}}
}}"""
    return bibtex

# 使用
for paper in results[:5]:
    print(create_bibtex(paper))
    print()
```

### 2. 与PDF分析集成

```python
def analyze_pdf_structure(pdf_path):
    """分析PDF结构（需要额外库）"""
    try:
        import PyPDF2

        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)

            num_pages = len(reader.pages)
            print(f"页数: {num_pages}")

            # 提取第一页内容
            first_page = reader.pages[0].extract_text()
            print(f"第一页预览: {first_page[:200]}")

    except Exception as e:
        print(f"分析失败: {e}")

# 下载后分析
file_path = searcher.download_pdf('2312.11805')
if file_path:
    analyze_pdf_structure(file_path)
```

### 3. 与数据库集成

```python
import sqlite3

def save_to_database(papers, db_path='papers.db'):
    """保存到SQLite数据库"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 创建表
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS papers (
            arxiv_id TEXT PRIMARY KEY,
            title TEXT,
            authors TEXT,
            summary TEXT,
            published TEXT,
            categories TEXT,
            pdf_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # 插入数据
    for paper in papers:
        cursor.execute("""
            INSERT OR REPLACE INTO papers
            (arxiv_id, title, authors, summary, published, categories, pdf_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            paper['arxiv_id'],
            paper['title'],
            '; '.join(paper['authors']),
            paper['summary'],
            paper['published'],
            '; '.join(paper['categories']),
            paper['pdf_url']
        ))

    conn.commit()
    print(f"保存 {len(papers)} 篇论文到数据库")

# 使用
save_to_database(results)
```

---

## 自动化工作流

### 1. 每日论文更新通知

```python
def daily_paper_update(topics):
    """每日论文更新"""
    from datetime import datetime, timedelta

    searcher = ArxivPaperSearcher()

    # 获取昨天到今天的论文
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")

    report = f"论文更新报告 ({today})\n"
    report += "=" * 60 + "\n\n"

    for topic in topics:
        results = searcher.search(
            topic,
            date_range={"start": yesterday, "end": today},
            max_results=10
        )

        report += f"\n## {topic}\n"
        report += f"找到 {len(results)} 篇新论文\n\n"

        for i, paper in enumerate(results[:5], 1):
            report += f"{i}. {paper['title']}\n"
            report += f"   作者: socienceAI.com
            report += f"   链接: {paper['pdf_url']}\n\n"

    return report

# 使用
topics = ["transformer", "diffusion model", "LLM"]
report = daily_paper_update(topics)

# 保存或发送报告
with open('daily_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print(report)
```

### 2. 文献调研自动化

```python
def automated_literature_review(topic, max_papers=100):
    """自动化文献调研"""
    searcher = ArxivPaperSearcher()

    print(f"主题: {topic}")
    print(f"目标: {max_papers} 篇论文\n")

    # 1. 搜索
    print("[1/4] 搜索论文...")
    results = searcher.search(topic, max_results=max_papers)
    print(f"找到 {len(results)} 篇")

    # 2. 去重
    print("\n[2/4] 去重...")
    unique = deduplicate_papers(results)
    print(f"去重后 {len(unique)} 篇")

    # 3. 筛选
    print("\n[3/4] 筛选高质量论文...")
    filtered = [p for p in unique if len(p['summary']) > 300]
    print(f"筛选后 {len(filtered)} 篇")

    # 4. 保存
    print("\n[4/4] 保存结果...")
    searcher.save_abstracts(filtered, f'{topic}_review.json')
    searcher.export_to_csv(filtered, f'{topic}_review.csv')

    # 5. 生成报告
    print("\n生成统计报告...")
    generate_statistics(filtered)

    return filtered

def generate_statistics(papers):
    """生成统计报告"""
    from collections import Counter

    # 分类分布
    all_cats = []
    for paper in papers:
        all_cats.extend(paper['categories'])
    cat_dist = Counter(all_cats)

    # 年份分布
    years = [p['published'][:4] for p in papers]
    year_dist = Counter(years)

    print("\n分类分布:")
    for cat, count in cat_dist.most_common(10):
        print(f"  {cat}: {count}")

    print("\n年份分布:")
    for year, count in sorted(year_dist.items()):
        print(f"  {year}: {count}")

# 使用
results = automated_literature_review("vision transformer", max_papers=100)
```

---

**文档版本**: 1.0.0
**最后更新**: 2025-12-28
