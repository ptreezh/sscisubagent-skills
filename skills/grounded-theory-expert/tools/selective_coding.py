#!/usr/bin/env python3
"""
选择性编码工具
基于Strauss & Corbin (1990)的选择性编码方法
确定核心范畴，整合理论
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from collections import defaultdict


class SelectiveCoder:
    """选择性编码器"""
    
    def __init__(self, working_dir: str = './session'):
        """初始化选择性编码器
        
        参数:
            working_dir: 工作目录
        """
        self.working_dir = working_dir
        self.core_category = None
        self.theoretical_framework = {}
        self.story_line = ""
        self.propositions = []
        
    def perform_selective_coding(self, 
                                  categories: Dict[str, Dict],
                                  relationships: List[Dict],
                                  paradigm_model: Dict) -> Dict[str, Any]:
        """执行选择性编码
        
        参数:
            categories: 范畴字典
            relationships: 关系列表
            paradigm_model: 范式模型
            
        返回:
            选择性编码结果
        """
        # 步骤1: 识别核心范畴
        core_category = self._identify_core_category(categories, relationships)
        
        # 步骤2: 构建故事线
        story_line = self._construct_story_line(core_category, paradigm_model)
        
        # 步骤3: 整合理论框架
        theoretical_framework = self._integrate_theory(
            core_category, categories, relationships
        )
        
        # 步骤4: 生成理论命题
        propositions = self._generate_propositions(
            core_category, relationships, theoretical_framework
        )
        
        # 步骤5: 验证理论
        validation_result = self._validate_theory(
            core_category, categories, propositions
        )
        
        # 步骤6: 生成理论备忘录
        memos = self._generate_theoretical_memos(
            core_category, story_line, propositions
        )
        
        result = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'core_category': core_category,
            'story_line': story_line,
            'theoretical_framework': theoretical_framework,
            'propositions': propositions,
            'validation': validation_result,
            'memos': memos
        }
        
        return result
    
    def _identify_core_category(self, 
                                categories: Dict[str, Dict],
                                relationships: List[Dict]) -> Dict[str, Any]:
        """识别核心范畴
        
        参数:
            categories: 范畴字典
            relationships: 关系列表
            
        返回:
            核心范畴信息
        """
        if not categories:
            return {'name': None, 'reason': '没有可用的范畴'}
        
        # 计算每个范畴的中心度
        centrality_scores = defaultdict(int)
        
        for rel in relationships:
            centrality_scores[rel['source']] += 1
            centrality_scores[rel['target']] += 1
        
        # 计算每个范畴的概念数量
        concept_counts = {
            cat_name: len(cat_data.get('codes', []))
            for cat_name, cat_data in categories.items()
        }
        
        # 综合评分：中心度 + 概念数量
        combined_scores = {}
        for cat_name in categories:
            combined_scores[cat_name] = (
                centrality_scores.get(cat_name, 0) * 2 + 
                concept_counts.get(cat_name, 0)
            )
        
        # 选择得分最高的作为核心范畴
        core_name = max(combined_scores.keys(), key=lambda x: combined_scores[x])
        
        return {
            'name': core_name,
            'definition': categories[core_name].get('definition', ''),
            'centrality_score': centrality_scores.get(core_name, 0),
            'concept_count': concept_counts.get(core_name, 0),
            'combined_score': combined_scores[core_name],
            'selection_reason': f"该范畴具有最高的综合评分({combined_scores[core_name]})，"
                               f"包含{concept_counts.get(core_name, 0)}个概念，"
                               f"参与{centrality_scores.get(core_name, 0)}个关系"
        }
    
    def _construct_story_line(self, 
                              core_category: Dict,
                              paradigm_model: Dict) -> str:
        """构建故事线
        
        参数:
            core_category: 核心范畴
            paradigm_model: 范式模型
            
        返回:
            故事线叙述
        """
        core_name = core_category.get('name', '核心现象')
        
        # 构建故事线各部分
        conditions = paradigm_model.get('conditions', [])
        phenomenon = paradigm_model.get('phenomenon', core_name)
        context = paradigm_model.get('context', [])
        intervening = paradigm_model.get('intervening_conditions', [])
        actions = paradigm_model.get('action_strategies', [])
        consequences = paradigm_model.get('consequences', [])
        
        story_parts = []
        
        # 条件部分
        if conditions:
            story_parts.append(
                f"在{', '.join(conditions)}等条件下，"
            )
        
        # 核心现象
        story_parts.append(f"{phenomenon}成为研究关注的核心现象。")
        
        # 情境和中介条件
        if context:
            story_parts.append(f"这一现象发生在{', '.join(context)}的情境中。")
        if intervening:
            story_parts.append(f"受到{', '.join(intervening)}等因素的影响。")
        
        # 行动策略
        if actions:
            story_parts.append(
                f"行动者采取了{', '.join(actions)}等策略来应对。"
            )
        
        # 结果
        if consequences:
            story_parts.append(f"最终产生了{', '.join(consequences)}等结果。")
        
        story_line = ''.join(story_parts)
        
        return story_line
    
    def _integrate_theory(self,
                         core_category: Dict,
                         categories: Dict[str, Dict],
                         relationships: List[Dict]) -> Dict[str, Any]:
        """整合理论框架
        
        参数:
            core_category: 核心范畴
            categories: 范畴字典
            relationships: 关系列表
            
        返回:
            理论框架
        """
        core_name = core_category.get('name')
        
        # 构建层级结构
        framework = {
            'core_category': core_name,
            'core_definition': categories.get(core_name, {}).get('definition', ''),
            'major_categories': [],
            'minor_categories': [],
            'relationship_network': []
        }
        
        # 区分主要范畴和次要范畴
        for cat_name, cat_data in categories.items():
            if cat_name == core_name:
                continue
                
            # 检查是否与核心范畴直接相关
            is_major = any(
                (r['source'] == core_name and r['target'] == cat_name) or
                (r['target'] == core_name and r['source'] == cat_name)
                for r in relationships
            )
            
            category_info = {
                'name': cat_name,
                'definition': cat_data.get('definition', ''),
                'properties': cat_data.get('properties', {}),
                'relationship_to_core': self._get_relationship_to_core(
                    core_name, cat_name, relationships
                )
            }
            
            if is_major:
                framework['major_categories'].append(category_info)
            else:
                framework['minor_categories'].append(category_info)
        
        # 关系网络
        framework['relationship_network'] = [
            {
                'source': r['source'],
                'target': r['target'],
                'type': r['type'],
                'evidence': r.get('evidence', '')
            }
            for r in relationships
        ]
        
        return framework
    
    def _get_relationship_to_core(self,
                                  core_name: str,
                                  cat_name: str,
                                  relationships: List[Dict]) -> Optional[str]:
        """获取范畴与核心范畴的关系
        
        参数:
            core_name: 核心范畴名称
            cat_name: 目标范畴名称
            relationships: 关系列表
            
        返回:
            关系描述
        """
        for r in relationships:
            if r['source'] == core_name and r['target'] == cat_name:
                return f"核心范畴->{r['type']}->{cat_name}"
            if r['target'] == core_name and r['source'] == cat_name:
                return f"{cat_name}->{r['type']}->核心范畴"
        return None
    
    def _generate_propositions(self,
                               core_category: Dict,
                               relationships: List[Dict],
                               framework: Dict) -> List[Dict]:
        """生成理论命题
        
        参数:
            core_category: 核心范畴
            relationships: 关系列表
            framework: 理论框架
            
        返回:
            理论命题列表
        """
        propositions = []
        core_name = core_category.get('name')
        
        # 基于关系生成命题
        for i, rel in enumerate(relationships, 1):
            if rel['source'] == core_name or rel['target'] == core_name:
                if rel['source'] == core_name:
                    prop_text = f"{rel['source']}的增强会{rel['type']}{rel['target']}的变化"
                else:
                    prop_text = f"{rel['source']}的变化会{rel['type']}{rel['target']}"
                
                propositions.append({
                    'id': f'P{i}',
                    'proposition': prop_text,
                    'type': 'causal',
                    'evidence': rel.get('evidence', ''),
                    'confidence': 'medium' if rel.get('strength') == 'medium' else 'high'
                })
        
        # 添加整合性命题
        major_cats = framework.get('major_categories', [])
        if len(major_cats) >= 2:
            cat_names = [c['name'] for c in major_cats[:3]]
            propositions.append({
                'id': f'P{len(propositions)+1}',
                'proposition': f"{core_name}是连接{', '.join(cat_names)}的关键枢纽",
                'type': 'integrative',
                'evidence': '基于理论框架整合分析',
                'confidence': 'high'
            })
        
        return propositions
    
    def _validate_theory(self,
                        core_category: Dict,
                        categories: Dict[str, Dict],
                        propositions: List[Dict]) -> Dict[str, Any]:
        """验证理论
        
        参数:
            core_category: 核心范畴
            categories: 范畴字典
            propositions: 理论命题
            
        返回:
            验证结果
        """
        validation = {
            'core_category_valid': core_category.get('name') is not None,
            'categories_count': len(categories),
            'propositions_count': len(propositions),
            'theoretical_density': len(propositions) / len(categories) if categories else 0,
            'coverage_rate': 0,
            'issues': [],
            'recommendations': []
        }
        
        # 检查理论覆盖度
        connected_cats = set()
        for prop in propositions:
            # 简单检查命题中提到的范畴
            for cat_name in categories:
                if cat_name in prop.get('proposition', ''):
                    connected_cats.add(cat_name)
        
        validation['coverage_rate'] = (
            len(connected_cats) / len(categories) * 100 if categories else 0
        )
        
        # 检查问题
        if validation['theoretical_density'] < 0.5:
            validation['issues'].append('理论密度较低，需要更多命题')
        
        if validation['coverage_rate'] < 70:
            validation['issues'].append('理论覆盖度不足，部分范畴未被整合')
        
        # 生成建议
        if validation['issues']:
            validation['recommendations'].append('建议继续收集数据，发展理论命题')
        else:
            validation['recommendations'].append('理论已基本完善，可进行饱和度检验')
        
        return validation
    
    def _generate_theoretical_memos(self,
                                    core_category: Dict,
                                    story_line: str,
                                    propositions: List[Dict]) -> List[Dict]:
        """生成理论备忘录
        
        参数:
            core_category: 核心范畴
            story_line: 故事线
            propositions: 理论命题
            
        返回:
            备忘录列表
        """
        memos = []
        
        # 核心范畴确定备忘录
        memos.append({
            'type': 'core_category_selection',
            'content': f"确定'{core_category.get('name')}'为核心范畴。"
                      f"原因：{core_category.get('selection_reason', '')}",
            'timestamp': datetime.now().isoformat()
        })
        
        # 故事线备忘录
        memos.append({
            'type': 'story_line_construction',
            'content': f"构建故事线：{story_line}",
            'timestamp': datetime.now().isoformat()
        })
        
        # 命题生成备忘录
        for prop in propositions[:3]:  # 只记录前3个关键命题
            memos.append({
                'type': 'proposition_generation',
                'content': f"生成命题{prop['id']}：{prop['proposition']}",
                'timestamp': datetime.now().isoformat()
            })
        
        return memos
    
    def save_results(self, result: Dict, filename: str = 'selective_coding_result.json'):
        """保存选择性编码结果
        
        参数:
            result: 编码结果
            filename: 保存文件名
        """
        filepath = os.path.join(self.working_dir, filename)
        os.makedirs(self.working_dir, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    # 测试
    coder = SelectiveCoder()
    
    test_categories = {
        '工作压力': {
            'definition': '工作中的压力感受',
            'codes': ['工作压力', '时间紧迫', '任务繁重']
        },
        '应对策略': {
            'definition': '应对压力的方式',
            'codes': ['寻求支持', '调整心态', '时间管理']
        },
        '工作效果': {
            'definition': '工作结果',
            'codes': ['工作效率提升', '满意度变化', '绩效改善']
        }
    }
    
    test_relationships = [
        {'source': '工作压力', 'target': '应对策略', 'type': '引发'},
        {'source': '应对策略', 'target': '工作效果', 'type': '导致'}
    ]
    
    test_paradigm = {
        'conditions': ['组织环境'],
        'phenomenon': '工作压力',
        'action_strategies': ['应对策略'],
        'consequences': ['工作效果']
    }
    
    result = coder.perform_selective_coding(
        test_categories, test_relationships, test_paradigm
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
