#!/usr/bin/env python3
"""
bourdieu-field-analysis-expert - 场域边界识别工具
基于布迪厄场域理论识别分析场域的边界
"""

from typing import Dict, List, Set, Any, Optional
from collections import defaultdict
import re
import json


# 场域边界识别指标
FIELD_INDICATORS = {
    # 场域特有词汇
    "stakes": [" stakes ", "利益", "赌注", "竞争", "争夺", " enjeu "],
    "competition": ["竞争", "争夺", "比赛", "竞赛", " competition ", " rivalry "],
    "conflict": ["冲突", "对立", "矛盾", "争议", " conflict ", " tension "],
    "resources": ["资源", "资本", "资产", "利益", " resource ", " capital "],
    "rules": ["规则", "规范", "制度", "法则", " rule ", " norm "],
    "agents": ["行动者", "参与者", "主体", " agent ", " actor "],
    # 中英文专业术语
    "bourdieu_terms": [
        "场域",
        "field",
        "资本",
        "capital",
        "习性",
        "habitus",
        "位置",
        "position",
        "策略",
        "strategy",
        "惯习",
        "性情倾向",
        "文化资本",
        "cultural capital",
        "经济资本",
        "economic capital",
        "社会资本",
        "social capital",
        "象征资本",
        "symbolic capital",
        "场域自主性",
        "field autonomy",
        "位置取用",
        "position-taking",
    ],
}


class FieldIdentifier:
    """场域边界识别器"""

    def __init__(self):
        self.identified_fields = []
        self.field_actors = defaultdict(list)
        self.field_indicators = defaultdict(list)
        self.boundary_evidence = []

    def identify_field_boundaries(self, text: str, context: str = None) -> Dict:
        """
        识别场域边界

        参数:
            text: 分析文本
            context: 上下文信息（可选）

        返回:
            场域识别结果
        """
        # 识别场域指标
        found_indicators = self._find_indicators(text)

        # 提取可能的场域
        possible_fields = self._extract_possible_fields(text)

        # 评估场域边界强度
        field_assessment = self._assess_field_boundaries(
            possible_fields, found_indicators
        )

        return {
            "possible_fields": possible_fields,
            "indicators_found": found_indicators,
            "boundary_strength": field_assessment,
            "field_actors": dict(self.field_actors),
            "evidence": self.boundary_evidence,
        }

    def _find_indicators(self, text: str) -> Dict[str, List[str]]:
        """查找场域指标"""
        found = defaultdict(list)

        for indicator_type, keywords in FIELD_INDICATORS.items():
            for keyword in keywords:
                if keyword.lower() in text.lower():
                    found[indicator_type].append(keyword)

        return dict(found)

    def _extract_possible_fields(self, text: str) -> List[Dict]:
        """提取可能的场域"""
        possible_fields = []

        # 基于场域类型识别
        field_types = {
            "学术场域": [
                "学术",
                "大学",
                "研究",
                "论文",
                "学者",
                "学术期刊",
                "学术会议",
            ],
            "艺术场域": ["艺术", "美术馆", "画廊", "艺术家", "作品", "展览"],
            "政治场域": ["政治", "政府", "政党", "选举", "政策", "权力"],
            "经济场域": ["经济", "市场", "企业", "商业", "交易", "利润"],
            "媒体场域": ["媒体", "新闻", "报纸", "电视", "记者", "报道"],
            "教育场域": ["教育", "学校", "学生", "教师", "课程", "考试"],
            "宗教场域": ["宗教", "信仰", "教会", "神职", "仪式"],
        }

        for field_name, keywords in field_types.items():
            matches = []
            for keyword in keywords:
                if keyword in text:
                    matches.append(keyword)

            if matches:
                possible_fields.append(
                    {
                        "field_name": field_name,
                        "matched_keywords": matches,
                        "confidence": len(matches) / len(keywords),
                    }
                )

        return possible_fields

    def _assess_field_boundaries(self, fields: List[Dict], indicators: Dict) -> Dict:
        """评估场域边界强度"""
        if not fields:
            return {"strength": "weak", "score": 0, "reason": "未发现明确的场域指标"}

        # 计算边界强度分数
        indicator_score = sum(len(v) for v in indicators.values())
        field_score = sum(f["confidence"] for f in fields)

        total_score = (indicator_score * 0.6) + (field_score * 0.4)

        if total_score >= 0.7:
            strength = "strong"
        elif total_score >= 0.4:
            strength = "moderate"
        else:
            strength = "weak"

        return {
            "strength": strength,
            "score": round(total_score, 2),
            "indicator_count": indicator_score,
            "field_count": len(fields),
        }

    def extract_field_actors(self, text: str, field_name: str) -> List[str]:
        """提取特定场域的行动者"""
        actors = []

        # 提取组织
        org_patterns = [
            r"([^\s]+大学)",
            r"([^\s]+公司)",
            r"([^\s]+机构)",
            r"([^\s]+组织)",
            r"([^\s]+部门)",
        ]

        for pattern in org_patterns:
            matches = re.findall(pattern, text)
            actors.extend(matches)

        # 提取个人
        person_patterns = [
            r"([A-Z][a-z]+\s+[A-Z][a-z]+)",
            r"([^\s]+教授)",
            r"([^\s]+博士)",
            r"([^\s]+主任)",
            r"([^\s]+经理)",
        ]

        for pattern in person_patterns:
            matches = re.findall(pattern, text)
            actors.extend(matches)

        self.field_actors[field_name] = list(set(actors))
        return list(set(actors))

    def generate_field_report(self, analysis_result: Dict) -> str:
        """生成场域识别报告"""
        lines = []
        lines.append("# 场域边界识别报告\n")

        fields = analysis_result.get("possible_fields", [])
        if fields:
            lines.append("## 识别的场域\n")
            for field in fields:
                lines.append(
                    f"- **{field['field_name']}**: 置信度 {field['confidence']:.2%}"
                )
            lines.append("")

        indicators = analysis_result.get("indicators_found", {})
        if indicators:
            lines.append("## 场域指标\n")
            for ind_type, items in indicators.items():
                lines.append(f"- {ind_type}: {len(items)} 处")
            lines.append("")

        boundary = analysis_result.get("boundary_strength", {})
        lines.append(f"## 边界强度评估\n")
        lines.append(f"- 强度: {boundary.get('strength', 'unknown')}")
        lines.append(f"- 分数: {boundary.get('score', 0):.2f}")

        return "\n".join(lines)


def identify_field_boundaries(text: str, context: str = None) -> Dict:
    """场域边界识别入口函数"""
    identifier = FieldIdentifier()
    return identifier.identify_field_boundaries(text, context)


if __name__ == "__main__":
    # 测试
    test_text = """
    在学术场域中，大学教授和科研人员通过发表论文来竞争学术资本。
    学术期刊的编辑掌握着重要的符号资本，决定着哪些研究能够发表。
    大学的排名竞争日益激烈，各校争夺优秀的教授和学生资源。
    学术会议提供了交流和建立学术网络的平台。
    """

    result = identify_field_boundaries(test_text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
