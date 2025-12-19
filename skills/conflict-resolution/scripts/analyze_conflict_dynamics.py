#!/usr/bin/env python
"""
冲突动态分析工具
分析冲突的发展趋势和解决难度
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any
import numpy as np

def calculate_resolution_difficulty(conflict: Dict) -> float:
    """计算解决难度（0-1）"""
    difficulty = 0.3  # 基础难度
    
    # 基于强度
    intensity = conflict.get('intensity', 0.5)
    difficulty += intensity * 0.3
    
    # 基于参与方数量
    n_parties = conflict.get('n_parties', 2)
    if n_parties > 2:
        difficulty += 0.1 * (n_parties - 2)
    
    # 基于尝试次数
    n_attempts = conflict.get('n_attempts', 0)
    if n_attempts > 0:
        difficulty += 0.1 * min(n_attempts, 3)  # 最多增加0.3
    
    # 基于冲突类型
    conflict_type = conflict.get('classified_type', '')
    if conflict_type == '理论分歧':
        difficulty += 0.2
    elif conflict_type == '资源分配':
        difficulty += 0.15
    elif conflict_type == '作者署名':
        difficulty += 0.25
    
    return min(1.0, difficulty)

def analyze_escalation_history(conflict: Dict) -> Dict:
    """分析冲突升级历史"""
    attempts = conflict.get('attempts', [])
    
    if not attempts:
        return {
            'escalation_level': '稳定',
            'trend': '无',
            'n_attempts': 0
        }
    
    # 分析解决尝试的模式
    outcomes = [attempt.get('outcome', '') for attempt in attempts]
    
    # 计算升级趋势
    negative_outcomes = sum(1 for o in outcomes if '未' in o or '失败' in o)
    escalation_score = negative_outcomes / len(outcomes) if outcomes else 0
    
    if escalation_score > 0.7:
        escalation_level = '高度升级'
        trend = '恶化'
    elif escalation_score > 0.4:
        escalation_level = '中度升级'
        trend = '波动'
    else:
        escalation_level = '稳定'
        trend = '改善'
    
    return {
        'escalation_level': escalation_level,
        'trend': trend,
        'n_attempts': len(attempts),
        'success_rate': 1 - escalation_score
    }

def predict_resolution_timeline(conflict: Dict) -> Dict:
    """预测解决时间线"""
    difficulty = calculate_resolution_difficulty(conflict)
    intensity = conflict.get('intensity', 0.5)
    
    # 基础时间（周）
    base_timeline = 4
    
    # 根据难度调整
    if difficulty > 0.8:
        base_timeline *= 3
    elif difficulty > 0.6:
        base_timeline *= 2
    
    # 根据强度调整
    if intensity > 0.8:
        base_timeline *= 1.5
    
    # 根据历史尝试调整
    n_attempts = conflict.get('n_attempts', 0)
    if n_attempts > 2:
        base_timeline *= 1.2
    
    # 生成时间线预测
    timeline = {
        'optimistic': int(base_timeline * 0.7),
        'realistic': int(base_timeline),
        'pessimistic': int(base_timeline * 1.5)
    }
    
    return timeline

def identify_resolution_blockers(conflict: Dict) -> List[str]:
    """识别解决障碍"""
    blockers = []
    
    # 基于冲突类型
    conflict_type = conflict.get('classified_type', '')
    if conflict_type == '理论分歧':
        blockers.append('理论框架差异')
        blockers.append('方法论争议')
    elif conflict_type == '资源分配':
        blockers.append('资源限制')
        blockers.append('优先级冲突')
    elif conflict_type == '作者署名':
        blockers.append('贡献认定困难')
        blockers.append('公平性争议')
    
    # 基于参与方特征
    parties = conflict.get('parties', [])
    if len(parties) > 2:
        blockers.append('多方协调复杂')
    
    # 基于历史
    if conflict.get('n_attempts', 0) > 2:
        blockers.append('历史解决失败')
    
    # 基于时间压力
    timeline = conflict.get('context', {}).get('timeline', '')
    if '尽快' in timeline or '立即' in timeline:
        blockers.append('时间压力过大')
    
    return blockers

def calculate_intervention_urgency(conflict: Dict) -> Dict:
    """计算干预紧急度"""
    urgency = 0.5  # 基础紧急度
    
    # 基于强度
    intensity = conflict.get('intensity', 0.5)
    urgency += intensity * 0.3
    
    # 基于影响
    impact = conflict.get('context', {}).get('impact', '')
    if impact == '高':
        urgency += 0.2
    
    # 基于时间
    timeline = conflict.get('context', {}).get('timeline', '')
    if '尽快' in timeline or '立即' in timeline:
        urgency += 0.2
    
    # 基于升级趋势
    escalation = analyze_escalation_history(conflict)
    if escalation['trend'] == '恶化':
        urgency += 0.15
    
    urgency = min(1.0, urgency)
    
    # 确定紧急级别
    if urgency > 0.8:
        level = '紧急'
    elif urgency > 0.6:
        level = '高'
    elif urgency > 0.4:
        level = '中'
    else:
        level = '低'
    
    return {
        'score': round(urgency, 3),
        'level': level,
        'recommendation': get_urgency_recommendation(level)
    }

def get_urgency_recommendation(level: str) -> str:
    """获取紧急度建议"""
    recommendations = {
        '紧急': '需要立即干预，建议召开紧急会议',
        '高': '本周内必须处理，建议指定协调人',
        '中': '两周内处理，建议安排专题讨论',
        '低': '可按计划处理，建议纳入常规议程'
    }
    return recommendations.get(level, '需要评估具体情况')

def main():
    parser = argparse.ArgumentParser(
        description='冲突动态分析工具',
        epilog='示例：python analyze_conflict_dynamics.py --input identified.json --output dynamics.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入已识别的冲突数据（JSON）')
    parser.add_argument('--output', '-o', default='conflict_dynamics.json', help='输出文件')
    
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
    conflicts = data.get('details', {}).get('conflicts', [])
    if not conflicts:
        print("错误：未找到冲突数据", file=sys.stderr)
        sys.exit(1)
    
    # 分析每个冲突
    analyzed_conflicts = []
    for conflict in conflicts:
        analyzed = conflict.copy()
        analyzed['resolution_difficulty'] = calculate_resolution_difficulty(conflict)
        analyzed['escalation_history'] = analyze_escalation_history(conflict)
        analyzed['timeline_prediction'] = predict_resolution_timeline(conflict)
        analyzed['resolution_blockers'] = identify_resolution_blockers(conflict)
        analyzed['intervention_urgency'] = calculate_intervention_urgency(conflict)
        analyzed_conflicts.append(analyzed)
    
    # 计算整体指标
    difficulties = [c['resolution_difficulty'] for c in analyzed_conflicts]
    urgencies = [c['intervention_urgency']['score'] for c in analyzed_conflicts]
    
    overall_metrics = {
        'avg_difficulty': round(np.mean(difficulties), 3) if difficulties else 0,
        'avg_urgency': round(np.mean(urgencies), 3) if urgencies else 0,
        'high_urgency_count': sum(1 for u in urgencies if u > 0.7),
        'complex_conflicts': sum(1 for d in difficulties if d > 0.7)
    }
    
    end_time = datetime.now()
    
    # 准备输出
    output = {
        'summary': {
            'n_analyzed': len(analyzed_conflicts),
            'avg_intensity': data.get('summary', {}).get('avg_intensity', 0),
            'avg_difficulty': overall_metrics['avg_difficulty'],
            'avg_urgency': overall_metrics['avg_urgency'],
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'analyzed_conflicts': analyzed_conflicts,
            'overall_metrics': overall_metrics
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
        
        print(f"✓ 冲突动态分析完成")
        print(f"  - 分析冲突数：{len(analyzed_conflicts)}")
        print(f"  - 平均解决难度：{overall_metrics['avg_difficulty']:.3f}")
        print(f"  - 平均紧急度：{overall_metrics['avg_urgency']:.3f}")
        print(f"  - 高紧急度冲突：{overall_metrics['high_urgency_count']}")
        print(f"  - 输出文件：{args.output}")
        
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()