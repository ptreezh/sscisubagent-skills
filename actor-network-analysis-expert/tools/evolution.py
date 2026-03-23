#!/usr/bin/env python3
"""
行动者网络分析技能 - 自进化模块
"""

import os
import json
import yaml
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass, field
from enum import Enum


class QualityGate(Enum):
    PASS = "pass"
    WARNING = "warning"
    FAIL = "fail"


class ANTPhase(Enum):
    INITIAL = "initial"
    PROBLEM_ARTICULATION = "problem_articulation"
    ACTOR_IDENTIFICATION = "actor_identification"
    NETWORK_BUILDING = "network_building"
    TRANSLATION = "translation"
    COMPLETE = "complete"


@dataclass
class EvolutionState:
    iteration: int = 1
    phase: ANTPhase = ANTPhase.INITIAL
    quality_score: float = 0.0
    actors_identified: int = 0
    networks_built: bool = False
    refinement_history: List[Dict] = field(default_factory=list)


class ActorNetworkEvolution:
    def __init__(self, skill_dir: str = None):
        if skill_dir:
            self.skill_dir = Path(skill_dir)
        else:
            self.skill_dir = Path(__file__).parent

        self.session_dir = self.skill_dir / ".evolution"
        self.session_dir.mkdir(parents=True, exist_ok=True)

        self.state = self._load_state()
        self.quality_gates = self._load_quality_gates()

    def _load_state(self) -> EvolutionState:
        state_file = self.session_dir / "evolution_state.yaml"
        if state_file.exists():
            with open(state_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
                return EvolutionState(
                    iteration=data.get("iteration", 1),
                    phase=ANTPhase(data.get("phase", "initial")),
                    quality_score=data.get("quality_score", 0.0),
                    actors_identified=data.get("actors_identified", 0),
                    networks_built=data.get("networks_built", False),
                    refinement_history=data.get("refinement_history", []),
                )
        return EvolutionState()

    def _save_state(self) -> None:
        state_file = self.session_dir / "evolution_state.yaml"
        data = {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "actors_identified": self.state.actors_identified,
            "networks_built": self.state.networks_built,
            "refinement_history": self.state.refinement_history,
            "updated_at": datetime.now().isoformat(),
        }
        with open(state_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def _load_quality_gates(self) -> Dict[str, Any]:
        return {
            "actor_identification": {
                "min_actors": 5,
                "required_types": ["human", "non_human"],
            },
            "network_building": {
                "min_relations": 3,
                "required_elements": ["nodes", "edges", "directions"],
            },
            "translation": {
                "required": True,
                "processes": [
                    "problematization",
                    "interessement",
                    "enrollment",
                    "mobilization",
                ],
            },
        }

    def start_session(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        print(f"\n{'=' * 50}")
        print(f"行动者网络分析自进化系统")
        print(f"迭代: {self.state.iteration}")
        print(f"{'=' * 50}\n")

        self.state.phase = ANTPhase.PROBLEM_ARTICULATION
        self._save_state()

        return {
            "status": "started",
            "phase": self.state.phase.value,
            "quality_gates": list(self.quality_gates.keys()),
        }

    def run_quality_gate(self, gate_name: str, result: Dict[str, Any]) -> QualityGate:
        gate = self.quality_gates.get(gate_name, {})
        if not gate:
            return QualityGate.WARNING

        min_actors = gate.get("min_actors", 0)
        actors = result.get("actors", [])

        if len(actors) >= min_actors:
            return QualityGate.PASS
        return QualityGate.FAIL

    def get_status(self) -> Dict[str, Any]:
        return {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "actors": self.state.actors_identified,
            "networks_built": self.state.networks_built,
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="行动者网络自进化系统")
    parser.add_argument("--action", choices=["start", "status"], default="status")
    args = parser.parse_args()

    evolution = ActorNetworkEvolution()

    if args.action == "start":
        print(json.dumps(evolution.start_session(), ensure_ascii=False, indent=2))
    elif args.action == "status":
        print(json.dumps(evolution.get_status(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
