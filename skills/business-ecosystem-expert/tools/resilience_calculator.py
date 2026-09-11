#!/usr/bin/env python3
"""
Ecosystem Resilience Calculator Tool
Calculates ecosystem resilience using Adner's Innovation Ecosystem framework.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any
import math


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
        return {"raw_text": content}


def calculate_resilience_metrics(data: Dict) -> Dict[str, Any]:
    """Calculate ecosystem resilience metrics."""
    actors = data.get("actors", [])
    dependencies = data.get("dependencies", [])
    raw_text = data.get("raw_text", "")

    # Calculate redundancy (multiple actors can fulfill same function)
    redundancy_score = 0.5  # Default

    # Calculate diversity (variety of actor types)
    if actors:
        roles = set(a.get("role", a.get("type", "")) for a in actors)
        diversity_score = min(len(roles) / 5.0, 1.0)  # Normalize to 0-1
    else:
        diversity_score = 0.3

    # Calculate connectivity (interdependence)
    if dependencies:
        dep_count = sum(len(d) for d in dependencies.values())
        connectivity_score = min(dep_count / 20.0, 1.0)
    else:
        connectivity_score = 0.4

    # Calculate robustness (ability to withstand shocks)
    text_lower = raw_text.lower()
    robustness_factors = {
        "backup_systems": "backup" in text_lower or "redundancy" in text_lower,
        "diversified_revenue": "diversified" in text_lower or "multiple" in text_lower,
        "strong_partnerships": "partnership" in text_lower or "alliance" in text_lower,
        "financial_reserves": "reserve" in text_lower or "cash" in text_lower,
    }
    robustness_score = sum(robustness_factors.values()) / len(robustness_factors)

    # Calculate recovery capability
    recovery_factors = {
        "has_contingency": "contingency" in text_lower or "contingency" in text_lower,
        "has_alternatives": "alternative" in text_lower or "backup" in text_lower,
        "adaptive_capacity": "adapt" in text_lower or "flexible" in text_lower,
    }
    recovery_score = sum(recovery_factors.values()) / len(recovery_factors)

    # Calculate overall resilience score (weighted average)
    resilience_score = (
        redundancy_score * 0.2
        + diversity_score * 0.25
        + connectivity_score * 0.15
        + robustness_score * 0.25
        + recovery_score * 0.15
    )

    # Determine resilience level
    if resilience_score >= 0.7:
        resilience_level = "high"
    elif resilience_score >= 0.5:
        resilience_level = "moderate"
    else:
        resilience_level = "low"

    return {
        "resilience_score": round(resilience_score, 3),
        "resilience_level": resilience_level,
        "component_scores": {
            "redundancy": round(redundancy_score, 3),
            "diversity": round(diversity_score, 3),
            "connectivity": round(connectivity_score, 3),
            "robustness": round(robustness_score, 3),
            "recovery": round(recovery_score, 3),
        },
        "risk_factors": identify_risks(data),
        "improvement_suggestions": generate_suggestions(
            robustness_factors, recovery_factors
        ),
    }


def identify_risks(data: Dict) -> List[Dict]:
    """Identify ecosystem risks."""
    risks = []
    dependencies = data.get("dependencies", {})
    actors = data.get("actors", [])

    # Single point of failure risks
    if dependencies:
        for actor, deps in dependencies.items():
            if len(deps) == 0 and len(actors) > 3:
                risks.append(
                    {
                        "type": "single_point_of_failure",
                        "actor": actor,
                        "severity": "high",
                        "description": f"{actor} has no dependencies - may be isolated",
                    }
                )

    return risks


def generate_suggestions(robustness: Dict, recovery: Dict) -> List[str]:
    """Generate improvement suggestions."""
    suggestions = []

    if not robustness.get("backup_systems"):
        suggestions.append("Implement backup systems for critical functions")
    if not robustness.get("diversified_revenue"):
        suggestions.append("Diversify revenue streams to reduce dependency")
    if not robustness.get("strong_partnerships"):
        suggestions.append("Strengthen partnerships and alliances")
    if not recovery.get("has_contingency"):
        suggestions.append("Develop contingency plans for disruptions")
    if not recovery.get("adaptive_capacity"):
        suggestions.append("Build adaptive capacity for rapid response")

    if not suggestions:
        suggestions.append("Ecosystem resilience is well-managed")

    return suggestions


def main():
    parser = argparse.ArgumentParser(description="Calculate ecosystem resilience")
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = calculate_resilience_metrics(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Resilience analysis saved to {args.output}")
    print(
        f"Resilience score: {result['resilience_score']} ({result['resilience_level']})"
    )
    print(f"Improvement suggestions: {len(result['improvement_suggestions'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
