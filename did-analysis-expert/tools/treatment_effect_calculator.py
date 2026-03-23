#!/usr/bin/env python3
"""
did-analysis-expert - 处理效应计算工具
计算DID处理效应
"""

from typing import Dict, Any
import json


class TreatmentEffectCalculator:
    """处理效应计算器"""

    def __init__(self):
        pass

    def calculate(self, data: Any) -> Dict:
        """计算处理效应"""
        if isinstance(data, list):
            return self._calculate_from_list(data)
        elif isinstance(data, dict):
            return self._calculate_from_dict(data)
        return {"error": "无法处理的数据格式"}

    def _calculate_from_list(self, data: list) -> Dict:
        # 提取数据
        t_before, t_after = [], []
        c_before, c_after = [], []

        for row in data:
            group = row.get("group", "")
            time = row.get("time", 0)
            y = row.get("y", 0)

            if group == "treatment":
                if time == 0:
                    t_before.append(y)
                else:
                    t_after.append(y)
            elif group == "control":
                if time == 0:
                    c_before.append(y)
                else:
                    c_after.append(y)

        # 计算均值
        t_before_mean = sum(t_before) / len(t_before) if t_before else 0
        t_after_mean = sum(t_after) / len(t_after) if t_after else 0
        c_before_mean = sum(c_before) / len(c_before) if c_before else 0
        c_after_mean = sum(c_after) / len(c_after) if c_after else 0

        # DID计算
        t_effect = t_after_mean - t_before_mean
        c_effect = c_after_mean - c_before_mean
        did_effect = t_effect - c_effect

        return {
            "treatment_before": t_before_mean,
            "treatment_after": t_after_mean,
            "control_before": c_before_mean,
            "control_after": c_after_mean,
            "treatment_effect": t_effect,
            "control_effect": c_effect,
            "did_estimate": did_effect,
            "interpretation": f"处理效应为{did_effect:.2f}",
            "significant": abs(did_effect) > 0,
        }

    def _calculate_from_dict(self, data: Dict) -> Dict:
        t_before = data.get("treatment_before", 0)
        t_after = data.get("treatment_after", 0)
        c_before = data.get("control_before", 0)
        c_after = data.get("control_after", 0)

        did = (t_after - t_before) - (c_after - c_before)

        return {
            "did_estimate": did,
            "interpretation": f"DID估计量: {did:.2f}",
        }


def calculate_treatment_effect(data: Any) -> Dict:
    return TreatmentEffectCalculator().calculate(data)


if __name__ == "__main__":
    test_data = [
        {"group": "treatment", "time": 0, "y": 10},
        {"group": "treatment", "time": 1, "y": 20},
        {"group": "control", "time": 0, "y": 8},
        {"group": "control", "time": 1, "y": 12},
    ]
    result = calculate_treatment_effect(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
