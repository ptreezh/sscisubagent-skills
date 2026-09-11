#!/usr/bin/env python3
"""说服策略评估工具"""

import argparse
import json

def evaluate_logos(text: str) -> dict:
    """评估逻辑诉求"""
    score = 0
    indicators = ['因为', '所以', '因此', '证据', '数据', '研究', '证明']
    for ind in indicators:
        if ind in text:
            score += 1
    return {'score': min(score, 5), 'level': 'high' if score >= 3 else 'low'}

def evaluate_pathos(text: str) -> dict:
    """评估情感诉求"""
    score = 0
    indicators = ['悲伤', '愤怒', '恐惧', '希望', '痛苦', '幸福', '爱']
    for ind in indicators:
        if ind in text:
            score += 1
    return {'score': min(score, 5), 'level': 'high' if score >= 3 else 'low'}

def evaluate_ethos(text: str) -> dict:
    """评估人格诉求"""
    score = 0
    indicators = ['我们', '我', '相信', '承诺', '责任', '诚信', '专业']
    for ind in indicators:
        if ind in text:
            score += 1
    return {'score': min(score, 5), 'level': 'high' if score >= 3 else 'low'}

def evaluate_persuasion(text: str) -> dict:
    """综合评估说服策略"""
    logos = evaluate_logos(text)
    pathos = evaluate_pathos(text)
    ethos = evaluate_ethos(text)
    
    return {
        'logos': logos,
        'pathos': pathos,
        'ethos': ethos,
        'overall': (logos['score'] + pathos['score'] + ethos['score']) / 3,
        'dominant': max(['logos', 'pathos', 'ethos'], 
                       key=lambda x: locals()[x]['score'])
    }

def main():
    parser = argparse.ArgumentParser(description='说服策略评估')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = evaluate_persuasion(data.get('text', ''))
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
