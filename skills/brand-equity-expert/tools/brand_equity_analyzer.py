"""
品牌资产评估工具

功能：评估品牌资产五维度
"""

import json
from dataclasses import dataclass
from typing import List

@dataclass
class BrandEquityScore:
    dimension: str  # loyalty, awareness, quality, associations, other
    score: float  # 1-5
    metrics: dict

EQUITY_DIMENSIONS = {
    'loyalty': '品牌忠诚度',
    'awareness': '品牌认知度',
    'quality': '感知质量',
    'associations': '品牌联想',
    'other': '其他资产'
}

def calculate_brand_equity(scores: List[BrandEquityScore]) -> float:
    """计算品牌资产综合得分"""
    weights = {
        'loyalty': 0.25,
        'awareness': 0.20,
        'quality': 0.25,
        'associations': 0.20,
        'other': 0.10
    }
    total = sum(s.score * weights.get(s.dimension, 0) for s in scores)
    return total

if __name__ == '__main__':
    print("Brand Equity Assessment Tool v5.0.0")
