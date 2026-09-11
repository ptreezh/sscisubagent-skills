# 内容分析最佳实践

## 版本信息
- **版本**: 1.0.0
- **方法论标准**: Krippendorff (2018), Neuendorf (2017)
- **创建时间**: 2026-03-15

---

## 一、编码方案开发

### 1.1 类目设计原则

**排他性检验**:
- 每个分析单位能否只归入一个类目？
- 类目定义是否有重叠部分？
- 边界案例如何处理？

**穷尽性检验**:
- 所有可能的内容是否都能归类？
- 是否需要"其他"类目？
- "其他"类目的比例是否合理（<10%）？

**实践建议**:
```
类目设计检查表
├── 定义清晰度
│   ├── 是否有明确定义？
│   ├── 定义是否可操作？
│   └── 定义是否有边界？
├── 操作指标
│   ├── 是否有具体指标？
│   ├── 指标是否可观察？
│   └── 指标是否可计数？
└── 编码示例
    ├── 是否有正例？
    ├── 是否有反例？
    └── 是否涵盖边界情况？
```

### 1.2 编码手册编制

**必备内容**:
1. 研究概述
2. 变量列表和定义
3. 每个变量的编码规则
4. 编码示例（正例和反例）
5. 特殊情况处理指南
6. 编码表/编码表

**编码表示例**:
```
编码表结构
├── 编号: [唯一标识]
├── 基本信息: [来源、日期等]
├── 变量编码区
│   ├── V1: [ ] [选项]
│   ├── V2: [ ] [选项]
│   └── ...
├── 备注区
└── 编码员签名
```

---

## 二、编码员培训

### 2.1 培训流程

**标准培训流程**:
```
第一阶段: 理论导入
├── 内容分析方法论介绍
├── 研究背景和目的说明
└── 理论框架讲解

第二阶段: 方案讲解
├── 编码方案逐条讲解
├── 重点难点分析
└── 问题答疑

第三阶段: 练习编码
├── 共同编码示范样本
├── 独立编码练习样本
└── 讨论分歧和问题

第四阶段: 信度检验
├── 独立编码测试样本
├── 计算信度系数
└── 达标后正式编码
```

### 2.2 培训要点

**讲解要点**:
- 每个类目都要举例
- 边界情况重点讲解
- 编码规则要一致理解

**练习要点**:
- 练习样本要有代表性
- 数量足够（建议20-30个）
- 包含各种情况和边界案例

---

## 三、信度检验

### 3.1 信度检验标准流程

```
Step 1: 样本选择
├── 选择10-15%的样本
├── 或至少50-100个单位
└── 随机或分层抽样

Step 2: 独立编码
├── 编码员独立编码
├── 不讨论、不交流
└── 记录编码时间和困难

Step 3: 计算信度
├── 选择适当系数
├── 计算每个变量信度
└── 计算总体信度

Step 4: 分析分歧
├── 识别分歧热点
├── 分析分歧原因
└── 提出改进方案

Step 5: 达标判断
├── α ≥ 0.80: 继续
├── 0.667 ≤ α < 0.80: 优化
└── α < 0.667: 修订方案
```

### 3.2 信度系数选择

| 情况 | 推荐系数 |
|------|---------|
| 2名编码员，类目变量 | Cohen's κ 或 Krippendorff's α |
| 多名编码员 | Krippendorff's α |
| 存在缺失数据 | Krippendorff's α |
| 连续变量 | Krippendorff's α 或 ICC |

### 3.3 信度提升策略

**分歧原因分析**:
| 原因 | 解决策略 |
|------|---------|
| 定义模糊 | 细化操作定义 |
| 无示例 | 增加编码示例 |
| 边界不清 | 明确边界规则 |
| 培训不足 | 补充培训 |

---

## 四、编码过程管理

### 4.1 编码质量控制

**定期检查**:
- 每1-2周进行一次信度检验
- 抽取5-10%样本复查
- 监控编码速度变化

**问题处理**:
```
发现信度下降 →
├── 分析原因
│   ├── 编码疲劳？
│   ├── 新情况出现？
│   └── 方案理解偏差？
├── 采取措施
│   ├── 休息调整
│   ├── 更新编码手册
│   └── 补充培训
└── 验证效果
    └── 再次信度检验
```

### 4.2 编码记录

**必须记录**:
- 编码日期和时间
- 编码员编号
- 编码决策依据
- 特殊情况说明
- 无法编码的原因

---

## 五、数据分析

### 5.1 描述性分析

**基本统计**:
```python
# 频次和百分比
import pandas as pd

# 类目频次
freq = df['category'].value_counts()
percent = df['category'].value_counts(normalize=True) * 100

# 汇总表
summary = pd.DataFrame({
    '频次': freq,
    '百分比': percent.round(1)
})
```

### 5.2 卡方检验

**适用情况**:
- 类目变量
- 比较组间差异
- 检验变量关联

**注意事项**:
- 期望频次 ≥ 5
- 样本量影响显著性
- 报告效应量（Cramer's V）

```python
from scipy.stats import chi2_contingency

# 列联表
contingency = pd.crosstab(df['group'], df['category'])

# 卡方检验
chi2, p, dof, expected = chi2_contingency(contingency)

# Cramer's V
n = contingency.sum().sum()
min_dim = min(contingency.shape) - 1
cramers_v = np.sqrt(chi2 / (n * min_dim))
```

### 5.3 结果报告

**标准报告格式**:
```
描述性结果:
X类目出现n次（XX%），Y类目出现m次（YY%）。

统计检验:
χ²(df) = XX.XX, p = .XXX, V = .XX

结论:
[基于统计结果的解释]
```

---

## 六、效度检验

### 6.1 内容效度检验

**专家评审法**:
1. 邀请2-3名领域专家
2. 评审编码方案
3. 评估类目与构念的对应关系
4. 提出修改建议

**评审内容**:
- 类目定义是否准确
- 操作指标是否合理
- 类目体系是否完整

### 6.2 构念效度检验

**理论一致性**:
- 类目是否与理论概念对应
- 结果是否符合理论预期

**外部比较**:
- 与已有研究结果比较
- 与其他测量方法比较

---

## 七、常见问题与解决方案

### 7.1 编码分歧

| 问题 | 解决方案 |
|------|---------|
| 定义理解不同 | 明确操作定义，增加示例 |
| 边界案例处理 | 制定明确规则，记录决策 |
| 编码疲劳 | 合理分工，定期休息 |

### 7.2 信度不达标

| 原因 | 解决方案 |
|------|---------|
| 类目定义模糊 | 细化定义和指标 |
| 培训不充分 | 补充培训 |
| 编码方案问题 | 修订方案 |

### 7.3 数据分析问题

| 问题 | 解决方案 |
|------|---------|
| 期望频次过低 | 合并类目或增加样本 |
| 样本量不足 | 增加数据或调整分析 |
| 结果不显著 | 检查效应量和样本量 |

---

## 八、工具使用

### 8.1 coding_scheme.py

```bash
# 创建编码方案
python tools/coding_scheme.py --create --config scheme.yaml --output coding_scheme.json

# 验证编码方案
python tools/coding_scheme.py --validate --scheme coding_scheme.json

# 导出编码手册
python tools/coding_scheme.py --export --scheme coding_scheme.json --format pdf
```

### 8.2 reliability_tester.py

```bash
# 计算信度
python tools/reliability_tester.py \
  --coder1 data/coder1.json \
  --coder2 data/coder2.json \
  --method krippendorff \
  --output reliability_report.json

# 详细分析
python tools/reliability_tester.py \
  --coder1 data/coder1.json \
  --coder2 data/coder2.json \
  --detailed \
  --output detailed_report.json
```

### 8.3 frequency_analyzer.py

```bash
# 基本频次分析
python tools/frequency_analyzer.py --input coded_data.json --output frequency.json

# 分组比较
python tools/frequency_analyzer.py --input coded_data.json --group-by year --output comparison.json

# 统计检验
python tools/frequency_analyzer.py --input coded_data.json --test chi-square --output test_results.json
```

---

## 九、质量检查清单

### 编码前
- [ ] 编码方案完整
- [ ] 类目定义清晰
- [ ] 编码示例充分
- [ ] 编码员培训完成

### 编码中
- [ ] 独立编码
- [ ] 定期信度检验
- [ ] 记录编码决策
- [ ] 问题及时处理

### 编码后
- [ ] 信度达标
- [ ] 效度检验
- [ ] 数据清理
- [ ] 结果核实

---

**维护者**: 内容分析专家技能
**最后更新**: 2026-03-15
