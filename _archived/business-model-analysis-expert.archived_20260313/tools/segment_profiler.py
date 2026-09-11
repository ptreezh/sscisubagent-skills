#!/usr/bin/env python3
"""
Customer Segment Profiler Tool
Profiles and analyzes customer segments.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List


def load_input(path: str) -> Dict:
    p = Path(path)
    if p.suffix == ".json":
        with open(p) as f:
            return json.load(f)
    return {"segments": [{"name": "default"}]}


def profile_segments(data: Dict) -> Dict:
    segments = data.get("segments", [])
    profiled = []

    for s in segments:
        profiled.append(
            {
                "name": s.get("name", "Unknown"),
                "size": s.get("size", 0),
                "value": s.get("value", s.get("size", 0) * 100),
                "acquisition_cost": s.get("acquisition_cost", 50),
                "lifetime_value": s.get("lifetime_value", 500),
            }
        )

    return {
        "segments": profiled,
        "total_addressable": sum(s["size"] for s in profiled),
        "most_valuable": max(profiled, key=lambda x: x["value"])["name"]
        if profiled
        else None,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()

    data = load_input(args.input)
    result = profile_segments(data)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Segment profiling saved to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
