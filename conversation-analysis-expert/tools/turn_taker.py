#!/usr/bin/env python3
"""话轮转换分析工具"""

import argparse
import json
from typing import List, Dict

class TurnAnalyzer:
    """话轮分析器"""
    
    def __init__(self):
        self.turns = []
    
    def load_transcript(self, filepath: str) -> None:
        """加载转写文本"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.turns = json.load(f)
    
    def identify_trp(self) -> List[Dict]:
        """识别转换相关位置"""
        trps = []
        for i, turn in enumerate(self.turns):
            # 检查话轮末端特征
            text = turn.get('text', '')
            # 简化规则：句末标点
            if text.rstrip().endswith(('.', '?', '!', '？', '。', '！')):
                trps.append({
                    'turn_index': i,
                    'position': 'end',
                    'type': 'possible_trp'
                })
        return trps
    
    def analyze_turn_allocation(self) -> Dict:
        """分析话轮分配方式"""
        allocation_types = {
            'current_selects_next': 0,
            'next_self_selects': 0,
            'current_continues': 0
        }
        
        for i in range(1, len(self.turns)):
            current = self.turns[i-1]
            next_turn = self.turns[i]
            
            # 简化判断逻辑
            if self._has_address_term(current.get('text', '')):
                allocation_types['current_selects_next'] += 1
            else:
                allocation_types['next_self_selects'] += 1
        
        return allocation_types
    
    def _has_address_term(self, text: str) -> bool:
        """检查是否有称呼语"""
        address_terms = ['老师说', '医生', '请问']
        return any(term in text for term in address_terms)

def main():
    parser = argparse.ArgumentParser(description='话轮转换分析')
    parser.add_argument('--input', required=True, help='转写文件')
    parser.add_argument('--output', required=True, help='输出文件')
    args = parser.parse_args()
    
    analyzer = TurnAnalyzer()
    analyzer.load_transcript(args.input)
    
    results = {
        'trps': analyzer.identify_trp(),
        'allocation': analyzer.analyze_turn_allocation()
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
