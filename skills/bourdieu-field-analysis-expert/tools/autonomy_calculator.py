#!/usr/bin/env python3
"""
bourdieu-field-analysis-expert - 场域自主性计算器
计算场域的自主性程度（相对于外部场域的独立性）

【方法论说明】
本工具不包含任何硬编码关键词匹配。所有自主性判断由LLM根据理论备忘录完成。
工具仅负责：状态管理、空结构返回、方法论引导。
"""

from typing import Dict, List, Any, Optional
import json


# ---------------------------------------------------------------------------
# 场域自主性理论备忘录（供LLM判断时参考）
# ---------------------------------------------------------------------------
AUTONOMY_THEORY_MEMO = """
=== 布迪厄场域自主性理论备忘录 ===

【核心定义】
场域自主性（autonomy）是指场域相对于外部力量（尤其是经济场域和政治场域）
的独立性程度。高度自主的场域有其内在的运作逻辑，不受外部利益直接支配。

【自主性维度框架】（供LLM判断参考）

1. 内在逻辑（Internal Logic）
   - 场域是否有其特有的评价标准和运作规则？
   - 核心行动者是否按照场域特定逻辑行事？
   - 分析时问：经济利益是否压倒了场域内在标准？外部逻辑是否被内化？

2. 特定资本（Specific Capital）
   - 场域是否以特定类型的资本为主导？
   - 其他类型资本能否轻易兑换进入？
   - 分析时问：经济资本能否直接购买学术地位？关系能否直接转化为知识权威？

3. 准入门槛（Entry Barrier）
   - 进入场域是否有专业性门槛？
   - 门槛是否由场域内部设定而非外部力量？
   - 分析时问：有钱就能进入？还是需要专业知识积累？

4. 评价标准（Evaluation Criteria）
   - 谁有权定义场域的成功标准？
   - 评价标准是内在的还是外在的？
   - 分析时问：评价是由同行决定还是市场/政治决定？

5. 权力自主（Power Autonomy）
   - 场域内部权力关系是否自主？
   - 外部权力是否干预场域内部事务？
   - 分析时问：学术场域的决策由谁作出？政府/市场如何介入？

【分析方法论】
- 五个维度不必全部满足，可有所侧重
- 关注：哪些外部力量试图侵入场域？如何侵入？
- 追问：场域如何维护自主性？有何防御机制？
- 判断结果填入返回结构中的 None 字段
"""


class AutonomyCalculator:
    """场域自主性计算器（无关键词匹配版）

    所有自主性判断由调用方/LLM根据 AUTONOMY_THEORY_MEMO 完成。
    """

    def __init__(self):
        self.autonomy_scores = {}

    def calculate_autonomy(
        self,
        text: str,
        field_name: str = None,
        reference_fields: List[str] = None,
    ) -> Dict:
        """
        计算场域自主性（返回空结构供LLM填充）

        参数:
            text: 分析文本
            field_name: 场域名称（可选）
            reference_fields: 参考场域列表（用于比较）

        返回:
            含空结构的自主性分析结果，需LLM根据 AUTONOMY_THEORY_MEMO 填充
        """
        result: Dict = {
            "field_name": field_name or "未知场域",
            "dimensions": {
                # LLM填充：判断每个维度的自主性得分(0.0-1.0)和证据
                "internal_logic": {
                    "score": None,       # 0.0-1.0
                    "positive_indicators": None,  # 正向指标数（LLM主观判断）
                    "negative_indicators": None,  # 负向指标数（LLM主观判断）
                    "description": "内在逻辑 - 场域是否有特有的运作逻辑",
                    "evidence": [],       # LLM提取的证据文本片段
                    "reasoning": None,    # LLM判断理由
                },
                "specific_capital": {
                    "score": None,
                    "positive_indicators": None,
                    "negative_indicators": None,
                    "description": "特定资本 - 特定类型资本是否主导",
                    "evidence": [],
                    "reasoning": None,
                },
                "entry_barrier": {
                    "score": None,
                    "positive_indicators": None,
                    "negative_indicators": None,
                    "description": "准入门槛 - 是否有专业准入限制",
                    "evidence": [],
                    "reasoning": None,
                },
                "evaluation_criteria": {
                    "score": None,
                    "positive_indicators": None,
                    "negative_indicators": None,
                    "description": "评价标准 - 评价标准是否内在化",
                    "evidence": [],
                    "reasoning": None,
                },
                "power_autonomy": {
                    "score": None,
                    "positive_indicators": None,
                    "negative_indicators": None,
                    "description": "权力自主 - 场域是否有自主决策权",
                    "evidence": [],
                    "reasoning": None,
                },
            },
            "overall_autonomy": None,  # LLM综合评分: 0.0-1.0
            "autonomy_level": None,   # LLM判断: "高度自主"/"中度自主"/"低度自主"/"高度他律"
            "sources": [],            # LLM识别: [{source, strength, evidence}, ...]
            "threats": [],            # LLM识别: [{threat, severity, evidence}, ...]
            "comparison": {},          # LLM填充（如有参考场域）
            "recommendations": [],     # LLM基于分析提出建议
            "theory_memo": AUTONOMY_THEORY_MEMO.strip(),
            "raw_text_for_llm": text[:5000],
        }
        self.autonomy_scores[field_name or "unknown"] = result
        return result

    def generate_autonomy_report(self, analysis_result: Dict) -> str:
        """生成自主性分析报告"""
        lines = []
        lines.append("# 场域自主性分析报告\n")
        lines.append("> 本报告由LLM基于布迪厄场域自主性理论生成，工具仅提供数据结构管理。\n")

        field_name = analysis_result.get("field_name", "未知场域")
        overall = analysis_result.get("overall_autonomy")
        level = analysis_result.get("autonomy_level", "（待LLM判断）")

        lines.append(f"## {field_name}自主性评估\n")
        if overall is not None:
            lines.append(f"- 自主性得分: {overall:.2%}")
        lines.append(f"- 自主性等级: {level}")
        lines.append("")

        lines.append("## 各维度自主性（需LLM根据理论备忘录填充）\n")
        dimensions = analysis_result.get("dimensions", {})
        for dim_name, data in dimensions.items():
            score = data.get("score")
            desc = data.get("description", dim_name)
            lines.append(f"- {desc}: {score if score is not None else '（待判断）'}")
        lines.append("")

        sources = analysis_result.get("sources", [])
        if sources:
            lines.append("## 自主性来源\n")
            for s in sources[:3]:
                lines.append(f"- {s.get('source', '未知')}: {s.get('strength', 'N/A')}")
            lines.append("")

        threats = analysis_result.get("threats", [])
        if threats:
            lines.append("## 自主性威胁\n")
            for t in threats[:3]:
                lines.append(f"- {t.get('threat', '未知')}: {t.get('severity', 'N/A')}")
            lines.append("")

        recommendations = analysis_result.get("recommendations", [])
        if recommendations:
            lines.append("## 提升建议\n")
            for rec in recommendations:
                lines.append(f"- {rec}")

        return "\n".join(lines)


def calculate_autonomy(
    text: str, field_name: str = None, reference_fields: List[str] = None
) -> Dict:
    """场域自主性计算入口函数"""
    calculator = AutonomyCalculator()
    return calculator.calculate_autonomy(text, field_name, reference_fields)


if __name__ == "__main__":
    test_text = """
    学术场域具有较强的自主性。学者们遵循知识逻辑和学术规范，
    通过同行评议来评价学术成果。学术自由是核心价值。
    学者追求真理，不受政治干预。

    但是，学术场域也面临一些威胁。政府资助减少后，
    学者们越来越依赖企业赞助。市场化导向的科研评价
    正在影响学术自由。
    """
    result = calculate_autonomy(test_text, "学术场域")
    print("=== 返回结构（需LLM填充） ===")
    print(f"overall_autonomy: {result['overall_autonomy']}")
    print(f"autonomy_level: {result['autonomy_level']}")
    print(f"\n理论备忘录（前300字）:\n{result['theory_memo'][:300]}")
