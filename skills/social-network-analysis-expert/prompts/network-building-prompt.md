# Network Building Prompt Template

## 任务

构建社会网络对象并计算基础指标。

## 输入

- 边列表或邻接矩阵
- 网络类型参数（有向/无向、加权/无权）

## 执行步骤

1. **数据解析**
   - 解析输入数据格式
   - 提取节点列表
   - 提取边列表

2. **数据验证**
   - 检查边格式正确性
   - 检查节点数量（≥3）
   - 检查边数量（≥2）

3. **网络构建**
   - 创建NetworkX图对象
   - 设置有向/无向属性
   - 添加权重（如有）

4. **基础指标计算**
   - 节点数 (num_nodes)
   - 边数 (num_edges)
   - 密度 (density)
   - 连通性 (is_connected)
   - 连通分量数 (num_components)
   - 平均度数 (avg_degree)

## 输出格式

```json
{
  "network_info": {
    "num_nodes": 50,
    "num_edges": 120,
    "directed": false,
    "weighted": false
  },
  "basic_metrics": {
    "density": 0.098,
    "is_connected": true,
    "num_components": 1,
    "avg_degree": 4.8
  },
  "validation": {
    "valid": true,
    "issues": []
  },
  "nodes": ["A", "B", "C", ...],
  "edges": [["A", "B"], ["B", "C"], ...]
}
```

## 质量标准

- 网络必须有≥3个节点
- 网络必须有≥2条边
- 密度值必须在[0,1]范围
- 孤立节点必须记录
