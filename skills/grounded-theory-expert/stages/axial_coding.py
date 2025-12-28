"""
轴心编码模块
此模块提供扎根理论轴心编码阶段的各项功能
"""

from typing import Dict, List, Any
import json


def axial_coding(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行扎根理论的轴心编码阶段
    
    Args:
        data: 包含开放编码结果的数据字典
    
    Returns:
        包含轴心编码结果的字典
    """
    # 从数据中提取开放编码结果
    concepts = data.get('concepts', [])
    
    # 执行范畴识别
    categories = identify_categories(concepts)
    
    # 执行属性维度分析
    category_properties = analyze_properties(categories)
    
    # 执行关系建立
    relationships = build_relationships(categories)
    
    # 执行Paradigm构建
    paradigm = construct_paradigm(categories, relationships)
    
    # 返回轴心编码结果
    return {
        "categories": categories,
        "category_properties": category_properties,
        "relationships": relationships,
        "paradigm": paradigm,
        "axial_coding_process": {
            "initial_concepts": len(concepts),
            "identified_categories": len(categories),
            "established_relationships": len(relationships),
            "paradigm_completeness": calculate_paradigm_completeness(paradigm)
        },
        "memo_notes": generate_axial_memos(categories, relationships)
    }


def identify_categories(concepts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    从概念中识别范畴
    
    Args:
        concepts: 概念列表
    
    Returns:
        识别出的范畴列表
    """
    # 简化的范畴识别逻辑
    # 在实际应用中，这里会使用更复杂的聚类算法
    categories = []
    
    # 按概念名称的首字母进行简单分组
    category_map = {}
    for concept in concepts:
        first_char = concept["code"][0] if concept["code"] else "其他"
        if first_char not in category_map:
            category_map[first_char] = {
                "id": f"category_{first_char}",
                "name": f"关于{first_char}的范畴",
                "definition": f"包含与{first_char}相关的概念",
                "concepts": [],
                "properties": {}
            }
        category_map[first_char]["concepts"].append(concept)
    
    # 将映射转换为列表
    categories = list(category_map.values())
    
    # 为每个范畴计算属性
    for category in categories:
        category["properties"] = calculate_category_properties(category["concepts"])
    
    return categories


def calculate_category_properties(concepts: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    计算范畴的属性
    
    Args:
        concepts: 概念列表
    
    Returns:
        范畴属性字典
    """
    if not concepts:
        return {}
    
    # 简化的属性计算
    total_examples = sum(len(c.get("examples", [])) for c in concepts)
    avg_example_length = sum(len(" ".join(c.get("examples", []))) for c in concepts) / len(concepts) if concepts else 0
    
    return {
        "total_concepts": len(concepts),
        "total_examples": total_examples,
        "avg_example_length": avg_example_length,
        "concept_diversity": len(set(c["code"][0] if c["code"] else "" for c in concepts))
    }


def analyze_properties(categories: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析范畴的属性维度
    
    Args:
        categories: 范畴列表
    
    Returns:
        属性分析结果
    """
    properties_analysis = {}
    
    for category in categories:
        category_id = category["id"]
        properties_analysis[category_id] = {
            "core_attributes": ["frequency", "diversity", "complexity"],  # 简化属性
            "dimensions": ["temporal", "contextual", "relational"],  # 简化维度
            "attribute_values": {
                "frequency": len(category["concepts"]),
                "diversity": category["properties"]["concept_diversity"],
                "complexity": len(category["concepts"]) * category["properties"]["avg_example_length"]
            }
        }
    
    return properties_analysis


def build_relationships(categories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    建立范畴间的关系
    
    Args:
        categories: 范畴列表
    
    Returns:
        关系列表
    """
    relationships = []
    
    # 简化的范畴关系建立
    for i, cat1 in enumerate(categories):
        for j, cat2 in enumerate(categories[i+1:], i+1):
            # 计算范畴间的关系强度（简化计算）
            relationship_strength = calculate_relationship_strength(cat1, cat2)
            
            # 确定关系类型（简化判断）
            relationship_type = determine_relationship_type(cat1, cat2)
            
            relationship = {
                "id": f"rel_{cat1['id']}_to_{cat2['id']}",
                "source_category": cat1["id"],
                "target_category": cat2["id"],
                "type": relationship_type,
                "strength": relationship_strength,
                "evidence": f"基于范畴 {cat1['name']} 和 {cat2['name']} 的概念重叠"
            }
            
            relationships.append(relationship)
    
    return relationships


def calculate_relationship_strength(cat1: Dict[str, Any], cat2: Dict[str, Any]) -> float:
    """
    计算范畴间的关系强度
    
    Args:
        cat1: 范畴1
        cat2: 范畴2
    
    Returns:
        关系强度 (0-1)
    """
    # 简化的强度计算
    # 在实际应用中，这里会使用更复杂的语义分析
    return 0.5  # 简化值


def determine_relationship_type(cat1: Dict[str, Any], cat2: Dict[str, Any]) -> str:
    """
    确定范畴间的关系类型
    
    Args:
        cat1: 范畴1
        cat2: 茌畴2
    
    Returns:
        关系类型
    """
    # 简化的关系类型判断
    # 在实际应用中，这里会使用更复杂的逻辑
    import random
    relationship_types = ["causal", "conditional", "strategic", "interactive"]
    return random.choice(relationship_types)


def construct_paradigm(categories: List[Dict[str, Any]], relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    构建Paradigm模型
    
    Args:
        categories: 范畴列表
        relationships: 关系列表
    
    Returns:
        Paradigm模型
    """
    # 简化的Paradigm构建
    # 在实际应用中，这里会使用更复杂的理论构建算法
    
    if not categories:
        return {}
    
    # 选择第一个范畴作为核心现象
    core_phenomenon = categories[0]["name"]
    
    # 简化的Paradigm组件
    paradigm = {
        "phenomenon": core_phenomenon,
        "conditions": [cat["name"] for cat in categories[1:3]] if len(categories) > 1 else [],
        "context": [cat["name"] for cat in categories[1:3]] if len(categories) > 1 else [],
        "action_strategies": [cat["name"] for cat in categories[2:4]] if len(categories) > 2 else [],
        "consequences": [cat["name"] for cat in categories[3:5]] if len(categories) > 3 else [],
        "relationships": relationships
    }
    
    return paradigm


def calculate_paradigm_completeness(paradigm: Dict[str, Any]) -> float:
    """
    计算Paradigm的完整度
    
    Args:
        paradigm: Paradigm模型
    
    Returns:
        完整度分数 (0-1)
    """
    required_components = ["phenomenon", "conditions", "action_strategies"]
    present_components = [comp for comp in required_components if paradigm.get(comp)]
    
    return len(present_components) / len(required_components)


def generate_axial_memos(categories: List[Dict[str, Any]], relationships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    生成轴心编码备忘录
    
    Args:
        categories: 范畴列表
        relationships: 关系列表
    
    Returns:
        备忘录列表
    """
    memos = []
    
    # 为每个范畴生成备忘录
    for category in categories:
        memo = {
            "type": "category_memo",
            "title": f"关于范畴 '{category['name']}' 的轴心编码备忘录",
            "content": f"在轴心编码阶段，将相关概念整合为范畴 '{category['name']}'。该范畴包含 {len(category['concepts'])} 个概念，具有 {category['properties']['concept_diversity']} 种不同属性。",
            "date": "2025-12-27",
            "related_categories": [category['id']]
        }
        memos.append(memo)
    
    # 为关系模式生成备忘录
    if relationships:
        relationship_memo = {
            "type": "relationship_memo",
            "title": "范畴关系模式备忘录",
            "content": f"识别出 {len(relationships)} 个范畴间关系，包括因果、条件、策略和互动关系。这些关系构成了理论模型的基础。",
            "date": "2025-12-27",
            "related_categories": list(set([rel["source_category"] for rel in relationships] + [rel["target_category"] for rel in relationships]))
        }
        memos.append(relationship_memo)
    
    return memos