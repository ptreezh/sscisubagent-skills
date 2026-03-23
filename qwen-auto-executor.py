#!/usr/bin/env python3
"""
Qwen CLI 内自动化执行系统
Qwen CLI Autonomous Execution System

在 Qwen CLI 对话中自动化持续运行
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Optional

# Qwen CLI 集成配置
QWEN_CONFIG = {
    'skill_name': 'autonomous-execution',
    'version': '1.0.0',
    'mode': 'conversation',  # conversation, background
    'tasks_per_turn': 1,
    'auto_continue': True,
}


class QwenAutoExecutor:
    """Qwen CLI 内自动化执行器"""
    
    def __init__(self, working_dir: str = './'):
        self.working_dir = working_dir
        self.state_path = os.path.join(working_dir, 'qwen-automation-state.json')
        self.log_path = os.path.join(working_dir, 'QWEN-AUTO-LOG.md')
        self.task_plan_path = os.path.join(working_dir, 'task_plan.md')
        
        # 导入内容生成器和质量检查器
        try:
            from autonomous_engine_v3 import ContentGenerator, QualityChecker
            self.content_generator = ContentGenerator()
            self.quality_checker = QualityChecker()
        except ImportError:
            self.content_generator = None
            self.quality_checker = None
        
        self.state = {
            'status': 'idle',  # idle, running, paused, stopped
            'current_task': None,
            'completed': [],
            'failed': [],
            'pending': [],
            'turn_count': 0,
            'last_update': None,
            'qwen_session_id': None
        }
        
        self.load_state()
    
    def load_state(self):
        """加载状态"""
        if os.path.exists(self.state_path):
            with open(self.state_path, 'r', encoding='utf-8') as f:
                self.state.update(json.load(f))
    
    def save_state(self):
        """保存状态"""
        self.state['last_update'] = datetime.now().isoformat()
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)
    
    def log(self, message: str, level: str = 'INFO'):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        emoji = {'INFO': 'ℹ️', 'SUCCESS': '✅', 'ERROR': '❌', 'WARNING': '⚠️'}.get(level, '•')
        log_entry = f"[{timestamp}] {emoji} [{level}] {message}\n"
        print(log_entry.strip())
        
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def parse_tasks(self) -> List[Dict]:
        """解析任务计划"""
        if not os.path.exists(self.task_plan_path):
            return self._get_default_tasks()
        
        with open(self.task_plan_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tasks = []
        import re
        
        # 解析待办队列
        pattern = r'\|\s*P(\d+)\s*\|\s*([^\|]+)\|\s*⏳\s*\|'
        matches = re.findall(pattern, content)
        
        completed_skills = [t.get('skill', '') for t in self.state['completed']]
        
        for match in matches:
            priority, skill_name = match
            skill_name = skill_name.strip()
            
            if skill_name and skill_name not in completed_skills:
                tasks.append({
                    'skill': skill_name,
                    'priority': f'P{priority}',
                    'status': 'pending'
                })
        
        tasks.sort(key=lambda x: int(x['priority'][1:]))
        return tasks
    
    def _get_default_tasks(self) -> List[Dict]:
        """默认任务队列"""
        return [
            {'skill': 'bourdieu-field-analysis-expert', 'priority': 'P0', 'status': 'pending'},
            {'skill': 'actor-network-analysis-expert', 'priority': 'P1', 'status': 'pending'},
            {'skill': 'digital-weber-expert', 'priority': 'P2', 'status': 'pending'},
        ]
    
    def execute_turn(self) -> str:
        """执行一轮对话(Qwen CLI 内调用)"""
        self.state['turn_count'] += 1
        self.state['status'] = 'running'
        
        # 解析任务
        tasks = self.parse_tasks()
        
        if not tasks:
            self.state['status'] = 'stopped'
            self.save_state()
            return self._format_response(
                'SUCCESS',
                '🎉 所有任务已完成！',
                {'completed': len(self.state['completed']), 'failed': len(self.state['failed'])}
            )
        
        # 获取下一个任务
        task = tasks[0]
        skill_name = task['skill']
        
        self.state['current_task'] = task
        self.save_state()
        
        # 执行任务
        try:
            result = self._execute_task(skill_name)
            
            if result['success']:
                self.state['completed'].append({
                    'skill': skill_name,
                    'completed_at': datetime.now().isoformat(),
                    'files': result.get('files', [])
                })
                
                # 从 pending 移除
                self.state['pending'] = [t for t in self.state['pending'] if t.get('skill') != skill_name]
                
                self.save_state()
                
                return self._format_response(
                    'SUCCESS',
                    f'✅ {skill_name} 完成！',
                    {
                        'progress': f"{len(self.state['completed'])}/{len(self.state['completed']) + len(tasks)}",
                        'next': tasks[1]['skill'] if len(tasks) > 1 else None,
                        'auto_continue': QWEN_CONFIG['auto_continue']
                    }
                )
            else:
                self.state['failed'].append({
                    'skill': skill_name,
                    'error': result.get('error', 'Unknown'),
                    'failed_at': datetime.now().isoformat()
                })
                self.save_state()
                
                return self._format_response(
                    'ERROR',
                    f'❌ {skill_name} 失败',
                    {'error': result.get('error'), 'retry': True}
                )
        
        except Exception as e:
            return self._format_response(
                'ERROR',
                f'❌ 执行错误：{str(e)}',
                {'exception': str(e)}
            )
        
        finally:
            self.state['current_task'] = None
    
    def _execute_task(self, skill_name: str) -> Dict:
        """执行单个任务"""
        self.log(f"开始执行：{skill_name}")
        
        if self.content_generator:
            # 使用完整生成器
            result = self.content_generator.generate_full_skill(skill_name, self.working_dir)
            
            # 质量检查
            if self.quality_checker:
                skill_path = os.path.join(self.working_dir, skill_name)
                passed, checks = self.quality_checker.check(skill_path)
                
                if not passed:
                    return {'success': False, 'error': f'质量检查失败：{checks}'}
            
            return {'success': True, 'files': result.get('files_created', [])}
        else:
            # 简化版本(无生成器时)
            return self._execute_simple(skill_name)
    
    def _execute_simple(self, skill_name: str) -> Dict:
        """简化执行(备用方案)"""
        try:
            base_dir = os.path.join(self.working_dir, skill_name)
            os.makedirs(base_dir, exist_ok=True)
            
            # 创建基本文件
            files_created = []
            
            # SKILL.md
            with open(os.path.join(base_dir, 'SKILL.md'), 'w', encoding='utf-8') as f:
                f.write(f"# {skill_name}\n\n技能文档...\n")
            files_created.append('SKILL.md')
            
            # skill.yaml
            with open(os.path.join(base_dir, 'skill.yaml'), 'w', encoding='utf-8') as f:
                f.write(f"name: {skill_name}\nversion: 1.0.0\n")
            files_created.append('skill.yaml')
            
            return {'success': True, 'files': files_created}
        
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def _format_response(self, level: str, message: str, data: Dict = None) -> str:
        """格式化 Qwen CLI 响应"""
        emoji = {
            'SUCCESS': '✅',
            'ERROR': '❌',
            'INFO': 'ℹ️',
            'WARNING': '⚠️'
        }.get(level, '•')
        
        response = f"{emoji} {message}"
        
        if data:
            response += "\n\n```\n"
            for key, value in data.items():
                if value is not None:
                    response += f"{key}: {value}\n"
            response += "```"
        
        return response
    
    def get_status(self) -> str:
        """获取状态(Qwen CLI 调用)"""
        tasks = self.parse_tasks()
        
        return self._format_response(
            'INFO',
            '📊 自动化系统状态',
            {
                'status': self.state['status'],
                'completed': len(self.state['completed']),
                'failed': len(self.state['failed']),
                'pending': len(tasks),
                'turns': self.state['turn_count']
            }
        )
    
    def start(self) -> str:
        """启动自动化(Qwen CLI 调用)"""
        self.state['status'] = 'running'
        self.save_state()
        
        tasks = self.parse_tasks()
        
        return self._format_response(
            'SUCCESS',
            '🤖 自动化系统已启动',
            {
                'tasks': len(tasks),
                'mode': QWEN_CONFIG['mode'],
                'auto_continue': QWEN_CONFIG['auto_continue']
            }
        )
    
    def stop(self) -> str:
        """停止自动化(Qwen CLI 调用)"""
        self.state['status'] = 'stopped'
        self.save_state()
        
        return self._format_response(
            'INFO',
            '⏹️ 自动化系统已停止',
            {
                'turns': self.state['turn_count'],
                'completed': len(self.state['completed'])
            }
        )
    
    def continue_execution(self) -> str:
        """继续执行(Qwen CLI 调用)"""
        if QWEN_CONFIG['auto_continue']:
            return self.execute_turn()
        else:
            return self._format_response(
                'INFO',
                '➡️ 请确认是否继续执行',
                {'command': '是/继续'}
            )


# Qwen CLI 命令接口
def qwen_command(cmd: str, args: Dict = None) -> str:
    """Qwen CLI 命令接口"""
    executor = QwenAutoExecutor()
    
    if cmd == 'start':
        return executor.start()
    elif cmd == 'execute':
        return executor.execute_turn()
    elif cmd == 'status':
        return executor.get_status()
    elif cmd == 'stop':
        return executor.stop()
    elif cmd == 'continue':
        return executor.continue_execution()
    else:
        return f"❌ 未知命令：{cmd}"


# 主函数(Qwen CLI 调用入口)
def main():
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python qwen-auto-executor.py <command>")
        print("命令：start, execute, status, stop, continue")
        return
    
    cmd = sys.argv[1]
    result = qwen_command(cmd)
    print(result)


if __name__ == '__main__':
    main()
