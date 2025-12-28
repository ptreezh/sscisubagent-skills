# PubScholar自动搜索技能 - API参考

**版本**: 1.0.0
**更新日期**: 2025-12-28

---

## 目录

1. [类概览](#类概览)
2. [PubScholarSearcher](#pubscholarsearcher)
3. [SynchronousPubScholarSearcher](#synchronouspubscholarsearcher)
4. [数据模型](#数据模型)
5. [错误码](#错误码)

---

## 类概览

```
PubScholarSearcher (异步)
    ├── search()              # 主搜索方法
    ├── _execute_search()     # 执行单次搜索
    ├── _smart_expansion()    # 智能扩展
    ├── export_to_json()      # 导出JSON
    ├── export_to_csv()       # 导出CSV
    └── generate_citations()  # 生成引用

SynchronousPubScholarSearcher (同步)
    └── 封装PubScholarSearcher的简化接口
```

---

## PubScholarSearcher

异步搜索器，推荐用于生产环境。

### 初始化

```python
PubScholarSearcher(debug: bool = False, headless: bool = True)
```

**参数**:
- `debug` (bool): 是否启用调试模式，默认False
- `headless` (bool): 是否使用无头浏览器，默认True

**示例**:
```python
searcher = PubScholarSearcher(debug=True, headless=False)
```

### search()

主搜索方法，支持智能扩展。

```python
async def search(
    keyword: str,
    auto_expand: bool = True,
    min_results: int = 5,
    max_results: int = 50
) -> List[Dict]
```

**参数**:
- `keyword` (str, 必需): 搜索关键词
- `auto_expand` (bool): 是否启用智能扩展，默认True
- `min_results` (int): 触发扩展的最小结果数，默认5
- `max_results` (int): 最大返回结果数，默认50

**返回**: List[Dict] - 文献列表

**示例**:
```python
# 基本搜索
results = await searcher.search("数字鸿沟")

# 精准搜索
results = await searcher.search("社会网络分析", auto_expand=False)

# 自定义阈值
results = await searcher.search("人工智能", min_results=10)
```

### _execute_search()

执行单次搜索（内部方法）。

```python
async def _execute_search(keyword: str) -> List[Dict]
```

**参数**:
- `keyword` (str): 搜索关键词

**返回**: List[Dict] - 文献列表

### _smart_expansion()

智能扩展搜索（内部方法）。

```python
async def _smart_expansion(
    original_keyword: str,
    current_results: int,
    target: int
) -> List[Dict]
```

**参数**:
- `original_keyword` (str): 原始关键词
- `current_results` (int): 当前结果数量
- `target` (int): 目标结果数量

**返回**: List[Dict] - 额外文献列表

### export_to_json()

导出为JSON格式。

```python
def export_to_json(results: List[Dict], filename: str) -> None
```

**参数**:
- `results` (List[Dict]): 文献列表
- `filename` (str): 输出文件名

**示例**:
```python
searcher.export_to_json(results, 'output.json')
```

### export_to_csv()

导出为CSV格式。

```python
def export_to_csv(results: List[Dict], filename: str) -> None
```

**参数**:
- `results` (List[Dict]): 文献列表
- `filename` (str): 输出文件名

**示例**:
```python
searcher.export_to_csv(results, 'output.csv')
```

### generate_citations()

生成GB/T 7714引用格式。

```python
def generate_citations(results: List[Dict]) -> List[str]
```

**参数**:
- `results` (List[Dict]): 文献列表

**返回**: List[str] - 引用字符串列表

**示例**:
```python
citations = searcher.generate_citations(results)
for citation in citations:
    print(citation)
```

---

## SynchronousPubScholarSearcher

同步搜索器，简化使用。

### 初始化

```python
SynchronousPubScholarSearcher(debug: bool = False, headless: bool = True)
```

**参数**:
- `debug` (bool): 是否启用调试模式，默认False
- `headless` (bool): 是否使用无头浏览器，默认True

**示例**:
```python
searcher = SynchronousPubScholarSearcher(debug=True)
```

### search()

同步搜索方法。

```python
def search(
    keyword: str,
    auto_expand: bool = True,
    min_results: int = 5,
    max_results: int = 50
) -> List[Dict]
```

**参数**: 与`PubScholarSearcher.search()`相同

**返回**: List[Dict] - 文献列表

**示例**:
```python
searcher = SynchronousPubScholarSearcher()
results = searcher.search("人工智能")
```

---

## 数据模型

### 文献对象 (Paper)

```json
{
  "index": 1,
  "title": "文献标题",
  "authors": ["作者1", "作者2"],
  "journal": "期刊名称",
  "year": "2024",
  "volume": "25",
  "issue": "3",
  "pages": "45-60",
  "abstract": "摘要内容...",
  "keywords": ["关键词1", "关键词2"],
  "url": "https://pubscholar.cn/...",
  "source": "PubScholar"
}
```

### 字段说明

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| index | int | 序号 | 1 |
| title | str | 文献标题 | "人工智能研究" |
| authors | List[str] | 作者列表 | ["张三", "李四"] |
| journal | str | 期刊名称 | "计算机学报" |
| year | str | 发表年份 | "2024" |
| volume | str | 卷号 | "25" |
| issue | str | 期号 | "3" |
| pages | str | 页码 | "45-60" |
| abstract | str | 摘要 | "摘要内容..." |
| keywords | List[str] | 关键词列表 | ["AI", "机器学习"] |
| url | str | 原文链接 | "https://..." |
| source | str | 来源平台 | "PubScholar" |

### 搜索请求对象

```json
{
  "search_request": {
    "keyword": "搜索关键词",
    "auto_expand": true,
    "min_results": 5,
    "max_results": 50,
    "year_range": {
      "start": 2020,
      "end": 2024
    },
    "document_types": ["期刊论文", "学位论文", "会议论文", "专利"]
  }
}
```

### 搜索结果对象

```json
{
  "search_summary": {
    "keyword": "搜索关键词",
    "total_results": 25,
    "expansion_used": true,
    "strategies_applied": ["同义词扩展", "英文翻译"],
    "search_time_seconds": 15.3
  },
  "papers": [/* 文献对象列表 */]
}
```

---

## 错误码

### 常见异常

| 异常类型 | 原因 | 解决方案 |
|---------|------|---------|
| PlaywrightError | 浏览器启动失败 | 检查Playwright安装 |
| TimeoutError | 页面加载超时 | 增加timeout参数 |
| ValueError | 参数错误 | 检查输入参数 |
| RuntimeError | 搜索执行失败 | 查看调试日志 |

### 错误处理示例

```python
try:
    results = await searcher.search("关键词")
except PlaywrightError as e:
    print(f"浏览器错误: {e}")
except TimeoutError:
    print("页面加载超时")
except Exception as e:
    print(f"未知错误: {e}")
```

---

## 使用示例

### 完整工作流

```python
import asyncio
from skills.pubscholar_auto_search.scripts.pubscholar_searcher import PubScholarSearcher

async def main():
    async with PubScholarSearcher(debug=True) as searcher:
        # 1. 搜索
        results = await searcher.search("人工智能")

        # 2. 验证
        print(f"找到 {len(results)} 篇文献")

        # 3. 导出
        searcher.export_to_json(results, 'ai_papers.json')
        searcher.export_to_csv(results, 'ai_papers.csv')

        # 4. 生成引用
        citations = searcher.generate_citations(results)
        for citation in citations[:5]:
            print(citation)

asyncio.run(main())
```

---

**文档版本**: 1.0.0
**最后更新**: 2025-12-28
