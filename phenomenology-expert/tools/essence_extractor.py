#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Essence Extractor for Phenomenology Research
本质结构提取工具

使用方法:
    python essence_extractor.py --init
    python essence_extractor.py --create-experience "考试焦虑"
    python essence_extractor.py --add-feature EA001 "心跳加速" "偶然"
    python essence_extractor.py --variation EA001 "心跳加速"
    python essence_extractor.py --essence EA001
    python essence_extractor.py --report
"""

import json
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
from collections import Counter
import argparse


@dataclass
class Feature:
    """特征数据结构"""
    id: str
    experience_id: str
    name: str
    description: str = ""
    status: str = "pending"  # pending, necessary, accidental, uncertain
    variation_results: List[Dict] = field(default_factory=list)
    notes: str = ""


@dataclass
class Experience:
    """体验数据结构"""
    id: str
    name: str
    description: str = ""
    features: List[str] = field(default_factory=list)
    essence_structure: str = ""
    created_at: str = ""
    updated_at: str = ""


class EssenceExtractor:
    """本质结构提取器"""
    
    FEATURE_STATUS = {
        "pending": "待检验",
        "necessary": "必要特征",
        "accidental": "偶然特征",
        "uncertain": "不确定"
    }
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.data_dir = self.project_path / "phenomenology-workspace" / "essence"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.experiences_file = self.data_dir / "experiences.json"
        self.features_file = self.data_dir / "features.json"
        self.report_file = self.data_dir / "essence_report.md"
        
        self.experiences: Dict[str, Experience] = {}
        self.features: Dict[str, Feature] = {}
        
        self._load_data()
    
    def _load_data(self):
        """加载数据"""
        if self.experiences_file.exists():
            with open(self.experiences_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for eid, edata in data.items():
                    self.experiences[eid] = Experience(**edata)
        
        if self.features_file.exists():
            with open(self.features_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for fid, fdata in data.items():
                    self.features[fid] = Feature(**fdata)
    
    def _save_data(self):
        """保存数据"""
        with open(self.experiences_file, 'w', encoding='utf-8') as f:
            json.dump({k: v.__dict__ for k, v in self.experiences.items()}, 
                     f, ensure_ascii=False, indent=2)
        
        with open(self.features_file, 'w', encoding='utf-8') as f:
            json.dump({k: v.__dict__ for k, v in self.features.items()}, 
                     f, ensure_ascii=False, indent=2)
    
    def _generate_experience_id(self) -> str:
        """生成体验ID"""
        count = len(self.experiences)
        return f"EA{count+1:03d}"
    
    def _generate_feature_id(self, experience_id: str) -> str:
        """生成特征ID"""
        count = len([f for f in self.features.values() 
                    if f.experience_id == experience_id])
        return f"{experience_id}-F{count+1:02d}"
    
    def create_experience(self, name: str, description: str = "") -> Experience:
        """创建体验"""
        now = datetime.now()
        exp_id = self._generate_experience_id()
        
        experience = Experience(
            id=exp_id,
            name=name,
            description=description,
            created_at=now.isoformat(),
            updated_at=now.isoformat()
        )
        
        self.experiences[exp_id] = experience
        self._save_data()
        
        return experience
    
    def add_feature(self, experience_id: str, name: str,
                   description: str = "") -> Optional[Feature]:
        """添加特征"""
        if experience_id not in self.experiences:
            return None
        
        feature_id = self._generate_feature_id(experience_id)
        
        feature = Feature(
            id=feature_id,
            experience_id=experience_id,
            name=name,
            description=description
        )
        
        self.features[feature_id] = feature
        self.experiences[experience_id].features.append(feature_id)
        self.experiences[experience_id].updated_at = datetime.now().isoformat()
        
        self._save_data()
        return feature
    
    def record_variation(self, feature_id: str, question: str,
                        answer: str, is_necessary: bool) -> Optional[Feature]:
        """记录想象变异结果"""
        if feature_id not in self.features:
            return None
        
        feature = self.features[feature_id]
        
        variation = {
            "question": question,
            "answer": answer,
            "is_necessary": is_necessary,
            "timestamp": datetime.now().isoformat()
        }
        
        feature.variation_results.append(variation)
        
        # 更新状态
        if is_necessary:
            feature.status = "necessary"
        else:
            feature.status = "accidental"
        
        self._save_data()
        return feature
    
    def update_feature_status(self, feature_id: str, status: str,
                             notes: str = "") -> Optional[Feature]:
        """更新特征状态"""
        if feature_id not in self.features:
            return None
        
        feature = self.features[feature_id]
        feature.status = status
        if notes:
            feature.notes = notes
        
        self._save_data()
        return feature
    
    def get_essence_structure(self, experience_id: str) -> Dict:
        """获取本质结构"""
        if experience_id not in self.experiences:
            return {"error": "体验不存在"}
        
        experience = self.experiences[experience_id]
        
        necessary = []
        accidental = []
        pending = []
        
        for fid in experience.features:
            feature = self.features[fid]
            if feature.status == "necessary":
                necessary.append(feature)
            elif feature.status == "accidental":
                accidental.append(feature)
            else:
                pending.append(feature)
        
        return {
            "experience": experience.name,
            "necessary_features": [{"name": f.name, "description": f.description} for f in necessary],
            "accidental_features": [{"name": f.name, "description": f.description} for f in accidental],
            "pending_features": [{"name": f.name, "description": f.description} for f in pending],
            "essence_description": self._generate_essence_description(necessary)
        }
    
    def _generate_essence_description(self, necessary_features: List[Feature]) -> str:
        """生成本质描述"""
        if not necessary_features:
            return "尚未确定必要特征"
        
        description = f"本质结构包含以下必要特征：\n"
        for i, f in enumerate(necessary_features, 1):
            description += f"{i}. {f.name}"
            if f.description:
                description += f"：{f.description}"
            description += "\n"
        
        return description
    
    def set_essence_structure(self, experience_id: str, 
                             essence: str) -> Optional[Experience]:
        """设置本质结构"""
        if experience_id not in self.experiences:
            return None
        
        self.experiences[experience_id].essence_structure = essence
        self.experiences[experience_id].updated_at = datetime.now().isoformat()
        
        self._save_data()
        return self.experiences[experience_id]
    
    def get_statistics(self) -> Dict:
        """获取统计"""
        status_counts = Counter(f.status for f in self.features.values())
        
        return {
            "total_experiences": len(self.experiences),
            "total_features": len(self.features),
            "features_per_experience": len(self.features) / len(self.experiences) if self.experiences else 0,
            "status_distribution": dict(status_counts)
        }
    
    def generate_report(self) -> str:
        """生成报告"""
        stats = self.get_statistics()
        
        report = "# 本质结构提取报告\n\n"
        report += f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        
        report += "## 统计概览\n\n"
        report += f"- 体验总数: {stats['total_experiences']}\n"
        report += f"- 特征总数: {stats['total_features']}\n"
        report += f"- 平均每体验特征数: {stats['features_per_experience']:.1f}\n\n"
        
        report += "## 特征状态分布\n\n"
        for status, count in stats['status_distribution'].items():
            report += f"- {self.FEATURE_STATUS.get(status, status)}: {count}\n"
        
        report += "\n## 本质结构\n\n"
        for experience in self.experiences.values():
            essence = self.get_essence_structure(experience.id)
            
            report += f"### {experience.name} ({experience.id})\n\n"
            
            if essence.get("necessary_features"):
                report += "**必要特征**:\n"
                for f in essence["necessary_features"]:
                    report += f"- {f['name']}"
                    if f['description']:
                        report += f": {f['description']}"
                    report += "\n"
                report += "\n"
            
            if essence.get("accidental_features"):
                report += "**偶然特征**:\n"
                for f in essence["accidental_features"]:
                    report += f"- {f['name']}\n"
                report += "\n"
            
            if essence.get("pending_features"):
                report += "**待检验特征**:\n"
                for f in essence["pending_features"]:
                    report += f"- {f['name']}\n"
                report += "\n"
            
            if experience.essence_structure:
                report += f"**本质描述**:\n{experience.essence_structure}\n\n"
            
            report += "---\n\n"
        
        # 保存报告
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        return report


def main():
    parser = argparse.ArgumentParser(description="本质结构提取工具")
    
    parser.add_argument("--init", action="store_true", help="初始化工具")
    parser.add_argument("--create-experience", type=str, help="创建体验名称")
    parser.add_argument("--description", type=str, default="", help="描述")
    parser.add_argument("--add-feature", type=str, nargs=2,
                       help="添加特征 (体验ID 特征名)")
    parser.add_argument("--feature-desc", type=str, default="", help="特征描述")
    parser.add_argument("--variation", type=str, nargs=2,
                       help="想象变异 (特征ID 问题)")
    parser.add_argument("--answer", type=str, help="变异答案")
    parser.add_argument("--necessary", type=str, choices=["yes", "no"],
                       help="是否必要特征")
    parser.add_argument("--update-status", type=str, nargs=2,
                       help="更新特征状态 (特征ID 状态)")
    parser.add_argument("--essence", type=str, help="显示本质结构(体验ID)")
    parser.add_argument("--set-essence", type=str, nargs=2,
                       help="设置本质结构 (体验ID 描述)")
    parser.add_argument("--stats", action="store_true", help="显示统计")
    parser.add_argument("--report", action="store_true", help="生成报告")
    
    args = parser.parse_args()
    
    extractor = EssenceExtractor()
    
    if args.init:
        print("✅ 本质结构提取工具已初始化")
        print(f"   数据目录: {extractor.data_dir}")
    
    if args.create_experience:
        exp = extractor.create_experience(
            name=args.create_experience,
            description=args.description
        )
        print(f"✅ 体验已创建: {exp.id} - {exp.name}")
    
    if args.add_feature:
        feature = extractor.add_feature(
            experience_id=args.add_feature[0],
            name=args.add_feature[1],
            description=args.feature_desc
        )
        if feature:
            print(f"✅ 特征已添加: {feature.id} - {feature.name}")
        else:
            print(f"❌ 体验 {args.add_feature[0]} 不存在")
    
    if args.variation and args.answer and args.necessary:
        is_necessary = args.necessary == "yes"
        feature = extractor.record_variation(
            feature_id=args.variation[0],
            question=args.variation[1],
            answer=args.answer,
            is_necessary=is_necessary
        )
        if feature:
            print(f"✅ 变异已记录: {feature.id}")
            print(f"   问题: {args.variation[1]}")
            print(f"   答案: {args.answer}")
            print(f"   结果: {'必要特征' if is_necessary else '偶然特征'}")
    
    if args.update_status:
        feature = extractor.update_feature_status(
            feature_id=args.update_status[0],
            status=args.update_status[1]
        )
        if feature:
            print(f"✅ 特征状态已更新: {feature.id}")
            print(f"   新状态: {extractor.FEATURE_STATUS.get(feature.status, feature.status)}")
    
    if args.essence:
        essence = extractor.get_essence_structure(args.essence)
        if "error" not in essence:
            print(f"📊 本质结构: {essence['experience']}")
            print(f"\n必要特征 ({len(essence['necessary_features'])}个):")
            for f in essence['necessary_features']:
                print(f"   - {f['name']}")
            print(f"\n偶然特征 ({len(essence['accidental_features'])}个):")
            for f in essence['accidental_features']:
                print(f"   - {f['name']}")
            if essence['essence_description']:
                print(f"\n{essence['essence_description']}")
        else:
            print(f"❌ {essence['error']}")
    
    if args.set_essence:
        exp = extractor.set_essence_structure(
            experience_id=args.set_essence[0],
            essence=args.set_essence[1]
        )
        if exp:
            print(f"✅ 本质结构已设置: {exp.id}")
    
    if args.stats:
        stats = extractor.get_statistics()
        print("📊 本质结构统计:")
        print(f"   体验总数: {stats['total_experiences']}")
        print(f"   特征总数: {stats['total_features']}")
        for status, count in stats['status_distribution'].items():
            print(f"   - {extractor.FEATURE_STATUS.get(status, status)}: {count}")
    
    if args.report:
        report = extractor.generate_report()
        print(report)
        print(f"\n📄 报告已保存: {extractor.report_file}")


if __name__ == "__main__":
    main()
