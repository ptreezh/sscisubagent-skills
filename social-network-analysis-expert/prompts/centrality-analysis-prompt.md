# Centrality Analysis Prompt Template

## 任务

计算并解释多种中心性指标。

## 输入

- NetworkX图对象（来自网络构建阶段）
- 分析选项

## 执行步骤

1. **度中心性计算**
   - 公式: C_D(v) = d(v) / (n-1)
   - 归一化到[0,1]范围

2. **介数中心性计算**
   - 公式: C_B(v) = Σ σ_{st}(v) / σ_{st}
   - 归一化到[0,1]范围

3. **接近中心性计算**
   - 公式: C_C(v) = (n-1) / Σ d(v, u)
   - 注意：不连通网络需特殊处理

4. **特征向量中心性计算**
   - 迭代求解
   - 处理不收敛情况

5. **PageRank计算**
   - 设置阻尼系数α=0.85
   - 处理悬挂节点

6. **排名生成**
   - 综合得分计算
   - Top-K节点识别

## 输出格式

```json
{
  "degree_centrality": {"A": 0.45, "B": 0.32, ...},
  "betweenness_centrality": {"A": 0.28, "B": 0.15, ...},
  "closeness_centrality": {"A": 0.52, "B": 0.48, ...},
  "eigenvector_centrality": {"A": 0.38, "B": 0.42, ...},
  "pagerank": {"A": 0.045, "B": 0.038, ...},
  "ranking": [
    {"node": "A", "composite_score": 0.42, "rank": 1},
    {"node": "B", "composite_score": 0.35, "rank": 2},
    ...
  ],
  "validation": {
    "valid": true,
    "issues": []
  }
}
```

## 解释框架

对于Top-5节点，提供：
- 中心性类型
- 数值解释（高/中/低）
- 网络位置描述
- 理论意义

## 质量标准

- 所有中心性值必须在[0,1]范围
- 不连通网络接近中心性需特殊处理
- 特征向量不收敛时需记录
