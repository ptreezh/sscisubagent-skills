---
name: secondary-analysis-expert
description: |
  Secondary Analysis expert. Provides existing dataset reanalysis, variable recoding, methodological adaptation, new research question formulation, and archival data mining. Suitable for social science research, data reuse, and secondary data investigation.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

## 基本信息

**名称**: secondary-analysis-expert (二手数据分析专家)
**版本**: 2.0.0
**理论基础**: Kiecolt & Nathan (1985) · Stewart & Kamins (1993) · Riley (2018) · Smith (2008)
**许可证**: MIT

---

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | data_quality_assessor.py | 数据质量评估（5维评估/适用性判断/限制识别） |
| 2 | trend_analyzer.py | 趋势分析（时间序列/跨期比较/变化检测） |
| 3 | variable_reconstructor.py | 变量重构（从原始变量构建新变量/跨数据集对齐） |

### 使用示例

```bash
# 1. 数据质量评估
python tools/data_quality_assessor.py \
  --data-info data/quality_info.json \
  --output results/quality.json

# 2. 趋势分析
python tools/trend_analyzer.py \
  --input data/time_series.json \
  --output results/trend.json

# 3. 变量重构
python tools/variable_reconstructor.py \
  --input data/original_vars.json \
  --output results/reconstructed.json
```

---

## 核心能力

### 1. 二手数据分析方法论

**Kiecolt & Nathan (1985) 二手分析特点：**

```
二手数据分析 = 使用他人收集的数据回答新研究问题

优势:
  ├── 经济性: 不需要自己收集数据
  ├── 大样本: 可利用大型调查
  ├── 历史数据: 可研究历史现象
  └── 比较可能: 跨数据集比较

挑战:
  ├── 概念不匹配: 原变量 ≠ 你的概念
  ├── 测量差异: 不同时期/研究测量不同
  └── 伦理复杂: 被研究者同意用于当前研究？
```

### 2. Stewart & Kamins (1993) 数据质量评估

**DataQualityAssessor 工具使用：**

```python
# 定义数据信息
data_info = {
    "conceptual_validity": 0.8,         # 概念效度
    "sample_representativeness": 0.7,    # 样本代表性
    "data_completeness": 0.9,           # 数据完整性
    "measurement_reliability": 0.75,     # 测量可靠性
    "documentation_quality": 0.85        # 文档质量
}

assessor = DataQualityAssessor()
result = assessor.assess(data_info)

# 输出: overall_score / dimensions / suitability / limitations / recommendations
# 综合评分: 加权平均 (conceptual:25%, sample:25%, completeness:20%, reliability:15%, docs:15%)
```

**质量评估五维度：**

| 维度 | 权重 | 评估问题 |
|------|------|---------|
| 概念效度 | 25% | 变量是否测量了你声称的概念？ |
| 样本代表性 | 25% | 样本能否代表目标总体？ |
| 数据完整性 | 20% | 数据缺失程度如何？ |
| 测量可靠性 | 15% | 测量是否一致？ |
| 文档质量 | 15% | 代码本/文档是否完整？ |

### 3. Riley (2018) 大型调查数据分析

**大型调查数据使用注意事项：**

```
复杂抽样设计:
  - 调查通常使用分层/整群/多阶段抽样
  - 需要加权才能获得总体估计
  - 标准误计算需考虑设计效应

权重使用原则:
  ├── 分析权重: 用于描述总体特征
  ├── 重新标准化权重: 用于子群分析
  └── 不使用权重: 当样本本身代表总体时

设计效应:
  - 复杂抽样的标准误 > 简单随机抽样
  - 需要使用特殊方法（Taylor展开/刀切法/自助法）
```

### 4. Smith (2008) 比较研究中的二手数据

**跨数据集比较的挑战：**

```
测量等价性（Measurement Equivalence）:
  - 同样的概念在不同时期/群体是否测量相同？
  - 例: "教育程度"在不同时期的分类标准可能不同

历史情境化:
  - 变量含义随时间变化
  - 例: 1960年代的"家庭收入" vs 2020年代的"家庭收入"
  - 需要历史知识来正确解释数据

数据集整合:
  - 变量命名不一致
  - 编码系统不同
  - 需要仔细的匹配和转换
```

---

## ⚠️ 六大绝对禁止原则

### 1. 禁止忽视原始研究设计

**错误做法**:
```yaml
研究设计黑箱:
  - 把数据当作"自然产生"的
  - 不问原始研究的抽样设计
  - 不考虑原始研究的局限性

示例:
  "这个全国调查数据显示X"
  （未问：这个调查的抽样设计是什么？是否有覆盖率问题？）
```

**正确做法**:
```yaml
研究设计追溯:
  Step 1: 找到原始研究设计文档
    - 抽样设计是什么？
    - 问卷是如何设计的？
    - 收集过程是怎样的？

  Step 2: 评估对当前分析的适用性
    - 原始设计是否满足当前研究需要？
    - 有哪些设计局限需要承认？

  工具辅助:
    python tools/data_quality_assessor.py --data-info data_info.json --output quality.json
```

### 2. 禁止忽视数据收集局限

**错误做法**:
```yaml
数据客观幻觉:
  - 把数据当作"客观事实"
  - 不问数据是如何产生的
  - 忽略产生过程中的偏差

示例:
  "数据显示A导致了B"
  （未问：数据收集过程中是否有系统性偏差？）
```

**正确做法**:
```yaml
数据产生批判:
  - 数据是如何收集的？（自填/访谈/观察）
  - 收集者是谁？（研究者/政府/商业机构）
  - 收集目的是什么？（与当前研究目的匹配吗？）
  - 有什么已知的收集局限？
```

### 3. 禁止过度解释数据

**错误做法**:
```yaml
数据过度延伸:
  - "相关性证明了因果性"
  - 不考虑替代解释
  - 忽略统计不确定性

示例:
  "数据显示使用社交媒体与抑郁正相关，因此社交媒体导致抑郁"
  （未问：是否是反向因果？是否有混淆变量？相关性有多强？）
```

**正确做法**:
```yaml
解释约束:
  - 明确区分相关与因果
  - 报告效应量和置信区间
  - 讨论替代解释
  - 承认统计不确定性

  因果推断需要:
    1. 时间顺序（因在果之前）
    2. 关联（因与果相关）
    3. 无替代解释（排除混淆）
    4. 机制（因果如何发生）
```

### 4. 禁止忽视测量等价性

**错误做法**:
```yaml
测量等同假设:
  - 假设同样的变量在不同时期测量相同
  - 跨群体比较时不考虑测量差异
  - 用名义上有相同名称的变量直接比较

示例:
  直接比较1960年和2020年的"职业地位"
  （未问：职业分类标准是否改变？）
```

**正确做法**:
```yaml
测量等价性检验:
  Step 1: 检查变量定义
    - 变量在不同时期/群体是否定义相同？
    - 编码系统是否一致？

  Step 2: 检验测量等价性
    - 如果有多个指标，是否在群体间测量相同？

  Step 3: 谨慎比较
    - 如果不等价，比较需加注
    - 考虑变量重构

  工具辅助:
    python tools/variable_reconstructor.py --input data.json --output reconstructed.json
```

### 5. 禁止忽视样本代表性

**错误做法**:
```yaml
代表性问题:
  - 把样本发现推广到更大的总体
  - 不问样本如何选取
  - 不考虑无响应偏差

示例:
  "大学生样本显示X，因此年轻人普遍有X特征"
  （大学生能代表所有年轻人吗？）
```

**正确做法**:
```yaml
代表性评估:
  Step 1: 评估样本与目标总体的差异
    - 抽样框架是什么？
    - 响应率是多少？
    - 无响应者与响应者有何差异？

  Step 2: 调整推断范围
    - 结论可以推广到哪个总体？
    - 在哪里需要加注？

  Step 3: 敏感性分析
    - 在不同假设下结论是否稳健？
```

### 6. 禁止忽视伦理问题

**错误做法**:
```yaml
伦理豁免:
  - "数据是匿名的所以没问题"
  - 不考虑被研究者同意范围
  - 不报告二次使用的伦理审查

示例:
  "使用了政府发布的公开数据集进行研究"
  （未问：原始被研究者是否同意了这种二次使用？）
```

**正确做法**:
```yaml
伦理审查:
  Step 1: 检查数据使用协议
    - 原始研究是否允许二次使用？
    - 是否需要额外同意？

  Step 2: 评估隐私风险
    - 即是匿名数据，是否可能间接识别？
    - "马赛克效应"：多处信息可识别身份

  Step 3: 报告伦理情况
    - 说明伦理审查情况
    - 讨论数据使用限制
    - 在发表时注明数据来源和使用合规性
```

---

## 适用场景

- ✅ 档案数据再分析（政府统计/历史调查）
- ✅ 大型调查数据利用（CGSS/CFPS/CSS等中国数据）
- ✅ 跨时间趋势分析（追踪社会变迁）
- ✅ 跨群体比较（年龄/地区/阶层）
- ✅ 元分析数据整合（多研究数据合并）
- ✅ 政策评估数据二次利用

---

## 实施流程

### Phase 1: 数据源识别与获取

```
步骤:
  1. 识别潜在二手数据源
  2. 评估数据可获取性
  3. 获取数据使用许可
  4. 了解数据收集背景
```

### Phase 2: 数据质量评估

```
使用 data_quality_assessor.py:
  python tools/data_quality_assessor.py \
    --data-info data/quality_info.json \
    --output results/quality.json

  输出: overall_score / dimensions / suitability / limitations / recommendations
```

### Phase 3: 变量重构

```
使用 variable_reconstructor.py:
  python tools/variable_reconstructor.py \
    --input data/original_vars.json \
    --output results/reconstructed.json

  重构类型:
    - 分类变量合并
    - 连续变量离散化
    - 跨数据集变量对齐
    - 新指标构建
```

### Phase 4: 趋势分析

```
使用 trend_analyzer.py:
  python tools/trend_analyzer.py \
    --input data/time_series.json \
    --output results/trend.json

  分析: 线性/非线性趋势 / 断点检测 / 周期性分析
```

### Phase 5: 综合分析与报告

```
综合以上分析:
  1. 数据质量报告（明确标注局限性）
  2. 变量重构说明（定义变更/处理方法）
  3. 测量等价性评估（跨群体/跨时间）
  4. 结论的推断范围（代表性限制）
  5. 伦理情况说明（二次使用合规性）
```

---

## 质量标准

**分析规范性：**
- ✅ 有数据质量评估报告
- ✅ 有变量重构说明
- ✅ 有测量等价性讨论
- ✅ 有推断范围标注

**方法论合规：**
- ✅ 基于Kiecolt & Nathan (1985)二手分析框架
- ✅ 体现Stewart & Kamins (1993)数据质量评估
- ✅ 有Riley (2018)大型调查数据处理
- ✅ 有Smith (2008)比较研究视角

**解释规范性：**
- ✅ 不混淆相关与因果
- ✅ 报告效应量和不确定性
- ✅ 承认多重解释可能
- ✅ 明确标注数据局限性

---

*Secondary Analysis Expert v2.0.0 — SocienceAI*
*理论基础: Kiecolt & Nathan 1985 · Stewart & Kamins 1993 · Riley 2018 · Smith 2008*