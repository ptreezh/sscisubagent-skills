#!/usr/bin/env python3
"""
digital-marx-expert - 商品化分析工具
分析商品化过程：物质商品化、服务商品化、数据商品化、时间商品化、情感商品化等
基于马克思《资本论》和消费社会理论

【方法论说明】
本工具不包含任何硬编码关键词匹配。所有商品化分析由LLM根据理论备忘录完成。
工具仅负责：状态管理、空结构返回、方法论引导。
"""

from typing import Dict, List, Any
import json


# ---------------------------------------------------------------------------
# 商品化理论备忘录（供LLM判断时参考）
# ---------------------------------------------------------------------------
COMMODIFICATION_THEORY_MEMO = """
=== 商品化（Commodification）理论备忘录 ===

【核心概念】
商品化是将原本非商品性质的事物转化为可买卖、可交换的商品的过程。
马克思在《资本论》中指出，资本主义的核心逻辑是不断将一切纳入商品交换体系。

【商品化类型框架】（供LLM判断参考）

1. 物质商品化（Material Commodification）
   - 物质产品（食品、衣物、住房）被生产为用于交换的商品
   - 分析要点：是否以交换为目的生产？是否遵循价值规律？

2. 服务商品化（Service Commodification）
   - 服务（教育、医疗、金融）被转化为商品
   - 关键问题：服务是否变成"付费才能获得"？谁有能力支付？
   - 订阅制、会员制是服务商品化的典型形式

3. 劳动商品化（Labor Commodification）
   - 劳动力成为可买卖的商品（雇佣劳动）
   - 马克思的核心：劳动力是唯一在使用中能产生大于自身价值的价值
   - 关键问题：劳动者是否自由得不占有生产资料，只能出卖劳动力？

4. 数据商品化（Data Commodification）
   - 用户数据和行为数据成为可交易商品
   - 平台资本主义的特征：用户"免费"使用平台，平台出售用户数据/注意力
   - 关键问题：谁拥有数据？用户是否知情并同意？数据收益如何分配？

5. 时间商品化（Time Commodification）
   - 时间被商品化：注意力经济、时间银行、速递服务
   - 关键问题：人们是否在"购买时间"？谁有更多时间被商品化的选择权？

6. 情感商品化（Emotional Commodification）
   - 情感、关系、认同成为商品
   - 典型：社交媒体点赞、粉丝文化、网红经济
   - 关键问题：真实情感还是表演性情感？"关系"是可以量化的吗？

【商品化程度评估】（供LLM综合判断）
- 全面商品化：社会生活各方面都被纳入市场交换
- 有限商品化：某些领域仍保留非商品化关系（家庭、友谊、公共服务）
- 分析时问：哪些领域的商品化是可逆的？哪些是不可逆的？
- 追问：谁从商品化中获益？谁承担商品化的代价？

【分析方法论】
- 六个维度不必全部满足，可有所侧重
- 关注商品化如何改变人与物的关系
- 判断结果填入返回结构中的 None 字段
"""


class CommodificationAnalyzer:
    """商品化分析器（无关键词匹配版）

    所有商品化分析由调用方/LLM根据 COMMODIFICATION_THEORY_MEMO 完成。
    """

    def __init__(self):
        self.analysis_results = []

    def analyze_commodification(self, data: Any, society_type: str = None) -> Dict:
        """
        分析商品化程度（返回空结构供LLM填充）

        参数:
            data: 分析数据
            society_type: 社会类型

        返回:
            含空结构的商品化分析结果，需LLM根据 COMMODIFICATION_THEORY_MEMO 填充
        """
        raw_text = self._convert_to_text(data)

        result: Dict = {
            "data_type": type(data).__name__,
            "society_type": society_type,
            "dimensions": {
                # LLM填充：判断每个维度的得分(0.0-1.0)和证据
                "material_commodification": {
                    "score": None,        # 0.0-1.0
                    "evidence_count": None,    # LLM主观证据计数
                    "description": "物质商品化 - 物质产品被纳入商品交换",
                    "evidence": [],            # LLM提取的证据片段
                    "reasoning": None,         # LLM判断理由
                },
                "service_commodification": {
                    "score": None,
                    "evidence_count": None,
                    "description": "服务商品化 - 服务成为付费商品",
                    "evidence": [],
                    "reasoning": None,
                },
                "labor_commodification": {
                    "score": None,
                    "evidence_count": None,
                    "description": "劳动商品化 - 劳动力成为可买卖的商品",
                    "evidence": [],
                    "reasoning": None,
                },
                "data_commodification": {
                    "score": None,
                    "evidence_count": None,
                    "description": "数据商品化 - 数据和注意力成为商品",
                    "evidence": [],
                    "reasoning": None,
                },
                "time_commodification": {
                    "score": None,
                    "evidence_count": None,
                    "description": "时间商品化 - 时间和注意力被商品化",
                    "evidence": [],
                    "reasoning": None,
                },
                "emotion_commodification": {
                    "score": None,
                    "evidence_count": None,
                    "description": "情感商品化 - 情感和关系被商品化",
                    "evidence": [],
                    "reasoning": None,
                },
            },
            "overall_commodification": None,   # LLM综合评分: 0.0-1.0
            "commodification_level": None,     # LLM判断: "全面商品化"/"高度商品化"/"中度商品化"/"轻度商品化"/"低度商品化"
            "main_domains": [],                # LLM识别: [{domain, contribution, description}, ...]
            "explanation": None,               # LLM基于马克思商品化理论的解释
            "theory_memo": COMMODIFICATION_THEORY_MEMO.strip(),
            "raw_text_for_llm": raw_text[:5000],
        }
        self.analysis_results.append(result)
        return result

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


def analyze_commodification(data: Any, society_type: str = None) -> Dict:
    """商品化分析入口函数"""
    analyzer = CommodificationAnalyzer()
    return analyzer.analyze_commodification(data, society_type)


if __name__ == "__main__":
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
    print("=== 返回结构（需LLM填充） ===")
    print(f"overall_commodification: {result['overall_commodification']}")
    print(f"commodification_level: {result['commodification_level']}")
    print(f"\n理论备忘录（前300字）:\n{result['theory_memo'][:300]}")
