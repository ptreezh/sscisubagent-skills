#!/usr/bin/env python3
"""
bourdieu-field-analysis-expert - 资本分析工具
分析经济资本、文化资本、社会资本、象征资本的分布
"""

from typing import Dict, List, Set, Any
from collections import defaultdict
import re
import json


# 资本类型关键词
CAPITAL_PATTERNS = {
    "economic": {
        "keywords": [
            "金钱",
            "财富",
            "收入",
            "资产",
            "财产",
            "金钱",
            "工资",
            "薪酬",
            "投资",
            "利润",
            "收入",
            "房产",
            "金钱",
            " money ",
            " wealth ",
            " income ",
            " asset ",
            " property ",
            " salary ",
        ],
        "indicators": ["经济资本", "经济资源", "物质资源", "金钱"],
    },
    "cultural": {
        "keywords": [
            "教育",
            "学历",
            "文凭",
            "文化",
            "知识",
            "艺术",
            "品位",
            "鉴赏",
            "教养",
            " 文化资本 ",
            " education ",
            " knowledge ",
            " culture ",
            " taste ",
            " diploma ",
        ],
        "indicators": ["文化资本", "教育资本", "学历", "专业知识"],
    },
    "social": {
        "keywords": [
            "关系",
            "人脉",
            "网络",
            "社交",
            "联系",
            "朋友",
            "同事",
            "同学",
            " 社会资本 ",
            " social capital ",
            " network ",
            " relationship ",
            " connection ",
        ],
        "indicators": ["社会资本", "社会关系", "社会网络"],
    },
    "symbolic": {
        "keywords": [
            "声望",
            "声誉",
            "名望",
            "地位",
            "头衔",
            "称号",
            "荣誉",
            "象征",
            " 象征资本 ",
            " symbolic capital ",
            " prestige ",
            " reputation ",
            " status ",
            " honor ",
        ],
        "indicators": ["象征资本", "符号资本", "名望资本"],
    },
}


class CapitalAnalyzer:
    """资本分析器"""

    def __init__(self):
        self.capital_distributions = defaultdict(lambda: defaultdict(float))
        self.actor_capitals = defaultdict(dict)
        self.capital_conversions = []

    def analyze_capital_distribution(self, text: str, actors: List[str] = None) -> Dict:
        """
        分析资本分布

        参数:
            text: 分析文本
            actors: 行动者列表（可选）

        返回:
            资本分布分析结果
        """
        # 识别资本类型
        capital_types = self._identify_capital_types(text)

        # 提取行动者资本
        if actors:
            actor_capitals = self._extract_actor_capitals(text, actors)
        else:
            actor_capitals = self._extract_capitals_from_text(text)

        # 计算资本总量
        total_capitals = self._calculate_total_capitals(capital_types)

        # 识别资本转换
        conversions = self._identify_capital_conversions(text)

        return {
            "capital_types": capital_types,
            "actor_capitals": actor_capitals,
            "total_capitals": total_capitals,
            "conversions": conversions,
            "heterogeneity_score": self._calculate_heterogeneity(total_capitals),
        }

    def _identify_capital_types(self, text: str) -> Dict[str, List[Dict]]:
        """识别文本中的资本类型"""
        results = {capital_type: [] for capital_type in CAPITAL_PATTERNS.keys()}

        for capital_type, patterns in CAPITAL_PATTERNS.items():
            # 关键词匹配
            for keyword in patterns["keywords"]:
                if keyword.lower() in text.lower():
                    results[capital_type].append(
                        {
                            "type": "keyword",
                            "keyword": keyword,
                            "context": self._extract_context(text, keyword),
                        }
                    )

            # 指标匹配
            for indicator in patterns.get("indicators", []):
                if indicator in text:
                    results[capital_type].append(
                        {
                            "type": "indicator",
                            "indicator": indicator,
                            "context": self._extract_context(text, indicator),
                        }
                    )

        # 清理空结果
        return {k: v for k, v in results.items() if v}

    def _extract_context(self, text: str, keyword: str, context_size: int = 50) -> str:
        """提取关键词上下文"""
        idx = text.lower().find(keyword.lower())
        if idx == -1:
            return ""

        start = max(0, idx - context_size)
        end = min(len(text), idx + len(keyword) + context_size)

        return text[start:end].strip()

    def _extract_actor_capitals(self, text: str, actors: List[str]) -> Dict[str, Dict]:
        """提取每个行动者的资本"""
        actor_capitals = defaultdict(
            lambda: {
                "economic": 0,
                "cultural": 0,
                "social": 0,
                "symbolic": 0,
                "evidence": [],
            }
        )

        for actor in actors:
            # 查找该行动者附近的资本描述
            for capital_type in CAPITAL_PATTERNS.keys():
                # 简化实现：基于关键词出现位置估算
                mentions = self._count_actor_capital_mentions(text, actor, capital_type)
                if mentions > 0:
                    actor_capitals[actor][capital_type] = mentions
                    actor_capitals[actor]["evidence"].append(
                        {"capital_type": capital_type, "mentions": mentions}
                    )

        return dict(actor_capitals)

    def _count_actor_capital_mentions(
        self, text: str, actor: str, capital_type: str
    ) -> int:
        """计算行动者与特定资本的关联次数"""
        keywords = CAPITAL_PATTERNS.get(capital_type, {}).get("keywords", [])

        # 查找行动者附近（简化：整个文本中）的资本关键词
        count = 0
        for keyword in keywords:
            count += len(re.findall(keyword, text, re.IGNORECASE))

        return count

    def _extract_capitals_from_text(self, text: str) -> Dict[str, Dict]:
        """从文本中提取资本（无行动者信息）"""
        capitals = defaultdict(lambda: {"count": 0, "examples": []})

        for capital_type, patterns in CAPITAL_PATTERNS.items():
            for keyword in patterns["keywords"]:
                matches = re.findall(keyword, text, re.IGNORECASE)
                if matches:
                    capitals[capital_type]["count"] += len(matches)
                    capitals[capital_type]["examples"].append(keyword)

        return dict(capitals)

    def _calculate_total_capitals(self, capital_types: Dict) -> Dict[str, float]:
        """计算各类型资本总量"""
        totals = {}

        for capital_type, mentions in capital_types.items():
            if isinstance(mentions, list):
                totals[capital_type] = len(mentions)
            else:
                totals[capital_type] = 0

        return totals

    def _identify_capital_conversions(self, text: str) -> List[Dict]:
        """识别资本转换"""
        conversions = []

        # 常见转换模式
        conversion_patterns = [
            ("经济转文化", ["购买", "教育", "投资", "学费", "购买艺术品"]),
            ("文化转经济", ["出售", "交易", "变现", "知识产权"]),
            ("经济转社会", ["宴请", "送礼", "赞助", "建立关系"]),
            ("社会转经济", ["人脉", "介绍", "资源", "合作机会"]),
            ("文化转象征", ["获得", "荣誉", "头衔", "声誉"]),
            ("象征转经济", ["代言", "品牌", "影响力", "变现"]),
        ]

        for conversion_type, keywords in conversion_patterns:
            for keyword in keywords:
                if keyword in text:
                    conversions.append(
                        {
                            "type": conversion_type,
                            "keyword": keyword,
                            "context": self._extract_context(text, keyword),
                        }
                    )

        return conversions

    def _calculate_heterogeneity(self, capitals: Dict[str, float]) -> float:
        """计算资本异质性分数"""
        total = sum(capitals.values())

        if total == 0:
            return 0.0

        # 使用熵来衡量异质性
        import math

        entropy = 0
        for value in capitals.values():
            if value > 0:
                p = value / total
                entropy -= p * math.log(p, len(capitals))

        # 归一化
        max_entropy = math.log(len(capitals)) if capitals else 1

        return entropy / max_entropy if max_entropy > 0 else 0

    def generate_capital_report(self, analysis_result: Dict) -> str:
        """生成资本分析报告"""
        lines = []
        lines.append("# 资本分布分析报告\n")

        # 资本类型
        capitals = analysis_result.get("total_capitals", {})
        if capitals:
            lines.append("## 资本分布\n")
            for cap_type, count in capitals.items():
                cap_names = {
                    "economic": "经济资本",
                    "cultural": "文化资本",
                    "social": "社会资本",
                    "symbolic": "象征资本",
                }
                lines.append(f"- {cap_names.get(cap_type, cap_type)}: {count}")
            lines.append("")

        # 异质性
        hetero = analysis_result.get("heterogeneity_score", 0)
        lines.append(f"## 资本异质性\n")
        lines.append(f"异质性分数: {hetero:.2%}")
        if hetero > 0.7:
            lines.append("评估: 资本分布高度异质")
        elif hetero > 0.4:
            lines.append("评估: 资本分布中等异质")
        else:
            lines.append("评估: 资本分布相对单一")
        lines.append("")

        # 转换
        conversions = analysis_result.get("conversions", [])
        if conversions:
            lines.append("## 资本转换\n")
            for conv in conversions[:5]:
                lines.append(f"- {conv['type']}: {conv['keyword']}")

        return "\n".join(lines)


def analyze_capital_distribution(text: str, actors: List[str] = None) -> Dict:
    """资本分析入口函数"""
    analyzer = CapitalAnalyzer()
    return analyzer.analyze_capital_distribution(text, actors)


if __name__ == "__main__":
    # 测试
    test_text = """
    王教授拥有高学历（文化资本）和大学教职（象征资本）。
    他通过教学和研究积累学术声誉，每年收入数十万元（经济资本）。
    他与社会各界人士有广泛联系（社会资本），经常参加学术会议。
    
    张企业家拥有大量财富（经济资本），投资教育事业，
    购买艺术品收藏（文化资本），与社会名流交往（社会资本），
    获得慈善家称号（象征资本）。
    """

    actors = ["王教授", "张企业家"]
    result = analyze_capital_distribution(test_text, actors)
    print(json.dumps(result, ensure_ascii=False, indent=2))
