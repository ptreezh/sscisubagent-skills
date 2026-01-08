---
name: business-ecosystem-data-collection
description: 从真实外部数据源收集商业生态系统分析所需数据，包括企业信息、关系数据、行业信息等，为后续生态系统分析提供高质量数据支持
version: 1.0.0
author: socienceAI.com
license: MIT
tags: [business, ecosystem, data-collection, real-data, external-sources]
compatibility: Node.js environment
metadata:
  domain: business-analysis
  methodology: data-collection
  complexity: intermediate
  integration_type: analysis_tool
  last_updated: "2025-12-26"
allowed-tools: [node, bash, read_file, write_file]
---

# 商业生态系统数据收集技能

## 何时使用
- 商业生态系统分析所需的基础数据收集
- 行业内关键实体（企业、机构等）的识别和搜索
- 企业详细信息（业务模式、规模、市场地位等）的收集
- 实体间关系（供应关系、投资关系、合作关系等）的识别和映射
- 行业趋势、市场规模、竞争格局等宏观信息的收集
- 数据质量和完整性的验证

## 核心功能
1. **多源真实数据收集**: 从百度搜索、企业官网、新闻资讯、政府公开信息、行业报告等多个真实数据源获取信息
2. **数据收集范围**: 地理范围、实体类型、数据类型的灵活配置
3. **收集深度**: 基本、标准、全面三个深度级别
4. **数据验证**: 实体信息完整性、关系数据准确性、行业信息时效性验证

## 脚本调用时机
当需要执行商业生态系统数据收集时，调用 `ecosystem_data_collector.py` 脚本。

## 输入格式
```json
{
  "targetIndustry": "目标行业名称",
  "search_scope": {
    "geographic": "地理范围",
    "timeRange": "时间范围"
  },
  "entities": [
    {
      "id": "实体唯一标识",
      "name": "实体名称",
      "type": "实体类型",
      "industry": "所属行业",
      "characteristics": {}
    }
  ],
  "relationships": [
    {
      "source": "源实体ID",
      "target": "目标实体ID",
      "type": "关系类型",
      "strength": "关系强度(0-1)",
      "description": "关系描述"
    }
  ],
  "data_types": ["company_info", "relationships", "industry_trends"],
  "collection_depth": "basic|standard|comprehensive",
  "verification_required": true
}
```

## 输出格式
```json
{
  "summary": {
    "entities_found": "找到的实体数量",
    "relationships_found": "找到的关系数量",
    "data_quality_score": "数据质量分数(0-1)",
    "collection_time": "收集时间"
  },
  "details": {
    "collected_entities": [
      {
        "id": "实体唯一标识",
        "name": "实体名称",
        "type": "实体类型",
        "industry": "所属行业",
        "characteristics": "实体特征"
      }
    ],
    "relationships": [
      {
        "source": "源实体ID",
        "target": "目标实体ID",
        "type": "关系类型",
        "strength": "关系强度(0-1)",
        "description": "关系描述"
      }
    ],
    "industry_info": "行业信息",
    "collection_metrics": {
      "target_industry": "目标行业",
      "search_scope": "搜索范围",
      "data_types": "数据类型",
      "collection_depth": "收集深度"
    },
    "data_quality_report": {
      "validation_score": "验证分数",
      "validation_details": "验证详情",
      "verification_performed": "是否执行验证"
    }
  },
  "metadata": {
    "timestamp": "时间戳",
    "version": "版本号",
    "skill": "技能名称"
  }
}
```

## 执行步骤
1. 定义收集目标和参数
2. 执行数据收集任务
3. 验证收集到的数据质量
4. 映射实体间的关系
5. 整合行业宏观信息

## 输出结果
- 完整的实体列表（企业、机构等）
- 详细的实体间关系网络
- 行业宏观信息和趋势
- 数据质量报告和验证结果
- 改进建议和后续分析建议