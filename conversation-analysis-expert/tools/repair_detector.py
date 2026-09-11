#!/usr/bin/env python3
"""修复机制识别工具"""

import argparse
import json
import re
from typing import List, Dict

class RepairDetector:
    """修复检测器"""
    
    # 修复发起词
    REPAIR_INITIATORS = ['什么', '哪个', '谁', '哪里', '你是说', '意思是']
    
    def __init__(self):
        self.turns = []
    
    def load_transcript(self, filepath: str) -> None:
        """加载转写文本"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self.turns = json.load(f)
    
    def detect_repairs(self) -> List[Dict]:
        """检测修复序列"""
        repairs = []
        
        for i in range(len(self.turns)):
            turn = self.turns[i]
            text = turn.get('text', '')
            
            # 检查自我修复(话轮内)
            self_repairs = self._detect_self_repair(text)
            if self_repairs:
                repairs.extend([{
                    'type': 'self-initiated-self-repair',
                    'turn_index': i,
                    'position': pos
                } for pos in self_repairs])
            
            # 检查他人发起的修复
            if i > 0:
                other_initiated = self._detect_other_initiated(
                    self.turns[i-1].get('text', ''),
                    text
                )
                if other_initiated:
                    repairs.append({
                        'type': 'other-initiated-self-repair',
                        'turn_index': i,
                        'initiator': self.turns[i-1].get('speaker')
                    })
        
        return repairs
    
    def _detect_self_repair(self, text: str) -> List[int]:
        """检测话轮内自我修复"""
        # 简化规则：查找中断模式
        repairs = []
        # 查找 "//" 或类似标记
        if '//' in text:
            repairs.append(text.index('//'))
        return repairs
    
    def _detect_other_initiated(self, prev_text: str, curr_text: str) -> bool:
        """检测他人发起的修复"""
        # 检查上一话轮是否有修复发起
        return any(init in prev_text for init in self.REPAIR_INITIATORS)
    
    def classify_repair_type(self, repair: Dict) -> str:
        """分类修复类型"""
        return repair.get('type', 'unknown')

def main():
    parser = argparse.ArgumentParser(description='修复机制识别')
    parser.add_argument('--input', required=True, help='转写文件')
    parser.add_argument('--output', required=True, help='输出文件')
    args = parser.parse_args()
    
    detector = RepairDetector()
    detector.load_transcript(args.input)
    
    results = {
        'repairs': detector.detect_repairs(),
        'count': len(detector.detect_repairs())
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
