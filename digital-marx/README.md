# 数字马克思技能使用指南

## 快速开始

### 环境要求
- Python 3.8+
- 依赖包：pandas, numpy, jieba, matplotlib, seaborn

### 安装依赖
```bash
pip install pandas numpy jieba matplotlib seaborn
```

### 基本使用

#### 1. 单独分析模块
```python
from scripts.historical_materialism_analyzer import HistoricalMaterialismAnalyzer

# 创建分析器
analyzer = HistoricalMaterialismAnalyzer()

# 分析生产力水平
productivity_results = analyzer.analyze_productivity_level(text_data)

# 分析生产关系
relations_results = analyzer.analyze_production_relations(text_data)

# 分析上层建筑
superstructure_results = analyzer.analyze_superstructure(text_data)

# 分析社会变革
change_results = analyzer.analyze_social_change(text_data)
```

#### 2. 集成分析
```python
from scripts.integrated_marx_analyzer import DigitalMarxIntegratedAnalyzer

# 创建集成分析器
integrated_analyzer = DigitalMarxIntegratedAnalyzer()

# 执行完整分析
results = integrated_analyzer.execute_comprehensive_analysis(text_data)

# 获取综合报告
report = results['comprehensive_report']
print(report)
```

#### 3. 质量检验
```python
from scripts.quality_validator import MarxSkillQualityValidator

# 创建质量检验器
validator = MarxSkillQualityValidator()

# 执行质量检验
test_results = validator.run_comprehensive_quality_test()

# 生成质量报告
quality_report = validator.generate_quality_report(test_results)
```

## 分析流程

### 四阶段分析架构

1. **物质基础分析**
   - 生产力水平评估
   - 生产工具与技术形态分析
   - 劳动效率评估
   - 生产力发展阶段判断

2. **生产关系分析**
   - 生产资料所有制形式分析
   - 人们在生产中的地位分析
   - 产品分配方式分析
   - 阶级结构分析

3. **上层建筑分析**
   - 政治制度分析
   - 意识形态分析
   - 文化特征分析
   - 上层建筑与经济基础关系分析

4. **社会变革预测**
   - 基本矛盾分析
   - 变革条件分析
   - 变革动力分析
   - 发展趋势预测

## 提示词使用

### 理论分析提示词
在需要深度理论分析时，加载相应的提示词文件：

```python
# 物质基础分析
with open('prompts/material-base-analysis.md', 'r', encoding='utf-8') as f:
    material_base_prompt = f.read()

# 生产关系分析
with open('prompts/production-relations-analysis.md', 'r', encoding='utf-8') as f:
    production_relations_prompt = f.read()

# 上层建筑分析
with open('prompts/superstructure-analysis.md', 'r', encoding='utf-8') as f:
    superstructure_prompt = f.read()

# 社会变革预测
with open('prompts/social-change-prediction.md', 'r', encoding='utf-8') as f:
    social_change_prompt = f.read()
```

## 输出解读

### 分析结果结构
每个分析阶段的结果包含：
- `quantitative_results`: 定量计算结果
- `theoretical_guidance`: 理论分析指导
- `quality_assessment`: 质量评估
- `phase_completed`: 阶段完成状态

### 质量指标
- `overall_quality`: 整体质量分数 (0-10)
- `completeness`: 完整性评估
- `consistency`: 一致性评估
- `theoretical_relevance`: 理论相关性评估

### 等级划分
- 优秀 (8.0-10.0)
- 良好 (6.0-7.9)
- 一般 (4.0-5.9)
- 需要改进 (0-3.9)

## 常见问题

### Q: 如何提高分析质量？
A: 
1. 确保输入文本包含足够的分析信息
2. 使用专业的马克思主义理论术语
3. 提供具体的历史背景和社会条件
4. 避免过于抽象或空泛的描述

### Q: 分析结果与预期不符怎么办？
A: 
1. 检查输入文本的准确性和完整性
2. 运行质量检验识别具体问题
3. 根据改进建议优化分析方法
4. 调整分析参数或重新组织输入

### Q: 如何处理复杂的社会现象？
A: 
1. 将复杂现象分解为具体分析维度
2. 分别进行各阶段的专业分析
3. 注意各阶段之间的逻辑关系
4. 综合考虑多种影响因素

## 最佳实践

### 文本准备
- 提供具体、准确的社会现象描述
- 包足够的历史背景和时代特征
- 使用规范的马克思主义理论术语
- 避免主观臆断和价值判断

### 分析流程
- 按照四阶段顺序进行系统分析
- 重视各阶段之间的内在联系
- 关注理论与实践的结合
- 确保逻辑推理的严密性

### 结果应用
- 结合具体历史条件理解分析结果
- 注意分析结果的适用范围
- 关注实践指导价值
- 持续完善分析方法

## 技术支持

### 依赖问题
确保所有依赖包正确安装：
```bash
pip install -r requirements.txt
```

### 编码问题
所有文件使用UTF-8编码，确保中文显示正常。

### 性能优化
对于大文本分析，建议：
1. 预处理文本，去除无关内容
2. 分段分析，逐步整合结果
3. 使用缓存机制，避免重复计算

## 扩展开发

### 添加新的分析维度
1. 在相应的分析器中添加新方法
2. 更新质量检验标准
3. 完善提示词文件
4. 测试新功能的准确性

### 集成外部数据
1. 开发数据接口模块
2. 实现数据预处理功能
3. 更新分析算法
4. 验证数据质量

### 自定义分析模型
1. 继承基础分析器类
2. 重写相关分析方法
3. 调整质量评估标准
4. 进行充分测试验证