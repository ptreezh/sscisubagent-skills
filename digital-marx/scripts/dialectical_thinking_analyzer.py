#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
辩证思维算法模块 - 马克思主义辩证法三大规律的专业化实现
包含对立统一规律、量变质变规律、否定之否定规律的算法化分析
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any, Tuple
import re
from collections import Counter
import jieba
import jieba.analyse
from dataclasses import dataclass
from enum import Enum


class DialecticalLawType(Enum):
    """辩证法规律类型"""
    UNITY_OF_OPPOSITES = "对立统一规律"
    QUANTITY_QUALITY_CHANGE = "量变质变规律"
    NEGATION_OF_NEGATION = "否定之否定规律"


@dataclass
class Contradiction:
    """矛盾结构"""
    primary_aspect: str
    secondary_aspect: str
    unity_relationship: float
    struggle_intensity: float
    transformation_tendency: str
    development_stage: str


@dataclass
class QuantityQualityChange:
    """量变质变结构"""
    quantity_accumulation: float
    quality_leap_point: float
    gradual_process: List[str]
    revolutionary_change: List[str]
    change_direction: str


@dataclass
class NegationProcess:
    """否定之否定结构"""
    original_thesis: str
    first_negation: str
    second_negation: str
    spiral_trajectory: float
    developmental_level: str
    retention_elements: List[str]


class DialecticalThinkingAnalyzer:
    """辩证思维分析器"""
    
    def __init__(self):
        # 初始化jieba分词
        jieba.initialize()
        
        # 对立统一规律词汇库
        self.unity_of_opposites_vocabulary = {
            'contradiction_pairs': [
                ('生产力', '生产关系'), ('经济基础', '上层建筑'), ('无产阶级', '资产阶级'),
                ('公有制', '私有制'), ('计划', '市场'), ('民主', '集中'), ('自由', '必然'),
                ('现象', '本质'), ('形式', '内容'), ('原因', '结果'), ('可能', '现实'),
                ('个别', '一般'), ('特殊', '普遍'), ('相对', '绝对'), ('有限', '无限')
            ],
            'unity_indicators': [
                '相互依存', '相互联系', '相互促进', '相互制约', '相互影响', '相互作用',
                '统一', '一体', '不可分割', '辩证统一', '有机统一'
            ],
            'struggle_indicators': [
                '对立', '冲突', '矛盾', '斗争', '排斥', '对抗', '分歧', '差异',
                '斗争性', '对立性', '冲突性', '矛盾性'
            ],
            'transformation_indicators': [
                '转化', '转变', '变化', '发展', '飞跃', '质变', '突变', '演进',
                '相互转化', '辩证转化', '质的飞跃'
            ]
        }
        
        # 量变质变规律词汇库
        self.quantity_quality_vocabulary = {
            'quantity_indicators': [
                '数量', '程度', '水平', '规模', '速度', '效率', '比例', '比重',
                '积累', '增长', '提高', '扩大', '增加', '发展', '进步'
            ],
            'quality_indicators': [
                '性质', '本质', '特征', '特点', '属性', '状态', '阶段', '水平',
                '质变', '飞跃', '突破', '变革', '革命', '转型', '升级'
            ],
            'gradual_indicators': [
                '渐进', '逐步', '逐渐', '慢慢', '稳步', '持续', '渐进式', '循序渐进',
                '量的积累', '渐进发展', '平稳发展'
            ],
            'leap_indicators': [
                '飞跃', '突变', '质变', '革命', '突破', '跨越', '跃升', '剧变',
                '质的飞跃', '革命性变化', '根本性转变'
            ]
        }
        
        # 否定之否定规律词汇库
        self.negation_vocabulary = {
            'thesis_indicators': [
                '肯定', '正题', '原始', '初始', '起点', '基础', '根本', '本源',
                '原有状态', '初始状态', '原始形态'
            ],
            'negation_indicators': [
                '否定', '批判', '推翻', '打破', '超越', '克服', '扬弃', '变革',
                '辩证否定', '积极否定', '创造性否定'
            ],
            'retention_indicators': [
                '保留', '继承', '发扬', '吸收', '借鉴', '扬弃', '批判继承',
                '辩证扬弃', '积极扬弃', '创造性转化'
            ],
            'spiral_indicators': [
                '螺旋', '循环', '回归', '重现', '重复', '波浪', '周期', '阶段',
                '螺旋式上升', '波浪式前进', '周期性发展'
            ]
        }
        
        # 矛盾发展阶段定义
        self.contradiction_stages = {
            'latent': '潜在阶段',
            'emerging': '显现阶段', 
            'developing': '发展阶段',
            'acute': '激化阶段',
            'resolving': '解决阶段'
        }
        
        # 分析结果存储
        self.analysis_results = {}
    
    def analyze_unity_of_opposites(self, text_data: str) -> Dict:
        """分析对立统一规律"""
        
        processed_text = self._preprocess_text(text_data)
        keywords = jieba.analyse.extract_tags(processed_text, topK=100, withWeight=True)
        
        # 识别对立统一体
        contradictions = self._identify_contradictions(processed_text, keywords)
        
        # 分析矛盾的主要方面和次要方面
        primary_secondary_aspects = self._analyze_contradiction_aspects(processed_text, contradictions)
        
        # 评估统一性和斗争性
        unity_struggle_balance = self._assess_unity_struggle_balance(processed_text, keywords)
        
        # 分析矛盾转化趋势
        transformation_tendencies = self._analyze_transformation_tendencies(processed_text, keywords)
        
        # 判断矛盾发展阶段
        development_stages = self._determine_contradiction_stages(processed_text, contradictions)
        
        # 综合分析结果
        analysis_result = {
            'contradictions': contradictions,
            'primary_secondary_aspects': primary_secondary_aspects,
            'unity_struggle_balance': unity_struggle_balance,
            'transformation_tendencies': transformation_tendencies,
            'development_stages': development_stages,
            'dialectical_quality': self._assess_dialectical_quality(
                contradictions, unity_struggle_balance, transformation_tendencies
            )
        }
        
        self.analysis_results['unity_of_opposites'] = analysis_result
        return analysis_result
    
    def analyze_quantity_quality_change(self, text_data: str) -> Dict:
        """分析量变质变规律"""
        
        processed_text = self._preprocess_text(text_data)
        keywords = jieba.analyse.extract_tags(processed_text, topK=100, withWeight=True)
        
        # 识别量变积累过程
        quantity_accumulation = self._identify_quantity_accumulation(processed_text, keywords)
        
        # 检测质变飞跃点
        quality_leap_points = self._detect_quality_leap_points(processed_text, keywords)
        
        # 分析渐进性过程
        gradual_processes = self._analyze_gradual_processes(processed_text, keywords)
        
        # 识别革命性变化
        revolutionary_changes = self._identify_revolutionary_changes(processed_text, keywords)
        
        # 评估变化方向和趋势
        change_directions = self._assess_change_directions(processed_text, keywords)
        
        # 综合分析结果
        analysis_result = {
            'quantity_accumulation': quantity_accumulation,
            'quality_leap_points': quality_leap_points,
            'gradual_processes': gradual_processes,
            'revolutionary_changes': revolutionary_changes,
            'change_directions': change_directions,
            'quantity_quality_synthesis': self._synthesize_quantity_quality_analysis(
                quantity_accumulation, quality_leap_points, gradual_processes, revolutionary_changes
            )
        }
        
        self.analysis_results['quantity_quality_change'] = analysis_result
        return analysis_result
    
    def analyze_negation_of_negation(self, text_data: str) -> Dict:
        """分析否定之否定规律"""
        
        processed_text = self._preprocess_text(text_data)
        keywords = jieba.analyse.extract_tags(processed_text, topK=100, withWeight=True)
        
        # 识别正题（肯定）
        thesis_elements = self._identify_thesis_elements(processed_text, keywords)
        
        # 识别第一次否定
        first_negation_elements = self._identify_first_negation(processed_text, keywords)
        
        # 识别第二次否定
        second_negation_elements = self._identify_second_negation(processed_text, keywords)
        
        # 分析扬弃过程
        sublation_processes = self._analyze_sublation_processes(processed_text, keywords)
        
        # 识别螺旋式上升轨迹
        spiral_trajectories = self._identify_spiral_trajectories(processed_text, keywords)
        
        # 评估发展水平
        developmental_levels = self._assess_developmental_levels(
            thesis_elements, first_negation_elements, second_negation_elements
        )
        
        # 综合分析结果
        analysis_result = {
            'thesis_elements': thesis_elements,
            'first_negation_elements': first_negation_elements,
            'second_negation_elements': second_negation_elements,
            'sublation_processes': sublation_processes,
            'spiral_trajectories': spiral_trajectories,
            'developmental_levels': developmental_levels,
            'negation_synthesis': self._synthesize_negation_analysis(
                thesis_elements, first_negation_elements, second_negation_elements, spiral_trajectories
            )
        }
        
        self.analysis_results['negation_of_negation'] = analysis_result
        return analysis_result
    
    def comprehensive_dialectical_analysis(self, text_data: str) -> Dict:
        """综合辩证分析"""
        
        # 执行三大规律分析
        unity_analysis = self.analyze_unity_of_opposites(text_data)
        quantity_quality_analysis = self.analyze_quantity_quality_change(text_data)
        negation_analysis = self.analyze_negation_of_negation(text_data)
        
        # 分析三大规律的内在联系
        internal_connections = self._analyze_internal_connections(
            unity_analysis, quantity_quality_analysis, negation_analysis
        )
        
        # 评估整体辩证思维水平
        overall_dialectical_level = self._assess_overall_dialectical_level(
            unity_analysis, quantity_quality_analysis, negation_analysis
        )
        
        # 生成辩证思维建议
        dialectical_recommendations = self._generate_dialectical_recommendations(
            unity_analysis, quantity_quality_analysis, negation_analysis
        )
        
        # 综合结果
        comprehensive_result = {
            'unity_of_opposites': unity_analysis,
            'quantity_quality_change': quantity_quality_analysis,
            'negation_of_negation': negation_analysis,
            'internal_connections': internal_connections,
            'overall_dialectical_level': overall_dialectical_level,
            'dialectical_recommendations': dialectical_recommendations,
            'analysis_timestamp': pd.Timestamp.now().isoformat()
        }
        
        return comprehensive_result
    
    def _preprocess_text(self, text_data: str) -> str:
        """文本预处理"""
        text = re.sub(r'\s+', ' ', text_data.strip())
        return text
    
    def _identify_contradictions(self, text_data: str, keywords: List[Tuple]) -> List[Contradiction]:
        """识别对立统一体"""
        contradictions = []
        
        for pair in self.unity_of_opposites_vocabulary['contradiction_pairs']:
            aspect1, aspect2 = pair
            
            # 计算两个方面的出现频率
            freq1 = sum(weight for word, weight in keywords if word in aspect1)
            freq2 = sum(weight for word, weight in keywords if word in aspect2)
            
            # 如果两个方面都出现，则认为存在矛盾
            if freq1 > 0 and freq2 > 0:
                # 计算统一关系强度
                unity_score = self._calculate_unity_score(text_data, aspect1, aspect2)
                
                # 计算斗争强度
                struggle_score = self._calculate_struggle_score(text_data, aspect1, aspect2)
                
                # 判断转化趋势
                transformation_tendency = self._determine_transformation_tendency(
                    text_data, aspect1, aspect2
                )
                
                # 判断发展阶段
                development_stage = self._determine_contradiction_stage(
                    text_data, aspect1, aspect2
                )
                
                contradiction = Contradiction(
                    primary_aspect=aspect1 if freq1 >= freq2 else aspect2,
                    secondary_aspect=aspect2 if freq1 >= freq2 else aspect1,
                    unity_relationship=unity_score,
                    struggle_intensity=struggle_score,
                    transformation_tendency=transformation_tendency,
                    development_stage=development_stage
                )
                
                contradictions.append(contradiction)
        
        return contradictions
    
    def _calculate_unity_score(self, text_data: str, aspect1: str, aspect2: str) -> float:
        """计算统一关系强度"""
        unity_indicators = self.unity_of_opposites_vocabulary['unity_indicators']
        
        # 查找统一性指标的出现
        unity_count = 0
        for indicator in unity_indicators:
            if indicator in text_data:
                # 检查指标是否与两个对立面相关
                context_window = 50  # 上下文窗口大小
                for match in re.finditer(indicator, text_data):
                    start = max(0, match.start() - context_window)
                    end = min(len(text_data), match.end() + context_window)
                    context = text_data[start:end]
                    
                    if aspect1 in context and aspect2 in context:
                        unity_count += 1
        
        # 归一化分数
        return min(unity_count * 2.0, 10.0)
    
    def _calculate_struggle_score(self, text_data: str, aspect1: str, aspect2: str) -> float:
        """计算斗争强度"""
        struggle_indicators = self.unity_of_opposites_vocabulary['struggle_indicators']
        
        struggle_count = 0
        for indicator in struggle_indicators:
            if indicator in text_data:
                context_window = 50
                for match in re.finditer(indicator, text_data):
                    start = max(0, match.start() - context_window)
                    end = min(len(text_data), match.end() + context_window)
                    context = text_data[start:end]
                    
                    if aspect1 in context and aspect2 in context:
                        struggle_count += 1
        
        return min(struggle_count * 2.0, 10.0)
    
    def _determine_transformation_tendency(self, text_data: str, aspect1: str, aspect2: str) -> str:
        """判断转化趋势"""
        transformation_indicators = self.unity_of_opposites_vocabulary['transformation_indicators']
        
        transformation_count = 0
        for indicator in transformation_indicators:
            if indicator in text_data:
                context_window = 50
                for match in re.finditer(indicator, text_data):
                    start = max(0, match.start() - context_window)
                    end = min(len(text_data), match.end() + context_window)
                    context = text_data[start:end]
                    
                    if aspect1 in context and aspect2 in context:
                        transformation_count += 1
        
        if transformation_count >= 3:
            return "活跃转化"
        elif transformation_count >= 1:
            return "潜在转化"
        else:
            return "相对稳定"
    
    def _determine_contradiction_stage(self, text_data: str, aspect1: str, aspect2: str) -> str:
        """判断矛盾发展阶段"""
        # 根据斗争强度和转化趋势判断阶段
        struggle_score = self._calculate_struggle_score(text_data, aspect1, aspect2)
        transformation_tendency = self._determine_transformation_tendency(text_data, aspect1, aspect2)
        
        if struggle_score >= 8.0:
            return self.contradiction_stages['acute']
        elif struggle_score >= 5.0:
            return self.contradiction_stages['developing']
        elif struggle_score >= 2.0:
            return self.contradiction_stages['emerging']
        else:
            return self.contradiction_stages['latent']
    
    def _analyze_contradiction_aspects(self, text_data: str, contradictions: List[Contradiction]) -> Dict:
        """分析矛盾的主要方面和次要方面"""
        aspects_analysis = {}
        
        for contradiction in contradictions:
            # 主要方面分析
            primary_dominance = self._analyze_aspect_dominance(
                text_data, contradiction.primary_aspect
            )
            
            # 次要方面分析
            secondary_dominance = self._analyze_aspect_dominance(
                text_data, contradiction.secondary_aspect
            )
            
            # 主要方面与次要方面的关系
            aspect_relationship = self._analyze_aspect_relationship(
                text_data, contradiction.primary_aspect, contradiction.secondary_aspect
            )
            
            aspects_analysis[f"{contradiction.primary_aspect}-{contradiction.secondary_aspect}"] = {
                'primary_dominance': primary_dominance,
                'secondary_dominance': secondary_dominance,
                'aspect_relationship': aspect_relationship,
                'dominant_aspect': contradiction.primary_aspect
            }
        
        return aspects_analysis
    
    def _analyze_aspect_dominance(self, text_data: str, aspect: str) -> Dict:
        """分析方面的主导性"""
        keywords = jieba.analyse.extract_tags(text_data, topK=100, withWeight=True)
        
        # 计算方面的权重
        aspect_weight = sum(weight for word, weight in keywords if word in aspect)
        
        # 查找主导性指标
        dominance_indicators = ['主导', '主要', '决定', '支配', '控制', '核心', '关键']
        dominance_count = sum(1 for indicator in dominance_indicators if indicator in text_data)
        
        return {
            'weight': aspect_weight,
            'dominance_indicators': dominance_count,
            'dominance_level': self._determine_dominance_level(aspect_weight, dominance_count)
        }
    
    def _determine_dominance_level(self, weight: float, indicators_count: int) -> str:
        """确定主导性水平"""
        if weight >= 5.0 and indicators_count >= 2:
            return "强主导"
        elif weight >= 3.0 or indicators_count >= 1:
            return "中等主导"
        else:
            return "弱主导"
    
    def _analyze_aspect_relationship(self, text_data: str, primary: str, secondary: str) -> str:
        """分析主要方面与次要方面的关系"""
        relationship_indicators = {
            '支配关系': ['支配', '决定', '主导', '控制'],
            '相互促进': ['促进', '推动', '带动', '拉动'],
            '相互制约': ['制约', '限制', '约束', '影响'],
            '辩证统一': ['统一', '结合', '融合', '协调']
        }
        
        max_count = 0
        relationship_type = '未知关系'
        
        for rel_type, indicators in relationship_indicators.items():
            count = sum(1 for indicator in indicators if indicator in text_data)
            if count > max_count:
                max_count = count
                relationship_type = rel_type
        
        return relationship_type
    
    def _assess_unity_struggle_balance(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """评估统一性和斗争性的平衡"""
        # 计算统一性分数
        unity_score = 0
        for indicator in self.unity_of_opposites_vocabulary['unity_indicators']:
            unity_score += sum(weight for word, weight in keywords if word in indicator)
        
        # 计算斗争性分数
        struggle_score = 0
        for indicator in self.unity_of_opposites_vocabulary['struggle_indicators']:
            struggle_score += sum(weight for word, weight in keywords if word in indicator)
        
        # 归一化
        unity_score = min(unity_score, 10.0)
        struggle_score = min(struggle_score, 10.0)
        
        # 判断平衡状态
        if abs(unity_score - struggle_score) <= 2.0:
            balance_state = "相对平衡"
        elif unity_score > struggle_score:
            balance_state = "统一性主导"
        else:
            balance_state = "斗争性主导"
        
        return {
            'unity_score': unity_score,
            'struggle_score': struggle_score,
            'balance_state': balance_state,
            'balance_quality': self._assess_balance_quality(unity_score, struggle_score)
        }
    
    def _assess_balance_quality(self, unity_score: float, struggle_score: float) -> str:
        """评估平衡质量"""
        total_score = unity_score + struggle_score
        
        if total_score >= 15.0:
            return "高质量平衡"
        elif total_score >= 10.0:
            return "中等质量平衡"
        else:
            return "低质量平衡"
    
    def _analyze_transformation_tendencies(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析矛盾转化趋势"""
        transformation_indicators = self.unity_of_opposites_vocabulary['transformation_indicators']
        
        transformation_score = 0
        transformation_types = {}
        
        for indicator in transformation_indicators:
            indicator_score = sum(weight for word, weight in keywords if word in indicator)
            transformation_score += indicator_score
            
            # 分类转化类型
            if '转化' in indicator:
                transformation_types['一般转化'] = transformation_types.get('一般转化', 0) + indicator_score
            elif '质变' in indicator or '飞跃' in indicator:
                transformation_types['质的转化'] = transformation_types.get('质的转化', 0) + indicator_score
            elif '发展' in indicator:
                transformation_types['发展转化'] = transformation_types.get('发展转化', 0) + indicator_score
        
        # 判断转化强度
        if transformation_score >= 8.0:
            transformation_intensity = "强转化趋势"
        elif transformation_score >= 4.0:
            transformation_intensity = "中等转化趋势"
        else:
            transformation_intensity = "弱转化趋势"
        
        return {
            'transformation_score': transformation_score,
            'transformation_intensity': transformation_intensity,
            'transformation_types': transformation_types,
            'primary_transformation_type': max(transformation_types.items(), key=lambda x: x[1])[0] if transformation_types else '无'
        }
    
    def _determine_contradiction_stages(self, text_data: str, contradictions: List[Contradiction]) -> Dict:
        """判断矛盾发展阶段"""
        stage_analysis = {}
        
        for contradiction in contradictions:
            stage_analysis[f"{contradiction.primary_aspect}-{contradiction.secondary_aspect}"] = {
                'current_stage': contradiction.development_stage,
                'stage_characteristics': self._describe_stage_characteristics(contradiction.development_stage),
                'next_stage_tendency': self._predict_next_stage(contradiction)
            }
        
        return stage_analysis
    
    def _describe_stage_characteristics(self, stage: str) -> str:
        """描述阶段特征"""
        stage_descriptions = {
            '潜在阶段': '矛盾尚未显现，处于潜伏状态',
            '显现阶段': '矛盾开始显现，对立面初步形成',
            '发展阶段': '矛盾得到发展，各方面逐步展开',
            '激化阶段': '矛盾激化，斗争性突出',
            '解决阶段': '矛盾开始解决，向新的形态转化'
        }
        return stage_descriptions.get(stage, '未知阶段')
    
    def _predict_next_stage(self, contradiction: Contradiction) -> str:
        """预测下一阶段"""
        stage_progression = {
            '潜在阶段': '显现阶段',
            '显现阶段': '发展阶段',
            '发展阶段': '激化阶段',
            '激化阶段': '解决阶段',
            '解决阶段': '新的矛盾循环'
        }
        
        current_stage = contradiction.development_stage
        return stage_progression.get(current_stage, '未知')
    
    def _assess_dialectical_quality(self, contradictions: List[Contradiction], 
                                  unity_struggle_balance: Dict, 
                                  transformation_tendencies: Dict) -> Dict:
        """评估辩证思维质量"""
        
        # 矛盾识别质量
        contradiction_quality = len(contradictions) * 2.0  # 每个矛盾2分
        contradiction_quality = min(contradiction_quality, 10.0)
        
        # 统一斗争平衡质量
        balance_score = (unity_struggle_balance['unity_score'] + 
                        unity_struggle_balance['struggle_score']) / 2
        
        # 转化趋势质量
        transformation_quality = transformation_tendencies['transformation_score']
        transformation_quality = min(transformation_quality, 10.0)
        
        # 综合质量分数
        overall_quality = (contradiction_quality + balance_score + transformation_quality) / 3
        
        return {
            'contradiction_quality': contradiction_quality,
            'balance_quality': balance_score,
            'transformation_quality': transformation_quality,
            'overall_quality': overall_quality,
            'quality_level': self._determine_quality_level(overall_quality)
        }
    
    def _determine_quality_level(self, score: float) -> str:
        """确定质量等级"""
        if score >= 8.0:
            return "优秀"
        elif score >= 6.0:
            return "良好"
        elif score >= 4.0:
            return "一般"
        else:
            return "需要改进"
    
    def _identify_quantity_accumulation(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """识别量变积累过程"""
        quantity_indicators = self.quantity_quality_vocabulary['quantity_indicators']
        
        accumulation_score = 0
        accumulation_processes = []
        
        for indicator in quantity_indicators:
            indicator_score = sum(weight for word, weight in keywords if word in indicator)
            accumulation_score += indicator_score
            
            if indicator_score > 0:
                # 提取相关的量变过程描述
                processes = self._extract_quantity_processes(text_data, indicator)
                accumulation_processes.extend(processes)
        
        return {
            'accumulation_score': accumulation_score,
            'accumulation_level': self._determine_accumulation_level(accumulation_score),
            'accumulation_processes': accumulation_processes
        }
    
    def _determine_accumulation_level(self, score: float) -> str:
        """确定积累水平"""
        if score >= 8.0:
            return "高度积累"
        elif score >= 5.0:
            return "中等积累"
        elif score >= 2.0:
            return "初步积累"
        else:
            return "积累不足"
    
    def _extract_quantity_processes(self, text_data: str, indicator: str) -> List[str]:
        """提取量变过程描述"""
        processes = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if indicator in sentence and len(sentence.strip()) > 10:
                processes.append(sentence.strip())
        
        return processes[:3]  # 返回前3个相关过程
    
    def _detect_quality_leap_points(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """检测质变飞跃点"""
        leap_indicators = self.quantity_quality_vocabulary['leap_indicators']
        
        leap_score = 0
        leap_points = []
        
        for indicator in leap_indicators:
            indicator_score = sum(weight for word, weight in keywords if word in indicator)
            leap_score += indicator_score
            
            if indicator_score > 0:
                # 提取飞跃点描述
                points = self._extract_leap_points(text_data, indicator)
                leap_points.extend(points)
        
        return {
            'leap_score': leap_score,
            'leap_intensity': self._determine_leap_intensity(leap_score),
            'leap_points': leap_points
        }
    
    def _determine_leap_intensity(self, score: float) -> str:
        """确定飞跃强度"""
        if score >= 6.0:
            return "强飞跃"
        elif score >= 3.0:
            return "中等飞跃"
        elif score >= 1.0:
            return "弱飞跃"
        else:
            return "无明显飞跃"
    
    def _extract_leap_points(self, text_data: str, indicator: str) -> List[str]:
        """提取飞跃点描述"""
        points = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if indicator in sentence and len(sentence.strip()) > 10:
                points.append(sentence.strip())
        
        return points[:3]
    
    def _analyze_gradual_processes(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析渐进性过程"""
        gradual_indicators = self.quantity_quality_vocabulary['gradual_indicators']
        
        gradual_score = 0
        gradual_processes = []
        
        for indicator in gradual_indicators:
            indicator_score = sum(weight for word, weight in keywords if word in indicator)
            gradual_score += indicator_score
            
            if indicator_score > 0:
                processes = self._extract_gradual_processes(text_data, indicator)
                gradual_processes.extend(processes)
        
        return {
            'gradual_score': gradual_score,
            'gradual_level': self._determine_gradual_level(gradual_score),
            'gradual_processes': gradual_processes
        }
    
    def _determine_gradual_level(self, score: float) -> str:
        """确定渐进水平"""
        if score >= 6.0:
            return "高度渐进"
        elif score >= 3.0:
            return "中等渐进"
        elif score >= 1.0:
            return "初步渐进"
        else:
            return "渐进不明显"
    
    def _extract_gradual_processes(self, text_data: str, indicator: str) -> List[str]:
        """提取渐进过程描述"""
        processes = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if indicator in sentence and len(sentence.strip()) > 10:
                processes.append(sentence.strip())
        
        return processes[:3]
    
    def _identify_revolutionary_changes(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """识别革命性变化"""
        revolutionary_indicators = ['革命', '变革', '突破', '跨越', '转型', '升级']
        
        revolutionary_score = 0
        revolutionary_changes = []
        
        for indicator in revolutionary_indicators:
            indicator_score = sum(weight for word, weight in keywords if word in indicator)
            revolutionary_score += indicator_score
            
            if indicator_score > 0:
                changes = self._extract_revolutionary_changes(text_data, indicator)
                revolutionary_changes.extend(changes)
        
        return {
            'revolutionary_score': revolutionary_score,
            'revolutionary_level': self._determine_revolutionary_level(revolutionary_score),
            'revolutionary_changes': revolutionary_changes
        }
    
    def _determine_revolutionary_level(self, score: float) -> str:
        """确定革命性水平"""
        if score >= 6.0:
            return "高度革命性"
        elif score >= 3.0:
            return "中等革命性"
        elif score >= 1.0:
            return "初步革命性"
        else:
            return "革命性不明显"
    
    def _extract_revolutionary_changes(self, text_data: str, indicator: str) -> List[str]:
        """提取革命性变化描述"""
        changes = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if indicator in sentence and len(sentence.strip()) > 10:
                changes.append(sentence.strip())
        
        return changes[:3]
    
    def _assess_change_directions(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """评估变化方向和趋势"""
        direction_indicators = {
            'forward': ['前进', '发展', '进步', '提升', '改善', '优化'],
            'backward': ['倒退', '退步', '恶化', '下降', '衰退'],
            'stable': ['稳定', '保持', '维持', '持续', '平稳']
        }
        
        direction_scores = {}
        for direction, indicators in direction_indicators.items():
            score = sum(weight for word, weight in keywords 
                       for indicator in indicators if word in indicator)
            direction_scores[direction] = score
        
        # 确定主要方向
        primary_direction = max(direction_scores.items(), key=lambda x: x[1])[0]
        
        return {
            'direction_scores': direction_scores,
            'primary_direction': primary_direction,
            'direction_certainty': self._assess_direction_certainty(direction_scores)
        }
    
    def _assess_direction_certainty(self, direction_scores: Dict) -> str:
        """评估方向确定性"""
        max_score = max(direction_scores.values())
        total_score = sum(direction_scores.values())
        
        if total_score == 0:
            return "方向不明"
        
        certainty_ratio = max_score / total_score
        
        if certainty_ratio >= 0.6:
            return "方向明确"
        elif certainty_ratio >= 0.4:
            return "方向较明确"
        else:
            return "方向模糊"
    
    def _synthesize_quantity_quality_analysis(self, quantity_accumulation: Dict,
                                            quality_leap_points: Dict,
                                            gradual_processes: Dict,
                                            revolutionary_changes: Dict) -> Dict:
        """综合量变质变分析"""
        
        # 计算量变质变协调性
        coordination_score = self._calculate_quantity_quality_coordination(
            quantity_accumulation, quality_leap_points
        )
        
        # 评估发展模式
        development_pattern = self._assess_development_pattern(
            gradual_processes, revolutionary_changes
        )
        
        # 判断发展阶段
        development_stage = self._determine_development_stage(
            quantity_accumulation, quality_leap_points
        )
        
        return {
            'coordination_score': coordination_score,
            'development_pattern': development_pattern,
            'development_stage': development_stage,
            'synthesis_quality': self._assess_synthesis_quality(
                coordination_score, development_pattern
            )
        }
    
    def _calculate_quantity_quality_coordination(self, quantity_accumulation: Dict,
                                               quality_leap_points: Dict) -> float:
        """计算量变质变协调性"""
        quantity_score = quantity_accumulation.get('accumulation_score', 0)
        quality_score = quality_leap_points.get('leap_score', 0)
        
        # 理想情况下，量变积累应该为质变飞跃做准备
        # 协调性 = 量变分数的适当性 + 质变分数的合理性
        if quantity_score >= 5.0 and quality_score >= 3.0:
            coordination = 8.0
        elif quantity_score >= 3.0 and quality_score >= 1.0:
            coordination = 6.0
        elif quantity_score >= 1.0 or quality_score >= 1.0:
            coordination = 4.0
        else:
            coordination = 2.0
        
        return coordination
    
    def _assess_development_pattern(self, gradual_processes: Dict,
                                   revolutionary_changes: Dict) -> str:
        """评估发展模式"""
        gradual_score = gradual_processes.get('gradual_score', 0)
        revolutionary_score = revolutionary_changes.get('revolutionary_score', 0)
        
        if gradual_score >= 5.0 and revolutionary_score >= 3.0:
            return "渐进与飞跃结合"
        elif gradual_score >= 5.0:
            return "渐进发展为主"
        elif revolutionary_score >= 3.0:
            return "飞跃发展为主"
        else:
            return "发展模式不明显"
    
    def _determine_development_stage(self, quantity_accumulation: Dict,
                                   quality_leap_points: Dict) -> str:
        """判断发展阶段"""
        quantity_level = quantity_accumulation.get('accumulation_level', '')
        leap_intensity = quality_leap_points.get('leap_intensity', '')
        
        if quantity_level == "高度积累" and leap_intensity == "强飞跃":
            return "质变阶段"
        elif quantity_level in ["中等积累", "高度积累"]:
            return "量变积累阶段"
        elif leap_intensity in ["中等飞跃", "强飞跃"]:
            return "质变准备阶段"
        else:
            return "初始发展阶段"
    
    def _assess_synthesis_quality(self, coordination_score: float,
                                 development_pattern: str) -> str:
        """评估综合质量"""
        if coordination_score >= 7.0 and "结合" in development_pattern:
            return "优秀"
        elif coordination_score >= 5.0:
            return "良好"
        elif coordination_score >= 3.0:
            return "一般"
        else:
            return "需要改进"
    
    def _identify_thesis_elements(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """识别正题（肯定）元素"""
        thesis_indicators = self.negation_vocabulary['thesis_indicators']
        
        thesis_score = 0
        thesis_elements = []
        
        for indicator in thesis_indicators:
            indicator_score = sum(weight for word, weight in keywords if word in indicator)
            thesis_score += indicator_score
            
            if indicator_score > 0:
                elements = self._extract_thesis_elements(text_data, indicator)
                thesis_elements.extend(elements)
        
        return {
            'thesis_score': thesis_score,
            'thesis_strength': self._determine_thesis_strength(thesis_score),
            'thesis_elements': thesis_elements
        }
    
    def _determine_thesis_strength(self, score: float) -> str:
        """确定正题强度"""
        if score >= 6.0:
            return "强正题"
        elif score >= 3.0:
            return "中等正题"
        elif score >= 1.0:
            return "弱正题"
        else:
            return "正题不明显"
    
    def _extract_thesis_elements(self, text_data: str, indicator: str) -> List[str]:
        """提取正题元素"""
        elements = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if indicator in sentence and len(sentence.strip()) > 10:
                elements.append(sentence.strip())
        
        return elements[:3]
    
    def _identify_first_negation(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """识别第一次否定"""
        negation_indicators = self.negation_vocabulary['negation_indicators']
        
        negation_score = 0
        negation_elements = []
        
        for indicator in negation_indicators:
            indicator_score = sum(weight for word, weight in keywords if word in indicator)
            negation_score += indicator_score
            
            if indicator_score > 0:
                elements = self._extract_negation_elements(text_data, indicator)
                negation_elements.extend(elements)
        
        return {
            'negation_score': negation_score,
            'negation_intensity': self._determine_negation_intensity(negation_score),
            'negation_elements': negation_elements
        }
    
    def _determine_negation_intensity(self, score: float) -> str:
        """确定否定强度"""
        if score >= 6.0:
            return "强否定"
        elif score >= 3.0:
            return "中等否定"
        elif score >= 1.0:
            return "弱否定"
        else:
            return "否定不明显"
    
    def _extract_negation_elements(self, text_data: str, indicator: str) -> List[str]:
        """提取否定元素"""
        elements = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if indicator in sentence and len(sentence.strip()) > 10:
                elements.append(sentence.strip())
        
        return elements[:3]
    
    def _identify_second_negation(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """识别第二次否定"""
        # 第二次否定通常通过"再否定"、"重新否定"等词汇识别
        second_negation_indicators = ['再否定', '重新否定', '二次否定', '否定之否定']
        
        second_negation_score = 0
        second_negation_elements = []
        
        for indicator in second_negation_indicators:
            indicator_score = sum(weight for word, weight in keywords if word in indicator)
            second_negation_score += indicator_score
            
            if indicator_score > 0:
                elements = self._extract_second_negation_elements(text_data, indicator)
                second_negation_elements.extend(elements)
        
        return {
            'second_negation_score': second_negation_score,
            'second_negation_intensity': self._determine_second_negation_intensity(second_negation_score),
            'second_negation_elements': second_negation_elements
        }
    
    def _determine_second_negation_intensity(self, score: float) -> str:
        """确定第二次否定强度"""
        if score >= 4.0:
            return "强二次否定"
        elif score >= 2.0:
            return "中等二次否定"
        elif score >= 1.0:
            return "弱二次否定"
        else:
            return "二次否定不明显"
    
    def _extract_second_negation_elements(self, text_data: str, indicator: str) -> List[str]:
        """提取第二次否定元素"""
        elements = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if indicator in sentence and len(sentence.strip()) > 10:
                elements.append(sentence.strip())
        
        return elements[:3]
    
    def _analyze_sublation_processes(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析扬弃过程"""
        retention_indicators = self.negation_vocabulary['retention_indicators']
        
        retention_score = 0
        retention_elements = []
        
        for indicator in retention_indicators:
            indicator_score = sum(weight for word, weight in keywords if word in indicator)
            retention_score += indicator_score
            
            if indicator_score > 0:
                elements = self._extract_retention_elements(text_data, indicator)
                retention_elements.extend(elements)
        
        return {
            'retention_score': retention_score,
            'sublation_level': self._determine_sublation_level(retention_score),
            'retention_elements': retention_elements
        }
    
    def _determine_sublation_level(self, score: float) -> str:
        """确定扬弃水平"""
        if score >= 6.0:
            return "高度扬弃"
        elif score >= 3.0:
            return "中等扬弃"
        elif score >= 1.0:
            return "初步扬弃"
        else:
            return "扬弃不明显"
    
    def _extract_retention_elements(self, text_data: str, indicator: str) -> List[str]:
        """提取扬弃元素"""
        elements = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if indicator in sentence and len(sentence.strip()) > 10:
                elements.append(sentence.strip())
        
        return elements[:3]
    
    def _identify_spiral_trajectories(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """识别螺旋式上升轨迹"""
        spiral_indicators = self.negation_vocabulary['spiral_indicators']
        
        spiral_score = 0
        spiral_elements = []
        
        for indicator in spiral_indicators:
            indicator_score = sum(weight for word, weight in keywords if word in indicator)
            spiral_score += indicator_score
            
            if indicator_score > 0:
                elements = self._extract_spiral_elements(text_data, indicator)
                spiral_elements.extend(elements)
        
        return {
            'spiral_score': spiral_score,
            'spiral_intensity': self._determine_spiral_intensity(spiral_score),
            'spiral_elements': spiral_elements
        }
    
    def _determine_spiral_intensity(self, score: float) -> str:
        """确定螺旋强度"""
        if score >= 6.0:
            return "强螺旋"
        elif score >= 3.0:
            return "中等螺旋"
        elif score >= 1.0:
            return "弱螺旋"
        else:
            return "螺旋不明显"
    
    def _extract_spiral_elements(self, text_data: str, indicator: str) -> List[str]:
        """提取螺旋元素"""
        elements = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            if indicator in sentence and len(sentence.strip()) > 10:
                elements.append(sentence.strip())
        
        return elements[:3]
    
    def _assess_developmental_levels(self, thesis_elements: Dict,
                                   first_negation_elements: Dict,
                                   second_negation_elements: Dict) -> Dict:
        """评估发展水平"""
        thesis_score = thesis_elements.get('thesis_score', 0)
        first_negation_score = first_negation_elements.get('negation_score', 0)
        second_negation_score = second_negation_elements.get('second_negation_score', 0)
        
        # 计算发展水平
        if second_negation_score >= 3.0:
            developmental_level = "高级发展阶段"
        elif first_negation_score >= 3.0:
            developmental_level = "中级发展阶段"
        elif thesis_score >= 3.0:
            developmental_level = "初级发展阶段"
        else:
            developmental_level = "初始阶段"
        
        return {
            'developmental_level': developmental_level,
            'developmental_completeness': self._assess_developmental_completeness(
                thesis_score, first_negation_score, second_negation_score
            )
        }
    
    def _assess_developmental_completeness(self, thesis_score: float,
                                         first_negation_score: float,
                                         second_negation_score: float) -> str:
        """评估发展完整性"""
        if thesis_score >= 3.0 and first_negation_score >= 3.0 and second_negation_score >= 3.0:
            return "完整发展周期"
        elif thesis_score >= 3.0 and first_negation_score >= 3.0:
            return "部分发展周期"
        elif thesis_score >= 3.0:
            return "初始发展阶段"
        else:
            return "发展不完整"
    
    def _synthesize_negation_analysis(self, thesis_elements: Dict,
                                     first_negation_elements: Dict,
                                     second_negation_elements: Dict,
                                     spiral_trajectories: Dict) -> Dict:
        """综合否定之否定分析"""
        
        # 计算否定质量
        negation_quality = self._calculate_negation_quality(
            thesis_elements, first_negation_elements, second_negation_elements
        )
        
        # 评估发展轨迹
        development_trajectory = self._assess_development_trajectory(
            spiral_trajectories, first_negation_elements, second_negation_elements
        )
        
        return {
            'negation_quality': negation_quality,
            'development_trajectory': development_trajectory,
            'synthesis_level': self._determine_synthesis_level(negation_quality, development_trajectory)
        }
    
    def _calculate_negation_quality(self, thesis_elements: Dict,
                                   first_negation_elements: Dict,
                                   second_negation_elements: Dict) -> float:
        """计算否定质量"""
        thesis_score = thesis_elements.get('thesis_score', 0)
        first_negation_score = first_negation_elements.get('negation_score', 0)
        second_negation_score = second_negation_elements.get('second_negation_score', 0)
        
        # 理想的否定之否定应该有三个阶段
        if thesis_score >= 3.0 and first_negation_score >= 3.0 and second_negation_score >= 3.0:
            return 8.0
        elif thesis_score >= 3.0 and first_negation_score >= 3.0:
            return 6.0
        elif thesis_score >= 3.0:
            return 4.0
        else:
            return 2.0
    
    def _assess_development_trajectory(self, spiral_trajectories: Dict,
                                      first_negation_elements: Dict,
                                      second_negation_elements: Dict) -> str:
        """评估发展轨迹"""
        spiral_score = spiral_trajectories.get('spiral_score', 0)
        first_negation_score = first_negation_elements.get('negation_score', 0)
        second_negation_score = second_negation_elements.get('second_negation_score', 0)
        
        if spiral_score >= 5.0 and second_negation_score >= 3.0:
            return "螺旋式上升"
        elif spiral_score >= 3.0:
            return "波浪式前进"
        elif first_negation_score >= 3.0:
            return "线性发展"
        else:
            return "发展轨迹不明显"
    
    def _determine_synthesis_level(self, negation_quality: float,
                                  development_trajectory: str) -> str:
        """确定综合水平"""
        if negation_quality >= 7.0 and "螺旋" in development_trajectory:
            return "优秀"
        elif negation_quality >= 5.0:
            return "良好"
        elif negation_quality >= 3.0:
            return "一般"
        else:
            return "需要改进"
    
    def _analyze_internal_connections(self, unity_analysis: Dict,
                                     quantity_quality_analysis: Dict,
                                     negation_analysis: Dict) -> Dict:
        """分析三大规律的内在联系"""
        
        # 分析对立统一与量变质变的关系
        unity_quantity_relation = self._analyzeUnityQuantityRelation(
            unity_analysis, quantity_quality_analysis
        )
        
        # 分析对立统一与否定之否定的关系
        unity_negation_relation = self._analyzeUnityNegationRelation(
            unity_analysis, negation_analysis
        )
        
        # 分析量变质变与否定之否定的关系
        quantity_negation_relation = self._analyzeQuantityNegationRelation(
            quantity_quality_analysis, negation_analysis
        )
        
        return {
            'unity_quantity_relation': unity_quantity_relation,
            'unity_negation_relation': unity_negation_relation,
            'quantity_negation_relation': quantity_negation_relation,
            'overall_coherence': self._assess_overall_coherence(
                unity_analysis, quantity_quality_analysis, negation_analysis
            )
        }
    
    def _analyzeUnityQuantityRelation(self, unity_analysis: Dict,
                                     quantity_quality_analysis: Dict) -> Dict:
        """分析对立统一与量变质变的关系"""
        unity_quality = unity_analysis.get('dialectical_quality', {}).get('overall_quality', 0)
        quantity_quality = quantity_quality_analysis.get('synthesis_quality', 0)
        
        # 矛盾的发展推动量变质变
        relation_strength = (unity_quality + quantity_quality) / 2
        
        return {
            'relation_strength': relation_strength,
            'relation_description': '矛盾的发展是量变质变的内在动力',
            'relation_quality': self._assess_relation_quality(relation_strength)
        }
    
    def _analyzeUnityNegationRelation(self, unity_analysis: Dict,
                                     negation_analysis: Dict) -> Dict:
        """分析对立统一与否定之否定的关系"""
        unity_quality = unity_analysis.get('dialectical_quality', {}).get('overall_quality', 0)
        negation_quality = negation_analysis.get('synthesis_level', 0)
        
        # 矛盾的解决通过否定之否定实现
        relation_strength = (unity_quality + negation_quality) / 2
        
        return {
            'relation_strength': relation_strength,
            'relation_description': '矛盾的解决通过否定之否定实现发展',
            'relation_quality': self._assess_relation_quality(relation_strength)
        }
    
    def _analyzeQuantityNegationRelation(self, quantity_quality_analysis: Dict,
                                        negation_analysis: Dict) -> Dict:
        """分析量变质变与否定之否定的关系"""
        quantity_quality = quantity_quality_analysis.get('synthesis_quality', 0)
        negation_quality = negation_analysis.get('synthesis_level', 0)
        
        # 量变质变是否定之否定的具体表现
        relation_strength = (quantity_quality + negation_quality) / 2
        
        return {
            'relation_strength': relation_strength,
            'relation_description': '量变质变是否定之否定的具体表现形式',
            'relation_quality': self._assess_relation_quality(relation_strength)
        }
    
    def _assess_relation_quality(self, strength: float) -> str:
        """评估关系质量"""
        if strength >= 7.0:
            return "高度协调"
        elif strength >= 5.0:
            return "较好协调"
        elif strength >= 3.0:
            return "一般协调"
        else:
            return "协调不足"
    
    def _assess_overall_coherence(self, unity_analysis: Dict,
                                quantity_quality_analysis: Dict,
                                negation_analysis: Dict) -> Dict:
        """评估整体协调性"""
        unity_quality = unity_analysis.get('dialectical_quality', {}).get('overall_quality', 0)
        quantity_quality = quantity_quality_analysis.get('synthesis_quality', 0)
        negation_quality = negation_analysis.get('synthesis_level', 0)
        
        # 计算整体协调性
        overall_coherence = (unity_quality + quantity_quality + negation_quality) / 3
        
        return {
            'overall_coherence_score': overall_coherence,
            'coherence_level': self._determine_coherence_level(overall_coherence),
            'coherence_description': self._describe_coherence(overall_coherence)
        }
    
    def _determine_coherence_level(self, score: float) -> str:
        """确定协调性水平"""
        if score >= 8.0:
            return "高度协调"
        elif score >= 6.0:
            return "良好协调"
        elif score >= 4.0:
            return "一般协调"
        else:
            return "协调不足"
    
    def _describe_coherence(self, score: float) -> str:
        """描述协调性"""
        if score >= 8.0:
            return "三大规律高度统一，形成完整的辩证思维体系"
        elif score >= 6.0:
            return "三大规律基本协调，辩证思维较为完整"
        elif score >= 4.0:
            return "三大规律有一定协调，但需要进一步完善"
        else:
            return "三大规律协调不足，辩证思维需要系统性提升"
    
    def _assess_overall_dialectical_level(self, unity_analysis: Dict,
                                        quantity_quality_analysis: Dict,
                                        negation_analysis: Dict) -> Dict:
        """评估整体辩证思维水平"""
        
        # 计算各规律的质量分数
        unity_quality = unity_analysis.get('dialectical_quality', {}).get('overall_quality', 0)
        quantity_quality = quantity_quality_analysis.get('synthesis_quality', 0)
        negation_quality = negation_analysis.get('synthesis_level', 0)
        
        # 计算整体水平
        overall_score = (unity_quality + quantity_quality + negation_quality) / 3
        
        # 确定能力等级
        if overall_score >= 8.5:
            dialectical_level = "辩证思维大师级"
        elif overall_score >= 7.0:
            dialectical_level = "辩证思维专家级"
        elif overall_score >= 5.5:
            dialectical_level = "辩证思维熟练级"
        elif overall_score >= 4.0:
            dialectical_level = "辩证思维基础级"
        else:
            dialectical_level = "辩证思维入门级"
        
        return {
            'overall_score': overall_score,
            'dialectical_level': dialectical_level,
            'strengths': self._identify_dialectical_strengths(unity_analysis, quantity_quality_analysis, negation_analysis),
            'weaknesses': self._identify_dialectical_weaknesses(unity_analysis, quantity_quality_analysis, negation_analysis),
            'improvement_directions': self._suggest_improvement_directions(unity_analysis, quantity_quality_analysis, negation_analysis)
        }
    
    def _identify_dialectical_strengths(self, unity_analysis: Dict,
                                       quantity_quality_analysis: Dict,
                                       negation_analysis: Dict) -> List[str]:
        """识别辩证思维优势"""
        strengths = []
        
        unity_quality = unity_analysis.get('dialectical_quality', {}).get('overall_quality', 0)
        quantity_quality = quantity_quality_analysis.get('synthesis_quality', 0)
        negation_quality = negation_analysis.get('synthesis_level', 0)
        
        if unity_quality >= 7.0:
            strengths.append("对立统一分析能力强")
        if quantity_quality >= 7.0:
            strengths.append("量变质变分析能力强")
        if negation_quality >= 7.0:
            strengths.append("否定之否定分析能力强")
        
        return strengths
    
    def _identify_dialectical_weaknesses(self, unity_analysis: Dict,
                                        quantity_quality_analysis: Dict,
                                        negation_analysis: Dict) -> List[str]:
        """识别辩证思维不足"""
        weaknesses = []
        
        unity_quality = unity_analysis.get('dialectical_quality', {}).get('overall_quality', 0)
        quantity_quality = quantity_quality_analysis.get('synthesis_quality', 0)
        negation_quality = negation_analysis.get('synthesis_level', 0)
        
        if unity_quality < 5.0:
            weaknesses.append("对立统一分析需要加强")
        if quantity_quality < 5.0:
            weaknesses.append("量变质变分析需要加强")
        if negation_quality < 5.0:
            weaknesses.append("否定之否定分析需要加强")
        
        return weaknesses
    
    def _suggest_improvement_directions(self, unity_analysis: Dict,
                                       quantity_quality_analysis: Dict,
                                       negation_analysis: Dict) -> List[str]:
        """建议改进方向"""
        directions = []
        
        unity_quality = unity_analysis.get('dialectical_quality', {}).get('overall_quality', 0)
        quantity_quality = quantity_quality_analysis.get('synthesis_quality', 0)
        negation_quality = negation_analysis.get('synthesis_level', 0)
        
        if unity_quality < 6.0:
            directions.append("深入学习对立统一规律，增强矛盾分析能力")
        if quantity_quality < 6.0:
            directions.append("加强对量变质变规律的理解和应用")
        if negation_quality < 6.0:
            directions.append("提升对否定之否定规律的掌握程度")
        
        # 综合建议
        avg_quality = (unity_quality + quantity_quality + negation_quality) / 3
        if avg_quality < 5.0:
            directions.append("系统性学习马克思主义辩证法基本原理")
        elif avg_quality < 7.0:
            directions.append("加强辩证思维的实际应用训练")
        
        return directions
    
    def _generate_dialectical_recommendations(self, unity_analysis: Dict,
                                            quantity_quality_analysis: Dict,
                                            negation_analysis: Dict) -> List[str]:
        """生成辩证思维建议"""
        recommendations = []
        
        # 基于各规律分析结果生成建议
        unity_quality = unity_analysis.get('dialectical_quality', {}).get('overall_quality', 0)
        quantity_quality = quantity_quality_analysis.get('synthesis_quality', 0)
        negation_quality = negation_analysis.get('synthesis_level', 0)
        
        if unity_quality >= 7.0:
            recommendations.append("对立统一分析能力优秀，继续保持和深化")
        elif unity_quality >= 5.0:
            recommendations.append("对立统一分析能力良好，可进一步提升矛盾转化分析")
        else:
            recommendations.append("重点加强对立统一规律的学习，特别是矛盾的主要方面分析")
        
        if quantity_quality >= 7.0:
            recommendations.append("量变质变分析能力优秀，继续保持")
        elif quantity_quality >= 5.0:
            recommendations.append("量变质变分析能力良好，可加强质变飞跃点的识别")
        else:
            recommendations.append("重点学习量变质变规律，关注量变积累的临界点")
        
        if negation_quality >= 7.0:
            recommendations.append("否定之否定分析能力优秀，继续保持")
        elif negation_quality >= 5.0:
            recommendations.append("否定之否定分析能力良好，可加强螺旋式上升轨迹分析")
        else:
            recommendations.append("重点学习否定之否定规律，理解扬弃的辩证含义")
        
        # 综合建议
        overall_level = self._assess_overall_dialectical_level(unity_analysis, quantity_quality_analysis, negation_analysis)
        overall_score = overall_level.get('overall_score', 0)
        
        if overall_score >= 7.0:
            recommendations.append("辩证思维整体水平较高，建议在复杂问题分析中进一步应用")
        elif overall_score >= 5.0:
            recommendations.append("辩证思维基础良好，建议加强系统性训练")
        else:
            recommendations.append("建议系统学习马克思主义辩证法，打好理论基础")
        
        return recommendations


def main():
    """测试辩证思维分析器"""
    analyzer = DialecticalThinkingAnalyzer()
    
    test_text = """
    在当代社会发展中，生产力与生产关系的矛盾日益突出。一方面，数字技术和人工智能
    带来了生产力的巨大飞跃；另一方面，传统的生产关系在一定程度上制约了这种发展。
    
    这种对立统一的关系推动着社会变革。随着生产力的不断积累，当达到一定临界点时，
    就会发生质的飞跃，推动生产关系的根本性变革。这种变革不是简单的否定，
    而是辩证的否定，既克服了旧生产关系的局限性，又保留了其中的合理因素。
    
    经过这样的否定之否定过程，社会进入了更高的发展阶段，呈现出螺旋式上升
    的发展轨迹。在这个过程中，矛盾的解决不是消灭矛盾，而是推动矛盾向更高
    层次发展，体现了事物发展的辩证规律。
    """
    
    print("=== 辩证思维分析器测试 ===")
    
    # 执行综合辩证分析
    result = analyzer.comprehensive_dialectical_analysis(test_text)
    
    # 显示主要结果
    print("\n=== 对立统一规律分析 ===")
    unity_analysis = result['unity_of_opposites']
    dialectical_quality = unity_analysis.get('dialectical_quality', {})
    print(f"辩证思维质量: {dialectical_quality.get('overall_quality', 0):.2f}")
    print(f"质量等级: {dialectical_quality.get('quality_level', '未知')}")
    
    print("\n=== 量变质变规律分析 ===")
    quantity_analysis = result['quantity_quality_change']
    synthesis = quantity_analysis.get('quantity_quality_synthesis', {})
    print(f"综合质量: {synthesis.get('synthesis_quality', '未知')}")
    print(f"发展阶段: {synthesis.get('development_stage', '未知')}")
    
    print("\n=== 否定之否定规律分析 ===")
    negation_analysis = result['negation_of_negation']
    synthesis = negation_analysis.get('negation_synthesis', {})
    print(f"综合水平: {synthesis.get('synthesis_level', '未知')}")
    print(f"发展轨迹: {synthesis.get('development_trajectory', '未知')}")
    
    print("\n=== 整体辩证思维水平 ===")
    overall_level = result['overall_dialectical_level']
    print(f"整体分数: {overall_level.get('overall_score', 0):.2f}")
    print(f"能力等级: {overall_level.get('dialectical_level', '未知')}")
    
    strengths = overall_level.get('strengths', [])
    if strengths:
        print("优势:")
        for strength in strengths:
            print(f"  - {strength}")
    
    weaknesses = overall_level.get('weaknesses', [])
    if weaknesses:
        print("不足:")
        for weakness in weaknesses:
            print(f"  - {weakness}")
    
    recommendations = overall_level.get('improvement_directions', [])
    if recommendations:
        print("改进建议:")
        for recommendation in recommendations:
            print(f"  - {recommendation}")


if __name__ == "__main__":
    main()
