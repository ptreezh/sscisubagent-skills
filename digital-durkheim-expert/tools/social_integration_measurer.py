#!/usr/bin/env python3
"""
digital-durkheim-expert - 社会整合度测量工具
测量社会整合（social integration）程度
基于涂尔干《自杀论》
"""

from typing import Dict, List, Any
import re
import json


# 社会整合指标
INTEGRATION_INDICATORS = {
    # 社会联结
    "social_bonds": {
        "strong": [
            "紧密",
            "牢固",
            "强有力",
            "频繁",
            " strong ",
            " close ",
            " tight ",
            " frequent ",
        ],
        "weak": [
            "松散",
            "薄弱",
            "疏离",
            "断裂",
            " loose ",
            " weak ",
            " fragmented ",
            " broken ",
        ],
        "description": "社会联结强度",
    },
    # 归属感
    "belonging": {
        "keywords": [
            "归属",
            "认同",
            "成员",
            "归属感",
            "认同感",
            " belonging ",
            " identity ",
            " membership ",
        ],
        "description": "成员归属感",
    },
    # 社会参与
    "participation": {
        "keywords": [
            "参与",
            "活动",
            "组织",
            "社团",
            " participation ",
            " activity ",
            " organization ",
            " group ",
        ],
        "description": "社会参与程度",
    },
    # 社会支持
    "support": {
        "keywords": [
            "支持",
            "帮助",
            "互助",
            "援助",
            " support ",
            " help ",
            " assistance ",
            " mutual ",
        ],
        "description": "社会支持网络",
    },
    # 宗教整合
    "religious_integration": {
        "keywords": [
            "宗教",
            "信仰",
            "教会",
            "仪式",
            " religious ",
            " faith ",
            " church ",
            " ritual ",
        ],
        "description": "宗教整合程度",
    },
    # 家庭整合
    "family_integration": {
        "keywords": [
            "家庭",
            "婚姻",
            "子女",
            " family ",
            " marriage ",
            " children ",
        ],
        "description": "家庭整合程度",
    },
}


class SocialIntegrationMeasurer:
    """社会整合度测量器"""

    def __init__(self):
        self.measurement_results = []

    def measure_integration(self, data: Any, measure_type: str = "general") -> Dict:
        """
        测量社会整合度

        参数:
            data: 分析数据
            measure_type: 测量类型（general/religious/family）

        返回:
            社会整合度测量结果
        """
        # 转换为文本
        text = self._convert_to_text(data)

        # 分析各维度
        social_bonds = self._analyze_social_bonds(text)
        belonging = self._analyze_dimension("belonging", text)
        participation = self._analyze_dimension("participation", text)
        support = self._analyze_dimension("support", text)

        # 根据测量类型添加特定维度
        specific = {}
        if measure_type == "religious":
            specific = self._analyze_dimension("religious_integration", text)
        elif measure_type == "family":
            specific = self._analyze_dimension("family_integration", text)

        # 计算总体整合度
        overall = self._calculate_overall_integration(
            social_bonds, belonging, participation, support, specific
        )

        # 分类等级
        level = self._classify_integration_level(overall)

        # 识别整合来源
        sources = self._identify_integration_sources(
            social_bonds, belonging, participation, support
        )

        # 生成理论解释
        explanation = self._generate_explanation(level, sources)

        return {
            "data_type": type(data).__name__,
            "measure_type": measure_type,
            "dimensions": {
                "social_bonds": social_bonds,
                "belonging": belonging,
                "participation": participation,
                "support": support,
            },
            "specific_dimension": specific if specific else None,
            "overall_integration": overall,
            "integration_level": level,
            "integration_sources": sources,
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

    def _analyze_social_bonds(self, text: str) -> Dict:
        """分析社会联结"""
        indicators = INTEGRATION_INDICATORS["social_bonds"]

        strong_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("strong", [])
        )
        weak_count = sum(
            len(re.findall(kw, text, re.IGNORECASE))
            for kw in indicators.get("weak", [])
        )

        total = strong_count + weak_count
        if total == 0:
            score = 0.5
        else:
            score = strong_count / total

        return {
            "score": score,
            "strong_indicators": strong_count,
            "weak_indicators": weak_count,
            "description": indicators.get("description", ""),
        }

    def _analyze_dimension(self, dimension: str, text: str) -> Dict:
        """分析特定维度"""
        indicators = INTEGRATION_INDICATORS.get(dimension, {})
        keywords = indicators.get("keywords", [])

        count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)
        score = min(1.0, count / 3)

        return {
            "score": score,
            "evidence_count": count,
            "description": indicators.get("description", ""),
        }

    def _calculate_overall_integration(
        self,
        social_bonds: Dict,
        belonging: Dict,
        participation: Dict,
        support: Dict,
        specific: Dict,
    ) -> float:
        """计算总体社会整合度"""
        scores = [
            social_bonds.get("score", 0.5),
            belonging.get("score", 0),
            participation.get("score", 0),
            support.get("score", 0),
        ]

        if specific:
            scores.append(specific.get("score", 0))
            weights = [0.30, 0.15, 0.15, 0.15, 0.25]
        else:
            weights = [0.35, 0.20, 0.20, 0.25]

        return sum(s * w for s, w in zip(scores, weights))

    def _classify_integration_level(self, score: float) -> str:
        """分类社会整合等级"""
        if score >= 0.8:
            return "高度整合"
        elif score >= 0.6:
            return "中度整合"
        elif score >= 0.4:
            return "低度整合"
        elif score >= 0.2:
            return "边缘整合"
        else:
            return "原子化"

    def _identify_integration_sources(
        self,
        social_bonds: Dict,
        belonging: Dict,
        participation: Dict,
        support: Dict,
    ) -> List[Dict]:
        """识别整合主要来源"""
        sources = []

        dimensions = [
            ("社会联结", social_bonds),
            ("归属感", belonging),
            ("社会参与", participation),
            ("社会支持", support),
        ]

        for name, data in dimensions:
            score = data.get("score", 0.5 if name == "社会联结" else 0)
            if score >= 0.3 or (name == "社会联结" and score >= 0.4):
                sources.append(
                    {
                        "source": name,
                        "contribution": score,
                        "description": data.get("description", ""),
                    }
                )

        sources.sort(key=lambda x: x["contribution"], reverse=True)
        return sources[:3]

    def _generate_explanation(self, level: str, sources: List[Dict]) -> str:
        """生成理论解释"""
        explanations = {
            "高度整合": "社会整合程度高，个体紧密嵌入社会网络，社会联结强。",
            "中度整合": "社会保持基本整合，个体有一定的社会联结。",
            "低度整合": "社会整合程度低，个体与社会联结较弱。",
            "边缘整合": "个体处于社会边缘，整合程度很低。",
            "原子化": "个体处于原子化状态，几乎没有社会联结。",
        }

        base = explanations.get(level, "")

        if sources:
            source_names = [s.get("source") for s in sources[:2]]
            if "社会联结" in source_names:
                base += " 主要依靠社会联结实现整合。"

        return base


def measure_integration(data: Any, measure_type: str = "general") -> Dict:
    """社会整合度测量入口函数"""
    measurer = SocialIntegrationMeasurer()
    return measurer.measure_integration(data, measure_type)


if __name__ == "__main__":
    # 测试
    test_data = """
    该群体成员之间联系紧密，经常参加集体活动。
    成员有强烈的归属感和认同感，互相帮助支持。
    形成了稳定的社会支持网络，社会凝聚力强。
    """

    result = measure_integration(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
