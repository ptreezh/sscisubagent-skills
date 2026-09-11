#!/usr/bin/env python3
"""
Sampling Calculator Tool
Calculates sample size and designs sampling strategy following Fowler's methodology.
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
        return {"parameters": content}


def calculate_sample_size(data: Dict) -> Dict[str, Any]:
    """Calculate sample size using various methods."""
    params = data.get("parameters", data)

    # Extract parameters
    population = params.get("population_size", float("inf"))
    confidence_level = params.get("confidence_level", 0.95)  # 95% default
    margin_of_error = params.get("margin_of_error", 0.05)  # 5% default
    proportion = params.get("expected_proportion", 0.5)  # Most conservative

    # Calculate Z-score from confidence level
    z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    z = z_scores.get(confidence_level, 1.96)

    # Cochran's formula for infinite population
    n0 = (z**2 * proportion * (1 - proportion)) / (margin_of_error**2)

    # Adjust for finite population
    if population != float("inf") and population > 0:
        n = n0 / (1 + (n0 - 1) / population)
    else:
        n = n0

    n = math.ceil(n)

    # Calculate for subgroups if needed
    subgroups = params.get("subgroups", [])
    if subgroups:
        subgroup_sizes = []
        for sg in subgroups:
            sg_proportion = sg.get("proportion", proportion)
            sg_n = (z**2 * sg_proportion * (1 - sg_proportion)) / (margin_of_error**2)
            if population != float("inf"):
                sg_n = sg_n / (1 + (sg_n - 1) / (population * sg_proportion))
            subgroup_sizes.append(
                {
                    "subgroup": sg.get("name", "unknown"),
                    "size": math.ceil(sg_n),
                    "proportion": sg_proportion,
                }
            )
    else:
        subgroup_sizes = []

    # Determine sampling method
    sampling_method = params.get(
        "sampling_method", determine_sampling_method(population, n)
    )

    return {
        "sample_size_calculation": {
            "method": "Cochran's Formula",
            "confidence_level": confidence_level,
            "margin_of_error": margin_of_error,
            "expected_proportion": proportion,
            "population_size": population
            if population != float("inf")
            else "Infinite/unknown",
        },
        "recommended_sample_size": n,
        "sampling_method": sampling_method,
        "subgroup_analysis": subgroup_sizes,
        "recommendations": generate_recommendations(n, population, sampling_method),
    }


def determine_sampling_method(population: float, sample_size: int) -> str:
    """Determine appropriate sampling method."""
    if population < 1000:
        return "census"  # Small population - census
    elif sample_size < 30:
        return "purposive"  # Very small sample
    elif sample_size < 100:
        return "simple_random"  # Small sample
    else:
        return "stratified_random"  # Larger sample - can stratify


def generate_recommendations(n: int, population: float, method: str) -> List[str]:
    """Generate sampling recommendations."""
    recommendations = []

    recommendations.append(f"Use {method} sampling with n={n}")

    if n < 50:
        recommendations.append("Warning: Small sample size may limit statistical power")

    if population != float("inf") and n / population > 0.1:
        recommendations.append("Consider finite population correction")

    if method == "stratified_random":
        recommendations.append("Ensure each stratum has adequate representation")

    recommendations.append("Plan for 20% oversample to account for non-response")

    return recommendations


def main():
    parser = argparse.ArgumentParser(description="Calculate survey sample size")
    parser.add_argument("-i", "--input", required=True, help="Input parameters file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = calculate_sample_size(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Sampling calculation saved to {args.output}")
    print(f"Recommended sample size: {result['recommended_sample_size']}")
    print(f"Sampling method: {result['sampling_method']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
