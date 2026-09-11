#!/usr/bin/env python3
"""
编码备忘录管理工具
支持扎根理论分析过程中的备忘录撰写和管理
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum


class MemoType(Enum):
    """备忘录类型"""
    CODE = "code_memo"              # 编码备忘录
    THEORETICAL = "theoretical_memo" # 理论备忘录
    OPERATIONAL = "operational_memo" # 操作备忘录
    ANALYTICAL = "analytical_memo"   # 分析备忘录
    REFLEXIVE = "reflexive_memo"     # 反思备忘录


class MemoManager:
    """备忘录管理器"""
    
    def __init__(self, working_dir: str = './session'):
        """初始化备忘录管理器
        
        参数:
            working_dir: 工作目录
        """
        self.working_dir = working_dir
        self.memos = []
        self.memo_file = os.path.join(working_dir, 'memos.json')
        
        # 加载已有备忘录
        self._load_memos()
    
    def _load_memos(self):
        """加载已有备忘录"""
        if os.path.exists(self.memo_file):
            try:
                with open(self.memo_file, 'r', encoding='utf-8') as f:
                    self.memos = json.load(f)
            except Exception:
                self.memos = []
    
    def create_memo(self,
                    memo_type: str,
                    title: str,
                    content: str,
                    related_codes: List[str] = None,
                    related_categories: List[str] = None,
                    phase: str = None) -> Dict[str, Any]:
        """创建新备忘录
        
        参数:
            memo_type: 备忘录类型
            title: 备忘录标题
            content: 备忘录内容
            related_codes: 相关编码列表
            related_categories: 相关范畴列表
            phase: 编码阶段
            
        返回:
            创建的备忘录
        """
        memo = {
            'id': f"memo_{datetime.now().strftime('%Y%m%d%H%M%S')}_{len(self.memos)+1}",
            'type': memo_type,
            'title': title,
            'content': content,
            'related_codes': related_codes or [],
            'related_categories': related_categories or [],
            'phase': phase,
            'timestamp': datetime.now().isoformat(),
            'modified': None
        }
        
        self.memos.append(memo)
        self._save_memos()
        
        return memo
    
    def update_memo(self, memo_id: str, updates: Dict[str, Any]) -> Optional[Dict]:
        """更新备忘录
        
        参数:
            memo_id: 备忘录ID
            updates: 更新内容
            
        返回:
            更新后的备忘录
        """
        for memo in self.memos:
            if memo['id'] == memo_id:
                memo.update(updates)
                memo['modified'] = datetime.now().isoformat()
                self._save_memos()
                return memo
        
        return None
    
    def delete_memo(self, memo_id: str) -> bool:
        """删除备忘录
        
        参数:
            memo_id: 备忘录ID
            
        返回:
            是否删除成功
        """
        for i, memo in enumerate(self.memos):
            if memo['id'] == memo_id:
                del self.memos[i]
                self._save_memos()
                return True
        
        return False
    
    def get_memo(self, memo_id: str) -> Optional[Dict]:
        """获取单个备忘录
        
        参数:
            memo_id: 备忘录ID
            
        返回:
            备忘录内容
        """
        for memo in self.memos:
            if memo['id'] == memo_id:
                return memo
        
        return None
    
    def search_memos(self,
                     memo_type: str = None,
                     phase: str = None,
                     keyword: str = None,
                     related_code: str = None) -> List[Dict]:
        """搜索备忘录
        
        参数:
            memo_type: 备忘录类型
            phase: 编码阶段
            keyword: 关键词
            related_code: 相关编码
            
        返回:
            匹配的备忘录列表
        """
        results = []
        
        for memo in self.memos:
            match = True
            
            if memo_type and memo['type'] != memo_type:
                match = False
            
            if phase and memo.get('phase') != phase:
                match = False
            
            if keyword and keyword.lower() not in memo['content'].lower():
                match = False
            
            if related_code and related_code not in memo.get('related_codes', []):
                match = False
            
            if match:
                results.append(memo)
        
        return results
    
    def get_memos_by_type(self, memo_type: str) -> List[Dict]:
        """按类型获取备忘录
        
        参数:
            memo_type: 备忘录类型
            
        返回:
            备忘录列表
        """
        return [m for m in self.memos if m['type'] == memo_type]
    
    def get_memos_by_phase(self, phase: str) -> List[Dict]:
        """按阶段获取备忘录
        
        参数:
            phase: 编码阶段
            
        返回:
            备忘录列表
        """
        return [m for m in self.memos if m.get('phase') == phase]
    
    def generate_theoretical_memo_report(self) -> Dict[str, Any]:
        """生成理论备忘录报告
        
        返回:
            报告内容
        """
        report = {
            'total_memos': len(self.memos),
            'by_type': {},
            'by_phase': {},
            'timeline': [],
            'key_insights': []
        }
        
        # 按类型统计
        for memo in self.memos:
            memo_type = memo['type']
            if memo_type not in report['by_type']:
                report['by_type'][memo_type] = 0
            report['by_type'][memo_type] += 1
        
        # 按阶段统计
        for memo in self.memos:
            phase = memo.get('phase', 'unspecified')
            if phase not in report['by_phase']:
                report['by_phase'][phase] = 0
            report['by_phase'][phase] += 1
        
        # 时间线
        sorted_memos = sorted(self.memos, key=lambda x: x['timestamp'])
        report['timeline'] = [
            {
                'timestamp': m['timestamp'],
                'type': m['type'],
                'title': m['title']
            }
            for m in sorted_memos
        ]
        
        # 提取关键洞察（从理论备忘录中）
        theoretical_memos = self.get_memos_by_type(MemoType.THEORETICAL.value)
        report['key_insights'] = [
            {
                'title': m['title'],
                'content': m['content'][:200] + '...' if len(m['content']) > 200 else m['content']
            }
            for m in theoretical_memos
        ]
        
        return report
    
    def export_memos(self, format: str = 'json') -> str:
        """导出备忘录
        
        参数:
            format: 导出格式 (json, markdown)
            
        返回:
            导出内容
        """
        if format == 'json':
            return json.dumps(self.memos, ensure_ascii=False, indent=2)
        
        elif format == 'markdown':
            lines = ['# 编码备忘录汇总\n']
            
            for memo in sorted(self.memos, key=lambda x: x['timestamp']):
                lines.append(f"## {memo['title']}\n")
                lines.append(f"- **类型**: {memo['type']}\n")
                lines.append(f"- **时间**: {memo['timestamp']}\n")
                
                if memo.get('phase'):
                    lines.append(f"- **阶段**: {memo['phase']}\n")
                
                if memo.get('related_codes'):
                    lines.append(f"- **相关编码**: {', '.join(memo['related_codes'])}\n")
                
                if memo.get('related_categories'):
                    lines.append(f"- **相关范畴**: {', '.join(memo['related_categories'])}\n")
                
                lines.append(f"\n{memo['content']}\n")
                lines.append("\n---\n\n")
            
            return ''.join(lines)
        
        return ''
    
    def _save_memos(self):
        """保存备忘录到文件"""
        os.makedirs(self.working_dir, exist_ok=True)
        
        with open(self.memo_file, 'w', encoding='utf-8') as f:
            json.dump(self.memos, f, ensure_ascii=False, indent=2)
    
    # 便捷方法：创建特定类型的备忘录
    
    def create_code_memo(self,
                        code: str,
                        definition: str,
                        rationale: str,
                        examples: List[str] = None) -> Dict:
        """创建编码备忘录
        
        参数:
            code: 编码名称
            definition: 编码定义
            rationale: 编码理由
            examples: 示例引用
            
        返回:
            创建的备忘录
        """
        content = f"**编码定义**: {definition}\n\n**编码理由**: {rationale}"
        
        if examples:
            content += f"\n\n**示例引用**:\n" + '\n'.join(f"- {ex}" for ex in examples)
        
        return self.create_memo(
            memo_type=MemoType.CODE.value,
            title=f"编码备忘录: {code}",
            content=content,
            related_codes=[code]
        )
    
    def create_theoretical_memo(self,
                                insight: str,
                                evidence: str,
                                implications: str = None) -> Dict:
        """创建理论备忘录
        
        参数:
            insight: 理论洞察
            evidence: 证据支持
            implications: 理论含义
            
        返回:
            创建的备忘录
        """
        content = f"**理论洞察**: {insight}\n\n**证据支持**: {evidence}"
        
        if implications:
            content += f"\n\n**理论含义**: {implications}"
        
        return self.create_memo(
            memo_type=MemoType.THEORETICAL.value,
            title=f"理论备忘录: {insight[:30]}...",
            content=content
        )
    
    def create_reflexive_memo(self,
                             reflection: str,
                             context: str = None) -> Dict:
        """创建反思备忘录
        
        参数:
            reflection: 反思内容
            context: 反思情境
            
        返回:
            创建的备忘录
        """
        content = reflection
        
        if context:
            content = f"**情境**: {context}\n\n**反思**: {reflection}"
        
        return self.create_memo(
            memo_type=MemoType.REFLEXIVE.value,
            title=f"反思备忘录: {datetime.now().strftime('%Y-%m-%d')}",
            content=content
        )
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取备忘录统计
        
        返回:
            统计信息
        """
        stats = {
            'total_memos': len(self.memos),
            'by_type': {},
            'by_phase': {},
            'earliest': None,
            'latest': None,
            'average_per_day': 0
        }
        
        if not self.memos:
            return stats
        
        # 按类型统计
        for memo in self.memos:
            memo_type = memo['type']
            stats['by_type'][memo_type] = stats['by_type'].get(memo_type, 0) + 1
        
        # 按阶段统计
        for memo in self.memos:
            phase = memo.get('phase', 'unspecified')
            stats['by_phase'][phase] = stats['by_phase'].get(phase, 0) + 1
        
        # 时间统计
        sorted_memos = sorted(self.memos, key=lambda x: x['timestamp'])
        stats['earliest'] = sorted_memos[0]['timestamp']
        stats['latest'] = sorted_memos[-1]['timestamp']
        
        # 计算平均每天备忘录数量
        try:
            earliest = datetime.fromisoformat(sorted_memos[0]['timestamp'])
            latest = datetime.fromisoformat(sorted_memos[-1]['timestamp'])
            days = (latest - earliest).days + 1
            stats['average_per_day'] = round(len(self.memos) / days, 2) if days > 0 else 0
        except Exception:
            pass
        
        return stats


if __name__ == '__main__':
    # 测试
    manager = MemoManager('./test_session')
    
    # 创建编码备忘录
    code_memo = manager.create_code_memo(
        code='工作压力',
        definition='员工在工作中感受到的心理压力',
        rationale='该概念从多位受访者的描述中涌现，具有普遍性',
        examples=['我觉得每天都很紧张', '工作任务总是做不完']
    )
    print(f"创建编码备忘录: {code_memo['id']}")
    
    # 创建理论备忘录
    theory_memo = manager.create_theoretical_memo(
        insight='工作压力与应对策略之间存在动态平衡关系',
        evidence='多位受访者在描述压力时都提到了相应的应对方式',
        implications='这可能解释为什么相同压力水平下员工表现不同'
    )
    print(f"创建理论备忘录: {theory_memo['id']}")
    
    # 获取统计
    stats = manager.get_statistics()
    print(f"\n备忘录统计: {json.dumps(stats, ensure_ascii=False, indent=2)}")
