#!/usr/bin/env python3
"""
Business Model Canvas Designer Tool
Designs business models using Osterwalder's Business Model Canvas.
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


def design_canvas(data: Dict) -> Dict[str, Any]:
    """Design Business Model Canvas."""
    business_idea = data.get("business_idea", data.get("description", ""))

    # Generate canvas structure with placeholders
    canvas = {
        "value_propositions": {
            "title": "Value Propositions",
            "description": "Value delivered to customers",
            "elements": generate_value_propositions(business_idea),
            "tips": [
                "Solve customer problems",
                "Meet customer needs",
                "Create value propositions for each segment",
            ],
        },
        "customer_segments": {
            "title": "Customer Segments",
            "description": "Target customers and users",
            "elements": generate_customer_segments(business_idea),
            "tips": [
                "Identify core segments",
                "Define mass market vs niche",
                "Consider different needs",
            ],
        },
        "channels": {
            "title": "Channels",
            "description": "How to reach customers",
            "elements": ["Online", "Retail", "Direct Sales"],
            "tips": [
                "Choose effective channels",
                "Consider customer preferences",
                "Balance cost and reach",
            ],
        },
        "customer_relationships": {
            "title": "Customer Relationships",
            "description": "Types of relationships to establish",
            "elements": ["Self-service", "Assisted", "Community"],
            "tips": [
                "Match relationship type to segment",
                "Consider customer lifecycle",
            ],
        },
        "revenue_streams": {
            "title": "Revenue Streams",
            "description": "How to monetize",
            "elements": generate_revenue_streams(business_idea),
            "tips": ["Consider payment timing", "Explore multiple streams"],
        },
        "key_resources": {
            "title": "Key Resources",
            "description": "Critical assets needed",
            "elements": ["Intellectual", "Physical", "Human", "Financial"],
            "tips": ["Identify core resources", "Consider resource ownership"],
        },
        "key_activities": {
            "title": "Key Activities",
            "description": "Critical actions to take",
            "elements": ["Production", "Problem-solving", "Platform"],
            "tips": ["Focus on core activities", "Consider outsourcing"],
        },
        "key_partnerships": {
            "title": "Key Partnerships",
            "description": "Network of suppliers and partners",
            "elements": ["Suppliers", "Strategic Alliances", "Platform Partners"],
            "tips": ["Identify partnership opportunities", "Consider alliance types"],
        },
        "cost_structure": {
            "title": "Cost Structure",
            "description": "Business costs",
            "elements": ["Fixed Costs", "Variable Costs"],
            "tips": ["Identify cost drivers", "Consider economies of scale"],
        },
    }

    return {
        "canvas_title": f"Business Model Canvas: {business_idea[:50] if business_idea else 'Untitled'}",
        "nine_building_blocks": canvas,
        "completeness_score": calculate_completeness(canvas),
        "recommendations": generate_canvas_recommendations(canvas),
    }


def generate_value_propositions(idea: str) -> List[str]:
    """Generate value propositions based on business idea."""
    if not idea:
        return ["[Define your value proposition]"]
    return [f"Value for customers based on: {idea[:30]}"]


def generate_customer_segments(idea: str) -> List[str]:
    """Generate customer segments."""
    if not idea:
        return ["[Define your customer segments]"]
    return ["Primary segment: [Target market]"]


def generate_revenue_streams(idea: str) -> List[str]:
    """Generate revenue streams."""
    if not idea:
        return ["[Define revenue streams]"]
    return ["Primary revenue: [Main income source]"]


def calculate_completeness(canvas: Dict) -> float:
    """Calculate canvas completeness score."""
    filled = sum(
        1
        for block in canvas.values()
        if isinstance(block, dict) and block.get("elements")
    )
    return round(filled / 9.0, 2)


def generate_canvas_recommendations(canvas: Dict) -> List[str]:
    """Generate canvas recommendations."""
    recommendations = []

    # Check for empty elements
    empty_blocks = []
    for name, block in canvas.items():
        if isinstance(block, dict):
            elements = block.get("elements", [])
            if not elements or all("[Define" in str(e) for e in elements):
                empty_blocks.append(block.get("title", name))

    if empty_blocks:
        recommendations.append(f"F complete: {', '.join(empty_blocks)}")
    else:
        recommendations.append("All canvas blocks are filled")

    return recommendations


def main():
    parser = argparse.ArgumentParser(description="Design Business Model Canvas")
    parser.add_argument("-i", "--input", required=True, help="Input business idea file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = design_canvas(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Business Model Canvas saved to {args.output}")
    print(f"Completeness: {result['completeness_score'] * 100}%")

    return 0


if __name__ == "__main__":
    sys.exit(main())
