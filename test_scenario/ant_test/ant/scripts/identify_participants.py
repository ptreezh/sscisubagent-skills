#!/usr/bin/env python
"""
ANT参与者识别工具
识别行动者网络中的所有人类和非人类行动者
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

def extract_human_actors(data: Dict) -> List[Dict]:
    """提取人类行动者"""
    actors = data.get('actors', [])
    human_actors = []
    
    for actor in actors:
        if actor.get('type') in ['机构', '企业', 'NGO', '公众']:
            human_actors.append({
                'name': actor.get('name', ''),
                'type': actor.get('type', ''),
                'role': actor.get('role', ''),
                'agency': calculate_agency_score(actor),
                'interests': actor.get('interests', []),
                'resources': actor.get('resources', []),
                'actions': actor.get('actions', [])
            })
    
    return human_actors

def extract_nonhuman_actors(data: Dict) -> List[Dict]:
    """提取非人类行动者"""
    nonhuman_actors = []
    
    # 从网络关系中识别非人类行动者
    relations = data.get('network_relations', [])
    for relation in relations:
        # 识别技术、制度、概念等非人类行动者
        if relation.get('type') in ['技术标准', '法规', '基础设施', '概念框架']:
            nonhuman_actors.append({
                'name': relation.get('type'),
                'type': '非人类行动者',
                'role': relation.get('type'),
                'agency': calculate_nonhuman_agency(relation),
                'influence': relation.get('strength', 0.5)
            })
    
    # 添加常见的非人类行动者
    case_study = data.get('case_study', '')
    if '新能源汽车' in case_study:
        nonhuman_actors.extend([
            {
                'name': '电池技术',
                'type': '非人类行动者',
                'role': '技术',
                'agency': 0.7,
                'influence': 0.8
            },
            {
                'name': '充电标准',
                'type': '非人类行动者',
                'role': '标准',
                'agency': 0.6,
                'influence': 0.7
            },
            {
                'name': '补贴政策',
                'type': '非人类行动者',
                'role': '制度',
                'agency': 0.8,
                'influence': 0.9
            }
        ])
    
    return nonhuman_actors

def calculate_agency_score(actor: Dict) -> float:
    """计算行动者的能动性得分"""
    score = 0.0
    
    # 基于资源数量
    resources = actor.get('resources', [])
    score += len(resources) * 0.1
    
    # 基于行动数量
    actions = actor.get('actions', [])
    score += len(actions) * 0.1
    
    # 基于利益多样性
    interests = actor.get('interests', [])
    score += len(interests) * 0.05
    
    # 基于角色重要性
    role = actor.get('role', '')
    if '制定' in role or '提供' in role:
        score += 0.3
    elif '监督' in role or '使用' in role:
        score += 0.2
    
    return min(score, 1.0)

def calculate_nonhuman_agency(relation: Dict) -> float:
    """计算非人类行动者的能动性"""
    strength = relation.get('strength', 0.5)
    type_multipliers = {
        '政策支持': 0.9,
        '技术标准': 0.8,
        '基础设施': 0.7,
        '法规': 0.9,
        '概念框架': 0.6
    }
    
    relation_type = relation.get('type', '')
    multiplier = type_multipliers.get(relation_type, 0.5)
    
    return strength * multiplier

def analyze_actor_network(actors: List[Dict]) -> Dict:
    """分析行动者网络结构"""
    n_actors = len(actors)
    
    # 计算能动性分布
    agency_scores = [actor.get('agency', 0) for actor in actors]
    avg_agency = sum(agency_scores) / n_actors if n_actors > 0 else 0
    
    # 识别关键行动者（能动性>0.7）
    key_actors = [actor for actor in actors if actor.get('agency', 0) > 0.7]
    
    # 分析行动者类型分布
    type_counts = {}
    for actor in actors:
        actor_type = actor.get('type', '未知')
        type_counts[actor_type] = type_counts.get(actor_type, 0) + 1
    
    return {
        'total_actors': n_actors,
        'average_agency': round(avg_agency, 3),
        'key_actors_count': len(key_actors),
        'key_actors': [actor.get('name') for actor in key_actors],
        'type_distribution': type_counts,
        'network_density': calculate_network_density(actors)
    }

def calculate_network_density(actors: List[Dict]) -> float:
    """计算网络密度（简化版）"""
    n = len(actors)
    if n < 2:
        return 0.0
    
    # 假设网络中的实际连接数
    # 这里使用简化计算，实际应该基于网络关系数据
    potential_connections = n * (n - 1) / 2
    
    # 估算实际连接数（基于行动者的资源 overlap）
    actual_connections = 0
    for i in range(n):
        for j in range(i + 1, n):
            resources_i = set(actors[i].get('resources', []))
            resources_j = set(actors[j].get('resources', []))
            if resources_i & resources_j:
                actual_connections += 1
    
    return actual_connections / potential_connections

def main():
    parser = argparse.ArgumentParser(
        description='ANT参与者识别工具',
        epilog='示例：python identify_participants.py --input data.json --output participants.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入数据文件（JSON）')
    parser.add_argument('--output', '-o', default='participants.json', help='输出文件')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 识别行动者
    human_actors = extract_human_actors(data)
    nonhuman_actors = extract_nonhuman_actors(data)
    all_actors = human_actors + nonhuman_actors
    
    # 分析网络
    network_analysis = analyze_actor_network(all_actors)
    
    end_time = datetime.now()
    
    # 标准化输出
    output = {
        'summary': {
            'case_study': data.get('case_study', ''),
            'n_human_actors': len(human_actors),
            'n_nonhuman_actors': len(nonhuman_actors),
            'n_total_actors': len(all_actors),
            'network_density': network_analysis['network_density'],
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'human_actors': human_actors,
            'nonhuman_actors': nonhuman_actors,
            'network_analysis': network_analysis
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
        print(f"✓ 参与者识别完成")
        print(f"  - 人类行动者：{len(human_actors)}")
        print(f"  - 非人类行动者：{len(nonhuman_actors)}")
        print(f"  - 网络密度：{network_analysis['network_density']:.3f}")
        print(f"  - 输出文件：{args.output}")
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()