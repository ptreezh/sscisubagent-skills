# 信息验证专家技能文档

## 概述
信息验证专家技能是商业模型系统分析智能体的重要组成部分，专门负责对企业信息来源、准确性、可信度和时效性进行全面验证。该技能基于信息科学和验证理论，采用多种验证方法和技术，确保分析所依据的信息真实、准确、可靠。

## 功能特性
1. **来源验证**：验证信息来源的权威性和可靠性
2. **准确性检查**：验证信息内容的准确性
3. **可信度评估**：评估信息的可信度和可靠性
4. **数据完整性**：检查数据是否完整无缺
5. **时效性验证**：验证信息的时效性和更新状态
6. **一致性检查**：验证信息在不同来源间的一致性
7. **完整性验证**：检查信息是否全面涵盖所需内容
8. **综合验证**：执行全面的信息验证流程

## 输入参数
- `information`：待验证的信息对象（必需）
- `verificationType`：验证类型（必需）
  - `source-verification`：来源验证
  - `accuracy-check`：准确性检查
  - `credibility-assessment`：可信度评估
  - `data-integrity`：数据完整性
  - `completeness-check`：完整性检查
  - `timeliness-check`：时效性验证
  - `consistency-check`：一致性检查
  - `comprehensive-verification`：综合验证
- `config`：验证配置选项
  - `depth`：验证深度
  - `authoritativeSources`：权威信息源列表
  - `toleranceLevel`：容错水平

## 输出结果
返回包含以下字段的验证结果对象：
- `verification`：验证对象
  - `type`：验证类型
  - `result`：验证结果
    - `isVerified`：是否验证通过
    - `confidenceScore`：置信度分数
    - `details`：验证详情
    - `issues`：发现的问题列表
- `recommendations`：验证改进建议
- `dataQualityReport`：数据质量报告
- `validationScore`：验证分数
- `metadata`：元数据信息

## 实现架构
该技能采用模块化设计，包含以下核心模块：
1. **InformationValidationProcessor**：信息验证处理
2. **SourceVerificationModule**：来源验证
3. **AccuracyValidationModule**：准确性验证
4. **CredibilityAssessmentModule**：可信度评估
5. **DataIntegrityModule**：数据完整性检查
6. **InformationReportingModule**：报告生成

## 设计原则
1. **渐进式信息披露**：根据用户需求逐步展开详细信息
2. **多维度验证**：从多个维度验证信息质量
3. **权威性优先**：优先使用权威信息源进行验证
4. **准确性保障**：确保验证结果的准确性
5. **透明性原则**：提供验证过程的透明度

## 使用示例
```javascript
const skill = new InformationVerificationSkill();
const inputs = {
  information: {
    company: "示例公司",
    revenue: 1000000000,
    source: "年度报告"
  },
  verificationType: "accuracy-check",
  config: {
    depth: "standard",
    authoritativeSources: ["官方财报", "政府数据库"],
    toleranceLevel: 0.05
  }
};

const result = await skill.execute(inputs);
```