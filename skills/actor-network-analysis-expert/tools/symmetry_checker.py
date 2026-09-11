#!/usr/bin/env python3
"""
actor-network-analysis-expert - 对称性检查工具
验证行动者网络中人类/非人行动者的对称性原则
严格遵循ANT的"对称性原则" - 对人类和非人行动者使用相同的分析范畴
"""

from typing import Dict, List, Set, Any, Tuple
from collections import defaultdict
import json
import re


# ANT对称性原则methodology memo
# 行动者分类是诠释性判断，由LLM基于ANT理论完成
# Python仅提供数据结构和统计辅助
SYMMETRY_METHODOLOGY_MEMO = """【ANT对称性原则 - LLM专属判断】
Callon(1986)和Latour(1992)的ANT要求对人类和非人行动者使用相同的分析范畴。
- 禁止：仅因名称含"algorithm"/"system"就归类为"非人"
- 禁止：仅因名称含"manager"/"engineer"就归类为"人类"
- 正确做法：基于行动者的行为角色（actor role）而非名称标签分类
- 对称性评估：非人行动者是否被赋予与人类行动者同等的"行动者资格"
- 30%阈值仅作为信号，LLM需判断"这是真实对称还是形式对称"
"""


# 关键词字典已禁用：禁止用关键词匹配替代LLM的ANT诠释性判断


# 人类行动者类别关键词（已禁用，由LLM做诠释性判断）


def classify_actor(actor_name: str) -> Tuple[str, str]:
    """
    分类行动者类型。

    ⚠️ 关键词匹配已禁用。行动者分类是ANT诠释性判断，由LLM完成。
    本函数返回None，LLM基于SYMMETRY_METHODOLOGY_MEMO填充分类。
    """
    # 返回None表示需LLM判断，Python不做关键词匹配替代诠释判断
    return None


def check_symmetry(actors: List[str], actor_details: Dict[str, Dict] = None) -> Dict:
    """
    检查行动者网络的对称性

    参数:
        actors: 行动者名称列表
        actor_details: 行动者详细信息字典 {actor_name: {type, role, description}}

    返回:
        对称性检查结果
    """
    if actor_details is None:
        actor_details = {}

    # 分类统计
    human_count = 0
    nonhuman_count = 0
    unknown_count = 0

    human_actors = []
    nonhuman_actors = []
    unknown_actors = []

    for actor in actors:
        if actor in actor_details:
            actor_type = actor_details[actor].get("type", "unknown")
        else:
            category_type, _ = classify_actor(actor)
            actor_type = category_type

        if actor_type == "human":
            human_count += 1
            human_actors.append(actor)
        elif actor_type == "nonhuman":
            nonhuman_count += 1
            nonhuman_actors.append(actor)
        else:
            unknown_count += 1
            unknown_actors.append(actor)

    total_known = human_count + nonhuman_count
    nonhuman_ratio = nonhuman_count / total_known if total_known > 0 else 0

    # 对称性评估（阈值判断已禁用，由LLM做诠释性评估）
    # ANT对称性：非人行动者是否被赋予与人类同等的行动者资格
    # 30%/20%阈值仅作为定量信号，LLM判断这是"真实对称"还是"形式对称"
    symmetry_status = None  # LLM填充: pass/warning/fail
    symmetry_score = None    # LLM填充: 0-100评分

    return {
        "symmetry_status": symmetry_status,
        "symmetry_score": symmetry_score,
        "nonhuman_ratio": round(nonhuman_ratio, 3),
        "threshold": 0.30,
        "counts": {
            "human": human_count,
            "nonhuman": nonhuman_count,
            "unknown": unknown_count,
            "total": len(actors),
        },
        "actors": {
            "human": human_actors,
            "nonhuman": nonhuman_actors,
            "unknown": unknown_actors,
        },
        "violations": _detect_symmetry_violations(
            actor_details, human_actors, nonhuman_actors
        ),
    }


def _detect_symmetry_violations(
    actor_details: Dict, human_actors: List, nonhuman_actors: List
) -> List[Dict]:
    """
    检测对称性违规

    参数:
        actor_details: 行动者详细信息
        human_actors: 人类行动者列表
        nonhuman_actors: 非人行动者列表

    返回:
        违规列表
    """
    violations = []

    # 检查是否只关注人类行动者
    if len(nonhuman_actors) == 0 and len(human_actors) > 0:
        violations.append(
            {
                "type": "missing_nonhuman",
                "severity": "critical",
                "message": "网络中没有任何非人行动者, 违反了ANT对称性原则",
                "recommendation": "需要识别技术、工具、 artifacts 等非人行动者",
            }
        )

    # 检查行动者描述的对称性
    for actor, details in actor_details.items():
        if "description" in details:
            # 检查是否对人类行动者使用"意图"、"信念"等心理词汇
            # 而对非人行动者只使用"功能"等工具性词汇
            desc_lower = details["description"].lower()

            if actor in human_actors:
                if "intention" in desc_lower or "belief" in desc_lower:
                    # 这是可以的, 但要检查非人行动者是否被平等对待
                    pass

    return violations


def analyze_actor_roles_symmetrically(actor_details: Dict[str, Dict]) -> Dict:
    """
    对称性地分析行动者角色

    参数:
        actor_details: 行动者详细信息

    返回:
        对称性角色分析结果
    """
    # 提取所有行动者的角色属性
    human_roles = defaultdict(list)
    nonhuman_roles = defaultdict(list)

    for actor, details in actor_details.items():
        role = details.get("role", "unknown")
        category_type, _ = classify_actor(actor)

        if category_type == "human":
            human_roles[role].append(actor)
        elif category_type == "nonhuman":
            nonhuman_roles[role].append(actor)

    # 检查是否使用相同的角色范畴
    human_role_set = set(human_roles.keys())
    nonhuman_role_set = set(nonhuman_roles.keys())

    # 分析角色分布的对称性
    analysis = {
        "human_roles": dict(human_roles),
        "nonhuman_roles": dict(nonhuman_roles),
        "shared_roles": list(human_role_set & nonhuman_role_set),
        "human_only_roles": list(human_role_set - nonhuman_role_set),
        "nonhuman_only_roles": list(nonhuman_role_set - human_role_set),
        "symmetry_assessment": _assess_role_symmetry(human_roles, nonhuman_roles),
    }

    return analysis


def _assess_role_symmetry(human_roles: Dict, nonhuman_roles: Dict) -> Dict:
    """评估角色对称性"""
    human_set = set(human_roles.keys())
    nonhuman_set = set(nonhuman_roles.keys())

    shared = human_set & nonhuman_set
    only_human = human_set - nonhuman_set
    only_nonhuman = nonhuman_set - human_set

    # 如果有大量独有角色, 说明可能存在不对称
    asymmetry_score = 0
    if len(only_human) > 0:
        asymmetry_score += len(only_human) * 10
    if len(only_nonhuman) > 0:
        asymmetry_score += len(only_nonhuman) * 10

    # 硬编码阈值判断已禁用，由LLM做ANT对称性诠释判断
    status = None   # LLM填充: good/warning/poor
    score = None     # LLM填充: 0-100评分

    return {
        "status": status,
        "score": max(0, score),
        "message": f"共享角色: {len(shared)}, 人类独有: {len(only_human)}, 非人独有: {len(only_nonhuman)}",
    }


if __name__ == "__main__":
    # 测试
    test_actors = [
        "engineer",
        "manager",
        "AI_system",
        "software",
        "regulation",
        "company",
        "user",
        "database",
    ]
    test_details = {
        "engineer": {
            "type": "human",
            "role": "developer",
            "description": "intends to build system",
        },
        "manager": {
            "type": "human",
            "role": "decision_maker",
            "description": "makes decisions",
        },
        "AI_system": {
            "type": "nonhuman",
            "role": "actor",
            "description": "processes data",
        },
        "software": {
            "type": "nonhuman",
            "role": "tool",
            "description": "provides functionality",
        },
        "regulation": {
            "type": "nonhuman",
            "role": "constraint",
            "description": "limits actions",
        },
        "company": {
            "type": "nonhuman",
            "role": "organization",
            "description": "allocates resources",
        },
        "user": {
            "type": "human",
            "role": "beneficiary",
            "description": "uses the system",
        },
        "database": {
            "type": "nonhuman",
            "role": "infrastructure",
            "description": "stores data",
        },
    }

    result = check_symmetry(test_actors, test_details)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    print("\n--- Role Analysis ---")
    role_result = analyze_actor_roles_symmetrically(test_details)
    print(json.dumps(role_result, ensure_ascii=False, indent=2))
