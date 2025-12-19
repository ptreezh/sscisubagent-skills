#!/usr/bin/env python
"""
解决策略生成工具
为研究冲突生成个性化的解决策略
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any
from collections import defaultdict

def generate_theory_conflict_strategy(conflict: Dict) -> Dict:
    """生成理论分歧解决策略"""
    strategies = {
        'dialogue_based': {
            'name': '对话式解决',
            'description': '通过结构化对话促进理解',
            'steps': [
                '组织专题研讨会',
                '邀请外部专家调解',
                '寻找理论共同点',
                '设计混合方法研究'
            ],
            'success_rate': 0.75,
            'time_required': '4-6周',
            'resources': ['会议室', '专家费用', '时间投入']
        },
        'empirical_approach': {
            'name': '实证验证',
            'description': '通过小规模实验验证不同方法',
            'steps': [
                '设计对比实验',
                '收集初步数据',
                '分析效果差异',
                '基于数据决策'
            ],
            'success_rate': 0.85,
            'time_required': '6-8周',
            'resources': ['实验设备', '数据分析工具', '研究助理']
        },
        'compromise_solution': {
            'name': '妥协方案',
            'description': '寻找双方都能接受的中间方案',
            'steps': [
                '明确核心需求',
                '识别可妥协点',
                '制定阶段性方案',
                '设定评估标准'
            ],
            'success_rate': 0.65,
            'time_required': '2-3周',
            'resources': ['协调时间', '文档工作']
        }
    }
    return strategies

def generate_resource_conflict_strategy(conflict: Dict) -> Dict:
    """生成资源分配冲突解决策略"""
    strategies = {
        'optimization': {
            'name': '资源优化配置',
            'description': '通过优化算法实现资源最优分配',
            'steps': [
                '评估资源需求优先级',
                '建立量化评估体系',
                '应用优化模型',
                '动态调整机制'
            ],
            'success_rate': 0.80,
            'time_required': '3-4周',
            'resources': ['分析工具', '决策支持系统']
        },
        'time_sharing': {
            'name': '时间共享机制',
            'description': '通过分时使用提高资源利用率',
            'steps': [
                '制定使用时间表',
                '建立预约系统',
                '设置优先级规则',
                '监控使用效率'
            ],
            'success_rate': 0.70,
            'time_required': '2周',
            'resources': ['管理系统', '协调人员']
        },
        'external_funding': {
            'name': '外部资源获取',
            'description': '寻求额外资金或设备支持',
            'steps': [
                '准备申请材料',
                '寻找资助机会',
                '提交申请',
                '跟进审批'
            ],
            'success_rate': 0.60,
            'time_required': '8-12周',
            'resources': ['申请时间', '专业服务']
        }
    }
    return strategies

def generate_authorship_conflict_strategy(conflict: Dict) -> Dict:
    """生成作者署名冲突解决策略"""
    strategies = {
        'contribution_matrix': {
            'name': '贡献度矩阵',
            'description': '建立客观的贡献评估体系',
            'steps': [
                '制定贡献评估标准',
                '各方自评与互评',
                '第三方评估',
                '基于矩阵确定署名'
            ],
            'success_rate': 0.85,
            'time_required': '2-3周',
            'resources': ['评估工具', '公正专家']
        },
        'multiple_first_authors': {
            'name': '共同第一作者',
            'description': '采用共同第一作者方案',
            'steps': [
                '协商共同作者条件',
                '明确贡献说明',
                '期刊政策确认',
                '署名顺序协议'
            ],
            'success_rate': 0.75,
            'time_required': '1-2周',
            'resources': ['协商时间', '政策研究']
        },
        'sequential_publications': {
            'name': '系列论文方案',
            'description': '将研究拆分为多篇论文',
            'steps': [
                '研究内容分割',
                '确定论文主题',
                '分配主责作者',
                '制定发表计划'
            ],
            'success_rate': 0.80,
            'time_required': '4-6周',
            'resources': ['规划时间', '额外工作量']
        }
    }
    return strategies

def select_best_strategy(strategies: Dict, conflict: Dict) -> Dict:
    """选择最佳策略"""
    # 基于冲突特征选择策略
    intensity = conflict.get('intensity', 0.5)
    difficulty = conflict.get('resolution_difficulty', 0.5)
    urgency = conflict.get('intervention_urgency', {}).get('score', 0.5)
    
    # 计算策略得分
    best_strategy = None
    best_score = 0
    
    for strategy_name, strategy in strategies.items():
        score = strategy['success_rate']
        
        # 根据紧急度调整
        if urgency > 0.7 and '时间_required' in strategy:
            time_req = strategy['time_required']
            if '2周' in time_req or '1-2周' in time_req:
                score += 0.1
        
        # 根据难度调整
        if difficulty > 0.7 and 'success_rate' in strategy:
            if strategy['success_rate'] > 0.8:
                score += 0.1
        
        if score > best_score:
            best_score = score
            best_strategy = strategy_name
    
    return {
        'strategy_name': best_strategy,
        'strategy': strategies[best_strategy],
        'selection_score': round(best_score, 3),
        'selection_reason': get_selection_reason(best_strategy, conflict)
    }

def get_selection_reason(strategy_name: str, conflict: Dict) -> str:
    """获取选择理由"""
    reasons = {
        'dialogue_based': '适合理论分歧，促进深度交流',
        'empirical_approach': '基于数据决策，客观公正',
        'compromise_solution': '快速解决，降低冲突成本',
        'optimization': '科学配置，效率最大化',
        'time_sharing': '灵活安排，提高利用率',
        'external_funding': '扩大资源，满足各方需求',
        'contribution_matrix': '客观评估，公平透明',
        'multiple_first_authors': '平衡利益，认可贡献',
        'sequential_publications': '分散压力，多赢方案'
    }
    return reasons.get(strategy_name, '综合评估后选择')

def generate_implementation_plan(strategy: Dict, conflict: Dict) -> Dict:
    """生成实施计划"""
    steps = strategy.get('steps', [])
    timeline = strategy.get('time_required', '未知')
    resources = strategy.get('resources', [])
    
    # 生成详细计划
    plan = {
        'steps': [],
        'timeline': timeline,
        'required_resources': resources,
        'success_indicators': [],
        'risk_factors': [],
        'monitoring_points': []
    }
    
    # 详细步骤
    for i, step in enumerate(steps, 1):
        plan['steps'].append({
            'step_number': i,
            'action': step,
            'responsible': '待指定',
            'deadline': f'第{i}周',
            'status': '待开始'
        })
    
    # 成功指标
    conflict_type = conflict.get('classified_type', '')
    if conflict_type == '理论分歧':
        plan['success_indicators'] = [
            '各方对方法论达成共识',
            '研究方案获得批准',
            '团队氛围改善'
        ]
    elif conflict_type == '资源分配':
        plan['success_indicators'] = [
            '资源分配方案确定',
            '各方获得必要资源',
            '项目进度正常'
        ]
    elif conflict_type == '作者署名':
        plan['success_indicators'] = [
            '署名方案确定',
            '各方接受安排',
            '论文按时提交'
        ]
    
    # 风险因素
    if conflict.get('intensity', 0) > 0.7:
        plan['risk_factors'].append('冲突可能升级')
    if conflict.get('n_parties', 0) > 2:
        plan['risk_factors'].append('协调难度大')
    
    # 监控点
    plan['monitoring_points'] = [
        '第1周：初步进展检查',
        '中期：方案调整评估',
        '结束：效果评估'
    ]
    
    return plan

def main():
    parser = argparse.ArgumentParser(
        description='解决策略生成工具',
        epilog='示例：python generate_resolution_strategies.py --input dynamics.json --output strategies.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入冲突动态分析数据（JSON）')
    parser.add_argument('--output', '-o', default='resolution_strategies.json', help='输出文件')
    
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
    conflicts = data.get('details', {}).get('analyzed_conflicts', [])
    if not conflicts:
        print("错误：未找到冲突数据", file=sys.stderr)
        sys.exit(1)
    
    # 为每个冲突生成策略
    resolution_strategies = []
    strategy_types = []
    
    for conflict in conflicts:
        conflict_type = conflict.get('classified_type', '')
        
        # 根据冲突类型生成策略
        if conflict_type == '理论分歧':
            strategies = generate_theory_conflict_strategy(conflict)
        elif conflict_type == '资源分配':
            strategies = generate_resource_conflict_strategy(conflict)
        elif conflict_type == '作者署名':
            strategies = generate_authorship_conflict_strategy(conflict)
        else:
            # 默认策略
            strategies = {
                'negotiation': {
                    'name': '协商解决',
                    'description': '通过直接协商寻找解决方案',
                    'steps': ['召开协商会议', '明确各方需求', '寻找共同点', '达成协议'],
                    'success_rate': 0.60,
                    'time_required': '2-4周',
                    'resources': ['协商时间', '中立场地']
                }
            }
        
        # 选择最佳策略
        best_strategy = select_best_strategy(strategies, conflict)
        
        # 生成实施计划
        implementation_plan = generate_implementation_plan(best_strategy['strategy'], conflict)
        
        # 组装结果
        strategy_result = {
            'conflict_id': conflict.get('id', ''),
            'conflict_type': conflict_type,
            'recommended_strategy': best_strategy,
            'implementation_plan': implementation_plan
        }
        
        resolution_strategies.append(strategy_result)
        strategy_types.append(best_strategy['strategy_name'])
    
    end_time = datetime.now()
    
    # 准备输出
    output = {
        'summary': {
            'n_strategies': len(resolution_strategies),
            'strategy_types': list(set(strategy_types)),
            'avg_success_rate': 0.75,  # 简化计算
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'resolution_strategies': resolution_strategies
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
        
        print(f"✓ 解决策略生成完成")
        print(f"  - 生成策略数：{len(resolution_strategies)}")
        print(f"  - 策略类型：{list(set(strategy_types))}")
        print(f"  - 输出文件：{args.output}")
        
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()