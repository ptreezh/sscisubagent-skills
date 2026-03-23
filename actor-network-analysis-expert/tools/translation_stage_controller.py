#!/usr/bin/env python3
"""
actor-network-analysis-expert - 转译阶段控制器
管理ANT分析的4个转译阶段：问题化、利益赋予、招募、动员
"""

from typing import Dict, List, Set, Any, Optional
from collections import defaultdict
import json
from datetime import datetime


# 转译阶段定义
TRANSLATION_STAGES = ["problematization", "attribution", "enrollment", "mobilization"]

# 每个阶段的关键词
STAGE_KEYWORDS = {
    "problematization": [
        "problem",
        "issue",
        "challenge",
        "question",
        "dilemma",
        "conflict",
        "tension",
        "contradiction",
        "obstacle",
    ],
    "attribution": [
        "interest",
        "motivation",
        "goal",
        "objective",
        "benefit",
        "value",
        "incentive",
        "resource",
        "capacity",
    ],
    "enrollment": [
        "recruit",
        "enroll",
        "involve",
        "engage",
        "align",
        "negotiate",
        "convince",
        "persuade",
        "co-opt",
    ],
    "mobilization": [
        "mobilize",
        "activate",
        "delegate",
        "represent",
        "speak",
        "act",
        "perform",
        "execute",
        "implement",
    ],
}


class TranslationStageController:
    """转译阶段控制器"""

    def __init__(self, case_id: str = None):
        """
        初始化控制器

        参数:
            case_id: 案例ID
        """
        self.case_id = case_id or "default"
        self.stages = {
            "problematization": {
                "status": "pending",
                "actors": [],
                "problems": [],
                "obligatory_passage_points": [],
                "notes": "",
            },
            "attribution": {
                "status": "pending",
                "actors": [],
                "interests": {},
                "resources": {},
                "capacities": {},
                "notes": "",
            },
            "enrollment": {
                "status": "pending",
                "actors": [],
                "roles": {},
                "negotiations": [],
                "alliances": [],
                "notes": "",
            },
            "mobilization": {
                "status": "pending",
                "actors": [],
                "representatives": {},
                "actions": [],
                "delegations": [],
                "notes": "",
            },
        }
        self.current_stage = "problematization"
        self.completed_stages = []
        self.metadata = {
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "version": "1.0",
        }

    def get_stage_status(self, stage: str) -> Dict:
        """获取指定阶段的状态"""
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
        """获取当前阶段"""
        return self.current_stage

    def get_completed_stages(self) -> List[str]:
        """获取已完成的阶段"""
        return self.completed_stages

    def get_all_stages(self) -> Dict:
        """获取所有阶段状态"""
        return {stage: self.get_stage_status(stage) for stage in TRANSLATION_STAGES}

    def add_problematization(
        self, actors: List[str], problems: List[str], opps: List[str] = None
    ) -> Dict:
        """
        添加问题化阶段内容

        参数:
            actors: 参与问题定义的关键行动者
            problems: 识别出的问题
            opps:  obligatory passage points (必经点)

        返回:
            更新结果
        """
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
        }

    def add_attribution(
        self,
        actors: List[str],
        interests: Dict[str, List],
        resources: Dict[str, List] = None,
        capacities: Dict[str, List] = None,
    ) -> Dict:
        """
        添加利益赋予阶段内容

        参数:
            actors: 被赋予利益的行动者
            interests: 利益字典 {actor: [interests]}
            resources: 资源字典 {actor: [resources]}
            capacities: 能力字典 {actor: [capacities]}

        返回:
            更新结果
        """
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
        }

    def add_enrollment(
        self,
        actors: List[str],
        roles: Dict[str, str],
        negotiations: List[Dict] = None,
        alliances: List[str] = None,
    ) -> Dict:
        """
        添加招募阶段内容

        参数:
            actors: 被招募的行动者
            roles: 角色分配字典 {actor: role}
            negotiations: 谈判记录列表
            alliances: 联盟列表

        返回:
            更新结果
        """
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
        }

    def add_mobilization(
        self,
        actors: List[str],
        representatives: Dict[str, str],
        actions: List[str] = None,
        delegations: List[Dict] = None,
    ) -> Dict:
        """
        添加动员阶段内容

        参数:
            actors: 被动员的行动者
            representatives: 代表关系字典 {actor: representative}
            actions: 行动列表
            delegations: 授权列表

        返回:
            更新结果
        """
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
        }

    def complete_stage(self, stage: str, notes: str = "") -> Dict:
        """
        完成一个阶段

        参数:
            stage: 阶段名称
            notes: 阶段完成备注

        返回:
            完成结果
        """
        if stage not in self.stages:
            return {"error": f"Unknown stage: {stage}"}

        # 检查前置阶段是否完成
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

        # 更新当前阶段
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
        }

    def validate_completeness(self) -> Dict:
        """
        验证4个阶段的完整性

        返回:
            完整性验证结果
        """
        required_stages = set(TRANSLATION_STAGES)
        completed = set(self.completed_stages)

        missing = required_stages - completed

        # 检查每个阶段的内容完整性
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
        }

    def get_translation_narrative(self) -> str:
        """
        生成转译叙事

        返回:
            完整的转译叙事文本
        """
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
                        narrative_parts.append(
                            f"**{actor}的利益**: {', '.join(interests)}"
                        )

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
        """导出当前状态"""
        return {
            "case_id": self.case_id,
            "stages": self.stages,
            "current_stage": self.current_stage,
            "completed_stages": self.completed_stages,
            "metadata": self.metadata,
        }

    def import_state(self, state: Dict):
        """导入状态"""
        self.case_id = state.get("case_id", self.case_id)
        self.stages = state.get("stages", self.stages)
        self.current_stage = state.get("current_stage", "problematization")
        self.completed_stages = state.get("completed_stages", [])
        self.metadata = state.get("metadata", self.metadata)

    def _update_timestamp(self):
        """更新时间戳"""
        self.metadata["updated_at"] = datetime.now().isoformat()


def create_translation_controller(case_id: str = None) -> TranslationStageController:
    """创建转译控制器实例"""
    return TranslationStageController(case_id)


if __name__ == "__main__":
    # 测试
    controller = TranslationStageController("test_case")

    # 添加问题化阶段
    controller.add_problemization(
        actors=["engineer", "manager", "AI_system"],
        problems=["效率低下", "成本过高", "用户体验差"],
        opps=["系统优化"],
    )

    # 完成问题化阶段
    result = controller.complete_stage("problematization")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    print("\n--- Stage Status ---")
    print(json.dumps(controller.get_all_stages(), ensure_ascii=False, indent=2))

    print("\n--- Completeness ---")
    print(json.dumps(controller.validate_completeness(), ensure_ascii=False, indent=2))
