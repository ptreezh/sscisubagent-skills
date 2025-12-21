---
name: ant
description: 执行行动者网络理论分析，包括参与者识别、关系网络构建、转译过程追踪和网络动态分析。当需要分析异质性行动者网络、追踪事实构建过程或分析技术社会互动时使用此技能。
---

# 行动者网络理论技能 (ANT)

基于拉图尔的行动者网络理论，分析异质性行动者网络中的关系构建和事实转译过程。

## 使用时机

当用户提到以下需求时，使用此技能：
- "行动者网络" 或 "ANT分析"
- "参与者识别" 或 "行动者网络构建"
- "转译过程" 或 "事实追踪"
- "异质网络" 或 "技术社会互动"
- "网络动态" 或 "关系演化"
- 需要分析人-物-观念的混合网络

## 核心概念

### 1. 行动者（Actors）
人类、非人类（技术、观念、组织）的平等参与者

### 2. 网络（Network）
行动者之间关系的集合

### 3. 转译（Translation）
将一个行动者的兴趣转化为另一个行动者兴趣的过程

---

## 分析流程

### 第一步：参与者识别
- 识别所有相关行动者
- 分类行动者类型
- 分析行动者特征

### 第二步：关系网络构建
- 构建行动者关系网络
- 分析网络结构
- 识别关键节点

### 第三步：转译过程追踪
- 追踪事实构建
- 分析转译链条
- 识别争议点

---

## 快速开始

```bash
# 参与者识别
python scripts/identify_participants.py \
  --input data.json \
  --output participants.json

# 网络分析
python scripts/analyze_network.py \
  --input participants.json \
  --output network.json

# 转译追踪
python scripts/trace_translation.py \
  --input data.json \
  --output translation.json
```

## 输出格式

统一的三层JSON格式：

```json
{
  "summary": {
    "n_actors": 15,
    "network_density": 0.35,
    "translation_stages": 4
  },
  "details": {
    "actors": [...],
    "network": {...},
    "translation": {...}
  }
}
```

---

*此技能基于行动者网络理论，为异质性行动者网络分析提供工具支持。*