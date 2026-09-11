#!/usr/bin/env python3
"""
actor-network-analysis-expert - 网络饱和度评估工具
评估行动者网络分析是否达到饱和状态
"""

from typing import Dict, List, Set, Any
from collections import defaultdict
import json


def assess_actor_saturation(existing_actors: Set[str], new_actors: Set[str]) -> Dict:
    """
    评估行动者饱和度

    参数:
        existing_actors: 已有行动者集合
        new_actors: 新增数据产生的行动者集合

    返回:
        饱和度评估结果
    """
    if not existing_actors:
        return {"score": 0, "status": "needs_more_data", "message": "没有已有行动者"}

    # 计算新行动者出现率
    new_actors_found = new_actors - existing_actors
    new_actor_rate = (
        len(new_actors_found) / len(existing_actors) if existing_actors else 0
    )

    # 饱和度分数(新行动者出现率越低, 饱和度越高)
    if new_actor_rate < 0.05:
        score = 95
        status = "saturated"
    elif new_actor_rate < 0.10:
        score = 85
        status = "saturated"
    elif new_actor_rate < 0.15:
        score = 75
        status = "needs_more_data"
    else:
        score = 60
        status = "needs_more_data"

    return {
        "type": "actor_saturation",
        "score": score,
        "status": status,
        "existing_actors": len(existing_actors),
        "new_actors": len(new_actors_found),
        "new_actor_rate": round(new_actor_rate, 3),
        "new_actor_list": list(new_actors_found),
        "threshold": 0.10,
    }


def assess_relationship_saturation(
    relationships: List[Dict], new_relationships: List[Dict]
) -> Dict:
    """
    评估关系饱和度

    参数:
        relationships: 已有关系列表
        new_relationships: 新增关系列表

    返回:
        关系饱和度评估结果
    """
    if not relationships:
        return {"score": 0, "status": "needs_more_data", "message": "没有已有关系"}

    # 提取关系特征
    existing_rels = set(f"{r.get('source')}-{r.get('target')}" for r in relationships)
    new_rels = set(f"{r.get('source')}-{r.get('target')}" for r in new_relationships)

    new_rel_found = new_rels - existing_rels
    new_rel_rate = len(new_rel_found) / len(existing_rels) if existing_rels else 0

    # 饱和度评估
    if new_rel_rate < 0.03:
        score = 95
        status = "saturated"
    elif new_rel_rate < 0.07:
        score = 85
        status = "saturated"
    elif new_rel_rate < 0.12:
        score = 75
        status = "needs_more_data"
    else:
        score = 60
        status = "needs_more_data"

    return {
        "type": "relationship_saturation",
        "score": score,
        "status": status,
        "existing_relationships": len(relationships),
        "new_relationships": len(new_rel_found),
        "new_relationship_rate": round(new_rel_rate, 3),
        "threshold": 0.07,
    }


def assess_translation_saturation(
    translation_stages: Dict, complete_stages: Set[str]
) -> Dict:
    """
    评估转译阶段饱和度

    参数:
        translation_stages: 转译阶段字典
        complete_stages: 已完成的阶段集合

    返回:
        转译饱和度评估结果
    """
    required_stages = {"problematization", "attribution", "enrollment", "mobilization"}

    # 检查4个阶段是否完整
    stage_completeness = len(complete_stages & required_stages) / len(required_stages)

    # 评估每个阶段的细节程度
    stage_detail_scores = []
    for stage in required_stages:
        if stage in translation_stages:
            stage_data = translation_stages[stage]
            # 检查该阶段是否有足够的细节
            detail_score = min(
                100,
                len(stage_data.get("actors", [])) * 10
                + len(stage_data.get("actions", [])) * 10,
            )
            stage_detail_scores.append(detail_score)

    avg_detail_score = (
        sum(stage_detail_scores) / len(stage_detail_scores)
        if stage_detail_scores
        else 0
    )

    # 综合饱和度分数
    overall_score = stage_completeness * 50 + avg_detail_score * 0.5

    if overall_score >= 90:
        status = "saturated"
    elif overall_score >= 75:
        status = "near_saturation"
    elif overall_score >= 60:
        status = "needs_more_data"
    else:
        status = "incomplete"

    return {
        "type": "translation_saturation",
        "score": round(overall_score, 1),
        "status": status,
        "stage_completeness": round(stage_completeness * 100, 1),
        "average_detail_score": round(avg_detail_score, 1),
        "complete_stages": list(complete_stages),
        "required_stages": list(required_stages),
        "missing_stages": list(required_stages - complete_stages),
    }


def assess_network_saturation(actor_data: Dict, new_data: Dict = None) -> Dict:
    """
    综合评估网络饱和度

    参数:
        actor_data: 已有网络数据 {
            'actors': Set[str],
            'relationships': List[Dict],
            'translation_stages': Dict,
            'complete_stages': Set[str]
        }
        new_data: 新增数据(可选)

    返回:
        综合饱和度评估结果
    """
    if new_data is None:
        new_data = {
            "actors": set(),
            "relationships": [],
            "translation_stages": {},
            "complete_stages": set(),
        }

    # 评估各个维度
    actor_result = assess_actor_saturation(
        actor_data.get("actors", set()), new_data.get("actors", set())
    )

    relationship_result = assess_relationship_saturation(
        actor_data.get("relationships", []), new_data.get("relationships", [])
    )

    translation_result = assess_translation_saturation(
        actor_data.get("translation_stages", {}),
        actor_data.get("complete_stages", set()),
    )

    # 综合评分
    weights = {"actor": 0.4, "relationship": 0.3, "translation": 0.3}
    overall_score = (
        actor_result["score"] * weights["actor"]
        + relationship_result["score"] * weights["relationship"]
        + translation_result["score"] * weights["translation"]
    )

    # 确定整体状态
    if overall_score >= 85:
        overall_status = "saturated"
    elif overall_score >= 70:
        overall_status = "near_saturation"
    elif overall_score >= 50:
        overall_status = "needs_more_data"
    else:
        overall_status = "incomplete"

    return {
        "overall_score": round(overall_score, 1),
        "overall_status": overall_status,
        "actor_saturation": actor_result,
        "relationship_saturation": relationship_result,
        "translation_saturation": translation_result,
        "recommendations": _generate_recommendations(
            actor_result, relationship_result, translation_result
        ),
    }


def _generate_recommendations(
    actor_result: Dict, relationship_result: Dict, translation_result: Dict
) -> List[str]:
    """生成饱和度改进建议"""
    recommendations = []

    if actor_result["status"] == "needs_more_data":
        recommendations.append(
            f"需要更多数据发现新行动者 (当前新增率: {actor_result['new_actor_rate']})"
        )

    if relationship_result["status"] == "needs_more_data":
        recommendations.append(
            f"需要更多数据发现新关系 (当前新增率: {relationship_result['new_relationship_rate']})"
        )

    if translation_result["status"] in ["needs_more_data", "incomplete"]:
        missing = translation_result.get("missing_stages", [])
        if missing:
            recommendations.append(f"转译阶段不完整, 缺少: {', '.join(missing)}")

    if not recommendations:
        recommendations.append("网络已达到饱和状态, 可以进行最终分析")

    return recommendations


if __name__ == "__main__":
    # 测试
    test_actor_data = {
        "actors": {"human1", "human2", "technology1", "organization1"},
        "relationships": [
            {"source": "human1", "target": "technology1"},
            {"source": "human2", "target": "organization1"},
        ],
        "translation_stages": {
            "problematization": {"actors": ["human1"], "actions": ["define_problem"]},
            "attribution": {"actors": ["technology1"], "actions": ["assign_interest"]},
        },
        "complete_stages": {"problematization", "attribution"},
    }

    test_new_data = {
        "actors": {"technology2"},
        "relationships": [],
        "translation_stages": {},
        "complete_stages": set(),
    }

    result = assess_network_saturation(test_actor_data, test_new_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
