#!/usr/bin/env python3
"""
Business Model Pattern Analyzer Tool
Analyzes business models against known patterns (Platform, Subscription, Marketplace, etc.)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def load_input_data(input_path: str) -> Dict[str, Any]:
    path = Path(input_path)
    if not path.exists():
        return {}
    if path.suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        with open(path, "r", encoding="utf-8") as f:
            return {"description": f.read()}


def analyze_patterns(data: Dict) -> Dict[str, Any]:
    desc = data.get("description", data.get("business_model", ""))

    patterns = [
        {
            "name": "Platform",
            "indicators": ["marketplace", "two-sided", "network", "ecosystem"],
        },
        {
            "name": "Subscription",
            "indicators": ["recurring", "monthly", "annual", "membership"],
        },
        {"name": "Freemium", "indicators": ["free", "premium", "tier", "basic"]},
        {
            "name": "Marketplace",
            "indicators": ["connect", "transaction", "commission", "seller-buyer"],
        },
        {"name": "SaaS", "indicators": ["software", "cloud", "web-based", "on-demand"]},
        {
            "name": "Direct-to-Consumer",
            "indicators": [" DTC ", "brand-owned", "retail", "online"],
        },
    ]

    identified = []
    desc_lower = desc.lower()
    for p in patterns:
        matches = sum(1 for ind in p["indicators"] if ind in desc_lower)
        if matches > 0:
            identified.append(
                {
                    "pattern": p["name"],
                    "confidence": min(matches / len(p["indicators"]), 1.0),
                    "indicators_found": matches,
                }
            )

    return {
        "patterns_analyzed": len(patterns),
        "patterns_found": sorted(
            identified, key=lambda x: x["confidence"], reverse=True
        ),
        "primary_pattern": identified[0]["pattern"] if identified else None,
        "recommendations": [
            f"Consider {p['pattern']} business model" for p in identified[:2]
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True)
    parser.add_argument("-o", "--output", required=True)
    args = parser.parse_args()

    data = load_input_data(args.input)
    result = analyze_patterns(data)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    with open(args.output, "w") as f:
        json.dump(result, f, indent=2)
    print(f"Pattern analysis saved to {args.output}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
