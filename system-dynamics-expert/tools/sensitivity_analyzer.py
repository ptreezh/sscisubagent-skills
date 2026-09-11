#!/usr/bin/env python3
"""
Sensitivity Analyzer for System Dynamics
Analyzes how changes in parameters affect model behavior.
"""

import argparse
import json
import sys
from typing import Any, Dict


def calculate_elasticity(
    base_value: float, perturbed_value: float, base_param: float, perturbed_param: float
) -> float:
    """Calculate elasticity (% change in output / % change in input)."""
    if base_value == 0 or base_param == 0:
        return 0.0

    pct_change_output = (perturbed_value - base_value) / base_value
    pct_change_input = (perturbed_param - base_param) / base_param

    if pct_change_input == 0:
        return 0.0

    return pct_change_output / pct_change_input


def analyze_sensitivity(
    model: dict, parameter: str, perturbations: list = None
) -> dict:
    """Analyze sensitivity of model to parameter changes."""
    if perturbations is None:
        perturbations = [-0.5, -0.25, 0.25, 0.5]

    results = {
        "parameter": parameter,
        "base_value": model.get("parameters", {}).get(parameter, 1.0),
        "sensitivities": [],
    }

    base_value = run_simple_simulation(model)

    for pct in perturbations:
        perturbed_model = perturb_parameter(model, parameter, pct)
        perturbed_value = run_simple_simulation(perturbed_model)

        elasticity = calculate_elasticity(
            base_value,
            perturbed_value,
            results["base_value"],
            results["base_value"] * (1 + pct),
        )

        results["sensitivities"].append(
            {
                "perturbation_pct": pct,
                "perturbed_value": perturbed_value,
                "elasticity": elasticity,
            }
        )

    # Calculate average absolute sensitivity
    avg_sensitivity = sum(abs(s["elasticity"]) for s in results["sensitivities"]) / len(
        results["sensitivities"]
    )
    results["average_sensitivity"] = avg_sensitivity
    results["ranking"] = (
        "high"
        if avg_sensitivity > 1.0
        else "medium"
        if avg_sensitivity > 0.5
        else "low"
    )

    return results


def perturb_parameter(model: dict, param: str, pct_change: float) -> dict:
    """Create a model with perturbed parameter."""
    import copy

    modified = copy.deepcopy(model)

    if "parameters" not in modified:
        modified["parameters"] = {}

    current = modified["parameters"].get(param, 1.0)
    modified["parameters"][param] = current * (1 + pct_change)

    return modified


def run_simple_simulation(model: dict) -> float:
    """Run simplified simulation and return key metric."""
    stocks = model.get("stocks", {})
    if not stocks:
        return 0.0

    # Simple evaluation
    stock_values = {name: data.get("initial_value", 0) for name, data in stocks.items()}

    for _ in range(10):
        flows = model.get("flows", {})
        for flow_name, flow_def in flows.items():
            try:
                expr = flow_def.get("expression", "0")
                for s, v in stock_values.items():
                    expr = expr.replace(s, str(v))
                eval(expr)
            except:
                pass

    return sum(stock_values.values())


def main():
    parser = argparse.ArgumentParser(
        description="Sensitivity analysis for system dynamics"
    )
    parser.add_argument("--model", type=str, required=True, help="Model configuration")
    parser.add_argument(
        "--parameter", type=str, required=True, help="Parameter to analyze"
    )
    parser.add_argument(
        "--perturbations", type=str, help="JSON array of perturbation percentages"
    )
    parser.add_argument("--output", type=str, help="Output file")

    args = parser.parse_args()

    with open(args.model) as f:
        model = json.load(f)

    perturbations = None
    if args.perturbations:
        with open(args.perturbations) as f:
            perturbations = json.load(f)

    results = analyze_sensitivity(model, args.parameter, perturbations)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
    else:
        print(json.dumps(results, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
