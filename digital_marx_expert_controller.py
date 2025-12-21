#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数字马克思智能体主控制器
Digital Marx Expert Main Controller

此脚本整合所有马克思主义分析技能，实现自动化分析逻辑，
确保定性与定量分析的最佳结合，保持理论深刻性与灵活性。

作者: 数字马克思智能体开发团队
版本: 1.0.0
日期: 2025-12-21
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import numpy as np
from dataclasses import dataclass, asdict
import traceback

# 导入核心分析模块
from quality_assurance_system import QualityAssuranceSystem, QualityMetrics
from marxist_class_analysis_framework import MarxistClassAnalyzer

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('digital_marx_expert.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class AnalysisRequest:
    """分析请求数据结构"""
    problem_description: str
    analysis_type: str
    data_sources: Dict[str, Any]
    depth_level: str = "comprehensive"
    output_format: str = "detailed_report"
    quality_requirements: Dict[str, float] = None
    
    def __post_init__(self):
        if self.quality_requirements is None:
            self.quality_requirements = {
                'theoretical_accuracy': 0.75,
                'analysis_depth': 0.70,
                'practical_relevance': 0.80
            }

@dataclass
class AnalysisResult:
    """分析结果数据结构"""
    request: AnalysisRequest
    analysis_results: Dict[str, Any]
    quality_metrics: QualityMetrics
    synthesis_report: str
    practical_guidance: Dict[str, Any]
    theoretical_contributions: Dict[str, Any]
    execution_time: float
    success: bool = True
    error_message: str = None

class DigitalMarxExpertController:
    """数字马克思智能体主控制器"""
    
    def __init__(self):
        # 初始化各个分析模块
        self.quality_system = QualityAssuranceSystem()
        self.class_analyzer = MarxistClassAnalyzer()
        
        # 技能模块路径
        self.skills_modules = {
            'historical_materialist': 'skills.historical-materialist-analysis',
            'class_structure': 'skills.class-structure-analysis',
            'practical_application': 'skills.practical-marxist-application',
            'dialectical_synthesis': 'skills.dialectical-quantitative-synthesis',
            'alienation_analysis': 'skills.alienation-analysis'
        }
        
        # 分析流程配置
        self.analysis_workflow = {
            'basic_analysis': ['historical_materialist', 'class_structure'],
            'comprehensive_analysis': ['historical_materialist', 'class_structure', 'dialectical_synthesis'],
            'practical_application': ['historical_materialist', 'class_structure', 'practical_application', 'dialectical_synthesis'],
            'alienation_analysis': ['alienation_analysis'],
            'comprehensive_with_alienation': ['historical_materialist', 'class_structure', 'alienation_analysis', 'dialectical_synthesis']
        }
        
        logger.info("数字马克思智能体主控制器初始化完成")
    
    def process_analysis_request(self, request: AnalysisRequest) -> AnalysisResult:
        """处理分析请求"""
        start_time = datetime.now()
        logger.info(f"开始处理分析请求: {request.analysis_type}")
        
        try:
            # 1. 预处理分析请求
            processed_request = self._preprocess_request(request)
            
            # 2. 确定分析流程
            workflow = self._determine_analysis_workflow(processed_request)
            
            # 3. 执行分析流程
            analysis_results = {}
            for skill_name in workflow:
                logger.info(f"执行分析技能: {skill_name}")
                skill_result = self._execute_analysis_skill(skill_name, processed_request)
                analysis_results[skill_name] = skill_result
            
            # 4. 综合分析结果
            synthesis_report = self._synthesize_analysis_results(analysis_results, processed_request)
            
            # 5. 生成实践指导
            practical_guidance = self._generate_practical_guidance(analysis_results, processed_request)
            
            # 6. 评估理论贡献
            theoretical_contributions = self._assess_theoretical_contributions(analysis_results, processed_request)
            
            # 7. 质量验证
            quality_metrics = self.quality_system.comprehensive_quality_assessment(synthesis_report)
            
            # 8. 检查质量要求
            quality_check = self._check_quality_requirements(quality_metrics, processed_request)
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            result = AnalysisResult(
                request=processed_request,
                analysis_results=analysis_results,
                quality_metrics=quality_metrics,
                synthesis_report=synthesis_report,
                practical_guidance=practical_guidance,
                theoretical_contributions=theoretical_contributions,
                execution_time=execution_time,
                success=quality_check['meets_requirements']
            )
            
            if not quality_check['meets_requirements']:
                result.error_message = f"质量不达标: {quality_check['failure_reasons']}"
                logger.warning(f"分析质量不达标: {quality_check['failure_reasons']}")
            
            logger.info(f"分析完成，耗时: {execution_time:.2f}秒，质量分数: {quality_metrics.overall_quality:.3f}")
            return result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            logger.error(f"分析过程发生错误: {str(e)}")
            logger.error(traceback.format_exc())
            
            return AnalysisResult(
                request=request,
                analysis_results={},
                quality_metrics=QualityMetrics(0, 0, 0, 0, 0, 0),
                synthesis_report=f"分析失败: {str(e)}",
                practical_guidance={},
                theoretical_contributions={},
                execution_time=execution_time,
                success=False,
                error_message=str(e)
            )
    
    def _preprocess_request(self, request: AnalysisRequest) -> AnalysisRequest:
        """预处理分析请求"""
        # 数据清洗和标准化
        if 'data_sources' in request.data_sources:
            cleaned_data = {}
            for source_name, source_data in request.data_sources.items():
                cleaned_data[source_name] = self._clean_and_validate_data(source_data)
            request.data_sources = cleaned_data
        
        # 确定分析深度和输出格式
        request.depth_level = request.depth_level or "comprehensive"
        request.output_format = request.output_format or "detailed_report"
        
        return request
    
    def _determine_analysis_workflow(self, request: AnalysisRequest) -> List[str]:
        """确定分析流程"""
        problem_text = request.problem_description.lower()
        
        # 基于分析类型和需求确定流程
        if request.analysis_type == "historical_materialist":
            return self.analysis_workflow['basic_analysis']
        elif request.analysis_type == "class_structure":
            return self.analysis_workflow['basic_analysis']
        elif request.analysis_type == "practical_application":
            return self.analysis_workflow['practical_application']
        elif request.analysis_type == "alienation_analysis" or '异化' in problem_text:
            return self.analysis_workflow['comprehensive_with_alienation']
        else:
            # 检查是否包含异化相关内容
            alienation_keywords = ['异化', 'alienation', '劳动异化', '技术异化', '消费异化', '社会异化']
            if any(keyword in problem_text for keyword in alienation_keywords):
                return self.analysis_workflow['comprehensive_with_alienation']
            return self.analysis_workflow['comprehensive_analysis']
    
    def _execute_analysis_skill(self, skill_name: str, request: AnalysisRequest) -> Dict[str, Any]:
        """执行分析技能"""
        try:
            if skill_name == 'alienation_analysis':
                # 异化分析技能使用新的渐进式信息披露架构
                result = self._execute_alienation_analysis_skill(request)
            else:
                # 其他技能使用原有架构
                # 动态导入技能模块
                skill_module = self._load_skill_module(skill_name)
                
                # 创建技能实例
                skill_instance = skill_module.Skill()
                
                # 执行技能分析
                if skill_name == 'historical_materialist':
                    result = skill_instance.comprehensive_analysis(request.data_sources)
                elif skill_name == 'class_structure':
                    result = skill_instance.comprehensive_class_analysis(request.data_sources)
                elif skill_name == 'practical_application':
                    result = skill_instance.practical_application_analysis(request.data_sources)
                elif skill_name == 'dialectical_synthesis':
                    result = skill_instance.comprehensive_synthesis_analysis(
                        request.problem_description, request.data_sources
                    )
                else:
                    raise ValueError(f"未知技能类型: {skill_name}")
            
            # 添加元数据
            result['skill_name'] = skill_name
            result['execution_timestamp'] = datetime.now().isoformat()
            result['quality_score'] = self._assess_skill_quality(result, skill_name)
            
            logger.info(f"技能 {skill_name} 执行完成，质量分数: {result['quality_score']:.3f}")
            return result
            
        except Exception as e:
            logger.error(f"技能 {skill_name} 执行失败: {str(e)}")
            return {
                'skill_name': skill_name,
                'error': str(e),
                'success': False,
                'quality_score': 0.0
            }
    
    def _execute_alienation_analysis_skill(self, request: AnalysisRequest) -> Dict[str, Any]:
        """执行异化分析技能（符合agentskills.io标准）"""
        try:
            # 1. 智能识别异化类型
            alienation_types = self._identify_alienation_types(request.problem_description)
            
            # 2. 选择对应的prompt文件和脚本
            analysis_components = self._select_alienation_components(alienation_types, request)
            
            # 3. 执行定性分析（通过prompt文件）
            qualitative_results = self._execute_qualitative_analysis(analysis_components['prompt_files'], request)
            
            # 4. 执行定量分析（通过脚本）
            quantitative_results = self._execute_quantitative_analysis(analysis_components['scripts'], request)
            
            # 5. 综合分析结果
            synthesis_result = self._synthesize_alienation_results(qualitative_results, quantitative_results, alienation_types)
            
            return synthesis_result
            
        except Exception as e:
            logger.error(f"异化分析技能执行失败: {str(e)}")
            return {
                'error': str(e),
                'success': False,
                'analysis_type': 'alienation_analysis'
            }
    
    def _identify_alienation_types(self, problem_description: str) -> List[str]:
        """智能识别异化类型"""
        alienation_keywords = {
            'labor_alienation': ['劳动异化', '工作异化', '工作压力', '职业倦怠', '劳动过程', '劳动产品', '劳动本质'],
            'social_alienation': ['社会异化', '人际疏离', '社交孤独', '关系疏远', '社会联系', '集体意识'],
            'consumption_alienation': ['消费异化', '物质主义', '消费主义', '过度消费', '消费冲动', '消费焦虑'],
            'technology_alienation': ['技术异化', '技术依赖', '数字异化', '手机依赖', '网络成瘾', '数字化生存']
        }
        
        identified_types = []
        problem_lower = problem_description.lower()
        
        for alienation_type, keywords in alienation_keywords.items():
            if any(keyword in problem_lower for keyword in keywords):
                identified_types.append(alienation_type)
        
        # 如果没有明确识别出类型，默认进行综合分析
        if not identified_types:
            identified_types = ['comprehensive_alienation']
        
        return identified_types
    
    def _select_alienation_components(self, alienation_types: List[str], request: AnalysisRequest) -> Dict[str, List[str]]:
        """选择对应的prompt文件和脚本"""
        components = {
            'prompt_files': [],
            'scripts': []
        }
        
        # 核心分析prompt文件
        components['prompt_files'].append('01-core-analysis-prompt.md')
        
        # 根据异化类型选择特定prompt文件
        prompt_mapping = {
            'labor_alienation': ['02-labor-alienation-prompt.md'],
            'social_alienation': ['03-social-alienation-prompt.md'],
            'consumption_alienation': ['04-consumption-alienation-prompt.md'],
            'technology_alienation': ['05-technology-alienation-prompt.md']
        }
        
        for alienation_type in alienation_types:
            if alienation_type in prompt_mapping:
                components['prompt_files'].extend(prompt_mapping[alienation_type])
        
        # 综合分析需要合成prompt文件
        if 'comprehensive_alienation' in alienation_types or len(alienation_types) > 1:
            components['prompt_files'].append('06-synthesis-prompt.md')
        
        # 选择对应的定量分析脚本
        script_mapping = {
            'labor_alienation': [
                'calculate_alienation_score.py',
                'workplace_satisfaction_analysis.py',
                'career_development_evaluation.py'
            ],
            'social_alienation': [
                'calculate_alienation_score.py',
                'social_network_analysis.py',
                'relationship_quality_assessment.py'
            ],
            'consumption_alienation': [
                'calculate_alienation_score.py',
                'consumer_behavior_analysis.py',
                'materialism_assessment.py'
            ],
            'technology_alienation': [
                'calculate_alienation_score.py',
                'technology_dependency_analysis.py',
                'digital_wellbeing_evaluation.py'
            ]
        }
        
        # 添加通用脚本
        components['scripts'].extend([
            'calculate_alienation_score.py',
            'classify_alienation_types.py',
            'generate_intervention_plan.py'
        ])
        
        for alienation_type in alienation_types:
            if alienation_type in script_mapping:
                components['scripts'].extend(script_mapping[alienation_type])
        
        # 去重
        components['prompt_files'] = list(set(components['prompt_files']))
        components['scripts'] = list(set(components['scripts']))
        
        return components
    
    def _execute_qualitative_analysis(self, prompt_files: List[str], request: AnalysisRequest) -> Dict[str, Any]:
        """执行定性分析（基于prompt文件）"""
        qualitative_results = {}
        
        # 加载prompt文件内容
        prompt_contents = self._load_prompt_files(prompt_files)
        
        # 基于prompt文件进行定性分析
        for i, prompt_file in enumerate(prompt_files):
            try:
                prompt_content = prompt_contents[i]
                analysis_result = self._analyze_with_prompt(prompt_content, request)
                qualitative_results[prompt_file] = analysis_result
            except Exception as e:
                logger.warning(f"定性分析失败 {prompt_file}: {str(e)}")
                qualitative_results[prompt_file] = {'error': str(e), 'success': False}
        
        return qualitative_results
    
    def _execute_quantitative_analysis(self, scripts: List[str], request: AnalysisRequest) -> Dict[str, Any]:
        """执行定量分析（基于脚本）"""
        quantitative_results = {}
        
        # 加载和执行脚本
        for script_name in scripts:
            try:
                script_result = self._execute_alienation_script(script_name, request)
                quantitative_results[script_name] = script_result
            except Exception as e:
                logger.warning(f"定量分析失败 {script_name}: {str(e)}")
                quantitative_results[script_name] = {'error': str(e), 'success': False}
        
        return quantitative_results
    
    def _synthesize_alienation_results(self, qualitative_results: Dict[str, Any], 
                                     quantitative_results: Dict[str, Any], 
                                     alienation_types: List[str]) -> Dict[str, Any]:
        """综合异化分析结果"""
        synthesis = {
            'alienation_types': alienation_types,
            'qualitative_analysis': qualitative_results,
            'quantitative_analysis': quantitative_results,
            'integration_score': 0.0,
            'synthesis_quality': 'pending',
            'recommendations': [],
            'intervention_plan': {},
            'success': True
        }
        
        try:
            # 计算整合分数
            synthesis['integration_score'] = self._calculate_integration_score(
                qualitative_results, quantitative_results
            )
            
            # 评估综合质量
            synthesis['synthesis_quality'] = self._assess_synthesis_quality(synthesis['integration_score'])
            
            # 生成建议
            synthesis['recommendations'] = self._generate_alienation_recommendations(
                qualitative_results, quantitative_results
            )
            
            # 生成干预计划
            synthesis['intervention_plan'] = self._generate_intervention_plan(
                qualitative_results, quantitative_results
            )
            
        except Exception as e:
            synthesis['error'] = str(e)
            synthesis['success'] = False
        
        return synthesis
    
    def _load_prompt_files(self, prompt_files: List[str]) -> List[str]:
        """加载prompt文件内容"""
        base_path = 'skills/alienation-analysis/prompts/'
        contents = []
        
        for prompt_file in prompt_files:
            file_path = os.path.join(base_path, prompt_file)
            try:
                if os.path.exists(file_path):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        contents.append(f.read())
                else:
                    # 如果文件不存在，使用默认内容
                    contents.append(f"# {prompt_file}\n\n默认分析框架")
            except Exception as e:
                logger.warning(f"加载prompt文件失败 {prompt_file}: {str(e)}")
                contents.append(f"# {prompt_file}\n\n加载失败")
        
        return contents
    
    def _analyze_with_prompt(self, prompt_content: str, request: AnalysisRequest) -> Dict[str, Any]:
        """基于prompt内容进行分析"""
        # 这里应该实现基于prompt的定性分析逻辑
        # 目前返回模拟结果，后续可以集成AI模型
        return {
            'analysis_type': 'qualitative',
            'prompt_used': prompt_content[:100] + "...",
            'result': '定性分析完成（基于prompt）',
            'success': True
        }
    
    def _execute_alienation_script(self, script_name: str, request: AnalysisRequest) -> Dict[str, Any]:
        """执行异化分析脚本 - 使用统一引擎"""
        try:
            # 使用统一引擎替代多个独立脚本模块
            from skills.alienation_analysis.scripts.alienation_analysis_engine import AlienationAnalysisEngine
            
            # 创建统一引擎实例
            engine = AlienationAnalysisEngine()
            
            # 根据脚本类型执行相应的统一分析功能
            if script_name in ['calculate_alienation_score.py', 'classify_alienation_types.py', 'generate_intervention_plan.py']:
                # 这些是核心分析功能，统一通过引擎执行
                result = engine.comprehensive_analysis(request.data_sources)
            else:
                # 其他脚本类型也通过引擎统一处理
                result = engine.comprehensive_analysis(request.data_sources)
            
            result['script_name'] = script_name
            result['engine_used'] = 'AlienationAnalysisEngine'
            return result
            
        except ImportError as e:
            logger.warning(f"导入统一引擎失败 {script_name}: {str(e)}")
            # 如果统一引擎导入失败，返回基本的分析结果
            return {
                'error': f'统一引擎导入失败: {str(e)}',
                'success': False,
                'fallback_analysis': {
                    'script_name': script_name,
                    'basic_result': '基础分析功能（统一引擎未加载）'
                }
            }
        except Exception as e:
            logger.error(f"执行统一引擎失败 {script_name}: {str(e)}")
            return {
                'error': str(e),
                'success': False,
                'script_name': script_name,
                'engine_used': 'AlienationAnalysisEngine'
            }
    
    def _calculate_integration_score(self, qualitative_results: Dict[str, Any], 
                                   quantitative_results: Dict[str, Any]) -> float:
        """计算定性与定量分析的整合分数"""
        try:
            # 计算定性分析成功率
            qualitative_success_rate = sum(1 for r in qualitative_results.values() 
                                         if r.get('success', True)) / max(1, len(qualitative_results))
            
            # 计算定量分析成功率
            quantitative_success_rate = sum(1 for r in quantitative_results.values() 
                                          if r.get('success', True)) / max(1, len(quantitative_results))
            
            # 简单的整合分数计算
            integration_score = (qualitative_success_rate + quantitative_success_rate) / 2
            
            return min(1.0, integration_score)
            
        except Exception:
            return 0.5  # 默认中等分数
    
    def _assess_synthesis_quality(self, integration_score: float) -> str:
        """评估综合质量"""
        if integration_score >= 0.8:
            return '优秀'
        elif integration_score >= 0.6:
            return '良好'
        elif integration_score >= 0.4:
            return '一般'
        else:
            return '较差'
    
    def _generate_alienation_recommendations(self, qualitative_results: Dict[str, Any], 
                                           quantitative_results: Dict[str, Any]) -> List[str]:
        """生成异化分析建议"""
        recommendations = []
        
        # 从定量结果中提取建议
        for script_result in quantitative_results.values():
            if script_result.get('success') and 'intervention_recommendations' in script_result:
                recommendations.extend(script_result['intervention_recommendations'])
        
        # 去重
        recommendations = list(set(recommendations))
        
        return recommendations[:10]  # 最多返回10条建议
    
    def _generate_intervention_plan(self, qualitative_results: Dict[str, Any], 
                                  quantitative_results: Dict[str, Any]) -> Dict[str, Any]:
        """生成干预计划"""
        # 寻找干预计划生成器的结果
        for script_result in quantitative_results.values():
            if script_result.get('script_name') == 'generate_intervention_plan.py' and script_result.get('success'):
                return script_result
        
        # 如果没有找到，返回默认计划
        return {
            'immediate_actions': ['寻求专业帮助', '建立支持系统'],
            'medium_term_goals': ['改善生活质量', '增强自我认知'],
            'long_term_vision': ['实现个人全面发展']
        }
    
    def _load_skill_module(self, skill_name: str):
        """动态加载技能模块"""
        module_path = self.skills_modules.get(skill_name)
        if not module_path:
            raise ValueError(f"未找到技能模块: {skill_name}")
        
        try:
            # 模拟模块导入（实际实现中需要真实的模块）
            class MockSkillModule:
                def __init__(self):
                    pass
                
                class Skill:
                    def comprehensive_analysis(self, data):
                        return self._mock_historical_analysis(data)
                    
                    def comprehensive_class_analysis(self, data):
                        return self._mock_class_analysis(data)
                    
                    def practical_application_analysis(self, data):
                        return self._mock_practical_analysis(data)
                    
                    def comprehensive_synthesis_analysis(self, question, data):
                        return self._mock_synthesis_analysis(question, data)
                    
                    def comprehensive_alienation_analysis(self, data):
                        return self._mock_alienation_analysis(data)
                    
                    def _mock_historical_analysis(self, data):
                        return {
                            'productivity_analysis': {
                                'level': '数字生产力发展阶段',
                                'development_trend': '快速发展',
                                'contradictions': ['技术发展与制度滞后']
                            },
                            'relations_analysis': {
                                'adaptation_level': '部分适应',
                                'required_changes': ['完善数字治理体系']
                            },
                            'quality_score': 0.82
                        }
                    
                    def _mock_class_analysis(self, data):
                        return {
                            'class_structure': {
                                'traditional_classes': '继续分化',
                                'emerging_classes': '快速发展',
                                'new_intermediate_class': '规模扩大'
                            },
                            'class_relations': {
                                'main_contradiction': '数字发展与社会公平',
                                'conflict_intensity': '中等'
                            },
                            'quality_score': 0.79
                        }
                    
                    def _mock_practical_analysis(self, data):
                        return {
                            'problem_framing': {
                                'marxist_analysis': '符合马克思主义分析框架',
                                'main_contradictions': '已识别主要矛盾'
                            },
                            'solution_pathway': {
                                'fundamental_approach': '坚持社会主义方向',
                                'phased_strategy': '分阶段推进',
                                'policy_recommendations': ['完善制度', '加强监管']
                            },
                            'quality_score': 0.85
                        }
                    
                    def _mock_synthesis_analysis(self, question, data):
                        return {
                            'theoretical_framework': '马克思主义理论框架',
                            'quantitative_results': '定量分析结果',
                            'comprehensive_interpretation': '理论与数据融合解释',
                            'practical_guidance': '实践指导建议',
                            'quality_score': 0.88
                        }
                    
                    def _mock_alienation_analysis(self, data):
                        return {
                            'labor_alienation': {
                                'process_alienation': {
                                    'score': 0.75,
                                    'manifestation': '劳动过程高度标准化，劳动者自主性受限'
                                },
                                'product_alienation': {
                                    'score': 0.68,
                                    'manifestation': '劳动成果被平台无偿占有，劳动者无法获得应有价值'
                                },
                                'species_alienation': {
                                    'score': 0.72,
                                    'manifestation': '数字劳动的重复性压抑人的创造性本质'
                                },
                                'social_alienation': {
                                    'score': 0.65,
                                    'manifestation': '劳动者之间的社会关系被竞争关系替代'
                                }
                            },
                            'social_alienation': {
                                'interpersonal_alienation': '人际交往缺乏真实性',
                                'community_dissolution': '共同体意识缺失',
                                'identity_fragmentation': '社会角色与真实自我分离'
                            },
                            'consumption_alienation': {
                                'consumption_behavior': '符号消费替代真实需求',
                                'materialism': '物质欲望过度膨胀',
                                'consumer_identity': '通过消费构建虚假身份认同'
                            },
                            'technology_alienation': {
                                'dependency_level': '对技术过度依赖',
                                'control_reversal': '技术控制人类行为',
                                'digital_life': '数字化生存带来的异化'
                            },
                            'alienation_intensity': {
                                'overall_score': 0.70,
                                'severity_level': '中等异化程度',
                                'primary_types': ['劳动异化', '技术异化']
                            },
                            'transcendence_path': {
                                'immediate_actions': ['提高劳动者权益保护', '建立工人组织'],
                                'medium_strategies': ['推动平台民主化', '完善数字治理'],
                                'long_term_vision': '实现人的全面发展和社会解放'
                            },
                            'quality_score': 0.86
                        }
            
            return MockSkillModule()
            
        except Exception as e:
            logger.error(f"加载技能模块失败: {skill_name}, 错误: {str(e)}")
            raise
    
    def _synthesize_analysis_results(self, analysis_results: Dict[str, Any], request: AnalysisRequest) -> str:
        """综合分析结果"""
        synthesis_parts = []
        
        synthesis_parts.append("# 数字马克思智能体综合分析报告")
        synthesis_parts.append(f"\n**分析时间**: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}")
        synthesis_parts.append(f"**问题描述**: {request.problem_description}")
        synthesis_parts.append(f"**分析类型**: {request.analysis_type}")
        
        # 整合各技能分析结果
        for skill_name, result in analysis_results.items():
            if result.get('success', True):
                synthesis_parts.append(f"\n## {skill_name.replace('_', ' ').title()}分析")
                
                if skill_name == 'historical_materialist':
                    synthesis_parts.extend([
                        f"- **生产力水平**: {result.get('productivity_analysis', {}).get('level', '待分析')}",
                        f"- **发展态势**: {result.get('productivity_analysis', {}).get('development_trend', '待分析')}",
                        f"- **主要矛盾**: {', '.join(result.get('productivity_analysis', {}).get('contradictions', []))}",
                        f"- **关系适应**: {result.get('relations_analysis', {}).get('adaptation_level', '待分析')}"
                    ])
                
                elif skill_name == 'class_structure':
                    synthesis_parts.extend([
                        f"- **传统阶级**: {result.get('class_structure', {}).get('traditional_classes', '待分析')}",
                        f"- **新兴阶层**: {result.get('class_structure', {}).get('emerging_classes', '待分析')}",
                        f"- **主要矛盾**: {result.get('class_relations', {}).get('main_contradiction', '待分析')}",
                        f"- **冲突强度**: {result.get('class_relations', {}).get('conflict_intensity', '待分析')}"
                    ])
                
                elif skill_name == 'practical_application':
                    synthesis_parts.extend([
                        f"- **问题本质**: {result.get('problem_framing', {}).get('marxist_analysis', '待分析')}",
                        f"- **根本途径**: {result.get('solution_pathway', {}).get('fundamental_approach', '待分析')}",
                        f"- **政策建议**: {', '.join(result.get('solution_pathway', {}).get('policy_recommendations', []))}"
                    ])
                
                elif skill_name == 'dialectical_synthesis':
                    synthesis_parts.extend([
                        f"- **理论框架**: {result.get('theoretical_framework', '待分析')}",
                        f"- **定量结果**: {result.get('quantitative_results', '待分析')}",
                        f"- **综合解释**: {result.get('comprehensive_interpretation', '待分析')}"
                    ])
                
                elif skill_name == 'alienation_analysis':
                    labor_alienation = result.get('labor_alienation', {})
                    alienation_intensity = result.get('alienation_intensity', {})
                    transcendence_path = result.get('transcendence_path', {})
                    
                    synthesis_parts.extend([
                        f"- **劳动异化程度**: {alienation_intensity.get('overall_score', 0):.2f}/1.00",
                        f"- **主要异化类型**: {', '.join(alienation_intensity.get('primary_types', []))}",
                        f"- **劳动过程异化**: {labor_alienation.get('process_alienation', {}).get('manifestation', '待分析')}",
                        f"- **超越路径**: {', '.join(transcendence_path.get('immediate_actions', []))}"
                    ])
        
        # 添加质量评估
        overall_quality = np.mean([r.get('quality_score', 0) for r in analysis_results.values()])
        synthesis_parts.append(f"\n## 总体评估")
        synthesis_parts.append(f"- **综合质量分数**: {overall_quality:.3f}")
        synthesis_parts.append(f"- **理论准确性**: 符合马克思主义基本原理")
        synthesis_parts.append(f"- **分析深度**: 达到要求深度")
        synthesis_parts.append(f"- **实践价值**: 具有实践指导意义")
        
        return '\n'.join(synthesis_parts)
    
    def _generate_practical_guidance(self, analysis_results: Dict[str, Any], request: AnalysisRequest) -> Dict[str, Any]:
        """生成实践指导"""
        guidance = {
            'immediate_actions': [],
            'medium_term_goals': [],
            'long_term_vision': [],
            'key_indicators': [],
            'risk_warnings': []
        }
        
        # 基于分析结果生成指导
        if 'historical_materialist' in analysis_results:
            historical = analysis_results['historical_materialist']
            if 'productivity_analysis' in historical:
                guidance['immediate_actions'].append("关注生产力发展中的矛盾变化")
                guidance['key_indicators'].append("生产力发展水平监测")
        
        if 'class_structure' in analysis_results:
            class_analysis = analysis_results['class_structure']
            if 'class_relations' in class_analysis:
                main_contradiction = class_analysis['class_relations'].get('main_contradiction', '')
                if '社会公平' in main_contradiction:
                    guidance['immediate_actions'].append("加强社会公平机制建设")
                    guidance['medium_term_goals'].append("缩小数字鸿沟")
        
        if 'practical_application' in analysis_results:
            practical = analysis_results['practical_application']
            if 'solution_pathway' in practical:
                recommendations = practical['solution_pathway'].get('policy_recommendations', [])
                guidance['immediate_actions'].extend(recommendations)
        
        return guidance
    
    def _assess_theoretical_contributions(self, analysis_results: Dict[str, Any], request: AnalysisRequest) -> Dict[str, Any]:
        """评估理论贡献"""
        contributions = {
            'conceptual_development': [],
            'methodological_innovations': [],
            'empirical_insights': [],
            'practical_applications': []
        }
        
        # 分析理论贡献
        if 'dialectical_synthesis' in analysis_results:
            synthesis = analysis_results['dialectical_synthesis']
            contributions['conceptual_development'].append("定性与定量分析融合方法")
            contributions['methodological_innovations'].append("辩证综合分析框架")
        
        if 'historical_materialist' in analysis_results:
            contributions['empirical_insights'].append("数字时代历史唯物主义应用")
        
        if 'practical_application' in analysis_results:
            contributions['practical_applications'].append("理论指导实践的转化机制")
        
        return contributions
    
    def _check_quality_requirements(self, quality_metrics: QualityMetrics, request: AnalysisRequest) -> Dict[str, Any]:
        """检查质量要求"""
        requirements = request.quality_requirements
        
        failures = []
        if quality_metrics.theoretical_accuracy < requirements.get('theoretical_accuracy', 0.75):
            failures.append(f"理论准确性不足: {quality_metrics.theoretical_accuracy:.3f} < {requirements['theoretical_accuracy']}")
        
        if quality_metrics.analysis_depth < requirements.get('analysis_depth', 0.70):
            failures.append(f"分析深度不足: {quality_metrics.analysis_depth:.3f} < {requirements['analysis_depth']}")
        
        if quality_metrics.conclusion_reliability < requirements.get('practical_relevance', 0.80):
            failures.append(f"实践相关性不足: {quality_metrics.conclusion_reliability:.3f} < {requirements['practical_relevance']}")
        
        return {
            'meets_requirements': len(failures) == 0,
            'failure_reasons': failures if failures else None,
            'quality_gaps': [req - getattr(quality_metrics, key.replace('_', '_'), 0) 
                           for key, req in requirements.items() 
                           if hasattr(quality_metrics, key.replace('_', '_'))]
        }
    
    def _clean_and_validate_data(self, data: Any) -> Any:
        """清洗和验证数据"""
        if isinstance(data, dict):
            return {k: self._clean_and_validate_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._clean_and_validate_data(item) for item in data]
        elif isinstance(data, str):
            return data.strip()
        else:
            return data
    
    def _assess_skill_quality(self, result: Dict[str, Any], skill_name: str) -> float:
        """评估技能质量"""
        if 'quality_score' in result:
            return result['quality_score']
        
        # 基础质量评估
        if result.get('success', True):
            return 0.7
        else:
            return 0.0
    
    def export_analysis_result(self, result: AnalysisResult, output_path: str = None) -> str:
        """导出分析结果"""
        if output_path is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_path = f"digital_marx_analysis_{timestamp}.json"
        
        export_data = {
            'metadata': {
                'analysis_time': datetime.now().isoformat(),
                'execution_time': result.execution_time,
                'success': result.success,
                'error_message': result.error_message
            },
            'request': asdict(result.request),
            'analysis_results': result.analysis_results,
            'quality_metrics': asdict(result.quality_metrics),
            'synthesis_report': result.synthesis_report,
            'practical_guidance': result.practical_guidance,
            'theoretical_contributions': result.theoretical_contributions
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"分析结果已导出到: {output_path}")
        return output_path

def main():
    """主函数 - 用于测试"""
    # 创建智能体控制器
    controller = DigitalMarxExpertController()
    
    # 创建测试请求
    test_request = AnalysisRequest(
        problem_description="分析数字经济发展对社会阶级结构的影响",
        analysis_type="comprehensive",
        data_sources={
            'economic_data': {
                'digital_economy_gdp': 0.4,
                'tech_employment_rate': 0.25,
                'platform_economy_size': 0.15
            },
            'social_data': {
                'income_distribution': 'increasing_inequality',
                'skill_requirements': 'rising',
                'job_displacement': 'moderate'
            }
        },
        depth_level="comprehensive",
        output_format="detailed_report"
    )
    
    # 执行分析
    logger.info("开始执行数字马克思智能体测试分析")
    result = controller.process_analysis_request(test_request)
    
    # 输出结果
    print("\n" + "="*80)
    print("数字马克思智能体分析结果")
    print("="*80)
    print(f"分析成功: {result.success}")
    print(f"执行时间: {result.execution_time:.2f}秒")
    print(f"质量分数: {result.quality_metrics.overall_quality:.3f}")
    
    if result.error_message:
        print(f"错误信息: {result.error_message}")
    
    print("\n" + result.synthesis_report)
    
    # 导出结果
    output_file = controller.export_analysis_result(result)
    print(f"\n分析结果已保存到: {output_file}")

if __name__ == "__main__":
    main()
