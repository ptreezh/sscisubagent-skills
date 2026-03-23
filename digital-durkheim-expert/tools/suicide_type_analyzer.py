#!/usr/bin/env python3
"""
digital-durkheim-expert - 自杀类型分析工具
分析自杀类型：利己型、利他型、失范型、宿命型
基于涂尔干《自杀论》
"""

from typing import Dict, List, Any, Optional
import re
import json


# 自杀类型指标
SUICIDE_TYPE_INDICATORS = {
    # 利己型自杀 (Egoistic) - 社会整合度低
    "egoistic": {
        "integration": ["低", "弱", "疏离", "孤独", "个人主义", "分离"],
        "relatedness": [
            "个人",
            "自我",
            "独立",
            "疏远",
            "孤独感",
            " low ",
            " weak ",
            " individual ",
            " isolated ",
        ],
        "description": "利己型自杀 - 社会整合度低导致个体过度关注自我",
    },
    # 利他型自杀 (Altruistic) - 社会整合度过高
    "altruistic": {
        "integration": ["高", "强", "融合", "集体", "共同体"],
        "relatedness": [
            "集体",
            "群体",
            "义务",
            "牺牲",
            "责任",
            " high ",
            " strong ",
            " collective ",
            " duty ",
        ],
        "description": "利他型自杀 - 社会整合度过高导致个体为集体牺牲",
    },
    # 失范型自杀 (Anomic) - 社会规范混乱
    "anomic": {
        "normlessness": ["混乱", "失范", "无序", "规范缺失", "价值崩溃"],
        "relatedness": [
            "规范",
            "秩序",
            "价值",
            "崩溃",
            "紊乱",
            " chaos ",
            " disorder ",
            " normless ",
        ],
        "description": "失范型自杀 - 社会规范混乱导致个体无所适从",
    },
    # 宿命型自杀 (Fatalistic) - 社会规范过度严格
    "fatalistic": {
        "overregulation": ["过度", "压抑", "控制", "严格", "限制"],
        "relatedness": [
            "绝望",
            "无助",
            "压抑",
            "无法逃脱",
            "束缚",
            "oppression",
            " desperation ",
        ],
        "description": "宿命型自杀 - 社会规范过度严格导致个体感到绝望",
    },
}


class SuicideTypeAnalyzer:
    """自杀类型分析器"""

    def __init__(self):
        self.analysis_results = []

    def analyze_suicide_types(self, data: Any, group_variable: str = None) -> Dict:
        """
        分析自杀类型

        参数:
            data: 分析数据
            group_variable: 分组变量（如宗教、国家等）

        返回:
            自杀类型分析结果
        """
        # 转换为文本
        text = self._convert_to_text(data)

        # 分析各类型指标
        egoistic = self._analyze_egoistic(text)
        altruistic = self._analyze_altruistic(text)
        anomic = self._analyze_anomic(text)
        fatalistic = self._analyze_fatalistic(text)

        # 确定主导类型
        dominant_type = self._determine_dominant_type(
            egoistic, altruistic, anomic, fatalistic
        )

        # 计算社会整合/失范指数
        integration_index = self._calculate_integration_index(egoistic, altruistic)
        anomie_index = self._calculate_anomie_index(anomic)

        # 生成理论解释
        theoretical_explanation = self._generate_explanation(
            dominant_type, integration_index, anomie_index
        )

        return {
            "data_type": type(data).__name__,
            "group_variable": group_variable,
            "types": {
                "egoistic": egoistic,
                "altruistic": altruistic,
                "anomic": anomic,
                "fatalistic": fatalistic,
            },
            "dominant_type": dominant_type,
            "indices": {
                "integration_index": integration_index,
                "anomie_index": anomie_index,
            },
            "theoretical_explanation": theoretical_explanation,
        }

    def _convert_to_text(self, data: Any) -> str:
        """将数据转换为文本"""
        if isinstance(data, str):
            return data
        elif isinstance(data, dict):
            return json.dumps(data, ensure_ascii=False)
        elif isinstance(data, list):
            return " ".join(str(item) for item in data)
        else:
            return str(data)

    def _analyze_egoistic(self, text: str) -> Dict:
        """分析利己型自杀指标"""
        indicators = SUICIDE_TYPE_INDICATORS["egoistic"]

        integration_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("integration", [])
        )
        relatedness_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("relatedness", [])
        )

        total_count = integration_count + relatedness_count
        score = min(1.0, total_count / 5)

        return {
            "score": score,
            "evidence_count": total_count,
            "description": indicators.get("description", ""),
        }

    def _analyze_altruistic(self, text: str) -> Dict:
        """分析利他型自杀指标"""
        indicators = SUICIDE_TYPE_INDICATORS["altruistic"]

        integration_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("integration", [])
        )
        relatedness_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("relatedness", [])
        )

        total_count = integration_count + relatedness_count
        score = min(1.0, total_count / 5)

        return {
            "score": score,
            "evidence_count": total_count,
            "description": indicators.get("description", ""),
        }

    def _analyze_anomic(self, text: str) -> Dict:
        """分析失范型自杀指标"""
        indicators = SUICIDE_TYPE_INDICATORS["anomic"]

        normlessness_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("normlessness", [])
        )
        relatedness_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("relatedness", [])
        )

        total_count = normlessness_count + relatedness_count
        score = min(1.0, total_count / 5)

        return {
            "score": score,
            "evidence_count": total_count,
            "description": indicators.get("description", ""),
        }

    def _analyze_fatalistic(self, text: str) -> Dict:
        """分析宿命型自杀指标"""
        indicators = SUICIDE_TYPE_INDICATORS["fatalistic"]

        overregulation_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("overregulation", [])
        )
        relatedness_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("relatedness", [])
        )

        total_count = overregulation_count + relatedness_count
        score = min(1.0, total_count / 5)

        return {
            "score": score,
            "evidence_count": total_count,
            "description": indicators.get("description", ""),
        }

    def _determine_dominant_type(
        self,
        egoistic: Dict,
        altruistic: Dict,
        anomic: Dict,
        fatalistic: Dict,
    ) -> str:
        """确定主导自杀类型"""
        scores = {
            "利己型": egoistic.get("score", 0),
            "利他型": altruistic.get("score", 0),
            "失范型": anomic.get("score", 0),
            "宿命型": fatalistic.get("score", 0),
        }

        max_type = max(scores, key=scores.get)
        max_score = scores[max_type]

        if max_score < 0.2:
            return "未确定"
        return max_type

    def _calculate_integration_index(self, egoistic: Dict, altruistic: Dict) -> float:
        """计算社会整合指数"""
        # 利己型 = 低整合，利他型 = 高整合
        ego_score = egoistic.get("score", 0)
        alt_score = altruistic.get("score", 0)

        # 整合指数 = 利他型得分 - 利己型得分 + 0.5
        return alt_score - ego_score + 0.5

    def _calculate_anomie_index(self, anomic: Dict) -> float:
        """计算失范指数"""
        return anomic.get("score", 0)

    def _generate_explanation(
        self, dominant_type: str, integration_index: float, anomie_index: float
    ) -> str:
        """生成理论解释"""
        if dominant_type == "利己型":
            return (
                "社会整合度较低，个体过度关注自我，缺乏社会联结和支持，导致自杀倾向。"
            )
        elif dominant_type == "利他型":
            return "社会整合度过高，个体完全融入集体，愿意为集体利益牺牲自我。"
        elif dominant_type == "失范型":
            return "社会规范混乱或崩溃，个体失去行为指南，感到无所适从和迷失。"
        elif dominant_type == "宿命型":
            return "社会规范过度严格，个体感到绝望和无助，认为无法逃脱现有处境。"
        else:
            return "数据不足以确定自杀类型"


def analyze_suicide_types(data: Any, group_variable: str = None) -> Dict:
    """自杀类型分析入口函数"""
    analyzer = SuicideTypeAnalyzer()
    return analyzer.analyze_suicide_types(data, group_variable)


if __name__ == "__main__":
    # 测试
    test_data = """
    该群体的社会整合度较低，个体主义倾向明显，
    社会联结薄弱，孤独感较强。缺乏集体支持和归属感。
    同时，社会规范处于混乱状态，价值观念多元，
    传统规范失去约束力。
    """

    result = analyze_suicide_types(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
