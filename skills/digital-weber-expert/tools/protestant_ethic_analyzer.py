#!/usr/bin/env python3
"""
digital-weber-expert - 新教伦理分析工具
分析新教伦理与资本主义精神的关系
基于韦伯《新教伦理与资本主义精神》
"""

from typing import Dict, List, Any
import re
import json


PROTESTANT_ETHIC_INDICATORS = {
    "calling": {
        "keywords": ["天职", "召唤", "使命", " calling ", " vocation ", " mission "],
        "description": "天职观",
    },
    "asceticism": {
        "keywords": ["禁欲", "节俭", "勤奋", " ascetic ", " frugal ", " diligent "],
        "description": "禁欲主义",
    },
    "predestination": {
        "keywords": [
            "预定",
            "救赎",
            "选民",
            " predestination ",
            " salvation ",
            " elect ",
        ],
        "description": "预定论",
    },
    "worldly_asceticism": {
        "keywords": ["世俗", "工作", "职业", " worldly ", " work ", " profession "],
        "description": "世俗禁欲",
    },
}


class ProtestantEthicAnalyzer:
    def __init__(self):
        pass

    def analyze_protestant_ethic(self, data: Any) -> Dict:
        text = self._convert_to_text(data)
        calling = self._analyze_dimension("calling", text)
        asceticism = self._analyze_dimension("asceticism", text)
        predestination = self._analyze_dimension("predestination", text)
        worldly = self._analyze_dimension("worldly_asceticism", text)

        overall = (
            calling.get("score", 0)
            + asceticism.get("score", 0)
            + predestination.get("score", 0)
            + worldly.get("score", 0)
        ) / 4

        return {
            "dimensions": {
                "天职观": calling,
                "禁欲主义": asceticism,
                "预定论": predestination,
                "世俗禁欲": worldly,
            },
            "overall": overall,
            "explanation": f"新教伦理特征: {overall:.2f}",
        }

    def _convert_to_text(self, data):
        if isinstance(data, str):
            return data
        return json.dumps(data, ensure_ascii=False)

    def _analyze_dimension(self, dim, text):
        kw = PROTESTANT_ETHIC_INDICATORS.get(dim, {}).get("keywords", [])
        count = sum(len(re.findall(k, text, re.IGNORECASE)) for k in kw)
        return {"score": min(1.0, count / 3), "evidence_count": count}


def analyze_protestant_ethic(data: Any) -> Dict:
    return ProtestantEthicAnalyzer().analyze_protestant_ethic(data)


if __name__ == "__main__":
    test_data = "新教强调天职观，认为工作是上帝的召唤。信徒通过勤奋工作和节俭生活来证明自己是选民。"
    result = analyze_protestant_ethic(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
