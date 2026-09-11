#!/usr/bin/env python3
"""论证分析工具"""

import argparse
import json

def extract_premises(text: str) -> list:
    """提取前提"""
    premises = []
    markers = ['因为', '由于', '鉴于', '既然']
    for marker in markers:
        if marker in text:
            parts = text.split(marker)
            if len(parts) > 1:
                premises.append({
                    'marker': marker,
                    'content': parts[1].split('所以')[0].strip() if '所以' in parts[1] else parts[1].strip()
                })
    return premises

def extract_conclusion(text: str) -> dict:
    """提取结论"""
    markers = ['所以', '因此', '故', '由此可见']
    for marker in markers:
        if marker in text:
            parts = text.split(marker)
            if len(parts) > 1:
                return {'marker': marker, 'content': parts[-1].strip()}
    return None

def analyze_argument(text: str) -> dict:
    """分析论证结构"""
    return {
        'premises': extract_premises(text),
        'conclusion': extract_conclusion(text),
        'type': 'enthymeme' if '因为' in text or '所以' in text else 'narrative'
    }

def main():
    parser = argparse.ArgumentParser(description='论证分析')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = analyze_argument(data.get('text', ''))
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
