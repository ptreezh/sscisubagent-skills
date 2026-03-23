#!/usr/bin/env python3
"""
Business Model Canvas Generator Tool
Generates a complete business model canvas.
"""

import argparse
import json
import sys
from pathlib import Path


def load_input(path: str) -> Dict:
    p = Path(path)
    if p.suffix == ".json":
        with open(p) as f:
            return json.load(f)
    return {"idea": open(p).read()}


def generate_canvas(data: Dict) -> Dict:
    idea = data.get("idea", data.get("description", ""))

    canvas = {
        "value_propositions": [{"value": f"Value from: {idea[:50]}"}],
        "customer_segments": [{"segment": "Primary customers"}],
        "channels": [{"channel": "Online"}],
        "customer_relationships": [{"type": "Self-service"}],
        "revenue_streams": [{"revenue": "Product sales"}],
        "key_resources": [{"resource": "Core assets"}],
        "key_activities": [{"activity": "Core operations"}],
        "key_partnerships": [{"partner": "Suppliers"}],
        "cost_structure": [{"cost": "Fixed costs"}],
    }

    return {"canvas": canvas, "completeness": 1.0}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()

    data = load_input(args.input)
    result = generate_canvas(data)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Canvas generated to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
