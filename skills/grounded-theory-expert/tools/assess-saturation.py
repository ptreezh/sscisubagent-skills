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

    # score/status 阈值分支自动判断已禁用
    # Python保留原始定量计算，LLM基于GT理论做诠释判断
    # 正确分工：Python算比率，LLM判断是否饱和
    computed_score = round(new_concept_rate * 100, 1)  # 原始定量（不是阈值分支）
    return {
        'score': computed_score,  # 保留：原始定量信号（不是阈值分支）
        'status': None,           # 禁用：阈值分支自动判断 → LLM填充
        'methodology_memo': (
            "GT饱和判断原则:\n"
            "1. score是原始定量信号，0.05/0.10/0.15阈值仅为参考\n"
            "2. status判定必须由LLM基于理论原则完成\n"
            "3. 表面新概念（词汇差异）与实质性新范畴（理论意义）需LLM区分\n"
            "4. 饱和是渐进过程，不是二值状态"
        ),
        'existing_concepts': len(existing_codes),
        'new_concepts': len(new_concepts),
        'new_concept_rate': round(new_concept_rate, 3),
        'new_concept_list': list(new_concepts),
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

    # 硬编码80分阈值判断status已禁用
    # Python保留原始定量信号，status判定由LLM完成
    computed_score = score  # 保留原始定量计算
    return {
        'score': computed_score,  # 保留：原始定量信号
        'status': None,           # 禁用阈值判断 → LLM填充
        'methodology_memo': (
            "范畴饱和判断:\n"
            "1. 80分阈值仅为信号，LLM需判断范畴是否已充分"发展"（dimensionally）\n"
            "2. 层级完整性+属性发展+维度发展是必要条件，但不是充分条件\n"
            "3. 新范畴出现≠不饱和，需评估其与现有范畴的关系"
        ),
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

    # 硬编码关系饱和判断已禁用
    # Python保留原始定量信号，status判定由LLM完成
    computed_score = 90 if len(new_relation_types) == 0 else (75 if len(new_relation_types) == 1 else 60)
    return {
        'score': computed_score,  # 保留：原始定量信号
        'status': None,           # 禁用阈值判断 → LLM填充
        'methodology_memo': (
            "关系饱和判断:\n"
            "1. 新关系类型出现数量仅为定量信号\n"
            "2. 关系质量（因果强度、理论意义）比数量更重要\n"
            "3. 相同关系类型的不同案例 ≠ 新关系类型"
        ),
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

    # 硬编码命题饱和判断已禁用
    # Python保留原始定量信号，status判定由LLM完成
    computed_score = 90 if len(new_prop_ids) == 0 else (75 if len(new_prop_ids) <= 2 else 60)
    return {
        'score': computed_score,  # 保留：原始定量信号
        'status': None,           # 禁用阈值判断 → LLM填充
        'methodology_memo': (
            "命题饱和判断:\n"
            "1. 新命题数量仅为定量信号\n"
            "2. 命题的理论整合程度比数量更重要\n"
            "3. 已有命题的深化 ≠ 新命题出现"
        ),
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
    # 80分阈值判断status已禁用
    # Python保留加权平均计算（定量），status判定由LLM完成
    weights = {'concept': 0.3, 'category': 0.3, 'relationship': 0.2, 'proposition': 0.2}
    cs = concept_sat.get('score', 0) or 0
    cat = category_sat.get('score', 0) or 0
    rel = relationship_sat.get('score', 0) or 0
    prop = proposition_sat.get('score', 0) or 0
    overall = round(cs * weights['concept'] + cat * weights['category'] +
                   rel * weights['relationship'] + prop * weights['proposition'], 1)
    return {
        'overall_saturation': overall,  # 保留：加权平均计算
        'status': None,  # 禁用阈值判断 → LLM填充
        'methodology_memo': (
            "整体饱和判断:\n"
            "1. 加权平均和80分阈值仅为定量信号\n"
            "2. 理论建构的完整性比各维度分数更重要\n"
            "3. 各维度权重(0.3/0.3/0.2/0.2)不是绝对标准\n"
            "4. LLM需综合四维度做整体理论饱和判断"
        ),
        'by_dimension': {
            'concept_saturation': concept_sat,
            'category_saturation': category_sat,
            'relationship_saturation': relationship_sat,
            'proposition_saturation': proposition_sat
        },
        'recommendations': None,  # LLM填充
    }


def generate_recommendations(concept_sat: Dict, category_sat: Dict,
                            relationship_sat: Dict, proposition_sat: Dict) -> List[str]:
    """
    生成改进建议。

    ⚠️ 建议生成由LLM基于methodology_memo完成，不做硬编码状态判断。
    Python返回结构化空字段，LLM结合各维度的methodology_memo做实质性建议。
    """
    return {
        "recommendations": [],  # LLM填充
        "methodology_memo": (
            "建议生成原则:\n"
            "1. 各维度分数仅作为诊断信号，LLM做实质性判断\n"
            "2. 新概念判断需区分表面词汇差异与理论实质差异\n"
            "3. 建议需具体到数据收集方向，而非泛泛的"继续采样""
        ),
    }


if __name__ == '__main__':
    # 测试
    existing_codes = {'A', 'B', 'C', 'D', 'E'}
    new_codes = {'A', 'B', 'F'}  # F 是新概念
    
    concept_result = assess_concept_saturation(existing_codes, new_codes)
    print(f"概念饱和度：{concept_result['score']}% - {concept_result['status']}")
    print(f"新概念出现率：{concept_result['new_concept_rate']}")
    print(f"新概念：{concept_result['new_concept_list']}")
