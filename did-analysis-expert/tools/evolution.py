#!/usr/bin/env python3
"""
双重差分分析技能 - 自进化模块
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


class DIDPhase(Enum):
    INITIAL = "initial"
    IDENTIFICATION = "identification"
    PARALLEL_TRENDS = "parallel_trends"
    ESTIMATION = "estimation"
    ROBUSTNESS = "robustness"
    COMPLETE = "complete"


@dataclass
class EvolutionState:
    iteration: int = 1
    phase: DIDPhase = DIDPhase.INITIAL
    quality_score: float = 0.0
    identification_valid: bool = False
    parallel_trends_passed: bool = False
    refinement_history: List[Dict] = field(default_factory=list)


class DIDEvolution:
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
                    phase=DIDPhase(data.get("phase", "initial")),
                    quality_score=data.get("quality_score", 0.0),
                    identification_valid=data.get("identification_valid", False),
                    parallel_trends_passed=data.get("parallel_trends_passed", False),
                    refinement_history=data.get("refinement_history", []),
                )
        return EvolutionState()

    def _save_state(self) -> None:
        state_file = self.session_dir / "evolution_state.yaml"
        data = {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "identification_valid": self.state.identification_valid,
            "parallel_trends_passed": self.state.parallel_trends_passed,
            "refinement_history": self.state.refinement_history,
            "updated_at": datetime.now().isoformat(),
        }
        with open(state_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def _load_quality_gates(self) -> Dict[str, Any]:
        return {
            "identification": {
                "required": ["treatment", "control", "pre", "post"],
                "exogeneity": True,
            },
            "parallel_trends": {"test_required": True, "p_value": 0.05},
            "estimation": {"methods": ["fixed_effects", "random_effects", "did"]},
        }

    def start_session(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        print(f"\n{'=' * 50}")
        print(f"双重差分分析自进化系统")
        print(f"迭代: {self.state.iteration}")
        print(f"{'=' * 50}\n")

        self.state.phase = DIDPhase.IDENTIFICATION
        self._save_state()

        return {"status": "started", "phase": self.state.phase.value}

    def run_quality_gate(self, gate_name: str, result: Dict[str, Any]) -> QualityGate:
        gate = self.quality_gates.get(gate_name, {})
        if not gate:
            return QualityGate.WARNING

        if gate_name == "parallel_trends":
            p_value = result.get("p_value", 1.0)
            threshold = gate.get("p_value", 0.05)
            if p_value <= threshold:
                self.state.parallel_trends_passed = True
                return QualityGate.PASS
            return QualityGate.FAIL

        return QualityGate.PASS

    def get_status(self) -> Dict[str, Any]:
        return {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "identification": self.state.identification_valid,
            "parallel_trends": self.state.parallel_trends_passed,
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="DID自进化系统")
    parser.add_argument("--action", choices=["start", "status"], default="status")
    args = parser.parse_args()

    evolution = DIDEvolution()

    if args.action == "start":
        print(json.dumps(evolution.start_session(), ensure_ascii=False, indent=2))
    elif args.action == "status":
        print(json.dumps(evolution.get_status(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
