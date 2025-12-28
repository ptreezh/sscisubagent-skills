---
name: performing-industry-ecosystem-analysis
description: 该技能用于对特定行业进行深入的商业生态分析，从结构、参与者、价值链、竞争格局等多个维度全面剖析行业现状，为后续的数字化转型分析提供基础。当需要对某个行业进行全面的生态分析，了解行业结构、主要参与者及其相互关系时使用此技能。
---

# 行业生态系统分析技能

## 何时使用
当需要对某个行业进行全面的生态分析，了解行业结构、主要参与者及其相互关系时使用此技能。

## 核心功能
1. **行业结构分析**: 分析行业的整体结构特征、发展阶段和成熟度
2. **参与者识别**: 识别行业内的主要参与者类型和角色
3. **价值链分析**: 梳理行业的价值链结构和关键环节
4. **竞争格局评估**: 评估行业内的竞争态势和市场集中度
5. **市场驱动力分析**: 识别影响行业发展的关键驱动因素

## 脚本调用时机
当需要执行行业生态系统分析时，调用 `business_ecosystem_analyzer.py` 脚本中的 `performing-industry-ecosystem-analysis` 功能。

## 输入格式
```json
{
  "targetIndustry": "目标行业名称",
  "analysis_objectives": ["分析目标列表"],
  "resource_constraints": ["资源约束列表"],
  "success_metrics": ["成功指标列表"]
}
```

## 输出格式
```json
{
  "analysis_type": "performing-industry-ecosystem-analysis",
  "industry_context": "行业上下文",
  "industry_structure": {
    "life_cycle_stage": "生命周期阶段",
    "market_structure": "市场结构",
    "value_distribution": "价值分布",
    "external_factors": "外部因素",
    "innovation_trends": "创新趋势"
  },
  "participants": [
    {
      "name": "参与者名称",
      "role": "角色",
      "importance": "重要性"
    }
  ],
  "value_chain": {
    "primary_activities": "主要活动",
    "support_activities": "支持活动"
  },
  "competition_landscape": "竞争格局",
  "market_drivers": "市场驱动力",
  "output_results": {
    "ecosystem_structure_map": "生态系统结构图",
    "participant_classification_matrix": "参与者分类矩阵",
    "value_chain_analysis_diagram": "价值链分析图",
    "competition_landscape_report": "竞争格局分析报告",
    "industry_trend_prediction": "行业趋势预测"
  }
}
```

## 执行步骤
1. 收集行业基础数据和信息
2. 分析行业整体结构和特征
3. 识别并分类行业参与者
4. 梳理价值链和业务流程
5. 评估竞争格局和市场驱动力
6. 生成生态分析报告

## 输出结果
- 行业生态结构图
- 参与者分类矩阵
- 价值链分析图
- 竞争格局分析报告
- 行业发展趋势预测