#!/usr/bin/env python3
"""
bourdieu-field-analysis-expert - 场域自主性计算器
计算场域的自主性程度（相对于外部场域的独立性）
"""

from typing import Dict, List, Any, Optional
import re
import json


# 自主性指标
AUTONOMY_INDICATORS = {
    # 场域内在逻辑
    "internal_logic": {
        "positive": [
            "学术自由",
            "学术自主",
            "知识逻辑",
            "真理追求",
            "学术规范",
            "同行评议",
            " intrinsic logic ",
            " academic freedom ",
            " peer review ",
        ],
        "negative": [
            "经济逻辑",
            "市场逻辑",
            "政治干预",
            " external ",
            " market ",
        ],
        "description": "内在逻辑",
    },
    # 特定资本
    "specific_capital": {
        "positive": [
            "专业声誉",
            "学术地位",
            "知识权威",
            " expertise ",
            " scholarly ",
            " academic ",
        ],
        "negative": [
            "经济资本",
            "金钱",
            "财富",
            " economic ",
            " wealth ",
        ],
        "description": "特定资本",
    },
    # 准入门槛
    "entry_barrier": {
        "positive": [
            "专业门槛",
            "资格认证",
            "学历要求",
            "专业资格",
            " qualification ",
            " certification ",
        ],
        "negative": [
            "开放准入",
            "自由进入",
            "门槛低",
            " open access ",
        ],
        "description": "准入门槛",
    },
    # 评价标准
    "evaluation_criteria": {
        "positive": [
            "内在标准",
            "学术质量",
            "创新性",
            "理论贡献",
            " intrinsic ",
            " quality ",
            " innovation ",
        ],
        "negative": [
            "外在标准",
            "经济回报",
            "实用性",
            "市场价值",
            " economic ",
            "实用性",
        ],
        "description": "评价标准",
    },
    # 权力自主
    "power_autonomy": {
        "positive": [
            "自主决策",
            "独立",
            "不受干预",
            " autonomy ",
            " independent ",
        ],
        "negative": [
            "受制于",
            "依附",
            "听命于",
            " dependent ",
            " subordinated ",
        ],
        "description": "权力自主",
    },
}


class AutonomyCalculator:
    """场域自主性计算器"""

    def __init__(self):
        self.autonomy_scores = {}

    def calculate_autonomy(
        self,
        text: str,
        field_name: str = None,
        reference_fields: List[str] = None,
    ) -> Dict:
        """
        计算场域自主性

        参数:
            text: 分析文本
            field_name: 场域名称（可选）
            reference_fields: 参考场域列表（用于比较）

        返回:
            自主性分析结果
        """
        # 计算各维度自主性
        dimensions = self._calculate_dimension_autonomy(text)

        # 计算总体自主性
        overall = self._calculate_overall_autonomy(dimensions)

        # 分析自主性来源
        sources = self._identify_autonomy_sources(text)

        # 分析自主性威胁
        threats = self._identify_autonomy_threats(text)

        # 比较分析（如果有参考场域）
        comparison = (
            self._compare_with_reference(text, reference_fields)
            if reference_fields
            else {}
        )

        return {
            "field_name": field_name or "未知场域",
            "dimensions": dimensions,
            "overall_autonomy": overall,
            "autonomy_level": self._classify_autonomy_level(overall),
            "sources": sources,
            "threats": threats,
            "comparison": comparison,
            "recommendations": self._generate_recommendations(dimensions, threats),
        }

    def _calculate_dimension_autonomy(self, text: str) -> Dict[str, Dict]:
        """计算各维度自主性"""
        results = {}

        for dim_name, data in AUTONOMY_INDICATORS.items():
            positive_kw = data.get("positive", [])
            negative_kw = data.get("negative", [])

            # 计算正向和负向指标
            positive_count = sum(
                len(re.findall(kw, text, re.IGNORECASE)) for kw in positive_kw
            )
            negative_count = sum(
                len(re.findall(kw, text, re.IGNORECASE)) for kw in negative_kw
            )

            total = positive_count + negative_count

            if total == 0:
                score = 0.5  # 中立
            else:
                score = positive_count / total

            results[dim_name] = {
                "score": score,
                "positive_indicators": positive_count,
                "negative_indicators": negative_count,
                "description": data.get("description", dim_name),
            }

        return results

    def _calculate_overall_autonomy(self, dimensions: Dict) -> float:
        """计算总体自主性"""
        if not dimensions:
            return 0.5

        scores = [d.get("score", 0.5) for d in dimensions.values()]

        # 权重：内在逻辑和权力自主更重要
        weights = {
            "internal_logic": 0.25,
            "specific_capital": 0.20,
            "entry_barrier": 0.15,
            "evaluation_criteria": 0.20,
            "power_autonomy": 0.20,
        }

        weighted_sum = sum(
            scores[i] * weights.get(dim, 0.2) for i, dim in enumerate(dimensions.keys())
        )

        return weighted_sum

    def _classify_autonomy_level(self, score: float) -> str:
        """分类自主性等级"""
        if score >= 0.8:
            return "高度自主"
        elif score >= 0.6:
            return "中度自主"
        elif score >= 0.4:
            return "低度自主"
        else:
            return "高度他律"

    def _identify_autonomy_sources(self, text: str) -> List[Dict]:
        """识别自主性来源"""
        sources = []

        source_indicators = [
            (["学术自由", "自由探索", "学术独立"], "学术自由", 0.9),
            (["同行评议", "专家评审"], "同行认可机制", 0.8),
            (["专业资格", "专业门槛", "资格证书"], "专业准入门槛", 0.7),
            (["理论创新", "知识贡献", "学术声誉"], "知识权威", 0.8),
            (["独立资金", "研究经费", "基金会"], "财务独立", 0.7),
            (["自主决策", "自我管理", "自治"], "组织自主", 0.8),
        ]

        for keywords, source_name, base_score in source_indicators:
            count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)
            if count > 0:
                sources.append(
                    {
                        "source": source_name,
                        "strength": min(1.0, base_score * (1 + count * 0.1)),
                        "evidence_count": count,
                    }
                )

        # 按强度排序
        sources.sort(key=lambda x: x["strength"], reverse=True)
        return sources[:5]

    def _identify_autonomy_threats(self, text: str) -> List[Dict]:
        """识别自主性威胁"""
        threats = []

        threat_indicators = [
            (["政治干预", "政治控制", "政府"], "政治干预", 0.9),
            (["市场导向", "商业化", "利润"], "市场侵蚀", 0.8),
            (["资金依赖", "资助", "拨款"], "资金依赖", 0.7),
            (["行政干预", "行政控制", "管理层"], "行政干预", 0.7),
            (["媒体压力", "舆论", "公众意见"], "舆论压力", 0.5),
            (["企业赞助", "商业合作", "产业"], "产业渗透", 0.6),
        ]

        for keywords, threat_name, base_severity in threat_indicators:
            count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)
            if count > 0:
                threats.append(
                    {
                        "threat": threat_name,
                        "severity": min(1.0, base_severity * (1 + count * 0.1)),
                        "evidence_count": count,
                    }
                )

        # 按严重程度排序
        threats.sort(key=lambda x: x["severity"], reverse=True)
        return threats[:5]

    def _compare_with_reference(self, text: str, reference_fields: List[str]) -> Dict:
        """与参考场域比较"""
        # 这里可以扩展为更复杂的比较逻辑
        # 目前返回简化版本
        return {
            "reference_fields": reference_fields,
            "note": "需要更多数据进行精确比较",
        }

    def _generate_recommendations(
        self, dimensions: Dict, threats: List[Dict]
    ) -> List[str]:
        """生成提升自主性建议"""
        recommendations = []

        # 基于薄弱维度
        for dim_name, data in dimensions.items():
            score = data.get("score", 0.5)
            if score < 0.5:
                dim_chinese = data.get("description", dim_name)
                if dim_name == "internal_logic":
                    recommendations.append(f"加强{dim_chinese}：建立清晰的内在评价标准")
                elif dim_name == "specific_capital":
                    recommendations.append(f"强化{dim_chinese}：积累专业声誉和知识权威")
                elif dim_name == "entry_barrier":
                    recommendations.append(f"完善{dim_chinese}：建立专业资格认证体系")
                elif dim_name == "evaluation_criteria":
                    recommendations.append(f"优化{dim_chinese}：减少外在标准的影响")
                elif dim_name == "power_autonomy":
                    recommendations.append(f"提升{dim_chinese}：争取更多自主决策空间")

        # 基于威胁
        if threats:
            top_threat = threats[0]
            threat_name = top_threat.get("threat", "")
            if "政治" in threat_name:
                recommendations.append("减少政治干预，保持学术独立")
            elif "市场" in threat_name or "商业" in threat_name:
                recommendations.append("平衡市场需要与学术自由")
            elif "资金" in threat_name:
                recommendations.append("多元化资金来源，降低依赖")
            elif "行政" in threat_name:
                recommendations.append("争取更多自治权")

        if not recommendations:
            recommendations.append("场域自主性良好，维持现状")

        return recommendations[:5]

    def generate_autonomy_report(self, analysis_result: Dict) -> str:
        """生成自主性分析报告"""
        lines = []

        lines.append("# 场域自主性分析报告\n")

        # 总体评估
        overall = analysis_result.get("overall_autonomy", 0.5)
        level = analysis_result.get("autonomy_level", "未知")
        field_name = analysis_result.get("field_name", "未知场域")

        lines.append(f"## {field_name}自主性评估\n")
        lines.append(f"- 自主性得分: {overall:.2%}")
        lines.append(f"- 自主性等级: {level}")
        lines.append("")

        # 各维度分析
        lines.append("## 各维度自主性\n")
        dimensions = analysis_result.get("dimensions", {})
        for dim_name, data in dimensions.items():
            score = data.get("score", 0.5)
            desc = data.get("description", dim_name)
            level_icon = "✓" if score >= 0.5 else "✗"
            lines.append(f"- {level_icon} {desc}: {score:.2%}")
        lines.append("")

        # 自主性来源
        sources = analysis_result.get("sources", [])
        if sources:
            lines.append("## 自主性来源\n")
            for source in sources[:3]:
                lines.append(f"- {source.get('source')}: {source.get('strength'):.2%}")
            lines.append("")

        # 自主性威胁
        threats = analysis_result.get("threats", [])
        if threats:
            lines.append("## 自主性威胁\n")
            for threat in sources[:3]:
                lines.append(f"- {threat.get('threat')}: {threat.get('severity'):.2%}")
            lines.append("")

        # 建议
        recommendations = analysis_result.get("recommendations", [])
        if recommendations:
            lines.append("## 提升建议\n")
            for rec in recommendations:
                lines.append(f"- {rec}")

        return "\n".join(lines)


def calculate_autonomy(
    text: str, field_name: str = None, reference_fields: List[str] = None
) -> Dict:
    """场域自主性计算入口函数"""
    calculator = AutonomyCalculator()
    return calculator.calculate_autonomy(text, field_name, reference_fields)


if __name__ == "__main__":
    # 测试
    test_text = """
    学术场域具有较强的自主性。学者们遵循知识逻辑和学术规范，
    通过同行评议来评价学术成果。学术自由是核心价值。
    学者追求真理，不受政治干预。

    但是，学术场域也面临一些威胁。政府资助减少后，
    学者们越来越依赖企业赞助。市场化导向的科研评价
    正在影响学术自由。资金来源的多元化成为挑战。
    """

    result = calculate_autonomy(test_text, "学术场域")
    print(json.dumps(result, ensure_ascii=False, indent=2))
