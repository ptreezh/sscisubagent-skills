---
name: processing-network-data
description: 处理社会网络数据，包括关系数据收集、矩阵构建、数据清洗验证和多模网络处理。当需要从问卷、访谈、观察或数字记录中提取关系数据，构建标准化的网络矩阵时使用此技能。
---

# 网络数据处理技能

专门用于社会网络研究的数据收集和预处理，将原始关系数据转换为标准化的网络分析格式。

## 核心能力

### 1. 关系数据提取
- **问卷数据处理**：标准化社会网络问卷的数据提取
- **访谈关系识别**：从深度访谈文本中提取关系信息
- **观察记录编码**：参与观察中的互动关系编码
- **数字痕迹挖掘**：从社交媒体、通信记录中提取关系
- **多源数据整合**：不同来源关系数据的整合处理

### 2. 矩阵构建技术
- **邻接矩阵生成**：标准邻接矩阵的自动化构建
- **赋值矩阵处理**：加权关系矩阵的量化处理
- **有向网络矩阵**：有向关系的矩阵表示
- **多模网络矩阵**：多种关系类型的矩阵组织
- **动态网络矩阵**：时间序列网络数据的矩阵构建

### 3. 数据清洗验证
- **缺失值处理**：关系数据缺失值的识别和处理
- **异常值检测**：异常关系数据的识别和修正
- **一致性检验**：关系数据的逻辑一致性验证
- **完整性评估**：数据完整性和覆盖度评估
- **质量控制**：数据质量的多维度评估

### 4. 属性数据整合
- **节点属性整合**：节点属性与关系数据的整合
- **边属性处理**：边属性数据的标准化处理
- **时间属性编码**：时间相关属性的编码处理
- **分类变量处理**：分类变量的数值化处理
- **连续变量标准化**：连续变量的标准化处理

## 处理流程

### 第一步：问卷数据处理
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import json
import re

class QuestionnaireDataProcessor:
    def __init__(self):
        self.ego_networks = {}
        self.alter_list = []
        self.relationship_matrix = None
        
    def process_ego_network_questionnaire(self, questionnaire_file: str) -> Dict:
        """处理自我中心网络问卷数据"""
        # 读取问卷数据
        df = pd.read_excel(questionnaire_file)
        
        # 提取自我中心网络信息
        ego_networks = {}
        
        for _, row in df.iterrows():
            ego_id = row['受访者ID']
            alters = self.extract_alters(row)
            relationships = self.extract_relationships(row, alters)
            
            ego_networks[ego_id] = {
                'ego_attributes': self.extract_ego_attributes(row),
                'alters': alters,
                'relationships': relationships
            }
        
        return ego_networks
    
    def extract_alters(self, row: pd.Series) -> List[Dict]:
        """提取关系对象信息"""
        alters = []
        
        # 提取前5个重要关系对象
        for i in range(1, 6):
            alter_name = row.get(f'关系对象{i}_姓名', '')
            if pd.isna(alter_name) or alter_name == '':
                continue
                
            alter = {
                'name': alter_name,
                'relationship_type': row.get(f'关系对象{i}_关系', ''),
                'contact_frequency': row.get(f'关系对象{i}_联系频率', ''),
                'relationship_duration': row.get(f'关系对象{i}_认识时间', ''),
                'emotional_closeness': row.get(f'关系对象{i}_情感距离', '')
            }
            alters.append(alter)
        
        return alters
    
    def extract_relationships(self, row: pd.Series, alters: List[Dict]) -> Dict:
        """提取关系间的关系"""
        relationships = {}
        
        # 构建关系对象间的关系矩阵
        n_alters = len(alters)
        if n_alters > 1:
            relationship_matrix = np.zeros((n_alters, n_alters))
            
            for i in range(n_alters):
                for j in range(i+1, n_alters):
                    # 检查关系对象间是否认识
                    knows_key = f'关系对象{i+1}_认识关系对象{j+1}'
                    knows_value = row.get(knows_key, 0)
                    
                    if not pd.isna(knows_value) and knows_value == 1:
                        relationship_matrix[i][j] = 1
                        relationship_matrix[j][i] = 1
            
            relationships['matrix'] = relationship_matrix.tolist()
            relationships['alters'] = [alter['name'] for alter in alters]
        
        return relationships
    
    def extract_ego_attributes(self, row: pd.Series) -> Dict:
        """提取自我属性信息"""
        return {
            'age': row.get('年龄', ''),
            'gender': row.get('性别', ''),
            'education': row.get('教育程度', ''),
            'occupation': row.get('职业', ''),
            'income': row.get('收入水平', '')
        }
    
    def build_global_network(self, ego_networks: Dict) -> Dict:
        """构建全局网络"""
        # 收集所有节点
        all_nodes = set()
        all_edges = []
        
        for ego_id, network_data in ego_networks.items():
            all_nodes.add(ego_id)
            
            # 添加关系对象
            for alter in network_data['alters']:
                all_nodes.add(alter['name'])
                # 添加自我到关系对象的边
                all_edges.append({
                    'source': ego_id,
                    'target': alter['name'],
                    'weight': 1,
                    'relationship_type': alter['relationship_type']
                })
            
            # 添加关系对象间的关系
            if 'relationships' in network_data:
                rel_matrix = network_data['relationships']['matrix']
                alter_names = network_data['relationships']['alters']
                
                for i in range(len(alter_names)):
                    for j in range(i+1, len(alter_names)):
                        if rel_matrix[i][j] == 1:
                            all_edges.append({
                                'source': alter_names[i],
                                'target': alter_names[j],
                                'weight': 1,
                                'relationship_type': 'alter_relationship'
                            })
        
        return {
            'nodes': list(all_nodes),
            'edges': all_edges
        }
    
    def export_to_matrix(self, network_data: Dict, output_file: str):
        """导出为矩阵格式"""
        nodes = network_data['nodes']
        edges = network_data['edges']
        
        # 创建节点索引映射
        node_index = {node: i for i, node in enumerate(nodes)}
        
        # 创建邻接矩阵
        n = len(nodes)
        adj_matrix = np.zeros((n, n))
        
        for edge in edges:
            source_idx = node_index[edge['source']]
            target_idx = node_index[edge['target']]
            adj_matrix[source_idx][target_idx] = edge['weight']
            # 如果是无向网络，对称设置
            if edge.get('undirected', True):
                adj_matrix[target_idx][source_idx] = edge['weight']
        
        # 保存矩阵
        matrix_data = {
            'nodes': nodes,
            'adjacency_matrix': adj_matrix.tolist(),
            'node_index': node_index
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(matrix_data, f, ensure_ascii=False, indent=2)

# 使用示例
if __name__ == "__main__":
    processor = QuestionnaireDataProcessor()
    
    # 处理问卷数据
    ego_networks = processor.process_ego_network_questionnaire('social_network_questionnaire.xlsx')
    
    # 构建全局网络
    global_network = processor.build_global_network(ego_networks)
    
    # 导出矩阵
    processor.export_to_matrix(global_network, 'network_matrix.json')
    
    print(f"处理完成，共{len(global_network['nodes'])}个节点，{len(global_network['edges'])}条边")
```

### 第二步：访谈关系提取
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import jieba
import jieba.posseg as pseg
import re
from typing import Dict, List, Tuple
import networkx as nx

class InterviewRelationExtractor:
    def __init__(self):
        self.relation_patterns = [
            r'(.+?)和(.+?)是(.+?)',
            r'(.+?)与(.+?)有(.+?)',
            r'(.+?)向(.+?)(.+?)',
            r'(.+?)从(.+?)(.+?)',
            r'(.+?)帮(.+?)(.+?)',
            r'(.+?)支持(.+?)(.+?)'
        ]
        
        self.entity_types = ['人物', '组织', '机构', '部门', '团队', '家庭']
        
    def extract_relations_from_text(self, text: str) -> List[Dict]:
        """从访谈文本中提取关系"""
        relations = []
        
        # 分句处理
        sentences = self.split_sentences(text)
        
        for sentence in sentences:
            sentence_relations = self.extract_sentence_relations(sentence)
            relations.extend(sentence_relations)
        
        return relations
    
    def split_sentences(self, text: str) -> List[str]:
        """分句处理"""
        # 按句号、问号、感叹号分句
        sentences = re.split(r'[。！？；]', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def extract_sentence_relations(self, sentence: str) -> List[Dict]:
        """从单个句子中提取关系"""
        relations = []
        
        # 使用模式匹配提取关系
        for pattern in self.relation_patterns:
            matches = re.findall(pattern, sentence)
            for match in matches:
                if len(match) >= 2:
                    relation = {
                        'source': match[0].strip(),
                        'target': match[1].strip(),
                        'relation_type': match[2].strip() if len(match) > 2 else '未知关系',
                        'sentence': sentence,
                        'confidence': self.calculate_confidence(match, sentence)
                    }
                    relations.append(relation)
        
        # 使用依存句法分析提取关系
        dependency_relations = self.extract_dependency_relations(sentence)
        relations.extend(dependency_relations)
        
        return relations
    
    def calculate_confidence(self, match: Tuple, sentence: str) -> float:
        """计算关系提取的置信度"""
        confidence = 0.5  # 基础置信度
        
        # 如果匹配完整度高，提高置信度
        if len(match) >= 3 and match[2]:
            confidence += 0.2
        
        # 如果句子包含关系关键词，提高置信度
        relation_keywords = ['关系', '联系', '合作', '支持', '帮助', '沟通', '交流']
        for keyword in relation_keywords:
            if keyword in sentence:
                confidence += 0.1
                break
        
        # 如果实体是已知类型，提高置信度
        for entity in match[:2]:
            if self.is_named_entity(entity):
                confidence += 0.1
        
        return min(confidence, 1.0)
    
    def is_named_entity(self, text: str) -> bool:
        """判断是否是命名实体"""
        # 使用jieba词性标注
        words = pseg.cut(text)
        for word, flag in words:
            if flag == 'nr':  # 人名
                return True
            if flag == 'ns':  # 地名
                return True
            if flag == 'nt':  # 机构名
                return True
        
        return False
    
    def extract_dependency_relations(self, sentence: str) -> List[Dict]:
        """使用依存句法分析提取关系"""
        # 这里简化处理，实际应用中可以使用LTP、spaCy等工具
        relations = []
        
        # 识别主谓宾结构
        words = list(jieba.cut(sentence))
        pos_tags = [flag for word, flag in pseg.cut(sentence)]
        
        # 简化的主谓宾关系识别
        for i, (word, pos) in enumerate(zip(words, pos_tags)):
            if pos == 'v':  # 动词
                # 查找主语和宾语
                subject = self.find_subject(words, pos_tags, i)
                object = self.find_object(words, pos_tags, i)
                
                if subject and object:
                    relation = {
                        'source': subject,
                        'target': object,
                        'relation_type': word,
                        'sentence': sentence,
                        'confidence': 0.6,
                        'extraction_method': 'dependency'
                    }
                    relations.append(relation)
        
        return relations
    
    def find_subject(self, words: List[str], pos_tags: List[str], verb_index: int) -> str:
        """查找主语"""
        # 在动词前查找主语
        for i in range(verb_index - 1, -1, -1):
            if pos_tags[i] in ['n', 'nr', 'ns', 'nt']:
                return words[i]
        return ''
    
    def find_object(self, words: List[str], pos_tags: List[str], verb_index: int) -> str:
        """查找宾语"""
        # 在动词后查找宾语
        for i in range(verb_index + 1, len(words)):
            if pos_tags[i] in ['n', 'nr', 'ns', 'nt']:
                return words[i]
        return ''
    
    def build_network_from_relations(self, relations: List[Dict], threshold: float = 0.5) -> nx.Graph:
        """从关系数据构建网络"""
        G = nx.Graph()
        
        # 添加节点和边
        for relation in relations:
            if relation['confidence'] >= threshold:
                source = relation['source']
                target = relation['target']
                
                # 添加节点
                if not G.has_node(source):
                    G.add_node(source, entity_type=self.identify_entity_type(source))
                if not G.has_node(target):
                    G.add_node(target, entity_type=self.identify_entity_type(target))
                
                # 添加边
                if G.has_edge(source, target):
                    # 增加边权重
                    G[source][target]['weight'] += 1
                    G[source][target]['relations'].append(relation)
                else:
                    G.add_edge(source, target, 
                              weight=1,
                              relations=[relation],
                              relation_types=[relation['relation_type']])
        
        return G
    
    def identify_entity_type(self, entity: str) -> str:
        """识别实体类型"""
        for entity_type in self.entity_types:
            if entity_type in entity:
                return entity_type
        
        # 使用词性标注判断
        words = list(jieba.cut(entity))
        pos_tags = [flag for word, flag in pseg.cut(entity)]
        
        for pos in pos_tags:
            if pos == 'nr':
                return '人物'
            elif pos == 'ns':
                return '地点'
            elif pos == 'nt':
                return '组织'
        
        return '未知'
    
    def filter_relations_by_confidence(self, relations: List[Dict], threshold: float = 0.6) -> List[Dict]:
        """按置信度过滤关系"""
        return [rel for rel in relations if rel['confidence'] >= threshold]
    
    def resolve_entity_names(self, relations: List[Dict]) -> List[Dict]:
        """解析实体名称（处理别名、简称等）"""
        # 构建实体名称映射
        entity_mapping = {}
        
        # 收集所有实体
        all_entities = set()
        for relation in relations:
            all_entities.add(relation['source'])
            all_entities.add(relation['target'])
        
        # 简化的实体名称解析
        for entity in all_entities:
            # 处理常见的别名情况
            normalized_name = self.normalize_entity_name(entity)
            if normalized_name != entity:
                entity_mapping[entity] = normalized_name
        
        # 应用名称映射
        for relation in relations:
            if relation['source'] in entity_mapping:
                relation['source'] = entity_mapping[relation['source']]
            if relation['target'] in entity_mapping:
                relation['target'] = entity_mapping[relation['target']]
        
        return relations
    
    def normalize_entity_name(self, name: str) -> str:
        """标准化实体名称"""
        # 去除常见的称谓
        titles = ['老师', '教授', '博士', '先生', '女士', '同学', '同事']
        for title in titles:
            if name.endswith(title):
                return name[:-len(title)]
        
        # 处理简称情况
        abbreviations = {
            '北京大学': '北大',
            '清华大学': '清华',
            '中国人民大学': '人大'
        }
        
        for full_name, abbrev in abbreviations.items():
            if name == full_name:
                return abbrev
            if name == abbrev:
                return full_name
        
        return name

# 使用示例
if __name__ == "__main__":
    extractor = InterviewRelationExtractor()
    
    # 示例访谈文本
    interview_text = """
    我和我的导师张教授关系很好，他经常指导我的研究。我的同学李明也和张教授有合作关系。
    我们实验室的王老师支持我们的研究项目。我和李明经常讨论学术问题，互相帮助。
    """
    
    # 提取关系
    relations = extractor.extract_relations_from_text(interview_text)
    
    # 过滤低置信度关系
    filtered_relations = extractor.filter_relations_by_confidence(relations, 0.5)
    
    # 解析实体名称
    resolved_relations = extractor.resolve_entity_names(filtered_relations)
    
    # 构建网络
    G = extractor.build_network_from_relations(resolved_relations)
    
    print(f"提取到 {len(relations)} 个关系")
    print(f"过滤后保留 {len(filtered_relations)} 个关系")
    print(f"构建的网络有 {G.number_of_nodes()} 个节点，{G.number_of_edges()} 条边")
```

### 第三步：数据质量验证
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
import networkx as nx

class NetworkDataValidator:
    def __init__(self):
        self.validation_results = {}
        self.quality_metrics = {}
        
    def validate_matrix_format(self, matrix: np.ndarray, node_names: List[str]) -> Dict:
        """验证矩阵格式"""
        results = {
            'is_valid': True,
            'errors': [],
            'warnings': []
        }
        
        # 检查矩阵维度
        if matrix.ndim != 2:
            results['is_valid'] = False
            results['errors'].append('矩阵必须是二维的')
        
        # 检查矩阵是否为方阵
        if matrix.shape[0] != matrix.shape[1]:
            results['is_valid'] = False
            results['errors'].append('矩阵必须是方阵')
        
        # 检查节点名称数量
        if len(node_names) != matrix.shape[0]:
            results['is_valid'] = False
            results['errors'].append('节点名称数量与矩阵维度不匹配')
        
        # 检查数据类型
        if not np.issubdtype(matrix.dtype, np.number):
            results['warnings'].append('矩阵数据类型不是数值类型')
        
        # 检查对角线元素
        diagonal_elements = np.diag(matrix)
        if np.any(diagonal_elements != 0):
            results['warnings'].append('对角线元素不为0，可能存在自环')
        
        return results
    
    def check_missing_values(self, matrix: np.ndarray) -> Dict:
        """检查缺失值"""
        results = {
            'has_missing': False,
            'missing_count': 0,
            'missing_positions': [],
            'missing_percentage': 0.0
        }
        
        missing_positions = np.argwhere(np.isnan(matrix))
        
        if len(missing_positions) > 0:
            results['has_missing'] = True
            results['missing_count'] = len(missing_positions)
            results['missing_positions'] = missing_positions.tolist()
            results['missing_percentage'] = len(missing_positions) / matrix.size * 100
        
        return results
    
    def detect_outliers(self, matrix: np.ndarray) -> Dict:
        """检测异常值"""
        results = {
            'has_outliers': False,
            'outlier_count': 0,
            'outlier_positions': [],
            'outlier_values': []
        }
        
        # 使用IQR方法检测异常值
        flattened = matrix.flatten()
        flattened = flattened[flattened != 0]  # 排除0值
        
        if len(flattened) > 0:
            Q1 = np.percentile(flattened, 25)
            Q3 = np.percentile(flattened, 75)
            IQR = Q3 - Q1
            
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outlier_mask = (matrix < lower_bound) | (matrix > upper_bound)
            outlier_positions = np.argwhere(outlier_mask)
            
            if len(outlier_positions) > 0:
                results['has_outliers'] = True
                results['outlier_count'] = len(outlier_positions)
                results['outlier_positions'] = outlier_positions.tolist()
                results['outlier_values'] = matrix[outlier_mask].tolist()
        
        return results
    
    def check_network_connectivity(self, matrix: np.ndarray) -> Dict:
        """检查网络连通性"""
        G = nx.from_numpy_array(matrix)
        
        results = {
            'is_connected': nx.is_connected(G),
            'components': nx.number_connected_components(G),
            'largest_component_size': 0,
            'isolated_nodes': list(nx.isolates(G))
        }
        
        if not results['is_connected']:
            components = list(nx.connected_components(G))
            largest_component = max(components, key=len)
            results['largest_component_size'] = len(largest_component)
        
        return results
    
    def calculate_density_metrics(self, matrix: np.ndarray) -> Dict:
        """计算网络密度指标"""
        G = nx.from_numpy_array(matrix)
        
        results = {
            'density': nx.density(G),
            'average_degree': 0,
            'degree_std': 0,
            'clustering_coefficient': 0
        }
        
        if G.number_of_nodes() > 0:
            degrees = dict(G.degree())
            degree_values = list(degrees.values())
            
            results['average_degree'] = np.mean(degree_values)
            results['degree_std'] = np.std(degree_values)
            results['clustering_coefficient'] = nx.average_clustering(G)
        
        return results
    
    def validate_data_consistency(self, matrix: np.ndarray, node_attributes: Dict) -> Dict:
        """验证数据一致性"""
        results = {
            'is_consistent': True,
            'inconsistencies': []
        }
        
        # 检查节点数量一致性
        if len(node_attributes) != matrix.shape[0]:
            results['is_consistent'] = False
            results['inconsistencies'].append(
                f'节点属性数量({len(node_attributes)})与矩阵维度({matrix.shape[0]})不一致'
            )
        
        # 检查节点名称一致性
        matrix_nodes = set(range(matrix.shape[0]))
        attribute_nodes = set(node_attributes.keys())
        
        if matrix_nodes != attribute_nodes:
            results['is_consistent'] = False
            results['inconsistencies'].append('矩阵节点与属性节点不一致')
        
        return results
    
    def generate_quality_report(self, matrix: np.ndarray, node_names: List[str], 
                              node_attributes: Dict = None) -> Dict:
        """生成数据质量报告"""
        report = {
            'summary': {
                'total_nodes': len(node_names),
                'matrix_shape': matrix.shape,
                'data_type': str(matrix.dtype)
            },
            'validation_results': {},
            'quality_metrics': {},
            'recommendations': []
        }
        
        # 矩阵格式验证
        format_validation = self.validate_matrix_format(matrix, node_names)
        report['validation_results']['matrix_format'] = format_validation
        
        # 缺失值检查
        missing_check = self.check_missing_values(matrix)
        report['validation_results']['missing_values'] = missing_check
        
        # 异常值检测
        outlier_check = self.detect_outliers(matrix)
        report['validation_results']['outliers'] = outlier_check
        
        # 网络连通性检查
        connectivity_check = self.check_network_connectivity(matrix)
        report['validation_results']['connectivity'] = connectivity_check
        
        # 密度指标计算
        density_metrics = self.calculate_density_metrics(matrix)
        report['quality_metrics']['density'] = density_metrics
        
        # 数据一致性验证
        if node_attributes:
            consistency_check = self.validate_data_consistency(matrix, node_attributes)
            report['validation_results']['consistency'] = consistency_check
        
        # 生成建议
        report['recommendations'] = self.generate_recommendations(report)
        
        return report
    
    def generate_recommendations(self, report: Dict) -> List[str]:
        """生成改进建议"""
        recommendations = []
        
        # 基于验证结果生成建议
        validation_results = report['validation_results']
        
        # 缺失值建议
        if validation_results['missing_values']['has_missing']:
            missing_pct = validation_results['missing_values']['missing_percentage']
            if missing_pct < 5:
                recommendations.append('缺失值较少，建议使用均值或中位数填充')
            elif missing_pct < 20:
                recommendations.append('缺失值适中，建议使用插值方法填充')
            else:
                recommendations.append('缺失值较多，建议重新收集数据或考虑删除相关节点')
        
        # 异常值建议
        if validation_results['outliers']['has_outliers']:
            recommendations.append('发现异常值，建议检查数据来源并考虑修正或删除')
        
        # 连通性建议
        if not validation_results['connectivity']['is_connected']:
            components = validation_results['connectivity']['components']
            if components > 1:
                recommendations.append(f'网络不连通，有{components}个连通分量，建议检查数据完整性')
        
        # 密度建议
        density = report['quality_metrics']['density']['density']
        if density < 0.1:
            recommendations.append('网络密度较低，可能导致分析结果不稳定')
        elif density > 0.9:
            recommendations.append('网络密度较高，可能存在冗余连接')
        
        return recommendations

# 使用示例
if __name__ == "__main__":
    validator = NetworkDataValidator()
    
    # 示例矩阵和节点名称
    matrix = np.array([
        [0, 1, 1, 0],
        [1, 0, 1, 1],
        [1, 1, 0, 0],
        [0, 1, 0, 0]
    ])
    node_names = ['A', 'B', 'C', 'D']
    node_attributes = {
        0: {'name': 'A', 'age': 25},
        1: {'name': 'B', 'age': 30},
        2: {'name': 'C', 'age': 28},
        3: {'name': 'D', 'age': 35}
    }
    
    # 生成质量报告
    quality_report = validator.generate_quality_report(matrix, node_names, node_attributes)
    
    print("数据质量报告：")
    print(json.dumps(quality_report, ensure_ascii=False, indent=2))
```

## 质量保证

### 数据提取质量检查
- [ ] 关系识别准确率 > 85%
- [ ] 实体名称解析正确率 > 90%
- [ ] 关系类型分类准确率 > 80%
- [ ] 置信度评估合理
- [ ] 人工验证样本充分

### 矩阵构建质量检查
- [ ] 矩阵维度正确
- [ ] 节点映射准确
- [ ] 权重计算合理
- [ ] 对称性处理正确
- [ ] 数据类型转换无误

### 数据清洗质量检查
- [ ] 缺失值处理合理
- [ ] 异常值检测准确
- [ ] 数据一致性良好
- [ ] 完整性评估全面
- [ ] 质量控制有效

## 输出格式

### 网络数据输出格式
```json
{
  "network_data": {
    "nodes": [
      {
        "id": "node_1",
        "name": "节点1",
        "attributes": {
          "type": "人物",
          "age": 25,
          "gender": "男"
        }
      }
    ],
    "edges": [
      {
        "source": "node_1",
        "target": "node_2",
        "weight": 1.0,
        "relationship_type": "朋友",
        "attributes": {
          "duration": "5年",
          "frequency": "经常"
        }
      }
    ]
  },
  "matrix_data": {
    "adjacency_matrix": [[0, 1, 0], [1, 0, 1], [0, 1, 0]],
    "node_names": ["节点1", "节点2", "节点3"]
  },
  "quality_report": {
    "validation_results": {...},
    "quality_metrics": {...},
    "recommendations": [...]
  }
}
```

---

**此网络数据处理技能专门为中文社会网络研究设计，提供从原始数据到标准化矩阵的完整数据处理支持，确保网络数据的质量和可用性。**