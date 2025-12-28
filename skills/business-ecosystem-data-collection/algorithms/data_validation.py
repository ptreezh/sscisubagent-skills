"""
数据验证算法模块
单一职责：验证数据的完整性和一致性
"""

def validate_data(entities, relationships, industry_info):
    """
    验证数据的完整性和一致性
    输入: 实体列表、关系列表、行业信息
    输出: 包含验证结果的字典
    """
    # 检查实体ID是否唯一
    entity_ids = [e['id'] for e in entities]
    unique_entity_count = len(set(entity_ids))
    
    # 检查关系是否有效（源和目标实体存在）
    valid_relationships = []
    entity_id_set = set(entity_ids)
    
    for rel in relationships:
        source_exists = rel.get('source') in entity_id_set
        target_exists = rel.get('target') in entity_id_set
        if source_exists and target_exists:
            valid_relationships.append(rel)
    
    # 计算验证分数
    entity_uniqueness_score = unique_entity_count / len(entities) if entities else 1.0
    relationship_validity_score = len(valid_relationships) / len(relationships) if relationships else 1.0
    
    # 综合验证分数
    validation_score = (entity_uniqueness_score + relationship_validity_score) / 2
    
    return {
        "entities": entities,
        "relationships": valid_relationships,
        "industry_info": industry_info,
        "validation_score": validation_score,
        "validation_details": {
            "entity_uniqueness": entity_uniqueness_score,
            "relationship_validity": relationship_validity_score,
            "entity_count": len(entities),
            "relationship_count": len(valid_relationships)
        }
    }