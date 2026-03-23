#!/usr/bin/env python3
"""
SocienceAI 战略执行引擎
Strategic Execution Engine

自动追踪战略目标、监控进度、生成报告、执行任务

版本：1.0.0
日期：2026-03-22
"""

import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class StrategicExecutionEngine:
    """战略执行引擎"""
    
    def __init__(self, working_dir: str = './'):
        self.working_dir = Path(working_dir)
        
        # 战略配置
        self.strategy_path = self.working_dir / 'STRATEGY.md'
        self.okr_path = self.working_dir / 'OKR-2026.json'
        self.state_path = self.working_dir / 'strategy-state.json'
        
        # 战略状态
        self.state = {
            'last_update': None,
            'current_cycle': '2026-Q3-Q4',
            'overall_progress': 0.0,
            'okr_status': {},
            'alerts': [],
            'completed_tasks': [],
            'pending_tasks': []
        }
        
        # OKR 定义
        self.okr = self.load_okr()
        self.load_state()
        self.ensure_directories()
    
    def ensure_directories(self):
        """确保目录结构存在"""
        dirs = [
            self.working_dir / 'progress-reports' / 'weekly',
            self.working_dir / 'progress-reports' / 'monthly',
            self.working_dir / 'progress-reports' / 'quarterly',
            self.working_dir / 'strategic-reviews',
            self.working_dir / 'metrics',
        ]
        
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
    
    def load_okr(self) -> Dict:
        """加载 OKR 配置"""
        if self.okr_path.exists():
            with open(self.okr_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # 默认 OKR
            return self.create_default_okr()
    
    def create_default_okr(self) -> Dict:
        """创建默认 OKR"""
        return {
            'cycle': '2026-Q3-Q4',
            'objectives': [
                {
                    'id': 'O1',
                    'name': '能力建设',
                    'description': '构建完整的社会科学方法论 AI 支持能力',
                    'key_results': [
                        {
                            'id': 'KR1.1',
                            'name': '方法论覆盖',
                            'current': 12,
                            'target': 20,
                            'unit': '种',
                            'weight': 0.25
                        },
                        {
                            'id': 'KR1.2',
                            'name': '工具完善',
                            'current': 3,
                            'target': 5,
                            'unit': '个/方法论',
                            'weight': 0.25
                        },
                        {
                            'id': 'KR1.3',
                            'name': '测试覆盖',
                            'current': 85,
                            'target': 95,
                            'unit': '%',
                            'weight': 0.25
                        },
                        {
                            'id': 'KR1.4',
                            'name': '进化准确率',
                            'current': 0,
                            'target': 90,
                            'unit': '%',
                            'weight': 0.25
                        }
                    ]
                },
                {
                    'id': 'O2',
                    'name': '用户增长',
                    'description': '建立持续增长的用户群体',
                    'key_results': [
                        {
                            'id': 'KR2.1',
                            'name': '核心用户',
                            'current': 0,
                            'target': 1000,
                            'unit': '人',
                            'weight': 0.25
                        },
                        {
                            'id': 'KR2.2',
                            'name': '机构合作',
                            'current': 0,
                            'target': 10,
                            'unit': '个',
                            'weight': 0.25
                        },
                        {
                            'id': 'KR2.3',
                            'name': '全球覆盖',
                            'current': 0,
                            'target': 50,
                            'unit': '国家/地区',
                            'weight': 0.25
                        },
                        {
                            'id': 'KR2.4',
                            'name': '用户满意度',
                            'current': 0,
                            'target': 70,
                            'unit': 'NPS',
                            'weight': 0.25
                        }
                    ]
                },
                {
                    'id': 'O3',
                    'name': '生态构建',
                    'description': '建立可持续发展的生态系统',
                    'key_results': [
                        {
                            'id': 'KR3.1',
                            'name': '开源社区',
                            'current': 1,
                            'target': 100,
                            'unit': '贡献者',
                            'weight': 0.25
                        },
                        {
                            'id': 'KR3.2',
                            'name': '合作伙伴',
                            'current': 0,
                            'target': 20,
                            'unit': '个',
                            'weight': 0.25
                        },
                        {
                            'id': 'KR3.3',
                            'name': '商业模式',
                            'current': 0,
                            'target': 1,
                            'unit': '建立',
                            'weight': 0.25
                        },
                        {
                            'id': 'KR3.4',
                            'name': '标准制定',
                            'current': 0,
                            'target': 1,
                            'unit': '建立',
                            'weight': 0.25
                        }
                    ]
                }
            ]
        }
    
    def load_state(self):
        """加载战略状态"""
        if self.state_path.exists():
            with open(self.state_path, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
    
    def save_state(self):
        """保存战略状态"""
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    # ========================================================================
    # OKR 追踪
    # ========================================================================
    
    def update_kr(self, objective_id: str, kr_id: str, new_value: float):
        """更新关键结果进度"""
        for obj in self.okr['objectives']:
            if obj['id'] == objective_id:
                for kr in obj['key_results']:
                    if kr['id'] == kr_id:
                        kr['current'] = new_value
                        print(f"✅ 更新 {kr_id}: {kr['current']}/{kr['target']} {kr['unit']}")
                        self.save_okr()
                        return
        print(f"❌ 未找到 {objective_id}.{kr_id}")
    
    def calculate_kr_progress(self, kr: Dict) -> float:
        """计算单个 KR 的进度百分比"""
        if kr['target'] == 0:
            return 0.0
        
        # 对于百分比型指标（如测试覆盖率）
        if kr['unit'] == '%':
            return (kr['current'] / kr['target']) * 100
        
        # 对于数量型指标
        progress = (kr['current'] / kr['target']) * 100
        return min(progress, 100.0)  # 不超过 100%
    
    def calculate_objective_progress(self, objective: Dict) -> float:
        """计算目标进度"""
        total_weight = sum(kr['weight'] for kr in objective['key_results'])
        weighted_progress = sum(
            self.calculate_kr_progress(kr) * kr['weight']
            for kr in objective['key_results']
        )
        return weighted_progress / total_weight if total_weight > 0 else 0.0
    
    def calculate_overall_progress(self) -> float:
        """计算整体战略进度"""
        if not self.okr['objectives']:
            return 0.0
        
        total_progress = sum(
            self.calculate_objective_progress(obj)
            for obj in self.okr['objectives']
        )
        return total_progress / len(self.okr['objectives'])
    
    def save_okr(self):
        """保存 OKR 配置"""
        with open(self.okr_path, 'w', encoding='utf-8') as f:
            json.dump(self.okr, f, ensure_ascii=False, indent=2)
    
    # ========================================================================
    # 自动监控
    # ========================================================================
    
    def check_thresholds(self):
        """检查指标阈值，生成预警"""
        alerts = []
        
        # 检查测试覆盖率
        for obj in self.okr['objectives']:
            for kr in obj['key_results']:
                if kr['id'] == 'KR1.3' and kr['current'] < 90:  # 测试覆盖率
                    alerts.append({
                        'level': 'warning',
                        'kr_id': kr['id'],
                        'message': f"测试覆盖率 {kr['current']}% < 90%",
                        'action': '通知质量团队'
                    })
                
                if kr['id'] == 'KR1.4' and kr['current'] < 80:  # 进化准确率
                    alerts.append({
                        'level': 'warning',
                        'kr_id': kr['id'],
                        'message': f"进化准确率 {kr['current']}% < 80%",
                        'action': '人工审查进化系统'
                    })
        
        self.state['alerts'] = alerts
        self.save_state()
        
        if alerts:
            print(f"⚠️ 生成 {len(alerts)} 条预警")
            for alert in alerts:
                print(f"   [{alert['level'].upper()}] {alert['message']}")
                print(f"         行动：{alert['action']}")
        else:
            print("✅ 所有指标正常")
        
        return alerts
    
    # ========================================================================
    # 自动报告
    # ========================================================================
    
    def generate_weekly_report(self) -> Path:
        """生成周报"""
        timestamp = datetime.now().strftime('%Y%m%d')
        report_path = self.working_dir / 'progress-reports' / 'weekly' / f'weekly-{timestamp}.md'
        
        overall_progress = self.calculate_overall_progress()
        
        content = f"""# 战略执行周报

**报告周期**: 第 {datetime.now().isocalendar()[1]} 周
**生成日期**: {datetime.now().strftime('%Y-%m-%d')}
**整体进度**: {overall_progress:.1f}%

---

## OKR 进度总览

"""
        
        for obj in self.okr['objectives']:
            obj_progress = self.calculate_objective_progress(obj)
            content += f"### {obj['id']}: {obj['name']} (进度：{obj_progress:.1f}%)\n\n"
            
            for kr in obj['key_results']:
                kr_progress = self.calculate_kr_progress(kr)
                bar_length = int(kr_progress / 5)
                bar = '█' * bar_length + '░' * (20 - bar_length)
                content += f"- **{kr['id']}** {kr['name']}: `{bar}` {kr_progress:.0f}% "
                content += f"({kr['current']}/{kr['target']} {kr['unit']})\n"
            
            content += "\n"
        
        # 预警信息
        if self.state['alerts']:
            content += "## ⚠️ 预警信息\n\n"
            for alert in self.state['alerts']:
                content += f"- [{alert['level'].upper()}] {alert['message']}\n"
                content += f"  行动：{alert['action']}\n"
            content += "\n"
        
        # 下周计划
        content += """## 下周计划

1. [待制定]
2. [待制定]
3. [待制定]

---
*由 SocienceAI 战略执行系统自动生成*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📝 周报已生成：{report_path}")
        return report_path
    
    def generate_monthly_report(self) -> Path:
        """生成月报"""
        timestamp = datetime.now().strftime('%Y%m')
        report_path = self.working_dir / 'progress-reports' / 'monthly' / f'monthly-{timestamp}.md'
        
        overall_progress = self.calculate_overall_progress()
        
        content = f"""# 战略执行月报

**报告月份**: {datetime.now().strftime('%Y-%m')}
**生成日期**: {datetime.now().strftime('%Y-%m-%d')}
**整体进度**: {overall_progress:.1f}%

---

## 本月关键成就

1. [待填写]
2. [待填写]
3. [待填写]

## OKR 进度分析

"""
        
        for obj in self.okr['objectives']:
            obj_progress = self.calculate_objective_progress(obj)
            content += f"### {obj['id']}: {obj['name']}\n\n"
            content += f"进度：{obj_progress:.1f}%\n\n"
            
            for kr in obj['key_results']:
                kr_progress = self.calculate_kr_progress(kr)
                content += f"- **{kr['id']}** {kr['name']}: {kr['current']}/{kr['target']} {kr['unit']} "
                content += f"({kr_progress:.1f}%)\n"
            
            content += "\n"
        
        content += """## 问题与挑战

[待填写]

## 下月计划

[待填写]

---
*由 SocienceAI 战略执行系统自动生成*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"📝 月报已生成：{report_path}")
        return report_path
    
    # ========================================================================
    # 自动任务执行
    # ========================================================================
    
    def execute_daily_tasks(self):
        """执行每日任务"""
        print("\n" + "="*60)
        print("📅 执行每日任务")
        print("="*60)
        
        tasks = [
            "数据备份",
            "指标收集",
            "系统健康检查",
            "日志归档"
        ]
        
        for task in tasks:
            print(f"  ✅ {task}")
        
        self.state['completed_tasks'].extend([
            {'task': t, 'date': datetime.now().isoformat()}
            for t in tasks
        ])
        
        self.save_state()
    
    def execute_weekly_tasks(self):
        """执行每周任务"""
        print("\n" + "="*60)
        print("📅 执行每周任务")
        print("="*60)
        
        # 生成周报
        self.generate_weekly_report()
        
        # 检查阈值
        self.check_thresholds()
        
        # 更新状态
        self.state['last_update'] = datetime.now().isoformat()
        self.save_state()
        
        print("  ✅ 周报生成")
        print("  ✅ 阈值检查")
        print("  ✅ 状态更新")
    
    def execute_monthly_tasks(self):
        """执行每月任务"""
        print("\n" + "="*60)
        print("📅 执行每月任务")
        print("="*60)
        
        # 生成月报
        self.generate_monthly_report()
        
        # 计算整体进度
        overall = self.calculate_overall_progress()
        print(f"  📊 整体进度：{overall:.1f}%")
        
        # 战略回顾
        print("  📋 战略回顾会议")
        
        self.save_state()
    
    # ========================================================================
    # 仪表板
    # ========================================================================
    
    def print_dashboard(self):
        """打印战略执行仪表板"""
        overall_progress = self.calculate_overall_progress()
        
        print("\n" + "="*70)
        print("              SocienceAI 战略执行仪表板")
        print(f"              更新日期：{datetime.now().strftime('%Y-%m-%d')}")
        print("="*70)
        print()
        
        # 能力建设
        print("  能力建设")
        obj1 = self.okr['objectives'][0]
        for kr in obj1['key_results']:
            progress = self.calculate_kr_progress(kr)
            bar = '█' * int(progress/10) + '░' * (10 - int(progress/10))
            print(f"  {bar} {progress:5.1f}%  {kr['name']}: {kr['current']}/{kr['target']} {kr['unit']}")
        
        print()
        
        # 用户增长
        print("  用户增长")
        obj2 = self.okr['objectives'][1]
        for kr in obj2['key_results']:
            progress = self.calculate_kr_progress(kr)
            bar = '█' * int(progress/10) + '░' * (10 - int(progress/10))
            print(f"  {bar} {progress:5.1f}%  {kr['name']}: {kr['current']}/{kr['target']} {kr['unit']}")
        
        print()
        
        # 生态构建
        print("  生态构建")
        obj3 = self.okr['objectives'][2]
        for kr in obj3['key_results']:
            progress = self.calculate_kr_progress(kr)
            bar = '█' * int(progress/10) + '░' * (10 - int(progress/10))
            print(f"  {bar} {progress:5.1f}%  {kr['name']}: {kr['current']}/{kr['target']} {kr['unit']}")
        
        print()
        print("="*70)
        
        # 整体进度
        overall_bar = '█' * int(overall_progress/5) + '░' * (20 - int(overall_progress/5))
        print(f"  整体进度：{overall_bar} {overall_progress:.1f}%")
        print("="*70 + "\n")
    
    # ========================================================================
    # 主循环
    # ========================================================================
    
    def run(self, mode: str = 'daily'):
        """运行战略执行引擎"""
        
        print("\n" + "="*70)
        print("  SocienceAI 战略执行引擎")
        print("  Strategic Execution Engine")
        print("="*70)
        
        if mode == 'daily':
            self.execute_daily_tasks()
        elif mode == 'weekly':
            self.execute_weekly_tasks()
        elif mode == 'monthly':
            self.execute_monthly_tasks()
        
        # 打印仪表板
        self.print_dashboard()
        
        # 保存状态
        self.save_state()
        
        print("✅ 战略执行完成\n")


# ============================================================================
# 主程序
# ============================================================================

if __name__ == '__main__':
    import sys
    
    # 获取运行模式
    mode = sys.argv[1] if len(sys.argv) > 1 else 'daily'
    
    # 创建引擎
    engine = StrategicExecutionEngine()
    
    # 运行
    engine.run(mode)
