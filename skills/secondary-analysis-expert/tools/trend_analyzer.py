#!/usr/bin/env python3
"""趋势分析器 - 分析时间序列趋势"""

import argparse
import json
from datetime import datetime
from typing import Dict, Any, List, Tuple

class TrendAnalyzer:
    """趋势分析器"""
    
    def __init__(self):
        self.trend_methods = {
            "linear": self._linear_trend,
            "moving_average": self._moving_average,
            "percentage_change": self._percentage_change
        }
    
    def analyze(self, time_series: List[Dict], value_var: str, 
                time_var: str = "year") -> Dict[str, Any]:
        """
        分析时间序列趋势
        
        Args:
            time_series: 时间序列数据
            value_var: 值变量名
            time_var: 时间变量名
            
        Returns:
            趋势分析结果
        """
        result = {
            "summary": {},
            "trend_direction": None,
            "trend_strength": None,
            "change_points": [],
            "projections": {},
            "timestamp": datetime.now().isoformat()
        }
        
        # 提取时间和值
        times = [d.get(time_var) for d in time_series]
        values = [d.get(value_var) for d in time_series]
        
        # 基本统计
        result["summary"] = {
            "start_time": times[0] if times else None,
            "end_time": times[-1] if times else None,
            "start_value": values[0] if values else None,
            "end_value": values[-1] if values else None,
            "min_value": min(values) if values else None,
            "max_value": max(values) if values else None,
            "mean_value": sum(values) / len(values) if values else None
        }
        
        # 线性趋势
        slope, intercept = self._linear_trend(times, values)
        result["linear_trend"] = {
            "slope": slope,
            "intercept": intercept,
            "direction": "increasing" if slope > 0 else "decreasing" if slope < 0 else "stable"
        }
        
        # 趋势强度
        result["trend_strength"] = self._calculate_trend_strength(values)
        
        # 变化率
        if values and values[0] != 0:
            total_change = (values[-1] - values[0]) / values[0] * 100
            result["total_change_rate"] = total_change
        
        # 变化点检测
        result["change_points"] = self._detect_change_points(times, values)
        
        return result
    
    def _linear_trend(self, times: List, values: List) -> Tuple[float, float]:
        """计算线性趋势"""
        if not values or len(values) < 2:
            return (0, 0)
        
        # 简化：用索引作为x
        n = len(values)
        x = list(range(n))
        y = values
        
        sum_x = sum(x)
        sum_y = sum(y)
        sum_xy = sum(xi * yi for xi, yi in zip(x, y))
        sum_x2 = sum(xi ** 2 for xi in x)
        
        denominator = n * sum_x2 - sum_x ** 2
        if denominator == 0:
            return (0, sum_y / n if n > 0 else 0)
        
        slope = (n * sum_xy - sum_x * sum_y) / denominator
        intercept = (sum_y - slope * sum_x) / n
        
        return (slope, intercept)
    
    def _moving_average(self, values: List, window: int = 3) -> List[float]:
        """计算移动平均"""
        if len(values) < window:
            return values
        
        result = []
        for i in range(len(values)):
            if i < window - 1:
                result.append(values[i])
            else:
                avg = sum(values[i-window+1:i+1]) / window
                result.append(avg)
        
        return result
    
    def _percentage_change(self, values: List) -> List[float]:
        """计算百分比变化"""
        if not values:
            return []
        
        changes = [0]  # 第一个点无变化
        for i in range(1, len(values)):
            if values[i-1] != 0:
                change = (values[i] - values[i-1]) / values[i-1] * 100
            else:
                change = 0
            changes.append(change)
        
        return changes
    
    def _calculate_trend_strength(self, values: List) -> str:
        """计算趋势强度"""
        if not values or len(values) < 2:
            return "unknown"
        
        slope, _ = self._linear_trend([], values)
        
        # 计算变异系数
        mean_val = sum(values) / len(values)
        if mean_val == 0:
            return "unknown"
        
        variance = sum((v - mean_val) ** 2 for v in values) / len(values)
        std = variance ** 0.5
        cv = std / abs(mean_val)
        
        # 结合斜率和变异系数判断
        if abs(slope) / abs(mean_val) > 0.05 and cv < 0.3:
            return "strong"
        elif abs(slope) / abs(mean_val) > 0.02:
            return "moderate"
        else:
            return "weak"
    
    def _detect_change_points(self, times: List, values: List) -> List[Dict]:
        """检测变化点"""
        if not values or len(values) < 3:
            return []
        
        changes = []
        for i in range(1, len(values) - 1):
            # 简化：检测大的方向变化
            prev_diff = values[i] - values[i-1]
            next_diff = values[i+1] - values[i]
            
            if prev_diff * next_diff < 0:  # 方向变化
                changes.append({
                    "time": times[i],
                    "value": values[i],
                    "type": "direction_change"
                })
        
        return changes

def main():
    parser = argparse.ArgumentParser(description="趋势分析器")
    parser.add_argument("--data", "-d", help="时间序列数据JSON文件")
    parser.add_argument("--value-var", "-v", default="value", help="值变量名")
    parser.add_argument("--time-var", "-t", default="year", help="时间变量名")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 默认数据
    time_series = [
        {"year": 2020, "value": 100},
        {"year": 2021, "value": 110},
        {"year": 2022, "value": 125},
        {"year": 2023, "value": 140},
        {"year": 2024, "value": 160}
    ]
    
    if args.data:
        with open(args.data, "r", encoding="utf-8") as f:
            time_series = json.load(f)
    
    analyzer = TrendAnalyzer()
    result = analyzer.analyze(time_series, args.value_var, args.time_var)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[完成] 结果已保存到 {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
