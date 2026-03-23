#!/usr/bin/env python3
"""
Planning-with-Files Integration Tool
规划文件集成工具 - 持久化机制核心
"""

import os
from datetime import datetime
from typing import Dict, Optional


class PlanningFilesManager:
    """
    规划文件管理器
    
    实现持久化任务计划运行机制
    """
    
    def __init__(self, working_dir: str):
        """
        初始化
        
        参数:
            working_dir: 工作目录
        """
        self.working_dir = working_dir
        self.task_plan_path = os.path.join(working_dir, 'task_plan.md')
        self.findings_path = os.path.join(working_dir, 'findings.md')
        self.progress_path = os.path.join(working_dir, 'progress.md')
        
        # 确保目录存在
        os.makedirs(working_dir, exist_ok=True)
    
    def create_planning_files(self, task_id: str, **kwargs) -> Dict:
        """创建规划文件"""
        timestamp = datetime.now().isoformat()
        
        # 创建 task_plan.md
        task_plan = f"""# 任务计划

**任务 ID**: {task_id}
**创建时间**: {timestamp}

## 阶段

### Phase 1: 场域识别
- [ ] 场域边界界定
- [ ] 场域结构分析

### Phase 2: 资本分析
- [ ] 四种资本类型分析

### Phase 3: 习性分析
- [ ] 习性模式识别

**进度**: 0/3
"""
        with open(self.task_plan_path, 'w', encoding='utf-8') as f:
            f.write(task_plan)
        
        return {'status': 'success', 'task_id': task_id}
    
    def update_phase_status(self, phase: int, status: str, results: Optional[Dict] = None):
        """更新阶段状态"""
        if not os.path.exists(self.task_plan_path):
            return
        
        with open(self.task_plan_path, 'a', encoding='utf-8') as f:
            f.write(f"\n[{datetime.now().isoformat()}] Phase {phase}: {status}\n")
            if results:
                f.write(f"结果：{str(results)}\n")
    
    def get_current_status(self) -> Dict:
        """获取当前状态"""
        if not os.path.exists(self.task_plan_path):
            return {'status': 'error', 'message': 'task_plan.md 不存在'}
        
        with open(self.task_plan_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        completed = content.count('[x]')
        total = 3
        
        return {
            'completed_phases': completed,
            'total_phases': total,
            'progress_percentage': round(completed / total * 100, 1) if total > 0 else 0
        }
    
    def recover_session(self) -> Dict:
        """恢复会话"""
        status = self.get_current_status()
        
        if status.get('status') == 'error':
            return status
        
        current_phase = status['completed_phases'] + 1
        if current_phase > 3:
            current_phase = 3
        
        return {
            'status': 'recovered',
            'current_phase': current_phase,
            'completed_phases': status['completed_phases'],
            'progress_percentage': status['progress_percentage']
        }


if __name__ == '__main__':
    manager = PlanningFilesManager('./test')
    manager.create_planning_files('TEST-001')
    print("Planning files created successfully")
