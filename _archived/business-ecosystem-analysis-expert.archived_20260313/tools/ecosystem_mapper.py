#!/usr/bin/env python3
"""
Business Ecosystem Mapper Tool
Maps business ecosystem actors and their relationships using Moore's Business Ecosystem framework.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional


def load_input_data(input_path: str) -> Dict[str, Any]:
    """Load input data from file."""
    path = Path(input_path)
    if not path.exists():
        return {}

    if path.suffix == ".json":
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    elif path.suffix == ".csv":
        # Simple CSV parsing
        import csv

        data = []
        with open(path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        return {"actors": data}
    else:
        # Try to read as text
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"raw_text": content}


def identify_keystones(actors: List[Dict]) -> List[Dict]:
    """Identify keystone actors in the ecosystem."""
    keystones = []
    for actor in actors:
        # Keystone characteristics: creates value for others, low market share
        if actor.get("creates_value_for_others", "").lower() == "high":
            keystones.append(actor)
    return keystones


def identify_dominators(actors: List[Dict]) -> List[Dict]:
    """Identify dominator actors (high market share, controls resources)."""
    dominators = []
    for actor in actors:
        if actor.get("market_share", "0").replace("%", "").isdigit():
            share = float(actor.get("market_share", "0").replace("%", ""))
            if share > 30:
                dominators.append(actor)
    return dominators


def identify_niche_players(actors: List[Dict]) -> List[Dict]:
    """Identify niche players (specialized, dependent)."""
    niche_players = []
    for actor in actors:
        role = actor.get("role", "").lower()
        if "niche" in role or "specialized" in role:
            niche_players.append(actor)
    return niche_players


def analyze_dependencies(actors: List[Dict]) -> Dict[str, List[str]]:
    """Analyze dependencies between actors."""
    dependencies = {}
    for actor in actors:
        actor_name = actor.get("name", actor.get("id", "unknown"))
        deps = actor.get("depends_on", "").split(",")
        dependencies[actor_name] = [d.strip() for d in deps if d.strip()]
    return dependencies


def generate_ecosystem_map(actors: List[Dict]) -> Dict[str, Any]:
    """Generate business ecosystem map."""
    keystones = identify_keystones(actors)
    dominators = identify_dominators(actors)
    niche_players = identify_niche_players(actors)
    other_actors = [
        a for a in actors if a not in keystones + dominators + niche_players
    ]
    dependencies = analyze_dependencies(actors)

    return {
        "ecosystem_structure": {
            "keystones": keystones,
            "dominators": dominators,
            "niche_players": niche_players,
            "other_actors": other_actors,
        },
        "total_actors": len(actors),
        "keystone_count": len(keystones),
        "dominator_count": len(dominators),
        "niche_player_count": len(niche_players),
        "dependencies": dependencies,
        "ecosystem_health": "balanced"
        if len(keystones) > 0 and len(dominators) < len(actors) / 2
        else "at_risk",
    }


def main():
    parser = argparse.ArgumentParser(description="Map business ecosystem actors")
    parser.add_argument(
        "-i", "--input", required=True, help="Input data file (JSON/CSV)"
    )
    parser.add_argument("-o", "--output", required=True, help="Output file path")
    args = parser.parse_args()

    data = load_input_data(args.input)
    actors = data.get("actors", [])

    if not actors and "raw_text" in data:
        # Try to parse from raw text
        actors = [{"name": "extracted_actor", "description": data["raw_text"][:200]}]

    result = generate_ecosystem_map(actors)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Ecosystem map saved to {args.output}")
    print(f"Total actors: {result['total_actors']}")
    print(f"Keystones: {result['keystone_count']}")
    print(f"Dominators: {result['dominator_count']}")
    print(f"Niche players: {result['niche_player_count']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
