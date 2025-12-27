#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
马克思主义理论准确性验证器 - 基于经典文献和权威标准的严格验证
确保算法与准确的理论标准对齐，避免常见的理论错误
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import re
from dataclasses import dataclass
from enum import Enum


class TheoryAccuracyLevel(Enum):
    """理论准确性等级"""
    EXCELLENT = "优秀"
    GOOD = "良好"
    AVERAGE = "一般"
    POOR = "不足"
    SERIOUS_ERROR = "严重错误"


@dataclass
class TheoryError:
    """理论错误"""
    error_type: str
    description: str
    severity: str
    correction: str
    reference: str


class MarxistTheoryValidator:
    """马克思主义理论准确性验证器"""
    
    def __init__(self):
        # 经典理论定义库
        self.classic_definitions = self._load_classic_definitions()
        
        # 常见错误模式库
        self.common_errors = self._load_common_errors()
        
        # 理论准确性标准
        self.accuracy_standards = self._load_accuracy_standards()
        
        # 验证历史
        self.validation_history = []
    
    def _load_classic_definitions(self) -> Dict:
        """加载经典理论定义"""
        return {
            # 生产力定义
            'productive_forces': {
                'classic_definition': '生产力是人类改造自然的能力，包括劳动者、劳动资料、劳动对象三个基本要素',
                'essential_elements': ['劳动者', '劳动资料', '劳动对象'],
                'not_equivalent_to': ['技术', '经济水平', 'GDP', '发展水平'],
                'key_characteristics': ['社会性', '历史性', '客观性'],
                'classical_source': '《资本论》第一卷'
            },
            
            # 生产关系定义
            'relations_of_production': {
                'classic_definition': '生产关系是人们在物质生产过程中结成的社会关系，是生产的社会形式',
                'essential_elements': ['生产资料所有制形式', '人们在生产中的地位', '产品分配方式'],
                'not_equivalent_to': ['收入分配', '贫富差距', '经济关系'],
                'key_characteristics': ['物质性', '社会性', '历史性'],
                'classical_source': '《德意志意识形态》'
            },
            
            # 矛盾定义
            'contradiction': {
                'classic_definition': '矛盾是指事物内部包含的既对立又统一的关系，是事物发展的根本动力',
                'essential_elements': ['对立性', '统一性', '相互依存', '相互转化'],
                'not_equivalent_to': ['冲突', '斗争', '分歧', '差异'],
                'key_characteristics': ['普遍性', '客观性', '发展性'],
                'classical_source': '《矛盾论》'
            },
            
            # 辩证法定义
            'dialectics': {
                'classic_definition': '辩证法是关于自然、社会和思维发展的普遍规律的科学，是认识世界和改造世界的根本方法',
                'essential_elements': ['对立统一规律', '量变质变规律', '否定之否定规律'],
                'not_equivalent_to': ['变化规律', '发展规律', '进化论'],
                'key_characteristics': ['科学性', '革命性', '实践性'],
                'classical_source': '《反杜林论》'
            },
            
            # 阶级定义
            'class': {
                'classic_definition': '阶级是在生产资料占有关系中处于不同地位的社会集团',
                'essential_elements': ['生产资料占有关系', '社会地位', '根本利益'],
                'not_equivalent_to': ['收入群体', '贫富群体', '职业群体'],
                'key_characteristics': ['历史性', '对抗性', '集团性'],
                'classical_source': '《共产党宣言》'
            },
            
            # 经济基础定义
            'economic_base': {
                'classic_definition': '经济基础是社会发展一定阶段上的生产关系的总和',
                'essential_elements': ['生产关系总和', '社会形式', '制度基础'],
                'not_equivalent_to': ['经济水平', 'GDP', '经济实力'],
                'key_characteristics': ['基础性', '决定性', '社会性'],
                'classical_source': '《政治经济学批判》序言'
            },
            
            # 上层建筑定义
            'superstructure': {
                'classic_definition': '上层建筑是建立在经济基础之上的意识形态、政治法律制度及设施',
                'essential_elements': ['政治制度', '法律制度', '意识形态', '文化设施'],
                'not_equivalent_to': ['政治制度', '法律体系', '文化'],
                'key_characteristics': ['相对独立性', '反作用性', '社会性'],
                'classical_source': '《政治经济学批判》序言'
            }
        }
    
    def _load_common_errors(self) -> Dict:
        """加载常见错误模式"""
        return {
            'concept_confusion': {
                '生产力_vs_技术': {
                    'error': '将生产力等同于技术发展',
                    'correction': '生产力包括劳动者、劳动资料、劳动对象三要素，技术只是劳动资料的组成部分',
                    'severity': 'high'
                },
                '经济_base_vs_economy': {
                    'error': '将经济基础等同于经济发展水平',
                    'correction': '经济基础是生产关系的总和，不等于经济发展水平或GDP',
                    'severity': 'high'
                },
                'class_vs_income': {
                    'error': '按收入水平划分阶级',
                    'correction': '阶级划分依据是生产资料占有关系，而非收入水平',
                    'severity': 'high'
                },
                'contradiction_vs_conflict': {
                    'error': '将矛盾等同于简单的冲突',
                    'correction': '矛盾是对立统一的关系，既对立又统一，比冲突更深刻',
                    'severity': 'high'
                }
            },
            
            'principle_simplification': {
                'determinism': {
                    'error': '绝对化的生产力决定论或经济基础决定论',
                    'correction': '生产力决定生产关系，但生产关系对生产力有反作用；经济基础决定上层建筑，但上层建筑有相对独立性',
                    'severity': 'high'
                },
                'class_struggle': {
                    'error': '将阶级斗争简单化为暴力冲突',
                    'correction': '阶级斗争是根本利益的对立，有多种形式',
                    'severity': 'medium'
                }
            },
            
            'methodology_errors': {
                'mechanical_materialism': {
                    'error': '用机械的、形而上学的观点看问题',
                    'correction': '必须用辩证的、发展的观点看问题',
                    'severity': 'high'
                },
                'dogmatism': {
                    'error': '机械套用理论概念和公式',
                    'correction': '必须理论联系实际，具体问题具体分析',
                    'severity': 'medium'
                },
                'empiricism': {
                    'error': '满足于表面现象，忽视本质分析',
                    'correction': '必须透过现象看本质，揭示内在规律',
                    'severity': 'medium'
                }
            }
        }
    
    def _load_accuracy_standards(self) -> Dict:
        """加载理论准确性标准"""
        return {
            'concept_accuracy': {
                'excellent': 9.0,
                'good': 7.5,
                'average': 6.0,
                'poor': 4.0,
                'serious_error': 0.0
            },
            'principle_application': {
                'excellent': 9.0,
                'good': 7.5,
                'average': 6.0,
                'poor': 4.0,
                'serious_error': 0.0
            },
            'methodology_soundness': {
                'excellent': 9.0,
                'good': 7.5,
                'average': 6.0,
                'poor': 4.0,
                'serious_error': 0.0
            },
            'analytical_depth': {
                'excellent': 9.0,
                'good': 7.5,
                'average': 6.0,
                'poor': 4.0,
                'serious_error': 0.0
            }
        }
    
    def validate_concept_accuracy(self, text_data: str, analysis_result: Dict) -> Dict:
        """验证概念准确性"""
        
        validation_errors = []
        concept_scores = {}
        
        # 检查概念混淆错误
        for concept, definition in self.classic_definitions.items():
            concept_score = self._validate_single_concept(text_data, analysis_result, concept, definition)
            concept_scores[concept] = concept_score
            
            # 识别概念错误
            if concept_score < 6.0:
                errors = self._identify_concept_errors(text_data, analysis_result, concept, definition)
                validation_errors.extend(errors)
        
        # 计算概念准确性总分
        if concept_scores:
            concept_accuracy = sum(concept_scores.values()) / len(concept_scores)
        else:
            concept_accuracy = 0.0
        
        return {
            'concept_accuracy': concept_accuracy,
            'concept_scores': concept_scores,
            'validation_errors': validation_errors,
            'accuracy_level': self._determine_accuracy_level(concept_accuracy, 'concept_accuracy')
        }
    
    def _validate_single_concept(self, text_data: str, analysis_result: Dict, 
                               concept: str, definition: Dict) -> float:
        """验证单个概念的准确性"""
        
        score = 10.0  # 满分10分
        
        # 检查是否使用了错误等价概念
        for wrong_equivalent in definition['not_equivalent_to']:
            # 使用正则表达式匹配，避免字符串索引错误
            error_pattern = r'\b' + re.escape(wrong_equivalent) + r'\b'
            if re.search(error_pattern, text_data):
                score -= 3.0
        
        # 检查是否包含了本质要素
        essential_elements_found = 0
        for element in definition['essential_elements']:
            if element in text_data:
                essential_elements_found += 1
        
        if definition['essential_elements']:
            element_score = (essential_elements_found / len(definition['essential_elements'])) * 5
            score = min(score, element_score)
        
        # 检查是否体现了关键特征
        key_characteristics_found = 0
        for characteristic in definition['key_characteristics']:
            if characteristic in text_data:
                key_characteristics_found += 1
        
        if definition['key_characteristics']:
            characteristic_score = (key_characteristics_found / len(definition['key_characteristics'])) * 5
            score = min(score, characteristic_score)
        
        return max(score, 0.0)
    
    def _identify_concept_errors(self, text_data: str, analysis_result: Dict,
                                concept: str, definition: Dict) -> List[TheoryError]:
        """识别概念错误"""
        
        errors = []
        
        # 检查概念混淆错误
        if concept in self.common_errors['concept_confusion']:
            for error_type, error_info in self.common_errors['concept_confusion'][concept].items():
                # 使用正则表达式匹配，避免字符串索引错误
                error_pattern = r'\b' + re.escape(error_type) + r'\b'
                error_detected = re.search(error_pattern, text_data)
                
                if error_detected:
                    errors.append(TheoryError(
                        error_type=f"概念混淆_{concept}_{error_type}",
                        description=error_info['error'],
                        severity=error_info['severity'],
                        correction=error_info['correction'],
                        reference=definition['classical_source']
                    ))
        
        return errors
    
    def validate_principle_application(self, text_data: str, analysis_result: Dict) -> Dict:
        """验证原理应用准确性"""
        
        validation_errors = []
        principle_scores = {}
        
        # 检查辩证思维应用
        dialectics_score = self._validate_dialectics_application(text_data)
        principle_scores['dialectics'] = dialectics_score
        
        # 检查历史唯物主义应用
        historical_materialism_score = self._validate_historical_materialism_application(text_data)
        principle_scores['historical_materialism'] = historical_materialism_score
        
        # 检查阶级分析应用
        class_analysis_score = self._validate_class_analysis_application(text_data)
        principle_scores['class_analysis'] = class_analysis_score
        
        # 识别原理应用错误
        principle_errors = self._identify_principle_errors(text_data)
        validation_errors.extend(principle_errors)
        
        # 计算原理应用准确性总分
        if principle_scores:
            principle_accuracy = sum(principle_scores.values()) / len(principle_scores)
        else:
            principle_accuracy = 0.0
        
        return {
            'principle_accuracy': principle_accuracy,
            'principle_scores': principle_scores,
            'validation_errors': validation_errors,
            'accuracy_level': self._determine_accuracy_level(principle_accuracy, 'principle_application')
        }
    
    def _validate_dialectics_application(self, text_data: str) -> float:
        """验证辩证法应用"""
        
        score = 10.0
        
        # 检查是否体现了对立统一
        unity_indicators = ['对立统一', '既对立又统一', '相互依存', '相互转化']
        unity_found = any(indicator in text_data for indicator in unity_indicators)
        if not unity_found:
            score -= 3.0
        
        # 检查是否体现了发展变化
        development_indicators = ['发展', '变化', '运动', '过程', '转化']
        development_found = any(indicator in text_data for indicator in development_indicators)
        if not development_found:
            score -= 3.0
        
        # 检查是否体现了普遍联系
        connection_indicators = ['联系', '关系', '相互', '影响', '作用']
        connection_found = any(indicator in text_data for indicator in connection_indicators)
        if not connection_found:
            score -= 2.0
        
        # 检查是否避免了形而上学
        metaphysics_indicators = ['孤立', '静止', '绝对', '永恒', '不变']
        metaphysics_found = any(indicator in text_data for indicator in metaphysics_indicators)
        if metaphysics_found:
            score -= 2.0
        
        return max(score, 0.0)
    
    def _validate_historical_materialism_application(self, text_data: str) -> float:
        """验证历史唯物主义应用"""
        
        score = 10.0
        
        # 检查是否体现了生产力决定作用
        productivity_determining = ['生产力决定', '生产力基础', '生产力是基础']
        productivity_found = any(indicator in text_data for indicator in productivity_determining)
        if not productivity_found:
            score -= 3.0
        
        # 检查是否体现了生产关系反作用
        relations_reaction = ['反作用', '影响', '促进', '制约']
        reaction_found = any(indicator in text_data for indicator in relations_reaction)
        if not reaction_found:
            score -= 2.0
        
        # 检查是否体现了经济基础决定上层建筑
        base_determining = ['经济基础决定', '基础决定', '经济基础是基础']
        base_found = any(indicator in text_data for indicator in base_determining)
        if not base_found:
            score -= 3.0
        
        # 检查是否体现了上层建筑相对独立性
        superstructure_independence = ['相对独立', '独立性', '自身规律']
        independence_found = any(indicator in text_data for indicator in superstructure_independence)
        if not independence_found:
            score -= 2.0
        
        return max(score, 0.0)
    
    def _validate_class_analysis_application(self, text_data: str) -> float:
        """验证阶级分析应用"""
        
        score = 10.0
        
        # 检查是否基于生产资料占有关系
        ownership_indicators = ['生产资料占有', '所有制', '占有关系']
        ownership_found = any(indicator in text_data for indicator in ownership_indicators)
        if not ownership_found:
            score -= 4.0
        
        # 检查是否避免了收入水平划分
        income_indicators = ['收入水平', '贫富差距', '经济分化']
        income_found = any(indicator in text_data for indicator in income_indicators)
        if income_found:
            score -= 3.0
        
        # 检查是否体现了根本利益对立
        interest_indicators = ['根本利益', '利益对立', '阶级利益']
        interest_found = any(indicator in text_data for indicator in interest_indicators)
        if not interest_found:
            score -= 3.0
        
        return max(score, 0.0)
    
    def _identify_principle_errors(self, text_data: str) -> List[TheoryError]:
        """识别原理应用错误"""
        
        errors = []
        
        # 检查原理简化错误
        principle_simplification = self.common_errors.get('principle_simplification', {})
        for principle_type, principle_errors in principle_simplification.items():
            if isinstance(principle_errors, dict):
                for error_name, error_info in principle_errors.items():
                    if isinstance(error_info, dict) and 'error' in error_info:
                        # 使用正则表达式匹配，避免字符串索引错误
                        error_pattern = r'\b' + re.escape(error_info['error']) + r'\b'
                        error_detected = re.search(error_pattern, text_data)
                        
                        if error_detected:
                            errors.append(TheoryError(
                                error_type=f"原理简化_{principle_type}_{error_name}",
                                description=error_info['error'],
                                severity=error_info.get('severity', 'medium'),
                                correction=error_info.get('correction', '需要纠正'),
                                reference="马克思主义基本原理"
                            ))
        
        # 检查方法论错误
        methodology_errors = self.common_errors.get('methodology_errors', {})
        for method_type, method_errors in methodology_errors.items():
            if isinstance(method_errors, dict):
                for error_name, error_info in method_errors.items():
                    if isinstance(error_info, dict) and 'error' in error_info:
                        # 使用正则表达式匹配，避免字符串索引错误
                        error_pattern = r'\b' + re.escape(error_info['error']) + r'\b'
                        error_detected = re.search(error_pattern, text_data)
                        
                        if error_detected:
                            errors.append(TheoryError(
                                error_type=f"方法论错误_{method_type}_{error_name}",
                                description=error_info['error'],
                                severity=error_info.get('severity', 'medium'),
                                correction=error_info.get('correction', '需要纠正'),
                                reference="马克思主义方法论"
                            ))
        
        return errors
    
    def validate_methodology_soundness(self, text_data: str, analysis_result: Dict) -> Dict:
        """验证方法论科学性"""
        
        validation_errors = []
        methodology_scores = {}
        
        # 检查辩证思维方法
        dialectical_method_score = self._validate_dialectical_method(text_data)
        methodology_scores['dialectical_method'] = dialectical_method_score
        
        # 检查理论联系实际
        practice_connection_score = self._validate_practice_connection(text_data)
        methodology_scores['practice_connection'] = practice_connection_score
        
        # 检查具体问题具体分析
        concrete_analysis_score = self._validate_concrete_analysis(text_data)
        methodology_scores['concrete_analysis'] = concrete_analysis_score
        
        # 检查现象到本质
        phenomenon_to_essence_score = self._validate_phenomenon_to_essence(text_data)
        methodology_scores['phenomenon_to_essence'] = phenomenon_to_essence_score
        
        # 识别方法论错误
        methodology_errors = self._identify_methodology_errors(text_data)
        validation_errors.extend(methodology_errors)
        
        # 计算方法论科学性总分
        if methodology_scores:
            methodology_soundness = sum(methodology_scores.values()) / len(methodology_scores)
        else:
            methodology_soundness = 0.0
        
        return {
            'methodology_soundness': methodology_soundness,
            'methodology_scores': methodology_scores,
            'validation_errors': validation_errors,
            'accuracy_level': self._determine_accuracy_level(methodology_soundness, 'methodology_soundness')
        }
    
    def _validate_dialectical_method(self, text_data: str) -> float:
        """验证辩证思维方法"""
        
        score = 10.0
        
        # 检查是否避免形而上学
        metaphysical_indicators = ['孤立', '静止', '绝对', '永恒', '不变']
        metaphysical_found = any(indicator in text_data for indicator in metaphysical_indicators)
        if metaphysical_found:
            score -= 4.0
        
        # 检查是否体现发展观点
        development_indicators = ['发展', '变化', '运动', '过程', '转化']
        development_found = any(indicator in text_data for indicator in development_indicators)
        if not development_found:
            score -= 3.0
        
        # 检查是否体现矛盾观点
        contradiction_indicators = ['矛盾', '对立统一', '相互依存', '相互转化']
        contradiction_found = any(indicator in text_data for indicator in contradiction_indicators)
        if not contradiction_found:
            score -= 3.0
        
        return max(score, 0.0)
    
    def _validate_practice_connection(self, text_data: str) -> float:
        """验证理论联系实际"""
        
        score = 10.0
        
        # 检查是否涉及实际问题
        practical_indicators = ['实际', '现实', '具体', '实践', '应用']
        practical_found = any(indicator in text_data for indicator in practical_indicators)
        if not practical_found:
            score -= 4.0
        
        # 检查是否避免教条主义
        dogmatic_indicators = ['教条', '公式', '套用', '机械']
        dogmatic_found = any(indicator in text_data for indicator in dogmatic_indicators)
        if dogmatic_found:
            score -= 3.0
        
        # 检查是否体现实践标准
        practice_standard_indicators = ['实践是检验真理的标准', '实践', '检验', '标准']
        practice_standard_found = any(indicator in text_data for indicator in practice_standard_indicators)
        if not practice_standard_found:
            score -= 3.0
        
        return max(score, 0.0)
    
    def _validate_concrete_analysis(self, text_data: str) -> float:
        """验证具体问题具体分析"""
        
        score = 10.0
        
        # 检查是否涉及具体问题
        concrete_indicators = ['具体', '个别', '特殊', '实际']
        concrete_found = any(indicator in text_data for indicator in concrete_indicators)
        if not concrete_found:
            score -= 4.0
        
        # 检查是否避免泛泛而谈
        general_indicators = ['泛泛而谈', '空洞', '抽象', '笼统']
        general_found = any(indicator in text_data for indicator in general_indicators)
        if general_found:
            score -= 3.0
        
        # 检查是否体现具体分析
        analysis_indicators = ['分析', '具体分析', '详细分析', '深入分析']
        analysis_found = any(indicator in text_data for indicator in analysis_indicators)
        if not analysis_found:
            score -= 3.0
        
        return max(score, 0.0)
    
    def _validate_phenomenon_to_essence(self, text_data: str) -> float:
        """验证现象到本质"""
        
        score = 10.0
        
        # 检查是否涉及本质分析
        essence_indicators = ['本质', '规律', '内在', '根本', '深层']
        essence_found = any(indicator in text_data for indicator in essence_indicators)
        if not essence_found:
            score -= 4.0
        
        # 检查是否避免表面化
        surface_indicators = ['表面', '现象', '表象', '浅层']
        surface_found = any(indicator in text_data for indicator in surface_indicators)
        if surface_found:
            score -= 3.0
        
        # 检查是否体现透过现象看本质
        透过现象看本质_indicators = ['透过现象看本质', '透过', '现象', '本质']
        透过现象看本质_found = any(indicator in text_data for indicator in 透过现象看本质_indicators)
        if not 透过现象看本质_found:
            score -= 3.0
        
        return max(score, 0.0)
    
    def _identify_methodology_errors(self, text_data: str) -> List[TheoryError]:
        """识别方法论错误"""
        
        errors = []
        
        # 检查方法论错误
        methodology_errors = self.common_errors.get('methodology_errors', {})
        for method_type, method_errors in methodology_errors.items():
            if isinstance(method_errors, dict):
                for error_name, error_info in method_errors.items():
                    if isinstance(error_info, dict) and 'error' in error_info:
                        if error_info['error'] in text_data:
                            errors.append(TheoryError(
                                error_type=f"方法论错误_{method_type}_{error_name}",
                                description=error_info['error'],
                                severity=error_info.get('severity', 'medium'),
                                correction=error_info.get('correction', '需要纠正'),
                                reference="马克思主义方法论"
                            ))
        
        return errors
    
    def validate_analytical_depth(self, text_data: str, analysis_result: Dict) -> Dict:
        """验证分析深度"""
        
        validation_errors = []
        depth_scores = {}
        
        # 检查现象分析深度
        phenomenon_score = self._validate_phenomenon_analysis(text_data)
        depth_scores['phenomenon_analysis'] = phenomenon_score
        
        # 检查本质分析深度
        essence_score = self._validate_essence_analysis(text_data)
        depth_scores['essence_analysis'] = essence_score
        
        # 检查关系分析深度
        relation_score = self._validate_relation_analysis(text_data)
        depth_scores['relation_analysis'] = relation_score
        
        # 检查发展分析深度
        development_score = self._validate_development_analysis(text_data)
        depth_scores['development_analysis'] = development_score
        
        # 识别深度不足错误
        depth_errors = self._identify_depth_errors(text_data)
        validation_errors.extend(depth_errors)
        
        # 计算分析深度总分
        if depth_scores:
            analytical_depth = sum(depth_scores.values()) / len(depth_scores)
        else:
            analytical_depth = 0.0
        
        return {
            'analytical_depth': analytical_depth,
            'depth_scores': depth_scores,
            'validation_errors': validation_errors,
            'accuracy_level': self._determine_accuracy_level(analytical_depth, 'analytical_depth')
        }
    
    def _validate_phenomenon_analysis(self, text_data: str) -> float:
        """验证现象分析深度"""
        
        score = 10.0
        
        # 检查是否描述了现象特征
        phenomenon_indicators = ['现象', '表现', '特征', '状况', '情况']
        phenomenon_found = any(indicator in text_data for indicator in phenomenon_indicators)
        if not phenomenon_found:
            score -= 4.0
        
        # 检查是否进行了现象分类
        classification_indicators = ['分类', '类型', '种类', '类别']
        classification_found = any(indicator in text_data for indicator in classification_indicators)
        if not classification_found:
            score -= 3.0
        
        # 检查是否分析了现象原因
        cause_indicators = ['原因', '原因分析', '导致']
        cause_found = any(indicator in text_data for indicator in cause_indicators)
        if not cause_found:
            score -= 3.0
        
        return max(score, 0.0)
    
    def _validate_essence_analysis(self, text_data: str) -> float:
        """验证本质分析深度"""
        
        score = 10.0
        
        # 检查是否涉及本质概念
        essence_indicators = ['本质', '规律', '内在', '根本']
        essence_found = any(indicator in text_data for indicator in essence_indicators)
        if not essence_found:
            score -= 4.0
        
        # 检查是否揭示了内在联系
        inner_connection_indicators = ['内在联系', '内在关系', '本质联系']
        inner_connection_found = any(indicator in text_data for indicator in inner_connection_indicators)
        if not inner_connection_found:
            score -= 3.0
        
        # 检查是否揭示了根本原因
        root_cause_indicators = ['根本原因', '深层次原因', '本质原因']
        root_cause_found = any(indicator in text_data for indicator in root_cause_indicators)
        if not root_cause_found:
            score -= 3.0
        
        return max(score, 0.0)
    
    def _validate_relation_analysis(self, text_data: str) -> float:
        """验证关系分析深度"""
        
        score = 10.0
        
        # 检查是否分析了相互关系
        relation_indicators = ['关系', '相互关系', '联系', '相互作用']
        relation_found = any(indicator in text_data for indicator in relation_indicators)
        if not relation_found:
            score -= 4.0
        
        # 检查是否分析了相互作用机制
        mechanism_indicators = ['机制', '作用机制', '互动机制']
        mechanism_found = any(indicator in text_data for indicator in mechanism_indicators)
        if not mechanism_found:
            score -= 3.0
        
        # 检查是否分析了影响和作用
        influence_indicators = ['影响', '作用', '促进', '制约']
        influence_found = any(indicator in text_data for indicator in influence_indicators)
        if not influence_found:
            score -= 3.0
        
        return max(score, 0.0)
    
    def _validate_development_analysis(self, text_data: str) -> float:
        """验证发展分析深度"""
        
        score = 10.0
        
        # 检查是否涉及发展趋势
        trend_indicators = ['趋势', '发展', '变化', '演变']
        trend_found = any(indicator in text_data for indicator in trend_indicators)
        if not trend_found:
            score -= 4.0
        
        # 检查是否分析了发展规律
        law_indicators = ['规律', '发展规律', '客观规律']
        law_found = any(indicator in text_data for indicator in law_indicators)
        if not law_found:
            score -= 3.0
        
        # 检查是否进行了预测
        prediction_indicators = ['预测', '展望', '前景', '趋势预测']
        prediction_found = any(indicator in text_data for indicator in prediction_indicators)
        if not prediction_found:
            score -= 3.0
        
        return max(score, 0.0)
    
    def _identify_depth_errors(self, text_data: str) -> List[TheoryError]:
        """识别深度不足错误"""
        
        errors = []
        
        # 检查表面化错误
        surface_indicators = ['表面', '现象', '表象', '浅层', '表面化']
        for indicator in surface_indicators:
            if indicator in text_data:
                errors.append(TheoryError(
                    error_type="深度不足_表面化",
                    description=f"分析停留在{indicator}，缺乏深度",
                    severity="medium",
                    correction="必须透过现象看本质，揭示内在规律",
                    reference="马克思主义认识论"
                ))
        
        # 检查简单化错误
        simple_indicators = ['简单', '单纯', '笼统', '泛泛而谈']
        for indicator in simple_indicators:
            if indicator in text_data:
                errors.append(TheoryError(
                    error_type="深度不足_简单化",
                    description=f"分析过于{indicator}，缺乏深入分析",
                    severity="medium",
                    correction="必须深入分析，避免简单化倾向",
                    reference="马克思主义方法论"
                ))
        
        return errors
    
    def _determine_accuracy_level(self, score: float, category: str) -> TheoryAccuracyLevel:
        """确定准确性等级"""
        # 如果是overall类别，使用concept_accuracy的标准作为默认
        if category == 'overall':
            standards = self.accuracy_standards.get('concept_accuracy', {
                'excellent': 9.0,
                'good': 7.5,
                'average': 6.0,
                'poor': 4.0,
                'serious_error': 0.0
            })
        else:
            standards = self.accuracy_standards.get(category, {
                'excellent': 9.0,
                'good': 7.5,
                'average': 6.0,
                'poor': 4.0,
                'serious_error': 0.0
            })
        
        if score >= standards['excellent']:
            return TheoryAccuracyLevel.EXCELLENT
        elif score >= standards['good']:
            return TheoryAccuracyLevel.GOOD
        elif score >= standards['average']:
            return TheoryAccuracyLevel.AVERAGE
        elif score >= standards['poor']:
            return TheoryAccuracyLevel.POOR
        else:
            return TheoryAccuracyLevel.SERIOUS_ERROR
    
    def comprehensive_theory_validation(self, text_data: str, analysis_result: Dict) -> Dict:
        """综合理论准确性验证"""
        
        # 执行各项验证
        concept_validation = self.validate_concept_accuracy(text_data, analysis_result)
        principle_validation = self.validate_principle_application(text_data, analysis_result)
        methodology_validation = self.validate_methodology_soundness(text_data, analysis_result)
        depth_validation = self.validate_analytical_depth(text_data, analysis_result)
        
        # 收集所有验证错误
        all_errors = []
        all_errors.extend(concept_validation['validation_errors'])
        all_errors.extend(principle_validation['validation_errors'])
        all_errors.extend(methodology_validation['validation_errors'])
        all_errors.extend(depth_validation['validation_errors'])
        
        # 计算综合准确性分数
        concept_weight = 0.3
        principle_weight = 0.3
        methodology_weight = 0.2
        depth_weight = 0.2
        
        overall_accuracy = (
            concept_validation['concept_accuracy'] * concept_weight +
            principle_validation['principle_accuracy'] * principle_weight +
            methodology_validation['methodology_soundness'] * methodology_weight +
            depth_validation['analytical_depth'] * depth_weight
        )
        
        # 确定整体准确性等级
        overall_level = self._determine_accuracy_level(overall_accuracy, 'overall')
        
        # 生成改进建议
        improvement_suggestions = self._generate_improvement_suggestions(
            concept_validation, principle_validation, methodology_validation, depth_validation
        )
        
        # 验证结果
        validation_result = {
            'overall_accuracy': overall_accuracy,
            'overall_level': overall_level,
            'concept_validation': concept_validation,
            'principle_validation': principle_validation,
            'methodology_validation': methodology_validation,
            'depth_validation': depth_validation,
            'all_errors': all_errors,
            'improvement_suggestions': improvement_suggestions,
            'validation_timestamp': pd.Timestamp.now().isoformat()
        }
        
        # 记录验证历史
        self._record_validation(validation_result)
        
        return validation_result
    
    def _generate_improvement_suggestions(self, concept_validation: Dict,
                                       principle_validation: Dict,
                                       methodology_validation: Dict,
                                       depth_validation: Dict) -> List[str]:
        """生成改进建议"""
        
        suggestions = []
        
        # 基于概念验证结果生成建议
        if concept_validation['concept_accuracy'] < 6.0:
            suggestions.extend([
                "深入学习马克思主义核心概念的经典定义",
                "准确理解和运用概念内涵和外延",
                "避免概念混淆和错误等价",
                "建立准确的概念关系网络"
            ])
        
        # 基于原理验证结果生成建议
        if principle_validation['principle_accuracy'] < 6.0:
            suggestions.extend([
                "掌握马克思主义基本原理的科学内涵",
                "避免原理应用的简单化和绝对化",
                "正确处理决定作用与反作用的关系",
                "坚持辩证思维，避免形而上学"
            ])
        
        # 基于方法论验证结果生成建议
        if methodology_validation['methodology_soundness'] < 6.0:
            suggestions.extend([
                "掌握马克思主义的科学方法论",
                "坚持理论联系实际，避免教条主义",
                "坚持具体问题具体分析",
                "坚持透过现象看本质，避免经验主义"
            ])
        
        # 基于深度验证结果生成建议
        if depth_validation['analytical_depth'] < 6.0:
            suggestions.extend([
                "深化理论分析的层次性和全面性",
                "从现象分析深入到本质分析",
                "加强关系分析和发展分析",
                "避免表面化和简单化倾向"
            ])
        
        return list(set(suggestions))
    
    def _record_validation(self, validation_result: Dict):
        """记录验证历史"""
        
        validation_record = {
            'timestamp': validation_result['validation_timestamp'],
            'overall_accuracy': validation_result['overall_accuracy'],
            'overall_level': validation_result['overall_level'].value,
            'error_count': len(validation_result['all_errors']),
            'suggestion_count': len(validation_result['improvement_suggestions'])
        }
        
        self.validation_history.append(validation_record)
        
        # 保持历史记录不超过100条
        if len(self.validation_history) > 100:
            self.validation_history = self.validation_history[-100:]
    
    def get_validation_statistics(self) -> Dict:
        """获取验证统计信息"""
        
        if not self.validation_history:
            return {
                'total_validations': 0,
                'average_accuracy': 0,
                'accuracy_distribution': {},
                'improvement_trend': '无数据'
            }
        
        total_validations = len(self.validation_history)
        average_accuracy = sum(record['overall_accuracy'] for record in self.validation_history) / total_validations
        
        # 准确性分布
        accuracy_distribution = {}
        for record in self.validation_history:
            level = record['overall_level']
            accuracy_distribution[level] = accuracy_distribution.get(level, 0) + 1
        
        # 改进趋势
        if total_validations >= 2:
            recent_avg = sum(record['overall_accuracy'] for record in self.validation_history[-5:]) / min(5, total_validations)
            earlier_avg = sum(record['overall_accuracy'] for record in self.validation_history[:-5]) / max(1, total_validations - 5)
            
            if recent_avg > earlier_avg + 0.5:
                improvement_trend = "明显改善"
            elif recent_avg > earlier_avg:
                improvement_trend = "有所改善"
            elif recent_avg < earlier_avg - 0.5:
                improvement_trend = "明显下降"
            elif recent_avg < earlier_avg:
                improvement_trend = "有所下降"
            else:
                improvement_trend = "保持稳定"
        else:
            improvement_trend = "数据不足"
        
        return {
            'total_validations': total_validations,
            'average_accuracy': average_accuracy,
            'accuracy_distribution': accuracy_distribution,
            'improvement_trend': improvement_trend
        }
    
    def generate_validation_report(self, validation_result: Dict) -> str:
        """生成理论准确性验证报告"""
        
        overall_accuracy = validation_result['overall_accuracy']
        overall_level = validation_result['overall_level']
        all_errors = validation_result['all_errors']
        improvement_suggestions = validation_result['improvement_suggestions']
        
        report = []
        report.append("# 马克思主义理论准确性验证报告")
        report.append(f"验证时间: {validation_result['validation_timestamp']}")
        report.append("")
        
        # 总体评估
        report.append("## 总体评估")
        report.append(f"- 综合准确性分数: {overall_accuracy:.2f}/10")
        report.append(f"- 准确性等级: {overall_level.value}")
        report.append(f"- 验证结果: {'通过' if overall_level != TheoryAccuracyLevel.SERIOUS_ERROR else '未通过'}")
        report.append("")
        
        # 各项验证结果
        report.append("## 各项验证结果")
        
        # 概念准确性
        concept_validation = validation_result['concept_validation']
        report.append(f"### 概念准确性")
        report.append(f"- 准确性分数: {concept_validation['concept_accuracy']:.2f}/10")
        report.append(f"- 准确性等级: {concept_validation['accuracy_level'].value}")
        
        concept_scores = concept_validation.get('concept_scores', {})
        if concept_scores:
            report.append("- 概念分数:")
            for concept, score in concept_scores.items():
                report.append(f"  - {concept}: {score:.2f}")
        report.append("")
        
        # 原理应用准确性
        principle_validation = validation_result['principle_validation']
        report.append(f"### 原理应用准确性")
        report.append(f"- 准确性分数: {principle_validation['principle_accuracy']:.2f}/10")
        report.append(f"- 准确性等级: {principle_validation['accuracy_level'].value}")
        
        principle_scores = principle_validation.get('principle_scores', {})
        if principle_scores:
            report.append("- 原理分数:")
            for principle, score in principle_scores.items():
                report.append(f"  - {principle}: {score:.2f}")
        report.append("")
        
        # 方法论科学性
        methodology_validation = validation_result['methodology_validation']
        report.append(f"### 方法论科学性")
        report.append(f"- 准确性分数: {methodology_validation['methodology_soundness']:.2f}/10")
        report.append(f"- 准确性等级: {methodology_validation['accuracy_level'].value}")
        
        methodology_scores = methodology_validation.get('methodology_scores', {})
        if methodology_scores:
            report.append("- 方法论分数:")
            for method, score in methodology_scores.items():
                report.append(f"  - {method}: {score:.2f}")
        report.append("")
        
        # 分析深度
        depth_validation = validation_result['depth_validation']
        report.append(f"### 分析深度")
        report.append(f"- 深度分数: {depth_validation['analytical_depth']:.2f}/10")
        report.append(f"- 深度等级: {depth_validation['accuracy_level'].value}")
        
        depth_scores = depth_validation.get('depth_scores', {})
        if depth_scores:
            report.append("- 深度分数:")
            for depth, score in depth_scores.items():
                report.append(f"  - {depth}: {score:.2f}")
        report.append("")
        
        # 理论错误
        if all_errors:
            report.append("## 理论错误")
            report.append(f"发现错误数量: {len(all_errors)}")
            
            # 按严重程度分类
            high_severity_errors = [error for error in all_errors if error.severity == 'high']
            medium_severity_errors = [error for error in all_errors if error.severity == 'medium']
            low_severity_errors = [error for error in all_errors if error.severity == 'low']
            
            if high_severity_errors:
                report.append("### 严重错误")
                for error in high_severity_errors:
                    report.append(f"- **{error.error_type}**: {error.description}")
                    report.append(f"  - 改正: {error.correction}")
                    report.append(f"  - 参考: {error.reference}")
                report.append("")
            
            if medium_severity_errors:
                report.append("### 中等错误")
                for error in medium_severity_errors:
                    report.append(f"- **{error.error_type}**: {error.description}")
                    report.append(f"  - 改正: {error.correction}")
                    report.append(f"  - 参考: {error.reference}")
                report.append("")
            
            if low_severity_errors:
                report.append("### 轻微错误")
                for error in low_severity_errors:
                    report.append(f"- **{error.error_type}**: {error.description}")
                    report.append(f"  - 改正: {error.correction}")
                    report.append(f"  - 参考: {error.reference}")
                report.append("")
        
        # 改进建议
        if improvement_suggestions:
            report.append("## 改进建议")
            for i, suggestion in enumerate(improvement_suggestions, 1):
                report.append(f"{i}. {suggestion}")
            report.append("")
        
        # 验证统计
        statistics = self.get_validation_statistics()
        report.append("## 验证统计")
        report.append(f"- 总验证次数: {statistics['total_validations']}")
        report.append(f"- 平均准确性分数: {statistics['average_accuracy']:.2f}")
        report.append(f"- 改进趋势: {statistics['improvement_trend']}")
        report.append("")
        
        # 总结
        report.append("## 总结")
        if overall_level == TheoryAccuracyLevel.EXCELLENT:
            report.append("理论准确性优秀，完全符合马克思主义理论标准。")
        elif overall_level == TheoryAccuracyLevel.GOOD:
            report.append("理论准确性良好，基本符合马克思主义理论标准。")
        elif overall_level == TheoryAccuracyLevel.AVERAGE:
            report.append("理论准确性一般，需要在理论理解和应用方面进一步提升。")
        elif overall_level == TheoryAccuracyLevel.POOR:
            report.append("理论准确性不足，存在明显理论偏差，需要系统学习马克思主义理论。")
        else:
            report.append("理论准确性存在严重错误，必须立即纠正理论偏差。")
        
        return "\n".join(report)


def main():
    """测试理论准确性验证器"""
    validator = MarxistTheoryValidator()
    
    test_text = """
    在当代社会发展中，生产力水平显著提升，特别是数字技术的快速发展。
    生产资料所有制坚持公有制为主体，劳动关系呈现多元化特点。
    经济基础的变革为上层建筑的完善提供了物质基础。
    当前社会主要矛盾是人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾。
    人民群众在历史发展中发挥着主体作用。
    """
    
    print("=== 马克思主义理论准确性验证器测试 ===")
    
    # 模拟分析结果（实际使用时应该用真实的分析结果）
    mock_analysis_result = {
        'dialectical_results': {
            'overall_dialectical_level': {
                'overall_score': 6.5
            }
        },
        'historical_results': {
            'overall_theoretical_level': {
                'overall_score': 5.8
            }
        }
    }
    
    # 执行综合验证
    validation_result = validator.comprehensive_theory_validation(test_text, mock_analysis_result)
    
    # 显示验证结果
    print(f"\n综合准确性分数: {validation_result['overall_accuracy']:.2f}/10")
    print(f"准确性等级: {validation_result['overall_level'].value}")
    
    # 显示各项指标
    print(f"\n各项指标:")
    print(f"- 概念准确性: {validation_result['concept_validation']['concept_accuracy']:.2f}/10")
    print(f"- 原理应用准确性: {validation_result['principle_validation']['principle_accuracy']:.2f}/10")
    print(f"- 方法论科学性: {validation_result['methodology_validation']['methodology_soundness']:.2f}/10")
    print(f"- 分析深度: {validation_result['depth_validation']['analytical_depth']:.2f}/10")
    
    # 显示理论错误
    all_errors = validation_result['all_errors']
    if all_errors:
        print(f"\n理论错误 ({len(all_errors)}个):")
        for error in all_errors:
            print(f"- {error.error_type}: {error.description}")
    
    # 显示改进建议
    improvement_suggestions = validation_result['improvement_suggestions']
    if improvement_suggestions:
        print(f"\n改进建议 ({len(improvement_suggestions)}项):")
        for suggestion in improvement_suggestions:
            print(f"- {suggestion}")
    
    # 生成验证报告
    validation_report = validator.generate_validation_report(validation_result)
    
    print(f"\n{validation_report}")


if __name__ == "__main__":
    main()
