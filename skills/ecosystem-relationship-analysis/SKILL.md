---
name: ecosystem-relationship-analysis
description: 专门分析商业生态系统中各主体间关系的技能，提供关系类型分析、网络拓扑分析、关键关系识别、生态系统健康度评估等功能，分析合作、竞争、供应、投资、监管等多种关系类型
---

# 生态系统关系分析技能

## 何时使用
- 商业生态系统中实体间关系的全面分析
- 生态系统网络拓扑结构的分析
- 关键关系和重要实体的识别
- 生态系统健康度和稳定性的评估
- 供应链网络的分析和优化
- 合作伙伴关系的评估
- 竞争格局和网络效应的分析
- 生态系统稳定性评估

## 核心功能
1. **关系类型分析**: 分析实体间的合作、竞争、供应、投资、监管等关系
2. **网络拓扑分析**: 计算网络密度、连通性、度分布、聚类系数、路径长度等
3. **关键关系识别**: 识别高强关系和网络中的关键节点
4. **生态系统健康度评估**: 评估网络结构健康度、连接质量、多样性、稳定性
5. **社区检测**: 识别生态系统中的功能模块

## 脚本调用时机
当需要执行生态系统关系分析时，调用 `ecosystem_relationship_analyzer.py` 脚本。

## 输入格式
```json
{
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
  ]
}
```

## 输出格式
```json
{
  "summary": {
    "total_entities": "实体总数",
    "total_relationships": "关系总数",
    "relationship_types": "关系类型列表",
    "ecosystem_health_score": "生态系统健康度分数",
    "key_relationships_count": "关键关系数量"
  },
  "details": {
    "relationshipAnalysis": {
      "summary": {
        "totalRelationships": "总关系数",
        "averageStrength": "平均强度",
        "relationshipTypeCount": "关系类型数",
        "keyRelationshipCount": "关键关系数",
        "primaryTypes": "主要关系类型"
      },
      "relationshipTypes": {
        "关系类型": {
          "count": "该类型关系数",
          "avgStrength": "该类型平均强度"
        }
      },
      "keyRelationships": [
        {
          "source": "源实体ID",
          "target": "目标实体ID",
          "type": "关系类型",
          "strength": "关系强度",
          "keyScore": "关键分数",
          "sourceImportance": "源实体重要性",
          "targetImportance": "目标实体重要性"
        }
      ]
    },
    "networkProperties": {
      "topology": {
        "entityCount": "实体数",
        "relationshipCount": "关系数",
        "density": "网络密度",
        "averageDegree": "平均度"
      },
      "centralities": {
        "degree": "度中心性",
        "closeness": "接近中心性",
        "betweenness": "中介中心性"
      },
      "communities": {
        "count": "社区数量",
        "communities": [
          {
            "id": "社区ID",
            "entities": "实体列表",
            "size": "社区规模"
          }
        ],
        "entityToCommunity": "实体到社区映射"
      },
      "health": {
        "score": "健康度分数",
        "indicators": {
          "density": "密度指标",
          "connectivity": "连通性指标",
          "diversity": "多样性指标",
          "averageDegree": "平均度指标"
        },
        "assessment": "健康度评估"
      }
    }
  },
  "metadata": {
    "timestamp": "时间戳",
    "version": "版本号",
    "skill": "技能名称",
    "validationScore": "验证分数"
  }
}
```

## 执行步骤
1. 准备生态系统实体和关系数据
2. 分析不同类型的关系
3. 计算网络拓扑属性
4. 识别关键关系和实体
5. 评估生态系统健康度
6. 执行社区检测

## 输出结果
- 完整的关系类型分析结果
- 准确的网络拓扑属性计算
- 有效的关键关系和实体识别
- 合理的生态系统健康度评估
- 清晰的社区结构分析
- 具体可行的优化建议