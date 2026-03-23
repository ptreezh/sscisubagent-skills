#!/usr/bin/env python3
"""
did-analysis-expert - 数据验证工具
验证DID分析所需的数据结构：处理组、对照组、面板数据
"""

from typing import Dict, List, Any
import json


class DataValidator:
    """DID数据验证器"""

    def __init__(self):
        pass

    def validate(self, data: Any) -> Dict:
        """验证DID数据结构"""
        if isinstance(data, dict):
            return self._validate_dict(data)
        elif isinstance(data, list):
            return self._validate_list(data)
        else:
            return {"valid": False, "issues": ["无法识别的数据格式"]}

    def _validate_dict(self, data: Dict) -> Dict:
        issues = []
        required_fields = ["treatment", "control", "time", "outcome"]

        for field in required_fields:
            if field not in data and field not in data.get("required", []):
                issues.append(f"缺少必需字段: {field}")

        # 检查数据结构
        if "treatment" in data:
            treatment = data["treatment"]
            if not isinstance(treatment, (list, dict)):
                issues.append("treatment应为列表或字典")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "summary": f"验证{'通过' if len(issues) == 0 else '失败'}",
        }

    def _validate_list(self, data: List) -> Dict:
        if len(data) == 0:
            return {"valid": False, "issues": ["数据为空"], "summary": "验证失败"}

        # 检查每行数据结构
        sample = data[0]
        if not isinstance(sample, dict):
            return {
                "valid": False,
                "issues": ["数据应为字典列表"],
                "summary": "验证失败",
            }

        # 检查必需字段
        required = ["group", "time", "y"]
        issues = []
        for field in required:
            if field not in sample:
                issues.append(f"缺少字段: {field}")

        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "num_observations": len(data),
            "summary": f"验证{'通过' if len(issues) == 0 else '失败'}",
        }


def validate_did_data(data: Any) -> Dict:
    return DataValidator().validate(data)


if __name__ == "__main__":
    test_data = [
        {"group": "treatment", "time": 0, "y": 10},
        {"group": "treatment", "time": 1, "y": 15},
        {"group": "control", "time": 0, "y": 8},
        {"group": "control", "time": 1, "y": 9},
    ]
    result = validate_did_data(test_data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
