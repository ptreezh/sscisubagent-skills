#!/usr/bin/env python3
"""
Simulation Runner for System Dynamics Models
Executes system dynamics simulations with configurable time steps and parameters.
"""

import argparse
import json
import sys
from typing import Any


def run_simulation(
    model_config: dict, time_horizon: int = 100, dt: float = 1.0
) -> dict:
    """Execute a system dynamics simulation."""
    stocks = model_config.get("stocks", {})
    flows = model_config.get("flows", {})
    auxiliaries = model_config.get("auxiliaries", {})

    results = {"time": [], "stocks": {s: [] for s in stocks}}

    for t in range(0, int(time_horizon) + 1, int(dt)):
        results["time"].append(t)

        # Calculate flows
        flow_values = {}
        for flow_name, flow_def in flows.items():
            expression = flow_def.get("expression", "0")
            # Simplified evaluation - in production would use proper parser
            flow_values[flow_name] = evaluate_expression(
                expression, stocks, auxiliaries, t
            )

        # Update stocks
        for stock_name, stock_def in stocks.items():
            inflow = sum(flow_values.get(f, 0) for f in stock_def.get("inflows", []))
            outflow = sum(flow_values.get(f, 0) for f in stock_def.get("outflows", []))
            current = stock_def.get("initial_value", 0)
            new_value = current + (inflow - outflow) * dt
            results["stocks"][stock_name].append(new_value)
            stock_def["initial_value"] = new_value

    return results


def evaluate_expression(expr: str, stocks: dict, auxiliaries: dict, t: float) -> float:
    """Evaluate a mathematical expression."""
    try:
        # Simple evaluation - replace variables with values
        eval_expr = expr
        for name, value in stocks.items():
            eval_expr = eval_expr.replace(name, str(value.get("initial_value", 0)))
        for name, value in auxiliaries.items():
            eval_expr = eval_expr.replace(name, str(value))
        eval_expr = eval_expr.replace("time", str(t))
        return eval(eval_expr)
    except:
        return 0.0


def main():
    parser = argparse.ArgumentParser(description="Run system dynamics simulation")
    parser.add_argument("--config", type=str, help="Model configuration JSON file")
    parser.add_argument(
        "--horizon", type=int, default=100, help="Simulation time horizon"
    )
    parser.add_argument("--dt", type=float, default=1.0, help="Time step")
    parser.add_argument("--output", type=str, help="Output file for results")

    args = parser.parse_args()

    if args.config:
        with open(args.config) as f:
            model_config = json.load(f)
    else:
        # Default model: simple exponential growth
        model_config = {
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
            "auxiliaries": {},
        }

    results = run_simulation(model_config, args.horizon, args.dt)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
    else:
        print(json.dumps(results, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
