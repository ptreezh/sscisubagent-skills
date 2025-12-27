# 资本分析技能文档

## 概述
资本分析技能是商业模型系统分析智能体的核心能力之一，专门负责对企业资本结构、融资策略、投资决策和风险管理进行深入分析。该技能基于现代金融理论框架，采用定量与定性相结合的分析方法，为企业管理层和投资者提供全面的资本状况评估。

## 功能特性
1. **资本结构分析**：分析企业债务与股权结构的合理性
2. **融资模式评估**：评估企业融资渠道和策略的有效性
3. **投资策略分析**：分析企业投资方向和资源配置效率
4. **风险状况评估**：识别和评估企业面临的财务风险
5. **估值指标计算**：计算关键估值指标并进行市场比较
6. **现金流分析**：分析企业现金流状况和质量
7. **融资需求预测**：预测企业未来融资需求和策略
8. **投资者关系评估**：评估企业与投资者的关系质量

## 输入参数
- `companyData`：企业基本信息对象
  - `name`：企业名称（必需）
  - `industry`：所属行业
  - `financials`：财务报表数据
  - `marketInfo`：市场信息
- `detailedAnalysis`：是否进行详细分析（默认：false）
- `detailedReport`：是否生成详细报告（默认：false）
- `comparativeAnalysis`：是否包含对比分析（默认：false）
- `focusAreas`：指定分析领域数组（可选）

## 输出结果
返回包含以下字段的分析结果对象：
- `summary`：分析摘要
- `keyMetrics`：关键指标
- `capitalElements`：各资本要素分析结果（详细模式下）
- `ratings`：各项评级
- `validationScore`：验证分数
- `metadata`：元数据信息

## 实现架构
该技能采用模块化设计，包含以下核心模块：
1. **CapitalDataCollectionModule**：财务数据收集
2. **CapitalAnalysisModule**：资本分析逻辑
3. **CapitalValidationModule**：结果验证
4. **CapitalReportingModule**：报告生成

## 设计原则
1. **渐进式信息披露**：根据用户需求逐步展开详细信息
2. **定量与定性结合**：程序化处理定量计算，AI处理定性分析
3. **数据验证**：多维度验证数据准确性和一致性
4. **行业对比**：结合行业基准进行比较分析
5. **风险导向**：重点关注财务风险识别和管理

## 使用示例
```javascript
const skill = new CapitalAnalysisSkill();
const inputs = {
  companyData: {
    name: "示例公司",
    industry: "technology",
    financials: { /* 财务报表数据 */ },
    marketInfo: { /* 市场数据 */ }
  },
  detailedAnalysis: true,
  focusAreas: ["capitalStructure", "riskProfile"]
};

const result = await skill.execute(inputs);
```