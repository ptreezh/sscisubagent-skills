#!/usr/bin/env python3
"""
Revenue Stream Modeler Tool
Models different revenue stream scenarios.
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
    return {"model": open(p).read()}


def model_revenue(data: Dict) -> Dict:
    streams = data.get("revenue_streams", [])
    projections = []

    for s in streams:
        projections.append(
            {
                "stream": s.get("name", "Unknown"),
                "monthly": s.get("price", 0) * s.get("customers", 0),
                "annual": s.get("price", 0) * s.get("customers", 0) * 12,
            }
        )

    total_monthly = sum(p["monthly"] for p in projections)
    total_annual = sum(p["annual"] for p in projections)

    return {
        "streams": projections,
        "total_monthly": total_monthly,
        "total_annual": total_annual,
        "diversified": len(projections) >= 3,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()

    data = load_input(args.input)
    result = model_revenue(data)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Revenue model saved to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
