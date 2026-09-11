---
name: factor-analysis-expert
description: |
  Factor Analysis expert. Provides dimensionality reduction, factor extraction, rotation methods, reliability testing, and construct validation. Suitable for psychometric research, scale development, and multivariate analysis.
license: MIT
compatibility: "Python 3.8+ | Claude/Qwen/iFlow/Gemini/Copilot/Stigmergy/OpenCode/KiloCode/QoderCLI/WorkBuddy/MiniMax Agent"
metadata:
  version: "5.0.0-cli-native+agent"
  agentskills-io: "true"
  cross-platform: "true"
  darwin-evolution: "frontmatter-fixed"
  darwin-evolution-date: "2026-05-03"
---

---|-----|-----|
| 目的 | 探索因子结构 | 验证预设模型 |
| 因子数量 | 数据驱动 | 理论驱动 |
| 因子载荷 | 自由估计 | 约束估计 |
| 模型拟合 | 无 | 有拟合指标 |
| 应用阶段 | 量表开发早期 | 量表验证阶段 |

## 分析流程

```
步骤1: 数据准备
├── 样本量检查 (N ≥ 5k, 推荐 N ≥ 10k)
├── 缺失值处理
└── 异常值检测
    ↓
步骤2: 适用性检验
├── KMO检验 (≥ 0.60)
├── Bartlett球形检验 (p < .05)
└── 相关矩阵检验
    ↓
步骤3: 因子数确定
├── 特征值 > 1 (Kaiser准则)
├── 碎石图
├── 平行分析
└── 理论考量
    ↓
步骤4: 因子提取
├── 主成分分析 (PCA)
├── 主轴因子法 (PAF)
├── 最大似然法 (ML)
└── alpha因子分析
    ↓
步骤5: 因子旋转
├── 正交旋转 (Varimax, Quartimax)
├── 斜交旋转 (Promax, Oblimin)
└── 旋转选择依据
    ↓
步骤6: 结果解释
├── 因子载荷解释
├── 共同度检验
├── 因子命名
└── 内部一致性检验
    ↓
步骤7: 报告撰写
```

## 因子提取方法

| 方法 | 适用场景 | 特点 |
|------|---------|------|
| PCA | 数据降维 | 提取总方差 |
| PAF | 共同因素分析 | 提取共同方差 |
| ML | 正态分布数据 | 可做统计检验 |
| Alpha | 信度优化 | 最大化alpha系数 |
| Image | 小样本 | 减少偏差 |

## 因子旋转策略

### 正交旋转
- **Varimax**: 简化载荷，最常用
- **Quartimax**: 简化因子
- **Equamax**: 折中方案

### 斜交旋转
- **Promax**: 快速斜交
- **Oblimin**: 灵活斜交
- **Geomin**: 适合复杂结构

### 选择依据
```
因子间相关理论预期?
├── 是 → 斜交旋转
└── 否 → 正交旋转
    
研究目的?
├── 数据简化 → PCA + Varimax
├── 构念开发 → PAF + Oblimin
└── 理论验证 → CFA
```

## 拟合指标(CFA)

| 指标 | 可接受 | 良好 | 说明 |
|------|--------|------|------|
| χ²/df | < 5 | < 3 | 受样本量影响大 |
| CFI | ≥ 0.90 | ≥ 0.95 | 比较拟合指数 |
| TLI | ≥ 0.90 | ≥ 0.95 | Tucker-Lewis指数 |
| RMSEA | ≤ 0.08 | ≤ 0.06 | 近似误差均方根 |
| SRMR | ≤ 0.10 | ≤ 0.08 | 标准化残差均方根 |

## 信效度评估

### 信度
| 指标 | 公式 | 可接受值 |
|------|------|---------|
| Cronbach's α | α = kr/(1+(k-1)r̄) | ≥ 0.70 |
| 组合信度(CR) | CR = (Σλ)²/[(Σλ)²+Σ(1-λ²)] | ≥ 0.70 |
| AVE | AVE = Σλ²/k | ≥ 0.50 |

### 效度
- **内容效度**: 专家评审
- **收敛效度**: AVE ≥ 0.50, 载荷 ≥ 0.50
- **区分效度**: √AVE > 因子间相关

## 使用示例

```
用户: 分析这个问卷的因子结构

AI: 我将进行探索性因子分析：

## 适用性检验
- KMO = 0.85 (良好)
- Bartlett χ² = 1234.56, p < .001 (适合)

## 因子数确定
- 特征值 > 1: 3个因子
- 平行分析: 建议3个因子
- 碎石图: 转折点在第4个因子

## 因子提取与旋转
采用主轴因子法 + Oblimin斜交旋转

## 结果
因子1 (解释方差32%): 项目1, 2, 3 → 命名为"工作满意度"
因子2 (解释方差24%): 项目4, 5, 6 → 命名为"组织承诺"  
因子3 (解释方差18%): 项目7, 8 → 命名为"离职倾向"

## 信度检验
α₁ = 0.87, α₂ = 0.82, α₃ = 0.79 (均可接受)
```

## 🚫 绝对禁止原则

> **使用前必读**：以下原则是不可逾越的红线，违反将导致因子分析结论失效。

1. **禁止适用性不足仍强行分析** — KMO < 0.60 或 Bartlett检验不显著(p > .05)时继续进行因子分析，导致因子结构不可靠
2. **禁止预设不合理的因子数** — 盲目使用Kaiser准则（特征值>1）而不结合碎石图和平行分析，导致过度或不足提取
3. **禁止忽视因子载荷解释标准** — 将载荷<0.40的条目纳入因子，或不报告共同度而直接解释因子
4. **禁止混淆EFA与CFA** — 将探索性因子分析的结果直接当作验证性结论，忽略两种方法的本质区别
5. **禁止忽视旋转选择的理论依据** — 因子间理论上相关却使用正交旋转（Varimax），或反之
6. **禁止跳过信效度完整评估** — 仅报告因子载荷，不检验Cronbach's α、组合信度(CR)、收敛效度(AVE)、区分效度

## ✅ 质量标准

### 完整性
- 必做项清单完成度 ≥ 90%
- 适用性检验报告完整（KMO、Bartlett）
- 因子提取与旋转有据可查

### 方法论
- 理论框架与数据一致性 ≥ 90%
- 因子数确定有多种方法交叉验证
- 分析步骤可复现性高

### 深度
- 核心维度覆盖 ≥ 80%
- 信效度完整评估（α、CR、AVE、√AVE）
- 结果解释有理论支撑

## 🖥️ Python 工具

### 工具链

| # | 工具名称 | 功能描述 |
|---|----------|----------|
| 1 | efa_analyzer.py | 探索性因子分析，支持主成分分析、主轴因子法、KMO检验、Bartlett检验、平行分析 |
| 2 | rotation_selector.py | 旋转策略选择，支持Varimax/Promax/Oblimin正交与斜交旋转 |
| 3 | cfa_validator.py | 验证性因子分析，支持拟合指标计算（χ²/df、CFI、TLI、RMSEA、SRMR） |
| 4 | reliability_calculator.py | 信效度计算，支持Cronbach's α、组合信度(CR)、AVE、区分效度检验 |

### CLI用法

```bash
python tools/efa_analyzer.py --input data.csv --method paf --rotation oblimin --output factors.json
python tools/cfa_validator.py --input model.json --data data.csv --output fit_indices.json
python tools/reliability_calculator.py --input coded_data.csv --output reliability.json
```

## 参考文献

1. Tabachnick, B.G., & Fidell, L.S. (2019). *Using Multivariate Statistics*. 7th ed.
2. Hair, J.F., et al. (2019). *Multivariate Data Analysis*. 8th ed.
3. Brown, T.A. (2015). *Confirmatory Factor Analysis for Applied Research*. 2nd ed.
4. Fabrigar, L.R., et al. (1999). Evaluating the use of EFA. *Psychological Methods*, 4, 272-299.

---

**技能版本**: 5.0.0  
**方法论标准**: Tabachnick & Fidell (2019)  
**创建时间**: 2026-03-15