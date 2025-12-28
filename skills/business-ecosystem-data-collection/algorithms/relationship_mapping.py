"""
关系映射算法模块
单一职责：识别和映射实体之间的关系
"""

def map_relationships_from_input(input_data):
    """
    从输入数据中映射关系
    输入: 包含关系信息的字典
    输出: 关系列表，每个关系包含源实体、目标实体、类型和强度
    """
    relationships = []
    
    # 直接从输入数据中获取关系
    if 'relationships' in input_data:
        for rel in input_data['relationships']:
            relationships.append({
                'source': rel.get('source'),
                'target': rel.get('target'),
                'type': rel.get('type', 'unknown'),
                'strength': rel.get('strength', 0.5),
                'description': rel.get('description', '')
            })
    
    return relationships


def validate_relationship_integrity(relationships, entity_ids):
    """
    验证关系的完整性（源和目标实体必须存在）
    输入: 关系列表，实体ID集合
    输出: 验证后的关系列表
    """
    valid_relationships = []
    entity_id_set = set(entity_ids)
    
    for rel in relationships:
        source_exists = rel.get('source') in entity_id_set
        target_exists = rel.get('target') in entity_id_set
        
        if source_exists and target_exists:
            valid_relationships.append(rel)
    
    return valid_relationships