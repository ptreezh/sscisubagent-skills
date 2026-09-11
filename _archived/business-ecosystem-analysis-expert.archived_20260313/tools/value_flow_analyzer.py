#!/usr/bin/env python3
"""
Value Flow Analyzer Tool
Analyzes value flows between ecosystem actors using Iansiti & Levien framework.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from collections import defaultdict


def load_input_data(input_path: str) -> Dict[str, Any]:
    """Load input data from file."""
    path = Path(input_path)
    if not path.exists():
        return {}

    if path.suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    elif path.suffix == ".csv":
        import csv

        data = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return {"flows": data}
    else:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"raw_text": content}


def calculate_value_flows(flows: List[Dict]) -> Dict[str, Any]:
    """Calculate value flows between actors."""
    value_in = defaultdict(float)
    value_out = defaultdict(float)
    flow_details = []

    for flow in flows:
        from_actor = flow.get("from", flow.get("source", ""))
        to_actor = flow.get("to", flow.get("target", ""))

        # Try to extract value amount
        value_str = flow.get("value", flow.get("amount", "0"))
        try:
            value = float(str(value_str).replace("$", "").replace(",", ""))
        except ValueError:
            value = 1.0  # Default unit value

        value_out[from_actor] += value
        value_in[to_actor] += value

        flow_details.append(
            {
                "from": from_actor,
                "to": to_actor,
                "value": value,
                "type": flow.get("type", "transaction"),
            }
        )

    # Calculate network metrics
    actors = set(value_in.keys()) | set(value_out.keys())
    total_value = sum(value_in.values())

    # Identify value creators (high out, low in)
    value_creators = []
    for actor in actors:
        net_value = value_out[actor] - value_in[actor]
        if net_value > 0:
            value_creators.append(
                {"actor": actor, "net_value": net_value, "role": "value_creator"}
            )

    # Identify value consumers (high in, low out)
    value_consumers = []
    for actor in actors:
        net_value = value_out[actor] - value_in[actor]
        if net_value < 0:
            value_consumers.append(
                {"actor": actor, "net_value": net_value, "role": "value_consumer"}
            )

    # Value hub (balanced)
    hubs = []
    for actor in actors:
        net_value = value_out[actor] - value_in[actor]
        if abs(net_value) < total_value * 0.1:  # Within 10%
            hubs.append({"actor": actor, "net_value": net_value, "role": "value_hub"})

    return {
        "summary": {
            "total_value_flow": total_value,
            "actor_count": len(actors),
            "flow_count": len(flows),
        },
        "actor_metrics": {
            "value_creators": sorted(
                value_creators, key=lambda x: x["net_value"], reverse=True
            ),
            "value_consumers": sorted(value_consumers, key=lambda x: x["net_value"]),
            "value_hubs": hubs,
        },
        "flow_details": flow_details,
        "network_metrics": {
            "density": len(flows) / max(len(actors) * (len(actors) - 1), 1),
            "avg_value_per_flow": total_value / max(len(flows), 1),
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze value flows in business ecosystem"
    )
    parser.add_argument("-i", "--input", required=True, help="Input data file")
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    flows = data.get("flows", [])

    if not flows and "raw_text" in data:
        flows = [
            {"from": "unknown1", "to": "unknown2", "value": 1, "type": "extracted"}
        ]

    result = calculate_value_flows(flows)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Value flow analysis saved to {args.output}")
    print(f"Total value: ${result['summary']['total_value_flow']:,.2f}")
    print(f"Actors: {result['summary']['actor_count']}")
    print(f"Value creators: {len(result['actor_metrics']['value_creators'])}")
    print(f"Value consumers: {len(result['actor_metrics']['value_consumers'])}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
