#!/usr/bin/env python3
"""
digital-durkheim-expert - 社会事实识别工具
识别数据中的社会事实（外在性、强制性、普遍性）
基于涂尔干《社会学方法的准则》
"""

from typing import Dict, List, Any, Optional
import re
import json


# 社会事实指标
SOCIAL_FACTS_INDICATORS = {
    # 外在性指标
    "externality": {
        "positive": [
            "社会规范",
            "社会制度",
            "集体意识",
            "社会价值观",
            "法律",
            "道德",
            "习俗",
            "制度",
            "external ",
            " social norm ",
            " institution ",
            " collective ",
        ],
        "description": "外在性 - 社会事实独立于个体存在",
    },
    # 强制性指标
    "coerciveness": {
        "positive": [
            "强制",
            "约束",
            "规范",
            "必须",
            "应当",
            "禁止",
            "惩罚",
            "制裁",
            " pressure ",
            " constraint ",
            " obligation ",
            " sanction ",
        ],
        "description": "强制性 - 社会事实对个体施加压力",
    },
    # 普遍性指标
    "generality": {
        "positive": [
            "普遍",
            "共同",
            "共享",
            "一般",
            "全体",
            "广泛",
            " common ",
            " universal ",
            " shared ",
            " general ",
        ],
        "description": "普遍性 - 社会事实在社会中广泛存在",
    },
    # 功能性指标
    "functionality": {
        "positive": [
            "功能",
            "作用",
            "维持",
            "整合",
            "秩序",
            "稳定",
            " function ",
            " maintain ",
            " integrate ",
            " order ",
        ],
        "description": "功能性 - 社会事实对社会具有功能",
    },
    # 物质性 vs 精神性
    "materiality": {
        "material": [
            "法律",
            "制度",
            "组织",
            "机构",
            "法律",
            "规则",
            " law ",
            " institution ",
            " organization ",
        ],
        "non_material": [
            "价值观",
            "信念",
            "意识",
            "心态",
            "集体意识",
            "道德",
            " values ",
            " beliefs ",
            " consciousness ",
        ],
        "description": "物质性/精神性 - 社会事实的存在形式",
    },
}


class SocialFactsIdentifier:
    """社会事实识别器"""

    def __init__(self):
        self.identified_facts = []

    def identify_social_facts(
        self, data: Any, analysis_type: str = "general"
    ) -> Dict:
        """
        识别社会事实

        参数:
            data: 分析数据（文本、统计、观察等）
            analysis_type: 分析类型

        返回:
            社会事实识别结果
        """
        # 转换为文本
        text = self._convert_to_text(data)

        # 识别各维度指标
        externality = self._analyze_externality(text)
        coerciveness = self._analyze_coerciveness(text)
        generality = self._analyze_generality(text)
        functionality = self._analyze_functionality(text)
        materiality = self._analyze_materiality(text)

        # 识别具体社会事实
        specific_facts = self._identify_specific_facts(text)

        # 计算社会事实强度
        strength = self._calculate_facts_strength(
            externality, coerciveness, generality, functionality
        )

        # 分类
        classification = self._classify_social_facts(
            externality, coerciveness, generality, materiality
        )

        return {
            "data_type": type(data).__name__,
            "analysis_type": analysis_type,
            "dimensions": {
                "externality": externality,
                "coerciveness": coerciveness,
                "generality": generality,
                "functionality": functionality,
                "materiality": materiality,
            },
            "specific_facts": specific_facts,
            "strength": strength,
            "classification": classification,
            "verdict": self._make_verdict(strength, classification),
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

    def _analyze_externality(self, text: str) -> Dict:
        """分析外在性"""
        positive_kw = SOCIAL_FACTS_INDICATORS["externality"]["positive"]
        count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in positive_kw)

        return {
            "score": min(1.0, count / 5),
            "evidence_count": count,
            "description": SOCIAL_FACTS_INDICATORS["externality"]["description"],
        }

    def _analyze_coerciveness(self, text: str) -> Dict:
        """分析强制性"""
        positive_kw = SOCIAL_FACTS_INDICATORS["coerciveness"]["positive"]
        count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in positive_kw)

        return {
            "score": min(1.0, count / 5),
            "evidence_count": count,
            "description": SOCIAL_FACTS_INDICATORS["coerciveness"]["description"],
        }

    def _analyze_generality(self, text: str) -> Dict:
        """分析普遍性"""
        positive_kw = SOCIAL_FACTS_INDICATORS["generality"]["positive"]
        count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in positive_kw)

        return {
            "score": min(1.0, count / 5),
            "evidence_count": count,
            "description": SOCIAL_FACTS_INDICATORS["generality"]["description"],
        }

    def _analyze_functionality(self, text: str) -> Dict:
        """分析功能性"""
        positive_kw = SOCIAL_FACTS_INDICATORS["functionality"]["positive"]
        count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in positive_kw)

        return {
            "score": min(1.0, count / 5),
            "evidence_count": count,
            "description": SOCIAL_FACTS_INDICATORS["functionality"]["description"],
        }

    def _analyze_materiality(self, text: str) -> Dict:
        """分析物质性/精神性"""
        material_kw = SOCIAL_FACTS_INDICATORS["materiality"]["material"]
        non_material_kw = SOCIAL_FACTS_INDICATORS["materiality"]["non_material"]

        material_count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in material_kw)
        non_material_count = sum(
            len(re.findall(kw, text, re.IGNORECASE)) for kw in non_material_kw
        )

        total = material_count + non_material_count
        if total == 0:
            score = 0.5
        else:
            score = material_count / total

        return {
            "score": score,
            "material_count": material_count,
            "non_material_count": non_material_count,
            "description": SOCIAL_FACTS_INDICATORS["materiality"]["description"],
        }

    def _identify_specific_facts(self, text: str) -> List[Dict]:
        """识别具体社会事实"""
        facts = []

        # 法律规范
        law_patterns = ["法律", "法规", "条例", "规范", " law ", " regulation "]
        if any(p in text for p in law_patterns):
            facts.append(
                {
                    "type": "法律规范",
                    "evidence": "法律/法规相关表述",
                    "category": "物质性社会事实",
                }
            )

        # 道德规范
        moral_patterns = ["道德", "伦理", "价值观", " moral ", " ethics ", " values "]
        if any(p in text for p in moral_patterns):
            facts.append(
                {
                    "type": "道德规范",
                    "evidence": "道德/价值观相关表述",
                    "category": "精神性社会事实",
                }
            )

        # 宗教信仰
        religion_patterns = ["宗教", "信仰", "教义", "仪式", " religion ", " faith "]
        if any(p in text for p in religion_patterns):
            facts.append(
                {
                    "type": "宗教信仰",
                    "evidence": "宗教/信仰相关表述",
                    "category": "精神性社会事实",
                }
            )

        # 社会制度
        institution_patterns = [
            "制度",
            "体制",
            "组织",
            "机构",
            " institution ",
            " organization ",
        ]
        if any(p in text for p in institution_patterns):
            facts.append(
                {
                    "type": "社会制度",
                    "evidence": "制度/组织相关表述",
                    "category": "物质性社会事实",
                }
            )

        # 集体意识
        collective_patterns = [
            "集体意识",
            "共同价值观",
            "社会共识",
            " collective ",
            " shared ",
        ]
        if any(p in text for p in collective_patterns):
            facts.append(
                {
                    "type": "集体意识",
                    "evidence": "集体/共享相关表述",
                    "category": "精神性社会事实",
                }
            )

        return facts

    def _calculate_facts_strength(
        self,
        externality: Dict,
        coerciveness: Dict,
        generality: Dict,
        functionality: Dict,
    ) -> float:
        """计算社会事实强度"""
        scores = [
            externality.get("score", 0),
            coerciveness.get("score", 0),
            generality.get("score", 0),
            functionality.get("score", 0),
        ]
        return sum(scores) / len(scores)

    def _classify_social_facts(
        self,
        externality: Dict,
        coerciveness: Dict,
        generality: Dict,
        materiality: Dict,
    ) -> Dict:
        """分类社会事实"""
        # 判断是否为社会事实
        is_social_fact = (
            externality.get("score", 0) >= 0.3
            and coerciveness.get("score", 0) >= 0.3
            and generality.get("score", 0) >= 0.3
        )

        # 判断类型
        material_score = materiality.get("score", 0.5)
        if material_score > 0.6:
            fact_type = "物质性社会事实"
        elif material_score < 0.4:
            fact_type = "精神性社会事实"
        else:
            fact_type = "混合型社会事实"

        return {
            "is_social_fact": is_social_fact,
            "fact_type": fact_type if is_social_fact else "非社会事实",
            "confidence": (externality.get("score", 0) + coerciveness.get("score", 0)) / 2,
        }

    def _make_verdict(self, strength: float, classification: Dict) -> str:
        """做出判断"""
        if classification.get("is_social_fact") and strength >= 0.5:
            return "强社会事实"
        elif classification.get("is_social_fact"):
            return "弱社会事实"
        else:
            return "非社会事实"

    def generate_report(self, result: Dict) -> str:
        """生成分析报告"""
        lines = []
        lines.append("# 社会事实识别报告\n")

        # 总体判断
        verdict = result.get("verdict", "未知")
        lines.append(f"## 总体判断: {verdict}\n")

        # 各维度分析
        lines.append("## 维度分析\n")
        dimensions = result.get("dimensions", {})
        for dim_name, data in dimensions.items():
            score = data.get("score", 0)
            desc = data.get("description", dim_name)
            dim_icon = "✓" if score >= 0.3 else "✗"
            lines.append(f"- {dim_icon} {desc}: {score:.2%}")
        lines.append("")

        # 具体事实
        specific_facts = result.get("specific_facts", [])
        if specific_facts:
            lines.append("## 识别的社会事实\n")
            for fact in specific_facts:
                lines.append(f"- **{fact.get('type')}** ({fact.get('category')})")
                lines.append(f"  - 证据: {fact.get('evidence')}")
            lines.append("")

        # 分类
        classification = result.get("classification", {})
        lines.append("## 分类结果\n")
        lines.append(f"- 类型: {classification.get('fact_type', '未知')}")
        lines.append(f"- 置信度: {classification.get('confidence', 0):.2%}")

        return "\n".join(lines)


def identify_social_facts(data: Any, analysis_type: str = "general") -> Dict:
    """社会事实识别入口函数"""
    identifier = SocialFactsIdentifier()
    return identifier.identify_social_facts(data, analysis_type)


if __name__ == "__main__":
    # 测试
    test_data = """
    在现代社会，法律制度是典型的社会事实。法律具有外在性，
    它独立于个体存在，不以个人意志为转移。同时，法律具有强制性，
    公民必须遵守，否则将面临法律制裁。法律在社会中普遍存在，
    维护着社会秩序和稳定。法律对社会具有重要的功能，
    它整合社会成员，维持社会秩序。
    
    除了法律，道德规范也是重要的社会事实。道德规范体现了
    集体意识，是社会成员共同价值观的体现。
    """

    result = identify_social_facts(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
