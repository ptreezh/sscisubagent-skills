#!/usr/bin/env python3
"""媒介生态分析工具"""

import argparse
import json

def analyze_medium_ecology(medium_data: dict) -> dict:
    """分析媒介生态"""
    return {
        'technology': analyze_technology(medium_data),
        'institution': analyze_institution(medium_data),
        'culture': analyze_culture(medium_data)
    }

def analyze_technology(medium_data: dict) -> dict:
    """分析媒介技术"""
    return {
        'type': medium_data.get('medium_type', 'digital'),
        'affordances': medium_data.get('affordances', []),
        'bias': detect_bias(medium_data),
        'extension': medium_data.get('human_extension', 'cognitive')
    }

def detect_bias(medium_data: dict) -> dict:
    """检测媒介偏向"""
    return {
        'time_space': medium_data.get('time_bias', False) and 'time' or 'space',
        'sensory': medium_data.get('primary_sense', 'visual'),
        'participation': medium_data.get('participation_level', 'medium')
    }

def analyze_institution(medium_data: dict) -> dict:
    """分析媒介制度"""
    return {
        'ownership': medium_data.get('ownership_type', 'private'),
        'regulation': medium_data.get('regulation_level', 'moderate'),
        'business_model': medium_data.get('business_model', 'advertising')
    }

def analyze_culture(medium_data: dict) -> dict:
    """分析媒介文化"""
    return {
        'content_types': medium_data.get('content_types', []),
        'audience_size': medium_data.get('audience_size', 'mass'),
        'cultural_impact': 'high' if medium_data.get('penetration', 0) > 0.5 else 'medium'
    }

def main():
    parser = argparse.ArgumentParser(description='媒介生态分析')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = analyze_medium_ecology(data)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
