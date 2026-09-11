---
metadata:
  version: "5.0.0-cli-native"
  methodology: "Business Ecosystem Analysis (Moore, Iansiti)"
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

# 商业生态分析专家 - 子Agent支持示例

## 子Agent调用模式

### 1. 生态结构分析阶段

```yaml
子Agent调用:
  - agent: social-network-analysis-expert
    task: "分析生态系统参与者网络"
    reason: "识别关键物种和网络结构"
    input:
      - 参与者清单
      - 互动关系数据
    output:
      - 网络拓扑结构
      - 中心性指标
      - 社群识别
      - 关键节点

  - agent: business-model-expert
    task: "分析关键参与者商业模式"
    reason: "理解价值创造和捕获机制"
    input:
      - 关键参与者列表
      - 商业文档
    output:
      - 商业模式画布
      - 价值主张
      - 收入模式
```

### 2. 共生成因分析阶段

```yaml
子Agent调用:
  - agent: grounded-theory-expert
    task: "从访谈中提取价值共创机制"
    reason: "理解合作和价值创造过程"
    input:
      - 合作伙伴访谈
      - 客户反馈
    output:
      - 价值共创主题
      - 合作机制
      - 利益分配模式

  - agent: data-analysis-expert
    task: "量化价值流动分析"
    reason: "测量价值分配效率"
    input:
      - 交易数据
      - 财务数据
    output:
      - 价值流动模式
      - 分配公平性
      - 效率指标
```

### 3. 演化分析阶段

```yaml
子Agent调用:
  - agent: cas-simulation-expert
    task: "模拟生态系统演化"
    reason: "预测未来演化轨迹"
    input:
      - 互动规则
      - 初始状态
    output:
      - 演化情景
      - 临界点
      - 涌现模式

  - agent: system-dynamics-expert
    task: "建模生态反馈回路"
    reason: "理解生态动态机制"
    input:
      - 因果假设
      - 关键变量
    output:
      - Stock-Flow模型
      - 反馈回路
      - 动态行为
```

## 完整示例：平台生态系统分析

```yaml
主任务: "分析某数字平台生态系统"

Phase 1: 生态结构分析 (2小时)
  调用 social-network-analysis-expert:
    任务: 分析平台参与者网络
    输入: 平台互动数据
    输出:
      - 网络类型（小世界/无标度）
      - 关键参与者（中心性>0.7）
      - 社群结构
      - 桥接节点

  调用 business-model-expert:
    任务: 分析平台关键参与者商业模式
    输入: 商业文档
    输出:
      - 平台商业模式画布
      - 核心企业价值主张
      - 合作伙伴收入模式
      - 成本结构

Phase 2: 共生成因分析 (2.5小时)
  调用 grounded-theory-expert:
    任务: 提取价值共创机制
    输入: 30份深度访谈
    输出:
      - 价值共创主题
      - 合作机制编码
      - 利益分配模式
      - 信任机制

  调用 data-analysis-expert:
    任务: 量化价值流动
    输入: 交易数据（12个月）
    输出:
      - 价值流动网络图
      - 分配公平性指数
      - 效率指标
      - 不平衡识别

Phase 3: 演化分析 (2小时)
  调用 cas-simulation-expert:
    任务: 模拟平台演化
    输入:
      - 参与者互动规则
      - 初始网络结构
    输出:
      - 3年演化情景
      - 网络效应临界点
      - 涌现模式
      - 稳定性分析

  调用 system-dynamics-expert:
    任务: 建模生态动态
    输入:
      - 关键变量（用户/开发者/收入）
      - 反馈假设
    输出:
      - Stock-Flow模型
      - 主要反馈回路
      - 动态行为模式
      - 政策杠杆点
```

## 子Agent协作原则

1. **结构分析**
   - 用网络分析识别生态结构
   - 用商业模式理解价值机制

2. **机制分析**
   - 用质性方法提取共创机制
   - 用量化分析测量价值流动

3. **演化预测**
   - 用CAS模拟微观互动
   - 用SD建模宏观动态
