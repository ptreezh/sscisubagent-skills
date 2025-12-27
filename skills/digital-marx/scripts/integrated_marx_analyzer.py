#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数字马克思集成分析引擎 - 协调AI理论分析与脚本定量计算
实现四阶段分析流程的智能协调和结果整合
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import json
import os
import sys
from datetime import datetime

# 添加脚本路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from historical_materialism_analyzer import HistoricalMaterialismAnalyzer


class DigitalMarxIntegratedAnalyzer:
    """数字马克思集成分析引擎"""
    
    def __init__(self):
        self.analyzer = HistoricalMaterialismAnalyzer()
        self.analysis_state = {}
        self.analysis_history = []
        
        # 提示词文件路径
        self.prompts_path = {
            'material_base': '../prompts/material-base-analysis.md',
            'production_relations': '../prompts/production-relations-analysis.md',
            'superstructure': '../prompts/superstructure-analysis.md',
            'social_change': '../prompts/social-change-prediction.md'
        }
        
        # 分析阶段配置
        self.analysis_phases = {
            'material_base': {
                'name': '物质基础分析',
                'prompt_file': 'material-base-analysis.md',
                'script_function': 'analyze_productivity_level',
                'description': '分析社会发展的物质技术基础'
            },
            'production_relations': {
                'name': '生产关系分析',
                'prompt_file': 'production-relations-analysis.md',
                'script_function': 'analyze_production_relations',
                'description': '分析社会生产关系结构'
            },
            'superstructure': {
                'name': '上层建筑分析',
                'prompt_file': 'superstructure-analysis.md',
                'script_function': 'analyze_superstructure',
                'description': '分析政治法律制度和意识形态'
            },
            'social_change': {
                'name': '社会变革预测',
                'prompt_file': 'social-change-prediction.md',
                'script_function': 'analyze_social_change',
                'description': '分析社会发展趋势和变革可能'
            }
        }
    
    def execute_comprehensive_analysis(self, text_data: str, context: Dict = None) -> Dict:
        """执行完整的四阶段分析"""
        
        # 初始化分析状态
        self._initialize_analysis_state(text_data, context)
        
        # 执行四阶段分析
        analysis_results = {}
        
        # 阶段1: 物质基础分析
        print("执行阶段1: 物质基础分析")
        material_base_results = self._execute_material_base_analysis(text_data, context)
        analysis_results['material_base'] = material_base_results
        
        # 阶段2: 生产关系分析
        print("执行阶段2: 生产关系分析")
        production_relations_results = self._execute_production_relations_analysis(text_data, context)
        analysis_results['production_relations'] = production_relations_results
        
        # 阶段3: 上层建筑分析
        print("执行阶段3: 上层建筑分析")
        superstructure_results = self._execute_superstructure_analysis(text_data, context)
        analysis_results['superstructure'] = superstructure_results
        
        # 阶段4: 社会变革预测
        print("执行阶段4: 社会变革预测")
        social_change_results = self._execute_social_change_analysis(text_data, context)
        analysis_results['social_change'] = social_change_results
        
        # 整合分析结果
        integrated_results = self._integrate_analysis_results(analysis_results)
        
        # 生成综合报告
        comprehensive_report = self._generate_comprehensive_report(integrated_results)
        
        # 更新分析历史
        self._update_analysis_history(integrated_results)
        
        return {
            'analysis_results': analysis_results,
            'integrated_results': integrated_results,
            'comprehensive_report': comprehensive_report,
            'analysis_metadata': self._get_analysis_metadata()
        }
    
    def _initialize_analysis_state(self, text_data: str, context: Dict = None):
        """初始化分析状态"""
        self.analysis_state = {
            'start_time': datetime.now(),
            'text_data': text_data,
            'context': context or {},
            'current_phase': None,
            'completed_phases': [],
            'quality_scores': {},
            'warnings': [],
            'errors': []
        }
    
    def _execute_material_base_analysis(self, text_data: str, context: Dict = None) -> Dict:
        """执行物质基础分析"""
        self.analysis_state['current_phase'] = 'material_base'
        
        try:
            # 调用脚本进行定量分析
            quantitative_results = self.analyzer.analyze_productivity_level(text_data, context)
            
            # 生成AI理论分析建议
            theoretical_guidance = self._generate_theoretical_guidance(
                'material_base', quantitative_results
            )
            
            # 质量评估
            quality_assessment = self._assess_phase_quality(
                'material_base', quantitative_results
            )
            
            results = {
                'quantitative_results': quantitative_results,
                'theoretical_guidance': theoretical_guidance,
                'quality_assessment': quality_assessment,
                'phase_completed': True
            }
            
            self.analysis_state['completed_phases'].append('material_base')
            self.analysis_state['quality_scores']['material_base'] = quality_assessment['overall_quality']
            
            return results
            
        except Exception as e:
            error_info = f"物质基础分析阶段出错: {str(e)}"
            self.analysis_state['errors'].append(error_info)
            return {
                'error': error_info,
                'phase_completed': False
            }
    
    def _execute_production_relations_analysis(self, text_data: str, context: Dict = None) -> Dict:
        """执行生产关系分析"""
        self.analysis_state['current_phase'] = 'production_relations'
        
        try:
            # 调用脚本进行定量分析
            quantitative_results = self.analyzer.analyze_production_relations(text_data, context)
            
            # 生成AI理论分析建议
            theoretical_guidance = self._generate_theoretical_guidance(
                'production_relations', quantitative_results
            )
            
            # 质量评估
            quality_assessment = self._assess_phase_quality(
                'production_relations', quantitative_results
            )
            
            results = {
                'quantitative_results': quantitative_results,
                'theoretical_guidance': theoretical_guidance,
                'quality_assessment': quality_assessment,
                'phase_completed': True
            }
            
            self.analysis_state['completed_phases'].append('production_relations')
            self.analysis_state['quality_scores']['production_relations'] = quality_assessment['overall_quality']
            
            return results
            
        except Exception as e:
            error_info = f"生产关系分析阶段出错: {str(e)}"
            self.analysis_state['errors'].append(error_info)
            return {
                'error': error_info,
                'phase_completed': False
            }
    
    def _execute_superstructure_analysis(self, text_data: str, context: Dict = None) -> Dict:
        """执行上层建筑分析"""
        self.analysis_state['current_phase'] = 'superstructure'
        
        try:
            # 调用脚本进行定量分析
            quantitative_results = self.analyzer.analyze_superstructure(text_data, context)
            
            # 生成AI理论分析建议
            theoretical_guidance = self._generate_theoretical_guidance(
                'superstructure', quantitative_results
            )
            
            # 质量评估
            quality_assessment = self._assess_phase_quality(
                'superstructure', quantitative_results
            )
            
            results = {
                'quantitative_results': quantitative_results,
                'theoretical_guidance': theoretical_guidance,
                'quality_assessment': quality_assessment,
                'phase_completed': True
            }
            
            self.analysis_state['completed_phases'].append('superstructure')
            self.analysis_state['quality_scores']['superstructure'] = quality_assessment['overall_quality']
            
            return results
            
        except Exception as e:
            error_info = f"上层建筑分析阶段出错: {str(e)}"
            self.analysis_state['errors'].append(error_info)
            return {
                'error': error_info,
                'phase_completed': False
            }
    
    def _execute_social_change_analysis(self, text_data: str, context: Dict = None) -> Dict:
        """执行社会变革预测"""
        self.analysis_state['current_phase'] = 'social_change'
        
        try:
            # 调用脚本进行定量分析
            quantitative_results = self.analyzer.analyze_social_change(text_data, context)
            
            # 生成AI理论分析建议
            theoretical_guidance = self._generate_theoretical_guidance(
                'social_change', quantitative_results
            )
            
            # 质量评估
            quality_assessment = self._assess_phase_quality(
                'social_change', quantitative_results
            )
            
            results = {
                'quantitative_results': quantitative_results,
                'theoretical_guidance': theoretical_guidance,
                'quality_assessment': quality_assessment,
                'phase_completed': True
            }
            
            self.analysis_state['completed_phases'].append('social_change')
            self.analysis_state['quality_scores']['social_change'] = quality_assessment['overall_quality']
            
            return results
            
        except Exception as e:
            error_info = f"社会变革预测阶段出错: {str(e)}"
            self.analysis_state['errors'].append(error_info)
            return {
                'error': error_info,
                'phase_completed': False
            }
    
    def _generate_theoretical_guidance(self, phase: str, quantitative_results: Dict) -> Dict:
        """生成理论分析指导"""
        
        guidance_templates = {
            'material_base': {
                'focus_areas': [
                    '生产力发展水平的客观评估',
                    '生产工具和技术形态的历史分析',
                    '劳动效率的社会意义',
                    '生产力与生产关系的适应性'
                ],
                'key_questions': [
                    '当前生产力处于哪个历史阶段？',
                    '技术发展对社会结构的影响如何？',
                    '劳动效率变化体现了什么社会规律？',
                    '生产力发展面临哪些瓶颈？'
                ],
                'analysis_depth': '深入分析生产力发展的内在规律和历史必然性'
            },
            'production_relations': {
                'focus_areas': [
                    '生产资料所有制的性质和特征',
                    '人们在生产中的地位和相互关系',
                    '产品分配方式的公平性和效率性',
                    '阶级结构的形成和演变'
                ],
                'key_questions': [
                    '当前生产关系的本质特征是什么？',
                    '所有制形式如何影响社会发展？',
                    '分配方式体现了什么样的价值取向？',
                    '阶级矛盾的主要表现是什么？'
                ],
                'analysis_depth': '深入分析生产关系的阶级本质和历史作用'
            },
            'superstructure': {
                'focus_areas': [
                    '政治制度的阶级性质和服务对象',
                    '意识形态的社会功能和历史作用',
                    '文化传统与现代文明的融合',
                    '上层建筑与经济基础的辩证关系'
                ],
                'key_questions': [
                    '政治制度为哪个阶级服务？',
                    '主流意识形态如何维护现有秩序？',
                    '文化发展反映了什么样的社会变迁？',
                    '上层建筑如何反作用于经济基础？'
                ],
                'analysis_depth': '深入分析上层建筑的阶级属性和相对独立性'
            },
            'social_change': {
                'focus_areas': [
                    '社会基本矛盾的激化程度',
                    '社会变革的主客观条件',
                    '社会变革的动力和阻力',
                    '社会发展的可能路径和趋势'
                ],
                'key_questions': [
                    '当前社会的主要矛盾是什么？',
                    '社会变革的条件是否成熟？',
                    '推动社会变革的主要力量有哪些？',
                    '社会发展的历史趋势如何？'
                ],
                'analysis_depth': '深入分析社会变革的客观规律和历史必然性'
            }
        }
        
        template = guidance_templates.get(phase, {})
        
        # 基于定量结果生成具体建议
        specific_suggestions = self._generate_specific_suggestions(phase, quantitative_results)
        
        return {
            'phase': phase,
            'focus_areas': template.get('focus_areas', []),
            'key_questions': template.get('key_questions', []),
            'analysis_depth': template.get('analysis_depth', ''),
            'specific_suggestions': specific_suggestions,
            'prompt_file': self.prompts_path.get(phase, ''),
            'quantitative_summary': self._generate_quantitative_summary(quantitative_results)
        }
    
    def _generate_specific_suggestions(self, phase: str, quantitative_results: Dict) -> List[str]:
        """基于定量结果生成具体建议"""
        suggestions = []
        
        if phase == 'material_base':
            productivity_stage = quantitative_results.get('productivity_stage', '未知')
            overall_score = quantitative_results.get('overall_productivity', 0)
            
            suggestions.append(f"重点关注生产力阶段: {productivity_stage}")
            if overall_score < 5.0:
                suggestions.append("生产力水平较低，需要深入分析制约因素")
            else:
                suggestions.append("生产力发展较好，关注其对生产关系的影响")
        
        elif phase == 'production_relations':
            overall_score = quantitative_results.get('overall_production_relations', 0)
            class_structure = quantitative_results.get('class_structure', {})
            conflict_intensity = class_structure.get('class_conflict_intensity', 0)
            
            suggestions.append(f"生产关系综合评分: {overall_score:.2f}")
            if conflict_intensity > 3.0:
                suggestions.append("阶级矛盾较为突出，需要重点分析")
            else:
                suggestions.append("阶级关系相对缓和，关注其他社会矛盾")
        
        elif phase == 'superstructure':
            overall_score = quantitative_results.get('overall_superstructure', 0)
            economic_relation = quantitative_results.get('economic_base_relation', {})
            dominant_relation = economic_relation.get('dominant_relation', '未知')
            
            suggestions.append(f"上层建筑综合评分: {overall_score:.2f}")
            suggestions.append(f"与经济基础关系: {dominant_relation}")
            if dominant_relation == 'determined':
                suggestions.append("强调经济基础的决定作用")
            else:
                suggestions.append("关注上层建筑的相对独立性")
        
        elif phase == 'social_change':
            contradictions = quantitative_results.get('basic_contradictions', {})
            primary_contradiction = contradictions.get('primary_contradiction', '未知')
            conditions = quantitative_results.get('change_conditions', {})
            maturity = conditions.get('maturity_level', '未知')
            
            suggestions.append(f"主要矛盾: {primary_contradiction}")
            suggestions.append(f"变革条件成熟度: {maturity}")
            if maturity in ['高度成熟', '比较成熟']:
                suggestions.append("社会变革条件较为成熟，关注实践路径")
            else:
                suggestions.append("变革条件尚未完全成熟，关注条件培育")
        
        return suggestions
    
    def _generate_quantitative_summary(self, quantitative_results: Dict) -> Dict:
        """生成定量结果摘要"""
        summary = {}
        
        # 提取关键指标
        for key, value in quantitative_results.items():
            if isinstance(value, dict) and 'score' in value:
                summary[key] = value['score']
            elif isinstance(value, (int, float)):
                summary[key] = value
        
        return summary
    
    def _assess_phase_quality(self, phase: str, quantitative_results: Dict) -> Dict:
        """评估阶段分析质量"""
        
        quality_metrics = quantitative_results.get('quality_metrics', {})
        
        # 基础质量分数
        base_quality = quality_metrics.get('overall_quality', 0)
        
        # 数据完整性评估
        completeness = self._assess_data_completeness(quantitative_results)
        
        # 逻辑一致性评估
        consistency = self._assess_logical_consistency(phase, quantitative_results)
        
        # 理论相关性评估
        theoretical_relevance = self._assess_theoretical_relevance(phase, quantitative_results)
        
        # 综合质量分数
        overall_quality = (
            base_quality * 0.4 +
            completeness * 0.2 +
            consistency * 0.2 +
            theoretical_relevance * 0.2
        )
        
        return {
            'base_quality': base_quality,
            'completeness': completeness,
            'consistency': consistency,
            'theoretical_relevance': theoretical_relevance,
            'overall_quality': overall_quality,
            'quality_level': self._determine_quality_level(overall_quality),
            'improvement_suggestions': self._generate_improvement_suggestions(phase, overall_quality)
        }
    
    def _assess_data_completeness(self, quantitative_results: Dict) -> float:
        """评估数据完整性"""
        required_fields = {
            'productivity_analysis': ['tool_level', 'technology_complexity', 'labor_efficiency'],
            'production_relations_analysis': ['ownership_form', 'labor_relations', 'distribution_method'],
            'superstructure_analysis': ['political_system', 'ideology', 'culture'],
            'social_change_analysis': ['basic_contradictions', 'change_conditions', 'change_drivers']
        }
        
        # 根据不同的分析类型确定必需字段
        missing_fields = 0
        total_fields = 0
        
        for analysis_type, fields in required_fields.items():
            for field in fields:
                total_fields += 1
                if field not in quantitative_results:
                    missing_fields += 1
        
        completeness = 1.0 - (missing_fields / total_fields) if total_fields > 0 else 0
        return completeness * 10  # 转换为10分制
    
    def _assess_logical_consistency(self, phase: str, quantitative_results: Dict) -> float:
        """评估逻辑一致性"""
        consistency_score = 8.0  # 基础分数
        
        # 检查不同部分之间的逻辑关系
        if phase == 'material_base':
            # 检查工具水平与技术复杂度的一致性
            tool_score = quantitative_results.get('tool_level', {}).get('confidence', 0)
            tech_score = quantitative_results.get('technology_complexity', {}).get('confidence', 0)
            
            if abs(tool_score - tech_score) > 5.0:
                consistency_score -= 2.0
        
        elif phase == 'production_relations':
            # 检查所有制与劳动关系的一致性
            ownership_score = quantitative_results.get('ownership_form', {}).get('confidence', 0)
            relation_score = quantitative_results.get('labor_relations', {}).get('confidence', 0)
            
            if abs(ownership_score - relation_score) > 5.0:
                consistency_score -= 2.0
        
        return max(consistency_score, 0)
    
    def _assess_theoretical_relevance(self, phase: str, quantitative_results: Dict) -> float:
        """评估理论相关性"""
        relevance_score = 8.0  # 基础分数
        
        # 检查是否包含马克思主义理论的核心要素
        key_concepts = {
            'material_base': ['生产力', '工具', '技术', '劳动'],
            'production_relations': ['所有制', '阶级', '分配', '剥削'],
            'superstructure': ['政治', '意识形态', '文化', '国家'],
            'social_change': ['矛盾', '变革', '发展', '革命']
        }
        
        phase_concepts = key_concepts.get(phase, [])
        concept_coverage = 0
        
        # 这里简化处理，实际应该检查文本中是否包含这些概念
        concept_coverage = len(phase_concepts) * 0.8  # 假设80%的概念被覆盖
        
        relevance_score = min(concept_coverage * 2, 10)
        
        return relevance_score
    
    def _determine_quality_level(self, overall_quality: float) -> str:
        """确定质量等级"""
        if overall_quality >= 8.0:
            return "优秀"
        elif overall_quality >= 6.0:
            return "良好"
        elif overall_quality >= 4.0:
            return "一般"
        else:
            return "需要改进"
    
    def _generate_improvement_suggestions(self, phase: str, overall_quality: float) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if overall_quality < 4.0:
            suggestions.append("分析质量较低，建议重新审视理论基础")
            suggestions.append("加强数据收集和分析的系统性")
        elif overall_quality < 6.0:
            suggestions.append("分析质量一般，建议深化理论分析")
            suggestions.append("关注不同分析维度的平衡性")
        elif overall_quality < 8.0:
            suggestions.append("分析质量良好，可进一步优化")
            suggestions.append("加强理论与实践的结合")
        else:
            suggestions.append("分析质量优秀，保持现有水平")
        
        return suggestions
    
    def _integrate_analysis_results(self, analysis_results: Dict) -> Dict:
        """整合分析结果"""
        
        # 提取各阶段的关键指标
        phase_summary = {}
        for phase, results in analysis_results.items():
            if results.get('phase_completed', False):
                quantitative = results.get('quantitative_results', {})
                quality = results.get('quality_assessment', {})
                
                phase_summary[phase] = {
                    'overall_score': quality.get('overall_quality', 0),
                    'key_indicators': self._extract_key_indicators(phase, quantitative),
                    'quality_level': quality.get('quality_level', '未知'),
                    'main_findings': self._extract_main_findings(phase, quantitative)
                }
        
        # 计算整体分析质量
        overall_quality = self._calculate_overall_quality(phase_summary)
        
        # 识别主要矛盾和趋势
        major_contradictions = self._identify_major_contradictions(analysis_results)
        development_trends = self._identify_development_trends(analysis_results)
        
        # 生成综合结论
        comprehensive_conclusions = self._generate_comprehensive_conclusions(
            phase_summary, major_contradictions, development_trends
        )
        
        return {
            'phase_summary': phase_summary,
            'overall_quality': overall_quality,
            'major_contradictions': major_contradictions,
            'development_trends': development_trends,
            'comprehensive_conclusions': comprehensive_conclusions,
            'integration_timestamp': datetime.now().isoformat()
        }
    
    def _extract_key_indicators(self, phase: str, quantitative_results: Dict) -> Dict:
        """提取关键指标"""
        indicators = {}
        
        if phase == 'material_base':
            indicators['productivity_stage'] = quantitative_results.get('productivity_stage', '未知')
            indicators['overall_productivity'] = quantitative_results.get('overall_productivity', 0)
        
        elif phase == 'production_relations':
            indicators['overall_relations'] = quantitative_results.get('overall_production_relations', 0)
            class_structure = quantitative_results.get('class_structure', {})
            indicators['class_conflict_intensity'] = class_structure.get('class_conflict_intensity', 0)
        
        elif phase == 'superstructure':
            indicators['overall_superstructure'] = quantitative_results.get('overall_superstructure', 0)
            economic_relation = quantitative_results.get('economic_base_relation', {})
            indicators['dominant_relation'] = economic_relation.get('dominant_relation', '未知')
        
        elif phase == 'social_change':
            contradictions = quantitative_results.get('basic_contradictions', {})
            indicators['primary_contradiction'] = contradictions.get('primary_contradiction', '未知')
            conditions = quantitative_results.get('change_conditions', {})
            indicators['condition_maturity'] = conditions.get('maturity_level', '未知')
        
        return indicators
    
    def _extract_main_findings(self, phase: str, quantitative_results: Dict) -> List[str]:
        """提取主要发现"""
        findings = []
        
        if phase == 'material_base':
            productivity_stage = quantitative_results.get('productivity_stage', '未知')
            findings.append(f"生产力处于{productivity_stage}阶段")
        
        elif phase == 'production_relations':
            class_structure = quantitative_results.get('class_structure', {})
            major_classes = class_structure.get('major_classes', [])
            if major_classes:
                findings.append(f"主要阶级包括: {', '.join(major_classes)}")
        
        elif phase == 'superstructure':
            political_system = quantitative_results.get('political_system', {})
            dominant_system = political_system.get('dominant_system', '未知')
            findings.append(f"政治制度以{dominant_system}为主导")
        
        elif phase == 'social_change':
            contradictions = quantitative_results.get('basic_contradictions', {})
            primary_contradiction = contradictions.get('primary_contradiction', '未知')
            findings.append(f"主要矛盾是{primary_contradiction}")
        
        return findings
    
    def _calculate_overall_quality(self, phase_summary: Dict) -> Dict:
        """计算整体分析质量"""
        quality_scores = [summary.get('overall_score', 0) for summary in phase_summary.values()]
        
        if not quality_scores:
            return {'average_quality': 0, 'quality_level': '未知'}
        
        average_quality = sum(quality_scores) / len(quality_scores)
        
        # 质量等级
        if average_quality >= 8.0:
            quality_level = "优秀"
        elif average_quality >= 6.0:
            quality_level = "良好"
        elif average_quality >= 4.0:
            quality_level = "一般"
        else:
            quality_level = "需要改进"
        
        return {
            'average_quality': average_quality,
            'quality_level': quality_level,
            'phase_scores': dict(zip(phase_summary.keys(), quality_scores)),
            'completed_phases': len(phase_summary),
            'total_phases': 4
        }
    
    def _identify_major_contradictions(self, analysis_results: Dict) -> List[str]:
        """识别主要矛盾"""
        contradictions = []
        
        # 从社会变革分析中提取矛盾信息
        social_change_results = analysis_results.get('social_change', {})
        quantitative_results = social_change_results.get('quantitative_results', {})
        
        basic_contradictions = quantitative_results.get('basic_contradictions', {})
        primary_contradiction = basic_contradictions.get('primary_contradiction', '未知')
        
        if primary_contradiction != '未知':
            contradictions.append(f"主要矛盾: {primary_contradiction}")
        
        # 从生产关系分析中提取阶级矛盾
        production_relations_results = analysis_results.get('production_relations', {})
        pr_quantitative = production_relations_results.get('quantitative_results', {})
        
        class_structure = pr_quantitative.get('class_structure', {})
        conflict_intensity = class_structure.get('class_conflict_intensity', 0)
        
        if conflict_intensity > 3.0:
            contradictions.append("阶级矛盾较为突出")
        
        return contradictions
    
    def _identify_development_trends(self, analysis_results: Dict) -> List[str]:
        """识别发展趋势"""
        trends = []
        
        # 从社会变革分析中提取趋势
        social_change_results = analysis_results.get('social_change', {})
        quantitative_results = social_change_results.get('quantitative_results', {})
        
        development_trends = quantitative_results.get('development_trends', {})
        primary_trend = development_trends.get('primary_trend', '未知')
        
        if primary_trend != '未知':
            trends.append(f"主要发展趋势: {primary_trend}")
        
        # 从生产力分析中提取发展趋势
        material_base_results = analysis_results.get('material_base', {})
        mb_quantitative = material_base_results.get('quantitative_results', {})
        
        productivity_stage = mb_quantitative.get('productivity_stage', '未知')
        trends.append(f"生产力发展趋势: {productivity_stage}")
        
        return trends
    
    def _generate_comprehensive_conclusions(self, phase_summary: Dict, major_contradictions: List[str], development_trends: List[str]) -> List[str]:
        """生成综合结论"""
        conclusions = []
        
        # 基于各阶段分析生成结论
        material_base = phase_summary.get('material_base', {})
        if material_base:
            productivity_stage = material_base.get('key_indicators', {}).get('productivity_stage', '未知')
            conclusions.append(f"社会生产力处于{productivity_stage}阶段")
        
        production_relations = phase_summary.get('production_relations', {})
        if production_relations:
            conflict_intensity = production_relations.get('key_indicators', {}).get('class_conflict_intensity', 0)
            if conflict_intensity > 3.0:
                conclusions.append("阶级矛盾是社会发展的主要动力")
        
        superstructure = phase_summary.get('superstructure', {})
        if superstructure:
            dominant_relation = superstructure.get('key_indicators', {}).get('dominant_relation', '未知')
            conclusions.append(f"上层建筑与经济基础呈现{dominant_relation}关系")
        
        # 添加主要矛盾和发展趋势结论
        conclusions.extend(major_contradictions)
        conclusions.extend(development_trends)
        
        return conclusions
    
    def _generate_comprehensive_report(self, integrated_results: Dict) -> str:
        """生成综合报告"""
        report = []
        report.append("# 数字马克思社会学分析综合报告\n")
        
        # 总体质量评估
        overall_quality = integrated_results.get('overall_quality', {})
        report.append("## 总体评估")
        report.append(f"- 整体质量分数: {overall_quality.get('average_quality', 0):.2f}/10")
        report.append(f"- 质量等级: {overall_quality.get('quality_level', '未知')}")
        report.append(f"- 完成阶段: {overall_quality.get('completed_phases', 0)}/{overall_quality.get('total_phases', 4)}")
        report.append("")
        
        # 各阶段分析结果
        phase_summary = integrated_results.get('phase_summary', {})
        report.append("## 各阶段分析结果")
        
        for phase, summary in phase_summary.items():
            phase_name = self.analysis_phases.get(phase, {}).get('name', phase)
            report.append(f"### {phase_name}")
            report.append(f"- 质量分数: {summary.get('overall_score', 0):.2f}/10")
            report.append(f"- 质量等级: {summary.get('quality_level', '未知')}")
            
            # 关键指标
            key_indicators = summary.get('key_indicators', {})
            if key_indicators:
                report.append("- 关键指标:")
                for indicator, value in key_indicators.items():
                    report.append(f"  - {indicator}: {value}")
            
            # 主要发现
            main_findings = summary.get('main_findings', [])
            if main_findings:
                report.append("- 主要发现:")
                for finding in main_findings:
                    report.append(f"  - {finding}")
            
            report.append("")
        
        # 主要矛盾和发展趋势
        major_contradictions = integrated_results.get('major_contradictions', [])
        if major_contradictions:
            report.append("## 主要矛盾")
            for contradiction in major_contradictions:
                report.append(f"- {contradiction}")
            report.append("")
        
        development_trends = integrated_results.get('development_trends', [])
        if development_trends:
            report.append("## 发展趋势")
            for trend in development_trends:
                report.append(f"- {trend}")
            report.append("")
        
        # 综合结论
        comprehensive_conclusions = integrated_results.get('comprehensive_conclusions', [])
        if comprehensive_conclusions:
            report.append("## 综合结论")
            for conclusion in comprehensive_conclusions:
                report.append(f"- {conclusion}")
            report.append("")
        
        # 分析时间戳
        integration_timestamp = integrated_results.get('integration_timestamp', '')
        if integration_timestamp:
            report.append("## 分析时间")
            report.append(f"- 完成时间: {integration_timestamp}")
        
        return "\n".join(report)
    
    def _update_analysis_history(self, integrated_results: Dict):
        """更新分析历史"""
        history_entry = {
            'timestamp': datetime.now().isoformat(),
            'overall_quality': integrated_results.get('overall_quality', {}),
            'completed_phases': len(integrated_results.get('phase_summary', {})),
            'major_contradictions': integrated_results.get('major_contradictions', []),
            'development_trends': integrated_results.get('development_trends', [])
        }
        
        self.analysis_history.append(history_entry)
    
    def _get_analysis_metadata(self) -> Dict:
        """获取分析元数据"""
        return {
            'analysis_id': f"marx_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            'start_time': self.analysis_state.get('start_time', '').isoformat() if self.analysis_state.get('start_time') else '',
            'end_time': datetime.now().isoformat(),
            'completed_phases': self.analysis_state.get('completed_phases', []),
            'quality_scores': self.analysis_state.get('quality_scores', {}),
            'warnings': self.analysis_state.get('warnings', []),
            'errors': self.analysis_state.get('errors', []),
            'analysis_history_count': len(self.analysis_history)
        }
    
    def save_analysis_results(self, results: Dict, output_file: str = None) -> str:
        """保存分析结果"""
        if output_file is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"marx_analysis_results_{timestamp}.json"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2, default=str)
            
            return output_file
            
        except Exception as e:
            error_msg = f"保存分析结果失败: {str(e)}"
            self.analysis_state['errors'].append(error_msg)
            return ""
    
    def load_analysis_results(self, input_file: str) -> Dict:
        """加载分析结果"""
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                results = json.load(f)
            
            return results
            
        except Exception as e:
            error_msg = f"加载分析结果失败: {str(e)}"
            self.analysis_state['errors'].append(error_msg)
            return {}


def main():
    """测试集成分析引擎"""
    analyzer = DigitalMarxIntegratedAnalyzer()
    
    test_text = """
    在当代中国社会，生产力发展迅速，特别是数字技术和人工智能的广泛应用，
    推动了社会生产力的跨越式发展。智能制造、数字经济、平台经济等新业态
    不断涌现，劳动生产率显著提升。
    
    生产资料所有制坚持公有制为主体、多种所有制经济共同发展的基本经济制度。
    国有经济发挥主导作用，民营经济蓬勃发展，形成了多元化的所有制结构。
    劳动关系呈现出新的特点，传统的雇佣关系与新兴的平台经济、零工经济并存。
    收入分配制度坚持按劳分配为主体、多种分配方式并存，效率与公平并重。
    
    政治制度坚持中国特色社会主义政治发展道路，发展全过程人民民主。
    意识形态领域坚持马克思主义指导地位，培育和践行社会主义核心价值观。
    传统文化得到创造性转化和创新性发展，形成了开放包容的社会主义先进文化。
    
    社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾。
    改革开放不断深化，国家治理体系和治理能力现代化稳步推进。
    """
    
    print("=== 数字马克思集成分析引擎测试 ===")
    
    # 执行完整分析
    results = analyzer.execute_comprehensive_analysis(test_text)
    
    # 显示结果摘要
    integrated_results = results.get('integrated_results', {})
    overall_quality = integrated_results.get('overall_quality', {})
    
    print(f"\n整体质量分数: {overall_quality.get('average_quality', 0):.2f}/10")
    print(f"质量等级: {overall_quality.get('quality_level', '未知')}")
    print(f"完成阶段: {overall_quality.get('completed_phases', 0)}/4")
    
    # 显示主要矛盾和发展趋势
    major_contradictions = integrated_results.get('major_contradictions', [])
    if major_contradictions:
        print("\n主要矛盾:")
        for contradiction in major_contradictions:
            print(f"- {contradiction}")
    
    development_trends = integrated_results.get('development_trends', [])
    if development_trends:
        print("\n发展趋势:")
        for trend in development_trends:
            print(f"- {trend}")
    
    # 保存分析结果
    output_file = analyzer.save_analysis_results(results)
    if output_file:
        print(f"\n分析结果已保存到: {output_file}")
    
    # 显示综合报告
    comprehensive_report = results.get('comprehensive_report', '')
    if comprehensive_report:
        print(f"\n{comprehensive_report}")


if __name__ == "__main__":
    main()