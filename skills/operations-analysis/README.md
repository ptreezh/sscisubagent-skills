# 运营分析技能文档

## 概述
运营分析技能是商业模型系统分析智能体的重要组成部分，专门负责对企业运营流程、效率、质量、供应链等进行系统性分析。该技能基于运营管理理论，包括精益管理、六西格玛、供应链管理等理论框架，全面评估企业的运营效能。

## 功能特性
1. **流程效率分析**：分析企业运营流程的效率和瓶颈
2. **质量管理评估**：评估企业质量管理体系和控制措施
3. **供应链分析**：分析供应链结构和管理效率
4. **成本优化评估**：评估运营成本结构和优化潜力
5. **产能规划分析**：分析企业产能配置和规划
6. **库存管理评估**：评估库存管理策略和效率
7. **物流分析**：分析物流网络和配送效率
8. **绩效指标评估**：评估运营绩效指标体系

## 输入参数
- `companyData`：企业基本信息对象
  - `name`：企业名称（必需）
  - `industry`：所属行业
  - `operationsData`：运营相关数据
- `detailedReport`：是否生成详细报告（默认：false）
- `focusAreas`：指定分析领域数组（可选）
- `analysisDepth`：分析深度（summary/standard/detailed）

## 输出结果
返回包含以下字段的分析结果对象：
- `analysisSummary`：分析摘要
- `operationsElements`：各运营要素分析结果
- `recommendations`：改进建议
- `validationScore`：验证分数
- `metadata`：元数据信息

## 实现架构
该技能采用模块化设计，包含以下核心模块：
1. **OperationsDataCollectionModule**：运营数据收集
2. **OperationsAnalysisModule**：运营分析逻辑
3. **ValidationModule**：结果验证
4. **OperationsReportingModule**：报告生成

## 设计原则
1. **渐进式信息披露**：根据用户需求逐步展开详细信息
2. **定量与定性结合**：程序化处理定量分析，AI处理定性评估
3. **理论与实践结合**：基于运营管理理论框架分析实际运营实践
4. **多维度评估**：从多个维度全面评估运营效能
5. **优化导向**：提供可操作的运营改进方案

## 使用示例
```javascript
const skill = new OperationsAnalysisSkill();
const inputs = {
  companyData: {
    name: "示例公司",
    industry: "manufacturing",
    operationsData: { /* 运营数据 */ }
  },
  detailedReport: true,
  focusAreas: ["processEfficiency", "qualityManagement"]
};

const result = await skill.execute(inputs);
```