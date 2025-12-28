# PubScholar自动搜索技能 - 用户指南

**版本**: 1.0.0
**更新日期**: 2025-12-28

---

## 目录

1. [快速开始](#快速开始)
2. [基本用法](#基本用法)
3. [高级用法](#高级用法)
4. [搜索逻辑详解](#搜索逻辑详解)
5. [结果格式](#结果格式)
6. [结果导出](#结果导出)
7. [调试和模拟模式](#调试和模拟模式)
8. [常见问题](#常见问题)
9. [性能优化](#性能优化)
10. [集成指南](#集成指南)

---

## 快速开始

### 安装依赖

```bash
# 安装Playwright浏览器
pip install playwright
playwright install chromium

# 或使用项目依赖
pip install -r requirements.txt
```

### 验证安装

```bash
# 运行测试
python scripts/test_pubscholar_search.py
```

---

## 基本用法

### 1. 异步模式（推荐）

```python
import asyncio
from skills.pubscholar_auto_search.scripts.pubscholar_searcher import PubScholarSearcher

async def search_example():
    async with PubScholarSearcher(debug=True) as searcher:
        # 执行搜索（自动智能扩展）
        results = await searcher.search("数字鸿沟")

        # 查看结果
        for paper in results[:5]:
            print(f"标题: {paper['title']}")
            print(f"作者: socienceAI.com
            print(f"期刊: {paper['journal']}")
            print()

# 运行
asyncio.run(search_example())
```

### 2. 同步模式

```python
from skills.pubscholar_auto_search.scripts.pubscholar_searcher import SynchronousPubScholarSearcher

searcher = SynchronousPubScholarSearcher(debug=True)
results = searcher.search("社会网络分析")

# 导出结果
searcher.export_to_json(results, 'results.json')
searcher.export_to_csv(results, 'results.csv')
```

---

## 高级用法

### 1. 精准搜索（不扩展）

```python
async with PubScholarSearcher() as searcher:
    # 禁用自动扩展
    results = await searcher.search(
        keyword="人工智能 伦理",
        auto_expand=False  # 只精准搜索
    )
```

### 2. 限制结果数量

```python
async with PubScholarSearcher() as searcher:
    # 只返回前20篇
    results = await searcher.search(
        keyword="机器学习",
        max_results=20
    )
```

### 3. 调整扩展阈值

```python
async with PubScholarSearcher() as searcher:
    # 结果少于10篇时才扩展
    results = await searcher.search(
        keyword="深度学习 应用",
        min_results=10  # 默认是5
    )
```

### 4. 批量搜索

```python
keywords = ["数字鸿沟", "信息不平等", "数字不平等"]

async with PubScholarSearcher() as searcher:
    all_results = {}

    for keyword in keywords:
        print(f"搜索: {keyword}")
        results = await searcher.search(keyword)
        all_results[keyword] = results

        # 避免请求过快
        await asyncio.sleep(3)

    # 合并所有结果
    combined = []
    for results in all_results.values():
        combined.extend(results)

    searcher.export_to_csv(combined, 'all_results.csv')
```

---

## 搜索逻辑详解

### 阶段1: 精准搜索

```
输入: "数字鸿沟 教育"
↓
完全按照输入搜索
↓
检查结果数量
```

**适用场景**:
- 明确知道要搜索的主题
- 希望获得最相关的结果
- 关键词组合已经很精确

### 阶段2: 智能扩展（自动触发）

当精准搜索结果 < 5篇时：

```
策略1: 添加同义词
  "数字鸿沟" → "数字鸿沟 信息不平等"

策略2: 添加英文翻译
  "人工智能" → "人工智能 artificial intelligence"

策略3: 简化关键词
  "数字鸿沟 教育 影响" → "数字鸿沟"

策略4: 添加相关领域
  "机器学习" → "机器学习 教育"

策略5: 使用核心概念
  "深度神经网络 算法" → "神经网络"
```

**扩展规则**:
- 依次尝试每个策略
- 直到累计结果 ≥ 5篇
- 最多尝试5个扩展策略

---

## 结果格式

每条文献包含以下信息：

```json
{
  "index": 1,
  "title": "文献标题",
  "authors": ["作者1", "作者2", "..."],
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

---

## 结果导出

### 导出为JSON

```python
searcher.export_to_json(results, 'output.json')
```

### 导出为CSV

```python
searcher.export_to_csv(results, 'output.csv')
```

### 生成引用列表

```python
citations = searcher.generate_citations(results)
for citation in citations:
    print(citation)
```

输出示例：
```
张三, 李四. 人工智能在医疗诊断中的应用研究[J]. 计算机学报, 2024: 45-60
王五. 基于深度学习的疾病预测系统[J]. 软件学报, 2023: 123-140
```

---

## 调试和模拟模式

### 调试模式

启用调试模式查看详细日志：

```python
async with PubScholarSearcher(debug=True) as searcher:
    results = await searcher.search("测试关键词")
```

调试输出：
```
✓ 浏览器已启动
✓ 已导航到PubScholar首页

[阶段1] 精准搜索: '测试关键词'
✓ 精准搜索返回 8 篇文献
✓ 找到 8 个文献条目
✓ 结果统计: 显示 8 篇，总计 8 篇
✓ 浏览器已关闭
```

### 模拟模式

如果未安装Playwright，脚本会自动使用模拟模式：

```python
searcher = SynchronousPubScholarSearcher()
results = searcher.search("任意关键词")
# 返回模拟数据，用于测试和开发
```

---

## 常见问题

### Q: 搜索速度慢？

A: 这是正常的，因为：
- 浏览器需要启动和加载页面
- 等待JavaScript渲染
- 提取DOM元素

可以：
- 使用 `headless=True`（无头模式）加速
- 减少 `max_results` 限制提取数量
- 使用同步接口简化代码

### Q: 结果数量不准确？

A: PubScholar显示的是估算数量，实际提取的可能有差异。这是正常的。

### Q: 某些文献信息提取不完整？

A: 可能原因：
- 页面结构差异（不同类型文献布局不同）
- 动态加载内容未完成
- 网站更新

建议：
- 使用调试模式查看具体问题
- 手动检查页面结构
- 更新选择器

### Q: 如何只搜索中文文献？

A: 在搜索界面勾选"语种: 中文"筛选项，或在脚本中添加：
```python
# 目前需要在界面上手动操作，或在结果中过滤
chinese_results = [r for r in results if any('\u4e00' <= c <= '\u9fff' for c in r['title'])]
```

---

## 性能优化

### 1. 批量搜索优化

```python
import asyncio

async def batch_search(keywords):
    """并发搜索多个关键词"""
    tasks = []

    async with PubScholarSearcher() as searcher:
        for keyword in keywords:
            # 创建搜索任务
            task = asyncio.create_task(searcher.search(keyword))
            tasks.append(task)

            # 避免同时启动太多任务
            await asyncio.sleep(1)

        # 等待所有搜索完成
        all_results = await asyncio.gather(*tasks)

        return all_results

# 使用
keywords = ["人工智能", "机器学习", "深度学习"]
results = await batch_search(keywords)
```

### 2. 缓存结果

```python
import pickle
from pathlib import Path

class CachedPubScholarSearcher(PubScholarSearcher):
    def __init__(self, cache_dir='cache'):
        super().__init__()
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    async def search(self, keyword: str, **kwargs):
        # 检查缓存
        cache_file = self.cache_dir / f"{keyword}.pkl"

        if cache_file.exists():
            with open(cache_file, 'rb') as f:
                return pickle.load(f)

        # 执行搜索
        results = await super().search(keyword, **kwargs)

        # 保存缓存
        with open(cache_file, 'wb') as f:
            pickle.dump(results, f)

        return results
```

---

## 集成指南

### 在Claude Code中使用

1. **直接调用Python脚本**:
```bash
python skills/pubscholar-auto-search/scripts/pubscholar_searcher.py
```

2. **导入使用**:
```python
# 在其他Python脚本中导入
from skills.pubscholar_auto_search.scripts.pubscholar_searcher import SynchronousPubScholarSearcher

searcher = SynchronousPubScholarSearcher()
results = searcher.search("你的关键词")
```

3. **作为技能集成**:
在需要文献搜索的agent或技能中导入并使用此模块。

### 与其他技能集成

```python
# 示例：与文献分析技能集成
from skills.pubscholar_auto_search.scripts.pubscholar_searcher import SynchronousPubScholarSearcher
from skills.literature_analysis import LiteratureAnalyzer

# 1. 搜索文献
searcher = SynchronousPubScholarSearcher()
results = searcher.search("人工智能 伦理")

# 2. 分析文献
analyzer = LiteratureAnalyzer()
analysis = analyzer.analyze(results)

print(analysis)
```

---

## 许可和免责

- ✅ 仅用于学术研究和教育目的
- ✅ 遵守PubScholar平台使用条款
- ❌ 不用于商业用途
- ❌ 不用于大规模数据采集
- ❌ 不绕过访问限制

---

**文档版本**: 1.0.0
**最后更新**: 2025-12-28
