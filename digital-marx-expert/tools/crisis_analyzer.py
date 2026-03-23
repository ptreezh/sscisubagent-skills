#!/usr/bin/env python3
"""
Crisis Analysis Tool
Analyzes economic crises and contradictions using Marxist theory.
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
    return {"description": open(p).read()}


def analyze_crisis(data: Dict) -> Dict:
    desc = data.get("description", "").lower()

    crisis_types = []
    if "overproduction" in desc:
        crisis_types.append("overproduction")
    if "financial" in desc or "bubble" in desc:
        crisis_types.append("financial")
    if "labor" in desc or "unemployment" in desc:
        crisis_types.append("labor")

    return {
        "crisis_types": crisis_types,
        "contradictions_identified": [
            "production_vs_consumption",
            "capital_accumulation",
        ],
        "analysis": "Crisis analyzed through Marxist lens",
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()

    data = load_input(args.input)
    result = analyze_crisis(data)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
