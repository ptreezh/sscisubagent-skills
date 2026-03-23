#!/usr/bin/env python3
"""
问卷设计技能 - 自进化模块
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


class SurveyPhase(Enum):
    INITIAL = "initial"
    DESIGN = "design"
    VALIDITY = "validity"
    RELIABILITY = "reliability"
    PILOT = "pilot"
    COMPLETE = "complete"


@dataclass
class EvolutionState:
    iteration: int = 1
    phase: SurveyPhase = SurveyPhase.INITIAL
    quality_score: float = 0.0
    questions_count: int = 0
    validity_achieved: bool = False
    refinement_history: List[Dict] = field(default_factory=list)


class SurveyEvolution:
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
                    phase=SurveyPhase(data.get("phase", "initial")),
                    quality_score=data.get("quality_score", 0.0),
                    questions_count=data.get("questions_count", 0),
                    validity_achieved=data.get("validity_achieved", False),
                    refinement_history=data.get("refinement_history", []),
                )
        return EvolutionState()

    def _save_state(self) -> None:
        state_file = self.session_dir / "evolution_state.yaml"
        data = {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "questions_count": self.state.questions_count,
            "validity_achieved": self.state.validity_achieved,
            "refinement_history": self.state.refinement_history,
            "updated_at": datetime.now().isoformat(),
        }
        with open(state_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def _load_quality_gates(self) -> Dict[str, Any]:
        return {
            "design": {
                "min_questions": 10,
                "required_sections": ["demographic", "attitude", "behavior"],
            },
            "validity": {"content_validity": True, "construct_validity": True},
            "reliability": {"cronbach_alpha": 0.7},
        }

    def start_session(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        print(f"\n{'=' * 50}")
        print(f"问卷设计自进化系统")
        print(f"迭代: {self.state.iteration}")
        print(f"{'=' * 50}\n")

        self.state.phase = SurveyPhase.DESIGN
        self._save_state()

        return {"status": "started", "phase": self.state.phase.value}

    def run_quality_gate(self, gate_name: str, result: Dict[str, Any]) -> QualityGate:
        gate = self.quality_gates.get(gate_name, {})
        if not gate:
            return QualityGate.WARNING

        min_questions = gate.get("min_questions", 0)
        questions = result.get("questions", [])

        if len(questions) >= min_questions:
            return QualityGate.PASS
        return QualityGate.FAIL

    def get_status(self) -> Dict[str, Any]:
        return {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "questions": self.state.questions_count,
            "validity": self.state.validity_achieved,
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="问卷设计自进化系统")
    parser.add_argument("--action", choices=["start", "status"], default="status")
    args = parser.parse_args()

    evolution = SurveyEvolution()

    if args.action == "start":
        print(json.dumps(evolution.start_session(), ensure_ascii=False, indent=2))
    elif args.action == "status":
        print(json.dumps(evolution.get_status(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
