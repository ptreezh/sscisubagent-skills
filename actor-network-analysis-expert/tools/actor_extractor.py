#!/usr/bin/env python3
"""
actor-network-analysis-expert - 行动者提取工具
从异质性数据源(访谈、文档、观察记录、artifacts)中提取行动者
严格遵循ANT的对称性原则 - 不预设人类/非人二分法
"""

from typing import Dict, List, Set, Any, Tuple, Optional
from collections import defaultdict
import re
import json


# 行动者类别模式 - 英文
ACTOR_PATTERNS_EN = {
    "human_individual": [
        r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b",
        r"\b(the (manager|engineer|doctor|researcher|user|customer|patient|worker|director|chief|lead))\b",
    ],
    "organization": [
        r"\b([A-Z][A-Z][a-z]+ (Corporation|Company|Inc|Ltd|Agency|Department|Institute|University|Hospital))\b",
    ],
    "technology": [
        r"\b(the (software|hardware|system|platform|algorithm|AI|robot|database|network|server|app|tool))\b",
    ],
    "artifact": [
        r"\b(the (document|protocol|standard|policy|law|regulation|contract|agreement))\b",
    ],
    "concept": [
        r"\b(the (idea|theory|model|framework|paradigm|method|approach|strategy))\b",
    ],
}

# 行动者类别模式 - 中文
ACTOR_PATTERNS_CN = {
    "human_chinese": [
        r"(局长|处长|科长|工程师|医生|护士|研究员|教授|校长|院长|主任|经理|总理|省长|市长|县长|书记|主席|董事长|CEO|总监|主管|市民|用户|客户|患者|工作人员|技术员|管理员)",
    ],
    "organization_chinese": [
        r"(交通局|公安局|城管局|财政局|大数据局|教育局|卫生局|环保局|工商局|税务局|法院|检察院|政府|市委|省厅|市局|管理局|热线|部门|单位|医院|学校|大学|公司|企业|集团)",
        r"(华为|阿里|腾讯|百度|字节|微软|谷歌|亚马逊|西门子|IBM|供应商|运营商)",
    ],
    "technology_chinese": [
        r"(传感器|摄像头|雷达|GPS|北斗|物联网|互联网|5G|光纤|WiFi|电脑|手机|设备|终端|系统|平台|软件|硬件|算法|数据库|服务器|云端|APP|应用程序|人工智能|机器学习|深度学习|模型|技术)",
        r"(交通系统|指挥中心|数据处理中心|信号灯|感应设备|监测设备|预测系统|大屏|工作平台|视频|后台)",
    ],
    "artifact_chinese": [
        r"(数据|信息|政策|法规|标准|规范|制度|协议|合同|证书|执照|牌照|投诉|建议|路况|车流量|历史数据|天气数据|活动信息)",
    ],
    "concept_chinese": [
        r"(交通拥堵|城市管理|智慧城市|数字化|智能化|现代化|大数据|人工智能|互联网+|机器学习|预测|优化|自动|人工|实时|动态)",
    ],
}


class ActorExtractor:
    """行动者提取器"""

    def __init__(self):
        self.extracted_actors = set()
        self.actor_types = {}
        self.actor_relationships = []
        self.actor_mentions = defaultdict(int)

    def extract_from_text(self, text: str, source_type: str = "document") -> Dict:
        actors_found = set()

        # 使用英文模式提取
        for actor_type, patterns in ACTOR_PATTERNS_EN.items():
            for pattern in patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        actor = " ".join(match) if len(match) > 1 else match[0]
                    else:
                        actor = match
                    actor = self._normalize_actor(actor)
                    if actor and len(actor) > 2:
                        actors_found.add(actor)
                        self.actor_types[actor] = actor_type

        # 使用中文模式提取
        for actor_type, patterns in ACTOR_PATTERNS_CN.items():
            for pattern in patterns:
                matches = re.findall(pattern, text)
                for match in matches:
                    if isinstance(match, tuple):
                        actor = " ".join(match) if len(match) > 1 else match[0]
                    else:
                        actor = match
                    actor = self._normalize_actor(actor)
                    if actor and len(actor) > 1:
                        actors_found.add(actor)
                        self.actor_types[actor] = actor_type

        # 记录提取结果
        for actor in actors_found:
            self.extracted_actors.add(actor)
            self.actor_mentions[actor] += 1

        return {
            "source_type": source_type,
            "actors_found": list(actors_found),
            "actor_count": len(actors_found),
            "relationships_found": [],
        }

    def extract_from_interview(self, interview_text: str) -> Dict:
        return self.extract_from_text(interview_text, "interview")

    def extract_from_document(self, document_text: str) -> Dict:
        return self.extract_from_text(document_text, "document")

    def _normalize_actor(self, actor: str) -> str:
        actor = " ".join(actor.split())
        actor = actor.strip(".,;:!?()[]{}\"'")
        return actor

    def classify_actors(self) -> Dict:
        categories = {
            "human": [],
            "organization": [],
            "technology": [],
            "artifact": [],
            "concept": [],
            "unclassified": [],
        }

        for actor, actor_type in self.actor_types.items():
            if "human" in actor_type:
                categories["human"].append(actor)
            elif "organization" in actor_type:
                categories["organization"].append(actor)
            elif "technology" in actor_type:
                categories["technology"].append(actor)
            elif "artifact" in actor_type:
                categories["artifact"].append(actor)
            elif "concept" in actor_type:
                categories["concept"].append(actor)
            else:
                categories["unclassified"].append(actor)

        human_actors = categories["human"]
        nonhuman_actors = (
            categories["organization"]
            + categories["technology"]
            + categories["artifact"]
            + categories["concept"]
        )

        total = len(self.extracted_actors) if self.extracted_actors else 1

        return {
            "categories": {k: v for k, v in categories.items() if v},
            "total_actors": len(self.extracted_actors),
            "human_count": len(human_actors),
            "nonhuman_count": len(nonhuman_actors),
            "human_ratio": len(human_actors) / total,
            "nonhuman_ratio": len(nonhuman_actors) / total,
            "symmetry_warning": len(nonhuman_actors) / total < 0.3,
        }

    def get_top_actors(self, n: int = 10) -> List[Tuple[str, int]]:
        sorted_actors = sorted(
            self.actor_mentions.items(), key=lambda x: x[1], reverse=True
        )
        return sorted_actors[:n]

    def get_summary(self) -> Dict:
        return {
            "total_actors": len(self.extracted_actors),
            "actor_list": list(self.extracted_actors),
            "actor_types": dict(self.actor_types),
            "relationships": self.actor_relationships,
            "top_actors": self.get_top_actors(10),
            "classification": self.classify_actors(),
        }

    def reset(self):
        self.extracted_actors = set()
        self.actor_types = {}
        self.actor_relationships = []
        self.actor_mentions = defaultdict(int)


def create_extractor() -> ActorExtractor:
    return ActorExtractor()


if __name__ == "__main__":
    extractor = ActorExtractor()

    with open(
        "../test_data/case_01_smart_city/interview_01.txt", "r", encoding="utf-8"
    ) as f:
        text = f.read()

    result = extractor.extract_from_interview(text)
    print("=== Actor Extraction Results ===")
    print(f"Total actors found: {result['actor_count']}")
    print(f"Actors: {result['actors_found'][:15]}")
    print()
    classification = extractor.classify_actors()
    print("=== Classification ===")
    print(f"Human: {classification['human_count']}")
    print(f"Nonhuman: {classification['nonhuman_count']}")
    print(f"Nonhuman ratio: {classification['nonhuman_ratio']:.2%}")
    print(f"Symmetry warning: {classification['symmetry_warning']}")
    print()
    print(
        "Categories:",
        {k: len(v) for k, v in classification["categories"].items() if len(v) > 0},
    )
