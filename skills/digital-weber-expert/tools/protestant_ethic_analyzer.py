#!/usr/bin/env python3
"""
digital-weber-expert - 新教伦理分析工具
分析新教伦理与资本主义精神的关系
基于韦伯《新教伦理与资本主义精神》
"""

from typing import Dict, List, Any
import json


# Weber新教伦理分析methodology memo
PROTESTANT_ETHIC_METHODOLOGY_MEMO = """【Weber新教伦理分析 - LLM专属判断】
Weber(1905)分析新教伦理与资本主义精神的关系。
- 禁止：用关键词匹配("天职"/"禁欲"/"预定")判断新教伦理维度
- 正确做法：分析行动者行为动机背后的宗教-伦理基础
  * 天职观: 劳动作为对上帝的义务
  * 禁欲主义: 节俭、克制物质享受
  * 预定论: 通过现世成功证明被拣选
  * 世俗禁欲: 在世俗生活中实践宗教伦理
- 新教伦理是"理想类型"，实际案例多为混合形态
- 判断是否具有"资本主义精神"需综合分析
"""


class ProtestantEthicAnalyzer:
    def __init__(self):
        pass

    def analyze_protestant_ethic(self, data: Any) -> Dict:
        # 关键词匹配已禁用
        # 新教伦理分析由LLM基于Weber理论做诠释判断
        return {
            "dimensions": {
                "天职观": {"score": None, "evidence_count": None},
                "禁欲主义": {"score": None, "evidence_count": None},
                "预定论": {"score": None, "evidence_count": None},
                "世俗禁欲": {"score": None, "evidence_count": None},
            },
            "overall": None,   # LLM填充
            "explanation": None,   # LLM填充
            "methodology_memo": PROTESTANT_ETHIC_METHODOLOGY_MEMO,
        }


def analyze_protestant_ethic(data: Any) -> Dict:
    return ProtestantEthicAnalyzer().analyze_protestant_ethic(data)


if __name__ == "__main__":
    test_data = "新教强调天职观，认为工作是上帝的召唤。信徒通过勤奋工作和节俭生活来证明自己是选民。"
    result = analyze_protestant_ethic(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
