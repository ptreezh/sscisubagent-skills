#!/usr/bin/env python3
"""
did-analysis-expert - 平行趋势检验工具
检验处理组和对照组在干预前的趋势是否平行
"""

from typing import Dict, List, Any
import json


class ParallelTrendsChecker:
    """平行趋势检验器"""

    def __init__(self):
        pass

    def check(self, data: Any) -> Dict:
        """检验平行趋势"""
        if isinstance(data, list):
            return self._check_from_list(data)
        elif isinstance(data, dict):
            return self._check_from_dict(data)
        return {"error": "无法处理的数据格式"}

    def _check_from_list(self, data: List) -> Dict:
        # 简单趋势计算
        trends = {"treatment": [], "control": []}

        for row in data:
            group = row.get("group", "")
            time = row.get("time", 0)
            y = row.get("y", 0)

            if group == "treatment":
                trends["treatment"].append((time, y))
            elif group == "control":
                trends["control"].append((time, y))

        # 计算趋势斜率
        treatment_slope = self._calculate_slope(trends["treatment"])
        control_slope = self._calculate_slope(trends["control"])

        # 判断平行趋势
        diff = abs(treatment_slope - control_slope)
        parallel = diff < 0.5  # 简化判断

        return {
            "treatment_slope": treatment_slope,
            "control_slope": control_slope,
            "slope_difference": diff,
            "parallel": parallel,
            "verdict": "通过" if parallel else "不通过",
            "explanation": "趋势平行" if parallel else "趋势不平行",
        }

    def _check_from_dict(self, data: Dict) -> Dict:
        # 从字典提取数据
        treatment = data.get("treatment", {})
        control = data.get("control", {})

        t_trend = [(t, v) for t, v in treatment.items()]
        c_trend = [(t, v) for t, v in control.items()]

        t_slope = self._calculate_slope(t_trend)
        c_slope = self._calculate_slope(c_trend)

        diff = abs(t_slope - c_slope)

        return {
            "treatment_slope": t_slope,
            "control_slope": c_slope,
            "slope_difference": diff,
            "parallel": diff < 0.5,
            "verdict": "通过" if diff < 0.5 else "不通过",
        }

    def _calculate_slope(self, points: List) -> float:
        if len(points) < 2:
            return 0.0
        points.sort(key=lambda x: x[0])
        n = len(points)
        sum_x = sum(p[0] for p in points)
        sum_y = sum(p[1] for p in points)
        sum_xy = sum(p[0] * p[1] for p in points)
        sum_x2 = sum(p[0] ** 2 for p in points)

        denom = n * sum_x2 - sum_x**2
        if denom == 0:
            return 0.0

        return (n * sum_xy - sum_x * sum_y) / denom


def check_parallel_trends(data: Any) -> Dict:
    return ParallelTrendsChecker().check(data)


if __name__ == "__main__":
    test_data = [
        {"group": "treatment", "time": 0, "y": 10},
        {"group": "treatment", "time": 1, "y": 12},
        {"group": "treatment", "time": 2, "y": 14},
        {"group": "control", "time": 0, "y": 8},
        {"group": "control", "time": 1, "y": 10},
        {"group": "control", "time": 2, "y": 12},
    ]
    result = check_parallel_trends(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
