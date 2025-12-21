#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
历史唯物主义分析器 - 基于马克思主义理论的社会结构分析
通过量化指标和算法模型，实现历史唯物主义的精确分析
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
import re
from collections import Counter
import warnings
import jieba
import jieba.analyse


class HistoricalMaterialismAnalyzer:
    """历史唯物主义分析器"""
    
    def __init__(self):
        self.analysis_results = {}
        self.quality_metrics = {}
        
        # 初始化jieba分词
        jieba.initialize()
        
        # 生产力发展水平指标
        self.productivity_indicators = {
            'tool_level': {
                'primitive': ['石器', '木器', '骨器', '原始工具', '手工工具'],
                'agricultural': ['金属工具', '铁器', '青铜器', '犁', '耕具', '农具'],
                'industrial': ['机器', '蒸汽机', '内燃机', '机床', '工厂设备'],
                'information': ['计算机', '网络', '信息', '数据', '软件'],
                'intelligent': ['人工智能', 'AI', '自动化', '机器人', '智能设备']
            },
            'technology_complexity': {
                'simple': ['简单', '基础', '初级', '基本'],
                'moderate': ['中等', '一般', '普通', '标准'],
                'complex': ['复杂', '高级', '精密', '尖端'],
                'sophisticated': ['先进', '前沿', '领先', '突破']
            },
            'labor_efficiency': {
                'low': ['低效', '缓慢', '落后', '低下'],
                'medium': ['一般', '中等', '普通', '平稳'],
                'high': ['高效', '快速', '先进', '提升'],
                'very_high': ['极高', '飞速', '突破', '跨越']
            }
        }
        
        # 生产关系指标
        self.production_relations_indicators = {
            'ownership': {
                'public': ['公有', '公共', '集体', '共享', '共同'],
                'private': ['私有', '私人', '个体', '个人', '家庭'],
                'state': ['国有', '国家', '政府', '官方', '公有'],
                'mixed': ['混合', '多元', '多种', '复合']
            },
            'labor_relation': {
                'exploitation': ['剥削', '压迫', '奴役', '强制', '不等价'],
                'cooperation': ['合作', '协作', '互助', '联合', '平等'],
                'hierarchy': ['等级', '层级', '上下级', '主从', '支配'],
                'autonomy': ['自主', '独立', '自由', '自愿', '民主']
            },
            'distribution': {
                'equal': ['平均', '平等', '公平', '均衡', '均等'],
                'unequal': ['不平等', '差距', '悬殊', '分化', '不均'],
                'merit': ['按劳', '绩效', '贡献', '能力', '业绩'],
                'need': ['按需', '需求', '保障', '福利', '救助']
            }
        }
        
        # 上层建筑指标
        self.superstructure_indicators = {
            'political_system': {
                'democracy': ['民主', '选举', '投票', '参与', '议会'],
                'autocracy': ['专制', '独裁', '集权', '威权', '统治'],
                'republic': ['共和', '宪政', '法治', '制衡', '分权'],
                'people': ['人民', '群众', '民主', '共和', '社会主义']
            },
            'ideology': {
                'liberalism': ['自由', '个人', '权利', '市场', '竞争'],
                'conservatism': ['传统', '秩序', '权威', '稳定', '保守'],
                'socialism': ['社会主义', '集体', '平等', '公平', '公益'],
                'nationalism': ['民族', '国家', '爱国', '统一', '独立']
            },
            'culture': {
                'traditional': ['传统', '习俗', '历史', '遗产', '经典'],
                'modern': ['现代', '进步', '科学', '理性', '创新'],
                'revolutionary': ['革命', '变革', '进步', '解放', '创新'],
                'global': ['全球', '国际', '多元', '包容', '开放']
            }
        }
    
    def analyze_productivity_level(self, text_data: str, context: Dict = None) -> Dict:
        """分析生产力发展水平"""
        
        # 预处理文本
        processed_text = self._preprocess_text(text_data)
        
        # 获取关键词和语义特征
        keywords = jieba.analyse.extract_tags(processed_text, topK=100, withWeight=True)
        
        # 分析工具水平
        tool_level_score = self._analyze_tool_level(processed_text, keywords)
        
        # 分析技术复杂度
        tech_complexity_score = self._analyze_technology_complexity(processed_text, keywords)
        
        # 分析劳动效率
        labor_efficiency_score = self._analyze_labor_efficiency(processed_text, keywords)
        
        # 综合生产力水平评估
        overall_productivity = self._calculate_overall_productivity(
            tool_level_score, tech_complexity_score, labor_efficiency_score
        )
        
        # 质量评估
        quality_metrics = self._assess_productivity_analysis_quality(
            tool_level_score, tech_complexity_score, labor_efficiency_score
        )
        
        results = {
            'tool_level': tool_level_score,
            'technology_complexity': tech_complexity_score,
            'labor_efficiency': labor_efficiency_score,
            'overall_productivity': overall_productivity,
            'productivity_stage': self._determine_productivity_stage(overall_productivity),
            'quality_metrics': quality_metrics
        }
        
        self.analysis_results['productivity_analysis'] = results
        return results
    
    def analyze_production_relations(self, text_data: str, context: Dict = None) -> Dict:
        """分析生产关系"""
        
        processed_text = self._preprocess_text(text_data)
        keywords = jieba.analyse.extract_tags(processed_text, topK=100, withWeight=True)
        
        # 分析所有制形式
        ownership_score = self._analyze_ownership_form(processed_text, keywords)
        
        # 分析劳动关系
        labor_relation_score = self._analyze_labor_relations(processed_text, keywords)
        
        # 分析分配方式
        distribution_score = self._analyze_distribution_method(processed_text, keywords)
        
        # 综合生产关系评估
        overall_relations = self._calculate_overall_production_relations(
            ownership_score, labor_relation_score, distribution_score
        )
        
        # 阶级结构分析
        class_structure = self._analyze_class_structure(processed_text, keywords)
        
        # 质量评估
        quality_metrics = self._assess_production_relations_quality(
            ownership_score, labor_relation_score, distribution_score
        )
        
        results = {
            'ownership_form': ownership_score,
            'labor_relations': labor_relation_score,
            'distribution_method': distribution_score,
            'overall_production_relations': overall_relations,
            'class_structure': class_structure,
            'quality_metrics': quality_metrics
        }
        
        self.analysis_results['production_relations_analysis'] = results
        return results
    
    def analyze_superstructure(self, text_data: str, context: Dict = None) -> Dict:
        """分析上层建筑"""
        
        processed_text = self._preprocess_text(text_data)
        keywords = jieba.analyse.extract_tags(processed_text, topK=100, withWeight=True)
        
        # 分析政治制度
        political_system_score = self._analyze_political_system(processed_text, keywords)
        
        # 分析意识形态
        ideology_score = self._analyze_ideology(processed_text, keywords)
        
        # 分析文化特征
        culture_score = self._analyze_culture(processed_text, keywords)
        
        # 综合上层建筑评估
        overall_superstructure = self._calculate_overall_superstructure(
            political_system_score, ideology_score, culture_score
        )
        
        # 与经济基础关系分析
        economic_base_relation = self._analyze_economic_base_relation(processed_text, keywords)
        
        # 质量评估
        quality_metrics = self._assess_superstructure_quality(
            political_system_score, ideology_score, culture_score
        )
        
        results = {
            'political_system': political_system_score,
            'ideology': ideology_score,
            'culture': culture_score,
            'overall_superstructure': overall_superstructure,
            'economic_base_relation': economic_base_relation,
            'quality_metrics': quality_metrics
        }
        
        self.analysis_results['superstructure_analysis'] = results
        return results
    
    def analyze_social_change(self, text_data: str, context: Dict = None) -> Dict:
        """分析社会变革"""
        
        processed_text = self._preprocess_text(text_data)
        keywords = jieba.analyse.extract_tags(processed_text, topK=100, withWeight=True)
        
        # 分析基本矛盾
        basic_contradictions = self._analyze_basic_contradictions(processed_text, keywords)
        
        # 分析变革条件
        change_conditions = self._analyze_change_conditions(processed_text, keywords)
        
        # 分析变革动力
        change_drivers = self._analyze_change_drivers(processed_text, keywords)
        
        # 发展趋势预测
        development_trends = self._predict_development_trends(processed_text, keywords)
        
        # 实践路径探索
        practice_paths = self._explore_practice_paths(processed_text, keywords)
        
        # 质量评估
        quality_metrics = self._assess_social_change_quality(
            basic_contradictions, change_conditions, change_drivers
        )
        
        results = {
            'basic_contradictions': basic_contradictions,
            'change_conditions': change_conditions,
            'change_drivers': change_drivers,
            'development_trends': development_trends,
            'practice_paths': practice_paths,
            'quality_metrics': quality_metrics
        }
        
        self.analysis_results['social_change_analysis'] = results
        return results
    
    def _preprocess_text(self, text_data: str) -> str:
        """文本预处理"""
        text = re.sub(r'\s+', ' ', text_data.strip())
        return text
    
    def _analyze_tool_level(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析工具水平"""
        indicators = self.productivity_indicators['tool_level']
        
        level_scores = {}
        for level, words in indicators.items():
            # 基于关键词的评分
            keyword_score = sum(weight for word, weight in keywords if word in words)
            
            # 基于文本频率的评分
            text_score = sum(text_data.count(word) for word in words)
            
            # 综合评分
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            level_scores[level] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        # 确定主导水平
        dominant_level = max(level_scores.keys(), key=lambda x: level_scores[x]['score'])
        
        return {
            'level_scores': level_scores,
            'dominant_level': dominant_level,
            'confidence': level_scores[dominant_level]['score']
        }
    
    def _analyze_technology_complexity(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析技术复杂度"""
        indicators = self.productivity_indicators['technology_complexity']
        
        complexity_scores = {}
        for complexity, words in indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            complexity_scores[complexity] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        dominant_complexity = max(complexity_scores.keys(), key=lambda x: complexity_scores[x]['score'])
        
        return {
            'complexity_scores': complexity_scores,
            'dominant_complexity': dominant_complexity,
            'confidence': complexity_scores[dominant_complexity]['score']
        }
    
    def _analyze_labor_efficiency(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析劳动效率"""
        indicators = self.productivity_indicators['labor_efficiency']
        
        efficiency_scores = {}
        for efficiency, words in indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            efficiency_scores[efficiency] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        dominant_efficiency = max(efficiency_scores.keys(), key=lambda x: efficiency_scores[x]['score'])
        
        return {
            'efficiency_scores': efficiency_scores,
            'dominant_efficiency': dominant_efficiency,
            'confidence': efficiency_scores[dominant_efficiency]['score']
        }
    
    def _calculate_overall_productivity(self, tool_level: Dict, tech_complexity: Dict, labor_efficiency: Dict) -> float:
        """计算综合生产力水平"""
        tool_score = tool_level['confidence']
        tech_score = tech_complexity['confidence']
        labor_score = labor_efficiency['confidence']
        
        # 加权平均
        weights = [0.4, 0.3, 0.3]  # 工具水平权重最高
        overall_score = (tool_score * weights[0] + tech_score * weights[1] + labor_score * weights[2])
        
        return overall_score
    
    def _determine_productivity_stage(self, overall_score: float) -> str:
        """确定生产力发展阶段"""
        if overall_score >= 8.0:
            return "智能生产力"
        elif overall_score >= 6.0:
            return "信息生产力"
        elif overall_score >= 4.0:
            return "工业生产力"
        elif overall_score >= 2.0:
            return "农业生产力"
        else:
            return "原始生产力"
    
    def _analyze_ownership_form(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析所有制形式"""
        indicators = self.production_relations_indicators['ownership']
        
        ownership_scores = {}
        for ownership, words in indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            ownership_scores[ownership] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        dominant_ownership = max(ownership_scores.keys(), key=lambda x: ownership_scores[x]['score'])
        
        return {
            'ownership_scores': ownership_scores,
            'dominant_ownership': dominant_ownership,
            'confidence': ownership_scores[dominant_ownership]['score']
        }
    
    def _analyze_labor_relations(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析劳动关系"""
        indicators = self.production_relations_indicators['labor_relation']
        
        relation_scores = {}
        for relation, words in indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            relation_scores[relation] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        dominant_relation = max(relation_scores.keys(), key=lambda x: relation_scores[x]['score'])
        
        return {
            'relation_scores': relation_scores,
            'dominant_relation': dominant_relation,
            'confidence': relation_scores[dominant_relation]['score']
        }
    
    def _analyze_distribution_method(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析分配方式"""
        indicators = self.production_relations_indicators['distribution']
        
        distribution_scores = {}
        for distribution, words in indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            distribution_scores[distribution] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        dominant_distribution = max(distribution_scores.keys(), key=lambda x: distribution_scores[x]['score'])
        
        return {
            'distribution_scores': distribution_scores,
            'dominant_distribution': dominant_distribution,
            'confidence': distribution_scores[dominant_distribution]['score']
        }
    
    def _calculate_overall_production_relations(self, ownership: Dict, labor_relation: Dict, distribution: Dict) -> float:
        """计算综合生产关系水平"""
        ownership_score = ownership['confidence']
        relation_score = labor_relation['confidence']
        distribution_score = distribution['confidence']
        
        # 加权平均
        weights = [0.4, 0.3, 0.3]  # 所有制权重最高
        overall_score = (ownership_score * weights[0] + relation_score * weights[1] + distribution_score * weights[2])
        
        return overall_score
    
    def _analyze_class_structure(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析阶级结构"""
        class_indicators = {
            'bourgeoisie': ['资产阶级', '资本家', '资产阶级', '剥削阶级', '统治阶级'],
            'proletariat': ['无产阶级', '工人', '劳动者', '被剥削阶级', '劳动人民'],
            'petty_bourgeoisie': ['小资产阶级', '小生产者', '手工业者', '小商人', '农民'],
            'lumpenproletariat': ['流民', '无业者', '游民', '失业者', '贫困阶层']
        }
        
        class_scores = {}
        for class_type, words in class_indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            class_scores[class_type] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        # 识别主要阶级
        major_classes = [cls for cls, data in class_scores.items() if data['score'] > 1.0]
        
        return {
            'class_scores': class_scores,
            'major_classes': major_classes,
            'class_conflict_intensity': self._calculate_class_conflict_intensity(class_scores)
        }
    
    def _calculate_class_conflict_intensity(self, class_scores: Dict) -> float:
        """计算阶级冲突强度"""
        bourgeoisie_score = class_scores.get('bourgeoisie', {}).get('score', 0)
        proletariat_score = class_scores.get('proletariat', {}).get('score', 0)
        
        # 冲突强度基于两个主要阶级的存在程度
        conflict_intensity = min(bourgeoisie_score, proletariat_score) * 2
        
        return conflict_intensity
    
    def _analyze_political_system(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析政治制度"""
        indicators = self.superstructure_indicators['political_system']
        
        system_scores = {}
        for system, words in indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            system_scores[system] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        dominant_system = max(system_scores.keys(), key=lambda x: system_scores[x]['score'])
        
        return {
            'system_scores': system_scores,
            'dominant_system': dominant_system,
            'confidence': system_scores[dominant_system]['score']
        }
    
    def _analyze_ideology(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析意识形态"""
        indicators = self.superstructure_indicators['ideology']
        
        ideology_scores = {}
        for ideology, words in indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            ideology_scores[ideology] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        dominant_ideology = max(ideology_scores.keys(), key=lambda x: ideology_scores[x]['score'])
        
        return {
            'ideology_scores': ideology_scores,
            'dominant_ideology': dominant_ideology,
            'confidence': ideology_scores[dominant_ideology]['score']
        }
    
    def _analyze_culture(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析文化特征"""
        indicators = self.superstructure_indicators['culture']
        
        culture_scores = {}
        for culture, words in indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            culture_scores[culture] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        dominant_culture = max(culture_scores.keys(), key=lambda x: culture_scores[x]['score'])
        
        return {
            'culture_scores': culture_scores,
            'dominant_culture': dominant_culture,
            'confidence': culture_scores[dominant_culture]['score']
        }
    
    def _calculate_overall_superstructure(self, political: Dict, ideology: Dict, culture: Dict) -> float:
        """计算综合上层建筑水平"""
        political_score = political['confidence']
        ideology_score = ideology['confidence']
        culture_score = culture['confidence']
        
        # 加权平均
        weights = [0.4, 0.3, 0.3]  # 政治制度权重最高
        overall_score = (political_score * weights[0] + ideology_score * weights[1] + culture_score * weights[2])
        
        return overall_score
    
    def _analyze_economic_base_relation(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析上层建筑与经济基础关系"""
        relation_indicators = {
            'determined': ['决定', '基础', '根本', '决定性', '基础性'],
            'relative_independence': ['相对独立', '自主性', '独立性', '自身规律'],
            'reaction': ['反作用', '影响', '作用', '促进', '阻碍'],
            'adaptation': ['适应', '协调', '配合', '一致', '统一']
        }
        
        relation_scores = {}
        for relation, words in relation_indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            relation_scores[relation] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        dominant_relation = max(relation_scores.keys(), key=lambda x: relation_scores[x]['score'])
        
        return {
            'relation_scores': relation_scores,
            'dominant_relation': dominant_relation,
            'confidence': relation_scores[dominant_relation]['score']
        }
    
    def _analyze_basic_contradictions(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析基本矛盾"""
        contradiction_indicators = {
            'productivity_relations': ['生产力', '生产关系', '矛盾', '冲突', '不适应'],
            'economic_base_superstructure': ['经济基础', '上层建筑', '矛盾', '冲突', '不协调'],
            'class_contradiction': ['阶级', '矛盾', '斗争', '对立', '冲突'],
            'social_contradiction': ['社会', '矛盾', '问题', '挑战', '困境']
        }
        
        contradiction_scores = {}
        for contradiction, words in contradiction_indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            contradiction_scores[contradiction] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        # 识别主要矛盾
        primary_contradiction = max(contradiction_scores.keys(), key=lambda x: contradiction_scores[x]['score'])
        
        return {
            'contradiction_scores': contradiction_scores,
            'primary_contradiction': primary_contradiction,
            'contradiction_intensity': contradiction_scores[primary_contradiction]['score']
        }
    
    def _analyze_change_conditions(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析变革条件"""
        condition_indicators = {
            'objective_conditions': ['客观', '物质', '条件', '基础', '环境'],
            'subjective_conditions': ['主观', '意识', '思想', '认识', '觉悟'],
            'historical_conditions': ['历史', '时机', '机遇', '阶段', '时期'],
            'international_conditions': ['国际', '全球', '外部', '世界', '国际环境']
        }
        
        condition_scores = {}
        for condition, words in condition_indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            condition_scores[condition] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        # 评估条件成熟度
        total_score = sum(data['score'] for data in condition_scores.values())
        maturity_level = self._assess_condition_maturity(total_score)
        
        return {
            'condition_scores': condition_scores,
            'total_score': total_score,
            'maturity_level': maturity_level
        }
    
    def _analyze_change_drivers(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析变革动力"""
        driver_indicators = {
            'class_drivers': ['阶级', '群众', '人民', '劳动者', '被压迫者'],
            'technological_drivers': ['技术', '科技', '创新', '进步', '发展'],
            'economic_drivers': ['经济', '生产', '发展', '增长', '利益'],
            'social_drivers': ['社会', '民生', '公正', '平等', '解放']
        }
        
        driver_scores = {}
        for driver, words in driver_indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            driver_scores[driver] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        # 识别主要动力
        primary_driver = max(driver_scores.keys(), key=lambda x: driver_scores[x]['score'])
        
        return {
            'driver_scores': driver_scores,
            'primary_driver': primary_driver,
            'driving_force': driver_scores[primary_driver]['score']
        }
    
    def _predict_development_trends(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """预测发展趋势"""
        trend_indicators = {
            'progressive': ['进步', '发展', '前进', '提升', '改善'],
            'revolutionary': ['革命', '变革', '突破', '飞跃', '跨越'],
            'reformist': ['改革', '改良', '调整', '完善', '优化'],
            'conservative': ['保守', '稳定', '维持', '延续', '传统']
        }
        
        trend_scores = {}
        for trend, words in trend_indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            trend_scores[trend] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        # 确定主要趋势
        primary_trend = max(trend_scores.keys(), key=lambda x: trend_scores[x]['score'])
        
        return {
            'trend_scores': trend_scores,
            'primary_trend': primary_trend,
            'trend_confidence': trend_scores[primary_trend]['score']
        }
    
    def _explore_practice_paths(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """探索实践路径"""
        path_indicators = {
            'revolutionary_path': ['革命', '武装', '斗争', '推翻', '夺取'],
            'reform_path': ['改革', '改良', '渐进', '逐步', '和平'],
            'development_path': ['发展', '建设', '创新', '创造', '发展'],
            'cooperation_path': ['合作', '联合', '团结', '协作', '共同']
        }
        
        path_scores = {}
        for path, words in path_indicators.items():
            keyword_score = sum(weight for word, weight in keywords if word in words)
            text_score = sum(text_data.count(word) for word in words)
            composite_score = keyword_score * 0.6 + text_score * 0.4
            
            path_scores[path] = {
                'score': composite_score,
                'level': self._score_to_level(composite_score),
                'evidence': self._extract_evidence(text_data, words)
            }
        
        # 确定可行路径
        feasible_paths = [path for path, data in path_scores.items() if data['score'] > 1.0]
        
        return {
            'path_scores': path_scores,
            'feasible_paths': feasible_paths,
            'primary_path': max(path_scores.keys(), key=lambda x: path_scores[x]['score'])
        }
    
    def _extract_evidence(self, text_data: str, words: List[str]) -> List[str]:
        """提取证据"""
        evidence = []
        sentences = re.split(r'[。！？]', text_data)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 5:
                continue
            
            relevance = sum(1 for word in words if word in sentence)
            if relevance > 0:
                evidence.append(sentence)
        
        return evidence[:3]  # 返回前3个相关句子
    
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
    
    def _assess_condition_maturity(self, total_score: float) -> str:
        """评估条件成熟度"""
        if total_score >= 20.0:
            return "高度成熟"
        elif total_score >= 15.0:
            return "比较成熟"
        elif total_score >= 10.0:
            return "部分成熟"
        elif total_score >= 5.0:
            return "初步成熟"
        else:
            return "尚未成熟"
    
    def _assess_productivity_analysis_quality(self, tool_level: Dict, tech_complexity: Dict, labor_efficiency: Dict) -> Dict:
        """评估生产力分析质量"""
        scores = [tool_level['confidence'], tech_complexity['confidence'], labor_efficiency['confidence']]
        
        avg_score = sum(scores) / len(scores)
        completeness = len([s for s in scores if s > 1.0]) / len(scores)
        balance = 1.0 - (max(scores) - min(scores)) / 10.0
        
        overall_quality = (avg_score * 0.4 + completeness * 0.3 + balance * 0.3) * 10
        
        return {
            'average_score': avg_score,
            'completeness': completeness,
            'balance': balance,
            'overall_quality': overall_quality
        }
    
    def _assess_production_relations_quality(self, ownership: Dict, labor_relation: Dict, distribution: Dict) -> Dict:
        """评估生产关系分析质量"""
        scores = [ownership['confidence'], labor_relation['confidence'], distribution['confidence']]
        
        avg_score = sum(scores) / len(scores)
        completeness = len([s for s in scores if s > 1.0]) / len(scores)
        balance = 1.0 - (max(scores) - min(scores)) / 10.0
        
        overall_quality = (avg_score * 0.4 + completeness * 0.3 + balance * 0.3) * 10
        
        return {
            'average_score': avg_score,
            'completeness': completeness,
            'balance': balance,
            'overall_quality': overall_quality
        }
    
    def _assess_superstructure_quality(self, political: Dict, ideology: Dict, culture: Dict) -> Dict:
        """评估上层建筑分析质量"""
        scores = [political['confidence'], ideology['confidence'], culture['confidence']]
        
        avg_score = sum(scores) / len(scores)
        completeness = len([s for s in scores if s > 1.0]) / len(scores)
        balance = 1.0 - (max(scores) - min(scores)) / 10.0
        
        overall_quality = (avg_score * 0.4 + completeness * 0.3 + balance * 0.3) * 10
        
        return {
            'average_score': avg_score,
            'completeness': completeness,
            'balance': balance,
            'overall_quality': overall_quality
        }
    
    def _assess_social_change_quality(self, contradictions: Dict, conditions: Dict, drivers: Dict) -> Dict:
        """评估社会变革分析质量"""
        scores = [contradictions['contradiction_intensity'], conditions['total_score'], drivers['driving_force']]
        
        avg_score = sum(scores) / len(scores)
        completeness = len([s for s in scores if s > 1.0]) / len(scores)
        balance = 1.0 - (max(scores) - min(scores)) / max(scores) if max(scores) > 0 else 0
        
        overall_quality = (avg_score * 0.4 + completeness * 0.3 + balance * 0.3) * 10
        
        return {
            'average_score': avg_score,
            'completeness': completeness,
            'balance': balance,
            'overall_quality': overall_quality
        }
    
    def generate_comprehensive_report(self) -> str:
        """生成综合分析报告"""
        if not self.analysis_results:
            return "暂无分析结果"
        
        report = []
        report.append("# 数字马克思社会学分析报告\n")
        
        # 各阶段分析结果
        for phase, results in self.analysis_results.items():
            report.append(f"## {phase}")
            
            if 'quality_metrics' in results:
                quality = results['quality_metrics']
                report.append(f"### 质量评估")
                report.append(f"- 整体质量: {quality.get('overall_quality', 0):.2f}/10")
                report.append(f"- 平均分数: {quality.get('average_score', 0):.2f}")
                report.append(f"- 完整性: {quality.get('completeness', 0):.2f}")
                report.append(f"- 平衡性: {quality.get('balance', 0):.2f}")
            
            # 添加具体分析结果
            if phase == 'productivity_analysis':
                report.append(f"### 生产力分析")
                report.append(f"- 生产力阶段: {results.get('productivity_stage', '未知')}")
                report.append(f"- 综合水平: {results.get('overall_productivity', 0):.2f}")
                
            elif phase == 'production_relations_analysis':
                report.append(f"### 生产关系分析")
                report.append(f"- 综合水平: {results.get('overall_production_relations', 0):.2f}")
                
            elif phase == 'superstructure_analysis':
                report.append(f"### 上层建筑分析")
                report.append(f"- 综合水平: {results.get('overall_superstructure', 0):.2f}")
                
            elif phase == 'social_change_analysis':
                report.append(f"### 社会变革分析")
                contradictions = results.get('basic_contradictions', {})
                report.append(f"- 主要矛盾: {contradictions.get('primary_contradiction', '未知')}")
                report.append(f"- 矛盾强度: {contradictions.get('contradiction_intensity', 0):.2f}")
            
            report.append("")
        
        # 整体评估
        overall_scores = []
        for phase, results in self.analysis_results.items():
            if 'quality_metrics' in results:
                overall_scores.append(results['quality_metrics']['overall_quality'])
        
        if overall_scores:
            avg_overall = sum(overall_scores) / len(overall_scores)
            report.append(f"## 整体评估")
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
    """测试历史唯物主义分析器"""
    analyzer = HistoricalMaterialismAnalyzer()
    
    test_text = """
    在当代信息社会中，人工智能和大数据技术快速发展，推动生产力进入智能阶段。
    自动化设备和智能系统的广泛应用，极大提高了劳动生产率。
    
    生产资料所有制呈现多元化趋势，既有国有经济的主导地位，也有民营经济的活跃发展。
    劳动关系更加复杂，既有传统的雇佣关系，也有新兴的平台经济和零工经济。
    收入分配制度不断完善，按劳分配为主体，多种分配方式并存。
    
    政治制度坚持社会主义民主政治，发展全过程人民民主。
    意识形态领域坚持马克思主义指导地位，发展社会主义先进文化。
    传统文化与现代文明交相辉映，形成开放包容的文化格局。
    
    社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾。
    变革条件日趋成熟，但仍需要深化改革开放，推动高质量发展。
    """
    
    print("=== 历史唯物主义分析器测试 ===")
    
    # 执行分析
    productivity_results = analyzer.analyze_productivity_level(test_text)
    print(f"生产力阶段: {productivity_results['productivity_stage']}")
    print(f"生产力质量: {productivity_results['quality_metrics']['overall_quality']:.2f}")
    
    relations_results = analyzer.analyze_production_relations(test_text)
    print(f"生产关系质量: {relations_results['quality_metrics']['overall_quality']:.2f}")
    
    superstructure_results = analyzer.analyze_superstructure(test_text)
    print(f"上层建筑质量: {superstructure_results['quality_metrics']['overall_quality']:.2f}")
    
    change_results = analyzer.analyze_social_change(test_text)
    print(f"社会变革质量: {change_results['quality_metrics']['overall_quality']:.2f}")
    
    # 生成报告
    print(f"\n{analyzer.generate_comprehensive_report()}")


if __name__ == "__main__":
    main()
