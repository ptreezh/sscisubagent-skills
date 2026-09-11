#!/usr/bin/env python3
"""
Cost Structure Calculator Tool
Calculates and analyzes business cost structure.
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
        return {"business_operations": content}


def calculate_cost_structure(data: Dict) -> Dict[str, Any]:
    """Calculate cost structure."""
    business_ops = data.get("business_operations", "")
    costs = data.get("costs", [])

    # Define cost categories
    fixed_costs = [
        {"category": "Rent", "description": "Physical space costs"},
        {"category": "Salaries", "description": "Fixed personnel costs"},
        {"category": "Insurance", "description": "Business insurance"},
        {"category": "Software Licenses", "description": "Fixed software costs"},
    ]

    variable_costs = [
        {"category": "Raw Materials", "description": "Direct material costs"},
        {"category": "Shipping", "description": "Delivery costs"},
        {"category": "Sales Commission", "description": "Sales-based costs"},
        {"category": "Utilities", "description": "Usage-based costs"},
    ]

    # Calculate structure type
    structure_type = determine_structure_type(costs, business_ops)

    return {
        "fixed_costs": fixed_costs,
        "variable_costs": variable_costs,
        "structure_type": structure_type,
        "cost_optimization": identify_optimization_opportunities(
            fixed_costs, variable_costs
        ),
        "break_even_analysis": estimate_break_even(costs),
        "recommendations": generate_cost_recommendations(structure_type),
    }


def determine_structure_type(costs: List, business_ops: str) -> str:
    """Determine cost structure type."""
    if not costs and not business_ops:
        return "cost_driven"  # Default assumption

    if business_ops:
        ops_lower = business_ops.lower()
        if "manufacturing" in ops_lower or "production" in ops_lower:
            return "value_driven"  # Manufacturing typically cost-focused
        elif "software" in ops_lower or "service" in ops_lower:
            return "value_driven"  # Service typically value-focused

    return "balanced"


def identify_optimization_opportunities(fixed: List, variable: List) -> List[Dict]:
    """Identify cost optimization opportunities."""
    opportunities = [
        {
            "area": "Fixed Costs",
            "opportunity": "Consider remote work to reduce rent",
            "impact": "medium",
        },
        {
            "area": "Variable Costs",
            "opportunity": "Negotiate supplier contracts",
            "impact": "high",
        },
        {
            "area": "Technology",
            "opportunity": "Automate repetitive tasks",
            "impact": "medium",
        },
    ]
    return opportunities


def estimate_break_even(costs: List) -> Dict[str, Any]:
    """Estimate break-even point."""
    # Placeholder for break-even calculation
    return {
        "fixed_costs_estimate": "[Calculate from data]",
        "price_per_unit": "[Enter price]",
        "variable_cost_per_unit": "[Enter cost]",
        "break_even_units": "[Calculate: FC / (P - VC)]",
    }


def generate_cost_recommendations(structure_type: str) -> List[str]:
    """Generate cost recommendations."""
    recommendations = []

    if structure_type == "cost_driven":
        recommendations.append("Focus on cost optimization and efficiency")
        recommendations.append("Consider economies of scale")

    if structure_type == "value_driven":
        recommendations.append("Focus on value creation over cost cutting")
        recommendations.append("Invest in differentiation")

    recommendations.append("Regularly review and optimize cost structure")

    return recommendations


def main():
    parser = argparse.ArgumentParser(description="Calculate cost structure")
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = calculate_cost_structure(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Cost structure analysis saved to {args.output}")
    print(f"Structure type: {result['structure_type']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
