#!/usr/bin/env python3
"""
digital-durkheim-expert - 自杀类型分析工具
分析自杀类型：利己型、利他型、失范型、宿命型
基于涂尔干《自杀论》
"""

from typing import Dict, List, Any
import json


# 自杀类型分析methodology memo
# 关键词匹配已禁用，自杀类型判断由LLM基于涂尔干理论完成
SUICIDE_TYPE_METHODOLOGY_MEMO = """【涂尔干自杀论 - LLM专属判断】
自杀类型判断基于涂尔干《自杀论》的理论框架。
- 禁止：用关键词匹配("低整合"/"集体"/"失范")判断自杀类型
- 正确做法：
  * 利己型：分析社会整合度是否过低，个体是否过度原子化
  * 利他型：分析社会整合度是否过高，个体是否为集体利益牺牲
  * 失范型：分析社会规范是否混乱或崩溃
  * 宿命型：分析社会规范是否过度压制
- 自杀类型判断由LLM综合分析，不可用关键词计数自动确定
"""


class SuicideTypeAnalyzer:
    """自杀类型分析器"""

    def __init__(self):
        self.analysis_results = []

    def analyze_suicide_types(self, data: Any, group_variable: str = None) -> Dict:
        """
        分析自杀类型（返回空结构供LLM填充）

        参数:
            data: 分析数据
            group_variable: 分组变量（如宗教、国家等）

        返回:
            含空结构的自杀类型分析结果，需LLM根据 theory_memo 填充
        """
        raw_text = self._convert_to_text(data)

        return {
            "data_type": type(data).__name__,
            "group_variable": group_variable,
            "types": {
                "egoistic": {
                    "score": None,      # LLM填充
                    "evidence": [],      # LLM填充
                    "description": "利己型自杀 - 社会整合度过低导致个体原子化",
                },
                "altruistic": {
                    "score": None,      # LLM填充
                    "evidence": [],      # LLM填充
                    "description": "利他型自杀 - 社会整合度过高导致为集体牺牲",
                },
                "anomic": {
                    "score": None,       # LLM填充
                    "evidence": [],       # LLM填充
                    "description": "失范型自杀 - 社会规范混乱导致无所适从",
                },
                "fatalistic": {
                    "score": None,       # LLM填充
                    "evidence": [],       # LLM填充
                    "description": "宿命型自杀 - 社会规范过度压制导致绝望",
                },
            },
            "dominant_type": None,   # LLM填充
            "indices": {
                "integration_index": None,  # LLM填充
                "anomie_index": None,       # LLM填充
            },
            "theoretical_explanation": "",   # LLM填充
            "theory_memo": SUICIDE_TYPE_METHODOLOGY_MEMO.strip(),
            "raw_data_for_llm": raw_text[:5000],
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


def analyze_suicide_types(data: Any, group_variable: str = None) -> Dict:
    """自杀类型分析入口函数"""
    analyzer = SuicideTypeAnalyzer()
    return analyzer.analyze_suicide_types(data, group_variable)


if __name__ == "__main__":
    test_data = """
    该群体的社会整合度较低，个体主义倾向明显，
    社会联结薄弱，孤独感较强。缺乏集体支持和归属感。
    同时，社会规范处于混乱状态，价值观念多元，
    传统规范失去约束力。
    """
    result = analyze_suicide_types(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
