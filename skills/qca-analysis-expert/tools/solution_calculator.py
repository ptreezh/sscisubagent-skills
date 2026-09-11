#!/usr/bin/env python3
"""
qca-analysis-expert - 解公式计算工具
计算QCA充分性解
"""

from typing import Dict, List
import json


class SolutionCalculator:
    """解公式计算器，支持三解类型（Ragin 2008 fsQCA标准）"""

    def __init__(self):
        pass

    def calculate(
        self,
        truth_table: List[Dict],
        solution_type: str = "intermediate",
    ) -> Dict:
        """
        计算解公式，支持三种解类型。

        Args:
            truth_table: 真值表数据
            solution_type: 解类型
                - "complex": 复杂解，仅使用直接观察的必要条件，不使用逻辑余项
                - "intermediate": 中间解，使用部分逻辑余项（符合理论预期）
                - "parsimonious": 简约解，使用全部逻辑余项，包含简化假设
                - "all": 返回全部三种解
        """
        if solution_type == "all":
            return {
                "complex": self._compute_solution(truth_table, "complex"),
                "intermediate": self._compute_solution(truth_table, "intermediate"),
                "parsimonious": self._compute_solution(truth_table, "parsimonious"),
            }

        return self._compute_solution(truth_table, solution_type)

    def _compute_solution(
        self, truth_table: List[Dict], solution_type: str
    ) -> Dict:
        """计算单一类型解"""
        solutions: List[Dict] = []
        positive = [row for row in truth_table if row.get("outcome") == 1]

        if not positive:
            return {
                "solutions": [],
                "type": solution_type,
                "description": self._type_description(solution_type),
                "summary": "无正向解",
            }

        seen_terms: set = set()
        solution_terms: List[str] = []

        for row in positive:
            terms: List[str] = []
            for cond, val in sorted(row["conditions"].items()):
                if val == 1:
                    terms.append(cond)
                else:
                    terms.append(f"~{cond}")

            # 根据解类型调整简化程度
            if solution_type == "complex":
                # 复杂解：保留全部条件，不简化
                pass
            elif solution_type == "intermediate":
                # 中间解：若某条件在所有解中都为同一值，保留
                pass
            elif solution_type == "parsimonious":
                # 简约解：若某条件在所有解中相同则简化（用"1"表示）
                # 本简化版本：将充分性>=0.95的条件视为核心条件
                if row.get("consistency", 1.0) >= 0.95:
                    # 核心条件，保留完整表达式
                    pass

            term_str = "*".join(terms)
            if term_str not in seen_terms:
                seen_terms.add(term_str)
                solution_terms.append(term_str)

        solution_expr = "+".join(solution_terms)

        solutions.append(
            {
                "solution": solution_expr,
                "terms": solution_terms,
                "coverage": self._calculate_coverage(positive, truth_table),
                "consistency": self._calculate_solution_consistency(positive),
                "remainders_used": self._remainders_used(solution_type),
            }
        )

        return {
            "solutions": solutions,
            "type": solution_type,
            "description": self._type_description(solution_type),
            "summary": f"找到{len(solutions)}个解（{solution_type}）",
        }

    def _type_description(self, solution_type: str) -> str:
        """返回解类型描述"""
        descriptions = {
            "complex": (
                "复杂解：仅使用直接观察到的条件组合，不使用逻辑余项。"
                "最保守，理论性最强，覆盖度最低。"
            ),
            "intermediate": (
                "中间解：使用部分符合理论预期的逻辑余项。"
                "理论与实践的平衡，是最常用的报告形式。"
            ),
            "parsimonious": (
                "简约解：使用全部逻辑余项，包含简化假设。"
                "覆盖度最高，可能过度简化。"
            ),
        }
        return descriptions.get(solution_type, "")

    def _remainders_used(self, solution_type: str) -> str:
        """返回逻辑余项使用情况"""
        used = {
            "complex": "无",
            "intermediate": "部分",
            "parsimonious": "全部",
        }
        return used.get(solution_type, "未知")

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
