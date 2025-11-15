---
name: writing-grounded-theory-memos
description: 撰写扎根理论备忘录，包括过程记录、反思分析、理论备忘录和编码备忘录。当需要记录编码过程、深化理论思考、保存研究发现或进行理论反思时使用此技能。
---

# 扎根理论备忘录写作技能

## 🎯 核心目标（最高优先级）
为扎根理论研究提供系统化的备忘录写作支持，确保研究过程的透明性、可追溯性和理论深度。

## 📋 必须首先掌握的备忘录原则

### 1. 备忘录的核心作用
**最重要原则**：
- **过程记录**：记录每个编码决策的思考过程
- **反思分析**：对编码结果进行深度反思
- **理论发展**：记录理论概念的演化过程
- **质量控制**：确保研究的严谨性和可信度

### 2. 备忘录类型分类
**必须区分**：
- **过程备忘录**：记录编码过程中的具体操作和思考
- **理论备忘录**：记录理论概念的发展和关系
- **操作备忘录**：记录具体的技术操作和方法选择
- **反思备忘录**：对研究过程和结果的深度反思

### 3. 质量控制的黄金标准
**必须确保**：
- **及时性**：编码后立即记录，避免遗忘
- **具体性**：详细记录具体内容和思考过程
- **反思性**：包含深度分析和批判性思考
- **连贯性**：保持备忘录之间的逻辑连贯

## 🔄 动态知识库加载

### 启动时加载
```
/knowledge-base/main-knowledge.md
/knowledge-base/core-concepts.md
/knowledge-base/grounded-theory-fundamentals.md
```

### 按需加载
```
用户需要过程记录 → /knowledge-base/memo-templates.md
用户需要理论发展 → /knowledge-base/theory-memos.md
用户需要反思分析 → /knowledge-base/reflection-memos.md
```

## 🚨 紧急处理协议

### 红色警报（编码截止）
**快速记录模式**：
1. 提供核心备忘录模板
2. 快速记录关键概念
3. 生成简要分析框架
4. 承诺24小时内补充详细内容

### 黄色警报（导师要求）
**标准记录模式**：
1. 详细记录编码过程
2. 深度分析编码结果
3. 系统整理理论发展
4. 提供完整备忘录

## 🛠️ 核心写作技能

### 1. 过程备忘录写作
**核心技能**：
```python
def write_process_memo(coding_session):
    """撰写过程备忘录"""
    memo_structure = {
        'session_info': {
            'date': coding_session['date'],
            'duration': coding_session['duration'],
            'data_source': coding_session['data_source'],
            'coding_type': coding_session['coding_type']
        },
        'coding_decisions': {
            'concepts_identified': coding_session['concepts'],
            'coding_rationale': coding_session['rationale'],
            'changes_made': coding_session['changes'],
            'questions_raised': coding_session['questions']
        },
        'preliminary_analysis': {
            'initial_patterns': coding_session['patterns'],
            'emerging_categories': coding_session['categories'],
            'theoretical_insights': coding_session['insights']
        },
        'next_steps': {
            'immediate_actions': coding_session['next_actions'],
            'further_questions': coding_session['further_questions'],
            'data_needs': coding_session['data_needs']
        }
    }
    
    return memo_structure

# 中文备忘录模板
chinese_memo_templates = {
    'coding_decision': [
        "编码决策：{concept}",
        "编码理由：{reason}",
        "原始数据：{data}",
        "思考过程：{thinking}"
    ],
    'pattern_observation': [
        "观察到的模式：{pattern}",
        "出现频率：{frequency}",
        "相关概念：{related_concepts}",
        "理论意义：{significance}"
    ]
}
```

### 2. 理论备忘录写作
**核心技能**：
```python
def write_theory_memo(theory_development):
    """撰写理论备忘录"""
    memo_structure = {
        'theory_status': {
            'current_stage': theory_development['stage'],
            'core_concepts': theory_development['concepts'],
            'relationships': theory_development['relationships']
        },
        'theoretical_insights': {
            'new_insights': theory_development['insights'],
            'concept_evolution': theory_development['evolution'],
            'theoretical_gaps': theory_development['gaps']
        },
        'empirical_support': {
            'supporting_data': theory_development['data'],
            'case_examples': theory_development['examples'],
            'contradictory_evidence': theory_development['contradictions']
        },
        'future_directions': {
            'refinement_needs': theory_development['refinements'],
            'further_questions': theory_development['questions'],
            'research_implications': theory_development['implications']
        }
    }
    
    return memo_structure

def generate_theoretical_insights(concepts, relationships):
    """生成理论洞察"""
    insights = []
    
    # 概念关系分析
    for concept in concepts:
        related_concepts = [r for r in relationships if r['source'] == concept or r['target'] == concept]
        if related_concepts:
            insight = f"概念'{concept}'与{len(related_concepts)}个其他概念相关，"
            insight += f"可能形成'{concept}'为中心的理论节点"
            insights.append(insight)
    
    # 关系模式识别
    relationship_types = [r['type'] for r in relationships]
    if relationship_types:
        most_common = max(set(relationship_types), key=relationship_types.count)
        insight = f"最常见的关系类型是'{most_common}'，"
        insight += f"这可能反映了研究中的核心动态"
        insights.append(insight)
    
    return insights
```

### 3. 反思备忘录写作
**核心技能**：
```python
def write_reflection_memo(reflection_point):
    """撰写反思备忘录"""
    memo_structure = {
        'reflection_context': {
            'reflection_trigger': reflection_point['trigger'],
            'current_progress': reflection_point['progress'],
            'challenges_encountered': reflection_point['challenges']
        },
        'critical_reflection': {
            'what_worked': reflection_point['successes'],
            'what_didnt_work': reflection_point['failures'],
            'reasoning': reflection_point['reasoning'],
            'lessons_learned': reflection_point['lessons']
        },
        'methodological_reflection': {
            'method_effectiveness': reflection_point['method_effectiveness'],
            'limitations': reflection_point['limitations'],
            'adaptations_needed': reflection_point['adaptations']
        },
        'theoretical_reflection': {
            'theoretical_adequacy': reflection_point['theory_adequacy'],
            'conceptual_clarity': reflection_point['conceptual_clarity'],
            'theoretical_contributions': reflection_point['contributions']
        }
    }
    
    return memo_structure

def generate_reflection_questions(coding_stage):
    """生成反思问题"""
    questions = {
        'open_coding': [
            "我是否保持了开放的心态？",
            "我是否避免了先入为主的观念？",
            "我是否充分让数据说话？"
        ],
        'axial_coding': [
            "我构建的范畴是否有足够的属性和维度？",
            "范畴之间的关系是否有充分的数据支持？",
            "我的编码是否过于复杂或过于简单？"
        ],
        'selective_coding': [
            "我选择的核心范畴是否真的核心？",
            "我的故事线是否能够解释所有重要现象？",
            "我的理论是否具有足够的解释力？"
        ]
    }
    
    return questions.get(coding_stage, [])
```

## 📊 质量检查清单

### 备忘录完整性
- [ ] 是否包含基本会话信息
- [ ] 是否记录了编码决策过程
- [ ] 是否包含初步分析结果
- [ ] 是否规划了下一步行动

### 理论深度
- [ ] 是否有深度理论思考
- [ ] 是否识别了理论洞察
- [ ] 是否连接了实证数据
- [ ] 是否提出了理论问题

### 反思质量
- [ ] 是否进行了批判性反思
- [ ] 是否识别了成功和失败
- [ ] 是否总结了经验教训
- [ ] 是否提出了改进方向

## 💡 快速响应模板

### 紧急备忘录模板
```
1. 提供核心备忘录框架
2. 快速记录关键信息
3. 生成初步分析要点
4. 提供反思问题清单
5. 承诺24小时内完善内容
```

### 标准备忘录模板
```
1. 详细记录编码过程
2. 深度分析编码结果
3. 系统整理理论发展
4. 全面进行反思分析
5. 规划下一步研究
```

## 🔧 备忘录管理工具

### 备忘录组织结构
```
memos/
├── process-memos/          # 过程备忘录
│   ├── 2025-11-15-session1.md
│   ├── 2025-11-15-session2.md
│   └── ...
├── theory-memos/           # 理论备忘录
│   ├── concept-development.md
│   ├── relationship-analysis.md
│   └── ...
├── reflection-memos/        # 反思备忘录
│   ├── weekly-reflection.md
│   ├── milestone-reflection.md
│   └── ...
└── operational-memos/      # 操作备忘录
    ├── method-choices.md
    ├── tool-usage.md
    └── ...
```

### 备忘录命名规范
- **过程备忘录**：YYYY-MM-DD-session-N.md
- **理论备忘录**：concept-name-development.md
- **反思备忘录**：YYYY-MM-DD-reflection.md
- **操作备忘录**：tool-name-usage.md

---

**使用说明**：此技能严格遵循扎根理论备忘录写作规范，确保研究过程的透明性和理论发展的可追溯性。