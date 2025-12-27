#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版韦伯社会学分析器 - 基于第一性原理的质量提升
通过语义分析、上下文理解和智能权重分配，大幅提升分析质量
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import re
from collections import Counter
import warnings
import jieba
import jieba.analyse


class EnhancedWeberianAnalyzer:
    """增强版韦伯社会学分析器"""
    
    def __init__(self):
        self.analysis_results = {}
        self.quality_metrics = {}
        
        # 初始化jieba分词
        jieba.initialize()
        
        # 韦伯理论核心词汇库（增强版）
        self.weber_vocabulary = {
            'purposive_rationality': {
                'core_words': ['目标', '目的', '效率', '效果', '计算', '规划', '策略', '优化', '选择', '决策', '手段', '工具', '理性', '利益', '收益', '回报', '成本', '效益'],
                'context_words': ['实现', '达成', '追求', '最大化', '最优化', '合理', '有效'],
                'weight': 1.5
            },
            'value_rationality': {
                'core_words': ['价值', '信念', '理想', '原则', '道德', '伦理', '责任', '义务', '使命', '信仰', '理念', '追求', '坚持', '奉献', '正义', '善良', '美德'],
                'context_words': ['应该', '必须', '应当', '坚持', '捍卫', '维护', '践行', '实现'],
                'weight': 1.8  # 价值理性权重更高，因为更难识别
            },
            'affective_action': {
                'core_words': ['情感', '情绪', '感觉', '感受', '冲动', '激情', '热爱', '愤怒', '恐惧', '喜悦', '悲伤', '情感', '心情', '体验', '感触'],
                'context_words': ['因为', '由于', '出于', '源于', '发自', '充满'],
                'weight': 1.2
            },
            'traditional_action': {
                'core_words': ['传统', '习惯', '习俗', '惯例', '常规', '历史', '传承', '沿袭', '遵循', '守旧', '传统', '经典', '古老', '历来', '一向'],
                'context_words': ['历来如此', '一直', '传统上', '习俗上', '惯例上'],
                'weight': 1.3
            }
        }
        
        # 理性化过程词汇库
        self.rationalization_vocabulary = {
            'disenchantment': {
                'core_words': ['理性', '科学', '世俗', '理性化', '现代化', '除魅', '去神秘化', '理性', '科学化', '世俗化'],
                'context_words': ['取代', '代替', '取代了', '代替了'],
                'weight': 1.6
            },
            'formal_rationality': {
                'core_words': ['规则', '程序', '制度', '法律', '规范', '标准', '程序', '规则', '制度', '法律', '形式', '规范', '体系'],
                'context_words': ['按照', '根据', '遵循', '遵守', '执行'],
                'weight': 1.4
            },
            'substantive_rationality': {
                'core_words': ['价值', '伦理', '道德', '正义', '公平', '善', '价值', '伦理', '道德', '正义', '善', '目的', '意义'],
                'context_words': ['为了', '旨在', '致力于', '追求'],
                'weight': 1.7
            }
        }
        
        # 权威类型词汇库
        self.authority_vocabulary = {
            'traditional_authority': {
                'core_words': ['传统', '习俗', '习惯', '历史', '世袭', '传统', '习俗', '历史', '世袭', '惯例', '常规'],
                'context_words': ['历来', '一直', '传统上', '世袭', '继承'],
                'weight': 1.4
            },
            'charismatic_authority': {
                'core_words': ['魅力', '个人', '领袖', '崇拜', '追随', '魅力', '个人', '领袖', '崇拜', '追随', '感召', '影响力'],
                'context_words': ['崇拜', '追随', '信任', '信仰', '仰慕'],
                'weight': 1.5
            },
            'legal_rational_authority': {
                'core_words': ['法律', '规则', '制度', '程序', '合法', '理性', '法律', '规则', '制度', '程序', '合法性', '正当性'],
                'context_words': ['依法', '按照法律', '根据规定', '合法'],
                'weight': 1.6
            }
        }
    
    def analyze_social_action_typology_enhanced(self, text_data: str, 
                                             context: Dict = None) -> Dict:
        """
        增强版社会行动类型学分析
        """
        # 使用jieba进行分词和关键词提取
        words = jieba.lcut(text_data)
        keywords = jieba.analyse.extract_tags(text_data, topK=50, withWeight=True)
        
        # 增强的四类行动分析
        action_types = {}
        
        for action_type, vocab_info in self.weber_vocabulary.items():
            # 语义匹配分析
            semantic_score = self._calculate_semantic_score(text_data, vocab_info, keywords)
            
            # 上下文分析
            context_score = self._calculate_context_score(text_data, vocab_info)
            
            # 综合评分
            composite_score = (semantic_score * 0.7 + context_score * 0.3) * vocab_info['weight']
            
            # 归一化到0-10分
            normalized_score = min(composite_score, 10.0)
            
            action_types[action_type] = {
                'score': normalized_score,
                'level': self._score_to_level(normalized_score),
                'semantic_score': semantic_score,
                'context_score': context_score,
                'evidence': self._extract_enhanced_evidence(text_data, vocab_info)
            }
        
        # 行动类型判断（改进版）
        action_type = self._determine_action_type_enhanced(action_types)
        
        # 意义结构分析
        meaning_structure = self._analyze_meaning_structure_enhanced(text_data, keywords)
        
        # 计算理性分数
        rationality_score = self._calculate_rationality_score_enhanced(action_types)
        
        # 质量评估
        quality_metrics = self._assess_action_typology_quality_enhanced(action_types)
        
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
    
    def _calculate_semantic_score(self, text_data: str, vocab_info: Dict, 
                                keywords: List[Tuple]) -> float:
        """计算语义匹配分数"""
        core_words = vocab_info['core_words']
        
        # 基于jieba关键词的语义匹配
        keyword_score = 0.0
        for word, weight in keywords:
            if word in core_words:
                keyword_score += weight
        
        # 基于词频的语义匹配
        word_count = 0
        for word in core_words:
            word_count += text_data.count(word)
        
        # 综合语义分数
        total_words = len(jieba.lcut(text_data))
        if total_words == 0:
            return 0.0
        
        semantic_score = (keyword_score * 2 + word_count) / total_words * 10
        return min(semantic_score, 10.0)
    
    def _calculate_context_score(self, text_data: str, vocab_info: Dict) -> float:
        """计算上下文关联分数"""
        context_words = vocab_info['context_words']
        
        if not context_words:
            return 0.0
        
        # 上下文词汇匹配
        context_count = sum(text_data.count(word) for word in context_words)
        
        # 句子级别的上下文分析
        sentences = re.split(r'[。！？]', text_data)
        context_sentences = 0
        
        for sentence in sentences:
            if any(word in sentence for word in context_words):
                context_sentences += 1
        
        # 上下文分数
        context_score = (context_count * 0.5 + context_sentences * 0.5) / len(sentences) * 10
        return min(context_score, 10.0)
    
    def _extract_enhanced_evidence(self, text_data: str, vocab_info: Dict) -> List[str]:
        """提取增强版证据"""
        core_words = vocab_info['core_words']
        evidence = []
        
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 5:  # 过短的句子跳过
                continue
                
            # 计算句子与词汇的相关性
            relevance = sum(1 for word in core_words if word in sentence)
            
            if relevance > 0:
                evidence.append({
                    'text': sentence,
                    'relevance': relevance,
                    'length': len(sentence)
                })
        
        # 按相关性排序，返回前3个
        evidence.sort(key=lambda x: x['relevance'], reverse=True)
        return [e['text'] for e in evidence[:3]]
    
    def _determine_action_type_enhanced(self, action_types: Dict) -> str:
        """增强版行动类型判断"""
        scores = {
            '目的理性': action_types['purposive_rationality']['score'],
            '价值理性': action_types['value_rationality']['score'],
            '情感性': action_types['affective_action']['score'],
            '传统性': action_types['traditional_action']['score']
        }
        
        max_score = max(scores.values())
        dominant_type = max(scores, key=scores.get)
        
        # 考虑混合类型的情况
        second_max = sorted(scores.values())[-2]
        if abs(max_score - second_max) < 1.5:  # 阈值放宽
            return f"混合型({dominant_type}主导)"
        
        # 考虑分数较低的情况
        if max_score < 3.0:
            return "行动类型不明确"
        
        return dominant_type
    
    def _analyze_meaning_structure_enhanced(self, text_data: str, 
                                          keywords: List[Tuple]) -> Dict:
        """增强版意义结构分析"""
        meaning_indicators = {
            '工具意义': ['工具', '手段', '方法', '途径', '方式', '策略', '技巧'],
            '价值意义': ['价值', '意义', '目的', '理想', '追求', '使命', '愿景'],
            '情感意义': ['感受', '体验', '情感', '心情', '感觉', '情绪', '心境'],
            '社会意义': ['社会', '群体', '关系', '地位', '角色', '身份', '归属']
        }
        
        meaning_structure = {}
        for meaning_type, indicators in meaning_indicators.items():
            # 基于jieba关键词的分析
            keyword_score = sum(weight for word, weight in keywords if word in indicators)
            
            # 基于词频的分析
            word_count = sum(text_data.count(indicator) for indicator in indicators)
            
            # 综合评分
            composite_score = keyword_score * 0.7 + word_count * 0.3
            
            meaning_structure[meaning_type] = {
                'frequency': word_count,
                'keyword_score': keyword_score,
                'composite_score': composite_score,
                'prominence': self._score_to_level(min(composite_score, 10.0))
            }
            
        return meaning_structure
    
    def _calculate_rationality_score_enhanced(self, action_types: Dict) -> float:
        """增强版理性分数计算"""
        purposive = action_types['purposive_rationality']['score']
        value = action_types['value_rationality']['score']
        
        # 考虑价值理性的特殊权重
        rationality_score = (purposive * 0.6 + value * 0.4)
        
        return rationality_score
    
    def _assess_action_typology_quality_enhanced(self, action_types: Dict) -> Dict:
        """增强版行动类型学质量评估"""
        # 计算各类型的平均分数
        scores = [action_types[key]['score'] for key in action_types.keys()]
        avg_score = sum(scores) / len(scores)
        
        # 计算平衡度
        max_score = max(scores)
        min_score = min(scores)
        balance = 1.0 - (max_score - min_score) / 10.0
        
        # 计算清晰度（主导类型的优势）
        dominant_score = max(scores)
        clarity = dominant_score / 10.0
        
        # 计算完整性（是否有明显的类型特征）
        significant_types = len([s for s in scores if s >= 3.0])
        completeness = significant_types / len(scores)
        
        # 综合质量分数
        overall_quality = (avg_score * 0.4 + balance * 0.2 + clarity * 0.2 + completeness * 0.2)
        
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
        else:
            return "低"
    
    def analyze_rationalization_process_enhanced(self, text_data: str,
                                               modernity_context: Dict = None) -> Dict:
        """增强版理性化过程分析"""
        # 使用增强版分析方法
        rationalization_aspects = {}
        
        for aspect, vocab_info in self.rationalization_vocabulary.items():
            # 语义匹配分析
            semantic_score = self._calculate_semantic_score(text_data, vocab_info, [])
            
            # 上下文分析
            context_score = self._calculate_context_score(text_data, vocab_info)
            
            # 综合评分
            composite_score = (semantic_score * 0.7 + context_score * 0.3) * vocab_info['weight']
            normalized_score = min(composite_score, 10.0)
            
            rationalization_aspects[aspect] = {
                'score': normalized_score,
                'level': self._score_to_level(normalized_score),
                'semantic_score': semantic_score,
                'context_score': context_score
            }
        
        # 理性化冲突分析（增强版）
        conflicts = self._analyze_rationality_conflicts_enhanced(text_data)
        
        # 理性化指数计算
        rationalization_index = self._calculate_rationalization_index_enhanced(rationalization_aspects)
        
        # 现代化水平评估
        modernization_level = self._assess_modernization_level_enhanced(rationalization_aspects)
        
        # 质量评估
        quality_metrics = self._evaluate_rationalization_quality_enhanced(rationalization_aspects)
        
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
    
    def _analyze_rationality_conflicts_enhanced(self, text_data: str) -> Dict:
        """增强版理性化冲突分析"""
        conflict_indicators = {
            '工具价值冲突': ['工具理性', '价值理性', '冲突', '矛盾', '张力'],
            '形式实质冲突': ['形式理性', '实质理性', '冲突', '矛盾'],
            '理性化悖论': ['理性化', '悖论', '困境', '矛盾', '冲突'],
            '现代性困境': ['现代性', '困境', '问题', '挑战', '危机']
        }
        
        conflict_analysis = {}
        total_conflict_intensity = 0
        
        for conflict_type, indicators in conflict_indicators.items():
            intensity = sum(text_data.count(indicator) for indicator in indicators)
            conflict_analysis[conflict_type] = {
                'intensity': intensity,
                'level': self._score_to_level(min(intensity * 2, 10.0))
            }
            total_conflict_intensity += intensity
        
        return {
            'conflict_analysis': conflict_analysis,
            'total_intensity': total_conflict_intensity,
            'conflict_level': self._score_to_level(min(total_conflict_intensity / 2, 10.0)),
            'conflict_types': list(conflict_analysis.keys())
        }
    
    def _calculate_rationalization_index_enhanced(self, rationalization_aspects: Dict) -> float:
        """增强版理性化指数计算"""
        scores = [aspect['score'] for aspect in rationalization_aspects.values()]
        
        # 加权平均，给除魅过程更高权重
        weights = [1.2, 1.0, 1.1]  # disenchantment, formal_rationality, substantive_rationality
        
        weighted_sum = sum(score * weight for score, weight in zip(scores, weights))
        weight_sum = sum(weights)
        
        return weighted_sum / weight_sum
    
    def _assess_modernization_level_enhanced(self, rationalization_aspects: Dict) -> Dict:
        """增强版现代化水平评估"""
        disenchantment = rationalization_aspects['disenchantment']['score']
        formal_rationality = rationalization_aspects['formal_rationality']['score']
        
        modernization_score = (disenchantment * 0.6 + formal_rationality * 0.4)
        
        return {
            'modernization_score': modernization_score,
            'modernization_level': self._score_to_level(modernization_score),
            'disenchantment_contribution': disenchantment / 10.0,
            'formal_rationality_contribution': formal_rationality / 10.0
        }
    
    def _evaluate_rationalization_quality_enhanced(self, rationalization_aspects: Dict) -> Dict:
        """增强版理性化分析质量评估"""
        scores = [aspect['score'] for aspect in rationalization_aspects.values()]
        
        # 完整性：是否有明显的理性化特征
        significant_aspects = len([s for s in scores if s >= 3.0])
        completeness = significant_aspects / len(scores)
        
        # 平衡性：各维度是否平衡
        max_score = max(scores)
        min_score = min(scores)
        balance = 1.0 - (max_score - min_score) / 10.0
        
        # 深度：整体理性化水平
        depth = sum(scores) / len(scores)
        
        # 综合质量分数
        overall_quality = (completeness * 0.3 + balance * 0.3 + depth * 0.4)
        
        return {
            'completeness': completeness,
            'balance': balance,
            'depth': depth,
            'overall_quality': overall_quality * 10
        }
    
    def generate_enhanced_quality_report(self) -> str:
        """生成增强版质量报告"""
        if not self.analysis_results:
            return "暂无分析结果"
        
        report = []
        report.append("# 增强版韦伯分析质量报告\n")
        
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
        
        # 改进建议
        report.append("## 质量提升建议")
        
        # 基于分析结果提供建议
        if 'social_action_typology' in self.analysis_results:
            action_quality = self.analysis_results['social_action_typology']['quality_metrics']['overall_quality']
            if action_quality < 6.0:
                report.append("- 建议加强社会行动类型学分析的深度和准确性")
        
        if 'rationalization_process' in self.analysis_results:
            rationalization_quality = self.analysis_results['rationalization_process']['quality_metrics']['overall_quality']
            if rationalization_quality < 6.0:
                report.append("- 建议深化理性化过程的多维度分析")
        
        return "\n".join(report)


def main():
    """测试增强版分析器"""
    analyzer = EnhancedWeberianAnalyzer()
    
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
    
    print("=== 增强版韦伯分析器测试 ===")
    
    # 执行增强版分析
    action_results = analyzer.analyze_social_action_typology_enhanced(test_text)
    print(f"\n行动类型: {action_results['action_type']}")
    print(f"理性分数: {action_results['rationality_score']:.2f}")
    print(f"行动类型学质量: {action_results['quality_metrics']['overall_quality']:.2f}")
    
    rationalization_results = analyzer.analyze_rationalization_process_enhanced(test_text)
    print(f"\n理性化指数: {rationalization_results['rationalization_index']:.2f}")
    print(f"现代化水平: {rationalization_results['modernization_level']['modernization_level']}")
    print(f"理性化过程质量: {rationalization_results['quality_metrics']['overall_quality']:.2f}")
    
    # 生成质量报告
    print(f"\n{analyzer.generate_enhanced_quality_report()}")


if __name__ == "__main__":
    main()