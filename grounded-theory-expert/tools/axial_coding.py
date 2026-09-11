#!/usr/bin/env python3
"""
轴心编码工具
基于Strauss & Corbin (1990)的轴心编码方法
建立范畴和关系连接
"""

import os
import json
from typing import Dict, List, Any, Tuple
from datetime import datetime
from collections import defaultdict


class AxialCoder:
    """轴心编码器"""
    
    def __init__(self, working_dir: str = './session'):
        """初始化轴心编码器
        
        参数:
            working_dir: 工作目录
        """
        self.working_dir = working_dir
        self.categories = {}
        self.relationships = []
        self.paradigm_model = {}
        
    def perform_axial_coding(self, open_codes: List[Dict]) -> Dict[str, Any]:
        """执行轴心编码
        
        参数:
            open_codes: 开放编码结果列表
            
        返回:
            轴心编码结果
        """
        # 步骤1: 概念聚类为范畴
        categories = self._cluster_codes_to_categories(open_codes)
        
        # 步骤2: 识别范畴属性和维度
        for cat_name, cat_data in categories.items():
            cat_data['properties'] = self._identify_properties(cat_data['codes'])
            cat_data['dimensions'] = self._identify_dimensions(cat_data['properties'])
        
        # 步骤3: 建立范畴间关系
        relationships = self._identify_relationships(categories)
        
        # 步骤4: 构建范式模型
        paradigm_model = self._build_paradigm_model(categories, relationships)
        
        # 步骤5: 生成轴心编码备忘录
        memos = self._generate_axial_memos(categories, relationships)
        
        result = {
            'status': 'success',
            'timestamp': datetime.now().isoformat(),
            'categories': categories,
            'relationships': relationships,
            'paradigm_model': paradigm_model,
            'memos': memos,
            'statistics': {
                'total_categories': len(categories),
                'total_relationships': len(relationships),
                'avg_codes_per_category': sum(len(c['codes']) for c in categories.values()) / len(categories) if categories else 0
            }
        }
        
        return result
    
    def _cluster_codes_to_categories(self, codes: List[Dict]) -> Dict[str, Dict]:
        """将开放编码聚类为范畴
        
        参数:
            codes: 开放编码列表
            
        返回:
            范畴字典
        """
        categories = defaultdict(lambda: {'codes': [], 'definition': '', 'frequency': 0})
        
        for code in codes:
            # 基于概念相似性进行聚类
            category_name = self._determine_category(code)
            categories[category_name]['codes'].append(code['code'])
            categories[category_name]['frequency'] += code.get('frequency', 1)
        
        # 为每个范畴生成定义
        for cat_name, cat_data in categories.items():
            cat_data['definition'] = self._generate_category_definition(cat_name, cat_data['codes'])
        
        return dict(categories)
    
    def _determine_category(self, code: Dict) -> str:
        """确定概念所属的范畴
        
        参数:
            code: 编码条目
            
        返回:
            范畴名称
        """
        # 基于编码内容和关键词确定范畴
        code_name = code.get('code', '').lower()
        definition = code.get('definition', '').lower()
        
        # 常见范畴关键词映射
        category_keywords = {
            '条件因素': ['条件', '背景', '情境', '环境', '前提', '基础'],
            '行动策略': ['行动', '策略', '行为', '应对', '处理', '选择'],
            '互动过程': ['互动', '交流', '沟通', '协商', '合作', '冲突'],
            '结果后果': ['结果', '后果', '影响', '效果', '产出', '变化'],
            '中介条件': ['中介', '调节', '影响因素', '变量', '情境因素'],
            '核心现象': ['现象', '问题', '核心', '本质', '关键']
        }
        
        for category, keywords in category_keywords.items():
            if any(kw in code_name or kw in definition for kw in keywords):
                return category
        
        # 默认归类为"其他现象"
        return '其他现象'
    
    def _identify_properties(self, codes: List[str]) -> Dict[str, str]:
        """识别范畴属性
        
        参数:
            codes: 范畴包含的编码列表
            
        返回:
            属性字典
        """
        properties = {}
        
        for i, code in enumerate(codes):
            property_name = f"属性_{i+1}"
            properties[property_name] = f"与'{code}'相关的特征"
        
        return properties
    
    def _identify_dimensions(self, properties: Dict[str, str]) -> Dict[str, Tuple[str, str]]:
        """识别属性维度
        
        参数:
            properties: 属性字典
            
        返回:
            维度字典（属性名 -> (低维度, 高维度)）
        """
        dimensions = {}
        
        for prop_name, prop_desc in properties.items():
            # 为每个属性定义变化维度
            dimensions[prop_name] = ('低程度', '高程度')
        
        return dimensions
    
    def _identify_relationships(self, categories: Dict) -> List[Dict]:
        """识别范畴间关系
        
        参数:
            categories: 范畴字典
            
        返回:
            关系列表
        """
        relationships = []
        cat_names = list(categories.keys())
        
        # 基于范式模型识别关系
        relation_types = [
            ('条件因素', '核心现象', '导致'),
            ('核心现象', '行动策略', '引发'),
            ('行动策略', '结果后果', '产生'),
            ('中介条件', '行动策略', '影响'),
            ('互动过程', '行动策略', '塑造')
        ]
        
        for source, target, rel_type in relation_types:
            if source in cat_names and target in cat_names:
                relationships.append({
                    'source': source,
                    'target': target,
                    'type': rel_type,
                    'evidence': f"基于{source}和{target}范畴的内容分析",
                    'strength': 'medium'
                })
        
        return relationships
    
    def _build_paradigm_model(self, categories: Dict, relationships: List[Dict]) -> Dict:
        """构建范式模型
        
        参数:
            categories: 范畴字典
            relationships: 关系列表
            
        返回:
            范式模型
        """
        cat_names = list(categories.keys())
        
        model = {
            'conditions': [],
            'phenomenon': None,
            'context': [],
            'intervening_conditions': [],
            'action_strategies': [],
            'consequences': []
        }
        
        for cat_name in cat_names:
            if '条件' in cat_name:
                model['conditions'].append(cat_name)
            elif '现象' in cat_name or '核心' in cat_name:
                model['phenomenon'] = cat_name
            elif '情境' in cat_name or '背景' in cat_name:
                model['context'].append(cat_name)
            elif '中介' in cat_name or '影响' in cat_name:
                model['intervening_conditions'].append(cat_name)
            elif '行动' in cat_name or '策略' in cat_name:
                model['action_strategies'].append(cat_name)
            elif '结果' in cat_name or '后果' in cat_name:
                model['consequences'].append(cat_name)
        
        return model
    
    def _generate_category_definition(self, category_name: str, codes: List[str]) -> str:
        """生成范畴定义
        
        参数:
            category_name: 范畴名称
            codes: 包含的编码列表
            
        返回:
            范畴定义
        """
        code_str = '、'.join(codes[:5])
        if len(codes) > 5:
            code_str += f'等{len(codes)}个概念'
        
        return f"{category_name}：包含{code_str}等相关概念"
    
    def _generate_axial_memos(self, categories: Dict, relationships: List[Dict]) -> List[Dict]:
        """生成轴心编码备忘录
        
        参数:
            categories: 范畴字典
            relationships: 关系列表
            
        返回:
            备忘录列表
        """
        memos = []
        
        # 范畴形成备忘录
        for cat_name, cat_data in categories.items():
            memos.append({
                'type': 'category_formation',
                'category': cat_name,
                'content': f"范畴'{cat_name}'由{len(cat_data['codes'])}个概念聚类形成，"
                          f"具有{len(cat_data.get('properties', {}))}个属性。",
                'timestamp': datetime.now().isoformat()
            })
        
        # 关系发现备忘录
        for rel in relationships:
            memos.append({
                'type': 'relationship_discovery',
                'content': f"发现'{rel['source']}'通过'{rel['type']}'关系与'{rel['target']}'相连。",
                'timestamp': datetime.now().isoformat()
            })
        
        return memos
    
    def save_results(self, result: Dict, filename: str = 'axial_coding_result.json'):
        """保存轴心编码结果
        
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
    coder = AxialCoder()
    
    test_codes = [
        {'code': '工作压力', 'definition': '工作中的压力感受', 'frequency': 5},
        {'code': '时间紧迫', 'definition': '时间不够用的情况', 'frequency': 3},
        {'code': '寻求支持', 'definition': '向他人寻求帮助', 'frequency': 4},
        {'code': '调整心态', 'definition': '改变自己的心态', 'frequency': 2},
        {'code': '工作效率提升', 'definition': '工作变得更快', 'frequency': 3}
    ]
    
    result = coder.perform_axial_coding(test_codes)
    print(json.dumps(result, ensure_ascii=False, indent=2))
