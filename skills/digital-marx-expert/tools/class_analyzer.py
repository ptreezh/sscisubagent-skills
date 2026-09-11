#!/usr/bin/env python3
"""
digital-marx-expert - 阶级分析工具
分析社会阶级结构：资产阶级、无产阶级、中产阶级等
基于马克思阶级理论

【方法论说明】
本工具不包含任何硬编码关键词匹配。所有阶级分析由LLM根据理论备忘录完成。
工具仅负责：状态管理、空结构返回、方法论引导。
"""

from typing import Dict, List, Any
import json


# ---------------------------------------------------------------------------
# 马克思阶级理论备忘录（供LLM判断时参考）
# ---------------------------------------------------------------------------
CLASS_THEORY_MEMO = """
=== 马克思阶级（Class）理论备忘录 ===

【阶级理论核心】
马克思认为，阶级是由人们在生产体系中的客观位置决定的。
最根本的区分标准是：是否占有生产资料。

【经典阶级框架】（供LLM判断参考）

1. 资产阶级（Bourgeoisie）
   - 生产资料的占有者
   - 凭借所有权获取剩余价值（剥削劳动）
   - 特征：占有生产工具、雇佣劳动、获取利润/利息/地租
   - 行动逻辑：扩大资本积累、维持有利于私有产权的制度
   - 判断标准：是否占有生产资料并从中获取非劳动收入？

2. 无产阶级（Proletariat）
   - 不占有生产资料，只能出卖劳动力为生
   - 其劳动成果被资本家占有（被剥削）
   - 特征：领取工资、受雇于他人、缺乏生产资料所有权
   - 行动逻辑：争取提高工资、改善劳动条件、最终消灭雇佣劳动制度
   - 判断标准：是否不占有生产资料，只能靠出卖劳动力生活？

3. 中间阶级/小资产阶级（Petty Bourgeoisie）
   - 介于资产阶级和无产阶级之间
   - 可能占有少量生产资料（小店主、小农）
   - 可能拥有专业技能（医生、律师）
   - 特征：既有剥削倾向，又有被剥削处境
   - 在资本主义发展中的双重命运：一方面上升为资产阶级，另一方面沦为无产阶级

4. 农民阶级（Peasantry）
   - 在封建主义向资本主义过渡中有特殊地位
   - 可能占有小块土地（自耕农）
   - 或依附于地主（佃农）
   - 马克思对农民阶级的复杂态度：既是生产者，又可能分化

5. 地主阶级（Landlord Class）
   - 主要占有土地
   - 收取地租
   - 在不同生产方式中有不同形态：封建地主、资本主义农场主

【阶级关系分析】
- 剥削关系：资产阶级通过占有剩余价值剥削无产阶级
- 对抗性矛盾：阶级利益根本对立
- 虚假意识 vs. 阶级意识：无产阶级是否认识到自己的被剥削地位？

【数字时代的阶级变化】
- 平台工人：是独立劳动者还是新的无产者？
- 知识工作者：白领是否是"新中产阶级"？
- 用户/产消者：使用"免费"平台的用户的阶级位置是什么？

【分析方法论】
- 不应仅凭职业名称判断阶级，要分析其实际的生产关系位置
- 关注：谁占有劳动产品？谁决定生产活动？谁承担风险？
- 追问：是否存在阶级流动？什么因素决定阶级位置？
- 判断结果填入返回结构中的 None 字段
"""


class ClassAnalyzer:
    """阶级分析器（无关键词匹配版）

    所有阶级分析由调用方/LLM根据 CLASS_THEORY_MEMO 完成。
    """

    def __init__(self):
        self.analysis_results = []

    def analyze_class(self, data: Any, focus_class: str = None) -> Dict:
        """
        分析阶级结构（返回空结构供LLM填充）

        参数:
            data: 分析数据
            focus_class: 关注的主要阶级

        返回:
            含空结构的阶级分析结果，需LLM根据 CLASS_THEORY_MEMO 填充
        """
        raw_text = self._convert_to_text(data)

        result: Dict = {
            "data_type": type(data).__name__,
            "focus_class": focus_class,
            "classes": {
                # LLM填充：判断每个阶级的存在程度(0.0-1.0)和证据
                "bourgeoisie": {
                    "score": None,           # 0.0-1.0
                    "evidence_count": None,       # LLM主观证据计数
                    "description": "资产阶级 - 占有生产资料并剥削劳动的阶级",
                    "evidence": [],               # LLM提取的证据片段
                    "reasoning": None,            # LLM判断理由
                },
                "proletariat": {
                    "score": None,
                    "evidence_count": None,
                    "description": "无产阶级 - 不占有生产资料、靠出卖劳动为生的阶级",
                    "evidence": [],
                    "reasoning": None,
                },
                "middle_class": {
                    "score": None,
                    "evidence_count": None,
                    "description": "中产阶级 - 介于资产阶级和无产阶级之间",
                    "evidence": [],
                    "reasoning": None,
                },
                "peasantry": {
                    "score": None,
                    "evidence_count": None,
                    "description": "农民阶级 - 从事农业生产的阶级",
                    "evidence": [],
                    "reasoning": None,
                },
                "landlord": {
                    "score": None,
                    "evidence_count": None,
                    "description": "地主阶级 - 占有土地的阶级",
                    "evidence": [],
                    "reasoning": None,
                },
            },
            "dominant_class": None,         # LLM判断: "资产阶级"/"无产阶级"/"中产阶级"/"农民阶级"/"地主阶级"/"未确定"
            "class_relations": [],          # LLM识别: [{relation, classes, description}, ...]
            "class_tension": None,          # LLM评分: 0.0-1.0（阶级对立的紧张程度）
            "explanation": None,            # LLM基于马克思阶级理论的解释
            "theory_memo": CLASS_THEORY_MEMO.strip(),
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


def analyze_class(data: Any, focus_class: str = None) -> Dict:
    """阶级分析入口函数"""
    analyzer = ClassAnalyzer()
    return analyzer.analyze_class(data, focus_class)


if __name__ == "__main__":
    test_data = """
    该社会存在明显的阶级分化。资产阶级占有生产资料，
    雇佣大量工人进行生产，获取利润。工人阶级出卖劳动力，
    获取工资收入，处于被剥削地位。中产阶级拥有专业技能，
    生活水平相对稳定。
    """
    result = analyze_class(test_data)
    print("=== 返回结构（需LLM填充） ===")
    print(f"dominant_class: {result['dominant_class']}")
    print(f"class_tension: {result['class_tension']}")
    print(f"\n理论备忘录（前300字）:\n{result['theory_memo'][:300]}")
