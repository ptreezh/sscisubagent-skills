---
metadata:
  version: "5.0.0-cli-native"
  methodology: "System Dynamics Modeling"
  absolute-prohibitions: true
  task-decomposition-rules: true
  ai-cli-native: true
  task-queue-support: true
  agentskills-io: true
  cross-platform: true
  state-persistence: true
  self-iteration: true
  academic-alignment: true
  subagent-support: true
  created: "2026-03-08"
  updated: "2026-03-08"
  author: "SocienceAI Methodology Expert"
  license: "MIT"
  alignment_reference: "grounded-theory-coding (v5.0.0)"
---

# 系统动力学专家 - 子Agent支持示例

## 子Agent调用模式

### 1. 问题界定阶段

```yaml
子Agent调用:
  - agent: grounded-theory-expert
    task: "从利益相关者访谈中提取关键变量"
    reason: "确保模型基于真实问题感知"
    input:
      - 访谈记录
      - 开放编码结果
    output:
      - 关键变量清单
      - 变量间因果假设
      - 问题边界建议

  - agent: survey-design-expert
    task: "设计量化测量方案"
    reason: "变量可测量性和数据收集"
    input:
      - 关键变量清单
      - 测量概念
    output:
      - 测量指标
      - 问卷设计
      - 数据收集计划
```

### 2. 系统建模阶段

```yaml
子Agent调用:
  - agent: social-network-analysis-expert
    task: "分析影响传播的网络结构"
    reason: "信息扩散和社会影响建模"
    input:
      - 互动网络数据
      - 传播路径
    output:
      - 网络指标
      - 影响函数
      - 网络参数

  - agent: data-analysis-expert
    task: "时间序列分析与模式识别"
    reason: "参考模式提取和模型校准"
    input:
      - 历史时间序列
      - 变量数据
    output:
      - 参考模式图
      - 趋势和周期
      - 参数初值
```

### 3. 仿真与政策分析阶段

```yaml
子Agent调用:
  - agent: qca-analysis-expert
    task: "识别政策成功的条件构型"
    reason: "理解干预成功的多重路径"
    input:
      - 多情景仿真结果
      - 政策变量组合
    output:
      - 必要/充分条件
      - 政策构型
      - 因果路径

  - agent: business-ecosystem-expert
    task: "分析政策对生态系统的影响"
    reason: "理解系统间反馈和溢出效应"
    input:
      - 政策情景
      - 生态系统边界
    output:
      - 跨系统影响
      - 反馈回路
      - 意外后果
```

## 完整示例：公共卫生政策建模

```yaml
主任务: "建立传染病防控政策系统动力学模型"

Phase 1: 问题界定 (1周)
  调用 grounded-theory-expert:
    任务: 分析公共卫生专家认知
    输入: 专家访谈记录
    输出:
      - 关键变量（易感/感染/康复）
      - 行为反馈（戴口罩/社交距离）
      - 政策干预点

  调用 survey-design-expert:
    任务: 设计公众行为调查
    输入: 行为变量清单
    输出:
      - 问卷设计
      - 行为测量指标
      - 抽样策略

Phase 2: 系统建模 (2周)
  调用 social-network-analysis-expert:
    任务: 分析接触网络结构
    输入: 社交接触数据
    输出:
      - 网络类型和参数
      - 传播速度估计
      - 超级传播者识别

  调用 data-analysis-expert:
    任务: 历史疫情数据校准
    输入: 过去疫情时间序列
    输出:
      - 传播率估计
      - 参数分布
      - 参考模式

Phase 3: 政策分析 (2周)
  调用 qca-analysis-expert:
    任务: 识别有效政策组合
    输入: 50种政策情景仿真
    输出:
      - 必要政策条件
      - 政策构型
      - 跨部门协同

  调用 business-ecosystem-expert:
    任务: 评估经济社会影响
    输入: 政策情景结果
    输出:
      - 经济成本分析
      - 社会接受度
      - 生态系统影响
```

## 子Agent协作原则

1. **问题界定**
   - 用质性方法确保模型相关性
   - 用调研确保变量可测量

2. **模型构建**
   - 用网络分析改进社会影响建模
   - 用数据分析支持参数估计

3. **政策设计**
   - 用QCA识别多重因果路径
   - 用生态分析评估系统影响
