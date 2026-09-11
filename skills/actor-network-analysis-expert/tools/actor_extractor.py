#!/usr/bin/env python3
"""
actor-network-analysis-expert - 行动者提取工具
从异质性数据源（访谈、文档、观察记录、artifacts）中提取行动者
严格遵循ANT的对称性原则 - 不预设人类/非人二分法

【方法论说明】
本工具不包含任何硬编码正则模式匹配。所有行动者类型判断由LLM根据理论备忘录完成。
工具仅负责：数据清洗、空结构返回、方法论引导。
"""

from typing import Dict, List, Set, Any, TypedDict
from collections import defaultdict
import json


# ---------------------------------------------------------------------------
# ANT行动者识别理论备忘录（供LLM判断时参考）
# ---------------------------------------------------------------------------
ACTOR_NETWORK_THEORY_MEMO = """
=== ANT行动者（Actor）识别理论备忘录 ===

【ANT核心原则：行动者网络理论（Actor-Network Theory）】

1. 行动者（Actor/Actant）定义:
   - 任何通过行动产生差异的东西都是行动者
   - 不预设人类vs非人类的二元划分
   - 行动者可以是人、组织、技术、文本、理念、动物……
   - 关键标准：是否在网络中"行动"（act）？

2. 行动者网络理论（ANT）的对称性原则:
   - 方法论对称性：人类和非人类用相同的概念工具分析
   - 不给人类行动以优先地位
   - 技术、文本、制度同等地参与社会

【行动者类型分类框架】（供LLM分类参考）

人类行动者（Human Actors）:
- 个人：研究者、工程师、用户、管理者……
- 群体：团队、部门、社区……
- 分析要点：
  * 谁在说话？其社会角色是什么？
  * 其立场和利益是什么？
  * 如何与其他行动者互动？

组织行动者（Organizational Actors）:
- 企业、政府机构、非营利组织……
- 分析要点：
  * 组织的结构和利益是什么？
  * 谁代表组织行动？

技术行动者（Non-human / Material Actors）:
- 硬件：传感器、机器人、终端设备……
- 软件：算法、平台、数据库、AI系统……
- 分析要点（关键！）：
    这些技术是被动工具，还是主动参与者？
    技术的"代理"（agency）如何体现？
    技术如何塑造人类行为？

制品行动者（Artifact / Textual Actors）:
- 制度性文本：法律、政策、合同、标准……
- 知识性文本：报告、论文、数据、模型……
- 分析要点：
    文本如何被引用？是否有约束力？
    谁有权解释/修改该文本？

概念行动者（Conceptual / Ideational Actors）:
- 意识形态： neoliberalism, sustainability, innovation……
- 框架：smart city, circular economy, AI ethics……
- 分析要点：
    概念如何被使用？为谁的利益服务？
    概念如何连接不同的行动者？

【行动者识别步骤】
1. 列出文本中所有被指称（mentioned）的实体
2. 筛选：在网络构建中发挥作用的实体（不只是被提及）
3. 分类：按上述类型框架分类
4. 分析关系：行动者之间如何连接？

【对称性分析要求】
- 检查人类vs非人类的比例
- 若非人类行动者少于30%，需反思：是否遗漏了技术的能动性？
- 追问：哪些非人类行动者实际上塑造了人类决策？

【分析方法论】
- 不能仅凭实体名称判断行动者类型（公司名≠组织）
- 关注行动者如何被赋予角色（enrollment）
- 分析行动者的"代言人"（spokesperson）：谁代表谁说话？
- 网络是否稳定取决于转译（translation）是否成功
"""


class ActorEntry(TypedDict, total=False):
    name: str | None           # 行动者名称（LLM提取）
    type: str | None           # 行动者类型（LLM判断）
    type_confidence: float | None  # 判断置信度（LLM填充）
    evidence: List[str]       # 证据片段（LLM填充）
    notes: str                 # 备注


class ActorCategories(TypedDict, total=False):
    human: List[Dict]
    organization: List[Dict]
    technology: List[Dict]
    artifact: List[Dict]
    concept: List[Dict]
    unclassified: List[Dict]


class ActorExtractionResult(TypedDict):
    source_type: str
    actors_found: List[Dict]        # 行动者列表（LLM填充）
    actor_count: int
    categories: ActorCategories     # 分类结果（LLM填充）
    human_count: int | None
    nonhuman_count: int | None
    human_ratio: float | None
    nonhuman_ratio: float | None
    symmetry_warning: bool | None   # 对称性警告（LLM判断）
    relationships_found: List[Dict]  # 关系列表（LLM填充）
    theory_memo: str                # 方法论备忘录
    raw_data_for_llm: str           # 供LLM分析的原始文本


class ActorExtractor:
    """行动者提取器（无关键词匹配版）

    所有行动者识别和类型判断由调用方/LLM完成。
    """

    def __init__(self):
        self.extracted_actors: Set[str] = set()
        self.actor_types: Dict[str, str] = {}
        self.actor_relationships: List[Dict] = []
        self.actor_mentions: Dict[str, int] = defaultdict(int)

    def extract_from_text(self, text: str, source_type: str = "document") -> Dict:
        """
        从文本中提取行动者（返回空结构供LLM填充）

        参数:
            text: 原始文本
            source_type: 来源类型

        返回:
            含空结构的行动者提取结果，需LLM根据 theory_memo 填充
        """
        result: Dict = {
            "source_type": source_type,
            "actors_found": [],       # 需LLM填充
            "actor_count": 0,
            "categories": {
                "human": [],
                "organization": [],
                "technology": [],
                "artifact": [],
                "concept": [],
                "unclassified": [],
            },
            "human_count": None,
            "nonhuman_count": None,
            "human_ratio": None,
            "nonhuman_ratio": None,
            "symmetry_warning": None,
            "relationships_found": [],
            "theory_memo": ACTOR_NETWORK_THEORY_MEMO.strip(),
            "raw_data_for_llm": text[:5000],
        }
        return result

    def extract_from_interview(self, interview_text: str) -> Dict:
        """从访谈文本中提取行动者"""
        return self.extract_from_text(interview_text, "interview")

    def extract_from_document(self, document_text: str) -> Dict:
        """从文档中提取行动者"""
        return self.extract_from_text(document_text, "document")

    def classify_actors(self, actors: List[Dict]) -> Dict:
        """
        分类行动者（返回空结构供LLM填充）

        参数:
            actors: 行动者列表

        返回:
            含空结构的分类结果，需LLM根据 theory_memo 判断类型
        """
        result: Dict = {
            "categories": {
                "human": [],
                "organization": [],
                "technology": [],
                "artifact": [],
                "concept": [],
                "unclassified": [],
            },
            "total_actors": len(actors),
            "human_count": None,
            "nonhuman_count": None,
            "human_ratio": None,
            "nonhuman_ratio": None,
            "symmetry_warning": None,
            "theory_memo": ACTOR_NETWORK_THEORY_MEMO.strip(),
        }
        return result

    def get_top_actors(self, n: int = 10) -> List[Any]:
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
            "theory_memo": ACTOR_NETWORK_THEORY_MEMO.strip(),
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
    test_text = """
    工程师李明负责系统设计，交通局张处长主持项目推进会议。
    华为公司提供技术支持，智慧城市平台整合了传感器和AI算法。
    政策文件规定数据共享标准，用户通过APP提交出行建议。
    """
    result = extractor.extract_from_text(test_text, "document")
    print("=== 返回结构（需LLM填充） ===")
    print(f"actors_found: {result['actors_found']}")
    print(f"actor_count: {result['actor_count']}")
    print(f"symmetry_warning: {result['symmetry_warning']}")
    print("\n理论备忘录（前300字）:")
    print(result["theory_memo"][:300])
