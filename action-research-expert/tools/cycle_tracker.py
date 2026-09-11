#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action Research Cycle Tracker
追踪行动研究多轮循环的进展和数据

使用方法:
    python cycle_tracker.py --init "项目名称"
    python cycle_tracker.py --start-cycle 1
    python cycle_tracker.py --record --stage plan --data "诊断结果..."
    python cycle_tracker.py --end-cycle 1
    python cycle_tracker.py --report
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse


class CycleTracker:
    """行动研究循环追踪器"""
    
    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.data_dir = self.project_path / "action-research-workspace" / "cycles"
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.current_file = self.data_dir / "tracker_state.json"
        self.state = self._load_state()
    
    def _load_state(self) -> Dict:
        """加载当前状态"""
        if self.current_file.exists():
            with open(self.current_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "project_name": "",
            "created_at": None,
            "current_cycle": 0,
            "cycles": [],
            "metadata": {}
        }
    
    def _save_state(self):
        """保存当前状态"""
        with open(self.current_file, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def init_project(self, project_name: str, metadata: Optional[Dict] = None):
        """初始化项目"""
        self.state["project_name"] = project_name
        self.state["created_at"] = datetime.now().isoformat()
        if metadata:
            self.state["metadata"] = metadata
        self._save_state()
        print(f"✅ 项目 '{project_name}' 初始化成功")
    
    def start_cycle(self, cycle_num: int, plan: Optional[str] = None):
        """开始新一轮循环"""
        cycle_data = {
            "cycle_number": cycle_num,
            "started_at": datetime.now().isoformat(),
            "ended_at": None,
            "stages": {
                "plan": {"data": plan or "", "completed": False, "timestamp": None},
                "act": {"data": "", "completed": False, "timestamp": None},
                "observe": {"data": "", "completed": False, "timestamp": None},
                "reflect": {"data": "", "completed": False, "timestamp": None}
            },
            "outcomes": {},
            "learnings": []
        }
        
        # 确保cycles列表足够长
        while len(self.state["cycles"]) < cycle_num:
            self.state["cycles"].append(None)
        
        self.state["cycles"][cycle_num - 1] = cycle_data
        self.state["current_cycle"] = cycle_num
        self._save_state()
        print(f"✅ 第 {cycle_num} 轮循环开始")
    
    def record_stage(self, stage: str, data: str):
        """记录阶段数据"""
        stage = stage.lower()
        valid_stages = ["plan", "act", "observe", "reflect"]
        
        if stage not in valid_stages:
            print(f"❌ 无效的阶段: {stage}。有效阶段: {valid_stages}")
            return
        
        current = self.state["current_cycle"]
        if current == 0:
            print("❌ 没有活动的循环。请先使用 --start-cycle 开始一轮循环")
            return
        
        cycle = self.state["cycles"][current - 1]
        cycle["stages"][stage]["data"] = data
        cycle["stages"][stage]["completed"] = True
        cycle["stages"][stage]["timestamp"] = datetime.now().isoformat()
        
        self._save_state()
        print(f"✅ 第 {current} 轮循环 - {stage.upper()} 阶段数据已记录")
    
    def end_cycle(self, cycle_num: int, outcomes: Optional[Dict] = None, 
                  learnings: Optional[List[str]] = None):
        """结束循环"""
        cycle = self.state["cycles"][cycle_num - 1]
        cycle["ended_at"] = datetime.now().isoformat()
        
        if outcomes:
            cycle["outcomes"] = outcomes
        if learnings:
            cycle["learnings"] = learnings
        
        self._save_state()
        
        # 生成循环报告
        report_path = self.data_dir / f"cycle_{cycle_num}_report.md"
        self._generate_cycle_report(cycle_num, report_path)
        
        print(f"✅ 第 {cycle_num} 轮循环结束")
        print(f"📄 报告已生成: {report_path}")
    
    def _generate_cycle_report(self, cycle_num: int, output_path: Path):
        """生成循环报告"""
        cycle = self.state["cycles"][cycle_num - 1]
        
        report = f"""# 第 {cycle_num} 轮循环报告

## 基本信息
- **开始时间**: {cycle['started_at']}
- **结束时间**: {cycle['ended_at']}
- **项目**: {self.state['project_name']}

## 四阶段记录

### 1. 计划 (Plan)
{cycle['stages']['plan']['data'] or '未记录'}

### 2. 行动 (Act)
{cycle['stages']['act']['data'] or '未记录'}

### 3. 观察 (Observe)
{cycle['stages']['observe']['data'] or '未记录'}

### 4. 反思 (Reflect)
{cycle['stages']['reflect']['data'] or '未记录'}

## 成果
```json
{json.dumps(cycle.get('outcomes', {}), ensure_ascii=False, indent=2)}
```

## 学习要点
"""
        for learning in cycle.get('learnings', []):
            report += f"- {learning}\n"
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)
    
    def generate_summary_report(self) -> str:
        """生成总体报告"""
        report = f"""# 行动研究项目总结报告

## 项目信息
- **项目名称**: {self.state['project_name']}
- **创建时间**: {self.state['created_at']}
- **总循环数**: {len([c for c in self.state['cycles'] if c])}

## 循环概览

| 轮次 | 开始时间 | 结束时间 | 状态 |
|------|----------|----------|------|
"""
        for i, cycle in enumerate(self.state['cycles'], 1):
            if cycle:
                status = "完成" if cycle['ended_at'] else "进行中"
                report += f"| {i} | {cycle['started_at'][:10]} | {cycle['ended_at'][:10] if cycle['ended_at'] else '-'} | {status} |\n"
        
        report += "\n## 各轮学习要点汇总\n\n"
        
        for i, cycle in enumerate(self.state['cycles'], 1):
            if cycle and cycle.get('learnings'):
                report += f"### 第 {i} 轮\n"
                for learning in cycle['learnings']:
                    report += f"- {learning}\n"
                report += "\n"
        
        # 保存报告
        report_path = self.data_dir.parent / "summary_report.md"
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"📄 总结报告已生成: {report_path}")
        return report
    
    def check_completeness(self) -> Dict[str, Any]:
        """检查循环完整性"""
        issues = []
        completed_stages = 0
        total_stages = 0
        
        for i, cycle in enumerate(self.state['cycles'], 1):
            if not cycle:
                continue
            
            for stage, data in cycle['stages'].items():
                total_stages += 1
                if data['completed']:
                    completed_stages += 1
                else:
                    issues.append(f"第 {i} 轮 - {stage.upper()} 阶段未完成")
            
            if not cycle.get('learnings'):
                issues.append(f"第 {i} 轮 - 缺少学习要点")
        
        completeness = completed_stages / total_stages if total_stages > 0 else 0
        
        return {
            "completeness": f"{completeness:.1%}",
            "completed_stages": completed_stages,
            "total_stages": total_stages,
            "issues": issues,
            "quality_score": self._calculate_quality()
        }
    
    def _calculate_quality(self) -> int:
        """计算质量分数(1-5)"""
        if not self.state['cycles']:
            return 0
        
        score = 0
        completed_cycles = [c for c in self.state['cycles'] if c and c['ended_at']]
        
        # 循环数量
        if len(completed_cycles) >= 3:
            score += 2
        elif len(completed_cycles) >= 2:
            score += 1
        
        # 数据完整性
        for cycle in completed_cycles:
            stages_complete = sum(1 for s in cycle['stages'].values() if s['completed'])
            if stages_complete == 4:
                score += 0.5
        
        # 反思深度
        for cycle in completed_cycles:
            if cycle.get('learnings') and len(cycle['learnings']) >= 3:
                score += 0.5
        
        return min(5, int(score))


def main():
    parser = argparse.ArgumentParser(description="行动研究循环追踪器")
    
    parser.add_argument("--init", type=str, help="初始化项目，提供项目名称")
    parser.add_argument("--start-cycle", type=int, help="开始指定轮次的循环")
    parser.add_argument("--record", action="store_true", help="记录阶段数据")
    parser.add_argument("--stage", type=str, help="阶段名称(plan/act/observe/reflect)")
    parser.add_argument("--data", type=str, help="阶段数据")
    parser.add_argument("--end-cycle", type=int, help="结束指定轮次的循环")
    parser.add_argument("--outcomes", type=str, help="循环成果(JSON格式)")
    parser.add_argument("--learnings", type=str, nargs='+', help="学习要点")
    parser.add_argument("--report", action="store_true", help="生成总结报告")
    parser.add_argument("--check", action="store_true", help="检查完整性")
    
    args = parser.parse_args()
    
    tracker = CycleTracker()
    
    if args.init:
        tracker.init_project(args.init)
    
    elif args.start_cycle:
        tracker.start_cycle(args.start_cycle)
    
    elif args.record and args.stage and args.data:
        tracker.record_stage(args.stage, args.data)
    
    elif args.end_cycle:
        outcomes = json.loads(args.outcomes) if args.outcomes else None
        tracker.end_cycle(args.end_cycle, outcomes, args.learnings)
    
    elif args.report:
        tracker.generate_summary_report()
    
    elif args.check:
        result = tracker.check_completeness()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
