#!/usr/bin/env python3
"""
digital-marx-expert - 生产方式识别工具
识别社会生产方式：资本主义、社会主义、封建主义、数字资本主义等
基于马克思历史唯物主义

【方法论说明】
本工具不包含任何硬编码关键词匹配。所有生产方式判断由LLM根据理论备忘录完成。
工具仅负责：状态管理、空结构返回、方法论引导。
"""

from typing import Dict, List, Any
import json


# ---------------------------------------------------------------------------
# 生产方式理论备忘录（供LLM判断时参考）
# ---------------------------------------------------------------------------
MODE_OF_PRODUCTION_THEORY_MEMO = """
=== 马克思生产方式（Mode of Production）理论备忘录 ===

【核心概念】
生产方式由生产力（人和自然的关系）和生产关系（人和人的社会关系）构成。
马克思的历史唯物主义认为：生产力决定生产关系，生产关系总和构成经济基础，
经济基础决定上层建筑（法律、政治、意识形态）。

【历史唯物主义分析框架】

1. 首先识别生产力水平：
   - 使用什么工具和技术？
   - 劳动分工发展到什么程度？
   - 生产的社会化程度如何？

2. 然后分析生产关系：
   - 生产资料所有制：谁占有生产工具和劳动产品？
   - 劳动关系：剥削关系还是平等关系？
   - 产品分配：按什么原则分配？

【主要生产方式识别框架】（供LLM判断参考）

1. 资本主义生产方式
   - 生产资料私有制（资本家占有工厂、机器、土地）
   - 雇佣劳动关系（工人不占有生产资料，出卖劳动力）
   - 剩余价值生产（劳动创造的价值超过劳动力价值）
   - 商品生产普遍化（一切皆可成为商品）
   - 核心矛盾：生产社会化与生产资料私有制之间的矛盾
   - 判断标准：是否存在雇佣劳动关系？资本家是否占有剩余价值？

2. 社会主义生产方式
   - 生产资料公有制（国家所有或集体所有）
   - 计划经济（国家计划配置资源）或市场社会主义
   - 按劳分配原则
   - 无产阶级专政（过渡阶段）
   - 判断标准：公有制是否占主导？国家是否控制生产资料？

3. 封建主义生产方式
   - 封建土地所有制（地主占有土地）
   - 超经济强制（人身依附关系：农奴、佃农）
   - 自然经济为主（生产主要为满足自身需要）
   - 地租形态（劳役地租、实物地租、货币地租）
   - 判断标准：是否存在人身依附关系？土地是否是最主要的生产资料？

4. 奴隶制生产方式
   - 奴隶主对奴隶的完全人身所有权
   - 奴隶本身是生产工具，是"会说话的工具"
   - 奴隶无偿劳动，产品全部归奴隶主
   - 判断标准：是否存在对人的完全所有权？

5. 数字资本主义（当代新形式）
   - 数字平台成为核心生产资料
   - 数据成为新的生产要素
   - 零工经济（gig economy）：形式上的灵活就业，实为新的雇佣形式
   - 产消者（prosumers）：用户同时是生产者和消费者
   - 平台垄断：平台对生态系统的控制
   - 判断标准：平台是否成为新的生产资料控制者？

【分析方法论】
- 实际社会往往是多种生产方式的混合或过渡形态
- 追问：什么是最具决定性的生产关系？
- 关注：生产方式如何决定社会阶层结构和意识形态？
- 判断结果填入返回结构中的 None 字段
"""


class ModeOfProductionIdentifier:
    """生产方式识别器（无关键词匹配版）

    所有生产方式判断由调用方/LLM根据 MODE_OF_PRODUCTION_THEORY_MEMO 完成。
    """

    def __init__(self):
        self.identification_results = []

    def identify_mode_of_production(
        self, data: Any, historical_context: str = None
    ) -> Dict:
        """
        识别生产方式（返回空结构供LLM填充）

        参数:
            data: 分析数据
            historical_context: 历史背景

        返回:
            含空结构的生产方式识别结果，需LLM根据 MODE_OF_PRODUCTION_THEORY_MEMO 填充
        """
        raw_text = self._convert_to_text(data)

        result: Dict = {
            "data_type": type(data).__name__,
            "historical_context": historical_context,
            "modes": {
                # LLM填充：判断每种生产方式的存在程度(0.0-1.0)和证据
                "capitalist": {
                    "score": None,           # 0.0-1.0
                    "evidence_count": None,       # LLM主观证据计数
                    "production_relations_evidence": None,  # 生产关系证据
                    "class_structure_evidence": None,        # 阶级结构证据
                    "description": "资本主义生产方式 - 生产资料私有制+雇佣劳动",
                    "evidence": [],               # LLM提取的证据片段
                    "reasoning": None,            # LLM判断理由
                },
                "socialist": {
                    "score": None,
                    "evidence_count": None,
                    "production_relations_evidence": None,
                    "class_structure_evidence": None,
                    "description": "社会主义生产方式 - 生产资料公有制+计划经济",
                    "evidence": [],
                    "reasoning": None,
                },
                "feudal": {
                    "score": None,
                    "evidence_count": None,
                    "production_relations_evidence": None,
                    "class_structure_evidence": None,
                    "description": "封建主义生产方式 - 土地封建所有制+人身依附",
                    "evidence": [],
                    "reasoning": None,
                },
                "slave": {
                    "score": None,
                    "evidence_count": None,
                    "production_relations_evidence": None,
                    "class_structure_evidence": None,
                    "description": "奴隶制生产方式 - 对人的完全所有权",
                    "evidence": [],
                    "reasoning": None,
                },
                "digital_capitalist": {
                    "score": None,
                    "evidence_count": None,
                    "production_relations_evidence": None,
                    "class_structure_evidence": None,
                    "description": "数字资本主义 - 平台+数据+零工经济",
                    "evidence": [],
                    "reasoning": None,
                },
            },
            "dominant_mode": None,            # LLM判断: "资本主义"/"社会主义"/"封建主义"/"数字资本主义"/"未确定"
            "transitional_features": [],      # LLM识别: ["封建主义向资本主义过渡", ...]
            "explanation": None,               # LLM基于历史唯物主义的解释
            "theory_memo": MODE_OF_PRODUCTION_THEORY_MEMO.strip(),
            "raw_text_for_llm": raw_text[:5000],
        }
        self.identification_results.append(result)
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


def identify_mode_of_production(data: Any, historical_context: str = None) -> Dict:
    """生产方式识别入口函数"""
    identifier = ModeOfProductionIdentifier()
    return identifier.identify_mode_of_production(data, historical_context)


if __name__ == "__main__":
    test_data = """
    该社会以雇佣劳动为基础，资本家占有生产资料，
    通过市场进行商品交换。存在资产阶级和无产阶级的对立。
    工人为资本家生产剩余价值。
    同时，平台经济发展迅速，数据成为新的生产资料。
    """
    result = identify_mode_of_production(test_data)
    print("=== 返回结构（需LLM填充） ===")
    print(f"dominant_mode: {result['dominant_mode']}")
    print(f"transitional_features: {result['transitional_features']}")
    print(f"\n理论备忘录（前300字）:\n{result['theory_memo'][:300]}")
