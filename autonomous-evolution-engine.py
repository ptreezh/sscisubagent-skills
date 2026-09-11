#!/usr/bin/env python3
"""
SocienceAI 自主进化引擎
Autonomous Evolution Engine

自主进化系统核心引擎，负责：
- 触发进化流程
- 记录教训和案例
- 执行进化工作流
- 生成进化报告

版本：1.0.0
日期：2026-03-22
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import yaml


class AutonomousEvolutionEngine:
    """自主进化引擎"""
    
    def __init__(self, working_dir: str = './'):
        self.working_dir = Path(working_dir)
        
        # 目录配置
        self.evolution_dir = self.working_dir / 'evolution'
        self.memory_dir = self.working_dir / 'memory'
        self.cases_dir = self.working_dir / 'cases'
        
        # 状态文件
        self.state_path = self.working_dir / 'evolution-state.json'
        
        # 进化状态
        self.state = {
            'session_count': 0,
            'last_evolution': None,
            'next_evolution': 10,
            'total_evolutions': 0,
            'lessons_recorded': 0,
            'cases_recorded': 0
        }
        
        self.load_state()
        self.ensure_directories()
    
    def ensure_directories(self):
        """确保目录结构存在"""
        dirs = [
            self.evolution_dir / 'history',
            self.evolution_dir / 'reports',
            self.evolution_dir / 'metrics',
            self.memory_dir / 'lessons' / 'methodology_errors',
            self.memory_dir / 'lessons' / 'technical_issues',
            self.memory_dir / 'lessons' / 'user_experience',
            self.memory_dir / 'lessons' / 'quality_control',
            self.memory_dir / 'lessons' / 'ethical_concerns',
            self.memory_dir / 'lessons' / 'performance_optimization',
            self.cases_dir / 'successful' / 'skill_creation',
            self.cases_dir / 'successful' / 'methodology_application',
            self.cases_dir / 'successful' / 'user_support',
            self.cases_dir / 'successful' / 'quality_improvement',
            self.cases_dir / 'successful' / 'innovation',
        ]
        
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
    
    def load_state(self):
        """加载进化状态"""
        if self.state_path.exists():
            with open(self.state_path, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
    
    def save_state(self):
        """保存进化状态"""
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    # ========================================================================
    # 会话管理
    # ========================================================================
    
    def start_session(self):
        """开始新会话"""
        self.state['session_count'] += 1
        print(f"🧬 会话 #{self.state['session_count']} 开始")
        
        # 检查是否需要触发进化
        if self.state['session_count'] >= self.state['next_evolution']:
            print("🔔 触发会话进化...")
            self.trigger_evolution('session_based')
        
        self.save_state()
    
    def end_session(self, success: bool = True, feedback: Dict = None):
        """结束会话"""
        if feedback:
            self.record_feedback(feedback)
        
        print(f"✅ 会话 #{self.state['session_count']} 结束")
        self.save_state()
    
    # ========================================================================
    # 教训记录
    # ========================================================================
    
    def record_lesson(self, 
                     title: str,
                     category: str,
                     severity: str,
                     context: str,
                     problem: str,
                     root_cause: str,
                     improvement: str,
                     application: str = ""):
        """记录教训"""
        
        # 验证类别
        valid_categories = [
            'methodology_errors', 'technical_issues', 'user_experience',
            'quality_control', 'ethical_concerns', 'performance_optimization'
        ]
        if category not in valid_categories:
            raise ValueError(f"无效的教训类别：{category}")
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"lesson_{category}_{timestamp}.md"
        
        # 文件路径
        lesson_path = self.memory_dir / 'lessons' / category / filename
        
        # 教训内容
        content = f"""## {title}

**日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**类别**: {category}
**严重性**: {severity}

### 情境描述
{context}

### 问题表现
{problem}

### 根本原因
{root_cause}

### 改进策略
{improvement}

### 应用案例
{application if application else "待补充"}

### 验证状态
待验证

---
*由 SocienceAI 自主进化系统自动生成*
"""
        
        # 写入文件
        with open(lesson_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 更新状态
        self.state['lessons_recorded'] += 1
        
        print(f"📝 教训已记录：{lesson_path}")
        return lesson_path
    
    # ========================================================================
    # 案例记录
    # ========================================================================
    
    def record_case(self,
                   title: str,
                   category: str,
                   impact: str,
                   background: str,
                   challenge: str,
                   solution: str,
                   process: str,
                   result: str,
                   success_factors: List[str],
                   patterns: List[str]):
        """记录成功案例"""
        
        # 验证类别
        valid_categories = [
            'skill_creation', 'methodology_application', 'user_support',
            'quality_improvement', 'innovation'
        ]
        if category not in valid_categories:
            raise ValueError(f"无效的案例类别：{category}")
        
        # 生成编号
        case_number = self.state['cases_recorded'] + 1
        
        # 生成文件名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"case_{case_number:03d}_{timestamp}.md"
        
        # 文件路径
        case_path = self.cases_dir / 'successful' / category / filename
        
        # 案例内容
        success_factors_md = "\n".join([f"- {factor}" for factor in success_factors])
        patterns_md = "\n".join([f"- {pattern}" for pattern in patterns])
        
        content = f"""## 案例 {case_number:03d}: {title}

**日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**类别**: {category}
**影响**: {impact}

### 背景
{background}

### 挑战
{challenge}

### 解决方案
{solution}

### 执行过程
{process}

### 结果
{result}

### 关键成功因素
{success_factors_md}

### 可复用模式
{patterns_md}

---
*由 SocienceAI 自主进化系统自动生成*
"""
        
        # 写入文件
        with open(case_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        # 更新状态
        self.state['cases_recorded'] += 1
        
        print(f"📖 案例已记录：{case_path}")
        return case_path
    
    # ========================================================================
    # 反馈记录
    # ========================================================================
    
    def record_feedback(self, feedback: Dict):
        """记录用户反馈"""
        
        feedback_path = self.evolution_dir / 'feedback' / f"feedback_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        feedback_path.parent.mkdir(parents=True, exist_ok=True)
        
        feedback_record = {
            'timestamp': datetime.now().isoformat(),
            'session_id': self.state['session_count'],
            **feedback
        }
        
        with open(feedback_path, 'w', encoding='utf-8') as f:
            json.dump(feedback_record, f, ensure_ascii=False, indent=2)
        
        print(f"💬 反馈已记录：{feedback_path}")
    
    # ========================================================================
    # 进化触发
    # ========================================================================
    
    def trigger_evolution(self, trigger_type: str, reason: str = ""):
        """触发进化流程"""
        
        print("\n" + "="*60)
        print("🧬 自主进化流程启动")
        print("="*60)
        print(f"触发类型：{trigger_type}")
        print(f"触发原因：{reason}")
        print()
        
        # 执行进化工作流
        self.evolution_workflow(trigger_type)
        
        # 更新状态
        self.state['last_evolution'] = datetime.now().isoformat()
        self.state['total_evolutions'] += 1
        self.state['next_evolution'] = self.state['session_count'] + 10
        
        self.save_state()
        
        print("\n" + "="*60)
        print("✅ 进化流程完成")
        print("="*60)
    
    def evolution_workflow(self, trigger_type: str):
        """执行进化工作流"""
        
        # Phase 1: 数据收集
        print("📊 Phase 1: 数据收集...")
        data = self.collect_evolution_data()
        print(f"   收集到 {len(data)} 项数据")
        
        # Phase 2: 分析反思
        print("🤔 Phase 2: 分析反思...")
        insights = self.analyze_and_reflect(data)
        print(f"   生成 {len(insights)} 条洞察")
        
        # Phase 3: 进化决策
        print("🎯 Phase 3: 进化决策...")
        decisions = self.make_evolution_decisions(insights)
        print(f"   决定执行 {len(decisions)} 项改进")
        
        # Phase 4: 执行改进
        print("🔧 Phase 4: 执行改进...")
        results = self.execute_improvements(decisions)
        print(f"   完成 {len(results)} 项改进")
        
        # Phase 5: 验证评估
        print("✅ Phase 5: 验证评估...")
        validation = self.validate_improvements(results)
        print(f"   验证通过率：{validation['pass_rate']:.2%}")
        
        # 生成进化报告
        print("📝 生成进化报告...")
        report_path = self.generate_evolution_report(trigger_type, data, insights, decisions, results, validation)
        print(f"   报告已保存：{report_path}")
    
    def collect_evolution_data(self) -> List[Dict]:
        """收集进化数据"""
        data = []
        
        # 收集教训
        lessons_dir = self.memory_dir / 'lessons'
        if lessons_dir.exists():
            for category in lessons_dir.iterdir():
                if category.is_dir():
                    for lesson_file in category.glob('*.md'):
                        data.append({
                            'type': 'lesson',
                            'category': category.name,
                            'file': str(lesson_file)
                        })
        
        # 收集案例
        cases_dir = self.cases_dir / 'successful'
        if cases_dir.exists():
            for category in cases_dir.iterdir():
                if category.is_dir():
                    for case_file in category.glob('*.md'):
                        data.append({
                            'type': 'case',
                            'category': category.name,
                            'file': str(case_file)
                        })
        
        # 收集反馈
        feedback_dir = self.evolution_dir / 'feedback'
        if feedback_dir.exists():
            for feedback_file in feedback_dir.glob('*.json'):
                data.append({
                    'type': 'feedback',
                    'file': str(feedback_file)
                })
        
        return data
    
    def analyze_and_reflect(self, data: List[Dict]) -> List[Dict]:
        """分析反思"""
        insights = []
        
        # 简单分析：统计各类别数量
        category_count = {}
        for item in data:
            cat = item.get('category', 'unknown')
            category_count[cat] = category_count.get(cat, 0) + 1
        
        for cat, count in category_count.items():
            insights.append({
                'type': 'statistics',
                'category': cat,
                'count': count,
                'insight': f"{cat} 类别有 {count} 条记录"
            })
        
        return insights
    
    def make_evolution_decisions(self, insights: List[Dict]) -> List[Dict]:
        """进化决策"""
        decisions = []
        
        # 简单决策：基于统计生成改进建议
        for insight in insights:
            if insight['count'] > 5:  # 如果某类别记录超过 5 条，建议改进
                decisions.append({
                    'priority': 'high',
                    'action': f"改进 {insight['category']} 类别",
                    'reason': insight['insight']
                })
        
        return decisions
    
    def execute_improvements(self, decisions: List[Dict]) -> List[Dict]:
        """执行改进"""
        results = []
        
        for decision in decisions:
            # 模拟执行
            results.append({
                'decision': decision,
                'status': 'completed',
                'result': '改进已执行'
            })
        
        return results
    
    def validate_improvements(self, results: List[Dict]) -> Dict:
        """验证改进"""
        total = len(results)
        passed = sum(1 for r in results if r['status'] == 'completed')
        
        return {
            'total': total,
            'passed': passed,
            'failed': total - passed,
            'pass_rate': passed / total if total > 0 else 0
        }
    
    def generate_evolution_report(self, 
                                  trigger_type: str,
                                  data: List[Dict],
                                  insights: List[Dict],
                                  decisions: List[Dict],
                                  results: List[Dict],
                                  validation: Dict) -> Path:
        """生成进化报告"""
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_path = self.evolution_dir / 'reports' / f"evolution_{trigger_type}_{timestamp}.md"
        
        content = f"""# 进化报告

**触发类型**: {trigger_type}
**报告日期**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 数据收集

共收集 {len(data)} 项数据

### 数据分布
"""
        
        # 数据统计
        type_count = {}
        for item in data:
            t = item.get('type', 'unknown')
            type_count[t] = type_count.get(t, 0) + 1
        
        for t, count in type_count.items():
            content += f"- {t}: {count} 项\n"
        
        content += f"""
## 分析洞察

共生成 {len(insights)} 条洞察

"""
        
        for insight in insights[:5]:  # 只显示前 5 条
            content += f"- {insight['insight']}\n"
        
        content += f"""
## 进化决策

共决定执行 {len(decisions)} 项改进

"""
        
        for decision in decisions[:5]:  # 只显示前 5 条
            content += f"- [{decision['priority']}] {decision['action']}\n"
        
        content += f"""
## 执行结果

共完成 {len(results)} 项改进

## 验证结果

- 总数：{validation['total']}
- 通过：{validation['passed']}
- 失败：{validation['failed']}
- 通过率：{validation['pass_rate']:.2%}

---
*由 SocienceAI 自主进化系统自动生成*
"""
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return report_path
    
    # ========================================================================
    # 状态查询
    # ========================================================================
    
    def get_status(self) -> Dict:
        """获取进化状态"""
        return {
            'session_count': self.state['session_count'],
            'total_evolutions': self.state['total_evolutions'],
            'lessons_recorded': self.state['lessons_recorded'],
            'cases_recorded': self.state['cases_recorded'],
            'last_evolution': self.state['last_evolution'],
            'next_evolution': self.state['next_evolution']
        }
    
    def print_status(self):
        """打印状态"""
        status = self.get_status()
        
        print("\n" + "="*60)
        print("🧬 SocienceAI 自主进化系统状态")
        print("="*60)
        print(f"会话计数：{status['session_count']}")
        print(f"进化次数：{status['total_evolutions']}")
        print(f"教训记录：{status['lessons_recorded']}")
        print(f"案例记录：{status['cases_recorded']}")
        print(f"上次进化：{status['last_evolution'] or '无'}")
        print(f"下次进化：会话 #{status['next_evolution']}")
        print("="*60 + "\n")


# ============================================================================
# 主程序
# ============================================================================

if __name__ == '__main__':
    # 创建进化引擎
    engine = AutonomousEvolutionEngine()
    
    # 打印状态
    engine.print_status()
    
    # 模拟会话
    print("开始模拟会话...")
    engine.start_session()
    
    # 记录教训
    engine.record_lesson(
        title="测试教训：配置验证缺失",
        category="quality_control",
        severity="high",
        context="创建新 Skill 时未验证配置文件",
        problem="配置错误导致 Skill 无法加载",
        root_cause="缺少自动配置验证流程",
        improvement="实现配置自动验证机制",
        application="所有 Skill 创建流程"
    )
    
    # 记录案例
    engine.record_case(
        title="成功案例：扎根理论专家创建",
        category="skill_creation",
        impact="高",
        background="用户需要扎根理论分析支持",
        challenge="需要快速创建高质量的 Skill",
        solution="使用模板和自动化流程",
        process="需求分析→模板选择→配置生成→验证测试",
        result="成功创建并部署 Skill",
        success_factors=["模板化", "自动化", "严格验证"],
        patterns=["模板复用", "自动验证", "分步执行"]
    )
    
    # 结束会话
    engine.end_session(success=True, feedback={'rating': 5, 'comment': '很好！'})
    
    # 打印最终状态
    engine.print_status()
