#!/usr/bin/env python3
"""媒介化追踪工具"""

import argparse
import json

def track_mediatization(domain_data: dict) -> dict:
    """追踪媒介化过程"""
    return {
        'level': assess_mediatization_level(domain_data),
        'process': analyze_mediatization_process(domain_data),
        'effects': analyze_effects(domain_data)
    }

def assess_mediatization_level(domain_data: dict) -> str:
    """评估媒介化程度"""
    indicators = domain_data.get('mediatization_indicators', {})
    
    score = 0
    if indicators.get('media_dependency', False):
        score += 1
    if indicators.get('media_logic_adoption', False):
        score += 1
    if indicators.get('media_infrastructure', False):
        score += 1
    
    if score >= 3:
        return 'strong'
    elif score >= 2:
        return 'medium'
    else:
        return 'weak'

def analyze_mediatization_process(domain_data: dict) -> dict:
    """分析媒介化过程"""
    return {
        'extension': domain_data.get('media_extension', 'ongoing'),
        'substitution': domain_data.get('media_substitution', 'partial'),
        'convergence': domain_data.get('media_convergence', 'emerging'),
        'differentiation': domain_data.get('institutional_differentiation', 'moderate')
    }

def analyze_effects(domain_data: dict) -> dict:
    """分析媒介化效果"""
    return {
        'structural': domain_data.get('structural_changes', []),
        'cultural': domain_data.get('cultural_changes', []),
        'identity': domain_data.get('identity_changes', [])
    }

def main():
    parser = argparse.ArgumentParser(description='媒介化追踪')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = track_mediatization(data)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
