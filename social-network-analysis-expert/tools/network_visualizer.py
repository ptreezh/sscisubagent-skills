#!/usr/bin/env python3
"""
social-network-analysis-expert - 网络可视化工具
生成社会网络可视化图表
"""

from typing import Dict, List, Any, Optional
import json


# 可视化类型
VISUALIZATION_TYPES = {
    "basic": "基础网络图",
    "centrality": "中心性可视化",
    "community": "社群可视化",
    "temporal": "时序网络图",
    "heatmap": "关系热力图",
}


class NetworkVisualizer:
    """网络可视化器"""

    def __init__(self):
        self.visualization_results = []

    def visualize(
        self,
        network_data: Any,
        viz_type: str = "basic",
        output_format: str = "json",
    ) -> Dict:
        """
        生成网络可视化

        参数:
            network_data: 网络数据（边列表、邻接矩阵等）
            viz_type: 可视化类型
            output_format: 输出格式

        返回:
            可视化结果
        """
        # 解析网络数据
        nodes, edges = self._parse_network_data(network_data)

        # 生成可视化配置
        config = self._generate_viz_config(nodes, edges, viz_type)

        # 计算布局
        layout = self._calculate_layout(nodes, edges, viz_type)

        # 生成可视化数据
        viz_data = {
            "nodes": layout,
            "edges": edges,
            "config": config,
            "type": viz_type,
        }

        return {
            "viz_type": viz_type,
            "output_format": output_format,
            "num_nodes": len(nodes),
            "num_edges": len(edges),
            "layout": "force-directed" if viz_type == "basic" else "custom",
            "visualization_data": viz_data,
            "recommendations": self._get_viz_recommendations(
                viz_type, len(nodes), len(edges)
            ),
        }

    def _parse_network_data(self, data: Any) -> tuple:
        """解析网络数据"""
        nodes = []
        edges = []

        if isinstance(data, dict):
            # 边列表格式
            if "edges" in data:
                edges = data["edges"]
            if "nodes" in data:
                nodes = data["nodes"]
            # 自动从边列表提取节点
            if edges and not nodes:
                node_set = set()
                for edge in edges:
                    if isinstance(edge, dict):
                        node_set.add(edge.get("source", edge.get("from", "")))
                        node_set.add(edge.get("target", edge.get("to", "")))
                    elif isinstance(edge, (list, tuple)):
                        node_set.add(str(edge[0]))
                        node_set.add(str(edge[1]))
                nodes = [{"id": n} for n in sorted(node_set)]
        elif isinstance(data, list):
            edges = data
            node_set = set()
            for edge in edges:
                if isinstance(edge, dict):
                    node_set.add(edge.get("source", edge.get("from", "")))
                    node_set.add(edge.get("target", edge.get("to", "")))
                elif isinstance(edge, (list, tuple)):
                    node_set.add(str(edge[0]))
                    node_set.add(str(edge[1]))
            nodes = [{"id": n} for n in sorted(node_set)]

        return nodes, edges

    def _generate_viz_config(self, nodes: List, edges: List, viz_type: str) -> Dict:
        """生成可视化配置"""
        config = {
            "width": 800,
            "height": 600,
            "node_size_range": [10, 30],
            "edge_width_range": [1, 5],
            "colors": {
                "default": "#4A90D9",
                "highlight": "#E74C3C",
                "community": ["#4A90D9", "#E74C3C", "#2ECC71", "#F39C12", "#9B59B6"],
            },
        }

        # 根据可视化类型调整配置
        if viz_type == "centrality":
            config["node_size_range"] = [15, 50]
            config["show_labels"] = True
        elif viz_type == "community":
            config["node_size_range"] = [12, 40]
            config["show_community_colors"] = True

        return config

    def _calculate_layout(self, nodes: List, edges: List, viz_type: str) -> List[Dict]:
        """计算布局"""
        import math

        layout = []
        n = len(nodes)

        if n == 0:
            return layout

        # 简单的圆形布局作为基础
        for i, node in enumerate(nodes):
            if n == 1:
                x, y = 0.5, 0.5
            else:
                angle = 2 * math.pi * i / n
                x = 0.5 + 0.3 * math.cos(angle)
                y = 0.5 + 0.3 * math.sin(angle)

            layout.append(
                {
                    "id": node.get("id", f"node_{i}"),
                    "x": x,
                    "y": y,
                    "size": 20,
                    "color": "#4A90D9",
                }
            )

        # 力导向布局优化（简化的）
        layout = self._apply_force_layout(layout, edges)

        return layout

    def _apply_force_layout(self, nodes: List[Dict], edges: List) -> List[Dict]:
        """应用力导向布局"""
        # 简化的力导向算法
        iterations = 10

        for _ in range(iterations):
            # 计算节点之间的斥力
            for i, node1 in enumerate(nodes):
                fx, fy = 0, 0
                for j, node2 in enumerate(nodes):
                    if i != j:
                        dx = node1["x"] - node2["x"]
                        dy = node1["y"] - node2["y"]
                        dist = max(0.01, (dx**2 + dy**2) ** 0.5)
                        # 斥力
                        fx += dx / (dist * dist) * 0.01
                        fy += dy / (dist * dist) * 0.01

                # 计算边的引力
                node_id = node1["id"]
                for edge in edges:
                    source = edge.get("source", edge.get("from", ""))
                    target = edge.get("target", edge.get("to", ""))

                    if source == node_id:
                        target_node = next(
                            (n for n in nodes if n["id"] == target), None
                        )
                        if target_node:
                            dx = node1["x"] - target_node["x"]
                            dy = node1["y"] - target_node["y"]
                            fx -= dx * 0.1
                            fy -= dy * 0.1

                # 应用力
                nodes[i]["x"] = max(0.1, min(0.9, nodes[i]["x"] + fx))
                nodes[i]["y"] = max(0.1, min(0.9, nodes[i]["y"] + fy))

        return nodes

    def _get_viz_recommendations(
        self, viz_type: str, num_nodes: int, num_edges: int
    ) -> List[str]:
        """获取可视化建议"""
        recommendations = []

        if num_nodes > 100:
            recommendations.append("节点数量较多，建议使用聚合或筛选进行可视化")
        if num_edges > 500:
            recommendations.append("边数量较多，建议使用采样或动态边显示")
        if viz_type == "temporal":
            recommendations.append("时序网络建议使用动画或时间滑块")
        if num_nodes < 10:
            recommendations.append("小规模网络适合详细标签和所有边显示")

        if not recommendations:
            recommendations.append("当前参数适合标准可视化")

        return recommendations

    def generate_report(self, result: Dict) -> str:
        """生成可视化报告"""
        lines = []
        lines.append("# 网络可视化报告\n")

        lines.append(f"## 可视化类型\n{result.get('viz_type', '未知')}\n")
        lines.append(f"## 网络规模\n")
        lines.append(f"- 节点数: {result.get('num_nodes', 0)}")
        lines.append(f"- 边数: {result.get('num_edges', 0)}")
        lines.append(f"## 布局方法\n{result.get('layout', 'unknown')}")

        recommendations = result.get("recommendations", [])
        if recommendations:
            lines.append("\n## 可视化建议\n")
            for rec in recommendations:
                lines.append(f"- {rec}")

        return "\n".join(lines)


def visualize(
    network_data: Any, viz_type: str = "basic", output_format: str = "json"
) -> Dict:
    """网络可视化入口函数"""
    visualizer = NetworkVisualizer()
    return visualizer.visualize(network_data, viz_type, output_format)


if __name__ == "__main__":
    # 测试
    test_data = {
        "edges": [
            {"source": "A", "target": "B"},
            {"source": "B", "target": "C"},
            {"source": "C", "target": "D"},
            {"source": "D", "target": "A"},
            {"source": "A", "target": "C"},
        ]
    }

    result = visualize(test_data, "basic")
    print(json.dumps(result, ensure_ascii=False, indent=2))
