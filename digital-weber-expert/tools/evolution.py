#!/usr/bin/env python3
"""
韦伯分析技能 - 自进化模块
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


class WeberPhase(Enum):
    INITIAL = "initial"
    SOCIAL_ACTION = "social_action"
    AUTHORITY = "authority"
    STATUS_GROUPS = "status_groups"
    RELIGION = "religion"
    COMPLETE = "complete"


@dataclass
class EvolutionState:
    iteration: int = 1
    phase: WeberPhase = WeberPhase.INITIAL
    quality_score: float = 0.0
    actions_analyzed: int = 0
    authority_types: int = 0
    refinement_history: List[Dict] = field(default_factory=list)


class DigitalWeberEvolution:
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
                    phase=WeberPhase(data.get("phase", "initial")),
                    quality_score=data.get("quality_score", 0.0),
                    actions_analyzed=data.get("actions_analyzed", 0),
                    authority_types=data.get("authority_types", 0),
                    refinement_history=data.get("refinement_history", []),
                )
        return EvolutionState()

    def _save_state(self) -> None:
        state_file = self.session_dir / "evolution_state.yaml"
        data = {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "actions_analyzed": self.state.actions_analyzed,
            "authority_types": self.state.authority_types,
            "refinement_history": self.state.refinement_history,
            "updated_at": datetime.now().isoformat(),
        }
        with open(state_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def _load_quality_gates(self) -> Dict[str, Any]:
        return {
            "social_action": {"min_actions": 4},
            "authority": {
                "min_types": 3,
                "required": ["traditional", "legal", "charismatic"],
            },
            "status_groups": {"min_groups": 2},
            "religion": {"required": True},
        }

    def start_session(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        print(f"\n{'=' * 50}")
        print(f"韦伯分析自进化系统")
        print(f"迭代: {self.state.iteration}")
        print(f"{'=' * 50}\n")

        self.state.phase = WeberPhase.SOCIAL_ACTION
        self._save_state()

        return {"status": "started", "phase": self.state.phase.value}

    def run_quality_gate(self, gate_name: str, result: Dict[str, Any]) -> QualityGate:
        gate = self.quality_gates.get(gate_name, {})
        if not gate:
            return QualityGate.WARNING

        min_elements = gate.get(
            "min_actions", gate.get("min_types", gate.get("min_groups", 0))
        )
        elements = result.get("actions", result.get("types", result.get("groups", [])))

        if len(elements) >= min_elements:
            return QualityGate.PASS
        return QualityGate.FAIL

    def get_status(self) -> Dict[str, Any]:
        return {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "actions": self.state.actions_analyzed,
            "authority_types": self.state.authority_types,
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="韦伯自进化系统")
    parser.add_argument("--action", choices=["start", "status"], default="status")
    args = parser.parse_args()

    evolution = DigitalWeberEvolution()

    if args.action == "start":
        print(json.dumps(evolution.start_session(), ensure_ascii=False, indent=2))
    elif args.action == "status":
        print(json.dumps(evolution.get_status(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
