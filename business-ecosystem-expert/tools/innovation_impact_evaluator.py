#!/usr/bin/env python3
"""
Innovation Impact Evaluator Tool
Evaluates innovation impact on business ecosystem using Adner's framework.
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
        return {"raw_text": content}


def evaluate_innovation_impact(data: Dict) -> Dict[str, Any]:
    """Evaluate innovation impact on ecosystem."""
    raw_text = data.get("raw_text", "")
    innovations = data.get("innovations", [])
    actors = data.get("actors", [])

    # If no structured data, analyze text
    if not innovations and raw_text:
        # Basic extraction
        innovations = [{"name": "extracted_innovation", "description": raw_text[:300]}]

    impacts = []
    for innovation in innovations:
        name = innovation.get("name", "unknown")
        desc = innovation.get("description", "").lower()

        # Evaluate different impact dimensions
        disruption_level = assess_disruption(desc)
        value_creation = assess_value_creation(desc)
        adoption_barriers = assess_barriers(desc)
        ecosystem_effects = assess_ecosystem_effects(desc)

        impacts.append(
            {
                "innovation": name,
                "disruption_level": disruption_level,
                "value_creation_potential": value_creation,
                "adoption_barriers": adoption_barriers,
                "ecosystem_effects": ecosystem_effects,
                "overall_impact_score": calculate_impact_score(
                    disruption_level, value_creation, adoption_barriers
                ),
            }
        )

    # Generate ecosystem-level summary
    if impacts:
        avg_impact = sum(i["overall_impact_score"] for i in impacts) / len(impacts)
    else:
        avg_impact = 0

    return {
        "innovation_count": len(impacts),
        "innovations": impacts,
        "ecosystem_impact_summary": {
            "average_impact_score": round(avg_impact, 2),
            "most_disruptive": max(impacts, key=lambda x: x["disruption_level"])[
                "innovation"
            ]
            if impacts
            else "N/A",
            "highest_value_creation": max(
                impacts, key=lambda x: x["value_creation_potential"]
            )["innovation"]
            if impacts
            else "N/A",
        },
        "strategic_recommendations": generate_strategic_recommendations(impacts),
    }


def assess_disruption(description: str) -> str:
    """Assess disruption level."""
    if any(
        term in description
        for term in ["disrupt", "revolution", "game-changer", "transform"]
    ):
        return "high"
    elif any(term in description for term in ["improve", "enhance", "better"]):
        return "medium"
    return "low"


def assess_value_creation(description: str) -> str:
    """Assess value creation potential."""
    if any(
        term in description for term in ["new value", "create", "generate", "benefit"]
    ):
        return "high"
    elif any(term in description for term in ["improve", "increase", "reduce"]):
        return "medium"
    return "low"


def assess_barriers(description: str) -> str:
    """Assess adoption barriers."""
    if any(
        term in description
        for term in ["complex", "expensive", "difficult", "challenge"]
    ):
        return "high"
    elif any(term in description for term in ["moderate", "some", "limited"]):
        return "medium"
    return "low"


def assess_ecosystem_effects(description: str) -> str:
    """Assess ecosystem-level effects."""
    if any(
        term in description
        for term in ["ecosystem", "network", "platform", "industry-wide"]
    ):
        return "high"
    elif any(term in description for term in ["market", "competitors", "partners"]):
        return "medium"
    return "low"


def calculate_impact_score(disruption: str, value: str, barriers: str) -> float:
    """Calculate overall impact score."""
    scores = {"low": 0.3, "medium": 0.6, "high": 1.0}

    disruption_score = scores.get(disruption, 0.5)
    value_score = scores.get(value, 0.5)
    barrier_penalty = 1.0 - (scores.get(barriers, 0.5) * 0.3)

    return round(disruption_score * 0.4 + value_score * 0.4 + barrier_penalty * 0.2, 2)


def generate_strategic_recommendations(impacts: List[Dict]) -> List[str]:
    """Generate strategic recommendations."""
    recommendations = []

    if not impacts:
        recommendations.append("No innovations identified for analysis")
        return recommendations

    high_impact = [i for i in impacts if i["overall_impact_score"] >= 0.7]
    low_barriers = [i for i in impacts if i["adoption_barriers"] == "low"]

    if high_impact:
        recommendations.append(
            f"Prioritize {len(high_impact)} high-impact innovations for ecosystem transformation"
        )

    if low_barriers:
        recommendations.append(
            f"Focus on {len(low_barriers)} innovations with low adoption barriers"
        )

    for innovation in impacts:
        if (
            innovation["disruption_level"] == "high"
            and innovation["ecosystem_effects"] == "high"
        ):
            recommendations.append(
                f"Monitor {innovation['innovation']} - high disruption with ecosystem effects"
            )

    if not recommendations:
        recommendations.append("Maintain current innovation monitoring approach")

    return recommendations


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate innovation impact on ecosystem"
    )
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = evaluate_innovation_impact(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Innovation impact analysis saved to {args.output}")
    print(f"Total innovations: {result['innovation_count']}")
    print(
        f"Average impact score: {result['ecosystem_impact_summary']['average_impact_score']}"
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
