#!/usr/bin/env python3
"""
bourdieu-field-analysis-expert - 场域动力学追踪工具
追踪场域内部的力量变化、位置变动和资本流动
"""

from typing import Dict, List, Any, Optional
from collections import defaultdict
import re
import json


# 动力学指标
DYNAMICS_INDICATORS = {
    "power_struggle": {
        "keywords": [
            "权力斗争",
            "争夺",
            "竞争",
            "冲突",
            "对抗",
            "博弈",
            "较量",
            "权力更迭",
            " dominance ",
            " struggle ",
            " conflict ",
            " competition ",
            " power ",
        ],
        "description": "权力斗争",
    },
    "position_mobility": {
        "keywords": [
            "晋升",
            "降职",
            "崛起",
            "衰落",
            "崛起",
            "失势",
            "上位",
            "下台",
            "流动",
            " movement ",
            " mobility ",
            " rise ",
            " fall ",
            " promotion ",
        ],
        "description": "位置流动",
    },
    "capital_flow": {
        "keywords": [
            "投资",
            "转移",
            "积累",
            "流失",
            "集中",
            "分散",
            "资本流动",
            "资源分配",
            " investment ",
            " transfer ",
            " accumulation ",
            " flow ",
            " distribution ",
        ],
        "description": "资本流动",
    },
    "boundary_change": {
        "keywords": [
            "扩张",
            "收缩",
            "融合",
            "分裂",
            "新兴",
            "瓦解",
            "边界变化",
            " expansion ",
            " contraction ",
            " fusion ",
            " boundary ",
        ],
        "description": "边界变化",
    },
    "rule_emergence": {
        "keywords": [
            "新规则",
            "规范",
            "制度变革",
            "惯例形成",
            "潜规则",
            " new rules ",
            " norm ",
            " institution ",
            " regulation ",
        ],
        "description": "规则形成",
    },
}


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
        """分析各时间点的动力学特征"""
        results = []

        for i, text in enumerate(texts):
            period_name = (
                time_periods[i]
                if time_periods and i < len(time_periods)
                else f"时期{i + 1}"
            )

            # 识别动力学指标
            indicators = {}
            for dyn_type, data in DYNAMICS_INDICATORS.items():
                keywords = data.get("keywords", [])
                count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)
                indicators[dyn_type] = count

            # 识别主导力量
            dominant_forces = self._identify_dominant_forces(text)

            # 识别新兴行动者
            emerging_actors = self._identify_emerging_actors(text)

            results.append(
                {
                    "period": period_name,
                    "period_index": i,
                    "indicators": indicators,
                    "dominant_forces": dominant_forces,
                    "emerging_actors": emerging_actors,
                    "intensity": self._calculate_dynamics_intensity(indicators),
                }
            )

        return results

    def _identify_dominant_forces(self, text: str) -> List[Dict]:
        """识别主导力量"""
        forces = []

        force_patterns = [
            (["权威", "权威性", "权力中心"], "authority"),
            (["资本", "资金", "财富"], "economic_capital"),
            (["知识", " expertise ", "专业"], "cultural_capital"),
            (["人脉", " network ", "关系"], "social_capital"),
            (["声望", " reputation ", "名望"], "symbolic_capital"),
        ]

        for keywords, force_type in force_patterns:
            count = sum(len(re.findall(kw, text, re.IGNORECASE)) for kw in keywords)
            if count > 0:
                forces.append(
                    {
                        "type": force_type,
                        "strength": min(1.0, count / 5),
                        "evidence_count": count,
                    }
                )

        # 按强度排序
        forces.sort(key=lambda x: x["strength"], reverse=True)
        return forces[:5]

    def _identify_emerging_actors(self, text: str) -> List[str]:
        """识别新兴行动者"""
        emerging_indicators = [
            "新兴",
            "崛起",
            " new ",
            " emerging ",
            " newcomer ",
            " newcomer",
            " new actor",
            " newly ",
        ]

        actors = []
        for indicator in emerging_indicators:
            matches = re.findall(r"([^,\s]{2,6})(?:新|新兴|崛起)", text)
            actors.extend(matches)

        return list(set(actors))[:5]

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
        """从文本中提取行动者力量"""
        forces = {}

        for actor in actors:
            # 基于关键词计算力量
            power_indicators = [
                "领导",
                " control ",
                " dominant ",
                " authority ",
                "决策",
                "决定",
            ]

            count = sum(
                len(re.findall(f"{actor}.{{0,10}}{kw}", text))
                for kw in power_indicators
            )
            count += sum(
                len(re.findall(f"{kw}.{{0,10}}{actor}", text))
                for kw in power_indicators
            )

            forces[actor] = min(1.0, count / 3)

        return forces

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
        """提取行动者位置（-1到1）"""
        # 支配性指标
        dominant_kw = ["支配", "控制", "领导", "主导"]
        dominated_kw = ["服从", "依附", "从属", "边缘"]

        dominant_count = sum(
            len(re.findall(f"{actor}.{{0,10}}{kw}", text)) for kw in dominant_kw
        )
        dominant_count += sum(
            len(re.findall(f"{kw}.{{0,10}}{actor}", text)) for kw in dominant_kw
        )

        dominated_count = sum(
            len(re.findall(f"{actor}.{{0,10}}{kw}", text)) for kw in dominated_kw
        )
        dominated_count += sum(
            len(re.findall(f"{kw}.{{0,10}}{actor}", text)) for kw in dominated_kw
        )

        total = dominant_count + dominated_count
        if total == 0:
            return 0.0

        return (dominant_count - dominated_count) / total

    def _identify_critical_events(
        self, texts: List[str], actors: List[str] = None
    ) -> List[Dict]:
        """识别关键事件"""
        events = []

        event_indicators = [
            (["冲突", "斗争", "controversy", "conflict"], "conflict"),
            (["联盟", "合作", " partnership ", "alliance"], "alliance"),
            (["分裂", "决裂", "break", "split"], "rupture"),
            (["改革", "变革", " reform ", "change"], "reform"),
            (["退出", "离开", " exit ", "leave"], "exit"),
            (["进入", "加入", " join ", "enter"], "entry"),
        ]

        for i, text in enumerate(texts):
            for keywords, event_type in event_indicators:
                for keyword in keywords:
                    matches = list(re.finditer(keyword, text, re.IGNORECASE))
                    if matches:
                        # 提取上下文
                        for match in matches[:2]:  # 限制数量
                            start = max(0, match.start() - 50)
                            end = min(len(text), match.end() + 50)
                            context = text[start:end]

                            events.append(
                                {
                                    "period": i,
                                    "type": event_type,
                                    "keyword": keyword,
                                    "context": f"...{context}...",
                                }
                            )

        return events[:10]  # 限制返回数量

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

        if change > 0.2:
            direction = "intensifying"
        elif change < -0.2:
            direction = "stabilizing"
        else:
            direction = "stable"

        return {
            "direction": direction,
            "intensity_change": change,
            "average_intensity": sum(intensities) / len(intensities),
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
