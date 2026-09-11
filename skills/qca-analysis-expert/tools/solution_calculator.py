#!/usr/bin/env python3
"""
qca-analysis-expert - 解公式计算工具
计算QCA充分性解
"""

from typing import Dict, List
import json


class SolutionCalculator:
    """解公式计算器"""

    def __init__(self):
        pass

    def calculate(self, truth_table: List[Dict]) -> Dict:
        """计算解公式"""
        # 简化的解计算
        # 实际需要使用Quine-McCluskey算法

        solutions = []

        # 按outcome分组
        positive = [row for row in truth_table if row.get("outcome") == 1]

        if positive:
            # 提取解
            solution_terms = []
            for row in positive:
                terms = []
                for cond, val in row["conditions"].items():
                    if val == 1:
                        terms.append(cond)
                    else:
                        terms.append(f"~{cond}")
                solution_terms.append("*".join(terms))

            # 简化表示
            solution = "+".join(solution_terms)

            solutions.append(
                {
                    "solution": solution,
                    "terms": solution_terms,
                    "coverage": self._calculate_coverage(positive, truth_table),
                    "consistency": self._calculate_solution_consistency(positive),
                }
            )

        return {
            "solutions": solutions,
            "type": "sufficiency",
            "summary": f"找到{len(solutions)}个解",
        }

    def _calculate_coverage(
        self, positive: List[Dict], truth_table: List[Dict]
    ) -> float:
        """计算覆盖度"""
        total_outcome = sum(
            row.get("n", 1) for row in truth_table if row.get("outcome") == 1
        )
        covered = sum(row.get("n", 1) for row in positive)

        if total_outcome == 0:
            return 0.0
        return covered / total_outcome

    def _calculate_solution_consistency(self, positive: List[Dict]) -> float:
        """计算解的一致性"""
        if not positive:
            return 0.0

        consistencies = [row.get("consistency", 1.0) for row in positive]
        return sum(consistencies) / len(consistencies)


def calculate_solution(truth_table: List[Dict]) -> Dict:
    return SolutionCalculator().calculate(truth_table)


if __name__ == "__main__":
    test_table = [
        {"conditions": {"A": 1, "B": 1}, "n": 5, "outcome": 1, "consistency": 0.9},
        {"conditions": {"A": 1, "B": 0}, "n": 3, "outcome": 1, "consistency": 0.8},
        {"conditions": {"A": 0, "B": 1}, "n": 2, "outcome": 0, "consistency": 0.7},
    ]
    result = calculate_solution(test_table)
    print(json.dumps(result, ensure_ascii=False, indent=2))
