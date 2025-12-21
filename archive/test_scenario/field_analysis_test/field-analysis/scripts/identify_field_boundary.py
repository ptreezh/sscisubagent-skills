#!/usr/bin/env python3
"""
场域边界识别工具

功能：
1. 识别场域的核心参与者
2. 分析场域的边界条件
3. 评估场域的自主程度
4. 识别场域的规则体系

标准化接口：argparse + 三层JSON输出
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Set, Any

import numpy as np
import networkx as nx
from sklearn.cluster import KMeans


def identify_core_participants(data: List[Dict], threshold: float = 0.5) -> Dict:
    """识别核心参与者"""
    # 计算每个参与者的综合影响力
    participants = []
    
    for item in data:
        participant = item.get('participant', {})
        
        # 综合评分：教育 + 职位 + 社会资本 + 声望
        education_score = {
            '博士': 5, '硕士': 4, '本科': 3, '大专': 2, '高中': 1, '其他': 0
        }.get(participant.get('education', ''), 0)
        
        position_score = {
            '教授': 5, '副教授': 4, '讲师': 3, '研究员': 3, '其他': 1
        }.get(participant.get('position', ''), 0)
        
        social_score = min(len(participant.get('social_network', {})) / 20.0, 1.0)
        prestige_score = min(participant.get('prestige_score', 0) / 100.0, 1.0)
        
        # 加权平均
        influence = (education_score * 0.3 + 
                    position_score * 0.4 + 
                    social_score * 0.2 + 
                    prestige_score * 0.1)
        
        participants.append({
            'name': participant.get('name', ''),
            'influence': round(influence, 4),
            'education': participant.get('education', ''),
            'position': participant.get('position', '')
        })
    
    # 识别核心参与者
    sorted_participants = sorted(participants, key=lambda x: x['influence'], reverse=True)
    core_threshold = sorted_participants[int(len(sorted_participants) * threshold)]['influence']
    
    core_participants = [p for p in sorted_participants if p['influence'] >= core_threshold]
    peripheral_participants = [p for p in sorted_participants if p['influence'] < core_threshold]
    
    return {
        'core_participants': core_participants,
        'peripheral_participants': peripheral_participants,
        'n_core': len(core_participants),
        'n_peripheral': len(peripheral_participants),
        'influence_threshold': core_threshold
    }


def analyze_field_rules(data: List[Dict], core_participants: List[Dict]) -> Dict:
    """分析场域规则"""
    # 收集规则证据
    rules = {
        'educational_requirements': [],
        'professional_standards': [],
        'social_conventions': [],
        'evaluation_criteria': []
    }
    
    for item in data:
        participant = item.get('participant', {})
        
        # 教育要求
        edu = participant.get('education')
        if edu in ['博士', '硕士', '本科']:
            rules['educational_requirements'].append({
                'participant': participant.get('name', ''),
                'requirement': edu
            })
        
        # 专业标准
        position = participant.get('position', '')
        if position in ['教授', '副教授', '讲师']:
            rules['professional_standards'].append({
                'participant': participant.get('name', ''),
                'standard': position
            })
        
        # 社会惯例
        network = participant.get('social_network', {})
        if len(network) > 10:
            rules['social_conventions'].append({
                'participant': participant.get('name', ''),
                'convention': 'extensive_networking'
            })
        
        # 评价标准
        if participant.get('publications', 0) > 5:
            rules['evaluation_criteria'].append({
                'participant': participant.get('name', ''),
                'criterion': 'publications'
            })
    
    # 分析规则的普遍性
    rule_analysis = {}
    for rule_type, rule_list in rules.items():
        if rule_list:
            # 统计规则出现的频率
            rule_counts = {}
            for rule in rule_list:
                key = rule.get('requirement') or rule.get('standard') or rule.get('convention') or rule.get('criterion')
                rule_counts[key] = rule_counts.get(key, 0) + 1
            
            # 识别主要规则
            if rule_counts:
                main_rule = max(rule_counts.items(), key=lambda x: x[1])[0]
                frequency = rule_counts[main_rule] / len(core_participants) if core_participants else 0
            else:
                main_rule = None
                frequency = 0
            
            rule_analysis[rule_type] = {
                'main_rule': main_rule,
                'frequency': round(frequency, 3),
                'n_rules': len(rule_list)
            }
    
    return {
        'rules': rules,
        'analysis': rule_analysis,
        'rule_strength': {
            'strong': sum(1 for r in rule_analysis.values() if r['frequency'] > 0.5),
            'moderate': sum(1 for r in rule_analysis.values() if 0.2 <= r['frequency'] <= 0.5),
            'weak': sum(1 for r in rule_analysis.values() if r['frequency'] < 0.2)
        }
    }


def assess_autonomy(data: List[Dict], external_influences: List[str] = None) -> Dict:
    """评估场域自主性"""
    if external_influences is None:
        external_influences = ['政府政策', '市场力量', '媒体影响', '公众舆论', '国际标准']
    
    # 分析外部影响
    external_scores = {}
    for influence in external_influences:
        # 检查参与者是否提到外部影响
        affected_count = 0
        for item in data:
            if influence in str(item).lower():
                affected_count += 1
        
        external_scores[influence] = affected_count / len(data)
    
    # 计算自主性分数
    total_external_influence = sum(external_scores.values())
    autonomy_score = max(0, 1 - total_external_influence / len(external_influences))
    
    # 解释标准
    if autonomy_score >= 0.8:
        autonomy_level = "高度自主"
    elif autonomy_score >= 0.6:
        autonomy_level = "中等自主"
    elif autonomy_score >= 0.4:
        autonomy_level = "低度自主"
    else:
        autonomy_level = "高度依赖"
    
    return {
        'autonomy_score': round(autonomy_score, 4),
        'autonomy_level': autonomy_level,
        'external_influences': external_scores,
        'n_external_factors': len(external_influences),
        'affected_participants': int(total_external_influence * len(data))
    }


def main():
    parser = argparse.ArgumentParser(
        description='场域边界识别工具',
        epilog='示例：python identify_field_boundary.py --input data.json --output boundary.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--output', '-o', default='field_boundary.json', help='输出文件')
    parser.add_argument('--threshold', '-t', type=float, default=0.5, help='核心参与者阈值（默认：0.5）')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if isinstance(data, dict):
            if 'data' in data:
                data = data['data']
            else:
                data = [data]
        elif not isinstance(data, list):
            data = [data]
    
    except Exception as e:
        print(f"错误：{e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 识别核心参与者
    core_analysis = identify_core_participants(data, args.threshold)
    
    # 分析场域规则
    rules_analysis = analyze_field_rules(data, core_analysis['core_participants'])
    
    # 评估自主性
    autonomy_analysis = assess_autonomy(data)
    
    end_time = datetime.now()
    
    # 标准化输出
    output = {
        'summary': {
            'field_name': '学术场域',
            'n_participants': len(data),
            'n_core': core_analysis['n_core'],
            'autonomy_level': autonomy_analysis['autonomy_level'],
            'autonomy_score': autonomy_analysis['autonomy_score'],
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'core_participants': core_analysis['core_participants'],
            'peripheral_participants': core_analysis['peripheral_participants'],
            'field_rules': rules_analysis['rules'],
            'rule_analysis': rules_analysis['analysis'],
            'autonomy_analysis': autonomy_analysis
        },
        'metadata': {
            'input_file': args.input,
            'threshold': args.threshold,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'field-analysis'
        }
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 场域边界识别完成")
    print(f"  - 参与者数：{len(data)}")
    print(f"  - 核心参与者：{core_analysis['n_core']}")
    print(f"  - 自主性水平：{autonomy_analysis['autonomy_level']}")
    print(f"  - 输出文件：{args.output}")


if __name__ == '__main__':
    main()