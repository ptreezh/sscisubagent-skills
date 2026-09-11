#!/usr/bin/env python3
"""
bourdieu-field-analysis-expert - 位置映射工具
映射行动者在场域中的位置（支配/被支配、主导/跟随）
"""

from typing import Dict, List, Set, Any
from collections import defaultdict
import json


# Bourdieu位置分析methodology memo
# 位置指标关键词匹配已禁用
# 位置判断是布迪厄场域诠释性判断，由LLM完成
POSITION_METHODOLOGY_MEMO = """【布迪厄位置分析 - LLM专属判断】
Bourdieu场域中的位置由资本总量和资本结构决定。
- 禁止：用关键词匹配("支配"/"服从"/"核心")判断行动者位置
- 正确做法：
  * 支配/被支配：基于资本总量和资本转化能力
  * 自主/他律：基于场域自主性程度
  * 核心/边缘：基于与其他行动者的关系网络位置
- 位置是相对的，不是绝对的
- 位置类型判断需LLM综合分析，不可用关键词计数自动确定
"""


# 关键词字典已禁用（保留占位，防止引用处报错）
POSITION_INDICATORS = {}


class PositionMapper:
    """位置映射器"""

    def __init__(self):
        self.actor_positions = {}
        self.position_relations = []

    def map_positions(self, text: str, actors: List[str] = None) -> Dict:
        """
        映射行动者位置

        参数:
            text: 分析文本
            actors: 行动者列表（可选）

        返回:
            位置映射结果
        """
        # 识别位置指标
        indicators = self._identify_position_indicators(text)

        # 提取行动者位置
        if actors:
            positions = self._extract_actor_positions(text, actors)
        else:
            positions = self._infer_positions_from_text(text)

        # 识别位置关系
        relations = self._identify_position_relations(text, positions)

        # 计算位置结构
        structure = self._calculate_position_structure(positions)

        return {
            "indicators": indicators,
            "actor_positions": positions,
            "position_relations": relations,
            "structure": structure,
        }

    def _identify_position_indicators(self, text: str) -> Dict[str, int]:
        """识别位置指标。

        ⚠️ 关键词计数已禁用，由LLM做布迪厄场域位置诠释判断。
        """
        return {
            "indicators": None,  # LLM填充
            "methodology_memo": POSITION_METHODOLOGY_MEMO,
        }

    def _extract_actor_positions(self, text: str, actors: List[str]) -> Dict[str, Dict]:
        """提取每个行动者的位置。

        ⚠️ 关键词计数已禁用，由LLM做布迪厄场域诠释判断。
        """
        positions = {}
        for actor in actors:
            positions[actor] = {
                "dominance": None,  # LLM填充
                "autonomy": None,  # LLM填充
                "centrality": None,  # LLM填充
                "evidence": [],  # LLM填充
            }
        return positions

    def _calculate_dominance(self, text: str, actor: str) -> float:
        """
        返回支配度原始比值占位。

        ⚠️ 关键词匹配已禁用。
        支配/被支配判断由LLM基于布迪厄场域理论完成。
        返回值固定为None，强制LLM做诠释判断。
        """
        return None  # LLM基于POSITION_METHODOLOGY_MEMO做布迪厄诠释判断

    def _calculate_autonomy(self, text: str, actor: str) -> float:
        """
        返回自主度原始比值占位。

        ⚠️ 关键词匹配已禁用。
        自主/他律判断由LLM基于布迪厄场域理论完成。
        """
        return None  # LLM基于POSITION_METHODOLOGY_MEMO做布迪厄诠释判断

    def _calculate_centrality(self, text: str, actor: str) -> float:
        """
        返回中心度原始比值占位。

        ⚠️ 关键词匹配已禁用。
        核心/边缘判断由LLM基于布迪厄场域理论完成。
        """
        return None  # LLM基于POSITION_METHODOLOGY_MEMO做布迪厄诠释判断

    def _collect_position_evidence(self, text: str, actor: str) -> List[str]:
        """收集位置证据占位。关键词匹配已禁用。"""
        return []  # LLM基于POSITION_METHODOLOGY_MEMO填充

    def _infer_positions_from_text(self, text: str) -> Dict:
        """从文本推断位置（无行动者）"""
        # 基于整体文本推断位置结构
        dominance = self._calculate_dominance(text, "")
        autonomy = self._calculate_autonomy(text, "")
        centrality = self._calculate_centrality(text, "")

        return {
            "overall": {
                "dominance": dominance,
                "autonomy": autonomy,
                "centrality": centrality,
            }
        }

    def _identify_position_relations(self, text: str, positions: Dict) -> List[Dict]:
        """识别位置关系。

        ⚠️ 关键词匹配已禁用，由LLM基于布迪厄场域理论做诠释判断。
        """
        # 硬编码判断已禁用，返回空结构由LLM填充
        return []  # LLM填充: [{actor1, actor2, relation, reasoning, evidence}]

    def _calculate_position_structure(self, positions: Dict) -> Dict:
        """
        计算位置结构统计值。

        Python计算极化程度和平均值（定量）
        0.7/0.3阈值分支判断结构类型已禁用，由LLM做诠释判断
        """
        import statistics
        valid_doms = [p for p in positions.values() if p.get("dominance") is not None]
        valid_auts = [p for p in positions.values() if p.get("autonomy") is not None]
        valid_cents = [p for p in positions.values() if p.get("centrality") is not None]

        dominances = [p["dominance"] for p in valid_doms]
        autonomies = [p["autonomy"] for p in valid_auts]
        centralities = [p["centrality"] for p in valid_cents]

        polar = None
        if len(dominances) > 1:
            try:
                polar = round(min(1.0, statistics.stdev(dominances) * 2), 3)
            except:
                polar = None

        avg_dom = round(sum(dominances) / len(dominances), 3) if dominances else None
        avg_aut = round(sum(autonomies) / len(autonomies), 3) if autonomies else None
        avg_cent = round(sum(centralities) / len(centralities), 3) if centralities else None

        return {
            "type": None,   # 禁用阈值分支 → LLM填充
            "polarization": polar,
            "avg_dominance": avg_dom,
            "avg_autonomy": avg_aut,
            "avg_centrality": avg_cent,
            "methodology_memo": "type判断由LLM基于布迪厄场域理论完成，0.7/0.3仅为定量参考",
        }

    def generate_position_report(self, analysis_result: Dict) -> str:
        """生成位置映射报告"""
        lines = []
        lines.append("# 位置映射分析报告\n")

        # 位置结构
        structure = analysis_result.get("structure", {})
        if structure:
            lines.append("## 位置结构\n")
            struct_names = {
                "hierarchical_dominant": "支配性层级",
                "hierarchical_dominated": "从属性层级",
                "autonomous_plural": "多元自主",
                "mixed": "混合结构",
            }
            lines.append(
                f"- 结构类型: {structure.get('type') or 'LLM填充'}"
            )
            lines.append(f"- 极化程度: {structure.get('polarization') or 'LLM填充'}")
            lines.append("")

        # 行动者位置
        positions = analysis_result.get("actor_positions", {})
        if positions:
            lines.append("## 行动者位置\n")
            for actor, pos in positions.items():
                lines.append(f"### {actor}\n")
                dom = pos.get("dominance")
                aut = pos.get("autonomy")
                cent = pos.get("centrality")

                position_type = self._classify_position(dom, aut, cent)
                lines.append(f"- 位置类型: {position_type or 'LLM填充（定量计算后由LLM判断）'}")
                lines.append(f"- 支配度: {dom if dom is not None else '无关键词信号，LLM诠释'}")
                lines.append(f"- 自主度: {aut if aut is not None else '无关键词信号，LLM诠释'}")
                lines.append(f"- 中心度: {cent if cent is not None else '无关键词信号，LLM诠释'}")
            lines.append("")

        # 位置关系
        relations = analysis_result.get("position_relations", [])
        if relations:
            lines.append("## 位置关系\n")
            for rel in relations[:5]:
                lines.append(
                    f"- {rel.get('actor1')} {rel.get('relation')} {rel.get('actor2')}"
                )

        return "\n".join(lines)

    def _classify_position(
        self, dominance: float, autonomy: float, centrality: float
    ) -> str:
        """分类位置类型。

        ⚠️ 0.7/0.3阈值分支已禁用，由LLM基于布迪厄场域理论做诠释判断。
        """
        return None  # LLM填充


def map_positions(text: str, actors: List[str] = None) -> Dict:
    """位置映射入口函数"""
    mapper = PositionMapper()
    return mapper.map_positions(text, actors)


if __name__ == "__main__":
    # 测试
    test_text = """
    王教授是学术场域的核心人物，控制着学术资源分配，
    主导学术评价标准，决定哪些论文可以发表。
    他拥有很大的学术自主权。
    
    张博士依附于王教授的研究团队，
    服从导师的决定，跟随研究方向。
    他的学术自主性较低，处于边缘位置。
    
    企业家李总资助王教授的研究，形成合作关系。
    """

    actors = ["王教授", "张博士", "李总"]
    result = map_positions(test_text, actors)
    print(json.dumps(result, ensure_ascii=False, indent=2))
