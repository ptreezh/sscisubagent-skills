#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
社会事实分析器 - 基于涂尔干理论的量化分析工具
提供社会事实特征识别、集体意识分析、功能分析等计算功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import re
from collections import Counter
import warnings


class SocialFactAnalyzer:
    """社会事实分析器类"""
    
    def __init__(self):
        self.analysis_results = {}
        self.quality_metrics = {}
        
    def identify_social_facts(self, text_data: str, 
                             context: Dict = None) -> Dict:
        """
        识别和分析社会事实特征
        
        Parameters:
        -----------
        text_data : str
            待分析的文本数据
        context : Dict
            分析上下文信息
            
        Returns:
        --------
        Dict : 分析结果和质量指标
        """
        # 外在性分析
        externality_score = self._analyze_externality(text_data)
        
        # 强制性分析
        coerciveness_score = self._analyze_coerciveness(text_data)
        
        # 独立性分析
        independence_score = self._analyze_independence(text_data)
        
        # 社会事实分类
        fact_type = self._classify_social_fact(
            externality_score, coerciveness_score, independence_score
        )
        
        results = {
            'fact_type': fact_type,
            'externality': {
                'score': externality_score,
                'level': self._score_to_level(externality_score),
                'evidence': self._extract_externality_evidence(text_data)
            },
            'coerciveness': {
                'score': coerciveness_score,
                'level': self._score_to_level(coerciveness_score),
                'evidence': self._extract_coerciveness_evidence(text_data)
            },
            'independence': {
                'score': independence_score,
                'level': self._score_to_level(independence_score),
                'evidence': self._extract_independence_evidence(text_data)
            },
            'quality_metrics': self._calculate_quality_metrics(
                externality_score, coerciveness_score, independence_score
            )
        }
        
        self.analysis_results['social_fact_identification'] = results
        return results
    
    def analyze_collective_consciousness(self, text_data: str,
                                       fact_type: str = None) -> Dict:
        """
        分析集体意识特征
        
        Parameters:
        -----------
        text_data : str
            待分析的文本数据
        fact_type : str
            社会事实类型
            
        Returns:
        --------
        Dict : 集体意识分析结果
        """
        # 集体表征识别
        representations = self._identify_collective_representations(text_data)
        
        # 价值体系分析
        value_system = self._analyze_value_system(text_data)
        
        # 社会规范分析
        social_norms = self._analyze_social_norms(text_data)
        
        # 集体情感分析
        collective_emotions = self._analyze_collective_emotions(text_data)
        
        results = {
            'representations': representations,
            'value_system': value_system,
            'social_norms': social_norms,
            'collective_emotions': collective_emotions,
            'consciousness_strength': self._calculate_consciousness_strength(
                representations, value_system, social_norms
            ),
            'quality_metrics': self._assess_consciousness_quality(
                representations, value_system, social_norms, collective_emotions
            )
        }
        
        self.analysis_results['collective_consciousness'] = results
        return results
    
    def perform_functional_analysis(self, text_data: str,
                                  phenomenon: str = None) -> Dict:
        """
        执行功能分析
        
        Parameters:
        -----------
        text_data : str
            待分析的文本数据
        phenomenon : str
            待分析的现象
            
        Returns:
        --------
        Dict : 功能分析结果
        """
        # 显功能识别
        manifest_functions = self._identify_manifest_functions(text_data)
        
        # 潜功能识别
        latent_functions = self._identify_latent_functions(text_data)
        
        # 功能替代分析
        functional_substitutes = self._analyze_functional_substitutes(text_data)
        
        # 功能整合分析
        functional_integration = self._analyze_functional_integration(text_data)
        
        results = {
            'manifest_functions': manifest_functions,
            'latent_functions': latent_functions,
            'functional_substitutes': functional_substitutes,
            'functional_integration': functional_integration,
            'functional_balance': self._assess_functional_balance(
                manifest_functions, latent_functions
            ),
            'quality_metrics': self._evaluate_functional_analysis_quality(
                manifest_functions, latent_functions, functional_integration
            )
        }
        
        self.analysis_results['functional_analysis'] = results
        return results
    
    def analyze_social_solidarity(self, text_data: str,
                                social_context: Dict = None) -> Dict:
        """
        分析社会团结类型和特征
        
        Parameters:
        -----------
        text_data : str
            待分析的文本数据
        social_context : Dict
            社会背景信息
            
        Returns:
        --------
        Dict : 社会团结分析结果
        """
        # 团结类型判断
        solidarity_type = self._determine_solidarity_type(text_data)
        
        # 社会分化分析
        social_differentiation = self._analyze_social_differentiation(text_data)
        
        # 整合机制评估
        integration_mechanisms = self._assess_integration_mechanisms(text_data)
        
        # 变迁趋势分析
        change_trends = self._analyze_change_trends(text_data)
        
        results = {
            'solidarity_type': solidarity_type,
            'social_differentiation': social_differentiation,
            'integration_mechanisms': integration_mechanisms,
            'change_trends': change_trends,
            'solidarity_index': self._calculate_solidarity_index(
                solidarity_type, social_differentiation, integration_mechanisms
            ),
            'quality_metrics': self._evaluate_solidarity_analysis_quality(
                solidarity_type, social_differentiation, integration_mechanisms
            )
        }
        
        self.analysis_results['social_solidarity'] = results
        return results
    
    def _analyze_externality(self, text_data: str) -> float:
        """分析外在性特征"""
        externality_indicators = [
            '制度', '法律', '规范', '传统', '文化', '社会', '公共',
            '集体', '共同', '普遍', '客观', '独立', '外在'
        ]
        
        score = 0.0
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
            
        for indicator in externality_indicators:
            count = text_data.count(indicator)
            score += count * 1.0
            
        return min(score / total_words * 10, 10.0)
    
    def _analyze_coerciveness(self, text_data: str) -> float:
        """分析强制性特征"""
        coerciveness_indicators = [
            '必须', '应当', '强制', '约束', '制裁', '惩罚', '规范',
            '要求', '义务', '责任', '遵守', '执行', '监督'
        ]
        
        score = 0.0
        for indicator in coerciveness_indicators:
            count = text_data.count(indicator)
            score += count * 1.5
            
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
            
        return min(score / total_words * 10, 10.0)
    
    def _analyze_independence(self, text_data: str) -> float:
        """分析独立性特征"""
        independence_indicators = [
            '自主', '独立', '稳定', '持续', '历史', '传统',
            '延续', '传承', '制度', '结构', '体系', '框架'
        ]
        
        score = 0.0
        for indicator in independence_indicators:
            count = text_data.count(indicator)
            score += count * 1.2
            
        words = re.findall(r'[\u4e00-\u9fff]+', text_data)
        total_words = len(words)
        
        if total_words == 0:
            return 0.0
            
        return min(score / total_words * 10, 10.0)
    
    def _classify_social_fact(self, externality: float, 
                            coerciveness: float, 
                            independence: float) -> str:
        """分类社会事实类型"""
        if externality >= 7.0 and coerciveness >= 7.0:
            return "制度性事实"
        elif externality >= 6.0 and coerciveness >= 5.0:
            return "规范性事实"
        elif externality >= 5.0 and independence >= 6.0:
            return "价值性事实"
        else:
            return "行为性事实"
    
    def _score_to_level(self, score: float) -> str:
        """将分数转换为等级"""
        if score >= 7.0:
            return "高"
        elif score >= 4.0:
            return "中"
        else:
            return "低"
    
    def _extract_externality_evidence(self, text_data: str) -> List[str]:
        """提取外在性证据"""
        evidence = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if any(indicator in sentence for indicator in ['制度', '法律', '社会', '公共']):
                evidence.append(sentence.strip())
                
        return evidence[:3]  # 返回前3个证据
    
    def _extract_coerciveness_evidence(self, text_data: str) -> List[str]:
        """提取强制性证据"""
        evidence = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if any(indicator in sentence for indicator in ['必须', '应当', '强制', '约束']):
                evidence.append(sentence.strip())
                
        return evidence[:3]
    
    def _extract_independence_evidence(self, text_data: str) -> List[str]:
        """提取独立性证据"""
        evidence = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if any(indicator in sentence for indicator in ['自主', '独立', '稳定', '持续']):
                evidence.append(sentence.strip())
                
        return evidence[:3]
    
    def _calculate_quality_metrics(self, externality: float, 
                                 coerciveness: float, 
                                 independence: float) -> Dict:
        """计算质量指标"""
        return {
            'completeness': (externality + coerciveness + independence) / 3.0,
            'consistency': 1.0 - abs(externality - coerciveness) / 10.0,
            'reliability': min(externality, coerciveness, independence),
            'overall_quality': (externality + coerciveness + independence) / 3.0
        }
    
    def _identify_collective_representations(self, text_data: str) -> Dict:
        """识别集体表征"""
        representation_types = {
            '符号表征': ['旗帜', '标志', '象征', '符号', '仪式'],
            '语言表征': ['术语', '概念', '话语', '表达', '语言'],
            '行为表征': ['行为', '行动', '实践', '活动', '做法'],
            '制度表征': ['制度', '规则', '法律', '政策', '规范']
        }
        
        representations = {}
        for rep_type, indicators in representation_types.items():
            count = sum(text_data.count(indicator) for indicator in indicators)
            representations[rep_type] = {
                'count': count,
                'prominence': '高' if count >= 3 else '中' if count >= 1 else '低'
            }
            
        return representations
    
    def _analyze_value_system(self, text_data: str) -> Dict:
        """分析价值体系"""
        value_indicators = {
            '核心价值': ['自由', '平等', '正义', '民主', '人权'],
            '社会价值': ['公共利益', '社会责任', '集体利益', '社会福祉'],
            '群体价值': ['团结', '合作', '互助', '忠诚', '归属'],
            '个体价值': ['个人发展', '自我实现', '个人权利', '个性']
        }
        
        value_system = {}
        for value_type, indicators in value_indicators.items():
            count = sum(text_data.count(indicator) for indicator in indicators)
            value_system[value_type] = {
                'frequency': count,
                'importance': '高' if count >= 2 else '中' if count >= 1 else '低'
            }
            
        return value_system
    
    def _analyze_social_norms(self, text_data: str) -> Dict:
        """分析社会规范"""
        norm_types = {
            '正式规范': ['法律', '法规', '制度', '政策'],
            '非正式规范': ['道德', '习俗', '传统', '惯例'],
            '隐性规范': ['文化', '观念', '思维', '模式'],
            '新兴规范': ['时尚', '潮流', '网络', '流行']
        }
        
        social_norms = {}
        for norm_type, indicators in norm_types.items():
            count = sum(text_data.count(indicator) for indicator in indicators)
            social_norms[norm_type] = {
                'presence': count,
                'strength': '强' if count >= 3 else '中' if count >= 1 else '弱'
            }
            
        return social_norms
    
    def _analyze_collective_emotions(self, text_data: str) -> Dict:
        """分析集体情感"""
        emotion_indicators = {
            '积极情感': ['自豪', '信心', '希望', '热情', '认同'],
            '消极情感': ['焦虑', '恐惧', '愤怒', '不满', '担忧'],
            '中性情感': ['理性', '客观', '冷静', '审慎', '理性']
        }
        
        collective_emotions = {}
        for emotion_type, indicators in emotion_indicators.items():
            count = sum(text_data.count(indicator) for indicator in indicators)
            collective_emotions[emotion_type] = {
                'intensity': count,
                'dominance': '主导' if count >= 2 else '存在' if count >= 1 else '缺失'
            }
            
        return collective_emotions
    
    def _calculate_consciousness_strength(self, representations: Dict,
                                        value_system: Dict,
                                        social_norms: Dict) -> float:
        """计算集体意识强度"""
        rep_score = sum(1 for rep in representations.values() if rep['prominence'] == '高')
        value_score = sum(1 for value in value_system.values() if value['importance'] == '高')
        norm_score = sum(1 for norm in social_norms.values() if norm['strength'] == '强')
        
        max_score = 12  # 4 + 4 + 4
        return (rep_score + value_score + norm_score) / max_score * 10
    
    def _assess_consciousness_quality(self, representations: Dict,
                                    value_system: Dict,
                                    social_norms: Dict,
                                    collective_emotions: Dict) -> Dict:
        """评估集体意识分析质量"""
        return {
            'completeness': len([r for r in representations.values() if r['count'] > 0]) / 4.0,
            'depth': len([v for v in value_system.values() if v['frequency'] > 0]) / 4.0,
            'diversity': len([n for n in social_norms.values() if n['presence'] > 0]) / 4.0,
            'emotional_richness': len([e for e in collective_emotions.values() if e['intensity'] > 0]) / 3.0
        }
    
    def _identify_manifest_functions(self, text_data: str) -> List[Dict]:
        """识别显功能"""
        function_indicators = ['目的', '目标', '功能', '作用', '效果']
        functions = []
        
        sentences = re.split(r'[。！？]', text_data)
        for sentence in sentences:
            if any(indicator in sentence for indicator in function_indicators):
                functions.append({
                    'description': sentence.strip(),
                    'type': '显功能',
                    'visibility': '高'
                })
                
        return functions[:5]  # 返回前5个显功能
    
    def _identify_latent_functions(self, text_data: str) -> List[Dict]:
        """识别潜功能"""
        latent_indicators = ['影响', '后果', '结果', '效应', '作用']
        functions = []
        
        sentences = re.split(r'[。！？]', text_data)
        for sentence in sentences:
            if any(indicator in sentence for indicator in latent_indicators):
                if '意外' in sentence or '非预期' in sentence or '潜在' in sentence:
                    functions.append({
                        'description': sentence.strip(),
                        'type': '潜功能',
                        'visibility': '低'
                    })
                    
        return functions[:3]  # 返回前3个潜功能
    
    def _analyze_functional_substitutes(self, text_data: str) -> Dict:
        """分析功能替代"""
        substitute_indicators = ['替代', '取代', '替换', '代替', '互换']
        
        substitute_count = sum(text_data.count(indicator) for indicator in substitute_indicators)
        
        return {
            'substitute_potential': substitute_count,
            'substitute_likelihood': '高' if substitute_count >= 3 else '中' if substitute_count >= 1 else '低',
            'substitute_types': ['完全替代', '部分替代', '功能补充', '功能竞争']
        }
    
    def _analyze_functional_integration(self, text_data: str) -> Dict:
        """分析功能整合"""
        integration_indicators = ['协调', '配合', '整合', '统一', '和谐']
        conflict_indicators = ['冲突', '矛盾', '对立', '不一致', '冲突']
        
        integration_score = sum(text_data.count(indicator) for indicator in integration_indicators)
        conflict_score = sum(text_data.count(indicator) for indicator in conflict_indicators)
        
        return {
            'integration_level': integration_score,
            'conflict_level': conflict_score,
            'integration_quality': '高' if integration_score > conflict_score else '中' if integration_score == conflict_score else '低'
        }
    
    def _assess_functional_balance(self, manifest_functions: List[Dict],
                                 latent_functions: List[Dict]) -> Dict:
        """评估功能平衡"""
        return {
            'manifest_count': len(manifest_functions),
            'latent_count': len(latent_functions),
            'balance_ratio': len(latent_functions) / max(len(manifest_functions), 1),
            'analysis_depth': '深' if len(latent_functions) >= 2 else '中' if len(latent_functions) >= 1 else '浅'
        }
    
    def _evaluate_functional_analysis_quality(self, manifest_functions: List[Dict],
                                            latent_functions: List[Dict],
                                            functional_integration: Dict) -> Dict:
        """评估功能分析质量"""
        return {
            'completeness': (len(manifest_functions) + len(latent_functions)) / 8.0,
            'depth': len(latent_functions) / 3.0,
            'integration_awareness': 1.0 if functional_integration['integration_level'] > 0 else 0.5,
            'balance_quality': min(len(manifest_functions), len(latent_functions)) / max(len(manifest_functions), len(latent_functions), 1)
        }
    
    def _determine_solidarity_type(self, text_data: str) -> Dict:
        """判断团结类型"""
        mechanical_indicators = [
            '同质', '相似', '一致', '相同', '统一', '集体', '传统',
            '习俗', '压制', '约束', '一致', '认同'
        ]
        
        organic_indicators = [
            '异质', '差异', '多样', '分工', '专业', '个人', '自主',
            '独立', '互补', '协作', '合作', '契约'
        ]
        
        mechanical_score = sum(text_data.count(indicator) for indicator in mechanical_indicators)
        organic_score = sum(text_data.count(indicator) for indicator in organic_indicators)
        
        total_score = mechanical_score + organic_score
        if total_score == 0:
            solidarity_type = '未确定'
            mechanical_ratio = 0.5
        else:
            mechanical_ratio = mechanical_score / total_score
            if mechanical_ratio >= 0.7:
                solidarity_type = '机械团结主导'
            elif mechanical_ratio <= 0.3:
                solidarity_type = '有机团结主导'
            else:
                solidarity_type = '混合型团结'
        
        return {
            'type': solidarity_type,
            'mechanical_score': mechanical_score,
            'organic_score': organic_score,
            'mechanical_ratio': mechanical_ratio
        }
    
    def _analyze_social_differentiation(self, text_data: str) -> Dict:
        """分析社会分化"""
        differentiation_indicators = [
            '分化', '分层', '差异', '多样', '专业', '分工',
            '分类', '区别', '不同', '多元', '复杂'
        ]
        
        differentiation_score = sum(text_data.count(indicator) for indicator in differentiation_indicators)
        
        return {
            'differentiation_level': differentiation_score,
            'differentiation_degree': '高' if differentiation_score >= 5 else '中' if differentiation_score >= 2 else '低',
            'complexity_indicator': differentiation_score / 10.0
        }
    
    def _assess_integration_mechanisms(self, text_data: str) -> Dict:
        """评估整合机制"""
        mechanism_types = {
            '制度整合': ['法律', '制度', '政策', '法规'],
            '经济整合': ['市场', '经济', '分工', '交易'],
            '文化整合': ['文化', '价值', '认同', '传统'],
            '社会整合': ['社会', '组织', '网络', '群体']
        }
        
        mechanisms = {}
        for mech_type, indicators in mechanism_types.items():
            count = sum(text_data.count(indicator) for indicator in indicators)
            mechanisms[mech_type] = {
                'strength': count,
                'effectiveness': '强' if count >= 3 else '中' if count >= 1 else '弱'
            }
            
        return mechanisms
    
    def _analyze_change_trends(self, text_data: str) -> Dict:
        """分析变迁趋势"""
        change_indicators = {
            '现代化': ['现代', '发展', '进步', '革新'],
            '传统化': ['传统', '保守', '延续', '稳定'],
            '多元化': ['多元', '多样', '开放', '包容'],
            '全球化': ['全球', '国际', '世界', '跨国']
        }
        
        trends = {}
        for trend_type, indicators in change_indicators.items():
            count = sum(text_data.count(indicator) for indicator in indicators)
            trends[trend_type] = {
                'strength': count,
                'direction': '强' if count >= 3 else '中' if count >= 1 else '弱'
            }
            
        return trends
    
    def _calculate_solidarity_index(self, solidarity_type: Dict,
                                 social_differentiation: Dict,
                                 integration_mechanisms: Dict) -> float:
        """计算团结指数"""
        type_score = 1.0 - abs(solidarity_type['mechanical_ratio'] - 0.5) * 2  # 平衡型得分最高
        differentiation_score = social_differentiation['complexity_indicator']
        integration_score = sum(mech['strength'] for mech in integration_mechanisms.values()) / 20.0
        
        return (type_score + differentiation_score + integration_score) / 3.0 * 10
    
    def _evaluate_solidarity_analysis_quality(self, solidarity_type: Dict,
                                            social_differentiation: Dict,
                                            integration_mechanisms: Dict) -> Dict:
        """评估团结分析质量"""
        return {
            'type_clarity': 1.0 if solidarity_type['type'] != '未确定' else 0.5,
            'differentiation_depth': min(social_differentiation['differentiation_level'] / 5.0, 1.0),
            'integration_comprehensiveness': len([m for m in integration_mechanisms.values() if m['strength'] > 0]) / 4.0,
            'overall_quality': (solidarity_type['mechanical_score'] + solidarity_type['organic_score']) / 20.0
        }
    
    def generate_comprehensive_report(self) -> str:
        """生成综合分析报告"""
        report = []
        report.append("# 数字涂尔干社会分析报告\n")
        
        if 'social_fact_identification' in self.analysis_results:
            results = self.analysis_results['social_fact_identification']
            report.append("## 社会事实识别")
            report.append(f"**事实类型**: {results['fact_type']}")
            report.append(f"**外在性**: {results['externality']['level']} (分数: {results['externality']['score']:.2f})")
            report.append(f"**强制性**: {results['coerciveness']['level']} (分数: {results['coerciveness']['score']:.2f})")
            report.append(f"**独立性**: {results['independence']['level']} (分数: {results['independence']['score']:.2f})")
            report.append("")
        
        if 'collective_consciousness' in self.analysis_results:
            results = self.analysis_results['collective_consciousness']
            report.append("## 集体意识分析")
            report.append(f"**意识强度**: {results['consciousness_strength']:.2f}")
            
            report.append("### 集体表征")
            for rep_type, rep_data in results['representations'].items():
                report.append(f"- **{rep_type}**: {rep_data['prominence']} (频次: {rep_data['count']})")
            
            report.append("### 价值体系")
            for value_type, value_data in results['value_system'].items():
                report.append(f"- **{value_type}**: {value_data['importance']} (频次: {value_data['frequency']})")
            report.append("")
        
        if 'functional_analysis' in self.analysis_results:
            results = self.analysis_results['functional_analysis']
            report.append("## 功能分析")
            report.append(f"**显功能数量**: {len(results['manifest_functions'])}")
            report.append(f"**潜功能数量**: {len(results['latent_functions'])}")
            report.append(f"**功能平衡**: {results['functional_balance']['analysis_depth']}")
            report.append("")
        
        if 'social_solidarity' in self.analysis_results:
            results = self.analysis_results['social_solidarity']
            report.append("## 社会团结分析")
            report.append(f"**团结类型**: {results['solidarity_type']['type']}")
            report.append(f"**团结指数**: {results['solidarity_index']:.2f}")
            report.append(f"**分化程度**: {results['social_differentiation']['differentiation_degree']}")
            report.append("")
        
        return "\n".join(report)


def main():
    """示例用法"""
    analyzer = SocialFactAnalyzer()
    
    # 示例文本数据
    sample_text = """
    现代教育制度作为社会的重要组成部分，具有强烈的外在性和强制性。
    教育规范要求所有适龄儿童必须接受义务教育，这种约束力体现了
    社会对个体行为的规范作用。教育制度独立于个体意志而存在，
    具有历史延续性和结构稳定性。同时，教育也承载着传递文化价值、
    培养集体认同的重要功能，这些潜在功能往往被忽视。
    在现代社会中，教育分化日益明显，不同类型的教育满足不同的社会需求。
    """
    
    # 执行完整分析
    print("=== 社会事实识别 ===")
    fact_results = analyzer.identify_social_facts(sample_text)
    print(f"事实类型: {fact_results['fact_type']}")
    print(f"外在性: {fact_results['externality']['level']} ({fact_results['externality']['score']:.2f})")
    print(f"强制性: {fact_results['coerciveness']['level']} ({fact_results['coerciveness']['score']:.2f})")
    print(f"独立性: {fact_results['independence']['level']} ({fact_results['independence']['score']:.2f})")
    
    print("\n=== 集体意识分析 ===")
    consciousness_results = analyzer.analyze_collective_consciousness(sample_text)
    print(f"意识强度: {consciousness_results['consciousness_strength']:.2f}")
    
    print("\n=== 功能分析 ===")
    functional_results = analyzer.perform_functional_analysis(sample_text)
    print(f"显功能: {len(functional_results['manifest_functions'])}")
    print(f"潜功能: {len(functional_results['latent_functions'])}")
    
    print("\n=== 社会团结分析 ===")
    solidarity_results = analyzer.analyze_social_solidarity(sample_text)
    print(f"团结类型: {solidarity_results['solidarity_type']['type']}")
    print(f"团结指数: {solidarity_results['solidarity_index']:.2f}")
    
    print("\n=== 综合报告 ===")
    report = analyzer.generate_comprehensive_report()
    print(report)


if __name__ == "__main__":
    main()
