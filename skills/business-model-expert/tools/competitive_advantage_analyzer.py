#!/usr/bin/env python3
"""
Competitive Advantage Analyzer Tool
Analyzes competitive advantage using Porter's framework.
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
        return {"business_idea": content}


def analyze_competitive_advantage(data: Dict) -> Dict[str, Any]:
    """Analyze competitive advantage."""
    business_idea = data.get("business_idea", "")
    competitors = data.get("competitors", [])

    # Porter's generic strategies
    strategies = [
        {
            "strategy": "cost_leadership",
            "description": "Become lowest cost producer",
            "requirements": [
                "Economies of scale",
                "Efficient processes",
                "Cost control",
            ],
            "risks": ["Technology changes", "Price wars", "Learning curve"],
        },
        {
            "strategy": "differentiation",
            "description": "Offer unique value",
            "requirements": ["R&D investment", "Brand strength", "Innovation culture"],
            "risks": [
                "Imitation",
                "Customer preference shifts",
                "Premium pricing limits",
            ],
        },
        {
            "strategy": "focus",
            "description": "Target specific niche",
            "requirements": [
                "Deep market knowledge",
                "Specialization",
                "Niche relationships",
            ],
            "risks": [
                "Niche shrinkage",
                "Broad competitors entering",
                "Segment shifts",
            ],
        },
    ]

    # Identify sources of competitive advantage
    sources = [
        {"source": "technology", "description": "Proprietary technology or patents"},
        {"source": "brand", "description": "Strong brand recognition"},
        {"source": "network_effects", "description": "Platform/network effects"},
        {"source": "switching_costs", "description": "High customer switching costs"},
        {"source": "economies_scale", "description": "Scale advantages"},
        {"source": "unique_resources", "description": "Exclusive access to resources"},
    ]

    # Competitive forces analysis
    forces = {
        "threat_new_entrants": {
            "level": "medium",
            "factors": ["Barriers to entry", "Capital requirements"],
        },
        "bargaining_suppliers": {
            "level": "medium",
            "factors": ["Supplier concentration", "Switching costs"],
        },
        "bargaining_buyers": {
            "level": "medium",
            "factors": ["Buyer concentration", "Price sensitivity"],
        },
        "threat_substitutes": {
            "level": "medium",
            "factors": ["Substitute availability", "Perceived value"],
        },
        "competitive_rivalry": {
            "level": "high",
            "factors": ["Number of competitors", "Industry growth"],
        },
    }

    return {
        "generic_strategies": strategies,
        "advantage_sources": sources,
        "competitive_forces": forces,
        "recommended_strategy": recommend_strategy(business_idea, sources),
        "sustainability_assessment": assess_sustainability(sources),
        "recommendations": generate_advantage_recommendations(sources, forces),
    }


def recommend_strategy(idea: str, sources: List[Dict]) -> str:
    """Recommend competitive strategy."""
    if not idea:
        return "differentiation"  # Default

    # Simple heuristic
    idea_lower = idea.lower()
    if any(term in idea_lower for term in ["price", "cheap", "cost", "discount"]):
        return "cost_leadership"
    elif any(term in idea_lower for term in ["unique", "premium", "innovative", "new"]):
        return "differentiation"

    return "differentiation"  # Most common for new ventures


def assess_sustainability(sources: List[Dict]) -> Dict[str, Any]:
    """Assess sustainability of competitive advantage."""
    return {
        "sustainability_score": 0.6,  # Placeholder
        "barriers_to_imitation": ["Medium - competitors can copy"],
        "duration_estimate": "2-5 years without protection",
        "moat_strength": "moderate",
    }


def generate_advantage_recommendations(sources: List[Dict], forces: Dict) -> List[str]:
    """Generate competitive advantage recommendations."""
    recommendations = []

    if not sources:
        recommendations.append("Identify clear sources of competitive advantage")

    # Check competitive forces
    high_forces = [k for k, v in forces.items() if v.get("level") == "high"]
    if high_forces:
        recommendations.append(
            f"Address high competitive pressure in: {', '.join(high_forces)}"
        )

    recommendations.append("Build sustainable competitive advantages")
    recommendations.append("Continuously innovate to maintain differentiation")

    return recommendations


def main():
    parser = argparse.ArgumentParser(description="Analyze competitive advantage")
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = analyze_competitive_advantage(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Competitive advantage analysis saved to {args.output}")
    print(f"Recommended strategy: {result['recommended_strategy']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
