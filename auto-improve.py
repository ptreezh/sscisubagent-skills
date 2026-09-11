#!/usr/bin/env python3
"""
自动化改进系统
Auto-Improvement System for Social Science Methodology Skills

改进维度:
1. 持久化任务计划运行
2. 复杂任务分解支持
3. 信息渐进式披露优化
"""

import os
import json
from datetime import datetime


class AutoImprover:
    """自动化改进器"""
    
    def __init__(self, agentskills_dir: str = './'):
        self.agentskills_dir = agentskills_dir
        self.log_path = os.path.join(agentskills_dir, 'AUTO-IMPROVE-LOG.md')
        
        # 需要改进的技能列表
        self.skills_to_improve = [
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
            'current_dimension': None,
            'current_skill': None,
            'completed': [],
            'failed': [],
            'start_time': None
        }
        
        self.log("="*70)
        self.log("🔧 自动化改进系统启动")
        self.log("="*70)
    
    def log(self, message: str):
        """记录日志"""
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}\n"
        print(log_entry.strip())
        
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    
    def improve_all(self):
        """执行完整改进"""
        self.state['start_time'] = datetime.now().isoformat()
        
        # 维度 1: 持久化任务计划运行
        self.log("\n" + "="*70)
        self.log("📋 维度 1: 持久化任务计划运行改进")
        self.log("="*70)
        self._improve_persistent_planning()
        
        # 维度 2: 复杂任务分解支持
        self.log("\n" + "="*70)
        self.log("📋 维度 2: 复杂任务分解支持改进")
        self.log("="*70)
        self._improve_task_decomposition()
        
        # 维度 3: 信息渐进式披露优化
        self.log("\n" + "="*70)
        self.log("📋 维度 3: 信息渐进式披露优化改进")
        self.log("="*70)
        self._improve_progressive_disclosure()
        
        # 完成
        self.log("\n" + "="*70)
        self.log("✅ 自动化改进完成！")
        self.log("="*70)
        self.log(f"开始时间：{self.state['start_time']}")
        self.log(f"完成时间：{datetime.now().isoformat()}")
        self.log(f"改进技能：{len(self.state['completed'])} 个")
        self.log(f"失败技能：{len(self.state['failed'])} 个")
    
    def _improve_persistent_planning(self):
        """改进维度 1: 持久化任务计划运行"""
        for skill_name in self.skills_to_improve:
            self.log(f"\n改进技能：{skill_name}")
            
            skill_path = os.path.join(self.agentskills_dir, skill_name)
            templates_dir = os.path.join(skill_path, 'templates')
            
            # 确保目录存在
            os.makedirs(templates_dir, exist_ok=True)
            
            # 创建 task_plan.md.template
            self._create_task_plan_template(skill_path)
            
            # 改进 analyze.py 添加持久化代码
            self._add_persistence_to_analyze(skill_path)
            
            self.state['completed'].append({
                'skill': skill_name,
                'dimension': 'persistent_planning',
                'timestamp': datetime.now().isoformat()
            })
    
    def _create_task_plan_template(self, skill_path: str):
        """创建 task_plan.md.template"""
        template_content = f"""# {{{{skill_name}}}} 任务计划

**任务 ID**: {{{{task_id}}}}  
**创建时间**: {{{{created_at}}}}  
**最后更新**: {{{{updated_at}}}}

---

## 基本信息

| 字段 | 内容 |
|------|------|
| 技能名称 | {os.path.basename(skill_path)} |
| 分析类型 | {{{{analysis_type}}}} |
| 数据规模 | {{{{data_size}}}} |

---

## 阶段规划

### Phase 1: 数据准备
- [ ] 数据验证
- [ ] 数据预处理
- [ ] 缺失值处理
- **状态**: ⏳ pending
- **开始时间**: -
- **完成时间**: -

### Phase 2: 分析执行
- [ ] 核心分析
- [ ] 辅助分析
- [ ] 敏感性分析
- **状态**: ⏳ pending
- **开始时间**: -
- **完成时间**: -

### Phase 3: 结果生成
- [ ] 结果汇总
- [ ] 质量检查
- [ ] 报告生成
- **状态**: ⏳ pending
- **开始时间**: -
- **完成时间**: -

---

## 完成进度

**总体进度**: {{{{completed_phases}}}}/3 阶段 ({{{{progress_percentage}}}}%)

---

## 错误日志

| 错误 | 阶段 | 尝试次数 | 解决方案 | 状态 | 时间 |
|------|------|----------|----------|------|------|
| - | - | - | - | - | - |

---

## 质量检查点

- [ ] Phase 1 完成：数据有效性验证
- [ ] Phase 2 完成：分析方法正确
- [ ] Phase 3 完成：结果质量检查

---

**最后更新**: {{{{updated_at}}}}  
**当前阶段**: Phase {{{{current_phase}}}}  
**下次会话计划**: {{{{next_session_plan}}}}
"""
        
        template_path = os.path.join(skill_path, 'templates', 'task_plan.md.template')
        with open(template_path, 'w', encoding='utf-8') as f:
            f.write(template_content)
        
        self.log(f"  ✅ 创建 task_plan.md.template")
    
    def _add_persistence_to_analyze(self, skill_path: str):
        """添加持久化代码到 analyze.py"""
        analyze_py_path = os.path.join(skill_path, 'tools', 'analyze.py')
        
        if not os.path.exists(analyze_py_path):
            self.log(f"  ⚠️ analyze.py 不存在, 跳过")
            return
        
        # 读取现有内容
        with open(analyze_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有持久化代码
        if 'save_state' in content and 'load_state' in content:
            self.log(f"  ✅ 已有持久化代码")
            return
        
        # 添加持久化方法
        persistence_code = '''

    def save_state(self, state: dict):
        """保存状态"""
        state_path = os.path.join(self.working_dir, 'state.json')
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def load_state(self) -> dict:
        """加载状态"""
        state_path = os.path.join(self.working_dir, 'state.json')
        if os.path.exists(state_path):
            with open(state_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def recover_session(self) -> dict:
        """恢复会话"""
        state = self.load_state()
        if state:
            return {
                'status': 'recovered',
                'last_phase': state.get('last_phase', 1),
                'completed_tasks': state.get('completed_tasks', [])
            }
        return {'status': 'new_session'}
'''
        
        # 找到类定义并添加方法
        if 'class' in content:
            # 在最后一个方法后添加
            lines = content.split('\n')
            # 找到最后一个方法的结尾
            insert_pos = len(lines)
            for i in range(len(lines)-1, 0, -1):
                if lines[i].startswith('    def '):
                    # 找到下一个空行
                    for j in range(i, len(lines)):
                        if lines[j].strip() == '' and j > i+1:
                            insert_pos = j
                            break
                    break
            
            lines.insert(insert_pos, persistence_code)
            content = '\n'.join(lines)
        
        # 保存
        with open(analyze_py_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log(f"  ✅ 添加持久化代码")
    
    def _improve_task_decomposition(self):
        """改进维度 2: 复杂任务分解支持"""
        for skill_name in self.skills_to_improve:
            self.log(f"\n改进技能：{skill_name}")
            
            skill_path = os.path.join(self.agentskills_dir, skill_name)
            
            # 改进 SKILL.md 添加多阶段流程
            self._add_phases_to_skill_md(skill_path)
            
            # 改进 analyze.py 添加子任务管理
            self._add_subtask_management(skill_path)
            
            self.state['completed'].append({
                'skill': skill_name,
                'dimension': 'task_decomposition',
                'timestamp': datetime.now().isoformat()
            })
    
    def _add_phases_to_skill_md(self, skill_path: str):
        """添加多阶段流程到 SKILL.md"""
        skill_md_path = os.path.join(skill_path, 'SKILL.md')
        
        if not os.path.exists(skill_md_path):
            self.log(f"  ⚠️ SKILL.md 不存在")
            return
        
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有阶段说明
        if 'Phase 1' in content or '阶段' in content:
            self.log(f"  ✅ 已有多阶段流程")
            return
        
        # 添加阶段说明
        phases_section = '''
## 分析流程

```
Phase 1: 数据准备
  ↓
  数据验证 → 数据预处理 → 缺失值处理
  ↓
Phase 2: 分析执行
  ↓
  核心分析 → 辅助分析 → 敏感性分析
  ↓
Phase 3: 结果生成
  ↓
  结果汇总 → 质量检查 → 报告生成
```

### Phase 1: 数据准备
- 数据验证：检查数据格式和质量
- 数据预处理：清洗和转换数据
- 缺失值处理：插补或删除

### Phase 2: 分析执行
- 核心分析：主要分析方法
- 辅助分析：补充分析
- 敏感性分析：稳健性检验

### Phase 3: 结果生成
- 结果汇总：整合分析结果
- 质量检查：验证结果可靠性
- 报告生成：生成最终报告
'''
        
        # 在文件末尾添加
        content += phases_section
        
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log(f"  ✅ 添加多阶段流程")
    
    def _add_subtask_management(self, skill_path: str):
        """添加子任务管理代码"""
        analyze_py_path = os.path.join(skill_path, 'tools', 'analyze.py')
        
        if not os.path.exists(analyze_py_path):
            return
        
        with open(analyze_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有子任务管理
        if 'subtask' in content.lower() or '子任务' in content:
            self.log(f"  ✅ 已有子任务管理")
            return
        
        # 添加子任务管理代码
        subtask_code = '''
    def _execute_subtasks(self, phase: int, data: dict) -> dict:
        """执行子任务"""
        subtasks = self._get_subtasks_for_phase(phase)
        results = {}
        
        for i, subtask in enumerate(subtasks, 1):
            self.log(f"  执行子任务 {i}/{len(subtasks)}: {subtask['name']}")
            try:
                result = subtask['func'](data)
                results[subtask['name']] = {'status': 'success', 'result': result}
            except Exception as e:
                results[subtask['name']] = {'status': 'failed', 'error': str(e)}
        
        return results
    
    def _get_subtasks_for_phase(self, phase: int) -> list:
        """获取指定阶段的子任务列表"""
        subtasks_map = {
            1: [
                {'name': '数据验证', 'func': self._validate_data},
                {'name': '数据预处理', 'func': self._preprocess_data},
                {'name': '缺失值处理', 'func': self._handle_missing}
            ],
            2: [
                {'name': '核心分析', 'func': self._core_analysis},
                {'name': '辅助分析', 'func': self._auxiliary_analysis},
                {'name': '敏感性分析', 'func': self._sensitivity_analysis}
            ],
            3: [
                {'name': '结果汇总', 'func': self._summarize_results},
                {'name': '质量检查', 'func': self._quality_check},
                {'name': '报告生成', 'func': self._generate_report}
            ]
        }
        return subtasks_map.get(phase, [])
'''
        
        # 添加代码
        if 'class' in content:
            lines = content.split('\n')
            insert_pos = len(lines)
            for i in range(len(lines)-1, 0, -1):
                if lines[i].startswith('    def '):
                    for j in range(i, len(lines)):
                        if lines[j].strip() == '' and j > i+1:
                            insert_pos = j
                            break
                    break
            
            lines.insert(insert_pos, subtask_code)
            content = '\n'.join(lines)
            
            with open(analyze_py_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.log(f"  ✅ 添加子任务管理代码")
    
    def _improve_progressive_disclosure(self):
        """改进维度 3: 信息渐进式披露优化"""
        for skill_name in self.skills_to_improve:
            self.log(f"\n改进技能：{skill_name}")
            
            skill_path = os.path.join(self.agentskills_dir, skill_name)
            
            # 改进 SKILL.md 添加分阶段输出说明
            self._add_progressive_output_to_skill_md(skill_path)
            
            # 改进 analyze.py 添加披露级别控制
            self._add_disclosure_control(skill_path)
            
            self.state['completed'].append({
                'skill': skill_name,
                'dimension': 'progressive_disclosure',
                'timestamp': datetime.now().isoformat()
            })
    
    def _add_progressive_output_to_skill_md(self, skill_path: str):
        """添加分阶段输出说明到 SKILL.md"""
        skill_md_path = os.path.join(skill_path, 'SKILL.md')
        
        if not os.path.exists(skill_md_path):
            return
        
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有分阶段输出说明
        if '渐进式' in content or 'progressive' in content.lower():
            self.log(f"  ✅ 已有分阶段输出")
            return
        
        # 添加说明
        disclosure_section = '''
## 信息渐进式披露

本技能支持分阶段输出和披露级别控制：

### 披露级别
- **摘要模式** (detail_level=1): 只输出关键结果和结论
- **标准模式** (detail_level=2): 输出主要结果和简要说明
- **详细模式** (detail_level=3): 输出完整结果和详细说明

### 分阶段输出
- Phase 1 完成后：输出数据准备摘要
- Phase 2 完成后：输出分析结果
- Phase 3 完成后：输出完整报告
'''
        
        content += disclosure_section
        
        with open(skill_md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.log(f"  ✅ 添加分阶段输出说明")
    
    def _add_disclosure_control(self, skill_path: str):
        """添加披露级别控制代码"""
        analyze_py_path = os.path.join(skill_path, 'tools', 'analyze.py')
        
        if not os.path.exists(analyze_py_path):
            return
        
        with open(analyze_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否已有披露控制
        if 'detail_level' in content or 'disclosure' in content.lower():
            self.log(f"  ✅ 已有披露控制")
            return
        
        # 添加披露控制代码
        disclosure_code = '''
    def _format_output(self, result: dict, detail_level: int = 2) -> dict:
        """格式化输出(支持渐进式披露)
        
        参数:
            result: 分析结果
            detail_level: 披露级别 (1=摘要, 2=标准, 3=详细)
        """
        if detail_level == 1:
            # 摘要模式
            return {
                'status': result.get('status', 'unknown'),
                'summary': result.get('summary', ''),
                'key_findings': result.get('key_findings', [])[:3]
            }
        elif detail_level == 2:
            # 标准模式
            return {
                'status': result.get('status', 'unknown'),
                'summary': result.get('summary', ''),
                'key_findings': result.get('key_findings', []),
                'main_results': result.get('main_results', {})
            }
        else:
            # 详细模式
            return result
'''
        
        # 添加代码
        if 'class' in content:
            lines = content.split('\n')
            insert_pos = len(lines)
            for i in range(len(lines)-1, 0, -1):
                if lines[i].startswith('    def '):
                    for j in range(i, len(lines)):
                        if lines[j].strip() == '' and j > i+1:
                            insert_pos = j
                            break
                    break
            
            lines.insert(insert_pos, disclosure_code)
            content = '\n'.join(lines)
            
            with open(analyze_py_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.log(f"  ✅ 添加披露级别控制代码")


def main():
    improver = AutoImprover()
    improver.improve_all()


if __name__ == '__main__':
    main()
