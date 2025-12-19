---
name: field-analysis
description: 执行布迪厄场域分析，包括场域边界识别、资本分布分析、自主性评估和习性模式分析。当需要分析社会场域的结构、权力关系和文化资本时使用此技能。
---

# 场域分析技能 (Field Analysis)

基于布迪厄场域理论，分析社会空间的权力结构和文化资本分布。

## 使用时机

当用户提到以下需求时，使用此技能：
- "场域分析" 或 "布迪厄场域"
- "权力结构分析" 或 "社会空间分析"
- "文化资本" 或 "社会资本"
- "自主性评估" 或 "场域自主性"
- "习性分析" 或 "惯习模式"
- 需要分析特定社会领域的结构和关系

## 快速开始

### 工具链

```bash
# 场域边界识别
python scripts/identify_field_boundary.py \
  --input data.json \
  --output boundary.json

# 资本分布分析
python scripts/analyze_capital_distribution.py \
  --input data.json \
  --type cultural \
  --output capital.json

# 自主性评估
python scripts/assess_autonomy.py \
  --input data.json \
  --output autonomy.json

# 习性模式分析
python scripts/analyze_habitus.py \
  --input data.json \
  --output habitus.json
```

## 核心概念

### 1. 场域（Field）
社会空间中的竞争领域，有自身的规则和权力结构

### 2. 资本类型
- **文化资本**：知识、技能、文化素养
- **社会资本**：关系网络、社会联系
- **象征资本**：声望、荣誉、认可
- **经济资本**：物质财富、经济资源

### 3. 习性（Habitus）
持久的、可转移的性情倾向系统

---

## 分析流程

### 第一步：场域边界识别

**使用工具识别**：
- 确定场域范围和边界
- 识别核心参与者
- 分析场域的自主程度

详见：`references/field-theory/INDEX.md`

---

### 第二步：资本分布分析

**四种资本类型分析**：
- 计算各类资本的分布
- 识别资本不平等
- 分析资本转换关系

详见：`references/capital-theory/INDEX.md`

---

### 第三步：自主性评估

**评估指标**：
- 场域相对于外部力量的独立性
- 内部规则的自主程度
- 权力结构的稳定性

详见：`references/autonomy/INDEX.md`

---

### 第四步：习性模式分析

**分析维度**：
- 识别行为模式和偏好
- 分析社会化过程
- 理解实践逻辑

详见：`references/habitus/INDEX.md`

## 输出格式

统一的三层JSON格式：

```json
{
  "summary": {
    "field_name": "学术场域",
    "autonomy_score": 0.75,
    "capital_distribution": {...},
    "habitus_patterns": 3
  },
  "details": {
    "boundary_analysis": {...},
    "capital_analysis": {...},
    "autonomy_analysis": {...},
    "habitus_analysis": {...}
  }
}
```

## 质量检查清单

- [ ] 场域边界清晰定义
- [ ] 资本类型准确识别
- [ ] 自主性评估合理
- [ ] 习性模式分析深入
- [ ] 考虑中国本土化特点

## 深入学习

- **场域理论**：`references/field-theory/INDEX.md`
- **资本理论**：`references/capital-theory/INDEX.md`
- **中国应用**：`references/chinese-context/INDEX.md`

---

*此技能基于布迪厄场域理论，为中国社会场域分析提供工具支持。*