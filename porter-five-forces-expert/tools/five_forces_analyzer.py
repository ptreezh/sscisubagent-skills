"""
波特五力分析工具

功能：识别和评估五力因素
"""

import json
from dataclasses import dataclass
from typing import List

@dataclass
class ForceFactor:
    force_type: str  # rivalry, entry, substitute, supplier, buyer
    name: str
    description: str
    intensity: int  # 1-5
    evidence: List[str]

FORCE_TYPES = {
    'rivalry': '现有竞争者竞争程度',
    'entry': '潜在进入者威胁',
    'substitute': '替代品威胁',
    'supplier': '供应商议价能力',
    'buyer': '买方议价能力'
}

def analyze_force(force_type: str, text: str) -> List[ForceFactor]:
    """分析特定力量的因素"""
    factors = []
    # 简化实现，实际应用中可接入NLP模型
    keywords = {
        'rivalry': ['竞争', '价格战', '市场份额'],
        'entry': ['进入壁垒', '资本需求', '政策限制'],
        'substitute': ['替代', '替代品', '新技术'],
        'supplier': ['供应商', '原材料', '议价'],
        'buyer': ['客户', '消费者', '价格敏感']
    }
    for kw in keywords.get(force_type, []):
        if kw in text:
            factors.append(ForceFactor(
                force_type=force_type,
                name=kw,
                description=f"识别到{kw}相关因素",
                intensity=3,
                evidence=[f"关键词匹配: {kw}"]
            ))
    return factors

if __name__ == '__main__':
    print("Porter Five Forces Analysis Tool v5.0.0")
