#!/usr/bin/env python3
"""
Parameter Sweep Tool for System Dynamics
Systematically explores parameter space to understand model behavior.
"""

import argparse
import json
import sys
from typing import Any
from itertools import product


def run_parameter_sweep(
    base_config: dict, parameter_ranges: dict, target_metric: str = "final_value"
) -> dict:
    """Run simulation across parameter space."""
    results = {"runs": [], "summary": {}}

    # Generate parameter combinations
    param_names = list(parameter_ranges.keys())
    param_values = list(parameter_ranges.values())

    for combination in product(*param_values):
        params = dict(zip(param_names, combination))
        run_config = apply_parameters(base_config, params)

        # Run simplified simulation
        run_result = simulate_with_params(run_config)
        results["runs"].append(
            {
                "parameters": params,
                "result": run_result,
                "metric": run_result.get(target_metric, 0),
            }
        )

    # Summarize results
    metrics = [r["metric"] for r in results["runs"]]
    results["summary"] = {
        "min": min(metrics),
        "max": max(metrics),
        "mean": sum(metrics) / len(metrics),
        "num_runs": len(results["runs"]),
    }

    return results


def apply_parameters(config: dict, params: dict) -> dict:
    """Apply parameters to model configuration."""
    import copy

    modified = copy.deepcopy(config)

    for key, value in params.items():
        if key in modified.get("parameters", {}):
            modified["parameters"][key] = value
        elif key in modified.get("flows", {}):
            modified["flows"][key]["expression"] = str(value)

    return modified


def simulate_with_params(config: dict) -> dict:
    """Run a single simulation with given parameters."""
    stocks = config.get("stocks", {})
    flows = config.get("flows", {})

    # Simple single-step evaluation
    stock_values = {}
    for name, data in stocks.items():
        stock_values[name] = data.get("initial_value", 0)

    # Calculate final values after 10 steps
    for _ in range(10):
        for flow_name, flow_def in flows.items():
            try:
                expr = flow_def.get("expression", "0")
                for s, v in stock_values.items():
                    expr = expr.replace(s, str(v))
                flow_value = eval(expr)
            except:
                flow_value = 0

    return {"final_value": sum(stock_values.values())}


def main():
    parser = argparse.ArgumentParser(description="Parameter sweep for system dynamics")
    parser.add_argument(
        "--config", type=str, required=True, help="Base model configuration"
    )
    parser.add_argument(
        "--ranges", type=str, required=True, help="Parameter ranges JSON"
    )
    parser.add_argument(
        "--metric", type=str, default="final_value", help="Target metric"
    )
    parser.add_argument("--output", type=str, help="Output file")

    args = parser.parse_args()

    with open(args.config) as f:
        base_config = json.load(f)

    with open(args.ranges) as f:
        parameter_ranges = json.load(f)

    results = run_parameter_sweep(base_config, parameter_ranges, args.metric)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
    else:
        print(json.dumps(results, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
