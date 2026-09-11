#!/usr/bin/env python3
"""
digital-weber-expert - 官僚制分析工具
分析官僚制特征：层级、非人格、规则、专业化
基于韦伯官僚制理论
"""

from typing import Dict, List, Any
import re
import json


BUREAUCRACY_INDICATORS = {
    "hierarchy": {
        "keywords": ["层级", "等级", "上下级", " hierarchy ", " rank ", " level "],
        "description": "层级结构",
    },
    "impersonal": {
        "keywords": [
            "非人格",
            "公私分明",
            "制度化",
            " impersonal ",
            " formal ",
            " institutional ",
        ],
        "description": "非人格化",
    },
    "rules": {
        "keywords": [
            "规则",
            "制度",
            "规章",
            "规则",
            " regulation ",
            " rule ",
            " procedure ",
        ],
        "description": "规则导向",
    },
    "specialization": {
        "keywords": [
            "专业",
            "分工",
            "职责",
            " specialization ",
            " division ",
            " expertise ",
        ],
        "description": "专业化分工",
    },
}


class BureaucracyAnalyzer:
    def __init__(self):
        pass

    def analyze_bureaucracy(self, data: Any) -> Dict:
        text = self._convert_to_text(data)
        hierarchy = self._analyze_dimension("hierarchy", text)
        impersonal = self._analyze_dimension("impersonal", text)
        rules = self._analyze_dimension("rules", text)
        specialization = self._analyze_dimension("specialization", text)

        overall = (
            hierarchy.get("score", 0)
            + impersonal.get("score", 0)
            + rules.get("score", 0)
            + specialization.get("score", 0)
        ) / 4

        return {
            "dimensions": {
                "层级": hierarchy,
                "非人格": impersonal,
                "规则": rules,
                "专业化": specialization,
            },
            "overall_bureaucracy": overall,
            "level": "高度官僚制" if overall > 0.6 else "低度官僚制",
            "explanation": f"官僚化程度: {overall:.2f}",
        }

    def _convert_to_text(self, data):
        if isinstance(data, str):
            return data
        return json.dumps(data, ensure_ascii=False)

    def _analyze_dimension(self, dim, text):
        kw = BUREAUCRACY_INDICATORS.get(dim, {}).get("keywords", [])
        count = sum(len(re.findall(k, text, re.IGNORECASE)) for k in kw)
        return {"score": min(1.0, count / 3), "evidence_count": count}


def analyze_bureaucracy(data: Any) -> Dict:
    return BureaucracyAnalyzer().analyze_bureaucracy(data)


if __name__ == "__main__":
    test_data = (
        "该组织有严格的层级结构，遵循明确的规章制度，讲究非人格化运作，专业分工明确。"
    )
    result = analyze_bureaucracy(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
