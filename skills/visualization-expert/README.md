# 可视化专家技能文档

## 概述
可视化专家技能是商业模型系统分析智能体的重要组成部分，专门负责将复杂的商业数据和分析结果转换为直观、易于理解的图表和仪表板。该技能基于数据可视化理论和最佳实践，遵循信息设计原则，确保可视化结果既美观又有效传达信息。

## 功能特性
1. **多种图表类型**：支持柱状图、折线图、饼图、散点图等多种图表
2. **仪表板创建**：创建综合性的数据仪表板
3. **智能推荐**：根据数据特征推荐最适合的可视化类型
4. **主题定制**：支持多种主题和样式定制
5. **无障碍设计**：确保可视化内容对所有用户可访问
6. **交互功能**：提供交互式可视化功能
7. **响应式设计**：适配不同设备和屏幕尺寸
8. **数据故事化**：将数据转化为有逻辑的故事

## 输入参数
- `data`：待可视化的数据对象（必需）
- `visualizationType`：可视化类型（必需）
  - `bar-chart`：柱状图
  - `line-chart`：折线图
  - `pie-chart`：饼图
  - `scatter-plot`：散点图
  - `dashboard`：仪表板
  - `heatmap`：热力图
  - `network-graph`：网络图
  - `custom-visualization`：自定义可视化
- `config`：可视化配置选项
  - `title`：图表标题
  - `theme`：主题风格
  - `size`：图表尺寸
  - `format`：输出格式
- `targetAudience`：目标受众类型

## 输出结果
返回包含以下字段的可视化结果对象：
- `visualization`：可视化对象
  - `type`：可视化类型
  - `content`：可视化内容
  - `metadata`：元数据信息
- `recommendations`：可视化改进建议
- `accessibilityReport`：无障碍访问报告
- `validationScore`：验证分数
- `metadata`：元数据信息

## 实现架构
该技能采用模块化设计，包含以下核心模块：
1. **VisualizationDataProcessor**：数据处理
2. **ChartRecommendationModule**：图表推荐
3. **VisualizationGenerator**：可视化生成
4. **AccessibilityModule**：无障碍访问
5. **VisualizationReportingModule**：报告生成

## 设计原则
1. **渐进式信息披露**：根据用户需求逐步展开详细信息
2. **数据驱动设计**：根据数据特征选择最佳可视化方式
3. **用户体验优先**：确保可视化易于理解和使用
4. **无障碍访问**：遵循无障碍设计标准
5. **美观与功能并重**：在保证功能的同时注重美观

## 使用示例
```javascript
const skill = new VisualizationExpertSkill();
const inputs = {
  data: {
    labels: ["产品A", "产品B", "产品C"],
    values: [100, 150, 200]
  },
  visualizationType: "bar-chart",
  config: {
    title: "产品销售情况",
    theme: "corporate",
    size: { width: 800, height: 600 }
  },
  targetAudience: "managers"
};

const result = await skill.execute(inputs);
```