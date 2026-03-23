# 批量技能升级指南

**如何高效升级多个技能 - 并行处理策略**

---

## 🎯 适用场景

当你需要升级多个技能时（5个以上），使用并行处理策略可以大幅提升效率。

**效率对比**:
- 单个逐个升级: 10个技能 × 3小时 = 30小时
- 5个并行处理: 2批次 × 3.5小时 = 7小时
- 10个并行处理: 1批次 × 4小时 = 4小时

**加速比**: 4x - 7.5x

---

## 📋 批量升级案例

### 案例背景

**任务**: 升级5个理论类技能

1. digital-durkheim-expert
2. digital-marx-expert
3. digital-weber-expert
4. bourdieu-field-analysis-expert
5. actor-network-analysis-expert

**目标**: 全部升级到5.0.0-cli-native

**策略**: 5个Agent并行处理

---

## Phase 1: 准备 (1小时)

### 1.1 技能分组

```yaml
分组原则:
  - 相似领域分组
  - 共享模板
  - 统一标准

理论组 (5个):
  - Durkheim (社会团结、自杀类型)
  - Marx (阶级分析、剥削)
  - Weber (理性化、权威类型)
  - Bourdieu (场域、资本、习性)
  - ANT (转译、对称性)

共同特点:
  - 都需要经典文献引用
  - 都有核心概念定义
  - 都需要正反案例
```

### 1.2 创建模板

**通用模板** (`templates/theory-skill-template.md`):

```yaml
# 理论类技能升级模板

## Level 1: 6大禁止原则

理论类技能通用原则:
1. 禁止脱离原始文本
2. 禁止断章取义
3. 禁止时代错位
4. 禁止过度简化
5. 禁止概念混淆
6. 禁止忽视批判

## Level 2: 经典文献

每个理论的核心文献（需要定制化）:
- 核心著作1-2本
- 关键论文3-5篇
- 二手文献2-3篇

## Level 3: CLI集成

统一集成模式:
- 任务队列: text-analysis, concept-mapping, case-application
- 状态持久化: 三层架构
- 模型驱动: 直接分析文本

## Level 4: 经验模式

共同模式类型:
- 概念识别模式
- 理论应用模式
- 批判分析模式
```

### 1.3 制定计划

```yaml
时间分配:
  准备: 1小时
  执行: 3.5小时
  验证: 1小时
  ---
  总计: 5.5小时

Agent分配:
  Agent 1: digital-durkheim-expert
  Agent 2: digital-marx-expert
  Agent 3: digital-weber-expert
  Agent 4: bourdieu-field-analysis-expert
  Agent 5: actor-network-analysis-expert

同步点:
  30分钟: Level 1完成检查
  1.5小时: Level 2完成检查
  2.5小时: Level 3完成检查
  3.5小时: Level 4完成检查
  4.5小时: 质量验证
```

---

## Phase 2: 并行执行 (3.5小时)

### 2.1 启动5个Agent

**并行执行命令**:

```bash
# Agent 1 - Durkheim
Agent(subagent_type="general-purpose",
      prompt="升级digital-durkheim-expert到5.0.0-cli-native标准，
            使用theory-skill-template模板，
            重点：社会团结、自杀类型、失范")

# Agent 2 - Marx
Agent(subagent_type="general-purpose",
      prompt="升级digital-marx-expert到5.0.0-cli-native标准，
            使用theory-skill-template模板，
            重点：阶级分析、剥削、异化")

# Agent 3 - Weber
Agent(subagent_type="general-purpose",
      prompt="升级digital-weber-expert到5.0.0-cli-native标准，
            使用theory-skill-template模板，
            重点：理性化、权威类型、理解社会学")

# Agent 4 - Bourdieu
Agent(subagent_type="general-purpose",
      prompt="升级bourdieu-field-analysis-expert到5.0.0-cli-native标准，
            使用theory-skill-template模板，
            重点：场域、资本、习性、动力学")

# Agent 5 - ANT
Agent(subagent_type="general-purpose",
      prompt="升级actor-network-analysis-expert到5.0.0-cli-native标准，
            使用theory-skill-template模板，
            重点：转译、对称性、非人行动者")
```

### 2.2 进度监控

**30分钟检查点** (Level 1):

```yaml
Agent 1 (Durkheim): ✅ Level 1完成
  - 6大禁止: 已定制（社会事实、团结）
  - 任务分解: 已定义（3层）

Agent 2 (Marx): ✅ Level 1完成
  - 6大禁止: 已定制（阶级、剥削）
  - 任务分解: 已定义（3层）

Agent 3 (Weber): ✅ Level 1完成
  - 6大禁止: 已定制（理性化、权威）
  - 任务分解: 已定义（3层）

Agent 4 (Bourdieu): ✅ Level 1完成
  - 6大禁止: 已定制（场域、资本）
  - 任务分解: 已定义（3层）

Agent 5 (ANT): ✅ Level 1完成
  - 6大禁止: 已定制（转译、对称性）
  - 任务分解: 已定义（3层）

状态: 全部正常，继续执行
```

**1.5小时检查点** (Level 2):

```yaml
Agent 1 (Durkheim): ✅ Level 2完成
  - 经典文献: Suicide, Division of Labor
  - 核心概念: 社会事实、团结、失范
  - 成功案例: 自杀率分析

Agent 2 (Marx): ✅ Level 2完成
  - 经典文献: Capital, Communist Manifesto
  - 核心概念: 阶级、剥削、异化
  - 成功案例: 外卖平台分析

Agent 3 (Weber): ✅ Level 2完成
  - 经典文献: Economy & Society, Protestant Ethic
  - 核心概念: 理性化、权威、理解
  - 成功案例: 平台理性化分析

Agent 4 (Bourdieu): ✅ Level 2完成
  - 经典文献: Distinction, Logic of Practice
  - 核心概念: 场域、资本、习性
  - 成功案例: 学术场域分析

Agent 5 (ANT): ✅ Level 2完成
  - 经典文献: Science in Action, Aramis
  - 核心概念: 转译、对称性、黑箱
  - 成功案例: 技术实施追踪

状态: 全部正常，继续执行
```

**3.5小时检查点** (全部完成):

```yaml
最终状态:
  Agent 1 (Durkheim): ✅ 全部4个Level完成
  Agent 2 (Marx): ✅ 全部4个Level完成
  Agent 3 (Weber): ✅ 全部4个Level完成
  Agent 4 (Bourdieu): ✅ 全部4个Level完成
  Agent 5 (ANT): ✅ 全部4个Level完成

完成率: 100% (5/5)
平均质量: 5/5 ⭐⭐⭐⭐⭐
总耗时: 3.5小时
```

---

## Phase 3: 质量验证 (1小时)

### 3.1 交叉验证

```yaml
验证策略:
  - Agent间交叉检查
  - 一致性验证
  - 质量评分

验证项:
  ☑ 目录结构一致性
  ☑ 文档格式统一
  ☑ Level完整性
  ☑ CLI集成正确性
  ☑ 案例质量

验证结果:
  Durkheim: 25/25 ✅
  Marx: 25/25 ✅
  Weber: 25/25 ✅
  Bourdieu: 25/25 ✅
  ANT: 25/25 ✅

一致性: 100% ✅
```

### 3.2 最终报告

```yaml
批量升级完成报告:

投入时间:
  准备: 1小时
  执行: 3.5小时
  验证: 1小时
  ---
  总计: 5.5小时

升级成果:
  技能数: 5个
  完成率: 100%
  平均质量: 5/5
  总文档量: ~12,000行

效率对比:
  单个升级: 5 × 3小时 = 15小时
  批量升级: 5.5小时
  加速比: 2.7x

交付物:
  SKILL.md: 5个
  经典文献: 25篇
  成功案例: 5个
  失败案例: 5个
  经验模式: 15个
```

---

## 💡 批量升级最佳实践

### DO (推荐做法)

```yaml
✅ 准备充分:
  - 提前创建模板
  - 明确任务要求
  - 制定详细计划

✅ 并行处理:
  - 使用多个Agent
  - 同时执行升级
  - 定期同步进度

✅ 质量控制:
  - 定期检查点
  - 交叉验证
  - 统一标准

✅ 经验共享:
  - Agent间共享模式
  - 复用成功经验
  - 避免重复错误
```

### DON'T (避免做法)

```yaml
❌ 不要顺序执行:
  - 效率低下
  - 时间浪费

❌ 不要缺少模板:
  - 导致不一致
  - 质量参差不齐

❌ 不要缺少监控:
  - 无法及时发现
  - 问题扩散

❌ 不要跳过验证:
  - 质量风险
  - 一致性问题
```

---

## 🚀 扩展到更大规模

### 10个技能并行

```yaml
策略: 2批次，每批5个

批次1 (3.5小时):
  - 理论类5个
  - Agent 1-5并行

批次2 (3.5小时):
  - 方法类5个
  - Agent 6-10并行

验证 (1小时):
  - 交叉验证
  - 一致性检查

总计: 8小时
效率: 3.75x加速
```

### 14个技能并行（实际案例）

```yaml
策略: 3批次

批次1 (3.5小时):
  - 5个理论类

批次2 (3.5小时):
  - 5个方法类（已有Level 3&4）

批次3 (3.5小时):
  - 4个应用类（已有Level 3&4）

验证 (1.5小时):
  - 全面验证
  - 最终报告

总计: 12小时
实际: 单日完成
效率: 3.5x加速
```

---

## 📊 效率分析

### 规模经济效应

```yaml
单个升级:
  时间: 3小时
  开销: 0
  总计: 3小时

5个并行:
  准备: 1小时
  执行: 3.5小时
  验证: 1小时
  总计: 5.5小时
  平均: 1.1小时/个

10个并行:
  准备: 1.5小时
  执行: 7小时
  验证: 1.5小时
  总计: 10小时
  平均: 1小时/个

14个并行:
  准备: 2小时
  执行: 10.5小时
  验证: 2小时
  总计: 14.5小时
  平均: 1小时/个

结论: 批量越大，效率越高
```

---

## 🎯 快速开始

### 检查清单

```yaml
批量升级准备:
  ☑ 确定要升级的技能列表
  ☑ 按领域分组
  ☑ 创建通用模板
  ☑ 制定详细计划
  ☑ 准备Agent提示词

执行阶段:
  ☑ 启动所有Agent
  ☑ 设置检查点
  ☑ 监控进度
  ☑ 及时处理问题

验证阶段:
  ☑ 交叉验证
  ☑ 一致性检查
  ☑ 质量评分
  ☑ 生成报告
```

---

## 🎉 成功案例

### 已完成的批量升级

**项目**: 升级14个研究方法技能

**策略**: 3批次并行处理

**结果**:
- 完成率: 100%
- 平均质量: 5/5
- 总耗时: 1个工作日
- 文档量: ~30,000行

**证明**: 批量升级策略高效可行！

---

**开始你的批量升级之旅！**
