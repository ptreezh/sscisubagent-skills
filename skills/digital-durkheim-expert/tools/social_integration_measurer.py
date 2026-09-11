#!/usr/bin/env python3
"""
digital-durkheim-expert - 社会整合度测量工具
测量社会整合（social integration）程度
基于涂尔干《自杀论》

【方法论说明】
本工具不包含任何硬编码关键词匹配。所有社会整合判断由LLM根据理论备忘录完成。
工具仅负责：状态管理、空结构返回、方法论引导。
"""

from typing import Dict, List, Any
import json


# ---------------------------------------------------------------------------
# 涂尔干社会整合理论备忘录（供LLM判断时参考）
# ---------------------------------------------------------------------------
INTEGRATION_THEORY_MEMO = """
=== 涂尔干社会整合（Social Integration）理论备忘录 ===

【核心概念】（来自《自杀论》, 1897）
社会整合是指个体嵌入社会网络、被社会关系所联结的程度。
涂尔干通过社会整合来解释不同类型自杀：
- 利己型自杀（egoistic）：社会整合程度过低
- 利他型自杀（altruistic）：社会整合程度过高
- 失范型自杀（anomic）：社会规范失效导致的整合崩溃
- 宿命型自杀（fatalistic）：社会整合过强，个体被过度压抑

【社会整合维度框架】（供LLM分析参考）

1. 社会联结（Social Bonds）
   - 个体与其他社会成员的联系强度和频率如何？
   - 联结是强关系（家庭、密友）还是弱关系（熟人、同事）？
   - 关键问题：个体在社会中是否"被看见"和"被需要"？

2. 归属感（Sense of Belonging）
   - 个体是否认同自己属于某个社会群体？
   - 归属感是基于血缘、地缘、趣缘还是职业？
   - 关键问题：个体离开群体会有什么情感代价？

3. 社会参与（Social Participation）
   - 个体参与社会活动的频率和深度如何？
   - 参与是主动还是被动的？
   - 关键问题：个体是否有机会表达意见和产生影响？

4. 社会支持（Social Support）
   - 个体在困难时能否获得社会帮助？
   - 支持网络包括哪些人？资源可及性如何？
   - 关键问题：谁提供支持？支持的性质是什么（物质/情感/信息）？

5. 宗教整合（Religious Integration）
   - 宗教群体提供何种社会整合？
   - 涂尔干研究：天主教比新教整合程度更高→自杀率更低
   - 关键问题：宗教提供的是真实整合还是表面整合？

6. 家庭整合（Family Integration）
   - 家庭关系的紧密度如何？
   - 涂尔干发现：鳏寡者的自杀率高于已婚者
   - 关键问题：家庭是否提供情感支持和日常联结？

【分析方法论】
- 测量应综合多个维度，不依赖单一指标
- 关注：整合是实质性的还是表面化的？
- 追问：哪些群体整合程度最低？最高？
- 判断结果填入返回结构中的 None 字段
"""


class SocialIntegrationMeasurer:
    """社会整合度测量器（无关键词匹配版）

    所有社会整合判断由调用方/LLM根据 INTEGRATION_THEORY_MEMO 完成。
    """

    def __init__(self):
        self.measurement_results = []

    def measure_integration(self, data: Any, measure_type: str = "general") -> Dict:
        """
        测量社会整合度（返回空结构供LLM填充）

        参数:
            data: 分析数据
            measure_type: 测量类型（general/religious/family）

        返回:
            含空结构的社会整合度测量结果，需LLM根据 INTEGRATION_THEORY_MEMO 填充
        """
        raw_text = self._convert_to_text(data)

        result: Dict = {
            "data_type": type(data).__name__,
            "measure_type": measure_type,
            "dimensions": {
                # LLM填充：判断每个维度的得分(0.0-1.0)和证据
                "social_bonds": {
                    "score": None,       # 0.0-1.0
                    "strong_indicators": None,   # 强联结指标（LLM主观）
                    "weak_indicators": None,     # 弱联结指标（LLM主观）
                    "description": "社会联结 - 个体与他人的联系强度",
                    "evidence": [],              # LLM提取的证据片段
                    "reasoning": None,           # LLM判断理由
                },
                "belonging": {
                    "score": None,
                    "evidence_count": None,
                    "description": "归属感 - 个体对群体的认同程度",
                    "evidence": [],
                    "reasoning": None,
                },
                "participation": {
                    "score": None,
                    "evidence_count": None,
                    "description": "社会参与 - 参与社会活动的程度",
                    "evidence": [],
                    "reasoning": None,
                },
                "support": {
                    "score": None,
                    "evidence_count": None,
                    "description": "社会支持 - 社会支持网络的可用性",
                    "evidence": [],
                    "reasoning": None,
                },
                "religious_integration": {
                    "score": None,
                    "evidence_count": None,
                    "description": "宗教整合 - 宗教群体的社会整合功能",
                    "evidence": [],
                    "reasoning": None,
                },
                "family_integration": {
                    "score": None,
                    "evidence_count": None,
                    "description": "家庭整合 - 家庭关系提供的社会整合",
                    "evidence": [],
                    "reasoning": None,
                },
            },
            "overall_integration": None,    # LLM综合评分: 0.0-1.0
            "integration_level": None,      # LLM判断: "高度整合"/"中度整合"/"低度整合"/"边缘整合"/"原子化"
            "integration_sources": [],       # LLM识别: [{source, contribution, description}, ...]
            "explanation": None,            # LLM基于涂尔干理论的解释
            "theory_memo": INTEGRATION_THEORY_MEMO.strip(),
            "raw_text_for_llm": raw_text[:5000],
        }
        self.measurement_results.append(result)
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

    def generate_report(self, result: Dict) -> str:
        """生成测量报告"""
        lines = []
        lines.append("# 社会整合度测量报告\n")
        lines.append("> 本报告由LLM基于涂尔干社会整合理论生成，工具仅提供数据结构管理。\n")

        level = result.get("integration_level", "（待LLM判断）")
        overall = result.get("overall_integration")
        measure_type = result.get("measure_type", "general")

        lines.append(f"## {measure_type}社会整合评估\n")
        if overall is not None:
            lines.append(f"- 整合度得分: {overall:.2%}")
        lines.append(f"- 整合等级: {level}")
        lines.append("")

        lines.append("## 各维度整合度（需LLM根据理论备忘录填充）\n")
        dimensions = result.get("dimensions", {})
        for dim_name, data in dimensions.items():
            score = data.get("score")
            desc = data.get("description", dim_name)
            lines.append(f"- {desc}: {score if score is not None else '（待判断）'}")
        lines.append("")

        sources = result.get("integration_sources", [])
        if sources:
            lines.append("## 整合主要来源\n")
            for s in sources[:3]:
                lines.append(f"- {s.get('source')}: {s.get('contribution', 'N/A')}")

        return "\n".join(lines)


def measure_integration(data: Any, measure_type: str = "general") -> Dict:
    """社会整合度测量入口函数"""
    measurer = SocialIntegrationMeasurer()
    return measurer.measure_integration(data, measure_type)


if __name__ == "__main__":
    test_data = """
    该群体成员之间联系紧密，经常参加集体活动。
    成员有强烈的归属感和认同感，互相帮助支持。
    形成了稳定的社会支持网络，社会凝聚力强。
    """
    result = measure_integration(test_data)
    print("=== 返回结构（需LLM填充） ===")
    print(f"overall_integration: {result['overall_integration']}")
    print(f"integration_level: {result['integration_level']}")
    print(f"\n理论备忘录（前300字）:\n{result['theory_memo'][:300]}")
