---
name: rct-experimental-design-expert
description: |
  Randomized Controlled Trial (RCT) design expert. Provides randomization procedures, control group design, blind/mask protocols, sample size calculation, and causal inference framework. Suitable for clinical trials, experimental research, and impact evaluation.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

------|---------|------|
| 平行设计 | 最常用 | 两组同时进行，比较干预效果 |
| 交叉设计 | 慢性病、稳定状态 | 每个受试者接受多种干预 |
| 因子设计 | 多因素研究 | 同时评估多个干预组合 |
| 集群随机 | 群体干预 | 以群体为单位随机化 |
| 适应性设计 | 灵活研究 | 根据中期结果调整设计 |

## 设计流程

```
步骤1: 研究问题定义 (PICO框架)
   ↓
步骤2: 设计类型选择
   ↓
步骤3: 样本量计算
   ↓
步骤4: 随机化方案
   ↓
步骤5: 盲法设计
   ↓
步骤6: 结局指标选择
   ↓
步骤7: 数据收集计划
   ↓
步骤8: 统计分析计划
   ↓
步骤9: 伦理审查准备
   ↓
步骤10: 试验注册
```

## PICO框架

| 要素 | 定义 | 示例 |
|------|------|------|
| P (Population) | 目标人群 | 2型糖尿病患者 |
| I (Intervention) | 干预措施 | 新型口服药物 |
| C (Comparison) | 对照措施 | 安慰剂/标准治疗 |
| O (Outcome) | 结局指标 | HbA1c降低幅度 |

## 样本量计算

### 连续结局变量

$$n = \frac{2(Z_{\alpha/2} + Z_{\beta})^2 \sigma^2}{\Delta^2}$$

### 二分类结局变量

$$n = \frac{(Z_{\alpha/2} + Z_{\beta})^2 \times [p_1(1-p_1) + p_2(1-p_2)]}{(p_1 - p_2)^2}$$

### 关键参数

| 参数 | 说明 | 典型值 |
|------|------|--------|
| α | I型错误率 | 0.05 |
| 1-β | 检验效能 | 0.80-0.90 |
| Δ | 最小临床重要差异 | 研究确定 |
| σ | 标准差 | 估计或文献 |
| 脱落率 | 预计失访 | 10-20% |

## 随机化方法

| 方法 | 特点 | 适用场景 |
|------|------|---------|
| 简单随机 | 完全随机 | 大样本研究 |
| 区组随机 | 组间平衡 | 常用 |
| 分层随机 | 控制混杂 | 重要预后因素 |
| 最小化法 | 动态平衡 | 小样本研究 |
| 协变量自适应 | 实时平衡 | 多中心研究 |

## 盲法设计

| 类型 | 干预提供者 | 受试者 | 结局评估者 | 数据分析师 |
|------|-----------|--------|-----------|-----------|
| 开放试验 | 否 | 否 | 否 | 否 |
| 单盲 | 是/否 | 是 | 否 | 否 |
| 双盲 | 是 | 是 | 是 | 否 |
| 三盲 | 是 | 是 | 是 | 是 |

## 分析原则

### 意向性分析(ITT)
- 所有随机分配的受试者都纳入分析
- 保持随机化的完整性
- 主要分析应采用ITT

### 符合方案分析(PP)
- 仅分析完成研究的受试者
- 可能引入偏倚
- 敏感性分析使用

### 处理效应估计
- 连续结局：均值差异，95% CI
- 二分类结局：相对风险(RR)，比值比(OR)，风险差(RD)
- 时间-事件结局：风险比(HR)

## CONSORT报告清单

| 项目 | 内容 |
|------|------|
| 标题 | 明确说明"随机对照试验" |
| 摘要 | 结构化摘要 |
| 背景 | 科学背景和原理 |
| 方法-参与者 | 入选/排除标准 |
| 方法-干预 | 干预详情 |
| 方法-结局 | 主要/次要结局 |
| 方法-样本量 | 计算方法 |
| 方法-随机化 | 序列生成、隐藏 |
| 方法-盲法 | 实施方法 |
| 结果-流程 | 受试者流程图 |
| 结果-基线 | 人口学特征 |
| 结果-结局 | 主要结果 |

## 使用示例

```
用户: 设计一个评估新型降压药疗效的RCT

AI: 我将为您设计一个符合CONSORT标准的平行随机对照试验：

## 研究设计概要

**设计类型**: 平行、双盲、安慰剂对照RCT

**PICO框架**:
- P: 18-75岁原发性高血压患者
- I: 新型降压药 10mg qd
- C: 安慰剂
- O: 8周后收缩压下降幅度

**样本量计算**:
- 预期差异: 5mmHg
- 标准差: 10mmHg
- α = 0.05, β = 0.20
- n = 64/组 × 1.2(脱落率) = 77/组

**随机化**: 区组随机化，区组大小4

**盲法**: 双盲，胶囊外观一致

[继续详细设计...]
```

## 🚫 绝对禁止原则

> **使用前必读**：以下原则是不可逾越的红线，违反将导致RCT结论失效。

1. **禁止随机化不充分** — 随机序列生成和分配隐藏不完善，导致选择性偏倚和基线不平衡
2. **禁止主要分析不采用ITT原则** — 意向性分析是RCT的金标准，违反ITT的符合方案分析(PP)会高估治疗效果
3. **禁止盲法实施不完整** — 声称"双盲"但实际无法实施或破盲未报告，导致实施偏倚
4. **禁止样本量计算依据不充分** — 不报告α、β、效应量、脱落率的设定依据，导致检验力不足
5. **禁止主要结局事后变更** — 试验过程中更改主要结局指标，导致假阳性风险增加（p-hacking）
6. **禁止未进行注册和方案公开** — 研究未在公共注册平台（如ChiCTR、ClinicalTrials.gov）预先注册，导致发表偏倚和选择性报告

## ✅ 质量标准

### 完整性
- 必做项清单完成度 ≥ 90%
- CONSORT清单完成度高
- 研究注册信息完整

### 方法论
- 理论框架与数据一致性 ≥ 90%
- 分析步骤可复现性高
- 随机化和盲法规范

### 深度
- 核心维度覆盖 ≥ 80%
- ITT + PP双分析
- 敏感性分析完整

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | sample_size_calculator.py | RCT样本量计算（连续/二分类结局），支持α、β、效应量、脱落率参数 |
| 2 | randomization_generator.py | 随机化序列生成（简单/区组/分层/最小化），支持分配隐藏 |
| 3 | consort_checker.py | CONSORT清单检查，支持2010版25项清单对照 |
| 4 | iit_analyzer.py | 意向性分析，支持ITT、PP、MI多重插补分析 |

### CLI用法

```bash
python tools/sample_size_calculator.py --continuous --mean-diff 5 --std-dev 10 --power 0.8
python tools/randomization_generator.py --method block --n 200 --block-size 4
```

## 参考文献

1. Schulz, K.F., et al. (2010). CONSORT 2010 Statement. *BMJ*, 340, c332.
2. Chan, A.W., et al. (2013). SPIRIT 2013 Statement. *Annals of Internal Medicine*, 158(3), 200-207.
3. Friedman, L.M., et al. (2015). *Fundamentals of Clinical Trials*. 5th ed. Springer.
4. ICH-GCP E6(R2). (2016). Guideline for Good Clinical Practice.

---

**技能版本**: 5.0.0  
**方法论标准**: CONSORT 2010, SPIRIT 2013  
**创建时间**: 2026-03-15