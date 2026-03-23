#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Epoch Guide for Phenomenology Research
悬置与反思指导工具

使用方法:
    python epoch_guide.py --init
    python epoch_guide.py --add-preset "理论预设" "学生应该喜欢学习"
    python epoch_guide.py --reflect "今天访谈时我意识到..."
    python epoch_guide.py --check
    python epoch_guide.py --report
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
import argparse


@dataclass
class Preset:
    """预设数据结构"""
    id: str
    category: str  # theoretical, commonsense, personal, cultural, value
    content: str
    source: str = ""
    status: str = "identified"  # identified, bracketed, suspended, returned
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""


@dataclass
class Reflection:
    """反思记录数据结构"""
    id: str
    date: str
    context: str  # interview, analysis, writing, general
    content: str
    preset_triggered: str = ""
    insight: str = ""
    created_at: str = ""


class EpochGuide:
    """悬置与反思指导器"""
    
    PRESET_CATEGORIES = {
        "theoretical": "理论预设",
        "commonsense": "常识观念",
        "personal": "个人经验",
        "cultural": "文化规范",
        "value": "价值判断"
    }
    
    PRESET_STATUS = {
        "identified": "已识别",
        "bracketed": "已括置",
        "suspended": "已悬置",
        "returned": "已回归"
    }
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.data_dir = self.project_path / "phenomenology-workspace" / "epoch"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.presets_file = self.data_dir / "presets.json"
        self.reflections_file = self.data_dir / "reflections.json"
        self.report_file = self.data_dir / "epoch_report.md"
        
        self.presets: Dict[str, Preset] = {}
        self.reflections: List[Reflection] = []
        
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        if self.presets_file.exists():
            with open(self.presets_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for pid, pdata in data.items():
                    self.presets[pid] = Preset(**pdata)
        
        if self.reflections_file.exists():
            with open(self.reflections_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for rdata in data:
                    self.reflections.append(Reflection(**rdata))
    
    def _save_data(self):
        """保存数据"""
        with open(self.presets_file, 'w', encoding='utf-8') as f:
            json.dump({k: v.__dict__ for k, v in self.presets.items()}, 
                     f, ensure_ascii=False, indent=2)
        
        with open(self.reflections_file, 'w', encoding='utf-8') as f:
            json.dump([r.__dict__ for r in self.reflections], 
                     f, ensure_ascii=False, indent=2)
    
    def _generate_preset_id(self) -> str:
        """生成预设ID"""
        count = len(self.presets)
        return f"PRE{count+1:03d}"
    
    def _generate_reflection_id(self) -> str:
        """生成反思ID"""
        count = len(self.reflections)
        return f"REF{count+1:03d}"
    
    def add_preset(self, category: str, content: str, 
                  source: str = "") -> Preset:
        """添加预设"""
        now = datetime.now()
        preset_id = self._generate_preset_id()
        
        preset = Preset(
            id=preset_id,
            category=category,
            content=content,
            source=source,
            created_at=now.isoformat(),
            updated_at=now.isoformat()
        )
        
        self.presets[preset_id] = preset
        self._save_data()
        
        return preset
    
    def update_preset_status(self, preset_id: str, status: str,
                            notes: str = "") -> Optional[Preset]:
        """更新预设状态"""
        if preset_id not in self.presets:
            return None
        
        preset = self.presets[preset_id]
        preset.status = status
        if notes:
            preset.notes = notes
        preset.updated_at = datetime.now().isoformat()
        
        self._save_data()
        return preset
    
    def add_reflection(self, context: str, content: str,
                      preset_triggered: str = "",
                      insight: str = "") -> Reflection:
        """添加反思记录"""
        now = datetime.now()
        reflection_id = self._generate_reflection_id()
        
        reflection = Reflection(
            id=reflection_id,
            date=now.strftime("%Y-%m-%d"),
            context=context,
            content=content,
            preset_triggered=preset_triggered,
            insight=insight,
            created_at=now.isoformat()
        )
        
        self.reflections.append(reflection)
        self._save_data()
        
        return reflection
    
    def get_epoch_status(self) -> Dict:
        """获取悬置状态"""
        status_counts = {}
        for preset in self.presets.values():
            status_counts[preset.status] = status_counts.get(preset.status, 0) + 1
        
        return {
            "total_presets": len(self.presets),
            "total_reflections": len(self.reflections),
            "by_status": status_counts,
            "by_category": self._get_category_counts(),
            "suspension_rate": self._calculate_suspension_rate(),
            "reflection_frequency": self._get_reflection_frequency()
        }
    
    def _get_category_counts(self) -> Dict:
        """获取类别计数"""
        counts = {}
        for preset in self.presets.values():
            counts[preset.category] = counts.get(preset.category, 0) + 1
        return counts
    
    def _calculate_suspension_rate(self) -> float:
        """计算悬置率"""
        if not self.presets:
            return 0.0
        suspended = sum(1 for p in self.presets.values() 
                       if p.status in ["bracketed", "suspended"])
        return suspended / len(self.presets)
    
    def _get_reflection_frequency(self) -> Dict:
        """获取反思频率"""
        frequency = {}
        for reflection in self.reflections:
            frequency[reflection.date] = frequency.get(reflection.date, 0) + 1
        return frequency
    
    def check_epoch_quality(self) -> Dict:
        """检查悬置质量"""
        issues = []
        
        # 检查预设识别
        if len(self.presets) < 3:
            issues.append("预设识别不足，建议至少识别5个预设")
        
        # 检查悬置状态
        suspended = sum(1 for p in self.presets.values() 
                       if p.status in ["bracketed", "suspended"])
        if suspended < len(self.presets) * 0.8:
            issues.append("部分预设尚未悬置，建议将至少80%的预设括置或悬置")
        
        # 检查反思频率
        if len(self.reflections) < 5:
            issues.append("反思记录不足，建议持续记录反思")
        
        return {
            "quality_score": self._calculate_quality_score(),
            "issues": issues,
            "recommendations": self._get_recommendations()
        }
    
    def _calculate_quality_score(self) -> float:
        """计算质量分数"""
        score = 0
        
        # 预设识别(30分)
        preset_score = min(len(self.presets) * 3, 30)
        score += preset_score
        
        # 悬置状态(40分)
        suspension_rate = self._calculate_suspension_rate()
        score += suspension_rate * 40
        
        # 反思记录(30分)
        reflection_score = min(len(self.reflections) * 3, 30)
        score += reflection_score
        
        return score
    
    def _get_recommendations(self) -> List[str]:
        """获取建议"""
        recommendations = []
        
        if len(self.presets) < 5:
            recommendations.append("继续识别和记录预设")
        
        suspended = sum(1 for p in self.presets.values() 
                       if p.status in ["bracketed", "suspended"])
        if suspended < len(self.presets):
            recommendations.append("将已识别的预设括置或悬置")
        
        if len(self.reflections) < 10:
            recommendations.append("持续记录研究过程中的反思")
        
        return recommendations
    
    def generate_report(self) -> str:
        """生成报告"""
        status = self.get_epoch_status()
        quality = self.check_epoch_quality()
        
        report = "# 悬置与反思报告\n\n"
        report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        report += "## 悬置状态概览\n\n"
        report += f"- 识别预设总数: {status['total_presets']}\n"
        report += f"- 反思记录总数: {status['total_reflections']}\n"
        report += f"- 悬置率: {status['suspension_rate']*100:.1f}%\n\n"
        
        report += "## 按状态分布\n\n"
        for status_name, count in status['by_status'].items():
            report += f"- {self.PRESET_STATUS.get(status_name, status_name)}: {count}\n"
        
        report += "\n## 按类别分布\n\n"
        for category, count in status['by_category'].items():
            report += f"- {self.PRESET_CATEGORIES.get(category, category)}: {count}\n"
        
        report += "\n## 质量评估\n\n"
        report += f"- 质量分数: {quality['quality_score']:.1f}/100\n"
        
        if quality['issues']:
            report += "\n### 问题\n\n"
            for issue in quality['issues']:
                report += f"- {issue}\n"
        
        if quality['recommendations']:
            report += "\n### 建议\n\n"
            for rec in quality['recommendations']:
                report += f"- {rec}\n"
        
        report += "\n## 预设清单\n\n"
        for preset in self.presets.values():
            report += f"### {preset.id}: {preset.content}\n\n"
            report += f"- 类别: {self.PRESET_CATEGORIES.get(preset.category, preset.category)}\n"
            report += f"- 状态: {self.PRESET_STATUS.get(preset.status, preset.status)}\n"
            if preset.notes:
                report += f"- 备注: {preset.notes}\n"
            report += "\n"
        
        report += "## 反思记录\n\n"
        for reflection in self.reflections[-10:]:  # 最近10条
            report += f"### {reflection.date} ({reflection.context})\n\n"
            report += f"{reflection.content}\n\n"
            if reflection.insight:
                report += f"**洞察**: {reflection.insight}\n\n"
        
        # 保存报告
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report


def main():
    parser = argparse.ArgumentParser(description="悬置与反思指导工具")
    
    parser.add_argument("--init", action="store_true", help="初始化工具")
    parser.add_argument("--add-preset", type=str, nargs=2, 
                       help="添加预设 (类别 内容)")
    parser.add_argument("--source", type=str, default="", help="预设来源")
    parser.add_argument("--update-status", type=str, nargs=2,
                       help="更新预设状态 (ID 状态)")
    parser.add_argument("--notes", type=str, default="", help="备注")
    parser.add_argument("--reflect", type=str, help="添加反思记录")
    parser.add_argument("--context", type=str, default="general",
                       help="反思情境")
    parser.add_argument("--insight", type=str, default="", help="洞察")
    parser.add_argument("--status", action="store_true", help="显示悬置状态")
    parser.add_argument("--check", action="store_true", help="检查悬置质量")
    parser.add_argument("--report", action="store_true", help="生成报告")
    
    args = parser.parse_args()
    
    guide = EpochGuide()
    
    if args.init:
        print("✅ 悬置与反思工具已初始化")
        print(f"   数据目录: {guide.data_dir}")
    
    if args.add_preset:
        preset = guide.add_preset(
            category=args.add_preset[0],
            content=args.add_preset[1],
            source=args.source
        )
        print(f"✅ 预设已添加: {preset.id}")
        print(f"   类别: {guide.PRESET_CATEGORIES.get(preset.category, preset.category)}")
        print(f"   内容: {preset.content}")
    
    if args.update_status:
        preset = guide.update_preset_status(
            preset_id=args.update_status[0],
            status=args.update_status[1],
            notes=args.notes
        )
        if preset:
            print(f"✅ 预设状态已更新: {preset.id}")
            print(f"   新状态: {guide.PRESET_STATUS.get(preset.status, preset.status)}")
        else:
            print(f"❌ 预设 {args.update_status[0]} 不存在")
    
    if args.reflect:
        reflection = guide.add_reflection(
            context=args.context,
            content=args.reflect,
            insight=args.insight
        )
        print(f"✅ 反思已记录: {reflection.id}")
        print(f"   日期: {reflection.date}")
        print(f"   情境: {reflection.context}")
    
    if args.status:
        status = guide.get_epoch_status()
        print("📊 悬置状态:")
        print(f"   预设总数: {status['total_presets']}")
        print(f"   反思总数: {status['total_reflections']}")
        print(f"   悬置率: {status['suspension_rate']*100:.1f}%")
    
    if args.check:
        quality = guide.check_epoch_quality()
        print(f"🔍 悬置质量检查:")
        print(f"   质量分数: {quality['quality_score']:.1f}/100")
        if quality['issues']:
            print("   问题:")
            for issue in quality['issues']:
                print(f"   - {issue}")
    
    if args.report:
        report = guide.generate_report()
        print(report)
        print(f"\n📄 报告已保存: {guide.report_file}")


if __name__ == "__main__":
    main()
