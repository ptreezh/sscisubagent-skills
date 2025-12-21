---
name: did-analysis
description: 执行双重差分法(DID)因果推断分析，结合计量经济学理论、统计检验方法、政策评估实践和数据科学技术。包含实验设计、模型设定、因果估计、政策解释四个阶段。
license: MIT
compatibility: Python 3.8+, pandas, numpy, scipy, statsmodels, matplotlib, seaborn
metadata:
  domain: causal-inference
  methodology: difference-in-differences
  complexity: advanced
  version: 2.0.0
  integration_type: theoretical_quantitative
  author: zhangshuren@hznu.edu.cn
  website: http://agentpsy.com
allowed-tools: python bash read_file write_file task
---

# 双重差分法(DID)分析技能

### 四层次渐进式信息披露

#### Level 1: 元数据层 (始终加载)
- **技能识别**: DID因果推断分析能力
- **触发条件**: 需要政策效果评估或因果推断时自动激活
- **Token成本**: ~100 tokens

#### Level 2: 指令层 (触发时加载)
- **分析流程**: DID因果推断框架概述
- **决策逻辑**: 理论指导与实证检验的结合原则
- **Token成本**: ~2000 tokens

#### Level 3: 理论指导层 (按需加载)
- **实验设计**: `prompts/experimental-design.md`
- **模型设定**: `prompts/model-specification.md`
- **因果解释**: `prompts/causal-interpretation.md`
- **政策建议**: `prompts/policy-recommendation.md`
- **Token成本**: 按具体分析需求动态加载

#### Level 4: 计算执行层 (脚本调用)
- **DID估计**: `scripts/did_estimator.py`
- **平行趋势检验**: `scripts/parallel_trend.py`
- **稳健性检验**: `scripts/robustness_test.py`
- **数据可视化**: `scripts/visualization.py`
- **集成引擎**: `scripts/integrated_did.py`
- **Token成本**: 0 (直接执行，不加载到上下文)

## 功能架构

### 理论指导层
- **实验设计**: 政策机制分析、实验组对照组选择
- **模型设定**: DID模型框架、内生性处理、异质性分析  
- **因果解释**: 统计结果阐释、竞争性解释排除
- **政策建议**: 政策效应评估、可行性分析、外推有效性

### 计算执行层
- **DID估计**: 双向固定效应、合成控制、异质性分析、动态效应
- **平行趋势检验**: 事件研究图、趋势一致性检验、预处理效应检测
- **稳健性检验**: 安慰剂检验、样本敏感性、模型设定检验、竞争性解释排除
- **数据可视化**: DID效应图、平行趋势图、异质性效应图、交互式仪表板
- **集成分析**: 理论与计量协调、分析流程控制、结果整合输出

## 智能协作机制

### 五阶段研究流程决策引擎
```python
# DID集成分析器的核心决策逻辑 - 五阶段研究流程
class IntegratedDIDAnalyzer:
    def execute_analysis(self, data, policy_context):
        # 阶段1: AI进行实验设计 (理论指导)
        experimental_design = self.execute_experimental_design(policy_context)
        
        # 阶段2: AI进行模型设定 (理论+方法)
        model_specification = self.execute_model_specification(data, experimental_design)
        
        # 阶段3: 脚本执行计量估计 (精确计算)
        estimation_results = self.execute_did_estimation(data, model_specification)
        
        # 阶段4: AI进行因果解释 (理论阐释)
        causal_interpretation = self.execute_causal_interpretation(estimation_results, experimental_design)
        
        # 阶段5: AI制定政策建议 (实践应用)
        policy_recommendations = self.execute_policy_recommendation(causal_interpretation, policy_context)
        
        return self.integrate_results(experimental_design, estimation_results, causal_interpretation, policy_recommendations)
```

### 智能调用时机
- **实验设计**: 研究开始时，加载`experimental-design.md`
- **模型设定**: 数据分析前，加载`model-specification.md`
- **计量估计**: 需要精确计算时，调用相应Python脚本
- **因果解释**: 获得估计结果后，加载`causal-interpretation.md`
- **政策建议**: 完成因果分析后，加载`policy-recommendation.md`

## 使用流程

### 第一阶段: 实验设计
**AI任务**: 加载`experimental-design.md`，进行深度政策机制分析
**输出**: 实验设计方案、组别选择、时间窗口设定
**计量支持**: 数据特征分析脚本提供数据描述

### 第二阶段: 模型设定
**AI任务**: 加载`model-specification.md`，设计DID模型框架
**输出**: 模型设定方案、内生性处理策略、异质性分析设计
**计量支持**: 计量理论基础和模型选择指导

### 第三阶段: 计量估计执行
**AI任务**: 决策调用哪些计量脚本
**脚本执行**: 
- `did_estimator.py`: 执行DID估计
- `parallel_trend.py`: 平行趋势检验
- `robustness_test.py`: 稳健性检验
**输出**: 精确的估计结果、统计检验、质量指标

### 第四阶段: 因果解释
**AI任务**: 加载`causal-interpretation.md`，进行因果机制阐释
**输出**: 因果效应解释、理论意义、统计可靠性评估
**计量支持**: 估计结果提供解释基础

### 第五阶段: 政策建议
**AI任务**: 加载`policy-recommendation.md`，制定政策建议
**输出**: 政策建议、可行性分析、外推有效性评估
**计量支持**: 因果效应大小和政策含义

## 应用场景

### 政策效果评估
- **公共政策**: 各类政策的经济社会效应评估
- **监管政策**: 金融监管、环境监管的效果分析
- **社会政策**: 教育、医疗、社保政策效果

### 医疗干预研究
- **医疗政策**: 医保改革、药品政策效果评估
- **公共卫生**: 疾病防控、健康干预效果分析
- **医疗技术**: 新技术、新疗法的效果评估

### 教育改革评估
- **教育政策**: 教育改革、资源配置效果评估
- **教学干预**: 教学方法、课程改革效果分析
- **教育公平**: 教育机会均等政策效果

### 环境政策分析
- **环境规制**: 环保政策、碳排放政策效果
- **能源政策**: 可再生能源、节能政策效果
- **生态保护**: 自然保护、生态修复政策效果

## 技术特性

### 渐进式信息披露
- **按需加载**: 只在需要时加载相应理论指导
- **上下文优化**: 避免无关信息干扰
- **计算独立**: 复杂计算不占用上下文

### 智能化因果推断
- **自动决策**: AI自动判断何时调用何种工具
- **质量保障**: 内置因果识别有效性检验
- **结果整合**: 自动生成完整的因果推断报告

## 技术特性

### 智能理论指导系统
每个提示词文件都采用渐进式结构：
- **理论框架**: 相关计量经济学和政策理论
- **分析流程**: 分步骤的操作指南
- **质量标准**: 因果推断有效性检验标准
- **输出规范**: 标准化的分析报告格式

### 高效计量分析引擎
- **算法优化**: 针对DID特点优化的计量算法
- **错误处理**: 完善的统计检验异常处理
- **性能监控**: 实时的估计质量监控
- **结果验证**: 多层次的因果识别验证

### 集成控制系统
- **状态跟踪**: 完整的因果推断状态管理
- **决策记录**: 所有理论决策的详细记录
- **版本控制**: 分析过程和结果的版本管理
- **审计追踪**: 完整的因果推断审计日志

## 质量保证

### 三层质量控制
1. **理论质量**: 计量模型的理论一致性和识别策略有效性
2. **统计质量**: 平行趋势假设、统计显著性、估计精度
3. **政策质量**: 政策现实相关性、建议可行性、外推有效性
    if not check_parallel_trend_assumption(did_results):
        quality_issues.append("平行趋势假设不满足")
    
    # 内生性检验
    if not assess_endogeneity_concerns(did_results):
        quality_issues.append("存在潜在内生性问题")
    
    # 稳健性检验
    if not validate_robustness_results(did_results):
        quality_issues.append("稳健性检验未通过")
    
    return quality_issues
```

## 开始使用

### 快速启动
```bash
# 进入技能目录
cd did-analysis/

# 运行集成分析
python scripts/integrated_did.py
```

### 自定义分析
1. 准备面板数据 (CSV格式，包含个体、时间、处理、结果变量)
2. 定义政策背景和研究问题
3. 运行集成分析器
4. 根据AI提示进行深度理论分析
5. 获得完整的因果推断报告

## 扩展资源

### 理论指导文件
- `prompts/experimental-design.md`: 实验设计专家提示
- `prompts/model-specification.md`: 模型设定专家提示
- `prompts/causal-interpretation.md`: 因果解释专家提示
- `prompts/policy-recommendation.md`: 政策建议专家提示

### 计量分析脚本
- `scripts/did_estimator.py`: DID估计核心算法
- `scripts/parallel_trend.py`: 平行趋势检验
- `scripts/robustness_test.py`: 稳健性检验
- `scripts/visualization.py`: 数据可视化
- `scripts/integrated_did.py`: 集成分析引擎

### 参考文档
- `references/METHODOLOGY.md`: DID方法论详解
- `references/BEST_PRACTICES.md`: 最佳实践指南
- `references/COMMON_PITFALLS.md`: 常见陷阱与避免
- `assets/templates/`: 数据模板和报告模板

---

**注意**: AI负责理论思考和因果解释，脚本负责精确计量估计，通过智能决策引擎实现因果推断的科学性和政策相关性的统一。