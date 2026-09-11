#!/usr/bin/env python3
"""
bourdieu-field-analysis-expert - 场域动力学追踪工具
追踪场域内部的力量变化、位置变动和资本流动
"""

from typing import Dict, List, Any, Optional
from collections import defaultdict
import re
import json


# Bourdieu场域动力学methodology memo
# 动力学指标关键词匹配已禁用
# 场域动力判断是布迪厄场域诠释性判断，由LLM完成
FIELD_DYNAMICS_METHODOLOGY_MEMO = """【布迪厄场域动力学 - LLM专属判断】
场域动力学分析基于Bourdieu的资本转化理论和场域结构理论。
- 禁止：用关键词匹配("权力斗争"/"资本流动")判断场域动力学类型
- 正确做法：
  * 权力斗争: 分析不同资本类型之间的转化和张力
  * 位置流动: 分析行动者资本结构变化
  * 资本流动: 分析经济/文化/社会资本的转化路径
  * 边界变化: 分析场域边界的扩张/收缩/融合
  * 规则形成: 分析场域内部规范的形成和固化
- 场域动力学类型判断由LLM综合分析，不可用关键词计数自动确定
"""


# 动力学指标字典已禁用（保留占位防止引用报错）
DYNAMICS_INDICATORS = {}


class FieldDynamicsTracker:
    """场域动力学追踪器"""

    def __init__(self):
        self.timeline = []
        self.events = []
        self.force_relations = []

    def track_dynamics(
        self,
        texts: List[str],
        actors: List[str] = None,
        time_periods: List[str] = None,
    ) -> Dict:
        """
        追踪场域动力学

        参数:
            texts: 多个时间点的文本（按时间顺序）
            actors: 行动者列表（可选）
            time_periods: 时间段标签（可选）

        返回:
            动力学分析结果
        """
        # 识别各时间点的动力学特征
        dynamics_by_period = self._analyze_dynamics_by_period(texts, time_periods)

        # 追踪力量关系变化
        force_changes = self._track_force_relation_changes(texts, actors)

        # 分析位置流动
        position_mobility = self._analyze_position_mobility(texts, actors)

        # 识别关键事件
        critical_events = self._identify_critical_events(texts, actors)

        # 计算动力学趋势
        trends = self._calculate_dynamics_trends(dynamics_by_period)

        return {
            "dynamics_by_period": dynamics_by_period,
            "force_changes": force_changes,
            "position_mobility": position_mobility,
            "critical_events": critical_events,
            "trends": trends,
            "summary": self._generate_dynamics_summary(
                dynamics_by_period, force_changes, trends
            ),
        }

    def _analyze_dynamics_by_period(
        self, texts: List[str], time_periods: List[str] = None
    ) -> List[Dict]:
        """分析各时间点的动力学特征。

        ⚠️ 关键词计数已禁用，由LLM做布迪厄场域动力学诠释判断。
        """
        results = []

        for i, text in enumerate(texts):
            period_name = (
                time_periods[i]
                if time_periods and i < len(time_periods)
                else f"时期{i + 1}"
            )

            results.append(
                {
                    "period": period_name,
                    "period_index": i,
                    "indicators": None,  # LLM填充
                    "dominant_forces": None,  # LLM填充
                    "emerging_actors": [],  # LLM填充
                    "intensity": None,  # LLM填充
                    "methodology_memo": FIELD_DYNAMICS_METHODOLOGY_MEMO,
                }
            )

        return results

    def _identify_dominant_forces(self, text: str) -> List[Dict]:
        """识别主导力量

        ⚠️ 场域动力类型判断由LLM基于布迪厄资本理论完成，本方法不做关键词匹配。
        返回空结构，LLM填充dominant_force_type和dynamics_pattern字段。
        """
        # 以下字段由LLM基于理论原则填充:
        # - dominant_force_type: authority/economic_capital/cultural_capital/social_capital/symbolic_capital
        # - dynamics_pattern: 场域动态模式（争夺/重组/稳定/瓦解）
        # - stability_assessment: 稳定性评估
        return {
            "identified_forces": [],      # LLM判断并填充
            "dominant_force_type": None, # LLM基于布迪厄资本理论判断
            "dynamics_pattern": None,   # LLM理论描述
            "stability_assessment": None,# LLM判断
            "methodology_memo": (
                "布迪厄场域动力判断原则：\n"
                "基于文本整体分析判断主导力量类型和动态模式，\n"
                "具体资本类型由LLM根据文本实际内容判定，不预设固定列表。"
            ),
        }

    def _identify_emerging_actors(self, text: str) -> List[str]:
        """识别新兴行动者。

        ⚠️ 关键词/regex匹配已禁用，由LLM做布迪厄场域诠释判断。
        """
        return []  # LLM填充

    def _calculate_dynamics_intensity(self, indicators: Dict) -> float:
        """计算动力学强度"""
        total = sum(indicators.values())
        # 归一化到 0-1
        return min(1.0, total / 20)

    def _track_force_relation_changes(
        self, texts: List[str], actors: List[str] = None
    ) -> List[Dict]:
        """追踪力量关系变化"""
        changes = []

        if not actors or len(texts) < 2:
            return changes

        # 分析相邻时间点之间的力量变化
        for i in range(len(texts) - 1):
            before_forces = self._extract_forces_from_text(texts[i], actors)
            after_forces = self._extract_forces_from_text(texts[i + 1], actors)

            # 计算变化
            for actor in actors:
                before_power = before_forces.get(actor, 0)
                after_power = after_forces.get(actor, 0)
                change = after_power - before_power

                if abs(change) > 0.1:  # 显著变化
                    changes.append(
                        {
                            "actor": actor,
                            "from_period": i,
                            "to_period": i + 1,
                            "power_before": before_power,
                            "power_after": after_power,
                            "change": change,
                            "direction": "rising" if change > 0 else "declining",
                        }
                    )

        return changes

    def _extract_forces_from_text(
        self, text: str, actors: List[str]
    ) -> Dict[str, float]:
        """从文本中提取行动者力量。

        ⚠️ 关键词计数已禁用，由LLM做布迪厄场域诠释判断。
        """
        return {actor: None for actor in actors}  # LLM填充

    def _analyze_position_mobility(
        self, texts: List[str], actors: List[str] = None
    ) -> Dict:
        """分析位置流动"""
        mobility = {
            "total_movements": 0,
            "upward": [],
            "downward": [],
            "stable": [],
        }

        if not actors or len(texts) < 2:
            return mobility

        # 分析每个行动者的流动
        for actor in actors:
            positions = []
            for text in texts:
                pos = self._extract_position_from_text(text, actor)
                positions.append(pos)

            # 计算净流动
            if len(positions) >= 2:
                first_pos = positions[0]
                last_pos = positions[-1]
                net_change = last_pos - first_pos

                mobility["total_movements"] += 1

                if net_change > 0.2:
                    mobility["upward"].append(
                        {"actor": actor, "change": net_change, "positions": positions}
                    )
                elif net_change < -0.2:
                    mobility["downward"].append(
                        {"actor": actor, "change": net_change, "positions": positions}
                    )
                else:
                    mobility["stable"].append({"actor": actor, "positions": positions})

        return mobility

    def _extract_position_from_text(self, text: str, actor: str) -> float:
        """提取行动者位置（-1到1）。

        ⚠️ 关键词计数已禁用，由LLM做布迪厄场域诠释判断。
        """
        return None  # LLM填充

    def _identify_critical_events(
        self, texts: List[str], actors: List[str] = None
    ) -> List[Dict]:
        """识别关键事件。

        ⚠️ 关键词匹配已禁用，由LLM做布迪厄场域动力学诠释判断。
        """
        # 硬编码关键词判断已禁用，返回空结构由LLM填充
        return []  # LLM填充: [{period, type, actors, reasoning, context}]

    def _calculate_dynamics_trends(self, dynamics_by_period: List[Dict]) -> Dict:
        """计算动力学趋势"""
        if len(dynamics_by_period) < 2:
            return {"trend": "insufficient_data", "direction": "unknown"}

        intensities = [d.get("intensity", 0) for d in dynamics_by_period]

        # 判断趋势方向
        first_half = sum(intensities[: len(intensities) // 2]) / (len(intensities) // 2)
        second_half = sum(intensities[len(intensities) // 2 :]) / (
            len(intensities) - len(intensities) // 2
        )

        change = second_half - first_half

        # 硬编码阈值(0.2)分支已禁用，由LLM做布迪厄场域动力学诠释判断
        return {
            "direction": None,  # LLM填充: intensifying/stabilizing/stable
            "intensity_change": change,
            "average_intensity": sum(intensities) / len(intensities) if intensities else None,
            "methodology_memo": "0.2阈值仅为定量信号，动力学方向由LLM基于布迪厄场域理论判断",
        }

    def _generate_dynamics_summary(
        self,
        dynamics_by_period: List[Dict],
        force_changes: List[Dict],
        trends: Dict,
    ) -> str:
        """生成动力学总结"""
        lines = []

        # 总体趋势
        lines.append("## 场域动力学总览\n")
        trend_names = {
            "intensifying": "趋于激烈",
            "stabilizing": "趋于稳定",
            "stable": "保持稳定",
            "insufficient_data": "数据不足",
        }
        lines.append(
            f"- 动力学趋势: {trend_names.get(trends.get('direction', 'unknown'), '未知')}"
        )
        lines.append(f"- 平均强度: {trends.get('average_intensity', 0):.2%}")
        lines.append("")

        # 关键变化
        if force_changes:
            lines.append("## 力量变化\n")
            rising = [c for c in force_changes if c.get("direction") == "rising"]
            declining = [c for c in force_changes if c.get("direction") == "declining"]

            if rising:
                lines.append("### 上升力量\n")
                for c in rising[:3]:
                    lines.append(f"- {c.get('actor')}: +{c.get('change', 0):.2f}")

            if declining:
                lines.append("### 下降力量\n")
                for c in declining[:3]:
                    lines.append(f"- {c.get('actor')}: {c.get('change', 0):.2f}")

        return "\n".join(lines)


def track_dynamics(
    texts: List[str], actors: List[str] = None, time_periods: List[str] = None
) -> Dict:
    """场域动力学追踪入口函数"""
    tracker = FieldDynamicsTracker()
    return tracker.track_dynamics(texts, actors, time_periods)


if __name__ == "__main__":
    # 测试
    test_texts = [
        """
        2010年，王教授主导学术场域，拥有绝对权力。
        张博士是他的学生，听从导师安排。
        学术评价标准由王教授一人决定。
        """,
        """
        2015年，王教授权力受到挑战。
        新兴学者李教授崛起，带来新理论。
        张博士开始独立研究，逐渐获得影响力。
        """,
        """
        2020年，场域发生剧烈变动。
        资本流向新兴领域，传统权威衰落。
        年轻学者形成新联盟。
        """,
    ]

    actors = ["王教授", "张博士", "李教授"]
    periods = ["2010", "2015", "2020"]

    result = track_dynamics(test_texts, actors, periods)
    print(json.dumps(result, ensure_ascii=False, indent=2))
