#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
现代阶级结构新变化分析系统
Modern Class Structure Change Analysis System

专门分析当代社会新阶层、阶级结构复杂化、传统理论与现实对接的专业系统
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union, Set
from dataclasses import dataclass
from enum import Enum
import math
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

class NewClassType(Enum):
    """新兴阶层类型枚举"""
    KNOWLEDGE_WORKER = "知识工作者"  # 知识工作者
    PRECARIAT = "不稳定无产者"  # 不稳定无产者
    DIGITAL_PROLETARIAT = "数字无产阶级"  # 数字无产阶级
    CREATIVE_CLASS = "创意阶层"  # 创意阶层
    SERVICE_INTELLECTUALS = "服务业知识分子"  # 服务业知识分子
    PLATFORM_WORKERS = "平台工作者"  # 平台工作者
    GIG_ECONOMY_WORKERS = "零工经济工作者"  # 零工经济工作者
    TECH_ENTREPRENEURS = "科技创业者"  # 科技创业者

class StructuralChangeType(Enum):
    """结构变化类型枚举"""
    FRAGMENTATION = "碎片化"  # 碎片化
    HIERARCHICAL_COMPLEXIFICATION = "层级复杂化"  # 层级复杂化
    CROSS_CLASS_MOBILITY = "跨阶级流动"  # 跨阶级流动
    IDENTITY_MULTIPLEXITY = "身份多重性"  # 身份多重性
    NETWORK_BASED_STRATIFICATION = "网络化分层"  # 网络化分层

class TheoryRealityGap(Enum):
    """理论与现实差距类型"""
    CONCEPTUAL_GAP = "概念差距"  # 概念差距
    EMPIRICAL_GAP = "实证差距"  # 实证差距
    TEMPORAL_GAP = "时代差距"  # 时代差距
    CULTURAL_GAP = "文化差距"  # 文化差距
    METHODOLOGICAL_GAP = "方法论差距"  # 方法论差距

@dataclass
class NewClassCharacteristics:
    """新阶层特征数据结构"""
    class_type: NewClassType
    size_percentage: float  # 规模占比
    economic_position: float  # 经济地位 (0-1)
    political_influence: float  # 政治影响 (0-1)
    cultural_capital: float  # 文化资本 (0-1)
    social_mobility: float  # 社会流动性 (0-1)
    stability_index: float  # 稳定性指数 (0-1)
    consciousness_level: float  # 意识水平 (0-1)
    key_features: List[str]  # 关键特征
    
    def complexity_score(self) -> float:
        """计算复杂度分数"""
        return np.std([
            self.economic_position,
            self.political_influence,
            self.cultural_capital,
            self.social_mobility,
            self.stability_index
        ])

@dataclass
class StructuralChangeIndicator:
    """结构变化指标"""
    change_type: StructuralChangeType
    magnitude: float  # 变化幅度 (0-1)
    direction: float  # 变化方向 (-1 to 1)
    speed: float  # 变化速度 (0-1)
    persistence: float  # 持续性 (0-1)
    affected_classes: List[str]  # 受影响阶级
    
    def change_impact(self) -> float:
        """计算变化影响"""
        return self.magnitude * abs(self.direction) * self.persistence

@dataclass
class TheoryRealityMismatch:
    """理论与现实不匹配"""
    gap_type: TheoryRealityGap
    traditional_theory: str  # 传统理论观点
    contemporary_reality: str  # 当代现实状况
    gap_magnitude: float  # 差距幅度 (0-1)
    bridging_strategies: List[str]  # 弥合策略
    theoretical_adaptation_needed: bool  # 是否需要理论调适

class ModernClassStructureAnalyzer:
    """现代阶级结构分析器"""
    
    def __init__(self):
        self.identification_thresholds = {
            'size_threshold': 0.05,  # 5%以上才算重要新阶层
            'complexity_threshold': 0.3,  # 复杂度阈值
            'stability_threshold': 0.4,  # 稳定性阈值
            'consciousness_threshold': 0.3  # 意识水平阈值
        }
        
        self.structural_change_weights = {
            StructuralChangeType.FRAGMENTATION: 0.25,
            StructuralChangeType.HIERARCHICAL_COMPLEXIFICATION: 0.2,
            StructuralChangeType.CROSS_CLASS_MOBILITY: 0.2,
            StructuralChangeType.IDENTITY_MULTIPLEXITY: 0.15,
            StructuralChangeType.NETWORK_BASED_STRATIFICATION: 0.2
        }
        
        self.theory_adaptation_framework = {
            'conceptual_refinement': '概念精细化',
            'empirical_validation': '实证验证',
            'theoretical_integration': '理论整合',
            'methodological_innovation': '方法论创新',
            'contextual_adaptation': '语境调适'
        }
    
    def identify_new_social_classes(self, 
                                  economic_data: Dict,
                                  labor_market_data: Dict,
                                  technology_data: Dict,
                                  social_data: Dict) -> List[NewClassCharacteristics]:
        """
        识别新兴社会阶层
        
        Args:
            economic_data: 经济数据
            labor_market_data: 劳动力市场数据
            technology_data: 技术数据
            social_data: 社会数据
            
        Returns:
            新兴阶层列表
        """
        new_classes = []
        
        # 识别知识工作者
        knowledge_workers = self._identify_knowledge_workers(
            economic_data, labor_market_data, technology_data
        )
        if knowledge_workers:
            new_classes.append(knowledge_workers)
        
        # 识别不稳定无产者
        precariat = self._identify_precariat(
            labor_market_data, economic_data, social_data
        )
        if precariat:
            new_classes.append(precariat)
        
        # 识别数字无产阶级
        digital_proletariat = self._identify_digital_proletariat(
            technology_data, labor_market_data, economic_data
        )
        if digital_proletariat:
            new_classes.append(digital_proletariat)
        
        # 识别创意阶层
        creative_class = self._identify_creative_class(
            economic_data, social_data, technology_data
        )
        if creative_class:
            new_classes.append(creative_class)
        
        # 识别平台工作者
        platform_workers = self._identify_platform_workers(
            technology_data, labor_market_data, economic_data
        )
        if platform_workers:
            new_classes.append(platform_workers)
        
        # 识别科技创业者
        tech_entrepreneurs = self._identify_tech_entrepreneurs(
            technology_data, economic_data, social_data
        )
        if tech_entrepreneurs:
            new_classes.append(tech_entrepreneurs)
        
        # 按规模排序
        new_classes.sort(key=lambda x: x.size_percentage, reverse=True)
        return new_classes
    
    def _identify_knowledge_workers(self, 
                                  economic_data: Dict,
                                  labor_market_data: Dict,
                                  technology_data: Dict) -> Optional[NewClassCharacteristics]:
        """识别知识工作者"""
        # 计算知识经济指标
        knowledge_economy_ratio = economic_data.get('knowledge_economy_percentage', 0)
        higher_education_rate = labor_market_data.get('higher_education_rate', 0)
        tech_employment_rate = technology_data.get('tech_employment_rate', 0)
        
        # 综合评估
        knowledge_score = (knowledge_economy_ratio + higher_education_rate + tech_employment_rate) / 3
        
        if knowledge_score >= self.identification_thresholds['size_threshold']:
            return NewClassCharacteristics(
                class_type=NewClassType.KNOWLEDGE_WORKER,
                size_percentage=knowledge_score,
                economic_position=0.6,  # 中上经济地位
                political_influence=0.5,  # 中等政治影响
                cultural_capital=0.8,  # 高文化资本
                social_mobility=0.7,  # 高社会流动性
                stability_index=0.7,  # 相对稳定
                consciousness_level=0.4,  # 中等意识水平
                key_features=[
                    '高技能知识劳动',
                    '信息生产与处理',
                    '相对自主性',
                    '中等收入水平',
                    '专业身份认同'
                ]
            )
        return None
    
    def _identify_precariat(self, 
                          labor_market_data: Dict,
                          economic_data: Dict,
                          social_data: Dict) -> Optional[NewClassCharacteristics]:
        """识别不稳定无产者"""
        # 计算不稳定指标
        temporary_work_rate = labor_market_data.get('temporary_work_percentage', 0)
        gig_economy_rate = labor_market_data.get('gig_economy_percentage', 0)
        unemployment_volatility = economic_data.get('unemployment_volatility', 0)
        social_insecurity = social_data.get('social_insecurity_index', 0)
        
        precariat_score = (temporary_work_rate + gig_economy_rate + 
                          unemployment_volatility + social_insecurity) / 4
        
        if precariat_score >= self.identification_thresholds['size_threshold']:
            return NewClassCharacteristics(
                class_type=NewClassType.PRECARITY,
                size_percentage=precariat_score,
                economic_position=0.3,  # 中下经济地位
                political_influence=0.2,  # 低政治影响
                cultural_capital=0.4,  # 中低文化资本
                social_mobility=0.3,  # 低社会流动性
                stability_index=0.2,  # 极不稳定
                consciousness_level=0.3,  # 低意识水平
                key_features=[
                    '工作不稳定性',
                    '缺乏社会保障',
                    '收入波动性大',
                    '阶级意识模糊',
                    '多重身份困扰'
                ]
            )
        return None
    
    def _identify_digital_proletariat(self, 
                                    technology_data: Dict,
                                    labor_market_data: Dict,
                                    economic_data: Dict) -> Optional[NewClassCharacteristics]:
        """识别数字无产阶级"""
        # 计算数字化指标
        digital_labor_rate = technology_data.get('digital_labor_percentage', 0)
        platform_dependency = technology_data.get('platform_dependency_rate', 0)
        algorithmic_control = technology_data.get('algorithmic_control_level', 0)
        digital_exploitation = economic_data.get('digital_exploitation_rate', 0)
        
        digital_score = (digital_labor_rate + platform_dependency + 
                        algorithmic_control + digital_exploitation) / 4
        
        if digital_score >= self.identification_thresholds['size_threshold']:
            return NewClassCharacteristics(
                class_type=NewClassType.DIGITAL_PROLETARIAT,
                size_percentage=digital_score,
                economic_position=0.35,  # 中下经济地位
                political_influence=0.15,  # 极低政治影响
                cultural_capital=0.5,  # 中等文化资本
                social_mobility=0.4,  # 中低社会流动性
                stability_index=0.3,  # 不稳定
                consciousness_level=0.25,  # 低意识水平
                key_features=[
                    '数字平台依赖',
                    '算法控制',
                    '数据剥削',
                    '虚拟身份',
                    '全球竞争'
                ]
            )
        return None
    
    def _identify_creative_class(self, 
                               economic_data: Dict,
                               social_data: Dict,
                               technology_data: Dict) -> Optional[NewClassCharacteristics]:
        """识别创意阶层"""
        # 计算创意经济指标
        creative_economy_ratio = economic_data.get('creative_economy_percentage', 0)
        cultural_production = social_data.get('cultural_production_index', 0)
        digital_creativity = technology_data.get('digital_creativity_rate', 0)
        
        creative_score = (creative_economy_ratio + cultural_production + digital_creativity) / 3
        
        if creative_score >= self.identification_thresholds['size_threshold']:
            return NewClassCharacteristics(
                class_type=NewClassType.CREATIVE_CLASS,
                size_percentage=creative_score,
                economic_position=0.55,  # 中上经济地位
                political_influence=0.4,  # 中等政治影响
                cultural_capital=0.9,  # 极高文化资本
                social_mobility=0.6,  # 中高社会流动性
                stability_index=0.5,  # 中等稳定性
                consciousness_level=0.5,  # 中等意识水平
                key_features=[
                    '文化创意生产',
                    '符号资本积累',
                    '个性化表达',
                    '网络化协作',
                    '审美劳动'
                ]
            )
        return None
    
    def _identify_platform_workers(self, 
                                 technology_data: Dict,
                                 labor_market_data: Dict,
                                 economic_data: Dict) -> Optional[NewClassCharacteristics]:
        """识别平台工作者"""
        # 计算平台经济指标
        platform_participation = technology_data.get('platform_participation_rate', 0)
        platform_income_dependency = economic_data.get('platform_income_dependency', 0)
        platform_work_conditions = labor_market_data.get('platform_work_conditions', 0)
        
        platform_score = (platform_participation + platform_income_dependency + 
                         platform_work_conditions) / 3
        
        if platform_score >= self.identification_thresholds['size_threshold']:
            return NewClassCharacteristics(
                class_type=NewClassType.PLATFORM_WORKERS,
                size_percentage=platform_score,
                economic_position=0.4,  # 中等经济地位
                political_influence=0.25,  # 低政治影响
                cultural_capital=0.45,  # 中低文化资本
                social_mobility=0.35,  # 低社会流动性
                stability_index=0.25,  # 不稳定
                consciousness_level=0.3,  # 低意识水平
                key_features=[
                    '平台中介就业',
                    '算法管理',
                    '灵活工作时间',
                    '收入不确定性',
                    '原子化状态'
                ]
            )
        return None
    
    def _identify_tech_entrepreneurs(self, 
                                   technology_data: Dict,
                                   economic_data: Dict,
                                   social_data: Dict) -> Optional[NewClassCharacteristics]:
        """识别科技创业者"""
        # 计算科技创业指标
        startup_rate = technology_data.get('startup_rate', 0)
        venture_investment = economic_data.get('venture_investment_level', 0)
        innovation_index = social_data.get('innovation_index', 0)
        
        entrepreneur_score = (startup_rate + venture_investment + innovation_index) / 3
        
        if entrepreneur_score >= self.identification_thresholds['size_threshold'] * 0.5:  # 降低阈值，因为这是精英群体
            return NewClassCharacteristics(
                class_type=NewClassType.TECH_ENTREPRENEURS,
                size_percentage=entrepreneur_score,
                economic_position=0.85,  # 高经济地位
                political_influence=0.7,  # 高政治影响
                cultural_capital=0.75,  # 高文化资本
                social_mobility=0.8,  # 高社会流动性
                stability_index=0.4,  # 中等稳定性（高风险）
                consciousness_level=0.6,  # 中高意识水平
                key_features=[
                    '技术创新驱动',
                    '风险投资依赖',
                    '高回报高风险',
                    '网络化资源',
                    '变革导向'
                ]
            )
        return None
    
    def analyze_structural_complexity(self, 
                                    traditional_classes: Dict,
                                    new_classes: List[NewClassCharacteristics],
                                    mobility_data: Dict) -> Dict:
        """
        分析阶级结构复杂化
        
        Args:
            traditional_classes: 传统阶级数据
            new_classes: 新兴阶层数据
            mobility_data: 流动性数据
            
        Returns:
            结构复杂化分析结果
        """
        # 计算碎片化程度
        fragmentation_score = self._calculate_fragmentation(traditional_classes, new_classes)
        
        # 计算层级复杂化
        hierarchical_complexity = self._calculate_hierarchical_complexity(
            traditional_classes, new_classes
        )
        
        # 计算跨阶级流动性
        cross_class_mobility = self._calculate_cross_class_mobility(mobility_data)
        
        # 计算身份多重性
        identity_multiplexity = self._calculate_identity_multiplexity(new_classes)
        
        # 计算网络化分层
        network_stratification = self._calculate_network_stratification(new_classes)
        
        # 综合复杂度指数
        overall_complexity = (
            fragmentation_score * self.structural_change_weights[StructuralChangeType.FRAGMENTATION] +
            hierarchical_complexity * self.structural_change_weights[StructuralChangeType.HIERARCHICAL_COMPLEXIFICATION] +
            cross_class_mobility * self.structural_change_weights[StructuralChangeType.CROSS_CLASS_MOBILITY] +
            identity_multiplexity * self.structural_change_weights[StructuralChangeType.IDENTITY_MULTIPLEXITY] +
            network_stratification * self.structural_change_weights[StructuralChangeType.NETWORK_BASED_STRATIFICATION]
        )
        
        return {
            'overall_complexity_index': overall_complexity,
            'fragmentation_score': fragmentation_score,
            'hierarchical_complexity': hierarchical_complexity,
            'cross_class_mobility': cross_class_mobility,
            'identity_multiplexity': identity_multiplexity,
            'network_stratification': network_stratification,
            'complexity_level': self._classify_complexity_level(overall_complexity),
            'dominant_change_types': self._identify_dominant_changes({
                'fragmentation': fragmentation_score,
                'hierarchical': hierarchical_complexity,
                'mobility': cross_class_mobility,
                'identity': identity_multiplexity,
                'network': network_stratification
            })
        }
    
    def _calculate_fragmentation(self, 
                               traditional_classes: Dict,
                               new_classes: List[NewClassCharacteristics]) -> float:
        """计算碎片化程度"""
        total_classes = len(traditional_classes) + len(new_classes)
        if total_classes <= 1:
            return 0.0
        
        # 计算各类别规模分布的熵
        all_sizes = list(traditional_classes.values()) + [nc.size_percentage for nc in new_classes]
        total_size = sum(all_sizes)
        
        if total_size == 0:
            return 0.0
        
        proportions = [size / total_size for size in all_sizes if size > 0]
        entropy = -sum(p * np.log2(p) for p in proportions if p > 0)
        max_entropy = np.log2(len(proportions))
        
        return entropy / max_entropy if max_entropy > 0 else 0.0
    
    def _calculate_hierarchical_complexity(self, 
                                         traditional_classes: Dict,
                                         new_classes: List[NewClassCharacteristics]) -> float:
        """计算层级复杂化"""
        # 计算经济地位的层级数
        all_positions = [0.5] * len(traditional_classes)  # 假设传统阶级中等地位
        all_positions.extend([nc.economic_position for nc in new_classes])
        
        if len(all_positions) <= 1:
            return 0.0
        
        # 使用标准差作为复杂度指标
        position_std = np.std(all_positions)
        return min(1.0, position_std * 2)  # 标准化到0-1
    
    def _calculate_cross_class_mobility(self, mobility_data: Dict) -> float:
        """计算跨阶级流动性"""
        upward_mobility = mobility_data.get('upward_mobility_rate', 0)
        downward_mobility = mobility_data.get('downward_mobility_rate', 0)
        lateral_mobility = mobility_data.get('lateral_mobility_rate', 0)
        
        total_mobility = upward_mobility + downward_mobility + lateral_mobility
        return min(1.0, total_mobility)
    
    def _calculate_identity_multiplexity(self, new_classes: List[NewClassCharacteristics]) -> float:
        """计算身份多重性"""
        if not new_classes:
            return 0.0
        
        # 基于新阶层的复杂度分数计算身份多重性
        complexity_scores = [nc.complexity_score() for nc in new_classes]
        return np.mean(complexity_scores)
    
    def _calculate_network_stratification(self, new_classes: List[NewClassCharacteristics]) -> float:
        """计算网络化分层"""
        if not new_classes:
            return 0.0
        
        # 基于技术依赖和网络化程度计算
        network_scores = []
        for nc in new_classes:
            if '网络' in ' '.join(nc.key_features) or '平台' in ' '.join(nc.key_features):
                network_scores.append(0.8)
            elif '数字' in ' '.join(nc.key_features) or '虚拟' in ' '.join(nc.key_features):
                network_scores.append(0.6)
            else:
                network_scores.append(0.3)
        
        return np.mean(network_scores)
    
    def _classify_complexity_level(self, complexity_score: float) -> str:
        """分类复杂度水平"""
        if complexity_score < 0.3:
            return "低复杂度"
        elif complexity_score < 0.6:
            return "中等复杂度"
        else:
            return "高复杂度"
    
    def _identify_dominant_changes(self, change_scores: Dict) -> List[str]:
        """识别主导变化类型"""
        sorted_changes = sorted(change_scores.items(), key=lambda x: x[1], reverse=True)
        dominant = []
        
        for change_type, score in sorted_changes:
            if score > 0.5:  # 阈值
                type_names = {
                    'fragmentation': '碎片化',
                    'hierarchical': '层级复杂化',
                    'mobility': '跨阶级流动',
                    'identity': '身份多重性',
                    'network': '网络化分层'
                }
                dominant.append(type_names.get(change_type, change_type))
        
        return dominant
    
    def bridge_theory_reality_gap(self, 
                                traditional_theory: Dict,
                                contemporary_reality: Dict,
                                new_classes: List[NewClassCharacteristics]) -> List[TheoryRealityMismatch]:
        """
        弥合理论与现实差距
        
        Args:
            traditional_theory: 传统理论观点
            contemporary_reality: 当代现实状况
            new_classes: 新兴阶层
            
        Returns:
            理论现实不匹配列表
        """
        mismatches = []
        
        # 概念差距
        concept_gap = self._analyze_conceptual_gap(traditional_theory, new_classes)
        if concept_gap:
            mismatches.append(concept_gap)
        
        # 实证差距
        empirical_gap = self._analyze_empirical_gap(traditional_theory, contemporary_reality)
        if empirical_gap:
            mismatches.append(empirical_gap)
        
        # 时代差距
        temporal_gap = self._analyze_temporal_gap(traditional_theory, contemporary_reality)
        if temporal_gap:
            mismatches.append(temporal_gap)
        
        # 文化差距
        cultural_gap = self._analyze_cultural_gap(traditional_theory, contemporary_reality)
        if cultural_gap:
            mismatches.append(cultural_gap)
        
        # 方法论差距
        methodological_gap = self._analyze_methodological_gap(traditional_theory, new_classes)
        if methodological_gap:
            mismatches.append(methodological_gap)
        
        return mismatches
    
    def _analyze_conceptual_gap(self, 
                              traditional_theory: Dict,
                              new_classes: List[NewClassCharacteristics]) -> Optional[TheoryRealityMismatch]:
        """分析概念差距"""
        traditional_concepts = traditional_theory.get('class_concepts', [])
        new_class_types = [nc.class_type.value for nc in new_classes]
        
        # 检查新阶层是否在传统概念中
        uncovered_concepts = []
        for class_type in new_class_types:
            if not any(concept in class_type for concept in traditional_concepts):
                uncovered_concepts.append(class_type)
        
        if uncovered_concepts:
            gap_magnitude = len(uncovered_concepts) / len(new_class_types)
            return TheoryRealityMismatch(
                gap_type=TheoryRealityGap.CONCEPTUAL_GAP,
                traditional_theory="基于工业社会的阶级概念体系",
                contemporary_reality=f"出现{', '.join(uncovered_concepts)}等新阶层",
                gap_magnitude=gap_magnitude,
                bridging_strategies=[
                    "扩展阶级概念内涵",
                    "建立新阶层分类框架",
                    "发展跨学科概念工具"
                ],
                theoretical_adaptation_needed=True
            )
        return None
    
    def _analyze_empirical_gap(self, 
                             traditional_theory: Dict,
                             contemporary_reality: Dict) -> Optional[TheoryRealityMismatch]:
        """分析实证差距"""
        predicted_structure = traditional_theory.get('predicted_class_structure', {})
        actual_structure = contemporary_reality.get('actual_class_structure', {})
        
        # 计算结构差异
        structure_diff = 0.0
        for class_name in set(predicted_structure.keys()) | set(actual_structure.keys()):
            predicted = predicted_structure.get(class_name, 0)
            actual = actual_structure.get(class_name, 0)
            structure_diff += abs(predicted - actual)
        
        if structure_diff > 0.3:  # 阈值
            return TheoryRealityMismatch(
                gap_type=TheoryRealityGap.EMPIRICAL_GAP,
                traditional_theory=f"预测结构: {predicted_structure}",
                contemporary_reality=f"实际结构: {actual_structure}",
                gap_magnitude=min(1.0, structure_diff),
                bridging_strategies=[
                    "更新实证调查方法",
                    "建立新数据收集体系",
                    "发展动态监测机制"
                ],
                theoretical_adaptation_needed=True
            )
        return None
    
    def _analyze_temporal_gap(self, 
                            traditional_theory: Dict,
                            contemporary_reality: Dict) -> Optional[TheoryRealityMismatch]:
        """分析时代差距"""
        theory_context = traditional_theory.get('historical_context', '工业时代')
        current_context = contemporary_reality.get('current_context', '数字时代')
        
        if theory_context != current_context:
            return TheoryRealityMismatch(
                gap_type=TheoryRealityGap.TEMPORAL_GAP,
                traditional_theory=f"基于{theory_context}的理论框架",
                contemporary_reality=f"面临{current_context}的现实挑战",
                gap_magnitude=0.7,  # 时代差距通常较大
                bridging_strategies=[
                    "发展时代适应性理论",
                    "建立历史比较框架",
                    "创新理论发展范式"
                ],
                theoretical_adaptation_needed=True
            )
        return None
    
    def _analyze_cultural_gap(self, 
                            traditional_theory: Dict,
                            contemporary_reality: Dict) -> Optional[TheoryRealityMismatch]:
        """分析文化差距"""
        traditional_culture = traditional_theory.get('cultural_assumptions', [])
        current_culture = contemporary_reality.get('cultural_realities', [])
        
        cultural_differences = set(traditional_culture) ^ set(current_culture)
        
        if len(cultural_differences) > 2:
            return TheoryRealityMismatch(
                gap_type=TheoryRealityGap.CULTURAL_GAP,
                traditional_theory=f"文化假设: {traditional_culture}",
                contemporary_reality=f"文化现实: {current_culture}",
                gap_magnitude=len(cultural_differences) / max(len(traditional_culture), len(current_culture)),
                bridging_strategies=[
                    "加强文化敏感性分析",
                    "发展跨文化理论框架",
                    "重视本土化研究"
                ],
                theoretical_adaptation_needed=True
            )
        return None
    
    def _analyze_methodological_gap(self, 
                                  traditional_theory: Dict,
                                  new_classes: List[NewClassCharacteristics]) -> Optional[TheoryRealityMismatch]:
        """分析方法论差距"""
        traditional_methods = traditional_theory.get('research_methods', [])
        required_methods = []
        
        for nc in new_classes:
            if '网络' in ' '.join(nc.key_features):
                required_methods.append('网络分析')
            if '数字' in ' '.join(nc.key_features):
                required_methods.append('数字追踪')
            if '平台' in ' '.join(nc.key_features):
                required_methods.append('平台数据分析')
        
        missing_methods = set(required_methods) - set(traditional_methods)
        
        if missing_methods:
            return TheoryRealityMismatch(
                gap_type=TheoryRealityGap.METHODOLOGICAL_GAP,
                traditional_theory=f"传统方法: {traditional_methods}",
                contemporary_reality=f"需要方法: {list(missing_methods)}",
                gap_magnitude=len(missing_methods) / max(len(traditional_methods), 1),
                bridging_strategies=[
                    "发展数字研究方法",
                    "整合多学科方法",
                    "创新分析技术工具"
                ],
                theoretical_adaptation_needed=True
            )
        return None
    
    def generate_theoretical_adaptation_proposals(self, 
                                                 mismatches: List[TheoryRealityMismatch]) -> Dict:
        """
        生成理论调适方案
        
        Args:
            mismatches: 理论现实不匹配列表
            
        Returns:
            理论调适方案
        """
        adaptation_proposals = {
            'conceptual_refinements': [],
            'methodological_innovations': [],
            'theoretical_integrations': [],
            'empirical_updates': [],
            'contextual_adaptations': []
        }
        
        for mismatch in mismatches:
            if mismatch.gap_type == TheoryRealityGap.CONCEPTUAL_GAP:
                adaptation_proposals['conceptual_refinements'].extend(mismatch.bridging_strategies)
            elif mismatch.gap_type == TheoryRealityGap.METHODOLOGICAL_GAP:
                adaptation_proposals['methodological_innovations'].extend(mismatch.bridging_strategies)
            elif mismatch.gap_type == TheoryRealityGap.EMPIRICAL_GAP:
                adaptation_proposals['empirical_updates'].extend(mismatch.bridging_strategies)
            elif mismatch.gap_type == TheoryRealityGap.TEMPORAL_GAP:
                adaptation_proposals['theoretical_integrations'].extend(mismatch.bridging_strategies)
            elif mismatch.gap_type == TheoryRealityGap.CULTURAL_GAP:
                adaptation_proposals['contextual_adaptations'].extend(mismatch.bridging_strategies)
        
        # 去重
        for key in adaptation_proposals:
            adaptation_proposals[key] = list(set(adaptation_proposals[key]))
        
        # 评估调适紧迫性
        total_gap_magnitude = sum(m.gap_magnitude for m in mismatches)
        urgency_level = '高' if total_gap_magnitude > 2.0 else '中' if total_gap_magnitude > 1.0 else '低'
        
        adaptation_proposals['urgency_level'] = urgency_level
        adaptation_proposals['total_gap_magnitude'] = total_gap_magnitude
        adaptation_proposals['adaptation_priority'] = self._calculate_adaptation_priority(mismatches)
        
        return adaptation_proposals
    
    def _calculate_adaptation_priority(self, mismatches: List[TheoryRealityMismatch]) -> List[str]:
        """计算调适优先级"""
        # 按差距大小排序
        sorted_mismatches = sorted(mismatches, key=lambda m: m.gap_magnitude, reverse=True)
        
        priority_mapping = {
            TheoryRealityGap.CONCEPTUAL_GAP: '概念更新',
            TheoryRealityGap.METHODOLOGICAL_GAP: '方法创新',
            TheoryRealityGap.EMPIRICAL_GAP: '实证更新',
            TheoryRealityGap.TEMPORAL_GAP: '理论整合',
            TheoryRealityGap.CULTURAL_GAP: '语境调适'
        }
        
        priorities = []
        for mismatch in sorted_mismatches:
            priority_name = priority_mapping.get(mismatch.gap_type, str(mismatch.gap_type))
            priorities.append(f"{priority_name} (紧迫度: {mismatch.gap_magnitude:.2f})")
        
        return priorities

def generate_modern_structure_analysis_report(analyzer: ModernClassStructureAnalyzer,
                                            economic_data: Dict,
                                            labor_market_data: Dict,
                                            technology_data: Dict,
                                            social_data: Dict,
                                            traditional_theory: Dict,
                                            contemporary_reality: Dict) -> str:
    """
    生成现代阶级结构分析报告
    
    Args:
        analyzer: 分析器实例
        economic_data: 经济数据
        labor_market_data: 劳动力市场数据
        technology_data: 技术数据
        social_data: 社会数据
        traditional_theory: 传统理论
        contemporary_reality: 当代现实
        
    Returns:
        分析报告
    """
    # 识别新兴阶层
    new_classes = analyzer.identify_new_social_classes(
        economic_data, labor_market_data, technology_data, social_data
    )
    
    # 分析结构复杂化
    traditional_classes = {'资产阶级': 0.1, '无产阶级': 0.6, '小资产阶级': 0.3}
    mobility_data = {
        'upward_mobility_rate': 0.15,
        'downward_mobility_rate': 0.1,
        'lateral_mobility_rate': 0.2
    }
    
    complexity_analysis = analyzer.analyze_structural_complexity(
        traditional_classes, new_classes, mobility_data
    )
    
    # 分析理论与现实差距
    theory_reality_gaps = analyzer.bridge_theory_reality_gap(
        traditional_theory, contemporary_reality, new_classes
    )
    
    # 生成理论调适方案
    adaptation_proposals = analyzer.generate_theoretical_adaptation_proposals(theory_reality_gaps)
    
    # 生成报告
    report = f"""
# 现代阶级结构新变化分析报告

## 一、新兴社会阶层识别
"""
    
    for new_class in new_classes:
        report += f"""
### {new_class.class_type.value}
- 规模占比: {new_class.size_percentage:.1%}
- 经济地位: {new_class.economic_position:.2f}
- 政治影响: {new_class.political_influence:.2f}
- 文化资本: {new_class.cultural_capital:.2f}
- 社会流动性: {new_class.social_mobility:.2f}
- 稳定性指数: {new_class.stability_index:.2f}
- 意识水平: {new_class.consciousness_level:.2f}
- 关键特征: {', '.join(new_class.key_features)}
"""
    
    report += f"""
## 二、阶级结构复杂化分析
- 整体复杂度指数: {complexity_analysis['overall_complexity_index']:.3f}
- 复杂度水平: {complexity_analysis['complexity_level']}

### 各维度变化
- 碎片化程度: {complexity_analysis['fragmentation_score']:.3f}
- 层级复杂化: {complexity_analysis['hierarchical_complexity']:.3f}
- 跨阶级流动: {complexity_analysis['cross_class_mobility']:.3f}
- 身份多重性: {complexity_analysis['identity_multiplexity']:.3f}
- 网络化分层: {complexity_analysis['network_stratification']:.3f}

### 主导变化类型
{', '.join(complexity_analysis['dominant_change_types']) if complexity_analysis['dominant_change_types'] else '无明显主导类型'}

## 三、理论与现实差距分析
"""
    
    for gap in theory_reality_gaps:
        report += f"""
### {gap.gap_type.value}
- 传统理论: {gap.traditional_theory}
- 当代现实: {gap.contemporary_reality}
- 差距幅度: {gap.gap_magnitude:.3f}
- 弥合策略: {', '.join(gap.bridging_strategies)}
- 需要理论调适: {'是' if gap.theoretical_adaptation_needed else '否'}
"""
    
    report += f"""
## 四、理论调适方案
- 调适紧迫性: {adaptation_proposals['urgency_level']}
- 总体差距: {adaptation_proposals['total_gap_magnitude']:.3f}

### 调适优先级
"""
    
    for priority in adaptation_proposals['adaptation_priority']:
        report += f"- {priority}\n"
    
    report += f"""
### 具体调适措施

#### 概念精细化
"""
    
    for refinement in adaptation_proposals['conceptual_refinements']:
        report += f"- {refinement}\n"
    
    report += f"""
#### 方法论创新
"""
    
    for innovation in adaptation_proposals['methodological_innovations']:
        report += f"- {innovation}\n"
    
    report += f"""
#### 理论整合
"""
    
    for integration in adaptation_proposals['theoretical_integrations']:
        report += f"- {integration}\n"
    
    report += f"""
## 五、专业建议

### 理论发展建议
1. 建立开放性理论框架，适应持续的社会变革
2. 发展跨学科研究方法，整合多视角分析
3. 重视本土化研究，反映具体社会现实
4. 建立动态监测机制，及时捕捉结构变化

### 政策制定建议
1. 针对新阶层的特殊需求制定差异化政策
2. 建立灵活的社会保障体系，适应就业形态变化
3. 促进教育体系改革，提升新阶层技能水平
4. 加强社会组织建设，促进新阶层有序参与

### 研究方向建议
1. 深化新阶层意识和行为模式研究
2. 探索数字技术对阶级关系的深层影响
3. 分析全球化背景下的阶级结构变迁
4. 发展适合当代社会的阶级分析工具
"""
    
    return report

# 示例使用
if __name__ == "__main__":
    # 创建分析器
    analyzer = ModernClassStructureAnalyzer()
    
    # 模拟数据
    economic_data = {
        'knowledge_economy_percentage': 0.25,
        'creative_economy_percentage': 0.15,
        'digital_exploitation_rate': 0.3,
        'platform_income_dependency': 0.2,
        'venture_investment_level': 0.08,
        'unemployment_volatility': 0.15
    }
    
    labor_market_data = {
        'higher_education_rate': 0.4,
        'temporary_work_percentage': 0.2,
        'gig_economy_percentage': 0.15,
        'tech_employment_rate': 0.12,
        'platform_work_conditions': 0.18
    }
    
    technology_data = {
        'tech_employment_rate': 0.12,
        'digital_labor_percentage': 0.3,
        'platform_dependency_rate': 0.25,
        'algorithmic_control_level': 0.35,
        'digital_creativity_rate': 0.2,
        'startup_rate': 0.05,
        'platform_participation_rate': 0.22
    }
    
    social_data = {
        'social_insecurity_index': 0.25,
        'cultural_production_index': 0.3,
        'innovation_index': 0.4
    }
    
    traditional_theory = {
        'class_concepts': ['资产阶级', '无产阶级', '小资产阶级'],
        'predicted_class_structure': {'资产阶级': 0.15, '无产阶级': 0.7, '小资产阶级': 0.15},
        'historical_context': '工业时代',
        'cultural_assumptions': ['阶级对立', '生产资料决定', '集体意识'],
        'research_methods': ['问卷调查', '统计分析', '历史文献']
    }
    
    contemporary_reality = {
        'actual_class_structure': {'资产阶级': 0.08, '无产阶级': 0.45, '小资产阶级': 0.2, '新阶层': 0.27},
        'current_context': '数字时代',
        'cultural_realities': ['身份多元', '网络认同', '个体化']
    }
    
    # 生成报告
    report = generate_modern_structure_analysis_report(
        analyzer, economic_data, labor_market_data, technology_data, 
        social_data, traditional_theory, contemporary_reality
    )
    print(report)