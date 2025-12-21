#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
韦伯社会学分析器 - 基于韦伯理论的量化分析工具
提供社会行动类型学分析、理性化过程研究、权威合法性分析等计算功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import re
from collections import Counter
import warnings


class WeberianAnalyzer:
    """韦伯社会学分析器类"""
    
    def __init__(self):
        self.analysis_results = {}
        self.quality_metrics = {}
        
    def analyze_social_action_typology(self, text_data: str, 
                                     context: Dict = None) -> Dict:
        """
        分析社会行动类型学
        
        Parameters:
        -----------
        text_data : str
            待分析的文本数据
        context : Dict
            分析上下文信息
            
        Returns:
        --------
        Dict : 社会行动类型学分析结果
        """
        # 目的理性分析
        purposive_rationality = self._analyze_purposive_rationality(text_data)
        
        # 价值理性分析
        value_rationality = self._analyze_value_rationality(text_data)
        
        # 情感性分析
        affective_action = self._analyze_affective_action(text_data)
        
        # 传统性分析
        traditional_action = self._analyze_traditional_action(text_data)
        
        # 行动类型判断
        action_type = self._determine_action_type(
            purposive_rationality, value_rationality, 
            affective_action, traditional_action
        )
        
        results = {
            'action_type': action_type,
            'purposive_rationality': purposive_rationality,
            'value_rationality': value_rationality,
            'affective_action': affective_action,
            'traditional_action': traditional_action,
            'rationality_score': self._calculate_rationality_score(
                purposive_rationality, value_rationality
            ),
            'meaning_structure': self._analyze_meaning_structure(text_data),
            'quality_metrics': self._assess_action_typology_quality(
                purposive_rationality, value_rationality, 
                affective_action, traditional_action
            )
        }
        
        self.analysis_results['social_action_typology'] = results
        return results
    
    def analyze_rationalization_process(self, text_data: str,
                                      modernity_context: Dict = None) -> Dict:
        """
        分析理性化过程
        
        Parameters:
        -----------
        text_data : str
            待分析的文本数据
        modernity_context : Dict
            现代性背景信息
            
        Returns:
        --------
        Dict : 理性化过程分析结果
        """
        # 除魅过程分析
        disenchantment = self._analyze_disenchantment(text_data)
        
        # 形式理性评估
        formal_rationality = self._analyze_formal_rationality(text_data)
        
        # 实质理性识别
        substantive_rationality = self._analyze_substantive_rationality(text_data)
        
        # 理性化冲突分析
        rationality_conflicts = self._analyze_rationality_conflicts(text_data)
        
        results = {
            'disenchantment': disenchantment,
            'formal_rationality': formal_rationality,
            'substantive_rationality': substantive_rationality,
            'rationality_conflicts': rationality_conflicts,
            'rationalization_index': self._calculate_rationalization_index(
                disenchantment, formal_rationality, substantive_rationality
            ),
            'modernization_level': self._assess_modernization_level(
                disenchantment, formal_rationality
            ),
            'quality_metrics': self._evaluate_rationalization_quality(
                disenchantment, formal_rationality, substantive_rationality
            )
        }
        
        self.analysis_results['rationalization_process'] = results
        return results
    
    def analyze_authority_legitimacy(self, text_data: str,
                                    political_context: Dict = None) -> Dict:
        """
        分析权威合法性
        
        Parameters:
        -----------
        text_data : str
            待分析的文本数据
        political_context : Dict
            政治背景信息
            
        Returns:
        --------
        Dict : 权威合法性分析结果
        """
        # 传统型权威分析
        traditional_authority = self._analyze_traditional_authority(text_data)
        
        # 魅力型权威分析
        charismatic_authority = self._analyze_charismatic_authority(text_data)
        
        # 法理型权威分析
        legal_rational_authority = self._analyze_legal_rational_authority(text_data)
        
        # 权威类型判断
        authority_type = self._determine_authority_type(
            traditional_authority, charismatic_authority, legal_rational_authority
        )
        
        results = {
            'authority_type': authority_type,
            'traditional_authority': traditional_authority,
            'charismatic_authority': charismatic_authority,
            'legal_rational_authority': legal_rational_authority,
            'legitimacy_base': self._analyze_legitimacy_base(text_data),
            'authority_stability': self._assess_authority_stability(
                traditional_authority, charismatic_authority, legal_rational_authority
            ),
            'quality_metrics': self._evaluate_authority_analysis_quality(
                traditional_authority, charismatic_authority, legal_rational_authority
            )
        }
        
        self.analysis_results['authority_legitimacy'] = results
        return results
    
    def analyze_bureaucracy_modernity(self, text_data: str,
                                    organizational_context: Dict = None) -> Dict:
        """
        分析科层制与现代性
        
        Parameters:
        -----------
        text_data : str
            待分析的文本数据
        organizational_context : Dict
            组织背景信息
            
        Returns:
        --------
        Dict : 科层制与现代性分析结果
        """
        # 组织效率评估
        organizational_efficiency = self._analyze_organizational_efficiency(text_data)
        
        # 非人格化程度测量
        impersonalization = self._analyze_impersonalization(text_data)
        
        # 现代性困境诊断
        modernity_dilemma = self._diagnose_modernity_dilemma(text_data)
        
        # "铁笼"现象分析
        iron_cage = self._analyze_iron_cage(text_data)
        
        results = {
            'organizational_efficiency': organizational_efficiency,
            'impersonalization': impersonalization,
            'modernity_dilemma': modernity_dilemma,
            'iron_cage': iron_cage,
            'bureaucracy_index': self._calculate_bureaucracy_index(
                organizational_efficiency, impersonalization
            ),
            'modernity_level': self._assess_modernity_level(
                organizational_efficiency, modernity_dilemma
            ),
            'quality_metrics': self._evaluate_bureaucracy_analysis_quality(
                organizational_efficiency, impersonalization, modernity_dilemma
            )
        }
        
        self.analysis_results['bureaucracy_modernity'] = results
        return results
    
    def _analyze_purposive_rationality(self, text_data: str) -> Dict:
        """分析目的理性"""
        purposive_indicators = [
            '目标', '目的', '效率', '效果', '计算', '规划', '策略',
            '优化', '选择', '决策', '手段', '工具', '理性', '利益'
        ]
        
        score = 0.0
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0.0, 'level': '低', 'evidence': []}
            
        for indicator in purposive_indicators:
            count = text_data.count(indicator)
            score += count * 1.0
            
        # 提取证据
        evidence = self._extract_purposive_evidence(text_data)
        
        return {
            'score': min(score / total_words * 10, 10.0),
            'level': self._score_to_level(score / total_words * 10),
            'evidence': evidence
        }
    
    def _analyze_value_rationality(self, text_data: str) -> Dict:
        """分析价值理性"""
        value_indicators = [
            '价值', '信念', '理想', '原则', '道德', '伦理', '责任',
            '义务', '使命', '信仰', '理念', '追求', '坚持', '奉献'
        ]
        
        score = 0.0
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0.0, 'level': '低', 'evidence': []}
            
        for indicator in value_indicators:
            count = text_data.count(indicator)
            score += count * 1.2
            
        evidence = self._extract_value_evidence(text_data)
        
        return {
            'score': min(score / total_words * 10, 10.0),
            'level': self._score_to_level(score / total_words * 10),
            'evidence': evidence
        }
    
    def _analyze_affective_action(self, text_data: str) -> Dict:
        """分析情感性行动"""
        affective_indicators = [
            '情感', '情绪', '感觉', '感受', '冲动', '激情', '热爱',
            '愤怒', '恐惧', '喜悦', '悲伤', '情感', '心情', '体验'
        ]
        
        score = 0.0
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0.0, 'level': '低', 'evidence': []}
            
        for indicator in affective_indicators:
            count = text_data.count(indicator)
            score += count * 1.1
            
        evidence = self._extract_affective_evidence(text_data)
        
        return {
            'score': min(score / total_words * 10, 10.0),
            'level': self._score_to_level(score / total_words * 10),
            'evidence': evidence
        }
    
    def _analyze_traditional_action(self, text_data: str) -> Dict:
        """分析传统性行动"""
        traditional_indicators = [
            '传统', '习惯', '习俗', '惯例', '常规', '历史', '传承',
            '古老', '传统', '沿袭', '遵循', '守旧', '传统', '经典'
        ]
        
        score = 0.0
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0.0, 'level': '低', 'evidence': []}
            
        for indicator in traditional_indicators:
            count = text_data.count(indicator)
            score += count * 1.0
            
        evidence = self._extract_traditional_evidence(text_data)
        
        return {
            'score': min(score / total_words * 10, 10.0),
            'level': self._score_to_level(score / total_words * 10),
            'evidence': evidence
        }
    
    def _determine_action_type(self, purposive: Dict, value: Dict, 
                             affective: Dict, traditional: Dict) -> str:
        """确定行动类型"""
        scores = {
            '目的理性': purposive['score'],
            '价值理性': value['score'],
            '情感性': affective['score'],
            '传统性': traditional['score']
        }
        
        max_score = max(scores.values())
        dominant_type = max(scores, key=scores.get)
        
        # 检查是否有明显的混合类型
        second_max = sorted(scores.values())[-2]
        if abs(max_score - second_max) < 1.0:
            return f"混合型({dominant_type}主导)"
        
        return dominant_type
    
    def _calculate_rationality_score(self, purposive: Dict, value: Dict) -> float:
        """计算理性分数"""
        return (purposive['score'] + value['score']) / 2.0
    
    def _analyze_meaning_structure(self, text_data: str) -> Dict:
        """分析意义结构"""
        meaning_indicators = {
            '工具意义': ['工具', '手段', '方法', '途径', '方式'],
            '价值意义': ['价值', '意义', '目的', '理想', '追求'],
            '情感意义': ['感受', '体验', '情感', '心情', '感觉'],
            '社会意义': ['社会', '群体', '关系', '地位', '角色']
        }
        
        meaning_structure = {}
        for meaning_type, indicators in meaning_indicators.items():
            count = sum(text_data.count(indicator) for indicator in indicators)
            meaning_structure[meaning_type] = {
                'frequency': count,
                'prominence': '高' if count >= 3 else '中' if count >= 1 else '低'
            }
            
        return meaning_structure
    
    def _assess_action_typology_quality(self, purposive: Dict, value: Dict,
                                     affective: Dict, traditional: Dict) -> Dict:
        """评估行动类型学分析质量"""
        return {
            'completeness': len([r for r in [purposive, value, affective, traditional] 
                               if r['score'] > 0]) / 4.0,
            'balance': self._calculate_balance(purposive, value, affective, traditional),
            'clarity': max(purposive['score'], value['score'], affective['score'], traditional['score']) / 10.0,
            'overall_quality': (purposive['score'] + value['score'] + affective['score'] + traditional['score']) / 40.0
        }
    
    def _analyze_disenchantment(self, text_data: str) -> Dict:
        """分析除魅过程"""
        disenchantment_indicators = [
            '理性', '科学', '世俗', '理性化', '现代化', '除魅',
            '去神秘化', '理性', '科学化', '世俗化', '理性'
        ]
        
        score = sum(text_data.count(indicator) for indicator in disenchantment_indicators)
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0.0, 'level': '低'}
            
        normalized_score = min(score / total_words * 10, 10.0)
        
        return {
            'score': normalized_score,
            'level': self._score_to_level(normalized_score),
            'indicators_found': score
        }
    
    def _analyze_formal_rationality(self, text_data: str) -> Dict:
        """分析形式理性"""
        formal_indicators = [
            '规则', '程序', '制度', '法律', '规范', '标准',
            '程序', '规则', '制度', '法律', '形式', '规范'
        ]
        
        score = sum(text_data.count(indicator) for indicator in formal_indicators)
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0.0, 'level': '低'}
            
        normalized_score = min(score / total_words * 10, 10.0)
        
        return {
            'score': normalized_score,
            'level': self._score_to_level(normalized_score),
            'procedural_elements': score
        }
    
    def _analyze_substantive_rationality(self, text_data: str) -> Dict:
        """分析实质理性"""
        substantive_indicators = [
            '价值', '伦理', '道德', '正义', '公平', '善',
            '价值', '伦理', '道德', '正义', '善', '目的'
        ]
        
        score = sum(text_data.count(indicator) for indicator in substantive_indicators)
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0.0, 'level': '低'}
            
        normalized_score = min(score / total_words * 10, 10.0)
        
        return {
            'score': normalized_score,
            'level': self._score_to_level(normalized_score),
            'value_elements': score
        }
    
    def _analyze_rationality_conflicts(self, text_data: str) -> Dict:
        """分析理性化冲突"""
        conflict_indicators = [
            '冲突', '矛盾', '张力', '对立', '冲突', '悖论',
            '矛盾', '冲突', '张力', '对立', '悖论'
        ]
        
        score = sum(text_data.count(indicator) for indicator in conflict_indicators)
        
        return {
            'conflict_intensity': score,
            'conflict_level': '高' if score >= 5 else '中' if score >= 2 else '低',
            'conflict_types': ['工具理性与价值理性冲突', '形式理性与实质理性冲突']
        }
    
    def _calculate_rationalization_index(self, disenchantment: Dict,
                                       formal: Dict, substantive: Dict) -> float:
        """计算理性化指数"""
        return (disenchantment['score'] + formal['score'] + substantive['score']) / 3.0
    
    def _assess_modernization_level(self, disenchantment: Dict,
                                  formal: Dict) -> float:
        """评估现代化水平"""
        return (disenchantment['score'] + formal['score']) / 2.0
    
    def _evaluate_rationalization_quality(self, disenchantment: Dict,
                                        formal: Dict, substantive: Dict) -> Dict:
        """评估理性化分析质量"""
        return {
            'completeness': len([r for r in [disenchantment, formal, substantive] 
                               if r['score'] > 0]) / 3.0,
            'balance': min(disenchantment['score'], formal['score'], substantive['score']) / 10.0,
            'depth': (disenchantment['score'] + formal['score'] + substantive['score']) / 30.0
        }
    
    def _analyze_traditional_authority(self, text_data: str) -> Dict:
        """分析传统型权威"""
        traditional_indicators = [
            '传统', '习俗', '习惯', '历史', '世袭', '传统',
            '惯例', '传统', '习俗', '历史', '世袭'
        ]
        
        score = sum(text_data.count(indicator) for indicator in traditional_indicators)
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0.0, 'level': '低'}
            
        normalized_score = min(score / total_words * 10, 10.0)
        
        return {
            'score': normalized_score,
            'level': self._score_to_level(normalized_score),
            'traditional_elements': score
        }
    
    def _analyze_charismatic_authority(self, text_data: str) -> Dict:
        """分析魅力型权威"""
        charismatic_indicators = [
            '魅力', '个人', '领袖', '崇拜', '追随', '魅力',
            '个人魅力', '领袖', '崇拜', '追随', '感召'
        ]
        
        score = sum(text_data.count(indicator) for indicator in charismatic_indicators)
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0.0, 'level': '低'}
            
        normalized_score = min(score / total_words * 10, 10.0)
        
        return {
            'score': normalized_score,
            'level': self._score_to_level(normalized_score),
            'charismatic_elements': score
        }
    
    def _analyze_legal_rational_authority(self, text_data: str) -> Dict:
        """分析法理型权威"""
        legal_indicators = [
            '法律', '规则', '制度', '程序', '合法', '理性',
            '法律', '规则', '制度', '程序', '合法性'
        ]
        
        score = sum(text_data.count(indicator) for indicator in legal_indicators)
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0.0, 'level': '低'}
            
        normalized_score = min(score / total_words * 10, 10.0)
        
        return {
            'score': normalized_score,
            'level': self._score_to_level(normalized_score),
            'legal_elements': score
        }
    
    def _determine_authority_type(self, traditional: Dict, charismatic: Dict,
                                legal: Dict) -> str:
        """确定权威类型"""
        scores = {
            '传统型权威': traditional['score'],
            '魅力型权威': charismatic['score'],
            '法理型权威': legal['score']
        }
        
        max_score = max(scores.values())
        dominant_type = max(scores, key=scores.get)
        
        # 检查混合类型
        second_max = sorted(scores.values())[-2]
        if abs(max_score - second_max) < 1.0:
            return f"混合型权威({dominant_type}主导)"
        
        return dominant_type
    
    def _analyze_legitimacy_base(self, text_data: str) -> Dict:
        """分析合法性基础"""
        legitimacy_indicators = {
            '传统合法性': ['传统', '习俗', '历史', '惯例'],
            '魅力合法性': ['魅力', '个人', '崇拜', '追随'],
            '法理合法性': ['法律', '规则', '程序', '制度'],
            '绩效合法性': ['效果', '效率', '成果', '绩效']
        }
        
        legitimacy_base = {}
        for leg_type, indicators in legitimacy_indicators.items():
            count = sum(text_data.count(indicator) for indicator in indicators)
            legitimacy_base[leg_type] = {
                'strength': count,
                'level': '强' if count >= 3 else '中' if count >= 1 else '弱'
            }
            
        return legitimacy_base
    
    def _assess_authority_stability(self, traditional: Dict, charismatic: Dict,
                                  legal: Dict) -> Dict:
        """评估权威稳定性"""
        # 传统型权威最稳定，法理型次之，魅力型最不稳定
        stability_scores = {
            '传统型权威': traditional['score'] * 1.2,
            '法理型权威': legal['score'] * 1.0,
            '魅力型权威': charismatic['score'] * 0.8
        }
        
        overall_stability = sum(stability_scores.values()) / len(stability_scores)
        
        return {
            'overall_stability': overall_stability,
            'stability_level': self._score_to_level(overall_stability),
            'stability_factors': stability_scores
        }
    
    def _evaluate_authority_analysis_quality(self, traditional: Dict,
                                           charismatic: Dict, legal: Dict) -> Dict:
        """评估权威分析质量"""
        return {
            'completeness': len([r for r in [traditional, charismatic, legal] 
                               if r['score'] > 0]) / 3.0,
            'balance': min(traditional['score'], charismatic['score'], legal['score']) / 10.0,
            'clarity': max(traditional['score'], charismatic['score'], legal['score']) / 10.0
        }
    
    def _analyze_organizational_efficiency(self, text_data: str) -> Dict:
        """分析组织效率"""
        efficiency_indicators = [
            '效率', '效果', '绩效', '优化', '改进', '提升',
            '效率', '效果', '绩效', '优化', '改进'
        ]
        
        score = sum(text_data.count(indicator) for indicator in efficiency_indicators)
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0.0, 'level': '低'}
            
        normalized_score = min(score / total_words * 10, 10.0)
        
        return {
            'score': normalized_score,
            'level': self._score_to_level(normalized_score),
            'efficiency_indicators': score
        }
    
    def _analyze_impersonalization(self, text_data: str) -> Dict:
        """分析非人格化程度"""
        impersonal_indicators = [
            '客观', '公正', '中立', '非人格化', '制度', '规则',
            '客观', '公正', '中立', '非人格化', '制度'
        ]
        
        score = sum(text_data.count(indicator) for indicator in impersonal_indicators)
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return {'score': 0.0, 'level': '低'}
            
        normalized_score = min(score / total_words * 10, 10.0)
        
        return {
            'score': normalized_score,
            'level': self._score_to_level(normalized_score),
            'impersonal_elements': score
        }
    
    def _diagnose_modernity_dilemma(self, text_data: str) -> Dict:
        """诊断现代性困境"""
        dilemma_indicators = [
            '困境', '悖论', '矛盾', '冲突', '问题', '挑战',
            '困境', '悖论', '矛盾', '冲突', '铁笼'
        ]
        
        score = sum(text_data.count(indicator) for indicator in dilemma_indicators)
        
        return {
            'dilemma_intensity': score,
            'dilemma_level': '高' if score >= 5 else '中' if score >= 2 else '低',
            'dilemma_types': ['理性化悖论', '自由与秩序冲突', '效率与人性的张力']
        }
    
    def _analyze_iron_cage(self, text_data: str) -> Dict:
        """分析"铁笼"现象"""
        iron_cage_indicators = [
            '铁笼', '束缚', '禁锢', '限制', '枷锁', '牢笼',
            '铁笼', '束缚', '禁锢', '限制', '官僚化'
        ]
        
        score = sum(text_data.count(indicator) for indicator in iron_cage_indicators)
        
        return {
            'iron_cage_intensity': score,
            'iron_cage_level': '高' if score >= 3 else '中' if score >= 1 else '低',
            'manifestations': ['理性化束缚', '官僚化限制', '制度化约束']
        }
    
    def _calculate_bureaucracy_index(self, efficiency: Dict, 
                                   impersonalization: Dict) -> float:
        """计算科层制指数"""
        return (efficiency['score'] + impersonalization['score']) / 2.0
    
    def _assess_modernity_level(self, efficiency: Dict, 
                              dilemma: Dict) -> Dict:
        """评估现代性水平"""
        modernity_score = efficiency['score']
        
        return {
            'modernity_score': modernity_score,
            'modernity_level': self._score_to_level(modernity_score),
            'dilemma_impact': dilemma['dilemma_level']
        }
    
    def _evaluate_bureaucracy_analysis_quality(self, efficiency: Dict,
                                             impersonalization: Dict, 
                                             dilemma: Dict) -> Dict:
        """评估科层制分析质量"""
        return {
            'completeness': len([r for r in [efficiency, impersonalization, dilemma] 
                               if r.get('score', 0) > 0 or r.get('dilemma_intensity', 0) > 0]) / 3.0,
            'balance': min(efficiency['score'], impersonalization['score']) / 10.0,
            'depth': (efficiency['score'] + impersonalization['score']) / 20.0
        }
    
    def _score_to_level(self, score: float) -> str:
        """将分数转换为等级"""
        if score >= 7.0:
            return "高"
        elif score >= 4.0:
            return "中"
        else:
            return "低"
    
    def _extract_purposive_evidence(self, text_data: str) -> List[str]:
        """提取目的理性证据"""
        evidence = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if any(indicator in sentence for indicator in ['目标', '目的', '效率', '效果']):
                evidence.append(sentence.strip())
                
        return evidence[:3]
    
    def _extract_value_evidence(self, text_data: str) -> List[str]:
        """提取价值理性证据"""
        evidence = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if any(indicator in sentence for indicator in ['价值', '信念', '理想', '原则']):
                evidence.append(sentence.strip())
                
        return evidence[:3]
    
    def _extract_affective_evidence(self, text_data: str) -> List[str]:
        """提取情感性证据"""
        evidence = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if any(indicator in sentence for indicator in ['情感', '情绪', '感觉', '感受']):
                evidence.append(sentence.strip())
                
        return evidence[:3]
    
    def _extract_traditional_evidence(self, text_data: str) -> List[str]:
        """提取传统性证据"""
        evidence = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if any(indicator in sentence for indicator in ['传统', '习惯', '习俗', '惯例']):
                evidence.append(sentence.strip())
                
        return evidence[:3]
    
    def _calculate_balance(self, purposive: Dict, value: Dict,
                          affective: Dict, traditional: Dict) -> float:
        """计算平衡度"""
        scores = [purposive['score'], value['score'], affective['score'], traditional['score']]
        max_score = max(scores)
        min_score = min(scores)
        
        return 1.0 - (max_score - min_score) / 10.0
    
    def generate_comprehensive_report(self) -> str:
        """生成综合分析报告"""
        report = []
        report.append("# 数字韦伯社会学分析报告\n")
        
        if 'social_action_typology' in self.analysis_results:
            results = self.analysis_results['social_action_typology']
            report.append("## 社会行动类型学分析")
            report.append(f"**行动类型**: {results['action_type']}")
            report.append(f"**理性分数**: {results['rationality_score']:.2f}")
            
            action_types = ['目的理性', '价值理性', '情感性', '传统性']
            for action_type in action_types:
                if action_type in results:
                    data = results[action_type]
                    report.append(f"**{action_type}**: {data['level']} (分数: {data['score']:.2f})")
            report.append("")
        
        if 'rationalization_process' in self.analysis_results:
            results = self.analysis_results['rationalization_process']
            report.append("## 理性化过程分析")
            report.append(f"**理性化指数**: {results['rationalization_index']:.2f}")
            report.append(f"**现代化水平**: {results['modernization_level']}")
            
            rationalization_aspects = ['disenchantment', 'formal_rationality', 'substantive_rationality']
            for aspect in rationalization_aspects:
                if aspect in results:
                    data = results[aspect]
                    report.append(f"**{aspect}**: {data['level']} (分数: {data['score']:.2f})")
            report.append("")
        
        if 'authority_legitimacy' in self.analysis_results:
            results = self.analysis_results['authority_legitimacy']
            report.append("## 权威合法性分析")
            report.append(f"**权威类型**: {results['authority_type']}")
            
            authority_types = ['traditional_authority', 'charismatic_authority', 'legal_rational_authority']
            for authority_type in authority_types:
                if authority_type in results:
                    data = results[authority_type]
                    report.append(f"**{authority_type}**: {data['level']} (分数: {data['score']:.2f})")
            report.append("")
        
        if 'bureaucracy_modernity' in self.analysis_results:
            results = self.analysis_results['bureaucracy_modernity']
            report.append("## 科层制与现代性分析")
            report.append(f"**科层制指数**: {results['bureaucracy_index']:.2f}")
            report.append(f"**现代性水平**: {results['modernity_level']['modernity_level']}")
            
            bureaucracy_aspects = ['organizational_efficiency', 'impersonalization']
            for aspect in bureaucracy_aspects:
                if aspect in results:
                    data = results[aspect]
                    report.append(f"**{aspect}**: {data['level']} (分数: {data['score']:.2f})")
            report.append("")
        
        return "\n".join(report)


def main():
    """示例用法"""
    analyzer = WeberianAnalyzer()
    
    # 示例文本数据
    sample_text = """
    现代官僚组织作为一种理性的组织形式，追求效率最大化和程序规范化。
    组织成员按照明确的规则和程序行动，个人的情感和偏好被排除在决策过程之外。
    这种非人格化的管理方式确保了组织的公正性和效率。
    
    然而，过度的理性化也带来了现代性的困境。组织成员被束缚在"铁笼"之中，
    失去了个性和自由。工具理性的过度发展压制了价值理性的空间，
    导致了意义危机和精神空虚。
    
    在权威类型方面，现代组织主要依靠法理型权威，
    通过合法的规则和程序来维持秩序。但这种权威也面临着挑战，
    需要在效率与人性之间找到平衡。
    """
    
    # 执行完整分析
    print("=== 社会行动类型学分析 ===")
    action_results = analyzer.analyze_social_action_typology(sample_text)
    print(f"行动类型: {action_results['action_type']}")
    print(f"理性分数: {action_results['rationality_score']:.2f}")
    
    print("\n=== 理性化过程分析 ===")
    rationalization_results = analyzer.analyze_rationalization_process(sample_text)
    print(f"理性化指数: {rationalization_results['rationalization_index']:.2f}")
    print(f"现代化水平: {rationalization_results['modernization_level']}")
    
    print("\n=== 权威合法性分析 ===")
    authority_results = analyzer.analyze_authority_legitimacy(sample_text)
    print(f"权威类型: {authority_results['authority_type']}")
    print(f"权威稳定性: {authority_results['authority_stability']['stability_level']}")
    
    print("\n=== 科层制与现代性分析 ===")
    bureaucracy_results = analyzer.analyze_bureaucracy_modernity(sample_text)
    print(f"科层制指数: {bureaucracy_results['bureaucracy_index']:.2f}")
    print(f"现代性水平: {bureaucracy_results['modernity_level']['modernity_level']}")
    
    print("\n=== 综合报告 ===")
    report = analyzer.generate_comprehensive_report()
    print(report)


if __name__ == "__main__":
    main()
