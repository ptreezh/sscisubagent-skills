#!/usr/bin/env python3
"""
bourdieu-field-analysis-expert - 习性检测工具
识别行动者的习性模式与场域对应关系
"""

from typing import Dict, List, Set, Any
from collections import defaultdict
import re
import json


# 习性指标
HABITUS_PATTERNS = {
    # 性情倾向
    "disposition": {
        "patterns": [
            "倾向于",
            "习惯于",
            "总是",
            "通常",
            "偏好",
            "喜欢",
            "倾向于",
            "惯于",
            " tendency ",
            " habit ",
            " preference ",
        ],
        "description": "持久的性情倾向",
    },
    # 实践
    "practice": {
        "patterns": [
            "做",
            "进行",
            "从事",
            "采取",
            "行动",
            "实践",
            "做",
            " practice ",
            " action ",
            " do ",
        ],
        "description": "身体化的行动",
    },
    # 表征/品位
    "taste": {
        "patterns": [
            "喜欢",
            "欣赏",
            "偏好",
            "选择",
            "品位",
            "品味",
            "选择",
            " taste ",
            " preference ",
            " appreciate ",
        ],
        "description": "区分实践与表征",
    },
    # 性情倾向关键词
    "disposition_keywords": [
        "性情",
        "倾向",
        "习惯",
        "习性",
        "惯习",
        "性情倾向",
        "disposition",
        "habitus",
        "tendency",
        "propensity",
    ],
    # 身体化指标
    "incorporated": [
        "内化",
        "不自觉",
        "潜意识",
        "本能",
        "自然",
        "自然而然",
        "incorporated",
        "internalized",
        "unconscious",
    ],
}


class HabitustDetector:
    """习性检测器"""

    def __init__(self):
        self.habitus_patterns = defaultdict(list)
        self.actor_habitus = {}
        self.habitus_field_correspondence = []

    def detect_habitus(self, text: str, actors: List[str] = None) -> Dict:
        """
        检测习性模式

        参数:
            text: 分析文本
            actors: 行动者列表（可选）

        返回:
            习性检测结果
        """
        # 识别习性指标
        indicators = self._identify_habitus_indicators(text)

        # 提取行动者习性
        if actors:
            actor_habitus = self._extract_actor_habitus(text, actors)
        else:
            actor_habitus = self._extract_habitus_patterns(text)

        # 分析习性与场域对应
        correspondence = self._analyze_field_correspondence(text, actor_habitus)

        return {
            "indicators": indicators,
            "actor_habitus": actor_habitus,
            "field_correspondence": correspondence,
            "habitus_strength": self._calculate_habitus_strength(indicators),
        }

    def _identify_habitus_indicators(self, text: str) -> Dict[str, int]:
        """识别习性指标"""
        indicators = {}

        for category, data in HABITUS_PATTERNS.items():
            if isinstance(data, dict) and "patterns" in data:
                patterns = data["patterns"]
            elif isinstance(data, list):
                patterns = data
            else:
                patterns = []

            count = 0
            for pattern in patterns:
                count += len(re.findall(pattern, text, re.IGNORECASE))

            if count > 0:
                indicators[category] = count

        return indicators

    def _extract_actor_habitus(self, text: str, actors: List[str]) -> Dict[str, Dict]:
        """提取每个行动者的习性"""
        actor_habitus = {}

        for actor in actors:
            actor_habitus[actor] = {
                "dispositions": self._find_dispositions_for_actor(text, actor),
                "practices": self._find_practices_for_actor(text, actor),
                "tastes": self._find_tastes_for_actor(text, actor),
                "incorporated": self._find_incorporated_for_actor(text, actor),
            }

        return actor_habitus

    def _find_dispositions_for_actor(self, text: str, actor: str) -> List[str]:
        """查找行动者的性情倾向"""
        dispositions = []

        patterns = HABITUS_PATTERNS.get("disposition", {}).get("patterns", [])
        for pattern in patterns:
            # 查找行动者附近的模式
            if pattern in text:
                dispositions.append(pattern)

        return list(set(dispositions))

    def _find_practices_for_actor(self, text: str, actor: str) -> List[str]:
        """查找行动者的实践"""
        practices = []

        patterns = HABITUS_PATTERNS.get("practice", {}).get("patterns", [])
        for pattern in patterns:
            if pattern in text:
                practices.append(pattern)

        return list(set(practices))

    def _find_tastes_for_actor(self, text: str, actor: str) -> List[str]:
        """查找行动者的品位"""
        tastes = []

        patterns = HABITUS_PATTERNS.get("taste", {}).get("patterns", [])
        for pattern in patterns:
            if pattern in text:
                tastes.append(pattern)

        return list(set(tastes))

    def _find_incorporated_for_actor(self, text: str, actor: str) -> List[str]:
        """查找行动者的身体化指标"""
        incorporated = []

        keywords = HABITUS_PATTERNS.get("incorporated", [])
        for keyword in keywords:
            if keyword in text:
                incorporated.append(keyword)

        return incorporated

    def _extract_habitus_patterns(self, text: str) -> Dict:
        """提取习性模式（无行动者）"""
        patterns = {
            "dispositions": [],
            "practices": [],
            "tastes": [],
            "incorporated": [],
        }

        # 性情倾向
        for pattern in HABITUS_PATTERNS.get("disposition", {}).get("patterns", []):
            if pattern.lower() in text.lower():
                patterns["dispositions"].append(pattern)

        # 实践
        for pattern in HABITUS_PATTERNS.get("practice", {}).get("patterns", []):
            if pattern.lower() in text.lower():
                patterns["practices"].append(pattern)

        # 品位
        for pattern in HABITUS_PATTERNS.get("taste", {}).get("patterns", []):
            if pattern.lower() in text.lower():
                patterns["tastes"].append(pattern)

        # 身体化
        for keyword in HABITUS_PATTERNS.get("incorporated", []):
            if keyword in text:
                patterns["incorporated"].append(keyword)

        return {k: list(set(v)) for k, v in patterns.items()}

    def _analyze_field_correspondence(
        self, text: str, actor_habitus: Dict
    ) -> List[Dict]:
        """分析习性与场域对应"""
        correspondence = []

        # 识别场域
        fields = self._identify_fields_in_text(text)

        # 建立对应关系
        for actor, habitus in actor_habitus.items():
            if habitus.get("dispositions") or habitus.get("practices"):
                correspondence.append(
                    {
                        "actor": actor,
                        "fields": fields,
                        "habitus_type": self._classify_habitus(habitus),
                        "correspondence_strength": self._calculate_correspondence(
                            habitus, fields
                        ),
                    }
                )

        return correspondence

    def _identify_fields_in_text(self, text: str) -> List[str]:
        """识别文本中的场域"""
        fields = []

        field_keywords = {
            "academic": ["学术", "大学", "研究", "学者"],
            "economic": ["经济", "商业", "市场", "企业"],
            "artistic": ["艺术", "文化", "审美"],
            "political": ["政治", "权力", "政府"],
        }

        for field, keywords in field_keywords.items():
            for keyword in keywords:
                if keyword in text:
                    fields.append(field)
                    break

        return list(set(fields))

    def _classify_habitus(self, habitus: Dict) -> str:
        """分类习性类型"""
        disposition_count = len(habitus.get("dispositions", []))
        practice_count = len(habitus.get("practices", []))
        taste_count = len(habitus.get("tastes", []))

        if taste_count > practice_count and taste_count > disposition_count:
            return "aesthetic"
        elif practice_count > disposition_count:
            return "practical"
        else:
            return "dispositional"

    def _calculate_correspondence(self, habitus: Dict, fields: List[str]) -> float:
        """计算对应强度"""
        if not fields:
            return 0.0

        # 简化实现：基于习性要素数量
        habitus_elements = (
            len(habitus.get("dispositions", []))
            + len(habitus.get("practices", []))
            + len(habitus.get("tastes", []))
        )

        return min(1.0, habitus_elements / len(fields))

    def _calculate_habitus_strength(self, indicators: Dict) -> float:
        """计算习性强度"""
        if not indicators:
            return 0.0

        total = sum(indicators.values())

        if total >= 10:
            return 1.0
        elif total >= 5:
            return 0.7
        elif total >= 2:
            return 0.4
        else:
            return 0.2

    def generate_habitus_report(self, analysis_result: Dict) -> str:
        """生成习性分析报告"""
        lines = []
        lines.append("# 习性分析报告\n")

        # 习性指标
        indicators = analysis_result.get("indicators", {})
        if indicators:
            lines.append("## 习性指标\n")
            for ind, count in indicators.items():
                lines.append(f"- {ind}: {count}处")
            lines.append("")

        # 行动者习性
        actor_habitus = analysis_result.get("actor_habitus", {})
        if actor_habitus:
            lines.append("## 行动者习性\n")
            for actor, habitus in actor_habitus.items():
                lines.append(f"### {actor}\n")
                hab_type = self._classify_habitus(habitus)
                lines.append(f"- 习性类型: {hab_type}")
                lines.append(f"- 性情倾向: {len(habitus.get('dispositions', []))}项")
                lines.append(f"- 实践: {len(habitus.get('practices', []))}项")
                lines.append(f"- 品位: {len(habitus.get('tastes', []))}项")
            lines.append("")

        # 对应关系
        corr = analysis_result.get("field_correspondence", [])
        if corr:
            lines.append("## 习性-场域对应\n")
            for c in corr[:3]:
                lines.append(
                    f"- {c.get('actor', 'Unknown')}: {c.get('correspondence_strength', 0):.2f}"
                )

        return "\n".join(lines)


def detect_habitus(text: str, actors: List[str] = None) -> Dict:
    """习性检测入口函数"""
    detector = HabitustDetector()
    return detector.detect_habitus(text, actors)


if __name__ == "__main__":
    # 测试
    test_text = """
    王教授习惯于每天早上去图书馆研究，倾向于选择理论性强的课题。
    他自然而然地用学术标准评判事物，不自觉地维护学术场域的规则。
    他的品位偏向理论深度，实践中总是追求创新。
    
    张企业家习惯于应酬交际，倾向于投资回报率高的项目。
    他自然而然地用商业眼光看问题，实践中总是追求利润最大化。
    他的品位偏向实用价值。
    """

    actors = ["王教授", "张企业家"]
    result = detect_habitus(test_text, actors)
    print(json.dumps(result, ensure_ascii=False, indent=2))
