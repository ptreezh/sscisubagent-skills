#!/usr/bin/env python3
"""
actor-network-analysis-expert - 争议记录工具
记录和分析行动者网络中的争议、冲突和失败
严格遵循ANT原则 - 必须记录所有争议和失败
"""

from typing import Dict, List, Set, Any, Optional
from collections import defaultdict
from datetime import datetime
import json


# 争议类型
CONTROVERSY_TYPES = [
    "technical",
    "ethical",
    "economic",
    "political",
    "social",
    "organizational",
    "environmental",
    "legal",
]

# 争议关键词
CONTROVERSY_KEYWORDS = {
    "conflict": [
        "conflict",
        "dispute",
        "disagreement",
        "tension",
        "controversy",
        "debate",
    ],
    "failure": [
        "fail",
        "error",
        "problem",
        "issue",
        "crisis",
        "breakdown",
        "malfunction",
    ],
    "resistance": ["resist", "refuse", "reject", "oppose", "protest", "complain"],
    "uncertainty": ["uncertain", "unknown", "unclear", "ambiguous", "unpredictable"],
    "risk": ["risk", "danger", "threat", "hazard", "concern", "fear"],
}


class ControversyRecorder:
    """争议记录器"""

    def __init__(self):
        self.controversies = []  # 争议列表
        self.actor_controversies = defaultdict(list)  # 行动者 -> 争议
        self.type_controversies = defaultdict(list)  # 类型 -> 争议
        self.resolved = []  # 已解决的争议
        self.unresolved = []  # 未解决的争议

    def record_controversy(
        self,
        actors: List[str],
        controversy_type: str,
        description: str,
        positions: Dict[str, str] = None,
        evidence: List[str] = None,
        impact: str = None,
        resolution: str = None,
    ) -> Dict:
        """
        记录争议

        参数:
            actors: 涉及的行动者
            controversy_type: 争议类型
            description: 争议描述
            positions: 各方立场 {actor: position}
            evidence: 证据列表
            impact: 影响
            resolution: 解决方案(如果有)

        返回:
            记录结果
        """
        controversy = {
            "id": f"contr_{len(self.controversies) + 1}",
            "actors": actors,
            "type": controversy_type,
            "description": description,
            "positions": positions or {},
            "evidence": evidence or [],
            "impact": impact,
            "resolution": resolution,
            "status": "resolved" if resolution else "unresolved",
            "recorded_at": datetime.now().isoformat(),
            "resolution_at": datetime.now().isoformat() if resolution else None,
        }

        self.controversies.append(controversy)

        # 更新索引
        for actor in actors:
            self.actor_controversies[actor].append(controversy)

        self.type_controversies[controversy_type].append(controversy)

        if resolution:
            self.resolved.append(controversy)
        else:
            self.unresolved.append(controversy)

        return {
            "status": "recorded",
            "controversy_id": controversy["id"],
            "total_controversies": len(self.controversies),
        }

    def record_conflict(
        self,
        actors: List[str],
        description: str,
        positions: Dict[str, str] = None,
        evidence: List[str] = None,
    ) -> Dict:
        """记录冲突"""
        return self.record_controversy(
            actors=actors,
            controversy_type="conflict",
            description=description,
            positions=positions,
            evidence=evidence,
        )

    def record_failure(
        self,
        actors: List[str],
        failure_description: str,
        cause: str = None,
        impact: str = None,
    ) -> Dict:
        """
        记录失败

        参数:
            actors: 涉及的行动者
            failure_description: 失败描述
            cause: 原因
            impact: 影响

        返回:
            记录结果
        """
        description = failure_description
        if cause:
            description += f" | 原因: {cause}"

        return self.record_controversy(
            actors=actors,
            controversy_type="failure",
            description=description,
            impact=impact,
        )

    def record_resistance(
        self,
        actor: str,
        description: str,
        resistance_type: str = None,
        evidence: List[str] = None,
    ) -> Dict:
        """
        记录阻力

        参数:
            actor: 抵制者
            description: 抵制描述
            resistance_type: 抵制类型
            evidence: 证据

        返回:
            记录结果
        """
        return self.record_controversy(
            actors=[actor],
            controversy_type="resistance",
            description=description,
            evidence=evidence,
        )

    def detect_controversies_from_text(
        self, text: str, source_actors: List[str] = None
    ) -> Dict:
        """
        从文本中检测争议

        参数:
            text: 输入文本
            source_actors: 已知行动者

        返回:
            检测结果
        """
        detected = []
        text_lower = text.lower()

        for category, keywords in CONTROVERSY_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    # 提取上下文
                    start = max(0, text_lower.find(keyword) - 50)
                    end = min(len(text), text_lower.find(keyword) + 50)
                    context = text[start:end]

                    detected.append(
                        {"keyword": keyword, "category": category, "context": context}
                    )

        return {
            "detected_count": len(detected),
            "detected": detected,
            "recommendation": "需要手动验证并记录为正式争议"
            if detected
            else "未检测到明显争议",
        }

    def get_actor_controversies(self, actor: str) -> List[Dict]:
        """获取特定行动者的所有争议"""
        return self.actor_controversies.get(actor, [])

    def get_type_controversies(self, controversy_type: str) -> List[Dict]:
        """获取特定类型的所有争议"""
        return self.type_controversies.get(controversy_type, [])

    def get_summary(self) -> Dict:
        """获取争议摘要"""
        return {
            "total_controversies": len(self.controversies),
            "resolved": len(self.resolved),
            "unresolved": len(self.unresolved),
            "resolution_rate": round(
                len(self.resolved) / len(self.controversies) * 100, 1
            )
            if self.controversies
            else 0,
            "by_type": {
                ctype: len(controversies)
                for ctype, controversies in self.type_controversies.items()
            },
            "actors_involved": list(self.actor_controversies.keys()),
        }

    def get_unresolved_controversies(self) -> List[Dict]:
        """获取所有未解决的争议"""
        return self.unresolved

    def get_critical_controversies(self) -> List[Dict]:
        """获取关键争议(影响网络的)"""
        critical = []

        for controversy in self.controversies:
            # 如果涉及多个行动者或影响重大, 则为关键
            if len(controversy["actors"]) > 1 or controversy.get("impact"):
                critical.append(controversy)

        return critical

    def resolve_controversy(self, controversy_id: str, resolution: str) -> Dict:
        """
        解决争议

        参数:
            controversy_id: 争议ID
            resolution: 解决方案

        返回:
            解决结果
        """
        for controversy in self.controversies:
            if controversy["id"] == controversy_id:
                controversy["status"] = "resolved"
                controversy["resolution"] = resolution
                controversy["resolution_at"] = datetime.now().isoformat()

                # 更新索引
                if controversy in self.unresolved:
                    self.unresolved.remove(controversy)
                    self.resolved.append(controversy)

                return {
                    "status": "resolved",
                    "controversy_id": controversy_id,
                    "resolution": resolution,
                }

        return {"status": "not_found", "controversy_id": controversy_id}

    def analyze_actor_network_impact(self) -> Dict:
        """
        分析争议对网络的影响

        返回:
            影响分析结果
        """
        actor_impact = defaultdict(
            lambda: {"conflicts": 0, "failures": 0, "resistances": 0}
        )

        for controversy in self.controversies:
            for actor in controversy["actors"]:
                ctype = controversy["type"]
                if ctype == "conflict":
                    actor_impact[actor]["conflicts"] += 1
                elif ctype == "failure":
                    actor_impact[actor]["failures"] += 1
                elif ctype == "resistance":
                    actor_impact[actor]["resistances"] += 1

        # 找出最受争议影响的行动者
        most_affected = sorted(
            actor_impact.items(), key=lambda x: sum(x[1].values()), reverse=True
        )[:5]

        return {
            "actor_impact": dict(most_affected),
            "total_affected_actors": len(actor_impact),
            "critical_actors": [actor for actor, _ in most_affected],
        }

    def generate_report(self) -> Dict:
        """生成完整报告"""
        return {
            "summary": self.get_summary(),
            "unresolved_controversies": self.unresolved,
            "critical_controversies": self.get_critical_controversies(),
            "network_impact": self.analyze_actor_network_impact(),
            "all_controversies": self.controversies,
        }

    def export_data(self) -> Dict:
        """导出数据"""
        return {
            "controversies": self.controversies,
            "actor_controversies": {k: v for k, v in self.actor_controversies.items()},
            "type_controversies": {k: v for k, v in self.type_controversies.items()},
            "resolved": self.resolved,
            "unresolved": self.unresolved,
        }

    def import_data(self, data: Dict):
        """导入数据"""
        self.controversies = data.get("controversies", [])
        self.resolved = data.get("resolved", [])
        self.unresolved = data.get("unresolved", [])

        # 重建索引
        self.actor_controversies = defaultdict(list)
        self.type_controversies = defaultdict(list)

        for controversy in self.controversies:
            for actor in controversy["actors"]:
                self.actor_controversies[actor].append(controversy)
            self.type_controversies[controversy["type"]].append(controversy)


def create_recorder() -> ControversyRecorder:
    """创建争议记录器实例"""
    return ControversyRecorder()


if __name__ == "__main__":
    # 测试
    recorder = ControversyRecorder()

    # 记录冲突
    recorder.record_conflict(
        actors=["manager", "engineer", "AI_system"],
        description="关于AI系统实施方式的分歧",
        positions={
            "manager": "倾向于快速部署",
            "engineer": "需要更多测试时间",
            "AI_system": "中立",
        },
        evidence=["会议记录", "邮件往来"],
    )

    # 记录失败
    recorder.record_failure(
        actors=["database", "server"],
        failure_description="系统崩溃导致数据丢失",
        cause="服务器过载",
        impact="严重影响业务",
    )

    # 记录阻力
    recorder.record_resistance(
        actor="doctor",
        description="医生抵制使用AI辅助诊断系统",
        evidence=["问卷调查", "访谈记录"],
    )

    print(json.dumps(recorder.get_summary(), ensure_ascii=False, indent=2))

    print("\n--- Unresolved ---")
    print(
        json.dumps(
            recorder.get_unresolved_controversies(), ensure_ascii=False, indent=2
        )
    )

    print("\n--- Network Impact ---")
    print(
        json.dumps(
            recorder.analyze_actor_network_impact(), ensure_ascii=False, indent=2
        )
    )
