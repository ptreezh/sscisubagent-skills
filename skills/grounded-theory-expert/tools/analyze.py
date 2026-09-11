#!/usr/bin/env python3
"""
grounded-theory-expert 分析协调器
协调三阶段编码流程的入口工具

⚠️ 核心原则：定性分析100%由LLM（Agent）驱动。
本文件只做工作流协调、文件路径管理和结果持久化。
不包含任何定性分析逻辑。

工作流：
  1. segment-data.py    → 数据分段（结构）
  2. axial_coding.py    → 轴心编码结构（LLM填充Paradigm）
  3. selective_coding.py → 核心范畴（LLM选择）
  4. assess-saturation.py → 饱和度评估（结构，LLM填充判断）
"""

import os
import json
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional


class SkillAnalyzer:
    """扎根理论分析协调器"""

    WORKFLOW_STAGES = [
        'open_coding',      # 开放编码
        'axial_coding',     # 轴心编码
        'selective_coding',  # 选择性编码
        'saturation',       # 饱和度评估
    ]

    def __init__(self, working_dir: str = './session'):
        self.working_dir = working_dir
        self.session_file = os.path.join(working_dir, 'session_state.json')
        self._ensure_working_dir()

    def _ensure_working_dir(self):
        os.makedirs(self.working_dir, exist_ok=True)

    def analyze(self, data: Dict[str, Any], stage: str = 'axial_coding', **kwargs) -> Dict[str, Any]:
        """执行分析（协调工作流）

        参数:
            data: 输入数据
            stage: 当前阶段 (axial_coding/selective_coding/open_coding/saturation)
            **kwargs: 额外参数

        返回:
            工作流协调结果
        """
        result = {
            'status': 'success',
            'skill': 'grounded-theory-expert',
            'timestamp': datetime.now().isoformat(),
            'stage': stage,
            'mode': 'llm_coordinated',
            'message': ('⚠️ 定性分析由LLM基于理论原则判断。'
                        '本协调器只管理数据结构和工作流。'),
            'workflow': self._get_workflow_status(stage),
            'data': data,
            'output_file': None,
        }

        # 持久化会话状态
        self._save_session(result)
        return result

    def _get_workflow_status(self, current_stage: str) -> Dict[str, Any]:
        """获取工作流状态"""
        current_idx = self.WORKFLOW_STAGES.index(current_stage) if current_stage in self.WORKFLOW_STAGES else -1
        return {
            'all_stages': self.WORKFLOW_STAGES,
            'current_stage': current_stage,
            'completed_stages': self.WORKFLOW_STAGES[:current_idx],
            'remaining_stages': self.WORKFLOW_STAGES[current_idx+1:],
            'progress_pct': int((current_idx + 1) / len(self.WORKFLOW_STAGES) * 100),
        }

    def _save_session(self, result: Dict):
        """保存会话状态"""
        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

    def load_session(self) -> Optional[Dict]:
        """加载会话状态"""
        if os.path.exists(self.session_file):
            with open(self.session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    def save_state(self, state: dict):
        """保存状态（兼容旧接口）"""
        state_path = os.path.join(self.working_dir, 'state.json')
        with open(state_path, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def load_state(self) -> dict:
        """加载状态（兼容旧接口）"""
        state_path = os.path.join(self.working_dir, 'state.json')
        if os.path.exists(state_path):
            with open(state_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def get_prompt_guide(self, stage: str) -> str:
        """获取方法论指导（LLM定性判断的引导，不是硬编码）

        ⚠️ 这些是方法论原则，不是分析结论。
        LLM必须基于这些原则做自己的理论判断。
        """
        guides = {
            'axial_coding': (
                '轴心编码方法论指导（Strauss & Corbin 1990）:\n'
                '1. Paradigm类型: 因果条件→核心现象→脉络→中介条件→行动策略→结果\n'
                '2. 判断原则: 这个范畴在因果链中扮演什么角色?\n'
                '3. 范畴归类: 按理论意义归类，不按表面词汇相似性\n'
                '4. 关系识别: 因果/脉络/中介/行动-结果，有数据支持\n'
                '5. 禁止: 不要用关键词匹配代替理论判断'
            ),
            'selective_coding': (
                '选择性编码方法论指导:\n'
                '1. 核心范畴: 高度抽象，覆盖面广，能整合其他范畴\n'
                '2. 选择原则: 核心范畴必须与至少50%的范畴相关\n'
                '3. 整合故事线: 围绕核心范畴叙述理论故事\n'
                '4. 理论饱和: 核心范畴是否能解释所有数据?\n'
                '5. 禁止: 不要预设核心范畴，必须从数据涌现'
            ),
            'saturation': (
                '理论饱和度方法论指导:\n'
                '1. 饱和标准: 新数据不再产生新范畴/属性/关系\n'
                '2. 三维检验: 范畴饱和? 属性饱和? 关系饱和?\n'
                '3. 证据标准: 至少8-10个受访者/案例仍无新范畴\n'
                '4. 负面案例: 不符合当前理论的案例是否被充分解释?\n'
                '5. 禁止: 不要用数量标准代替理论深度判断'
            ),
        }
        return guides.get(stage, '未知阶段，请参考SKILL.md方法论指导')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='grounded-theory-expert 分析协调器')
    parser.add_argument('--stage', default='axial_coding',
                       choices=['open_coding', 'axial_coding', 'selective_coding', 'saturation'],
                       help='当前分析阶段')
    parser.add_argument('--data', default='{}', help='输入数据(JSON)')
    parser.add_argument('--dir', default='./session', help='工作目录')
    args = parser.parse_args()

    analyzer = SkillAnalyzer(working_dir=args.dir)
    try:
        data = json.loads(args.data)
    except json.JSONDecodeError:
        data = {}

    result = analyzer.analyze(data, stage=args.stage)
    print(json.dumps(result, ensure_ascii=False, indent=2))
