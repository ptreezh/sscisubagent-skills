#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据分析工具 - CAS仿真技能

支持数据预处理、统计分析、格式转换
"""

import json
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
from pathlib import Path


def analyze_data(
    data: Dict[str, Any],
    analysis_type: str = "basic",
    output_format: str = "json"
) -> Dict[str, Any]:
    """
    分析输入数据
    
    Args:
        data: 输入数据字典
        analysis_type: 分析类型 (basic/statistical/distribution)
        output_format: 输出格式 (json/dict)
    
    Returns:
        分析结果字典
    """
    results = {
        "analysis_type": analysis_type,
        "status": "success",
        "data_summary": {},
        "statistics": {},
        "recommendations": []
    }
    
    # 基础分析
    if analysis_type in ["basic", "all"]:
        results["data_summary"] = _basic_analysis(data)
    
    # 统计分析
    if analysis_type in ["statistical", "all"]:
        results["statistics"] = _statistical_analysis(data)
    
    # 分布分析
    if analysis_type in ["distribution", "all"]:
        results["distributions"] = _distribution_analysis(data)
    
    # 生成仿真建议
    results["recommendations"] = _generate_recommendations(results)
    
    return results


def _basic_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """基础数据分析"""
    summary = {
        "keys": list(data.keys()),
        "key_count": len(data),
        "types": {}
    }
    
    for key, value in data.items():
        summary["types"][key] = type(value).__name__
        
        if isinstance(value, (list, np.ndarray)):
            summary[f"{key}_length"] = len(value)
        elif isinstance(value, dict):
            summary[f"{key}_keys"] = list(value.keys())
    
    return summary


def _statistical_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """统计分析"""
    stats = {}
    
    for key, value in data.items():
        if isinstance(value, (list, np.ndarray)):
            arr = np.array(value)
            if np.issubdtype(arr.dtype, np.number):
                stats[key] = {
                    "mean": float(np.mean(arr)),
                    "std": float(np.std(arr)),
                    "min": float(np.min(arr)),
                    "max": float(np.max(arr)),
                    "median": float(np.median(arr)),
                    "count": len(arr)
                }
    
    return stats


def _distribution_analysis(data: Dict[str, Any]) -> Dict[str, Any]:
    """分布分析"""
    distributions = {}
    
    for key, value in data.items():
        if isinstance(value, (list, np.ndarray)):
            arr = np.array(value)
            if np.issubdtype(arr.dtype, np.number):
                # 简单的分布检测
                distributions[key] = {
                    "type": _detect_distribution_type(arr),
                    "histogram": _compute_histogram(arr)
                }
    
    return distributions


def _detect_distribution_type(arr: np.ndarray) -> str:
    """检测分布类型"""
    if len(arr) < 10:
        return "insufficient_data"
    
    mean = np.mean(arr)
    std = np.std(arr)
    
    # 简单启发式判断
    if std < 0.01 * abs(mean):
        return "near_constant"
    elif abs(mean - np.median(arr)) < 0.1 * std:
        return "symmetric"
    else:
        return "skewed"


def _compute_histogram(arr: np.ndarray, bins: int = 10) -> Dict[str, Any]:
    """计算直方图"""
    hist, bin_edges = np.histogram(arr, bins=bins)
    return {
        "counts": hist.tolist(),
        "bin_edges": bin_edges.tolist()
    }


def _generate_recommendations(results: Dict[str, Any]) -> List[str]:
    """生成仿真建议"""
    recommendations = []
    
    stats = results.get("statistics", {})
    
    for key, stat in stats.items():
        if isinstance(stat, dict):
            if stat.get("std", 0) > stat.get("mean", 1) * 0.5:
                recommendations.append(
                    f"数据 {key} 变异系数较高，建议在仿真中考虑异质性"
                )
    
    if not recommendations:
        recommendations.append("数据适合进行CAS仿真分析")
    
    return recommendations


def preprocess_for_simulation(
    data: Dict[str, Any],
    target_format: str = "mesa"
) -> Dict[str, Any]:
    """
    预处理数据用于仿真
    
    Args:
        data: 原始数据
        target_format: 目标格式 (mesa/netlogo/repast)
    
    Returns:
        预处理后的数据
    """
    processed = {
        "format": target_format,
        "agents": [],
        "environment": {},
        "parameters": {}
    }
    
    # 提取主体数据
    if "agents" in data:
        processed["agents"] = _extract_agent_data(data["agents"])
    elif "nodes" in data:
        processed["agents"] = _extract_agent_data(data["nodes"])
    
    # 提取环境数据
    if "environment" in data:
        processed["environment"] = data["environment"]
    
    # 提取参数
    if "parameters" in data:
        processed["parameters"] = data["parameters"]
    
    return processed


def _extract_agent_data(agents_data: Any) -> List[Dict[str, Any]]:
    """提取主体数据"""
    if isinstance(agents_data, list):
        return agents_data
    elif isinstance(agents_data, dict):
        return [{"id": k, **v} for k, v in agents_data.items()]
    else:
        return []


def validate_simulation_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证仿真数据
    
    Returns:
        验证结果，包含 is_valid 和 issues
    """
    issues = []
    is_valid = True
    
    # 检查必要字段
    if not data:
        issues.append("数据为空")
        is_valid = False
    
    # 检查主体数据
    agents = data.get("agents", data.get("nodes", []))
    if not agents:
        issues.append("缺少主体数据")
        is_valid = False
    elif len(agents) < 2:
        issues.append("主体数量过少（建议≥100）")
    
    # 检查参数
    params = data.get("parameters", {})
    if not params:
        issues.append("缺少仿真参数（将使用默认值）")
    
    return {
        "is_valid": is_valid,
        "issues": issues,
        "agent_count": len(agents) if agents else 0,
        "parameter_count": len(params)
    }


# CLI入口
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        result = analyze_data(data)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        # 演示模式
        sample_data = {
            "agents": [{"id": i, "value": i * 0.5} for i in range(100)],
            "parameters": {"N": 100, "steps": 1000}
        }
        result = analyze_data(sample_data)
        print(json.dumps(result, indent=2, ensure_ascii=False))
