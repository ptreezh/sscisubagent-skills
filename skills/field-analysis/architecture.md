# 布迪厄场域分析技能SOLID架构设计

## SOLID原则应用

### S - 单一职责原则 (SRP)
每个类只负责一个明确的理论功能：
- `FieldBoundaryAnalyzer` - 只负责场域边界分析
- `AutonomyAssessor` - 只负责场域自主性评估
- `CapitalMapper` - 只负责资本分布分析
- `ConversionAnalyzer` - 只负责资本转换分析
- `HabitusAnalyzer` - 只负责习性模式分析
- `ResultFormatter` - 只负责结果格式化

### O - 开闭原则 (OCP)
通过接口和抽象类支持扩展：
- `IFieldAnalyzer` - 场域分析器接口
- `ICapitalAnalyzer` - 资本分析器接口
- `ITheoryApplication` - 理论应用接口
- `ILocalizationAdapter` - 本土化适配接口

### L - 里氏替换原则 (LSP)
所有实现都可以替换其接口，保证理论一致性

### I - 接口隔离原则 (ISP)
小而专一的接口，避免大接口：
- `IBoundaryAnalyzer` - 边界分析专用接口
- `IAutonomyCalculator` - 自主性计算专用接口
- `ICapitalTypeRecognizer` - 资本类型识别专用接口

### D - 依赖倒置原则 (DIP)
依赖抽象理论概念而非具体实现

## 目录结构
```
field-analysis-skills/
├── shared/
│   ├── interfaces/
│   │   ├── IFieldAnalyzer.js
│   │   ├── ICapitalAnalyzer.js
│   │   ├── ITheoryApplication.js
│   │   └── ILocalizationAdapter.js
│   ├── types/
│   │   ├── FieldTypes.js
│   │   ├── CapitalTypes.js
│   │   └── TheoryTypes.js
│   ├── constants/
│   │   ├── FieldConstants.js
│   │   └── ChineseConstants.js
│   └── utils/
│       ├── TextProcessor.js
│       ├── TheoryValidator.js
│       └── LocalizationHelper.js
├── field-structure-skill/
│   ├── __tests__/
│   │   ├── FieldBoundaryAnalyzer.test.js
│   │   ├── AutonomyAssessor.test.js
│   │   └── FieldStructureSkill.test.js
│   ├── src/
│   │   ├── FieldBoundaryAnalyzer.js
│   │   ├── AutonomyAssessor.js
│   │   ├── PowerStructureMapper.js
│   │   ├── RulesOfGameExtractor.js
│   │   └── ChineseFieldAdapter.js
│   └── index.js
├── capital-dynamics-skill/
│   ├── __tests__/
│   │   ├── CapitalMapper.test.js
│   │   ├── ConversionAnalyzer.test.js
│   │   ├── HabitusAnalyzer.test.js
│   │   └── CapitalDynamicsSkill.test.js
│   ├── src/
│   │   ├── CapitalMapper.js
│   │   ├── ConversionAnalyzer.js
│   │   ├── HabitusAnalyzer.js
│   │   ├── CompetitionAnalyzer.js
│   │   ├── ReproductionMechanism.js
│   │   └── ChineseCapitalAdapter.js
│   └── index.js
└── package.json
```

## 理论一致性保证

### 布迪厄理论概念映射
```javascript
// 理论概念的严格定义
const BOURDIEU_CONCEPTS = {
  FIELD: {
    definition: "一个具有相对自主性的社会空间",
    core_attributes: ["autonomy", "boundary", "rules", "positions"],
    theoretical_premise: "场域中的行动者争夺特定形式的资本"
  },

  CAPITAL: {
    types: ["cultural", "social", "economic", "symbolic"],
    properties: ["convertible", "unequally_distributed", "power_source"],
    theoretical_premise: "资本是权力的基础，可以转换形式"
  },

  HABITUS: {
    definition: "持久的、可转移的倾向系统",
    characteristics: ["structured", "structuring", "practice_generator"],
    theoretical_premise: "习性连接客观结构和主观实践"
  },

  AUTONOMY: {
    definition: "场域相对于外部力量的独立性",
    dimensions: ["economic", "political", "cultural"],
    theoretical_premise: "自主性决定场域的独特逻辑"
  }
};
```

### 中文本土化适配
```javascript
// 中国特色的布迪厄理论应用
const CHINESE_ADAPTATIONS = {
  FIELD_SPECIFICS: {
    danwei_system: "单位制的场域特征",
    guanxi_field: "关系场域的特殊逻辑",
    hierarchical_structure: "等级制的权力结构",
    state_influence: "国家在场域中的作用"
  },

  CAPITAL_EXTENSIONS: {
    political_capital: "政治资本（中国特色）",
    guanxi_capital: "关系资本（本土概念）",
    institutional_capital: "制度资本（单位制）",
    regional_capital: "地域资本（地方关系）"
  },

  HABITUS_PATTERNS: {
    collectivist_orientation: "集体主义倾向",
    authority_respect: "权威尊重模式",
    network_orientation: "关系网络导向",
    bureaucratic_logic: "官僚制思维模式"
  }
};
```