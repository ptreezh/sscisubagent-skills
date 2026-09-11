#!/usr/bin/env python3
"""
Scale Validator Tool
Validates survey measurement scales (Likert, semantic differential, etc.).
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
        return {"scales": [{"name": "scale1", "raw_data": content}]}


def validate_scale(data: Dict) -> Dict[str, Any]:
    """Validate measurement scales."""
    scales = data.get("scales", [])

    if not scales and "raw_text" in data:
        scales = [{"name": "default", "raw_data": data["raw_text"]}]

    results = []
    for scale in scales:
        scale_name = scale.get("name", "unknown")
        responses = scale.get("responses", [])
        raw_data = scale.get("raw_data", "")

        # If no structured responses, analyze raw data
        if not responses and raw_data:
            # Basic analysis
            scale_info = {
                "name": scale_name,
                "type": "analyzed_from_text",
                "is_valid": True,
                "recommendations": ["Requires pilot testing for full validation"],
            }
        else:
            # Full statistical validation
            if len(responses) < 2:
                scale_info = {
                    "name": scale_name,
                    "type": "unknown",
                    "is_valid": False,
                    "error": "Insufficient response data",
                }
            else:
                # Basic statistics
                mean = sum(responses) / len(responses)
                variance = sum((x - mean) ** 2 for x in responses) / len(responses)
                std_dev = variance**0.5

                scale_info = {
                    "name": scale_name,
                    "type": scale.get("type", "likert"),
                    "n_responses": len(responses),
                    "mean": round(mean, 2),
                    "std_dev": round(std_dev, 2),
                    "min": min(responses),
                    "max": max(responses),
                    "is_valid": std_dev > 0,
                    "recommendations": generate_scale_recommendations(
                        std_dev, len(responses)
                    ),
                }

        results.append(scale_info)

    return {
        "scales_validated": len(results),
        "valid_scales": [s for s in results if s.get("is_valid", False)],
        "invalid_scales": [s for s in results if not s.get("is_valid", True)],
        "scale_details": results,
    }


def generate_scale_recommendations(std_dev: float, n: int) -> List[str]:
    """Generate scale validation recommendations."""
    recommendations = []

    if std_dev == 0:
        recommendations.append("No variance - all responses are the same")
        recommendations.append("Consider revising the question")
    elif std_dev < 0.5:
        recommendations.append(
            "Low variance - consider if question is too easy/difficult"
        )
    elif std_dev > 2.0:
        recommendations.append("High variance - check for ambiguous wording")

    if n < 30:
        recommendations.append(
            "Small sample - need more responses for robust validation"
        )

    if std_dev > 0.5 and std_dev < 2.0:
        recommendations.append("Scale shows good variance")

    return recommendations


def main():
    parser = argparse.ArgumentParser(description="Validate survey scales")
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = validate_scale(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Scale validation saved to {args.output}")
    print(f"Scales validated: {result['scales_validated']}")
    print(f"Valid scales: {len(result['valid_scales'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
