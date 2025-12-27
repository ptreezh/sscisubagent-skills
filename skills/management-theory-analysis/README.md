# 管理理论分析技能文档

## 概述
管理理论分析技能是商业模型系统分析智能体的重要组成部分，专门负责对企业管理理论应用和实践进行系统性分析。该技能基于现代管理理论框架，包括组织理论、领导力理论、企业文化理论等，全面评估企业的管理效能和组织健康度。

## 功能特性
1. **组织架构分析**：分析企业组织结构类型和设计合理性
2. **领导风格评估**：识别和评估企业领导团队的领导风格
3. **企业文化分析**：分析企业文化和价值观体系
4. **决策机制评估**：评估企业决策流程和机制
5. **人才管理分析**：分析企业人才发展战略和实践
6. **绩效管理评估**：评估企业绩效管理体系
7. **治理机制分析**：分析企业治理结构和机制
8. **管理创新评估**：评估企业管理和技术创新实践

## 输入参数
- `companyData`：企业基本信息对象
  - `name`：企业名称（必需）
  - `industry`：所属行业
  - `employees`：员工数量
  - `headquarters`：总部位置
- `detailedReport`：是否生成详细报告（默认：false）
- `focusAreas`：指定分析领域数组（可选）
- `analysisDepth`：分析深度（summary/standard/detailed）

## 输出结果
返回包含以下字段的分析结果对象：
- `analysisSummary`：分析摘要
- `managementElements`：各管理要素分析结果
- `recommendations`：改进建议
- `validationScore`：验证分数
- `metadata`：元数据信息

## 实现架构
该技能采用模块化设计，包含以下核心模块：
1. **ManagementDataCollectionModule**：管理数据收集
2. **ManagementAnalysisModule**：管理分析逻辑
3. **ValidationModule**：结果验证
4. **ManagementReportingModule**：报告生成

## 设计原则
1. **渐进式信息披露**：根据用户需求逐步展开详细信息
2. **定量与定性结合**：程序化处理定量分析，AI处理定性评估
3. **理论与实践结合**：基于管理理论框架分析实际管理实践
4. **多维度评估**：从多个维度全面评估管理效能
5. **实用性导向**：提供可操作的管理改进建议

## 使用示例
```javascript
const skill = new ManagementTheoryAnalysisSkill();
const inputs = {
  companyData: {
    name: "示例公司",
    industry: "technology",
    employees: 1000,
    headquarters: "北京"
  },
  detailedReport: true,
  focusAreas: ["organizationalStructure", "leadershipStyle"]
};

const result = await skill.execute(inputs);
```