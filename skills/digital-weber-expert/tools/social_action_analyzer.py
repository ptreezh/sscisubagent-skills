#!/usr/bin/env python3
"""
digital-weber-expert - 社会行动类型分析工具
分析社会行动类型：目的理性、价值理性、传统、情感
基于韦伯社会行动理论
"""

from typing import Dict, List, Any
import re
import json


SOCIAL_ACTION_INDICATORS = {
    "purposive_rational": {
        "keywords": ["目的", "目标", "手段", "工具", " purpose ", " goal ", " means "],
        "description": "目的理性行动",
    },
    "value_rational": {
        "keywords": [
            "价值",
            "信念",
            "义务",
            "绝对命令",
            " value ",
            " belief ",
            " duty ",
        ],
        "description": "价值理性行动",
    },
    "affective": {
        "keywords": [
            "情感",
            "情绪",
            "激情",
            "感情",
            " emotion ",
            " feeling ",
            " passion ",
        ],
        "description": "情感行动",
    },
    "traditional": {
        "keywords": [
            "传统",
            "习惯",
            "惯例",
            "传统",
            " tradition ",
            " custom ",
            " habit ",
        ],
        "description": "传统行动",
    },
}


class SocialActionAnalyzer:
    def __init__(self):
        pass

    def analyze_social_action(self, data: Any) -> Dict:
        text = self._convert_to_text(data)
        purposive = self._analyze_dimension("purposive_rational", text)
        value = self._analyze_dimension("value_rational", text)
        affective = self._analyze_dimension("affective", text)
        traditional = self._analyze_dimension("traditional", text)

        scores = {
            "目的理性行动": purposive.get("score", 0),
            "价值理性行动": value.get("score", 0),
            "情感行动": affective.get("score", 0),
            "传统行动": traditional.get("score", 0),
        }
        dominant = max(scores, key=scores.get)

        return {
            "types": {
                "目的理性": purposive,
                "价值理性": value,
                "情感": affective,
                "传统": traditional,
            },
            "dominant": dominant,
            "explanation": f"主导社会行动类型: {dominant}",
        }

    def _convert_to_text(self, data):
        if isinstance(data, str):
            return data
        return json.dumps(data, ensure_ascii=False)

    def _analyze_dimension(self, dim, text):
        kw = SOCIAL_ACTION_INDICATORS.get(dim, {}).get("keywords", [])
        count = sum(len(re.findall(k, text, re.IGNORECASE)) for k in kw)
        return {"score": min(1.0, count / 3), "evidence_count": count}


def analyze_social_action(data: Any) -> Dict:
    return SocialActionAnalyzer().analyze_social_action(data)


if __name__ == "__main__":
    test_data = "人们根据目标选择手段，通过理性计算来决定行动。"
    result = analyze_social_action(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
