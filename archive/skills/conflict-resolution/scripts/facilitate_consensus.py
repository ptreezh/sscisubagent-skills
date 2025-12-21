#!/usr/bin/env python
"""
共识促进工具
提供促进团队共识的详细计划
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

def assess_consensus_potential(strategy: Dict) -> float:
    """评估共识可能性"""
    base_potential = 0.6
    
    # 基于策略成功率
    success_rate = strategy.get('strategy', {}).get('success_rate', 0.5)
    base_potential += (success_rate - 0.5) * 0.4
    
    # 基于实施计划的完整性
    plan = strategy.get('implementation_plan', {})
    if plan.get('steps') and len(plan['steps']) >= 3:
        base_potential += 0.1
    
    # 基于资源可用性
    if plan.get('required_resources'):
        base_potential += 0.1
    
    return min(1.0, base_potential)

def design_facilitation_process(strategy: Dict) -> Dict:
    """设计促进过程"""
    process = {
        'preparation': {
            'goal': '会议准备',
            'activities': [
                '确定会议议程',
                '准备背景材料',
                '选择中立场地',
                '邀请所有相关方'
            ],
            'time_required': '1-2天',
            'responsible': '项目协调员'
        },
        'opening': {
            'goal': '建立对话基础',
            'activities': [
                '欢迎与介绍',
                '设定会议规则',
                '明确讨论目标',
                '建立信任氛围'
            ],
            'time_required': '15-30分钟',
            'responsible': '主持人'
        },
        'exploration': {
            'goal': '深入了解各方观点',
            'activities': [
                '各方陈述立场',
                '倾听与理解',
                '识别共同利益',
                '澄清误解'
            ],
            'time_required': '60-90分钟',
            'responsible': '全体参与者'
        },
        'negotiation': {
            'goal': '寻找解决方案',
            'activities': [
                '头脑风暴方案',
                '评估可行性',
                '寻找折中点',
                '初步达成一致'
            ],
            'time_required': '90-120分钟',
            'responsible': '全体参与者'
        },
        'closure': {
            'goal': '巩固共识',
            'activities': [
                '总结协议要点',
                '明确下一步行动',
                '设定跟进机制',
                '表达感谢'
            ],
            'time_required': '30分钟',
            'responsible': '主持人'
        }
    }
    
    return process

def identify_facilitation_roles(teams: List[Dict]) -> Dict:
    """识别促进角色"""
    roles = {
        'facilitator': {
            'description': '中立主持人',
            'required_skills': ['沟通能力', '冲突管理', '中立性'],
            'candidates': []
        },
        'mediator': {
            'description': '外部调解员',
            'required_skills': ['专业知识', '权威性', '公正性'],
            'candidates': []
        },
        'recorder': {
            'description': '记录员',
            'required_skills': ['细致', '客观', '快速记录'],
            'candidates': []
        },
        'timekeeper': {
            'description': '时间管理员',
            'required_skills': ['时间管理', '坚持原则'],
            'candidates': []
        }
    }
    
    # 基于团队成员特征推荐角色
    for member in teams:
        name = member.get('name', '')
        role = member.get('role', '')
        style = member.get('communication_style', '')
        history = member.get('conflict_history', 0)
        
        # 项目负责人适合做协调
        if '项目负责人' in role and style == '理性' and history <= 2:
            roles['facilitator']['candidates'].append(name)
        
        # 沟通风格温和的适合记录
        if style == '温和':
            roles['recorder']['candidates'].append(name)
        
        # 冲突历史少的适合促进
        if history == 0:
            roles['mediator']['candidates'].append(name)
    
    return roles

def create_communication_plan(conflict: Dict) -> Dict:
    """创建沟通计划"""
    plan = {
        'before_meeting': {
            'purpose': '会前沟通',
            'activities': [
                '发送会议通知',
                '分享背景材料',
                '个别沟通了解立场',
                '确认参会时间'
            ],
            'channels': ['邮件', '电话', '面对面'],
            'frequency': '一次性'
        },
        'during_meeting': {
            'purpose': '会议中沟通',
            'activities': [
                '结构化发言',
                '积极倾听',
                '建设性反馈',
                '记录要点'
            ],
            'channels': ['面对面', '视频会议'],
            'frequency': '持续'
        },
        'after_meeting': {
            'purpose': '会后跟进',
            'activities': [
                '发送会议纪要',
                '确认行动项',
                '定期进度更新',
                '问题及时沟通'
            ],
            'channels': ['邮件', '项目管理工具'],
            'frequency': '每周'
        }
    }
    
    # 根据冲突类型调整
    conflict_type = conflict.get('classified_type', '')
    if conflict_type == '理论分歧':
        plan['before_meeting']['activities'].append('分享相关文献')
        plan['during_meeting']['activities'].append('专家观点分享')
    elif conflict_type == '资源分配':
        plan['before_meeting']['activities'].append('收集资源需求详情')
        plan['during_meeting']['activities'].append('资源使用展示')
    
    return plan

def generate_monitoring_mechanism(strategy: Dict) -> Dict:
    """生成监控机制"""
    monitoring = {
        'progress_tracking': {
            'method': '定期检查',
            'frequency': '每周',
            'indicators': [
                '协议执行情况',
                '各方满意度',
                '新问题出现',
                '整体进展'
            ],
            'responsible': '项目协调员'
        },
        'feedback_collection': {
            'method': '匿名反馈',
            'frequency': '每两周',
            'channels': ['在线表单', '意见箱'],
            'analysis': '月度汇总分析'
        },
        'escalation_process': {
            'trigger_conditions': [
                '协议无法执行',
                '新的冲突出现',
                '满意度低于60%'
            ],
            'steps': [
                '紧急会议',
                '外部调解',
                '方案调整'
            ],
            'timeline': '48小时内响应'
        }
    }
    
    return monitoring

def calculate_success_probability(strategy: Dict, process: Dict) -> Dict:
    """计算成功概率"""
    # 基础概率
    base_prob = strategy.get('strategy', {}).get('success_rate', 0.5)
    
    # 调整因素
    adjustments = {
        'process_completeness': 0.1 if len(process) >= 5 else 0,
        'resource_availability': 0.05,
        'stakeholder_commitment': 0.1,
        'time_adequacy': 0.05
    }
    
    # 计算最终概率
    final_prob = base_prob + sum(adjustments.values())
    final_prob = min(1.0, final_prob)
    
    # 确定置信度
    if final_prob > 0.8:
        confidence = '高'
        recommendation = '强烈推荐执行'
    elif final_prob > 0.6:
        confidence = '中'
        recommendation = '建议执行，需密切关注'
    else:
        confidence = '低'
        recommendation = '需要调整策略或寻求外部帮助'
    
    return {
        'probability': round(final_prob, 3),
        'confidence': confidence,
        'recommendation': recommendation,
        'key_factors': list(adjustments.keys())
    }

def main():
    parser = argparse.ArgumentParser(
        description='共识促进工具',
        epilog='示例：python facilitate_consensus.py --input strategies.json --output consensus.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入解决策略数据（JSON）')
    parser.add_argument('--output', '-o', default='consensus_plan.json', help='输出文件')
    
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
    strategies = data.get('details', {}).get('resolution_strategies', [])
    if not strategies:
        print("错误：未找到解决策略数据", file=sys.stderr)
        sys.exit(1)
    
    # 读取团队信息（如果有的话）
    teams = []
    # 这里简化处理，实际应该从原始数据读取
    
    # 为每个策略生成共识促进计划
    consensus_plans = []
    consensus_likelihoods = []
    
    for strategy in strategies:
        # 评估共识可能性
        consensus_likelihood = assess_consensus_potential(strategy)
        consensus_likelihoods.append(consensus_likelihood)
        
        # 设计促进过程
        facilitation_process = design_facilitation_process(strategy)
        
        # 识别促进角色
        facilitation_roles = identify_facilitation_roles(teams)
        
        # 创建沟通计划
        communication_plan = create_communication_plan(strategy)
        
        # 生成监控机制
        monitoring_mechanism = generate_monitoring_mechanism(strategy)
        
        # 计算成功概率
        success_analysis = calculate_success_probability(strategy, facilitation_process)
        
        # 组装计划
        consensus_plan = {
            'conflict_id': strategy.get('conflict_id', ''),
            'consensus_likelihood': round(consensus_likelihood, 3),
            'facilitation_process': facilitation_process,
            'facilitation_roles': facilitation_roles,
            'communication_plan': communication_plan,
            'monitoring_mechanism': monitoring_mechanism,
            'success_analysis': success_analysis
        }
        
        consensus_plans.append(consensus_plan)
    
    end_time = datetime.now()
    
    # 计算整体指标
    avg_likelihood = sum(consensus_likelihoods) / len(consensus_likelihoods) if consensus_likelihoods else 0
    n_steps = sum(len(plan['facilitation_process']) for plan in consensus_plans)
    
    # 准备输出
    output = {
        'summary': {
            'n_plans': len(consensus_plans),
            'consensus_likelihood': round(avg_likelihood, 3),
            'n_steps': n_steps,
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'consensus_plans': consensus_plans
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
        
        print(f"✓ 共识促进计划生成完成")
        print(f"  - 生成计划数：{len(consensus_plans)}")
        print(f"  - 平均共识可能性：{avg_likelihood:.3f}")
        print(f"  - 总步骤数：{n_steps}")
        print(f"  - 输出文件：{args.output}")
        
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()