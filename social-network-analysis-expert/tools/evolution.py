#!/usr/bin/env python3
"""
社会网络分析技能 - 自进化模块
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


class SNAPhase(Enum):
    INITIAL = "initial"
    NETWORK_CONSTRUCTION = "network_construction"
    CENTRALITY_ANALYSIS = "centrality_analysis"
    COMMUNITY_DETECTION = "community_detection"
    DYNAMIC_ANALYSIS = "dynamic_analysis"
    COMPLETE = "complete"


@dataclass
class EvolutionState:
    iteration: int = 1
    phase: SNAPhase = SNAPhase.INITIAL
    quality_score: float = 0.0
    nodes_analyzed: int = 0
    communities_detected: int = 0
    refinement_history: List[Dict] = field(default_factory=list)


class SocialNetworkEvolution:
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
                    phase=SNAPhase(data.get("phase", "initial")),
                    quality_score=data.get("quality_score", 0.0),
                    nodes_analyzed=data.get("nodes_analyzed", 0),
                    communities_detected=data.get("communities_detected", 0),
                    refinement_history=data.get("refinement_history", []),
                )
        return EvolutionState()

    def _save_state(self) -> None:
        state_file = self.session_dir / "evolution_state.yaml"
        data = {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "nodes_analyzed": self.state.nodes_analyzed,
            "communities_detected": self.state.communities_detected,
            "refinement_history": self.state.refinement_history,
            "updated_at": datetime.now().isoformat(),
        }
        with open(state_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def _load_quality_gates(self) -> Dict[str, Any]:
        return {
            "network_construction": {"min_nodes": 10, "min_edges": 5},
            "centrality_analysis": {
                "required_metrics": ["degree", "betweenness", "closeness"]
            },
            "community_detection": {"min_communities": 2, "algorithm": True},
        }

    def start_session(self, data: Dict[str, Any] = None) -> Dict[str, Any]:
        print(f"\n{'=' * 50}")
        print(f"社会网络分析自进化系统")
        print(f"迭代: {self.state.iteration}")
        print(f"{'=' * 50}\n")

        self.state.phase = SNAPhase.NETWORK_CONSTRUCTION
        self._save_state()

        return {"status": "started", "phase": self.state.phase.value}

    def run_quality_gate(self, gate_name: str, result: Dict[str, Any]) -> QualityGate:
        gate = self.quality_gates.get(gate_name, {})
        if not gate:
            return QualityGate.WARNING

        min_nodes = gate.get("min_nodes", 0)
        nodes = result.get("nodes", [])

        if len(nodes) >= min_nodes:
            return QualityGate.PASS
        return QualityGate.FAIL

    def get_status(self) -> Dict[str, Any]:
        return {
            "iteration": self.state.iteration,
            "phase": self.state.phase.value,
            "quality_score": self.state.quality_score,
            "nodes": self.state.nodes_analyzed,
            "communities": self.state.communities_detected,
        }


def main():
    import argparse

    parser = argparse.ArgumentParser(description="社会网络分析自进化系统")
    parser.add_argument("--action", choices=["start", "status"], default="status")
    args = parser.parse_args()

    evolution = SocialNetworkEvolution()

    if args.action == "start":
        print(json.dumps(evolution.start_session(), ensure_ascii=False, indent=2))
    elif args.action == "status":
        print(json.dumps(evolution.get_status(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
