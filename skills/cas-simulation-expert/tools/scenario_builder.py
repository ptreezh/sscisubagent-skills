#!/usr/bin/env python3
"""
Simulation Scenario Builder Tool
Builds simulation scenarios for CAS experiments.
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
    return {"context": open(p).read()}


def build_scenarios(data: Dict) -> Dict:
    return {
        "scenarios": [
            {"name": "baseline", "params": {}},
            {"name": "stress_test", "params": {"high_load": True}},
            {"name": "adaptation", "params": {"mutation_rate": 0.1}},
        ]
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()

    data = load_input(args.input)
    result = build_scenarios(data)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
