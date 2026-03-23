#!/usr/bin/env python3
"""
Platform Dynamics Analyzer Tool
Analyzes platform dynamics and network effects in business ecosystems.
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


def analyze_network_effects(data: Dict) -> Dict[str, Any]:
    """Analyze network effects in the platform."""
    raw_text = data.get("raw_text", "")
    actors = data.get("actors", [])

    # Analyze different types of network effects
    effects = {
        "direct_network_effects": [],
        "indirect_network_effects": [],
        "data_network_effects": [],
        "learning_network_effects": [],
    }

    # Check for mentions of network effects in text
    text_lower = raw_text.lower()

    if any(
        term in text_lower
        for term in ["more users", "more buyers", "more sellers", "direct effect"]
    ):
        effects["direct_network_effects"].append(
            {
                "type": "same-side",
                "description": "Direct network effect detected",
                "strength": "medium",
            }
        )

    if any(
        term in text_lower
        for term in ["two-sided", "cross-side", "complement", "ecosystem"]
    ):
        effects["indirect_network_effects"].append(
            {
                "type": "cross-side",
                "description": "Indirect network effect detected",
                "strength": "high",
            }
        )

    if any(term in text_lower for term in ["data", "learning", "ai", "algorithm"]):
        effects["data_network_effects"].append(
            {
                "type": "data-driven",
                "description": "Data network effect detected",
                "strength": "medium",
            }
        )

    # Calculate platform metrics if actors data available
    platform_metrics = {}
    if actors:
        try:
            user_count = sum(int(a.get("users", a.get("count", 0))) for a in actors)
            platform_metrics["total_users"] = user_count
            platform_metrics["platform_concentration"] = (
                "high" if len(actors) < 5 else "low"
            )
        except:
            pass

    return {
        "network_effects_detected": effects,
        "platform_metrics": platform_metrics,
        "effectiveness": {
            "has_direct_effects": len(effects["direct_network_effects"]) > 0,
            "has_indirect_effects": len(effects["indirect_network_effects"]) > 0,
            "has_data_effects": len(effects["data_network_effects"]) > 0,
            "overall_strength": "strong"
            if sum(len(v) for v in effects.values()) >= 3
            else "moderate",
        },
        "recommendations": generate_recommendations(effects),
    }


def generate_recommendations(effects: Dict) -> List[str]:
    """Generate recommendations based on network effects analysis."""
    recommendations = []

    if not effects["direct_network_effects"]:
        recommendations.append(
            "Consider strategies to increase same-side network effects"
        )

    if not effects["indirect_network_effects"]:
        recommendations.append(
            "Strengthen cross-side network effects through complementor support"
        )

    if not effects["data_network_effects"]:
        recommendations.append("Leverage data and learning for competitive advantage")

    return recommendations


def main():
    parser = argparse.ArgumentParser(description="Analyze platform dynamics")
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = analyze_network_effects(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Platform dynamics analysis saved to {args.output}")
    print(f"Network effects strength: {result['effectiveness']['overall_strength']}")
    print(f"Recommendations: {len(result['recommendations'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
