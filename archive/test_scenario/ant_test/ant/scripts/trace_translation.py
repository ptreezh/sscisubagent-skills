#!/usr/bin/env python
"""
ANT转译追踪工具
追踪行动者网络中的转译过程和关键时刻
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

def analyze_translation_phases(moments: List[Dict]) -> Dict:
    """分析转译的四个阶段"""
    phases = {
        '问题化': {
            'description': '将问题定义并确立主导地位',
            'key_characteristics': [],
            'primary_actors': [],
            'enrollment_strategies': [],
            'controversies': []
        },
        '利益介入': {
            'description': '通过利益机制吸引其他行动者',
            'key_characteristics': [],
            'primary_actors': [],
            'enrollment_strategies': [],
            'controversies': []
        },
        '动员': {
            'description': '确保各方履行承诺和角色',
            'key_characteristics': [],
            'primary_actors': [],
            'enrollment_strategies': [],
            'controversies': []
        },
        '巩固': {
            'description': '稳定网络并维持联盟',
            'key_characteristics': [],
            'primary_actors': [],
            'enrollment_strategies': [],
            'controversies': []
        }
    }
    
    # 分析每个阶段
    for moment in moments:
        phase_name = moment.get('phase', '')
        if phase_name in phases:
            phases[phase_name]['primary_actors'].append(moment.get('primary_actor', ''))
            phases[phase_name]['enrollment_strategies'] = moment.get('enrolled_actors', [])
            phases[phase_name]['controversies'].extend(moment.get('controversies', []))
            
            # 提取关键特征
            description = moment.get('description', '')
            phases[phase_name]['key_characteristics'].append(description)
    
    return phases

def identify_enrollment_mechanisms(data: Dict) -> Dict:
    """识别招募机制"""
    mechanisms = {
        '政策激励': {
            'description': '通过政策工具吸引行动者',
            'examples': [],
            'effectiveness': 0.0
        },
        '利益交换': {
            'description': '通过利益共享建立联盟',
            'examples': [],
            'effectiveness': 0.0
        },
        '技术标准化': {
            'description': '通过技术标准统一行动',
            'examples': [],
            'effectiveness': 0.0
        },
        '话语构建': {
            'description': '通过共同话语凝聚共识',
            'examples': [],
            'effectiveness': 0.0
        },
        '基础设施': {
            'description': '通过物质设施支撑网络',
            'examples': [],
            'effectiveness': 0.0
        }
    }
    
    # 从案例中提取机制实例
    actors = data.get('actors', [])
    relations = data.get('network_relations', [])
    moments = data.get('translation_moments', [])
    
    # 分析政策激励
    for actor in actors:
        if '政府' in actor.get('name', '') or '市' in actor.get('name', ''):
            actions = actor.get('actions', [])
            for action in actions:
                if '政策' in action or '补贴' in action:
                    mechanisms['政策激励']['examples'].append(f"{actor.get('name', '')}: {action}")
    
    # 分析利益交换
    for relation in relations:
        if relation.get('type') in ['产品供应', '服务支持']:
            mechanisms['利益交换']['examples'].append(
                f"{relation.get('from')} → {relation.get('to')}: {relation.get('type')}"
            )
    
    # 分析技术标准化
    case_study = data.get('case_study', '')
    if '标准' in case_study or '技术' in case_study:
        mechanisms['技术标准化']['examples'].append('技术标准统一')
    
    # 计算有效性（简化版）
    for key in mechanisms:
        mechanisms[key]['effectiveness'] = len(mechanisms[key]['examples']) * 0.2
    
    return mechanisms

def trace_controversy_resolution(moments: List[Dict]) -> Dict:
    """追踪争议解决过程"""
    controversies = {
        'identified_controversies': [],
        'resolution_strategies': {},
        'resolution_outcomes': {},
        'persistent_issues': []
    }
    
    # 收集所有争议
    all_controversies = []
    for moment in moments:
        phase = moment.get('phase', '')
        moment_controversies = moment.get('controversies', [])
        
        for controversy in moment_controversies:
            all_controversies.append({
                'controversy': controversy,
                'phase': phase,
                'primary_actor': moment.get('primary_actor', '')
            })
    
    controversies['identified_controversies'] = all_controversies
    
    # 分析解决策略（简化版）
    resolution_patterns = {
        '政策调整': ['补贴标准', '政策支持'],
        '技术协商': ['技术路线', '标准统一'],
        '利益协调': ['利益分配', '责任分担'],
        '制度创新': ['法规制定', '机制设计']
    }
    
    for strategy, keywords in resolution_patterns.items():
        controversies['resolution_strategies'][strategy] = []
        for controversy in all_controversies:
            for keyword in keywords:
                if keyword in controversy['controversy']:
                    controversies['resolution_strategies'][strategy].append(controversy)
                    break
    
    # 评估解决结果
    for strategy, items in controversies['resolution_strategies'].items():
        controversies['resolution_outcomes'][strategy] = {
            'addressed_count': len(items),
            'resolution_rate': len(items) / len(all_controversies) if all_controversies else 0
        }
    
    return controversies

def calculate_network_stability(actors: List[Dict], relations: List[Dict], moments: List[Dict]) -> Dict:
    """计算网络稳定性"""
    stability_metrics = {
        'actor_stability': 0.0,
        'relation_stability': 0.0,
        'goal_alignment': 0.0,
        'overall_stability': 0.0
    }
    
    # 行动者稳定性（基于参与持续性）
    if moments:
        enrolled_per_phase = []
        for moment in moments:
            enrolled_per_phase.append(len(moment.get('enrolled_actors', [])))
        
        if enrolled_per_phase:
            avg_enrollment = sum(enrolled_per_phase) / len(enrolled_per_phase)
            max_enrollment = max(enrolled_per_phase)
            stability_metrics['actor_stability'] = avg_enrollment / max_enrollment if max_enrollment > 0 else 0
    
    # 关系稳定性（基于关系强度）
    if relations:
        strengths = [rel.get('strength', 0) for rel in relations]
        stability_metrics['relation_stability'] = sum(strengths) / len(strengths) if strengths else 0
    
    # 目标一致性（基于利益重叠）
    actor_interests = {}
    for actor in actors:
        interests = set(actor.get('interests', []))
        actor_interests[actor.get('name', '')] = interests
    
    # 计算利益重叠度
    total_overlap = 0
    comparisons = 0
    actors_list = list(actor_interests.keys())
    
    for i in range(len(actors_list)):
        for j in range(i + 1, len(actors_list)):
            interests_i = actor_interests[actors_list[i]]
            interests_j = actor_interests[actors_list[j]]
            
            if interests_i and interests_j:
                overlap = len(interests_i & interests_j) / len(interests_i | interests_j)
                total_overlap += overlap
                comparisons += 1
    
    stability_metrics['goal_alignment'] = total_overlap / comparisons if comparisons > 0 else 0
    
    # 总体稳定性
    stability_metrics['overall_stability'] = (
        stability_metrics['actor_stability'] * 0.3 +
        stability_metrics['relation_stability'] * 0.4 +
        stability_metrics['goal_alignment'] * 0.3
    )
    
    return stability_metrics

def identify_key_moments(moments: List[Dict]) -> Dict:
    """识别关键时刻"""
    key_moments = {
        'turning_points': [],
        'critical_decisions': [],
        'enrollment_peaks': [],
        'crisis_points': []
    }
    
    for i, moment in enumerate(moments):
        phase = moment.get('phase', '')
        enrolled = moment.get('enrolled_actors', [])
        controversies = moment.get('controversies', [])
        
        # 转折点（阶段转换）
        if i > 0:
            prev_enrolled = moments[i-1].get('enrolled_actors', [])
            if len(enrolled) > len(prev_enrolled) * 1.5:
                key_moments['turning_points'].append({
                    'phase': phase,
                    'description': f"招募显著增加：{len(prev_enrolled)} → {len(enrolled)}",
                    'moment_index': i
                })
        
        # 关键决策（争议最多的阶段）
        if len(controversies) >= 2:
            key_moments['critical_decisions'].append({
                'phase': phase,
                'controversies_count': len(controversies),
                'controversies': controversies,
                'moment_index': i
            })
        
        # 招募高峰
        if len(enrolled) >= 3:
            key_moments['enrollment_peaks'].append({
                'phase': phase,
                'enrolled_count': len(enrolled),
                'enrolled_actors': enrolled,
                'moment_index': i
            })
        
        # 危机点（无争议但招募少的阶段）
        if len(controversies) == 0 and len(enrolled) <= 1:
            key_moments['crisis_points'].append({
                'phase': phase,
                'description': "进展缓慢，缺乏动力",
                'moment_index': i
            })
    
    return key_moments

def main():
    parser = argparse.ArgumentParser(
        description='ANT转译追踪工具',
        epilog='示例：python trace_translation.py --input data.json --output translation.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--output', '-o', default='translation_trace.json', help='输出文件')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 提取数据
    moments = data.get('translation_moments', [])
    actors = data.get('actors', [])
    relations = data.get('network_relations', [])
    
    # 分析转译过程
    phases = analyze_translation_phases(moments)
    mechanisms = identify_enrollment_mechanisms(data)
    controversies = trace_controversy_resolution(moments)
    stability = calculate_network_stability(actors, relations, moments)
    key_moments = identify_key_moments(moments)
    
    end_time = datetime.now()
    
    # 标准化输出
    output = {
        'summary': {
            'case_study': data.get('case_study', ''),
            'n_phases': len(moments),
            'n_mechanisms': len([m for m in mechanisms.values() if m['examples']]),
            'overall_stability': round(stability['overall_stability'], 3),
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'translation_phases': phases,
            'enrollment_mechanisms': mechanisms,
            'controversy_resolution': controversies,
            'stability_analysis': stability,
            'key_moments': key_moments
        },
        'metadata': {
            'input_file': args.input,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'ant'
        }
    }
    
    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"✓ 转译追踪完成")
        print(f"  - 转译阶段：{len(moments)}")
        print(f"  - 招募机制：{len([m for m in mechanisms.values() if m['examples']])}")
        print(f"  - 网络稳定性：{stability['overall_stability']:.3f}")
        print(f"  - 输出文件：{args.output}")
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()