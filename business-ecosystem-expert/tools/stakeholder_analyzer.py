#!/usr/bin/env python3
"""
Stakeholder Position Analyzer Tool
Analyzes stakeholder positions and power dynamics in business ecosystems.
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


def analyze_stakeholder_positions(data: Dict) -> Dict[str, Any]:
    """Analyze stakeholder positions and power dynamics."""
    raw_text = data.get("raw_text", "")
    stakeholders = data.get("stakeholders", data.get("actors", []))

    # If no structured data, extract from text
    if not stakeholders and raw_text:
        stakeholders = [{"name": "extracted", "description": raw_text[:500]}]

    positions = []
    for stakeholder in stakeholders:
        name = stakeholder.get("name", stakeholder.get("id", "unknown"))

        # Analyze power
        power_indicators = [
            stakeholder.get("market_share", ""),
            stakeholder.get("revenue", ""),
            stakeholder.get("users", ""),
        ]
        power_level = "low"
        if any(power_indicators):
            try:
                # Try to extract numeric value
                for p in power_indicators:
                    if p:
                        val = float(
                            str(p).replace("%", "").replace("$", "").replace(",", "")
                        )
                        if val > 1000000:
                            power_level = "high"
                        elif val > 100000:
                            power_level = "medium"
                        break
            except:
                pass

        # Analyze interest
        interest_level = stakeholder.get(
            "interest", stakeholder.get("involvement", "medium")
        )

        # Analyze influence
        influence = stakeholder.get("influence", "medium")

        positions.append(
            {
                "name": name,
                "power": power_level,
                "interest": interest_level,
                "influence": influence,
                "position": classify_position(power_level, interest_level),
            }
        )

    # Classify stakeholders using power/interest grid
    power_interest_grid = classify_stakeholder_grid(positions)

    return {
        "stakeholder_count": len(positions),
        "stakeholders": positions,
        "power_interest_grid": power_interest_grid,
        "key_players": [p for p in positions if p["power"] == "high"],
        "engagement_priorities": generate_engagement_plan(positions),
    }


def classify_position(power: str, interest: str) -> str:
    """Classify stakeholder position."""
    if power == "high" and interest in ["high", "medium"]:
        return "manage_closely"
    elif power == "high" and interest == "low":
        return "keep_satisfied"
    elif power == "low" and interest == "high":
        return "keep_informed"
    else:
        return "monitor"


def classify_stakeholder_grid(positions: List[Dict]) -> Dict[str, List[str]]:
    """Classify stakeholders on power/interest grid."""
    grid = {
        "manage_closely": [],  # High power, High interest
        "keep_satisfied": [],  # High power, Low interest
        "keep_informed": [],  # Low power, High interest
        "monitor": [],  # Low power, Low interest
    }

    for p in positions:
        pos = p["position"]
        grid[pos].append(p["name"])

    return grid


def generate_engagement_plan(positions: List[Dict]) -> List[str]:
    """Generate engagement plan based on positions."""
    plan = []

    closely = [p['name'] for p in positions if p['position'] == 'manage_closely']
    satisfied = [p['name'] for p in positions if p['position'] == 'keep_satisfied']
    informed = [p['name'] for p in positions if p['position'] == 'keep_informed']

    if closely:
        plan.append(f"Engage closely with: {', '.join(closely)}")
    if satisfied:
        plan.append(f"Satisfy needs of: {', '.join(satisfied)}")
    if informed:
        plan.append(f"Keep informed: {', '.join(informed)}")

    if not plan:
        plan.append("No specific engagement priorities identified")

    return plan


def main():
    parser = argparse.ArgumentParser(description="Analyze stakeholder positions")
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = analyze_stakeholder_positions(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Stakeholder analysis saved to {args.output}")
    print(f"Total stakeholders: {result['stakeholder_count']}")
    print(f"Key players: {len(result['key_players'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
