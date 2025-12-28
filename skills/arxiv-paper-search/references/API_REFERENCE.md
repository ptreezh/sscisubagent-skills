# arXiv论文检索技能 - API参考

**版本**: 1.0.0
**更新日期**: 2025-12-28

---

## 类概览

```
ArxivPaperSearcher
    ├── search()              # 主搜索方法
    ├── download_pdf()        # 下载单篇PDF
    ├── batch_download_pdfs() # 批量下载PDF
    ├── save_abstracts()      # 保存摘要到JSON
    ├── export_to_csv()       # 导出到CSV
    └── get_recent_ai_papers() # 获取最近AI论文
```

---

## ArxivPaperSearcher

主要的arXiv论文检索与下载器。

### 初始化

```python
ArxivPaperSearcher(debug: bool = False)
```

**参数**:
- `debug` (bool): 是否启用调试模式，默认False

**示例**:
```python
searcher = ArxivPaperSearcher(debug=True)
```

### search()

搜索arXiv论文。

```python
def search(
    self,
    query: str,
    max_results: int = 20,
    sort_by: str = "relevance",
    categories: Optional[List[str]] = None,
    date_range: Optional[Dict[str, str]] = None
) -> List[Dict]
```

**参数**:
- `query` (str, 必需): 搜索关键词
- `max_results` (int): 返回结果数，可选[10, 20, 50, 100]，默认20
- `sort_by` (str): 排序方式，可选["relevance", "lastUpdatedDate", "submittedDate"]，默认"relevance"
- `categories` (List[str]): arXiv分类列表（如["cs.AI", "cs.LG"]）
- `date_range` (Dict): 日期范围 {"start": "YYYY-MM-DD", "end": "YYYY-MM-DD"}

**返回**: List[Dict] - 论文列表

**示例**:
```python
# 基本搜索
results = searcher.search("large language models")

# 指定数量
results = searcher.search("GPT", max_results=50)

# 分类筛选
results = searcher.search("RL", categories=["cs.AI"])

# 日期筛选
results = searcher.search(
    "transformer",
    date_range={"start": "2024-01-01", "end": "2024-12-31"}
)

# 组合使用
results = searcher.search(
    query="attention",
    max_results=50,
    categories=["cs.AI", "cs.LG"],
    sort_by="submittedDate"
)
```

### download_pdf()

下载单篇论文PDF。

```python
def download_pdf(
    self,
    arxiv_id: str,
    output_dir: str = "papers/",
    filename: Optional[str] = None
) -> Optional[str]
```

**参数**:
- `arxiv_id` (str, 必需): arXiv ID（如"2312.11805"）或完整URL
- `output_dir` (str): 输出目录，默认"papers/"
- `filename` (str): 自定义文件名（可选）

**返回**: str - 保存的文件路径，失败返回None

**示例**:
```python
# 使用arXiv ID
file_path = searcher.download_pdf('2312.11805')

# 指定输出目录
file_path = searcher.download_pdf('2312.11805', output_dir='my_papers/')

# 自定义文件名
file_path = searcher.download_pdf('2312.11805', filename='attention.pdf')
```

### batch_download_pdfs()

批量下载论文PDF。

```python
def batch_download_pdfs(
    self,
    papers: List[Dict],
    output_dir: str = "papers/",
    max_papers: Optional[int] = None,
    delay: float = 3.0
) -> List[str]
```

**参数**:
- `papers` (List[Dict], 必需): 论文列表（来自search方法）
- `output_dir` (str): 输出目录，默认"papers/"
- `max_papers` (int): 最大下载数量
- `delay` (float): 每次下载间隔（秒），默认3.0

**返回**: List[str] - 成功下载的文件路径列表

**示例**:
```python
# 搜索论文
results = searcher.search("GAN", max_results=20)

# 下载所有论文
files = searcher.batch_download_pdfs(results)

# 限制下载数量
files = searcher.batch_download_pdfs(results, max_papers=5)

# 自定义间隔
files = searcher.batch_download_pdfs(results, delay=5.0)
```

### save_abstracts()

保存论文摘要到JSON文件。

```python
def save_abstracts(
    self,
    papers: List[Dict],
    output_file: str = "abstracts.json"
)
```

**参数**:
- `papers` (List[Dict], 必需): 论文列表
- `output_file` (str): 输出文件名，默认"abstracts.json"

**示例**:
```python
results = searcher.search("BERT", max_results=50)
searcher.save_abstracts(results, 'bert_abstracts.json')
```

### export_to_csv()

导出论文信息到CSV文件。

```python
def export_to_csv(
    self,
    papers: List[Dict],
    output_file: str = "papers.csv"
)
```

**参数**:
- `papers` (List[Dict], 必需): 论文列表
- `output_file` (str): 输出文件名，默认"papers.csv"

**示例**:
```python
results = searcher.search("diffusion", max_results=100)
searcher.export_to_csv(results, 'diffusion_papers.csv')
```

### get_recent_ai_papers()

获取最近AI领域的论文。

```python
def get_recent_ai_papers(
    self,
    days: int = 7,
    max_results: int = 20
) -> List[Dict]
```

**参数**:
- `days` (int): 最近几天，默认7
- `max_results` (int): 最大结果数，默认20

**返回**: List[Dict] - 论文列表

**示例**:
```python
# 最近7天
recent = searcher.get_recent_ai_papers(days=7)

# 最近30天，50篇
recent = searcher.get_recent_ai_papers(days=30, max_results=50)
```

---

## 数据模型

### 论文对象 (Paper)

```json
{
  "index": 1,
  "title": "论文标题",
  "authors": ["作者1", "作者2"],
  "summary": "摘要内容...",
  "published": "2017-06-12T10:37:23Z",
  "updated": "2017-06-12T10:37:23Z",
  "arxiv_id": "1706.03762",
  "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
  "categories": ["cs.CL", "cs.LG"],
  "doi": "10.1234/arxiv.1706.03762",
  "comment": "8 pages, 5 figures",
  "journal_ref": "NIPS 2017"
}
```

### 字段说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| index | int | 序号 | 1 |
| title | str | 论文标题 | "Attention Is All You Need" |
| authors | List[str] | 作者列表 | ["Vaswani, A.", "Shazeer, N."] |
| summary | str | 摘要 | "The dominant sequence..." |
| published | str | 发表时间（ISO 8601） | "2017-06-12T10:37:23Z" |
| updated | str | 更新时间（ISO 8601） | "2017-06-12T10:37:23Z" |
| arxiv_id | str | arXiv标识符 | "1706.03762" |
| pdf_url | str | PDF下载链接 | "https://arxiv.org/pdf/..." |
| categories | List[str] | 分类标签 | ["cs.CL", "cs.LG"] |
| doi | str | DOI（可选） | "10.1234/..." |
| comment | str | 作者备注 | "8 pages, 5 figures" |
| journal_ref | str | 期刊引用（可选） | "NIPS 2017" |

---

## 排序选项

| sort_by值 | 说明 | 适用场景 |
|-----------|------|---------|
| relevance | 相关性（默认） | 主题搜索 |
| lastUpdatedDate | 最后更新时间 | 获取最新版本 |
| submittedDate | 提交时间 | 按时间顺序 |

---

## 数量参数

| max_results | 说明 | 响应时间 | 推荐场景 |
|-------------|------|---------|---------|
| 10 | 快速预览 | ~1-2秒 | 初步探索 |
| 20 | 中等调研（默认） | ~2-3秒 | 常规搜索 |
| 50 | 深度调研 | ~5-8秒 | 全面覆盖 |
| 100 | 大批量 | ~10-15秒 | 批量分析 |

---

## 错误处理

### 常见异常

| 异常类型 | 原因 | 解决方案 |
|---------|------|---------|
| requests.RequestException | 网络错误 | 检查网络连接 |
| ValueError | 参数错误 | 检查输入参数 |
| TimeoutError | 请求超时 | 增加timeout参数 |

### 错误处理示例

```python
try:
    results = searcher.search("keyword")
except requests.RequestException as e:
    print(f"网络错误: {e}")
except Exception as e:
    print(f"未知错误: {e}")
```

---

## 使用示例

### 完整工作流

```python
from skills.arxiv_paper_search.scripts.arxiv_searcher import ArxivPaperSearcher

# 1. 初始化
searcher = ArxivPaperSearcher(debug=True)

# 2. 搜索
results = searcher.search(
    query="transformer architecture",
    max_results=50,
    categories=["cs.AI", "cs.LG"]
)

print(f"找到 {len(results)} 篇论文")

# 3. 保存摘要
searcher.save_abstracts(results, 'transformer_papers.json')

# 4. 导出CSV
searcher.export_to_csv(results, 'transformer_papers.csv')

# 5. 下载PDF（前10篇）
files = searcher.batch_download_pdfs(results[:10], 'transformer_papers/')

print(f"成功下载 {len(files)} 篇PDF")
```

---

**文档版本**: 1.0.0
**最后更新**: 2025-12-28
