# Validation Prompt - 验证提示词

## 任务描述

对扎根理论分析的完整结果进行质量验证，确保分析符合方法论标准，输出可靠、有效。

## 验证维度

### 1. 编码质量验证
- 编码定义清晰度
- 编码与数据的联系
- 编码命名规范性
- 编码备忘录质量

### 2. 范畴质量验证
- 范畴层级清晰度
- 范畴属性完整性
- 范畴维度发展度
- 范畴间区分度

### 3. 范式模型验证
- 6 要素完整性
- 因果关系合理性
- 数据支持充分性
- 逻辑一致性

### 4. 理论质量验证
- 核心范畴整合力
- 故事线连贯性
- 命题可验证性
- 理论贡献度

### 5. 饱和度验证
- 饱和度分数可靠性
- 增量分析充分性
- 数据收集建议合理性

## 验证步骤

### Step 1: 编码质量检查
对开放性编码结果：
1. 随机抽取 20% 的编码
2. 检查每个编码的定义是否清晰
3. 检查是否有至少 2 个数据示例
4. 检查命名是否行动导向
5. 检查备忘录质量

### Step 2: 信度验证
1. 检查 Cohen's Kappa 计算是否正确
2. 检查 Kappa 是否 > 0.7
3. 如低于阈值，检查原因

### Step 3: 范畴体系验证
1. 检查范畴层级是否清晰
2. 检查属性和维度是否完整
3. 检查范畴间是否有重叠
4. 检查是否有数据支持

### Step 4: 范式模型验证
1. 检查 6 要素是否完整
2. 检查因果关系是否合理
3. 检查是否有数据支持
4. 检查逻辑是否一致

### Step 5: 理论质量验证
1. 评估核心范畴整合力
2. 评估故事线连贯性
3. 评估命题可验证性
4. 评估理论贡献度

### Step 6: 饱和度验证
1. 检查饱和度计算方法
2. 检查增量数据量是否充分
3. 检查饱和度分数是否可靠
4. 检查建议是否合理

## 输出格式

```json
{
  "validation_result": {
    "overall_status": "pass|conditional_pass|fail",
    "overall_score": 85,
    "by_dimension": {
      "coding_quality": {
        "score": 90,
        "status": "pass",
        "comments": "编码质量良好，定义清晰，数据支持充分"
      },
      "category_quality": {
        "score": 85,
        "status": "pass",
        "comments": "范畴体系清晰，层级分明"
      },
      "paradigm_model": {
        "score": 80,
        "status": "pass",
        "comments": "范式模型完整，6 要素齐全"
      },
      "theory_quality": {
        "score": 85,
        "status": "pass",
        "comments": "理论框架连贯，命题可验证"
      },
      "saturation": {
        "score": 85,
        "status": "pass",
        "comments": "饱和度评估可靠，增量分析充分"
      }
    }
  },
  "issues": [
    {
      "dimension": "coding_quality",
      "severity": "low|medium|high",
      "description": "问题描述",
      "recommendation": "改进建议"
    }
  ],
  "recommendations": [
    "建议 1",
    "建议 2"
  ],
  "final_decision": {
    "status": "approved|revisions_needed|major_revisions",
    "message": "最终决定说明"
  }
}
```

## 验证标准

### 通过 (Pass)
- 总体分数 ≥ 80%
- 所有维度分数 ≥ 75%
- 无高严重度问题

### 有条件通过 (Conditional Pass)
- 总体分数 ≥ 70%
- 1-2 个维度分数 < 75%
- 仅有中低严重度问题

### 不通过 (Fail)
- 总体分数 < 70%
- 或有高严重度问题
- 或有 3 个以上维度 < 75%

## 质量检查清单

### 开放性编码检查
- [ ] 每个编码都有明确定义
- [ ] 每个编码至少有 2 个数据示例
- [ ] 编码命名是行动导向的
- [ ] Cohen's Kappa > 0.7
- [ ] 至少有 5 个编码备忘录

### 轴心编码检查
- [ ] 范畴体系层级清晰（至少 2 层）
- [ ] 每个范畴都有属性和维度
- [ ] 因果关系有数据支持
- [ ] 范式模型 6 要素完整
- [ ] 关系网络逻辑一致

### 选择式编码检查
- [ ] 核心范畴整合力强（≥8/10）
- [ ] 故事线连贯
- [ ] 理论命题可验证
- [ ] 命题有数据支持

### 饱和度检查
- [ ] 整体饱和度 > 80%
- [ ] 使用了增量数据（10-20%）
- [ ] 各维度饱和度记录完整
- [ ] 增量分析显示无新洞见

## 示例

### 验证结果示例
```json
{
  "validation_result": {
    "overall_status": "pass",
    "overall_score": 85,
    "by_dimension": {
      "coding_quality": {
        "score": 90,
        "status": "pass",
        "comments": "编码质量优秀，定义清晰，数据支持充分，Kappa = 0.78"
      },
      "category_quality": {
        "score": 85,
        "status": "pass",
        "comments": "范畴体系清晰，层级分明，属性和维度发展充分"
      },
      "paradigm_model": {
        "score": 80,
        "status": "pass",
        "comments": "范式模型完整，6 要素齐全，因果关系合理"
      },
      "theory_quality": {
        "score": 85,
        "status": "pass",
        "comments": "理论框架连贯，核心范畴整合力强，命题可验证"
      },
      "saturation": {
        "score": 85,
        "status": "pass",
        "comments": "饱和度评估可靠，整体饱和度 85%，增量分析充分"
      }
    }
  },
  "issues": [],
  "recommendations": [
    "建议补充一些负面案例分析",
    "建议增加研究者反身性讨论"
  ],
  "final_decision": {
    "status": "approved",
    "message": "分析质量良好，符合扎根理论方法论标准，可以发表"
  }
}
```

## 注意事项

1. **客观评估**: 基于方法论标准而非主观偏好
2. **建设性反馈**: 提供具体的改进建议
3. **承认局限**: 说明验证的局限性
4. **记录过程**: 记录验证过程和决策依据
