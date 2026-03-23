#!/usr/bin/env python3
"""
digital-marx-expert - 劳动过程分析工具
分析劳动过程：分工、协作、劳动控制等
基于马克思《资本论》和布雷弗曼《劳动与垄断资本》
"""

from typing import Dict, List, Any
import re
import json


# 劳动过程指标
LABOR_PROCESS_INDICATORS = {
    # 分工
    "division_of_labor": {
        "keywords": [
            "分工",
            "专业化",
            "精细化",
            "部门化",
            " division of labor ",
            " specialization ",
            " departmentalization ",
        ],
        "description": "劳动分工程度",
    },
    # 协作
    "cooperation": {
        "keywords": [
            "协作",
            "合作",
            "团队",
            "集体劳动",
            " cooperation ",
            " teamwork ",
            " collective labor ",
        ],
        "description": "劳动协作程度",
    },
    # 劳动控制
    "labor_control": {
        "keywords": [
            "监督",
            "管理",
            "控制",
            "考核",
            "规训",
            " surveillance ",
            " management ",
            " control ",
            " discipline ",
        ],
        "description": "劳动控制程度",
    },
    # 异化
    "alienation": {
        "keywords": [
            "异化",
            "疏离",
            "无意义",
            "单调",
            " alienation ",
            " estranged ",
            " meaningless ",
            " monotonous ",
        ],
        "description": "劳动异化程度",
    },
    # 技术条件
    "technology": {
        "keywords": [
            "机器",
            "自动化",
            "技术",
            "工具",
            " machine ",
            " automation ",
            " technology ",
            " tool ",
        ],
        "description": "技术条件",
    },
}


class LaborProcessAnalyzer:
    """劳动过程分析器"""

    def __init__(self):
        self.analysis_results = []

    def analyze_labor_process(self, data: Any, industry: str = None) -> Dict:
        """
        分析劳动过程

        参数:
            data: 分析数据
            industry: 行业类型

        返回:
            劳动过程分析结果
        """
        # 转换为文本
        text = self._convert_to_text(data)

        # 分析各维度
        division = self._analyze_dimension("division_of_labor", text)
        cooperation = self._analyze_dimension("cooperation", text)
        control = self._analyze_dimension("labor_control", text)
        alienation = self._analyze_dimension("alienation", text)
        technology = self._analyze_dimension("technology", text)

        # 计算总体劳动过程特征
        overall = self._calculate_overall(division, cooperation, control, alienation)

        # 分析劳动控制模式
        control_mode = self._analyze_control_mode(control, alienation)

        # 生成理论解释
        explanation = self._generate_explanation(
            division, cooperation, control_mode, technology
        )

        return {
            "data_type": type(data).__name__,
            "industry": industry,
            "dimensions": {
                "division_of_labor": division,
                "cooperation": cooperation,
                "labor_control": control,
                "alienation": alienation,
                "technology": technology,
            },
            "overall_score": overall,
            "control_mode": control_mode,
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

    def _analyze_dimension(self, dimension: str, text: str) -> Dict:
        """分析特定维度"""
        indicators = LABOR_PROCESS_INDICATORS.get(dimension, {})
        keywords = indicators.get("keywords", [])

        count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)
        score = min(1.0, count / 3)

        return {
            "score": score,
            "evidence_count": count,
            "description": indicators.get("description", ""),
        }

    def _calculate_overall(
        self,
        division: Dict,
        cooperation: Dict,
        control: Dict,
        alienation: Dict,
    ) -> float:
        """计算总体劳动过程特征"""
        scores = [
            division.get("score", 0),
            cooperation.get("score", 0),
            control.get("score", 0),
            alienation.get("score", 0),
        ]
        return sum(scores) / len(scores)

    def _analyze_control_mode(self, control: Dict, alienation: Dict) -> str:
        """分析劳动控制模式"""
        control_score = control.get("score", 0)
        alienation_score = alienation.get("score", 0)

        if control_score > 0.6 and alienation_score > 0.6:
            return "高度控制-异化型"
        elif control_score > 0.6:
            return "高度控制型"
        elif alienation_score > 0.6:
            return "高度异化型"
        elif control_score > 0.3 or alienation_score > 0.3:
            return "中等控制型"
        else:
            return "自主型"

    def _generate_explanation(
        self,
        division: Dict,
        cooperation: Dict,
        control_mode: str,
        technology: Dict,
    ) -> str:
        """生成理论解释"""
        lines = []

        # 分工
        if division.get("score", 0) > 0.5:
            lines.append("劳动分工高度发达，专业化程度高。")
        elif division.get("score", 0) > 0.2:
            lines.append("存在一定的劳动分工。")
        else:
            lines.append("劳动分工程度较低。")

        # 协作
        if cooperation.get("score", 0) > 0.5:
            lines.append("劳动协作程度高。")

        # 控制模式
        control_explanations = {
            "高度控制-异化型": "采用泰勒制管理，工人被严格监督，劳动异化严重。",
            "高度控制型": "采用严格的劳动管理制度。",
            "高度异化型": "劳动过程导致严重的异化。",
            "中等控制型": "劳动管理较为规范。",
            "自主型": "劳动者有较大的自主权。",
        }
        lines.append(control_explanations.get(control_mode, ""))

        # 技术
        if technology.get("score", 0) > 0.5:
            lines.append("技术自动化程度高。")

        return " ".join(lines)


def analyze_labor_process(data: Any, industry: str = None) -> Dict:
    """劳动过程分析入口函数"""
    analyzer = LaborProcessAnalyzer()
    return analyzer.analyze_labor_process(data, industry)


if __name__ == "__main__":
    # 测试
    test_data = """
    该工厂采用泰勒制的科学管理方法。劳动分工精细，
    每个工人只负责一个简单的操作动作。管理人员监督严格，
    工人必须按照规定的节奏工作。劳动单调重复，
    工人感到疏离和无意义。生产自动化程度不断提高。
    """

    result = analyze_labor_process(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
