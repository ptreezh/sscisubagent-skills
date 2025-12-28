---
name: msqca-analysis
description: 执行多值定性比较分析(msQCA)，结合定性理论分析与定量计算。包含理论分析、校准指导、定量计算、结果解释四个阶段。
license: MIT
compatibility: Python 3.8+, pandas, numpy
metadata:
  domain: qualitative-comparative-analysis
  methodology: msQCA
  complexity: advanced
  version: 2.0.0
  integration_type: qualitative_quantitative
  author: socienceAI.com
  website: http://agentpsy.com
allowed-tools: python bash read_file write_file task
---

# 多值定性比较分析(msQCA)技能

### 四阶段渐进式披露

#### Level 1: 元数据层 (始终加载)
- **技能识别**: msQCA分析能力
- **触发条件**: 需要复杂因果机制分析时自动激活
- **Token成本**: ~100 tokens

#### Level 2: 指令层 (触发时加载)
- **分析流程**: 四阶段分析框架
- **决策逻辑**: 定性与定量结合的决策机制
- **Token成本**: ~2000 tokens

#### Level 3: 定性提示词层 (按需加载)
- **理论分析**: `prompts/theoretical-analysis.md`
- **校准指导**: `prompts/calibration-guidance.md`  
- **结果解释**: `prompts/result-interpretation.md`
- **Token成本**: 按具体分析需求动态加载

#### Level 4: 定量计算层 (脚本调用)
- **校准算法**: `scripts/calibration.py`
- **真值表构建**: `scripts/truth_table.py`
- **逻辑最小化**: `scripts/minimization.py`
- **集成引擎**: `scripts/integrated_analysis.py`
- **Token成本**: 0 (直接执行，不加载到上下文)

## 功能架构

### 定性分析
通过专门的提示词文件引导AI进行分析：

1. **理论分析** (`theoretical-analysis.md`)
   - 条件变量的理论选择
   - 因果机制的构建
   - 理论框架的完善

2. **校准指导** (`calibration-guidance.md`)
   - 校准方法的理论依据
   - 阈值设定的合理性判断
   - 数据特征与理论的结合

3. **结果解释** (`result-interpretation.md`)
   - 统计结果的理论阐释
   - 因果机制的深度解释
   - 实践意义的提炼

### 定量计算
通过Python脚本执行计算任务：

1. **数据校准** (`calibration.py`)
   - 多种校准算法实现
   - 自动阈值识别
   - 质量检验指标

2. **真值表构建** (`truth_table.py`)
   - 智能组合识别
   - 矛盾组合处理
   - 逻辑余项管理

3. **逻辑最小化** (`minimization.py`)
   - Quine-McCluskey算法
   - 多种解类型生成
   - 质量指标计算

4. **集成分析** (`integrated_analysis.py`)
   - 定性与定量协调
   - 分析流程控制
   - 结果整合输出

## 智能协作机制

### AI决策引擎
```python
# 集成分析器的核心决策逻辑
class IntegratedQCAAnalyzer:
    def execute_analysis(self, data, research_context):
        # 阶段1: AI进行理论分析 (定性)
        theoretical_analysis = self.execute_theoretical_analysis(research_context)
        
        # 阶段2: AI制定校准方案 (定性+定量判断)
        calibration_plan = self.execute_calibration_guidance(data, theoretical_analysis)
        
        # 阶段3: 脚本执行定量计算 (定量)
        quantitative_results = self.execute_quantitative_analysis(data, calibration_plan)
        
        # 阶段4: AI进行结果解释 (定性)
        interpretation = self.execute_result_interpretation(quantitative_results, theoretical_analysis)
        
        return self.integrate_results(theoretical_analysis, quantitative_results, interpretation)
```

### 智能调用时机
- **理论分析**: 研究开始时，加载`theoretical-analysis.md`
- **校准指导**: 数据分析前，加载`calibration-guidance.md`  
- **定量计算**: 需要精确计算时，调用相应Python脚本
- **结果解释**: 获得统计结果后，加载`result-interpretation.md`

## 使用流程

### 第一阶段: 理论框架构建
**AI任务**: 加载`theoretical-analysis.md`，进行深度理论分析
**输出**: 理论框架、条件选择、因果机制假设
**定量支持**: 无需计算，纯理论思考

### 第二阶段: 校准方案制定  
**AI任务**: 加载`calibration-guidance.md`，结合理论与数据制定校准方案
**输出**: 每个变量的校准方法、阈值设定、理论依据
**定量支持**: 数据特征分析脚本提供数据描述

### 第三阶段: 定量计算执行
**AI任务**: 决策调用哪些计算脚本
**脚本执行**: 
- `calibration.py`: 执行数据校准
- `truth_table.py`: 构建分析真值表  
- `minimization.py`: 执行逻辑最小化
**输出**: 精确的计算结果、质量指标

### 第四阶段: 结果深度解释
**AI任务**: 加载`result-interpretation.md`，进行理论阐释
**输出**: 因果机制解释、理论贡献、实践建议
**定量支持**: 计算结果提供解释基础

## 适用场景

### 学术研究
- **理论构建**: 复杂因果机制的理论化
- **假设检验**: 理论假设的实证验证
- **方法创新**: QCA方法的改进和发展

### 政策分析
- **政策组合**: 多政策协同效应分析
- **条件识别**: 成功政策的关键条件
- **情境适配**: 政策移植的条件要求

### 组织管理  
- **绩效路径**: 高绩效的多重实现路径
- **资源配置**: 资源要素的最优组合
- **变革管理**: 组织变革的成功条件

## 技术特性

### 定性与定量结合
- **定性深度**: AI进行理论思考和机制解释
- **定量精度**: 脚本保证计算的准确性
- **智能协调**: 决策引擎协调两者

### 渐进式信息披露
- **按需加载**: 只在需要时加载相应提示词
- **上下文优化**: 避免无关信息干扰
- **计算独立**: 复杂计算不占用上下文

### 智能化分析流程
- **自动决策**: AI自动判断何时调用何种工具
- **质量保障**: 内置质量检验和改进机制
- **结果整合**: 自动生成完整的分析报告

## 技术特性

### 智能提示词系统
每个提示词文件都采用渐进式结构：
- **任务明确**: 清晰定义AI的具体任务
- **流程指导**: 分步骤的操作指南
- **质量标准**: 明确的质量检验清单
- **输出规范**: 标准化的输出格式

### 高效计算引擎
- **算法优化**: 针对msQCA特点优化的算法
- **错误处理**: 完善的异常处理机制
- **性能监控**: 实时的计算质量监控
- **结果验证**: 多层次的结果验证

### 集成控制系统
- **状态跟踪**: 完整的分析状态管理
- **决策记录**: 所有决策过程的详细记录
- **版本控制**: 分析过程和结果的版本管理
- **审计追踪**: 完整的操作审计日志

## 质量保证体系

### 三层质量控制
1. **输入质量**: 理论一致性和数据完整性检验
2. **过程质量**: 分析逻辑和计算准确性验证
3. **输出质量**: 结果稳健性和理论价值评估

### 智能质量监控
```python
# 自动质量检验示例
def quality_monitor(analysis_results):
    quality_issues = []
    
    # 理论一致性检验
    if not check_theoretical_consistency(analysis_results):
        quality_issues.append("理论一致性不足")
    
    # 计算准确性检验
    if not validate_computational_accuracy(analysis_results):
        quality_issues.append("计算准确性存疑")
    
    # 结果稳健性检验
    if not assess_result_robustness(analysis_results):
        quality_issues.append("结果稳健性不足")
    
    return quality_issues
```

## 开始使用

### 快速启动
```bash
# 进入技能目录
cd msqca-analysis/

# 运行集成分析
python scripts/integrated_analysis.py
```

### 自定义分析
1. 准备研究数据 (CSV格式)
2. 定义研究问题和理论框架
3. 运行集成分析器
4. 根据AI提示进行深度理论分析
5. 获得完整的分析报告

## 扩展资源

### 提示词文件
- `prompts/theoretical-analysis.md`: 理论分析专家提示
- `prompts/calibration-guidance.md`: 校准指导专家提示
- `prompts/result-interpretation.md`: 结果解释专家提示

### 计算脚本
- `scripts/calibration.py`: 数据校准算法
- `scripts/truth_table.py`: 真值表构建算法
- `scripts/minimization.py`: 逻辑最小化算法
- `scripts/integrated_analysis.py`: 集成分析引擎

### 参考文档
- `references/METHODOLOGY.md`: 完整方法论说明
- `references/BEST_PRACTICES.md`: 最佳实践指南
- `assets/templates/`: 数据模板和报告模板

---

**注意**: AI负责理论思考和解释，脚本负责精确计算，通过智能决策引擎实现协作。