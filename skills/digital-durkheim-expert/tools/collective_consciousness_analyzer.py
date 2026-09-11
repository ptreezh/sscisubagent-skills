#!/usr/bin/env python3
"""
digital-durkheim-expert - 集体意识分析工具
分析集体意识（collective consciousness）的强度和内容
基于涂尔干《宗教生活的基本形式》

【方法论说明】
本工具不包含任何硬编码关键词匹配。所有集体意识判断由LLM根据理论备忘录完成。
工具仅负责：状态管理、空结构返回、方法论引导。
"""

from typing import Dict, List, Any
import json


# ---------------------------------------------------------------------------
# 涂尔干集体意识理论备忘录（供LLM判断时参考）
# ---------------------------------------------------------------------------
COLLECTIVE_CONSCIOUSNESS_THEORY_MEMO = """
=== 涂尔干集体意识（Collective Consciousness）理论备忘录 ===

【核心定义】（来自《宗教生活的基本形式》, 1912）
集体意识是指社会成员平均共有的信仰和情感的总和，它构成了他们明确的社会生活。
它外在于个体意识，对个体具有强制性力量。

【集体意识的两分法】

物质性集体意识指标：
- 制度化形式：法律、组织、仪式程序
- 可观察的集体行为：集体活动、节日庆典、仪式
- 物理表征：旗帜、纪念碑、制服、徽章

精神性集体意识指标：
- 共享的道德规范和价值观
- 集体情感（shared emotions）：社会热潮、社会愤慨
- 共同信念和意识形态
- "我们"vs"他们"的心理边界

【集体意识强度判断框架】（供LLM分析参考）

1. 强度（Intensity）
   - 集体意识在多大程度上渗透到个体意识中？
   - 强：集体规范成为个体的第二天性，几乎不需思考
   - 弱：集体规范只存在于形式，个体内心不认同

2. 共同信念（Shared Beliefs）
   - 社会成员在多大程度上共享相同的信念？
   - 关键问题：是否存在根本性的价值共识？分歧多大？

3. 集体表征（Collective Representations）
   - 集体意识通过什么象征和符号表达？
   - 符号是否被广泛认可和尊重？
   - 关键问题：谁有权创造和解释集体符号？

4. 集体情感（Collective Sentiments）
   - 社会成员在多大程度上共享情感体验？
   - 集体情感如何产生和传播？
   - 关键问题：什么事件激发集体情感？强度如何？

5. 社会联结（Social Bond）
   - 集体意识如何维系社会团结？
   - 涂尔干：集体意识越强，社会越有机械团结（相似性联结）
   - 关键问题：个体差异被鼓励还是被压制？

【集体意识与社会团结的关系】
- 机械团结（Mechanical Solidarity）：集体意识强，个体相似，联结基于相似性
- 有机团结（Organic Solidarity）：劳动分工发达，联结基于相互依赖
- 集体意识弱化：失范（anomie）状态，社会联结瓦解

【分析方法论】
- 五个维度不必全部满足，可有所侧重
- 关注集体意识的强制性：违背集体意识会有什么后果？
- 追问：集体意识是由谁生产和维护的？
- 判断结果填入返回结构中的 None 字段
"""


class CollectiveConsciousnessAnalyzer:
    """集体意识分析器（无关键词匹配版）

    所有集体意识判断由调用方/LLM根据 COLLECTIVE_CONSCIOUSNESS_THEORY_MEMO 完成。
    """

    def __init__(self):
        self.analysis_results = []

    def analyze_collective_consciousness(self, data: Any, group: str = None) -> Dict:
        """
        分析集体意识（返回空结构供LLM填充）

        参数:
            data: 分析数据
            group: 分析群体

        返回:
            含空结构的集体意识分析结果，需LLM根据 COLLECTIVE_CONSCIOUSNESS_THEORY_MEMO 填充
        """
        raw_text = self._convert_to_text(data)

        result: Dict = {
            "data_type": type(data).__name__,
            "group": group,
            "dimensions": {
                # LLM填充：判断每个维度的得分(0.0-1.0)和证据
                "intensity": {
                    "score": None,       # 0.0-1.0
                    "strong_count": None,    # 强指标数（LLM主观）
                    "weak_count": None,      # 弱指标数（LLM主观）
                    "description": "集体意识强度 - 集体意识渗透个体意识的程度",
                    "evidence": [],          # LLM提取的证据片段
                    "reasoning": None,       # LLM判断理由
                },
                "shared_beliefs": {
                    "score": None,
                    "evidence_count": None,
                    "description": "共同信念 - 成员共享的信仰和价值观",
                    "evidence": [],
                    "reasoning": None,
                },
                "representations": {
                    "score": None,
                    "evidence_count": None,
                    "description": "集体表征 - 集体意识的符号和象征表达",
                    "evidence": [],
                    "reasoning": None,
                },
                "sentiments": {
                    "score": None,
                    "evidence_count": None,
                    "description": "集体情感 - 共享的情感体验和情绪",
                    "evidence": [],
                    "reasoning": None,
                },
                "social_bond": {
                    "score": None,
                    "evidence_count": None,
                    "description": "社会联结 - 集体意识维系社会团结的机制",
                    "evidence": [],
                    "reasoning": None,
                },
            },
            "overall_strength": None,   # LLM综合评分: 0.0-1.0
            "consciousness_level": None,  # LLM判断: "极强"/"强"/"中等"/"弱"/"极弱"
            "main_features": [],         # LLM识别: [{feature, strength, description}, ...]
            "explanation": None,        # LLM基于涂尔干理论的解释
            "theory_memo": COLLECTIVE_CONSCIOUSNESS_THEORY_MEMO.strip(),
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

    def generate_report(self, result: Dict) -> str:
        """生成分析报告框架（供LLM填充内容）"""
        lines = []
        lines.append("# 集体意识分析报告\n")
        lines.append("> 本报告由LLM基于涂尔干集体意识理论生成，工具仅提供数据结构管理。\n")

        lines.append(f"## 总体判断: {result.get('consciousness_level', '（待LLM判断）')}\n")
        lines.append("## 维度分析（需LLM根据理论备忘录填充）\n")
        for dim_name, data in result.get("dimensions", {}).items():
            score = data.get("score")
            lines.append(f"- {dim_name}: score={score if score is not None else '（待判断）'}")

        overall = result.get("overall_strength")
        if overall is not None:
            lines.append(f"\n综合强度: {overall:.2%}")

        features = result.get("main_features", [])
        if features:
            lines.append("\n## 主要特征\n")
            for f in features:
                lines.append(f"- {f.get('feature')}: {f.get('strength', 'N/A')}")

        return "\n".join(lines)


def analyze_collective_consciousness(data: Any, group: str = None) -> Dict:
    """集体意识分析入口函数"""
    analyzer = CollectiveConsciousnessAnalyzer()
    return analyzer.analyze_collective_consciousness(data, group)


if __name__ == "__main__":
    test_data = """
    该宗教群体拥有强烈的集体意识。成员共享相同的信念和价值观，
    定期参加集体仪式，使用共同的宗教符号。集体情感深厚，
    成员之间团结互助，社会凝聚力强。
    """
    result = analyze_collective_consciousness(test_data)
    print("=== 返回结构（需LLM填充） ===")
    print(f"overall_strength: {result['overall_strength']}")
    print(f"consciousness_level: {result['consciousness_level']}")
    print(f"\n理论备忘录（前300字）:\n{result['theory_memo'][:300]}")
