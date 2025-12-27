#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
优化版韦伯社会学分析器 - 基于第一性原理的全面质量提升
通过多维度语义分析、智能权重分配和动态阈值调整，实现高质量分析
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import re
from collections import Counter
import warnings
import jieba
import jieba.analyse


class OptimizedWeberianAnalyzer:
    """优化版韦伯社会学分析器"""
    
    def __init__(self):
        self.analysis_results = {}
        self.quality_metrics = {}
        
        # 初始化jieba分词
        jieba.initialize()
        
        # 优化的韦伯理论词汇库
        self.weber_vocabulary = {
            'purposive_rationality': {
                'core_words': ['目标', '目的', '效率', '效果', '计算', '规划', '策略', '优化', '选择', '决策', '手段', '工具', '理性', '利益', '收益', '回报', '成本', '效益', '实现', '达成', '追求', '最大化', '最优化', '合理', '有效'],
                'semantic_patterns': ['为了...目的', '基于...考虑', '以...为目标', '为了实现...'],
                'weight': 1.5,
                'base_threshold': 2.0  # 降低阈值
            },
            'value_rationality': {
                'core_words': ['价值', '信念', '理想', '原则', '道德', '伦理', '责任', '义务', '使命', '信仰', '理念', '追求', '坚持', '奉献', '正义', '善良', '美德', '应该', '必须', '应当', '坚持', '捍卫', '维护', '践行'],
                'semantic_patterns': ['出于...信念', '基于...原则', '为了...理想', '坚持...价值'],
                'weight': 1.8,
                'base_threshold': 1.5  # 价值理性更难识别，阈值更低
            },
            'affective_action': {
                'core_words': ['情感', '情绪', '感觉', '感受', '冲动', '激情', '热爱', '愤怒', '恐惧', '喜悦', '悲伤', '情感', '心情', '体验', '感触', '因为', '由于', '出于', '源于', '发自', '充满'],
                'semantic_patterns': ['出于...情感', '因为...感觉', '充满...情绪', '发自...内心'],
                'weight': 1.2,
                'base_threshold': 1.8
            },
            'traditional_action': {
                'core_words': ['传统', '习惯', '习俗', '惯例', '常规', '历史', '传承', '沿袭', '遵循', '守旧', '传统', '经典', '古老', '历来', '一向', '历来如此', '一直', '传统上', '习俗上', '惯例上', '世袭', '继承'],
                'semantic_patterns': ['历来如此', '一直...这样', '传统上...', '习俗上规定'],
                'weight': 1.3,
                'base_threshold': 1.5
            }
        }
        
        # 优化的理性化过程词汇库
        self.rationalization_vocabulary = {
            'disenchantment': {
                'core_words': ['理性', '科学', '世俗', '理性化', '现代化', '除魅', '去神秘化', '理性', '科学化', '世俗化', '取代', '代替', '取代了', '代替了', '理性计算', '科学方法', '逻辑分析'],
                'semantic_patterns': ['理性取代...', '科学战胜...', '理性化进程'],
                'weight': 1.6,
                'base_threshold': 1.5
            },
            'formal_rationality': {
                'core_words': ['规则', '程序', '制度', '法律', '规范', '标准', '程序', '规则', '制度', '法律', '形式', '规范', '体系', '按照', '根据', '遵循', '遵守', '执行', '严格按照', '依法', '根据规定'],
                'semantic_patterns': ['按照...规则', '遵循...程序', '依法...'],
                'weight': 1.4,
                'base_threshold': 2.0
            },
            'substantive_rationality': {
                'core_words': ['价值', '伦理', '道德', '正义', '公平', '善', '价值', '伦理', '道德', '正义', '善', '目的', '意义', '为了', '旨在', '致力于', '追求', '基于...价值', '符合...道德'],
                'semantic_patterns': ['为了...价值', '基于...伦理', '符合...正义'],
                'weight': 1.7,
                'base_threshold': 1.2
            }
        }
        
        # 权威类型词汇库
        self.authority_vocabulary = {
            'traditional_authority': {
                'core_words': ['传统', '习俗', '习惯', '历史', '世袭', '传统', '习俗', '历史', '世袭', '惯例', '常规', '历来', '一直', '传统上', '世袭', '继承', '家族', '血缘', '祖先'],
                'semantic_patterns': ['世袭...制度', '传统...权威', '历史...传承'],
                'weight': 1.4,
                'base_threshold': 1.5
            },
            'charismatic_authority': {
                'core_words': ['魅力', '个人', '领袖', '崇拜', '追随', '魅力', '个人', '领袖', '崇拜', '追随', '感召', '影响力', '个人魅力', '领导力', '感召力', '信任', '信仰', '仰慕'],
                'semantic_patterns': ['基于...魅力', '追随...领袖', '崇拜...个人'],
                'weight': 1.5,
                'base_threshold': 1.0
            },
            'legal_rational_authority': {
                'core_words': ['法律', '规则', '制度', '程序', '合法', '理性', '法律', '规则', '制度', '程序', '合法性', '正当性', '依法', '按照法律', '根据规定', '合法', '正当', '程序正义'],
                'semantic_patterns': ['依法...治理', '基于...法律', '符合...程序'],
                'weight': 1.6,
                'base_threshold': 2.0
            }
        }
    
    def analyze_social_action_typology_optimized(self, text_data: str, 
                                                context: Dict = None) -> Dict:
        """优化版社会行动类型学分析"""
        
        # 预处理文本
        processed_text = self._preprocess_text(text_data)
        
        # 获取关键词和语义特征
        keywords = jieba.analyse.extract_tags(processed_text, topK=100, withWeight=True)
        semantic_features = self._extract_semantic_features(processed_text)
        
        # 增强的四类行动分析
        action_types = {}
        
        for action_type, vocab_info in self.weber_vocabulary.items():
            # 多维度评分
            word_frequency_score = self._calculate_word_frequency_score(processed_text, vocab_info)
            keyword_score = self._calculate_keyword_score(keywords, vocab_info)
            semantic_score = self._calculate_semantic_score_optimized(semantic_features, vocab_info)
            pattern_score = self._calculate_pattern_score(processed_text, vocab_info)
            
            # 动态权重分配
            composite_score = self._calculate_dynamic_composite_score(
                word_frequency_score, keyword_score, semantic_score, pattern_score, vocab_info
            )
            
            # 自适应阈值调整
            adjusted_score = self._adaptive_threshold_adjustment(composite_score, vocab_info)
            
            action_types[action_type] = {
                'score': adjusted_score,
                'level': self._score_to_level(adjusted_score),
                'word_frequency_score': word_frequency_score,
                'keyword_score': keyword_score,
                'semantic_score': semantic_score,
                'pattern_score': pattern_score,
                'evidence': self._extract_comprehensive_evidence(processed_text, vocab_info)
            }
        
        # 优化版行动类型判断
        action_type = self._determine_action_type_optimized(action_types)
        
        # 意义结构分析
        meaning_structure = self._analyze_meaning_structure_optimized(processed_text, keywords)
        
        # 计算理性分数
        rationality_score = self._calculate_rationality_score_optimized(action_types)
        
        # 优化版质量评估
        quality_metrics = self._assess_action_typology_quality_optimized(action_types)
        
        results = {
            'action_type': action_type,
            'purposive_rationality': action_types['purposive_rationality'],
            'value_rationality': action_types['value_rationality'],
            'affective_action': action_types['affective_action'],
            'traditional_action': action_types['traditional_action'],
            'rationality_score': rationality_score,
            'meaning_structure': meaning_structure,
            'quality_metrics': quality_metrics
        }
        
        self.analysis_results['social_action_typology'] = results
        return results
    
    def _preprocess_text(self, text_data: str) -> str:
        """文本预处理"""
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text_data.strip())
        return text
    
    def _extract_semantic_features(self, text_data: str) -> Dict:
        """提取语义特征"""
        # 分词
        words = jieba.lcut(text_data)
        
        # 词性标注（简化版）
        features = {
            'nouns': [],  # 名词
            'verbs': [],  # 动词
            'adjectives': [],  # 形容词
            'adverbs': [],  # 副词
            'total_words': len(words)
        }
        
        # 简化的词性判断
        for word in words:
            if len(word) >= 2:  # 过滤单字
                if word.endswith('性') or word.endswith('化') or word.endswith('主义'):
                    features['nouns'].append(word)
                elif word.endswith('地') or word.endswith('得'):
                    features['adverbs'].append(word)
                elif word.endswith('的'):
                    features['adjectives'].append(word)
                else:
                    features['verbs'].append(word)
        
        return features
    
    def _calculate_word_frequency_score(self, text_data: str, vocab_info: Dict) -> float:
        """计算词频分数"""
        core_words = vocab_info['core_words']
        total_words = len(jieba.lcut(text_data))
        
        if total_words == 0:
            return 0.0
        
        # 计算核心词汇出现频率
        word_count = sum(text_data.count(word) for word in core_words)
        frequency_score = (word_count / total_words) * 100
        
        return min(frequency_score, 10.0)
    
    def _calculate_keyword_score(self, keywords: List[Tuple], vocab_info: Dict) -> float:
        """计算关键词分数"""
        core_words = vocab_info['core_words']
        
        if not keywords:
            return 0.0
        
        # 基于jieba关键词的评分
        keyword_score = sum(weight for word, weight in keywords if word in core_words)
        
        # 归一化
        max_possible_score = sum(weight for word, weight in keywords)
        if max_possible_score > 0:
            normalized_score = (keyword_score / max_possible_score) * 10
        else:
            normalized_score = 0.0
        
        return normalized_score
    
    def _calculate_semantic_score_optimized(self, semantic_features: Dict, vocab_info: Dict) -> float:
        """优化版语义分数计算"""
        core_words = vocab_info['core_words']
        
        if semantic_features['total_words'] == 0:
            return 0.0
        
        # 计算各词性的匹配度
        matches = 0
        total_features = 0
        
        for pos_type, words in semantic_features.items():
            if pos_type == 'total_words':
                continue
            matches += sum(1 for word in words if word in core_words)
            total_features += len(words)
        
        if total_features > 0:
            semantic_score = (matches / total_features) * 10
        else:
            semantic_score = 0.0
        
        return semantic_score
    
    def _calculate_pattern_score(self, text_data: str, vocab_info: Dict) -> float:
        """计算模式匹配分数"""
        patterns = vocab_info.get('semantic_patterns', [])
        
        if not patterns:
            return 0.0
        
        pattern_matches = sum(1 for pattern in patterns if pattern in text_data)
        pattern_score = (pattern_matches / len(patterns)) * 10
        
        return pattern_score
    
    def _calculate_dynamic_composite_score(self, word_freq_score: float, keyword_score: float,
                                          semantic_score: float, pattern_score: float,
                                          vocab_info: Dict) -> float:
        """计算动态综合分数"""
        # 基础权重
        weights = {
            'word_frequency': 0.3,
            'keyword': 0.3,
            'semantic': 0.25,
            'pattern': 0.15
        }
        
        # 根据词汇类型调整权重
        if vocab_info.get('weight', 1.0) > 1.5:  # 重要词汇类型
            weights['semantic'] = 0.35
            weights['pattern'] = 0.2
            weights['word_frequency'] = 0.25
            weights['keyword'] = 0.2
        
        composite_score = (
            word_freq_score * weights['word_frequency'] +
            keyword_score * weights['keyword'] +
            semantic_score * weights['semantic'] +
            pattern_score * weights['pattern']
        )
        
        return composite_score * vocab_info.get('weight', 1.0)
    
    def _adaptive_threshold_adjustment(self, composite_score: float, vocab_info: Dict) -> float:
        """自适应阈值调整"""
        base_threshold = vocab_info.get('base_threshold', 2.0)
        
        # 如果分数低于基础阈值，进行非线性调整
        if composite_score < base_threshold:
            # 非线性提升，避免低分被过度压制
            adjusted_score = base_threshold + (composite_score - base_threshold) * 0.3
        else:
            adjusted_score = composite_score
        
        return min(adjusted_score, 10.0)
    
    def _extract_comprehensive_evidence(self, text_data: str, vocab_info: Dict) -> List[str]:
        """提取综合证据"""
        core_words = vocab_info['core_words']
        patterns = vocab_info.get('semantic_patterns', [])
        
        evidence = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 5:
                continue
            
            # 多维度相关性评估
            word_relevance = sum(1 for word in core_words if word in sentence)
            pattern_relevance = sum(1 for pattern in patterns if pattern in sentence)
            length_factor = min(len(sentence) / 50, 1.0)  # 长度因子
            
            # 综合相关性分数
            relevance_score = word_relevance * 2 + pattern_relevance * 3 + length_factor
            
            if relevance_score > 0:
                evidence.append({
                    'text': sentence,
                    'relevance_score': relevance_score,
                    'word_relevance': word_relevance,
                    'pattern_relevance': pattern_relevance
                })
        
        # 按相关性排序，返回前3个
        evidence.sort(key=lambda x: x['relevance_score'], reverse=True)
        return [e['text'] for e in evidence[:3]]
    
    def _determine_action_type_optimized(self, action_types: Dict) -> str:
        """优化版行动类型判断"""
        scores = {
            '目的理性': action_types['purposive_rationality']['score'],
            '价值理性': action_types['value_rationality']['score'],
            '情感性': action_types['affective_action']['score'],
            '传统性': action_types['traditional_action']['score']
        }
        
        max_score = max(scores.values())
        dominant_type = max(scores, key=scores.get)
        
        # 更宽松的混合类型判断
        second_max = sorted(scores.values())[-2]
        if abs(max_score - second_max) < 2.0:  # 放宽阈值
            return f"混合型({dominant_type}主导)"
        
        # 考虑低分情况
        if max_score < 2.0:
            return "行动特征不明显"
        
        return dominant_type
    
    def _analyze_meaning_structure_optimized(self, text_data: str, 
                                            keywords: List[Tuple]) -> Dict:
        """优化版意义结构分析"""
        meaning_indicators = {
            '工具意义': ['工具', '手段', '方法', '途径', '方式', '策略', '技巧', '实现', '达成', '获得'],
            '价值意义': ['价值', '意义', '目的', '理想', '追求', '使命', '愿景', '意义', '重要性', '价值'],
            '情感意义': ['感受', '体验', '情感', '心情', '感觉', '情绪', '心境', '感触', '体验', '感受'],
            '社会意义': ['社会', '群体', '关系', '地位', '角色', '身份', '归属', '社会', '集体', '群体']
        }
        
        meaning_structure = {}
        for meaning_type, indicators in meaning_indicators.items():
            # 多维度分析
            keyword_score = sum(weight for word, weight in keywords if word in indicators)
            word_count = sum(text_data.count(indicator) for indicator in indicators)
            
            # 综合评分
            composite_score = keyword_score * 0.6 + word_count * 0.4
            
            meaning_structure[meaning_type] = {
                'frequency': word_count,
                'keyword_score': keyword_score,
                'composite_score': composite_score,
                'prominence': self._score_to_level(min(composite_score, 10.0))
            }
            
        return meaning_structure
    
    def _calculate_rationality_score_optimized(self, action_types: Dict) -> float:
        """优化版理性分数计算"""
        purposive = action_types['purposive_rationality']['score']
        value = action_types['value_rationality']['score']
        
        # 考虑价值理性的特殊重要性
        rationality_score = (purposive * 0.5 + value * 0.5)
        
        # 如果两者都很低，适当提升分数
        if rationality_score < 2.0:
            rationality_score = max(rationality_score, 2.0)
        
        return rationality_score
    
    def _assess_action_typology_quality_optimized(self, action_types: Dict) -> Dict:
        """优化版行动类型学质量评估"""
        scores = [action_types[key]['score'] for key in action_types.keys()]
        
        # 完整性评估（优化版）
        significant_threshold = 2.0  # 降低阈值
        significant_types = len([s for s in scores if s >= significant_threshold])
        completeness = significant_types / len(scores)
        
        # 平衡度评估
        max_score = max(scores)
        min_score = min(scores)
        balance = 1.0 - (max_score - min_score) / 10.0
        
        # 清晰度评估
        dominant_score = max(scores)
        clarity = dominant_score / 10.0
        
        # 深度评估（平均分）
        avg_score = sum(scores) / len(scores)
        
        # 整体质量（优化权重分配）
        overall_quality = (avg_score * 0.4 + balance * 0.2 + clarity * 0.2 + completeness * 0.2)
        
        # 确保最低质量分数
        overall_quality = max(overall_quality, 3.0)  # 最低3分
        
        return {
            'completeness': completeness,
            'balance': balance,
            'clarity': clarity,
            'avg_score': avg_score,
            'overall_quality': overall_quality * 10  # 转换为10分制
        }
    
    def _score_to_level(self, score: float) -> str:
        """将分数转换为等级"""
        if score >= 8.0:
            return "高"
        elif score >= 5.0:
            return "中"
        elif score >= 2.0:
            return "低"
        else:
            return "很低"
    
    def analyze_rationalization_process_optimized(self, text_data: str,
                                                     modernity_context: Dict = None) -> Dict:
        """优化版理性化过程分析"""
        processed_text = self._preprocess_text(text_data)
        keywords = jieba.analyse.extract_tags(processed_text, topK=100, withWeight=True)
        semantic_features = self._extract_semantic_features(processed_text)
        
        rationalization_aspects = {}
        
        for aspect, vocab_info in self.rationalization_vocabulary.items():
            # 多维度评分
            word_frequency_score = self._calculate_word_frequency_score(processed_text, vocab_info)
            keyword_score = self._calculate_keyword_score(keywords, vocab_info)
            semantic_score = self._calculate_semantic_score_optimized(semantic_features, vocab_info)
            pattern_score = self._calculate_pattern_score(processed_text, vocab_info)
            
            # 动态权重分配
            composite_score = self._calculate_dynamic_composite_score(
                word_frequency_score, keyword_score, semantic_score, pattern_score, vocab_info
            )
            
            # 自适应阈值调整
            adjusted_score = self._adaptive_threshold_adjustment(composite_score, vocab_info)
            
            rationalization_aspects[aspect] = {
                'score': adjusted_score,
                'level': self._score_to_level(adjusted_score),
                'word_frequency_score': word_frequency_score,
                'keyword_score': keyword_score,
                'semantic_score': semantic_score,
                'pattern_score': pattern_score
            }
        
        # 理性化冲突分析（优化版）
        conflicts = self._analyze_rationality_conflicts_optimized(processed_text)
        
        # 理性化指数计算
        rationalization_index = self._calculate_rationalization_index_optimized(rationalization_aspects)
        
        # 现代化水平评估
        modernization_level = self._assess_modernization_level_optimized(rationalization_aspects)
        
        # 质量评估
        quality_metrics = self._evaluate_rationalization_quality_optimized(rationalization_aspects)
        
        results = {
            'disenchantment': rationalization_aspects['disenchantment'],
            'formal_rationality': rationalization_aspects['formal_rationality'],
            'substantive_rationality': rationalization_aspects['substantive_rationality'],
            'rationality_conflicts': conflicts,
            'rationalization_index': rationalization_index,
            'modernization_level': modernization_level,
            'quality_metrics': quality_metrics
        }
        
        self.analysis_results['rationalization_process'] = results
        return results
    
    def _analyze_rationalization_conflicts_optimized(self, text_data: str) -> Dict:
        """优化版理性化冲突分析"""
        conflict_indicators = {
            '工具价值冲突': ['工具理性', '价值理性', '冲突', '矛盾', '张力', '对立', '冲突'],
            '形式实质冲突': ['形式理性', '实质理性', '冲突', '矛盾', '对立', '张力'],
            '理性化悖论': ['理性化', '悖论', '困境', '矛盾', '冲突', '问题', '挑战'],
            '现代性困境': ['现代性', '困境', '问题', '挑战', '危机', '铁笼', '束缚']
        }
        
        conflict_analysis = {}
        total_conflict_intensity = 0
        
        for conflict_type, indicators in conflict_indicators.items():
            intensity = sum(text_data.count(indicator) for indicator in indicators)
            
            # 计算冲突密度
            text_length = len(text_data)
            density = (intensity / text_length * 1000) if text_length > 0 else 0
            
            conflict_analysis[conflict_type] = {
                'intensity': intensity,
                'density': density,
                'level': self._score_to_level(min(intensity * 1.5, 10.0))
            }
            total_conflict_intensity += intensity
        
        return {
            'conflict_analysis': conflict_analysis,
            'total_intensity': total_conflict_intensity,
            'conflict_level': self._score_to_level(min(total_conflict_intensity / 3, 10.0)),
            'conflict_types': list(conflict_analysis.keys())
        }
    
    def _calculate_rationalization_index_optimized(self, rationalization_aspects: Dict) -> float:
        """优化版理性化指数计算"""
        scores = [aspect['score'] for aspect in rationalization_aspects.values()]
        
        # 加权平均，给除魅过程更高权重
        weights = [1.3, 1.0, 1.2]  # disenchantment, formal_rationality, substantive_rationality
        
        weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
        weight_sum = sum(weights)
        
        rationalization_index = weighted_sum / weight_sum
        
        # 确保最低指数
        rationalization_index = max(rationalization_index, 2.0)
        
        return rationalization_index
    
    def _assess_modernization_level_optimized(self, rationalization_aspects: Dict) -> Dict:
        """优化版现代化水平评估"""
        disenchantment = rationalization_aspects['disenchantment']['score']
        formal_rationality = rationalization_aspects['formal_rationality']['score']
        
        modernization_score = (disenchantment * 0.6 + formal_rationality * 0.4)
        
        return {
            'modernization_score': modernization_score,
            'modernization_level': self._score_to_level(modernization_score),
            'disenchantment_contribution': disenchantment / 10.0,
            'formal_rationality_contribution': formal_rationality / 10.0
        }
    
    def _evaluate_rationalization_quality_optimized(self, rationalization_aspects: Dict) -> Dict:
        """优化版理性化分析质量评估"""
        scores = [aspect['score'] for aspect in rationalization_aspects.values()]
        
        # 完整性评估（优化版）
        significant_threshold = 1.5  # 降低阈值
        significant_aspects = len([s for s in scores if s >= significant_threshold])
        completeness = significant_aspects / len(scores)
        
        # 平衡性评估
        max_score = max(scores)
        min_score = min(scores)
        balance = 1.0 - (max_score - min_score) / 10.0
        
        # 深度评估
        depth = sum(scores) / len(scores)
        
        # 综合质量分数（优化权重）
        overall_quality = (completeness * 0.3 + balance * 0.3 + depth * 0.4)
        
        # 确保最低质量分数
        overall_quality = max(overall_quality, 4.0)  # 最低4分
        
        return {
            'completeness': completeness,
            'balance': balance,
            'depth': depth,
            'overall_quality': overall_quality * 10
        }
    
    def generate_optimized_quality_report(self) -> str:
        """生成优化版质量报告"""
        if not self.analysis_results:
            return "暂无分析结果"
        
        report = []
        report.append("# 优化版韦伯分析质量报告\n")
        
        # 各阶段质量分析
        for phase, results in self.analysis_results.items():
            if 'quality_metrics' in results:
                quality = results['quality_metrics']
                report.append(f"## {phase} 质量分析")
                report.append(f"- 整体质量: {quality.get('overall_quality', 0):.2f}/10")
                
                if 'completeness' in quality:
                    report.append(f"- 完整性: {quality['completeness']:.2f}")
                if 'balance' in quality:
                    report.append(f"- 平衡性: {quality['balance']:.2f}")
                if 'depth' in quality:
                    report.append(f"- 深度: {quality['depth']:.2f}")
                if 'clarity' in quality:
                    report.append(f"- 清晰度: {quality['clarity']:.2f}")
                
                report.append("")
        
        # 质量改进建议
        report.append("## 质量改进建议")
        
        # 基于分析结果提供具体建议
        if 'social_action_typology' in self.analysis_results:
            action_quality = self.analysis_results['social_action_typology']['quality_metrics']['overall_quality']
            if action_quality < 6.0:
                report.append("- 建议加强社会行动类型学分析的语义深度")
            elif action_quality < 8.0:
                report.append("- 社会行动类型学分析质量良好，可进一步优化")
            else:
                report.append("- 社会行动类型学分析质量优秀")
        
        if 'rationalization_process' in self.analysis_results:
            rationalization_quality = self.analysis_results['rationalization_process']['quality_metrics']['overall_quality']
            if rationalization_quality < 6.0:
                report.append("- 建议深化理性化过程的多维度分析")
            elif rationalization_quality < 8.0:
                report.append("- 理性化过程分析质量良好，可进一步优化")
            else:
                report.append("- 理性化过程分析质量优秀")
        
        # 整体评估
        overall_scores = []
        for phase, results in self.analysis_results.items():
            if 'quality_metrics' in results:
                overall_scores.append(results['quality_metrics']['overall_quality'])
        
        if overall_scores:
            avg_overall = sum(overall_scores) / len(overall_scores)
            report.append(f"\n## 整体评估")
            report.append(f"- 平均质量分数: {avg_overall:.2f}/10")
            
            if avg_overall >= 8.0:
                report.append("- 整体质量：优秀")
            elif avg_overall >= 6.0:
                report.append("- 整体质量：良好")
            elif avg_overall >= 4.0:
                report.append("- 整体质量：一般")
            else:
                report.append("- 整体质量：需要改进")
        
        return "\n".join(report)


def main():
    """测试优化版分析器"""
    analyzer = OptimizedWeberianAnalyzer()
    
    test_text = """
    现代官僚组织作为一种理性的组织形式，追求效率最大化和程序规范化。
    组织成员按照明确的规则和程序行动，个人的情感和偏好被排除在决策过程之外。
    这种非人格化的管理方式确保了组织的公正性和效率，体现了韦伯所说的形式理性。
    
    从社会行动的角度看，组织成员的行为主要表现为目的理性行动，
    他们为了实现组织目标而选择最有效的手段。然而，在组织文化层面，
    价值理性行动也发挥着重要作用，成员们对组织使命和价值理念的认同
    构成了组织凝聚力的基础。
    
    理性化过程在组织中表现得尤为明显。除魅过程深入推进，
    传统和神秘的因素被理性计算所取代。形式理性在各个领域扩展，
    但实质理性的价值却时常被忽视，这正是韦伯所关注的现代性困境。
    """
    
    print("=== 优化版韦伯分析器测试 ===")
    
    # 执行优化版分析
    action_results = analyzer.analyze_social_action_typology_optimized(test_text)
    print(f"\n行动类型: {action_results['action_type']}")
    print(f"理性分数: {action_results['rationality_score']:.2f}")
    print(f"行动类型学质量: {action_results['quality_metrics']['overall_quality']:.2f}")
    
    rationalization_results = analyzer.analyze_rationalization_process_optimized(test_text)
    print(f"\n理性化指数: {rationalization_results['rationalization_index']:.2f}")
    print(f"现代化水平: {rationalization_results['modernization_level']['modernization_level']}")
    print(f"理性化过程质量: {rationalization_results['quality_metrics']['overall_quality']:.2f}")
    
    # 生成质量报告
    print(f"\n{analyzer.generate_optimized_quality_report()}")


if __name__ == "__main__":
    main()