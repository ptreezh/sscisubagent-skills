---
name: designing-research-methodology
description: 设计中文社会科学研究方法论，包括研究设计、抽样策略、数据收集方案和效度评估。当需要确定研究方法、设计研究方案或解决方法论问题时使用此技能。
---

# 中文社会科学研究方法设计技能

## 🎯 核心目标（最高优先级）
为中文社会科学研究者提供科学、适切、可行的研究方法论设计方案，确保研究的严谨性和实用性。

## 📋 必须首先掌握的方法论原则

### 1. 研究方法选择的黄金标准
**最重要原则**：
- **适切性原则**：方法必须适合研究问题和研究对象
- **可行性原则**：在现有条件下可以实施
- **科学性原则**：符合学术规范和科学要求
- **本土化原则**：考虑中国社会的特殊性

### 2. 中文社科研究方法论特色
**必须考虑**：
- **文化敏感性**：考虑中国文化背景和社会制度
- **实践导向**：理论联系实际，解决中国问题
- **政策相关性**：关注政策制定和实践应用
- **伦理特殊性**：符合中国研究伦理要求

### 3. 质量控制的四大支柱
**必须确保**：
- **内在效度**：因果推断的准确性
- **外在效度**：结果推广的适用性
- **信度**：测量和结果的稳定性
- **伦理合规**：研究伦理的严格遵守

## 🔄 动态知识库加载

### 启动时加载
```
/knowledge-base/main-knowledge.md
/knowledge-base/core-concepts.md
```

### 按需加载
```
用户需要问卷 → /knowledge-base/questionnaire-design.md
用户需要访谈 → /knowledge-base/interview-methods.md
用户需要实验 → /knowledge-base/experimental-design.md
用户需要案例 → /knowledge-base/case-study-methods.md
```

## 🚨 紧急处理协议

### 红色警报（开题报告截止）
**快速设计模式**：
1. 提供标准方法论模板
2. 快速匹配研究问题与方法
3. 生成基础研究设计
4. 承诺48小时内完善

### 黄色警报（导师要求修改）
**标准设计模式**：
1. 深度分析研究问题
2. 系统比较多种方法
3. 详细设计实施方案
4. 全面评估方案可行性

## 🛠️ 核心设计技能

### 1. 研究问题类型识别
**关键技能**：
```python
def identify_research_question_type(question):
    """识别研究问题类型"""
    question_types = {
        'descriptive': {
            'keywords': ['现状', '特征', '状况', '分布', '情况'],
            'methods': ['问卷调查', '描述性统计', '文献分析'],
            'examples': ['大学生就业现状如何？', '农民工生活状况怎样？']
        },
        'explanatory': {
            'keywords': ['原因', '影响', '关系', '机制', '作用'],
            'methods': ['回归分析', '路径分析', '结构方程'],
            'examples': ['什么因素影响学习成绩？', '为什么会产生社会不平等？']
        },
        'exploratory': {
            'keywords': ['探索', '发现', '识别', '揭示', '了解'],
            'methods': ['质性研究', '案例研究', '扎根理论'],
            'examples': ['如何理解新生代农民工的身份认同？', '数字化转型带来哪些变化？']
        },
        'evaluative': {
            'keywords': ['效果', '评估', '评价', '影响', '价值'],
            'methods': ['实验研究', '准实验研究', '前后对比'],
            'examples': ['某政策实施效果如何？', '教育改革是否成功？']
        }
    }
    
    for q_type, details in question_types.items():
        if any(keyword in question for keyword in details['keywords']):
            return {
                'type': q_type,
                'recommended_methods': details['methods'],
                'examples': details['examples']
            }
    
    return {'type': 'mixed', 'recommended_methods': ['混合方法研究']}

def generate_research_design_matrix(question_type):
    """生成研究设计矩阵"""
    design_matrix = {
        'descriptive': {
            'quantitative': ['横断面调查', '描述性统计', '相关分析'],
            'qualitative': ['案例研究', '观察法', '文献分析'],
            'mixed': ['描述性混合设计', '顺序解释设计']
        },
        'explanatory': {
            'quantitative': ['实验研究', '回归分析', '结构方程'],
            'qualitative': ['过程追踪', '比较案例研究', '扎根理论'],
            'mixed': ['三角验证设计', '嵌入式设计']
        },
        'exploratory': {
            'quantitative': ['探索性因子分析', '聚类分析'],
            'qualitative': ['扎根理论', '民族志', '现象学'],
            'mixed': ['探索性顺序设计', '转换设计']
        },
        'evaluative': {
            'quantitative': ['实验设计', '准实验设计', '断点回归'],
            'qualitative': ['过程评估', '案例评估', '参与式评估'],
            'mixed': ['评估混合设计', '实时评估设计']
        }
    }
    
    return design_matrix.get(question_type, {})
```

### 2. 抽样策略设计
**核心技能**：
```python
def design_sampling_strategy(research_type, population_size, constraints):
    """设计抽样策略"""
    strategies = {
        'probability_sampling': {
            'simple_random': '简单随机抽样',
            'systematic': '系统抽样',
            'stratified': '分层抽样',
            'cluster': '整群抽样',
            'multistage': '多阶段抽样'
        },
        'non_probability_sampling': {
            'convenience': '便利抽样',
            'purposive': '立意抽样',
            'snowball': '雪球抽样',
            'quota': '配额抽样',
            'volunteer': '志愿者抽样'
        }
    }
    
    # 根据研究类型推荐抽样方法
    if research_type in ['descriptive', 'explanatory']:
        recommended = 'probability_sampling'
        rationale = "需要确保样本代表性，提高结果推广性"
    else:
        recommended = 'non_probability_sampling'
        rationale = "探索性研究注重深度而非代表性"
    
    # 计算样本量
    sample_size = calculate_sample_size(population_size, confidence_level=0.95, margin_of_error=0.05)
    
    return {
        'recommended_approach': recommended,
        'rationale': rationale,
        'specific_methods': strategies[recommended],
        'sample_size': sample_size,
        'implementation_steps': generate_sampling_steps(recommended)
    }

def calculate_sample_size(population_size, confidence_level=0.95, margin_of_error=0.05):
    """计算样本量"""
    # 标准正态分布的Z值
    z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    z = z_scores.get(confidence_level, 1.96)
    
    # 有限总体校正
    if population_size < 100000:
        n_infinite = (z**2 * 0.25) / (margin_of_error**2)
        sample_size = n_infinite / (1 + (n_infinite - 1) / population_size)
    else:
        sample_size = (z**2 * 0.25) / (margin_of_error**2)
    
    return int(sample_size)
```

### 3. 数据收集方案设计
**关键技能**：
```python
def design_data_collection_plan(methodology, research_context):
    """设计数据收集方案"""
    collection_methods = {
        'survey': {
            'questionnaire_design': '问卷设计',
            'distribution_channels': '发放渠道',
            'quality_control': '质量控制',
            'response_rate': '回应率提升'
        },
        'interview': {
            'interview_protocol': '访谈提纲',
            'interviewer_training': '访谈员培训',
            'recording_methods': '记录方法',
            'transcription': '转录整理'
        },
        'observation': {
            'observation_protocol': '观察方案',
            'observer_training': '观察员培训',
            'field_notes': '田野笔记',
            'reflexive_journal': '反思日记'
        },
        'experiment': {
            'experimental_design': '实验设计',
            'treatment_manipulation': '处理操纵',
            'measurement_tools': '测量工具',
            'control_procedures': '控制程序'
        }
    }
    
    # 根据中国特殊情况调整
    chinese_adaptations = {
        'cultural_sensitivity': '文化敏感性考虑',
        'language_appropriateness': '语言适切性',
        'institutional_coordination': '机构协调',
        'ethical_approval': '伦理审查',
        'informed_consent': '知情同意'
    }
    
    return {
        'primary_method': methodology,
        'collection_procedures': collection_methods.get(methodology, {}),
        'chinese_adaptations': chinese_adaptations,
        'timeline': generate_collection_timeline(methodology),
        'budget': estimate_collection_costs(methodology)
    }
```

### 4. 效度评估设计
**核心技能**：
```python
def design_validity_assessment(research_design):
    """设计效度评估方案"""
    validity_types = {
        'internal_validity': {
            'threats': [
                '历史效应', '成熟效应', '测试效应',
                '工具效应', '统计回归', '选择效应',
                '实验流失', '选择-成熟交互'
            ],
            'strategies': [
                '随机分配', '控制组设计', '前测-后测设计',
                '双盲设计', '协变量控制', '匹配设计'
            ]
        },
        'external_validity': {
            'threats': [
                '样本代表性', '情境特殊性', '历史特殊性',
                '干预效应', '多重干预干扰', '效应衰减'
            ],
            'strategies': [
                '随机抽样', '多情境研究', '重复研究',
                '现场实验', '元分析', '统计概括化'
            ]
        },
        'construct_validity': {
            'threats': [
                '操作化不当', '单方法偏差', '单操作偏差',
                '构念-方法混淆', '水平混淆', '单元混淆'
            ],
            'strategies': [
                '多方法测量', '多操作测量', '三角验证',
                '专家评审', '预测试', '统计验证'
            ]
        }
    }
    
    return {
        'validity_assessment': validity_types,
        'threat_analysis': analyze_specific_threats(research_design),
        'mitigation_strategies': generate_mitigation_plan(research_design),
        'assessment_timeline': create_validation_timeline(research_design)
    }
```

## 📊 质量检查清单

### 方法设计质量
- [ ] 研究问题是否明确
- [ ] 方法选择是否适切
- [ ] 抽样策略是否科学
- [ ] 数据收集是否可行
- [ ] 效度控制是否充分

### 实施可行性
- [ ] 时间安排是否合理
- [ ] 资源需求是否满足
- [ ] 伦理要求是否合规
- [ ] 技术要求是否可达
- [ ] 风险控制是否到位

### 中文本土化
- [ ] 文化敏感性是否考虑
- [ ] 语言适切性是否保证
- [ ] 制度因素是否纳入
- [ ] 实践价值是否体现
- [ ] 政策相关性是否明确

## 💡 快速响应模板

### 紧急方法设计模板
```
1. 快速识别研究问题类型
2. 推荐最适合的研究方法
3. 生成基础研究设计框架
4. 提供抽样策略建议
5. 承诺48小时内完善细节
```

### 方法修改模板
```
1. 分析现有方法论问题
2. 提供多种替代方案
3. 详细比较方案优劣
4. 推荐最优解决方案
5. 生成修改实施计划
```

---

**使用说明**：此技能严格遵循中文社会科学研究方法论规范，提供科学、适切、可行的研究设计方案。