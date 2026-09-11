#!/usr/bin/env python3
"""
Planning-with-Files Integration Tool
规划文件集成工具 - 持久化机制核心
"""

import os
from datetime import datetime
from typing import Dict, Optional


class PlanningFilesManager:
    """规划文件管理器"""
    
    def __init__(self, working_dir: str):
        self.working_dir = working_dir
        self.task_plan_path = os.path.join(working_dir, 'task_plan.md')
        self.findings_path = os.path.join(working_dir, 'findings.md')
        self.progress_path = os.path.join(working_dir, 'progress.md')
        os.makedirs(working_dir, exist_ok=True)
    
    def create_planning_files(self, task_id: str, **kwargs) -> Dict:
        """创建规划文件"""
        timestamp = datetime.now().isoformat()
        task_plan = f"""# 任务计划\n\n**任务 ID**: {{task_id}}\n**创建时间**: {{timestamp}}\n\n## 阶段\n\n### Phase 1: 数据准备\n### Phase 2: 分析执行\n### Phase 3: 结果生成\n\n**进度**: 0/3\n"""
        with open(self.task_plan_path, 'w', encoding='utf-8') as f:
            f.write(task_plan)
        return {{'status': 'success', 'task_id': task_id}}
    
    def update_phase_status(self, phase: int, status: str, results: Optional[Dict] = None):
        """更新阶段状态"""
        if not os.path.exists(self.task_plan_path):
            return
        with open(self.task_plan_path, 'a', encoding='utf-8') as f:
            f.write(f"\n[{{datetime.now().isoformat()}}] Phase {{phase}}: {{status}}\n")
    
    def get_current_status(self) -> Dict:
        """获取当前状态"""
        if not os.path.exists(self.task_plan_path):
            return {{'status': 'error'}}
        with open(self.task_plan_path, 'r', encoding='utf-8') as f:
            content = f.read()
        completed = content.count('[x]')
        return {{'completed_phases': completed, 'progress_percentage': round(completed / 3 * 100, 1)}}
    
    def recover_session(self) -> Dict:
        """恢复会话"""
        status = self.get_current_status()
        if status.get('status') == 'error':
            return status
        return {{'status': 'recovered', 'current_phase': status['completed_phases'] + 1}}


if __name__ == '__main__':
    manager = PlanningFilesManager('./test')
    manager.create_planning_files('TEST-001')
    print("Planning files created")
