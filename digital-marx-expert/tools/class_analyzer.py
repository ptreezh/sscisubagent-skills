#!/usr/bin/env python3
"""
digital-marx-expert - 阶级分析工具
分析社会阶级结构：资产阶级、无产阶级、中产阶级等
基于马克思阶级理论
"""

from typing import Dict, List, Any
import re
import json


# 阶级指标
CLASS_INDICATORS = {
    # 资产阶级
    "bourgeoisie": {
        "keywords": [
            "资产阶级",
            "资本家",
            "企业家",
            "企业主",
            "富有的",
            " bourgeoisie ",
            " capitalist ",
            " entrepreneur ",
            " owner ",
        ],
        "attributes": [
            "占有生产资料",
            "雇佣劳动",
            "获得利润",
            "资本积累",
            " owns production ",
            " hires labor ",
            " profit ",
        ],
        "description": "资产阶级 - 占有生产资料的阶级",
    },
    # 无产阶级
    "proletariat": {
        "keywords": [
            "无产阶级",
            "工人",
            "劳动者",
            "雇工",
            "薪金劳动者",
            " proletariat ",
            " worker ",
            " laborer ",
            " employee ",
        ],
        "attributes": [
            "出卖劳动力",
            "受雇于",
            "获取工资",
            "不占有生产资料",
            " sells labor ",
            " works for ",
            " wage ",
        ],
        "description": "无产阶级 - 出卖劳动力的阶级",
    },
    # 中产阶级
    "middle_class": {
        "keywords": [
            "中产阶级",
            "中产阶层",
            "白领",
            "专业人员",
            " middle class ",
            " white collar ",
            " professional ",
        ],
        "attributes": [
            "专业技能",
            "稳定收入",
            "小资产",
            " expertise ",
            " stable income ",
        ],
        "description": "中产阶级 - 介于资产阶级和无产阶级之间",
    },
    # 农民阶级
    "peasantry": {
        "keywords": [
            "农民",
            "农夫",
            "农业劳动者",
            " peasant ",
            " farmer ",
        ],
        "attributes": [
            "耕种土地",
            "小块土地",
            "自耕农",
            " farms land ",
            " smallholding ",
        ],
        "description": "农民阶级 - 从事农业生产的阶级",
    },
    # 地主阶级
    "landlord": {
        "keywords": [
            "地主",
            "土地所有者",
            "封建主",
            " landlord ",
            " landowner ",
        ],
        "attributes": [
            "占有土地",
            "收取地租",
            "土地出租",
            " owns land ",
            " collects rent ",
        ],
        "description": "地主阶级 - 占有土地的阶级",
    },
}


class ClassAnalyzer:
    """阶级分析器"""

    def __init__(self):
        self.analysis_results = []

    def analyze_class(self, data: Any, focus_class: str = None) -> Dict:
        """
        分析阶级结构

        参数:
            data: 分析数据
            focus_class: 关注的主要阶级

        返回:
            阶级分析结果
        """
        # 转换为文本
        text = self._convert_to_text(data)

        # 分析各阶级
        bourgeoisie = self._analyze_class("bourgeoisie", text)
        proletariat = self._analyze_class("proletariat", text)
        middle_class = self._analyze_class("middle_class", text)
        peasantry = self._analyze_class("peasantry", text)
        landlord = self._analyze_class("landlord", text)

        # 确定主导阶级
        dominant_class = self._determine_dominant_class(
            bourgeoisie, proletariat, middle_class, peasantry, landlord
        )

        # 分析阶级关系
        class_relations = self._analyze_class_relations(
            bourgeoisie, proletariat, middle_class
        )

        # 计算阶级张力
        class_tension = self._calculate_class_tension(bourgeoisie, proletariat)

        # 生成理论解释
        explanation = self._generate_explanation(
            dominant_class, class_relations, class_tension
        )

        return {
            "data_type": type(data).__name__,
            "focus_class": focus_class,
            "classes": {
                "bourgeoisie": bourgeoisie,
                "proletariat": proletariat,
                "middle_class": middle_class,
                "peasantry": peasantry,
                "landlord": landlord,
            },
            "dominant_class": dominant_class,
            "class_relations": class_relations,
            "class_tension": class_tension,
            "explanation": explanation,
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

    def _analyze_class(self, class_name: str, text: str) -> Dict:
        """分析特定阶级"""
        indicators = CLASS_INDICATORS.get(class_name, {})

        keywords = indicators.get("keywords", [])
        attributes = indicators.get("attributes", [])

        keyword_count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)
        attribute_count = sum(
            len(re.findall(kw, text, re.IGNORECASE)) for kw in attributes
        )

        total_count = keyword_count + attribute_count
        score = min(1.0, total_count / 5)

        return {
            "score": score,
            "evidence_count": total_count,
            "description": indicators.get("description", ""),
        }

    def _determine_dominant_class(
        self,
        bourgeoisie: Dict,
        proletariat: Dict,
        middle_class: Dict,
        peasantry: Dict,
        landlord: Dict,
    ) -> str:
        """确定主导阶级"""
        scores = {
            "资产阶级": bourgeoisie.get("score", 0),
            "无产阶级": proletariat.get("score", 0),
            "中产阶级": middle_class.get("score", 0),
            "农民阶级": peasantry.get("score", 0),
            "地主阶级": landlord.get("score", 0),
        }

        max_class = max(scores, key=scores.get)
        max_score = scores[max_class]

        if max_score < 0.2:
            return "未确定"
        return max_class

    def _analyze_class_relations(
        self,
        bourgeoisie: Dict,
        proletariat: Dict,
        middle_class: Dict,
    ) -> List[Dict]:
        """分析阶级关系"""
        relations = []

        # 资产阶级与无产阶级的关系
        if bourgeoisie.get("score", 0) > 0.2 and proletariat.get("score", 0) > 0.2:
            relations.append(
                {
                    "relation": "剥削关系",
                    "classes": ["资产阶级", "无产阶级"],
                    "description": "资产阶级通过雇佣劳动剥削无产阶级",
                }
            )

        # 中间阶级的位置
        if middle_class.get("score", 0) > 0.3:
            relations.append(
                {
                    "relation": "中间阶级",
                    "classes": ["中产阶级"],
                    "description": "介于资产阶级和无产阶级之间",
                }
            )

        return relations

    def _calculate_class_tension(self, bourgeoisie: Dict, proletariat: Dict) -> float:
        """计算阶级张力"""
        # 阶级张力取决于两个阶级的对立程度
        combined_score = bourgeoisie.get("score", 0) + proletariat.get("score", 0)

        if combined_score < 0.3:
            return 0.0

        # 张力 = 资产阶级得分 * 无产阶级得分
        tension = bourgeoisie.get("score", 0) * proletariat.get("score", 0)

        return min(1.0, tension * 2)

    def _generate_explanation(
        self,
        dominant_class: str,
        class_relations: List[Dict],
        class_tension: float,
    ) -> str:
        """生成理论解释"""
        lines = []

        if dominant_class != "未确定":
            lines.append(f"主导阶级: {dominant_class}")

        if class_relations:
            lines.append("阶级关系:")
            for rel in class_relations:
                lines.append(f"  - {rel.get('relation')}: {rel.get('description')}")

        if class_tension > 0.5:
            lines.append(f"阶级张力: 高 (存在显著的阶级对立)")
        elif class_tension > 0.2:
            lines.append(f"阶级张力: 中等")
        else:
            lines.append(f"阶级张力: 低")

        return "\n".join(lines)


def analyze_class(data: Any, focus_class: str = None) -> Dict:
    """阶级分析入口函数"""
    analyzer = ClassAnalyzer()
    return analyzer.analyze_class(data, focus_class)


if __name__ == "__main__":
    # 测试
    test_data = """
    该社会存在明显的阶级分化。资产阶级占有生产资料，
    雇佣大量工人进行生产，获取利润。工人阶级出卖劳动力，
    获取工资收入，处于被剥削地位。中产阶级拥有专业技能，
    生活水平相对稳定。
    """

    result = analyze_class(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
