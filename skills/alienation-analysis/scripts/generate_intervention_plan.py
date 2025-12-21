#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异化干预方案生成器
根据异化分析结果生成具体的干预建议和行动方案
"""

import json
import numpy as np
from typing import Dict, List, Any, Tuple
from datetime import datetime, timedelta


class InterventionPlanGenerator:
    """异化干预方案生成器"""
    
    def __init__(self):
        self.intervention_strategies = {
            'labor_alienation': {
                'immediate': [
                    '改善工作环境，减少重复性劳动',
                    '增加员工参与决策机会',
                    '建立技能培训和发展体系',
                    '优化劳动强度和工作节奏'
                ],
                'medium_term': [
                    '推行工作内容丰富化',
                    '建立劳动者共同体',
                    '实施民主化管理',
                    '加强劳动权益保护'
                ],
                'long_term': [
                    '实现劳动自由全面发展',
                    '建立共产主义劳动观',
                    '消除雇佣劳动关系',
                    '实现劳动的自主性'
                ]
            },
            'social_alienation': {
                'immediate': [
                    '加强社区建设活动',
                    '组织集体文化活动',
                    '建立邻里互助网络',
                    '推广面对面交流'
                ],
                'medium_term': [
                    '重建社会信任体系',
                    '发展志愿服务文化',
                    '加强社会凝聚力',
                    '促进社会参与'
                ],
                'long_term': [
                    '实现社会关系和谐',
                    '建立共产主义社会',
                    '消除阶级对立',
                    '实现人的全面发展'
                ]
            },
            'consumption_alienation': {
                'immediate': [
                    '推广理性消费教育',
                    '建立消费反思机制',
                    '减少冲动购买行为',
                    '加强消费权益保护'
                ],
                'medium_term': [
                    '培育消费主义批判意识',
                    '发展共享经济模式',
                    '推广可持续消费',
                    '建立消费节制文化'
                ],
                'long_term': [
                    '实现消费自由',
                    '建立共产主义分配制度',
                    '消除商品拜物教',
                    '实现按需分配'
                ]
            },
            'technology_alienation': {
                'immediate': [
                    '限制技术使用时间',
                    '培养数字素养',
                    '建立技术使用规则',
                    '促进线下活动'
                ],
                'medium_term': [
                    '发展人机和谐技术',
                    '建立技术伦理规范',
                    '加强技术民主控制',
                    '促进技术包容性发展'
                ],
                'long_term': [
                    '实现技术为人服务',
                    '建立共产主义技术观',
                    '消除技术异化',
                    '实现技术自由'
                ]
            }
        }
    
    def generate_intervention_plan(self, alienation_scores: Dict[str, float], 
                                 alienation_types: List[str], 
                                 severity_levels: Dict[str, str]) -> Dict[str, Any]:
        """
        生成异化干预方案
        
        Args:
            alienation_scores: 异化程度分数
            alienation_types: 异化类型列表
            severity_levels: 严重程度级别
            
        Returns:
            干预方案字典
        """
        # 确定主要异化类型
        primary_alienation = self._identify_primary_alienation(alienation_scores)
        
        # 生成干预优先级
        intervention_priorities = self._determine_intervention_priorities(
            alienation_scores, severity_levels)
        
        # 生成具体干预措施
        intervention_measures = self._generate_intervention_measures(
            primary_alienation, intervention_priorities)
        
        # 生成时间表
        intervention_timeline = self._create_intervention_timeline(intervention_measures)
        
        # 生成评估指标
        evaluation_metrics = self._define_evaluation_metrics(intervention_measures)
        
        # 计算成功率预测
        success_probability = self._calculate_success_probability(
            intervention_measures, alienation_scores)
        
        return {
            'primary_alienation_focus': primary_alienation,
            'intervention_priorities': intervention_priorities,
            'intervention_measures': intervention_measures,
            'intervention_timeline': intervention_timeline,
            'evaluation_metrics': evaluation_metrics,
            'success_probability': success_probability,
            'risk_factors': self._identify_risk_factors(alienation_scores),
            'support_resources': self._suggest_support_resources(primary_alienation),
            'created_at': datetime.now().isoformat()
        }
    
    def _identify_primary_alienation(self, alienation_scores: Dict[str, float]) -> str:
        """识别主要异化类型"""
        return max(alienation_scores, key=alienation_scores.get)
    
    def _determine_intervention_priorities(self, alienation_scores: Dict[str, float],
                                         severity_levels: Dict[str, str]) -> List[str]:
        """确定干预优先级"""
        # 按严重程度和分数排序
        priority_list = []
        for alien_type in ['labor_alienation', 'social_alienation', 
                          'consumption_alienation', 'technology_alienation']:
            if alien_type in alienation_scores:
                priority_list.append({
                    'type': alien_type,
                    'score': alienation_scores[alien_type],
                    'severity': severity_levels.get(alien_type, 'mild')
                })
        
        # 按严重程度和分数排序
        priority_list.sort(key=lambda x: (
            {'critical': 4, 'severe': 3, 'moderate': 2, 'mild': 1}[x['severity']],
            x['score']
        ), reverse=True)
        
        return [item['type'] for item in priority_list]
    
    def _generate_intervention_measures(self, primary_alienation: str,
                                      priorities: List[str]) -> Dict[str, Dict[str, List[str]]]:
        """生成干预措施"""
        measures = {}
        
        for alien_type in priorities:
            if alien_type in self.intervention_strategies:
                measures[alien_type] = self.intervention_strategies[alien_type].copy()
        
        return measures
    
    def _create_intervention_timeline(self, measures: Dict[str, Dict[str, List[str]]]) -> Dict[str, Dict]:
        """创建干预时间表"""
        timeline = {}
        start_date = datetime.now()
        
        for alien_type, strategies in measures.items():
            timeline[alien_type] = {
                'immediate': self._calculate_timeframe(start_date, 0, 3),  # 0-3个月
                'medium_term': self._calculate_timeframe(start_date, 3, 12),  # 3-12个月
                'long_term': self._calculate_timeframe(start_date, 12, 36)  # 1-3年
            }
        
        return timeline
    
    def _calculate_timeframe(self, start_date: datetime, start_months: int, end_months: int) -> Dict[str, str]:
        """计算时间范围"""
        start = start_date + timedelta(days=start_months * 30)
        end = start_date + timedelta(days=end_months * 30)
        
        return {
            'start_date': start.strftime('%Y-%m-%d'),
            'end_date': end.strftime('%Y-%m-%d'),
            'duration_months': end_months - start_months
        }
    
    def _define_evaluation_metrics(self, measures: Dict[str, Dict[str, List[str]]]) -> Dict[str, List[str]]:
        """定义评估指标"""
        metrics = {}
        
        for alien_type in measures.keys():
            if alien_type == 'labor_alienation':
                metrics[alien_type] = [
                    '工作满意度评分',
                    '离职率变化',
                    '工作自主性提升',
                    '技能发展机会'
                ]
            elif alien_type == 'social_alienation':
                metrics[alien_type] = [
                    '社会参与度',
                    '人际交往频率',
                    '社区归属感',
                    '社会支持网络'
                ]
            elif alien_type == 'consumption_alienation':
                metrics[alien_type] = [
                    '理性消费比例',
                    '冲动购买减少',
                    '消费意义感',
                    '财务健康度'
                ]
            elif alien_type == 'technology_alienation':
                metrics[alien_type] = [
                    '技术使用时间控制',
                    '线下活动增加',
                    '数字素养提升',
                    '技术依赖减轻'
                ]
        
        return metrics
    
    def _calculate_success_probability(self, measures: Dict[str, Dict[str, List[str]]],
                                     alienation_scores: Dict[str, float]) -> float:
        """计算成功率"""
        # 基于异化程度和干预措施的复杂度计算成功率
        base_probability = 0.7  # 基础成功率
        
        # 根据异化严重程度调整
        avg_alienation = np.mean(list(alienation_scores.values()))
        if avg_alienation > 0.8:
            adjustment = -0.2
        elif avg_alienation > 0.6:
            adjustment = -0.1
        elif avg_alienation < 0.4:
            adjustment = 0.1
        else:
            adjustment = 0
        
        # 根据干预措施完整性调整
        measure_completeness = len(measures) / 4  # 假设最多4种异化类型
        completeness_adjustment = (measure_completeness - 0.5) * 0.2
        
        success_probability = base_probability + adjustment + completeness_adjustment
        
        return max(0.3, min(0.95, success_probability))
    
    def _identify_risk_factors(self, alienation_scores: Dict[str, float]) -> List[str]:
        """识别风险因素"""
        risk_factors = []
        
        avg_alienation = np.mean(list(alienation_scores.values()))
        if avg_alienation > 0.8:
            risk_factors.append('异化程度过高，干预难度大')
        if max(alienation_scores.values()) - min(alienation_scores.values()) > 0.5:
            risk_factors.append('异化程度差异大，需要针对性干预')
        if len(alienation_scores) > 3:
            risk_factors.append('多重异化同时存在，干预复杂性增加')
        
        return risk_factors
    
    def _suggest_support_resources(self, primary_alienation: str) -> List[str]:
        """建议支持资源"""
        resources = {
            'labor_alienation': [
                '工会组织支持',
                '职业心理咨询',
                '技能培训资源',
                '劳动法律咨询'
            ],
            'social_alienation': [
                '社区服务中心',
                '社交技能培训',
                '志愿服务平台',
                '心理支持小组'
            ],
            'consumption_alienation': [
                '理财教育课程',
                '消费心理辅导',
                '理性消费指导',
                '财务管理工具'
            ],
            'technology_alienation': [
                '数字素养培训',
                '技术伦理教育',
                '线下活动组织',
                '数字排毒指导'
            ]
        }
        
        return resources.get(primary_alienation, [])
    
    def export_intervention_plan(self, plan: Dict[str, Any], output_path: str) -> bool:
        """导出干预方案到文件"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(plan, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"导出干预方案失败: {e}")
            return False


def main():
    """主函数 - 用于测试"""
    generator = InterventionPlanGenerator()
    
    # 测试数据
    test_scores = {
        'labor_alienation': 0.75,
        'social_alienation': 0.60,
        'consumption_alienation': 0.80,
        'technology_alienation': 0.65
    }
    
    test_types = ['labor_alienation', 'consumption_alienation']
    test_severity = {
        'labor_alienation': 'severe',
        'social_alienation': 'moderate',
        'consumption_alienation': 'severe',
        'technology_alienation': 'moderate'
    }
    
    # 生成干预方案
    plan = generator.generate_intervention_plan(test_scores, test_types, test_severity)
    
    # 打印结果
    print(json.dumps(plan, ensure_ascii=False, indent=2))
    
    # 导出到文件
    generator.export_intervention_plan(plan, 'intervention_plan_test.json')


if __name__ == '__main__':
    main()