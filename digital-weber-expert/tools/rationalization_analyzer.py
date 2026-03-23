#!/usr/bin/env python3
"""
digital-weber-expert - 理性化分析工具
分析社会理性化程度：目的理性、价值理性、传统理性、情感理性
基于韦伯社会行动理论
"""

from typing import Dict, List, Any
import re
import json


# 理性化指标
RATIONALIZATION_INDICATORS = {
    # 目的理性
    "purposive_rational": {
        "keywords": [
            "目的",
            "目标",
            "效率",
            "计算",
            "利益",
            " purpose ",
            " goal ",
            " efficiency ",
            " calculation ",
            " interest ",
        ],
        "description": "目的理性 - 以目标为导向的工具合理性",
    },
    # 价值理性
    "value_rational": {
        "keywords": [
            "价值",
            "信念",
            "义务",
            "责任",
            "伦理",
            " value ",
            " belief ",
            " duty ",
            " ethics ",
        ],
        "description": "价值理性 - 以价值信念为导向的合理性",
    },
    # 传统理性
    "traditional_rational": {
        "keywords": [
            "传统",
            "习惯",
            "惯例",
            "风俗",
            " heritage ",
            " custom ",
            " tradition ",
            " convention ",
        ],
        "description": "传统理性 - 基于传统习惯的合理性",
    },
    # 情感理性
    "affective_rational": {
        "keywords": [
            "情感",
            "情绪",
            "激情",
            "感情",
            " emotion ",
            " feeling ",
            " passion ",
            " affect ",
        ],
        "description": "情感理性 - 基于情感冲动的行为",
    },
}


class RationalizationAnalyzer:
    """理性化分析器"""

    def __init__(self):
        self.analysis_results = []

    def analyze_rationalization(self, data: Any, focus: str = None) -> Dict:
        """
        分析理性化程度

        参数:
            data: 分析数据
            focus: 关注重点

        返回:
            理性化分析结果
        """
        # 转换为文本
        text = self._convert_to_text(data)

        # 分析各理性类型
        purposive = self._analyze_dimension("purposive_rational", text)
        value = self._analyze_dimension("value_rational", text)
        traditional = self._analyze_dimension("traditional_rational", text)
        affective = self._analyze_dimension("affective_rational", text)

        # 确定主导理性类型
        dominant = self._determine_dominant_rational(
            purposive, value, traditional, affective
        )

        # 计算理性化程度
        rationalization_degree = self._calculate_rationalization_degree(
            purposive, value
        )

        # 生成理论解释
        explanation = self._generate_explanation(dominant, rationalization_degree)

        return {
            "data_type": type(data).__name__,
            "focus": focus,
            "rational_types": {
                "purposive_rational": purposive,
                "value_rational": value,
                "traditional_rational": traditional,
                "affective_rational": affective,
            },
            "dominant_type": dominant,
            "rationalization_degree": rationalization_degree,
            "explanation": explanation,
        }

    def _convert_to_text(self, data: Any) -> str:
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            return json.dumps(data, ensure_ascii=False)
        elif isinstance(data, list):
            return " ".join(str(item) for item in data)
        else:
            return str(data)

    def _analyze_dimension(self, dimension: str, text: str) -> Dict:
        indicators = RATIONALIZATION_INDICATORS.get(dimension, {})
        keywords = indicators.get("keywords", [])
        count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)
        score = min(1.0, count / 3)
        return {
            "score": score,
            "evidence_count": count,
            "description": indicators.get("description", ""),
        }

    def _determine_dominant_rational(self, purposive, value, traditional, affective):
        scores = {
            "目的理性": purposive.get("score", 0),
            "价值理性": value.get("score", 0),
            "传统理性": traditional.get("score", 0),
            "情感理性": affective.get("score", 0),
        }
        max_type = max(scores, key=scores.get)
        max_score = scores[max_type]
        if max_score < 0.2:
            return "未确定"
        return max_type

    def _calculate_rationalization_degree(self, purposive, value):
        return (purposive.get("score", 0) + value.get("score", 0)) / 2

    def _generate_explanation(self, dominant, degree):
        if degree > 0.6:
            level = "高度理性化"
        elif degree > 0.3:
            level = "中等理性化"
        else:
            level = "低度理性化"
        return f"{level}社会，主要以{dominant}为主。"


def analyze_rationalization(data: Any, focus: str = None) -> Dict:
    analyzer = RationalizationAnalyzer()
    return analyzer.analyze_rationalization(data, focus)


if __name__ == "__main__":
    test_data = """
    现代资本主义社会以目的理性为主导。
    人们追求效率最大化，进行理性计算。
    目标和利益成为行动的主要驱动力。
    """
    result = analyze_rationalization(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
