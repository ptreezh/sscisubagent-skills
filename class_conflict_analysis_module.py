#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶级矛盾分析模块
Class Conflict Analysis Module

专门用于分析阶级利益冲突、矛盾发展阶段和斗争形式的专业模块
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
import math
from datetime import datetime, timedelta

class ConflictType(Enum):
    """矛盾类型枚举"""
    ECONOMIC_CONFLICT = "经济矛盾"  # 经济矛盾
    POLITICAL_CONFLICT = "政治矛盾"  # 政治矛盾
    IDEOLOGICAL_CONFLICT = "意识形态矛盾"  # 意识形态矛盾
    CULTURAL_CONFLICT = "文化矛盾"  # 文化矛盾
    SOCIAL_CONFLICT = "社会矛盾"  # 社会矛盾

class StruggleForm(Enum):
    """斗争形式枚举"""
    ECONOMIC_STRUGGLE = "经济斗争"  # 经济斗争
    POLITICAL_STRUGGLE = "政治斗争"  # 政治斗争
    IDEOLOGICAL_STRUGGLE = "思想斗争"  # 思想斗争
    LEGAL_STRUGGLE = "法律斗争"  # 法律斗争
    VIOLENT_STRUGGLE = "暴力斗争"  # 暴力斗争

class ConflictStage(Enum):
    """矛盾发展阶段枚举"""
    LATENT_STAGE = "潜伏阶段"  # 潜伏阶段
    EMERGING_STAGE = "显现阶段"  # 显现阶段
    DEVELOPING_STAGE = "发展阶段"  # 发展阶段
    ACUTE_STAGE = "激化阶段"  # 激化阶段
    RESOLUTION_STAGE = "解决阶段"  # 解决阶段

@dataclass
class InterestConflict:
    """利益冲突数据结构"""
    conflict_type: ConflictType
    intensity: float  # 冲突强度 (0-1)
    scope: float  # 影响范围 (0-1)
    duration: float  # 持续时间 (年)
    participants_involved: int  # 参与人数
    economic_damage: float  # 经济损失
    
    def conflict_weight(self) -> float:
        """计算冲突权重"""
        return (self.intensity * 0.4 + 
                self.scope * 0.3 + 
                self.duration * 0.2 + 
                self.participants_involved / 1000000 * 0.1)

@dataclass
class StruggleEvent:
    """斗争事件数据结构"""
    form: StruggleForm
    scale: float  # 规模 (0-1)
    success_rate: float  # 成功率 (0-1)
    casualties: int  # 伤亡人数
    economic_impact: float  # 经济影响
    political_impact: float  # 政治影响
    
    def struggle_effectiveness(self) -> float:
        """计算斗争有效性"""
        return self.scale * 0.3 + self.success_rate * 0.4 + \
               (1 - self.casualties / 10000) * 0.3

class ClassConflictAnalyzer:
    """阶级矛盾分析器"""
    
    def __init__(self):
        self.conflict_thresholds = {
            'low_intensity': 0.3,
            'medium_intensity': 0.6,
            'high_intensity': 0.8,
            'critical_intensity': 0.9
        }
        
        self.struggle_form_weights = {
            StruggleForm.ECONOMIC_STRUGGLE: 0.2,
            StruggleForm.POLITICAL_STRUGGLE: 0.3,
            StruggleForm.IDEOLOGICAL_STRUGGLE: 0.15,
            StruggleForm.LEGAL_STRUGGLE: 0.1,
            StruggleForm.VIOLENT_STRUGGLE: 0.25
        }
    
    def quantify_class_interests(self, 
                               class_data: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        量化阶级利益
        
        Args:
            class_data: 各阶级数据
            
        Returns:
            量化后的阶级利益数据
        """
        quantified_interests = {}
        
        for class_name, data in class_data.items():
            # 经济利益
            economic_interests = {
                'income_preservation': data.get('income_stability', 0.5),
                'property_rights': data.get('property_security', 0.5),
                'economic_growth': data.get('growth_expectation', 0.5),
                'redistribution_preference': data.get('redistribution_support', 0.5)
            }
            
            # 政治利益
            political_interests = {
                'political_power': data.get('political_influence', 0.5),
                'policy_influence': data.get('policy_impact', 0.5),
                'representation': data.get('representation_level', 0.5),
                'legal_protection': data.get('legal_security', 0.5)
            }
            
            # 社会利益
            social_interests = {
                'social_status': data.get('social_prestige', 0.5),
                'education_access': data.get('education_opportunity', 0.5),
                'healthcare_access': data.get('healthcare_access', 0.5),
                'social_mobility': data.get('mobility_opportunity', 0.5)
            }
            
            quantified_interests[class_name] = {
                'economic': economic_interests,
                'political': political_interests,
                'social': social_interests,
                'total_interest_score': np.mean([
                    *economic_interests.values(),
                    *political_interests.values(),
                    *social_interests.values()
                ])
            }
        
        return quantified_interests
    
    def calculate_interest_conflict_matrix(self, 
                                         interests_data: Dict) -> np.ndarray:
        """
        计算利益冲突矩阵
        
        Args:
            interests_data: 量化利益数据
            
        Returns:
            冲突矩阵
        """
        classes = list(interests_data.keys())
        n_classes = len(classes)
        conflict_matrix = np.zeros((n_classes, n_classes))
        
        for i, class_i in enumerate(classes):
            for j, class_j in enumerate(classes):
                if i != j:
                    # 计算两个阶级在各维度上的利益差异
                    economic_diff = self._calculate_interest_difference(
                        interests_data[class_i]['economic'],
                        interests_data[class_j]['economic']
                    )
                    political_diff = self._calculate_interest_difference(
                        interests_data[class_i]['political'],
                        interests_data[class_j]['political']
                    )
                    social_diff = self._calculate_interest_difference(
                        interests_data[class_i]['social'],
                        interests_data[class_j]['social']
                    )
                    
                    # 综合冲突强度
                    total_conflict = (economic_diff * 0.4 + 
                                    political_diff * 0.4 + 
                                    social_diff * 0.2)
                    
                    conflict_matrix[i][j] = total_conflict
        
        return conflict_matrix
    
    def _calculate_interest_difference(self, 
                                     interests_i: Dict, 
                                     interests_j: Dict) -> float:
        """计算利益差异度"""
        differences = []
        for key in interests_i.keys():
            diff = abs(interests_i[key] - interests_j[key])
            differences.append(diff)
        return np.mean(differences)
    
    def identify_conflict_hotspots(self, 
                                 conflict_matrix: np.ndarray,
                                 class_names: List[str]) -> List[Dict]:
        """
        识别冲突热点
        
        Args:
            conflict_matrix: 冲突矩阵
            class_names: 阶级名称列表
            
        Returns:
            冲突热点列表
        """
        hotspots = []
        threshold = self.conflict_thresholds['medium_intensity']
        
        for i in range(len(class_names)):
            for j in range(len(class_names)):
                if i != j and conflict_matrix[i][j] > threshold:
                    hotspots.append({
                        'class_a': class_names[i],
                        'class_b': class_names[j],
                        'conflict_intensity': conflict_matrix[i][j],
                        'conflict_level': self._classify_conflict_level(conflict_matrix[i][j])
                    })
        
        # 按冲突强度排序
        hotspots.sort(key=lambda x: x['conflict_intensity'], reverse=True)
        return hotspots
    
    def _classify_conflict_level(self, intensity: float) -> str:
        """分类冲突等级"""
        if intensity >= self.conflict_thresholds['critical_intensity']:
            return "极高强度"
        elif intensity >= self.conflict_thresholds['high_intensity']:
            return "高强度"
        elif intensity >= self.conflict_thresholds['medium_intensity']:
            return "中等强度"
        else:
            return "低强度"
    
    def analyze_struggle_forms(self, 
                             conflict_hotspots: List[Dict],
                             historical_events: List[Dict]) -> Dict:
        """
        分析斗争形式
        
        Args:
            conflict_hotspots: 冲突热点
            historical_events: 历史事件
            
        Returns:
            斗争形式分析结果
        """
        struggle_analysis = {
            'dominant_forms': {},
            'form_effectiveness': {},
            'evolution_trends': {},
            'future_predictions': {}
        }
        
        # 统计各斗争形式的使用频率
        form_counts = {form: 0 for form in StruggleForm}
        form_success = {form: [] for form in StruggleForm}
        
        for event in historical_events:
            form = StruggleForm(event.get('form', 'ECONOMIC_STRUGGLE'))
            form_counts[form] += 1
            form_success[form].append(event.get('success_rate', 0.5))
        
        # 计算主导形式
        total_events = sum(form_counts.values())
        for form, count in form_counts.items():
            if total_events > 0:
                struggle_analysis['dominant_forms'][form.value] = count / total_events
                if form_success[form]:
                    struggle_analysis['form_effectiveness'][form.value] = np.mean(form_success[form])
        
        # 分析演化趋势
        if len(historical_events) >= 5:
            struggle_analysis['evolution_trends'] = self._analyze_form_evolution(historical_events)
        
        # 预测未来趋势
        struggle_analysis['future_predictions'] = self._predict_form_trends(
            struggle_analysis['dominant_forms'],
            struggle_analysis['evolution_trends']
        )
        
        return struggle_analysis
    
    def _analyze_form_evolution(self, events: List[Dict]) -> Dict:
        """分析斗争形式演化"""
        # 按时间排序
        sorted_events = sorted(events, key=lambda x: x.get('date', ''))
        
        # 分时期统计
        periods = len(sorted_events) // 3
        form_evolution = {form.value: [] for form in StruggleForm}
        
        for i in range(3):
            start_idx = i * periods
            end_idx = (i + 1) * periods if i < 2 else len(sorted_events)
            period_events = sorted_events[start_idx:end_idx]
            
            period_counts = {form: 0 for form in StruggleForm}
            for event in period_events:
                form = StruggleForm(event.get('form', 'ECONOMIC_STRUGGLE'))
                period_counts[form] += 1
            
            total_period = sum(period_counts.values())
            for form, count in period_counts.items():
                if total_period > 0:
                    form_evolution[form.value].append(count / total_period)
        
        return form_evolution
    
    def _predict_form_trends(self, 
                           dominant_forms: Dict, 
                           evolution_trends: Dict) -> Dict:
        """预测斗争形式趋势"""
        predictions = {}
        
        for form_name, current_ratio in dominant_forms.items():
            if form_name in evolution_trends and len(evolution_trends[form_name]) >= 2:
                # 计算趋势斜率
                recent_trend = evolution_trends[form_name][-2:]
                if len(recent_trend) == 2:
                    slope = recent_trend[1] - recent_trend[0]
                    predictions[form_name] = {
                        'current_ratio': current_ratio,
                        'trend_slope': slope,
                        'prediction_5_years': max(0, current_ratio + slope * 5),
                        'trend_direction': '上升' if slope > 0 else '下降' if slope < 0 else '稳定'
                    }
        
        return predictions
    
    def determine_conflict_stage(self, 
                               conflict_indicators: Dict) -> Tuple[ConflictStage, float]:
        """
        确定矛盾发展阶段
        
        Args:
            conflict_indicators: 冲突指标
            
        Returns:
            (发展阶段, 阶段分数)
        """
        # 计算各项指标
        intensity = conflict_indicators.get('intensity', 0)
        frequency = conflict_indicators.get('frequency', 0)
        scope = conflict_indicators.get('scope', 0)
        organization = conflict_indicators.get('organization_level', 0)
        consciousness = conflict_indicators.get('consciousness_level', 0)
        
        # 综合分数计算
        stage_score = (intensity * 0.3 + 
                      frequency * 0.2 + 
                      scope * 0.2 + 
                      organization * 0.15 + 
                      consciousness * 0.15)
        
        # 确定发展阶段
        if stage_score < 0.2:
            return ConflictStage.LATENT_STAGE, stage_score
        elif stage_score < 0.4:
            return ConflictStage.EMERGING_STAGE, stage_score
        elif stage_score < 0.6:
            return ConflictStage.DEVELOPING_STAGE, stage_score
        elif stage_score < 0.8:
            return ConflictStage.ACUTE_STAGE, stage_score
        else:
            return ConflictStage.RESOLUTION_STAGE, stage_score
    
    def predict_conflict_evolution(self, 
                                 current_stage: ConflictStage,
                                 stage_score: float,
                                 driving_factors: Dict,
                                 historical_patterns: List[Dict]) -> Dict:
        """
        预测矛盾演化路径
        
        Args:
            current_stage: 当前阶段
            stage_score: 阶段分数
            driving_factors: 驱动因素
            historical_patterns: 历史模式
            
        Returns:
            演化预测结果
        """
        evolution_prediction = {
            'current_stage': current_stage.value,
            'stage_score': stage_score,
            'time_to_next_stage': None,
            'next_stage': None,
            'evolution_path': [],
            'critical_factors': [],
            'intervention_points': []
        }
        
        # 计算驱动因素的综合影响
        total_driving_force = sum(driving_factors.values()) / len(driving_factors)
        
        # 基于历史模式预测时间
        if historical_patterns:
            avg_transition_time = self._calculate_average_transition_time(
                historical_patterns, current_stage
            )
            evolution_prediction['time_to_next_stage'] = avg_transition_time
        
        # 预测下一阶段
        next_stage = self._predict_next_stage(current_stage, stage_score, total_driving_force)
        evolution_prediction['next_stage'] = next_stage.value if next_stage else None
        
        # 构建演化路径
        evolution_prediction['evolution_path'] = self._construct_evolution_path(
            current_stage, stage_score, total_driving_force
        )
        
        # 识别关键因素
        evolution_prediction['critical_factors'] = self._identify_critical_factors(driving_factors)
        
        # 确定干预点
        evolution_prediction['intervention_points'] = self._identify_intervention_points(
            current_stage, evolution_prediction['evolution_path']
        )
        
        return evolution_prediction
    
    def _calculate_average_transition_time(self, 
                                         patterns: List[Dict], 
                                         current_stage: ConflictStage) -> float:
        """计算平均转换时间"""
        transition_times = []
        current_stage_name = current_stage.value
        
        for pattern in patterns:
            if pattern.get('from_stage') == current_stage_name:
                transition_times.append(pattern.get('transition_time', 2.0))
        
        return np.mean(transition_times) if transition_times else 2.0
    
    def _predict_next_stage(self, 
                          current_stage: ConflictStage,
                          stage_score: float,
                          driving_force: float) -> Optional[ConflictStage]:
        """预测下一阶段"""
        stage_order = [
            ConflictStage.LATENT_STAGE,
            ConflictStage.EMERGING_STAGE,
            ConflictStage.DEVELOPING_STAGE,
            ConflictStage.ACUTE_STAGE,
            ConflictStage.RESOLUTION_STAGE
        ]
        
        current_index = stage_order.index(current_stage)
        
        # 驱动力强且分数高时进入下一阶段
        if driving_force > 0.6 and stage_score > 0.7:
            if current_index < len(stage_order) - 1:
                return stage_order[current_index + 1]
        
        # 驱动力弱时可能倒退
        elif driving_force < 0.3 and stage_score < 0.4:
            if current_index > 0:
                return stage_order[current_index - 1]
        
        return None
    
    def _construct_evolution_path(self, 
                                current_stage: ConflictStage,
                                stage_score: float,
                                driving_force: float) -> List[Dict]:
        """构建演化路径"""
        path = []
        stage_order = [
            ConflictStage.LATENT_STAGE,
            ConflictStage.EMERGING_STAGE,
            ConflictStage.DEVELOPING_STAGE,
            ConflictStage.ACUTE_STAGE,
            ConflictStage.RESOLUTION_STAGE
        ]
        
        current_index = stage_order.index(current_stage)
        
        # 正向演化路径
        if driving_force > 0.5:
            for i in range(current_index, min(current_index + 3, len(stage_order))):
                path.append({
                    'stage': stage_order[i].value,
                    'estimated_score': min(1.0, stage_score + (i - current_index) * 0.2),
                    'probability': 0.8 - (i - current_index) * 0.2
                })
        
        # 负向演化路径
        elif driving_force < 0.3:
            for i in range(current_index, max(current_index - 2, -1), -1):
                path.append({
                    'stage': stage_order[i].value,
                    'estimated_score': max(0.0, stage_score - (current_index - i) * 0.15),
                    'probability': 0.7 - (current_index - i) * 0.2
                })
        
        return path
    
    def _identify_critical_factors(self, driving_factors: Dict) -> List[Dict]:
        """识别关键因素"""
        critical_factors = []
        sorted_factors = sorted(driving_factors.items(), key=lambda x: x[1], reverse=True)
        
        for factor_name, factor_value in sorted_factors[:3]:  # 取前3个
            critical_factors.append({
                'factor': factor_name,
                'influence_level': factor_value,
                'importance': '关键' if factor_value > 0.7 else '重要' if factor_value > 0.5 else '一般'
            })
        
        return critical_factors
    
    def _identify_intervention_points(self, 
                                    current_stage: ConflictStage,
                                    evolution_path: List[Dict]) -> List[Dict]:
        """识别干预点"""
        intervention_points = []
        
        # 基于当前阶段的干预点
        stage_interventions = {
            ConflictStage.LATENT_STAGE: [
                "加强预警监测",
                "完善利益表达机制",
                "促进阶级对话"
            ],
            ConflictStage.EMERGING_STAGE: [
                "及时回应诉求",
                "建立调解机制",
                "防止冲突升级"
            ],
            ConflictStage.DEVELOPING_STAGE: [
                "深化制度改革",
                "加强法律规范",
                "促进社会和解"
            ],
            ConflictStage.ACUTE_STAGE: [
                "紧急危机干预",
                "维护社会稳定",
                "寻求解决方案"
            ],
            ConflictStage.RESOLUTION_STAGE: [
                "巩固改革成果",
                "建立长效机制",
                "总结经验教训"
            ]
        }
        
        interventions = stage_interventions.get(current_stage, [])
        for intervention in interventions:
            intervention_points.append({
                'intervention': intervention,
                'timing': '当前阶段',
                'priority': '高'
            })
        
        # 基于演化路径的预防性干预点
        if evolution_path and len(evolution_path) > 1:
            next_stage = evolution_path[1]['stage']
            if next_stage == '激化阶段':
                intervention_points.append({
                    'intervention': "预防性冲突降温",
                    'timing': '近期',
                    'priority': '极高'
                })
        
        return intervention_points

def generate_conflict_analysis_report(analyzer: ClassConflictAnalyzer,
                                   class_data: Dict,
                                   historical_events: List[Dict]) -> str:
    """
    生成阶级矛盾分析报告
    
    Args:
        analyzer: 分析器实例
        class_data: 阶级数据
        historical_events: 历史事件
        
    Returns:
        分析报告
    """
    # 量化阶级利益
    interests_data = analyzer.quantify_class_interests(class_data)
    
    # 计算冲突矩阵
    conflict_matrix = analyzer.calculate_interest_conflict_matrix(interests_data)
    class_names = list(class_data.keys())
    
    # 识别冲突热点
    hotspots = analyzer.identify_conflict_hotspots(conflict_matrix, class_names)
    
    # 分析斗争形式
    struggle_analysis = analyzer.analyze_struggle_forms(hotspots, historical_events)
    
    # 确定当前阶段
    conflict_indicators = {
        'intensity': np.mean([h['conflict_intensity'] for h in hotspots]) if hotspots else 0,
        'frequency': len(historical_events) / 10,  # 假设10年期间
        'scope': 0.6,  # 需要实际数据
        'organization_level': 0.5,  # 需要实际数据
        'consciousness_level': 0.4  # 需要实际数据
    }
    
    current_stage, stage_score = analyzer.determine_conflict_stage(conflict_indicators)
    
    # 预测演化
    driving_factors = {
        'economic_inequality': 0.7,
        'political_polarization': 0.6,
        'social_mobility_decline': 0.5,
        'technology_disruption': 0.4
    }
    
    evolution_prediction = analyzer.predict_conflict_evolution(
        current_stage, stage_score, driving_factors, []
    )
    
    # 生成报告
    report = f"""
# 阶级矛盾分析报告

## 一、利益冲突量化分析
"""
    
    for class_name, interests in interests_data.items():
        report += f"""
### {class_name}
- 经济利益总分: {np.mean(list(interests['economic'].values())):.3f}
- 政治利益总分: {np.mean(list(interests['political'].values())):.3f}
- 社会利益总分: {np.mean(list(interests['social'].values())):.3f}
- 综合利益分数: {interests['total_interest_score']:.3f}
"""
    
    report += f"""
## 二、冲突热点识别
"""
    
    for hotspot in hotspots[:5]:  # 显示前5个热点
        report += f"""
- {hotspot['class_a']} vs {hotspot['class_b']}: {hotspot['conflict_level']} ({hotspot['conflict_intensity']:.3f})
"""
    
    report += f"""
## 三、斗争形式分析
"""
    
    for form, ratio in struggle_analysis['dominant_forms'].items():
        effectiveness = struggle_analysis['form_effectiveness'].get(form, 0)
        report += f"- {form}: 占比{ratio:.1%}, 有效性{effectiveness:.3f}\n"
    
    report += f"""
## 四、矛盾发展阶段
- 当前阶段: {current_stage.value}
- 阶段分数: {stage_score:.3f}
- 阶段特征: {evolution_prediction['current_stage']}

## 五、演化趋势预测
- 下一阶段: {evolution_prediction['next_stage']}
- 预计转换时间: {evolution_prediction['time_to_next_stage']:.1f}年

### 关键驱动因素
"""
    
    for factor in evolution_prediction['critical_factors']:
        report += f"- {factor['factor']}: {factor['importance']} (影响度: {factor['influence_level']:.3f})\n"
    
    report += f"""
### 干预建议
"""
    
    for intervention in evolution_prediction['intervention_points']:
        report += f"- {intervention['intervention']} ({intervention['priority']}优先级)\n"
    
    return report

# 示例使用
if __name__ == "__main__":
    # 创建分析器
    analyzer = ClassConflictAnalyzer()
    
    # 模拟数据
    class_data = {
        '资产阶级': {
            'income_stability': 0.9,
            'property_security': 0.95,
            'growth_expectation': 0.7,
            'redistribution_support': 0.2,
            'political_influence': 0.85,
            'policy_impact': 0.8,
            'representation_level': 0.9,
            'legal_security': 0.95,
            'social_prestige': 0.9,
            'education_opportunity': 0.95,
            'healthcare_access': 0.95,
            'mobility_opportunity': 0.8
        },
        '无产阶级': {
            'income_stability': 0.3,
            'property_security': 0.2,
            'growth_expectation': 0.4,
            'redistribution_support': 0.8,
            'political_influence': 0.3,
            'policy_impact': 0.25,
            'representation_level': 0.4,
            'legal_security': 0.5,
            'social_prestige': 0.3,
            'education_opportunity': 0.4,
            'healthcare_access': 0.6,
            'mobility_opportunity': 0.3
        }
    }
    
    historical_events = [
        {
            'date': '2020-01-01',
            'form': 'ECONOMIC_STRUGGLE',
            'success_rate': 0.6,
            'scale': 0.7
        },
        {
            'date': '2021-06-01',
            'form': 'POLITICAL_STRUGGLE',
            'success_rate': 0.4,
            'scale': 0.5
        }
    ]
    
    # 生成报告
    report = generate_conflict_analysis_report(analyzer, class_data, historical_events)
    print(report)