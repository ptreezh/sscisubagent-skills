---
name: trusted-web-scraper
description: 专门用于爬取可信网站（企业官网、教育网、政务网）信息的爬虫技能，确保数据来源的可靠性
version: 1.0.0
author: socienceAI.com
license: MIT
tags: [web-scraping, trusted-sources, data-collection, research, enterprise-websites, educational-sites, government-sites]
compatibility: Claude 3.5 Sonnet and above
metadata:
  domain: data-collection
  methodology: web-scraping
  complexity: advanced
  integration_type: data_collection_tool
  last_updated: "2025-12-27"
allowed-tools: [python, bash, read_file, write_file, web_fetch]
---

# 可信网站爬虫技能 (Trusted Web Scraper)

## 概述

可信网站爬虫技能专门用于从可信网站（企业官网、教育网、政务网）收集信息，确保数据来源的可靠性和权威性。该技能采用多种技术手段来验证网站可信度，并使用适当的爬取策略来获取所需信息。

## 使用时机

当用户请求以下操作时使用此技能：
- 从企业官网收集公司信息、产品数据或公告
- 从教育网站收集学术信息、课程数据或研究资料
- 从政府网站收集政策文件、统计数据或官方公告
- 验证网站可信度并收集相关信息
- 研究特定机构的公开信息

## 快速开始

当用户请求爬取可信网站信息时：
1. **验证**网站的可信度（域名、SSL证书、机构归属）
2. **选择**适当的爬取策略（静态解析、动态加载、API接口）
3. **提取**所需信息并确保数据质量
4. **验证**信息的准确性和时效性
5. **整理**信息并提供结构化输出

## 核心功能（渐进式披露）

### 主要功能
- **可信度验证**: 验证网站的可信度和权威性
- **信息提取**: 从可信网站提取所需信息
- **数据清洗**: 清洗和标准化提取的数据
- **结构化输出**: 提供结构化的数据输出

### 次要功能
- **反爬虫对策**: 应对常见的反爬虫机制
- **动态内容处理**: 处理JavaScript渲染的内容
- **速率控制**: 控制爬取频率以遵守robots.txt
- **错误处理**: 处理网络错误和异常情况

### 高级功能
- **多源验证**: 从多个可信源验证信息
- **变更监测**: 监测网站内容的变化
- **智能解析**: 智能识别和解析网页结构
- **数据融合**: 融合来自多个页面的数据

## 详细指令

### 第一阶段：可信度验证
   - 检查域名是否属于可信机构（edu、gov、知名企业的域名）
   - 验证SSL证书的有效性
   - 检查网站的WHOIS信息
   - 确认网站的官方身份
   - 评估网站的权威性和可靠性

### 第二阶段：爬取策略选择
   - 分析网站的技术架构（静态、动态、SPA等）
   - 检查是否存在API接口
   - 查看robots.txt文件
   - 评估反爬虫机制
   - 选择最适合的爬取方法

### 第三阶段：信息提取
   - 识别目标信息的CSS选择器或XPath
   - 提取文本、图片、表格等不同类型的数据
   - 保持数据的原始格式和上下文
   - 记录信息的来源和时间戳
   - 验证提取数据的完整性

### 第四阶段：数据处理
   - 清洗和标准化提取的数据
   - 去除无关信息和广告内容
   - 统一数据格式和单位
   - 验证数据的一致性和准确性
   - 处理编码和特殊字符

### 第五阶段：输出生成
   - 生成结构化的数据输出
   - 提供数据来源和可信度信息
   - 包含提取时间戳和验证信息
   - 提供数据质量评估
   - 生成爬取报告

## 参数
- `url`: 要爬取的网站URL
- `content_type`: 要提取的内容类型（text, images, tables, documents等）
- `data_fields`: 指定要提取的数据字段
- `verification_level`: 验证级别（basic, standard, thorough）
- `rate_limit`: 请求频率限制（requests per minute）
- `timeout`: 请求超时时间（秒）
- `retry_attempts`: 重试次数
- `output_format`: 输出格式（json, csv, markdown等）
- `methodology`: 爬取方法（static, dynamic, api）
- `cultural_context`: 文化背景考虑（特别是中文网站）

## 示例

### 示例 1: 企业官网信息收集
User: "收集某知名科技公司的产品信息和最新公告"
Response: 验证网站可信度，提取产品目录和新闻公告，生成结构化数据。

### 示例 2: 教育网站课程信息
User: "提取某大学计算机科学专业的课程信息"
Response: 验证教育网站可信度，提取课程列表、描述和要求，整理成结构化格式。

### 示例 3: 政府网站政策文件
User: "获取最新的教育政策文件"
Response: 验证政府网站可信度，提取政策文件和相关内容，提供结构化摘要。

## 质量标准

- 确保数据来源的可信度和权威性
- 遵遵守网站的使用条款和robots.txt
- 维护适当的请求频率以避免对服务器造成负担
- 确保提取数据的准确性和完整性
- 考虑中文网站的特殊性（编码、排版等）

## 输出格式

```json
{
  "summary": {
    "url": "https://example.com",
    "status_code": 200,
    "trust_level": "high",
    "content_extracted": 15,
    "processing_time": 2.5
  },
  "details": {
    "extracted_data": [...],
    "metadata": {...},
    "verification_info": {...}
  },
  "metadata": {
    "timestamp": "2025-12-27T10:30:00",
    "version": "1.0.0"
  }
}
```

## 资源
- 网页爬取最佳实践
- 可信网站识别指南
- 数据提取技术文档
- 中文网站处理技巧

## 完成标志

完成高质量的可信网站爬取应包括：
1. 网站可信度验证报告
2. 完整的数据提取结果
3. 数据质量评估
4. 爬取过程记录
5. 结构化数据输出

---

*此技能为研究提供可靠的网络数据收集支持，确保数据来源的可信度和提取过程的合规性。*