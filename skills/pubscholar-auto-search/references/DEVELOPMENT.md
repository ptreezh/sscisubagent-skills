# PubScholar自动搜索技能 - 开发文档

**版本**: 1.0.0
**更新日期**: 2025-12-28

---

## 目录

1. [技术架构](#技术架构)
2. [搜索流程图](#搜索流程图)
3. [关键词扩展策略](#关键词扩展策略)
4. [DOM结构分析](#dom结构分析)
5. [错误处理](#错误处理)
6. [性能优化](#性能优化)
7. [扩展性](#扩展性)
8. [测试指南](#测试指南)
9. [维护和更新](#维护和更新)

---

## 技术架构

### 核心组件

```
PubScholarSearcher
├── 浏览器管理
│   ├── start_browser() - 启动Playwright浏览器
│   ├── close_browser() - 关闭浏览器
│   └── _navigate_to_homepage() - 导航到首页
│
├── 搜索功能
│   ├── search() - 主搜索方法（支持智能扩展）
│   ├── _execute_search() - 执行单次搜索
│   └── _smart_expansion() - 智能扩展搜索
│
├── 数据提取
│   ├── _extract_results() - 提取所有结果
│   ├── _extract_paper_info() - 提取单篇文献信息
│   └── _parse_journal_info() - 解析期刊信息
│
└── 结果处理
    ├── export_to_json() - 导出JSON
    ├── export_to_csv() - 导出CSV
    └── generate_citations() - 生成引用
```

### 技术栈

- **Playwright**: 浏览器自动化（Chrome）
- **Python 3.8+**: 异步编程模型
- **BeautifulSoup4**: HTML解析（备用）
- **CSV/JSON**: 数据导出

---

## 搜索流程图

### 完整搜索流程

```
用户输入关键词
    ↓
打开PubScholar网站
    ↓
执行精准搜索
    ↓
检查结果数量
    ↓
┌─── 结果 ≥ 5篇？ ────Yes──→ 返回结果
    ↓ No
生成扩展策略
    ↓
依次尝试扩展搜索
    ↓
合并去重
    ↓
返回所有结果
```

### 扩展策略流程

```
检测结果数量 < min_results
    ↓
生成5种扩展策略
    ↓
For each strategy:
    ↓
    执行搜索
    ↓
    累计结果
    ↓
    检查是否达标
    ↓
    达标 → 停止扩展
    ↓
未达标 → 继续下一个策略
    ↓
返回所有结果
```

---

## 关键词扩展策略

### 策略生成逻辑

```python
def _generate_expansion_strategies(keyword):
    strategies = []

    # 1. 同义词扩展
    if "人工智能" in keyword:
        strategies.append(keyword + " AI")
        strategies.append(keyword + " 机器学习")

    # 2. 英文翻译
    if "人工智能" in keyword:
        strategies.append(keyword + " artificial intelligence")

    # 3. 简化关键词
    words = keyword.split()
    if len(words) > 1:
        strategies.append(words[0])  # 第一个词
        strategies.append(words[-1])  # 最后一个词

    # 4. 相关领域
    if "教育" in keyword:
        strategies.append(keyword + " 教学")

    # 5. 去重并限制数量
    return unique(strategies)[:5]
```

### 预定义扩展映射

| 原始关键词 | 同义词 | 英文翻译 | 相关词 |
|-----------|-------|---------|--------|
| 人工智能 | AI、机器学习 | artificial intelligence | 深度学习、神经网络 |
| 数字鸿沟 | 信息不平等、数字分化 | digital divide | 信息贫富差距 |
| 社会网络 | 社交网络、关系网络 | social network | 网络分析、社会结构 |
| 深度学习 | DL | deep learning | 神经网络、机器学习 |

---

## DOM结构分析

### 首页结构

```html
<main>
  <div>
    <!-- 搜索框 -->
    <textarea placeholder="发现你感兴趣的内容..." />

    <!-- 检索按钮 -->
    <button>检索</button>
  </div>
</main>
```

### 结果页结构

```html
<main>
  <!-- 筛选面板（左侧） -->
  <div class="filters">
    <list>
      <listitem>
        <checkbox>期刊论文</checkbox>
        <text>295,939</text>
      </listitem>
      <!-- 更多筛选... -->
    </list>
  </div>

  <!-- 结果列表（右侧） -->
  <div class="results">
    <!-- 每篇文献条目 -->
    <generic class="paper-item">
      <!-- 标题 -->
      <h2>文献标题</h2>

      <!-- 作者 -->
      <generic>作者1, 作者2, ...</generic>

      <!-- 期刊信息 -->
      <link>《期刊名称》</link>
      <text>2025, Volume 75, Pages 243-267</text>

      <!-- 摘要 -->
      <text>摘要内容...</text>

      <!-- 关键词 -->
      <text>Keywords:</text>
      <link>关键词1</link>
      <link>关键词2</link>

      <!-- 链接 -->
      <generic>原文链接: <link>其他来源</link></generic>
    </generic>
  </div>
</main>
```

### 选择器映射

| 元素 | Playwright选择器 | 说明 |
|------|------------------|------|
| 搜索框 | `textarea[placeholder*="发现你感兴趣的内容"]` | 支持textarea和input |
| 搜索按钮 | `button:has-text("检索")` | 包含"检索"文本的按钮 |
| 结果计数 | `text=/\d+\/\d+ 条` | 显示"X / Y 条"的文本 |
| 文献条目 | `generic` | 每个结果容器 |
| 标题 | `h2` 或 `[role="heading"]` | 标题元素 |
| 作者 | `generic:has-text(",")` | 包含逗号的文本 |
| 期刊 | `link:has-text("《")` | 包含书名号的链接 |
| 摘要 | `generic:has-text("...")` | 包含省略号的文本 |
| 链接 | `a` | 任意链接 |

---

## 错误处理

### 常见错误和解决方案

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 超时错误 | 页面加载慢 | 增加 `wait_for_timeout()` |
| 元素未找到 | DOM结构变化 | 更新选择器 |
| 浏览器崩溃 | 内存不足 | 使用 `headless=True` |
| 结果为空 | 关键词太冷门 | 启用智能扩展 |

### 重试机制

```python
async def _execute_search_with_retry(self, keyword, max_retries=3):
    """带重试的搜索"""
    for attempt in range(max_retries):
        try:
            return await self._execute_search(keyword)
        except Exception as e:
            if attempt < max_retries - 1:
                await asyncio.sleep(2)
                continue
            else:
                raise
```

---

## 性能优化

### 1. 并发搜索

```python
async def concurrent_search(keywords):
    """并发搜索多个关键词"""
    async with PubScholarSearcher() as searcher:
        tasks = [
            searcher.search(kw) for kw in keywords
        ]
        results = await asyncio.gather(*tasks)
    return results
```

### 2. 选择性提取

```python
async def _extract_results(self, max_papers=20):
    """只提取前N篇"""
    papers = []

    # 只遍历前max_papers个元素
    items = await self.page.locator('generic').all()

    for item in items[:max_papers]:
        paper = await self._extract_paper_info(item)
        if paper:
            papers.append(paper)

    return papers
```

### 3. 缓存机制

```python
from functools import lru_cache

class CachedPubScholarSearcher(PubScholarSearcher):
    @lru_cache(maxsize=100)
    async def _cached_search(self, keyword):
        return await self._execute_search(keyword)
```

---

## 扩展性

### 添加新的扩展策略

```python
def _generate_expansion_strategies(self, keyword):
    strategies = super()._generate_expansion_strategies(keyword)

    # 添加自定义策略
    if "教育学" in keyword:
        strategies.append(keyword + " 教学")

    return strategies
```

### 支持其他字段提取

```python
async def _extract_paper_info(self, item, index):
    paper = await super()._extract_paper_info(item, index)

    # 添加DOI提取
    doi_elem = item.locator('text=/DOI:/')
    if await doi_elem.count() > 0:
        doi_text = await doi_elem.text_content()
        paper['doi'] = doi_text.replace('DOI:', '').strip()

    return paper
```

---

## 测试指南

### 单元测试

```python
import pytest

@pytest.mark.asyncio
async def test_basic_search():
    async with PubScholarSearcher() as searcher:
        results = await searcher.search("测试")
        assert len(results) >= 0

@pytest.mark.asyncio
async def test_export():
    async with PubScholarSearcher() as searcher:
        results = await searcher.search("测试")
        searcher.export_to_json(results, 'test.json')
        assert Path('test.json').exists()
```

### 集成测试

```python
async def test_full_workflow():
    """测试完整工作流"""
    async with PubScholarSearcher(debug=True) as searcher:
        # 搜索
        results = await searcher.search("人工智能")

        # 验证
        assert len(results) > 0

        # 导出
        searcher.export_to_json(results, 'test.json')
        searcher.export_to_csv(results, 'test.csv')

        # 验证文件
        assert Path('test.json').exists()
        assert Path('test.csv').exists()
```

---

## 维护和更新

### 定期检查项

1. **DOM结构变化** - PubScholar网站更新可能导致选择器失效
2. **性能监控** - 监控搜索速度和成功率
3. **用户反馈** - 收集使用问题和改进建议
4. **依赖更新** - 定期更新Playwright和浏览器版本

### 更新流程

1. 修复选择器问题
2. 更新测试用例
3. 增加版本号
4. 更新文档
5. 发布更新

---

**文档版本**: 1.0.0
**最后更新**: 2025-12-28
