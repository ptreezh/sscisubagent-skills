# Saturation Check Prompt - 饱和度检验

## 任务描述

执行扎根理论的饱和度检验，评估理论是否达到饱和状态，即没有新数据能产生新的理论洞见。

## 饱和度评估维度

### 1. 概念饱和度 (Concept Saturation)
- 新概念出现频率 < 10%
- 已有概念的定义稳定
- 概念的变异范围充分

### 2. 范畴饱和度 (Category Saturation)
- 范畴层级完整
- 范畴属性充分发展
- 范畴维度变化范围充分

### 3. 关系饱和度 (Relationship Saturation)
- 范畴间关系稳定
- 关系模式重复出现
- 没有新的关系类型

### 4. 命题饱和度 (Proposition Saturation)
- 理论命题稳定
- 命题间关系清晰
- 没有新的命题产生

### 5. 整体饱和度 (Overall Saturation)
- 综合以上 4 个维度
- 整体评估理论成熟度

## 评估步骤

### Step 1: 增量数据分析
1. 收集新的数据片段（10-20% 的原始数据量）
2. 对新增数据进行编码
3. 记录新概念、新范畴、新关系

### Step 2: 饱和度计算
对每个维度：
1. 计算新概念出现率
2. 计算范畴完善度
3. 计算关系稳定性
4. 计算命题稳定性

### Step 3: 饱和度判断
- **已饱和 (Saturated)**: 整体饱和度 ≥ 80%
- **需更多数据 (Needs More Data)**: 整体饱和度 < 80%

### Step 4: 生成报告
1. 各维度饱和度分数
2. 饱和度证据
3. 数据收集建议（如未饱和）

## 输出格式

```json
{
  "overall_saturation": 85,
  "status": "saturated",
  "by_dimension": {
    "concept_saturation": {
      "score": 90,
      "evidence": "新增数据仅产生 2 个新概念，概念出现率 5%",
      "status": "saturated"
    },
    "category_saturation": {
      "score": 85,
      "evidence": "范畴层级完整，属性充分发展",
      "status": "saturated"
    },
    "relationship_saturation": {
      "score": 80,
      "evidence": "关系模式稳定，无新关系类型",
      "status": "saturated"
    },
    "proposition_saturation": {
      "score": 85,
      "evidence": "理论命题稳定，无新命题产生",
      "status": "saturated"
    }
  },
  "incremental_analysis": {
    "new_data_size": "1500 字",
    "new_concepts": 2,
    "new_categories": 0,
    "new_relationships": 0,
    "new_propositions": 0
  },
  "recommendations": {
    "status": "complete",
    "message": "理论已达到饱和状态，可以结束数据收集"
  }
}
```

## 饱和度标准

### 已饱和 (≥80%)
- 新概念出现率 < 10%
- 范畴层级完整
- 关系模式稳定
- 理论命题充分

### 需更多数据 (<80%)
- 新概念出现率 ≥ 10%
- 范畴发展不充分
- 关系模式不稳定
- 理论命题不足

## 质量检查

饱和度检验完成后，检查：
- [ ] 使用了增量数据（10-20% 原始数据量）
- [ ] 4 个维度都进行了评估
- [ ] 每个维度都有证据支持
- [ ] 饱和度计算逻辑正确
- [ ] 建议具体可行

## 示例

### 饱和度报告示例
```json
{
  "overall_saturation": 85,
  "status": "saturated",
  "by_dimension": {
    "concept_saturation": {
      "score": 90,
      "evidence": "分析新增 1500 字数据，仅发现 2 个新概念，概念出现率 5%，低于 10% 阈值",
      "status": "saturated"
    },
    "category_saturation": {
      "score": 85,
      "evidence": "所有范畴的属性和维度都已充分发展，新增数据未产生新范畴",
      "status": "saturated"
    },
    "relationship_saturation": {
      "score": 80,
      "evidence": "范畴间关系模式稳定，新增数据确认了现有关系，未发现新关系类型",
      "status": "saturated"
    },
    "proposition_saturation": {
      "score": 85,
      "evidence": "理论命题已充分发展，新增数据支持现有命题，未产生新命题",
      "status": "saturated"
    }
  },
  "recommendations": {
    "status": "complete",
    "message": "理论已达到饱和状态，可以结束数据收集并撰写最终报告"
  }
}
```

## 注意事项

1. **增量数据量**: 应该是原始数据的 10-20%
2. **客观评估**: 基于数据而非主观判断
3. **记录证据**: 每个维度的评估都要有数据支持
4. **承认不足**: 如未饱和，明确指出需要哪类数据
