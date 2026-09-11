"""
理论饱和度评估工具
评估扎根理论分析是否达到饱和状态
"""

from typing import Dict, List, Set
from collections import defaultdict


def assess_concept_saturation(existing_codes: Set[str], new_codes: Set[str]) -> Dict:
    """
    评估概念饱和度
    
    参数:
        existing_codes: 已有编码集合
        new_codes: 新增数据产生的编码集合
    
    返回:
        饱和度评估结果
    """
    if not existing_codes:
        return {
            'score': 0,
            'status': 'needs_more_data',
            'message': '没有已有编码'
        }
    
    # 计算新概念出现率
    new_concepts = new_codes - existing_codes
    new_concept_rate = len(new_concepts) / len(existing_codes) if existing_codes else 0
    
    # 饱和度分数(新概念出现率越低, 饱和度越高)
    if new_concept_rate < 0.05:
        score = 95
        status = 'saturated'
    elif new_concept_rate < 0.10:
        score = 85
        status = 'saturated'
    elif new_concept_rate < 0.15:
        score = 75
        status = 'needs_more_data'
    else:
        score = 60
        status = 'needs_more_data'
    
    return {
        'score': score,
        'status': status,
        'existing_concepts': len(existing_codes),
        'new_concepts': len(new_concepts),
        'new_concept_rate': round(new_concept_rate, 3),
        'new_concept_list': list(new_concepts),
        'threshold': 0.10
    }


def assess_category_saturation(categories: Dict, new_categories: Dict) -> Dict:
    """
    评估范畴饱和度
    
    参数:
        categories: 已有范畴字典 {name: {subcategories, properties, dimensions}}
        new_categories: 新增范畴字典
    
    返回:
        饱和度评估结果
    """
    if not categories:
        return {
            'score': 0,
            'status': 'needs_more_data',
            'message': '没有已有范畴'
        }
    
    # 检查范畴层级完整性
    hierarchy_complete = all(
        'subcategories' in cat and len(cat['subcategories']) > 0
        for cat in categories.values()
    )
    
    # 检查属性发展
    properties_developed = all(
        'properties' in cat and len(cat['properties']) > 0
        for cat in categories.values()
    )
    
    # 检查维度发展
    dimensions_developed = all(
        'dimensions' in cat and len(cat['dimensions']) > 0
        for cat in categories.values()
    )
    
    # 计算饱和度
    score = 0
    if hierarchy_complete:
        score += 30
    if properties_developed:
        score += 30
    if dimensions_developed:
        score += 30
    
    # 检查是否有新范畴
    new_cat_count = len(set(new_categories.keys()) - set(categories.keys()))
    if new_cat_count == 0:
        score += 10
    
    status = 'saturated' if score >= 80 else 'needs_more_data'
    
    return {
        'score': score,
        'status': status,
        'total_categories': len(categories),
        'new_categories': new_cat_count,
        'hierarchy_complete': hierarchy_complete,
        'properties_developed': properties_developed,
        'dimensions_developed': dimensions_developed
    }


def assess_relationship_saturation(existing_relationships: List[Dict], 
                                   new_relationships: List[Dict]) -> Dict:
    """
    评估关系饱和度
    
    参数:
        existing_relationships: 已有关系列表
        new_relationships: 新增关系列表
    
    返回:
        饱和度评估结果
    """
    if not existing_relationships:
        return {
            'score': 0,
            'status': 'needs_more_data',
            'message': '没有已有关系'
        }
    
    # 检查是否有新关系类型
    existing_types = set(r.get('type', 'unknown') for r in existing_relationships)
    new_types = set(r.get('type', 'unknown') for r in new_relationships)
    
    new_relation_types = new_types - existing_types
    
    # 计算饱和度
    if len(new_relation_types) == 0:
        score = 90
        status = 'saturated'
    elif len(new_relation_types) == 1:
        score = 75
        status = 'needs_more_data'
    else:
        score = 60
        status = 'needs_more_data'
    
    return {
        'score': score,
        'status': status,
        'total_relationships': len(existing_relationships),
        'new_relationships': len(new_relationships),
        'new_relation_types': list(new_relation_types),
        'relation_types': list(existing_types)
    }


def assess_proposition_saturation(existing_propositions: List[Dict],
                                   new_propositions: List[Dict]) -> Dict:
    """
    评估命题饱和度
    
    参数:
        existing_propositions: 已有命题列表
        new_propositions: 新增命题列表
    
    返回:
        饱和度评估结果
    """
    if not existing_propositions:
        return {
            'score': 0,
            'status': 'needs_more_data',
            'message': '没有已有命题'
        }
    
    # 检查是否有新命题
    existing_ids = set(p.get('id', '') for p in existing_propositions)
    new_ids = set(p.get('id', '') for p in new_propositions)
    
    new_prop_ids = new_ids - existing_ids
    
    # 计算饱和度
    if len(new_prop_ids) == 0:
        score = 90
        status = 'saturated'
    elif len(new_prop_ids) <= 2:
        score = 75
        status = 'needs_more_data'
    else:
        score = 60
        status = 'needs_more_data'
    
    return {
        'score': score,
        'status': status,
        'total_propositions': len(existing_propositions),
        'new_propositions': len(new_prop_ids),
        'new_proposition_ids': list(new_prop_ids)
    }


def assess_overall_saturation(concept_sat: Dict, category_sat: Dict, 
                              relationship_sat: Dict, proposition_sat: Dict) -> Dict:
    """
    评估整体饱和度
    
    参数:
        concept_sat: 概念饱和度评估结果
        category_sat: 范畴饱和度评估结果
        relationship_sat: 关系饱和度评估结果
        proposition_sat: 命题饱和度评估结果
    
    返回:
        整体饱和度评估结果
    """
    # 计算加权平均
    weights = {
        'concept': 0.3,
        'category': 0.3,
        'relationship': 0.2,
        'proposition': 0.2
    }
    
    overall_score = (
        concept_sat['score'] * weights['concept'] +
        category_sat['score'] * weights['category'] +
        relationship_sat['score'] * weights['relationship'] +
        proposition_sat['score'] * weights['proposition']
    )
    
    overall_score = round(overall_score, 1)
    
    # 判断状态
    if overall_score >= 80:
        status = 'saturated'
    else:
        status = 'needs_more_data'
    
    return {
        'overall_saturation': overall_score,
        'status': status,
        'by_dimension': {
            'concept_saturation': concept_sat,
            'category_saturation': category_sat,
            'relationship_saturation': relationship_sat,
            'proposition_saturation': proposition_sat
        },
        'threshold': 80,
        'recommendations': generate_recommendations(concept_sat, category_sat, 
                                                    relationship_sat, proposition_sat)
    }


def generate_recommendations(concept_sat: Dict, category_sat: Dict,
                            relationship_sat: Dict, proposition_sat: Dict) -> List[str]:
    """
    生成改进建议
    
    参数:
        各维度饱和度评估结果
    
    返回:
        建议列表
    """
    recommendations = []
    
    if concept_sat['status'] == 'needs_more_data':
        recommendations.append(
            f"概念饱和度不足 ({concept_sat['score']}%), 建议收集更多数据, "
            f"特别关注新概念出现：{', '.join(concept_sat.get('new_concept_list', []))}"
        )
    
    if category_sat['status'] == 'needs_more_data':
        if not category_sat.get('hierarchy_complete'):
            recommendations.append("范畴层级不完整, 需要进一步抽象和归类")
        if not category_sat.get('properties_developed'):
            recommendations.append("范畴属性发展不充分, 需要细化范畴特征")
        if not category_sat.get('dimensions_developed'):
            recommendations.append("范畴维度发展不充分, 需要探索变化范围")
    
    if relationship_sat['status'] == 'needs_more_data':
        recommendations.append(
            f"关系饱和度不足 ({relationship_sat['score']}%), 需要进一步探索范畴间关系"
        )
    
    if proposition_sat['status'] == 'needs_more_data':
        recommendations.append(
            f"命题饱和度不足 ({proposition_sat['score']}%), 需要生成更多理论命题"
        )
    
    if not recommendations:
        recommendations.append("理论已达到饱和状态, 可以结束数据收集并撰写最终报告")
    
    return recommendations


if __name__ == '__main__':
    # 测试
    existing_codes = {'A', 'B', 'C', 'D', 'E'}
    new_codes = {'A', 'B', 'F'}  # F 是新概念
    
    concept_result = assess_concept_saturation(existing_codes, new_codes)
    print(f"概念饱和度：{concept_result['score']}% - {concept_result['status']}")
    print(f"新概念出现率：{concept_result['new_concept_rate']}")
    print(f"新概念：{concept_result['new_concept_list']}")
