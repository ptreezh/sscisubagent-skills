---
name: assessing-validity-reliability
description: 评估研究信度和效度，包括内在效度、外在效度、构念效度、统计结论效度的检验和提升。当需要验证研究质量、处理效度问题或提高研究严谨性时使用此技能。
---

# 信度效度分析技能

## 🎯 核心目标（最高优先级）
为中文社会科学研究提供科学、系统的信度效度评估和提升方案，确保研究的科学性和可信度。

## 📋 必须首先掌握的效度类型

### 1. 四大效度类型
**最重要概念**：
- **内在效度**：因果推断的准确性，研究是否真正测量了想要测量的概念
- **外在效度**：结果推广的适用性，研究结果是否适用于其他情境
- **构念效度**：测量的准确性，测量工具是否真正反映了理论概念
- **统计结论效度**：统计推断的可靠性，统计结论是否准确

### 2. 中文社科研究特殊挑战
**必须考虑**：
- **文化敏感性**：中国文化的特殊性对测量工具的影响
- **语言适切性**：中文表达和理解的复杂性
- **制度环境**：中国制度环境对研究结果的限制
- **实践相关性**：理论与实践的结合度

### 3. 质量控制的黄金标准
**必须确保**：
- **多重验证**：使用多种方法验证同一结果
- **三角验证**：定量、定性、方法三角验证
- **专家评审**：领域专家的独立评估
- **透明报告**：详细报告效度评估过程

## 🔄 动态知识库加载

### 启动时加载
```
/knowledge-base/main-knowledge.md
/knowledge-base/core-concepts.md
/knowledge-base/validity-fundamentals.md
```

### 按需加载
```
用户检验内在效度 → /knowledge-base/internal-validity.md
用户检验外在效度 → /knowledge-base/external-validity.md
用户需要效度提升 → /knowledge-base/validity-improvement.md
```

## 🚨 紧急处理协议

### 红色警报（论文答辩）
**快速评估模式**：
1. 快速检查四大效度基本要求
2. 识别最严重的效度威胁
3. 提供紧急改进方案
4. 生成效度检查清单
5. 承诺48小时内完成详细评估

### 黄色警报（导师要求）
**标准评估模式**：
1. 系统性四大效度检验
2. 详细分析效度威胁
3. 制定改进策略
4. 提供效度提升方案
5. 生成完整评估报告

## 🛠️ 核心评估技能

### 1. 内在效度评估
**核心技能**：
```python
def assess_internal_validity(research_design, data):
    """评估内在效度"""
    validity_threats = {
        'history': {
            'threat': '历史事件影响',
            'mitigation': ['前测-后测设计', '对照组设计', '统计控制'],
            'assessment': check_history_threats
        },
        'maturation': {
            'threat': '被试者成熟变化',
            'mitigation': ['缩短研究周期', '成熟度匹配', '统计分析'],
            'assessment': check_maturation_threats
        },
        'testing': {
            'threat': '测试效应影响',
            'mitigation': ['Solomon四组设计', '隐蔽测试', '工具平衡'],
            'assessment': check_testing_threats
        },
        'instrumentation': {
            'threat': '测量工具不准确',
            'mitigation': '工具验证', '预测试', '校准程序'],
            'assessment': check_instrumentation_threats
        }
    }
    
    # 综合评估
    overall_validity = calculate_overall_validity(validity_threats, data)
    
    return {
        'threats': validity_threats,
        'overall_score': overall_validity,
        'recommendations': generate_improvement_recommendations(validity_threats),
        'timeline': create_improvement_timeline(overall_validity)
    }

def check_history_threats(research_design, data):
    """检查历史威胁"""
    threats = []
    
    # 检查是否有重大事件
    major_events = identify_major_events(research_design['timeframe'])
    if major_events:
        threats.append({
            'type': '历史事件',
            'event': major_events,
            'impact': '可能影响研究结果',
            'mitigation': '需要在分析中控制'
        })
    
    return threats

def calculate_overall_validity(threats, data):
    """计算综合效度"""
    threat_scores = {
        'history': 0.8,
        'maturation': 0.7,
        'testing': 0.6,
        'instrumentation': 0.9
    }
    
    total_threat = 0
    weighted_threat = 0
    
    for threat_type, threats_list in threats.items():
        for threat in threats_list:
            total_threat += 1
            weighted_threat += threat_scores[threat_type]
    
    if total_threat == 0:
        return 1.0
    
    return 1.0 - (weighted_threat / total_threat)
```

### 2. 外在效度评估
**核心技能**：
```python
def assess_external_validity(research_results, target_population):
    """评估外在效度"""
    validity_types = {
        'population_validity': {
            'description': '目标总体的代表性',
            'assessment': assess_population_representativeness
        },
        'ecological_validity': {
            'description': '真实环境的适用性',
            'assessment': assess_ecological_applicability
        },
        'temporal_validity': {
            'description': '时间跨度的适用性',
            'assessment': assess_temporal_generalizability
        },
        'cross_cultural_validity': {
            'description': '跨文化的适用性',
            'assessment': assess_cultural_transferability
        }
    }
    
    validity_scores = {}
    for validity_type, details in validity_types.items():
        validity_scores[validity_type] = details['assessment'](research_results, target_population)
    
    return {
        'scores': validity_scores,
        'overall_score': sum(validity_scores.values()) / len(validity_scores),
        'limitations': identify_external_limitations(validity_scores),
        'generalizability_statement': generate_generalizability_statement(validity_scores)
    }

def assess_population_representativeness(sample, population):
    """评估样本代表性"""
    representativeness_indicators = {
        'sample_size_adequacy': check_sample_size(sample, population),
        'sampling_method_appropriateness': check_sampling_method(sample),
        'demographic_similarity': check_demographic_similarity(sample, population),
        'geographic_coverage': check_geographic_coverage(sample, population)
    }
    
    # 综合评估
    adequacy_score = calculate_representativeness_score(representativeness_indicators)
    
    return adequacy_score
```

### 3. 构念效度评估
**核心技能**：
```python
def assess_construct_validity(measurement_tools, theoretical_concepts):
    """评估构念效度"""
    validity_assessment = {
        'content_validity': {
            'description': '测量内容的全面性',
            'assessment': assess_content_coverage
        },
        'criterion_validity': {
            'description': '测量标准的准确性',
            'assessment': assess_criterion_accuracy
        },
        'convergent_validity': {
            'description': '多种方法的一致性',
            'assessment': assess_convergent_methods
        },
        'discriminant_validity': {
            'description': '区分不同概念的能力',
            'assessment': assess_discriminant_ability
        }
    }
    
    validity_scores = {}
    for validity_type, details in validity_assessment.items():
        validity_scores[validity_type] = details['assessment'](measurement_tools, theoretical_concepts)
    
    return {
        'scores': validity_scores,
        'overall_score': sum(validity_scores.values()) / len(validity_scores),
        'improvement_strategies': generate_construct_improvement_strategies(validity_scores),
        'validation_matrix': create_validation_matrix(measurement_tools, theoretical_concepts)
    }

def assess_content_coverage(measurement_items, theoretical_framework):
    """评估内容覆盖度"""
    framework_concepts = extract_concepts(theoretical_framework)
    measured_concepts = extract_concepts(measurement_items)
    
    coverage_ratio = len(measured_concepts & framework_concepts) / len(framework_concepts)
    
    return coverage_ratio
```

### 4. 统计结论效度评估
**核心技能**：
```python
def assess_statistical_conclusion_validity(statistical_analysis):
    """评估统计结论效度"""
    validity_checks = {
        'sample_size_adequacy': check_sample_size(statistical_analysis),
        'assumption_violations': check_assumptions(statistical_analysis),
        'statistical_power': check_statistical_power(statistical_analysis),
        'multiple_comparisons': check_multiple_comparisons(statistical_analysis),
        'data_distribution': check_data_distribution(statistical_analysis)
    }
    
    validity_score = calculate_statistical_validity(validity_checks)
    
    return {
        'checks': validity_checks,
        'overall_score': validity_score,
        'threats': identify_statistical_threats(validity_checks),
        'recommendations': generate_statistical_recommendations(validity_checks)
    }

def check_statistical_power(statistical_analysis):
    """检查统计功效"""
    effect_size = statistical_analysis.get('effect_size')
    sample_size = statistical_analysis.get('sample_size')
    alpha = statistical_analysis.get('alpha', 0.05)
    
    # 使用Cohen's d计算功效
    if effect_size and sample_size:
        power = calculate_cohen_d_power(effect_size, sample_size, alpha)
        return power
    else:
        return None

def calculate_cohen_d_power(effect_size, sample_size, alpha):
    """计算Cohen's d的功效"""
    # 简化的功效计算
    z_alpha = 1.96  # 双尾检验，alpha=0.05
    z_beta = 0.84   # 功�效=0.80
    
    n = sample_size
    d = effect_size
    
    # Cohen's d功效公式（简化版）
    power = norm.cdf((n * d / 2) - z_alpha) + norm.cdf((-n * d / 2) - z_alpha)
    
    return power
```

## 📊 质量检查清单

### 效度评估完整性
- [ ] 是否进行了四种效度评估
- [ ] 是否识别了主要效度威胁
- [ ] 是否提供了改进建议
- [ ] 是否制定了改进计划
- [ ] 是否记录了评估过程

### 评估方法科学性
- [ ] 评估方法是否适合研究类型
- [ ] 评估工具是否可靠有效
- [ ] 评估过程是否透明可追溯
- [ ] 评估结果是否客观准确
- [ ] 改进建议是否具体可行

### 中文本土化适配
- [ ] 是否考虑了中国文化特殊性
- [ ] 是否适配了中文语境
- [ ] 是否结合了中国案例
- [ ] 是否符合中文学术规范
- [ ] 是否考虑了实践相关性

## 💡 快速响应模板

### 紧急效度评估模板
```
1. 快速检查四大效度基本要求
2. 识别最严重的效度威胁
3. 提供紧急改进方案
4. 生成效度检查清单
5. 承诺48小时内完成详细评估
```

### 标准效度评估模板
```
1. 系统性四大效度检验
2. 详细分析效度威胁
3. 制定改进策略
4. 提供效度提升方案
5. 生成完整评估报告
```

---

**使用说明**：此技能严格遵循社会科学研究效度评估规范，确保研究的科学性和可信度。