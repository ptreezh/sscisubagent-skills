#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主题分析专家 - 饱和度检验工具
Saturation Checker for Thematic Analysis

功能:
- 检验主题饱和度
- 计算新数据对新主题的贡献
- 评估编码充分性
- 生成饱和度报告

作者: Thematic Analysis Expert v5.0.0
创建时间: 2026-03-15
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import math

# 跨平台兼容
def get_output_dir() -> Path:
    """获取输出目录"""
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


@dataclass
class SaturationMetrics:
    """饱和度指标"""
    new_codes_rate: float = 0.0          # 新代码产生率
    new_themes_rate: float = 0.0         # 新主题产生率
    code_repetition_rate: float = 0.0    # 代码重复率
    theme_stability_rate: float = 0.0    # 主题稳定性
    overall_saturation: float = 0.0      # 总体饱和度
    
    def to_dict(self) -> Dict:
        return asdict(self)


class SaturationChecker:
    """饱和度检验器"""
    
    def __init__(self):
        self.code_history: List[Set[str]] = []      # 每个数据段产生的代码
        self.theme_history: List[Set[str]] = []     # 每个数据段产生的主题
        self.total_codes: Set[str] = set()          # 累计代码
        self.total_themes: Set[str] = set()         # 累计主题
        
    def add_data_segment(
        self,
        segment_id: str,
        new_codes: List[str],
        new_themes: List[str] = None
    ) -> Dict:
        """
        添加新的数据段分析结果
        
        Args:
            segment_id: 数据段标识
            new_codes: 该段产生的新代码
            new_themes: 该段产生的新主题
        
        Returns:
            更新后的饱和度状态
        """
        new_codes_set = set(new_codes)
        new_themes_set = set(new_themes or [])
        
        # 记录历史
        self.code_history.append(new_codes_set)
        self.theme_history.append(new_themes_set)
        
        # 更新累计
        previous_codes = self.total_codes.copy()
        previous_themes = self.total_themes.copy()
        
        self.total_codes.update(new_codes_set)
        self.total_themes.update(new_themes_set)
        
        # 计算新增
        truly_new_codes = new_codes_set - previous_codes
        truly_new_themes = new_themes_set - previous_themes
        
        return {
            "segment_id": segment_id,
            "segment_number": len(self.code_history),
            "codes_in_segment": len(new_codes_set),
            "new_codes": len(truly_new_codes),
            "themes_in_segment": len(new_themes_set),
            "new_themes": len(truly_new_themes),
            "cumulative_codes": len(self.total_codes),
            "cumulative_themes": len(self.total_themes)
        }
    
    def calculate_saturation_metrics(self) -> SaturationMetrics:
        """计算饱和度指标"""
        if len(self.code_history) < 2:
            return SaturationMetrics()
        
        metrics = SaturationMetrics()
        
        # 新代码产生率
        new_code_counts = []
        for i, codes in enumerate(self.code_history):
            if i == 0:
                new_code_counts.append(len(codes))
            else:
                previous = set()
                for j in range(i):
                    previous.update(self.code_history[j])
                new_codes = codes - previous
                new_code_counts.append(len(new_codes))
        
        if new_code_counts:
            # 计算后半段的平均新代码率
            mid = len(new_code_counts) // 2
            later_half = new_code_counts[mid:]
            if later_half:
                metrics.new_codes_rate = sum(later_half) / len(later_half)
        
        # 新主题产生率
        if self.theme_history:
            new_theme_counts = []
            for i, themes in enumerate(self.theme_history):
                if i == 0:
                    new_theme_counts.append(len(themes))
                else:
                    previous = set()
                    for j in range(i):
                        previous.update(self.theme_history[j])
                    new_themes = themes - previous
                    new_theme_counts.append(len(new_themes))
            
            if new_theme_counts:
                mid = len(new_theme_counts) // 2
                later_half = new_theme_counts[mid:]
                if later_half:
                    metrics.new_themes_rate = sum(later_half) / len(later_half)
        
        # 代码重复率
        if self.code_history:
            all_code_occurrences = []
            for codes in self.code_history:
                all_code_occurrences.extend(list(codes))
            
            if all_code_occurrences:
                unique_codes = set(all_code_occurrences)
                total_occurrences = len(all_code_occurrences)
                metrics.code_repetition_rate = 1 - (len(unique_codes) / total_occurrences)
        
        # 主题稳定性
        if len(self.theme_history) >= 3:
            last_three = self.theme_history[-3:]
            # 计算最后三个数据段主题的相似度
            intersection = set.intersection(*last_three) if last_three else set()
            union = set.union(*last_three) if last_three else set()
            if union:
                metrics.theme_stability_rate = len(intersection) / len(union)
        
        # 总体饱和度
        # 综合指标：新代码率低 + 代码重复率高 + 主题稳定性高 = 高饱和度
        if metrics.new_codes_rate < 1.0:  # 有足够的编码历史
            saturation = (
                (1 - min(metrics.new_codes_rate / 5, 1.0)) * 0.4 +  # 新代码率贡献
                metrics.code_repetition_rate * 0.3 +                # 重复率贡献
                metrics.theme_stability_rate * 0.3                  # 稳定性贡献
            )
            metrics.overall_saturation = saturation
        
        return metrics
    
    def assess_saturation(self, threshold: float = 0.80) -> Dict:
        """
        评估饱和度
        
        Args:
            threshold: 饱和度阈值
        
        Returns:
            饱和度评估结果
        """
        metrics = self.calculate_saturation_metrics()
        
        assessment = {
            "is_saturated": metrics.overall_saturation >= threshold,
            "saturation_level": metrics.overall_saturation,
            "threshold": threshold,
            "metrics": metrics.to_dict(),
            "recommendation": ""
        }
        
        if metrics.overall_saturation >= threshold:
            assessment["recommendation"] = "已达到饱和度阈值，可停止数据收集"
        elif metrics.overall_saturation >= threshold - 0.1:
            assessment["recommendation"] = "接近饱和，建议再收集少量数据进行确认"
        else:
            assessment["recommendation"] = "未达到饱和，建议继续数据收集"
        
        return assessment
    
    def get_saturation_curve_data(self) -> Dict:
        """获取饱和度曲线数据"""
        cumulative_codes = []
        cumulative_themes = []
        
        codes_so_far = set()
        themes_so_far = set()
        
        for i, (codes, themes) in enumerate(zip(self.code_history, self.theme_history)):
            codes_so_far.update(codes)
            themes_so_far.update(themes)
            cumulative_codes.append({
                "segment": i + 1,
                "cumulative_codes": len(codes_so_far)
            })
            cumulative_themes.append({
                "segment": i + 1,
                "cumulative_themes": len(themes_so_far)
            })
        
        return {
            "code_curve": cumulative_codes,
            "theme_curve": cumulative_themes
        }
    
    def generate_report(self) -> str:
        """生成饱和度报告"""
        metrics = self.calculate_saturation_metrics()
        assessment = self.assess_saturation()
        curve_data = self.get_saturation_curve_data()
        
        report = """# 主题饱和度检验报告

## 概述

- **分析数据段数**: {segments}
- **累计代码数**: {codes}
- **累计主题数**: {themes}
- **总体饱和度**: {saturation:.1%}

## 详细指标

| 指标 | 值 | 说明 |
|------|-----|------|
| 新代码产生率 | {new_codes_rate:.2f} | 平均每个数据段产生的新代码数 |
| 新主题产生率 | {new_themes_rate:.2f} | 平均每个数据段产生的新主题数 |
| 代码重复率 | {repetition:.1%} | 代码在多个数据段出现的比例 |
| 主题稳定性 | {stability:.1%} | 主题在近期数据中的一致性 |

## 饱和度评估

**状态**: {status}

**建议**: {recommendation}

## 累计曲线

### 代码累计曲线
```
数据段  累计代码数
{code_curve}
```

### 主题累计曲线
```
数据段  累计主题数
{theme_curve}
```

## 结论

{conclusion}
""".format(
            segments=len(self.code_history),
            codes=len(self.total_codes),
            themes=len(self.total_themes),
            saturation=metrics.overall_saturation,
            new_codes_rate=metrics.new_codes_rate,
            new_themes_rate=metrics.new_themes_rate,
            repetition=metrics.code_repetition_rate,
            stability=metrics.theme_stability_rate,
            status="✅ 已饱和" if assessment["is_saturated"] else "⚠️ 未饱和",
            recommendation=assessment["recommendation"],
            code_curve="\n".join([
                f"  {d['segment']:3d}      {d['cumulative_codes']:3d}" 
                for d in curve_data["code_curve"][-10:]
            ]),
            theme_curve="\n".join([
                f"  {d['segment']:3d}      {d['cumulative_themes']:3d}" 
                for d in curve_data["theme_curve"][-10:]
            ]),
            conclusion=self._generate_conclusion(assessment)
        )
        
        return report
    
    def _generate_conclusion(self, assessment: Dict) -> str:
        """生成结论"""
        if assessment["is_saturated"]:
            return """主题分析已达到饱和状态。后续数据不太可能产生新的重要主题或代码，
分析结果具有充分的代表性。可以进行最终报告撰写。"""
        else:
            return """主题分析尚未达到饱和状态。建议继续数据收集，
直到新数据不再产生新的重要主题或代码。"""


def check_saturation(code_history: List[List[str]], theme_history: List[List[str]] = None) -> Dict:
    """
    检验饱和度 - 主入口函数
    
    Args:
        code_history: 每个数据段的代码列表
        theme_history: 每个数据段的主题列表
    
    Returns:
        饱和度检验结果
    """
    checker = SaturationChecker()
    
    for i, codes in enumerate(code_history):
        themes = theme_history[i] if theme_history and i < len(theme_history) else None
        checker.add_data_segment(f"segment_{i+1}", codes, themes)
    
    return checker.assess_saturation()


# 示例使用
if __name__ == "__main__":
    # 模拟数据收集过程
    checker = SaturationChecker()
    
    # 模拟10个数据段的分析结果
    # 前期产生更多新代码，后期趋于饱和
    simulated_data = [
        (["C001", "C002", "C003"], ["T01"]),           # 段1: 很多新代码
        (["C004", "C005", "C001"], ["T01", "T02"]),    # 段2: 一些新代码
        (["C006", "C001", "C002"], ["T01"]),           # 段3: 少量新代码
        (["C007", "C003", "C004"], ["T02"]),           # 段4: 少量新代码
        (["C001", "C002", "C005"], ["T01", "T02"]),    # 段5: 无新代码
        (["C003", "C006", "C007"], ["T01"]),           # 段6: 无新代码
        (["C001", "C004", "C005"], ["T02"]),           # 段7: 无新代码
        (["C002", "C003", "C006"], ["T01", "T02"]),    # 段8: 无新代码
        (["C001", "C007"], ["T01"]),                   # 段9: 无新代码
        (["C003", "C004", "C005"], ["T02"]),           # 段10: 无新代码
    ]
    
    print("模拟数据收集过程...\n")
    for i, (codes, themes) in enumerate(simulated_data):
        result = checker.add_data_segment(f"访谈_{i+1}", codes, themes)
        print(f"段{i+1}: 新代码={result['new_codes']}, 累计={result['cumulative_codes']}")
    
    print("\n" + "="*50)
    print(checker.generate_report())
