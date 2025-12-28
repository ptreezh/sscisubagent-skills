"""
ANT参与者识别模块
此模块提供识别和分类行动者网络中各类参与者（人类和非人类）的功能
"""

from typing import Dict, List, Any, Union
import json


def participant_identification(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    识别和分类行动者网络中的各类参与者（人类和非人类）
    
    Args:
        data: 包含网络相关信息的字典
    
    Returns:
        包含参与者识别结果的字典
    """
    # 从数据中提取相关信息
    entities = data.get('entities', [])
    relationships = data.get('relationships', [])
    
    # 识别参与者
    human_actors = identify_human_actors(entities)
    non_human_actors = identify_non_human_actors(entities)
    
    # 分类参与者
    classified_actors = classify_actors(human_actors + non_human_actors)
    
    # 评估能动性
    agency_assessment = assess_agency(classified_actors)
    
    # 映射关系
    relationship_mapping = map_relationships(relationships, classified_actors)
    
    return {
        "human_actors": human_actors,
        "non_human_actors": non_human_actors,
        "classified_actors": classified_actors,
        "agency_assessment": agency_assessment,
        "relationship_mapping": relationship_mapping,
        "total_actors": len(human_actors) + len(non_human_actors)
    }


def identify_human_actors(entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    识别人类参与者
    
    Args:
        entities: 实体列表
    
    Returns:
        人类参与者列表
    """
    human_actors = []
    
    for entity in entities:
        if entity.get('type') in ['person', 'individual', 'human', 'expert', 'user', 'organization', 'group', 'community', 'movement']:
            actor = {
                "id": entity.get('id'),
                "name": entity.get('name'),
                "type": entity.get('type'),
                "role": entity.get('role', 'unknown'),
                "interests": entity.get('interests', []),
                "resources": entity.get('resources', []),
                "capabilities": entity.get('capabilities', [])
            }
            human_actors.append(actor)
    
    # 如果没有从实体中识别到人类参与者，尝试从文本中提取
    if not human_actors:
        # 基础实现：返回预定义的人类参与者类型
        human_actors = [
            {"id": "individuals", "name": "个人", "type": "person", "role": "参与者", "interests": [], "resources": [], "capabilities": []},
            {"id": "organizations", "name": "组织", "type": "organization", "role": "协调者", "interests": [], "resources": [], "capabilities": []},
            {"id": "communities", "name": "社区", "type": "community", "role": "受益者", "interests": [], "resources": [], "capabilities": []}
        ]
    
    return human_actors


def identify_non_human_actors(entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    识别非人类参与者
    
    Args:
        entities: 实体列表
    
    Returns:
        非人类参与者列表
    """
    non_human_actors = []
    
    for entity in entities:
        if entity.get('type') in ['technology', 'device', 'system', 'platform', 'material', 'resource', 'infrastructure', 'tool', 
                                  'concept', 'idea', 'framework', 'document', 'policy', 'contract', 'record', 
                                  'natural', 'environment', 'climate', 'geography', 'object']:
            actor = {
                "id": entity.get('id'),
                "name": entity.get('name'),
                "type": entity.get('type'),
                "role": entity.get('role', 'unknown'),
                "properties": entity.get('properties', {}),
                "functions": entity.get('functions', [])
            }
            non_human_actors.append(actor)
    
    # 如果没有从实体中识别到非人类参与者，尝试从文本中提取
    if not non_human_actors:
        # 基础实现：返回预定义的非人类参与者类型
        non_human_actors = [
            {"id": "technologies", "name": "技术", "type": "technology", "role": "中介", "properties": {}, "functions": ["连接", "转换"]},
            {"id": "materials", "name": "材料", "type": "material", "role": "基础", "properties": {}, "functions": ["支撑", "承载"]},
            {"id": "documents", "name": "文档", "type": "document", "role": "记录", "properties": {}, "functions": ["规范", "传达"]}
        ]
    
    return non_human_actors


def classify_actors(actors: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    """
    对参与者进行分类
    
    Args:
        actors: 参与者列表
    
    Returns:
        按类型分类的参与者字典
    """
    classification = {
        "by_agency": {"high": [], "medium": [], "low": []},
        "by_position": {"central": [], "peripheral": [], "bridging": []},
        "by_role": {"mediator": [], "intermediary": [], "translator": []},
        "by_stability": {"stable": [], "changing": [], "temporary": []}
    }
    
    # 基础分类逻辑
    for actor in actors:
        # 按能动性分类（随机分配，实际应用中应有具体逻辑）
        agency_level = "medium"  # 默认值
        classification["by_agency"][agency_level].append(actor)
        
        # 按位置分类（随机分配，实际应用中应有具体逻辑）
        position = "peripheral"  # 默认值
        classification["by_position"][position].append(actor)
        
        # 按角色分类（随机分配，实际应用中应有具体逻辑）
        role = "mediator"  # 默认值
        classification["by_role"][role].append(actor)
        
        # 按稳定性分类（随机分配，实际应用中应有具体逻辑）
        stability = "stable"  # 默认值
        classification["by_stability"][stability].append(actor)
    
    return classification


def assess_agency(actors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    评估参与者能动性
    
    Args:
        actors: 参与者列表
    
    Returns:
        能动性评估结果
    """
    agency_assessment = {}
    
    for actor in actors:
        # 检查actor是否为字典
        if isinstance(actor, dict):
            # 基础能动性评估
            agency_score = calculate_agency_score(actor)
            agency_assessment[actor.get('id', 'unknown')] = {
                "actor_name": actor.get('name', 'Unknown'),
                "agency_score": agency_score,
                "capacity_to_act": agency_score > 0.5,
                "mediation_ability": agency_score > 0.3,
                "autonomy_level": "medium"  # 基础版本
            }
        else:
            # 如果actor不是字典，跳过或处理为字符串
            continue
    
    return agency_assessment


def calculate_agency_score(actor: Dict[str, Any]) -> float:
    """
    计算参与者能动性得分
    
    Args:
        actor: 参与者信息
    
    Returns:
        能动性得分（0-1之间的浮点数）
    """
    # 检查actor是否为字典
    if not isinstance(actor, dict):
        return 0.5  # 默认值
    
    # 基础能动性计算（实际应用中应有更复杂的逻辑）
    base_score = 0.5  # 默认值
    
    # 根据参与者类型调整得分
    actor_type = actor.get('type', '')
    if actor_type in ['technology', 'system', 'platform']:
        base_score = 0.4  # 技术类参与者能动性中等
    elif actor_type in ['person', 'individual']:
        base_score = 0.7  # 人类参与者能动性较高
    elif actor_type in ['document', 'policy']:
        base_score = 0.3  # 文档类参与者能动性较低
    
    return base_score


def map_relationships(relationships: List[Dict[str, Any]], actors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    映射参与者关系
    
    Args:
        relationships: 关系列表
        actors: 参与者列表
    
    Returns:
        关系映射结果
    """
    # 基础关系映射
    relationship_mapping = {
        "total_relationships": len(relationships),
        "actor_connections": {},
        "relationship_strengths": {},
        "interaction_natures": {}
    }
    
    # 提取有效的actor IDs
    actor_ids = set()
    for actor in actors:
        if isinstance(actor, dict) and 'id' in actor:
            actor_ids.add(actor['id'])
        elif isinstance(actor, dict) and 'name' in actor:
            # 如果没有ID，使用name作为标识
            actor_ids.add(actor['name'])
    
    for relationship in relationships:
        if not isinstance(relationship, dict):
            continue
            
        source = relationship.get('source')
        target = relationship.get('target')
        
        # 仅处理在参与者列表中的关系
        if source in actor_ids and target in actor_ids:
            if source not in relationship_mapping["actor_connections"]:
                relationship_mapping["actor_connections"][source] = []
            relationship_mapping["actor_connections"][source].append(target)
            
            # 基础关系强度（默认值）
            relationship_mapping["relationship_strengths"][(source, target)] = 0.5
            relationship_mapping["interaction_natures"][(source, target)] = "associative"
    
    return relationship_mapping


def role_analysis(actors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    分析参与者角色
    
    Args:
        actors: 参与者列表
    
    Returns:
        角色分析结果
    """
    roles = {
        "mediators": [],
        "intermediaries": [],
        "translators": [],
        "others": []
    }
    
    for actor in actors:
        # 基础角色分配（实际应用中应有更复杂的逻辑）
        role = actor.get('role', 'unknown')
        if 'mediat' in role.lower():
            roles['mediators'].append(actor)
        elif 'intermed' in role.lower():
            roles['intermediaries'].append(actor)
        elif 'translat' in role.lower():
            roles['translators'].append(actor)
        else:
            roles['others'].append(actor)
    
    return roles


def position_mapping(actors: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    映射参与者在网络中的位置
    
    Args:
        actors: 参与者列表
    
    Returns:
        位置映射结果
    """
    positions = {
        "central_actors": [],
        "peripheral_actors": [],
        "bridging_actors": []
    }
    
    # 基础位置分配（实际应用中应基于网络分析结果）
    for i, actor in enumerate(actors):
        if i < len(actors) * 0.2:  # 前20%作为中心参与者
            positions["central_actors"].append(actor)
        elif i >= len(actors) * 0.8:  # 后20%作为边缘参与者
            positions["peripheral_actors"].append(actor)
        else:
            positions["bridging_actors"].append(actor)
    
    return positions