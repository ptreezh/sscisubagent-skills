#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Key Informant Tracker for Ethnography Research
关键报道人管理工具

使用方法:
    python key_informant_tracker.py --init
    python key_informant_tracker.py --add "王大爷" --type "cultural-expert"
    python key_informant_tracker.py --record-interview KI001 "2024-01-15" 90
    python key_informant_tracker.py --add-consent KI001 "signed"
    python key_informant_tracker.py --report
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
from collections import Counter
import hashlib
import argparse


@dataclass
class Interview:
    """访谈记录"""
    id: str
    date: str
    duration: int  # 分钟
    type: str  # semi-structured, oral-history, focus-group
    topics: List[str] = field(default_factory=list)
    notes: str = ""
    recording_consent: bool = False
    follow_up_needed: bool = False


@dataclass
class KeyInformant:
    """关键报道人数据结构"""
    id: str
    pseudonym: str  # 化名
    informant_type: str  # cultural-expert, marginal, ordinary, critic
    characteristics: str = ""
    expertise_areas: List[str] = field(default_factory=list)
    contact_info: str = ""  # 加密存储
    interviews: List[Interview] = field(default_factory=list)
    consent_status: str = "pending"  # pending, verbal, signed, declined
    consent_date: str = ""
    relationship_level: int = 1  # 1-5, 5最高
    reliability_rating: int = 3  # 1-5
    notes: str = ""
    created_at: str = ""
    updated_at: str = ""


class KeyInformantTracker:
    """关键报道人管理器"""
    
    INFORMANT_TYPES = {
        "cultural-expert": "文化专家",
        "marginal": "边缘人",
        "ordinary": "普通成员",
        "critic": "批评者"
    }
    
    CONSENT_STATUS = {
        "pending": "待确认",
        "verbal": "口头同意",
        "signed": "签署同意",
        "declined": "拒绝"
    }
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.data_dir = self.project_path / "ethnography-workspace" / "informants"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.informants_file = self.data_dir / "informants.json"
        self.report_file = self.data_dir / "informant_report.md"
        
        self.informants: Dict[str, KeyInformant] = {}
        
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        if self.informants_file.exists():
            with open(self.informants_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for iid, idata in data.items():
                    interviews = [Interview(**i) for i in idata.pop('interviews', [])]
                    informant = KeyInformant(**idata)
                    informant.interviews = interviews
                    self.informants[iid] = informant
    
    def _save_data(self):
        """保存数据"""
        data = {}
        for iid, informant in self.informants.items():
            idata = informant.__dict__.copy()
            idata['interviews'] = [i.__dict__ for i in informant.interviews]
            data[iid] = idata
        
        with open(self.informants_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _generate_id(self) -> str:
        """生成ID"""
        count = len(self.informants)
        return f"KI{count+1:03d}"
    
    def _hash_contact(self, contact: str) -> str:
        """加密联系方式"""
        return hashlib.sha256(contact.encode()).hexdigest()[:16]
    
    def add_informant(self, pseudonym: str, informant_type: str,
                     characteristics: str = "",
                     expertise_areas: List[str] = None,
                     contact_info: str = "") -> KeyInformant:
        """添加报道人"""
        now = datetime.now()
        informant_id = self._generate_id()
        
        informant = KeyInformant(
            id=informant_id,
            pseudonym=pseudonym,
            informant_type=informant_type,
            characteristics=characteristics,
            expertise_areas=expertise_areas or [],
            contact_info=self._hash_contact(contact_info) if contact_info else "",
            created_at=now.isoformat(),
            updated_at=now.isoformat()
        )
        
        self.informants[informant_id] = informant
        self._save_data()
        
        return informant
    
    def update_informant(self, informant_id: str, **kwargs) -> Optional[KeyInformant]:
        """更新报道人信息"""
        if informant_id not in self.informants:
            return None
        
        informant = self.informants[informant_id]
        for key, value in kwargs.items():
            if key == 'contact_info' and value:
                value = self._hash_contact(value)
            if hasattr(informant, key):
                setattr(informant, key, value)
        
        informant.updated_at = datetime.now().isoformat()
        self._save_data()
        
        return informant
    
    def record_interview(self, informant_id: str, date: str, 
                        duration: int, interview_type: str = "semi-structured",
                        topics: List[str] = None,
                        notes: str = "",
                        recording_consent: bool = False) -> Optional[Interview]:
        """记录访谈"""
        if informant_id not in self.informants:
            return None
        
        interview_count = len(self.informants[informant_id].interviews)
        interview_id = f"{informant_id}-IV{interview_count+1:02d}"
        
        interview = Interview(
            id=interview_id,
            date=date,
            duration=duration,
            type=interview_type,
            topics=topics or [],
            notes=notes,
            recording_consent=recording_consent
        )
        
        self.informants[informant_id].interviews.append(interview)
        self.informants[informant_id].updated_at = datetime.now().isoformat()
        
        self._save_data()
        return interview
    
    def add_consent(self, informant_id: str, consent_status: str,
                   consent_date: str = None) -> Optional[KeyInformant]:
        """添加同意状态"""
        if informant_id not in self.informants:
            return None
        
        informant = self.informants[informant_id]
        informant.consent_status = consent_status
        informant.consent_date = consent_date or datetime.now().strftime("%Y-%m-%d")
        informant.updated_at = datetime.now().isoformat()
        
        self._save_data()
        return informant
    
    def get_informant(self, informant_id: str) -> Optional[KeyInformant]:
        """获取报道人"""
        return self.informants.get(informant_id)
    
    def get_by_type(self, informant_type: str) -> List[KeyInformant]:
        """按类型获取"""
        return [i for i in self.informants.values() if i.informant_type == informant_type]
    
    def get_by_consent(self, consent_status: str) -> List[KeyInformant]:
        """按同意状态获取"""
        return [i for i in self.informants.values() if i.consent_status == consent_status]
    
    def get_statistics(self) -> Dict:
        """获取统计"""
        type_counts = Counter(i.informant_type for i in self.informants.values())
        consent_counts = Counter(i.consent_status for i in self.informants.values())
        
        total_interviews = sum(len(i.interviews) for i in self.informants.values())
        total_duration = sum(
            iv.duration for i in self.informants.values() for iv in i.interviews
        )
        
        return {
            "total_informants": len(self.informants),
            "total_interviews": total_interviews,
            "total_duration_hours": total_duration / 60,
            "by_type": dict(type_counts),
            "by_consent": dict(consent_counts),
            "average_interviews": total_interviews / len(self.informants) if self.informants else 0,
            "average_relationship": sum(i.relationship_level for i in self.informants.values()) / len(self.informants) if self.informants else 0
        }
    
    def generate_report(self) -> str:
        """生成报告"""
        stats = self.get_statistics()
        
        report = "# 关键报道人管理报告\n\n"
        report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        report += "## 统计概览\n\n"
        report += f"- 报道人总数: {stats['total_informants']}\n"
        report += f"- 访谈总数: {stats['total_interviews']}\n"
        report += f"- 总访谈时长: {stats['total_duration_hours']:.1f}小时\n\n"
        
        report += "## 按类型分布\n\n"
        for itype, count in stats['by_type'].items():
            report += f"- {self.INFORMANT_TYPES.get(itype, itype)}: {count}\n"
        
        report += "\n## 按同意状态分布\n\n"
        for status, count in stats['by_consent'].items():
            report += f"- {self.CONSENT_STATUS.get(status, status)}: {count}\n"
        
        report += "\n## 报道人详情\n\n"
        for informant in self.informants.values():
            report += f"### {informant.pseudonym} ({informant.id})\n\n"
            report += f"**类型**: {self.INFORMANT_TYPES.get(informant.informant_type, informant.informant_type)}\n\n"
            report += f"**特点**: {informant.characteristics}\n\n"
            report += f"**专长领域**: {', '.join(informant.expertise_areas) or '未记录'}\n\n"
            report += f"**同意状态**: {self.CONSENT_STATUS.get(informant.consent_status, informant.consent_status)}\n\n"
            report += f"**关系等级**: {informant.relationship_level}/5\n\n"
            report += f"**访谈次数**: {len(informant.interviews)}\n\n"
            if informant.interviews:
                report += "**访谈记录**:\n"
                for iv in informant.interviews:
                    report += f"- {iv.date}: {iv.duration}分钟 ({iv.type})\n"
            report += "\n---\n\n"
        
        # 保存报告
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report
    
    def check_ethics_compliance(self) -> Dict:
        """检查伦理合规"""
        pending = self.get_by_consent("pending")
        declined = self.get_by_consent("declined")
        consented = len([i for i in self.informants.values() 
                        if i.consent_status in ["verbal", "signed"]])
        
        issues = []
        if pending:
            issues.append(f"{len(pending)}位报道人尚未获得同意")
        if declined:
            issues.append(f"{len(declined)}位报道人已拒绝参与")
        
        return {
            "compliant": len(pending) == 0,
            "consented": consented,
            "pending": len(pending),
            "declined": len(declined),
            "issues": issues
        }


def main():
    parser = argparse.ArgumentParser(description="关键报道人管理工具")
    
    parser.add_argument("--init", action="store_true", help="初始化管理器")
    parser.add_argument("--add", type=str, help="添加报道人(化名)")
    parser.add_argument("--type", type=str, default="ordinary",
                       choices=["cultural-expert", "marginal", "ordinary", "critic"],
                       help="报道人类型")
    parser.add_argument("--characteristics", type=str, default="", help="特点描述")
    parser.add_argument("--expertise", type=str, nargs='+', help="专长领域")
    parser.add_argument("--record-interview", type=str, help="报道人ID")
    parser.add_argument("--date", type=str, help="访谈日期")
    parser.add_argument("--duration", type=int, help="访谈时长(分钟)")
    parser.add_argument("--interview-type", type=str, default="semi-structured",
                       help="访谈类型")
    parser.add_argument("--add-consent", type=str, nargs=2, 
                       help="添加同意状态 (ID 状态)")
    parser.add_argument("--update-relationship", type=str, nargs=2,
                       help="更新关系等级 (ID 等级)")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    parser.add_argument("--report", action="store_true", help="生成报告")
    parser.add_argument("--ethics-check", action="store_true", help="伦理合规检查")
    
    args = parser.parse_args()
    
    tracker = KeyInformantTracker()
    
    if args.init:
        print("✅ 关键报道人管理器已初始化")
        print(f"   数据目录: {tracker.data_dir}")
    
    if args.add:
        informant = tracker.add_informant(
            pseudonym=args.add,
            informant_type=args.type,
            characteristics=args.characteristics,
            expertise_areas=args.expertise
        )
        print(f"✅ 报道人已添加: {informant.id} - {informant.pseudonym}")
        print(f"   类型: {tracker.INFORMANT_TYPES[informant.informant_type]}")
    
    if args.record_interview and args.date and args.duration:
        interview = tracker.record_interview(
            informant_id=args.record_interview,
            date=args.date,
            duration=args.duration,
            interview_type=args.interview_type
        )
        if interview:
            print(f"✅ 访谈已记录: {interview.id}")
            print(f"   日期: {interview.date}")
            print(f"   时长: {interview.duration}分钟")
        else:
            print(f"❌ 报道人 {args.record_interview} 不存在")
    
    if args.add_consent:
        informant = tracker.add_consent(args.add_consent[0], args.add_consent[1])
        if informant:
            print(f"✅ 同意状态已更新: {informant.id}")
            print(f"   状态: {tracker.CONSENT_STATUS[informant.consent_status]}")
    
    if args.update_relationship:
        informant = tracker.update_informant(
            args.update_relationship[0],
            relationship_level=int(args.update_relationship[1])
        )
        if informant:
            print(f"✅ 关系等级已更新: {informant.id} - {informant.relationship_level}/5")
    
    if args.stats:
        stats = tracker.get_statistics()
        print("📊 关键报道人统计:")
        print(f"   总数: {stats['total_informants']}")
        print(f"   访谈总数: {stats['total_interviews']}")
        print(f"   总时长: {stats['total_duration_hours']:.1f}小时")
        for itype, count in stats['by_type'].items():
            print(f"   - {tracker.INFORMANT_TYPES[itype]}: {count}")
    
    if args.report:
        report = tracker.generate_report()
        print(report)
        print(f"\n📄 报告已保存: {tracker.report_file}")
    
    if args.ethics_check:
        result = tracker.check_ethics_compliance()
        print("📋 伦理合规检查:")
        print(f"   合规: {'是' if result['compliant'] else '否'}")
        print(f"   已同意: {result['consented']}")
        print(f"   待确认: {result['pending']}")
        print(f"   已拒绝: {result['declined']}")
        if result['issues']:
            print("   问题:")
            for issue in result['issues']:
                print(f"   - {issue}")


if __name__ == "__main__":
    main()
