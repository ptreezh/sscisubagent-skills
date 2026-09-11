#!/usr/bin/env python3
"""
business-ecosystem-analysis-expert - 主分析入口
商业生态系统分析专家技能

支持信息渐进式披露：
- detail_level: 1=摘要，2=标准, 3=详细
- phased_output: 分阶段输出
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional

from tools.planning_integration import PlanningFilesManager


class SkillExpert:
    """
    business-ecosystem-analysis-expert 专家类
    
    支持信息渐进式披露优化
    """
    
    def __init__(self, working_dir: str = './session'):
        self.working_dir = working_dir
        self.planning_manager = PlanningFilesManager(working_dir)
        self.state = {}
    
    def analyze(self, data: Dict[str, Any], 
                detail_level: int = 2,
                phased_output: bool = True,
                **kwargs) -> Dict[str, Any]:
        """
        执行分析
        
        参数:
            data: 输入数据
            detail_level: 披露级别 (1=摘要, 2=标准, 3=详细)
            phased_output: 是否分阶段输出
            **kwargs: 其他参数
        
        返回:
            分析结果字典
        """
        self.detail_level = detail_level
        self.phased_output = phased_output
        
        result = {
            'status': 'success',
            'skill': 'business-ecosystem-analysis-expert',
            'timestamp': datetime.now().isoformat(),
            'detail_level': detail_level,
            'data': data,
        }
        
        if phased_output:
            # 分阶段输出
            result['phases'] = self._perform_phased_analysis(data, **kwargs)
        else:
            # 一次性输出
            result['analysis'] = self._perform_analysis(data, **kwargs)
        
        # 根据 detail_level 格式化输出
        result = self._format_output(result)
        
        return result
    
    def _perform_phased_analysis(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """分阶段分析"""
        phases = {}
        
        # Phase 1
        phases['phase1'] = self._phase1(data, **kwargs)
        
        # Phase 2
        phases['phase2'] = self._phase2(phases['phase1'], **kwargs)
        
        # Phase 3
        phases['phase3'] = self._phase3(phases['phase2'], **kwargs)
        
        return phases
    
    def _perform_analysis(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """一次性分析(内部使用)"""
        return self._perform_phased_analysis(data, **kwargs)
    
    def _phase1(self, data: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Phase 1: 数据准备/初步分析"""
        return {'status': 'completed', 'phase': 1}
    
    def _phase2(self, phase1_result: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Phase 2: 核心分析"""
        return {'status': 'completed', 'phase': 2}
    
    def _phase3(self, phase2_result: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """Phase 3: 结果生成"""
        return {'status': 'completed', 'phase': 3}
    
    def _format_output(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """
        根据 detail_level 格式化输出(信息渐进式披露)
        
        detail_level:
          1 = 摘要模式：只输出关键结果和结论
          2 = 标准模式：输出主要结果和简要说明
          3 = 详细模式：输出完整结果和详细说明
        """
        if self.detail_level == 1:
            # 摘要模式
            return {
                'status': result.get('status', 'unknown'),
                'skill': result.get('skill', 'business-ecosystem-analysis-expert'),
                'summary': self._generate_summary(result),
                'key_findings': self._extract_key_findings(result)[:3],
                'detail_level': 1
            }
        
        elif self.detail_level == 2:
            # 标准模式
            return {
                'status': result.get('status', 'unknown'),
                'skill': result.get('skill', 'business-ecosystem-analysis-expert'),
                'summary': self._generate_summary(result),
                'key_findings': self._extract_key_findings(result),
                'main_results': self._extract_main_results(result),
                'detail_level': 2
            }
        
        else:
            # 详细模式 (detail_level == 3)
            return result
    
    def _generate_summary(self, result: Dict[str, Any]) -> str:
        """生成摘要"""
        return f"business-ecosystem-analysis-expert 分析完成. "
    
    def _extract_key_findings(self, result: Dict[str, Any]) -> list:
        """提取关键发现"""
        return ['关键发现 1', '关键发现 2', '关键发现 3']
    
    def _extract_main_results(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """提取主要结果"""
        return {'status': 'analyzed'}
    
    def save_state(self, state: dict):
        """保存状态(持久化机制)"""
        state_path = os.path.join(self.working_dir, 'state.json')
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
    
    def load_state(self) -> dict:
        """加载状态(持久化机制)"""
        state_path = os.path.join(self.working_dir, 'state.json')
        if os.path.exists(state_path):
            with open(state_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def recover_session(self) -> dict:
        """恢复会话(持久化机制)"""
        state = self.load_state()
        if state:
            return {
                'status': 'recovered',
                'last_phase': state.get('last_phase', 1),
                'completed_tasks': state.get('completed_tasks', [])
            }
        return {'status': 'new_session'}


if __name__ == '__main__':
    expert = SkillExpert()
    test_data = {'test': 'data'}
    
    # 测试不同 detail_level
    for level in [1, 2, 3]:
        print(f"\n=== Detail Level {level} ===")
        result = expert.analyze(test_data, detail_level=level)
        print(f"输出字段：{list(result.keys())}")
