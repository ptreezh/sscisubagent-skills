#!/usr/bin/env python3
"""
涂尔干社会分析技能 - 自进化模块
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


class DurkheimPhase(Enum):
    INITIAL = "initial"
    SOCIAL_FACTS = "social_facts"
    SUICIDE_TYPES = "suicide_types"
    ANOMIE = "anomie"
    SOLIDARITY = "solidarity"
    COMPLETE = "complete"


@dataclass
class EvolutionState:
    iteration: int = 1
    phase: DurkheimPhase = DurkheimPhase.INITIAL
    quality_score: float = 0.0
    suicide_types_identified: int = 0
    social_facts_analyzed: int = 0
    refinement_history: List[Dict] = field(default_factory=list)


class DigitalDurkheimEvolution:
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
                    phase=DurkheimPhase(data.get("phase", "initial")),
                    quality_score=data.get("quality_score", 0.0),
                    suicide_types_identified=data.get("suicide_types_identified", 0),
                    social_facts_analyzed=data.get("social_facts_analyzed", 0),
                    refinement_history=data.get("refinement_history", []),
                )
        return EvolutionState()

    def _save_state(self) -> None:
        state_file = self.session_dir / "evolution_state.yaml"
        data = {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "suicide_types_identified": self.state.suicide_types_identified,
            "social_facts_analyzed": self.state.social_facts_analyzed,
            "refinement_history": self.state.refinement_history,
            "updated_at": datetime.now().isoformat(),
        }
        with open(state_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def _load_quality_gates(self) -> Dict[str, Any]:
        return {
            "social_facts": {
                "min_facts": 3,
                "required_types": [
                    "collective_conscience",
                    "social_integration",
                    "anomie",
                ],
            },
            "suicide_types": {
                "min_types": 4,
                "required_types": ["egoistic", "altruistic", "anomic", "fatalistic"],
            },
            "solidarity": {"mechanical": True, "organic": True, "analysis": True},
        }

    def start_session(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        print(f"\n{'=' * 50}")
        print(f"涂尔干社会分析自进化系统")
        print(f"迭代: {self.state.iteration}")
        print(f"{'=' * 50}\n")

        self.state.phase = DurkheimPhase.SOCIAL_FACTS
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

        passed = True
        if "min_facts" in gate:
            facts = result.get("facts", [])
            if len(facts) < gate["min_facts"]:
                passed = False

        if "min_types" in gate:
            types = result.get("types", [])
            if len(types) < gate["min_types"]:
                passed = False

        return QualityGate.PASS if passed else QualityGate.FAIL

    def get_status(self) -> Dict[str, Any]:
        return {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "suicide_types": self.state.suicide_types_identified,
            "social_facts": self.state.social_facts_analyzed,
        }

    def reset(self) -> None:
        self.state = EvolutionState()
        self._save_state()


def main():
    import argparse

    parser = argparse.ArgumentParser(description="涂尔干自进化系统")
    parser.add_argument(
        "--action", choices=["start", "status", "reset"], default="status"
    )
    args = parser.parse_args()

    evolution = DigitalDurkheimEvolution()

    if args.action == "start":
        print(json.dumps(evolution.start_session(), ensure_ascii=False, indent=2))
    elif args.action == "status":
        print(json.dumps(evolution.get_status(), ensure_ascii=False, indent=2))
    elif args.action == "reset":
        evolution.reset()


if __name__ == "__main__":
    main()
