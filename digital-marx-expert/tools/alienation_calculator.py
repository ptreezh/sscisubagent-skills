#!/usr/bin/env python3
"""
digital-marx-expert - 异化程度计算工具
计算劳动异化程度：产品异化、劳动过程异化、自我异化、类本质异化
基于马克思《1844年经济学哲学手稿》
"""

from typing import Dict, List, Any
import re
import json


# 异化指标
ALIENATION_INDICATORS = {
    # 产品异化
    "product_alienation": {
        "keywords": [
            "产品",
            "成果",
            "不属于自己",
            "失去",
            "被剥夺",
            " product ",
            " output ",
            " not belong to ",
            " deprived ",
        ],
        "description": "产品异化 - 劳动产品不属于劳动者",
    },
    # 劳动过程异化
    "process_alienation": {
        "keywords": [
            "劳动",
            "工作",
            "痛苦",
            "折磨",
            "压抑",
            "强制",
            " labor ",
            " work ",
            " painful ",
            " forced ",
        ],
        "description": "劳动过程异化 - 劳动对劳动者来说是外在的",
    },
    # 自我异化
    "self_alienation": {
        "keywords": [
            "自我",
            "个性",
            "发展",
            "实现",
            "潜能",
            "自我实现",
            " self ",
            " personality ",
            " development ",
            " potential ",
        ],
        "description": "自我异化 - 劳动者无法实现自我",
    },
    # 类本质异化
    "species_alienation": {
        "keywords": [
            "类本质",
            "社会性",
            "交往",
            "合作",
            "有意识",
            " species-being ",
            " social ",
            " conscious ",
        ],
        "description": "类本质异化 - 劳动者失去社会性",
    },
    # 数字劳动异化
    "digital_alienation": {
        "keywords": [
            "数据",
            "平台",
            "监控",
            "算法",
            "评分",
            " data ",
            " platform ",
            " surveillance ",
            " algorithm ",
        ],
        "description": "数字劳动异化 - 数字时代的特殊异化形式",
    },
}


class AlienationCalculator:
    """异化程度计算器"""

    def __init__(self):
        self.calculation_results = []

    def calculate_alienation(self, data: Any, labor_type: str = "general") -> Dict:
        """
        计算异化程度

        参数:
            data: 分析数据
            labor_type: 劳动类型（general/digital）

        返回:
            异化程度分析结果
        """
        # 转换为文本
        text = self._convert_to_text(data)

        # 计算各维度异化
        product = self._calculate_dimension("product_alienation", text)
        process = self._calculate_dimension("process_alienation", text)
        self_alien = self._calculate_dimension("self_alienation", text)
        species = self._calculate_dimension("species_alienation", text)
        digital = self._calculate_dimension("digital_alienation", text)

        # 计算总体异化程度
        dimensions = [product, process, self_alien, species]
        if labor_type == "digital":
            dimensions.append(digital)

        overall = sum(d.get("score", 0) for d in dimensions) / len(dimensions)

        # 分类异化等级
        level = self._classify_alienation_level(overall)

        # 识别主要异化来源
        sources = self._identify_alienation_sources(
            product, process, self_alien, species, digital
        )

        # 生成理论解释
        explanation = self._generate_explanation(level, sources)

        return {
            "data_type": type(data).__name__,
            "labor_type": labor_type,
            "dimensions": {
                "product_alienation": product,
                "process_alienation": process,
                "self_alienation": self_alien,
                "species_alienation": species,
                "digital_alienation": digital,
            },
            "overall_alienation": overall,
            "alienation_level": level,
            "main_sources": sources,
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
        """计算特定异化维度"""
        indicators = ALIENATION_INDICATORS.get(dimension, {})
        keywords = indicators.get("keywords", [])

        count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)
        score = min(1.0, count / 3)

        return {
            "score": score,
            "evidence_count": count,
            "description": indicators.get("description", ""),
        }

    def _classify_alienation_level(self, score: float) -> str:
        """分类异化等级"""
        if score >= 0.8:
            return "极度异化"
        elif score >= 0.6:
            return "高度异化"
        elif score >= 0.4:
            return "中度异化"
        elif score >= 0.2:
            return "轻度异化"
        else:
            return "无明显异化"

    def _identify_alienation_sources(
        self,
        product: Dict,
        process: Dict,
        self_alien: Dict,
        species: Dict,
        digital: Dict,
    ) -> List[Dict]:
        """识别主要异化来源"""
        sources = []

        dimensions = [
            ("产品异化", product),
            ("劳动过程异化", process),
            ("自我异化", self_alien),
            ("类本质异化", species),
            ("数字异化", digital),
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

        sources.sort(key=lambda x: x["contribution"], reverse=True)
        return sources[:3]

    def _generate_explanation(self, level: str, sources: List[Dict]) -> str:
        """生成理论解释"""
        explanations = {
            "极度异化": "劳动者完全被异化，劳动产品和劳动过程都不属于自己。",
            "高度异化": "劳动者严重被异化，自我实现受阻。",
            "中度异化": "劳动者存在一定程度的异化。",
            "轻度异化": "劳动者感受到轻微的异化。",
            "无明显异化": "劳动未明显异化，劳动者有自主性。",
        }

        base = explanations.get(level, "")

        if sources:
            source_names = [s.get("source") for s in sources[:2]]
            base += f" 主要异化来源: {'、'.join(source_names)}。"

        return base


def calculate_alienation(data: Any, labor_type: str = "general") -> Dict:
    """异化程度计算入口函数"""
    calculator = AlienationCalculator()
    return calculator.calculate_alienation(data, labor_type)


if __name__ == "__main__":
    # 测试
    test_data = """
    该公司的流水线工人每天重复同样的动作十个小时。
    生产的产品不属于自己，而是被公司占有。
    工人只是机器的附属品，无法发挥创造性。
    劳动对他们来说只是谋生手段，没有任何乐趣。
    工作强度大，压力大，没有任何自我实现可言。
    """

    result = calculate_alienation(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
