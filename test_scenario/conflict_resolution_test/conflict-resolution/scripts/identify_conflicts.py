#!/usr/bin/env python
"""
冲突识别工具
识别和分类研究团队中的冲突
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any, Set
from collections import defaultdict

def classify_conflict_type(conflict: Dict) -> str:
    """分类冲突类型"""
    description = conflict.get('description', '').lower()
    type_field = conflict.get('type', '')
    
    # 基于类型字段
    if type_field:
        return type_field
    
    # 基于描述关键词
    if any(keyword in description for keyword in ['方法', '方法论', '理论']):
        return '理论分歧'
    elif any(keyword in description for keyword in ['资源', '资金', '设备', '场地']):
        return '资源分配'
    elif any(keyword in description for keyword in ['作者', '署名', '贡献']):
        return '作者署名'
    elif any(keyword in description for keyword in ['时间', '进度', '期限']):
        return '时间安排'
    elif any(keyword in description for keyword in ['责任', '分工', '任务']):
        return '责任分工'
    else:
        return '其他'

def assess_conflict_intensity(conflict: Dict) -> float:
    """评估冲突强度（0-1）"""
    intensity = 0.5  # 基础强度
    
    # 基于影响级别
    impact = conflict.get('context', {}).get('impact', '')
    if impact == '高':
        intensity += 0.3
    elif impact == '中':
        intensity += 0.1
    
    # 基于时间紧急性
    timeline = conflict.get('context', {}).get('timeline', '')
    if '尽快' in timeline or '立即' in timeline:
        intensity += 0.2
    
    # 基于参与方优先级
    parties = conflict.get('parties', [])
    if parties:
        avg_priority = sum(p.get('priority', 0.5) for p in parties) / len(parties)
        intensity += avg_priority * 0.2
    
    return min(1.0, intensity)

def identify_conflict_patterns(conflicts: List[Dict]) -> Dict:
    """识别冲突模式"""
    patterns = {
        'recurring_parties': defaultdict(int),
        'conflict_clusters': defaultdict(list),
        'escalation_risks': []
    }
    
    # 识别重复参与方
    party_conflicts = defaultdict(list)
    for conflict in conflicts:
        for party in conflict.get('parties', []):
            name = party.get('name', '')
            if name:
                patterns['recurring_parties'][name] += 1
                party_conflicts[name].append(conflict.get('id', ''))
    
    # 识别冲突集群（同一时间段或同一类型）
    for conflict in conflicts:
        conflict_id = conflict.get('id', '')
        conflict_type = classify_conflict_type(conflict)
        phase = conflict.get('context', {}).get('phase', '')
        
        cluster_key = f"{phase}_{conflict_type}"
        patterns['conflict_clusters'][cluster_key].append(conflict_id)
    
    # 识别升级风险
    for name, count in patterns['recurring_parties'].items():
        if count >= 2:
            patterns['escalation_risks'].append({
                'party': name,
                'conflict_count': count,
                'risk_level': '高' if count >= 3 else '中'
            })
    
    return patterns

def calculate_conflict_metrics(conflicts: List[Dict]) -> Dict:
    """计算冲突指标"""
    if not conflicts:
        return {
            'total_conflicts': 0,
            'avg_intensity': 0,
            'high_intensity_count': 0,
            'conflict_types': {},
            'phase_distribution': {}
        }
    
    # 基础统计
    total_conflicts = len(conflicts)
    intensities = [assess_conflict_intensity(c) for c in conflicts]
    avg_intensity = sum(intensities) / len(intensities)
    high_intensity_count = sum(1 for i in intensities if i > 0.7)
    
    # 冲突类型分布
    conflict_types = defaultdict(int)
    for conflict in conflicts:
        conflict_type = classify_conflict_type(conflict)
        conflict_types[conflict_type] += 1
    
    # 阶段分布
    phase_distribution = defaultdict(int)
    for conflict in conflicts:
        phase = conflict.get('context', {}).get('phase', '未知')
        phase_distribution[phase] += 1
    
    return {
        'total_conflicts': total_conflicts,
        'avg_intensity': round(avg_intensity, 3),
        'high_intensity_count': high_intensity_count,
        'conflict_types': dict(conflict_types),
        'phase_distribution': dict(phase_distribution)
    }

def identify_stakeholder_impact(conflicts: List[Dict]) -> Dict:
    """识别利益相关者影响"""
    stakeholder_impact = defaultdict(lambda: {'conflicts': [], 'impact_score': 0})
    
    for conflict in conflicts:
        intensity = assess_conflict_intensity(conflict)
        stakeholders = conflict.get('context', {}).get('stakeholders', [])
        
        for stakeholder in stakeholders:
            stakeholder_impact[stakeholder]['conflicts'].append(conflict.get('id', ''))
            stakeholder_impact[stakeholder]['impact_score'] += intensity
    
    # 计算平均影响
    for stakeholder in stakeholder_impact:
        n_conflicts = len(stakeholder_impact[stakeholder]['conflicts'])
        if n_conflicts > 0:
            stakeholder_impact[stakeholder]['avg_impact'] = \
                stakeholder_impact[stakeholder]['impact_score'] / n_conflicts
        else:
            stakeholder_impact[stakeholder]['avg_impact'] = 0
    
    return dict(stakeholder_impact)

def main():
    parser = argparse.ArgumentParser(
        description='冲突识别工具',
        epilog='示例：python identify_conflicts.py --input conflicts.json --output identified.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入冲突数据文件（JSON）')
    parser.add_argument('--output', '-o', default='identified_conflicts.json', help='输出文件')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 提取冲突数据
    conflicts = data.get('conflicts', [])
    if not conflicts:
        print("错误：未找到冲突数据", file=sys.stderr)
        sys.exit(1)
    
    # 处理每个冲突
    processed_conflicts = []
    for conflict in conflicts:
        processed = conflict.copy()
        processed['classified_type'] = classify_conflict_type(conflict)
        processed['intensity'] = assess_conflict_intensity(conflict)
        processed['n_parties'] = len(conflict.get('parties', []))
        processed['n_attempts'] = len(conflict.get('attempts', []))
        processed_conflicts.append(processed)
    
    # 识别模式和影响
    patterns = identify_conflict_patterns(processed_conflicts)
    metrics = calculate_conflict_metrics(processed_conflicts)
    stakeholder_impact = identify_stakeholder_impact(processed_conflicts)
    
    end_time = datetime.now()
    
    # 准备输出
    output = {
        'summary': {
            'n_conflicts': len(processed_conflicts),
            'conflict_types': list(metrics['conflict_types'].keys()),
            'avg_intensity': metrics['avg_intensity'],
            'high_intensity_conflicts': metrics['high_intensity_count'],
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'conflicts': processed_conflicts,
            'metrics': metrics,
            'patterns': patterns,
            'stakeholder_impact': stakeholder_impact
        },
        'metadata': {
            'input_file': args.input,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'conflict-resolution'
        }
    }
    
    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 冲突识别完成")
        print(f"  - 识别冲突数：{len(processed_conflicts)}")
        print(f"  - 冲突类型：{list(metrics['conflict_types'].keys())}")
        print(f"  - 平均强度：{metrics['avg_intensity']:.3f}")
        print(f"  - 高强度冲突：{metrics['high_intensity_count']}")
        print(f"  - 输出文件：{args.output}")
        
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()