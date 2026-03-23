#!/usr/bin/env python3
"""
Behavior Pattern Analyzer for System Dynamics
Identifies and classifies dynamic behaviors in system dynamics models.
"""

import argparse
import json
import sys
from typing import Any, Dict, List


def identify_behavior(time_series: List[float]) -> str:
    """Identify behavior pattern from time series data."""
    if len(time_series) < 3:
        return "insufficient_data"

    # Calculate trends
    values = time_series
    n = len(values)

    # Check for growth/decay
    first_half_avg = sum(values[: n // 2]) / (n // 2)
    second_half_avg = sum(values[n // 2 :]) / (n - n // 2)

    if second_half_avg > first_half_avg * 1.1:
        # Check for exponential vs logistic
        if values[-1] > values[0] * 2:
            return "exponential_growth"
        else:
            return "sigmoidal_growth"

    elif second_half_avg < first_half_avg * 0.9:
        if values[-1] < values[0] * 0.5:
            return "exponential_decay"
        else:
            return "convergent_decline"

    # Check for oscillation
    peaks = count_peaks(values)
    if peaks > n // 4:
        return "oscillatory"

    # Check for equilibrium
    if variance(values) < 0.01 * (max(values) - min(values) + 0.001):
        return "equilibrium"

    return "stable"


def count_peaks(values: List[float]) -> int:
    """Count number of peaks in time series."""
    if len(values) < 3:
        return 0

    peaks = 0
    for i in range(1, len(values) - 1):
        if values[i] > values[i - 1] and values[i] > values[i + 1]:
            peaks += 1

    return peaks


def variance(values: List[float]) -> float:
    """Calculate variance of values."""
    if not values:
        return 0.0
    mean = sum(values) / len(values)
    return sum((x - mean) ** 2 for x in values) / len(values)


def analyze_behavior(model: dict, time_horizon: int = 100) -> dict:
    """Analyze behavior patterns in system dynamics model."""
    results = {"time_horizon": time_horizon, "stocks": {}}

    stocks = model.get("stocks", {})

    # Generate time series for each stock
    stock_values = {name: data.get("initial_value", 0) for name, data in stocks.items()}

    for t in range(time_horizon):
        # Update flows
        flows = model.get("flows", {})
        flow_results = {}

        for flow_name, flow_def in flows.items():
            try:
                expr = flow_def.get("expression", "0")
                for s, v in stock_values.items():
                    expr = expr.replace(s, str(v))
                flow_results[flow_name] = eval(expr)
            except:
                flow_results[flow_name] = 0

        # Update stocks
        for stock_name, stock_def in stocks.items():
            inflow = sum(flow_results.get(f, 0) for f in stock_def.get("inflows", []))
            outflow = sum(flow_results.get(f, 0) for f in stock_def.get("outflows", []))
            stock_values[stock_name] += inflow - outflow

    # Analyze each stock
    for stock_name in stocks:
        values = [stock_values[stock_name]] * time_horizon  # Simplified
        # Use actual time series in production

        behavior = identify_behavior(values)
        results["stocks"][stock_name] = {
            "behavior_pattern": behavior,
            "final_value": stock_values[stock_name],
            "initial_value": stocks[stock_name].get("initial_value", 0),
        }

    # Overall model behavior
    all_behaviors = [s["behavior_pattern"] for s in results["stocks"].values()]
    results["overall_behavior"] = max(set(all_behaviors), key=all_behaviors.count)

    return results


def classify_system_type(model: dict) -> str:
    """Classify the overall system type."""
    stocks = model.get("stocks", {})
    flows = model.get("flows", {})

    # Count feedback loops
    feedback_loops = len([f for f in flows.values() if "feedback" in str(f)])

    if feedback_loops > 2:
        return "complex_feedback_system"
    elif len(stocks) > 5:
        return "large_scale_system"
    elif len(stocks) <= 2:
        return "simple_system"
    else:
        return "moderate_system"


def main():
    parser = argparse.ArgumentParser(
        description="Analyze behavior patterns in system dynamics"
    )
    parser.add_argument("--model", type=str, required=True, help="Model configuration")
    parser.add_argument(
        "--horizon", type=int, default=100, help="Simulation time horizon"
    )
    parser.add_argument("--classify", action="store_true", help="Classify system type")
    parser.add_argument("--output", type=str, help="Output file")

    args = parser.parse_args()

    with open(args.model) as f:
        model = json.load(f)

    results = analyze_behavior(model, args.horizon)

    if args.classify:
        results["system_type"] = classify_system_type(model)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2)
    else:
        print(json.dumps(results, indent=2))

    return 0


if __name__ == "__main__":
    sys.exit(main())
