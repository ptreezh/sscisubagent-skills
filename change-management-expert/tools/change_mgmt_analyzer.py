"""
变革管理工具

功能：评估变革进度和阻力
"""

import json
from dataclasses import dataclass
from typing import List

@dataclass
class ChangeStep:
    step: int  # 1-8
    name: str
    status: str  # pending, in_progress, completed
    progress: float  # 0-100

STEP_NAMES = {
    1: '建立紧迫感',
    2: '组建变革联盟',
    3: '制定变革愿景',
    4: '沟通变革愿景',
    5: '授权广泛行动',
    6: '创造短期胜利',
    7: '巩固成果深化',
    8: '根植文化'
}

def calculate_change_progress(steps: List[ChangeStep]) -> float:
    """计算变革整体进度"""
    if not steps:
        return 0
    return sum(s.progress for s in steps) / len(steps)

def identify_bottleneck(steps: List[ChangeStep]) -> int:
    """识别变革瓶颈步骤"""
    for s in steps:
        if s.status == 'in_progress' and s.progress < 50:
            return s.step
    return 0

if __name__ == '__main__':
    print("Change Management Tool v5.0.0")
