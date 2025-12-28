---
name: digital-marx
description: 数字马克思社会学分析专家，基于马克思主义理论进行历史唯物主义分析、阶级结构分析、资本运动规律分析和意识形态批判，包含物质基础分析、生产关系分析、上层建筑分析、社会变革预测四个阶段
license: MIT
compatibility: Python 3.8+, pandas, numpy, scikit-learn, matplotlib, seaborn
metadata:
  domain: sociology
  methodology: marxist-analysis
  complexity: advanced
  version: 1.0.0
  integration_type: theoretical_quantitative
  author: socienceAI.com
  website: http://agentpsy.com
allowed-tools: python bash read_file write_file task
---

# 数字马克思社会学分析技能

## 核心功能
- 历史唯物主义分析
- 阶级结构与社会关系分析
- 资本运动规律与剩余价值分析
- 意识形态批判与文化分析

## 脚本调用时机
当需要执行数字马克思社会学分析时，调用 `integrated_marx_analyzer.py` 脚本。

## 输入格式
```json
{
  "analysis_context": "分析的背景和范围",
  "target_society": "目标社会或现象",
  "analysis_phases": [
    "material_base_analysis", 
    "production_relation_analysis", 
    "superstructure_analysis", 
    "social_change_prediction"
  ],
  "data_sources": [
    {
      "type": "数据类型(文本/统计/其他)",
      "content": "具体数据内容",
      "relevance": "与分析的相关性"
    }
  ],
  "specific_questions": [
    "需要解答的具体问题"
  ],
  "constraints": {
    "theoretical_framework": "理论框架限制",
    "time_period": "时间范围",
    "geographical_scope": "地理范围"
  }
}
```

## 输出格式
```json
{
  "analysis_type": "digital-marx-analysis",
  "material_base_analysis": {
    "productivity_level": "生产力水平",
    "production_tools": "生产工具特征",
    "technology_form": "技术形态",
    "labor_efficiency": "劳动效率评估",
    "technical_impact": "科技进步对生产的影响"
  },
  "production_relation_analysis": {
    "ownership_form": "生产资料所有制形式",
    "production_position": "人们在生产中的地位",
    "product_distribution": "产品分配方式",
    "class_structure": "阶级结构分析",
    "contradiction_assessment": "矛盾分析"
  },
  "superstructure_analysis": {
    "political_system": "政治制度与法律体系",
    "ideology_form": "意识形态形式与功能",
    "culture_psychology": "文化与社会心理",
    "base_superstructure_relation": "上层建筑与经济基础关系"
  },
  "social_change_prediction": {
    "basic_contradiction": "社会基本矛盾分析",
    "change_condition": "变革条件评估",
    "trend_prediction": "发展趋势预测",
    "practice_path": "实践路径建议"
  },
  "quality_assessment": {
    "theoretical_consistency": "理论一致性检验结果",
    "methodological_validity": "方法论有效性",
    "analysis_completeness": "分析完整性"
  },
  "outputs": {
    "historical_materialism_report": "历史唯物主义分析报告",
    "class_structure_report": "阶级结构分析报告",
    "capital_movement_report": "资本运动分析报告",
    "social_change_assessment": "社会变革评估"
  }
}
```

## 分析流程

### 第一阶段: 物质基础分析
**目标**: 分析社会发展的物质技术基础
**操作**:
1. 生产力水平评估
2. 生产工具与技术形态分析
3. 劳动资料与劳动对象关系
4. 科技进步对生产的影响

**输出格式**:
```
生产力水平: [原始/农业/工业/信息/智能]
生产工具特征: [工具类型描述]
技术形态: [技术发展程度]
劳动效率: [高/中/低]
```

### 第二阶段: 生产关系分析
**目标**: 分析社会生产关系结构
**操作**:
1. 生产资料所有制形式
2. 人们在生产中的地位
3. 产品分配方式
4. 阶级结构与矛盾分析

### 第三阶段: 上层建筑分析
**目标**: 分析政治法律制度和意识形态
**操作**:
1. 政治制度与法律体系
2. 意识形态形式与功能
3. 文化与社会心理
4. 上层建筑与经济基础关系

### 第四阶段: 社会变革预测
**目标**: 分析社会发展趋势和变革可能
**操作**:
1. 社会基本矛盾分析
2. 变革条件与动力评估
3. 发展趋势预测
4. 实践路径探索

## 质量检验标准

### 理论一致性检验
- [ ] 是否坚持历史唯物主义基本原理
- [ ] 生产力与生产关系分析是否准确
- [ ] 经济基础与上层建筑关系是否正确
- [ ] 阶级分析方法是否科学

### 方法论检验
- [ ] 是否避免机械唯物主义
- [ ] 是否体现辩证思维
- [ ] 是否关注现实矛盾
- [ ] 是否揭示发展规律

### 分析完整性检验
- [ ] 物质基础分析全面
- [ ] 生产关系分析深入
- [ ] 上层建筑分析系统
- [ ] 社会变革分析有据

## 标准化输出

### 必需输出
1. **历史唯物主义分析报告**: 完整的社会结构分析
2. **阶级结构分析报告**: 阶级关系与矛盾分析
3. **资本运动分析报告**: 经济规律与趋势分析
4. **社会变革评估**: 变革条件与路径评估

### 可选输出
1. **比较历史分析**: 不同社会形态比较
2. **意识形态批判**: 主流意识形态分析
3. **实践策略建议**: 具体实践路径建议
4. **理论发展贡献**: 马克思主义理论创新

## 关键风险控制

### 高风险问题
- 违背历史唯物主义基本原理
- 机械套用理论概念
- 忽视具体历史条件
- 阶级分析简单化

### 风险缓解策略
- 严格遵循马克思主义方法论
- 坚持理论与实际相结合
- 深入分析具体历史条件
- 科学运用阶级分析方法