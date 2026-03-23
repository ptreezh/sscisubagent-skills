---
metadata:
  version: "5.0.0-cli-native"
  methodology: "Business Model Analysis (Osterwalder, Value Proposition Design)"
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

# 商业模式分析专家 - 子Agent支持示例

## 子Agent调用模式

### 1. 画布构建阶段

```yaml
子Agent调用:
  - agent: grounded-theory-expert
    task: "从客户访谈提取价值主张"
    reason: "确保价值主张基于真实需求"
    input:
      - 客户访谈记录
      - 开放编码结果
    output:
      - 客户痛点主题
      - 价值主张要素
      - 差异化维度

  - agent: survey-design-expert
    task: "设计客户细分问卷"
    reason: "量化客户细分和需求"
    input:
      - 初步客户细分
      - 价值假设
    output:
      - 问卷设计
      - 抽样策略
      - 数据收集计划
```

### 2. 深度分析阶段

```yaml
子Agent调用:
  - agent: data-analysis-expert
    task: "分析财务数据验证盈利模式"
    reason: "收入和成本模式的数据驱动分析"
    input:
      - 财务报表
      - 收入数据
      - 成本数据
    output:
      - 收入模式分析
      - 成本结构分析
      - 趋势和模式
      - 关键指标

  - agent: social-network-analysis-expert
    task: "分析客户关系网络"
    reason: "理解客户获取和传播机制"
    input:
      - 客户互动数据
      - 推荐网络
    output:
      - 网络结构
      - 影响者识别
      - 传播路径
```

### 3. 竞争与创新阶段

```yaml
子Agent调用:
  - agent: business-ecosystem-expert
    task: "分析企业在生态系统中的定位"
    reason: "理解生态位和共生关系"
    input:
      - 企业定位
      - 合作伙伴
      - 竞争对手
    output:
      - 生态位分析
      - 共生关系
      - 价值网络

  - agent: qca-analysis-expert
    task: "识别成功商业模式的构型"
    reason: "理解多重并发因果关系"
    input:
      - 多个商业模式案例
      - 成功/失败标记
    output:
      - 必要条件
      - 充分条件
      - 因素构型
      - 等效路径
```

## 完整示例：SaaS公司商业模式分析

```yaml
主任务: "分析某SaaS公司商业模式"

Phase 1: 画布构建 (1.5小时)
  调用 grounded-theory-expert:
    任务: 提取客户价值主张
    输入: 20份客户访谈
    输出:
      - 客户痛点主题（5个）
      - 价值主张要素（8个）
      - 差异化维度（3个）
      - 价值层级

  调用 survey-design-expert:
    任务: 设计客户细分问卷
    输入: 初步3个细分
    输出:
      - 问卷设计（15题）
      - 抽样策略（n=500）
      - 数据收集计划
      - 细分验证方法

Phase 2: 深度分析 (2.5小时)
  调用 data-analysis-expert:
    任务: 分析SaaS财务模式
    输入: 3年财务数据
    输出:
      - 收入模式分析（ARR/MRR/Churn）
      - 成本结构分析（CAC/LTV/固定成本）
      - 单位经济模型
      - 趋势和预测

  调用 social-network-analysis-expert:
    任务: 分析客户推荐网络
    输入: 客户推荐数据
    输出:
      - 网络结构（小世界特征）
      - 影响者识别（TOP 10%）
      - 推荐路径
      - 病毒系数

Phase 3: 竞争与创新 (1.5小时)
  调用 business-ecosystem-expert:
    任务: 分析SaaS生态位
    输入:
      - 公司定位
      - 5个竞争对手
      - 合作伙伴
    输出:
      - 生态位分析（中等企业/CRM）
      - 共生关系（平台/集成商）
      - 价值网络地图

  调用 qca-analysis-expert:
    任务: 识别SaaS成功构型
    输入: 20个SaaS案例
    输出:
      - 成功必要条件（3个）
      - 成功充分构型（2条路径）
      - 因素组合
      - 等效策略
```

## 子Agent协作原则

1. **画布构建**
   - 用质性方法确保价值主张真实性
   - 用调研量化客户细分

2. **深度分析**
   - 用数据分析验证财务模式
   - 用网络分析理解客户传播

3. **竞争与创新**
   - 用生态分析定位企业
   - 用QCA识别成功模式
