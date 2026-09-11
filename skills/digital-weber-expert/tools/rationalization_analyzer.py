#!/usr/bin/env python3
"""
digital-weber-expert - 理性化分析工具
分析社会理性化程度，基于韦伯社会行动理论

⚠️ 核心原则：定性分析由LLM驱动，本工具仅返回空结构+方法论备忘录。
不包含任何硬编码关键词判断。
"""

from typing import Dict, List, Any, TypedDict


# 韦伯理性化理论方法论备忘录（供LLM定性判断参考，非硬编码）
RATIONALIZATION_MEMO = [
    {
        "type": "type_guidance",
        "role": "llm_guidance",
        "content": (
            "【韦伯四类社会行动类型】\n"
            "1. 目的理性行动（Zweckrational）：以手段-目标计算为核心的理性行动。"
            "分析要点：行动者是否明确计算成本收益？是否有效率意识？"
            "判断时问：行动者是否在权衡手段与目标？\n"
            "2. 价值理性行动（Wertrational）：以绝对价值信念为依据的行动。"
            "分析要点：行动者是否表达某种信念或义务？是否超越功利计算？"
            "判断时问：行动者是否说"因为这是对的"而非"因为这样划算"？\n"
            "3. 情感行动（Affective）：由情感、激情直接驱动的非理性行动。"
            "分析要点：是否有强烈的情感表达？是否缺乏理性计算？"
            "判断时问：这是情感反应还是理性选择？\n"
            "4. 传统行动（Traditional）：沿袭习惯、风俗的行动，理由是"一直如此"。"
            "分析要点：行动者是否引用惯例？是否缺乏反思？"
            "判断时问：这是深思熟虑还是惯性使然？"
        )
    },
    {
        "type": "iron_cage_guidance",
        "role": "llm_guidance",
        "content": (
            "【理性化铁笼（Iron Cage）分析】\n"
            "目的理性（工具理性）压倒价值理性是现代性的核心矛盾。\n"
            "分析时问：这个案例中，工具理性（效率/计算）是否压倒了价值理性（意义/信念）？"
        )
    },
    {
        "type": "analysis_method",
        "role": "llm_guidance",
        "content": (
            "【分析方法论】\n"
            "• 不能仅凭"效率"等词判定目的理性，要分析行动者的自我诠释\n"
            "• 同一文本可能包含多种理性类型，需区分主次\n"
            "• 关注：谁在说？情境是什么？行动者自己如何解释行动理由？"
        )
    }
]


class RationalizationAnalyzer:
    """理性化分析器 — 仅返回空结构，LLM定性判断填充"""

    def analyze(self, text: str, context: str = "") -> Dict[str, Any]:
        """
        分析文本中的理性化类型

        ⚠️ 所有类型判断由LLM基于理论原则作出，本工具不包含任何关键词匹配。

        返回:
            空结构结果（LLM填充rationalization_types等字段）
        """
        return {
            "status": "success",
            "mode": "llm_driven",
            "message": "⚠️ 理性化类型判断由LLM基于韦伯理论原则完成，本工具仅提供方法论引导。",
            "text": text,
            # 以下字段由LLM填充，Python不判断
            "rationalization_types": {},  # {type_name: {presence, strength, evidence, reasoning}}
            "dominant_type": None,       # LLM判断：最主要类型
            "iron_cage_evidence": [],    # LLM判断：工具理性压倒价值理性的证据
            "methodology_memo": RATIONALIZATION_MEMO,
        }


if __name__ == "__main__":
    analyzer = RationalizationAnalyzer()
    result = analyzer.analyze("测试文本")
    print(result)
