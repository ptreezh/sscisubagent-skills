# 布迪厄场域分析技能平衡版Speckit规范文档

## 📋 文档信息
- **版本**: 1.5 (理论实用平衡版)
- **创建日期**: 2025-12-16
- **设计原则**: 理论完整性 + 实用性 + 渐进式披露
- **理论基础**: 完整的布迪厄场域理论框架
- **目标**: 保持理论价值的同时确保可用性

---

## 🎯 技能概览

### 平衡设计（2个核心技能）
1. **field-structure-skill** - 场域结构分析技能（保持理论完整性）
2. **capital-dynamics-skill** - 资本动态分析技能（核心理论价值）

### 平衡策略
- ✅ **保留理论精髓** - 不损害布迪厄理论的核心概念
- ✅ **分层信息披露** - 满足不同深度需求
- ✅ **本土化适配** - 深度适配中文语境
- ✅ **渐进式学习** - 从实用到理论的平滑过渡

---

## 📦 技能1: field-structure-skill

### 基本信息
```yaml
name: field-structure-skill
description: 场域结构分析技能，识别社会场域的结构特征、自主性程度和权力关系。保持布迪厄理论完整性。
version: 1.5.0
category: social-field-analysis
tags: [bourdieu, field-theory, 场域结构, 自主性, 权力关系]
```

### 理论核心（保持完整性）

#### 1. 场域特征识别算法
```javascript
// 完整的场域分析算法
class FieldStructureAnalyzer {
  analyzeFieldStructure(contextData) {
    return {
      field_boundary: this.identifyBoundary(contextData),
      field_autonomy: this.assessAutonomy(contextData),
      power_structure: this.mapPowerRelations(contextData),
      position_distribution: this.analyzePositions(contextData),
      rules_of_game: this.extractRules(contextData)
    };
  }
}
```

#### 2. 自主性评估（核心理论）
```javascript
// 场域自主性评估 - 布迪厄理论核心
assessFieldAutonomy(fieldData, externalInfluences) {
  const autonomyIndicators = {
    economic_independence: this.assessEconomicIndependence(fieldData),
    political_autonomy: this.assessPoliticalAutonomy(fieldData),
    cultural_specificity: this.assessCulturalSpecificity(fieldData),
    internal_legitimacy: this.assessInternalLegitimacy(fieldData)
  };

  return this.calculateAutonomyScore(autonomyIndicators);
}
```

### 3层信息披露（平衡设计）

#### 第1层：实用洞察（10秒理解）
```markdown
## 场域结构实用洞察

**场域是什么？**: 一个相对独立的社会竞技场
**核心特征**:
- 自主性程度：这个场域有多大独立性？
- 权力结构：谁是真正的权力掌握者？
- 竞争规则：想要成功需要什么条件？

**关键判断**:
- 这个场域受外界控制多吗？
- 内部权力是如何分配的？
- 进入这个场域需要什么资格？
```

#### 第2层：理论理解（30秒阅读）
```json
{
  "field_characteristics": {
    "field_type": "学术场域",
    "autonomy_level": "中等",
    "dominant_logic": "学术资本竞争",
    "external_pressures": ["市场化", "行政化"],
    "internal_legitimacy": "同行评议"
  },
  "structure_analysis": {
    "hierarchy_type": "等级制",
    "competition_intensity": "高",
    "mobility_barriers": ["学历", "成果", "人脉"],
    "power_distribution": "集中与分散并存"
  }
}
```

#### 第3层：深度理论（按需展开）
```json
{
  "theoretical_framework": {
    "field_boundary": {
      "internal_boundaries": ["学科壁垒", "机构界限"],
      "external_boundaries": ["政府影响", "市场压力"],
      "boundary_permeability": "中等",
      "boundary_mechanisms": ["准入制度", "评价标准"]
    },
    "autonomy_analysis": {
      "economic_autonomy": 0.6,
      "political_autonomy": 0.4,
      "cultural_autonomy": 0.8,
      "overall_autonomy": 0.6,
      "autonomy_trends": "下降"
    },
    "position_structure": [
      {
        "position": "教授",
        "capital_requirements": {
          "cultural_capital": 0.9,
          "social_capital": 0.6,
          "economic_capital": 0.5,
          "symbolic_capital": 0.8
        },
        "habitus_expectations": ["学术独立", "同行认可"],
        "power_abilities": ["知识生产", "学术评价", "资源分配"]
      }
    ]
  }
}
```

---

## 📦 技能2: capital-dynamics-skill

### 基本信息
```yaml
name: capital-dynamics-skill
description: 资本动态分析技能，分析不同资本类型的分布、转换机制和争夺策略。体现布迪厄资本理论的核心价值。
version: 1.5.0
category: capital-analysis
tags: [bourdieu, capital-theory, 资本转换, 资本争夺, 社会再生产]
```

### 理论核心（保持完整性）

#### 1. 四种资本类型识别
```javascript
// 完整的资本分析算法
class CapitalDynamicsAnalyzer {
  analyzeCapitalDynamics(fieldData, actors) {
    return {
      capital_distribution: this.mapCapitalDistribution(actors),
      conversion_rates: this.calculateConversionRates(actors),
      competition_dynamics: this.analyzeCompetition(actors),
      reproduction_mechanisms: this.identifyReproduction(actors)
    };
  }
}
```

#### 2. 资本转换机制（理论核心）
```javascript
// 资本转换分析 - 布迪厄理论的重要发现
analyzeCapitalConversion(actor, fieldContext) {
  const conversionMatrix = {
    cultural_to_economic: this.assessCulturalToEconomic(actor),
    social_to_cultural: this.assessSocialToCultural(actor),
    economic_to_symbolic: this.assessEconomicToSymbolic(actor),
    symbolic_to_all: this.assessSymbolicConversion(actor)
  };

  return this.identifyConversionStrategies(conversionMatrix);
}
```

#### 3. 习性模式识别
```javascript
// 习性分析 - 行为模式的理论解释
analyzeHabitus(actor, fieldPosition) {
  return {
    dispositions: this.identifyDispositions(actor),
    practices: this.identifyPractices(actor),
    expectations: this.identifyExpectations(actor, fieldPosition),
    trajectory: this.predictTrajectory(actor, fieldPosition)
  };
}
```

### 输出格式

#### 资本动态分析报告
```json
{
  "capital_overview": {
    "field_capital_distribution": {
      "cultural_capital": "35%",
      "social_capital": "25%",
      "economic_capital": "20%",
      "symbolic_capital": "20%"
    },
    "capital_inequality": {
      "gini_coefficient": 0.45,
      "concentration_level": "中等偏高"
    },
    "conversion_efficiency": {
      "most_efficient": "cultural→symbolic",
      "least_efficient": "economic→cultural"
    }
  },
  "actor_capital_profiles": [
    {
      "actor_name": "张教授",
      "capital_portfolio": {
        "cultural": 90,
        "social": 70,
        "economic": 60,
        "symbolic": 85
      },
      "conversion_capabilities": {
        "cultural_to_symbolic": 0.8,
        "social_to_cultural": 0.6,
        "economic_to_social": 0.4
      },
      "habitus_patterns": {
        "dispositions": ["学术追求", "同行认可"],
        "practice_styles": ["理论导向", "谨慎创新"],
        "expectations": ["学术声望", "自主研究"]
      }
    }
  ],
  "dynamics_analysis": {
    "competition_forms": ["学术竞争", "资源竞争", "声望竞争"],
    "reproduction_mechanisms": ["学历传承", "师徒关系", "精英网络"],
    "change_tendencies": ["市场化加剧", "自主性下降", "竞争激烈化"]
  }
}
```

---

## 🧪 TDD测试用例（理论完整性验证）

### 核心理论测试
```gherkin
Feature: 场域自主性分析

  Scenario: 评估学术场域自主性
    Given 大学内部的学术管理制度
    When 分析场域自主性
    Then 应评估经济自主性
    And 应评估政治自主性
    And 应评估文化自主性
    And 应给出综合自主性评分

  Scenario: 识别资本转换机制
    Given 教授的学术成就和社会关系信息
    When 分析资本转换
    Then 应识别文化资本向象征资本的转换
    And 应计算转换效率
    And 应分析转换策略

Feature: 习性模式识别

  Scenario: 分析行为模式
    Given 个体的职业发展轨迹
    When 识别习性模式
    Then 应识别其倾向和偏好
    And 应分析其实践方式
    And 应预测其行为轨迹
```

### 本土化测试
```gherkin
Feature: 中文本土化适配

  Scenario: 识别中国特色资本形式
    Given 中国组织中的权力关系信息
    When 分析资本类型
    Then 应识别政治资本
    And 应识别关系资本
    And 应识别制度资本

  Scenario: 分析中国场域特征
    Given 中国大学或企业文本
    When 分析场域结构
    Then 应识别单位制特征
    And 应分析关系网络作用
    And 应评估行政级别影响
```

---

## 🎯 使用场景分层

### 场景1: 实用快速分析（第1层）
```yaml
user_need: "快速了解这个组织的权力结构"
output: "权力中心、关键人物、基本规则"
time_required: "1-2分钟"
theoretical_depth: "表面实用"
```

### 场景2: 学术研究分析（第2层）
```yaml
user_need: "深入研究组织的社会机制"
output: "场域特征、资本分布、竞争动态"
time_required: "10-15分钟"
theoretical_depth: "理论应用"
```

### 场景3: 深度理论分析（第3层）
```yaml
user_need: "基于布迪厄理论的深度研究"
output: "完整的理论分析框架"
time_required: "30分钟以上"
theoretical_depth: "理论创新"
```

---

## 📊 平衡质量标准

### 理论完整性
```yaml
theoretical_completeness:
  field_concept: "100%保留"
  capital_types: "100%保留"
  autonomy_analysis: "100%保留"
  habitus_concept: "100%保留"
  conversion_mechanism: "100%保留"

theoretical_fidelity:
  bourdieu_core: "严格遵循"
  concept_accuracy: "高"
  relationship_logic: "完整"
  explanatory_power: "强"
```

### 实用性保证
```yaml
practical_usability:
  learning_curve: "渐进式（0-30分钟）"
  immediate_value: "第1层即可使用"
  depth_flexibility: "按需深入"
  chinese_adaptation: "深度本土化"
```

---

## ✅ 平衡方案优势

### 理论价值保持
- ✅ **完整框架** - 保留布迪厄理论的所有核心概念
- ✅ **逻辑完整** - 概念间关系逻辑不变
- ✅ **解释力强** - 保持理论的社会解释能力
- ✅ **学术价值** - 支持严肃的学术研究

### 实用性提升
- ✅ **分层使用** - 不同用户选择不同深度
- ✅ **渐进学习** - 从实用到理论的学习路径
- ✅ **本土适配** - 深度中文语境适配
- ✅ **可视化** - 复杂理论的直观呈现

### 开发可行
- ✅ **模块化设计** - 核心功能可分阶段实现
- ✅ **测试完整** - 理论完整性可通过测试验证
- ✅ **扩展友好** - 支持功能持续完善
- ✅ **维护简单** - 清晰的理论架构便于维护

---

## 🎯 最终建议

这个平衡版本在**保持布迪厄理论完整性的同时**，通过**分层信息披露**和**渐进式学习**解决了可用性问题。相比极简版本：

1. **理论价值不损失** - 完整保留布迪厄理论的核心贡献
2. **可用性不受损** - 第1层即可满足基本需求
3. **学术价值提升** - 支持深度理论分析和研究
4. **长期价值更大** - 理论的深度为后续扩展留出空间

**建议采用这个平衡版本**，它既避免了极简设计对理论的损害，又保持了足够的实用性。