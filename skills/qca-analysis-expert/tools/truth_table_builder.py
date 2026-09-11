#!/usr/bin/env python3
"""
qca-analysis-expert - 真值表构建工具
构建QCA真值表
"""

from typing import Dict, List
import json
from collections import defaultdict


class TruthTableBuilder:
    """真值表构建器"""

    def __init__(self):
        pass

    def build(self, data: List[Dict], conditions: List[str], outcome: str) -> Dict:
        """构建真值表"""
        # 统计每种条件组合
        combinations = defaultdict(lambda: {"cases": [], "outcome": None})

        for row in data:
            # 创建条件组合键
            combo = tuple(row.get(c, 0) for c in conditions)
            combinations[combo]["cases"].append(row)

            # 设置结果
            if outcome in row:
                combinations[combo]["outcome"] = row[outcome]

        # 构建真值表
        truth_table = []
        for combo, info in combinations.items():
            row = {
                "conditions": dict(zip(conditions, combo)),
                "n": len(info["cases"]),
                "outcome": info["outcome"],
                "consistency": self._calculate_consistency(info["cases"], outcome),
            }
            truth_table.append(row)

        # 按结果排序
        truth_table.sort(key=lambda x: (x["outcome"] or 0, x["n"]), reverse=True)

        return {
            "truth_table": truth_table,
            "num_configurations": len(truth_table),
            "conditions": conditions,
            "outcome": outcome,
        }

    def _calculate_consistency(self, cases: List[Dict], outcome: str) -> float:
        """计算一致性"""
        if not cases:
            return 0.0

        outcome_values = [c.get(outcome, 0) for c in cases]
        if not outcome_values:
            return 0.0

        return sum(outcome_values) / len(outcome_values)


def build_truth_table(data: List[Dict], conditions: List[str], outcome: str) -> Dict:
    return TruthTableBuilder().build(data, conditions, outcome)


if __name__ == "__main__":
    test_data = [
        {"A": 1, "B": 1, "Y": 1},
        {"A": 1, "B": 0, "Y": 1},
        {"A": 0, "B": 1, "Y": 0},
        {"A": 0, "B": 0, "Y": 0},
    ]
    result = build_truth_table(test_data, ["A", "B"], "Y")
    print(json.dumps(result, ensure_ascii=False, indent=2))
