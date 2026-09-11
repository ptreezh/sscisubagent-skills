#!/usr/bin/env python3
"""
digital-weber-expert - 权威类型分析工具
分析权威类型：传统型、魅力型、法理型
基于韦伯权威理论
"""

from typing import Dict, List, Any
import re
import json


AUTHORITY_INDICATORS = {
    "traditional": {
        "keywords": ["传统", "习俗", "惯例", " hereditary ", " tradition ", " custom "],
        "description": "传统型权威",
    },
    "charismatic": {
        "keywords": ["魅力", "领袖", "个人", " charisma ", " leader ", " personal "],
        "description": "魅力型权威",
    },
    "legal_rational": {
        "keywords": ["法律", "制度", "规则", "法律", " law ", "制度", " regulation "],
        "description": "法理型权威",
    },
}


class AuthorityAnalyzer:
    def __init__(self):
        pass

    def analyze_authority(self, data: Any) -> Dict:
        text = self._convert_to_text(data)
        traditional = self._analyze_dimension("traditional", text)
        charismatic = self._analyze_dimension("charismatic", text)
        legal = self._analyze_dimension("legal_rational", text)

        scores = {
            "传统型": traditional.get("score", 0),
            "魅力型": charismatic.get("score", 0),
            "法理型": legal.get("score", 0),
        }
        dominant = max(scores, key=scores.get)

        return {
            "types": {"传统型": traditional, "魅力型": charismatic, "法理型": legal},
            "dominant": dominant,
            "explanation": f"主导权威类型: {dominant}",
        }

    def _convert_to_text(self, data):
        if isinstance(data, str):
            return data
        return json.dumps(data, ensure_ascii=False)

    def _analyze_dimension(self, dim, text):
        kw = AUTHORITY_INDICATORS.get(dim, {}).get("keywords", [])
        count = sum(len(re.findall(k, text, re.IGNORECASE)) for k in kw)
        return {"score": min(1.0, count / 3), "evidence_count": count}


def analyze_authority(data: Any) -> Dict:
    return AuthorityAnalyzer().analyze_authority(data)


if __name__ == "__main__":
    test_data = "该公司有严格的规章制度和法律体系，组织运行依靠理性的法律制度。"
    result = analyze_authority(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
