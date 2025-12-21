# 智能体缺失功能完整规范需求文档

## 📋 **文档信息**

- **项目ID**: SCI-SUBAGENT-MISSING-001
- **规范版本**: 1.0.0
- **创建日期**: 2025-12-16
- **状态**: 设计完成，待实施
- **基于**: Claude智能体和技能设计原则深度分析

---

## 🎯 **设计原则理解**

### Claude智能体设计核心理念

#### 1. **分工明确原则**
- **智能体**: 承担专业知识和方法论指导，负责高级认知决策
- **技能**: 承担具体可执行的复杂逻辑固化，负责定量分析
- **工具化思维**: 程序处理数据计算，AI负责解释和决策

#### 2. **渐进式信息披露**
- **第1层**: 核心目标和关键概念（最高优先级）
- **第2层**: 处理流程和核心能力
- **第3层**: 具体工具脚本和代码实现
- **第4层**: 上下文适配和边界条件

#### 3. **最小认知负荷**
- 结构化输出，避免信息过载
- 用户控制信息获取节奏
- 渐进式展示结果
- 按需详细信息

#### 4. **技能调用规则机制**
- **关键词触发**: 基于用户输入自动识别
- **数据类型触发**: 根据数据格式选择技能
- **研究阶段触发**: 基于学术流程顺序执行
- **协同规则**: 多技能协作的优先级和顺序

---

## 🚨 **关键功能缺口分析**

### 1. **ANT专家功能缺口评估**

#### 当前状态
```
智能体: ant-expert.md ✅ (定义完整)
专业能力: 行动者识别、转译过程分析、网络构建追踪、权力关系分析
技能支持: ❌ 完全缺失 (0/4)
应用领域: 科技政策、医疗健康、环境治理、数字化转型
```

#### 核心缺失技能需求
1. **行动者识别技能** - Actor Identification Skill
2. **转译过程分析技能** - Translation Process Analysis Skill
3. **网络构建追踪技能** - Network Construction Tracking Skill
4. **权力关系分析技能** - Power Relationship Analysis Skill

#### 功能影响评估
```
影响范围: 8个学科领域
用户需求: 高 (ANT理论在中国研究应用广泛)
实施紧迫性: 🔥 极高 (理论无法实际应用)
```

### 2. **场域分析专家功能缺口评估**

#### 当前状态
```
智能体: field-analysis-expert.md ✅ (定义完整)
专业能力: 场域识别界定、资本类型分析、习性模式识别、场域动力学分析
技能支持: ❌ 完全缺失 (0/4)
应用领域: 教育社会学、文化社会学、政治社会学、经济社会学
```

#### 核心缺失技能需求
1. **场域识别界定技能** - Field Identification Skill
2. **资本类型分析技能** - Capital Analysis Skill
3. **习性模式识别技能** - Habitus Pattern Recognition Skill
4. **场域动力学分析技能** - Field Dynamics Analysis Skill

#### 功能影响评估
```
影响范围: 8个学科领域
用户需求: 高 (布迪厄理论在中文学术界重要)
实施紧迫性: 🔥 极高 (本土化研究关键工具)
```

### 3. **中文本土化专家功能缺口评估**

#### 当前状态
```
智能体: chinese-localization-expert.md ✅ (定义完整)
专业能力: 中文语境适配、文化背景分析、概念本土化
技能支持: ❌ 几乎完全缺失 (1/10)
应用领域: 所有中文学科研究领域
```

#### 核心缺失技能需求
1. **中文语境适配技能** - Chinese Context Adaptation Skill
2. **文化背景分析技能** - Cultural Background Analysis Skill
3. **概念本土化技能** - Concept Localization Skill
4. **跨文化比较技能** - Cross-Cultural Comparison Skill
5. **本土案例库构建技能** - Local Case Library Construction Skill

---

## 💡 **创新功能扩展分析**

### 1. **新兴学科专家需求**

#### 数字人文专家 (Digital Humanities Expert)
```
专业背景: 数字技术 + 人文学科交叉
核心能力:
- 数字文本挖掘和分析
- 文化数据可视化
- 数字人文方法论
- 跨媒体文化研究

技能需求:
- digital-text-mining-skill.md
- cultural-visualization-skill.md
- dh-methodology-skill.md
- multimedia-analysis-skill.md
```

#### 环境社会学专家 (Environmental Sociology Expert)
```
专业背景: 环境科学 + 社会学交叉
核心能力:
- 环境问题社会分析
- 可持续发展研究
- 环境政策评估
- 生态社会关系

技能需求:
- environmental-social-analysis-skill.md
- sustainability-assessment-skill.md
- eco-policy-evaluation-skill.md
- ecological-relations-skill.md
```

#### 医疗社会学专家 (Medical Sociology Expert)
```
专业背景: 医学 + 社会学交叉
核心能力:
- 医疗社会关系分析
- 健康不平等研究
- 医患关系分析
- 医疗制度评估

技能需求:
- medical-relations-analysis-skill.md
- health-inequality-skill.md
- doctor-patient-relations-skill.md
- healthcare-system-skill.md
```

### 2. **方法论创新扩展**

#### 混合方法研究专家 (Mixed Methods Expert)
```
专业能力:
- 定量定性方法整合
- 三角验证设计
- 混合数据分析
- 方法创新设计

技能需求:
- mixed-methods-design-skill.md
- triangulation-validation-skill.md
- integrated-analysis-skill.md
- method-innovation-skill.md
```

#### 大数据社会科学专家 (Big Data Social Science Expert)
```
专业能力:
- 社交媒体数据挖掘
- 大规模行为分析
- 计算社会科学
- 数据驱动社会研究

技能需求:
- social-media-mining-skill.md
- large-scale-behavior-skill.md
- computational-social-science-skill.md
- data-driven-research-skill.md
```

---

## 🛠️ **完整技能规范设计**

### A. **ANT理论技能包**

#### A1. 行动者识别技能规范
```markdown
---
name: actor-identification-skill
description: 行动者网络理论行动者识别技能，包括人类与非人类行动者的系统识别、分类和关系界定。当需要分析科技政策、医疗健康、环境治理等领域的行动者网络时使用此技能。
---

# 行动者识别技能

## 🎯 核心目标（最高优先级）
在给定的研究情境中系统性地识别所有相关的行动者，建立完整的行动者清单和分类体系。

## 📋 必须掌握的核心概念

### 1. 行动者的定义和类型
**最重要概念**：行动者是能够改变其他行动者状态的任何实体，包括人类和非人类。

### 2. 行动者分类框架
**必须分类**：
- **人类行动者**: 个体、群体、组织
- **非人类行动器**: 技术、制度、概念、自然元素
- **混合行动者**: 人机组合、技术社会系统

### 3. 中文语境特殊性
**必须考虑**：
- **制度性主体**: 政府机构、事业单位
- **集体性主体**: 企业、社会组织
- **文化性元素**: 传统、观念、价值观

## 🔧 核心能力要求

### 1. 行动者识别方法
```python
# 核心识别算法
def identify_actors(context_data: Dict) -> Dict:
    """
    行动者识别主算法

    输入: 研究情境数据
    输出: 行动者清单和分类
    """
    actors = []

    # 1. 文本分析识别
    text_actors = extract_actors_from_text(context_data['texts'])

    # 2. 网络关系识别
    network_actors = extract_actors_from_networks(context_data['networks'])

    # 3. 制度环境识别
    institutional_actors = extract_institutional_actors(context_data['context'])

    # 4. 去重和分类
    actors = deduplicate_and_classify(text_actors, network_actors, institutional_actors)

    return actors
```

### 2. 行动者关系界定
```python
def define_actor_relationships(actors: List[Dict]) -> List[Dict]:
    """
    界定行动者间关系

    输入: 行动者列表
    输出: 关系网络定义
    """
    relationships = []

    for actor1 in actors:
        for actor2 in actors:
            if actor1 != actor2:
                relationship = analyze_relationship(actor1, actor2)
                if relationship:
                    relationships.append(relationship)

    return relationships
```

## 📊 输出格式标准

### 行动者清单输出
```json
{
  "total_actors": 15,
  "human_actors": 8,
  "nonhuman_actors": 7,
  "actor_categories": {
    "individual": 5,
    "organization": 3,
    "technology": 4,
    "institution": 3
  },
  "actor_list": [
    {
      "id": "ACTOR001",
      "name": "政府环保部门",
      "type": "institutional_human",
      "role": "policy_maker",
      "influence_level": "high"
    }
  ]
}
```

## ⚠️ 使用限制

### 能力边界
- ✅ 基于文本和结构化数据的行动者识别
- ✅ 中文语境下的行动者分类
- ✅ 多层次行动者关系界定
- ❌ 未明确提及的隐性行动者
- ❌ 跨文化行动者比较

### 伦理约束
- 不涉及隐私信息的个人行动者识别
- 尊重组织机密信息的边界
- 遵循学术伦理规范
```

#### A2. 转译过程分析技能规范
```markdown
---
name: translation-process-analysis-skill
description: ANT转译过程分析技能，包括问题化、兴趣化、招募、动员四个转译环节的系统分析。当需要追踪技术政策、医疗改革、环境治理等领域的政策形成过程时使用此技能。
---

# 转译过程分析技能

## 🎯 核心目标（最高优先级）
分析行动者网络中转译过程的四个关键环节，揭示政策、技术、观念如何被塑造和传播。

## 📋 必须掌握的转译概念

### 1. 转译四环节模型
**核心模型**：
- **问题化(Problematization)**: 定义问题和解决方案
- **兴趣化(Interessement)**: 建立利益联盟
- **招募(Enrollment)**: 争取行动者参与
- **动员(Mobilization)**: 确保网络稳定性

### 2. 转译链分析
**分析要点**：
- 转译路径追踪
- 关键转译节点识别
- 转译失败原因分析
- 转译效果评估

## 🔧 转译分析方法

### 转译过程追踪算法
```python
def track_translation_process(case_data: Dict) -> Dict:
    """
    转译过程追踪主算法

    输入: 案例数据
    输出: 转译过程分析结果
    """
    translation_process = {
        'problematization': analyze_problematization(case_data),
        'interessement': analyze_interessement(case_data),
        'enrollment': analyze_enrollment(case_data),
        'mobilization': analyze_mobilization(case_data)
    }

    return translation_process

def analyze_problematization(case_data: Dict) -> Dict:
    """分析问题化环节"""
    # 识别问题定义过程
    problems = extract_problems(case_data)
    solutions = extract_solutions(case_data)

    return {
        'problems_identified': problems,
        'solutions_proposed': solutions,
        'problem_solution_mapping': map_problems_solutions(problems, solutions)
    }
```

### 转译效果评估
```python
def evaluate_translation_effectiveness(translation_data: Dict) -> Dict:
    """
    转译效果评估

    输入: 转译过程数据
    输出: 效果评估结果
    """
    evaluation = {
        'network_stability': assess_network_stability(translation_data),
        'goal_achievement': assess_goal_achievement(translation_data),
        'actor_satisfaction': assess_actor_satisfaction(translation_data)
    }

    return evaluation
```
```

### B. **场域分析技能包**

#### B1. 场域识别界定技能规范
```markdown
---
name: field-identification-skill
description: 布迪厄场域理论场域识别界定技能，包括场域边界确定、场域类型识别、场域特征分析和场域关系界定。当需要分析教育场域、文化场域、政治场域等中国本土场域时使用此技能。
---

# 场域识别界定技能

## 🎯 核心目标（最高优先级）
在复杂的社会现象中准确识别和界定分析对象所属的场域，为后续的资本分析和习性分析奠定基础。

## 📋 必须掌握的场域理论

### 1. 场域的基本定义
**核心概念**：场域是一个具有相对自主性的社会空间，其中的行动者争夺特定形式的资本。

### 2. 场域的基本特征
**必须识别**：
- **相对自主性**: 相对于其他场域的独立性
- **斗争性**: 场域内争夺资本的竞争关系
- **历史性**: 场域形成的历史轨迹
- **结构性**: 相对稳定的权力关系结构

### 3. 中文场域特殊性
**必须考虑**：
- **制度性场域**: 政府、事业单位、国有企业
- **传统文化场域**: 教育、学术、艺术
- **新兴场域**: 互联网、金融、科技创新

## 🔧 场域识别方法

### 场域边界确定算法
```python
def identify_field_boundaries(context_data: Dict) -> Dict:
    """
    场域边界确定主算法

    输入: 研究情境数据
    输出: 场域边界定义
    """
    boundaries = {
        'internal_boundaries': identify_internal_structure(context_data),
        'external_boundaries': identify_external_relations(context_data),
        'temporal_boundaries': identify_temporal_scope(context_data)
    }

    return boundaries

def identify_field_type(field_data: Dict) -> str:
    """
    场域类型识别

    输入: 场域数据
    输出: 场域类型
    """
    field_types = {
        'educational': check_educational_field(field_data),
        'cultural': check_cultural_field(field_data),
        'political': check_political_field(field_data),
        'economic': check_economic_field(field_data),
        'scientific': check_scientific_field(field_data)
    }

    # 返回最匹配的场域类型
    return max(field_types, key=field_types.get)
```

### 场域关系分析
```python
def analyze_field_relationships(fields: List[Dict]) -> Dict:
    """
    场域关系分析

    输入: 多个场域数据
    输出: 场域关系网络
    """
    relationships = []

    for field1 in fields:
        for field2 in fields:
            if field1 != field2:
                relationship = analyze_field_relation(field1, field2)
                if relationship:
                    relationships.append(relationship)

    return {
        'field_count': len(fields),
        'relationship_count': len(relationships),
        'relationship_network': relationships
    }
```

## 📊 场域识别输出标准

### 场域清单格式
```json
{
  "identified_fields": [
    {
      "field_name": "高等教育场域",
      "field_type": "educational",
      "autonomy_level": "medium",
      "dominant_capital": "cultural",
      "key_institutions": ["大学", "教育部"],
      "power_structure": {
        "dominant_positions": ["教授", "院长"],
        "marginal_positions": ["助教", "学生"]
      }
    }
  ],
  "field_relationships": [
    {
      "field1": "高等教育场域",
      "field2": "政治场域",
      "relationship_type": "dependency",
      "power_asymmetry": "political_dominant"
    }
  ]
}
```
```

### C. **中文本土化技能包**

#### C1. 中文语境适配技能规范
```markdown
---
name: chinese-context-adaptation-skill
description: 中文语境适配技能，包括中国文化背景分析、语境语义理解、表达习惯适配和概念本土化。当需要将西方理论和方法应用到中国本土研究时使用此技能。
---

# 中文语境适配技能

## 🎯 核心目标（最高优先级）
确保所有社会科学分析理论和方法在中国语境下的正确应用，避免文化误读和概念错配。

## 📋 必须掌握的中文文化要素

### 1. 中国文化核心特征
**必须理解**：
- **集体主义导向**: 个人与集体的关系
- **关系网络**: 人际关系的重要性
- **权力距离**: 等级制度的接受度
- **长期导向**: 历史传统的影响

### 2. 社会制度特征
**必须考虑**：
- **政府主导**: 政府在社会治理中的核心作用
- **单位制度**: 工作单位的社会组织功能
- **家庭结构**: 家庭在社会关系中的地位
- **城乡差异**: 城乡发展的不平衡性

### 3. 语言表达特征
**必须适配**：
- **含蓄表达**: 间接沟通和暗示
- **面子文化**: 社会面子的重要性
- **人情关系**: 义务和回报的平衡
- **等级称谓**: 社会地位的体现

## 🔧 语境适配方法

### 文化背景分析算法
```python
def adapt_chinese_context(theory_application: Dict) -> Dict:
    """
    中文语境适配主算法

    输入: 理论应用方案
    输出: 语境适配结果
    """
    adaptation = {
        'cultural_analysis': analyze_cultural_background(theory_application),
        'institutional_analysis': analyze_institutional_context(theory_application),
        'linguistic_analysis': analyze_linguistic_context(theory_application),
        'adaptation_recommendations': generate_recommendations(theory_application)
    }

    return adaptation

def analyze_cultural_background(application: Dict) -> Dict:
    """
    文化背景分析

    输入: 理论应用数据
    输出: 文化背景分析
    """
    cultural_factors = {
        'collectivism_level': assess_collectivism(application),
        'power_distance': assess_power_distance(application),
        'uncertainty_avoidance': assess_uncertainty_avoidance(application),
        'long_term_orientation': assess_long_term_orientation(application)
    }

    return cultural_factors
```

### 概念本土化转换
```python
def localize_concepts(western_concepts: List[str]) -> Dict:
    """
    西方概念本土化转换

    输入: 西方概念列表
    输出: 本土化结果
    """
    localization_results = {}

    for concept in western_concepts:
        chinese_equivalent = find_chinese_equivalent(concept)
        adaptation_needed = assess_adaptation_need(concept, chinese_equivalent)

        localization_results[concept] = {
            'chinese_equivalent': chinese_equivalent,
            'adaptation_needed': adaptation_needed,
            'localization_strategy': develop_localization_strategy(concept, chinese_equivalent)
        }

    return localization_results
```
```

---

## 📈 **实施优先级和资源需求**

### 实施时间表

#### 第1期：核心技能补充 (4周)
```
Week 1-2: ANT技能包 (4个技能)
- actor-identification-skill.md
- translation-process-analysis-skill.md
- network-construction-tracking-skill.md
- power-relationship-analysis-skill.md

Week 3-4: 场域分析技能包 (4个技能)
- field-identification-skill.md
- capital-analysis-skill.md
- habitus-analysis-skill.md
- field-dynamics-skill.md
```

#### 第2期：本土化技能 (3周)
```
Week 5-7: 中文本土化技能包 (5个技能)
- chinese-context-adaptation-skill.md
- cultural-background-analysis-skill.md
- concept-localization-skill.md
- cross-cultural-comparison-skill.md
- local-case-construction-skill.md
```

#### 第3期：创新扩展 (6周)
```
Week 8-10: 新兴学科专家 (3个专家，12个技能)
Week 11-13: 方法论创新 (2个专家，8个技能)
```

### 资源需求评估

#### 人力资源需求
```
核心开发团队 (6人):
- 理论专家 (2人): ANT、场域理论、布迪厄理论
- 技能开发工程师 (2人): 技能实现、代码开发
- 中文学者 (1人): 本土化适配、文化背景
- 项目经理 (1人): 进度协调、质量控制

支持团队 (4人):
- 领域专家 (2人): 新兴学科领域
- 方法论专家 (1人): 混合方法、大数据
- 质量保证工程师 (1人): 技能测试、验证
```

#### 技术资源需求
```
开发环境:
- 技能开发框架
- 测试自动化工具
- 文档生成系统
- 版本控制系统

研究资源:
- 理论文献库
- 案例数据库
- 中文化工具包
- 跨文化对比工具
```

### 成功指标

#### 功能完整性指标
```
- 技能覆盖率: 60% → 95%
- 智能体功能完整度: 50% → 90%
- 中文本土化支持: 20% → 80%
- 跨学科覆盖: 5 → 15个领域
```

#### 质量指标
```
- 技能准确性: >90%
- 代码质量评分: >8.5/10
- 文档完整性: 100%
- 用户满意度: >85%
```

#### 使用效果指标
```
- 任务完成率: >90%
- 错误率: <5%
- 响应时间: <3秒
- 学习曲线: <1小时
```

---

## 🎯 **实施建议**

### 立即行动项
1. **组建开发团队** - 招募理论专家和工程师
2. **建立开发规范** - 统一技能开发标准
3. **启动核心技能开发** - 优先ANT和场域分析
4. **建立质量保证体系** - 确保技能质量

### 风险控制
1. **理论准确性** - 理论专家全程参与
2. **文化适应性** - 中文学者深度参与
3. **技术可行性** - 分阶段实施和测试
4. **用户接受度** - 持续收集用户反馈

### 长期发展
1. **持续优化** - 基于用户使用反馈
2. **扩展覆盖** - 增加更多学科领域
3. **智能化升级** - 引入机器学习优化
4. **生态建设** - 构建开放的开发生态

---

**本规范文档基于对Claude智能体设计原则的深度理解，为缺失功能的完整实现提供了清晰的路线图和可执行的具体规范。**