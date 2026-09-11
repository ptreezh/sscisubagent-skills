#!/usr/bin/env python3
"""
Scenario Builder for System Dynamics
Creates alternative scenarios for model exploration.
"""

import argparse
import json
import sys
from typing import Any, Dict, List


def build_scenario(base_model: dict, changes: dict) -> dict:
    """Create a modified scenario from base model."""
    import copy

    scenario = copy.deepcopy(base_model)

    # Apply changes
    if "stocks" in changes:
        for name, changes in changes["stocks"].items():
            if name in scenario.get("stocks", {}):
                scenario["stocks"][name].update(changes)

    if "flows" in changes:
        for name, changes in changes["flows"].items():
            if name in scenario.get("flows", {}):
                scenario["flows"][name].update(changes)

    if "auxiliaries" in changes:
        scenario["auxiliaries"] = scenario.get("auxiliaries", {})
        scenario["auxiliaries"].update(changes["auxiliaries"])

    if "parameters" in changes:
        scenario["parameters"] = scenario.get("parameters", {})
        scenario["parameters"].update(changes["parameters"])

    scenario["scenario_name"] = changes.get("name", "Unnamed Scenario")
    scenario["description"] = changes.get("description", "")

    return scenario


def generate_scenarios(base_model: dict, scenario_specs: List[dict]) -> dict:
    """Generate multiple scenarios from specifications."""
    results = {"base_model": base_model.get("name", "model"), "scenarios": []}

    for spec in scenario_specs:
        scenario = build_scenario(base_model, spec)
        results["scenarios"].append(
            {
                "name": scenario["scenario_name"],
                "description": scenario.get("description", ""),
                "configuration": scenario,
            }
        )

    return results


def compare_scenarios(scenarios: List[dict]) -> dict:
    """Compare key characteristics across scenarios."""
    comparison = {"stocks": {}, "flows": {}, "parameters": {}}

    for scenario in scenarios:
        name = scenario.get("name", "unnamed")

        for stock in scenario.get("configuration", {}).get("stocks", {}):
            if stock not in comparison["stocks"]:
                comparison["stocks"][stock] = []
            comparison["stocks"][stock].append(
                {
                    "scenario": name,
                    "initial": scenario["configuration"]["stocks"][stock].get(
                        "initial_value", 0
                    ),
                }
            )

    return comparison


def main():
    parser = argparse.ArgumentParser(description="Build system dynamics scenarios")
    parser.add_argument("--base", type=str, help="Base model configuration")
    parser.add_argument("--changes", type=str, help="Scenario changes JSON")
    parser.add_argument("--compare", action="store_true", help="Compare scenarios")
    parser.add_argument("--output", type=str, help="Output file")

    args = parser.parse_args()

    if args.base and args.changes:
        with open(args.base) as f:
            base_model = json.load(f)

        with open(args.changes) as f:
            changes = json.load(f)

        if isinstance(changes, list):
            results = generate_scenarios(base_model, changes)
        else:
            scenario = build_scenario(base_model, changes)
            results = {"scenarios": [scenario]}

        if args.compare and len(results["scenarios"]) > 1:
            comparison = compare_scenarios(results["scenarios"])
            results["comparison"] = comparison
    else:
        # Default example
        base_model = {
            "name": "population_model",
            "stocks": {
                "population": {
                    "initial_value": 100,
                    "inflows": ["births"],
                    "outflows": ["deaths"],
                }
            },
            "flows": {
                "births": {"expression": "0.05 * population"},
                "deaths": {"expression": "0.01 * population"},
            },
        }

        scenarios = [
            {
                "name": "High Growth",
                "description": "Higher birth rate",
                "flows": {"births": {"expression": "0.10 * population"}},
            },
            {
                "name": "Low Growth",
                "description": "Lower birth rate",
                "flows": {"births": {"expression": "0.02 * population"}},
            },
        ]

        results = generate_scenarios(base_model, scenarios)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
    else:
        print(json.dumps(results, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
