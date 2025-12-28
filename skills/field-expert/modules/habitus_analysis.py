"""
场域习性分析模块
此模块提供分析社会场域中行动者习性模式的功能
"""

from typing import Dict, List, Any
import json


def field_habitus_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析社会场域中行动者的习性模式
    
    Args:
        data: 包含场域相关信息的字典
    
    Returns:
        包含习性分析结果的字典
    """
    # 从数据中提取相关信息
    actors = data.get('actors', [])
    practices = data.get('practices', [])
    field_structure = data.get('field_structure', {})
    social_conditions = data.get('social_conditions', {})
    
    # 执行习性分析
    disposition_analysis = analyze_dispositions(actors)
    embodied_knowledge_analysis = analyze_embodied_knowledge(actors)
    practice_logic_analysis = analyze_practice_logic(practices)
    structure_agency_analysis = analyze_structure_agency_relationship(actors, field_structure)
    practice_enablers_constraints = analyze_practice_enablers_constraints(actors)
    habitus_formation_analysis = analyze_habitus_formation(social_conditions)
    correspondence_analysis = assess_correspondence(actors, field_structure)
    change_adaptation_analysis = analyze_change_adaptation(actors)
    
    return {
        "disposition_analysis": disposition_analysis,
        "embodied_knowledge": embodied_knowledge_analysis,
        "practice_logic": practice_logic_analysis,
        "structure_agency_relationship": structure_agency_analysis,
        "practice_enablers_constraints": practice_enablers_constraints,
        "habitus_formation": habitus_formation_analysis,
        "correspondence_assessment": correspondence_analysis,
        "change_adaptation": change_adaptation_analysis
    }


def analyze_dispositions(actors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析行动倾向
    
    Args:
        actors: 行动者列表
    
    Returns:
        行动倾向分析结果
    """
    disposition_analysis = {
        "durable_transposable_dispositions": [],
        "generative_schemes": [],
        "cognitive_structures": [],
        "motivating_structures": [],
        "embodied_tendencies": []
    }
    
    for actor in actors:
        if 'dispositions' in actor:
            dispositions = actor['dispositions']
            disposition_analysis["durable_transposable_dispositions"].extend(dispositions.get('durable', []))
            disposition_analysis["generative_schemes"].extend(dispositions.get('generative', []))
            disposition_analysis["cognitive_structures"].extend(dispositions.get('cognitive', []))
            disposition_analysis["motivating_structures"].extend(dispositions.get('motivating', []))
            disposition_analysis["embodied_tendencies"].extend(dispositions.get('embodied', []))
    
    return disposition_analysis


def analyze_embodied_knowledge(actors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析具身体现的知识
    
    Args:
        actors: 行动者列表
    
    Returns:
        具身体现知识分析结果
    """
    embodied_knowledge_analysis = {
        "tacit_knowledge": [],
        "practical_mastery": [],
        "intuitive_understanding": [],
        "bodily_techniques": [],
        "non_verbal_aspects": []
    }
    
    for actor in actors:
        if 'embodied_knowledge' in actor:
            knowledge = actor['embodied_knowledge']
            embodied_knowledge_analysis["tacit_knowledge"].extend(knowledge.get('tacit', []))
            embodied_knowledge_analysis["practical_mastery"].extend(knowledge.get('practical_mastery', []))
            embodied_knowledge_analysis["intuitive_understanding"].extend(knowledge.get('intuitive', []))
            embodied_knowledge_analysis["bodily_techniques"].extend(knowledge.get('bodily_techniques', []))
            embodied_knowledge_analysis["non_verbal_aspects"].extend(knowledge.get('non_verbal', []))
    
    return embodied_knowledge_analysis


def analyze_practice_logic(practices: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析实践逻辑
    
    Args:
        practices: 实践列表
    
    Returns:
        实践逻辑分析结果
    """
    practice_logic_analysis = {
        "logic_transcending_rules": [],
        "creative_improvisational_aspects": [],
        "economy_of_practice": [],
        "past_present_relationship": [],
        "temporal_situational_aspects": []
    }
    
    for practice in practices:
        logic = practice.get('logic', {})
        practice_logic_analysis["logic_transcending_rules"].append(logic.get('transcends_rules', 'unknown'))
        practice_logic_analysis["creative_improvisational_aspects"].append(logic.get('creative', 'unknown'))
        practice_logic_analysis["economy_of_practice"].append(logic.get('economy', 'unknown'))
        practice_logic_analysis["past_present_relationship"].append(logic.get('past_present', 'unknown'))
        practice_logic_analysis["temporal_situational_aspects"].append(logic.get('temporal', 'unknown'))
    
    return practice_logic_analysis


def analyze_structure_agency_relationship(actors: List[Dict[str, Any]], field_structure: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析结构-能动性关系
    
    Args:
        actors: 行动者列表
        field_structure: 场域结构
    
    Returns:
        结构-能动性关系分析结果
    """
    structure_agency_analysis = {
        "habitus_incorporates_field_structure": {},
        "correspondence_between_habitus_field": {},
        "objective_conditions_subjective_dispositions": {},
        "habitus_reproduces_transforms_structure": {},
        "dialectical_relationship": {}
    }
    
    for actor in actors:
        actor_id = actor.get('id', actor.get('name', 'unknown'))
        # 简化的对应关系分析
        structure_agency_analysis["habitus_incorporates_field_structure"][actor_id] = True
        structure_agency_analysis["correspondence_between_habitus_field"][actor_id] = "high"  # 示例值
        structure_agency_analysis["objective_conditions_subjective_dispositions"][actor_id] = "matched"  # 示例值
    
    return structure_agency_analysis


def analyze_practice_enablers_constraints(actors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析实践的使能和约束因素
    
    Args:
        actors: 行动者列表
    
    Returns:
        实践使能和约束分析结果
    """
    enablers_constraints_analysis = {
        "practice_enablers": {},
        "practice_constraints": {},
        "selective_perception": {},
        "range_of_possible_actions": {},
        "creative_potential": {}
    }
    
    for actor in actors:
        actor_id = actor.get('id', actor.get('name', 'unknown'))
        # 简化的使能和约束分析
        enablers_constraints_analysis["practice_enablers"][actor_id] = actor.get('enablers', [])
        enablers_constraints_analysis["practice_constraints"][actor_id] = actor.get('constraints', [])
        enablers_constraints_analysis["range_of_possible_actions"][actor_id] = actor.get('action_range', 'broad')
        enablers_constraints_analysis["creative_potential"][actor_id] = actor.get('creative_potential', 'high')
    
    return enablers_constraints_analysis


def analyze_habitus_formation(social_conditions: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析习性形成过程
    
    Args:
        social_conditions: 社会条件
    
    Returns:
        习性形成分析结果
    """
    habitus_formation_analysis = {
        "social_origins": social_conditions.get('origins', []),
        "socialization_processes": social_conditions.get('socialization', []),
        "internalization_processes": social_conditions.get('internalization', []),
        "role_of_family_school_peers": social_conditions.get('influences', {}),
        "social_trajectory_relationship": social_conditions.get('trajectory', {}),
        "critical_life_experiences": social_conditions.get('critical_experiences', [])
    }
    
    return habitus_formation_analysis


def assess_correspondence(actors: List[Dict[str, Any]], field_structure: Dict[str, Any]) -> Dict[str, Any]:
    """
    评估对应关系
    
    Args:
        actors: 行动者列表
        field_structure: 场域结构
    
    Returns:
        对应关系评估结果
    """
    correspondence_analysis = {
        "fit_between_habitus_field": {},
        "correspondence_between_dispositions_opportunities": {},
        "selection_adaptation_processes": {},
        "habitus_field_position_relationship": {},
        "implications_for_success": {}
    }
    
    for actor in actors:
        actor_id = actor.get('id', actor.get('name', 'unknown'))
        # 简化的对应关系评估
        correspondence_analysis["fit_between_habitus_field"][actor_id] = actor.get('fit_level', 'medium')
        correspondence_analysis["implications_for_success"][actor_id] = actor.get('success_implications', 'moderate')
    
    return correspondence_analysis


def analyze_change_adaptation(actors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析变化和适应
    
    Args:
        actors: 行动者列表
    
    Returns:
        变化和适应分析结果
    """
    change_adaptation_analysis = {
        "habitus_transformation_processes": [],
        "impact_of_field_changes": [],
        "adaptation_mechanisms": [],
        "resistance_to_change": [],
        "modification_conditions": []
    }
    
    for actor in actors:
        transformations = actor.get('habitus_changes', [])
        change_adaptation_analysis["habitus_transformation_processes"].extend(transformations)
        
        resistance = actor.get('resistance_to_change', [])
        change_adaptation_analysis["resistance_to_change"].extend(resistance)
    
    return change_adaptation_analysis


def analyze_symbolic_violence(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析象征暴力
    
    Args:
        data: 包含场域信息的字典
    
    Returns:
        象征暴力分析结果
    """
    return {
        "mechanisms_of_symbolic_violence": data.get('symbolic_violence_mechanisms', []),
        "misrecognition_processes": data.get('misrecognition_processes', []),
        "power_inequality_perpetuation": data.get('power_inequality_perpetuation', []),
        "internalization_of_dominance": data.get('internalization_of_dominance', [])
    }


def analyze_cross_field_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析跨场域分析
    
    Args:
        data: 包含场域信息的字典
    
    Returns:
        跨场域分析结果
    """
    return {
        "habitus_transfer_between_fields": data.get('habitus_transfer', []),
        "field_boundary_crossings": data.get('field_boundary_crossings', []),
        "habitus_adaptation_new_fields": data.get('habitus_adaptation_new_fields', []),
        "competence_variations_fields": data.get('competence_variations_fields', [])
    }