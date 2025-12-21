#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶级意识分析系统
Class Consciousness Analysis System

专门用于分析阶级意识水平、从自在阶级到自为阶级转化、阶级意识发展规律的专业系统
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import math
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ConsciousnessDimension(Enum):
    """意识维度枚举"""
    ECONOMIC_CONSCIOUSNESS = "经济意识"  # 经济意识
    POLITICAL_CONSCIOUSNESS = "政治意识"  # 政治意识
    SOCIAL_CONSCIOUSNESS = "社会意识"  # 社会意识
    HISTORICAL_CONSCIOUSNESS = "历史意识"  # 历史意识
    REVOLUTIONARY_CONSCIOUSNESS = "革命意识"  # 革命意识

class TransformationPhase(Enum):
    """转化阶段枚举"""
    SPONTANEOUS_STAGE = "自发阶段"  # 自发阶段
    AWARENESS_EMERGING = "意识萌芽"  # 意识萌芽
    CONSCIOUS_ORGANIZATION = "自觉组织"  # 自觉组织
    THEORETICAL_MATURITY = "理论成熟"  # 理论成熟
    REVOLUTIONARY_ACTION = "革命行动"  # 革命行动

@dataclass
class ConsciousnessIndicator:
    """意识指标数据结构"""
    dimension: ConsciousnessDimension
    value: float  # 指标值 (0-1)
    weight: float  # 权重
    measurement_method: str  # 测量方法
    reliability: float  # 可靠性
    
    def weighted_score(self) -> float:
        """计算加权分数"""
        return self.value * self.weight

@dataclass
class TransformationFactor:
    """转化因子数据结构"""
    factor_name: str
    influence_direction: float  # 影响方向 (-1 to 1)
    influence_strength: float  # 影响强度 (0-1)
    time_lag: float  # 时间滞后 (年)
    sustainability: float  # 持续性 (0-1)
    
    def effective_influence(self) -> float:
        """计算有效影响"""
        return self.influence_direction * self.influence_strength * self.sustainability

@dataclass
class ConsciousnessDevelopment:
    """意识发展数据结构"""
    time_point: datetime
    overall_level: float  # 整体水平
    dimension_scores: Dict[ConsciousnessDimension, float]
    transformation_stage: TransformationPhase
    key_events: List[str]
    external_factors: Dict[str, float]
    
    def development_velocity(self, previous_point: 'ConsciousnessDevelopment') -> float:
        """计算发展速度"""
        time_diff = (self.time_point - previous_point.time_point).days / 365.25
        if time_diff == 0:
            return 0
        level_diff = self.overall_level - previous_point.overall_level
        return level_diff / time_diff

class ClassConsciousnessAnalyzer:
    """阶级意识分析器"""
    
    def __init__(self):
        self.consciousness_weights = {
            ConsciousnessDimension.ECONOMIC_CONSCIOUSNESS: 0.25,
            ConsciousnessDimension.POLITICAL_CONSCIOUSNESS: 0.25,
            ConsciousnessDimension.SOCIAL_CONSCIOUSNESS: 0.20,
            ConsciousnessDimension.HISTORICAL_CONSCIOUSNESS: 0.15,
            ConsciousnessDimension.REVOLUTIONARY_CONSCIOUSNESS: 0.15
        }
        
        self.transformation_thresholds = {
            'spontaneous_to_aware': 0.2,
            'aware_to_organized': 0.4,
            'organized_to_mature': 0.6,
            'mature_to_revolutionary': 0.8
        }
        
        self.measurement_methods = {
            'survey': '问卷调查',
            'interview': '深度访谈',
            'observation': '参与观察',
            'content_analysis': '内容分析',
            'behavioral_analysis': '行为分析'
        }
    
    def construct_consciousness_indicators(self) -> Dict[ConsciousnessDimension, List[ConsciousnessIndicator]]:
        """
        构建阶级意识指标体系
        
        Returns:
            各维度的指标列表
        """
        indicators = {}
        
        # 经济意识指标
        indicators[ConsciousnessDimension.ECONOMIC_CONSCIOUSNESS] = [
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.ECONOMIC_CONSCIOUSNESS,
                value=0.0,  # 待测量
                weight=0.3,
                measurement_method='survey',
                reliability=0.8
            ),
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.ECONOMIC_CONSCIOUSNESS,
                value=0.0,
                weight=0.4,
                measurement_method='interview',
                reliability=0.85
            ),
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.ECONOMIC_CONSCIOUSNESS,
                value=0.0,
                weight=0.3,
                measurement_method='observation',
                reliability=0.75
            )
        ]
        
        # 政治意识指标
        indicators[ConsciousnessDimension.POLITICAL_CONSCIOUSNESS] = [
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.POLITICAL_CONSCIOUSNESS,
                value=0.0,
                weight=0.35,
                measurement_method='survey',
                reliability=0.8
            ),
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.POLITICAL_CONSCIOUSNESS,
                value=0.0,
                weight=0.35,
                measurement_method='content_analysis',
                reliability=0.82
            ),
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.POLITICAL_CONSCIOUSNESS,
                value=0.0,
                weight=0.3,
                measurement_method='behavioral_analysis',
                reliability=0.78
            )
        ]
        
        # 社会意识指标
        indicators[ConsciousnessDimension.SOCIAL_CONSCIOUSNESS] = [
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.SOCIAL_CONSCIOUSNESS,
                value=0.0,
                weight=0.4,
                measurement_method='survey',
                reliability=0.79
            ),
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.SOCIAL_CONSCIOUSNESS,
                value=0.0,
                weight=0.3,
                measurement_method='interview',
                reliability=0.83
            ),
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.SOCIAL_CONSCIOUSNESS,
                value=0.0,
                weight=0.3,
                measurement_method='observation',
                reliability=0.77
            )
        ]
        
        # 历史意识指标
        indicators[ConsciousnessDimension.HISTORICAL_CONSCIOUSNESS] = [
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.HISTORICAL_CONSCIOUSNESS,
                value=0.0,
                weight=0.5,
                measurement_method='interview',
                reliability=0.85
            ),
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.HISTORICAL_CONSCIOUSNESS,
                value=0.0,
                weight=0.5,
                measurement_method='content_analysis',
                reliability=0.8
            )
        ]
        
        # 革命意识指标
        indicators[ConsciousnessDimension.REVOLUTIONARY_CONSCIOUSNESS] = [
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.REVOLUTIONARY_CONSCIOUSNESS,
                value=0.0,
                weight=0.4,
                measurement_method='survey',
                reliability=0.82
            ),
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.REVOLUTIONARY_CONSCIOUSNESS,
                value=0.0,
                weight=0.3,
                measurement_method='behavioral_analysis',
                reliability=0.79
            ),
            ConsciousnessIndicator(
                dimension=ConsciousnessDimension.REVOLUTIONARY_CONSCIOUSNESS,
                value=0.0,
                weight=0.3,
                measurement_method='interview',
                reliability=0.84
            )
        ]
        
        return indicators
    
    def measure_consciousness_level(self, 
                                  individual_data: Dict,
                                  indicators: Dict[ConsciousnessDimension, List[ConsciousnessIndicator]]) -> Dict:
        """
        测量阶级意识水平
        
        Args:
            individual_data: 个体数据
            indicators: 指标体系
            
        Returns:
            意识水平测量结果
        """
        measurement_results = {}
        
        for dimension, dim_indicators in indicators.items():
            dimension_score = 0.0
            total_weight = 0.0
            
            for indicator in dim_indicators:
                # 根据测量方法获取数据
                raw_value = self._extract_indicator_value(indicator.measurement_method, individual_data, dimension)
                indicator.value = raw_value
                
                weighted_score = indicator.weighted_score()
                dimension_score += weighted_score
                total_weight += indicator.weight
            
            # 标准化维度分数
            if total_weight > 0:
                dimension_score = dimension_score / total_weight
            
            measurement_results[dimension] = {
                'score': dimension_score,
                'indicators': dim_indicators,
                'reliability': np.mean([ind.reliability for ind in dim_indicators])
            }
        
        # 计算整体意识水平
        overall_score = 0.0
        for dimension, result in measurement_results.items():
            overall_score += result['score'] * self.consciousness_weights[dimension]
        
        return {
            'overall_level': overall_score,
            'dimension_scores': {dim.value: result['score'] for dim, result in measurement_results.items()},
            'dimension_reliability': {dim.value: result['reliability'] for dim, result in measurement_results.items()},
            'measurement_quality': np.mean([result['reliability'] for result in measurement_results.values()])
        }
    
    def _extract_indicator_value(self, 
                               method: str, 
                               data: Dict, 
                               dimension: ConsciousnessDimension) -> float:
        """提取指标值"""
        method_mappings = {
            'survey': {
                ConsciousnessDimension.ECONOMIC_CONSCIOUSNESS: data.get('economic_survey_score', 0.5),
                ConsciousnessDimension.POLITICAL_CONSCIOUSNESS: data.get('political_survey_score', 0.5),
                ConsciousnessDimension.SOCIAL_CONSCIOUSNESS: data.get('social_survey_score', 0.5),
                ConsciousnessDimension.HISTORICAL_CONSCIOUSNESS: data.get('historical_survey_score', 0.5),
                ConsciousnessDimension.REVOLUTIONARY_CONSCIOUSNESS: data.get('revolutionary_survey_score', 0.5)
            },
            'interview': {
                ConsciousnessDimension.ECONOMIC_CONSCIOUSNESS: data.get('economic_interview_score', 0.5),
                ConsciousnessDimension.POLITICAL_CONSCIOUSNESS: data.get('political_interview_score', 0.5),
                ConsciousnessDimension.SOCIAL_CONSCIOUSNESS: data.get('social_interview_score', 0.5),
                ConsciousnessDimension.HISTORICAL_CONSCIOUSNESS: data.get('historical_interview_score', 0.5),
                ConsciousnessDimension.REVOLUTIONARY_CONSCIOUSNESS: data.get('revolutionary_interview_score', 0.5)
            },
            'observation': {
                ConsciousnessDimension.ECONOMIC_CONSCIOUSNESS: data.get('economic_observation_score', 0.5),
                ConsciousnessDimension.POLITICAL_CONSCIOUSNESS: data.get('political_observation_score', 0.5),
                ConsciousnessDimension.SOCIAL_CONSCIOUSNESS: data.get('social_observation_score', 0.5)
            },
            'content_analysis': {
                ConsciousnessDimension.POLITICAL_CONSCIOUSNESS: data.get('political_content_score', 0.5),
                ConsciousnessDimension.HISTORICAL_CONSCIOUSNESS: data.get('historical_content_score', 0.5)
            },
            'behavioral_analysis': {
                ConsciousnessDimension.POLITICAL_CONSCIOUSNESS: data.get('political_behavior_score', 0.5),
                ConsciousnessDimension.REVOLUTIONARY_CONSCIOUSNESS: data.get('revolutionary_behavior_score', 0.5)
            }
        }
        
        return method_mappings.get(method, {}).get(dimension, 0.5)
    
    def analyze_transformation_process(self, 
                                     consciousness_history: List[ConsciousnessDevelopment]) -> Dict:
        """
        分析从自在阶级到自为阶级的转化过程
        
        Args:
            consciousness_history: 意识发展历史
            
        Returns:
            转化过程分析结果
        """
        if len(consciousness_history) < 2:
            return {'error': '历史数据不足，无法分析转化过程'}
        
        # 识别转化阶段
        transformation_stages = self._identify_transformation_stages(consciousness_history)
        
        # 计算转化速度
        transformation_velocities = []
        for i in range(1, len(consciousness_history)):
            velocity = consciousness_history[i].development_velocity(consciousness_history[i-1])
            transformation_velocities.append(velocity)
        
        # 识别关键转折点
        turning_points = self._identify_turning_points(consciousness_history)
        
        # 分析转化因子
        transformation_factors = self._analyze_transformation_factors(consciousness_history)
        
        # 评估转化质量
        transformation_quality = self._evaluate_transformation_quality(consciousness_history)
        
        return {
            'transformation_stages': transformation_stages,
            'average_velocity': np.mean(transformation_velocities),
            'velocity_variance': np.var(transformation_velocities),
            'turning_points': turning_points,
            'transformation_factors': transformation_factors,
            'transformation_quality': transformation_quality,
            'current_stage': consciousness_history[-1].transformation_stage.value,
            'current_level': consciousness_history[-1].overall_level
        }
    
    def _identify_transformation_stages(self, 
                                      history: List[ConsciousnessDevelopment]) -> List[Dict]:
        """识别转化阶段"""
        stages = []
        
        for development in history:
            stage_info = {
                'time': development.time_point,
                'stage': development.transformation_stage.value,
                'level': development.overall_level,
                'key_events': development.key_events
            }
            stages.append(stage_info)
        
        return stages
    
    def _identify_turning_points(self, 
                               history: List[ConsciousnessDevelopment]) -> List[Dict]:
        """识别关键转折点"""
        turning_points = []
        
        for i in range(1, len(history)):
            prev_level = history[i-1].overall_level
            curr_level = history[i].overall_level
            level_change = abs(curr_level - prev_level)
            
            # 阶段变化
            prev_stage = history[i-1].transformation_stage
            curr_stage = history[i].transformation_stage
            
            if level_change > 0.1 or prev_stage != curr_stage:
                turning_points.append({
                    'time': history[i].time_point,
                    'level_change': level_change,
                    'previous_stage': prev_stage.value,
                    'current_stage': curr_stage.value,
                    'key_events': history[i].key_events,
                    'external_factors': history[i].external_factors
                })
        
        return turning_points
    
    def _analyze_transformation_factors(self, 
                                      history: List[ConsciousnessDevelopment]) -> List[TransformationFactor]:
        """分析转化因子"""
        factors = []
        
        # 经济因素
        economic_influence = self._calculate_factor_influence(history, 'economic_crisis')
        factors.append(TransformationFactor(
            factor_name='经济危机',
            influence_direction=1.0 if economic_influence > 0 else -1.0,
            influence_strength=abs(economic_influence),
            time_lag=0.5,
            sustainability=0.7
        ))
        
        # 政治因素
        political_influence = self._calculate_factor_influence(history, 'political_repression')
        factors.append(TransformationFactor(
            factor_name='政治压迫',
            influence_direction=1.0 if political_influence > 0 else -1.0,
            influence_strength=abs(political_influence),
            time_lag=0.3,
            sustainability=0.8
        ))
        
        # 组织因素
        organizational_influence = self._calculate_factor_influence(history, 'organizational_development')
        factors.append(TransformationFactor(
            factor_name='组织发展',
            influence_direction=1.0,
            influence_strength=abs(organizational_influence),
            time_lag=1.0,
            sustainability=0.9
        ))
        
        # 思想因素
        ideological_influence = self._calculate_factor_influence(history, 'ideological_education')
        factors.append(TransformationFactor(
            factor_name='思想教育',
            influence_direction=1.0,
            influence_strength=abs(ideological_influence),
            time_lag=0.8,
            sustainability=0.6
        ))
        
        return sorted(factors, key=lambda f: f.effective_influence(), reverse=True)
    
    def _calculate_factor_influence(self, 
                                  history: List[ConsciousnessDevelopment], 
                                  factor_name: str) -> float:
        """计算因子影响"""
        correlations = []
        
        for i in range(1, len(history)):
            factor_value = history[i].external_factors.get(factor_name, 0)
            prev_factor_value = history[i-1].external_factors.get(factor_name, 0)
            factor_change = factor_value - prev_factor_value
            
            consciousness_change = history[i].overall_level - history[i-1].overall_level
            
            if factor_change != 0:
                correlation = consciousness_change / factor_change
                correlations.append(correlation)
        
        return np.mean(correlations) if correlations else 0
    
    def _evaluate_transformation_quality(self, 
                                       history: List[ConsciousnessDevelopment]) -> Dict:
        """评估转化质量"""
        latest = history[-1]
        
        # 综合性评估
        dimension_balance = 1.0 - np.std(list(latest.dimension_scores.values()))
        
        # 持续性评估
        if len(history) >= 3:
            recent_trend = [h.overall_level for h in history[-3:]]
            sustainability = 1.0 if recent_trend == sorted(recent_trend) else 0.5
        else:
            sustainability = 0.5
        
        # 深度评估
        depth_score = np.mean([
            latest.dimension_scores.get('历史意识', 0),
            latest.dimension_scores.get('革命意识', 0)
        ])
        
        # 组织化程度
        organization_level = history[-1].external_factors.get('organizational_level', 0.5)
        
        return {
            'comprehensiveness': dimension_balance,
            'sustainability': sustainability,
            'depth': depth_score,
            'organization': organization_level,
            'overall_quality': (dimension_balance + sustainability + depth_score + organization_level) / 4
        }
    
    def model_consciousness_development_law(self, 
                                          historical_data: List[ConsciousnessDevelopment],
                                          social_context: Dict) -> Dict:
        """
        建立阶级意识发展规律模型
        
        Args:
            historical_data: 历史数据
            social_context: 社会背景
            
        Returns:
            发展规律模型
        """
        # 提取发展模式
        development_patterns = self._extract_development_patterns(historical_data)
        
        # 建立数学模型
        mathematical_model = self._build_mathematical_model(historical_data)
        
        # 识别发展阶段规律
        stage_patterns = self._identify_stage_patterns(historical_data)
        
        # 分析环境影响因素
        environmental_factors = self._analyze_environmental_factors(historical_data, social_context)
        
        # 预测未来发展趋势
        future_trends = self._predict_future_trends(mathematical_model, environmental_factors)
        
        return {
            'development_patterns': development_patterns,
            'mathematical_model': mathematical_model,
            'stage_patterns': stage_patterns,
            'environmental_factors': environmental_factors,
            'future_trends': future_trends,
            'model_confidence': self._calculate_model_confidence(historical_data)
        }
    
    def _extract_development_patterns(self, 
                                    history: List[ConsciousnessDevelopment]) -> Dict:
        """提取发展模式"""
        patterns = {}
        
        # 周期性模式
        if len(history) >= 6:
            levels = [h.overall_level for h in history]
            # 简化的周期性检测
            autocorr = np.correlate(levels, levels, mode='full')
            max_autocorr = np.max(autocorr[len(levels):])
            patterns['cyclical_pattern'] = max_autocorr > 0.5
        
        # 阶梯式发展模式
        stage_changes = 0
        for i in range(1, len(history)):
            if history[i].transformation_stage != history[i-1].transformation_stage:
                stage_changes += 1
        patterns['staircase_development'] = stage_changes >= 2
        
        # 突变模式
        level_changes = [abs(history[i].overall_level - history[i-1].overall_level) 
                        for i in range(1, len(history))]
        sudden_changes = sum(1 for change in level_changes if change > 0.2)
        patterns['sudden_change_pattern'] = sudden_changes > 0
        
        return patterns
    
    def _build_mathematical_model(self, 
                                history: List[ConsciousnessDevelopment]) -> Dict:
        """建立数学模型"""
        if len(history) < 3:
            return {'error': '数据不足，无法建立数学模型'}
        
        # 时间序列数据准备
        time_points = [(h.time_point - history[0].time_point).days / 365.25 for h in history]
        levels = [h.overall_level for h in history]
        
        # 线性趋势
        linear_coeffs = np.polyfit(time_points, levels, 1)
        linear_trend = linear_coeffs[0]
        
        # 二次趋势
        quadratic_coeffs = np.polyfit(time_points, levels, 2)
        
        # 逻辑增长模型参数
        try:
            max_level = max(levels)
            if max_level > 0:
                normalized_levels = [l / max_level for l in levels]
                # 简化的逻辑增长拟合
                logistic_params = {
                    'carrying_capacity': max_level,
                    'growth_rate': linear_trend * 2,
                    'inflection_point': time_points[len(time_points)//2]
                }
            else:
                logistic_params = None
        except:
            logistic_params = None
        
        return {
            'linear_model': {
                'slope': linear_trend,
                'intercept': linear_coeffs[1],
                'r_squared': self._calculate_r_squared(time_points, levels, linear_coeffs)
            },
            'quadratic_model': {
                'coefficients': quadratic_coeffs.tolist(),
                'r_squared': self._calculate_r_squared(time_points, levels, quadratic_coeffs)
            },
            'logistic_model': logistic_params,
            'best_fit_model': self._determine_best_fit_model(time_points, levels)
        }
    
    def _calculate_r_squared(self, 
                           x: List[float], 
                           y: List[float], 
                           coeffs: np.ndarray) -> float:
        """计算R平方"""
        y_pred = np.polyval(coeffs, x)
        ss_res = np.sum((y - y_pred) ** 2)
        ss_tot = np.sum((y - np.mean(y)) ** 2)
        return 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
    
    def _determine_best_fit_model(self, 
                                x: List[float], 
                                y: List[float]) -> str:
        """确定最佳拟合模型"""
        # 简化的最佳模型选择
        linear_coeffs = np.polyfit(x, y, 1)
        quadratic_coeffs = np.polyfit(x, y, 2)
        
        linear_r2 = self._calculate_r_squared(x, y, linear_coeffs)
        quadratic_r2 = self._calculate_r_squared(x, y, quadratic_coeffs)
        
        if quadratic_r2 > linear_r2 + 0.1:
            return 'quadratic'
        elif linear_r2 > 0.7:
            return 'linear'
        else:
            return 'complex'
    
    def _identify_stage_patterns(self, 
                               history: List[ConsciousnessDevelopment]) -> Dict:
        """识别阶段规律"""
        stage_durations = {}
        stage_sequences = []
        
        current_stage = None
        stage_start = None
        
        for development in history:
            if development.transformation_stage != current_stage:
                if current_stage is not None:
                    duration = (development.time_point - stage_start).days / 365.25
                    stage_durations[current_stage.value] = duration
                
                current_stage = development.transformation_stage
                stage_start = development.time_point
                stage_sequences.append(current_stage.value)
        
        # 计算平均阶段持续时间
        avg_durations = {}
        for stage, duration in stage_durations.items():
            avg_durations[stage] = duration
        
        return {
            'stage_sequence': stage_sequences,
            'average_durations': avg_durations,
            'stage_transition_patterns': self._analyze_transition_patterns(stage_sequences)
        }
    
    def _analyze_transition_patterns(self, sequences: List[str]) -> Dict:
        """分析转换模式"""
        transitions = {}
        
        for i in range(len(sequences) - 1):
            transition = f"{sequences[i]} -> {sequences[i+1]}"
            transitions[transition] = transitions.get(transition, 0) + 1
        
        return transitions
    
    def _analyze_environmental_factors(self, 
                                     history: List[ConsciousnessDevelopment],
                                     context: Dict) -> Dict:
        """分析环境因素"""
        factor_influences = {}
        
        for development in history:
            for factor, value in development.external_factors.items():
                if factor not in factor_influences:
                    factor_influences[factor] = []
                factor_influences[factor].append((development.overall_level, value))
        
        # 计算相关性
        factor_correlations = {}
        for factor, pairs in factor_influences.items():
            if len(pairs) >= 2:
                levels, values = zip(*pairs)
                correlation = np.corrcoef(levels, values)[0, 1]
                factor_correlations[factor] = correlation if not np.isnan(correlation) else 0
        
        return {
            'factor_correlations': factor_correlations,
            'significant_factors': {k: v for k, v in factor_correlations.items() if abs(v) > 0.5},
            'context_integration': context
        }
    
    def _predict_future_trends(self, 
                             mathematical_model: Dict,
                             environmental_factors: Dict) -> Dict:
        """预测未来趋势"""
        if 'error' in mathematical_model:
            return {'error': '无法预测：模型建立失败'}
        
        best_model = mathematical_model.get('best_fit_model', 'linear')
        future_years = 5
        
        if best_model == 'linear':
            slope = mathematical_model['linear_model']['slope']
            intercept = mathematical_model['linear_model']['intercept']
            future_trend = [intercept + slope * (10 + i) for i in range(future_years)]
        else:
            # 简化预测：使用当前趋势
            future_trend = [0.7 + i * 0.05 for i in range(future_years)]
        
        # 考虑环境因素影响
        significant_factors = environmental_factors.get('significant_factors', {})
        factor_adjustment = sum(significant_factors.values()) * 0.1
        
        adjusted_trend = [min(1.0, max(0.0, val + factor_adjustment)) for val in future_trend]
        
        return {
            'predicted_levels': adjusted_trend,
            'time_horizon': future_years,
            'confidence_interval': 0.15,  # 简化的置信区间
            'key_assumptions': [
                '环境因素保持相对稳定',
                '历史发展模式持续有效',
                '无重大突发干扰事件'
            ]
        }
    
    def _calculate_model_confidence(self, 
                                  history: List[ConsciousnessDevelopment]) -> float:
        """计算模型置信度"""
        # 基于数据量、质量、时间跨度的综合置信度
        data_points = len(history)
        time_span = (history[-1].time_point - history[0].time_point).days / 365.25
        
        data_confidence = min(1.0, data_points / 10)
        time_confidence = min(1.0, time_span / 10)
        
        return (data_confidence + time_confidence) / 2

def generate_consciousness_analysis_report(analyzer: ClassConsciousnessAnalyzer,
                                         individual_data: Dict,
                                         consciousness_history: List[ConsciousnessDevelopment],
                                         social_context: Dict) -> str:
    """
    生成阶级意识分析报告
    
    Args:
        analyzer: 分析器实例
        individual_data: 个体数据
        consciousness_history: 意识历史
        social_context: 社会背景
        
    Returns:
        分析报告
    """
    # 构建指标体系
    indicators = analyzer.construct_consciousness_indicators()
    
    # 测量意识水平
    measurement_result = analyzer.measure_consciousness_level(individual_data, indicators)
    
    # 分析转化过程
    transformation_analysis = analyzer.analyze_transformation_process(consciousness_history)
    
    # 建立发展规律模型
    development_model = analyzer.model_consciousness_development_law(consciousness_history, social_context)
    
    # 生成报告
    report = f"""
# 阶级意识分析报告

## 一、意识水平测量结果
- 整体意识水平: {measurement_result['overall_level']:.3f}
- 测量质量: {measurement_result['measurement_quality']:.3f}

### 各维度得分
"""
    
    for dimension, score in measurement_result['dimension_scores'].items():
        reliability = measurement_result['dimension_reliability'][dimension]
        report += f"- {dimension}: {score:.3f} (可靠性: {reliability:.3f})\n"
    
    if 'error' not in transformation_analysis:
        report += f"""
## 二、转化过程分析
- 当前转化阶段: {transformation_analysis['current_stage']}
- 平均转化速度: {transformation_analysis['average_velocity']:.3f}/年
- 转化质量: {transformation_analysis['transformation_quality']['overall_quality']:.3f}

### 关键转折点
"""
        
        for point in transformation_analysis['turning_points'][:3]:
            report += f"- {point['time'].strftime('%Y-%m')}: {point['previous_stage']} → {point['current_stage']}\n"
    
    if 'error' not in development_model:
        report += f"""
## 三、发展规律模型
- 最佳拟合模型: {development_model['mathematical_model'].get('best_fit_model', '未知')}
- 模型置信度: {development_model['model_confidence']:.3f}

### 未来趋势预测
"""
        
        future_levels = development_model['future_trends']['predicted_levels']
        for i, level in enumerate(future_levels):
            year = datetime.now().year + i + 1
            report += f"- {year}年: {level:.3f}\n"
        
        report += f"""
### 显著影响因素
"""
        
        significant_factors = development_model['environmental_factors'].get('significant_factors', {})
        for factor, correlation in significant_factors.items():
            report += f"- {factor}: 相关系数 {correlation:.3f}\n"
    
    report += f"""
## 四、专业建议

### 意识提升策略
1. 加强经济意识教育，提高阶级利益认识
2. 深化政治理论学习，增强政治判断力
3. 促进社会交往，扩大阶级认同范围
4. 学习历史经验，增强历史使命感
5. 培养革命精神，提升斗争自觉性

### 转化促进措施
"""
    
    if 'error' not in transformation_analysis:
        factors = transformation_analysis.get('transformation_factors', [])
        for factor in factors[:3]:
            direction = "促进" if factor.influence_direction > 0 else "阻碍"
            report += f"- {direction}{factor.factor_name}: 影响强度 {factor.influence_strength:.3f}\n"
    
    return report

# 示例使用
if __name__ == "__main__":
    # 创建分析器
    analyzer = ClassConsciousnessAnalyzer()
    
    # 模拟数据
    individual_data = {
        'economic_survey_score': 0.6,
        'political_survey_score': 0.5,
        'social_survey_score': 0.7,
        'historical_survey_score': 0.4,
        'revolutionary_survey_score': 0.3,
        'economic_interview_score': 0.65,
        'political_interview_score': 0.55,
        'social_interview_score': 0.75,
        'historical_interview_score': 0.45,
        'revolutionary_interview_score': 0.35
    }
    
    # 创建历史数据
    consciousness_history = [
        ConsciousnessDevelopment(
            time_point=datetime(2020, 1, 1),
            overall_level=0.3,
            dimension_scores={
                ConsciousnessDimension.ECONOMIC_CONSCIOUSNESS: 0.4,
                ConsciousnessDimension.POLITICAL_CONSCIOUSNESS: 0.3,
                ConsciousnessDimension.SOCIAL_CONSCIOUSNESS: 0.2,
                ConsciousnessDimension.HISTORICAL_CONSCIOUSNESS: 0.2,
                ConsciousnessDimension.REVOLUTIONARY_CONSCIOUSNESS: 0.1
            },
            transformation_stage=TransformationPhase.SPONTANEOUS_STAGE,
            key_events=['经济危机'],
            external_factors={'economic_crisis': 0.7, 'political_repression': 0.3}
        ),
        ConsciousnessDevelopment(
            time_point=datetime(2022, 1, 1),
            overall_level=0.5,
            dimension_scores={
                ConsciousnessDimension.ECONOMIC_CONSCIOUSNESS: 0.6,
                ConsciousnessDimension.POLITICAL_CONSCIOUSNESS: 0.5,
                ConsciousnessDimension.SOCIAL_CONSCIOUSNESS: 0.4,
                ConsciousnessDimension.HISTORICAL_CONSCIOUSNESS: 0.3,
                ConsciousnessDimension.REVOLUTIONARY_CONSCIOUSNESS: 0.2
            },
            transformation_stage=TransformationPhase.AWARENESS_EMERGING,
            key_events=['罢工运动'],
            external_factors={'economic_crisis': 0.5, 'organizational_development': 0.6}
        )
    ]
    
    social_context = {
        'economic_development': 'industrialization',
        'political_system': 'capitalism',
        'cultural_environment': 'diverse'
    }
    
    # 生成报告
    report = generate_consciousness_analysis_report(analyzer, individual_data, consciousness_history, social_context)
    print(report)
