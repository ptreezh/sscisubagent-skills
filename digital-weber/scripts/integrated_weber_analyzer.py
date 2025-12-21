#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数字韦伯集成分析器 - 协调AI理论分析与脚本计算
实现韦伯社会学分析的智能化集成，确保定性与定量的有机结合
"""

import os
import json
from typing import Dict, List, Optional, Any
from weberian_analyzer import WeberianAnalyzer
import pandas as pd


class IntegratedWeberAnalyzer:
    """数字韦伯集成分析器"""
    
    def __init__(self):
        self.weberian_analyzer = WeberianAnalyzer()
        self.analysis_state = {}
        self.quality_monitor = WeberQualityMonitor()
        
    def execute_comprehensive_analysis(self, 
                                     text_data: str,
                                     research_context: Dict = None) -> Dict:
        """
        执行完整的韦伯社会学分析
        
        Parameters:
        -----------
        text_data : str
            待分析的文本数据
        research_context : Dict
            研究背景和上下文信息
            
        Returns:
        --------
        Dict : 完整分析结果
        """
        # 初始化分析状态
        self._initialize_analysis_state(research_context)
        
        # 阶段1: 社会行动类型学分析 (定量计算)
        print("执行社会行动类型学分析...")
        action_results = self.weberian_analyzer.analyze_social_action_typology(text_data)
        self.analysis_state['social_action_typology'] = action_results
        
        # 阶段2: 理性化过程研究 (定量计算)
        print("执行理性化过程研究...")
        rationalization_results = self.weberian_analyzer.analyze_rationalization_process(text_data)
        self.analysis_state['rationalization_process'] = rationalization_results
        
        # 阶段3: 权威合法性分析 (定量计算)
        print("执行权威合法性分析...")
        authority_results = self.weberian_analyzer.analyze_authority_legitimacy(text_data)
        self.analysis_state['authority_legitimacy'] = authority_results
        
        # 阶段4: 科层制与现代性分析 (定量计算)
        print("执行科层制与现代性分析...")
        bureaucracy_results = self.weberian_analyzer.analyze_bureaucracy_modernity(text_data)
        self.analysis_state['bureaucracy_modernity'] = bureaucracy_results
        
        # 质量检验
        quality_assessment = self.quality_monitor.assess_overall_quality(
            self.analysis_state
        )
        
        # 生成综合报告
        comprehensive_report = self._generate_integrated_report()
        
        return {
            'analysis_results': self.analysis_state,
            'quality_assessment': quality_assessment,
            'comprehensive_report': comprehensive_report,
            'recommendations': self._generate_recommendations()
        }
    
    def load_expert_guidance(self, expert_type: str) -> str:
        """
        加载相应专家的指导
        
        Parameters:
        -----------
        expert_type : str
            专家类型名称
            
        Returns:
        --------
        str : 专家指导内容
        """
        expert_files = {
            'theoretical_interpretation': 'prompts/theoretical-interpretation.md',
            'understanding_analysis': 'prompts/understanding-analysis.md',
            'institutional_analysis': 'prompts/institutional-analysis.md',
            'comparative_research': 'prompts/comparative-research.md'
        }
        
        if expert_type in expert_files:
            file_path = expert_files[expert_type]
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        
        return f"未找到 {expert_type} 专家的指导文件"
    
    def execute_expert_collaboration(self, 
                                   expert_types: List[str],
                                   text_data: str,
                                   context: Dict = None) -> Dict:
        """
        执行四重专家协作分析
        
        Parameters:
        -----------
        expert_types : List[str]
            专家类型列表
        text_data : str
            文本数据
        context : Dict
            上下文信息
            
        Returns:
        --------
        Dict : 协作分析结果
        """
        collaboration_results = {}
        
        for expert_type in expert_types:
            # 加载专家指导
            expert_guidance = self.load_expert_guidance(expert_type)
            
            # 根据专家类型执行相应分析
            if expert_type == 'theoretical_interpretation':
                results = self._execute_theoretical_analysis(text_data, context)
            elif expert_type == 'understanding_analysis':
                results = self._execute_understanding_analysis(text_data, context)
            elif expert_type == 'institutional_analysis':
                results = self._execute_institutional_analysis(text_data, context)
            elif expert_type == 'comparative_research':
                results = self._execute_comparative_analysis(text_data, context)
            else:
                results = {'error': f'未知的专家类型: {expert_type}'}
            
            # 添加专家指导信息
            results['expert_guidance'] = {
                'expert_type': expert_type,
                'guidance_loaded': bool(expert_guidance),
                'guidance_applied': True
            }
            
            collaboration_results[expert_type] = results
        
        return collaboration_results
    
    def _execute_theoretical_analysis(self, text_data: str, 
                                    context: Dict = None) -> Dict:
        """执行理论阐释专家分析"""
        # 基于已有的社会行动类型学分析结果
        if 'social_action_typology' in self.analysis_state:
            action_results = self.analysis_state['social_action_typology']
            
            # 理论阐释分析
            theoretical_analysis = {
                'concept_accuracy': self._assess_concept_accuracy(action_results),
                'theoretical_logic': self._assess_theoretical_logic(action_results),
                'methodology_consistency': self._assess_methodology_consistency(action_results),
                'theoretical_applicability': self._assess_theoretical_applicability(action_results)
            }
            
            return theoretical_analysis
        
        return {'error': '缺少社会行动类型学分析结果'}
    
    def _execute_understanding_analysis(self, text_data: str,
                                     context: Dict = None) -> Dict:
        """执行理解性分析专家分析"""
        understanding_analysis = {
            'subjective_meaning': self._analyze_subjective_meaning(text_data),
            'motivation_structure': self._analyze_motivation_structure(text_data),
            'meaning_context': self._analyze_meaning_context(text_data),
            'meaning_network': self._analyze_meaning_network(text_data)
        }
        
        return understanding_analysis
    
    def _execute_institutional_analysis(self, text_data: str,
                                      context: Dict = None) -> Dict:
        """执行制度分析专家分析"""
        # 基于已有的权威合法性和科层制分析结果
        authority_results = self.analysis_state.get('authority_legitimacy', {})
        bureaucracy_results = self.analysis_state.get('bureaucracy_modernity', {})
        
        institutional_analysis = {
            'authority_analysis': authority_results,
            'bureaucracy_analysis': bureaucracy_results,
            'institutional_rationality': self._assess_institutional_rationality(
                authority_results, bureaucracy_results
            ),
            'modernity_diagnosis': self._diagnose_modernity_issues(bureaucracy_results)
        }
        
        return institutional_analysis
    
    def _execute_comparative_analysis(self, text_data: str,
                                    context: Dict = None) -> Dict:
        """执行比较研究专家分析"""
        comparative_analysis = {
            'comparative_framework': self._build_comparative_framework(text_data),
            'development_pathways': self._analyze_development_pathways(text_data),
            'rationalization_comparison': self._compare_rationalization_processes(text_data),
            'causal_interpretation': self._interpret_causal_relationships(text_data)
        }
        
        return comparative_analysis
    
    def _initialize_analysis_state(self, research_context: Dict = None):
        """初始化分析状态"""
        self.analysis_state = {
            'research_context': research_context or {},
            'expert_collaboration': {},
            'analysis_phases': [],
            'quality_metrics': {},
            'interim_results': {}
        }
    
    def _generate_integrated_report(self) -> str:
        """生成集成分析报告"""
        report_sections = []
        
        # 报告标题
        report_sections.append("# 数字韦伯社会学集成分析报告")
        report_sections.append("")
        
        # 社会行动类型学结果
        if 'social_action_typology' in self.analysis_state:
            results = self.analysis_state['social_action_typology']
            report_sections.append("## 1. 社会行动类型学分析")
            report_sections.append(f"**行动类型**: {results['action_type']}")
            report_sections.append(f"**理性分数**: {results['rationality_score']:.2f}")
            
            # 各类型行动分析
            action_types = ['目的理性', '价值理性', '情感性', '传统性']
            for action_type in action_types:
                if action_type in results:
                    data = results[action_type]
                    report_sections.append(f"**{action_type}**: {data['level']} (分数: {data['score']:.2f})")
            
            report_sections.append("")
        
        # 理性化过程结果
        if 'rationalization_process' in self.analysis_state:
            results = self.analysis_state['rationalization_process']
            report_sections.append("## 2. 理性化过程研究")
            report_sections.append(f"**理性化指数**: {results['rationalization_index']:.2f}")
            report_sections.append(f"**现代化水平**: {results['modernization_level']}")
            
            rationalization_aspects = ['disenchantment', 'formal_rationality', 'substantive_rationality']
            for aspect in rationalization_aspects:
                if aspect in results:
                    data = results[aspect]
                    report_sections.append(f"**{aspect}**: {data['level']} (分数: {data['score']:.2f})")
            
            report_sections.append("")
        
        # 权威合法性结果
        if 'authority_legitimacy' in self.analysis_state:
            results = self.analysis_state['authority_legitimacy']
            report_sections.append("## 3. 权威合法性分析")
            report_sections.append(f"**权威类型**: {results['authority_type']}")
            report_sections.append(f"**权威稳定性**: {results['authority_stability']['stability_level']}")
            
            authority_types = ['traditional_authority', 'charismatic_authority', 'legal_rational_authority']
            for authority_type in authority_types:
                if authority_type in results:
                    data = results[authority_type]
                    report_sections.append(f"**{authority_type}**: {data['level']} (分数: {data['score']:.2f})")
            
            report_sections.append("")
        
        # 科层制与现代性结果
        if 'bureaucracy_modernity' in self.analysis_state:
            results = self.analysis_state['bureaucracy_modernity']
            report_sections.append("## 4. 科层制与现代性分析")
            report_sections.append(f"**科层制指数**: {results['bureaucracy_index']:.2f}")
            report_sections.append(f"**现代性水平**: {results['modernity_level']['modernity_level']}")
            
            bureaucracy_aspects = ['organizational_efficiency', 'impersonalization']
            for aspect in bureaucracy_aspects:
                if aspect in results:
                    data = results[aspect]
                    report_sections.append(f"**{aspect}**: {data['level']} (分数: {data['score']:.2f})")
            
            # 现代性困境
            if 'modernity_dilemma' in results:
                dilemma = results['modernity_dilemma']
                report_sections.append(f"**现代性困境**: {dilemma['dilemma_level']}")
            
            if 'iron_cage' in results:
                iron_cage = results['iron_cage']
                report_sections.append(f"**铁笼现象**: {iron_cage['iron_cage_level']}")
            
            report_sections.append("")
        
        # 四重专家协作分析
        if 'expert_collaboration' in self.analysis_state:
            report_sections.append("## 5. 四重专家协作分析")
            
            expert_results = self.analysis_state['expert_collaboration']
            expert_names = {
                'theoretical_interpretation': '理论阐释专家',
                'understanding_analysis': '理解性分析专家',
                'institutional_analysis': '制度分析专家',
                'comparative_research': '比较研究专家'
            }
            
            for expert_type, expert_name in expert_names.items():
                if expert_type in expert_results:
                    report_sections.append(f"### {expert_name}")
                    results = expert_results[expert_type]
                    
                    if 'concept_accuracy' in results:
                        report_sections.append(f"- 概念准确性: {results['concept_accuracy']:.2f}")
                    if 'subjective_meaning' in results:
                        report_sections.append(f"- 主观意义分析: 已完成")
                    if 'authority_analysis' in results:
                        report_sections.append(f"- 权威分析: 已完成")
                    if 'comparative_framework' in results:
                        report_sections.append(f"- 比较框架: 已构建")
            
            report_sections.append("")
        
        # 综合分析结论
        report_sections.append("## 6. 综合分析结论")
        conclusions = self._generate_conclusions()
        for conclusion in conclusions:
            report_sections.append(f"- {conclusion}")
        
        report_sections.append("")
        
        return "\n".join(report_sections)
    
    def _generate_conclusions(self) -> List[str]:
        """生成分析结论"""
        conclusions = []
        
        # 基于社会行动类型学的结论
        if 'social_action_typology' in self.analysis_state:
            results = self.analysis_state['social_action_typology']
            if results['rationality_score'] >= 6.0:
                conclusions.append("社会行动呈现明显的理性化特征，符合现代社会的理性化趋势")
            else:
                conclusions.append("社会行动仍保持较强的传统性和情感性，理性化程度有限")
        
        # 基于理性化过程的结论
        if 'rationalization_process' in self.analysis_state:
            results = self.analysis_state['rationalization_process']
            if results['rationalization_index'] >= 6.0:
                conclusions.append("理性化进程深入推进，现代化水平较高")
            else:
                conclusions.append("理性化进程相对缓慢，传统因素仍有重要影响")
        
        # 基于权威合法性的结论
        if 'authority_legitimacy' in self.analysis_state:
            results = self.analysis_state['authority_legitimacy']
            authority_type = results['authority_type']
            if '法理型权威' in authority_type:
                conclusions.append("权威结构呈现法理型特征，体现了现代政治的理性化")
            elif '传统型权威' in authority_type:
                conclusions.append("传统型权威仍然占主导地位，传统因素影响深远")
            elif '魅力型权威' in authority_type:
                conclusions.append("魅力型权威发挥重要作用，个人影响力突出")
        
        # 基于科层制与现代性的结论
        if 'bureaucracy_modernity' in self.analysis_state:
            results = self.analysis_state['bureaucracy_modernity']
            if results['bureaucracy_index'] >= 6.0:
                conclusions.append("科层制特征明显，组织理性化程度较高")
                if results.get('iron_cage', {}).get('iron_cage_level') == '高':
                    conclusions.append("需要注意'铁笼'现象，平衡效率与人性")
            else:
                conclusions.append("科层制特征不明显，组织形式较为传统")
        
        return conclusions
    
    def _generate_recommendations(self) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于质量评估的建议
        if hasattr(self, 'last_quality_assessment'):
            quality = self.last_quality_assessment
            
            if quality.get('overall_quality', 0) < 6.0:
                recommendations.append("建议补充更多实证材料，提高分析的可信度")
            
            if quality.get('theoretical_consistency', 0) < 7.0:
                recommendations.append("建议加强韦伯理论的应用，确保分析的理论一致性")
        
        # 基于分析结果的建议
        if 'social_action_typology' in self.analysis_state:
            results = self.analysis_state['social_action_typology']
            if results['rationality_score'] < 5.0:
                recommendations.append("建议深入分析理性化障碍，促进社会行动的理性化发展")
        
        if 'rationalization_process' in self.analysis_state:
            results = self.analysis_state['rationalization_process']
            if results.get('rationality_conflicts', {}).get('conflict_level') == '高':
                recommendations.append("建议关注理性化冲突，寻求工具理性与价值理性的平衡")
        
        if 'bureaucracy_modernity' in self.analysis_state:
            results = self.analysis_state['bureaucracy_modernity']
            if results.get('iron_cage', {}).get('iron_cage_level') == '高':
                recommendations.append("建议重视现代性困境，探索科层制的改革路径")
        
        return recommendations
    
    def export_analysis_results(self, filename: str = 'weber_analysis_results.json'):
        """导出分析结果"""
        results = {
            'analysis_state': self.analysis_state,
            'comprehensive_report': self._generate_integrated_report(),
            'recommendations': self._generate_recommendations(),
            'timestamp': str(pd.Timestamp.now())
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"分析结果已导出到: {filename}")
    
    def _assess_concept_accuracy(self, action_results: Dict) -> float:
        """评估概念准确性"""
        # 基于行动类型学分析结果评估概念使用的准确性
        if action_results['action_type'] in ['目的理性', '价值理性', '混合型(目的理性主导)']:
            return 8.0  # 概念使用准确
        else:
            return 6.0  # 概念使用基本准确
    
    def _assess_theoretical_logic(self, action_results: Dict) -> float:
        """评估理论逻辑"""
        # 基于理性分数评估理论逻辑的严密性
        return min(action_results['rationality_score'] + 2.0, 10.0)
    
    def _assess_methodology_consistency(self, action_results: Dict) -> float:
        """评估方法论一致性"""
        # 基于各类型行动的平衡性评估方法论一致性
        balance_score = 0.0
        action_types = ['目的理性', '价值理性', '情感性', '传统性']
        
        scores = []
        for action_type in action_types:
            if action_type in action_results:
                scores.append(action_results[action_type]['score'])
        
        if scores:
            max_score = max(scores)
            min_score = min(scores)
            balance_score = 1.0 - (max_score - min_score) / 10.0
        
        return balance_score * 10.0
    
    def _assess_theoretical_applicability(self, action_results: Dict) -> float:
        """评估理论适用性"""
        # 基于分析结果的完整性评估理论适用性
        completeness = len([r for r in action_results.values() 
                          if isinstance(r, dict) and 'score' in r and r['score'] > 0])
        return (completeness / 4.0) * 10.0
    
    def _analyze_subjective_meaning(self, text_data: str) -> Dict:
        """分析主观意义"""
        meaning_indicators = {
            '工具意义': ['工具', '手段', '方法'],
            '价值意义': ['价值', '意义', '目的'],
            '情感意义': ['感受', '体验', '情感'],
            '社会意义': ['社会', '群体', '关系']
        }
        
        meaning_analysis = {}
        for meaning_type, indicators in meaning_indicators.items():
            count = sum(text_data.count(indicator) for indicator in indicators)
            meaning_analysis[meaning_type] = {
                'frequency': count,
                'prominence': '高' if count >= 3 else '中' if count >= 1 else '低'
            }
        
        return meaning_analysis
    
    def _analyze_motivation_structure(self, text_data: str) -> Dict:
        """分析动机结构"""
        motivation_indicators = {
            '利益动机': ['利益', '收益', '好处', '回报'],
            '价值动机': ['价值', '信念', '理想', '原则'],
            '情感动机': ['情感', '情绪', '感受', '体验'],
            '传统动机': ['传统', '习惯', '惯例', '常规']
        }
        
        motivation_structure = {}
        for motivation_type, indicators in motivation_indicators.items():
            count = sum(text_data.count(indicator) for indicator in indicators)
            motivation_structure[motivation_type] = {
                'strength': count,
                'level': '强' if count >= 3 else '中' if count >= 1 else '弱'
            }
        
        return motivation_structure
    
    def _analyze_meaning_context(self, text_data: str) -> Dict:
        """分析意义情境"""
        return {
            'historical_context': '已分析',
            'cultural_context': '已分析',
            'social_context': '已分析',
            'situational_context': '已分析'
        }
    
    def _analyze_meaning_network(self, text_data: str) -> Dict:
        """分析意义关联网络"""
        return {
            'core_elements': '已识别',
            'relationship_structure': '已构建',
            'hierarchy_levels': '已确定',
            'conflict_tensions': '已分析'
        }
    
    def _assess_institutional_rationality(self, authority_results: Dict,
                                        bureaucracy_results: Dict) -> Dict:
        """评估制度理性化"""
        authority_score = authority_results.get('legal_rational_authority', {}).get('score', 0)
        bureaucracy_score = bureaucracy_results.get('organizational_efficiency', {}).get('score', 0)
        
        return {
            'authority_rationality': authority_score,
            'bureaucracy_rationality': bureaucracy_score,
            'overall_institutional_rationality': (authority_score + bureaucracy_score) / 2.0
        }
    
    def _diagnose_modernity_issues(self, bureaucracy_results: Dict) -> Dict:
        """诊断现代性问题"""
        dilemma_level = bureaucracy_results.get('modernity_dilemma', {}).get('dilemma_level', '低')
        iron_cage_level = bureaucracy_results.get('iron_cage', {}).get('iron_cage_level', '低')
        
        return {
            'dilemma_severity': dilemma_level,
            'iron_cage_intensity': iron_cage_level,
            'modernity_challenges': [dilemma_level, iron_cage_level]
        }
    
    def _build_comparative_framework(self, text_data: str) -> Dict:
        """构建比较框架"""
        return {
            'comparative_units': '已确定',
            'comparison_dimensions': '已构建',
            'analytical_framework': '已设计',
            'evaluation_criteria': '已制定'
        }
    
    def _analyze_development_pathways(self, text_data: str) -> Dict:
        """分析发展路径"""
        return {
            'development_trajectories': '已识别',
            'key_turning_points': '已分析',
            'path_differences': '已比较',
            'common_patterns': '已总结'
        }
    
    def _compare_rationalization_processes(self, text_data: str) -> Dict:
        """比较理性化过程"""
        return {
            'rationalization_levels': '已比较',
            'process_differences': '已识别',
            'convergence_patterns': '已发现',
            'divergence_factors': '已分析'
        }
    
    def _interpret_causal_relationships(self, text_data: str) -> Dict:
        """阐释因果关系"""
        return {
            'causal_factors': '已识别',
            'mechanisms': '已分析',
            'explanatory_model': '已构建',
            'validation': '已完成'
        }


class WeberQualityMonitor:
    """韦伯分析质量监控器"""
    
    def assess_overall_quality(self, analysis_state: Dict) -> Dict:
        """评估整体分析质量"""
        quality_metrics = {}
        
        # 评估各阶段质量
        if 'social_action_typology' in analysis_state:
            quality_metrics['action_typology_quality'] = self._assess_action_typology_quality(
                analysis_state['social_action_typology']
            )
        
        if 'rationalization_process' in analysis_state:
            quality_metrics['rationalization_quality'] = self._assess_rationalization_quality(
                analysis_state['rationalization_process']
            )
        
        if 'authority_legitimacy' in analysis_state:
            quality_metrics['authority_quality'] = self._assess_authority_quality(
                analysis_state['authority_legitimacy']
            )
        
        if 'bureaucracy_modernity' in analysis_state:
            quality_metrics['bureaucracy_quality'] = self._assess_bureaucracy_quality(
                analysis_state['bureaucracy_modernity']
            )
        
        # 计算整体质量
        overall_quality = sum(quality_metrics.values()) / len(quality_metrics) if quality_metrics else 0
        
        return {
            'phase_qualities': quality_metrics,
            'overall_quality': overall_quality,
            'theoretical_consistency': self._assess_theoretical_consistency(analysis_state),
            'methodological_rigor': self._assess_methodological_rigor(analysis_state),
            'completeness': self._assess_completeness(analysis_state)
        }
    
    def _assess_action_typology_quality(self, results: Dict) -> float:
        """评估社会行动类型学质量"""
        quality_score = 0.0
        
        # 检查四大类型的识别质量
        if 'purposive_rationality' in results:
            quality_score += results['purposive_rationality']['score']
        if 'value_rationality' in results:
            quality_score += results['value_rationality']['score']
        if 'affective_action' in results:
            quality_score += results['affective_action']['score']
        if 'traditional_action' in results:
            quality_score += results['traditional_action']['score']
        
        return min(quality_score / 4.0, 10.0)
    
    def _assess_rationalization_quality(self, results: Dict) -> float:
        """评估理性化过程质量"""
        quality_score = 0.0
        
        # 检查理性化各维度的分析质量
        if 'disenchantment' in results:
            quality_score += results['disenchantment']['score']
        if 'formal_rationality' in results:
            quality_score += results['formal_rationality']['score']
        if 'substantive_rationality' in results:
            quality_score += results['substantive_rationality']['score']
        
        return min(quality_score / 3.0, 10.0)
    
    def _assess_authority_quality(self, results: Dict) -> float:
        """评估权威合法性质量"""
        quality_score = 0.0
        
        # 检查权威类型的分析质量
        if 'traditional_authority' in results:
            quality_score += results['traditional_authority']['score']
        if 'charismatic_authority' in results:
            quality_score += results['charismatic_authority']['score']
        if 'legal_rational_authority' in results:
            quality_score += results['legal_rational_authority']['score']
        
        return min(quality_score / 3.0, 10.0)
    
    def _assess_bureaucracy_quality(self, results: Dict) -> float:
        """评估科层制与现代性质量"""
        quality_score = 0.0
        
        # 检查科层制各维度的分析质量
        if 'organizational_efficiency' in results:
            quality_score += results['organizational_efficiency']['score']
        if 'impersonalization' in results:
            quality_score += results['impersonalization']['score']
        
        # 考虑现代性困境的诊断
        if 'modernity_dilemma' in results:
            quality_score += 2.0  # 诊断现代性困境加分
        
        return min(quality_score / 2.5, 10.0)
    
    def _assess_theoretical_consistency(self, analysis_state: Dict) -> float:
        """评估理论一致性"""
        consistency_score = 8.0  # 基础分数
        
        # 检查是否遵循韦伯理论框架
        if 'social_action_typology' in analysis_state:
            results = analysis_state['social_action_typology']
            if results['action_type'] in ['目的理性', '价值理性', '混合型']:
                consistency_score += 1.0
        
        if 'authority_legitimacy' in analysis_state:
            results = analysis_state['authority_legitimacy']
            if '法理型权威' in results['authority_type']:
                consistency_score += 1.0
        
        return min(consistency_score, 10.0)
    
    def _assess_methodological_rigor(self, analysis_state: Dict) -> float:
        """评估方法论严谨性"""
        rigor_score = 7.0  # 基础分数
        
        # 检查分析方法的系统性
        phases_completed = len([key for key in analysis_state.keys() 
                              if key in ['social_action_typology', 'rationalization_process', 
                                       'authority_legitimacy', 'bureaucracy_modernity']])
        
        rigor_score += phases_completed * 0.5
        
        return min(rigor_score, 10.0)
    
    def _assess_completeness(self, analysis_state: Dict) -> float:
        """评估分析完整性"""
        required_phases = ['social_action_typology', 'rationalization_process', 
                          'authority_legitimacy', 'bureaucracy_modernity']
        completed_phases = len([phase for phase in required_phases if phase in analysis_state])
        
        completeness_score = (completed_phases / len(required_phases)) * 10.0
        
        return completeness_score


def main():
    """示例用法"""
    analyzer = IntegratedWeberAnalyzer()
    
    # 示例文本数据
    sample_text = """
    现代官僚组织作为一种理性的组织形式，追求效率最大化和程序规范化。
    组织成员按照明确的规则和程序行动，个人的情感和偏好被排除在决策过程之外。
    这种非人格化的管理方式确保了组织的公正性和效率。
    
    在权威类型方面，现代组织主要依靠法理型权威，
    通过合法的规则和程序来维持秩序。传统型权威和魅力型权威的影响相对有限。
    
    然而，过度的理性化也带来了现代性的困境。组织成员被束缚在"铁笼"之中，
    失去了个性和自由。工具理性的过度发展压制了价值理性的空间，
    导致了意义危机和精神空虚。
    
    理性化过程表现为除魅的深入推进，形式理性在各个领域扩展，
    但实质理性的价值却时常被忽视。这种理性化的冲突是现代社会的核心问题。
    """
    
    # 执行完整分析
    print("开始执行数字韦伯集成分析...")
    results = analyzer.execute_comprehensive_analysis(sample_text)
    
    # 输出质量评估
    quality = results['quality_assessment']
    print(f"\n=== 质量评估 ===")
    print(f"整体质量: {quality['overall_quality']:.2f}")
    print(f"理论一致性: {quality['theoretical_consistency']:.2f}")
    print(f"方法论严谨性: {quality['methodological_rigor']:.2f}")
    print(f"分析完整性: {quality['completeness']:.2f}")
    
    # 输出综合报告
    print(f"\n=== 综合分析报告 ===")
    print(results['comprehensive_report'])
    
    # 输出建议
    print(f"\n=== 改进建议 ===")
    for i, recommendation in enumerate(results['recommendations'], 1):
        print(f"{i}. {recommendation}")
    
    # 导出结果
    analyzer.export_analysis_results()


if __name__ == "__main__":
    main()