# Structural Holes Analysis Prompt Template

## 任务

分析网络结构洞并识别经纪人节点。

## 理论基础

基于 Burt (1992) 的结构洞理论：
- 结构洞：网络中未被连接的空缺
- 经纪人：占据结构洞位置的节点
- 约束指标：衡量节点被周围网络约束的程度

## 输入

- NetworkX图对象（来自网络构建阶段）

## 执行步骤

1. **约束指标计算 (Constraint)**
   - 公式: C_i = Σ_j (p_ij + Σ_q p_iq * p_qj)²
   - 值范围: [0, 1]
   - 低约束 = 高经纪人潜力

2. **有效规模计算 (Effective Size)**
   - 公式: ES_i = Σ_j (1 - Σ_q p_iq * p_qj)
   - 衡量非冗余连接

3. **效率计算 (Efficiency)**
   - 公式: Eff_i = ES_i / degree_i
   - 有效规模/实际度数

4. **层级性计算 (Hierarchy)**
   - 使用聚类系数近似

5. **经纪人识别**
   - 阈值：低于平均约束的节点
   - 列出经纪人清单

## 输出格式

```json
{
  "constraint": {"A": 0.25, "B": 0.42, "C": 0.38, ...},
  "effective_size": {"A": 4.2, "B": 2.8, "C": 3.5, ...},
  "efficiency": {"A": 0.85, "B": 0.62, "C": 0.70, ...},
  "hierarchy": {"A": 0.15, "B": 0.28, "C": 0.22, ...},
  "structural_holes": ["A", "D", "F"],
  "brokers": [
    {"node": "A", "constraint": 0.25, "effective_size": 4.2, "opportunity": "high"},
    {"node": "D", "constraint": 0.28, "effective_size": 3.8, "opportunity": "high"},
    ...
  ],
  "avg_constraint": 0.35,
  "num_structural_holes": 3,
  "validation": {
    "valid": true,
    "issues": []
  }
}
```

## 解释框架

### 经纪人优势
- 信息优势：获取非冗余信息
- 控制优势：信息流动的把关人
- 谈判优势：连接双方的桥梁

### 约束解释
- 低约束（<平均值）：高经纪人潜力，信息优势大
- 中约束（≈平均值）：一般位置
- 高约束（>平均值）：被约束位置，信息优势小

## 质量标准

- 约束指标必须在[0,1]范围
- 有效规模必须≥0
- 经纪人识别需有阈值依据
