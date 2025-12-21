---
name: assessing-research-validity
description: 评估研究信度效度，包括内在效度、外在效度、构念效度、统计结论效度和内容效度分析。当需要评估研究质量、检验研究设计、解决效度问题或应对审稿人质疑时使用此技能。
---

# 研究信度效度评估技能

## 🎯 核心目标（最高优先级）
为中文社会科学研究提供科学、系统的信度效度评估支持，确保研究结果的可靠性、准确性和推广性。

## 📋 必须首先掌握的效度概念

### 1. 效度的四大类型
**最重要概念**：
- **内在效度**：因果推断的准确性（内部真实性）
- **外在效度**：结果推广的适用性（外部真实性）
- **构念效度**：测量的准确性（构念真实性）
- **统计结论效度**：统计推断的可靠性（统计真实性）

### 2. 中文社科研究效度特殊性
**必须考虑**：
- **文化敏感性**：中国文化背景对测量的影响
- **制度因素**：社会制度对研究结果的制约
- **语言适切性**：中文表达和理解的准确性
- **实践相关性**：理论与中国实践的结合度

### 3. 效度威胁识别原则
**必须识别**：
- **选择威胁**：样本选择偏差
- **历史威胁**：时间序列变化影响
- **成熟威胁**：研究对象自身变化
- **测试威胁**：测量工具的影响
- **工具威胁**：测量工具的局限性

## 🔄 动态知识库加载

### 启动时加载
```
/knowledge-base/main-knowledge.md
/knowledge-base/core-concepts.md
/knowledge-base/validity-fundamentals.md
```

### 按需加载
```
用户需要内在效度 → /knowledge-base/internal-validity.md
用户需要外在效度 → /knowledge-base/external-validity.md
用户需要构念效度 → /knowledge-base/construct-validity.md
用户需要统计效度 → /knowledge-base/statistical-validity.md
```

## 🚨 紧急处理协议

### 红色警报（论文审稿）
**快速评估模式**：
1. 提供效度检查清单
2. 快速识别主要威胁
3. 生成改进建议
4. 承诺48小时内完成详细评估

### 黄色警报（导师要求）
**标准评估模式**：
1. 系统性四维度效度评估
2. 详细分析威胁因素
3. 设计效度增强方案
4. 提供实施指导

## 🛠️ 核心评估技能

### 1. 内在效度评估
**核心技能**：
```python
def assess_internal_validity(research_design):
    """评估内在效度"""
    validity_threats = {
        'selection': {
            'threat_level': assess_selection_threat(research_design),
            'mitigation_strategies': [
                '随机分配',
                '匹配设计',
                '前测-后测设计',
                '协变量控制'
            ],
            'indicators': [
                '随机化程度',
                '组间等价性',
                '控制变量数量'
            ]
        },
        'history': {
            'threat_level': assess_history_threat(research_design),
            'mitigation_strategies': [
                '时间序列设计',
                '间断时间序列设计',
                '多重时间序列设计',
                '控制组设计'
            ],
            'indicators': [
                '时间间隔合理性',
                '历史数据完整性',
                '外部事件记录'
            ]
        },
        'maturation': {
            'threat_level': assess_maturation_threat(research_design),
            'mitigation_strategies': [
                '缩短研究周期',
                '控制成熟影响',
                '成熟度测量',
                '统计控制'
            ],
            'indicators': [
                '研究对象稳定性',
                '成熟度变化规律',
                '成熟度测量工具'
            ]
        },
        'testing': {
            'threat_level': assess_testing_threat(research_design),
            'mitigation_strategies': [
                '标准化工具',
                '工具等效性检验',
                '双盲设计',
                '工具培训'
            ],
            'indicators': [
                '工具信度',
                '测试一致性',
                '测试者培训效果'
            ]
        },
        'instrumentation': {
            'threat_level': assess_instrumentation_threat(research_design),
            'mitigation_strategies': [
                '工具标准化',
                '预测试',
                '跨工具比较',
                '工具校准'
            ],
            'indicators': [
                '工具信度',
                '测量精度',
                '工具稳定性'
            ]
        }
    }
    
    return {
        'threats': validity_threats,
        'overall_assessment': calculate_overall_validity(validity_threats),
        'recommendations': generate_validity_recommendations(validity_threats)
    }

def assess_selection_threat(research_design):
    """评估选择威胁"""
    if research_design.get('sampling_method') == 'convenience':
        return 'high'
    elif research_design.get('sampling_method') == 'purposive':
        return 'medium'
    elif research_design.get('sampling_method') == 'random':
        return 'low'
    else:
        return 'unknown'

def calculate_overall_validity(threats):
    """计算整体效度"""
    threat_levels = [threat['threat_level'] for threat in threats.values()]
    
    # 简化评估（实际应用中需要更复杂的算法）
    if any(level == 'high' for level in threat_levels):
        return 'low'
    elif any(level == 'medium' for level in threat_levels):
        return 'medium'
    else:
        return 'high'
```

### 2. 外在效度评估
**核心技能**：
```python
def assess_external_validity(research_results):
    """评估外在效度"""
    validity_aspects = {
        'population_validity': {
            'target_population': research_results['target_population'],
            'sample_representativeness': assess_sample_representativeness(
                research_results['sample'], 
                research_results['target_population']
            ),
            'sampling_method': research_results['sampling_method']
        },
        'ecological_validity': {
            'real_world_setting': assess_setting_authenticity(research_results),
            'context_similarity': assess_context_similarity(research_results),
            'time_relevance': assess_time_relevance(research_results)
        },
        'temporal_validity': {
            'time_period_relevance': assess_time_relevance(research_results),
            'historical_context': assess_historical_context(research_results),
            'future_applicability': assess_future_applicability(research_results)
        },
        'cross_cultural_validity': {
            'cultural_applicability': assess_cultural_applicability(research_results),
            'language_applicability': assess_language_applicability(research_results),
            'contextual_relevance': assess_contextual_relevance(research_results)
        }
    }
    
    return {
        'aspects': validity_aspects,
        'overall_assessment': calculate_external_validity_score(validity_aspects),
        'generalizability': assess_generalizability(validity_aspects),
        'limitations': identify_external_limitations(validity_aspects)
    }

def assess_sample_representativeness(sample, population):
    """评估样本代表性"""
    # 简化评估
    sample_size = len(sample)
    population_size = len(population)
    
    # 检查关键特征分布
    key_characteristics = ['age', 'gender', 'education', 'income', 'region']
    representativeness_scores = []
    
    for characteristic in key_characteristics:
        sample_dist = get_characteristic_distribution(sample, characteristic)
        population_dist = get_characteristic_distribution(population, characteristic)
        
        # 计算分布相似度
        similarity = calculate_distribution_similarity(sample_dist, population_dist)
        representativeness_scores.append(similarity)
    
    return sum(representativeness_scores) / len(representativeness_scores)
```

### 3. 构念效度评估
**核心技能**：
```python
def assess_construct_validity(measurement_tools, research_concepts):
    """评估构念效度"""
    validity_assessment = {
        'content_validity': {
            'expert_validation': assess_expert_validation(measurement_tools, research_concepts),
            'face_validity': assess_face_validity(measurement_tools, research_concepts),
            'convergent_validity': assess_convergent_validity(measurement_tools, research_concepts),
            'discriminant_validity': assess_discriminant_validity(measurement_tools, research_concepts)
        },
        'criterion_validity': {
            'predictive_validity': assess_predictive_validity(measurement_tools, research_concepts),
            'concurrent_validity': assess_concurrent_validity(measurement_tools, research_concepts),
            'postdictive_validity': assess_postdictive_validity(measurement_tools, research_concepts)
        },
        'translation_validity': {
            'nomological_network': assess_nomological_network(measurement_tools),
            'convergent_discriminant': assess_convergent_discriminant(measurement_tools),
            'discriminant_convergent': assess_discriminant_convergent(measurement_tools)
        }
    }
    
    return {
        'assessment': validity_assessment,
        'overall_score': calculate_construct_validity_score(validity_assessment),
        'weaknesses': identify_construct_weaknesses(validity_assessment),
        'improvements': suggest_construct_improvements(validity_assessment)
    }

def assess_expert_validation(tools, concepts):
    """专家效度评估"""
    validation_results = {}
    
    for concept in concepts:
        # 模拟专家评估（实际应用中需要真实专家参与）
        expert_rating = simulate_expert_rating(concept, tools)
        validation_results[concept] = expert_rating
    
    return validation_results

def simulate_expert_rating(concept, available_tools):
    """模拟专家评分（简化版本）"""
    # 基于工具覆盖度和概念复杂度评估
    tool_coverage = len([tool for tool in available_tools if concept in tool['measures']])
    concept_complexity = assess_concept_complexity(concept)
    
    # 简化评分算法
    base_score = (tool_coverage / len(available_tools)) * 0.7
    complexity_adjustment = (concept_complexity / 10) * 0.3
    
    return min(base_score + complexity_adjustment, 1.0)
```

### 4. 统计结论效度评估
**核心技能**：
```python
def assess_statistical_conclusion(data_analysis):
    """评估统计结论效度"""
    validity_checks = {
        'assumption_testing': {
            'normality_assumption': assess_normality_assumption(data_analysis),
            'independence_assumption': assess_independence_assumption(data_analysis),
            'homogeneity_assumption': assess_homogeneity_assumption(data_analysis),
            'linearity_assumption': assess_linearity_assumption(data_analysis)
        },
        'statistical_power': {
            'power_analysis': calculate_statistical_power(data_analysis),
            'sample_size_adequacy': assess_sample_size_adequacy(data_analysis),
            'effect_size_meaning': assess_effect_size_meaning(data_analysis)
        },
        'multiple_comparisons': {
            'type_i_error_rate': calculate_type_i_error_rate(data_analysis),
            'familywise_error_rate': calculate_familywise_error_rate(data_analysis),
            'false_discovery_rate': calculate_false_discovery_rate(data_analysis)
        },
        'robustness_checks': {
            'sensitivity_analysis': perform_sensitivity_analysis(data_analysis),
            'outlier_influence': assess_outlier_influence(data_analysis),
            'model_specification': check_model_specification(data_analysis)
        }
    }
    
    return {
        'checks': validity_checks,
        'overall_assessment': calculate_statistical_validity(validity_checks),
        'recommendations': generate_statistical_recommendations(validity_checks),
        'report_templates': generate_statistical_report_templates(validity_checks)
    }

def assess_normality_assumption(data_analysis):
    """评估正态性假设"""
    test_stat, p_value = scipy.stats.shapiro(data_analysis['data'])
    
    if p_value > 0.05:
        return {'assumption_met': 'no', 'p_value': p_value, 'test_statistic': test_stat}
    else:
        return {'assumption_met': 'yes', 'p_value': p_value, 'test_statistic': test_stat}

def calculate_statistical_power(data_analysis):
    """计算统计功效"""
    effect_size = data_analysis.get('effect_size')
    sample_size = data_analysis.get('sample_size')
    alpha = 0.05  # 显著性水平
    
    # 使用Cohen's d的近似功效计算
    if effect_size is None or sample_size is None:
        return {'power': 'unknown', 'reason': 'Missing effect size or sample size'}
    
    # 简化的功效计算
    z_alpha = 1.96  # 双尾检验的临界值
    n1 = sample_size / 2
    n2 = sample_size / 2
    
    power = 0.5 * (1 - norm.cdf(z_alpha - effect_size * math.sqrt(n1 * n2 / 2)))
    
    return {'power': power, 'effect_size': effect_size, 'sample_size': sample_size}
```

## 📊 质量检查清单

### 效度评估完整性
- [ ] 是否进行了四维度效度评估
- [ ] 是否识别了主要威胁因素
- [ ] 是否提供了改进建议
- [ ] 是否考虑了中文语境特殊性
- [ ] 是否提供了具体实施方案

### 统计方法科学性
- [ ] 假设检验是否正确执行
- [ ] 功效分析是否充分
- [ ] 多重比较是否控制
- [ ] 鲾棒性检验是否完成

### 实践可行性
- [ ] 改进方案是否可操作
- [ ] 成本效益是否合理
- [ ] 时间安排是否可行
- [ ] 技术要求是否可达
- [ ] 伦理要求是否满足

## 💡 快速响应模板

### 紧急效度评估模板
```
1. 提供效度检查清单
2. 快速识别主要威胁
3. 生成初步改进建议
4. 提供标准化报告模板
5. 承诺48小时内完成详细评估
```

### 标准效度评估模板
```
1. 系统性四维度效度评估
2. 详细分析威胁因素
3. 设计效度增强方案
4. 生成完整评估报告
5. 提供实施指导和时间表
```

## 🔧 效度增强策略

### 内在效度增强
```python
def enhance_internal_validity(research_design):
    """增强内在效度"""
    enhancements = []
    
    # 随机化增强
    if research_design.get('randomization') != 'true':
        enhancements.append("建议采用随机分配方法")
    
    # 匹配设计增强
    if research_design.get('matching') != 'true':
        enhancements.append("建议采用匹配设计")
    
    # 前后测设计增强
    if not research_design.get('pretest'):
        enhancements.append("建议增加前测")
    
    return enhancements
```

### 外在效度增强
```python
def enhance_external_validity(research_design):
    """增强外在效度"""
    enhancements = []
    
    # 样本多样性增强
    if research_design.get('sample_diversity') == 'low':
        enhancements.append("建议增加样本多样性")
    
    # 多地点研究
    if not research_design.get('multi_site'):
        enhancements.append("建议考虑多地点研究")
    
    # 历史比较研究
    if not research_design.get('historical_comparison'):
        enhancements.append("建议添加历史比较")
    
    return enhancements
```

---

**使用说明**：此技能严格遵循社会科学研究效度评估规范，提供科学、系统的效度分析支持。