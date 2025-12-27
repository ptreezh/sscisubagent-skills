# 竞争分析技能文档

## 概述
竞争分析技能是商业模型系统分析智能体的重要组成部分，专门负责对企业竞争环境、竞争对手、竞争优势和竞争策略进行全面分析。该技能基于波特竞争战略理论，包括五力模型、SWOT分析、竞争情报等理论框架，全面评估企业的竞争地位。

## 功能特性
1. **市场竞争分析**：分析企业所处市场竞争格局
2. **竞争对手分析**：识别和分析主要竞争对手
3. **竞争定位分析**：评估企业竞争定位策略
4. **五力模型分析**：应用波特五力模型分析竞争环境
5. **竞争优势分析**：识别和评估企业竞争优势
6. **市场份额分析**：分析企业市场份额和变化趋势
7. **定价策略分析**：分析企业定价策略和竞争性
8. **差异化策略分析**：评估企业差异化竞争策略

## 输入参数
- `companyData`：企业基本信息对象
  - `name`：企业名称（必需）
  - `industry`：所属行业
  - `marketPosition`：市场地位
- `detailedReport`：是否生成详细报告（默认：false）
- `focusAreas`：指定分析领域数组（可选）
- `analysisDepth`：分析深度（summary/standard/detailed）

## 输出结果
返回包含以下字段的分析结果对象：
- `analysisSummary`：分析摘要
- `competitiveElements`：各竞争要素分析结果
- `recommendations`：改进建议
- `validationScore`：验证分数
- `metadata`：元数据信息

## 实现架构
该技能采用模块化设计，包含以下核心模块：
1. **CompetitiveDataCollectionModule**：竞争数据收集
2. **CompetitiveAnalysisModule**：竞争分析逻辑
3. **ValidationModule**：结果验证
4. **CompetitiveReportingModule**：报告生成

## 设计原则
1. **渐进式信息披露**：根据用户需求逐步展开详细信息
2. **定量与定性结合**：程序化处理定量分析，AI处理定性评估
3. **理论与实践结合**：基于竞争战略理论框架分析实际竞争实践
4. **多维度评估**：从多个维度全面评估竞争地位
5. **情报导向**：提供可操作的竞争情报和策略建议

## 使用示例
```javascript
const skill = new CompetitiveAnalysisSkill();
const inputs = {
  companyData: {
    name: "示例公司",
    industry: "technology",
    marketPosition: "市场领导者"
  },
  detailedReport: true,
  focusAreas: ["competitorAnalysis", "competitiveAdvantage"]
};

const result = await skill.execute(inputs);
```