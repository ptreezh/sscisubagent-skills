#!/usr/bin/env python3
"""
轴心编码工具
Strauss & Corbin (1990) 轴心编码参考实现

⚠️ 核心原则：定性分析是智识工作，必须由大模型（Agent/LLM）驱动。
本文件只做数据结构管理和输出格式化，不做任何定性判断。
Paradigm类型、范畴归类、关系推理100%由LLM基于理论原则作出。

Python工具的正确角色:
  ✅ 数据管理、文件I/O、结果格式化
  ✅ 定义清晰的输出JSON结构
  ❌ 关键词匹配做"定性分析"
  ❌ 规则引擎替代理论推理
"""

import os
import json
from typing import Dict, List, Any
from datetime import datetime


class AxialCoder:
    """轴心编码器 — 仅数据结构管理，无定性逻辑"""

    def __init__(self, working_dir: str = './session'):
        self.working_dir = working_dir
        self.categories: Dict[str, Dict] = {}
        self.relationships: List[Dict] = []
        self.paradigm_model: Dict[str, Any] = {}

    def perform_axial_coding(self, open_codes: List[Dict]) -> Dict[str, Any]:
        """执行轴心编码

        ⚠️ 本方法不执行任何定性分析逻辑。
        返回结构化的输出框架，定性分析（Paradigm类型/范畴关系/
        范式模型构建）由LLM基于理论原则判断。

        参数:
            open_codes: 开放编码结果列表
            格式: [{"code": "编码名称", "definition": "定义", "frequency": 次数}, ...]

        返回:
            轴心编码结果（结构框架，LLM填充定性内容）
        """
        result = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'mode': 'llm_driven',
            'message': ('⚠️ 定性分析由LLM基于Strauss & Corbin (1990)理论原则判断。'
                        'Paradigm类型、范畴归类、关系推理见memos中的理论指导。'),
            'open_codes_count': len(open_codes),
            'open_codes': open_codes,
            # 以下字段由LLM填充，Python只返回空结构
            'categories': self._init_categories_structure(open_codes),
            'relationships': [],  # LLM填充
            'paradigm_model': self._init_paradigm_model_structure(),
            'memos': self._generate_methodology_memos(open_codes),
            'statistics': {
                'total_codes': len(open_codes),
                'categories_count': None,  # LLM填充
                'relationships_count': None,  # LLM填充
            }
        }
        return result

    def _init_categories_structure(self, open_codes: List[Dict]) -> Dict[str, Dict]:
        """初始化范畴结构（LLM负责填充内容）

        Python只定义JSON Schema，LLM根据理论原则填充:
        - paradigm_type: 因果条件/核心现象/行动策略/结果后果/中介条件/互动过程
        - definition: 范畴的理论定义
        - properties: 范畴的属性和维度
        """
        return {
            f"范畴_{i+1}": {
                "paradigm_type": None,  # ⚠️ LLM基于理论判断填充
                "codes": [code['code'] for code in open_codes],
                "definition": None,  # ⚠️ LLM理论判断
                "properties": {},  # ⚠️ LLM填充 {属性名: 维度描述}
                "inter_relations": [],  # ⚠️ LLM识别
            }
            for i, code in enumerate(open_codes)
        }

    def _init_paradigm_model_structure(self) -> Dict[str, Any]:
        """初始化范式模型结构（LLM负责填充内容）

        Strauss & Corbin (1990) 范式模型6要素，LLM基于因果逻辑填充:
        """
        return {
            "causal_conditions": [],   # ⚠️ 导致现象发生的条件
            "phenomenon": None,        # ⚠️ 核心现象（唯一）
            "context": [],             # ⚠️ 脉络/情境条件
            "intervening_conditions": [],  # ⚠️ 促进/阻碍行动的因素
            "action_strategies": [],  # ⚠️ 行动/互动策略
            "consequences": [],       # ⚠️ 结果
            "notes": "以上字段由LLM基于理论原则填充，Python不做推断"
        }

    def _generate_methodology_memos(self, open_codes: List[Dict]) -> List[Dict]:
        """生成方法论备忘录（引导LLM定性判断）

        ⚠️ 这些备忘录是给LLM的方法论指导，不是硬编码分析。
        LLM必须基于这些理论原则做自己的判断。
        """
        memos = [
            {
                'type': 'paradigm_type_guidance',
                'role': 'llm_guidance',
                'content': (
                    'Paradigm类型判断原则（Strauss & Corbin 1990）:\n'
                    '- 因果条件: 导致现象发生的背景/历史/制度因素\n'
                    '- 核心现象: 研究的中心事件/问题/议题\n'
                    '- 脉络: 现象发生的时间/地点/文化情境\n'
                    '- 中介条件: 促进或阻碍行动/互动的调节因素\n'
                    '- 行动/互动策略: 个体/群体对现象的应对行为\n'
                    '- 结果: 行动的后果\n'
                    '判断Paradigm类型时，思考: 这个范畴在因果链中扮演什么角色?'
                ),
                'timestamp': datetime.now().isoformat()
            },
            {
                'type': 'category_formation_guidance',
                'role': 'llm_guidance',
                'content': (
                    '范畴归类原则:\n'
                    '- 同受访者来源的编码→优先聚类（情境一致性）\n'
                    '- 语义相近的编码→聚类（概念相似性）\n'
                    '- 编码数量建议3-8个/范畴（过少=范畴泛化；过多=需再分解）\n'
                    '⚠️ 不要按表面词汇相似性聚类，要按理论意义归类'
                ),
                'timestamp': datetime.now().isoformat()
            },
            {
                'type': 'relationship_identification_guidance',
                'role': 'llm_guidance',
                'content': (
                    '关系识别原则（Strauss & Corbin 1990）:\n'
                    '- 因果关系: X导致Y（因为...所以...）\n'
                    '- 脉络关系: X为Y提供情境（在这个背景下...）\n'
                    '- 中介关系: X调节Y的强度（...的情况下...）\n'
                    '- 行动-结果关系: 通过X达成Y（为了...而...）\n'
                    '⚠️ 关系必须有数据支持，不可凭空推断'
                ),
                'timestamp': datetime.now().isoformat()
            },
            {
                'type': 'saturation_check',
                'role': 'llm_guidance',
                'content': (
                    f'理论饱和度检查（基于{len(open_codes)}个开放编码）:\n'
                    '- 新数据是否产生新的Paradigm类型?\n'
                    '- 范畴间关系是否已经完整?\n'
                    '- 是否有未解释的负面案例?\n'
                    '- 达到饱和: 新数据不再产生新范畴/关系'
                ),
                'timestamp': datetime.now().isoformat()
            }
        ]
        return memos

    def save_results(self, result: Dict, filename: str = 'axial_coding_result.json'):
        """保存轴心编码结果"""
        filepath = os.path.join(self.working_dir, filename)
        os.makedirs(self.working_dir, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        return filepath


if __name__ == '__main__':
    # 测试: 6个街头哲学开放编码
    coder = AxialCoder()

    test_codes = [
        {'code': '知识权力不对称', 'definition': '博士vs路人，精英vs大众', 'frequency': 1},
        {'code': '身体化表达', 'definition': '现场互动，身体参与而非文字', 'frequency': 1},
        {'code': '语言游戏', 'definition': '哲学概念日常化，玩弄词语边界', 'frequency': 1},
        {'code': '观者共情', 'definition': '围观者的情感卷入', 'frequency': 1},
        {'code': '娱乐化教育', 'definition': '严肃知识的娱乐包装', 'frequency': 1},
        {'code': '自我展演', 'definition': '表演者/观众的双重展演', 'frequency': 1},
    ]

    result = coder.perform_axial_coding(test_codes)
    print(json.dumps(result, ensure_ascii=False, indent=2))
