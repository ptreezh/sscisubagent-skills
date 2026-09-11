#!/usr/bin/env python3
"""
actor-network-analysis-expert - 黑箱打开工具
打开网络中的"黑箱", 揭示其内部组成和运作机制
严格遵循ANT原则 - 任何被视为"黑箱"的事物都必须被打开分析

【方法论说明】
本工具不包含任何硬编码关键词匹配。所有黑箱识别和内部结构分析由LLM根据理论备忘录完成。
工具仅负责：状态管理、空结构返回、方法论引导。
"""

from typing import Dict, List, Set, Any, Optional
from collections import defaultdict
import json


# ---------------------------------------------------------------------------
# ANT黑箱理论备忘录（供LLM判断时参考）
# ---------------------------------------------------------------------------
BLACKBOX_THEORY_MEMO = """
=== ANT黑箱（Black Boxing）理论备忘录 ===

【黑箱概念】
黑箱（Black Box）是ANT中的一个核心概念，指那些内部运作机制被隐藏、
被当作不可分割整体对待的事物。黑箱一旦"关闭"（black-boxed），其内部复杂性
就不再被追问，成为网络的稳定节点。

【为什么要打开黑箱？】
- 黑箱掩盖了异质性行动者的网络关系
- 揭示非人类行动者（技术、算法、平台）的能动性
- 暴露谁有权定义黑箱的边界
- 发现网络中隐藏的权力关系

【黑箱识别标准】（供LLM判断参考）

技术类黑箱识别：
- 名称包含 system, AI, algorithm, model, platform, network, database, cloud, service
- 描述中包含 "automatic", "automatically handles", "seamless", "plug and play"
- 内部运作机制未被说明
- 对用户行为有塑造作用但用户不理解其原理

制度类黑箱识别：
- 被当作理所当然的存在
- 不被追问其形成过程
- 代表了某种网络共识

【打开黑箱的维度】（供LLM分析参考）
1. 内部组件（components）：黑箱由哪些异质性行动者组成？
2. 内部关系（relationships）：组件之间如何连接？
3. 输入（inputs）：什么进入黑箱？
4. 输出（outputs）：什么从黑箱出来？
5. 过程（processes）：转换过程是怎样的？
6. 依赖（dependencies）：黑箱依赖什么外部资源？
7. 限制（limitations）：黑箱有什么局限？
8. 争议（controversies）：黑箱是否存在争议？

【ANT分析要求】
- 不能仅凭名称判断是否为黑箱，要分析其实际运作
- 关注算法/AI类黑箱：算法决策如何塑造社会？
- 追问：谁制造了黑箱？谁受益于黑箱的存在？
- 分析黑箱打开后的网络变化
"""


class BlackboxOpener:
    """黑箱打开器（无关键词匹配版）

    所有黑箱识别和内部结构分析由调用方/LLM根据 theory_memo 完成。
    """

    def __init__(self):
        self.blackboxes: Dict[str, Dict] = {}  # actor -> blackbox_info
        self.opened_blackboxes: Dict[str, Dict] = {}  # actor -> opened_info
        self.traced_components: Dict[str, List] = defaultdict(list)

    def identify_blackboxes(
        self, actors: List[str], actor_details: Dict[str, Dict] = None
    ) -> Dict:
        """
        识别网络中的黑箱（返回空结构供LLM填充）

        参数:
            actors: 行动者列表
            actor_details: 行动者详细信息

        返回:
            含空结构的识别结果，需LLM根据 BLACKBOX_THEORY_MEMO 填充
        """
        if actor_details is None:
            actor_details = {}

        result: Dict = {
            "total_blackboxes": 0,
            "blackboxes": [],  # LLM填充: [{actor, reasons, risk_level, evidence}, ...]
            "risk_summary": {"high": 0, "medium": 0, "low": 0},  # LLM填充
            "theory_memo": BLACKBOX_THEORY_MEMO.strip(),
            "actors_checked": actors,
            "raw_details_for_llm": {
                name: details for name, details in actor_details.items()
            },
        }
        return result

    def open_blackbox(self, actor: str, investigation_data: Dict) -> Dict:
        """
        打开黑箱（investigation_data由LLM根据 BLACKBOX_THEORY_MEMO 填充）

        参数:
            actor: 行动者名称
            investigation_data: 调查数据（LLM填充）{
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
        self.blackboxes[actor] = {
            "identified": True,
            "status": "opened",
        }
        self.traced_components[actor] = investigation_data.get("components", [])

        return opened_info

    def _calculate_traceability(self, investigation_data: Dict) -> float:
        """计算可追溯性分数"""
        score = 0
        max_score = 6

        for key in ["components", "relationships", "inputs", "outputs", "processes", "dependencies"]:
            if investigation_data.get(key):
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
        related_actors = []
        relationships = []

        for rel in network_data.get("relationships", []):
            if rel.get("actor1") == actor or rel.get("actor2") == actor:
                related_actors.append(
                    rel.get("actor1") if rel.get("actor2") == actor else rel.get("actor2")
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
            验证结果（violations由LLM根据 BLACKBOX_THEORY_MEMO 填充）
        """
        opened = []
        still_black = []

        for actor in actors:
            if actor in self.opened_blackboxes:
                opened.append({
                    "actor": actor,
                    "traceability_score": self.opened_blackboxes[actor]["traceability_score"],
                })
            else:
                still_black.append(actor)

        total = len(actors)
        opening_rate = (len(opened) / total * 100) if total > 0 else 0

        return {
            "total_actors": total,
            "opened_count": len(opened),
            "still_blackbox_count": len(still_black),
            "opening_rate": round(opening_rate, 1),
            "opened": opened,
            "still_blackbox": still_black,
            "status": "complete" if len(still_black) == 0 else "incomplete",
            "violations": [],  # LLM根据 BLACKBOX_THEORY_MEMO 填充
            "theory_memo": BLACKBOX_THEORY_MEMO.strip(),
        }

    def generate_opening_report(self) -> Dict:
        """生成黑箱打开报告"""
        return {
            "summary": {
                "total_identified": len(self.blackboxes),
                "total_opened": len(self.opened_blackboxes),
                "opening_rate": round(
                    len(self.opened_blackboxes) / len(self.blackboxes) * 100, 1
                ) if self.blackboxes else 0,
            },
            "opened_blackboxes": self.opened_blackboxes,
            "remaining_blackboxes": {
                k: v for k, v in self.blackboxes.items()
                if k not in self.opened_blackboxes
            },
            "component_traces": dict(self.traced_components),
        }


def create_opener() -> BlackboxOpener:
    """创建黑箱打开器实例"""
    return BlackboxOpener()


if __name__ == "__main__":
    opener = BlackboxOpener()
    test_actors = ["AI_system", "database", "manager", "algorithm", "hospital"]
    test_details = {
        "AI_system": {"description": "Advanced AI system processes data automatically"},
        "database": {"description": "Database stores information"},
        "algorithm": {"description": "Algorithm selects outcomes automatically"},
    }
    result = opener.identify_blackboxes(test_actors, test_details)
    print("=== 返回结构（需LLM填充） ===")
    print(f"total_blackboxes: {result['total_blackboxes']}")
    print(f"blackboxes: {result['blackboxes']}")
    print(f"\n理论备忘录（前300字）:\n{result['theory_memo'][:300]}")
