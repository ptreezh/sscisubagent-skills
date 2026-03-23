#!/usr/bin/env python3
"""
social-network-analysis-expert - 时序网络分析工具
分析社会网络随时间的变化
"""

from typing import Dict, List, Any, Optional
import json
from collections import defaultdict


class TemporalAnalyzer:
    """时序网络分析器"""

    def __init__(self):
        self.temporal_data = []

    def analyze_temporal(
        self,
        time_series_data: List[Dict],
        time_field: str = "timestamp",
    ) -> Dict:
        """
        分析时序网络变化

        参数:
            time_series_data: 时间序列网络数据列表
            time_field: 时间字段名

        返回:
            时序分析结果
        """
        # 按时间排序
        sorted_data = self._sort_by_time(time_series_data, time_field)

        # 提取各时间点的网络
        networks = self._extract_networks(sorted_data)

        # 分析网络演变
        evolution = self._analyze_evolution(networks)

        # 计算网络指标变化
        metrics_trend = self._calculate_metrics_trend(networks)

        # 识别关键事件
        critical_events = self._identify_critical_events(networks)

        # 分析节点流动性
        node_mobility = self._analyze_node_mobility(networks)

        return {
            "num_time_points": len(networks),
            "time_range": self._get_time_range(sorted_data),
            "networks": networks,
            "evolution": evolution,
            "metrics_trend": metrics_trend,
            "critical_events": critical_events,
            "node_mobility": node_mobility,
            "summary": self._generate_summary(evolution, metrics_trend),
        }

    def _sort_by_time(self, data: List[Dict], time_field: str) -> List[Dict]:
        """按时间排序"""
        return sorted(data, key=lambda x: x.get(time_field, ""))

    def _extract_networks(self, data: List[Dict]) -> List[Dict]:
        """提取各时间点的网络"""
        networks = []

        for item in data:
            # 解析边
            edges = item.get("edges", [])
            nodes = set()

            for edge in edges:
                if isinstance(edge, dict):
                    nodes.add(edge.get("source", edge.get("from", "")))
                    nodes.add(edge.get("target", edge.get("to", "")))
                elif isinstance(edge, (list, tuple)):
                    nodes.add(str(edge[0]))
                    nodes.add(str(edge[1]))

            networks.append(
                {
                    "time": item.get("timestamp", item.get("time", "")),
                    "nodes": list(nodes),
                    "edges": edges,
                    "num_nodes": len(nodes),
                    "num_edges": len(edges),
                }
            )

        return networks

    def _analyze_evolution(self, networks: List[Dict]) -> Dict:
        """分析网络演变"""
        if len(networks) < 2:
            return {"trend": "insufficient_data"}

        # 计算网络规模变化
        node_counts = [n.get("num_nodes", 0) for n in networks]
        edge_counts = [n.get("num_edges", 0) for n in networks]

        # 节点变化趋势
        node_trend = "stable"
        if node_counts[-1] > node_counts[0] * 1.2:
            node_trend = "growing"
        elif node_counts[-1] < node_counts[0] * 0.8:
            node_trend = "shrinking"

        # 边变化趋势
        edge_trend = "stable"
        if edge_counts[-1] > edge_counts[0] * 1.2:
            edge_trend = "growing"
        elif edge_counts[-1] < edge_counts[0] * 0.8:
            edge_trend = "shrinking"

        # 计算密度变化
        densities = []
        for net in networks:
            n = net.get("num_nodes", 0)
            e = net.get("num_edges", 0)
            if n > 1:
                density = (2 * e) / (n * (n - 1))
            else:
                density = 0
            densities.append(density)

        density_trend = "stable"
        if len(densities) >= 2:
            if densities[-1] > densities[0] * 1.2:
                density_trend = "increasing"
            elif densities[-1] < densities[0] * 0.8:
                density_trend = "decreasing"

        return {
            "node_trend": node_trend,
            "edge_trend": edge_trend,
            "density_trend": density_trend,
            "node_counts": node_counts,
            "edge_counts": edge_counts,
            "densities": densities,
        }

    def _calculate_metrics_trend(self, networks: List[Dict]) -> Dict:
        """计算网络指标变化趋势"""
        trends = {}

        # 计算平均度
        avg_degrees = []
        for net in networks:
            n = net.get("num_nodes", 0)
            e = net.get("num_edges", 0)
            if n > 0:
                avg_degrees.append(2 * e / n)
            else:
                avg_degrees.append(0)

        if avg_degrees:
            trends["avg_degree"] = {
                "values": avg_degrees,
                "trend": "increasing"
                if avg_degrees[-1] > avg_degrees[0]
                else "decreasing"
                if avg_degrees[-1] < avg_degrees[0]
                else "stable",
                "change": avg_degrees[-1] - avg_degrees[0],
            }

        return trends

    def _identify_critical_events(self, networks: List[Dict]) -> List[Dict]:
        """识别关键事件"""
        events = []

        if len(networks) < 2:
            return events

        # 查找节点数量的显著变化
        for i in range(1, len(networks)):
            prev_nodes = networks[i - 1].get("num_nodes", 0)
            curr_nodes = networks[i].get("num_nodes", 0)

            if prev_nodes > 0:
                change_ratio = curr_nodes / prev_nodes

                if change_ratio > 1.5:
                    events.append(
                        {
                            "time": networks[i].get("time", ""),
                            "type": "node_surge",
                            "description": f"节点数量激增 {prev_nodes} -> {curr_nodes}",
                            "severity": "high",
                        }
                    )
                elif change_ratio < 0.5:
                    events.append(
                        {
                            "time": networks[i].get("time", ""),
                            "type": "node_drop",
                            "description": f"节点数量骤降 {prev_nodes} -> {curr_nodes}",
                            "severity": "high",
                        }
                    )

        # 查找边数量的显著变化
        for i in range(1, len(networks)):
            prev_edges = networks[i - 1].get("num_edges", 0)
            curr_edges = networks[i].get("num_edges", 0)

            if prev_edges > 0:
                change_ratio = curr_edges / prev_edges

                if change_ratio > 2.0:
                    events.append(
                        {
                            "time": networks[i].get("time", ""),
                            "type": "edge_surge",
                            "description": f"边数量激增 {prev_edges} -> {curr_edges}",
                            "severity": "medium",
                        }
                    )

        return events[:10]  # 限制返回数量

    def _analyze_node_mobility(self, networks: List[Dict]) -> Dict:
        """分析节点流动性"""
        if len(networks) < 2:
            return {"total_mobility": 0, "new_nodes": [], "left_nodes": []}

        # 获取所有时间点的节点
        all_nodes_sets = [set(net.get("nodes", [])) for net in networks]

        # 新进入的节点
        first_nodes = all_nodes_sets[0]
        last_nodes = all_nodes_sets[-1]
        new_nodes = list(last_nodes - first_nodes)
        left_nodes = list(first_nodes - last_nodes)

        # 计算流动性
        total_nodes = len(first_nodes | last_nodes)
        mobility = len(new_nodes) / total_nodes if total_nodes > 0 else 0

        return {
            "total_mobility": mobility,
            "new_nodes": new_nodes,
            "left_nodes": left_nodes,
            "total_new": len(new_nodes),
            "total_left": len(left_nodes),
        }

    def _get_time_range(self, data: List[Dict]) -> Dict:
        """获取时间范围"""
        if not data:
            return {"start": None, "end": None}

        return {
            "start": data[0].get("timestamp", data[0].get("time", "")),
            "end": data[-1].get("timestamp", data[-1].get("time", "")),
        }

    def _generate_summary(self, evolution: Dict, metrics_trend: Dict) -> str:
        """生成总结"""
        lines = []

        node_trend = evolution.get("node_trend", "unknown")
        edge_trend = evolution.get("edge_trend", "unknown")
        density_trend = evolution.get("density_trend", "unknown")

        trend_names = {
            "growing": "增长",
            "shrinking": "下降",
            "stable": "稳定",
            "increasing": "增加",
            "decreasing": "减少",
        }

        lines.append(f"网络规模{trend_names.get(node_trend, node_trend)}趋势")
        lines.append(f"连接密度{trend_names.get(density_trend, density_trend)}趋势")

        return "，".join(lines)


def analyze_temporal(
    time_series_data: List[Dict], time_field: str = "timestamp"
) -> Dict:
    """时序网络分析入口函数"""
    analyzer = TemporalAnalyzer()
    return analyzer.analyze_temporal(time_series_data, time_field)


if __name__ == "__main__":
    # 测试
    test_data = [
        {
            "timestamp": "2020-01",
            "edges": [{"source": "A", "target": "B"}, {"source": "B", "target": "C"}],
        },
        {
            "timestamp": "2020-02",
            "edges": [
                {"source": "A", "target": "B"},
                {"source": "B", "target": "C"},
                {"source": "C", "target": "D"},
            ],
        },
        {
            "timestamp": "2020-03",
            "edges": [
                {"source": "A", "target": "B"},
                {"source": "B", "target": "C"},
                {"source": "C", "target": "D"},
                {"source": "D", "target": "E"},
                {"source": "E", "target": "A"},
            ],
        },
    ]

    result = analyze_temporal(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
