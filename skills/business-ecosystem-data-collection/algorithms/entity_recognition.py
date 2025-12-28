"""
实体识别算法模块
单一职责：从输入数据中识别和提取实体信息
"""

def extract_entities_from_input(input_data):
    """
    从输入数据中提取实体信息
    输入: 包含实体信息的字典
    输出: 实体列表，每个实体包含id、name、type等属性
    """
    entities = []
    
    # 直接从输入数据中获取实体
    if 'entities' in input_data:
        for entity in input_data['entities']:
            entities.append({
                'id': entity.get('id'),
                'name': entity.get('name', ''),
                'type': entity.get('type', 'unknown'),
                'industry': entity.get('industry', input_data.get('targetIndustry', 'unknown')),
                'characteristics': entity.get('characteristics', {})
            })
    
    # 如果输入包含其他实体信息，也处理它们
    if 'input_entities' in input_data:
        for entity in input_data['input_entities']:
            entities.append({
                'id': entity.get('id', f"entity_{len(entities)+1}"),
                'name': entity.get('name', f"实体{len(entities)+1}"),
                'type': entity.get('type', 'unknown'),
                'industry': input_data.get('targetIndustry', 'unknown'),
                'characteristics': entity.get('characteristics', {})
            })
    
    return entities


def standardize_entity_format(entity):
    """
    标准化实体格式
    输入: 单个实体字典
    输出: 标准化后的实体字典
    """
    return {
        'id': entity.get('id', ''),
        'name': entity.get('name', ''),
        'type': entity.get('type', 'unknown'),
        'industry': entity.get('industry', ''),
        'characteristics': entity.get('characteristics', {}),
        'description': entity.get('description', ''),
        'contact': entity.get('contact', {})
    }