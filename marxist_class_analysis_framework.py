#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
马克思主义阶级分析专业框架
Marxist Class Analysis Professional Framework

作者: 马克思主义理论专家
版本: 1.0.0
日期: 2025-12-21
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional, Union
from dataclasses import dataclass
from enum import Enum
import json
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ClassType(Enum):
    """阶级类型枚举"""
    BOURGEOISIE = "资产阶级"  # 资产阶级
    PETTY_BOURGEOISIE = "小资产阶级"  # 小资产阶级
    PROLETARIAT = "无产阶级"  # 无产阶级
    SEMI_PROLETARIAT = "半无产阶级"  # 半无产阶级
    LUMPROLETARIAT = "流氓无产阶级"  # 流氓无产阶级
    NEW_MIDDLE_CLASS = "新中间阶层"  # 新中间阶层
    KNOWLEDGE_WORKER = "知识工作者"  # 知识工作者
    PRECARIAT = "不稳定无产者"  # 不稳定无产者

class ConsciousnessLevel(Enum):
    """阶级意识水平枚举"""
    CLASS_IN_ITSELF = "自在阶级"  # 自在阶级
    EMERGING_CONSCIOUSNESS = "萌芽意识"  # 萌芽意识
    DEVELOPING_CONSCIOUSNESS = "发展中意识"  # 发展中意识
    CLASS_FOR_ITSELF = "自为阶级"  # 自为阶级
    REVOLUTIONARY_CONSCIOUSNESS = "革命意识"  # 革命意识

@dataclass
class ProductionMeans:
    """生产资料占有关系"""
    ownership_rate: float  # 生产资料所有权比例 (0-1)
    control_rate: float   # 控制权比例 (0-1)
    access_rate: float    # 访问权比例 (0-1)
    inheritance_rate: float  # 继承权比例 (0-1)
    
    def total_control_score(self) -> float:
        """计算总控制分数"""
        return (self.ownership_rate * 0.4 + 
                self.control_rate * 0.3 + 
                self.access_rate * 0.2 + 
                self.inheritance_rate * 0.1)

@dataclass
class LaborRelation:
    """劳动关系特征"""
    wage_dependence: float  # 工资依赖度 (0-1)
    exploitation_rate: float  # 被剥削程度 (0-1)
    autonomy_level: float    # 自主性水平 (0-1)
    skill_level: float      # 技能水平 (0-1)
    
    def exploitation_score(self) -> float:
        """计算剥削分数"""
        return self.exploitation_rate * 0.6 + self.wage_dependence * 0.4

@dataclass
class ClassPosition:
    """阶级地位"""
    production_means: ProductionMeans
    labor_relation: LaborRelation
    income_level: float  # 收入水平
    education_level: float  # 教育水平
    social_status: float  # 社会地位
    
    def class_determination_score(self) -> float:
        """计算阶级判定分数"""
        pm_score = self.production_means.total_control_score()
        lr_score = self.labor_relation.exploitation_score()
        return pm_score * 0.5 - lr_score * 0.3 + self.income_level * 0.2

class MarxistClassAnalyzer:
    """马克思主义阶级分析器"""
    
    def __init__(self):
        self.class_boundaries = {
            'bourgeoisie_threshold': 0.7,
            'petty_bourgeoisie_upper': 0.3,
            'petty_bourgeoisie_lower': 0.0,
            'proletariat_upper': 0.0,
            'proletariat_lower': -0.5,
            'semi_proletariat_threshold': -0.3
        }
        
        self.consciousness_indicators = {
            'class_identity': 0.3,
            'political_awareness': 0.25,
            'collective_action': 0.2,
            'historical_understanding': 0.15,
            'revolutionary_will': 0.1
        }
    
    def classify_individual(self, position: ClassPosition) -> Tuple[ClassType, float]:
        """
        个体阶级分类算法
        
        Args:
            position: 阶级地位数据
            
        Returns:
            (阶级类型, 置信度)
        """
        score = position.class_determination_score()
        
        if score >= self.class_boundaries['bourgeoisie_threshold']:
            return ClassType.BOURGEOISIE, min(1.0, (score - 0.7) / 0.3)
        elif score >= self.class_boundaries['petty_bourgeoisie_upper']:
            return ClassType.PETTY_BOURGEOISIE, (score - 0.3) / 0.4
        elif score >= self.class_boundaries['petty_bourgeoisie_lower']:
            return ClassType.PETTY_BOURGEOISIE, (score - 0.0) / 0.3 + 0.5
        elif score >= self.class_boundaries['proletariat_upper']:
            return ClassType.PROLETARIAT, 1.0 - abs(score) / 0.5
        elif score >= self.class_boundaries['proletariat_lower']:
            return ClassType.PROLETARIAT, 0.7 - abs(score + 0.25) / 0.25
        else:
            return ClassType.SEMI_PROLETARIAT, min(1.0, abs(score + 0.5) / 0.3)
    
    def analyze_class_structure(self, positions: List[ClassPosition]) -> Dict:
        """
        阶级结构分析
        
        Args:
            positions: 个体阶级地位列表
            
        Returns:
            阶级结构分析结果
        """
        classifications = [self.classify_individual(pos) for pos in positions]
        class_counts = {}
        confidence_scores = []
        
        for class_type, confidence in classifications:
            class_name = class_type.value
            class_counts[class_name] = class_counts.get(class_name, 0) + 1
            confidence_scores.append(confidence)
        
        total = len(positions)
        class_percentages = {k: v/total*100 for k, v in class_counts.items()}
        
        # 计算阶级结构复杂度
        shannon_entropy = -sum((p/100) * np.log2(p/100) 
                              for p in class_percentages.values() if p > 0)
        max_entropy = np.log2(len(class_counts))
        complexity_index = shannon_entropy / max_entropy if max_entropy > 0 else 0
        
        return {
            'class_distribution': class_percentages,
            'class_counts': class_counts,
            'total_individuals': total,
            'complexity_index': complexity_index,
            'average_confidence': np.mean(confidence_scores),
            'shannon_entropy': shannon_entropy
        }
    
    def calculate_class_conflict_intensity(self, class_structure: Dict) -> float:
        """
        计算阶级冲突强度
        
        Args:
            class_structure: 阶级结构数据
            
        Returns:
            冲突强度指数 (0-1)
        """
        distribution = class_structure['class_distribution']
        
        # 资产阶级与无产阶级的比例差异
        bourgeoisie_ratio = distribution.get('资产阶级', 0) / 100
        proletariat_ratio = distribution.get('无产阶级', 0) / 100
        
        # 收入不平等指数 (基尼系数近似)
        income_inequality = abs(bourgeoisie_ratio - proletariat_ratio)
        
        # 结构复杂性导致的潜在冲突
        complexity_factor = class_structure['complexity_index']
        
        # 冲突强度综合计算
        conflict_intensity = (income_inequality * 0.5 + 
                            complexity_factor * 0.3 + 
                            (1 - class_structure['average_confidence']) * 0.2)
        
        return min(1.0, conflict_intensity)
    
    def assess_class_consciousness(self, 
                                individual_data: Dict,
                                social_context: Dict) -> Tuple[ConsciousnessLevel, float]:
        """
        评估阶级意识水平
        
        Args:
            individual_data: 个体数据
            social_context: 社会背景数据
            
        Returns:
            (意识水平, 意识指数)
        """
        # 计算各项指标得分
        class_identity = individual_data.get('class_identity_score', 0)
        political_awareness = individual_data.get('political_awareness', 0)
        collective_action = individual_data.get('collective_action_participation', 0)
        historical_understanding = individual_data.get('historical_understanding', 0)
        revolutionary_will = individual_data.get('revolutionary_will', 0)
        
        # 加权计算意识指数
        consciousness_index = (
            class_identity * self.consciousness_indicators['class_identity'] +
            political_awareness * self.consciousness_indicators['political_awareness'] +
            collective_action * self.consciousness_indicators['collective_action'] +
            historical_understanding * self.consciousness_indicators['historical_understanding'] +
            revolutionary_will * self.consciousness_indicators['revolutionary_will']
        )
        
        # 考虑社会环境影响
        social_pressure = social_context.get('class_struggle_intensity', 0)
        organizational_support = social_context.get('organizational_presence', 0)
        
        adjusted_index = consciousness_index * (1 + social_pressure * 0.2) * (1 + organizational_support * 0.1)
        adjusted_index = min(1.0, adjusted_index)
        
        # 确定意识水平
        if adjusted_index < 0.2:
            return ConsciousnessLevel.CLASS_IN_ITSELF, adjusted_index
        elif adjusted_index < 0.4:
            return ConsciousnessLevel.EMERGING_CONSCIOUSNESS, adjusted_index
        elif adjusted_index < 0.6:
            return ConsciousnessLevel.DEVELOPING_CONSCIOUSNESS, adjusted_index
        elif adjusted_index < 0.8:
            return ConsciousnessLevel.CLASS_FOR_ITSELF, adjusted_index
        else:
            return ConsciousnessLevel.REVOLUTIONARY_CONSCIOUSNESS, adjusted_index
    
    def identify_new_social_classes(self, 
                                  economic_data: Dict,
                                  technology_data: Dict) -> List[Dict]:
        """
        识别新兴社会阶层
        
        Args:
            economic_data: 经济数据
            technology_data: 技术数据
            
        Returns:
            新兴阶层列表
        """
        new_classes = []
        
        # 知识工作者识别
        knowledge_economy_ratio = economic_data.get('knowledge_economy_percentage', 0)
        if knowledge_economy_ratio > 0.15:
            new_classes.append({
                'name': '知识工作者',
                'characteristics': [
                    '高技能知识劳动',
                    '信息生产与处理',
                    '相对自主性',
                    '中等收入水平'
                ],
                'size_percentage': knowledge_economy_ratio * 100,
                'class_position': '介于小资产阶级与无产阶级之间'
            })
        
        # 不稳定无产者识别
        precariat_indicators = [
            technology_data.get('automation_displacement_rate', 0),
            economic_data.get('gig_economy_growth', 0),
            economic_data.get('temporary_work_percentage', 0)
        ]
        precariat_score = np.mean(precariat_indicators)
        
        if precariat_score > 0.2:
            new_classes.append({
                'name': '不稳定无产者',
                'characteristics': [
                    '工作不稳定性',
                    '缺乏社会保障',
                    '收入波动性大',
                    '阶级意识模糊'
                ],
                'size_percentage': precariat_score * 100,
                'class_position': '无产阶级的新形态'
            })
        
        # 新中间阶层识别
        service_economy_ratio = economic_data.get('service_economy_percentage', 0)
        professional_education = economic_data.get('higher_education_rate', 0)
        
        if service_economy_ratio > 0.6 and professional_education > 0.3:
            new_classes.append({
                'name': '新中间阶层',
                'characteristics': [
                    '专业技术人员',
                    '管理人员',
                    '服务业从业者',
                    '消费主义倾向'
                ],
                'size_percentage': (service_economy_ratio + professional_education) * 50,
                'class_position': '阶级立场摇摆'
            })
        
        return new_classes
    
    def predict_class_consciousness_evolution(self, 
                                            current_state: Dict,
                                            historical_trends: List[Dict]) -> Dict:
        """
        预测阶级意识演化趋势
        
        Args:
            current_state: 当前状态
            historical_trends: 历史趋势数据
            
        Returns:
            演化预测结果
        """
        # 提取历史趋势
        consciousness_trend = [t.get('consciousness_index', 0) for t in historical_trends]
        conflict_trend = [t.get('conflict_intensity', 0) for t in historical_trends]
        
        if len(consciousness_trend) < 3:
            return {'error': '历史数据不足，无法进行预测'}
        
        # 计算趋势斜率
        time_points = list(range(len(consciousness_trend)))
        consciousness_slope = np.polyfit(time_points, consciousness_trend, 1)[0]
        conflict_slope = np.polyfit(time_points, conflict_trend, 1)[0]
        
        # 预测未来5年
        future_years = 5
        future_consciousness = []
        future_conflict = []
        
        current_consciousness = current_state.get('average_consciousness', 0)
        current_conflict = current_state.get('conflict_intensity', 0)
        
        for i in range(1, future_years + 1):
            future_consciousness.append(current_consciousness + consciousness_slope * i)
            future_conflict.append(current_conflict + conflict_slope * i)
        
        # 识别关键转折点
        turning_points = []
        for i, (consciousness, conflict) in enumerate(zip(future_consciousness, future_conflict)):
            year = datetime.now().year + i
            if consciousness > 0.6 and conflict > 0.7:
                turning_points.append({
                    'year': year,
                    'type': '革命意识形成',
                    'consciousness_level': consciousness,
                    'conflict_level': conflict
                })
        
        return {
            'future_consciousness_trend': future_consciousness,
            'future_conflict_trend': future_conflict,
            'turning_points': turning_points,
            'consciousness_growth_rate': consciousness_slope,
            'conflict_growth_rate': conflict_slope,
            'prediction_confidence': min(len(historical_trends) / 10, 0.9)
        }
    
    def avoid_simplification_mechanisms(self, analysis_result: Dict) -> Dict:
        """
        防止简单化倾向的机制
        
        Args:
            analysis_result: 原始分析结果
            
        Returns:
            修正后的分析结果
        """
        # 检查教条化倾向
        simplification_warnings = []
        
        # 1. 检查过度概括
        class_distribution = analysis_result.get('class_distribution', {})
        dominant_class_percentage = max(class_distribution.values(), default=0)
        if dominant_class_percentage > 80:
            simplification_warnings.append(
                "警告：单一阶级占比过高，可能存在过度概括问题"
            )
        
        # 2. 检查历史具体性缺失
        if 'historical_context' not in analysis_result:
            simplification_warnings.append(
                "警告：缺乏历史具体性分析，结论可能过于抽象"
            )
        
        # 3. 检查阶级内部差异忽视
        if 'internal_class_variations' not in analysis_result:
            simplification_warnings.append(
                "警告：忽视阶级内部差异，可能存在标签化问题"
            )
        
        # 4. 添加复杂性指标
        complexity_enhancements = {
            'class_intersectionality': self._calculate_intersectionality(analysis_result),
            'regional_variations': self._assess_regional_variations(analysis_result),
            'historical_dynamics': self._evaluate_historical_dynamics(analysis_result),
            'cultural_factors': self._incorporate_cultural_factors(analysis_result)
        }
        
        # 5. 生成修正建议
        correction_recommendations = [
            "结合具体历史时期进行分析",
            "考虑阶级、性别、种族的交叉性",
            "关注地域差异和发展不平衡",
            "重视文化传统和意识形态影响",
            "避免机械套用经典理论"
        ]
        
        return {
            'original_analysis': analysis_result,
            'simplification_warnings': simplification_warnings,
            'complexity_enhancements': complexity_enhancements,
            'correction_recommendations': correction_recommendations,
            'scientific_validity_score': self._calculate_validity_score(analysis_result)
        }
    
    def _calculate_intersectionality(self, analysis_result: Dict) -> float:
        """计算交叉性指数"""
        # 简化的交叉性计算
        return np.random.uniform(0.3, 0.8)  # 实际应用中需要具体数据
    
    def _assess_regional_variations(self, analysis_result: Dict) -> Dict:
        """评估地域差异"""
        return {
            'urban_rural_gap': np.random.uniform(0.2, 0.6),
            'regional_development_gap': np.random.uniform(0.3, 0.7),
            'coastal_inland_difference': np.random.uniform(0.2, 0.5)
        }
    
    def _evaluate_historical_dynamics(self, analysis_result: Dict) -> float:
        """评估历史动态性"""
        return np.random.uniform(0.4, 0.9)  # 实际应用中需要历史数据
    
    def _incorporate_cultural_factors(self, analysis_result: Dict) -> Dict:
        """纳入文化因素"""
        return {
            'traditional_culture_influence': np.random.uniform(0.3, 0.7),
            'ideological_state': np.random.uniform(0.2, 0.8),
            'education_level_impact': np.random.uniform(0.4, 0.8)
        }
    
    def _calculate_validity_score(self, analysis_result: Dict) -> float:
        """计算科学性分数"""
        base_score = 0.7
        
        # 根据复杂度调整
        complexity = analysis_result.get('complexity_index', 0.5)
        complexity_bonus = (complexity - 0.5) * 0.2
        
        # 根据数据质量调整
        confidence = analysis_result.get('average_confidence', 0.5)
        confidence_bonus = (confidence - 0.5) * 0.1
        
        return min(1.0, base_score + complexity_bonus + confidence_bonus)

def generate_analysis_report(analyzer: MarxistClassAnalyzer, 
                           positions: List[ClassPosition],
                           context_data: Dict) -> str:
    """
    生成阶级分析报告
    
    Args:
        analyzer: 分析器实例
        positions: 个体数据
        context_data: 背景数据
        
    Returns:
        分析报告文本
    """
    # 执行分析
    structure_analysis = analyzer.analyze_class_structure(positions)
    conflict_intensity = analyzer.calculate_class_conflict_intensity(structure_analysis)
    new_classes = analyzer.identify_new_social_classes(
        context_data.get('economic_data', {}),
        context_data.get('technology_data', {})
    )
    
    # 防止简单化
    enhanced_analysis = analyzer.avoid_simplification_mechanisms(structure_analysis)
    
    # 生成报告
    report = f"""
# 马克思主义阶级分析报告

## 一、阶级结构分析
- 阶级分布: {structure_analysis['class_distribution']}
- 结构复杂度: {structure_analysis['complexity_index']:.3f}
- 分析置信度: {structure_analysis['average_confidence']:.3f}

## 二、阶级矛盾状况
- 冲突强度指数: {conflict_intensity:.3f}
- 矛盾发展阶段: {'激烈' if conflict_intensity > 0.7 else '缓和' if conflict_intensity < 0.3 else '发展中'}

## 三、新兴社会阶层
"""
    
    for new_class in new_classes:
        report += f"""
### {new_class['name']}
- 规模占比: {new_class['size_percentage']:.1f}%
- 阶级定位: {new_class['class_position']}
- 主要特征: {', '.join(new_class['characteristics'])}
"""
    
    report += f"""
## 四、科学性评估
- 科学性分数: {enhanced_analysis['scientific_validity_score']:.3f}
- 简单化警告: {len(enhanced_analysis['simplification_warnings'])}项
- 复杂性增强: {len(enhanced_analysis['complexity_enhancements'])}个维度

## 五、分析建议
"""
    
    for recommendation in enhanced_analysis['correction_recommendations']:
        report += f"- {recommendation}\n"
    
    return report

# 示例使用
if __name__ == "__main__":
    # 创建分析器
    analyzer = MarxistClassAnalyzer()
    
    # 模拟数据
    positions = [
        ClassPosition(
            production_means=ProductionMeans(0.8, 0.7, 0.6, 0.5),
            labor_relation=LaborRelation(0.2, 0.1, 0.8, 0.7),
            income_level=0.9,
            education_level=0.8,
            social_status=0.85
        ),
        ClassPosition(
            production_means=ProductionMeans(0.1, 0.1, 0.2, 0.0),
            labor_relation=LaborRelation(0.9, 0.8, 0.2, 0.4),
            income_level=0.3,
            education_level=0.5,
            social_status=0.4
        )
    ]
    
    context_data = {
        'economic_data': {
            'knowledge_economy_percentage': 0.25,
            'gig_economy_growth': 0.15,
            'service_economy_percentage': 0.7,
            'higher_education_rate': 0.4
        },
        'technology_data': {
            'automation_displacement_rate': 0.12
        }
    }
    
    # 生成报告
    report = generate_analysis_report(analyzer, positions, context_data)
    print(report)
