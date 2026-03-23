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


# 非人行动者类别关键词
NONHUMAN_CATEGORIES = {
    "technology": [
        "software",
        "hardware",
        "algorithm",
        "system",
        "platform",
        "device",
        "tool",
        "machine",
        "robot",
        "AI",
        "database",
        "network",
        "server",
        "app",
        "application",
    ],
    "artifact": [
        "document",
        "protocol",
        "standard",
        "policy",
        "law",
        "regulation",
        "contract",
        "agreement",
        "certificate",
        "license",
    ],
    "nature": [
        "river",
        "mountain",
        "climate",
        "weather",
        "soil",
        "water",
        "air",
        "animal",
        "plant",
        "ecosystem",
        "environment",
    ],
    "organization": [
        "company",
        "corporation",
        "agency",
        "institution",
        "department",
        "team",
        "group",
        "association",
    ],
    "concept": [
        "idea",
        "theory",
        "model",
        "framework",
        "paradigm",
        "method",
        "approach",
        "strategy",
    ],
    "material": [
        "building",
        "road",
        "bridge",
        "vehicle",
        "equipment",
        "infrastructure",
        "facility",
    ],
}

# 人类行动者类别关键词
HUMAN_CATEGORIES = {
    "individual": [
        "person",
        "individual",
        "human",
        "worker",
        "employee",
        "manager",
        "engineer",
        "researcher",
        "scientist",
        "doctor",
        "patient",
        "citizen",
        "user",
        "customer",
        "client",
    ],
    "role": [
        "actor",
        "agent",
        "stakeholder",
        "decision_maker",
        "implementer",
        "expert",
        "consultant",
        "advisor",
        "analyst",
    ],
    "group": ["team", "committee", "board", "council", "panel", "group", "department"],
}


def classify_actor(actor_name: str) -> Tuple[str, str]:
    """
    分类行动者类型

    参数:
        actor_name: 行动者名称

    返回:
        (category_type, category_name) - 例如 ('nonhuman', 'technology')
    """
    actor_lower = actor_name.lower()

    # 检查非人行动者
    for category, keywords in NONHUMAN_CATEGORIES.items():
        for keyword in keywords:
            if keyword in actor_lower:
                return ("nonhuman", category)

    # 检查人类行动者
    for category, keywords in HUMAN_CATEGORIES.items():
        for keyword in keywords:
            if keyword in actor_lower:
                return ("human", category)

    # 默认归类为未知, 需要进一步分析
    return ("unknown", "unclassified")


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

    # 对称性评估
    # ANT原则要求非人行动者至少占30%
    if nonhuman_ratio >= 0.30:
        symmetry_status = "pass"
        symmetry_score = min(100, 70 + int(nonhuman_ratio * 100))
    elif nonhuman_ratio >= 0.20:
        symmetry_status = "warning"
        symmetry_score = 60 + int(nonhuman_ratio * 50)
    else:
        symmetry_status = "fail"
        symmetry_score = int(nonhuman_ratio * 150)

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

    if asymmetry_score < 10:
        status = "good"
        score = 100 - asymmetry_score
    elif asymmetry_score < 30:
        status = "warning"
        score = 80 - asymmetry_score
    else:
        status = "poor"
        score = 60 - asymmetry_score

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
