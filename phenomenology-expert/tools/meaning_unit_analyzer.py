#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Meaning Unit Analyzer for Phenomenology Research
意义单元分析工具

使用方法:
    python meaning_unit_analyzer.py --init
    python meaning_unit_analyzer.py --add-participant "P01" "王女士"
    python meaning_unit_analyzer.py --add-description P01 "当我走进..."
    python meaning_unit_analyzer.py --analyze P01
    python meaning_unit_analyzer.py --report
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from pathlib import Path
from collections import Counter
import argparse


@dataclass
class MeaningUnit:
    """意义单元数据结构"""
    id: str
    participant_id: str
    original_phrase: str  # 原文短语
    meaning_unit: str     # 转译后的意义单元
    theme: str = ""       # 主题
    notes: str = ""
    created_at: str = ""


@dataclass
class Description:
    """描述数据结构"""
    id: str
    participant_id: str
    content: str
    source: str = "interview"  # interview, writing, observation
    date: str = ""
    meaning_units: List[str] = field(default_factory=list)


@dataclass
class Participant:
    """参与者数据结构"""
    id: str
    pseudonym: str
    characteristics: str = ""
    descriptions: List[str] = field(default_factory=list)


class MeaningUnitAnalyzer:
    """意义单元分析器"""
    
    THEME_COLORS = {
        "身体体验": "🔴",
        "情感体验": "🟠",
        "认知体验": "🟡",
        "关系体验": "🟢",
        "空间体验": "🔵",
        "时间体验": "🟣",
        "身份体验": "🟤",
        "其他": "⚪"
    }
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.data_dir = self.project_path / "phenomenology-workspace" / "analysis"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.participants_file = self.data_dir / "participants.json"
        self.descriptions_file = self.data_dir / "descriptions.json"
        self.units_file = self.data_dir / "meaning_units.json"
        self.report_file = self.data_dir / "analysis_report.md"
        
        self.participants: Dict[str, Participant] = {}
        self.descriptions: Dict[str, Description] = {}
        self.meaning_units: Dict[str, MeaningUnit] = {}
        
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        if self.participants_file.exists():
            with open(self.participants_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for pid, pdata in data.items():
                    self.participants[pid] = Participant(**pdata)
        
        if self.descriptions_file.exists():
            with open(self.descriptions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for did, ddata in data.items():
                    self.descriptions[did] = Description(**ddata)
        
        if self.units_file.exists():
            with open(self.units_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for uid, udata in data.items():
                    self.meaning_units[uid] = MeaningUnit(**udata)
    
    def _save_data(self):
        """保存数据"""
        with open(self.participants_file, 'w', encoding='utf-8') as f:
            json.dump({k: v.__dict__ for k, v in self.participants.items()}, 
                     f, ensure_ascii=False, indent=2)
        
        with open(self.descriptions_file, 'w', encoding='utf-8') as f:
            json.dump({k: v.__dict__ for k, v in self.descriptions.items()}, 
                     f, ensure_ascii=False, indent=2)
        
        with open(self.units_file, 'w', encoding='utf-8') as f:
            json.dump({k: v.__dict__ for k, v in self.meaning_units.items()}, 
                     f, ensure_ascii=False, indent=2)
    
    def add_participant(self, participant_id: str, pseudonym: str,
                       characteristics: str = "") -> Participant:
        """添加参与者"""
        participant = Participant(
            id=participant_id,
            pseudonym=pseudonym,
            characteristics=characteristics
        )
        
        self.participants[participant_id] = participant
        self._save_data()
        
        return participant
    
    def add_description(self, participant_id: str, content: str,
                       source: str = "interview",
                       date: str = "") -> Optional[Description]:
        """添加描述"""
        if participant_id not in self.participants:
            return None
        
        desc_id = f"{participant_id}-D{len(self.descriptions)+1:02d}"
        
        description = Description(
            id=desc_id,
            participant_id=participant_id,
            content=content,
            source=source,
            date=date or datetime.now().strftime("%Y-%m-%d")
        )
        
        self.descriptions[desc_id] = description
        self.participants[participant_id].descriptions.append(desc_id)
        
        self._save_data()
        return description
    
    def add_meaning_unit(self, description_id: str, original_phrase: str,
                        meaning_unit: str, theme: str = "") -> Optional[MeaningUnit]:
        """添加意义单元"""
        if description_id not in self.descriptions:
            return None
        
        desc = self.descriptions[description_id]
        unit_id = f"{desc.participant_id}-MU{len(self.meaning_units)+1:03d}"
        
        unit = MeaningUnit(
            id=unit_id,
            participant_id=desc.participant_id,
            original_phrase=original_phrase,
            meaning_unit=meaning_unit,
            theme=theme,
            created_at=datetime.now().isoformat()
        )
        
        self.meaning_units[unit_id] = unit
        desc.meaning_units.append(unit_id)
        
        self._save_data()
        return unit
    
    def analyze_text(self, text: str) -> List[Dict]:
        """分析文本，建议意义单元"""
        # 简单的分句分析
        sentences = re.split(r'[。！？；\n]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        suggestions = []
        for i, sentence in enumerate(sentences):
            # 尝试识别关键词
            keywords = self._extract_keywords(sentence)
            suggested_theme = self._suggest_theme(keywords)
            
            suggestions.append({
                "index": i + 1,
                "original": sentence,
                "keywords": keywords,
                "suggested_theme": suggested_theme
            })
        
        return suggestions
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取
        emotion_words = ["紧张", "害怕", "高兴", "焦虑", "担心", "放松", "平静"]
        body_words = ["身体", "手", "心", "头", "眼", "感觉"]
        time_words = ["时间", "等待", "突然", "一直", "开始", "结束"]
        space_words = ["这里", "那里", "走进", "离开", "靠近"]
        
        keywords = []
        for word in emotion_words + body_words + time_words + space_words:
            if word in text:
                keywords.append(word)
        
        return keywords
    
    def _suggest_theme(self, keywords: List[str]) -> str:
        """建议主题"""
        if any(k in ["紧张", "害怕", "高兴", "焦虑", "担心"] for k in keywords):
            return "情感体验"
        if any(k in ["身体", "手", "心", "头", "眼"] for k in keywords):
            return "身体体验"
        if any(k in ["时间", "等待", "突然"] for k in keywords):
            return "时间体验"
        if any(k in ["这里", "那里", "走进", "离开"] for k in keywords):
            return "空间体验"
        return "其他"
    
    def get_themes(self) -> Dict[str, List[str]]:
        """获取主题聚类"""
        themes = {}
        for unit in self.meaning_units.values():
            if unit.theme:
                if unit.theme not in themes:
                    themes[unit.theme] = []
                themes[unit.theme].append(unit.id)
        
        return themes
    
    def get_participant_units(self, participant_id: str) -> List[MeaningUnit]:
        """获取参与者的意义单元"""
        return [u for u in self.meaning_units.values() 
                if u.participant_id == participant_id]
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        theme_counts = Counter(u.theme for u in self.meaning_units.values())
        
        return {
            "total_participants": len(self.participants),
            "total_descriptions": len(self.descriptions),
            "total_units": len(self.meaning_units),
            "units_per_participant": len(self.meaning_units) / len(self.participants) if self.participants else 0,
            "theme_distribution": dict(theme_counts)
        }
    
    def generate_report(self) -> str:
        """生成分析报告"""
        stats = self.get_statistics()
        themes = self.get_themes()
        
        report = "# 意义单元分析报告\n\n"
        report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        report += "## 统计概览\n\n"
        report += f"- 参与者数: {stats['total_participants']}\n"
        report += f"- 描述总数: {stats['total_descriptions']}\n"
        report += f"- 意义单元数: {stats['total_units']}\n"
        report += f"- 平均每人单元数: {stats['units_per_participant']:.1f}\n\n"
        
        report += "## 主题分布\n\n"
        for theme, units in themes.items():
            emoji = self.THEME_COLORS.get(theme, "⚪")
            report += f"### {emoji} {theme} ({len(units)}个单元)\n\n"
            for unit_id in units[:5]:  # 显示前5个
                unit = self.meaning_units[unit_id]
                report += f"- **{unit.original_phrase[:30]}...**\n"
                report += f"  - 转译: {unit.meaning_unit}\n"
            if len(units) > 5:
                report += f"  - ...还有{len(units)-5}个单元\n"
            report += "\n"
        
        report += "## 参与者分析\n\n"
        for participant in self.participants.values():
            units = self.get_participant_units(participant.id)
            report += f"### {participant.pseudonym} ({participant.id})\n\n"
            report += f"- 意义单元数: {len(units)}\n"
            
            # 主题分布
            p_themes = Counter(u.theme for u in units)
            report += "- 主题分布:\n"
            for theme, count in p_themes.most_common():
                report += f"  - {theme}: {count}\n"
            report += "\n"
        
        # 保存报告
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report


def main():
    parser = argparse.ArgumentParser(description="意义单元分析工具")
    
    parser.add_argument("--init", action="store_true", help="初始化工具")
    parser.add_argument("--add-participant", type=str, nargs=2,
                       help="添加参与者 (ID 化名)")
    parser.add_argument("--add-description", type=str, nargs=2,
                       help="添加描述 (参与者ID 内容)")
    parser.add_argument("--add-unit", type=str, nargs=4,
                       help="添加意义单元 (描述ID 原文 转译 主题)")
    parser.add_argument("--analyze", type=str, help="分析描述ID")
    parser.add_argument("--themes", action="store_true", help="显示主题聚类")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    parser.add_argument("--report", action="store_true", help="生成报告")
    
    args = parser.parse_args()
    
    analyzer = MeaningUnitAnalyzer()
    
    if args.init:
        print("✅ 意义单元分析工具已初始化")
        print(f"   数据目录: {analyzer.data_dir}")
    
    if args.add_participant:
        participant = analyzer.add_participant(
            participant_id=args.add_participant[0],
            pseudonym=args.add_participant[1]
        )
        print(f"✅ 参与者已添加: {participant.id} - {participant.pseudonym}")
    
    if args.add_description:
        desc = analyzer.add_description(
            participant_id=args.add_description[0],
            content=args.add_description[1]
        )
        if desc:
            print(f"✅ 描述已添加: {desc.id}")
        else:
            print(f"❌ 参与者 {args.add_description[0]} 不存在")
    
    if args.add_unit:
        unit = analyzer.add_meaning_unit(
            description_id=args.add_unit[0],
            original_phrase=args.add_unit[1],
            meaning_unit=args.add_unit[2],
            theme=args.add_unit[3]
        )
        if unit:
            print(f"✅ 意义单元已添加: {unit.id}")
            print(f"   原文: {unit.original_phrase[:30]}...")
            print(f"   转译: {unit.meaning_unit}")
            print(f"   主题: {unit.theme}")
    
    if args.analyze:
        if args.analyze in analyzer.descriptions:
            desc = analyzer.descriptions[args.analyze]
            suggestions = analyzer.analyze_text(desc.content)
            print(f"📝 描述分析建议: {args.analyze}")
            for s in suggestions:
                print(f"   {s['index']}. {s['original'][:40]}...")
                print(f"      关键词: {s['keywords']}")
                print(f"      建议主题: {s['suggested_theme']}")
        else:
            print(f"❌ 描述 {args.analyze} 不存在")
    
    if args.themes:
        themes = analyzer.get_themes()
        print("📊 主题聚类:")
        for theme, units in themes.items():
            emoji = analyzer.THEME_COLORS.get(theme, "⚪")
            print(f"   {emoji} {theme}: {len(units)}个单元")
    
    if args.stats:
        stats = analyzer.get_statistics()
        print("📊 分析统计:")
        print(f"   参与者数: {stats['total_participants']}")
        print(f"   描述总数: {stats['total_descriptions']}")
        print(f"   意义单元数: {stats['total_units']}")
    
    if args.report:
        report = analyzer.generate_report()
        print(report)
        print(f"\n📄 报告已保存: {analyzer.report_file}")


if __name__ == "__main__":
    main()
