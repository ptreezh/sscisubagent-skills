#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pattern Matcher for Case Study
案例研究模式匹配工具

使用方法:
    python pattern_matcher.py --theory "A→B→C" --observed "A→B→C"
    python pattern_matcher.py --match
    python pattern_matcher.py --report
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import argparse


@dataclass
class Pattern:
    """模式定义"""
    id: str
    elements: List[str]
    relationships: List[Tuple[str, str, str]]  # (from, type, to)
    source: str  # theory/observed
    description: str = ""


@dataclass
class MatchResult:
    """匹配结果"""
    element: str
    theory_value: str
    observed_value: str
    match_level: str  # exact/partial/no_match
    notes: str = ""


class PatternMatcher:
    """模式匹配器"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.data_dir = self.project_path / "case-study-workspace" / "analysis"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.patterns_file = self.data_dir / "patterns.json"
        self.results_file = self.data_dir / "match_results.json"
        
        self.theory_patterns: List[Pattern] = []
        self.observed_patterns: List[Pattern] = []
        self.match_results: List[MatchResult] = []
        
        self._load_patterns()
    
    def _load_patterns(self):
        """加载模式数据"""
        if self.patterns_file.exists():
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.theory_patterns = [Pattern(**p) for p in data.get("theory", [])]
                self.observed_patterns = [Pattern(**p) for p in data.get("observed", [])]
        
        if self.results_file.exists():
            with open(self.results_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.match_results = [MatchResult(**r) for r in data]
    
    def _save_patterns(self):
        """保存模式数据"""
        data = {
            "theory": [p.__dict__ for p in self.theory_patterns],
            "observed": [p.__dict__ for p in self.observed_patterns]
        }
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _save_results(self):
        """保存匹配结果"""
        data = [r.__dict__ for r in self.match_results]
        with open(self.results_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def define_theory_pattern(self, pattern_str: str, description: str = "") -> Pattern:
        """定义理论模式"""
        # 解析模式字符串，如 "A→B→C" 或 "A->B->C"
        elements = re.split(r'[→->]+', pattern_str)
        elements = [e.strip() for e in elements if e.strip()]
        
        # 构建关系
        relationships = []
        for i in range(len(elements) - 1):
            relationships.append((elements[i], "leads_to", elements[i+1]))
        
        pattern = Pattern(
            id=f"theory-{len(self.theory_patterns)+1}",
            elements=elements,
            relationships=relationships,
            source="theory",
            description=description
        )
        
        self.theory_patterns.append(pattern)
        self._save_patterns()
        
        return pattern
    
    def define_observed_pattern(self, pattern_str: str, case_id: str, 
                                description: str = "") -> Pattern:
        """定义观察模式"""
        elements = re.split(r'[→->]+', pattern_str)
        elements = [e.strip() for e in elements if e.strip()]
        
        relationships = []
        for i in range(len(elements) - 1):
            relationships.append((elements[i], "observed_to", elements[i+1]))
        
        pattern = Pattern(
            id=f"observed-{case_id}-{len(self.observed_patterns)+1}",
            elements=elements,
            relationships=relationships,
            source="observed",
            description=f"案例{case_id}: {description}"
        )
        
        self.observed_patterns.append(pattern)
        self._save_patterns()
        
        return pattern
    
    def match_patterns(self, theory_id: str = None, observed_id: str = None) -> Dict:
        """执行模式匹配"""
        results = []
        
        # 选择要匹配的模式
        theory = None
        observed = None
        
        if theory_id:
            theory = next((p for p in self.theory_patterns if p.id == theory_id), None)
        elif self.theory_patterns:
            theory = self.theory_patterns[0]
        
        if observed_id:
            observed = next((p for p in self.observed_patterns if p.id == observed_id), None)
        elif self.observed_patterns:
            observed = self.observed_patterns[0]
        
        if not theory or not observed:
            return {"error": "需要指定理论和观察模式"}
        
        # 元素匹配
        theory_elements = set(theory.elements)
        observed_elements = set(observed.elements)
        
        # 完全匹配的元素
        exact_matches = theory_elements & observed_elements
        
        # 部分匹配的元素（相似但不完全相同）
        partial_matches = []
        for te in theory_elements - exact_matches:
            for oe in observed_elements - exact_matches:
                if self._similarity(te, oe) > 0.5:
                    partial_matches.append((te, oe))
        
        # 不匹配的元素
        unmatched_theory = theory_elements - exact_matches - {m[0] for m in partial_matches}
        unmatched_observed = observed_elements - exact_matches - {m[1] for m in partial_matches}
        
        # 计算匹配度
        total_elements = len(theory_elements)
        matched_elements = len(exact_matches) + len(partial_matches) * 0.5
        match_ratio = matched_elements / total_elements if total_elements > 0 else 0
        
        # 关系匹配
        theory_rels = set(theory.relationships)
        observed_rels = set(observed.relationships)
        matched_rels = theory_rels & observed_rels
        
        match_result = {
            "theory_pattern": theory.id,
            "observed_pattern": observed.id,
            "element_matching": {
                "exact_matches": list(exact_matches),
                "partial_matches": partial_matches,
                "unmatched_theory": list(unmatched_theory),
                "unmatched_observed": list(unmatched_observed),
                "match_ratio": f"{match_ratio:.1%}"
            },
            "relationship_matching": {
                "matched": len(matched_rels),
                "total_theory": len(theory_rels),
                "total_observed": len(observed_rels)
            },
            "overall_assessment": self._assess_match(match_ratio, len(matched_rels), len(theory_rels)),
            "interpretation": self._interpret_match(match_ratio, unmatched_theory, unmatched_observed)
        }
        
        return match_result
    
    def _similarity(self, str1: str, str2: str) -> float:
        """计算字符串相似度"""
        # 简化的相似度计算
        common = set(str1) & set(str2)
        total = set(str1) | set(str2)
        return len(common) / len(total) if total else 0
    
    def _assess_match(self, element_ratio: float, matched_rels: int, 
                      total_rels: int) -> str:
        """评估匹配程度"""
        if element_ratio >= 0.9 and matched_rels == total_rels:
            return "完全匹配 - 强支持理论"
        elif element_ratio >= 0.7:
            return "高度匹配 - 支持理论"
        elif element_ratio >= 0.5:
            return "部分匹配 - 需要修正理论"
        else:
            return "不匹配 - 挑战理论"
    
    def _interpret_match(self, match_ratio: float, unmatched_theory: set, 
                        unmatched_observed: set) -> str:
        """解释匹配结果"""
        interpretation = []
        
        if match_ratio >= 0.7:
            interpretation.append("观察数据支持理论预测。")
        elif match_ratio >= 0.5:
            interpretation.append("观察数据部分支持理论，需要关注差异。")
        else:
            interpretation.append("观察数据与理论预测存在显著差异。")
        
        if unmatched_theory:
            interpretation.append(f"理论预测但未观察到的要素: {', '.join(unmatched_theory)}")
        
        if unmatched_observed:
            interpretation.append(f"观察到但理论未预测的要素: {', '.join(unmatched_observed)}")
        
        return " ".join(interpretation)
    
    def cross_case_analysis(self) -> Dict:
        """跨案例分析"""
        if len(self.observed_patterns) < 2:
            return {"error": "跨案例分析需要至少2个观察模式"}
        
        # 收集所有元素
        all_elements = {}
        for pattern in self.observed_patterns:
            for element in pattern.elements:
                if element not in all_elements:
                    all_elements[element] = []
                all_elements[element].append(pattern.id)
        
        # 识别共同元素
        common_elements = {e: cases for e, cases in all_elements.items() 
                         if len(cases) >= len(self.observed_patterns) * 0.5}
        
        # 识别独特元素
        unique_elements = {e: cases for e, cases in all_elements.items() 
                         if len(cases) == 1}
        
        # 分析关系模式
        all_relationships = {}
        for pattern in self.observed_patterns:
            for rel in pattern.relationships:
                rel_str = f"{rel[0]} → {rel[2]}"
                if rel_str not in all_relationships:
                    all_relationships[rel_str] = []
                all_relationships[rel_str].append(pattern.id)
        
        common_relationships = {r: cases for r, cases in all_relationships.items()
                               if len(cases) >= len(self.observed_patterns) * 0.5}
        
        return {
            "common_elements": common_elements,
            "unique_elements": unique_elements,
            "common_relationships": common_relationships,
            "pattern_summary": f"识别出{len(common_elements)}个共同要素和{len(common_relationships)}个共同关系"
        }
    
    def generate_match_report(self) -> str:
        """生成匹配报告"""
        report = "# 模式匹配分析报告\n\n"
        
        # 理论模式
        report += "## 一、理论预测模式\n\n"
        for pattern in self.theory_patterns:
            report += f"### {pattern.id}\n"
            report += f"描述: {pattern.description}\n"
            report += f"要素: {' → '.join(pattern.elements)}\n\n"
        
        # 观察模式
        report += "## 二、观察模式\n\n"
        for pattern in self.observed_patterns:
            report += f"### {pattern.id}\n"
            report += f"描述: {pattern.description}\n"
            report += f"要素: {' → '.join(pattern.elements)}\n\n"
        
        # 匹配结果
        if self.match_results:
            report += "## 三、匹配结果\n\n"
            for result in self.match_results:
                report += f"| {result.element} | {result.theory_value} | {result.observed_value} | {result.match_level} |\n"
        
        # 跨案例分析
        if len(self.observed_patterns) >= 2:
            cross_case = self.cross_case_analysis()
            report += "## 四、跨案例分析\n\n"
            report += f"共同要素: {list(cross_case['common_elements'].keys())}\n\n"
            report += f"共同关系: {list(cross_case['common_relationships'].keys())}\n\n"
        
        return report


def main():
    parser = argparse.ArgumentParser(description="模式匹配工具")
    
    parser.add_argument("--theory", type=str, help="定义理论模式")
    parser.add_argument("--observed", type=str, help="定义观察模式")
    parser.add_argument("--case-id", type=str, help="案例ID")
    parser.add_argument("--description", type=str, default="", help="模式描述")
    parser.add_argument("--match", action="store_true", help="执行匹配")
    parser.add_argument("--cross-case", action="store_true", help="跨案例分析")
    parser.add_argument("--report", action="store_true", help="生成报告")
    
    args = parser.parse_args()
    
    matcher = PatternMatcher()
    
    if args.theory:
        pattern = matcher.define_theory_pattern(args.theory, args.description)
        print(f"✅ 理论模式已定义: {pattern.id}")
        print(f"   要素: {' → '.join(pattern.elements)}")
    
    if args.observed:
        pattern = matcher.define_observed_pattern(
            args.observed, 
            args.case_id or "unknown",
            args.description
        )
        print(f"✅ 观察模式已定义: {pattern.id}")
        print(f"   要素: {' → '.join(pattern.elements)}")
    
    if args.match:
        result = matcher.match_patterns()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if args.cross_case:
        result = matcher.cross_case_analysis()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if args.report:
        report = matcher.generate_match_report()
        print(report)


if __name__ == "__main__":
    main()
