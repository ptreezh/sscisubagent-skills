---
metadata:
  version: "5.0.0-cli-native"
  methodology: "Complex Adaptive Systems & Agent-Based Modeling"
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

# CAS仿真专家 - 子Agent支持示例

## 子Agent调用模式

### 1. 概念建模阶段

```yaml
子Agent调用:
  - agent: social-network-analysis-expert
    task: "分析创新扩散网络结构"
    reason: "确定网络拓扑对扩散模式的影响"
    input:
      - 主体类型列表
      - 互动规则草案
    output:
      - 网络结构分析
      - 关键节点识别
      - 网络参数建议

  - agent: grounded-theory-expert
    task: "从实证数据中提取主体行为模式"
    reason: "确保主体行为基于真实观察"
    input:
      - 访谈或观察数据
      - 开放编码结果
    output:
      - 行为规则草案
      - 异质性维度
```

### 2. 技术实现阶段

```yaml
子Agent调用:
  - agent: data-analysis-expert
    task: "分析历史数据用于模型校准"
    reason: "参数估计和模式验证"
    input:
      - 时间序列数据
      - 主体属性数据
    output:
      - 参数估计值
      - 分布类型
      - 校准目标

  - agent: system-dynamics-expert
    task: "对比ABM与SD模型结果"
    reason: "跨方法验证和洞察"
    input:
      - ABM仿真结果
      - 系统边界定义
    output:
      - 对比分析
      - 方法优势对比
```

### 3. 验证与分析阶段

```yaml
子Agent调用:
  - agent: qca-analysis-expert
    task: "识别涌现条件的构型"
    reason: "理解微观-宏观链接机制"
    input:
      - 多次仿真结果
      - 涌现模式标记
    output:
      - 必要/充分条件
      - 因素构型
      - 因果路径

  - agent: survey-design-expert
    task: "设计仿真结果验证问卷"
    reason: "与真实世界数据对比"
    input:
      - 仿真预测
      - 关键变量
    output:
      - 问卷设计
      - 数据收集计划
```

## 完整示例：创新扩散研究

```yaml
主任务: "模拟创新在社会网络中的扩散"

Phase 1: 概念建模 (30分钟)
  调用 social-network-analysis-expert:
    任务: 分析目标网络结构
    输入: 网络数据或拓扑描述
    输出:
      - 网络类型（小世界/无标度/随机）
      - 关键指标（聚类系数/平均路径长度）
      - 中心性分布

  调用 grounded-theory-expert:
    任务: 提取采用行为模式
    输入: 采用者访谈数据
    输出:
      - 采用决策因素
      - 异质性维度
      - 行为规则草案

Phase 2: 模型实现 (60分钟)
  调用 data-analysis-expert:
    任务: 历史扩散数据校准
    输入: 过去创新采用时间序列
    输出:
      - 传播率参数
      - 临界点估计
      - 采用曲线拟合

Phase 3: 验证与分析 (60分钟)
  调用 qca-analysis-expert:
    任务: 识别成功扩散的构型
    输入: 100次蒙特卡洛仿真结果
    输出:
      - 临界质量条件
      - 网络结构+创新特征构型
      - 多重并发路径

  调用 survey-design-expert:
    任务: 设计实证验证方案
    输入: 仿真关键预测
    输出:
      - 验证假设清单
      - 测量变量
      - 抽样策略
```

## 子Agent协作原则

1. **明确职责边界**
   - 主Agent负责ABM框架和仿真
   - 子Agent提供专门领域洞察

2. **标准化接口**
   - 输入: 清晰的数据需求
   - 输出: 结构化结果

3. **迭代优化**
   - 基于子Agent洞察调整模型
   - 多轮对话直到满意

4. **验证整合**
   - 对比多个子Agent建议
   - 整合互补视角
