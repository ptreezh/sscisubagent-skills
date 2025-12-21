#!/usr/bin/env python3
"""
场域自主性评估工具

功能：
1. 计算自主性指数
2. 分析外部依赖关系
3. 识别权力结构
4. 评估场域稳定性

标准化接口：argparse + 三层JSON输出
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Set

import numpy as np


def calculate_autonomy_index(data: List[Dict], external_factors: Dict[str, float]) -> Dict:
    """计算自主性指数"""
    # 内部因素权重
    internal_weights = {
        'internal_decision_making': 0.3,
        'self_governance': 0.3,
        'resource_control': 0.2,
        'norm_autonomy': 0.2
    }
    
    # 收集内部自主性数据
    internal_scores = {}
    
    for factor, weight in internal_weights.items():
        scores = []
        for item in data:
            participant = item.get('participant', {})
            
            if factor == 'internal_decision_making':
                # 参与内部决策的程度
                decision_participation = participant.get('decision_participation', 0.5)
                scores.append(decision_participation)
            
            elif factor == 'self_governance':
                # 内部治理机制的有效性
                governance_effectiveness = participant.get('governance_effectiveness', 0.5)
                scores.append(governance_effectiveness)
            
            elif factor == 'resource_control':
                # 控制关键资源的程度
                resource_control = participant.get('resource_control', 0.5)
                scores.append(resource_control)
            
            elif factor == 'norm_autonomy':
                # 遵守内部规范的程度
                norm_compliance = participant.get('norm_compliance', 0.5)
                scores.append(norm_compliance)
        
        if scores:
            internal_scores[factor] = {
                'mean': round(np.mean(scores), 4),
                'std': round(np.std(scores), 4),
                'weight': weight
            }
    
    # 计算内部自主性指数
    internal_autonomy = sum(
        scores['mean'] * scores['weight'] 
        for scores in internal_scores.values()
    )
    
    # 计算外部依赖指数
    external_dependency = sum(external_factors.values()) / len(external_factors)
    
    # 自主性指数 = 内部自主性 - 外部依赖
    autonomy_index = max(0, min(1, internal_autonomy - external_dependency))
    
    return {
        'autonomy_index': round(autonomy_index, 4),
        'internal_autonomy': round(internal_autonomy, 4),
        'external_dependency': round(external_dependency, 4),
        'internal_scores': internal_scores,
        'external_factors': external_factors
    }


def analyze_power_structure(data: List[Dict], core_participants: List[str]) -> Dict:
    """分析权力结构"""
    # 构建权力网络
    power_matrix = {}
    participant_names = [p.get('name', '') for p in data]
    
    for i, item in enumerate(data):
        participant = item.get('participant', {})
        name = participant.get('name', '')
        network = participant.get('power_network', {})
        
        for target, strength in network.items():
            if target in participant_names:
                power_matrix[(name, target)] = strength
    
    # 计算权力中心性
    power_centrality = {}
    for name in participant_names:
        outgoing = sum(power_matrix.get((name, target), 0) for target in participant_names)
        incoming = sum(power_matrix.get((target, name), 0) for target in participant_names)
        power_centrality[name] = outgoing + incoming
    
    # 识别权力结构
    if power_centrality:
        max_power = max(power_centrality.values())
        min_power = min(power_centrality.values())
        power_range = max_power - min_power
        
        if power_range > 0:
            power_levels = {}
            for name, power in power_centrality.items():
                normalized = (power - min_power) / power_range
                if normalized >= 0.8:
                    power_levels[name] = 'dominant'
                elif normalized >= 0.4:
                    power_levels[name] = 'influential'
                else:
                    power_levels[name] = 'peripheral'
        else:
            power_levels = {name: 'equal' for name in participant_names}
    else:
        power_levels = {}
    
    # 核心参与者的权力地位
    core_power = {name: power_centrality.get(name, 0) 
                  for name in core_participants if name in power_centrality}
    
    return {
        'power_centrality': power_centrality,
        'power_levels': power_levels,
        'core_power': core_power,
        'power_structure': {
            'hierarchical': len(set(power_levels.values())) > 2,
            'dominant_count': list(power_levels.values()).count('dominant'),
            'peripheral_count': list(power_levels.values()).count('peripheral')
        }
    }


def assess_field_stability(autonomy_index: float, power_structure: Dict) -> Dict:
    """评估场域稳定性"""
    # 稳定性因素
    stability_factors = {
        'autonomy': autonomy_index,
        'power_concentration': 1 - (power_structure['power_structure']['peripheral_count'] / 
                                  len(power_structure['power_levels'])),
        'rule_consistency': 0.8,  # 假设值，需要从规则分析中获取
        'resource_stability': 0.7  # 假设值，需要从数据分析中获取
    }
    
    # 计算稳定性指数
    stability_index = np.mean(list(stability_factors.values()))
    
    # 解释标准
    if stability_index >= 0.8:
        stability_level = "高度稳定"
    elif stability_index >= 0.6:
        stability_level = "中等稳定"
    elif stability_index >= 0.4:
        stability_level = "低度稳定"
    else:
        stability_level = "不稳定"
    
    return {
        'stability_index': round(stability_index, 4),
        'stability_level': stability_level,
        'stability_factors': stability_factors,
        'risk_factors': [
            factor for factor, score in stability_factors.items() if score < 0.5
        ]
    }


def main():
    parser = argparse.ArgumentParser(
        description='场域自主性评估工具',
        epilog='示例：python assess_autonomy.py --input data.json --output autonomy.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--output', '-o', default='autonomy.json', help='输出文件')
    parser.add_argument('--external-factors', help='外部因素权重（JSON格式）')
    
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
    
    # 读取外部因素
    external_factors = {
        'political_pressure': 0.3,
        'market_forces': 0.2,
        'media_influence': 0.2,
        'international_standards': 0.1
    }
    
    if args.external_factors:
        try:
            with open(args.external_factors, 'r', encoding='utf-8') as f:
                custom_factors = json.load(f)
            external_factors.update(custom_factors)
        except:
            pass
    
    start_time = datetime.now()
    
    # 识别核心参与者（简化版）
    core_participants = []
    for item in data:
        participant = item.get('participant', {})
        if participant.get('influence', 0) > 0.7:
            core_participants.append(participant.get('name', ''))
    
    # 计算自主性指数
    autonomy_analysis = calculate_autonomy_index(data, external_factors)
    
    # 分析权力结构
    power_analysis = analyze_power_structure(data, core_participants)
    
    # 评估稳定性
    stability_analysis = assess_field_stability(
        autonomy_analysis['autonomy_index'],
        power_analysis
    )
    
    end_time = datetime.now()
    
    # 标准化输出
    output = {
        'summary': {
            'autonomy_index': autonomy_analysis['autonomy_index'],
            'autonomy_level': autonomy_analysis['autonomy_index'] >= 0.6,
            'stability_index': stability_analysis['stability_index'],
            'stability_level': stability_analysis['stability_level'],
            'n_participants': len(data),
            'n_core_participants': len(core_participants),
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'autonomy_analysis': autonomy_analysis,
            'power_analysis': power_analysis,
            'stability_analysis': stability_analysis
        },
        'metadata': {
            'input_file': args.input,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'field-analysis'
        }
    }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"✓ 场域自主性评估完成")
    print(f"  - 自主性指数：{autonomy_analysis['autonomy_index']:.4f}")
    print(f"  - 稳定性指数：{stability_analysis['stability_index']:.4f}")
    print(f"  - 核心参与者：{len(core_participants)}")
    print(f"  - 输出文件：{args.output}")


if __name__ == '__main__':
    main()