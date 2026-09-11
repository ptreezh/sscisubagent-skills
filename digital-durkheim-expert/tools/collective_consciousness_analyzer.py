#!/usr/bin/env python3
"""
digital-durkheim-expert - 集体意识分析工具
分析集体意识（collective consciousness）的强度和内容
基于涂尔干《宗教生活的基本形式》
"""

from typing import Dict, List, Any
import re
import json


# 集体意识指标
COLLECTIVE_CONSCIOUSNESS_INDICATORS = {
    # 强度指标
    "intensity": {
        "strong": [
            "强烈",
            "深厚",
            "强有力",
            "坚定",
            "强烈",
            " strong ",
            " powerful ",
            " intense ",
        ],
        "weak": [
            "薄弱",
            "淡薄",
            "微弱",
            "脆弱",
            " weak ",
            " faint ",
            " fragile ",
        ],
        "description": "集体意识强度",
    },
    # 共同信念
    "shared_beliefs": {
        "keywords": [
            "信念",
            "信仰",
            "价值观",
            "理念",
            " belief ",
            " faith ",
            " values ",
            " ideology ",
        ],
        "description": "共同信念和价值观",
    },
    # 集体表征
    "representations": {
        "keywords": [
            "象征",
            "符号",
            "标志",
            "仪式",
            "符号",
            " symbol ",
            " ritual ",
            " emblem ",
        ],
        "description": "集体表征和象征",
    },
    # 集体情感
    "collective_sentiments": {
        "keywords": [
            "情感",
            "情绪",
            "感情",
            "激情",
            " sentiment ",
            " emotion ",
            " passion ",
        ],
        "description": "集体情感和情绪",
    },
    # 社会团结
    "social_bond": {
        "keywords": [
            "团结",
            "凝聚",
            "联结",
            "纽带",
            " solidarity ",
            " cohesion ",
            " bond ",
            " unity ",
        ],
        "description": "社会联结和团结",
    },
}


class CollectiveConsciousnessAnalyzer:
    """集体意识分析器"""

    def __init__(self):
        self.analysis_results = []

    def analyze_collective_consciousness(self, data: Any, group: str = None) -> Dict:
        """
        分析集体意识

        参数:
            data: 分析数据
            group: 分析群体

        返回:
            集体意识分析结果
        """
        # 转换为文本
        text = self._convert_to_text(data)

        # 分析各维度
        intensity = self._analyze_intensity(text)
        shared_beliefs = self._analyze_dimension("shared_beliefs", text)
        representations = self._analyze_dimension("representations", text)
        sentiments = self._analyze_dimension("collective_sentiments", text)
        social_bond = self._analyze_dimension("social_bond", text)

        # 计算总体强度
        overall = self._calculate_overall(
            intensity, shared_beliefs, representations, sentiments, social_bond
        )

        # 分类等级
        level = self._classify_level(overall)

        # 识别主要特征
        features = self._identify_features(
            intensity, shared_beliefs, representations, sentiments, social_bond
        )

        # 生成理论解释
        explanation = self._generate_explanation(level, features)

        return {
            "data_type": type(data).__name__,
            "group": group,
            "dimensions": {
                "intensity": intensity,
                "shared_beliefs": shared_beliefs,
                "representations": representations,
                "sentiments": sentiments,
                "social_bond": social_bond,
            },
            "overall_strength": overall,
            "consciousness_level": level,
            "main_features": features,
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

    def _analyze_intensity(self, text: str) -> Dict:
        """分析集体意识强度"""
        indicators = COLLECTIVE_CONSCIOUSNESS_INDICATORS["intensity"]

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
            # 强度 = 强指标 / (强指标 + 弱指标)
            score = strong_count / total

        return {
            "score": score,
            "strong_count": strong_count,
            "weak_count": weak_count,
            "description": indicators.get("description", ""),
        }

    def _analyze_dimension(self, dimension: str, text: str) -> Dict:
        """分析特定维度"""
        indicators = COLLECTIVE_CONSCIOUSNESS_INDICATORS.get(dimension, {})
        keywords = indicators.get("keywords", [])

        count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)
        score = min(1.0, count / 3)

        return {
            "score": score,
            "evidence_count": count,
            "description": indicators.get("description", ""),
        }

    def _calculate_overall(
        self,
        intensity: Dict,
        shared_beliefs: Dict,
        representations: Dict,
        sentiments: Dict,
        social_bond: Dict,
    ) -> float:
        """计算总体集体意识强度"""
        scores = [
            intensity.get("score", 0.5),
            shared_beliefs.get("score", 0),
            representations.get("score", 0),
            sentiments.get("score", 0),
            social_bond.get("score", 0),
        ]

        # 权重
        weights = [0.30, 0.20, 0.15, 0.15, 0.20]

        return sum(s * w for s, w in zip(scores, weights))

    def _classify_level(self, score: float) -> str:
        """分类集体意识等级"""
        if score >= 0.8:
            return "极强"
        elif score >= 0.6:
            return "强"
        elif score >= 0.4:
            return "中等"
        elif score >= 0.2:
            return "弱"
        else:
            return "极弱"

    def _identify_features(
        self,
        intensity: Dict,
        shared_beliefs: Dict,
        representations: Dict,
        sentiments: Dict,
        social_bond: Dict,
    ) -> List[Dict]:
        """识别主要特征"""
        features = []

        dimensions = [
            ("强度", intensity),
            ("共同信念", shared_beliefs),
            ("集体表征", representations),
            ("集体情感", sentiments),
            ("社会联结", social_bond),
        ]

        for name, data in dimensions:
            score = data.get("score", 0)
            if score >= 0.2:
                features.append(
                    {
                        "feature": name,
                        "strength": score,
                        "description": data.get("description", ""),
                    }
                )

        features.sort(key=lambda x: x["strength"], reverse=True)
        return features[:3]

    def _generate_explanation(self, level: str, features: List[Dict]) -> str:
        """生成理论解释"""
        explanations = {
            "极强": "集体意识极强，社会高度整合，个体完全融入集体。",
            "强": "集体意识强，社会凝聚力强，共同价值观主导行为。",
            "中等": "集体意识中等，社会保持基本整合。",
            "弱": "集体意识弱，个体化趋势明显，社会联结松散。",
            "极弱": "集体意识极弱，社会处于原子化状态。",
        }

        base = explanations.get(level, "")

        if features:
            feature_names = [f.get("feature") for f in features]
            if "共同信念" in feature_names:
                base += " 共同信念是集体意识的核心。"

        return base


def analyze_collective_consciousness(data: Any, group: str = None) -> Dict:
    """集体意识分析入口函数"""
    analyzer = CollectiveConsciousnessAnalyzer()
    return analyzer.analyze_collective_consciousness(data, group)


if __name__ == "__main__":
    # 测试
    test_data = """
    该宗教群体拥有强烈的集体意识。成员共享相同的信念和价值观，
    定期参加集体仪式，使用共同的宗教符号。集体情感深厚，
    成员之间团结互助，社会凝聚力强。
    """

    result = analyze_collective_consciousness(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
