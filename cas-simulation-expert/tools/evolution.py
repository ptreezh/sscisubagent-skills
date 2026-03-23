#!/usr/bin/env python3
"""
复杂适应系统仿真技能 - 自进化模块
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


class CASPhase(Enum):
    INITIAL = "initial"
    MODEL_SPECIFICATION = "model_specification"
    PARAMETER_TUNING = "parameter_tuning"
    SIMULATION = "simulation"
    EMERGENCE_DETECTION = "emergence_detection"
    VALIDATION = "validation"
    COMPLETE = "complete"


@dataclass
class EvolutionState:
    iteration: int = 1
    phase: CASPhase = CASPhase.INITIAL
    quality_score: float = 0.0
    agents_defined: int = 0
    emergent_patterns: int = 0
    validation_passed: bool = False
    refinement_history: List[Dict] = field(default_factory=list)


class CASSimulationEvolution:
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
                    phase=CASPhase(data.get("phase", "initial")),
                    quality_score=data.get("quality_score", 0.0),
                    agents_defined=data.get("agents_defined", 0),
                    emergent_patterns=data.get("emergent_patterns", 0),
                    validation_passed=data.get("validation_passed", False),
                    refinement_history=data.get("refinement_history", []),
                )
        return EvolutionState()

    def _save_state(self) -> None:
        state_file = self.session_dir / "evolution_state.yaml"
        data = {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "agents_defined": self.state.agents_defined,
            "emergent_patterns": self.state.emergent_patterns,
            "validation_passed": self.state.validation_passed,
            "refinement_history": self.state.refinement_history,
            "updated_at": datetime.now().isoformat(),
        }
        with open(state_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def _load_quality_gates(self) -> Dict[str, Any]:
        return {
            "model_specification": {
                "min_agents": 10,
                "required_elements": ["states", "rules", "environment"],
            },
            "parameter_tuning": {"min_iterations": 5, "convergence": True},
            "emergence_detection": {
                "min_patterns": 1,
                "metrics": ["spatial", "temporal", "behavioral"],
            },
        }

    def start_session(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        print(f"\n{'=' * 50}")
        print(f"复杂适应系统仿真自进化系统")
        print(f"迭代: {self.state.iteration}")
        print(f"{'=' * 50}\n")

        self.state.phase = CASPhase.MODEL_SPECIFICATION
        self._save_state()

        return {"status": "started", "phase": self.state.phase.value}

    def run_quality_gate(self, gate_name: str, result: Dict[str, Any]) -> QualityGate:
        gate = self.quality_gates.get(gate_name, {})
        if not gate:
            return QualityGate.WARNING

        min_agents = gate.get("min_agents", 0)
        agents = result.get("agents", [])

        if len(agents) >= min_agents:
            return QualityGate.PASS
        return QualityGate.FAIL

    def get_status(self) -> Dict[str, Any]:
        return {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "agents": self.state.agents_defined,
            "emergent_patterns": self.state.emergent_patterns,
            "validation": self.state.validation_passed,
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="CAS仿真自进化系统")
    parser.add_argument("--action", choices=["start", "status"], default="status")
    args = parser.parse_args()

    evolution = CASSimulationEvolution()

    if args.action == "start":
        print(json.dumps(evolution.start_session(), ensure_ascii=False, indent=2))
    elif args.action == "status":
        print(json.dumps(evolution.get_status(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
