#!/usr/bin/env python3
"""
digital-marx-expert - 商品化分析工具
分析商品化过程：一切皆可商品化、数据商品化、时间商品化等
基于马克思《资本论》和消费社会理论
"""

from typing import Dict, List, Any
import re
import json


# 商品化指标
COMMODIFICATION_INDICATORS = {
    # 物质商品化
    "material_commodity": {
        "keywords": [
            "商品",
            "买卖",
            "交易",
            "购买",
            "销售",
            " commodity ",
            " buy ",
            " sell ",
            " purchase ",
        ],
        "description": "物质商品的商品化",
    },
    # 服务商品化
    "service_commodity": {
        "keywords": [
            "服务",
            "付费",
            "订阅",
            "会员",
            " service ",
            " subscription ",
            " membership ",
            " fee ",
        ],
        "description": "服务的商品化",
    },
    # 劳动商品化
    "labor_commodity": {
        "keywords": [
            "雇佣",
            "劳动力",
            "工资",
            "出卖",
            " employment ",
            " labor power ",
            " wage ",
            " sell ",
        ],
        "description": "劳动力的商品化",
    },
    # 数据商品化
    "data_commodity": {
        "keywords": [
            "数据",
            "信息",
            "隐私",
            "追踪",
            "分析",
            " data ",
            " information ",
            " privacy ",
            " tracking ",
        ],
        "description": "数据和信息的商品化",
    },
    # 时间商品化
    "time_commodity": {
        "keywords": [
            "时间",
            "注意力",
            "空闲",
            "即时",
            " time ",
            " attention ",
            " leisure ",
            " instant ",
        ],
        "description": "时间和注意力的商品化",
    },
    # 情感商品化
    "emotion_commodity": {
        "keywords": [
            "情感",
            "关系",
            "社交",
            "点赞",
            "关注",
            " emotion ",
            " relationship ",
            " social ",
            " like ",
        ],
        "description": "情感和关系的商品化",
    },
}


class CommodificationAnalyzer:
    """商品化分析器"""

    def __init__(self):
        self.analysis_results = []

    def analyze_commodification(self, data: Any, society_type: str = None) -> Dict:
        """
        分析商品化程度

        参数:
            data: 分析数据
            society_type: 社会类型

        返回:
            商品化分析结果
        """
        # 转换为文本
        text = self._convert_to_text(data)

        # 分析各维度
        material = self._analyze_dimension("material_commodity", text)
        service = self._analyze_dimension("service_commodity", text)
        labor = self._analyze_dimension("labor_commodity", text)
        data_comm = self._analyze_dimension("data_commodity", text)
        time = self._analyze_dimension("time_commodity", text)
        emotion = self._analyze_dimension("emotion_commodity", text)

        # 计算总体商品化程度
        overall = self._calculate_overall_commodification(
            material, service, labor, data_comm, time, emotion
        )

        # 分类商品化等级
        level = self._classify_commodification_level(overall)

        # 识别主要商品化领域
        domains = self._identify_commodification_domains(
            material, service, labor, data_comm, time, emotion
        )

        # 生成理论解释
        explanation = self._generate_explanation(level, domains)

        return {
            "data_type": type(data).__name__,
            "society_type": society_type,
            "dimensions": {
                "material_commodity": material,
                "service_commodity": service,
                "labor_commodity": labor,
                "data_commodity": data_comm,
                "time_commodity": time,
                "emotion_commodity": emotion,
            },
            "overall_commodification": overall,
            "commodification_level": level,
            "main_domains": domains,
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

    def _analyze_dimension(self, dimension: str, text: str) -> Dict:
        """分析特定商品化维度"""
        indicators = COMMODIFICATION_INDICATORS.get(dimension, {})
        keywords = indicators.get("keywords", [])

        count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)
        score = min(1.0, count / 3)

        return {
            "score": score,
            "evidence_count": count,
            "description": indicators.get("description", ""),
        }

    def _calculate_overall_commodification(
        self,
        material: Dict,
        service: Dict,
        labor: Dict,
        data_comm: Dict,
        time: Dict,
        emotion: Dict,
    ) -> float:
        """计算总体商品化程度"""
        scores = [
            material.get("score", 0),
            service.get("score", 0),
            labor.get("score", 0),
            data_comm.get("score", 0),
            time.get("score", 0),
            emotion.get("score", 0),
        ]
        return sum(scores) / len(scores)

    def _classify_commodification_level(self, score: float) -> str:
        """分类商品化等级"""
        if score >= 0.8:
            return "全面商品化"
        elif score >= 0.6:
            return "高度商品化"
        elif score >= 0.4:
            return "中度商品化"
        elif score >= 0.2:
            return "轻度商品化"
        else:
            return "低度商品化"

    def _identify_commodification_domains(
        self,
        material: Dict,
        service: Dict,
        labor: Dict,
        data_comm: Dict,
        time: Dict,
        emotion: Dict,
    ) -> List[Dict]:
        """识别主要商品化领域"""
        domains = []

        dimensions = [
            ("物质商品", material),
            ("服务商品", service),
            ("劳动力商品", labor),
            ("数据商品", data_comm),
            ("时间商品", time),
            ("情感商品", emotion),
        ]

        for name, data in dimensions:
            score = data.get("score", 0)
            if score >= 0.2:
                domains.append(
                    {
                        "domain": name,
                        "contribution": score,
                        "description": data.get("description", ""),
                    }
                )

        domains.sort(key=lambda x: x["contribution"], reverse=True)
        return domains[:3]

    def _generate_explanation(self, level: str, domains: List[Dict]) -> str:
        """生成理论解释"""
        explanations = {
            "全面商品化": "社会生活各个方面都被商品化，包括物质、服务、劳动、数据、情感等。",
            "高度商品化": "商品化程度很高，大部分社会关系都通过市场交易实现。",
            "中度商品化": "商品化程度中等，部分领域仍保留非商品化关系。",
            "轻度商品化": "商品化程度较低，存在较多非商品化的社会关系。",
            "低度商品化": "商品化程度很低，社会关系主要以非市场形式存在。",
        }

        base = explanations.get(level, "")

        if domains:
            domain_names = [d.get("domain") for d in domains]
            base += f" 主要商品化领域: {'、'.join(domain_names)}。"

        return base


def analyze_commodification(data: Any, society_type: str = None) -> Dict:
    """商品化分析入口函数"""
    analyzer = CommodificationAnalyzer()
    return analyzer.analyze_commodification(data, society_type)


if __name__ == "__main__":
    # 测试
    test_data = """
    在这个消费社会，一切都变成了商品。
    不仅物质产品是商品，服务也被商品化了。
    人们的劳动成为雇佣劳动，出卖劳动力获取工资。
    更重要的是，数据成为新的商品。
    平台公司追踪用户的各种行为数据，进行分析并出售。
    人们的注意力成为商品，被广告商购买。
    情感和关系也被商品化，社交媒体上的点赞和关注都可以买卖。
    """

    result = analyze_commodification(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
