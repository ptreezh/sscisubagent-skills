# Community Detection Prompt Template

## 任务

执行社群检测并分析社群结构。

## 输入

- NetworkX图对象（来自网络构建阶段）
- 检测参数（分辨率等）

## 执行步骤

1. **Louvain算法执行**
   - 设置分辨率参数（默认1.0）
   - 执行社群划分
   - 获取分区结果

2. **模块化计算**
   - 公式: Q = Σ [e_ii - a_i²]
   - 记录Q值
   - 评估社群结构质量

3. **社群统计**
   - 社群数量
   - 各社群大小
   - 各社群内部密度
   - 平均社群规模

4. **社群结构分析**
   - 最大社群识别
   - 最小社群识别
   - 社群重叠检查（如有）

## 输出格式

```json
{
  "communities": {
    "0": ["A", "B", "C"],
    "1": ["D", "E", "F", "G"],
    "2": ["H", "I"]
  },
  "partition": {
    "A": 0, "B": 0, "C": 0,
    "D": 1, "E": 1, "F": 1, "G": 1,
    "H": 2, "I": 2
  },
  "modularity": 0.42,
  "stats": {
    "num_communities": 3,
    "avg_size": 3.0,
    "max_size": 4,
    "min_size": 2
  },
  "quality_assessment": {
    "modularity_quality": "good",
    "structure_strength": "moderate"
  },
  "validation": {
    "valid": true,
    "issues": []
  }
}
```

## 质量标准

- 模块化Q值>0.3才算有明显社群结构
- Q值>0.5为强社群结构
- Q值<0.3需警告用户社群结构不明显
- 单节点社群需记录
