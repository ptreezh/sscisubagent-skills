# Case 005: fsQCA性别平等政策 - 正面案例

**日期**: 2026-04-11
**分析类型**: fsQCA (Fuzzy-Set QCA)
**主题**: 性别平等政策有效实施条件
**案例数**: 18

---

## 分析背景

### 研究问题
什么条件组合导致国家或地区的性别平等政策有效实施（高性别平等指数）？

### 条件（4个）

```yaml
条件G1: 立法保护 (LEGIS)     # 是否有完善的性别平等法律
条件G2: 教育投入 (EDU)        # 女性受教育年限
条件G3: 女性参政 (POLIT)      # 女性议会占比
条件G4: 经济参与 (ECON)       # 女性劳动参与率

结果Y: 性别平等指数 (GEI)
```

### 校准锚点（理论依据）

| 条件 | 0完全不在 | 交叉点 | 完全在 | 理论来源 |
|------|----------|--------|--------|---------|
| LEGIS | 0 | 0.6 | 0.9 | UN Women (2023) 立法评分 |
| EDU | 8年 | 12年 | 16年 | UNESCO 平均受教育年限 |
| POLIT | 5% | 20% | 40% | IPU 性别平等基准 |
| ECON | 30% | 55% | 75% | ILO 女性劳动参与率 |
| GEI | 40 | 65 | 85 | EIGE 性别平等指数 |

---

## Step 1: 校准

使用 `data_calibrator.py` 进行模糊集校准：

```bash
python tools/data_calibrator.py \
  -i data/gender-policy-18countries.csv \
  --method fuzzy \
  --anchors LEGIS:0,0.6,0.9 \
  --anchors EDU:8,12,16 \
  --anchors POLIT:5,20,40 \
  --anchors ECON:30,55,75 \
  --anchors GEI:40,65,85 \
  -o results/gender-calibrated.json
```

---

## Step 2: 必要性分析

**使用 `consistency_analyzer.py`**：

```bash
python tools/consistency_analyzer.py \
  -i results/gender-calibrated.json \
  --outcome GEI \
  --analysis necessity \
  --threshold 0.9
```

**预期结果**：
- EDU接近必要条件（一致性可能≥0.9）
- 挪威/瑞典等高GEI国家可作为完全隶属锚点

---

## Step 3: 真值表构建

```bash
python tools/truth_table_builder.py \
  -i results/gender-calibrated.json \
  --conditions LEGIS,EDU,POLIT,ECON \
  --outcome GEI \
  --threshold 0.8 \
  -o results/gender-truth-table.json
```

**16种条件组合（4条件→2^4=16）**

---

## Step 4: 充分性分析（复杂解）

```bash
python tools/solution_calculator.py \
  -i results/gender-truth-table.json \
  --solution-type complex \
  -o results/gender-solution-complex.json
```

**预期解路径**（基于北欧模式理论）：

```
路径1（北欧模式）:
  LEGIS × EDU × POLIT → GEI
  一致性: 0.95
  覆盖度: 0.45
  解读: 立法+教育+参政三维度协同是高GEI的核心路径

路径2（经济补偿模式）:
  ECON × EDU → GEI
  一致性: 0.88
  覆盖度: 0.30
  解读: 即使立法/参政较低，高教育+高经济参与可部分补偿
```

---

## 稳健性检验

使用 `solution_calculator.py --solution-type parsimonious` 和 `intermediate` 检验解的稳定性。

---

## 与现有正面案例的差异化

| 案例 | 主题 | 条件数 | 理论框架 |
|------|------|--------|---------|
| case-001 | 社会运动 | 5 | 资源动员+政治机会 |
| case-002 | PISA教育 | 4 | Darling-Hammond/Hanushek |
| case-003 | 数字化转型 | 4 | Vial/Bharadwaj |
| case-004 | 民主化 | 3 | Lipset现代化理论 |
| **case-005** | **性别平等** | **4** | **EIGE/UN Women** |

---

## 与GT s011女性职场晋升障碍的关系

GT s011（女性职场晋升障碍）研究微观层面：
- 职业性别隔离
- 玻璃天花板
- 组织文化

QCA case-005研究宏观制度层面：
- 国家立法保护程度
- 教育机会差异
- 政治代表性
- 经济参与结构

**两者构成"微观-宏观"三角验证**：GT揭示机制，QCA验证条件。
