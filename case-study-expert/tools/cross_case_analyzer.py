#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cross Case Analyzer for Case Study
跨案例分析工具

使用方法:
    python cross_case_analyzer.py --init
    python cross_case_analyzer.py --add-case "案例A"
    python cross_case_analyzer.py --compare
    python cross_case_analyzer.py --report
"""

import json
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from collections import Counter
import argparse


@dataclass
class CaseData:
    """案例数据"""
    id: str
    name: str
    elements: List[str] = field(default_factory=list)
    relationships: List[Tuple[str, str, str]] = field(default_factory=list)
    attributes: Dict = field(default_factory=dict)
    findings: List[str] = field(default_factory=list)


@dataclass
class Pattern:
    """识别的模式"""
    id: str
    type: str  # common/unique/divergent
    elements: List[str]
    cases: List[str]
    description: str = ""


class CrossCaseAnalyzer:
    """跨案例分析器"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.data_dir = self.project_path / "case-study-workspace" / "analysis"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.cases_file = self.data_dir / "cases.json"
        self.patterns_file = self.data_dir / "patterns.json"
        self.report_file = self.data_dir / "cross_case_report.md"
        
        self.cases: Dict[str, CaseData] = {}
        self.patterns: List[Pattern] = []
        
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        if self.cases_file.exists():
            with open(self.cases_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for case_id, case_data in data.items():
                    self.cases[case_id] = CaseData(**case_data)
        
        if self.patterns_file.exists():
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.patterns = [Pattern(**p) for p in data]
    
    def _save_data(self):
        """保存数据"""
        with open(self.cases_file, 'w', encoding='utf-8') as f:
            json.dump({k: v.__dict__ for k, v in self.cases.items()}, 
                     f, ensure_ascii=False, indent=2)
        
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump([p.__dict__ for p in self.patterns], 
                     f, ensure_ascii=False, indent=2)
    
    def add_case(self, case_id: str, name: str, elements: List[str] = None,
                 relationships: List[Tuple] = None, attributes: Dict = None) -> CaseData:
        """添加案例"""
        case = CaseData(
            id=case_id,
            name=name,
            elements=elements or [],
            relationships=[tuple(r) for r in (relationships or [])],
            attributes=attributes or {}
        )
        self.cases[case_id] = case
        self._save_data()
        return case
    
    def identify_common_elements(self) -> Pattern:
        """识别共同要素"""
        if not self.cases:
            return None
        
        # 统计每个要素出现的案例数
        element_counts = Counter()
        for case in self.cases.values():
            for element in case.elements:
                element_counts[element] += 1
        
        # 找出在所有案例中都出现的要素
        total_cases = len(self.cases)
        common_elements = [e for e, c in element_counts.items() 
                          if c == total_cases]
        
        pattern = Pattern(
            id=f"pattern-common-{len(self.patterns)+1}",
            type="common",
            elements=common_elements,
            cases=list(self.cases.keys()),
            description=f"在所有{total_cases}个案例中出现的要素"
        )
        
        self.patterns.append(pattern)
        self._save_data()
        
        return pattern
    
    def identify_unique_elements(self) -> List[Pattern]:
        """识别独特要素"""
        unique_patterns = []
        
        # 统计每个要素出现的案例
        element_cases = {}
        for case in self.cases.values():
            for element in case.elements:
                if element not in element_cases:
                    element_cases[element] = []
                element_cases[element].append(case.id)
        
        # 找出只在一个案例中出现的要素
        for element, cases in element_cases.items():
            if len(cases) == 1:
                pattern = Pattern(
                    id=f"pattern-unique-{element}",
                    type="unique",
                    elements=[element],
                    cases=cases,
                    description=f"仅在案例{cases[0]}中出现的独特要素"
                )
                unique_patterns.append(pattern)
                self.patterns.append(pattern)
        
        self._save_data()
        return unique_patterns
    
    def identify_divergent_patterns(self) -> List[Pattern]:
        """识别分歧模式"""
        divergent_patterns = []
        
        # 比较关系模式
        relationship_comparison = {}
        for case in self.cases.values():
            for rel in case.relationships:
                rel_key = f"{rel[0]}-{rel[1]}-{rel[2]}"
                if rel_key not in relationship_comparison:
                    relationship_comparison[rel_key] = []
                relationship_comparison[rel_key].append(case.id)
        
        # 找出关系模式不同的地方
        for rel_key, cases in relationship_comparison.items():
            if len(cases) < len(self.cases):
                missing_cases = set(self.cases.keys()) - set(cases)
                pattern = Pattern(
                    id=f"pattern-divergent-{len(divergent_patterns)+1}",
                    type="divergent",
                    elements=[rel_key],
                    cases=cases,
                    description=f"关系模式分歧: {cases}有此关系，{list(missing_cases)}无"
                )
                divergent_patterns.append(pattern)
                self.patterns.append(pattern)
        
        self._save_data()
        return divergent_patterns
    
    def compare_cases(self, case1_id: str, case2_id: str) -> Dict:
        """比较两个案例"""
        if case1_id not in self.cases or case2_id not in self.cases:
            return {"error": "案例不存在"}
        
        case1 = self.cases[case1_id]
        case2 = self.cases[case2_id]
        
        # 要素比较
        elements1 = set(case1.elements)
        elements2 = set(case2.elements)
        
        common_elements = elements1 & elements2
        unique_to_1 = elements1 - elements2
        unique_to_2 = elements2 - elements1
        
        # 关系比较
        rels1 = set(case1.relationships)
        rels2 = set(case2.relationships)
        
        common_rels = rels1 & rels2
        unique_rels_1 = rels1 - rels2
        unique_rels_2 = rels2 - rels1
        
        # 属性比较
        attribute_comparison = {}
        all_attributes = set(case1.attributes.keys()) | set(case2.attributes.keys())
        for attr in all_attributes:
            val1 = case1.attributes.get(attr, "N/A")
            val2 = case2.attributes.get(attr, "N/A")
            attribute_comparison[attr] = {
                "case1": val1,
                "case2": val2,
                "same": val1 == val2
            }
        
        return {
            "case1": case1_id,
            "case2": case2_id,
            "elements": {
                "common": list(common_elements),
                "unique_to_case1": list(unique_to_1),
                "unique_to_case2": list(unique_to_2),
                "similarity": len(common_elements) / len(elements1 | elements2) if elements1 | elements2 else 0
            },
            "relationships": {
                "common": [list(r) for r in common_rels],
                "unique_to_case1": [list(r) for r in unique_rels_1],
                "unique_to_case2": [list(r) for r in unique_rels_2]
            },
            "attributes": attribute_comparison
        }
    
    def generate_comparison_matrix(self) -> str:
        """生成比较矩阵"""
        if len(self.cases) < 2:
            return "需要至少2个案例进行比较"
        
        case_ids = list(self.cases.keys())
        
        matrix = "# 跨案例比较矩阵\n\n"
        matrix += "## 一、要素比较\n\n"
        
        # 收集所有要素
        all_elements = set()
        for case in self.cases.values():
            all_elements.update(case.elements)
        
        # 要素矩阵
        matrix += "| 要素 | " + " | ".join(case_ids) + " |\n"
        matrix += "|" + "---|" * (len(case_ids) + 1) + "\n"
        
        for element in sorted(all_elements):
            row = f"| {element} |"
            for case_id in case_ids:
                if element in self.cases[case_id].elements:
                    row += " ✓ |"
                else:
                    row += " |"
            matrix += row + "\n"
        
        matrix += "\n## 二、关系比较\n\n"
        
        # 收集所有关系
        all_rels = set()
        for case in self.cases.values():
            for rel in case.relationships:
                all_rels.add(f"{rel[0]} → {rel[2]}")
        
        if all_rels:
            matrix += "| 关系 | " + " | ".join(case_ids) + " |\n"
            matrix += "|" + "---|" * (len(case_ids) + 1) + "\n"
            
            for rel in sorted(all_rels):
                row = f"| {rel} |"
                for case_id in case_ids:
                    case_rels = [f"{r[0]} → {r[2]}" for r in self.cases[case_id].relationships]
                    if rel in case_rels:
                        row += " ✓ |"
                    else:
                        row += " |"
                matrix += row + "\n"
        
        return matrix
    
    def generate_report(self) -> str:
        """生成跨案例分析报告"""
        report = "# 跨案例分析报告\n\n"
        
        report += f"## 分析概览\n\n"
        report += f"- 案例数量: {len(self.cases)}\n"
        report += f"- 识别模式数: {len(self.patterns)}\n\n"
        
        # 共同要素
        common_patterns = [p for p in self.patterns if p.type == "common"]
        if common_patterns:
            report += "## 共同要素\n\n"
            for pattern in common_patterns:
                report += f"- {', '.join(pattern.elements)}\n"
        
        # 独特要素
        unique_patterns = [p for p in self.patterns if p.type == "unique"]
        if unique_patterns:
            report += "\n## 独特要素\n\n"
            for pattern in unique_patterns:
                report += f"- **{pattern.cases[0]}**: {', '.join(pattern.elements)}\n"
        
        # 分歧模式
        divergent_patterns = [p for p in self.patterns if p.type == "divergent"]
        if divergent_patterns:
            report += "\n## 分歧模式\n\n"
            for pattern in divergent_patterns:
                report += f"- {pattern.description}\n"
        
        # 比较矩阵
        report += "\n" + self.generate_comparison_matrix()
        
        # 理论启示
        report += "\n## 理论启示\n\n"
        report += "基于跨案例分析，得出以下理论启示：\n\n"
        
        if common_patterns:
            report += "1. 共同要素表明这些因素可能是核心机制\n"
        if unique_patterns:
            report += "2. 独特要素揭示了情境因素的影响\n"
        if divergent_patterns:
            report += "3. 分歧模式提示了边界条件\n"
        
        # 保存报告
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def export_to_json(self) -> Dict:
        """导出为JSON格式"""
        return {
            "cases": {k: v.__dict__ for k, v in self.cases.items()},
            "patterns": [p.__dict__ for p in self.patterns],
            "summary": {
                "total_cases": len(self.cases),
                "total_patterns": len(self.patterns),
                "common_patterns": len([p for p in self.patterns if p.type == "common"]),
                "unique_patterns": len([p for p in self.patterns if p.type == "unique"]),
                "divergent_patterns": len([p for p in self.patterns if p.type == "divergent"])
            }
        }


def main():
    parser = argparse.ArgumentParser(description="跨案例分析工具")
    
    parser.add_argument("--init", action="store_true", help="初始化分析")
    parser.add_argument("--add-case", type=str, help="添加案例ID")
    parser.add_argument("--name", type=str, help="案例名称")
    parser.add_argument("--elements", type=str, nargs='+', help="案例要素")
    parser.add_argument("--compare", type=str, nargs=2, help="比较两个案例")
    parser.add_argument("--matrix", action="store_true", help="生成比较矩阵")
    parser.add_argument("--report", action="store_true", help="生成分析报告")
    parser.add_argument("--export", action="store_true", help="导出JSON")
    parser.add_argument("--analyze", action="store_true", help="执行完整分析")
    
    args = parser.parse_args()
    
    analyzer = CrossCaseAnalyzer()
    
    if args.add_case:
        case = analyzer.add_case(
            args.add_case,
            args.name or args.add_case,
            args.elements or []
        )
        print(f"✅ 案例 {case.id} 已添加")
        print(f"   名称: {case.name}")
        print(f"   要素: {case.elements}")
    
    if args.compare:
        result = analyzer.compare_cases(args.compare[0], args.compare[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if args.matrix:
        print(analyzer.generate_comparison_matrix())
    
    if args.analyze:
        analyzer.identify_common_elements()
        analyzer.identify_unique_elements()
        analyzer.identify_divergent_patterns()
        print("✅ 跨案例分析完成")
    
    if args.report:
        report = analyzer.generate_report()
        print(report)
        print(f"\n📄 报告已保存: {analyzer.report_file}")
    
    if args.export:
        data = analyzer.export_to_json()
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
