"""
场域边界分析模块
此模块提供识别和分析社会场域边界的各项功能
"""

from typing import Dict, List, Any
import json


def field_boundary_identification(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    识别和分析社会场域的边界、范围和排除机制
    
    Args:
        data: 包含场域相关信息的字典
    
    Returns:
        包含边界识别结果的字典
    """
    # 从数据中提取相关信息
    field_type = data.get('field_type', 'unknown')
    actors = data.get('actors', [])
    rules = data.get('rules', [])
    external_forces = data.get('external_forces', [])
    
    # 执行边界识别分析
    field_definition = define_field(data)
    boundary_mapping = map_boundaries(data)
    inclusion_analysis = analyze_inclusion_mechanisms(actors, rules)
    exclusion_analysis = analyze_exclusion_mechanisms(actors, rules)
    autonomy_assessment = assess_autonomy(external_forces, field_type)
    
    return {
        "field_definition": field_definition,
        "boundaries": boundary_mapping,
        "inclusion_mechanisms": inclusion_analysis,
        "exclusion_mechanisms": exclusion_analysis,
        "rules_logic": rules,
        "autonomy_assessment": autonomy_assessment,
        "multi_field_relations": analyze_multi_field_relations(data)
    }


def define_field(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    定义分析场域
    
    Args:
        data: 包含场域信息的字典
    
    Returns:
        场域定义结果
    """
    field_type = data.get('field_type', 'unknown')
    context = data.get('context', {})
    
    return {
        "field_type": field_type,
        "historical_context": context.get('historical', ''),
        "geographical_context": context.get('geographical', ''),
        "time_frame": data.get('time_frame', 'synchronic'),
        "key_actors": data.get('actors', [])[:5]  # 仅显示前5个关键行动者
    }


def map_boundaries(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    绘制场域边界
    
    Args:
        data: 包含场域信息的字典
    
    Returns:
        边界映射结果
    """
    boundaries = {
        "spatial_boundaries": data.get('spatial_boundaries', []),
        "conceptual_boundaries": data.get('conceptual_boundaries', []),
        "institutional_boundaries": data.get('institutional_boundaries', []),
        "symbolic_boundaries": data.get('symbolic_boundaries', []),
        "temporal_boundaries": data.get('temporal_boundaries', [])
    }
    
    return boundaries


def analyze_inclusion_mechanisms(actors: List[Dict[str, Any]], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析包含机制
    
    Args:
        actors: 行动者列表
        rules: 规则列表
    
    Returns:
        包含机制分析结果
    """
    inclusion_mechanisms = {
        "membership_criteria": [],
        "entry_processes": [],
        "required_resources": [],
        "membership_paths": []
    }
    
    # 基础包含机制分析
    for rule in rules:
        if 'inclusion' in rule.get('type', '').lower():
            inclusion_mechanisms["membership_criteria"].append(rule)
    
    for actor in actors:
        if actor.get('status') == 'member':
            inclusion_mechanisms["membership_paths"].append({
                "actor": actor.get('name'),
                "path": actor.get('entry_path', 'unknown')
            })
    
    return inclusion_mechanisms


def analyze_exclusion_mechanisms(actors: List[Dict[str, Any]], rules: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析排除机制
    
    Args:
        actors: 行动者列表
        rules: 规则列表
    
    Returns:
        排除机制分析结果
    """
    exclusion_mechanisms = {
        "entry_barriers": [],
        "exclusion_forms": [],
        "effects_on_excluded": [],
        "consequences_for_field": []
    }
    
    # 基础排除机制分析
    for rule in rules:
        if 'exclusion' in rule.get('type', '').lower():
            exclusion_mechanisms["entry_barriers"].append(rule)
    
    for actor in actors:
        if actor.get('status') == 'excluded':
            exclusion_mechanisms["exclusion_forms"].append({
                "actor": actor.get('name'),
                "reason": actor.get('exclusion_reason', 'unknown')
            })
    
    return exclusion_mechanisms


def assess_autonomy(external_forces: List[Dict[str, Any]], field_type: str) -> Dict[str, Any]:
    """
    评估场域自主性
    
    Args:
        external_forces: 外部力量列表
        field_type: 场域类型
    
    Returns:
        自主性评估结果
    """
    # 基础自主性评估
    autonomy_score = calculate_autonomy_score(external_forces, field_type)
    
    return {
        "autonomy_score": autonomy_score,
        "external_influences": external_forces,
        "field_specific_logic": f"Logic specific to {field_type} field",
        "symbolic_violence_mechanisms": ["Mechanism 1", "Mechanism 2"],  # 基础示例
        "historical_development": "Historical development of autonomy"
    }


def calculate_autonomy_score(external_forces: List[Dict[str, Any]], field_type: str) -> float:
    """
    计算自主性得分
    
    Args:
        external_forces: 外部力量列表
        field_type: 场域类型
    
    Returns:
        自主性得分（0-1之间的浮点数）
    """
    # 基础自主性计算逻辑
    # 外部力量越多，自主性越低
    max_forces = 10  # 假设最大外部力量数
    force_count = len(external_forces)
    
    # 计算自主性得分（外部力量越少，自主性越高）
    autonomy_score = 1.0 - (force_count / max_forces)
    autonomy_score = max(0.0, min(1.0, autonomy_score))  # 限制在0-1之间
    
    return autonomy_score


def analyze_multi_field_relations(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析多场域关系
    
    Args:
        data: 包含场域信息的字典
    
    Returns:
        多场域关系分析结果
    """
    return {
        "adjacent_fields": data.get('adjacent_fields', []),
        "boundary_interactions": "Interactions at field boundaries",
        "influence_on_boundary_maintenance": "Influence of adjacent fields on boundary maintenance",
        "dependency_relations": "Dependency relations between fields",
        "boundary_stability_impact": "Impact of field relations on boundary stability"
    }


def analyze_boundary_dynamics(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析边界动态
    
    Args:
        data: 包含场域信息的字典
    
    Returns:
        边界动态分析结果
    """
    return {
        "boundary_evolution_timeline": "Timeline of boundary evolution",
        "controversy_moments": "Moments of boundary controversy",
        "change_processes": "Processes of boundary change",
        "driving_factors": "Factors driving boundary changes",
        "change_consequences": "Consequences of boundary changes"
    }