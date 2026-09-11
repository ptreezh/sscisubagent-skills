#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fieldnote Manager for Ethnography Research
田野笔记管理工具

使用方法:
    python fieldnote_manager.py --init
    python fieldnote_manager.py --add "田野笔记内容" --type descriptive
    python fieldnote_manager.py --code FN001 --tags "仪式,宗教"
    python fieldnote_manager.py --search "关键词"
    python fieldnote_manager.py --export
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field
from pathlib import Path
from collections import Counter
import argparse


@dataclass
class Fieldnote:
    """田野笔记数据结构"""
    id: str
    date: str
    time: str
    location: str
    note_type: str  # descriptive, methodological, theoretical, emotional
    content: str
    context: str = ""
    analysis: str = ""
    feeling: str = ""
    follow_up: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    participants: List[str] = field(default_factory=list)
    created_at: str = ""
    updated_at: str = ""


class FieldnoteManager:
    """田野笔记管理器"""
    
    NOTE_TYPES = {
        "descriptive": "描述性笔记",
        "methodological": "方法论笔记",
        "theoretical": "理论笔记",
        "emotional": "情感笔记"
    }
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.data_dir = self.project_path / "ethnography-workspace" / "fieldnotes"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.notes_file = self.data_dir / "fieldnotes.json"
        self.codes_file = self.data_dir / "codes.json"
        self.index_file = self.data_dir / "index.json"
        
        self.notes: Dict[str, Fieldnote] = {}
        self.codes: Dict[str, List[str]] = {}  # code -> note_ids
        self.index: Dict[str, List[str]] = {}  # keyword -> note_ids
        
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        if self.notes_file.exists():
            with open(self.notes_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for note_id, note_data in data.items():
                    self.notes[note_id] = Fieldnote(**note_data)
        
        if self.codes_file.exists():
            with open(self.codes_file, 'r', encoding='utf-8') as f:
                self.codes = json.load(f)
        
        if self.index_file.exists():
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.index = json.load(f)
    
    def _save_data(self):
        """保存数据"""
        with open(self.notes_file, 'w', encoding='utf-8') as f:
            json.dump({k: v.__dict__ for k, v in self.notes.items()}, 
                     f, ensure_ascii=False, indent=2)
        
        with open(self.codes_file, 'w', encoding='utf-8') as f:
            json.dump(self.codes, f, ensure_ascii=False, indent=2)
        
        with open(self.index_file, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, ensure_ascii=False, indent=2)
    
    def _generate_id(self) -> str:
        """生成笔记ID"""
        today = datetime.now().strftime("%Y%m%d")
        count = len([n for n in self.notes if n.startswith(f"FN{today}")])
        return f"FN{today}-{count+1:03d}"
    
    def _update_index(self, note_id: str, content: str, tags: List[str]):
        """更新索引"""
        # 提取关键词
        keywords = set(tags)
        for word in content.split():
            if len(word) >= 2:
                keywords.add(word)
        
        for keyword in keywords:
            if keyword not in self.index:
                self.index[keyword] = []
            if note_id not in self.index[keyword]:
                self.index[keyword].append(note_id)
    
    def add_note(self, content: str, note_type: str = "descriptive",
                 location: str = "", context: str = "", 
                 analysis: str = "", feeling: str = "",
                 participants: List[str] = None) -> Fieldnote:
        """添加田野笔记"""
        now = datetime.now()
        note_id = self._generate_id()
        
        note = Fieldnote(
            id=note_id,
            date=now.strftime("%Y-%m-%d"),
            time=now.strftime("%H:%M:%S"),
            location=location,
            note_type=note_type,
            content=content,
            context=context,
            analysis=analysis,
            feeling=feeling,
            participants=participants or [],
            created_at=now.isoformat(),
            updated_at=now.isoformat()
        )
        
        self.notes[note_id] = note
        self._update_index(note_id, content, note.tags)
        self._save_data()
        
        return note
    
    def get_note(self, note_id: str) -> Optional[Fieldnote]:
        """获取笔记"""
        return self.notes.get(note_id)
    
    def update_note(self, note_id: str, **kwargs) -> Optional[Fieldnote]:
        """更新笔记"""
        if note_id not in self.notes:
            return None
        
        note = self.notes[note_id]
        for key, value in kwargs.items():
            if hasattr(note, key):
                setattr(note, key, value)
        
        note.updated_at = datetime.now().isoformat()
        self._save_data()
        
        return note
    
    def code_note(self, note_id: str, codes: List[str]) -> bool:
        """为笔记编码"""
        if note_id not in self.notes:
            return False
        
        for code in codes:
            if code not in self.codes:
                self.codes[code] = []
            if note_id not in self.codes[code]:
                self.codes[code].append(note_id)
        
        # 更新笔记的标签
        note = self.notes[note_id]
        note.tags = list(set(note.tags + codes))
        note.updated_at = datetime.now().isoformat()
        
        self._save_data()
        return True
    
    def search(self, query: str, note_type: str = None) -> List[Fieldnote]:
        """搜索笔记"""
        results = []
        query_lower = query.lower()
        
        for note in self.notes.values():
            # 类型过滤
            if note_type and note.note_type != note_type:
                continue
            
            # 内容搜索
            if (query_lower in note.content.lower() or
                query_lower in note.context.lower() or
                query_lower in note.analysis.lower() or
                query in note.tags):
                results.append(note)
        
        # 按日期排序
        results.sort(key=lambda x: x.date, reverse=True)
        return results
    
    def get_by_code(self, code: str) -> List[Fieldnote]:
        """按编码获取笔记"""
        if code not in self.codes:
            return []
        
        return [self.notes[nid] for nid in self.codes[code] if nid in self.notes]
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        type_counts = Counter(n.note_type for n in self.notes.values())
        
        return {
            "total_notes": len(self.notes),
            "by_type": dict(type_counts),
            "total_codes": len(self.codes),
            "date_range": self._get_date_range(),
            "top_codes": self._get_top_codes(10)
        }
    
    def _get_date_range(self) -> Dict:
        """获取日期范围"""
        if not self.notes:
            return {"start": None, "end": None}
        
        dates = [n.date for n in self.notes.values()]
        return {
            "start": min(dates),
            "end": max(dates)
        }
    
    def _get_top_codes(self, n: int = 10) -> List[tuple]:
        """获取最常用编码"""
        code_counts = [(code, len(notes)) for code, notes in self.codes.items()]
        code_counts.sort(key=lambda x: x[1], reverse=True)
        return code_counts[:n]
    
    def export_to_markdown(self, output_path: str = None) -> str:
        """导出为Markdown"""
        output = "# 田野笔记汇总\n\n"
        
        for note_type, type_name in self.NOTE_TYPES.items():
            notes = [n for n in self.notes.values() if n.note_type == note_type]
            if notes:
                output += f"## {type_name}\n\n"
                for note in sorted(notes, key=lambda x: x.date):
                    output += f"### {note.id} - {note.date}\n\n"
                    output += f"**地点**: {note.location}\n\n"
                    output += f"**在场者**: {', '.join(note.participants) or '无记录'}\n\n"
                    output += f"**内容**:\n{note.content}\n\n"
                    if note.context:
                        output += f"**情境**: {note.context}\n\n"
                    if note.analysis:
                        output += f"**分析**: {note.analysis}\n\n"
                    if note.feeling:
                        output += f"**感受**: {note.feeling}\n\n"
                    if note.tags:
                        output += f"**标签**: {', '.join(note.tags)}\n\n"
                    output += "---\n\n"
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(output)
        
        return output
    
    def generate_report(self) -> str:
        """生成笔记报告"""
        stats = self.get_statistics()
        
        report = "# 田野笔记统计报告\n\n"
        report += f"- 总笔记数: {stats['total_notes']}\n"
        report += f"- 编码数量: {stats['total_codes']}\n"
        report += f"- 日期范围: {stats['date_range']['start']} 至 {stats['date_range']['end']}\n\n"
        
        report += "## 按类型分布\n\n"
        for note_type, count in stats['by_type'].items():
            type_name = self.NOTE_TYPES.get(note_type, note_type)
            report += f"- {type_name}: {count}\n"
        
        report += "\n## 常用编码\n\n"
        for code, count in stats['top_codes']:
            report += f"- {code}: {count}次\n"
        
        return report


def main():
    parser = argparse.ArgumentParser(description="田野笔记管理工具")
    
    parser.add_argument("--init", action="store_true", help="初始化笔记系统")
    parser.add_argument("--add", type=str, help="添加笔记内容")
    parser.add_argument("--type", type=str, default="descriptive", 
                       choices=["descriptive", "methodological", "theoretical", "emotional"],
                       help="笔记类型")
    parser.add_argument("--location", type=str, default="", help="地点")
    parser.add_argument("--code", type=str, help="笔记ID(用于编码)")
    parser.add_argument("--tags", type=str, nargs='+', help="编码标签")
    parser.add_argument("--search", type=str, help="搜索关键词")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    parser.add_argument("--export", action="store_true", help="导出Markdown")
    parser.add_argument("--report", action="store_true", help="生成报告")
    
    args = parser.parse_args()
    
    manager = FieldnoteManager()
    
    if args.init:
        print("✅ 田野笔记系统已初始化")
        print(f"   数据目录: {manager.data_dir}")
    
    if args.add:
        note = manager.add_note(
            content=args.add,
            note_type=args.type,
            location=args.location
        )
        print(f"✅ 笔记已添加: {note.id}")
        print(f"   类型: {manager.NOTE_TYPES[note.note_type]}")
        print(f"   日期: {note.date}")
    
    if args.code and args.tags:
        if manager.code_note(args.code, args.tags):
            print(f"✅ 笔记 {args.code} 已编码: {', '.join(args.tags)}")
        else:
            print(f"❌ 笔记 {args.code} 不存在")
    
    if args.search:
        results = manager.search(args.search)
        print(f"🔍 找到 {len(results)} 条笔记:")
        for note in results[:10]:
            print(f"   - {note.id}: {note.date} | {note.content[:50]}...")
    
    if args.stats:
        stats = manager.get_statistics()
        print("📊 田野笔记统计:")
        print(f"   总数: {stats['total_notes']}")
        for note_type, count in stats['by_type'].items():
            print(f"   - {manager.NOTE_TYPES[note_type]}: {count}")
    
    if args.export:
        output_path = str(manager.data_dir / "fieldnotes_export.md")
        manager.export_to_markdown(output_path)
        print(f"📄 笔记已导出: {output_path}")
    
    if args.report:
        report = manager.generate_report()
        print(report)


if __name__ == "__main__":
    main()
