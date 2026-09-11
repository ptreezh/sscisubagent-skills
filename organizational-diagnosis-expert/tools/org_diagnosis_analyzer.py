"""
组织诊断工具

功能：评估组织六盒健康状况
"""

import json
from dataclasses import dataclass
from typing import List

@dataclass
class BoxScore:
    box: str  # purposes, structure, relationships, leadership, rewards, mechanisms
    score: float  # 1-5
    issues: List[str]

SIX_BOXES = {
    'purposes': '目的/目标',
    'structure': '结构',
    'relationships': '关系',
    'leadership': '领导',
    'rewards': '激励',
    'mechanisms': '机制'
}

def calculate_org_health(scores: List[BoxScore]) -> float:
    """计算组织健康综合得分"""
    if not scores:
        return 0
    return sum(s.score for s in scores) / len(scores)

def identify_critical_boxes(scores: List[BoxScore], threshold: float = 2.5) -> List[str]:
    """识别严重问题盒子"""
    return [s.box for s in scores if s.score < threshold]

if __name__ == '__main__':
    print("Organizational Diagnosis Tool v5.0.0")
