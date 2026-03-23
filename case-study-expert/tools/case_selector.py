#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Case Study Selector
案例选择与复制逻辑工具

使用方法:
    python case_selector.py --single --type critical
    python case_selector.py --multiple --replication literal --cases 4
    python case_selector.py --design
"""

import json
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
import argparse


@dataclass
class Case:
    """案例定义"""
    id: str
    name: str
    case_type: str  # single/multiple
    selection_rationale: str
    expected_outcome: str
    replication_type: Optional[str] = None  # literal/theoretical
    data_sources: List[str] = field(default_factory=list)
    status: str = "pending"  # pending/selected/completed


class CaseSelector:
    """案例选择器"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.config_dir = self.project_path / "case-study-workspace"
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.config_file = self.config_dir / "case_selection.json"
        self.config = self._load_config()
        
        # 单案例选择类型
        self.single_case_types = {
            "critical": {
                "name": "关键案例",
                "rationale": "测试理论的核心命题",
                "when_to_use": "理论有明确预测时"
            },
            "extreme": {
                "name": "极端案例",
                "rationale": "揭示通常难以观察的机制",
                "when_to_use": "需要发现边界条件时"
            },
            "typical": {
                "name": "典型案例",
                "rationale": "代表常见情况",
                "when_to_use": "描述性研究"
            },
            "revelatory": {
                "name": "启示性案例",
                "rationale": "之前无法研究的情况",
                "when_to_use": "新现象首次观察"
            },
            "longitudinal": {
                "name": "纵向案例",
                "rationale": "追踪变化过程",
                "when_to_use": "研究动态机制"
            }
        }
        
        # 复制逻辑类型
        self.replication_types = {
            "literal": {
                "name": "逐案例复制",
                "description": "预测相似结果的案例",
                "purpose": "验证理论预测"
            },
            "theoretical": {
                "name": "理论复制",
                "description": "预测不同结果的案例",
                "purpose": "检验边界条件"
            }
        }
    
    def _load_config(self) -> Dict:
        """加载配置"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "study_type": None,
            "cases": [],
            "selection_criteria": [],
            "replication_logic": None
        }
    
    def _save_config(self):
        """保存配置"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def design_single_case(self, case_type: str, case_name: str, 
                          rationale: str) -> Dict:
        """设计单案例研究"""
        if case_type not in self.single_case_types:
            return {"error": f"无效的案例类型: {case_type}"}
        
        type_info = self.single_case_types[case_type]
        
        case = Case(
            id=f"case-01",
            name=case_name,
            case_type="single",
            selection_rationale=f"{type_info['name']}: {rationale}",
            expected_outcome="待确定"
        )
        
        self.config["study_type"] = "single"
        self.config["cases"] = [case.__dict__]
        self._save_config()
        
        return {
            "study_type": "单案例研究",
            "case_type": type_info["name"],
            "case": case.__dict__,
            "guidance": {
                "rationale": type_info["rationale"],
                "when_to_use": type_info["when_to_use"],
                "data_requirements": [
                    "建议使用多源数据",
                    "建立完整证据链",
                    "进行深入案例分析"
                ]
            }
        }
    
    def design_multiple_case(self, replication_plan: List[Dict]) -> Dict:
        """设计多案例研究（复制逻辑）"""
        cases = []
        literal_count = 0
        theoretical_count = 0
        
        for i, plan in enumerate(replication_plan, 1):
            rep_type = plan.get("replication_type", "literal")
            case = Case(
                id=f"case-{i:02d}",
                name=plan.get("name", f"案例{i}"),
                case_type="multiple",
                selection_rationale=plan.get("rationale", ""),
                expected_outcome=plan.get("expected_outcome", ""),
                replication_type=rep_type
            )
            cases.append(case.__dict__)
            
            if rep_type == "literal":
                literal_count += 1
            else:
                theoretical_count += 1
        
        self.config["study_type"] = "multiple"
        self.config["cases"] = cases
        self.config["replication_logic"] = {
            "literal_replications": literal_count,
            "theoretical_replications": theoretical_count,
            "total_cases": len(cases)
        }
        self._save_config()
        
        return {
            "study_type": "多案例研究",
            "replication_logic": {
                "逐案例复制": f"{literal_count}个案例",
                "理论复制": f"{theoretical_count}个案例"
            },
            "cases": cases,
            "guidance": {
                "method": "复制逻辑(非抽样逻辑)",
                "analysis": "先案例内分析，后跨案例比较",
                "quality": f"建议至少{literal_count}个逐案例复制"
            }
        }
    
    def generate_selection_matrix(self) -> str:
        """生成案例选择矩阵"""
        if not self.config["cases"]:
            return "尚未设计案例选择方案"
        
        matrix = "# 案例选择矩阵\n\n"
        
        if self.config["study_type"] == "single":
            case = self.config["cases"][0]
            matrix += f"""## 单案例设计

| 项目 | 内容 |
|------|------|
| 案例ID | {case['id']} |
| 案例名称 | {case['name']} |
| 选择理由 | {case['selection_rationale']} |
| 状态 | {case['status']} |
"""
        else:
            matrix += """## 多案例复制逻辑设计

| 案例ID | 名称 | 复制类型 | 选择理由 | 预期结果 | 状态 |
|--------|------|----------|----------|----------|------|
"""
            for case in self.config["cases"]:
                rep_type = "逐案例复制" if case.get("replication_type") == "literal" else "理论复制"
                matrix += f"| {case['id']} | {case['name']} | {rep_type} | {case['selection_rationale']} | {case['expected_outcome']} | {case['status']} |\n"
        
        return matrix
    
    def validate_selection(self) -> Dict:
        """验证案例选择"""
        issues = []
        recommendations = []
        
        if self.config["study_type"] == "single":
            # 单案例验证
            case = self.config["cases"][0]
            if not case.get("selection_rationale"):
                issues.append("缺少选择理由")
            if len(case.get("data_sources", [])) < 3:
                recommendations.append("建议至少使用3种数据来源进行三角验证")
        
        elif self.config["study_type"] == "multiple":
            # 多案例验证
            rep_logic = self.config.get("replication_logic", {})
            literal = rep_logic.get("literal_replications", 0)
            theoretical = rep_logic.get("theoretical_replications", 0)
            
            if literal < 2:
                issues.append("逐案例复制数量不足（建议至少2个）")
            if theoretical < 1:
                recommendations.append("建议至少包含1个理论复制案例")
            if literal + theoretical < 4:
                recommendations.append("多案例研究建议至少4个案例")
        
        return {
            "valid": len(issues) == 0,
            "issues": issues,
            "recommendations": recommendations,
            "next_steps": [
                "确定数据收集方案",
                "设计访谈协议",
                "建立案例数据库"
            ] if len(issues) == 0 else ["修正选择方案"]
        }
    
    def suggest_case_selection(self, research_question: str, 
                               theory_propositions: List[str]) -> Dict:
        """建议案例选择方案"""
        suggestions = {
            "single_case": [],
            "multiple_case": []
        }
        
        # 基于研究问题类型建议
        if "如何" in research_question:
            suggestions["single_case"].append({
                "type": "longitudinal",
                "reason": "过程研究适合纵向案例"
            })
        
        if "为什么" in research_question:
            suggestions["multiple_case"].append({
                "replication": "theoretical",
                "reason": "因果研究需要理论复制"
            })
        
        # 基于理论命题数量建议
        if len(theory_propositions) > 2:
            suggestions["multiple_case"].append({
                "min_cases": 4,
                "reason": "多命题需要多案例验证"
            })
        
        return suggestions


def main():
    parser = argparse.ArgumentParser(description="案例选择工具")
    
    parser.add_argument("--single", action="store_true", help="单案例设计")
    parser.add_argument("--multiple", action="store_true", help="多案例设计")
    parser.add_argument("--type", type=str, choices=[
        "critical", "extreme", "typical", "revelatory", "longitudinal"
    ], help="单案例类型")
    parser.add_argument("--name", type=str, help="案例名称")
    parser.add_argument("--rationale", type=str, help="选择理由")
    parser.add_argument("--replication", type=str, choices=[
        "literal", "theoretical"
    ], help="复制类型")
    parser.add_argument("--cases", type=int, default=4, help="案例数量")
    parser.add_argument("--design", action="store_true", help="生成交互式设计")
    parser.add_argument("--matrix", action="store_true", help="生成选择矩阵")
    parser.add_argument("--validate", action="store_true", help="验证选择方案")
    
    args = parser.parse_args()
    
    selector = CaseSelector()
    
    if args.single and args.type:
        result = selector.design_single_case(
            args.type, 
            args.name or "待命名案例",
            args.rationale or "待补充理由"
        )
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if args.multiple:
        # 示例多案例设计
        replication_plan = []
        for i in range(args.cases):
            rep_type = "literal" if i < args.cases // 2 else "theoretical"
            replication_plan.append({
                "name": f"案例{i+1}",
                "replication_type": args.replication or rep_type,
                "rationale": "待补充",
                "expected_outcome": "待确定"
            })
        result = selector.design_multiple_case(replication_plan)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if args.matrix:
        print(selector.generate_selection_matrix())
    
    if args.validate:
        result = selector.validate_selection()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if args.design:
        print("=== 案例研究设计指南 ===\n")
        print("1. 单案例选择类型:")
        for t, info in selector.single_case_types.items():
            print(f"   - {t}: {info['name']} - {info['rationale']}")
        print("\n2. 多案例复制逻辑:")
        for t, info in selector.replication_types.items():
            print(f"   - {t}: {info['name']} - {info['description']}")
        print("\n3. 建议:")
        print("   - 探索性研究: 单案例或2-3个多案例")
        print("   - 解释性研究: 4个以上多案例，使用复制逻辑")
        print("   - 描述性研究: 典型单案例或代表性多案例")


if __name__ == "__main__":
    main()
