#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cultural Pattern Analyzer for Ethnography Research
文化模式分析工具

使用方法:
    python cultural_pattern_analyzer.py --init
    python cultural_pattern_analyzer.py --add-pattern "帮工制度" --type behavior
    python cultural_pattern_analyzer.py --add-evidence "PN001" "田野笔记FN001"
    python cultural_pattern_analyzer.py --validate "PN001"
    python cultural_pattern_analyzer.py --report
"""

import json
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from collections import Counter
import argparse


@dataclass
class CulturalPattern:
    """文化模式数据结构"""
    id: str
    name: str
    pattern_type: str  # behavior, language, relationship, space, time
    description: str = ""
    emic_view: str = ""  # 主位视角
    etic_view: str = ""  # 客位视角
    thick_description: str = ""  # 深描
    evidence_ids: List[str] = field(default_factory=list)
    validation_status: str = "tentative"  # tentative, validated, confirmed
    frequency: int = 0
    contexts: List[str] = field(default_factory=list)
    related_patterns: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Evidence:
    """证据数据结构"""
    id: str
    pattern_id: str
    source_type: str  # observation, interview, document
    source_id: str
    content: str
    context: str = ""
    date: str = ""
    location: str = ""


class CulturalPatternAnalyzer:
    """文化模式分析器"""
    
    PATTERN_TYPES = {
        "behavior": "行为模式",
        "language": "语言模式",
        "relationship": "关系模式",
        "space": "空间模式",
        "time": "时间模式"
    }
    
    VALIDATION_LEVELS = {
        "tentative": "初步识别",
        "validated": "已验证",
        "confirmed": "已确认"
    }
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.data_dir = self.project_path / "ethnography-workspace" / "patterns"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.patterns_file = self.data_dir / "patterns.json"
        self.evidence_file = self.data_dir / "evidence.json"
        self.report_file = self.data_dir / "pattern_report.md"
        
        self.patterns: Dict[str, CulturalPattern] = {}
        self.evidence: Dict[str, Evidence] = {}
        
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        if self.patterns_file.exists():
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for pid, pdata in data.items():
                    self.patterns[pid] = CulturalPattern(**pdata)
        
        if self.evidence_file.exists():
            with open(self.evidence_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for eid, edata in data.items():
                    self.evidence[eid] = Evidence(**edata)
    
    def _save_data(self):
        """保存数据"""
        with open(self.patterns_file, 'w', encoding='utf-8') as f:
            json.dump({k: v.__dict__ for k, v in self.patterns.items()}, 
                     f, ensure_ascii=False, indent=2)
        
        with open(self.evidence_file, 'w', encoding='utf-8') as f:
            json.dump({k: v.__dict__ for k, v in self.evidence.items()}, 
                     f, ensure_ascii=False, indent=2)
    
    def _generate_pattern_id(self) -> str:
        """生成模式ID"""
        count = len(self.patterns)
        return f"PN{count+1:03d}"
    
    def _generate_evidence_id(self) -> str:
        """生成证据ID"""
        count = len(self.evidence)
        return f"EV{count+1:03d}"
    
    def add_pattern(self, name: str, pattern_type: str,
                   description: str = "") -> CulturalPattern:
        """添加文化模式"""
        now = datetime.now()
        pattern_id = self._generate_pattern_id()
        
        pattern = CulturalPattern(
            id=pattern_id,
            name=name,
            pattern_type=pattern_type,
            description=description,
            created_at=now.isoformat(),
            updated_at=now.isoformat()
        )
        
        self.patterns[pattern_id] = pattern
        self._save_data()
        
        return pattern
    
    def update_pattern(self, pattern_id: str, **kwargs) -> Optional[CulturalPattern]:
        """更新模式"""
        if pattern_id not in self.patterns:
            return None
        
        pattern = self.patterns[pattern_id]
        for key, value in kwargs.items():
            if hasattr(pattern, key):
                setattr(pattern, key, value)
        
        pattern.updated_at = datetime.now().isoformat()
        self._save_data()
        
        return pattern
    
    def add_evidence(self, pattern_id: str, source_type: str,
                    source_id: str, content: str,
                    context: str = "", date: str = "",
                    location: str = "") -> Optional[Evidence]:
        """添加证据"""
        if pattern_id not in self.patterns:
            return None
        
        evidence_id = self._generate_evidence_id()
        
        evidence = Evidence(
            id=evidence_id,
            pattern_id=pattern_id,
            source_type=source_type,
            source_id=source_id,
            content=content,
            context=context,
            date=date,
            location=location
        )
        
        self.evidence[evidence_id] = evidence
        self.patterns[pattern_id].evidence_ids.append(evidence_id)
        self.patterns[pattern_id].frequency += 1
        
        self._save_data()
        return evidence
    
    def validate_pattern(self, pattern_id: str) -> Dict:
        """验证模式"""
        if pattern_id not in self.patterns:
            return {"error": "模式不存在"}
        
        pattern = self.patterns[pattern_id]
        validation_result = {
            "pattern_id": pattern_id,
            "checks": {},
            "passed": True,
            "recommendation": ""
        }
        
        # 频率检验
        freq_check = pattern.frequency >= 3
        validation_result["checks"]["frequency"] = {
            "passed": freq_check,
            "value": pattern.frequency,
            "required": 3
        }
        if not freq_check:
            validation_result["passed"] = False
        
        # 多情境检验
        context_check = len(pattern.contexts) >= 2
        validation_result["checks"]["contexts"] = {
            "passed": context_check,
            "value": len(pattern.contexts),
            "required": 2
        }
        if not context_check:
            validation_result["passed"] = False
        
        # 主位视角检验
        emic_check = len(pattern.emic_view) >= 50
        validation_result["checks"]["emic_view"] = {
            "passed": emic_check,
            "value": len(pattern.emic_view),
            "required": 50
        }
        if not emic_check:
            validation_result["passed"] = False
        
        # 深描检验
        thick_check = len(pattern.thick_description) >= 100
        validation_result["checks"]["thick_description"] = {
            "passed": thick_check,
            "value": len(pattern.thick_description),
            "required": 100
        }
        if not thick_check:
            validation_result["passed"] = False
        
        # 更新验证状态
        if validation_result["passed"]:
            if pattern.validation_status == "tentative":
                pattern.validation_status = "validated"
            elif pattern.validation_status == "validated":
                pattern.validation_status = "confirmed"
        validation_result["new_status"] = pattern.validation_status
        
        self._save_data()
        return validation_result
    
    def compare_patterns(self, pattern_id1: str, pattern_id2: str) -> Dict:
        """比较两个模式"""
        if pattern_id1 not in self.patterns or pattern_id2 not in self.patterns:
            return {"error": "模式不存在"}
        
        p1 = self.patterns[pattern_id1]
        p2 = self.patterns[pattern_id2]
        
        return {
            "pattern1": {"id": p1.id, "name": p1.name, "type": p1.pattern_type},
            "pattern2": {"id": p2.id, "name": p2.name, "type": p2.pattern_type},
            "same_type": p1.pattern_type == p2.pattern_type,
            "evidence_comparison": {
                "pattern1_count": len(p1.evidence_ids),
                "pattern2_count": len(p2.evidence_ids)
            },
            "shared_contexts": list(set(p1.contexts) & set(p2.contexts))
        }
    
    def get_patterns_by_type(self, pattern_type: str) -> List[CulturalPattern]:
        """按类型获取模式"""
        return [p for p in self.patterns.values() if p.pattern_type == pattern_type]
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        type_counts = Counter(p.pattern_type for p in self.patterns.values())
        status_counts = Counter(p.validation_status for p in self.patterns.values())
        
        return {
            "total_patterns": len(self.patterns),
            "total_evidence": len(self.evidence),
            "by_type": dict(type_counts),
            "by_status": dict(status_counts),
            "average_evidence_per_pattern": (
                len(self.evidence) / len(self.patterns) if self.patterns else 0
            )
        }
    
    def generate_report(self) -> str:
        """生成模式报告"""
        stats = self.get_statistics()
        
        report = "# 文化模式分析报告\n\n"
        report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        report += "## 统计概览\n\n"
        report += f"- 识别模式总数: {stats['total_patterns']}\n"
        report += f"- 收集证据总数: {stats['total_evidence']}\n"
        report += f"- 平均每模式证据数: {stats['average_evidence_per_pattern']:.1f}\n\n"
        
        report += "## 按类型分布\n\n"
        for ptype, count in stats['by_type'].items():
            report += f"- {self.PATTERN_TYPES.get(ptype, ptype)}: {count}\n"
        
        report += "\n## 按验证状态分布\n\n"
        for status, count in stats['by_status'].items():
            report += f"- {self.VALIDATION_LEVELS.get(status, status)}: {count}\n"
        
        report += "\n## 模式详情\n\n"
        for pattern in self.patterns.values():
            report += f"### {pattern.name} ({pattern.id})\n\n"
            report += f"**类型**: {self.PATTERN_TYPES.get(pattern.pattern_type, pattern.pattern_type)}\n\n"
            report += f"**状态**: {self.VALIDATION_LEVELS.get(pattern.validation_status, pattern.validation_status)}\n\n"
            report += f"**描述**: {pattern.description}\n\n"
            if pattern.emic_view:
                report += f"**主位视角**: {pattern.emic_view}\n\n"
            if pattern.etic_view:
                report += f"**客位分析**: {pattern.etic_view}\n\n"
            report += f"**证据数量**: {len(pattern.evidence_ids)}\n\n"
            report += "---\n\n"
        
        # 保存报告
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def export_to_json(self) -> Dict:
        """导出为JSON"""
        return {
            "patterns": {k: v.__dict__ for k, v in self.patterns.items()},
            "evidence": {k: v.__dict__ for k, v in self.evidence.items()},
            "statistics": self.get_statistics()
        }


def main():
    parser = argparse.ArgumentParser(description="文化模式分析工具")
    
    parser.add_argument("--init", action="store_true", help="初始化分析器")
    parser.add_argument("--add-pattern", type=str, help="添加模式名称")
    parser.add_argument("--type", type=str, default="behavior",
                       choices=["behavior", "language", "relationship", "space", "time"],
                       help="模式类型")
    parser.add_argument("--description", type=str, default="", help="模式描述")
    parser.add_argument("--add-evidence", type=str, help="模式ID(添加证据)")
    parser.add_argument("--source-type", type=str, help="证据来源类型")
    parser.add_argument("--source-id", type=str, help="来源ID")
    parser.add_argument("--content", type=str, help="证据内容")
    parser.add_argument("--validate", type=str, help="验证模式ID")
    parser.add_argument("--compare", type=str, nargs=2, help="比较两个模式")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    parser.add_argument("--report", action="store_true", help="生成报告")
    
    args = parser.parse_args()
    
    analyzer = CulturalPatternAnalyzer()
    
    if args.init:
        print("✅ 文化模式分析器已初始化")
        print(f"   数据目录: {analyzer.data_dir}")
    
    if args.add_pattern:
        pattern = analyzer.add_pattern(
            name=args.add_pattern,
            pattern_type=args.type,
            description=args.description
        )
        print(f"✅ 模式已添加: {pattern.id} - {pattern.name}")
        print(f"   类型: {analyzer.PATTERN_TYPES[pattern.pattern_type]}")
    
    if args.add_evidence and args.source_type and args.content:
        evidence = analyzer.add_evidence(
            pattern_id=args.add_evidence,
            source_type=args.source_type,
            source_id=args.source_id or "",
            content=args.content
        )
        if evidence:
            print(f"✅ 证据已添加: {evidence.id}")
            print(f"   关联模式: {evidence.pattern_id}")
        else:
            print(f"❌ 模式 {args.add_evidence} 不存在")
    
    if args.validate:
        result = analyzer.validate_pattern(args.validate)
        print(f"🔍 模式验证结果: {args.validate}")
        print(f"   通过: {result.get('passed', False)}")
        print(f"   新状态: {result.get('new_status', 'N/A')}")
        for check, details in result.get('checks', {}).items():
            status = "✓" if details['passed'] else "✗"
            print(f"   {status} {check}: {details['value']}/{details['required']}")
    
    if args.compare:
        result = analyzer.compare_patterns(args.compare[0], args.compare[1])
        if "error" not in result:
            print(f"📊 模式比较: {result['pattern1']['name']} vs {result['pattern2']['name']}")
            print(f"   同类型: {'是' if result['same_type'] else '否'}")
            print(f"   共享情境: {result['shared_contexts']}")
    
    if args.stats:
        stats = analyzer.get_statistics()
        print("📊 文化模式统计:")
        print(f"   模式总数: {stats['total_patterns']}")
        print(f"   证据总数: {stats['total_evidence']}")
        for ptype, count in stats['by_type'].items():
            print(f"   - {analyzer.PATTERN_TYPES[ptype]}: {count}")
    
    if args.report:
        report = analyzer.generate_report()
        print(report)
        print(f"\n📄 报告已保存: {analyzer.report_file}")


if __name__ == "__main__":
    main()
