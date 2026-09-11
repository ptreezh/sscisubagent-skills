"""
消费者行为分析工具

功能：识别和评估消费者行为影响因素
"""

import json
from dataclasses import dataclass
from typing import List

@dataclass
class ConsumerFactor:
    layer: str  # cultural, social, personal, psychological
    name: str
    description: str
    impact: int  # 1-5
    evidence: List[str]

FACTOR_LAYERS = {
    'cultural': '文化因素',
    'social': '社会因素',
    'personal': '个人因素',
    'psychological': '心理因素'
}

def analyze_factors(layer: str, text: str) -> List[ConsumerFactor]:
    """分析特定层次的因素"""
    factors = []
    keywords = {
        'cultural': ['文化', '价值观', '习俗', '亚文化'],
        'social': ['参照群体', '家庭', '朋友', 'KOL'],
        'personal': ['年龄', '收入', '职业', '生活方式'],
        'psychological': ['动机', '感知', '态度', '信念']
    }
    for kw in keywords.get(layer, []):
        if kw in text:
            factors.append(ConsumerFactor(
                layer=layer,
                name=kw,
                description=f"识别到{kw}相关因素",
                impact=3,
                evidence=[f"关键词匹配: {kw}"]
            ))
    return factors

if __name__ == '__main__':
    print("Consumer Behavior Analysis Tool v5.0.0")
