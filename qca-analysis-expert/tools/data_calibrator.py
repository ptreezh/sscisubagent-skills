#!/usr/bin/env python3
"""
qca-analysis-expert - 数据校准工具
将原始数据校准为模糊集隶属度(0-1)
基于Ragin (2008)模糊集QCA方法
"""

from typing import Dict, List, Any
import json


class DataCalibrator:
    """数据校准器"""

    def __init__(self):
        self.calibration_thresholds = {}

    def calibrate(self, data: Any, thresholds: Dict = None) -> Dict:
        """校准数据"""
        if thresholds:
            self.calibration_thresholds = thresholds

        if isinstance(data, list):
            return self._calibrate_list(data)
        elif isinstance(data, dict):
            return self._calibrate_dict(data)
        return {"error": "无法处理的数据格式"}

    def _calibrate_list(self, data: List) -> Dict:
        calibrated = []
        for row in data:
            if isinstance(row, dict):
                calibrated_row = {}
                for key, value in row.items():
                    calibrated_row[key] = self._calibrate_value(value)
                calibrated.append(calibrated_row)

        return {
            "calibrated_data": calibrated,
            "num_cases": len(calibrated),
            "method": "direct calibration",
        }

    def _calibrate_dict(self, data: Dict) -> Dict:
        calibrated = {}
        for key, value in data.items():
            if isinstance(value, list):
                calibrated[key] = [self._calibrate_value(v) for v in value]
            else:
                calibrated[key] = self._calibrate_value(value)
        return {"calibrated_data": calibrated}

    def _calibrate_value(self, value: Any) -> float:
        """直接校准为0-1"""
        if isinstance(value, (int, float)):
            # 简单归一化
            return min(1.0, max(0.0, value / 10 if value <= 10 else 1.0))
        elif isinstance(value, str):
            # 字符串映射
            if value.lower() in ["yes", "y", "true", "1"]:
                return 1.0
            elif value.lower() in ["no", "n", "false", "0"]:
                return 0.0
        return 0.5


def calibrate_data(data: Any, thresholds: Dict = None) -> Dict:
    return DataCalibrator().calibrate(data, thresholds)


if __name__ == "__main__":
    test_data = [
        {"education": 12, "income": 50000},
        {"education": 16, "income": 80000},
        {"education": 8, "income": 30000},
    ]
    result = calibrate_data(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
