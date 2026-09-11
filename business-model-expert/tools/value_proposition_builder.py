#!/usr/bin/env python3
"""
Value Proposition Builder Tool
Builds and analyzes value propositions following Osterwalder's methodology.
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
        return {"product_service": content}


def build_value_proposition(data: Dict) -> Dict[str, Any]:
    """Build value proposition."""
    product_service = data.get("product_service", data.get("value_proposition", ""))
    customer_jobs = data.get("customer_jobs", [])
    pain_points = data.get("pain_points", [])
    gain_creators = data.get("gain_creators", [])

    # Build value proposition canvas components
    customer_profile = {
        "customer_jobs": customer_jobs or generate_customer_jobs(product_service),
        "pains": pain_points or ["[Identify customer pain points]"],
        "gains": ["[Identify customer gains]"],
    }

    value_map = {
        "products_services": [product_service]
        if product_service
        else ["[Define your product/service]"],
        "pain_relievers": ["[How you solve pains]"],
        "gain_creators": gain_creators or ["[How you create gains]"],
    }

    # Generate value proposition statement
    statement = generate_value_statement(
        value_map.get("products_services", [""])[0],
        customer_profile.get("pains", [""])[0],
        customer_profile.get("gains", [""])[0],
    )

    return {
        "value_proposition": statement,
        "customer_profile": customer_profile,
        "value_map": value_map,
        "fit_assessment": assess_fit(customer_profile, value_map),
        "recommendations": generate_vp_recommendations(customer_profile, value_map),
    }


def generate_customer_jobs(product: str) -> List[str]:
    """Generate customer jobs."""
    if not product:
        return ["[Define customer jobs]"]
    return [f"Customer needs related to: {product[:30]}"]


def generate_value_statement(product: str, pain: str, gain: str) -> str:
    """Generate value proposition statement."""
    if not product:
        return "[Your value proposition]"

    return f"For [target customer] who [need/job], our [product] is [category] that [key benefit]. Unlike [competitor], our solution [key differentiator]."


def assess_fit(profile: Dict, value_map: Dict) -> Dict[str, Any]:
    """Assess value proposition fit."""
    # Check if all components are filled
    all_filled = True
    for section in list(profile.values()) + list(value_map.values()):
        if isinstance(section, list):
            if not section or any("[Define" in str(s) for s in section):
                all_filled = False

    return {
        "fit_level": "good" if all_filled else "needs_work",
        "profile_complete": bool(profile.get("customer_jobs")),
        "value_map_complete": bool(value_map.get("products_services")),
    }


def generate_vp_recommendations(profile: Dict, value_map: Dict) -> List[str]:
    """Generate value proposition recommendations."""
    recommendations = []

    if not profile.get("customer_jobs"):
        recommendations.append("Define customer jobs first")

    if not value_map.get("products_services") or "[Define" in str(
        value_map.get("products_services", [""])[0]
    ):
        recommendations.append("Clarify your product/service offering")

    if profile.get("pains") and "[Identify" in str(profile.get("pains", [""])[0]):
        recommendations.append("Identify specific customer pain points")

    if not recommendations:
        recommendations.append("Value proposition looks well-structured")

    return recommendations


def main():
    parser = argparse.ArgumentParser(description="Build value proposition")
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = build_value_proposition(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Value proposition saved to {args.output}")
    print(f"Value proposition: {result['value_proposition'][:50]}...")

    return 0


if __name__ == "__main__":
    sys.exit(main())
