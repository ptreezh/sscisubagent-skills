#!/usr/bin/env python3
"""变量重构器 - 从原始数据创建新变量"""

import argparse
import json
from datetime import datetime
from typing import Dict, Any, List, Callable

class VariableReconstructor:
    """变量重构器"""
    
    def __init__(self):
        self.recoding_rules = {}
        self.combination_rules = {}
    
    def register_recoding(self, var_name: str, mapping: Dict) -> None:
        """注册重新编码规则"""
        self.recoding_rules[var_name] = mapping
    
    def register_combination(self, new_var: str, formula: str, 
                            source_vars: List[str]) -> None:
        """注册组合规则"""
        self.combination_rules[new_var] = {
            "formula": formula,
            "source_vars": source_vars
        }
    
    def recode(self, data: Dict, var_name: str, value: Any) -> Any:
        """
        重新编码变量
        
        Args:
            data: 原始数据
            var_name: 变量名
            value: 原始值
            
        Returns:
            新编码值
        """
        if var_name not in self.recoding_rules:
            return value
        
        mapping = self.recoding_rules[var_name]
        
        # 直接映射
        if value in mapping:
            return mapping[value]
        
        # 范围映射
        if isinstance(mapping, dict) and "ranges" in mapping:
            for range_def, new_value in mapping["ranges"].items():
                if self._in_range(value, range_def):
                    return new_value
        
        return mapping.get("default", value)
    
    def combine(self, data: Dict, new_var: str) -> Any:
        """
        组合创建新变量
        
        Args:
            data: 原始数据
            new_var: 新变量名
            
        Returns:
            新变量值
        """
        if new_var not in self.combination_rules:
            return None
        
        rule = self.combination_rules[new_var]
        source_vars = rule["source_vars"]
        formula = rule["formula"]
        
        # 获取源变量值
        values = {var: data.get(var) for var in source_vars}
        
        # 执行计算
        if formula == "sum":
            return sum(v for v in values.values() if v is not None)
        elif formula == "mean":
            valid_values = [v for v in values.values() if v is not None]
            return sum(valid_values) / len(valid_values) if valid_values else None
        elif formula == "max":
            return max(v for v in values.values() if v is not None)
        elif formula == "min":
            return min(v for v in values.values() if v is not None)
        else:
            return None
    
    def create_index(self, data: Dict, var_list: List[str], 
                    method: str = "mean") -> float:
        """
        创建指数
        
        Args:
            data: 原始数据
            var_list: 变量列表
            method: 聚合方法
            
        Returns:
            指数值
        """
        values = [data.get(var) for var in var_list]
        values = [v for v in values if v is not None]
        
        if not values:
            return None
        
        if method == "mean":
            return sum(values) / len(values)
        elif method == "sum":
            return sum(values)
        elif method == "zscore":
            # 简化z-score（假设已知均值标准差）
            return sum(values) / len(values)
        
        return None
    
    def standardize(self, value: float, mean: float, std: float) -> float:
        """标准化"""
        if std == 0:
            return 0
        return (value - mean) / std
    
    def _in_range(self, value: Any, range_def: str) -> bool:
        """检查值是否在范围内"""
        try:
            if "-" in range_def:
                low, high = map(float, range_def.split("-"))
                return low <= float(value) <= high
            elif range_def.startswith("<"):
                return float(value) < float(range_def[1:])
            elif range_def.startswith(">"):
                return float(value) > float(range_def[1:])
        except (ValueError, TypeError):
            return False
        return False

def main():
    parser = argparse.ArgumentParser(description="变量重构器")
    parser.add_argument("--data", "-d", help="数据JSON文件")
    parser.add_argument("--rules", "-r", help="重构规则JSON文件")
    parser.add_argument("--output", "-o", help="输出文件路径")
    
    args = parser.parse_args()
    
    # 默认数据
    data = {"age": 35, "income": 5000, "education": 3}
    
    if args.data:
        with open(args.data, "r", encoding="utf-8") as f:
            data = json.load(f)
    
    reconstructor = VariableReconstructor()
    
    # 注册示例规则
    reconstructor.register_recoding("age", {
        "ranges": {"0-30": "young", "31-50": "middle", "51-100": "old"}
    })
    
    # 执行重构
    result = {
        "original_data": data,
        "reconstructed_variables": {},
        "timestamp": datetime.now().isoformat()
    }
    
    for var, value in data.items():
        if var in reconstructor.recoding_rules:
            result["reconstructed_variables"][f"{var}_recoded"] = \
                reconstructor.recode(data, var, value)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"[完成] 结果已保存到 {args.output}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()