#!/usr/bin/env python3
"""
Revenue Model Analyzer Tool
Analyzes revenue streams and pricing models.
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
        return {"business_model": content}


def analyze_revenue_model(data: Dict) -> Dict[str, Any]:
    """Analyze revenue model."""
    business_model = data.get("business_model", "")
    revenue_streams = data.get("revenue_streams", [])
    pricing = data.get("pricing", {})

    # Define revenue stream types
    revenue_types = [
        {
            "type": "asset_sale",
            "name": "Asset Sale",
            "description": "Selling ownership of physical/digital products",
        },
        {
            "type": "usage_fee",
            "name": "Usage Fee",
            "description": "Charging for service usage",
        },
        {
            "type": "subscription",
            "name": "Subscription",
            "description": "Recurring revenue from ongoing access",
        },
        {
            "type": "licensing",
            "name": "Licensing",
            "description": "Revenue from allowing use of IP/technology",
        },
        {
            "type": "commission",
            "name": "Commission",
            "description": "Taking percentage of transactions",
        },
        {
            "type": "advertising",
            "name": "Advertising",
            "description": "Revenue from ads displayed",
        },
    ]

    # Identify applicable revenue streams
    if not revenue_streams and business_model:
        identified = ["[Identify from business model]"]
    else:
        identified = revenue_streams or ["Subscription", "Usage Fee"]

    # Pricing mechanisms
    pricing_mechanisms = [
        {"type": "fixed", "description": "Fixed price"},
        {"type": "volume", "description": "Volume-based pricing"},
        {"type": "tiered", "description": "Tiered pricing"},
        {"type": "dynamic", "description": "Dynamic/auction pricing"},
        {"type": "freemium", "description": "Free + premium features"},
    ]

    return {
        "revenue_streams": identified,
        "revenue_types": revenue_types,
        "pricing_mechanisms": pricing_mechanisms,
        "revenue_diversity": {
            "count": len(identified),
            "diversified": len(identified) >= 3,
            "recommendation": "Diversify revenue streams"
            if len(identified) < 3
            else "Good revenue diversity",
        },
        "pricing_recommendations": generate_pricing_recommendations(
            identified, pricing
        ),
        "sustainability_assessment": assess_sustainability(identified),
    }


def generate_pricing_recommendations(streams: List[str], pricing: Dict) -> List[str]:
    """Generate pricing recommendations."""
    recommendations = []

    if len(streams) < 2:
        recommendations.append("Consider adding multiple revenue streams")

    if "Subscription" in streams:
        recommendations.append("Focus on reducing churn for subscription revenue")

    if "Usage Fee" in streams:
        recommendations.append("Monitor usage patterns and optimize pricing")

    return recommendations


def assess_sustainability(streams: List[str]) -> Dict[str, Any]:
    """Assess revenue sustainability."""
    return {
        "recurring_potential": "Subscription" in streams or "Usage Fee" in streams,
        "scalability": "Licensing" in streams or "Digital" in str(streams),
        "risk_level": "high" if len(streams) < 2 else "moderate",
    }


def main():
    parser = argparse.ArgumentParser(description="Analyze revenue model")
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = analyze_revenue_model(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Revenue analysis saved to {args.output}")
    print(f"Revenue streams identified: {result['revenue_diversity']['count']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
