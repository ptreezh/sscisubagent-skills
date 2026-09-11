#!/usr/bin/env python3
"""
consumer-behavior-expert - Darwin evolution module
"""

import json
import yaml
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any

class SkillEvolution:
    def __init__(self, skill_dir=None):
        if skill_dir:
            self.skill_dir = Path(skill_dir)
        else:
            self.skill_dir = Path(__file__).parent
        self.session_dir = self.skill_dir / ".evolution"
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self._load_state()

    def _load_state(self):
        f = self.session_dir / "evolution_state.yaml"
        self._data = yaml.safe_load(open(f, encoding='utf-8')) if f.exists() else {'quality_score': 0.0, 'refinement_history': [], 'improved': False}

    def _save_state(self):
        f = self.session_dir / "evolution_state.yaml"
        self._data['updated_at'] = datetime.now(timezone.utc).isoformat()
        yaml.dump(self._data, open(f, 'w', encoding='utf-8'), allow_unicode=True, default_flow_style=False)

    def record_refinement(self, iteration, action, delta=0.0):
        hist = self._data.get('refinement_history', [])
        hist.append({'iteration': iteration, 'action': action, 'delta': round(delta, 2), 'ts': datetime.now(timezone.utc).isoformat()})
        self._data['refinement_history'] = hist
        if delta > 0:
            self._data['improved'] = True
        self._save_state()

    def get_status(self):
        return {'skill': 'consumer-behavior-expert', 'quality_score': self._data.get('quality_score', 0.0), 'improved': self._data.get('improved', False), 'rounds': len(self._data.get('refinement_history', [])), 'phase': self._data.get('phase', 'initial')}

def main():
    import argparse
    p = argparse.ArgumentParser(description='consumer-behavior-expert Darwin')
    p.add_argument('--action', choices=['status', 'record'], default='status')
    p.add_argument('--iter', type=int, default=1)
    p.add_argument('--delta', type=float, default=0.0)
    args = p.parse_args()
    evo = SkillEvolution()
    if args.action == 'record':
        evo.record_refinement(args.iter, 'darwin_eval', args.delta)
    print(json.dumps(evo.get_status(), ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
