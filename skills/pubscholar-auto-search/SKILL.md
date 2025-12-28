---
name: pubscholar-auto-search
description: 在PubScholar公益学术平台自动搜索中文论文、文献或专利，支持智能关键词扩展和结果数量自适应。当用户需要搜索中文学术资源时使用此技能。
version: 1.0.0
author: socienceAI.com
license: MIT
tags: [literature-search, pubscholar, chinese-papers, academic-search, automation]
compatibility: Claude 3.5 Sonnet and above
metadata:
  domain: literature-search
  methodology: automated-search
  complexity: intermediate
  integration_type: web-automation
  last_updated: "2025-12-28"
  website: https://pubscholar.cn
  language: chinese
allowed-tools: [python, bash, playwright]
---

# PubScholar自动搜索技能 (PubScholar Auto Search)

## Overview
在PubScholar公益学术平台（https://pubscholar.cn/）自动搜索中文学术资源，支持智能关键词扩展确保获得足够的文献结果。

## When to Use This Skill
Use this skill when the user requests:
- 搜索中文论文或文献 ("搜索关于...的中文论文")
- 在PubScholar平台查找学术资源
- 查找中文学术文献、专利或会议论文
- 自动化文献检索和元数据提取
- 需要批量搜索多个关键词
- 智能扩展搜索策略（结果不足时自动添加相关词）

## Quick Start
When user needs Chinese literature search:
1. **识别**核心搜索关键词
2. **执行**精准搜索（使用原始关键词）
3. **评估**结果数量（< 5篇则触发扩展）
4. **扩展**搜索（添加同义词、英文翻译）
5. **提取**文献元数据（标题、作者、期刊等）
6. **返回**结构化结果列表

## 使用时机

当用户提到以下需求时，使用此技能：
- "搜索" + "中文论文" / "中文学术文献" / "中文期刊"
- "在PubScholar" / "公益学术平台" / "pubscholar" 搜索
- "查找" + "中文" + "论文/文献/专利"
- "文献检索" + "中文" / "中国"
- 需要"批量搜索" / "自动搜索"中文学术资源
- 用户指定在PubScholar平台搜索

**关键词触发**:
- PubScholar、pubscholar
- 中文论文、中文学术文献
- 中文专利、中文期刊
- 公益学术平台

## 核心功能

### 1. 双阶段智能搜索

**阶段1: 精准搜索**
- 使用用户提供的确切关键词
- 不添加任何额外术语
- 快速获取最相关结果

**阶段2: 智能扩展**（自动触发）
- 当结果 < 5篇时自动启用
- 扩展策略：
  - 添加同义词（人工智能 → AI）
  - 添加英文翻译（人工智能 → artificial intelligence）
  - 简化关键词（"A B C" → "A"）
  - 添加相关领域（机器学习 + 教育）

### 2. 完整数据提取

自动提取每篇文献的：
- 标题 (title)
- 作者列表 (authors)
- 期刊名称 (journal)
- 发表年份 (year)
- 卷期页码 (volume, issue, pages)
- 摘要 (abstract)
- 关键词 (keywords)
- 原文链接 (url)

### 3. 结果导出

支持多种格式：
- JSON格式（完整数据）
- CSV格式（表格数据）
- GB/T 7714引用格式（学术规范）

## 脚本调用

```python
from skills.pubscholar_auto_search.scripts.pubscholar_searcher import SynchronousPubScholarSearcher

# 初始化
searcher = SynchronousPubScholarSearcher(debug=False)

# 执行搜索
results = searcher.search(
    keyword="搜索关键词",
    auto_expand=True,      # 是否智能扩展
    min_results=5,         # 触发扩展的最小结果数
    max_results=50         # 最大返回结果数
)

# 导出结果
searcher.export_to_csv(results, 'output.csv')
```

**参数说明**:
- `keyword`: 搜索关键词（必需）
- `auto_expand`: 是否启用智能扩展（默认True）
- `min_results`: 触发扩展的阈值（默认5）
- `max_results`: 最大返回结果数（默认50）

## 统一输入格式

```json
{
  "search_request": {
    "keyword": "搜索关键词（必需）",
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

## 统一输出格式

```json
{
  "search_summary": {
    "keyword": "搜索关键词",
    "total_results": 25,
    "expansion_used": true,
    "strategies_applied": ["同义词扩展", "英文翻译"],
    "search_time_seconds": 15.3
  },
  "papers": [
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
  ]
}
```

## 扩展策略映射

| 场景 | 原始关键词 | 扩展策略 |
|------|-----------|---------|
| 人工智能 | 人工智能 | AI + 机器学习 + artificial intelligence |
| 数字鸿沟 | 数字鸿沟 | 信息不平等 + digital divide + 数字分化 |
| 社会网络 | 社会网络 | 社交网络 + 关系网络 + social network |
| 深度学习 | 深度学习 | 神经网络 + DL + neural network |

## 参考文档

详细文档请查看：
- `references/USER_GUIDE.md` - 完整使用指南
- `references/DEVELOPMENT.md` - 开发文档
- `references/API_REFERENCE.md` - API参考
- `references/EXTENSION_STRATEGIES.md` - 扩展策略详解

## 依赖要求

```bash
# 核心依赖
playwright>=1.40.0
beautifulsoup4>=4.12.0
pandas>=2.0.0

# 安装
pip install -r requirements.txt

# 测试
python scripts/test_pubscholar_search.py
```

## 示例用法

### 示例1: 基本搜索
```python
# 用户: "在PubScholar搜索关于人工智能的中文论文"
searcher = SynchronousPubScholarSearcher()
results = searcher.search("人工智能")
```

### 示例2: 精准搜索
```python
# 用户: "搜索'社会网络分析 在线社区'，不要扩展"
results = searcher.search("社会网络分析 在线社区", auto_expand=False)
```

### 示例3: 批量搜索
```python
# 用户: "搜索：数字鸿沟、信息不平等、数字不平等"
keywords = ["数字鸿沟", "信息不平等", "数字不平等"]
all_results = [searcher.search(kw) for kw in keywords]
```

## 注意事项

⚠️ **重要声明**:
- 仅用于学术研究和教育目的
- 尊重PubScholar平台使用条款
- 不提供文献下载功能，仅提取元数据
- 避免频繁请求，每次搜索间隔2-3秒
- 遵守学术规范和版权法律

✅ **最佳实践**:
- 建议每次搜索提取不超过50篇文献
- 使用debug模式查看详细日志
- 验证自动提取的信息准确性
- 正确引用原始文献来源

---

**版本**: 1.0.0
**最后更新**: 2025-12-28
**维护者**: SSCI Research Tools
