#!/usr/bin/env python3
"""
actor-network-analysis-expert - 转译阶段控制器
管理ANT分析的四个转译阶段：问题化、利益赋予、招募、动员
基于Callon(1986)《转译社会学》

【方法论说明】
本工具不包含任何硬编码关键词匹配。所有阶段判断由LLM根据理论备忘录完成。
工具仅负责：状态管理、空结构返回、方法论引导。
"""

from typing import Dict, List, Set, Any, Optional
from collections import defaultdict
import json
from datetime import datetime


# ---------------------------------------------------------------------------
# ANT转译过程理论备忘录（供LLM判断时参考）
# ---------------------------------------------------------------------------
TRANSLATION_THEORY_MEMO = """
=== ANT转译过程（Translation）理论备忘录 ===

【转译的核心概念】
转译（Translation）：行动者网络中不同利益、目标、角色被连接和重新定义的过程。
是ANT的核心分析工具，描述权力如何通过协商和代表关系建立。

【拉图的转译四阶段】（Callon, 1986）

阶段1：问题化（Problematization）
- 核心问题："谁是这个网络的关键行动者？"
- 关键行动者定义问题，将自己设置为"必经点"（Obligatory Passage Point, OPP）
- 其他行动者被"问题化"——他们的利益被定义为依赖于解决该问题
- 分析要点：
    * 谁在提出问题？其立场是什么？
    * 问题如何被定义？谁被包含/排除在问题定义之外？
    * 什么是"必经点"？谁声称自己处于该位置？
    * 不同行动者如何理解同一问题？

阶段2：利益赋予（Attribution of Interests）
- 核心问题："各行动者的利益是什么？如何被重新定义？"
- 将其他行动者的问题转化为利益，建立"代言人"关系
- 关键机制：interessement（利益赋予）——让其他行动者接受自己的角色定义
- 分析要点：
    * 哪些行动者的利益被强调？哪些被忽视？
    * 利益是如何被表述的？谁有权定义利益？
    * 资源、能力、限制条件是什么？
    * 是否存在利益冲突？如何处理？

阶段3：招募（Enrollment）
- 核心问题："谁被说服接受特定角色？"
- 通过谈判、说服、co-optation（拉拢）等手段，将其他行动者纳入网络
- 成功招募 = 其他行动者接受被赋予的角色
- 分析要点：
    * 招募策略是什么？说服/谈判/强制/交换？
    * 角色分配如何？是否有角色冲突？
    * 联盟如何建立？谁与谁结盟？
    * 是否有抵抗或异议？如何处理？

阶段4：动员（Mobilization）
- 核心问题："被招募的行动者是否真正代表网络行动？"
- 确保被招募的行动者能够代表更广泛的行动者群体行动
- 关键机制：representation（代表）和delegation（授权）
- 分析要点：
    * 谁是 spokesperson（代言人）？代表谁？
    * 代表关系是否稳定？是否被质疑？
    * 行动是否真正代表网络整体？
    * 是否有异议者（dissident）？如何处理？

阶段5（可选）：异议消除（Disarmament of Rivals）——处理反对派
- 将反对者纳入网络或削弱其影响力
- 分析要点：
    * 异议来自哪里？
    * 异议是被吸纳还是被压制？

【转译成功的标准】
- 问题定义被各方接受
- 利益分配达成某种平衡
- 角色分配被接受
- 代表关系稳定
- 网络具有一定的稳定性

【分析方法论】
- 四阶段是分析性框架，不必线性经过
- 实际过程可能有循环、倒退、分叉
- 每个阶段都需要检验：是否真正"成功"？
- 注意"黑箱化"（black-boxing）：成功转译后，网络变得稳定，问题消失
- 关注失败点：转译在哪个环节出现问题？为什么？
"""


# 转译阶段定义
TRANSLATION_STAGES = ["problematization", "attribution", "enrollment", "mobilization"]


class StageActor(TypedDict, total=False):
    name: str | None
    role: str | None          # 该行动者在该阶段的角色（LLM填充）
    interests: List[str]      # 利益（LLM填充）
    notes: str                 # 备注


class TranslationStage(TypedDict):
    status: str               # pending / in_progress / completed
    actors: List[Dict]        # 行动者列表（LLM填充）
    problems: List[str]       # 问题列表（LLM填充）
    interests: Dict[str, List[str]]  # 利益字典（LLM填充）
    roles: Dict[str, str]     # 角色分配（LLM填充）
    representatives: Dict[str, str]   # 代言关系（LLM填充）
    obligatory_passage_points: List[str]  # 必经点（LLM填充）
    alliances: List[str]      # 联盟（LLM填充）
    negotiations: List[Dict]  # 谈判记录（LLM填充）
    actions: List[str]        # 行动列表（LLM填充）
    delegations: List[Dict]   # 授权列表（LLM填充）
    notes: str


class TranslationStageController:
    """转译阶段控制器（无关键词匹配版）

    所有阶段内容由调用方/LLM根据 theory_memo 填充。
    """

    def __init__(self, case_id: str = None):
        self.case_id = case_id or "default"
        self.stages: Dict[str, Dict] = {
            "problematization": {
                "status": "pending",
                "actors": [],          # 需LLM填充
                "problems": [],       # 需LLM填充
                "obligatory_passage_points": [],  # 需LLM填充
                "notes": "",
            },
            "attribution": {
                "status": "pending",
                "actors": [],          # 需LLM填充
                "interests": {},       # 需LLM填充
                "resources": {},       # 需LLM填充
                "capacities": {},     # 需LLM填充
                "notes": "",
            },
            "enrollment": {
                "status": "pending",
                "actors": [],          # 需LLM填充
                "roles": {},          # 需LLM填充
                "negotiations": [],   # 需LLM填充
                "alliances": [],      # 需LLM填充
                "notes": "",
            },
            "mobilization": {
                "status": "pending",
                "actors": [],          # 需LLM填充
                "representatives": {},  # 需LLM填充
                "actions": [],        # 需LLM填充
                "delegations": [],    # 需LLM填充
                "notes": "",
            },
        }
        self.current_stage = "problematization"
        self.completed_stages: List[str] = []
        self.metadata: Dict = {
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "version": "2.0",  # 无关键词版本
        }
        # 附加方法论备忘录，供LLM参考
        self.theory_memo = TRANSLATION_THEORY_MEMO.strip()

    def get_stage_status(self, stage: str) -> Dict:
        if stage not in self.stages:
            return {"error": f"Unknown stage: {stage}"}
        stage_data = self.stages[stage]
        return {
            "stage": stage,
            "status": stage_data["status"],
            "actor_count": len(stage_data["actors"]),
            "is_complete": stage_data["status"] == "completed",
        }

    def get_current_stage(self) -> str:
        return self.current_stage

    def get_completed_stages(self) -> List[str]:
        return self.completed_stages

    def get_all_stages(self) -> Dict:
        return {stage: self.get_stage_status(stage) for stage in TRANSLATION_STAGES}

    def add_problematization(
        self, actors: List[str], problems: List[str], opps: List[str] = None
    ) -> Dict:
        stage = self.stages["problematization"]
        stage["actors"] = list(set(stage["actors"] + actors))
        stage["problems"] = list(set(stage["problems"] + problems))
        if opps:
            stage["obligatory_passage_points"] = list(
                set(stage["obligatory_passage_points"] + opps)
            )
        self._update_timestamp()
        return {
            "stage": "problematization",
            "status": "updated",
            "actors_count": len(stage["actors"]),
            "problems_count": len(stage["problems"]),
            "theory_memo": self.theory_memo,  # 引导LLM
        }

    def add_attribution(
        self,
        actors: List[str],
        interests: Dict[str, List],
        resources: Dict[str, List] = None,
        capacities: Dict[str, List] = None,
    ) -> Dict:
        stage = self.stages["attribution"]
        stage["actors"] = list(set(stage["actors"] + actors))
        for actor, actor_interests in interests.items():
            if actor not in stage["interests"]:
                stage["interests"][actor] = []
            stage["interests"][actor] = list(
                set(stage["interests"][actor] + actor_interests)
            )
        if resources:
            for actor, actor_resources in resources.items():
                if actor not in stage["resources"]:
                    stage["resources"][actor] = []
                stage["resources"][actor] = list(
                    set(stage["resources"][actor] + actor_resources)
                )
        if capacities:
            for actor, actor_capacities in capacities.items():
                if actor not in stage["capacities"]:
                    stage["capacities"][actor] = []
                stage["capacities"][actor] = list(
                    set(stage["capacities"][actor] + actor_capacities)
                )
        self._update_timestamp()
        return {
            "stage": "attribution",
            "status": "updated",
            "actors_count": len(stage["actors"]),
            "interests_count": sum(len(v) for v in stage["interests"].values()),
            "theory_memo": self.theory_memo,
        }

    def add_enrollment(
        self,
        actors: List[str],
        roles: Dict[str, str],
        negotiations: List[Dict] = None,
        alliances: List[str] = None,
    ) -> Dict:
        stage = self.stages["enrollment"]
        stage["actors"] = list(set(stage["actors"] + actors))
        stage["roles"].update(roles)
        if negotiations:
            stage["negotiations"].extend(negotiations)
        if alliances:
            stage["alliances"] = list(set(stage["alliances"] + alliances))
        self._update_timestamp()
        return {
            "stage": "enrollment",
            "status": "updated",
            "actors_count": len(stage["actors"]),
            "roles_assigned": len(stage["roles"]),
            "theory_memo": self.theory_memo,
        }

    def add_mobilization(
        self,
        actors: List[str],
        representatives: Dict[str, str],
        actions: List[str] = None,
        delegations: List[Dict] = None,
    ) -> Dict:
        stage = self.stages["mobilization"]
        stage["actors"] = list(set(stage["actors"] + actors))
        stage["representatives"].update(representatives)
        if actions:
            stage["actions"].extend(actions)
        if delegations:
            stage["delegations"].extend(delegations)
        self._update_timestamp()
        return {
            "stage": "mobilization",
            "status": "updated",
            "actors_count": len(stage["actors"]),
            "representatives_count": len(stage["representatives"]),
            "theory_memo": self.theory_memo,
        }

    def complete_stage(self, stage: str, notes: str = "") -> Dict:
        if stage not in self.stages:
            return {"error": f"Unknown stage: {stage}"}
        stage_index = TRANSLATION_STAGES.index(stage)
        if stage_index > 0:
            prev_stage = TRANSLATION_STAGES[stage_index - 1]
            if prev_stage not in self.completed_stages:
                return {
                    "error": f"Cannot complete {stage} before completing {prev_stage}",
                    "required": prev_stage,
                }
        self.stages[stage]["status"] = "completed"
        if notes:
            self.stages[stage]["notes"] = notes
        if stage not in self.completed_stages:
            self.completed_stages.append(stage)
        if stage_index + 1 < len(TRANSLATION_STAGES):
            self.current_stage = TRANSLATION_STAGES[stage_index + 1]
            self.stages[self.current_stage]["status"] = "in_progress"
        self._update_timestamp()
        return {
            "stage": stage,
            "status": "completed",
            "next_stage": self.current_stage
            if self.current_stage in TRANSLATION_STAGES
            else None,
            "theory_memo": self.theory_memo,
        }

    def validate_completeness(self) -> Dict:
        required_stages = set(TRANSLATION_STAGES)
        completed = set(self.completed_stages)
        missing = required_stages - completed
        stage_contents = {
            "problematization": len(self.stages["problematization"]["problems"]) > 0,
            "attribution": len(self.stages["attribution"]["interests"]) > 0,
            "enrollment": len(self.stages["enrollment"]["roles"]) > 0,
            "mobilization": len(self.stages["mobilization"]["representatives"]) > 0,
        }
        complete_count = sum(stage_contents.values())
        completeness_score = (complete_count / 4) * 100
        return {
            "is_complete": len(missing) == 0 and complete_count == 4,
            "completed_stages": self.completed_stages,
            "missing_stages": list(missing),
            "stage_contents": stage_contents,
            "completeness_score": completeness_score,
            "status": "valid" if len(missing) == 0 else "incomplete",
            "theory_memo": self.theory_memo,
        }

    def get_translation_narrative(self) -> str:
        narrative_parts = []
        for stage_name in TRANSLATION_STAGES:
            stage = self.stages[stage_name]
            narrative_parts.append(f"\n## {stage_name.upper()}")
            if stage["actors"]:
                narrative_parts.append(f"**行动者**: {', '.join(stage['actors'])}")
            if stage_name == "problematization":
                if stage["problems"]:
                    narrative_parts.append(f"**问题**: {'; '.join(stage['problems'])}")
                if stage["obligatory_passage_points"]:
                    narrative_parts.append(
                        f"**必经点**: {', '.join(stage['obligatory_passage_points'])}"
                    )
            elif stage_name == "attribution":
                if stage["interests"]:
                    for actor, interests in stage["interests"].items():
                        narrative_parts.append(f"**{actor}的利益**: {', '.join(interests)}")
            elif stage_name == "enrollment":
                if stage["roles"]:
                    for actor, role in stage["roles"].items():
                        narrative_parts.append(f"**{actor}的角色**: {role}")
            elif stage_name == "mobilization":
                if stage["representatives"]:
                    for actor, rep in stage["representatives"].items():
                        narrative_parts.append(f"**{actor}的代表**: {rep}")
            if stage["notes"]:
                narrative_parts.append(f"**备注**: {stage['notes']}")
        return "\n".join(narrative_parts)

    def export_state(self) -> Dict:
        return {
            "case_id": self.case_id,
            "stages": self.stages,
            "current_stage": self.current_stage,
            "completed_stages": self.completed_stages,
            "metadata": self.metadata,
            "theory_memo": self.theory_memo,
        }

    def import_state(self, state: Dict):
        self.case_id = state.get("case_id", self.case_id)
        self.stages = state.get("stages", self.stages)
        self.current_stage = state.get("current_stage", "problematization")
        self.completed_stages = state.get("completed_stages", [])
        self.metadata = state.get("metadata", self.metadata)
        self.theory_memo = state.get(
            "theory_memo", TRANSLATION_THEORY_MEMO.strip()
        )

    def _update_timestamp(self):
        self.metadata["updated_at"] = datetime.now().isoformat()


def create_translation_controller(case_id: str = None) -> TranslationStageController:
    """创建转译控制器实例"""
    return TranslationStageController(case_id)


if __name__ == "__main__":
    from typing import TypedDict

    controller = TranslationStageController("test_case")

    controller.add_problematization(
        actors=["engineer", "manager", "AI_system"],
        problems=["效率低下", "成本过高", "用户体验差"],
        opps=["系统优化"],
    )

    result = controller.complete_stage("problematization")
    print("=== 状态（需LLM根据备忘录填充） ===")
    print(f"current_stage: {controller.get_current_stage()}")
    print(f"all_stages: {controller.get_all_stages()}")
    print(f"\n理论备忘录（前300字）:\n{controller.theory_memo[:300]}")
