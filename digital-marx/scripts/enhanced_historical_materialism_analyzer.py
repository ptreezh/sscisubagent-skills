#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
增强版历史唯物主义分析器 - 基于马克思主义专家指导的深度优化
包含生产力-生产关系矛盾运动、经济基础-上层建筑辩证关系、社会形态发展规律的专业化分析
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
import math

# 导入辩证思维分析器
from dialectical_thinking_analyzer import DialecticalThinkingAnalyzer


class SocialFormationType(Enum):
    """社会形态类型"""
    PRIMITIVE_COMMUNISM = "原始共产主义"
    SLAVE_SOCIETY = "奴隶社会"
    FEUDAL_SOCIETY = "封建社会"
    CAPITALIST_SOCIETY = "资本主义社会"
    SOCIALIST_SOCIETY = "社会主义社会"
    COMMUNIST_SOCIETY = "共产主义社会"


class DevelopmentStage(Enum):
    """发展阶段"""
    EMERGENCE = "形成阶段"
    DEVELOPMENT = "发展阶段"
    MATURITY = "成熟阶段"
    DECLINE = "衰落阶段"
    TRANSFORMATION = "转型阶段"


@dataclass
class ProductiveForces:
    """生产力结构"""
    level: str
    technology_level: float
    labor_productivity: float
    production_tools: List[str]
    scientific_knowledge: float
    development_potential: float


@dataclass
class RelationsOfProduction:
    """生产关系结构"""
    ownership_form: str
    labor_relations: str
    distribution_method: str
    class_structure: Dict[str, float]
    adaptation_level: float


@dataclass
class EconomicBase:
    """经济基础结构"""
    productive_forces: ProductiveForces
    relations_of_production: RelationsOfProduction
    base_superstructure_relation: str
    economic_dynamics: str


@dataclass
class Superstructure:
    """上层建筑结构"""
    political_system: str
    legal_system: str
    ideology: str
    culture: str
    relative_independence: float
    counter_effect: float


@dataclass
class SocialContradiction:
    """社会矛盾结构"""
    primary_contradiction: str
    secondary_contradictions: List[str]
    contradiction_intensity: float
    development_stage: str
    resolution_tendency: str


class EnhancedHistoricalMaterialismAnalyzer:
    """增强版历史唯物主义分析器"""
    
    def __init__(self):
        # 初始化辩证思维分析器
        self.dialectical_analyzer = DialecticalThinkingAnalyzer()
        
        # 初始化jieba分词
        jieba.initialize()
        
        # 生产力发展水平词汇库（增强版）
        self.productive_forces_vocabulary = {
            'primitive_indicators': [
                '石器', '木器', '骨器', '原始工具', '狩猎', '采集', '原始',
                '部落', '氏族', '原始公社', '自然经济', '自给自足'
            ],
            'agricultural_indicators': [
                '金属工具', '铁器', '青铜器', '犁', '耕具', '农业', '畜牧业',
                '手工业', '土地', '农作物', '灌溉', '封建', '庄园', '自给自足'
            ],
            'industrial_indicators': [
                '机器', '蒸汽机', '内燃机', '电力', '工厂', '工业化', '大规模生产',
                '资本主义', '商品经济', '市场经济', '城市化', '无产阶级', '资产阶级'
            ],
            'information_indicators': [
                '计算机', '互联网', '信息技术', '数字经济', '知识经济', '网络',
                '自动化', '智能化', '全球化', '后工业', '信息社会'
            ],
            'intelligent_indicators': [
                '人工智能', 'AI', '机器人', '大数据', '云计算', '物联网',
                '智能制造', '智能社会', '数字孪生', '元宇宙'
            ]
        }
        
        # 生产关系词汇库（增强版）
        self.relations_of_production_vocabulary = {
            'ownership_indicators': {
                'public': ['公有制', '国有', '集体', '公共', '共享', '共同所有'],
                'private': ['私有制', '私人', '个体', '私营', '个人所有', '私有'],
                'mixed': ['混合所有制', '多元', '多种所有制', '股份制', '混合经济']
            },
            'labor_relations_indicators': {
                'exploitation': ['剥削', '压迫', '奴役', '强制', '不等价交换', '剩余价值'],
                'cooperation': ['合作', '协作', '互助', '联合', '平等', '互助合作'],
                'hierarchy': ['等级', '层级', '上下级', '主从', '支配', '等级制'],
                'autonomy': ['自主', '独立', '自由', '自愿', '民主', '自主管理']
            },
            'distribution_indicators': {
                'equal': ['平均', '平等', '公平', '均衡', '均等', '按需分配'],
                'unequal': ['不平等', '差距', '悬殊', '分化', '不均', '贫富差距'],
                'merit': ['按劳', '绩效', '贡献', '能力', '业绩', '按劳分配'],
                'need': ['按需', '需求', '保障', '福利', '救助', '按需分配']
            }
        }
        
        # 上层建筑词汇库（增强版）
        self.superstructure_vocabulary = {
            'political_indicators': {
                'democracy': ['民主', '选举', '投票', '参与', '议会', '民主政治'],
                'autocracy': ['专制', '独裁', '集权', '威权', '统治', '专制政治'],
                'republic': ['共和', '宪政', '法治', '制衡', '分权', '共和制'],
                'people': ['人民', '群众', '民主', '共和', '社会主义', '人民民主']
            },
            'legal_indicators': [
                '法律', '法规', '法治', '司法', '立法', '执法', '法律体系',
                '宪法', '民法', '刑法', '经济法', '依法治国'
            ],
            'ideology_indicators': {
                'liberalism': ['自由', '个人', '权利', '市场', '竞争', '自由主义'],
                'conservatism': ['传统', '秩序', '权威', '稳定', '保守', '保守主义'],
                'socialism': ['社会主义', '集体', '平等', '公平', '公益', '马克思主义'],
                'nationalism': ['民族', '国家', '爱国', '统一', '独立', '民族主义']
            },
            'culture_indicators': [
                '文化', '文明', '传统', '现代', '先进', '精神文明',
                '价值观', '道德', '伦理', '信仰', '文化自信'
            ]
        }
        
        # 社会形态发展规律词汇库
        self.social_development_vocabulary = {
            'transformation_indicators': [
                '变革', '革命', '转型', '更替', '过渡', '演变', '发展',
                '社会变革', '历史变革', '制度变迁'
            ],
            'necessity_indicators': [
                '必然', '客观规律', '历史必然', '客观必然', '不可避免',
                '历史趋势', '发展规律', '客观必然性'
            ],
            'diversity_indicators': [
                '多样性', '多道路', '特色', '具体', '特殊', '个别',
                '多样性统一', '普遍性与特殊性'
            ],
            'people_role_indicators': [
                '人民', '群众', '人民群众', '历史创造者', '主体',
                '人民主体', '群众路线', '人民历史作用'
            ]
        }
        
        # 分析结果存储
        self.analysis_results = {}
    
    def analyze_productive_forces_relations_contradiction(self, text_data: str) -> Dict:
        """分析生产力-生产关系矛盾运动"""
        
        processed_text = self._preprocess_text(text_data)
        keywords = jieba.analyse.extract_tags(processed_text, topK=150, withWeight=True)
        
        # 深度分析生产力发展水平
        productive_forces = self._deep_analyze_productive_forces(processed_text, keywords)
        
        # 深度分析生产关系结构
        relations_of_production = self._deep_analyze_relations_of_production(processed_text, keywords)
        
        # 分析矛盾运动状态
        contradiction_movement = self._analyze_contradiction_movement(
            productive_forces, relations_of_production
        )
        
        # 评估适应性水平
        adaptation_level = self._assess_adaptation_level(
            productive_forces, relations_of_production
        )
        
        # 预测发展趋势
        development_tendency = self._predict_development_tendency(
            productive_forces, relations_of_production, contradiction_movement
        )
        
        # 辩证分析
        dialectical_analysis = self.dialectical_analyzer.analyze_unity_of_opposites(text_data)
        
        # 综合分析结果
        analysis_result = {
            'productive_forces': productive_forces,
            'relations_of_production': relations_of_production,
            'contradiction_movement': contradiction_movement,
            'adaptation_level': adaptation_level,
            'development_tendency': development_tendency,
            'dialectical_analysis': dialectical_analysis,
            'contradiction_quality': self._assess_contradiction_quality(
                productive_forces, relations_of_production, adaptation_level
            )
        }
        
        self.analysis_results['productive_forces_relations'] = analysis_result
        return analysis_result
    
    def analyze_economic_base_superstructure_relation(self, text_data: str) -> Dict:
        """分析经济基础-上层建筑辩证关系"""
        
        processed_text = self._preprocess_text(text_data)
        keywords = jieba.analyse.extract_tags(processed_text, topK=150, withWeight=True)
        
        # 构建经济基础结构
        economic_base = self._construct_economic_base(processed_text, keywords)
        
        # 构建上层建筑结构
        superstructure = self._construct_superstructure(processed_text, keywords)
        
        # 分析决定作用
        determining_role = self._analyze_determining_role(economic_base, superstructure)
        
        # 分析相对独立性
        relative_independence = self._analyze_relative_independence(
            economic_base, superstructure, processed_text
        )
        
        # 分析反作用
        counter_effect = self._analyze_counter_effect(
            economic_base, superstructure, processed_text
        )
        
        # 评估辩证统一关系
        dialectical_unity = self._assess_dialectical_unity(
            determining_role, relative_independence, counter_effect
        )
        
        # 辩证分析
        dialectical_analysis = self.dialectical_analyzer.analyze_unity_of_opposites(text_data)
        
        # 综合分析结果
        analysis_result = {
            'economic_base': economic_base,
            'superstructure': superstructure,
            'determining_role': determining_role,
            'relative_independence': relative_independence,
            'counter_effect': counter_effect,
            'dialectical_unity': dialectical_unity,
            'dialectical_analysis': dialectical_analysis,
            'base_superstructure_quality': self._assess_base_superstructure_quality(
                economic_base, superstructure, dialectical_unity
            )
        }
        
        self.analysis_results['economic_base_superstructure'] = analysis_result
        return analysis_result
    
    def analyze_social_formation_development(self, text_data: str) -> Dict:
        """分析社会形态发展规律"""
        
        processed_text = self._preprocess_text(text_data)
        keywords = jieba.analyse.extract_tags(processed_text, topK=150, withWeight=True)
        
        # 识别当前社会形态
        current_formation = self._identify_social_formation(processed_text, keywords)
        
        # 分析发展阶段
        development_stage = self._analyze_development_stage(processed_text, keywords)
        
        # 识别主要矛盾
        primary_contradiction = self._identify_primary_contradiction(processed_text, keywords)
        
        # 分析历史必然性
        historical_necessity = self._analyze_historical_necessity(processed_text, keywords)
        
        # 分析发展道路多样性
        development_diversity = self._analyze_development_diversity(processed_text, keywords)
        
        # 分析人民群众历史作用
        people_role = self._analyze_people_historical_role(processed_text, keywords)
        
        # 量变质变分析
        quantity_quality_analysis = self.dialectical_analyzer.analyze_quantity_quality_change(text_data)
        
        # 否定之否定分析
        negation_analysis = self.dialectical_analyzer.analyze_negation_of_negation(text_data)
        
        # 综合分析结果
        analysis_result = {
            'current_formation': current_formation,
            'development_stage': development_stage,
            'primary_contradiction': primary_contradiction,
            'historical_necessity': historical_necessity,
            'development_diversity': development_diversity,
            'people_role': people_role,
            'quantity_quality_analysis': quantity_quality_analysis,
            'negation_analysis': negation_analysis,
            'formation_quality': self._assess_formation_quality(
                current_formation, development_stage, historical_necessity
            )
        }
        
        self.analysis_results['social_formation_development'] = analysis_result
        return analysis_result
    
    def comprehensive_historical_materialism_analysis(self, text_data: str) -> Dict:
        """综合历史唯物主义分析"""
        
        # 执行三大核心分析
        contradiction_analysis = self.analyze_productive_forces_relations_contradiction(text_data)
        base_superstructure_analysis = self.analyze_economic_base_superstructure_relation(text_data)
        formation_analysis = self.analyze_social_formation_development(text_data)
        
        # 综合辩证分析
        comprehensive_dialectical = self.dialectical_analyzer.comprehensive_dialectical_analysis(text_data)
        
        # 分析内在联系
        internal_connections = self._analyze_historical_materialism_connections(
            contradiction_analysis, base_superstructure_analysis, formation_analysis
        )
        
        # 评估整体理论水平
        overall_theoretical_level = self._assess_overall_theoretical_level(
            contradiction_analysis, base_superstructure_analysis, formation_analysis
        )
        
        # 生成专业建议
        professional_recommendations = self._generate_professional_recommendations(
            contradiction_analysis, base_superstructure_analysis, formation_analysis
        )
        
        # 综合结果
        comprehensive_result = {
            'contradiction_analysis': contradiction_analysis,
            'base_superstructure_analysis': base_superstructure_analysis,
            'formation_analysis': formation_analysis,
            'comprehensive_dialectical': comprehensive_dialectical,
            'internal_connections': internal_connections,
            'overall_theoretical_level': overall_theoretical_level,
            'professional_recommendations': professional_recommendations,
            'analysis_timestamp': pd.Timestamp.now().isoformat()
        }
        
        return comprehensive_result
    
    def _preprocess_text(self, text_data: str) -> str:
        """文本预处理"""
        text = re.sub(r'\s+', ' ', text_data.strip())
        return text
    
    def _deep_analyze_productive_forces(self, text_data: str, keywords: List[Tuple]) -> ProductiveForces:
        """深度分析生产力发展水平"""
        
        # 计算各阶段指标分数
        stage_scores = {}
        for stage, indicators in self.productive_forces_vocabulary.items():
            score = sum(weight for word, weight in keywords if word in indicators)
            stage_scores[stage] = score
        
        # 确定生产力水平
        max_stage = max(stage_scores.items(), key=lambda x: x[1])[0]
        level_mapping = {
            'primitive_indicators': '原始生产力',
            'agricultural_indicators': '农业生产力',
            'industrial_indicators': '工业生产力',
            'information_indicators': '信息生产力',
            'intelligent_indicators': '智能生产力'
        }
        level = level_mapping.get(max_stage, '未知生产力')
        
        # 计算技术水平
        technology_indicators = ['技术', '科技', '科学', '创新', '发明', '进步']
        technology_level = sum(weight for word, weight in keywords 
                              if word in technology_indicators)
        technology_level = min(technology_level, 10.0)
        
        # 计算劳动生产率
        productivity_indicators = ['效率', '生产率', '产出', '效益', '产能']
        labor_productivity = sum(weight for word, weight in keywords 
                                 if word in productivity_indicators)
        labor_productivity = min(labor_productivity, 10.0)
        
        # 识别生产工具
        tools = []
        tool_indicators = ['工具', '设备', '机器', '技术', '手段', '方法']
        for word, weight in keywords:
            if any(indicator in word for indicator in tool_indicators) and weight > 1.0:
                tools.append(word)
        
        # 计算科学知识水平
        knowledge_indicators = ['知识', '科学', '理论', '学问', '教育', '研究']
        scientific_knowledge = sum(weight for word, weight in keywords 
                                  if word in knowledge_indicators)
        scientific_knowledge = min(scientific_knowledge, 10.0)
        
        # 评估发展潜力
        potential_indicators = ['潜力', '前景', '发展', '未来', '空间', '可能']
        development_potential = sum(weight for word, weight in keywords 
                                   if word in potential_indicators)
        development_potential = min(development_potential, 10.0)
        
        return ProductiveForces(
            level=level,
            technology_level=technology_level,
            labor_productivity=labor_productivity,
            production_tools=tools[:5],  # 取前5个
            scientific_knowledge=scientific_knowledge,
            development_potential=development_potential
        )
    
    def _deep_analyze_relations_of_production(self, text_data: str, keywords: List[Tuple]) -> RelationsOfProduction:
        """深度分析生产关系结构"""
        
        # 分析所有制形式
        ownership_scores = {}
        for ownership_type, indicators in self.relations_of_production_vocabulary['ownership_indicators'].items():
            score = sum(weight for word, weight in keywords if word in indicators)
            ownership_scores[ownership_type] = score
        
        ownership_form = max(ownership_scores.items(), key=lambda x: x[1])[0]
        
        # 分析劳动关系
        labor_relations_scores = {}
        for relation_type, indicators in self.relations_of_production_vocabulary['labor_relations_indicators'].items():
            score = sum(weight for word, weight in keywords if word in indicators)
            labor_relations_scores[relation_type] = score
        
        labor_relations = max(labor_relations_scores.items(), key=lambda x: x[1])[0]
        
        # 分析分配方式
        distribution_scores = {}
        for distribution_type, indicators in self.relations_of_production_vocabulary['distribution_indicators'].items():
            score = sum(weight for word, weight in keywords if word in indicators)
            distribution_scores[distribution_type] = score
        
        distribution_method = max(distribution_scores.items(), key=lambda x: x[1])[0]
        
        # 分析阶级结构
        class_indicators = {
            '资产阶级': ['资产阶级', '资本家', '剥削阶级', '统治阶级', '富人'],
            '无产阶级': ['无产阶级', '工人', '劳动者', '被剥削阶级', '穷人'],
            '中产阶级': ['中产阶级', '中间阶层', '白领', '小资产阶级'],
            '农民阶级': ['农民', '农民阶级', '小农', '农业劳动者']
        }
        
        class_structure = {}
        total_class_score = 0
        for class_name, indicators in class_indicators.items():
            score = sum(weight for word, weight in keywords if word in indicators)
            class_structure[class_name] = score
            total_class_score += score
        
        # 归一化阶级结构分数
        if total_class_score > 0:
            for class_name in class_structure:
                class_structure[class_name] = class_structure[class_name] / total_class_score * 10
        
        # 评估适应性水平
        adaptation_indicators = ['适应', '协调', '匹配', '适合', '一致', '和谐']
        adaptation_level = sum(weight for word, weight in keywords if word in adaptation_indicators)
        adaptation_level = min(adaptation_level, 10.0)
        
        return RelationsOfProduction(
            ownership_form=ownership_form,
            labor_relations=labor_relations,
            distribution_method=distribution_method,
            class_structure=class_structure,
            adaptation_level=adaptation_level
        )
    
    def _analyze_contradiction_movement(self, productive_forces: ProductiveForces,
                                       relations_of_production: RelationsOfProduction) -> Dict:
        """分析矛盾运动状态"""
        
        # 计算生产力发展水平分数
        forces_score = (productive_forces.technology_level + 
                       productive_forces.labor_productivity + 
                       productive_forces.scientific_knowledge) / 3
        
        # 计算生产关系适应性分数
        relations_score = relations_of_production.adaptation_level
        
        # 判断矛盾状态
        if forces_score >= 7.0 and relations_score >= 7.0:
            contradiction_state = "基本适应"
        elif forces_score >= 7.0 and relations_score < 5.0:
            contradiction_state = "生产力超前，生产关系滞后"
        elif forces_score < 5.0 and relations_score >= 7.0:
            contradiction_state = "生产关系超前，生产力滞后"
        else:
            contradiction_state = "低水平平衡"
        
        # 计算矛盾强度
        contradiction_intensity = abs(forces_score - relations_score)
        
        # 判断运动趋势
        if forces_score > relations_score:
            movement_tendency = "要求变革生产关系"
        elif forces_score < relations_score:
            movement_tendency = "要求发展生产力"
        else:
            movement_tendency = "相对稳定发展"
        
        return {
            'contradiction_state': contradiction_state,
            'contradiction_intensity': contradiction_intensity,
            'movement_tendency': movement_tendency,
            'forces_score': forces_score,
            'relations_score': relations_score
        }
    
    def _assess_adaptation_level(self, productive_forces: ProductiveForces,
                                relations_of_production: RelationsOfProduction) -> Dict:
        """评估适应性水平"""
        
        # 计算适应性分数
        forces_score = (productive_forces.technology_level + 
                       productive_forces.labor_productivity + 
                       productive_forces.scientific_knowledge) / 3
        
        relations_score = relations_of_production.adaptation_level
        
        # 适应性水平
        adaptation_gap = abs(forces_score - relations_score)
        
        if adaptation_gap <= 1.0:
            adaptation_level = "高度适应"
        elif adaptation_gap <= 3.0:
            adaptation_level = "基本适应"
        elif adaptation_gap <= 5.0:
            adaptation_level = "部分不适应"
        else:
            adaptation_level = "严重不适应"
        
        # 适应性质量
        adaptation_quality = max(0, 10 - adaptation_gap)
        
        return {
            'adaptation_level': adaptation_level,
            'adaptation_quality': adaptation_quality,
            'adaptation_gap': adaptation_gap,
            'forces_score': forces_score,
            'relations_score': relations_score
        }
    
    def _predict_development_tendency(self, productive_forces: ProductiveForces,
                                     relations_of_production: RelationsOfProduction,
                                     contradiction_movement: Dict) -> Dict:
        """预测发展趋势"""
        
        forces_score = (productive_forces.technology_level + 
                       productive_forces.labor_productivity + 
                       productive_forces.scientific_knowledge) / 3
        
        relations_score = relations_of_production.adaptation_level
        
        # 发展方向预测
        if forces_score > relations_score + 2.0:
            development_direction = "生产关系变革"
            urgency_level = "紧迫"
        elif forces_score > relations_score:
            development_direction = "生产关系调整"
            urgency_level = "较紧迫"
        elif relations_score > forces_score + 2.0:
            development_direction = "生产力发展"
            urgency_level = "紧迫"
        elif relations_score > forces_score:
            development_direction = "生产力提升"
            urgency_level = "较紧迫"
        else:
            development_direction = "协调发展"
            urgency_level = "一般"
        
        # 变革方式预测
        if contradiction_movement['contradiction_intensity'] >= 6.0:
            transformation_method = "革命性变革"
        elif contradiction_movement['contradiction_intensity'] >= 3.0:
            transformation_method = "改革性调整"
        else:
            transformation_method = "渐进性改进"
        
        return {
            'development_direction': development_direction,
            'urgency_level': urgency_level,
            'transformation_method': transformation_method,
            'development_potential': productive_forces.development_potential
        }
    
    def _assess_contradiction_quality(self, productive_forces: ProductiveForces,
                                     relations_of_production: RelationsOfProduction,
                                     adaptation_level: Dict) -> Dict:
        """评估矛盾分析质量"""
        
        # 矛盾识别质量
        contradiction_quality = adaptation_level.get('adaptation_quality', 0)
        
        # 发展潜力评估
        potential_quality = productive_forces.development_potential
        
        # 综合质量分数
        overall_quality = (contradiction_quality + potential_quality) / 2
        
        return {
            'contradiction_quality': contradiction_quality,
            'potential_quality': potential_quality,
            'overall_quality': overall_quality,
            'quality_level': self._determine_quality_level(overall_quality)
        }
    
    def _construct_economic_base(self, text_data: str, keywords: List[Tuple]) -> EconomicBase:
        """构建经济基础结构"""
        
        # 分析生产力（复用之前的方法）
        productive_forces = self._deep_analyze_productive_forces(text_data, keywords)
        
        # 分析生产关系（复用之前的方法）
        relations_of_production = self._deep_analyze_relations_of_production(text_data, keywords)
        
        # 分析经济基础与上层建筑关系
        base_superstructure_indicators = {
            'determining': ['决定', '基础', '根本', '决定性', '基础性'],
            'relatively_independent': ['相对独立', '自主', '独立性', '自身规律'],
            'counter_effect': ['反作用', '影响', '作用', '促进', '阻碍']
        }
        
        relation_scores = {}
        for relation_type, indicators in base_superstructure_indicators.items():
            score = sum(weight for word, weight in keywords if word in indicators)
            relation_scores[relation_type] = score
        
        base_superstructure_relation = max(relation_scores.items(), key=lambda x: x[1])[0]
        
        # 分析经济动态
        economic_dynamics = self._analyze_economic_dynamics(text_data, keywords)
        
        return EconomicBase(
            productive_forces=productive_forces,
            relations_of_production=relations_of_production,
            base_superstructure_relation=base_superstructure_relation,
            economic_dynamics=economic_dynamics
        )
    
    def _construct_superstructure(self, text_data: str, keywords: List[Tuple]) -> Superstructure:
        """构建上层建筑结构"""
        
        # 分析政治制度
        political_scores = {}
        for system_type, indicators in self.superstructure_vocabulary['political_indicators'].items():
            score = sum(weight for word, weight in keywords if word in indicators)
            political_scores[system_type] = score
        
        political_system = max(political_scores.items(), key=lambda x: x[1])[0]
        
        # 分析法律体系
        legal_score = sum(weight for word, weight in keywords 
                         if word in self.superstructure_vocabulary['legal_indicators'])
        legal_system = f"法律体系水平: {legal_score:.1f}/10"
        
        # 分析意识形态
        ideology_scores = {}
        for ideology_type, indicators in self.superstructure_vocabulary['ideology_indicators'].items():
            score = sum(weight for word, weight in keywords if word in indicators)
            ideology_scores[ideology_type] = score
        
        ideology = max(ideology_scores.items(), key=lambda x: x[1])[0]
        
        # 分析文化
        culture_score = sum(weight for word, weight in keywords 
                          if word in self.superstructure_vocabulary['culture_indicators'])
        culture = f"文化发展水平: {culture_score:.1f}/10"
        
        # 计算相对独立性
        independence_indicators = ['相对独立', '自主', '独立性', '自身规律', '独立发展']
        relative_independence = sum(weight for word, weight in keywords 
                                   if word in independence_indicators)
        relative_independence = min(relative_independence, 10.0)
        
        # 计算反作用力
        counter_effect_indicators = ['反作用', '影响', '作用', '促进', '阻碍', '制约']
        counter_effect = sum(weight for word, weight in keywords 
                           if word in counter_effect_indicators)
        counter_effect = min(counter_effect, 10.0)
        
        return Superstructure(
            political_system=political_system,
            legal_system=legal_system,
            ideology=ideology,
            culture=culture,
            relative_independence=relative_independence,
            counter_effect=counter_effect
        )
    
    def _analyze_economic_dynamics(self, text_data: str, keywords: List[Tuple]) -> str:
        """分析经济动态"""
        
        dynamics_indicators = {
            'growth': ['增长', '发展', '扩张', '上升', '进步'],
            'stagnation': ['停滞', '缓慢', '低迷', '萧条', '衰退'],
            'transformation': ['转型', '变革', '升级', '调整', '改革'],
            'stability': ['稳定', '平稳', '持续', '均衡', '协调']
        }
        
        dynamics_scores = {}
        for dynamic_type, indicators in dynamics_indicators.items():
            score = sum(weight for word, weight in keywords if word in indicators)
            dynamics_scores[dynamic_type] = score
        
        primary_dynamic = max(dynamics_scores.items(), key=lambda x: x[1])[0]
        
        dynamic_mapping = {
            'growth': '经济增长态势',
            'stagnation': '经济停滞态势',
            'transformation': '经济转型态势',
            'stability': '经济稳定态势'
        }
        
        return dynamic_mapping.get(primary_dynamic, '经济动态不明')
    
    def _analyze_determining_role(self, economic_base: EconomicBase,
                                 superstructure: Superstructure) -> Dict:
        """分析决定作用"""
        
        # 经济基础的决定作用强度
        forces_score = (economic_base.productive_forces.technology_level + 
                       economic_base.productive_forces.labor_productivity) / 2
        
        # 基础强度评估
        if forces_score >= 8.0:
            base_strength = "强经济基础"
        elif forces_score >= 5.0:
            base_strength = "中等经济基础"
        else:
            base_strength = "弱经济基础"
        
        # 决定作用程度
        determining_degree = min(forces_score / 10 * 8, 8.0)  # 最高8分
        
        return {
            'base_strength': base_strength,
            'determining_degree': determining_degree,
            'forces_score': forces_score
        }
    
    def _analyze_relative_independence(self, economic_base: EconomicBase,
                                     superstructure: Superstructure,
                                     text_data: str) -> Dict:
        """分析相对独立性"""
        
        independence_score = superstructure.relative_independence
        
        # 独立性水平
        if independence_score >= 7.0:
            independence_level = "高度独立"
        elif independence_score >= 5.0:
            independence_level = "中等独立"
        elif independence_score >= 3.0:
            independence_level = "初步独立"
        else:
            independence_level = "独立性不足"
        
        # 独立性特征
        independence_features = []
        if independence_score >= 5.0:
            independence_features.append("具有自身发展规律")
        if independence_score >= 7.0:
            independence_features.append("对经济基础具有能动反作用")
        
        return {
            'independence_level': independence_level,
            'independence_score': independence_score,
            'independence_features': independence_features
        }
    
    def _analyze_counter_effect(self, economic_base: EconomicBase,
                               superstructure: Superstructure,
                               text_data: str) -> Dict:
        """分析反作用"""
        
        counter_effect_score = superstructure.counter_effect
        
        # 反作用强度
        if counter_effect_score >= 7.0:
            effect_intensity = "强反作用"
        elif counter_effect_score >= 5.0:
            effect_intensity = "中等反作用"
        elif counter_effect_score >= 3.0:
            effect_intensity = "弱反作用"
        else:
            effect_intensity = "反作用不明显"
        
        # 反作用方向
        positive_indicators = ['促进', '推动', '助力', '支持', '积极']
        negative_indicators = ['阻碍', '制约', '限制', '束缚', '消极']
        
        keywords = jieba.analyse.extract_tags(text_data, topK=100, withWeight=True)
        
        positive_score = sum(weight for word, weight in keywords if word in positive_indicators)
        negative_score = sum(weight for word, weight in keywords if word in negative_indicators)
        
        if positive_score > negative_score:
            effect_direction = "积极促进作用"
        elif negative_score > positive_score:
            effect_direction = "消极阻碍作用"
        else:
            effect_direction = "中性影响作用"
        
        return {
            'effect_intensity': effect_intensity,
            'effect_direction': effect_direction,
            'effect_score': counter_effect_score,
            'positive_score': positive_score,
            'negative_score': negative_score
        }
    
    def _assess_dialectical_unity(self, determining_role: Dict,
                                 relative_independence: Dict,
                                 counter_effect: Dict) -> Dict:
        """评估辩证统一关系"""
        
        # 计算统一性分数
        determining_score = determining_role.get('determining_degree', 0)
        independence_score = relative_independence.get('independence_score', 0)
        effect_score = counter_effect.get('effect_score', 0)
        
        # 理想情况下：决定作用7分 + 相对独立6分 + 反作用5分 = 较好平衡
        ideal_determining = 7.0
        ideal_independence = 6.0
        ideal_effect = 5.0
        
        # 计算偏离度
        determining_deviation = abs(determining_score - ideal_determining)
        independence_deviation = abs(independence_score - ideal_independence)
        effect_deviation = abs(effect_score - ideal_effect)
        
        # 统一性质量（偏离度越小越好）
        total_deviation = determining_deviation + independence_deviation + effect_deviation
        unity_quality = max(0, 10 - total_deviation / 3)
        
        # 统一性水平
        if unity_quality >= 8.0:
            unity_level = "高度辩证统一"
        elif unity_quality >= 6.0:
            unity_level = "较好辩证统一"
        elif unity_quality >= 4.0:
            unity_level = "一般辩证统一"
        else:
            unity_level = "辩证统一不足"
        
        return {
            'unity_level': unity_level,
            'unity_quality': unity_quality,
            'determining_score': determining_score,
            'independence_score': independence_score,
            'effect_score': effect_score,
            'total_deviation': total_deviation
        }
    
    def _assess_base_superstructure_quality(self, economic_base: EconomicBase,
                                          superstructure: Superstructure,
                                          dialectical_unity: Dict) -> Dict:
        """评估经济基础-上层建筑分析质量"""
        
        # 基础分析质量
        forces_quality = (economic_base.productive_forces.technology_level + 
                         economic_base.productive_forces.labor_productivity) / 2
        
        # 上层建筑分析质量
        superstructure_quality = (superstructure.relative_independence + 
                                superstructure.counter_effect) / 2
        
        # 辩证统一质量
        unity_quality = dialectical_unity.get('unity_quality', 0)
        
        # 综合质量分数
        overall_quality = (forces_quality + superstructure_quality + unity_quality) / 3
        
        return {
            'forces_quality': forces_quality,
            'superstructure_quality': superstructure_quality,
            'unity_quality': unity_quality,
            'overall_quality': overall_quality,
            'quality_level': self._determine_quality_level(overall_quality)
        }
    
    def _identify_social_formation(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """识别当前社会形态"""
        
        formation_indicators = {
            'primitive_communism': ['原始', '氏族', '部落', '原始公社', '公有制', '平均分配'],
            'slave_society': ['奴隶', '奴隶制', '奴隶主', '奴隶社会', '强迫劳动'],
            'feudal_society': ['封建', '地主', '农民', '土地', '农奴', '封建社会'],
            'capitalist_society': ['资本', '资本主义', '资产阶级', '无产阶级', '市场经济'],
            'socialist_society': ['社会主义', '公有制', '按劳分配', '人民民主', '计划经济'],
            'communist_society': ['共产主义', '按需分配', '各尽所能', '自由人联合体']
        }
        
        formation_scores = {}
        for formation, indicators in formation_indicators.items():
            score = sum(weight for word, weight in keywords if word in indicators)
            formation_scores[formation] = score
        
        # 确定主要社会形态
        primary_formation = max(formation_scores.items(), key=lambda x: x[1])[0]
        
        # 映射到中文社会形态名称
        formation_mapping = {
            'primitive_communism': '原始共产主义社会',
            'slave_society': '奴隶社会',
            'feudal_society': '封建社会',
            'capitalist_society': '资本主义社会',
            'socialist_society': '社会主义社会',
            'communist_society': '共产主义社会'
        }
        
        current_formation = formation_mapping.get(primary_formation, '未知社会形态')
        
        # 计算识别置信度
        max_score = formation_scores[primary_formation]
        total_score = sum(formation_scores.values())
        confidence = max_score / total_score if total_score > 0 else 0
        
        return {
            'current_formation': current_formation,
            'formation_type': primary_formation,
            'confidence': confidence,
            'formation_scores': formation_scores
        }
    
    def _analyze_development_stage(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析发展阶段"""
        
        stage_indicators = {
            'emergence': ['形成', '产生', '出现', '兴起', '起步', '初期'],
            'development': ['发展', '成长', '壮大', '扩展', '深化', '中期'],
            'maturity': ['成熟', '完善', '稳定', '高峰', '鼎盛', '成熟期'],
            'decline': ['衰落', '退化', '衰退', '下降', '萎缩', '后期'],
            'transformation': ['转型', '变革', '转变', '过渡', '转换', '变革期']
        }
        
        stage_scores = {}
        for stage, indicators in stage_indicators.items():
            score = sum(weight for word, weight in keywords if word in indicators)
            stage_scores[stage] = score
        
        # 确定主要发展阶段
        primary_stage = max(stage_scores.items(), key=lambda x: x[1])[0]
        
        # 映射到中文阶段名称
        stage_mapping = {
            'emergence': '形成阶段',
            'development': '发展阶段',
            'maturity': '成熟阶段',
            'decline': '衰落阶段',
            'transformation': '转型阶段'
        }
        
        current_stage = stage_mapping.get(primary_stage, '未知阶段')
        
        return {
            'current_stage': current_stage,
            'stage_type': primary_stage,
            'stage_scores': stage_scores
        }
    
    def _identify_primary_contradiction(self, text_data: str, keywords: List[Tuple]) -> SocialContradiction:
        """识别主要矛盾"""
        
        contradiction_indicators = {
            'productivity_relations': ['生产力', '生产关系', '矛盾', '冲突', '不适应'],
            'economic_base_superstructure': ['经济基础', '上层建筑', '矛盾', '冲突', '不协调'],
            'class_contradiction': ['阶级', '矛盾', '斗争', '对立', '冲突'],
            'social_contradiction': ['社会', '矛盾', '问题', '挑战', '困境']
        }
        
        contradiction_scores = {}
        for contradiction, indicators in contradiction_indicators.items():
            score = sum(weight for word, weight in keywords if word in indicators)
            contradiction_scores[contradiction] = score
        
        # 确定主要矛盾
        primary_contradiction = max(contradiction_scores.items(), key=lambda x: x[1])[0]
        
        # 识别次要矛盾
        secondary_contradictions = [contr for contr, score in contradiction_scores.items() 
                                 if score > 0 and contr != primary_contradiction]
        
        # 计算矛盾强度
        contradiction_intensity = contradiction_scores[primary_contradiction]
        
        # 判断发展阶段
        if contradiction_intensity >= 8.0:
            development_stage = "激化阶段"
        elif contradiction_intensity >= 5.0:
            development_stage = "发展阶段"
        elif contradiction_intensity >= 2.0:
            development_stage = "显现阶段"
        else:
            development_stage = "潜在阶段"
        
        # 判断解决趋势
        resolution_indicators = ['解决', '处理', '化解', '克服', '改革', '调整']
        resolution_score = sum(weight for word, weight in keywords if word in resolution_indicators)
        
        if resolution_score >= 5.0:
            resolution_tendency = "有望解决"
        elif resolution_score >= 2.0:
            resolution_tendency = "正在解决"
        else:
            resolution_tendency = "亟待解决"
        
        return SocialContradiction(
            primary_contradiction=primary_contradiction,
            secondary_contradictions=secondary_contradictions,
            contradiction_intensity=contradiction_intensity,
            development_stage=development_stage,
            resolution_tendency=resolution_tendency
        )
    
    def _analyze_historical_necessity(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析历史必然性"""
        
        necessity_indicators = self.social_development_vocabulary['necessity_indicators']
        
        necessity_score = sum(weight for word, weight in keywords if word in necessity_indicators)
        
        # 必然性水平
        if necessity_score >= 8.0:
            necessity_level = "历史必然性强"
        elif necessity_score >= 5.0:
            necessity_level = "历史必然性较强"
        elif necessity_score >= 2.0:
            necessity_level = "具有一定历史必然性"
        else:
            necessity_level = "历史必然性不明显"
        
        # 必然性特征
        necessity_features = []
        if necessity_score >= 5.0:
            necessity_features.append("符合客观规律")
        if necessity_score >= 7.0:
            necessity_features.append("具有历史趋势性")
        
        return {
            'necessity_level': necessity_level,
            'necessity_score': necessity_score,
            'necessity_features': necessity_features
        }
    
    def _analyze_development_diversity(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析发展道路多样性"""
        
        diversity_indicators = self.social_development_vocabulary['diversity_indicators']
        
        diversity_score = sum(weight for word, weight in keywords if word in diversity_indicators)
        
        # 多样性水平
        if diversity_score >= 8.0:
            diversity_level = "高度多样性"
        elif diversity_score >= 5.0:
            diversity_level = "较高多样性"
        elif diversity_score >= 2.0:
            diversity_level = "一定多样性"
        else:
            diversity_level = "多样性不足"
        
        # 多样性特征
        diversity_features = []
        if diversity_score >= 5.0:
            diversity_features.append("体现普遍性与特殊性统一")
        if diversity_score >= 7.0:
            diversity_features.append("具有本国特色")
        
        return {
            'diversity_level': diversity_level,
            'diversity_score': diversity_score,
            'diversity_features': diversity_features
        }
    
    def _analyze_people_historical_role(self, text_data: str, keywords: List[Tuple]) -> Dict:
        """分析人民群众历史作用"""
        
        people_role_indicators = self.social_development_vocabulary['people_role_indicators']
        
        people_role_score = sum(weight for word, weight in keywords if word in people_role_indicators)
        
        # 人民群众作用水平
        if people_role_score >= 8.0:
            role_level = "人民主体作用突出"
        elif people_role_score >= 5.0:
            role_level = "人民主体作用明显"
        elif people_role_score >= 2.0:
            role_level = "体现人民主体作用"
        else:
            role_level = "人民主体作用不明显"
        
        # 作用特征
        role_features = []
        if people_role_score >= 5.0:
            role_features.append("人民群众是历史创造者")
        if people_role_score >= 7.0:
            role_features.append("发挥人民首创精神")
        
        return {
            'role_level': role_level,
            'role_score': people_role_score,
            'role_features': role_features
        }
    
    def _assess_formation_quality(self, current_formation: Dict,
                                 development_stage: Dict,
                                 historical_necessity: Dict) -> Dict:
        """评估社会形态分析质量"""
        
        # 形态识别质量
        formation_confidence = current_formation.get('confidence', 0)
        formation_quality = formation_confidence * 10
        
        # 发展阶段分析质量
        stage_scores = development_stage.get('stage_scores', {})
        max_stage_score = max(stage_scores.values()) if stage_scores else 0
        stage_quality = min(max_stage_score, 10.0)
        
        # 历史必然性分析质量
        necessity_quality = historical_necessity.get('necessity_score', 0)
        necessity_quality = min(necessity_quality, 10.0)
        
        # 综合质量分数
        overall_quality = (formation_quality + stage_quality + necessity_quality) / 3
        
        return {
            'formation_quality': formation_quality,
            'stage_quality': stage_quality,
            'necessity_quality': necessity_quality,
            'overall_quality': overall_quality,
            'quality_level': self._determine_quality_level(overall_quality)
        }
    
    def _analyze_historical_materialism_connections(self, contradiction_analysis: Dict,
                                                  base_superstructure_analysis: Dict,
                                                  formation_analysis: Dict) -> Dict:
        """分析历史唯物主义内在联系"""
        
        # 生产力-生产关系矛盾与经济基础-上层建筑的关系
        contradiction_base_relation = self._analyze_contradiction_base_relation(
            contradiction_analysis, base_superstructure_analysis
        )
        
        # 经济基础-上层建筑与社会形态发展的关系
        base_formation_relation = self._analyze_base_formation_relation(
            base_superstructure_analysis, formation_analysis
        )
        
        # 矛盾运动与社会形态变革的关系
        contradiction_formation_relation = self._analyze_contradiction_formation_relation(
            contradiction_analysis, formation_analysis
        )
        
        return {
            'contradiction_base_relation': contradiction_base_relation,
            'base_formation_relation': base_formation_relation,
            'contradiction_formation_relation': contradiction_formation_relation,
            'overall_coherence': self._assess_historical_coherence(
                contradiction_analysis, base_superstructure_analysis, formation_analysis
            )
        }
    
    def _analyze_contradiction_base_relation(self, contradiction_analysis: Dict,
                                            base_superstructure_analysis: Dict) -> Dict:
        """分析矛盾运动与基础-建筑关系"""
        
        contradiction_quality = contradiction_analysis.get('contradiction_quality', {}).get('overall_quality', 0)
        base_quality = base_superstructure_analysis.get('base_superstructure_quality', {}).get('overall_quality', 0)
        
        relation_strength = (contradiction_quality + base_quality) / 2
        
        return {
            'relation_strength': relation_strength,
            'relation_description': '生产力-生产关系矛盾决定经济基础-上层建筑关系',
            'relation_quality': self._assess_relation_quality(relation_strength)
        }
    
    def _analyze_base_formation_relation(self, base_superstructure_analysis: Dict,
                                        formation_analysis: Dict) -> Dict:
        """分析基础-建筑关系与社会形态发展"""
        
        base_quality = base_superstructure_analysis.get('base_superstructure_quality', {}).get('overall_quality', 0)
        formation_quality = formation_analysis.get('formation_quality', {}).get('overall_quality', 0)
        
        relation_strength = (base_quality + formation_quality) / 2
        
        return {
            'relation_strength': relation_strength,
            'relation_description': '经济基础-上层建筑关系决定社会形态性质',
            'relation_quality': self._assess_relation_quality(relation_strength)
        }
    
    def _analyze_contradiction_formation_relation(self, contradiction_analysis: Dict,
                                                 formation_analysis: Dict) -> Dict:
        """分析矛盾运动与社会形态变革"""
        
        contradiction_quality = contradiction_analysis.get('contradiction_quality', {}).get('overall_quality', 0)
        formation_quality = formation_analysis.get('formation_quality', {}).get('overall_quality', 0)
        
        relation_strength = (contradiction_quality + formation_quality) / 2
        
        return {
            'relation_strength': relation_strength,
            'relation_description': '矛盾运动推动社会形态变革发展',
            'relation_quality': self._assess_relation_quality(relation_strength)
        }
    
    def _assess_relation_quality(self, strength: float) -> str:
        """评估关系质量"""
        if strength >= 8.0:
            return "高度协调"
        elif strength >= 6.0:
            return "较好协调"
        elif strength >= 4.0:
            return "一般协调"
        else:
            return "协调不足"
    
    def _assess_historical_coherence(self, contradiction_analysis: Dict,
                                    base_superstructure_analysis: Dict,
                                    formation_analysis: Dict) -> Dict:
        """评估历史唯物主义整体协调性"""
        
        contradiction_quality = contradiction_analysis.get('contradiction_quality', {}).get('overall_quality', 0)
        base_quality = base_superstructure_analysis.get('base_superstructure_quality', {}).get('overall_quality', 0)
        formation_quality = formation_analysis.get('formation_quality', {}).get('overall_quality', 0)
        
        overall_coherence = (contradiction_quality + base_quality + formation_quality) / 3
        
        return {
            'overall_coherence_score': overall_coherence,
            'coherence_level': self._determine_coherence_level(overall_coherence),
            'coherence_description': self._describe_historical_coherence(overall_coherence)
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
    
    def _describe_historical_coherence(self, score: float) -> str:
        """描述历史唯物主义协调性"""
        if score >= 8.0:
            return "历史唯物主义三大分析高度统一，形成完整的理论分析体系"
        elif score >= 6.0:
            return "历史唯物主义三大分析基本协调，理论分析较为完整"
        elif score >= 4.0:
            return "历史唯物主义三大分析有一定协调，但需要进一步完善"
        else:
            return "历史唯物主义三大分析协调不足，理论分析需要系统性提升"
    
    def _assess_overall_theoretical_level(self, contradiction_analysis: Dict,
                                        base_superstructure_analysis: Dict,
                                        formation_analysis: Dict) -> Dict:
        """评估整体理论水平"""
        
        # 计算各分析模块的质量分数
        contradiction_quality = contradiction_analysis.get('contradiction_quality', {}).get('overall_quality', 0)
        base_quality = base_superstructure_analysis.get('base_superstructure_quality', {}).get('overall_quality', 0)
        formation_quality = formation_analysis.get('formation_quality', {}).get('overall_quality', 0)
        
        # 计算整体水平
        overall_score = (contradiction_quality + base_quality + formation_quality) / 3
        
        # 确定理论等级
        if overall_score >= 8.5:
            theoretical_level = "历史唯物主义理论大师级"
        elif overall_score >= 7.0:
            theoretical_level = "历史唯物主义理论专家级"
        elif overall_score >= 5.5:
            theoretical_level = "历史唯物主义理论熟练级"
        elif overall_score >= 4.0:
            theoretical_level = "历史唯物主义理论基础级"
        else:
            theoretical_level = "历史唯物主义理论入门级"
        
        return {
            'overall_score': overall_score,
            'theoretical_level': theoretical_level,
            'strengths': self._identify_theoretical_strengths(
                contradiction_analysis, base_superstructure_analysis, formation_analysis
            ),
            'weaknesses': self._identify_theoretical_weaknesses(
                contradiction_analysis, base_superstructure_analysis, formation_analysis
            ),
            'improvement_directions': self._suggest_theoretical_improvements(
                contradiction_analysis, base_superstructure_analysis, formation_analysis
            )
        }
    
    def _identify_theoretical_strengths(self, contradiction_analysis: Dict,
                                        base_superstructure_analysis: Dict,
                                        formation_analysis: Dict) -> List[str]:
        """识别理论分析优势"""
        strengths = []
        
        contradiction_quality = contradiction_analysis.get('contradiction_quality', {}).get('overall_quality', 0)
        base_quality = base_superstructure_analysis.get('base_superstructure_quality', {}).get('overall_quality', 0)
        formation_quality = formation_analysis.get('formation_quality', {}).get('overall_quality', 0)
        
        if contradiction_quality >= 7.0:
            strengths.append("生产力-生产关系矛盾分析能力强")
        if base_quality >= 7.0:
            strengths.append("经济基础-上层建筑关系分析能力强")
        if formation_quality >= 7.0:
            strengths.append("社会形态发展规律分析能力强")
        
        return strengths
    
    def _identify_theoretical_weaknesses(self, contradiction_analysis: Dict,
                                         base_superstructure_analysis: Dict,
                                         formation_analysis: Dict) -> List[str]:
        """识别理论分析不足"""
        weaknesses = []
        
        contradiction_quality = contradiction_analysis.get('contradiction_quality', {}).get('overall_quality', 0)
        base_quality = base_superstructure_analysis.get('base_superstructure_quality', {}).get('overall_quality', 0)
        formation_quality = formation_analysis.get('formation_quality', {}).get('overall_quality', 0)
        
        if contradiction_quality < 5.0:
            weaknesses.append("生产力-生产关系矛盾分析需要加强")
        if base_quality < 5.0:
            weaknesses.append("经济基础-上层建筑关系分析需要加强")
        if formation_quality < 5.0:
            weaknesses.append("社会形态发展规律分析需要加强")
        
        return weaknesses
    
    def _suggest_theoretical_improvements(self, contradiction_analysis: Dict,
                                         base_superstructure_analysis: Dict,
                                         formation_analysis: Dict) -> List[str]:
        """建议理论改进方向"""
        directions = []
        
        contradiction_quality = contradiction_analysis.get('contradiction_quality', {}).get('overall_quality', 0)
        base_quality = base_superstructure_analysis.get('base_superstructure_quality', {}).get('overall_quality', 0)
        formation_quality = formation_analysis.get('formation_quality', {}).get('overall_quality', 0)
        
        if contradiction_quality < 6.0:
            directions.append("深入学习生产力-生产关系矛盾运动规律")
        if base_quality < 6.0:
            directions.append("加强对经济基础-上层建筑辩证关系的理解")
        if formation_quality < 6.0:
            directions.append("提升对社会形态发展规律的认识")
        
        # 综合建议
        avg_quality = (contradiction_quality + base_quality + formation_quality) / 3
        if avg_quality < 5.0:
            directions.append("系统学习历史唯物主义基本原理")
        elif avg_quality < 7.0:
            directions.append("加强历史唯物主义的实际应用训练")
        
        return directions
    
    def _generate_professional_recommendations(self, contradiction_analysis: Dict,
                                               base_superstructure_analysis: Dict,
                                               formation_analysis: Dict) -> List[str]:
        """生成专业建议"""
        recommendations = []
        
        # 基于各分析模块结果生成建议
        contradiction_quality = contradiction_analysis.get('contradiction_quality', {}).get('overall_quality', 0)
        base_quality = base_superstructure_analysis.get('base_superstructure_quality', {}).get('overall_quality', 0)
        formation_quality = formation_analysis.get('formation_quality', {}).get('overall_quality', 0)
        
        if contradiction_quality >= 7.0:
            recommendations.append("生产力-生产关系矛盾分析能力优秀，继续保持理论深度")
        elif contradiction_quality >= 5.0:
            recommendations.append("生产力-生产关系矛盾分析能力良好，可加强矛盾转化分析")
        else:
            recommendations.append("重点加强对立统一规律在生产力-生产关系分析中的应用")
        
        if base_quality >= 7.0:
            recommendations.append("经济基础-上层建筑关系分析能力优秀，继续保持")
        elif base_quality >= 5.0:
            recommendations.append("经济基础-上层建筑关系分析能力良好，可加强相对独立性分析")
        else:
            recommendations.append("重点学习经济基础决定作用和上层建筑相对独立性原理")
        
        if formation_quality >= 7.0:
            recommendations.append("社会形态发展规律分析能力优秀，继续保持")
        elif formation_quality >= 5.0:
            recommendations.append("社会形态发展规律分析能力良好，可加强历史必然性分析")
        else:
            recommendations.append("重点学习社会形态更替的历史必然性和多样性统一")
        
        # 综合建议
        overall_level = self._assess_overall_theoretical_level(
            contradiction_analysis, base_superstructure_analysis, formation_analysis
        )
        overall_score = overall_level.get('overall_score', 0)
        
        if overall_score >= 7.0:
            recommendations.append("历史唯物主义理论整体水平较高，建议在复杂社会分析中进一步应用")
        elif overall_score >= 5.0:
            recommendations.append("历史唯物主义理论基础良好，建议加强系统性训练")
        else:
            recommendations.append("建议系统学习历史唯物主义基本原理，打好理论基础")
        
        return recommendations
    
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


def main():
    """测试增强版历史唯物主义分析器"""
    analyzer = EnhancedHistoricalMaterialismAnalyzer()
    
    test_text = """
    在当代中国特色社会主义发展中，生产力水平显著提升，特别是数字经济和智能技术的快速发展，
    推动了社会生产力的跨越式发展。生产资料所有制坚持公有制为主体、多种所有制经济共同发展，
    劳动关系呈现多元化特点，分配制度坚持按劳分配为主体。
    
    经济基础的快速发展为上层建筑的完善提供了坚实物质基础。政治制度坚持社会主义民主政治，
    法律体系日益完善，意识形态领域坚持马克思主义指导地位，文化事业繁荣发展。
    上层建筑对经济基础发挥着重要的反作用，推动了经济社会的协调发展。
    
    当前社会主要矛盾已经转化为人民日益增长的美好生活需要和不平衡不充分的发展之间的矛盾。
    社会主义初级阶段的基本国情没有改变，但发展阶段进入了新时代。社会发展的历史必然性
    体现在中国特色社会主义道路的正确性上，同时体现了发展道路的多样性。人民群众在历史发展中
    发挥着主体作用，是历史的创造者。
    """
    
    print("=== 增强版历史唯物主义分析器测试 ===")
    
    # 执行综合历史唯物主义分析
    result = analyzer.comprehensive_historical_materialism_analysis(test_text)
    
    # 显示主要结果
    print("\n=== 生产力-生产关系矛盾运动分析 ===")
    contradiction_analysis = result['contradiction_analysis']
    contradiction_quality = contradiction_analysis.get('contradiction_quality', {})
    print(f"矛盾分析质量: {contradiction_quality.get('overall_quality', 0):.2f}")
    print(f"质量等级: {contradiction_quality.get('quality_level', '未知')}")
    
    print("\n=== 经济基础-上层建筑辩证关系分析 ===")
    base_superstructure_analysis = result['base_superstructure_analysis']
    base_quality = base_superstructure_analysis.get('base_superstructure_quality', {})
    print(f"基础-建筑分析质量: {base_quality.get('overall_quality', 0):.2f}")
    print(f"质量等级: {base_quality.get('quality_level', '未知')}")
    
    print("\n=== 社会形态发展规律分析 ===")
    formation_analysis = result['formation_analysis']
    formation_quality = formation_analysis.get('formation_quality', {})
    print(f"社会形态分析质量: {formation_quality.get('overall_quality', 0):.2f}")
    print(f"质量等级: {formation_quality.get('quality_level', '未知')}")
    
    print("\n=== 整体理论水平 ===")
    overall_level = result['overall_theoretical_level']
    print(f"整体分数: {overall_level.get('overall_score', 0):.2f}")
    print(f"理论等级: {overall_level.get('theoretical_level', '未知')}")
    
    strengths = overall_level.get('strengths', [])
    if strengths:
        print("理论优势:")
        for strength in strengths:
            print(f"  - {strength}")
    
    weaknesses = overall_level.get('weaknesses', [])
    if weaknesses:
        print("理论不足:")
        for weakness in weaknesses:
            print(f"  - {weakness}")
    
    recommendations = overall_level.get('improvement_directions', [])
    if recommendations:
        print("改进建议:")
        for recommendation in recommendations:
            print(f"  - {recommendation}")


if __name__ == "__main__":
    main()
