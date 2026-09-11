#!/usr/bin/env python3
"""序列组织分析工具"""

import argparse
import json
from typing import List, Dict, Tuple

class SequenceAnalyzer:
    """序列分析器"""
    
    # 邻接对类型定义
    ADJACENCY_PAIRS = {
        'question-answer': {'first': ['?', '吗', '什么'], 'second': ['是', '不是', '好']},
        'greeting-greeting': {'first': ['你好', '早', 'hi'], 'second': ['你好', '早', 'hi']},
        'request-accept/reject': {'first': ['请', '能', '可以'], 'second': ['好', '行', '不行']}
    }
    
    def __init__(self):
        self.turns = []
    
    def load_transcript(self, filepath: str) -> None:
        """加载转写文本"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.turns = json.load(f)
    
    def identify_adjacency_pairs(self) -> List[Dict]:
        """识别邻接对"""
        pairs = []
        
        for i in range(len(self.turns) - 1):
            first_turn = self.turns[i]
            second_turn = self.turns[i + 1]
            
            # 跳过同一说话人的连续话轮
            if first_turn.get('speaker') == second_turn.get('speaker'):
                continue
            
            pair_type = self._classify_pair(
                first_turn.get('text', ''),
                second_turn.get('text', '')
            )
            
            if pair_type:
                pairs.append({
                    'type': pair_type,
                    'first_position': i,
                    'second_position': i + 1,
                    'first_speaker': first_turn.get('speaker'),
                    'second_speaker': second_turn.get('speaker')
                })
        
        return pairs
    
    def _classify_pair(self, first_text: str, second_text: str) -> str:
        """分类邻接对类型"""
        for pair_type, patterns in self.ADJACENCY_PAIRS.items():
            first_match = any(p in first_text for p in patterns['first'])
            second_match = any(p in second_text for p in patterns['second'])
            if first_match and second_match:
                return pair_type
        return None
    
    def analyze_preference(self, pairs: List[Dict]) -> Dict:
        """分析偏好组织"""
        preference_count = {'preferred': 0, 'dispreferred': 0}
        
        for pair in pairs:
            # 简化判断：直接回应为偏好
            if pair['type'] == 'request-accept/reject':
                # 检查是否有延迟或解释
                second_turn = self.turns[pair['second_position']]['text']
                if '但是' in second_turn or '不过' in second_text:
                    preference_count['dispreferred'] += 1
                else:
                    preference_count['preferred'] += 1
        
        return preference_count

def main():
    parser = argparse.ArgumentParser(description='序列组织分析')
    parser.add_argument('--input', required=True, help='转写文件')
    parser.add_argument('--output', required=True, help='输出文件')
    args = parser.parse_args()
    
    analyzer = SequenceAnalyzer()
    analyzer.load_transcript(args.input)
    
    pairs = analyzer.identify_adjacency_pairs()
    results = {
        'adjacency_pairs': pairs,
        'preference': analyzer.analyze_preference(pairs)
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
