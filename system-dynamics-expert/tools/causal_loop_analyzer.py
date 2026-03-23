#!/usr/bin/env python3
"""
system-dynamics-expert - 因果回路图分析工具
分析系统动力学中的因果关系和反馈回路
"""

from typing import Dict, List
import json


class CausalLoopAnalyzer:
    """因果回路分析器"""

    def __init__(self):
        pass

    def analyze(self, variables: List[str], relationships: List[Dict]) -> Dict:
        """分析因果回路"""
        # 识别反馈回路
        loops = self._find_feedback_loops(variables, relationships)

        # 识别因果链
        causal_chains = self._find_causal_chains(variables, relationships)

        # 识别增强/平衡回路
        loop_types = self._classify_loops(loops, relationships)

        return {
            "variables": variables,
            "relationships": relationships,
            "feedback_loops": loops,
            "causal_chains": causal_chains,
            "loop_types": loop_types,
            "summary": f"发现{len(loops)}个反馈回路",
        }

    def _find_feedback_loops(
        self, variables: List[str], relationships: List[Dict]
    ) -> List[List[str]]:
        """查找反馈回路"""
        # 简化实现
        loops = []
        for rel in relationships:
            if rel.get("type") == "feedback":
                loops.append(rel.get("loop", []))
        return loops

    def _find_causal_chains(
        self, variables: List[str], relationships: List[Dict]
    ) -> List[Dict]:
        """查找因果链"""
        chains = []
        for rel in relationships:
            if rel.get("type") == "causal":
                chains.append(
                    {
                        "from": rel.get("from"),
                        "to": rel.get("to"),
                        "sign": rel.get("sign", "+"),
                    }
                )
        return chains

    def _classify_loops(
        self, loops: List[List[str]], relationships: List[Dict]
    ) -> Dict:
        """分类回路"""
        reinforcing = []
        balancing = []

        for loop in loops:
            if any(
                r.get("sign") == "+" for r in relationships if r.get("loop") == loop
            ):
                reinforcing.append(loop)
            else:
                balancing.append(loop)

        return {
            "reinforcing": reinforcing,
            "balancing": balancing,
        }


def analyze_causal_loops(variables: List[str], relationships: List[Dict]) -> Dict:
    return CausalLoopAnalyzer().analyze(variables, relationships)


if __name__ == "__main__":
    test_vars = ["population", "births", "resources"]
    test_rels = [
        {"from": "population", "to": "births", "type": "causal", "sign": "+"},
    ]
    result = analyze_causal_loops(test_vars, test_rels)
    print(json.dumps(result, ensure_ascii=False, indent=2))
