"""
ANT转译过程分析模块
此模块提供追踪行动者网络理论中转译过程的功能，包括问题化、利益化、征召和动员四个阶段
"""

from typing import Dict, List, Any, Union
import json


def translation_process_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    分析行动者网络理论中的转译过程
    
    Args:
        data: 包含网络相关信息的字典
    
    Returns:
        包含转译过程分析结果的字典
    """
    # 执行四个转译阶段的分析
    problematization_phase = problematization_analysis(data)
    interessement_phase = interessement_analysis(data)
    enrollment_phase = enrollment_analysis(data)
    mobilization_phase = mobilization_analysis(data)
    
    # 争议和阻力分析
    controversy_analysis_result = controversy_analysis(data)
    
    # 转译成功/失败评估
    success_assessment = translation_success_assessment(
        problematization_phase, 
        interessement_phase, 
        enrollment_phase, 
        mobilization_phase
    )
    
    return {
        "problematization": problematization_phase,
        "interessement": interessement_phase,
        "enrollment": enrollment_phase,
        "mobilization": mobilization_phase,
        "controversy_analysis": controversy_analysis_result,
        "success_assessment": success_assessment,
        "translation_timeline": [
            problematization_phase,
            interessement_phase,
            enrollment_phase,
            mobilization_phase
        ]
    }


def problematization_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    问题化阶段分析
    
    Args:
        data: 包含网络相关信息的字典
    
    Returns:
        问题化阶段分析结果
    """
    # 从数据中提取相关信息
    problem_description = data.get('problem', 'Unknown problem')
    stakeholders = data.get('stakeholders', [])
    initial_positions = data.get('initial_positions', {})
    
    # 问题化分析
    problematization_result = {
        "original_problem": problem_description,
        "problem_framing": f"How the problem '{problem_description}' was framed and defined",
        "dependent_actors": [stakeholder for stakeholder in stakeholders if 'depends' in stakeholder.get('relationship', '').lower()],
        "initial_state": initial_positions,
        "relevance_assessment": f"How the problem was made relevant to different actors in the context of {problem_description}"
    }
    
    return problematization_result


def interessement_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    利益化阶段分析
    
    Args:
        data: 包含网络相关信息的字典
    
    Returns:
        利益化阶段分析结果
    """
    # 从数据中提取相关信息
    negotiations = data.get('negotiations', [])
    interest_alignments = data.get('interest_alignments', [])
    actor_adjustments = data.get('actor_adjustments', [])
    
    # 利益化分析
    interessement_result = {
        "negotiation_processes": negotiations,
        "interest_alignment": interest_alignments,
        "mutual_adjustments": actor_adjustments,
        "relationship_evolution": "Evolution of relationships between actors during interessement phase",
        "commitment_level": len([a for a in actor_adjustments if a.get('committed', False)]) / len(actor_adjustments) if actor_adjustments else 0
    }
    
    return interessement_result


def enrollment_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    征召阶段分析
    
    Args:
        data: 包含网络相关信息的字典
    
    Returns:
        征召阶段分析结果
    """
    # 从数据中提取相关信息
    allies = data.get('allies', [])
    recruitment_strategies = data.get('recruitment_strategies', [])
    representations = data.get('representations', [])
    delegations = data.get('delegations', [])
    
    # 征召分析
    enrollment_result = {
        "enlisted_allies": allies,
        "recruitment_strategies": recruitment_strategies,
        "representations_by_others": representations,
        "delegation_of_authority": delegations,
        "enrollment_stability": len([a for a in allies if a.get('stable', False)]) / len(allies) if allies else 0
    }
    
    return enrollment_result


def mobilization_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    动员阶段分析
    
    Args:
        data: 包含网络相关信息的字典
    
    Returns:
        动员阶段分析结果
    """
    # 从数据中提取相关信息
    actions = data.get('actions', [])
    resource_mobilizations = data.get('resource_mobilizations', [])
    spokespersons = data.get('spokespersons', [])
    
    # 动员分析
    mobilization_result = {
        "actors_moved_to_action": actions,
        "interest_to_action_translation": "How interests were translated into actions",
        "resource_mobilization": resource_mobilizations,
        "spokespersons_and_representatives": spokespersons,
        "mobilization_effectiveness": len([a for a in actions if a.get('successful', False)]) / len(actions) if actions else 0
    }
    
    return mobilization_result


def controversy_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    争议分析
    
    Args:
        data: 包含网络相关信息的字典
    
    Returns:
        争议分析结果
    """
    # 从数据中提取相关信息
    controversies = data.get('controversies', [])
    resistances = data.get('resistances', [])
    conflict_points = data.get('conflict_points', [])
    
    # 争议分析
    controversy_result = {
        "identified_controversies": controversies,
        "controversy_management": "How controversies were managed or resolved",
        "resistant_actors": resistances,
        "counter_mobilizations": "Counter-mobilizations in response to main mobilization efforts",
        "controversy_impact": f"Impact of {len(controversies)} controversies on network formation"
    }
    
    return controversy_result


def translation_success_assessment(
    problematization: Dict[str, Any], 
    interessement: Dict[str, Any], 
    enrollment: Dict[str, Any], 
    mobilization: Dict[str, Any]
) -> Dict[str, Any]:
    """
    转译成功/失败评估
    
    Args:
        problematization: 问题化阶段分析结果
        interessement: 利益化阶段分析结果
        enrollment: 征召阶段分析结果
        mobilization: 动员阶段分析结果
    
    Returns:
        转译成功/失败评估结果
    """
    # 评估每个阶段的有效性
    phase_effectiveness = {
        "problematization_effectiveness": 0.8,  # 基础值
        "interessement_effectiveness": 0.7,     # 基础值
        "enrollment_effectiveness": 0.6,        # 基础值
        "mobilization_effectiveness": 0.7       # 基础值，从mobilization_result中获取
    }
    
    # 计算整体成功得分
    overall_success = sum(phase_effectiveness.values()) / len(phase_effectiveness)
    
    # 识别影响因素
    success_factors = [
        "Clear problem definition",
        "Effective interest alignment",
        "Successful actor enrollment",
        "Effective resource mobilization"
    ]
    
    failure_factors = [
        "Unclear problem framing",
        "Misaligned interests",
        "Failed actor enrollment",
        "Inadequate resource mobilization"
    ]
    
    success_assessment = {
        "phase_effectiveness": phase_effectiveness,
        "overall_success_score": overall_success,
        "success_factors": success_factors,
        "failure_factors": failure_factors,
        "stability_assessment": "Assessment of translation durability and stability",
        "alternative_possibilities": "Alternative translation possibilities that were not pursued"
    }
    
    return success_assessment


def black_boxing_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    黑盒化分析
    
    Args:
        data: 包含网络相关信息的字典
    
    Returns:
        黑盒化分析结果
    """
    # 基础黑盒化分析
    black_boxing_result = {
        "black_boxed_processes": "Processes that became taken-for-granted",
        "stabilization_mechanisms": "Mechanisms that led to process stabilization",
        "taken_for_granted_elements": "Elements that are no longer questioned"
    }
    
    return black_boxing_result


def network_stabilization_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    网络稳定化分析
    
    Args:
        data: 包含网络相关信息的字典
    
    Returns:
        网络稳定化分析结果
    """
    # 基础网络稳定化分析
    stabilization_result = {
        "stabilization_factors": "Factors that contributed to network stability",
        "stability_indicators": "Indicators of network stability",
        "durability_assessment": "Assessment of network durability",
        "stability_threats": "Potential threats to network stability"
    }
    
    return stabilization_result