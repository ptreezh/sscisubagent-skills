---
name: checking-theory-saturation
description: 检验扎根理论饱和度，包括新概念识别、范畴完善度、关系充分性和理论完整性评估。当需要判断理论是否达到饱和、是否需要补充数据或是否可以结束研究时使用此技能。
---

# 理论饱和度检验技能

## 🎯 核心目标（最高优先级）
为扎根理论研究提供科学、系统的理论饱和度检验，确保理论构建的完整性和可靠性。

## 📋 必须首先掌握的饱和度标准

### 1. 理论饱和的定义
**最重要标准**：
- **无新概念**：分析新数据时不再出现新的重要概念
- **范畴完善**：现有范畴的属性和维度发展充分
- **关系稳定**：范畴间的关系网络稳定
- **理论完整**：理论能够解释所有重要现象

### 2. 饱和度检验的四个维度
**必须检验**：
- **概念饱和**：概念库的稳定性
- **范畴饱和**：范畴发展的完整性
- **关系饱和**：关系网络的稳定性
- **理论饱和**：理论解释的充分性

### 3. 中文语境特殊要求
**必须考虑**：
- **文化特殊性**：中国文化背景下的概念理解
- **语言表达**：中文术语的准确性和一致性
- **实践相关性**：理论与实践的结合度
- **学术规范**：符合中文学术写作规范

## 🔄 动态知识库加载

### 启动时加载
```
/knowledge-base/main-knowledge.md
/knowledge-base/core-concepts.md
/knowledge-base/saturation-criteria.md
```

### 按需加载
```
用户需要检验概念 → /knowledge-base/concept-saturation.md
用户需要检验范畴 → /knowledge-base/category-saturation.md
用户需要检验关系 → /knowledge-base/relationship-saturation.md
```

## 🚨 紧急处理协议

### 红色警报（论文截止）
**快速检验模式**：
1. 使用简化饱和度检查表
2. 快速评估核心概念和范畴
3. 提供饱和度初步结论
4. 承诺24小时内完成详细检验

### 黄色警报（导师要求）
**标准检验模式**：
1. 系统性四维饱和度检验
2. 详细分析饱和度指标
3. 生成饱和度检验报告
4. 提供补充建议

## 🛠️ 核心检验技能

### 1. 概念饱和度检验
**核心技能**：
```python
def check_concept_saturation(coding_data, new_data):
    """检验概念饱和度"""
    existing_concepts = set(coding_data['concepts'])
    new_concepts = set(new_data['concepts'])
    
    saturation_metrics = {
        'new_concept_rate': len(new_concepts - existing_concepts) / len(new_concepts),
        'concept_overlap': len(existing_concepts & new_concepts) / len(existing_concepts),
        'concept_diversity': calculate_concept_diversity(existing_concepts),
        'concept_stability': assess_concept_stability(coding_data)
    }
    
    # 饱和度判断
    if saturation_metrics['new_concept_rate'] < 0.05:
        saturation_level = 'high'
        recommendation = "概念已基本饱和"
    elif saturation_metrics['new_concept_rate'] < 0.15:
        saturation_level = 'medium'
        recommendation = "概念接近饱和，建议继续观察"
    else:
        saturation_level = 'low'
        recommendation = "概念未饱和，需要继续收集数据"
    
    return {
        'metrics': saturation_metrics,
        'level': saturation_level,
        'recommendation': recommendation,
        'new_concepts': list(new_concepts - existing_concepts),
        'analysis': analyze_concept_patterns(new_concepts)
    }

def calculate_concept_diversity(concepts):
    """计算概念多样性"""
    # 基于概念属性计算多样性
    concept_attributes = {}
    for concept in concepts:
        concept_attributes[concept] = {
            'category': get_concept_category(concept),
            'abstraction_level': get_abstraction_level(concept),
            'domain': get_concept_domain(concept)
        }
    
    category_diversity = len(set(attr['category'] for attr in concept_attributes.values()))
    domain_diversity = len(set(attr['domain'] for attr in concept_attributes.values()))
    
    return (category_diversity + domain_diversity) / 2
```

### 2. 范畴饱和度检验
**核心技能**：
```python
def check_category_saturation(coding_data):
    """检验范畴饱和度"""
    categories = coding_data['categories']
    
    saturation_metrics = {
        'category_completeness': assess_category_completeness(categories),
        'attribute_development': assess_attribute_development(categories),
        'dimension_coverage': assess_dimension_coverage(categories),
        'relationship_clarity': assess_relationship_clarity(categories)
    }
    
    # 综合饱和度评估
    saturation_scores = list(saturation_metrics.values())
    average_score = sum(saturation_scores) / len(saturation_scores)
    
    if average_score >= 0.8:
        saturation_level = 'high'
        recommendation = "范畴发展充分，结构稳定"
    elif average_score >= 0.6:
        saturation_level = 'medium'
        recommendation = "范畴发展基本完善，可进一步细化"
    else:
        saturation_level = 'low'
        recommendation = "范畴发展不充分，需要继续分析"
    
    return {
        'metrics': saturation_metrics,
        'overall_score': average_score,
        'level': saturation_level,
        'recommendation': recommendation,
        'weak_categories': identify_weak_categories(categories),
        'improvement_suggestions': generate_improvement_suggestions(categories)
    }

def assess_category_completeness(categories):
    """评估范畴完整性"""
    completeness_scores = {}
    
    for category_name, category_data in categories.items():
        score = 0.0
        
        # 检查基本要素
        if category_data.get('definition'):
            score += 0.3
        if category_data.get('properties'):
            score += 0.3
        if category_data.get('dimensions'):
            score += 0.2
        if category_data.get('examples'):
            score += 0.1
        if category_data.get('relationships'):
            score += 0.1
        
        completeness_scores[category_name] = score
    
    return completeness_scores
```

### 3. 关系饱和度检验
**核心技能**：
```python
def check_relationship_saturation(coding_data):
    """检验关系饱和度"""
    relationships = coding_data['relationships']
    
    saturation_metrics = {
        'relationship_density': calculate_relationship_density(relationships),
        'relationship_stability': assess_relationship_stability(relationships),
        'pattern_consistency': assess_pattern_consistency(relationships),
        'missing_relationships': identify_missing_relationships(relationships)
    }
    
    # 关系网络分析
    network_analysis = analyze_relationship_network(relationships)
    
    if saturation_metrics['relationship_density'] > 0.7:
        saturation_level = 'high'
        recommendation = "关系网络密集，结构稳定"
    elif saturation_metrics['relationship_density'] > 0.5:
        saturation_level = 'medium'
        recommendation = "关系网络基本完整"
    else:
        saturation_level = 'low'
        recommendation = "关系网络稀疏，需要补充分析"
    
    return {
        'metrics': saturation_metrics,
        'level': saturation_level,
        'recommendation': recommendation,
        'network_analysis': network_analysis,
        'critical_relationships': identify_critical_relationships(relationships),
        'relationship_gaps': identify_relationship_gaps(relationships)
    }

def calculate_relationship_density(relationships):
    """计算关系密度"""
    if not relationships:
        return 0.0
    
    # 构建关系矩阵
    categories = set()
    for rel in relationships:
        categories.add(rel['source'])
        categories.add(rel['target'])
    
    n = len(categories)
    max_relationships = n * (n - 1) / 2
    actual_relationships = len(relationships)
    
    return actual_relationships / max_relationships if max_relationships > 0 else 0.0
```

### 4. 理论饱和度检验
**核心技能**：
```python
def check_theory_saturation(theory_framework, empirical_data):
    """检验理论饱和度"""
    saturation_metrics = {
        'explanatory_power': assess_explanatory_power(theory_framework, empirical_data),
        'theoretical_coherence': assess_theoretical_coherence(theory_framework),
        'empirical_coverage': assess_empirical_coverage(theory_framework, empirical_data),
        'boundary_conditions': assess_boundary_conditions(theory_framework)
    }
    
    # 综合理论评估
    theory_scores = list(saturation_metrics.values())
    average_score = sum(theory_scores) / len(theory_scores)
    
    if average_score >= 0.85:
        saturation_level = 'high'
        recommendation = "理论已充分发展，解释力强"
    elif average_score >= 0.7:
        saturation_level = 'medium'
        recommendation = "理论基本成熟，可进一步细化"
    else:
        saturation_level = 'low'
        recommendation = "理论发展不充分，需要继续构建"
    
    return {
        'metrics': saturation_metrics,
        'overall_score': average_score,
        'level': saturation_level,
        'recommendation': recommendation,
        'theoretical_gaps': identify_theoretical_gaps(theory_framework),
        'improvement_areas': suggest_theoretical_improvements(theory_framework)
    }

def assess_explanatory_power(theory, data):
    """评估解释力"""
    # 检查理论是否能够解释数据中的主要现象
    explained_phenomena = []
    unexplained_phenomena = []
    
    for phenomenon in data['key_phenomena']:
        if can_explain(theory, phenomenon):
            explained_phenomena.append(phenomenon)
        else:
            unexplained_phenomena.append(phenomenon)
    
    coverage_rate = len(explained_phenomena) / len(data['key_phenomena'])
    
    return coverage_rate
```

## 📊 质量检查清单

### 饱和度检验完整性
- [ ] 是否进行了四维饱和度检验
- [ ] 是否使用了科学的评估指标
- [ ] 是否提供了具体的饱和度结论
- [ ] 是否给出了明确的建议
- [ ] 是否记录了检验过程和依据

### 检验方法科学性
- [ ] 检验方法是否符合扎根理论规范
- [ ] 评估指标是否合理可靠
- [ ] 检验过程是否透明可追溯
- [ ] 结果解释是否客观准确
- [ ] 建议是否具有可操作性

### 中文本土化适配
- [ ] 是否考虑了中文语境特殊性
- [ ] 是否使用了中文术语规范
- [ ] 是否结合了中国案例
- [ ] 是否符合中文学术写作规范
- [ ] 是否考虑了实践相关性

## 💡 快速响应模板

### 紧急饱和度检验模板
```
1. 快速评估新概念出现率
2. 检查核心范畴完整性
3. 简单评估理论解释力
4. 提供饱和度初步结论
5. 承诺24小时内完成详细检验
```

### 标准饱和度检验模板
```
1. 系统性四维饱和度检验
2. 详细分析各项指标
3. 生成饱和度检验报告
4. 识别理论发展空间
5. 提供具体改进建议
```

---

**使用说明**：此技能严格遵循扎根理论饱和度检验规范，确保理论构建的科学性和完整性。