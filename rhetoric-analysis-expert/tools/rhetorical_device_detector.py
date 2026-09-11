#!/usr/bin/env python3
"""修辞格识别工具"""

import argparse
import json
import re

def detect_metaphor(text: str) -> list:
    """检测隐喻"""
    # 简化规则：检测"是"字句中的比喻
    pattern = r'(.+?)是(.+?)的?(?:比喻|象征)?'
    matches = re.findall(pattern, text)
    return [{'type': 'metaphor', 'tenor': m[0], 'vehicle': m[1]} for m in matches]

def detect_simile(text: str) -> list:
    """检测明喻"""
    pattern = r'(.+?)像(.+?)(?:一样)?'
    matches = re.findall(pattern, text)
    return [{'type': 'simile', 'tenor': m[0], 'vehicle': m[1]} for m in matches]

def detect_parallelism(text: str) -> list:
    """检测排比"""
    # 简化：检测重复结构
    results = []
    sentences = text.split('。')
    if len(sentences) >= 3:
        results.append({'type': 'parallelism', 'count': len(sentences)})
    return results

def analyze_rhetorical_devices(text: str) -> dict:
    """分析修辞格"""
    return {
        'metaphors': detect_metaphor(text),
        'similes': detect_simile(text),
        'parallelism': detect_parallelism(text)
    }

def main():
    parser = argparse.ArgumentParser(description='修辞格识别')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = analyze_rhetorical_devices(data.get('text', ''))
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
