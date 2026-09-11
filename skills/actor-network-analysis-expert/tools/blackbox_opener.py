#!/usr/bin/env python3
"""
actor-network-analysis-expert - 黑箱打开工具
打开网络中的"黑箱", 揭示其内部组成和运作机制
严格遵循ANT原则 - 任何被视为"黑箱"的事物都必须
"""

from typing import Dict, List, Set, Any, Optional
from collections import defaultdict
import json


# 黑箱关键词
BLACKBOX_INDICATORS = [
    "black box",
    "blackbox",
    "opaque",
    "unknown",
    "unclear",
    "hidden",
    "automatic",
    "seamless",
    "transparent",
    "magic",
    "mysterious",
    "complex",
    "sophisticated",
    "advanced",
    "intelligent",
    "works automatically",
    "handles automatically",
    "processes",
]

# 可疑的黑箱化陈述
SUSPICIOUS_STATEMENTS = [
    "the system automatically",
    "the algorithm automatically",
    "the AI automatically",
    "it just works",
    "transparent to users",
    "seamless integration",
    "plug and play",
    "out of the box",
    "set and forget",
    "magic happens",
]


class BlackboxOpener:
    """黑箱打开器"""

    def __init__(self):
        self.blackboxes = {}  # actor -> blackbox_info
        self.opened_blackboxes = {}  # actor -> opened_info
        self.traced_components = defaultdict(list)  # blackbox -> components

    def identify_blackboxes(
        self, actors: List[str], actor_details: Dict[str, Dict] = None
    ) -> Dict:
        """
        识别网络中的黑箱

        参数:
            actors: 行动者列表
            actor_details: 行动者详细信息

        返回:
            识别结果
        """
        if actor_details is None:
            actor_details = {}

        identified_blackboxes = []

        for actor in actors:
            details = actor_details.get(actor, {})
            description = details.get("description", "").lower()

            # 检查是否是黑箱
            is_blackbox = False
            reasons = []

            # 1. 检查名称是否暗示黑箱
            blackbox_names = [
                "system",
                "AI",
                "algorithm",
                "model",
                "platform",
                "network",
                "database",
                "cloud",
                "service",
            ]
            for name in blackbox_names:
                if name in actor.lower():
                    is_blackbox = True
                    reasons.append(f"名称包含黑箱关键词: {name}")

            # 2. 检查描述是否包含黑箱指标
            for indicator in BLACKBOX_INDICATORS:
                if indicator in description:
                    is_blackbox = True
                    reasons.append(f"描述包含黑箱指标: {indicator}")

            # 3. 检查可疑陈述
            for statement in SUSPICIOUS_STATEMENTS:
                if statement in description:
                    is_blackbox = True
                    reasons.append(f"包含可疑陈述: {statement}")

            # 4. 检查是否有内部结构未说明
            if (
                details.get("components") is None
                and details.get("internal_structure") is None
            ):
                if not details.get("is_opened", False):
                    is_blackbox = True
                    reasons.append("缺少内部结构说明")

            if is_blackbox:
                identified_blackboxes.append(
                    {
                        "actor": actor,
                        "reasons": reasons,
                        "risk_level": self._assess_blackbox_risk(actor, reasons),
                    }
                )
                self.blackboxes[actor] = {
                    "identified": True,
                    "reasons": reasons,
                    "status": "identified",
                }

        return {
            "total_blackboxes": len(identified_blackboxes),
            "blackboxes": identified_blackboxes,
            "risk_summary": self._summarize_risk(identified_blackboxes),
        }

    def _assess_blackbox_risk(self, actor: str, reasons: List[str]) -> str:
        """评估黑箱风险等级"""
        if any("algorithm" in r or "AI" in r or "model" in r for r in reasons):
            return "high"
        elif any("system" in r or "platform" in r for r in reasons):
            return "medium"
        else:
            return "low"

    def _summarize_risk(self, blackboxes: List[Dict]) -> Dict:
        """总结风险等级"""
        risk_counts = {"high": 0, "medium": 0, "low": 0}
        for bb in blackboxes:
            risk = bb.get("risk_level", "low")
            risk_counts[risk] += 1

        return risk_counts

    def open_blackbox(self, actor: str, investigation_data: Dict) -> Dict:
        """
        打开黑箱

        参数:
            actor: 行动者名称
            investigation_data: 调查数据 {
                'components': List[str],  # 内部组件
                'relationships': List[Dict],  # 内部关系
                'inputs': List[str],  # 输入
                'outputs': List[str],  # 输出
                'processes': List[str],  # 过程
                'dependencies': List[str],  # 依赖
                'limitations': List[str],  # 限制
                'controversies': List[str]  # 争议
            }

        返回:
            打开结果
        """
        if actor not in self.blackboxes:
            # 如果之前未识别, 先标记为黑箱
            self.blackboxes[actor] = {
                "identified": True,
                "reasons": ["在打开过程中识别"],
                "status": "identified",
            }

        opened_info = {
            "actor": actor,
            "status": "opened",
            "components": investigation_data.get("components", []),
            "relationships": investigation_data.get("relationships", []),
            "inputs": investigation_data.get("inputs", []),
            "outputs": investigation_data.get("outputs", []),
            "processes": investigation_data.get("processes", []),
            "dependencies": investigation_data.get("dependencies", []),
            "limitations": investigation_data.get("limitations", []),
            "controversies": investigation_data.get("controversies", []),
            "traceability_score": self._calculate_traceability(investigation_data),
        }

        self.opened_blackboxes[actor] = opened_info
        self.blackboxes[actor]["status"] = "opened"
        self.traced_components[actor] = investigation_data.get("components", [])

        return opened_info

    def _calculate_traceability(self, investigation_data: Dict) -> float:
        """计算可追溯性分数"""
        score = 0
        max_score = 6

        if investigation_data.get("components"):
            score += 1
        if investigation_data.get("relationships"):
            score += 1
        if investigation_data.get("inputs"):
            score += 1
        if investigation_data.get("outputs"):
            score += 1
        if investigation_data.get("processes"):
            score += 1
        if investigation_data.get("dependencies"):
            score += 1

        return (score / max_score) * 100

    def trace_actor_network(self, actor: str, network_data: Dict) -> Dict:
        """
        追踪行动者的网络关系

        参数:
            actor: 行动者名称
            network_data: 网络数据

        返回:
            追踪结果
        """
        # 提取与该行动者相关的所有连接
        related_actors = []
        relationships = []

        for rel in network_data.get("relationships", []):
            if rel.get("actor1") == actor or rel.get("actor2") == actor:
                related_actors.append(
                    rel.get("actor1")
                    if rel.get("actor2") == actor
                    else rel.get("actor2")
                )
                relationships.append(rel)

        return {
            "actor": actor,
            "related_actors": related_actors,
            "relationship_count": len(relationships),
            "relationships": relationships,
            "network_position": self._analyze_network_position(actor, network_data),
        }

    def _analyze_network_position(self, actor: str, network_data: Dict) -> Dict:
        """分析网络位置"""
        # 简化版本 - 实际应使用网络分析
        degree = 0
        for rel in network_data.get("relationships", []):
            if rel.get("actor1") == actor or rel.get("actor2") == actor:
                degree += 1

        return {"degree": degree, "position": "central" if degree > 5 else "peripheral"}

    def verify_blackbox_opening(self, actors: List[str]) -> Dict:
        """
        验证黑箱是否已被打开

        参数:
            actors: 行动者列表

        返回:
            验证结果
        """
        opened = []
        still_black = []

        for actor in actors:
            if actor in self.opened_blackboxes:
                opened.append(
                    {
                        "actor": actor,
                        "traceability_score": self.opened_blackboxes[actor][
                            "traceability_score"
                        ],
                    }
                )
            else:
                still_black.append(actor)

        total = len(actors)
        opened_count = len(opened)
        opening_rate = (opened_count / total * 100) if total > 0 else 0

        return {
            "total_actors": total,
            "opened_count": opened_count,
            "still_blackbox_count": len(still_black),
            "opening_rate": round(opening_rate, 1),
            "opened": opened,
            "still_blackbox": still_black,
            "status": "complete" if len(still_black) == 0 else "incomplete",
            "violations": self._identify_violations(still_black),
        }

    def _identify_violations(self, still_black: List[str]) -> List[Dict]:
        """识别黑箱化违规"""
        violations = []

        for actor in still_black:
            actor_lower = actor.lower()

            # 高风险黑箱未打开
            high_risk_keywords = ["AI", "algorithm", "system", "platform"]
            if any(kw in actor_lower for kw in high_risk_keywords):
                violations.append(
                    {
                        "actor": actor,
                        "violation_type": "high_risk_blackbox_not_opened",
                        "severity": "critical",
                        "recommendation": f"必须打开 {actor} 的内部结构",
                    }
                )

        return violations

    def generate_opening_report(self) -> Dict:
        """生成黑箱打开报告"""
        return {
            "summary": {
                "total_identified": len(self.blackboxes),
                "total_opened": len(self.opened_blackboxes),
                "opening_rate": round(
                    len(self.opened_blackboxes) / len(self.blackboxes) * 100, 1
                )
                if self.blackboxes
                else 0,
            },
            "opened_blackboxes": self.opened_blackboxes,
            "remaining_blackboxes": {
                k: v
                for k, v in self.blackboxes.items()
                if k not in self.opened_blackboxes
            },
            "component_traces": dict(self.traced_components),
        }


def create_opener() -> BlackboxOpener:
    """创建黑箱打开器实例"""
    return BlackboxOpener()


if __name__ == "__main__":
    # 测试
    opener = BlackboxOpener()

    test_actors = ["AI_system", "database", "manager", "algorithm", "hospital"]
    test_details = {
        "AI_system": {
            "description": "The AI system automatically processes data using advanced algorithms"
        },
        "database": {"description": "Database stores information"},
        "manager": {"description": "Manager makes decisions"},
        "algorithm": {"description": "The algorithm automatically selects outcomes"},
        "hospital": {"description": "Hospital provides healthcare services"},
    }

    result = opener.identify_blackboxes(test_actors, test_details)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    print("\n--- Opening AI_system ---")
    opening_result = opener.open_blackbox(
        "AI_system",
        {
            "components": ["data_processor", "model", "API", "interface"],
            "relationships": [
                {"from": "data_processor", "to": "model"},
                {"from": "model", "to": "API"},
            ],
            "inputs": ["raw_data", "user_query"],
            "outputs": ["predictions", "recommendations"],
            "processes": ["preprocessing", "inference", "postprocessing"],
            "dependencies": ["training_data", "compute_resource"],
            "limitations": ["bias", "accuracy", "interpretability"],
            "controversies": ["ethical_concerns", "transparency"],
        },
    )
    print(json.dumps(opening_result, ensure_ascii=False, indent=2))

    print("\n--- Verification ---")
    verify_result = opener.verify_blackbox_opening(test_actors)
    print(json.dumps(verify_result, ensure_ascii=False, indent=2))
