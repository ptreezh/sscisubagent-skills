#!/usr/bin/env python3
"""
Reliability Analyzer Tool
Analyzes survey reliability including Cronbach's alpha and test-retest reliability.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def load_input_data(input_path: str) -> Dict[str, Any]:
    """Load input data from file."""
    path = Path(input_path)
    if not path.exists():
        return {}

    if path.suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"items": [{"name": "item1", "data": content}]}


def calculate_cronbach_alpha(data: Dict) -> Dict[str, Any]:
    """Calculate Cronbach's alpha for reliability."""
    items = data.get("items", [])
    responses = data.get("responses", [])

    if not items and "data" in data:
        # Try to extract from raw data
        return {
            "reliability_type": "cronbach_alpha",
            "result": "requires_pilot_data",
            "note": "Need structured response data for calculation",
        }

    if not responses:
        return {
            "reliability_type": "cronbach_alpha",
            "alpha": None,
            "interpretation": "No response data available",
        }

    # Calculate Cronbach's alpha
    n_items = len(responses[0]) if responses else 0
    if n_items < 2:
        return {
            "reliability_type": "cronbach_alpha",
            "alpha": None,
            "interpretation": "Need at least 2 items",
        }

    # Calculate variance for each item
    item_variances = []
    for i in range(n_items):
        item_scores = [r[i] for r in responses]
        mean = sum(item_scores) / len(item_scores)
        variance = sum((x - mean) ** 2 for x in item_scores) / len(item_scores)
        item_variances.append(variance)

    # Calculate total variance
    total_scores = [sum(r) for r in responses]
    total_mean = sum(total_scores) / len(total_scores)
    total_variance = sum((x - total_mean) ** 2 for x in total_scores) / len(
        total_scores
    )

    # Calculate alpha
    if total_variance > 0:
        alpha = (n_items / (n_items - 1)) * (1 - sum(item_variances) / total_variance)
    else:
        alpha = 0

    # Interpret alpha
    interpretation = interpret_alpha(alpha)

    return {
        "reliability_type": "cronbach_alpha",
        "n_items": n_items,
        "n_responses": len(responses),
        "alpha": round(alpha, 3),
        "interpretation": interpretation,
        "is_reliable": alpha >= 0.7,
        "recommendations": generate_reliability_recommendations(alpha, n_items),
    }


def interpret_alpha(alpha: float) -> str:
    """Interpret Cronbach's alpha value."""
    if alpha >= 0.9:
        return "Excellent reliability"
    elif alpha >= 0.8:
        return "Good reliability"
    elif alpha >= 0.7:
        return "Acceptable reliability"
    elif alpha >= 0.6:
        return "Questionable reliability"
    elif alpha >= 0.5:
        return "Poor reliability"
    else:
        return "Unacceptable reliability"


def generate_reliability_recommendations(alpha: float, n_items: int) -> List[str]:
    """Generate reliability recommendations."""
    recommendations = []

    if alpha < 0.7:
        recommendations.append("Consider adding more items to the scale")
        recommendations.append("Review items for consistency")
        recommendations.append("Check if items measure the same construct")

    if alpha > 0.95:
        recommendations.append("Possible redundancy - some items may be too similar")

    if n_items < 5:
        recommendations.append("Consider adding more items (minimum 5 recommended)")

    if alpha >= 0.7:
        recommendations.append("Scale has acceptable internal consistency")

    return recommendations


def main():
    parser = argparse.ArgumentParser(description="Analyze survey reliability")
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = calculate_cronbach_alpha(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Reliability analysis saved to {args.output}")
    if result.get("alpha") is not None:
        print(f"Cronbach's alpha: {result['alpha']}")
        print(f"Interpretation: {result['interpretation']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
