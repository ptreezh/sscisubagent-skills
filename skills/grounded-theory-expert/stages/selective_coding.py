"""
选择式编码模块
此模块提供扎根理论选择式编码阶段的各项功能
"""

from typing import Dict, List, Any
import json


def selective_coding(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行扎根理论的选择式编码阶段
    
    Args:
        data: 包含轴心编码结果的数据字典
    
    Returns:
        包含选择式编码结果的字典
    """
    # 从数据中提取轴心编码结果
    categories = data.get('categories', [])
    relationships = data.get('relationships', [])
    
    # 执行核心范畴识别
    core_category = identify_core_category(categories, relationships)
    
    # 执行故事线构建
    storyline = construct_storyline(categories, relationships, core_category)
    
    # 执行理论框架整合
    theory_framework = integrate_theory(categories, relationships, core_category, storyline)
    
    # 返回选择式编码结果
    return {
        "core_category": core_category,
        "storyline": storyline,
        "theory_framework": theory_framework,
        "selective_coding_process": {
            "total_categories": len(categories),
            "core_category_selected": core_category["name"] if core_category else "None",
            "storyline_elements": len(storyline.get("elements", [])) if storyline else 0,
            "theoretical_propositions": len(theory_framework.get("propositions", [])) if theory_framework else 0
        },
        "memo_notes": generate_selective_memos(core_category, storyline, theory_framework)
    }


def identify_core_category(categories: List[Dict[str, Any]], relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    识别核心范畴
    
    Args:
        categories: 范畴列表
        relationships: 关系列表
    
    Returns:
        核心范畴
    """
    if not categories:
        return {}
    
    # 计算每个范畴的指标来确定核心范畴
    category_scores = []
    
    for category in categories:
        # 计算解释力（与多少其他范畴有关系）
        explanation_power = sum(
            1 for rel in relationships 
            if rel["source_category"] == category["id"] or rel["target_category"] == category["id"]
        )
        
        # 计算数据支持（包含的概念数量）
        data_support = len(category.get("concepts", []))
        
        # 综合评分
        score = explanation_power * 0.6 + data_support * 0.4  # 加权评分
        
        category_scores.append({
            "category": category,
            "explanation_power": explanation_power,
            "data_support": data_support,
            "score": score
        })
    
    # 按评分排序，选择最高分的作为核心范畴
    category_scores.sort(key=lambda x: x["score"], reverse=True)
    
    if category_scores:
        top_category = category_scores[0]["category"]
        return {
            "name": top_category["name"],
            "id": top_category["id"],
            "definition": top_category["definition"],
            "explanation_power": category_scores[0]["explanation_power"],
            "data_support": category_scores[0]["data_support"],
            "score": category_scores[0]["score"],
            "rationale": f"该范畴与最多其他范畴相关（{category_scores[0]['explanation_power']}个关系），且有充分数据支持（{category_scores[0]['data_support']}个概念）"
        }
    
    return {}


def construct_storyline(categories: List[Dict[str, Any]], relationships: List[Dict[str, Any]], core_category: Dict[str, Any]) -> Dict[str, Any]:
    """
    构建故事线
    
    Args:
        categories: 范畴列表
        relationships: 关系列表
        core_category: 核心范畴
    
    Returns:
        故事线
    """
    if not core_category:
        return {}
    
    # 构建以核心范畴为中心的故事线
    storyline_elements = []
    
    # 找到与核心范畴直接相关的范畴
    core_related = [
        rel for rel in relationships 
        if rel["source_category"] == core_category["id"] or rel["target_category"] == core_category["id"]
    ]
    
    # 构建故事线元素
    for rel in core_related:
        source_cat = next((cat for cat in categories if cat["id"] == rel["source_category"]), None)
        target_cat = next((cat for cat in categories if cat["id"] == rel["target_category"]), None)
        
        if source_cat and target_cat:
            element = {
                "relationship_type": rel["type"],
                "from_category": source_cat["name"],
                "to_category": target_cat["name"],
                "strength": rel["strength"],
                "description": f"{source_cat['name']} 通过 {rel['type']} 关系影响 {target_cat['name']}"
            }
            storyline_elements.append(element)
    
    # 构建完整的故事线
    storyline = {
        "central_theme": f"围绕 {core_category['name']} 的现象",
        "elements": storyline_elements,
        "narrative_flow": build_narrative_flow(storyline_elements, core_category),
        "coherence_score": calculate_narrative_coherence(storyline_elements)
    }
    
    return storyline


def build_narrative_flow(elements: List[Dict[str, Any]], core_category: Dict[str, Any]) -> str:
    """
    构建叙事流程
    
    Args:
        elements: 故事线元素列表
        core_category: 核心范畴
    
    Returns:
        叙事流程描述
    """
    if not elements:
        return f"理论围绕核心范畴 '{core_category['name']}' 构建，但需要更多关系数据来形成完整叙事。"
    
    # 简化的叙事构建
    flow_parts = [f"理论以 '{core_category['name']}' 为核心"]
    
    for element in elements[:3]:  # 只取前3个元素以简化
        flow_parts.append(element["description"])
    
    return "，然后".join(flow_parts) + "。"


def calculate_narrative_coherence(elements: List[Dict[str, Any]]) -> float:
    """
    计算叙事连贯性
    
    Args:
        elements: 故事线元素列表
    
    Returns:
        连贯性分数 (0-1)
    """
    if not elements:
        return 0.0
    
    # 简化的连贯性计算
    # 在实际应用中，这里会使用更复杂的逻辑
    return min(1.0, len(elements) * 0.3)  # 基于元素数量的简单计算


def integrate_theory(categories: List[Dict[str, Any]], relationships: List[Dict[str, Any]], core_category: Dict[str, Any], storyline: Dict[str, Any]) -> Dict[str, Any]:
    """
    整合理论框架
    
    Args:
        categories: 范畴列表
        relationships: 关系列表
        core_category: 核心范畴
        storyline: 故事线
    
    Returns:
        理论框架
    """
    # 提炼理论命题
    propositions = generate_theoretical_propositions(categories, relationships, core_category)
    
    # 构建概念框架
    conceptual_framework = build_conceptual_framework(categories, core_category)
    
    # 解释作用机制
    mechanisms = explain_mechanisms(relationships)
    
    theory_framework = {
        "core_category": core_category,
        "storyline_summary": storyline.get("central_theme", ""),
        "propositions": propositions,
        "conceptual_framework": conceptual_framework,
        "mechanisms": mechanisms,
        "boundary_conditions": identify_boundary_conditions(categories),
        "theoretical_contributions": identify_theoretical_contributions(core_category, propositions)
    }
    
    return theory_framework


def generate_theoretical_propositions(categories: List[Dict[str, Any]], relationships: List[Dict[str, Any]], core_category: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    生成理论命题
    
    Args:
        categories: 范畴列表
        relationships: 关系列表
        core_category: 核心范畴
    
    Returns:
        理论命题列表
    """
    propositions = []
    
    # 基于关系生成命题
    for rel in relationships[:5]:  # 限制数量以简化
        source_cat = next((cat for cat in categories if cat["id"] == rel["source_category"]), None)
        target_cat = next((cat for cat in categories if cat["id"] == rel["target_category"]), None)
        
        if source_cat and target_cat:
            proposition = {
                "id": f"prop_{rel['id']}",
                "statement": f"当 {source_cat['name']} 发生时，会导致 {target_cat['name']} 的变化",
                "type": rel["type"],
                "strength": rel["strength"],
                "evidence": f"基于对 {len(source_cat.get('concepts', []))} 个概念和 {len(target_cat.get('concepts', []))} 个概念的分析"
            }
            propositions.append(proposition)
    
    return propositions


def build_conceptual_framework(categories: List[Dict[str, Any]], core_category: Dict[str, Any]) -> Dict[str, Any]:
    """
    构建概念框架
    
    Args:
        categories: 范畴列表
        core_category: 核心范畴
    
    Returns:
        概念框架
    """
    # 确定核心范畴在框架中的位置
    core_position = "central"  # 核心范畴处于中心位置
    
    # 组织其他范畴
    peripheral_categories = [cat for cat in categories if cat["id"] != core_category.get("id")]
    
    framework = {
        "core_element": core_category["name"],
        "core_position": core_position,
        "peripheral_elements": [cat["name"] for cat in peripheral_categories],
        "organizing_principle": f"以 {core_category['name']} 为核心组织相关范畴",
        "hierarchical_structure": {
            "level_1": [core_category["name"]],
            "level_2": [cat["name"] for cat in peripheral_categories[:3]],  # 前3个作为二级
            "level_3": [cat["name"] for cat in peripheral_categories[3:]]   # 其余作为三级
        }
    }
    
    return framework


def explain_mechanisms(relationships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    解释作用机制
    
    Args:
        relationships: 关系列表
    
    Returns:
        作用机制列表
    """
    mechanisms = []
    
    # 基于关系类型归纳机制
    mechanism_types = {}
    for rel in relationships:
        rel_type = rel["type"]
        if rel_type not in mechanism_types:
            mechanism_types[rel_type] = {
                "type": rel_type,
                "description": f"{rel_type} 类型的关系机制",
                "instances": 0,
                "examples": []
            }
        mechanism_types[rel_type]["instances"] += 1
    
    for mech in mechanism_types.values():
        mech["description"] = f"{mech['type']} 机制在理论中出现 {mech['instances']} 次，是连接不同范畴的重要方式"
        mechanisms.append(mech)
    
    return mechanisms


def identify_boundary_conditions(categories: List[Dict[str, Any]]) -> List[str]:
    """
    识别边界条件
    
    Args:
        categories: 范畴列表
    
    Returns:
        边界条件列表
    """
    # 简化的边界条件识别
    return [
        "研究情境的特定性",
        "参与者特征的限制",
        "时间范围的约束"
    ]


def identify_theoretical_contributions(core_category: Dict[str, Any], propositions: List[Dict[str, Any]]) -> List[str]:
    """
    识别理论贡献
    
    Args:
        core_category: 核心范畴
        propositions: 理论命题列表
    
    Returns:
        理论贡献列表
    """
    contributions = [
        f"识别了核心现象 '{core_category.get('name', 'Unknown')}' 及其在理论中的中心作用",
        f"建立了 {len(propositions)} 个理论命题，阐明了范畴间的关系"
    ]
    
    return contributions


def generate_selective_memos(core_category: Dict[str, Any], storyline: Dict[str, Any], theory_framework: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    生成选择式编码备忘录
    
    Args:
        core_category: 核心范畴
        storyline: 故事线
        theory_framework: 理论框架
    
    Returns:
        备忘录列表
    """
    memos = []
    
    # 核心范畴备忘录
    if core_category:
        core_memo = {
            "type": "core_category_memo",
            "title": f"核心范畴 '{core_category['name']}' 识别备忘录",
            "content": f"通过分析范畴的解释力和数据支持，确定 '{core_category['name']}' 为核心范畴。该范畴与 {core_category.get('explanation_power', 0)} 个其他范畴相关，有 {core_category.get('data_support', 0)} 个概念支持。",
            "date": "2025-12-27",
            "related_elements": [core_category["id"]]
        }
        memos.append(core_memo)
    
    # 故事线备忘录
    if storyline:
        storyline_memo = {
            "type": "storyline_memo",
            "title": "故事线构建备忘录",
            "content": f"构建了围绕核心范畴的故事线，包含 {len(storyline.get('elements', []))} 个关键元素，形成了理论的叙事主线。",
            "date": "2025-12-27",
            "related_elements": [elem.get("from_category", "") for elem in storyline.get("elements", [])] + 
                              [elem.get("to_category", "") for elem in storyline.get("elements", [])]
        }
        memos.append(storyline_memo)
    
    # 理论框架备忘录
    if theory_framework:
        theory_memo = {
            "type": "theory_framework_memo",
            "title": "理论框架整合备忘录",
            "content": f"整合了包含 {len(theory_framework.get('propositions', []))} 个命题的理论框架，确立了以 {theory_framework.get('core_category', {}).get('name', 'Unknown')} 为核心的概念体系。",
            "date": "2025-12-27",
            "related_elements": [theory_framework.get("core_category", {}).get("id", "")]
        }
        memos.append(theory_memo)
    
    return memos