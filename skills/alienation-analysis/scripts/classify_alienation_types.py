#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
异化类型分类脚本
Alienation Type Classification Script

这个脚本识别和分类不同类型的异化现象，为精准分析提供基础。

作者: socienceAI.com
版本: 1.0.0
日期: 2025-12-21
"""

import re
import json
from typing import Dict, List, Tuple, Any
from collections import defaultdict

class AlienationTypeClassifier:
    """异化类型分类器"""
    
    def __init__(self):
        # 异化类型关键词映射
        self.alienation_keywords = {
            'labor_alienation': {
                'primary': [
                    '工作异化', '劳动异化', '职业异化', '工作满意度', '职业倦怠',
                    '工作压力', '劳动过程', '劳动成果', '职业发展', '工作自主性'
                ],
                'secondary': [
                    '技能发挥', '工作环境', '劳动条件', '职业规划', '工作意义',
                    '工作流程', '工作成果', '劳动价值', '职业认同', '工作关系'
                ],
                'contexts': ['职场', '工作', '职业', '劳动', '就业']
            },
            'social_alienation': {
                'primary': [
                    '社交异化', '人际关系', '社交焦虑', '孤独感', '社交隔离',
                    '社区关系', '邻里关系', '群体归属', '社会交往', '人际关系疏离'
                ],
                'secondary': [
                    '社交网络', '朋友圈', '社交媒体', '虚拟交往', '现实关系',
                    '社区参与', '社会支持', '集体认同', '社会联系', '交往质量'
                ],
                'contexts': ['社交', '人际关系', '社区', '群体', '交往']
            },
            'consumption_alienation': {
                'primary': [
                    '消费异化', '消费主义', '消费行为', '购物冲动', '消费满意度',
                    '物质欲望', '消费身份', '符号消费', '过度消费', '消费债务'
                ],
                'secondary': [
                    '消费观念', '消费习惯', '消费需求', '消费心理', '消费结构',
                    '消费金额', '消费频率', '消费决策', '消费价值', '消费影响'
                ],
                'contexts': ['消费', '购物', '物质', '购买', '消费行为']
            },
            'technology_alienation': {
                'primary': [
                    '技术异化', '技术依赖', '手机依赖', '网络成瘾', '数字生活',
                    '算法控制', '技术垄断', '智能设备', '屏幕时间', '技术焦虑'
                ],
                'secondary': [
                    '数字化', '虚拟现实', '人工智能', '大数据', '社交媒体',
                    '网络社交', '在线活动', '数字设备', '技术使用', '数字隔离'
                ],
                'contexts': ['技术', '数字', '网络', '智能', '在线']
            }
        }
        
        # 异化程度标识词
        self.severity_indicators = {
            'high': ['严重', '极度', '高度', '强烈', '深度', '突出', '明显'],
            'medium': ['中等', '一般', '适中', '适度', '普通', '常见'],
            'low': ['轻微', '轻度', '少量', '微弱', '轻度', '轻微']
        }
        
        # 异化表现特征
        self.alienation_patterns = {
            'labor_alienation': [
                r'工作.*?感到.*?不满足',
                r'职业.*?缺乏.*?意义',
                r'劳动.*?过程.*?机械化',
                r'工作.*?自主.*?受限',
                r'技能.*?无法.*?发挥'
            ],
            'social_alienation': [
                r'人际.*?关系.*?疏离',
                r'社交.*?感到.*?孤独',
                r'社区.*?缺乏.*?归属',
                r'交往.*?缺乏.*?深度',
                r'社会.*?联系.*?薄弱'
            ],
            'consumption_alienation': [
                r'消费.*?行为.*?冲动',
                r'购物.*?缺乏.*?理性',
                r'物质.*?欲望.*?过度',
                r'消费.*?身份.*?建构',
                r'消费.*?影响.*?生活'
            ],
            'technology_alienation': [
                r'技术.*?依赖.*?严重',
                r'数字.*?生活.*?失衡',
                r'网络.*?使用.*?过度',
                r'算法.*?控制.*?行为',
                r'智能.*?设备.*?控制'
            ]
        }
    
    def classify_alienation_types(self, text: str) -> Dict[str, Any]:
        """分类异化类型"""
        # 文本预处理
        processed_text = self._preprocess_text(text)
        
        # 关键词匹配分析
        keyword_scores = self._analyze_keywords(processed_text)
        
        # 模式匹配分析
        pattern_scores = self._analyze_patterns(processed_text)
        
        # 综合评分
        comprehensive_scores = self._calculate_comprehensive_scores(keyword_scores, pattern_scores)
        
        # 确定主要异化类型
        primary_types = self._identify_primary_types(comprehensive_scores)
        
        # 评估异化程度
        severity_assessment = self._assess_severity(processed_text, comprehensive_scores)
        
        return {
            'primary_types': primary_types,
            'comprehensive_scores': comprehensive_scores,
            'severity_assessment': severity_assessment,
            'keyword_analysis': keyword_scores,
            'pattern_analysis': pattern_scores,
            'classification_confidence': self._calculate_confidence(comprehensive_scores)
        }
    
    def _preprocess_text(self, text: str) -> str:
        """文本预处理"""
        # 去除多余空白
        text = re.sub(r'\s+', ' ', text.strip())
        # 统一标点符号
        text = re.sub(r'[，。！？；：""''（）【】]', '，', text)
        return text
    
    def _analyze_keywords(self, text: str) -> Dict[str, float]:
        """关键词匹配分析"""
        keyword_scores = {}
        
        for alienation_type, keywords_data in self.alienation_keywords.items():
            # 计算主关键词得分
            primary_score = self._calculate_keyword_match(text, keywords_data['primary'])
            
            # 计算次关键词得分
            secondary_score = self._calculate_keyword_match(text, keywords_data['secondary'])
            
            # 计算上下文得分
            context_score = self._calculate_context_match(text, keywords_data['contexts'])
            
            # 加权计算总得分
            total_score = (primary_score * 0.6 + secondary_score * 0.3 + context_score * 0.1)
            
            keyword_scores[alienation_type] = {
                'primary_score': primary_score,
                'secondary_score': secondary_score,
                'context_score': context_score,
                'total_score': total_score
            }
        
        return keyword_scores
    
    def _calculate_keyword_match(self, text: str, keywords: List[str]) -> float:
        """计算关键词匹配得分"""
        if not keywords:
            return 0.0
        
        matched_count = 0
        for keyword in keywords:
            if keyword in text:
                matched_count += 1
        
        return matched_count / len(keywords)
    
    def _calculate_context_match(self, text: str, contexts: List[str]) -> float:
        """计算上下文匹配得分"""
        if not contexts:
            return 0.0
        
        context_matches = 0
        for context in contexts:
            if context in text:
                context_matches += 1
        
        return context_matches / len(contexts)
    
    def _analyze_patterns(self, text: str) -> Dict[str, float]:
        """模式匹配分析"""
        pattern_scores = {}
        
        for alienation_type, patterns in self.alienation_patterns.items():
            matched_patterns = 0
            for pattern in patterns:
                if re.search(pattern, text):
                    matched_patterns += 1
            
            pattern_scores[alienation_type] = matched_patterns / len(patterns)
        
        return pattern_scores
    
    def _calculate_comprehensive_scores(self, keyword_scores: Dict, pattern_scores: Dict) -> Dict[str, float]:
        """计算综合得分"""
        comprehensive_scores = {}
        
        for alienation_type in keyword_scores:
            # 关键词得分权重
            keyword_weight = 0.7
            pattern_weight = 0.3
            
            keyword_score = keyword_scores[alienation_type]['total_score']
            pattern_score = pattern_scores.get(alienation_type, 0.0)
            
            comprehensive_score = keyword_score * keyword_weight + pattern_score * pattern_weight
            comprehensive_scores[alienation_type] = comprehensive_score
        
        return comprehensive_scores
    
    def _identify_primary_types(self, scores: Dict[str, float], threshold: float = 0.3) -> List[str]:
        """识别主要异化类型"""
        # 过滤低分类型
        filtered_scores = {k: v for k, v in scores.items() if v >= threshold}
        
        # 按得分排序
        sorted_types = sorted(filtered_scores.items(), key=lambda x: x[1], reverse=True)
        
        # 返回主要类型（得分最高的）
        if sorted_types:
            primary_score = sorted_types[0][1]
            primary_types = [t[0] for t in sorted_types if t[1] >= primary_score * 0.8]
            return primary_types
        
        return []
    
    def _assess_severity(self, text: str, scores: Dict[str, float]) -> Dict[str, Any]:
        """评估异化程度"""
        max_score = max(scores.values()) if scores else 0.0
        
        # 根据最高得分确定严重程度
        if max_score >= 0.8:
            severity_level = '高度异化'
        elif max_score >= 0.6:
            severity_level = '中度异化'
        elif max_score >= 0.4:
            severity_level = '轻度异化'
        else:
            severity_level = '基本正常'
        
        # 检查严重程度标识词
        severity_indicators = self._find_severity_indicators(text)
        
        return {
            'level': severity_level,
            'max_score': max_score,
            'severity_indicators': severity_indicators,
            'confidence': self._calculate_severity_confidence(max_score, severity_indicators)
        }
    
    def _find_severity_indicators(self, text: str) -> Dict[str, List[str]]:
        """查找严重程度标识词"""
        indicators = {}
        
        for level, keywords in self.severity_indicators.items():
            found_keywords = [kw for kw in keywords if kw in text]
            if found_keywords:
                indicators[level] = found_keywords
        
        return indicators
    
    def _calculate_severity_confidence(self, score: float, indicators: Dict[str, List[str]]) -> float:
        """计算严重程度评估置信度"""
        base_confidence = score
        
        # 根据标识词调整置信度
        if 'high' in indicators:
            base_confidence += 0.1
        elif 'medium' in indicators:
            base_confidence += 0.05
        
        return min(1.0, base_confidence)
    
    def _calculate_confidence(self, scores: Dict[str, float]) -> float:
        """计算分类置信度"""
        if not scores:
            return 0.0
        
        max_score = max(scores.values())
        second_max_score = sorted(scores.values(), reverse=True)[1] if len(scores) > 1 else 0
        
        # 置信度基于最高分和次高分的差距
        confidence = max_score - second_max_score
        
        # 标准化到0-1范围
        return min(1.0, max(0.0, confidence))
    
    def get_type_interpretation(self, alienation_type: str) -> Dict[str, str]:
        """获取异化类型解释"""
        interpretations = {
            'labor_alienation': {
                'name': '劳动异化',
                'description': '人在劳动过程中与劳动活动、劳动产品、人的本质以及他人关系的分离',
                'characteristics': '工作满意度低、技能发挥受限、劳动意义缺失、工作自主性不足',
                'intervention_focus': '改善工作环境、提高工作自主性、增强劳动意义感'
            },
            'social_alienation': {
                'name': '社会关系异化',
                'description': '人与人之间真实关系的异化，包括交往深度、真实性、意义感的缺失',
                'characteristics': '人际关系疏离、社交焦虑、孤独感、社区归属感缺失',
                'intervention_focus': '增强社交技能、建立深度关系、参与社区活动'
            },
            'consumption_alienation': {
                'name': '消费异化',
                'description': '消费行为与真实需求的分离，消费成为目的而非手段',
                'characteristics': '冲动消费、物质欲望过度、消费身份建构、符号消费',
                'intervention_focus': '理性消费教育、价值观重塑、消费行为引导'
            },
            'technology_alienation': {
                'name': '技术异化',
                'description': '技术对人的控制，人对技术的过度依赖',
                'characteristics': '技术依赖严重、数字生活失衡、算法控制行为、现实感丧失',
                'intervention_focus': '健康技术使用、数字生活平衡、技术依赖治疗'
            }
        }
        
        return interpretations.get(alienation_type, {})

def main():
    """测试函数"""
    classifier = AlienationTypeClassifier()
    
    # 测试文本
    test_texts = [
        "最近工作压力很大，感觉工作没有任何意义，技能也无法发挥，总是感到职业倦怠",
        "在人际关系中感到非常孤独，社交时总是焦虑，缺乏真正的朋友",
        "购物时总是冲动消费，物质欲望很强，总是通过购买东西来获得满足感",
        "对手机依赖很严重，离开手机就无法正常工作，数字化生活完全占据了生活"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"测试文本 {i}: {text}")
        result = classifier.classify_alienation_types(text)
        print(f"主要异化类型: {result['primary_types']}")
        print(f"严重程度: {result['severity_assessment']['level']}")
        print(f"置信度: {result['classification_confidence']:.2f}")
        print("-" * 50)

if __name__ == "__main__":
    main()