#!/usr/bin/env python3
"""
digital-durkheim-expert - 失范程度计算工具
计算社会失范(anomie)程度
基于涂尔干《自杀论》
"""

from typing import Dict, List, Any
import re
import json


# 失范指标
ANOMIE_INDICATORS = {
    # 规范缺失
    "normlessness": {
        "keywords": [
            "规范缺失",
            "规范混乱",
            "无规范",
            "规范失灵",
            " normless ",
            " normlessness ",
            " anomie ",
            " disorder ",
        ],
        "description": "规范缺失或失效",
    },
    # 价值崩溃
    "value_collapse": {
        "keywords": [
            "价值崩溃",
            "价值观混乱",
            "道德滑坡",
            "信念缺失",
            " value collapse ",
            " moral decline ",
            " crisis of values ",
        ],
        "description": "价值体系崩溃",
    },
    # 目标迷失
    "goal_disorientation": {
        "keywords": [
            "迷茫",
            "迷失",
            "无所适从",
            "目标缺失",
            "方向不明",
            " disoriented ",
            " lost ",
            " confused ",
        ],
        "description": "目标迷失和方向感缺失",
    },
    # 失控感
    "control_loss": {
        "keywords": [
            "失控",
            "无法控制",
            "不稳定",
            "不确定性",
            "焦虑",
            " uncertainty ",
            " unstable ",
            " out of control ",
        ],
        "description": "对社会失去控制感",
    },
    # 社会解体
    "social_disintegration": {
        "keywords": [
            "社会解体",
            "社会崩溃",
            "社会瓦解",
            "联结断裂",
            " social disintegration ",
            " breakdown ",
            " fragmentation ",
        ],
        "description": "社会联结解体",
    },
}


class AnomieCalculator:
    """失范程度计算器"""

    def __init__(self):
        self.anomie_scores = []

    def calculate_anomie(self, data: Any, time_period: str = None) -> Dict:
        """
        计算失范程度

        参数:
            data: 分析数据
            time_period: 时间段（用于纵向比较）

        返回:
            失范程度分析结果
        """
        # 转换为文本
        text = self._convert_to_text(data)

        # 计算各维度失范指数
        normlessness = self._calculate_dimension("normlessness", text)
        value_collapse = self._calculate_dimension("value_collapse", text)
        goal_disorientation = self._calculate_dimension("goal_disorientation", text)
        control_loss = self._calculate_dimension("control_loss", text)
        disintegration = self._calculate_dimension("social_disintegration", text)

        # 计算总体失范指数
        overall = self._calculate_overall_anomie(
            normlessness,
            value_collapse,
            goal_disorientation,
            control_loss,
            disintegration,
        )

        # 分类失范等级
        level = self._classify_anomie_level(overall)

        # 识别失范来源
        sources = self._identify_anomie_sources(
            normlessness,
            value_collapse,
            goal_disorientation,
            control_loss,
            disintegration,
        )

        # 生成理论解释
        explanation = self._generate_explanation(level, sources)

        return {
            "data_type": type(data).__name__,
            "time_period": time_period,
            "dimensions": {
                "normlessness": normlessness,
                "value_collapse": value_collapse,
                "goal_disorientation": goal_disorientation,
                "control_loss": control_loss,
                "disintegration": disintegration,
            },
            "overall_anomie": overall,
            "anomie_level": level,
            "sources": sources,
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

    def _calculate_dimension(self, dimension: str, text: str) -> Dict:
        """计算特定维度失范指数"""
        indicators = ANOMIE_INDICATORS.get(dimension, {})
        keywords = indicators.get("keywords", [])

        count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)
        score = min(1.0, count / 3)

        return {
            "score": score,
            "evidence_count": count,
            "description": indicators.get("description", ""),
        }

    def _calculate_overall_anomie(
        self,
        normlessness: Dict,
        value_collapse: Dict,
        goal_disorientation: Dict,
        control_loss: Dict,
        disintegration: Dict,
    ) -> float:
        """计算总体失范指数"""
        scores = [
            normlessness.get("score", 0),
            value_collapse.get("score", 0),
            goal_disorientation.get("score", 0),
            control_loss.get("score", 0),
            disintegration.get("score", 0),
        ]

        # 权重：规范缺失和价值崩溃更重要
        weights = [0.25, 0.25, 0.15, 0.15, 0.20]

        return sum(s * w for s, w in zip(scores, weights))

    def _classify_anomie_level(self, score: float) -> str:
        """分类失范等级"""
        if score >= 0.8:
            return "极高失范"
        elif score >= 0.6:
            return "高度失范"
        elif score >= 0.4:
            return "中度失范"
        elif score >= 0.2:
            return "轻度失范"
        else:
            return "正常"

    def _identify_anomie_sources(
        self,
        normlessness: Dict,
        value_collapse: Dict,
        goal_disorientation: Dict,
        control_loss: Dict,
        disintegration: Dict,
    ) -> List[Dict]:
        """识别失范主要来源"""
        sources = []

        dimensions = [
            ("规范缺失", normlessness),
            ("价值崩溃", value_collapse),
            ("目标迷失", goal_disorientation),
            ("失控感", control_loss),
            ("社会解体", disintegration),
        ]

        for name, data in dimensions:
            score = data.get("score", 0)
            if score >= 0.2:
                sources.append(
                    {
                        "source": name,
                        "contribution": score,
                        "description": data.get("description", ""),
                    }
                )

        # 按贡献度排序
        sources.sort(key=lambda x: x["contribution"], reverse=True)
        return sources[:3]

    def _generate_explanation(self, level: str, sources: List[Dict]) -> str:
        """生成理论解释"""
        if level == "正常":
            return "社会规范运作正常，个体能够正常融入社会。"

        explanations = {
            "轻度失范": "社会出现轻微的规范失调，但整体秩序仍然维持。",
            "中度失范": "社会规范出现明显失调，个体开始感到迷茫和不适。",
            "高度失范": "社会规范严重失调，普遍存在价值观念混乱。",
            "极高失范": "社会处于全面失范状态，社会秩序面临崩溃风险。",
        }

        base = explanations.get(level, "")

        if sources:
            source_names = [s.get("source") for s in sources[:2]]
            if "规范缺失" in source_names:
                base += " 主要表现为社会规范的缺失和失效。"
            elif "价值崩溃" in source_names:
                base += " 主要表现为价值体系的崩溃和道德滑坡。"
            elif "社会解体" in source_names:
                base += " 主要表现为社会联结的断裂和解体。"

        return base


def calculate_anomie(data: Any, time_period: str = None) -> Dict:
    """失范程度计算入口函数"""
    calculator = AnomieCalculator()
    return calculator.calculate_anomie(data, time_period)


if __name__ == "__main__":
    # 测试
    test_data = """
    当前社会处于快速转型期，传统规范失去约束力，
    新的规范尚未建立。价值观念多元化，传统道德滑坡。
    很多人感到迷茫和无所适从，不知道什么是正确的。
    社会不稳定因素增加，不确定性增强。
    """

    result = calculate_anomie(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
