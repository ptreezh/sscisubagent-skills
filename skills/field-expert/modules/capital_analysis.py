"""
场域资本分析模块
此模块提供分析社会场域中各种资本类型、分布、转换和竞争的功能
"""

from typing import Dict, List, Any
import json


def field_capital_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析社会场域中的各种资本类型、分布、转换和竞争
    
    Args:
        data: 包含场域相关信息的字典
    
    Returns:
        包含资本分析结果的字典
    """
    # 从数据中提取相关信息
    actors = data.get('actors', [])
    capital_distributions = data.get('capital_distributions', {})
    conversion_mechanisms = data.get('conversion_mechanisms', [])
    competition_instances = data.get('competition_instances', [])
    
    # 执行资本分析
    capital_identification = identify_capital_types(data)
    distribution_mapping = map_capital_distribution(actors, capital_distributions)
    competition_analysis = analyze_capital_competition(competition_instances)
    conversion_analysis = analyze_conversion_mechanisms(conversion_mechanisms)
    inequality_analysis = analyze_capital_inequality(capital_distributions)
    legitimacy_analysis = analyze_legitimacy_processes(data)
    power_analysis = analyze_power_relations(actors, capital_distributions)
    reproduction_analysis = analyze_reproduction_mechanisms(data)
    
    return {
        "capital_identification": capital_identification,
        "distribution_mapping": distribution_mapping,
        "competition_analysis": competition_analysis,
        "conversion_analysis": conversion_analysis,
        "inequality_analysis": inequality_analysis,
        "legitimacy_analysis": legitimacy_analysis,
        "power_analysis": power_analysis,
        "reproduction_analysis": reproduction_analysis
    }


def identify_capital_types(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    识别场域中被重视的资本类型
    
    Args:
        data: 包含场域信息的字典
    
    Returns:
        资本类型识别结果
    """
    # 识别各种资本类型
    capital_types = {
        "economic_capital": {
            "description": "金钱、财产、金融资源",
            "examples": data.get('economic_capital_examples', []),
            "value_in_field": data.get('economic_capital_value', 'high')
        },
        "social_capital": {
            "description": "网络、关系、社会连接",
            "examples": data.get('social_capital_examples', []),
            "value_in_field": data.get('social_capital_value', 'medium')
        },
        "cultural_capital": {
            "description": "知识、文凭、文化商品",
            "examples": data.get('cultural_capital_examples', []),
            "value_in_field": data.get('cultural_capital_value', 'high')
        },
        "symbolic_capital": {
            "description": "声望、认可、荣誉",
            "examples": data.get('symbolic_capital_examples', []),
            "value_in_field": data.get('symbolic_capital_value', 'high')
        }
    }
    
    # 识别场域特定的资本形式
    field_specific_capitals = data.get('field_specific_capitals', [])
    
    return {
        "general_capital_types": capital_types,
        "field_specific_capitals": field_specific_capitals,
        "relative_values": {
            "economic": data.get('economic_capital_value', 'high'),
            "social": data.get('social_capital_value', 'medium'),
            "cultural": data.get('cultural_capital_value', 'high'),
            "symbolic": data.get('symbolic_capital_value', 'high')
        }
    }


def map_capital_distribution(actors: List[Dict[str, Any]], capital_distributions: Dict[str, Any]) -> Dict[str, Any]:
    """
    映射资本在行动者之间的分布
    
    Args:
        actors: 行动者列表
        capital_distributions: 资本分布字典
    
    Returns:
        资本分布映射结果
    """
    distribution_map = {}
    
    # 为每个行动者映射其拥有的资本
    for actor in actors:
        actor_id = actor.get('id', actor.get('name', 'unknown'))
        distribution_map[actor_id] = {
            "economic": capital_distributions.get(actor_id, {}).get('economic', 0),
            "social": capital_distributions.get(actor_id, {}).get('social', 0),
            "cultural": capital_distributions.get(actor_id, {}).get('cultural', 0),
            "symbolic": capital_distributions.get(actor_id, {}).get('symbolic', 0)
        }
    
    # 分析资本集中或分散情况
    concentration_analysis = analyze_concentration(distribution_map)
    
    return {
        "actor_capital_map": distribution_map,
        "concentration_analysis": concentration_analysis,
        "high_low_holders": identify_high_low_holders(distribution_map),
        "capital_correlations": calculate_capital_correlations(distribution_map)
    }


def analyze_concentration(distribution_map: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析资本集中情况
    
    Args:
        distribution_map: 资本分布映射
    
    Returns:
        集中度分析结果
    """
    capital_types = ['economic', 'social', 'cultural', 'symbolic']
    concentration_results = {}
    
    for cap_type in capital_types:
        values = [actor_caps[cap_type] for actor_caps in distribution_map.values()]
        if values:
            avg = sum(values) / len(values)
            max_val = max(values)
            min_val = min(values)
            
            # 计算基尼系数的简化版本
            concentration = (max_val - min_val) / (max_val + min_val) if (max_val + min_val) != 0 else 0
            
            concentration_results[cap_type] = {
                "average": avg,
                "max": max_val,
                "min": min_val,
                "concentration_index": concentration
            }
    
    return concentration_results


def identify_high_low_holders(distribution_map: Dict[str, Any]) -> Dict[str, Any]:
    """
    识别高低资本持有者
    
    Args:
        distribution_map: 资本分布映射
    
    Returns:
        高低资本持有者识别结果
    """
    capital_types = ['economic', 'social', 'cultural', 'symbolic']
    high_low_holders = {
        "high_holders": {},
        "low_holders": {}
    }
    
    for cap_type in capital_types:
        # 按资本类型排序
        sorted_actors = sorted(
            distribution_map.items(),
            key=lambda x: x[1][cap_type],
            reverse=True
        )
        
        # 前20%为高持有者，后20%为低持有者
        num_actors = len(sorted_actors)
        high_count = max(1, int(num_actors * 0.2))
        low_count = max(1, int(num_actors * 0.2))
        
        high_holders = [actor[0] for actor in sorted_actors[:high_count]]
        low_holders = [actor[0] for actor in sorted_actors[-low_count:]]
        
        high_low_holders["high_holders"][cap_type] = high_holders
        high_low_holders["low_holders"][cap_type] = low_holders
    
    return high_low_holders


def calculate_capital_correlations(distribution_map: Dict[str, Any]) -> Dict[str, Any]:
    """
    计算资本类型之间的相关性
    
    Args:
        distribution_map: 资本分布映射
    
    Returns:
        资本相关性计算结果
    """
    # 基础相关性计算（简化版本）
    return {
        "economic_social": 0.5,  # 示例值
        "economic_cultural": 0.3,
        "social_cultural": 0.4,
        "symbolic_other": 0.6
    }


def analyze_capital_competition(competition_instances: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析资本竞争
    
    Args:
        competition_instances: 竞争实例列表
    
    Returns:
        资本竞争分析结果
    """
    competition_analysis = {
        "competition_types": [],
        "actors_involved": set(),
        "stakes_identified": set(),
        "strategies_used": set(),
        "alliances_oppotions": {}
    }
    
    for competition in competition_instances:
        comp_type = competition.get('type', 'unknown')
        competition_analysis["competition_types"].append(comp_type)
        
        actors = competition.get('actors', [])
        competition_analysis["actors_involved"].update(actors)
        
        stakes = competition.get('stakes', [])
        competition_analysis["stakes_identified"].update(stakes)
        
        strategy = competition.get('strategy', 'unknown')
        competition_analysis["strategies_used"].add(strategy)
        
        # 记录联盟和对立关系
        if 'allies' in competition and 'opponents' in competition:
            competition_analysis["alliances_oppotions"][comp_type] = {
                "allies": competition['allies'],
                "opponents": competition['opponents']
            }
    
    # 转换为列表以确保JSON序列化
    competition_analysis["actors_involved"] = list(competition_analysis["actors_involved"])
    competition_analysis["stakes_identified"] = list(competition_analysis["stakes_identified"])
    competition_analysis["strategies_used"] = list(competition_analysis["strategies_used"])
    
    return competition_analysis


def analyze_conversion_mechanisms(conversion_mechanisms: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析资本转换机制
    
    Args:
        conversion_mechanisms: 转换机制列表
    
    Returns:
        转换机制分析结果
    """
    conversion_analysis = {
        "mechanisms_identified": conversion_mechanisms,
        "conditions_for_conversion": [],
        "conversion_efficiency": {},
        "obstacles_to_conversion": [],
        "conversion_rates": {}
    }
    
    for mechanism in conversion_mechanisms:
        condition = mechanism.get('condition', 'unknown')
        conversion_analysis["conditions_for_conversion"].append(condition)
        
        efficiency = mechanism.get('efficiency', 'medium')
        source_cap = mechanism.get('source_capital', 'unknown')
        target_cap = mechanism.get('target_capital', 'unknown')
        conversion_analysis["conversion_efficiency"][f"{source_cap}_to_{target_cap}"] = efficiency
        
        obstacle = mechanism.get('obstacle', 'none')
        if obstacle != 'none':
            conversion_analysis["obstacles_to_conversion"].append(obstacle)
        
        rate = mechanism.get('rate', 'standard')
        conversion_analysis["conversion_rates"][f"{source_cap}_to_{target_cap}"] = rate
    
    return conversion_analysis


def analyze_capital_inequality(capital_distributions: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析资本不平等
    
    Args:
        capital_distributions: 资本分布字典
    
    Returns:
        资本不平等分析结果
    """
    inequality_analysis = {
        "inequality_levels": {},
        "causes_identified": [],
        "consequences_analyzed": [],
        "effects_on_field_dynamics": [],
        "reproduction_of_inequalities": []
    }
    
    # 计算每种资本类型的不平等程度
    capital_types = ['economic', 'social', 'cultural', 'symbolic']
    
    for cap_type in capital_types:
        values = [actor_dist.get(cap_type, 0) for actor_dist in capital_distributions.values()]
        if values:
            # 简化的不平等指标（基于极值比率）
            max_val = max(values)
            min_val = min(values) if min(values) > 0 else 1  # 避免除以零
            inequality_ratio = max_val / min_val if min_val != 0 else float('inf')
            
            inequality_analysis["inequality_levels"][cap_type] = {
                "ratio": inequality_ratio,
                "max_value": max_val,
                "min_value": min_val
            }
    
    return inequality_analysis


def analyze_legitimacy_processes(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析合法性过程
    
    Args:
        data: 包含场域信息的字典
    
    Returns:
        合法性过程分析结果
    """
    return {
        "legitimacy_processes": data.get('legitimacy_processes', []),
        "recognition_processes": data.get('recognition_processes', []),
        "challenges_to_legitimacy": data.get('challenges_to_legitimacy', []),
        "authorities_legitimizing_capitals": data.get('authorities', []),
        "symbolic_struggles_over_recognition": data.get('symbolic_struggles', [])
    }


def analyze_power_relations(actors: List[Dict[str, Any]], capital_distributions: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析权力关系
    
    Args:
        actors: 行动者列表
        capital_distributions: 资本分布字典
    
    Returns:
        权力关系分析结果
    """
    power_analysis = {
        "capital_power_correlation": {},
        "authority_connections": [],
        "capital_based_power_mechanisms": [],
        "resistance_to_capital_power": [],
        "power_relation_transformations": []
    }
    
    # 简化的资本-权力关系分析
    for actor in actors:
        actor_id = actor.get('id', actor.get('name', 'unknown'))
        if actor_id in capital_distributions:
            total_capital = sum(capital_distributions[actor_id].values())
            # 假设总资本与权力正相关
            power_analysis["capital_power_correlation"][actor_id] = total_capital
    
    return power_analysis


def analyze_reproduction_mechanisms(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析再生产机制
    
    Args:
        data: 包含场域信息的字典
    
    Returns:
        再生产机制分析结果
    """
    return {
        "reproduction_mechanisms": data.get('reproduction_mechanisms', []),
        "transmission_across_generations": data.get('transmission_mechanisms', []),
        "institutional_support": data.get('institutional_support', []),
        "challenges_to_reproduction": data.get('reproduction_challenges', []),
        "evolution_of_patterns": data.get('evolution_patterns', [])
    }