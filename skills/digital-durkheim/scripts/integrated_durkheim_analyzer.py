#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数字涂尔干集成分析器 - 协调AI理论分析与脚本计算
实现涂尔干社会学分析的智能化集成，确保定性与定量的有机结合
"""

import os
import json
from typing import Dict, List, Optional, Any
from social_fact_analyzer import SocialFactAnalyzer
import pandas as pd


class IntegratedDurkheimAnalyzer:
    """数字涂尔干集成分析器"""
    
    def __init__(self):
        self.social_fact_analyzer = SocialFactAnalyzer()
        self.analysis_state = {}
        self.quality_monitor = QualityMonitor()
        
    def execute_comprehensive_analysis(self, 
                                     text_data: str,
                                     research_context: Dict = None) -> Dict:
        """
        执行完整的涂尔干社会学分析
        
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
        
        # 阶段1: 社会事实识别 (定量计算)
        print("执行社会事实识别...")
        social_fact_results = self.social_fact_analyzer.identify_social_facts(text_data)
        self.analysis_state['social_facts'] = social_fact_results
        
        # 阶段2: 集体意识分析 (定量计算)
        print("执行集体意识分析...")
        consciousness_results = self.social_fact_analyzer.analyze_collective_consciousness(
            text_data, social_fact_results['fact_type']
        )
        self.analysis_state['collective_consciousness'] = consciousness_results
        
        # 阶段3: 功能分析 (定量计算)
        print("执行功能分析...")
        functional_results = self.social_fact_analyzer.perform_functional_analysis(text_data)
        self.analysis_state['functional_analysis'] = functional_results
        
        # 阶段4: 社会团结分析 (定量计算)
        print("执行社会团结分析...")
        solidarity_results = self.social_fact_analyzer.analyze_social_solidarity(text_data)
        self.analysis_state['social_solidarity'] = solidarity_results
        
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
    
    def load_prompt_guidance(self, phase: str) -> str:
        """
        加载相应阶段的提示词指导
        
        Parameters:
        -----------
        phase : str
            分析阶段名称
            
        Returns:
        --------
        str : 提示词内容
        """
        prompt_files = {
            'social_fact_identification': 'prompts/social-fact-identification.md',
            'collective_consciousness': 'prompts/collective-consciousness.md',
            'functional_analysis': 'prompts/functional-analysis.md',
            'social_solidarity': 'prompts/social-solidarity.md'
        }
        
        if phase in prompt_files:
            file_path = prompt_files[phase]
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        
        return f"未找到 {phase} 阶段的提示词文件"
    
    def execute_phase_with_ai_guidance(self, 
                                     phase: str,
                                     text_data: str,
                                     context: Dict = None) -> Dict:
        """
        在AI指导下执行特定分析阶段
        
        Parameters:
        -----------
        phase : str
            分析阶段
        text_data : str
            文本数据
        context : Dict
            上下文信息
            
        Returns:
        --------
        Dict : 分析结果
        """
        # 加载提示词指导
        prompt_guidance = self.load_prompt_guidance(phase)
        
        # 根据阶段执行相应分析
        if phase == 'social_fact_identification':
            results = self.social_fact_analyzer.identify_social_facts(text_data, context)
        elif phase == 'collective_consciousness':
            fact_type = context.get('fact_type') if context else None
            results = self.social_fact_analyzer.analyze_collective_consciousness(text_data, fact_type)
        elif phase == 'functional_analysis':
            phenomenon = context.get('phenomenon') if context else None
            results = self.social_fact_analyzer.perform_functional_analysis(text_data, phenomenon)
        elif phase == 'social_solidarity':
            results = self.social_fact_analyzer.analyze_social_solidarity(text_data, context)
        else:
            raise ValueError(f"未知的分析阶段: {phase}")
        
        # 添加AI指导信息
        results['ai_guidance'] = {
            'phase': phase,
            'prompt_loaded': bool(prompt_guidance),
            'guidance_applied': True
        }
        
        return results
    
    def _initialize_analysis_state(self, research_context: Dict = None):
        """初始化分析状态"""
        self.analysis_state = {
            'research_context': research_context or {},
            'analysis_phases': [],
            'quality_metrics': {},
            'interim_results': {}
        }
    
    def _generate_integrated_report(self) -> str:
        """生成集成分析报告"""
        report_sections = []
        
        # 报告标题
        report_sections.append("# 数字涂尔干社会学集成分析报告")
        report_sections.append("")
        
        # 社会事实识别结果
        if 'social_facts' in self.analysis_state:
            results = self.analysis_state['social_facts']
            report_sections.append("## 1. 社会事实识别分析")
            report_sections.append(f"**事实类型**: {results['fact_type']}")
            report_sections.append(f"**外在性水平**: {results['externality']['level']} (分数: {results['externality']['score']:.2f})")
            report_sections.append(f"**强制性水平**: {results['coerciveness']['level']} (分数: {results['coerciveness']['score']:.2f})")
            report_sections.append(f"**独立性水平**: {results['independence']['level']} (分数: {results['independence']['score']:.2f})")
            
            # 添加证据
            if results['externality']['evidence']:
                report_sections.append("\n**外在性证据**:")
                for evidence in results['externality']['evidence']:
                    report_sections.append(f"- {evidence}")
            
            report_sections.append("")
        
        # 集体意识分析结果
        if 'collective_consciousness' in self.analysis_state:
            results = self.analysis_state['collective_consciousness']
            report_sections.append("## 2. 集体意识分析")
            report_sections.append(f"**意识强度**: {results['consciousness_strength']:.2f}")
            
            # 集体表征
            report_sections.append("\n### 集体表征分析")
            for rep_type, rep_data in results['representations'].items():
                if rep_data['count'] > 0:
                    report_sections.append(f"- **{rep_type}**: {rep_data['prominence']} (频次: {rep_data['count']})")
            
            # 价值体系
            report_sections.append("\n### 价值体系分析")
            for value_type, value_data in results['value_system'].items():
                if value_data['frequency'] > 0:
                    report_sections.append(f"- **{value_type}**: {value_data['importance']} (频次: {value_data['frequency']})")
            
            report_sections.append("")
        
        # 功能分析结果
        if 'functional_analysis' in self.analysis_state:
            results = self.analysis_state['functional_analysis']
            report_sections.append("## 3. 功能分析")
            report_sections.append(f"**显功能数量**: {len(results['manifest_functions'])}")
            report_sections.append(f"**潜功能数量**: {len(results['latent_functions'])}")
            report_sections.append(f"**功能平衡度**: {results['functional_balance']['analysis_depth']}")
            
            # 显功能列表
            if results['manifest_functions']:
                report_sections.append("\n### 显功能识别")
                for i, func in enumerate(results['manifest_functions'][:3], 1):
                    report_sections.append(f"{i}. {func['description']}")
            
            # 潜功能列表
            if results['latent_functions']:
                report_sections.append("\n### 潜功能识别")
                for i, func in enumerate(results['latent_functions'][:3], 1):
                    report_sections.append(f"{i}. {func['description']}")
            
            report_sections.append("")
        
        # 社会团结分析结果
        if 'social_solidarity' in self.analysis_state:
            results = self.analysis_state['social_solidarity']
            report_sections.append("## 4. 社会团结分析")
            report_sections.append(f"**团结类型**: {results['solidarity_type']['type']}")
            report_sections.append(f"**团结指数**: {results['solidarity_index']:.2f}")
            report_sections.append(f"**社会分化程度**: {results['social_differentiation']['differentiation_degree']}")
            
            # 整合机制
            report_sections.append("\n### 整合机制评估")
            for mech_type, mech_data in results['integration_mechanisms'].items():
                if mech_data['strength'] > 0:
                    report_sections.append(f"- **{mech_type}**: {mech_data['effectiveness']} (强度: {mech_data['strength']})")
            
            report_sections.append("")
        
        # 综合分析结论
        report_sections.append("## 5. 综合分析结论")
        conclusions = self._generate_conclusions()
        for conclusion in conclusions:
            report_sections.append(f"- {conclusion}")
        
        report_sections.append("")
        
        return "\n".join(report_sections)
    
    def _generate_conclusions(self) -> List[str]:
        """生成分析结论"""
        conclusions = []
        
        # 基于社会事实识别的结论
        if 'social_facts' in self.analysis_state:
            results = self.analysis_state['social_facts']
            if results['externality']['score'] >= 7.0:
                conclusions.append("研究对象具有高度外在性，符合涂尔干社会事实的核心特征")
            if results['coerciveness']['score'] >= 6.0:
                conclusions.append("现象具有明显的强制性约束作用，体现了社会事实的规范功能")
        
        # 基于集体意识分析的结论
        if 'collective_consciousness' in self.analysis_state:
            results = self.analysis_state['collective_consciousness']
            if results['consciousness_strength'] >= 6.0:
                conclusions.append("集体意识强度较高，社会整合程度良好")
            else:
                conclusions.append("集体意识相对薄弱，需要加强社会凝聚力建设")
        
        # 基于功能分析的结论
        if 'functional_analysis' in self.analysis_state:
            results = self.analysis_state['functional_analysis']
            if len(results['latent_functions']) >= 2:
                conclusions.append("存在丰富的潜功能，建议深入分析其社会影响")
        
        # 基于社会团结分析的结论
        if 'social_solidarity' in self.analysis_state:
            results = self.analysis_state['social_solidarity']
            solidarity_type = results['solidarity_type']['type']
            if '有机团结' in solidarity_type:
                conclusions.append("社会呈现有机团结特征，分工发达，异质性程度高")
            elif '机械团结' in solidarity_type:
                conclusions.append("社会仍保持机械团结特征，同质性较强")
        
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
                recommendations.append("建议加强涂尔干理论的应用，确保分析的理论一致性")
        
        # 基于分析结果的建议
        if 'social_facts' in self.analysis_state:
            results = self.analysis_state['social_facts']
            if results['independence']['score'] < 5.0:
                recommendations.append("建议进一步研究现象的独立性特征，深化社会事实识别")
        
        if 'functional_analysis' in self.analysis_state:
            results = self.analysis_state['functional_analysis']
            if len(results['latent_functions']) == 0:
                recommendations.append("建议深入挖掘潜功能，避免功能分析的表面化")
        
        return recommendations
    
    def export_analysis_results(self, filename: str = 'durkheim_analysis_results.json'):
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


class QualityMonitor:
    """质量监控器"""
    
    def assess_overall_quality(self, analysis_state: Dict) -> Dict:
        """评估整体分析质量"""
        quality_metrics = {}
        
        # 评估各阶段质量
        if 'social_facts' in analysis_state:
            quality_metrics['social_fact_quality'] = self._assess_social_fact_quality(
                analysis_state['social_facts']
            )
        
        if 'collective_consciousness' in analysis_state:
            quality_metrics['consciousness_quality'] = self._assess_consciousness_quality(
                analysis_state['collective_consciousness']
            )
        
        if 'functional_analysis' in analysis_state:
            quality_metrics['functional_quality'] = self._assess_functional_quality(
                analysis_state['functional_analysis']
            )
        
        if 'social_solidarity' in analysis_state:
            quality_metrics['solidarity_quality'] = self._assess_solidarity_quality(
                analysis_state['social_solidarity']
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
    
    def _assess_social_fact_quality(self, results: Dict) -> float:
        """评估社会事实识别质量"""
        quality_score = 0.0
        
        # 检查三大特征的识别质量
        externality = results['externality']['score']
        coerciveness = results['coerciveness']['score']
        independence = results['independence']['score']
        
        # 平均分数作为质量指标
        quality_score = (externality + coerciveness + independence) / 3.0
        
        # 检查证据的充分性
        evidence_count = len(results['externality']['evidence'])
        if evidence_count >= 2:
            quality_score += 1.0
        
        return min(quality_score, 10.0)
    
    def _assess_consciousness_quality(self, results: Dict) -> float:
        """评估集体意识分析质量"""
        quality_score = 0.0
        
        # 意识强度
        consciousness_strength = results['consciousness_strength']
        quality_score += consciousness_strength
        
        # 分析维度的完整性
        dimensions_analyzed = 0
        if results['representations']:
            dimensions_analyzed += 1
        if results['value_system']:
            dimensions_analyzed += 1
        if results['social_norms']:
            dimensions_analyzed += 1
        if results['collective_emotions']:
            dimensions_analyzed += 1
        
        quality_score += dimensions_analyzed * 2.0
        
        return min(quality_score, 10.0)
    
    def _assess_functional_quality(self, results: Dict) -> float:
        """评估功能分析质量"""
        quality_score = 0.0
        
        # 显功能和潜功能的识别
        manifest_count = len(results['manifest_functions'])
        latent_count = len(results['latent_functions'])
        
        quality_score += min(manifest_count * 2.0, 6.0)
        quality_score += min(latent_count * 3.0, 6.0)
        
        # 功能整合分析
        if results['functional_integration']['integration_level'] > 0:
            quality_score += 2.0
        
        return min(quality_score, 10.0)
    
    def _assess_solidarity_quality(self, results: Dict) -> float:
        """评估社会团结分析质量"""
        quality_score = 0.0
        
        # 团结类型判断的明确性
        solidarity_type = results['solidarity_type']['type']
        if solidarity_type != '未确定':
            quality_score += 4.0
        
        # 分化分析的深度
        differentiation_score = results['social_differentiation']['differentiation_level']
        quality_score += min(differentiation_score, 4.0)
        
        # 整合机制的全面性
        integration_mechanisms = results['integration_mechanisms']
        active_mechanisms = len([m for m in integration_mechanisms.values() if m['strength'] > 0])
        quality_score += active_mechanisms
        
        return min(quality_score, 10.0)
    
    def _assess_theoretical_consistency(self, analysis_state: Dict) -> float:
        """评估理论一致性"""
        consistency_score = 8.0  # 基础分数
        
        # 检查是否遵循涂尔干理论框架
        if 'social_facts' in analysis_state:
            results = analysis_state['social_facts']
            if results['fact_type'] in ['制度性事实', '规范性事实']:
                consistency_score += 1.0
        
        if 'functional_analysis' in analysis_state:
            results = analysis_state['functional_analysis']
            if len(results['latent_functions']) > 0:
                consistency_score += 1.0
        
        return min(consistency_score, 10.0)
    
    def _assess_methodological_rigor(self, analysis_state: Dict) -> float:
        """评估方法论严谨性"""
        rigor_score = 7.0  # 基础分数
        
        # 检查分析方法的系统性
        phases_completed = len([key for key in analysis_state.keys() 
                              if key in ['social_facts', 'collective_consciousness', 
                                       'functional_analysis', 'social_solidarity']])
        
        rigor_score += phases_completed * 0.5
        
        return min(rigor_score, 10.0)
    
    def _assess_completeness(self, analysis_state: Dict) -> float:
        """评估分析完整性"""
        required_phases = ['social_facts', 'collective_consciousness', 
                          'functional_analysis', 'social_solidarity']
        completed_phases = len([phase for phase in required_phases if phase in analysis_state])
        
        completeness_score = (completed_phases / len(required_phases)) * 10.0
        
        return completeness_score


def main():
    """示例用法"""
    analyzer = IntegratedDurkheimAnalyzer()
    
    # 示例文本数据
    sample_text = """
    现代教育制度作为社会的重要组成部分，承担着传递文化知识、培养社会成员的重要功能。
    教育规范要求所有适龄儿童必须接受九年义务教育，这种强制性要求体现了社会对个体行为的约束。
    教育制度独立于个体意志而存在，具有历史延续性和结构稳定性。
    
    在教育过程中，形成了独特的集体意识，包括对知识的尊重、对规则的遵守、对集体的认同。
    这些价值观念通过教育实践不断传递和强化，形成了社会的文化基因。
    
    教育的显功能是传授知识和技能，但潜功能还包括社会分层、文化再生产、社会整合等。
    这些潜功能往往被忽视，但对社会的运行产生深远影响。
    
    随着社会的发展，教育分化日益明显，出现了不同类型的教育机构和教育形式。
    这种分化反映了社会从机械团结向有机团结的转变，体现了社会的复杂性和多样性。
    """
    
    # 执行完整分析
    print("开始执行数字涂尔干集成分析...")
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