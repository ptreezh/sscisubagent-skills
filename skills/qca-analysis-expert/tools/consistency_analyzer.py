#!/usr/bin/env python3
"""
Consistency Analyzer Tool
Analyzes consistency and PRI (Proportional Reduced Inclusion) of set relations in QCA.
Implements Ragin (2006) consistency/coverage + PRI (Skaaning 2021) standards.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List


def load_input(path: str) -> Dict:
    p = Path(path)
    if p.suffix == ".json":
        with open(p) as f:
            return json.load(f)
    return {"data": []}


def calculate_raw_consistency(subset: List[Dict], full: List[Dict]) -> float:
    """
    Raw consistency: proportion of subset cases that are also in full set.
    consistency(X→Y) = |X∩Y| / |X|
    """
    if not subset:
        return 0.0
    subset_sum = sum(row.get("n", 1) for row in subset)
    full_sum = sum(row.get("n", 1) for row in full)
    if full_sum == 0:
        return 0.0
    return min(subset_sum / full_sum, 1.0)


def calculate_coverage(subset: List[Dict], full: List[Dict]) -> float:
    """
    Coverage: proportion of full set explained by subset.
    coverage(X→Y) = |X∩Y| / |Y|
    """
    subset_sum = sum(row.get("n", 1) for row in subset)
    full_sum = sum(row.get("n", 1) for row in full)
    if full_sum == 0:
        return 0.0
    return min(subset_sum / full_sum, 1.0)


def calculate_pri_consistency(
    subset: List[Dict], full: List[Dict], negative: List[Dict]
) -> float:
    """
    PRI (Proportional Reduced Inclusion) consistency.
    Addresses 'limited diversity' problem by penalizing conditions that
    appear frequently when the outcome is absent.

    Formula: PRI = (consistency - exclusion) / (1 - exclusion)
    Where exclusion = |X∩~Y| / |X|

    Simplified (Skaaning 2021):
    PRI = (|X∩Y| - |X∩~Y|) / |X|
        = (consistency - exclusion_ratio)
    """
    if not subset:
        return 0.0
    subset_sum = sum(row.get("n", 1) for row in subset)
    if subset_sum == 0:
        return 0.0

    # Cases where condition present but outcome absent
    exclusion_sum = sum(row.get("n", 1) for row in negative)

    # PRI: (subset_in_outcome - subset_in_negative) / subset_total
    pri = (subset_sum - exclusion_sum) / subset_sum
    return max(0.0, min(pri, 1.0))


def analyze_necessity(
    condition: str, calibrated: Dict, outcome_col: str
) -> Dict:
    """
    Analyze whether a condition is necessary for the outcome.
    Returns consistency of necessity and coverage of necessity.
    """
    data = calibrated.get("data", calibrated)
    outcome_present = [r for r in data if r.get(outcome_col, 0) > 0.5]
    condition_present = [r for r in data if r.get(condition, 0) > 0.5]

    # Necessity: outcome → condition (when outcome present, condition should be)
    # consistency = |Y∩X| / |Y|
    if not outcome_present:
        return {"consistency": 0.0, "coverage": 0.0, "is_necessary": False}

    intersection = [r for r in outcome_present if r.get(condition, 0) > 0.5]
    necessity_consistency = calculate_raw_consistency(intersection, outcome_present)
    necessity_coverage = calculate_coverage(intersection, condition_present)

    return {
        "consistency": round(necessity_consistency, 4),
        "coverage": round(necessity_coverage, 4),
        "is_necessary": necessity_consistency >= 0.9,
    }


def analyze_sufficiency(
    condition: str, calibrated: Dict, outcome_col: str
) -> Dict:
    """
    Analyze whether a condition is sufficient for the outcome.
    Returns consistency and coverage of sufficiency, plus PRI.
    """
    data = calibrated.get("data", calibrated)
    outcome_present = [r for r in data if r.get(outcome_col, 0) > 0.5]
    condition_present = [r for r in data if r.get(condition, 0) > 0.5]
    condition_absent_neg = [r for r in data if r.get(condition, 0) <= 0.5]

    # Sufficiency: condition → outcome (when condition present, outcome should be)
    # consistency = |X∩Y| / |X|
    intersection = [r for r in condition_present if r.get(outcome_col, 0) > 0.5]
    sufficiency_consistency = calculate_raw_consistency(intersection, condition_present)
    sufficiency_coverage = calculate_coverage(intersection, outcome_present)

    # PRI for sufficiency
    outcome_absent = [r for r in data if r.get(outcome_col, 0) <= 0.5]
    neg_for_pri = [r for r in condition_present if r.get(outcome_col, 0) <= 0.5]
    pri = calculate_pri_consistency(condition_present, outcome_present, neg_for_pri)

    return {
        "consistency": round(sufficiency_consistency, 4),
        "coverage": round(sufficiency_coverage, 4),
        "pri": round(pri, 4),
        "is_sufficient": sufficiency_consistency >= 0.75,
        "interpretation": _interpret_pri(pri),
    }


# 废弃：定性解释由LLM基于理论原则完成
# Python仅提供原始数值，LLM结合Skaaning(2021)标准做实质性判断
METHODOLOGY_MEMO = """【QCA PRI解释原则 - LLM专属判断】
PRI (Proportional Reduced Inclusion) 由Skaaning(2021)提出，用于解决"有限多样性"问题。
- PRI > 0.50 表示负介入程度可接受，路径可纳入解公式
- 但PRI阈值本身不是绝对标准，需结合consistency和coverage综合判断
- "实质一致性"需要研究者根据案例质量和理论背景评估
- 0.50 < PRI < 0.75 时，路径是否纳入需LLM做实质性判断（不是机械阈值判断）
- 禁止：仅因PRI < 0.50 就自动判定"不适合纳入解公式"
"""


def _interpret_pri(pri: float) -> str:
    """
    废弃硬编码解释，改由LLM做实质性判断。
    本函数仅返回原始值 + methodology memo。
    """
    return None  # LLM填充


def analyze_consistency(data: Dict, outcome_col: str = "outcome") -> Dict:
    """
    Main consistency analysis function.
    Analyzes all conditions for necessity and sufficiency with PRI.
    """
    conditions = set()
    raw_data = data.get("data", data)
    for row in raw_data:
        for k in row.keys():
            if k not in (outcome_col, "n", "id", "case"):
                conditions.add(k)

    results = {
        "parameters": {
            "consistency_threshold_necessity": 0.9,
            "consistency_threshold_sufficiency": 0.75,
            "pri_threshold": 0.50,
        },
        "necessity_analysis": [],
        "sufficiency_analysis": [],
    }

    for cond in sorted(conditions):
        necessity = analyze_necessity(cond, {"data": raw_data}, outcome_col)
        sufficiency = analyze_sufficiency(cond, {"data": raw_data}, outcome_col)

        results["necessity_analysis"].append(
            {
                "condition": cond,
                "consistency": necessity["consistency"],
                "coverage": necessity["coverage"],
                "is_necessary": necessity["is_necessary"],
            }
        )

        results["sufficiency_analysis"].append(
            {
                "condition": cond,
                "consistency": sufficiency["consistency"],
                "coverage": sufficiency["coverage"],
                "pri": sufficiency["pri"],
                "interpretation": None,  # LLM基于methodology_memo填充
                "is_sufficient": sufficiency["is_sufficient"],
            }
        )

    # Methodology guidance for LLM
    results["methodology_memo"] = METHODOLOGY_MEMO

    # Summary
    necessary = [r["condition"] for r in results["necessity_analysis"] if r["is_necessary"]]
    sufficient = [r["condition"] for r in results["sufficiency_analysis"] if r["is_sufficient"]]
    high_pri = [r["condition"] for r in results["sufficiency_analysis"] if r["pri"] >= 0.5]

    results["summary"] = {
        "necessary_conditions": necessary,
        "sufficient_conditions": sufficient,
        "high_pri_conditions": high_pri,
        "total_conditions_analyzed": len(conditions),
    }

    return results


def main():
    parser = argparse.ArgumentParser(
        description="QCA一致性分析工具（支持PRI）"
    )
    parser.add_argument("-i", "--input", required=True, help="校准后JSON数据")
    parser.add_argument("-o", "--output", required=True, help="输出JSON结果")
    parser.add_argument(
        "--outcome", default="outcome", help="结果变量列名（默认: outcome）"
    )
    parser.add_argument(
        "--pri", action="store_true", help="输出PRI一致性分析"
    )
    args = parser.parse_args()

    data = load_input(args.input)
    result = analyze_consistency(data, args.outcome)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"分析完成: {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
