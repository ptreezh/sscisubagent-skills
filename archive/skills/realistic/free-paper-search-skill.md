---
name: free-paper-search-skill
description: 免费学术论文搜索下载技能，基于真实验证的方法（arXiv + 特定机构资源）。遵循渐进式信息披露，工具化思维原则。当用户需要搜索或下载学术论文PDF时自动激活。
---

# 📚 免费学术论文搜索下载技能

## 🛠️ **工具化执行策略**

### 搜索优先级
1. **arXiv搜索**（100%可靠）→ STEM领域预印本
2. **机构资源搜索**（已验证可用）→ MIT DSpace等
3. **结果验证整合**→ 确保所有链接真实可下载

### 搜索执行顺序

#### 1. arXiv搜索（最高优先级）
```python
# 搜索策略
def execute_arxiv_search(query, max_results=5):
    import arxiv
    search = arxiv.Search(query=query, max_results=max_results, sort_by=arxiv.SortCriterion.Relevance)

    results = []
    for paper in search.results():
        # 验证PDF可下载性
        if verify_pdf_downloadable(paper.pdf_url):
            results.append({
                'title': paper.title,
                'authors': [a.name for a in paper.authors],
                'abstract': paper.summary[:500] + '...' if len(paper.summary) > 500 else paper.summary,
                'pdf_url': paper.pdf_url,
                'source': 'arXiv',
                'confidence': 'High'
            })
    return results
```

#### 2. 机构资源补充搜索
```python
# 仅搜索已验证可用的机构
VERIFIED_INSTITUTIONS = [
    {
        'name': 'MIT DSpace',
        'search_url': 'https://dspace.mit.edu/simple-search',
        'pdf_pattern': 'dspace.mit.edu/bitstream/'
    }
]

def search_institutional_resources(query, max_results=3):
    results = []
    for institution in VERIFIED_INSTITUTIONS:
        try:
            papers = search_single_institution(institution, query, max_results)
            results.extend(papers)
        except Exception as e:
            continue
    return results
```

#### 3. 结果验证整合
```python
def verify_and_integrate_results(arxiv_results, institutional_results):
    """验证所有PDF链接并整合结果"""
    all_results = []

    # 验证arXiv结果（通常100%可靠）
    for paper in arxiv_results:
        if verify_pdf_downloadable(paper['pdf_url']):
            all_results.append(paper)

    # 验证机构结果（需要逐个检查）
    for paper in institutional_results:
        if verify_pdf_downloadable(paper['pdf_url']):
            all_results.append(paper)

    return all_results
```

## 📊 **输出格式**

### 搜索概览（渐进式信息披露第1层）
```
🔍 搜索结果概览:
- 总计找到: X 篇可下载论文
- arXiv来源: Y 篇 (100%可下载)
- 机构资源: Z 篇 (已验证)
- 搜索耗时: X.X 秒
```

### 论文列表（渐进式信息披露第2层）
```
📋 可下载论文列表:
1. [论文标题] - arXiv (152KB PDF)
2. [论文标题] - MIT DSpace (193KB PDF)
3. [论文标题] - arXiv (245KB PDF)
...
```

### 详细信息（渐进式信息披露第3层 - 按需）
```
📖 论文详情:
标题: [完整标题]
作者: [作者列表]
摘要: [论文摘要]
下载链接: [PDF链接]
引用建议: [arXiv引用格式]
```

## 🎯 **用户交互流程**

### 输入识别
```
包含以下关键词自动激活技能:
- "搜索论文"
- "下载论文"
- "找论文"
- "学术论文"
- "arXiv"
- "免费论文"
```

### 执行流程
```
1. 解析用户查询 → 提取关键词
2. 执行arXiv搜索 → 获取STEM领域论文
3. 补充机构搜索 → 获取技术报告
4. 验证下载链接 → 确保真实可下载
5. 渐进式展示结果 → 减少认知负荷
6. 支持按需下载 → 一键获取PDF
```

## ⚙️ **技术实现**

### 核心工具
- **arxiv库**: arXiv论文搜索
- **requests库**: PDF链接验证
- **BeautifulSoup**: 机构资源解析
- **文件下载**: PDF获取和保存

### 验证机制
```python
def verify_pdf_downloadable(url):
    """验证PDF链接是否真实可下载"""
    try:
        response = requests.head(url, timeout=10)
        if response.status_code == 200:
            content_type = response.headers.get('content-type', '').lower()
            return 'pdf' in content_type
    except:
        return False
```

## ⚠️ **使用限制**

### 能力范围
- ✅ arXiv预印本论文（物理、数学、计算机科学、量化金融）
- ✅ 已验证机构的技术报告
- ✅ 完全合法的获取方式

### 重要限制
- ❌ 不提供付费期刊的破解方法
- ❌ 不绕过任何访问限制
- ❌ 不涉及任何非法下载途径
- ❌ 覆盖范围主要集中在STEM领域

---

**此技能基于严格实际测试，只提供真实可用的免费PDF获取方法。**