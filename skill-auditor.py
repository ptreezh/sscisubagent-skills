#!/usr/bin/env python3
"""
社会科学方法论 Skill 核查系统
Social Science Methodology Skill Auditor

核查维度:
1. agentskills.io 规范符合性
2. 复杂任务分解支持
3. 持久化任务计划运行
4. 信息渐进式披露优化
"""

import os
import json
import yaml
from datetime import datetime
from typing import Dict, List, Tuple


class SkillAuditor:
    """Skill 核查器"""
    
    def __init__(self, agentskills_dir: str = './'):
        self.agentskills_dir = agentskills_dir
        self.audit_report_path = os.path.join(agentskills_dir, 'SKILL-AUDIT-REPORT.md')
        self.audit_state_path = os.path.join(agentskills_dir, 'audit-state.json')
        
        # 核查维度
        self.audit_dimensions = {
            'agentskills_io': 'agentskills.io 规范符合性',
            'task_decomposition': '复杂任务分解支持',
            'persistent_planning': '持久化任务计划运行',
            'progressive_disclosure': '信息渐进式披露优化'
        }
        
        # 社会科学方法论 skill 列表
        self.methodology_skills = [
            'grounded-theory-expert',
            'social-network-analysis-expert',
            'actor-network-analysis-expert',
            'bourdieu-field-analysis-expert',
            'digital-marx-expert',
            'digital-durkheim-expert',
            'digital-weber-expert',
            'msqca-analysis-expert',
            'did-analysis-expert',
            'data-analysis-expert',
            'business-ecosystem-analysis-expert',
            'business-model-analysis-expert',
            'survey-design-expert'
        ]
        
        self.state = {
            'current_skill': None,
            'completed': [],
            'failed': [],
            'results': {}
        }
        
        self.load_state()
    
    def load_state(self):
        """加载状态"""
        if os.path.exists(self.audit_state_path):
            with open(self.audit_state_path, 'r', encoding='utf-8') as f:
                self.state.update(json.load(f))
    
    def save_state(self):
        """保存状态"""
        with open(self.audit_state_path, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] {message}")
    
    def audit_skill(self, skill_name: str) -> Dict:
        """核查单个 skill"""
        self.log(f"\n{'='*60}")
        self.log(f"核查技能：{skill_name}")
        self.log(f"{'='*60}")
        
        skill_path = os.path.join(self.agentskills_dir, skill_name)
        
        if not os.path.exists(skill_path):
            self.log(f"❌ 技能目录不存在：{skill_path}")
            return {'status': 'error', 'reason': '目录不存在'}
        
        results = {
            'skill': skill_name,
            'timestamp': datetime.now().isoformat(),
            'dimensions': {}
        }
        
        # 维度 1: agentskills.io 规范符合性
        self.log("\n📋 维度 1: agentskills.io 规范符合性")
        results['dimensions']['agentskills_io'] = self._audit_agentskills_io(skill_path)
        
        # 维度 2: 复杂任务分解支持
        self.log("\n📋 维度 2: 复杂任务分解支持")
        results['dimensions']['task_decomposition'] = self._audit_task_decomposition(skill_path)
        
        # 维度 3: 持久化任务计划运行
        self.log("\n📋 维度 3: 持久化任务计划运行")
        results['dimensions']['persistent_planning'] = self._audit_persistent_planning(skill_path)
        
        # 维度 4: 信息渐进式披露优化
        self.log("\n📋 维度 4: 信息渐进式披露优化")
        results['dimensions']['progressive_disclosure'] = self._audit_progressive_disclosure(skill_path)
        
        # 计算总分
        results['overall_score'] = self._calculate_overall_score(results['dimensions'])
        results['status'] = 'pass' if results['overall_score'] >= 80 else 'needs_improvement'
        
        self.log(f"\n✅ 核查完成：{skill_name}")
        self.log(f"📊 总分：{results['overall_score']}/100")
        self.log(f"状态：{'✅ 通过' if results['overall_score'] >= 80 else '⚠️ 需要改进'}")
        
        return results
    
    def _audit_agentskills_io(self, skill_path: str) -> Dict:
        """核查 agentskills.io 规范"""
        score = 0
        max_score = 25
        checks = []
        
        # 检查 1: skill.yaml 存在
        skill_yaml_path = os.path.join(skill_path, 'skill.yaml')
        if os.path.exists(skill_yaml_path):
            checks.append({'item': 'skill.yaml 存在', 'pass': True})
            score += 5
            
            # 检查必需字段
            try:
                with open(skill_yaml_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                required_fields = ['name', 'version', 'description', 'inputs', 'outputs']
                missing = [f for f in required_fields if f not in config]
                
                if not missing:
                    checks.append({'item': '必需字段完整', 'pass': True})
                    score += 5
                else:
                    checks.append({'item': f'缺少字段：{missing}', 'pass': False})
            except Exception as e:
                checks.append({'item': f'YAML 解析失败：{e}', 'pass': False})
        else:
            checks.append({'item': 'skill.yaml 缺失', 'pass': False})
        
        # 检查 2: SKILL.md 存在
        skill_md_path = os.path.join(skill_path, 'SKILL.md')
        if os.path.exists(skill_md_path):
            checks.append({'item': 'SKILL.md 存在', 'pass': True})
            score += 5
        else:
            checks.append({'item': 'SKILL.md 缺失', 'pass': False})
        
        # 检查 3: 目录结构
        required_dirs = ['prompts', 'tools', 'templates']
        missing_dirs = [d for d in required_dirs if not os.path.exists(os.path.join(skill_path, d))]
        
        if not missing_dirs:
            checks.append({'item': '目录结构完整', 'pass': True})
            score += 5
        else:
            checks.append({'item': f'缺少目录：{missing_dirs}', 'pass': False})
        
        # 检查 4: tools/analyze.py 存在
        analyze_py = os.path.join(skill_path, 'tools', 'analyze.py')
        if os.path.exists(analyze_py):
            checks.append({'item': 'tools/analyze.py 存在', 'pass': True})
            score += 5
        else:
            checks.append({'item': 'tools/analyze.py 缺失', 'pass': False})
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': round(score / max_score * 100, 1),
            'checks': checks
        }
    
    def _audit_task_decomposition(self, skill_path: str) -> Dict:
        """核查复杂任务分解支持"""
        score = 0
        max_score = 25
        checks = []
        
        # 检查 1: 多阶段分析流程
        skill_md_path = os.path.join(skill_path, 'SKILL.md')
        if os.path.exists(skill_md_path):
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            phase_keywords = ['Phase', '阶段', '步骤', 'Step']
            has_phases = any(kw in content for kw in phase_keywords)
            
            if has_phases:
                checks.append({'item': '多阶段分析流程', 'pass': True})
                score += 8
            else:
                checks.append({'item': '缺少多阶段分析流程', 'pass': False})
            
            # 检查是否有 3 个以上阶段
            phase_count = content.count('Phase') + content.count('阶段')
            if phase_count >= 3:
                checks.append({'item': '阶段数≥3', 'pass': True})
                score += 7
            else:
                checks.append({'item': '阶段数<3', 'pass': False})
        else:
            checks.append({'item': 'SKILL.md 不存在', 'pass': False})
        
        # 检查 2: 任务分解逻辑
        analyze_py_path = os.path.join(skill_path, 'tools', 'analyze.py')
        if os.path.exists(analyze_py_path):
            with open(analyze_py_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            decomposition_keywords = ['phase', 'step', 'stage', '阶段', '步骤']
            has_decomposition = any(kw in content.lower() for kw in decomposition_keywords)
            
            if has_decomposition:
                checks.append({'item': '任务分解逻辑', 'pass': True})
                score += 5
            else:
                checks.append({'item': '缺少任务分解逻辑', 'pass': False})
        else:
            checks.append({'item': 'analyze.py 不存在', 'pass': False})
        
        # 检查 3: 子任务管理
        if os.path.exists(analyze_py_path):
            with open(analyze_py_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            subtask_keywords = ['subtask', 'sub_task', '子任务', 'child']
            has_subtasks = any(kw in content.lower() for kw in subtask_keywords)
            
            if has_subtasks:
                checks.append({'item': '子任务管理', 'pass': True})
                score += 5
            else:
                checks.append({'item': '缺少子任务管理', 'pass': False})
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': round(score / max_score * 100, 1),
            'checks': checks
        }
    
    def _audit_persistent_planning(self, skill_path: str) -> Dict:
        """核查持久化任务计划运行"""
        score = 0
        max_score = 25
        checks = []
        
        # 检查 1: planning-with-files 模板
        templates_dir = os.path.join(skill_path, 'templates')
        if os.path.exists(templates_dir):
            template_files = os.listdir(templates_dir)
            has_task_plan = any('task_plan' in f for f in template_files)
            
            if has_task_plan:
                checks.append({'item': 'task_plan 模板', 'pass': True})
                score += 8
            else:
                checks.append({'item': '缺少 task_plan 模板', 'pass': False})
        else:
            checks.append({'item': 'templates 目录不存在', 'pass': False})
        
        # 检查 2: 状态持久化代码
        analyze_py_path = os.path.join(skill_path, 'tools', 'analyze.py')
        if os.path.exists(analyze_py_path):
            with open(analyze_py_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            persistence_keywords = ['save', 'load', 'persist', 'state', 'session', '保存', '加载', '状态']
            has_persistence = any(kw in content.lower() for kw in persistence_keywords)
            
            if has_persistence:
                checks.append({'item': '状态持久化', 'pass': True})
                score += 8
            else:
                checks.append({'item': '缺少状态持久化', 'pass': False})
        else:
            checks.append({'item': 'analyze.py 不存在', 'pass': False})
        
        # 检查 3: 会话恢复
        if os.path.exists(analyze_py_path):
            with open(analyze_py_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            recovery_keywords = ['recover', 'resume', 'restore', '恢复', '继续']
            has_recovery = any(kw in content.lower() for kw in recovery_keywords)
            
            if has_recovery:
                checks.append({'item': '会话恢复', 'pass': True})
                score += 9
            else:
                checks.append({'item': '缺少会话恢复', 'pass': False})
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': round(score / max_score * 100, 1),
            'checks': checks
        }
    
    def _audit_progressive_disclosure(self, skill_path: str) -> Dict:
        """核查信息渐进式披露优化"""
        score = 0
        max_score = 25
        checks = []
        
        # 检查 1: 分阶段输出
        skill_md_path = os.path.join(skill_path, 'SKILL.md')
        if os.path.exists(skill_md_path):
            with open(skill_md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            disclosure_keywords = ['逐步', '渐进', '分步', '阶段性', 'progressive', 'step-by-step']
            has_disclosure = any(kw in content.lower() for kw in disclosure_keywords)
            
            if has_disclosure:
                checks.append({'item': '分阶段输出设计', 'pass': True})
                score += 8
            else:
                checks.append({'item': '缺少分阶段输出设计', 'pass': False})
        else:
            checks.append({'item': 'SKILL.md 不存在', 'pass': False})
        
        # 检查 2: 摘要 + 详情模式
        analyze_py_path = os.path.join(skill_path, 'tools', 'analyze.py')
        if os.path.exists(analyze_py_path):
            with open(analyze_py_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            summary_keywords = ['summary', '摘要', '概述', 'brief', 'overview']
            has_summary = any(kw in content.lower() for kw in summary_keywords)
            
            if has_summary:
                checks.append({'item': '摘要 + 详情模式', 'pass': True})
                score += 8
            else:
                checks.append({'item': '缺少摘要 + 详情模式', 'pass': False})
        else:
            checks.append({'item': 'analyze.py 不存在', 'pass': False})
        
        # 检查 3: 用户控制披露级别
        if os.path.exists(analyze_py_path):
            with open(analyze_py_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            control_keywords = ['level', 'detail', 'verbose', '详细', '级别', 'depth']
            has_control = any(kw in content.lower() for kw in control_keywords)
            
            if has_control:
                checks.append({'item': '披露级别控制', 'pass': True})
                score += 9
            else:
                checks.append({'item': '缺少披露级别控制', 'pass': False})
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': round(score / max_score * 100, 1),
            'checks': checks
        }
    
    def _calculate_overall_score(self, dimensions: Dict) -> int:
        """计算总分"""
        total_score = sum(d['score'] for d in dimensions.values())
        max_score = sum(d['max_score'] for d in dimensions.values())
        return round(total_score / max_score * 100) if max_score > 0 else 0
    
    def run_full_audit(self) -> Dict:
        """运行完整核查"""
        self.log("="*70)
        self.log("🔍 社会科学方法论 Skill 核查系统启动")
        self.log("="*70)
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_skills': len(self.methodology_skills),
            'skills': {}
        }
        
        for skill_name in self.methodology_skills:
            skill_result = self.audit_skill(skill_name)
            results['skills'][skill_name] = skill_result
            
            self.state['completed'].append({
                'skill': skill_name,
                'score': skill_result.get('overall_score', 0),
                'status': skill_result.get('status', 'unknown')
            })
            self.save_state()
        
        # 生成报告
        self._generate_report(results)
        
        return results
    
    def _generate_report(self, results: Dict):
        """生成核查报告"""
        report = []
        report.append("# 社会科学方法论 Skill 核查报告\n")
        report.append(f"**核查时间**: {results['timestamp']}\n")
        report.append(f"**核查技能数**: {results['total_skills']}\n")
        report.append(f"**核查维度**: 4\n")
        report.append("")
        
        # 汇总统计
        report.append("## 📊 汇总统计\n")
        
        passed = sum(1 for s in results['skills'].values() if s.get('overall_score', 0) >= 80)
        needs_improvement = results['total_skills'] - passed
        avg_score = sum(s.get('overall_score', 0) for s in results['skills'].values()) / results['total_skills']
        
        report.append(f"- ✅ 通过：{passed} 个\n")
        report.append(f"- ⚠️ 需要改进：{needs_improvement} 个\n")
        report.append(f"- 📊 平均分：{avg_score:.1f}\n")
        report.append("")
        
        # 详细结果
        report.append("## 📋 详细结果\n")
        
        for skill_name, result in results['skills'].items():
            score = result.get('overall_score', 0)
            status = '✅' if score >= 80 else '⚠️'
            
            report.append(f"### {status} {skill_name}\n")
            report.append(f"**总分**: {score}/100\n")
            report.append("")
            
            report.append("| 维度 | 得分 | 百分比 |\n")
            report.append("|------|------|--------|\n")
            
            for dim_key, dim_result in result.get('dimensions', {}).items():
                dim_name = self.audit_dimensions.get(dim_key, dim_key)
                report.append(f"| {dim_name} | {dim_result['score']}/{dim_result['max_score']} | {dim_result['percentage']}% |\n")
            
            report.append("\n")
        
        # 保存报告
        with open(self.audit_report_path, 'w', encoding='utf-8') as f:
            f.writelines(report)
        
        self.log(f"\n✅ 核查报告已保存：{self.audit_report_path}")


def main():
    auditor = SkillAuditor()
    results = auditor.run_full_audit()
    
    print("\n" + "="*70)
    print("核查完成！")
    print("="*70)
    
    # 打印摘要
    passed = sum(1 for s in results['skills'].values() if s.get('overall_score', 0) >= 80)
    print(f"总技能数：{results['total_skills']}")
    print(f"通过：{passed}")
    print(f"需要改进：{results['total_skills'] - passed}")


if __name__ == '__main__':
    main()
