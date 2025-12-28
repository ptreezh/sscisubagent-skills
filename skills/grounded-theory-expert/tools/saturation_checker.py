"""
理论饱和度检验模块
此模块提供扎根理论饱和度检验的各项功能
"""

from typing import Dict, List, Any
import json


def saturation_check(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    执行扎根理论的饱和度检验
    
    Args:
        data: 包含理论构建结果的数据字典
    
    Returns:
        包含饱和度检验结果的字典
    """
    # 从数据中提取理论构建结果
    existing_theory = data.get('existing_theory', {})
    new_data = data.get('new_data', [])
    
    # 执行概念饱和评估
    concept_saturation = assess_concept_saturation(existing_theory, new_data)
    
    # 执行范畴饱和评估
    category_saturation = assess_category_saturation(existing_theory)
    
    # 执行关系饱和评估
    relationship_saturation = assess_relationship_saturation(existing_theory)
    
    # 执行理论饱和评估
    theory_saturation = assess_theory_saturation(existing_theory)
    
    # 综合判断饱和度
    overall_saturation = determine_overall_saturation(
        concept_saturation, 
        category_saturation, 
        relationship_saturation, 
        theory_saturation
    )
    
    # 返回饱和度检验结果
    return {
        "concept_saturation": concept_saturation,
        "category_saturation": category_saturation,
        "relationship_saturation": relationship_saturation,
        "theory_saturation": theory_saturation,
        "overall_saturation": overall_saturation,
        "saturation_assessment": {
            "saturation_level": overall_saturation["level"],
            "confidence_level": overall_saturation["confidence"],
            "emerging_rate": concept_saturation.get("new_concepts_rate", 0),
            "development_score": category_saturation.get("completeness_score", 0)
        },
        "recommendations": generate_recommendations(overall_saturation, concept_saturation)
    }


def assess_concept_saturation(existing_theory: Dict[str, Any], new_data: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    评估概念饱和度
    
    Args:
        existing_theory: 现有理论
        new_data: 新数据
    
    Returns:
        概念饱和度评估结果
    """
    # 分析新数据中是否出现新概念
    existing_concepts = set()
    if 'open_coding' in existing_theory and 'concepts' in existing_theory['open_coding']:
        for concept in existing_theory['open_coding']['concepts']:
            existing_concepts.add(concept.get('code', '').lower())
    
    # 在新数据中识别概念（简化处理）
    new_concepts_found = 0
    total_new_segments = len(new_data) if new_data else 1  # 避免除零错误
    
    # 简化的概念识别
    for item in new_data:
        text = item.get('text', '') if isinstance(item, dict) else str(item)
        # 模拟概念提取
        words = text.split()
        for word in words[:3]:  # 只检查前3个词
            if word.lower() not in existing_concepts:
                new_concepts_found += 1
                existing_concepts.add(word.lower())
    
    # 计算新概念出现率
    new_concepts_rate = new_concepts_found / max(1, total_new_segments)
    
    # 评估概念饱和度
    if new_concepts_rate < 0.05:
        level = "high"
        judgment = "新概念出现率低，概念层面已达到饱和"
    elif new_concepts_rate < 0.15:
        level = "medium"
        judgment = "新概念出现率中等，概念层面接近饱和"
    else:
        level = "low"
        judgment = "新概念持续出现，概念层面未饱和"
    
    return {
        "new_concepts_found": new_concepts_found,
        "total_new_segments": total_new_segments,
        "new_concepts_rate": new_concepts_rate,
        "saturation_level": level,
        "judgment": judgment,
        "significance_assessment": "根据新概念出现率评估概念饱和度"
    }


def assess_category_saturation(existing_theory: Dict[str, Any]) -> Dict[str, Any]:
    """
    评估范畴饱和度
    
    Args:
        existing_theory: 现有理论
    
    Returns:
        范畴饱和度评估结果
    """
    categories = []
    if 'axial_coding' in existing_theory and 'categories' in existing_theory['axial_coding']:
        categories = existing_theory['axial_coding']['categories']
    
    # 评估范畴属性和维度的完整性
    total_categories = len(categories)
    avg_concepts_per_category = 0
    avg_attributes_per_category = 0
    
    if total_categories > 0:
        total_concepts = sum(len(cat.get('concepts', [])) for cat in categories)
        avg_concepts_per_category = total_concepts / total_categories
        
        # 计算属性完整性（简化）
        avg_attributes = sum(len(cat.get('properties', {})) for cat in categories)
        avg_attributes_per_category = avg_attributes / total_categories
    
    # 评估范畴饱和度
    if avg_concepts_per_category > 5 and avg_attributes_per_category > 3:
        completeness_level = "high"
        judgment = "范畴属性和维度发展充分，范畴层面达到饱和"
    elif avg_concepts_per_category > 2 and avg_attributes_per_category > 1:
        completeness_level = "medium"
        judgment = "范畴属性和维度发展一般，范畴层面接近饱和"
    else:
        completeness_level = "low"
        judgment = "范畴属性和维度发展不足，范畴层面未饱和"
    
    completeness_score = min(1.0, (avg_concepts_per_category / 10) * 0.6 + (avg_attributes_per_category / 5) * 0.4)
    
    return {
        "total_categories": total_categories,
        "avg_concepts_per_category": avg_concepts_per_category,
        "avg_attributes_per_category": avg_attributes_per_category,
        "completeness_score": completeness_score,
        "completeness_level": completeness_level,
        "judgment": judgment
    }


def assess_relationship_saturation(existing_theory: Dict[str, Any]) -> Dict[str, Any]:
    """
    评估关系饱和度
    
    Args:
        existing_theory: 现有理论
    
    Returns:
        关系饱和度评估结果
    """
    relationships = []
    if 'axial_coding' in existing_theory and 'relationships' in existing_theory['axial_coding']:
        relationships = existing_theory['axial_coding']['relationships']
    
    # 评估关系网络的稳定性
    total_relationships = len(relationships)
    avg_strength = 0
    
    if total_relationships > 0:
        total_strength = sum(rel.get('strength', 0) for rel in relationships)
        avg_strength = total_strength / total_relationships
    
    # 评估关系饱和度
    if total_relationships > 8 and avg_strength > 0.6:
        stability_level = "high"
        judgment = "关系网络稳定且完整，关系层面达到饱和"
    elif total_relationships > 4 and avg_strength > 0.4:
        stability_level = "medium"
        judgment = "关系网络基本稳定，关系层面接近饱和"
    else:
        stability_level = "low"
        judgment = "关系网络不稳定或不完整，关系层面未饱和"
    
    stability_score = min(1.0, (total_relationships / 15) * 0.7 + (avg_strength) * 0.3)
    
    return {
        "total_relationships": total_relationships,
        "avg_strength": avg_strength,
        "stability_score": stability_score,
        "stability_level": stability_level,
        "judgment": judgment
    }


def assess_theory_saturation(existing_theory: Dict[str, Any]) -> Dict[str, Any]:
    """
    评估理论饱和度
    
    Args:
        existing_theory: 现有理论
    
    Returns:
        理论饱和度评估结果
    """
    # 检查理论的解释覆盖度
    propositions_count = 0
    if 'selective_coding' in existing_theory and 'theory_framework' in existing_theory['selective_coding']:
        if 'propositions' in existing_theory['selective_coding']['theory_framework']:
            propositions_count = len(existing_theory['selective_coding']['theory_framework']['propositions'])
    
    # 评估理论一致性
    conceptual_framework_exists = 'conceptual_framework' in existing_theory.get('selective_coding', {}).get('theory_framework', {})
    core_category_exists = 'core_category' in existing_theory.get('selective_coding', {})
    
    # 评估理论饱和度
    if propositions_count >= 5 and conceptual_framework_exists and core_category_exists:
        coverage_level = "high"
        judgment = "理论能解释大部分重要现象，理论层面达到饱和"
    elif propositions_count >= 3 and (conceptual_framework_exists or core_category_exists):
        coverage_level = "medium"
        judgment = "理论能解释一些重要现象，理论层面接近饱和"
    else:
        coverage_level = "low"
        judgment = "理论解释力不足，理论层面未饱和"
    
    coverage_score = min(1.0, (propositions_count / 10) * 0.5 + (0.5 if conceptual_framework_exists else 0) + (0.3 if core_category_exists else 0))
    
    return {
        "propositions_count": propositions_count,
        "conceptual_framework_exists": conceptual_framework_exists,
        "core_category_exists": core_category_exists,
        "coverage_score": coverage_score,
        "coverage_level": coverage_level,
        "judgment": judgment
    }


def determine_overall_saturation(
    concept_sat: Dict[str, Any], 
    category_sat: Dict[str, Any], 
    relationship_sat: Dict[str, Any], 
    theory_sat: Dict[str, Any]
) -> Dict[str, Any]:
    """
    确定总体饱和度
    
    Args:
        concept_sat: 概念饱和度
        category_sat: 范畴饱和度
        relationship_sat: 关系饱和度
        theory_sat: 理论饱和度
    
    Returns:
        总体饱和度判断
    """
    # 计算综合饱和度分数
    concept_score = 1.0 if concept_sat["saturation_level"] == "high" else 0.5 if concept_sat["saturation_level"] == "medium" else 0.0
    category_score = category_sat["completeness_score"]
    relationship_score = relationship_sat["stability_score"]
    theory_score = theory_sat["coverage_score"]
    
    # 加权平均（可以调整权重）
    overall_score = (
        concept_score * 0.25 + 
        category_score * 0.25 + 
        relationship_score * 0.25 + 
        theory_score * 0.25
    )
    
    # 确定饱和度等级
    if overall_score >= 0.8:
        level = "fully_saturated"
        confidence = 0.9
        judgment = "理论在所有层面都达到饱和，可以结束数据收集"
    elif overall_score >= 0.6:
        level = "partially_saturated"
        confidence = 0.7
        judgment = "理论在多数层面接近饱和，可考虑结束数据收集"
    else:
        level = "not_saturated"
        confidence = 0.5
        judgment = "理论在多个层面未饱和，需要继续收集数据"
    
    return {
        "level": level,
        "score": overall_score,
        "confidence": confidence,
        "judgment": judgment,
        "component_scores": {
            "concept": concept_score,
            "category": category_score,
            "relationship": relationship_score,
            "theory": theory_score
        }
    }


def generate_recommendations(overall_saturation: Dict[str, Any], concept_saturation: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成建议
    
    Args:
        overall_saturation: 总体饱和度
        concept_saturation: 概念饱和度
    
    Returns:
        建议内容
    """
    level = overall_saturation["level"]
    
    if level == "fully_saturated":
        continue_collection = False
        focus_areas = ["理论完善", "验证研究"]
        next_steps = ["完成理论构建", "撰写研究报告", "准备验证研究"]
    elif level == "partially_saturated":
        continue_collection = False  # 在这种情况下也可能停止
        focus_areas = ["理论微调", "概念精炼"]
        next_steps = ["完成理论构建", "进行理论验证", "撰写部分报告"]
    else:
        continue_collection = True
        focus_areas = ["继续数据收集", "概念探索"]
        next_steps = ["收集更多数据", "进行额外编码", "重新评估饱和度"]
    
    return {
        "continue_data_collection": continue_collection,
        "focus_areas": focus_areas,
        "next_steps": next_steps,
        "confidence_level": overall_saturation["confidence"],
        "rationale": overall_saturation["judgment"]
    }