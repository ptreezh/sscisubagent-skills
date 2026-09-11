#!/usr/bin/env python3
"""
Business Model Validator Tool
Validates business model components and logic.
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
    return {"raw": open(p).read()}


def validate_model(data: Dict) -> Dict:
    checks = [
        {"component": "value_proposition", "required": True},
        {"component": "customer_segments", "required": True},
        {"component": "revenue_streams", "required": True},
        {"component": "cost_structure", "required": True},
    ]
    results = []
    for c in checks:
        has = c["component"] in data
        results.append(
            {"component": c["component"], "valid": has, "required": c["required"]}
        )

    return {
        "valid": all(r["valid"] or not r["required"] for r in results),
        "checks": results,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()

    data = load_input(args.input)
    result = validate_model(data)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Validation saved to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
