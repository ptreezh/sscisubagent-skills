#!/usr/bin/env python3
"""
bourdieu-field-analysis-expert - 位置映射工具
映射行动者在场域中的位置（支配/被支配、主导/跟随）
"""

from typing import Dict, List, Set, Any
from collections import defaultdict
import re
import json


# 位置指标
POSITION_INDICATORS = {
    "dominant": {
        "keywords": [
            "支配",
            "控制",
            "主导",
            "领导",
            "权威",
            "决定",
            "权力",
            "统治",
            "管理",
            "支配",
            " dominant ",
            " control ",
            " lead ",
            " authority ",
        ],
        "description": "支配性位置",
    },
    "dominated": {
        "keywords": [
            "服从",
            "被支配",
            "跟随",
            "依附",
            "从属",
            "弱势",
            "被动",
            " dominated ",
            " subordinate ",
            " dependent ",
        ],
        "description": "被支配位置",
    },
    "autonomous": {
        "keywords": [
            "独立",
            "自主",
            "自由",
            "不受约束",
            "自主性",
            " autonomous ",
            " independent ",
            " free ",
        ],
        "description": "自主位置",
    },
    "heteronomous": {
        "keywords": ["依附", "依赖", "受制", "不自主", " heteronomous ", " dependent "],
        "description": "他律位置",
    },
    "central": {
        "keywords": [
            "核心",
            "中心",
            "主要",
            "关键",
            "重要",
            " central ",
            " core ",
            " key ",
            " main ",
        ],
        "description": "核心位置",
    },
    "peripheral": {
        "keywords": [
            "边缘",
            "外围",
            "次要",
            "辅助",
            " peripheral ",
            " marginal ",
            " secondary ",
        ],
        "description": "边缘位置",
    },
}


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
        """识别位置指标"""
        indicators = {}

        for pos_type, data in POSITION_INDICATORS.items():
            keywords = data.get("keywords", [])
            count = 0
            for keyword in keywords:
                count += len(re.findall(keyword, text, re.IGNORECASE))

            if count > 0:
                indicators[pos_type] = count

        return indicators

    def _extract_actor_positions(self, text: str, actors: List[str]) -> Dict[str, Dict]:
        """提取每个行动者的位置"""
        positions = {}

        for actor in actors:
            positions[actor] = {
                "dominance": self._calculate_dominance(text, actor),
                "autonomy": self._calculate_autonomy(text, actor),
                "centrality": self._calculate_centrality(text, actor),
                "evidence": self._collect_position_evidence(text, actor),
            }

        return positions

    def _calculate_dominance(self, text: str, actor: str) -> float:
        """计算支配度"""
        # 支配性指标
        dominant_count = 0
        for keyword in POSITION_INDICATORS.get("dominant", {}).get("keywords", []):
            dominant_count += len(re.findall(keyword, text, re.IGNORECASE))

        # 被支配指标
        dominated_count = 0
        for keyword in POSITION_INDICATORS.get("dominated", {}).get("keywords", []):
            dominated_count += len(re.findall(keyword, text, re.IGNORECASE))

        total = dominant_count + dominated_count
        if total == 0:
            return 0.5

        return dominant_count / total

    def _calculate_autonomy(self, text: str, actor: str) -> float:
        """计算自主度"""
        autonomous_count = 0
        for keyword in POSITION_INDICATORS.get("autonomous", {}).get("keywords", []):
            autonomous_count += len(re.findall(keyword, text, re.IGNORECASE))

        heteronomous_count = 0
        for keyword in POSITION_INDICATORS.get("heteronomous", {}).get("keywords", []):
            heteronomous_count += len(re.findall(keyword, text, re.IGNORECASE))

        total = autonomous_count + heteronomous_count
        if total == 0:
            return 0.5

        return autonomous_count / total

    def _calculate_centrality(self, text: str, actor: str) -> float:
        """计算中心度"""
        central_count = 0
        for keyword in POSITION_INDICATORS.get("central", {}).get("keywords", []):
            central_count += len(re.findall(keyword, text, re.IGNORECASE))

        peripheral_count = 0
        for keyword in POSITION_INDICATORS.get("peripheral", {}).get("keywords", []):
            peripheral_count += len(re.findall(keyword, text, re.IGNORECASE))

        total = central_count + peripheral_count
        if total == 0:
            return 0.5

        return central_count / total

    def _collect_position_evidence(self, text: str, actor: str) -> List[str]:
        """收集位置证据"""
        evidence = []

        all_keywords = []
        for data in POSITION_INDICATORS.values():
            all_keywords.extend(data.get("keywords", []))

        for keyword in all_keywords:
            if keyword.lower() in text.lower():
                evidence.append(keyword)

        return list(set(evidence))[:10]

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
        """识别位置关系"""
        relations = []

        # 查找位置关系模式
        relation_patterns = [
            (["支配", "控制", "领导"], "dominates"),
            (["服从", "被支配", "跟随"], "is_dominated_by"),
            (["合作", "联合", "结盟"], "allies_with"),
            (["竞争", "对抗", "争夺"], "competes_with"),
        ]

        actors = list(positions.keys())
        for i, actor1 in enumerate(actors):
            for actor2 in actors[i + 1 :]:
                for keywords, rel_type in relation_patterns:
                    for keyword in keywords:
                        if keyword in text:
                            relations.append(
                                {
                                    "actor1": actor1,
                                    "actor2": actor2,
                                    "relation": rel_type,
                                    "keyword": keyword,
                                }
                            )
                            break

        return relations

    def _calculate_position_structure(self, positions: Dict) -> Dict:
        """计算位置结构"""
        if not positions:
            return {"type": "unknown", "polarization": 0}

        # 计算位置分布
        dominances = [p.get("dominance", 0.5) for p in positions.values()]
        autonomies = [p.get("autonomy", 0.5) for p in positions.values()]
        centralities = [p.get("centrality", 0.5) for p in positions.values()]

        # 极化程度
        import statistics

        try:
            dom_std = statistics.stdev(dominances) if len(dominances) > 1 else 0
            polar = min(1.0, dom_std * 2)
        except:
            polar = 0

        # 判断结构类型
        avg_dom = sum(dominances) / len(dominances)
        avg_aut = sum(autonomies) / len(autonomies)

        if avg_dom > 0.7:
            struct_type = "hierarchical_dominant"
        elif avg_dom < 0.3:
            struct_type = "hierarchical_dominated"
        elif avg_aut > 0.7:
            struct_type = "autonomous_plural"
        else:
            struct_type = "mixed"

        return {
            "type": struct_type,
            "polarization": polar,
            "avg_dominance": sum(dominances) / len(dominances),
            "avg_autonomy": avg_aut,
            "avg_centrality": sum(centralities) / len(centralities),
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
                f"- 结构类型: {struct_names.get(structure.get('type', 'unknown'), '未知')}"
            )
            lines.append(f"- 极化程度: {structure.get('polarization', 0):.2%}")
            lines.append("")

        # 行动者位置
        positions = analysis_result.get("actor_positions", {})
        if positions:
            lines.append("## 行动者位置\n")
            for actor, pos in positions.items():
                lines.append(f"### {actor}\n")
                dom = pos.get("dominance", 0.5)
                aut = pos.get("autonomy", 0.5)
                cent = pos.get("centrality", 0.5)

                position_type = self._classify_position(dom, aut, cent)
                lines.append(f"- 位置类型: {position_type}")
                lines.append(f"- 支配度: {dom:.2f}")
                lines.append(f"- 自主度: {aut:.2f}")
                lines.append(f"- 中心度: {cent:.2f}")
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
        """分类位置类型"""
        if dominance > 0.7 and centrality > 0.7:
            return "核心支配者"
        elif dominance > 0.7:
            return "支配者"
        elif dominance < 0.3 and centrality < 0.3:
            return "边缘被支配者"
        elif dominance < 0.3:
            return "被支配者"
        elif autonomy > 0.7:
            return "独立行动者"
        else:
            return "中间位置"


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
