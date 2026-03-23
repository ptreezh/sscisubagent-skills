#!/usr/bin/env python3
"""
digital-durkheim-expert - 团结类型分析工具
分析社会团结类型：机械团结、有机团结、混合型
基于涂尔干《社会分工论》
"""

from typing import Dict, List, Any
import re
import json


# 团结类型指标
SOLIDARITY_INDICATORS = {
    # 机械团结 - 基于相似性
    "mechanical": {
        "similarity": [
            "相似",
            "相同",
            "一致",
            "共同",
            "集体",
            "同质",
            " similar ",
            " same ",
            " collective ",
            " homogeneous ",
        ],
        "conscience": [
            "集体意识",
            "共同信念",
            "共同价值观",
            " shared belief ",
            " common values ",
        ],
        "description": "机械团结 - 基于成员相似性和共同集体意识",
    },
    # 有机团结 - 基于差异性和相互依赖
    "organic": {
        "difference": [
            "差异",
            "不同",
            "分工",
            "专业",
            "相互依赖",
            " different ",
            " division ",
            " specialized ",
            " interdependence ",
        ],
        "cooperation": [
            "合作",
            "互助",
            "依赖",
            "联系",
            " cooperation ",
            " dependency ",
            " connection ",
        ],
        "description": "有机团结 - 基于社会分工和相互依赖",
    },
    # 过渡型团结
    "transitional": {
        "mixed": [
            "转型",
            "过渡",
            "变化",
            "转变",
            " transition ",
            " changing ",
        ],
        "description": "过渡型团结 - 机械团结向有机团结转变",
    },
}


class SolidarityAnalyzer:
    """团结类型分析器"""

    def __init__(self):
        self.analysis_results = []

    def analyze_solidarity(self, data: Any, society_type: str = None) -> Dict:
        """
        分析社会团结类型

        参数:
            data: 分析数据
            society_type: 社会类型（传统/现代）

        返回:
            团结类型分析结果
        """
        # 转换为文本
        text = self._convert_to_text(data)

        # 分析各类型指标
        mechanical = self._analyze_mechanical(text)
        organic = self._analyze_organic(text)
        transitional = self._analyze_transitional(text)

        # 确定主导类型
        dominant_type = self._determine_dominant_type(mechanical, organic, transitional)

        # 计算团结强度
        strength = self._calculate_solidarity_strength(mechanical, organic)

        # 生成理论解释
        explanation = self._generate_explanation(dominant_type, strength)

        return {
            "data_type": type(data).__name__,
            "society_type": society_type,
            "types": {
                "mechanical": mechanical,
                "organic": organic,
                "transitional": transitional,
            },
            "dominant_type": dominant_type,
            "solidarity_strength": strength,
            "explanation": explanation,
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

    def _analyze_mechanical(self, text: str) -> Dict:
        """分析机械团结指标"""
        indicators = SOLIDARITY_INDICATORS["mechanical"]

        similarity_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("similarity", [])
        )
        conscience_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("conscience", [])
        )

        total_count = similarity_count + conscience_count
        score = min(1.0, total_count / 5)

        return {
            "score": score,
            "evidence_count": total_count,
            "description": indicators.get("description", ""),
        }

    def _analyze_organic(self, text: str) -> Dict:
        """分析有机团结指标"""
        indicators = SOLIDARITY_INDICATORS["organic"]

        difference_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("difference", [])
        )
        cooperation_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("cooperation", [])
        )

        total_count = difference_count + cooperation_count
        score = min(1.0, total_count / 5)

        return {
            "score": score,
            "evidence_count": total_count,
            "description": indicators.get("description", ""),
        }

    def _analyze_transitional(self, text: str) -> Dict:
        """分析过渡型团结指标"""
        indicators = SOLIDARITY_INDICATORS["transitional"]

        count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("mixed", [])
        )

        score = min(1.0, count / 3)

        return {
            "score": score,
            "evidence_count": count,
            "description": indicators.get("description", ""),
        }

    def _determine_dominant_type(
        self, mechanical: Dict, organic: Dict, transitional: Dict
    ) -> str:
        """确定主导团结类型"""
        scores = {
            "机械团结": mechanical.get("score", 0),
            "有机团结": organic.get("score", 0),
            "过渡型团结": transitional.get("score", 0),
        }

        max_type = max(scores, key=scores.get)
        max_score = scores[max_type]

        if max_score < 0.2:
            return "未确定"
        return max_type

    def _calculate_solidarity_strength(self, mechanical: Dict, organic: Dict) -> float:
        """计算团结强度"""
        mech_score = mechanical.get("score", 0)
        org_score = organic.get("score", 0)

        # 团结强度 = 两种团结类型的平均
        return (mech_score + org_score) / 2

    def _generate_explanation(self, dominant_type: str, strength: float) -> str:
        """生成理论解释"""
        if dominant_type == "机械团结":
            return (
                "该社会主要依靠成员间的相似性和共同信念维系团结。"
                "集体意识强烈，社会整合主要通过共同的价值观和规范实现。"
                "个人与集体高度同质化，社会凝聚力来自于相似性。"
            )
        elif dominant_type == "有机团结":
            return (
                "该社会主要依靠社会分工和成员间的相互依赖维系团结。"
                "社会高度分化，不同个体承担不同角色。"
                "社会凝聚力来自于功能上的相互补充和依赖。"
            )
        elif dominant_type == "过渡型团结":
            return (
                "该社会正处于从机械团结向有机团结的转型期。"
                "传统集体意识与现代化分工并存，社会团结机制正在演变。"
            )
        else:
            return "数据不足以确定团结类型"


def analyze_solidarity(data: Any, society_type: str = None) -> Dict:
    """团结类型分析入口函数"""
    analyzer = SolidarityAnalyzer()
    return analyzer.analyze_solidarity(data, society_type)


if __name__ == "__main__":
    # 测试
    test_data = """
    在传统农村社会，成员之间高度相似，共享相同的价值观和信念。
    集体意识强烈，社会规范约束着每个人的行为。
    人们从事类似的工作，遵循相同的传统习俗。
    个人与集体紧密联系，社会凝聚力强。
    """

    result = analyze_solidarity(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
