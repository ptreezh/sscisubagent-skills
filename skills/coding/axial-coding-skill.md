---
name: performing-axial-coding
description: 执行扎根理论的轴心编码过程，包括范畴识别、属性维度分析、关系建立和Paradigm构建。当需要将开放编码的结果整合为系统性的范畴体系，建立概念间的逻辑关系时使用此技能。
---

# 轴心编码技能

专门用于扎根理论研究的轴心编码阶段，将开放编码产生的概念整合为系统性的范畴体系，并建立范畴间的逻辑关系。

## 核心能力

### 1. 范畴识别与构建
- **概念聚类**：将相似概念归类为同一范畴
- **范畴命名**：为每个范畴提供准确的命名
- **范畴定义**：明确定义每个范畴的内涵和外延
- **范畴层级**：建立范畴的层级结构

### 2. 属性与维度分析
- **属性识别**：识别每个范畴的核心属性
- **维度确定**：确定每个属性的变化维度
- **维度定位**：在维度上定位具体案例
- **属性关系**：分析属性间的关系

### 3. 范畴关系建立
- **因果分析**：建立范畴间的因果关系
- **条件关系**：识别影响范畴的条件因素
- **策略关系**：分析应对策略和结果关系
- **互动关系**：分析范畴间的互动模式

### 4. Paradigm构建
- **条件维度**：识别导致现象的条件
- **行动/互动**：分析采取的行动或互动
- **结果维度**：分析行动的结果
- **整合模型**：构建完整的Paradigm模型

## 处理流程

### 第一步：概念聚类和范畴识别
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from typing import List, Dict, Tuple
import jieba
import jieba.analyse

class CategoryBuilder:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(max_features=1000)
        self.clusters = {}
        
    def prepare_concepts(self, concepts: List[Dict]) -> Tuple[List[str], List[str]]:
        """准备概念数据用于聚类"""
        concept_names = [concept['code'] for concept in concepts]
        concept_definitions = [concept['definition'] for concept in concepts]
        return concept_names, concept_definitions
    
    def extract_features(self, definitions: List[str]) -> np.ndarray:
        """提取特征向量"""
        # 使用TF-IDF提取特征
        tfidf_matrix = self.vectorizer.fit_transform(definitions)
        return tfidf_matrix.toarray()
    
    def cluster_concepts(self, features: np.ndarray, n_clusters: int = 8) -> np.ndarray:
        """聚类概念"""
        kmeans = KMeans(n_clusters=n_clusters, random_state=42)
        clusters = kmeans.fit_predict(features)
        return clusters
    
    def build_categories(self, concepts: List[Dict], clusters: np.ndarray) -> Dict:
        """构建范畴"""
        categories = {}
        
        for cluster_id in np.unique(clusters):
            cluster_concepts = [concepts[i] for i in range(len(concepts)) if clusters[i] == cluster_id]
            
            # 提取范畴名称
            category_name = self.generate_category_name(cluster_concepts)
            
            # 生成范畴定义
            category_definition = self.generate_category_definition(cluster_concepts)
            
            categories[category_name] = {
                'name': category_name,
                'definition': category_definition,
                'concepts': cluster_concepts,
                'concept_count': len(cluster_concepts),
                'attributes': self.extract_attributes(cluster_concepts)
            }
        
        return categories
    
    def generate_category_name(self, concepts: List[Dict]) -> str:
        """生成范畴名称"""
        # 提取所有概念名称的关键词
        all_keywords = []
        for concept in concepts:
            keywords = jieba.analyse.extract_tags(concept['definition'], topK=3)
            all_keywords.extend(keywords)
        
        # 统计词频
        keyword_freq = {}
        for keyword in all_keywords:
            keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
        
        # 选择频率最高的关键词作为范畴名称
        if keyword_freq:
            top_keyword = max(keyword_freq, key=keyword_freq.get)
            return f"{top_keyword}相关"
        
        return "未命名范畴"
    
    def generate_category_definition(self, concepts: List[Dict]) -> str:
        """生成范畴定义"""
        concept_codes = [concept['code'] for concept in concepts]
        concept_definitions = [concept['definition'] for concept in concepts]
        
        definition = f"包含以下概念：{', '.join(concept_codes)}。\n\n"
        definition += "这些概念共同描述了："
        
        # 提取共同主题
        common_themes = self.extract_common_themes(concept_definitions)
        if common_themes:
            definition += f"{'、'.join(common_themes)}等相关现象。"
        else:
            definition += "相关的行为和体验。"
        
        return definition
    
    def extract_common_themes(self, definitions: List[str]) -> List[str]:
        """提取共同主题"""
        # 合并所有定义
        all_text = ' '.join(definitions)
        
        # 提取关键词
        keywords = jieba.analyse.extract_tags(all_text, topK=10)
        
        return keywords[:5]  # 返回前5个关键词
    
    def extract_attributes(self, concepts: List[Dict]) -> List[Dict]:
        """提取范畴属性"""
        attributes = []
        
        # 分析概念的共同特征
        common_patterns = self.find_common_patterns(concepts)
        
        for pattern in common_patterns:
            attribute = {
                'name': pattern['name'],
                'definition': pattern['definition'],
                'dimensions': self.identify_dimensions(pattern)
            }
            attributes.append(attribute)
        
        return attributes
    
    def find_common_patterns(self, concepts: List[Dict]) -> List[Dict]:
        """寻找共同模式"""
        patterns = []
        
        # 分析行动模式
        action_patterns = self.analyze_action_patterns(concepts)
        patterns.extend(action_patterns)
        
        # 分析情感模式
        emotion_patterns = self.analyze_emotion_patterns(concepts)
        patterns.extend(emotion_patterns)
        
        # 分析关系模式
        relation_patterns = self.analyze_relation_patterns(concepts)
        patterns.extend(relation_patterns)
        
        return patterns
    
    def analyze_action_patterns(self, concepts: List[Dict]) -> List[Dict]:
        """分析行动模式"""
        action_keywords = ['寻求', '建立', '适应', '应对', '处理', '解决', '克服']
        patterns = []
        
        for keyword in action_keywords:
            related_concepts = [c for c in concepts if keyword in c['code']]
            if len(related_concepts) >= 2:
                patterns.append({
                    'name': f'{keyword}行为',
                    'definition': f'与{keyword}相关的各种行为表现',
                    'related_concepts': related_concepts
                })
        
        return patterns
    
    def analyze_emotion_patterns(self, concepts: List[Dict]) -> List[Dict]:
        """分析情感模式"""
        emotion_keywords = ['感受', '体验', '情绪', '态度', '认知']
        patterns = []
        
        for keyword in emotion_keywords:
            related_concepts = [c for c in concepts if keyword in c['definition']]
            if len(related_concepts) >= 2:
                patterns.append({
                    'name': f'{keyword}体验',
                    'definition': f'与{keyword}相关的各种体验',
                    'related_concepts': related_concepts
                })
        
        return patterns
    
    def analyze_relation_patterns(self, concepts: List[Dict]) -> List[Dict]:
        """分析关系模式"""
        relation_keywords = ['关系', '互动', '联系', '影响', '作用']
        patterns = []
        
        for keyword in relation_keywords:
            related_concepts = [c for c in concepts if keyword in c['definition']]
            if len(related_concepts) >= 2:
                patterns.append({
                    'name': f'{keyword}模式',
                    'definition': f'与{keyword}相关的各种模式',
                    'related_concepts': related_concepts
                })
        
        return patterns
    
    def identify_dimensions(self, pattern: Dict) -> List[Dict]:
        """识别维度"""
        dimensions = []
        
        if '行为' in pattern['name']:
            dimensions = [
                {'name': '主动性', 'range': '被动到主动'},
                {'name': '频率', 'range': '偶尔到经常'},
                {'name': '强度', 'range': '弱到强'}
            ]
        elif '体验' in pattern['name']:
            dimensions = [
                {'name': '情感强度', 'range': '弱到强'},
                {'name': '持续时间', 'range': '短暂到持久'},
                {'name': '影响程度', 'range': '轻微到深刻'}
            ]
        
        return dimensions

# 使用示例
if __name__ == "__main__":
    # 示例概念数据
    concepts = [
        {'code': '寻求支持', 'definition': '主动向他人寻求帮助和支持'},
        {'code': '获得帮助', 'definition': '从他人那里得到实际帮助'},
        {'code': '提供帮助', 'definition': '向他人提供支持和帮助'},
        {'code': '建立关系', 'definition': '与他人建立良好的关系'},
        {'code': '维护关系', 'definition': '维护和巩固已有的关系'}
    ]
    
    builder = CategoryBuilder()
    concept_names, concept_definitions = builder.prepare_concepts(concepts)
    features = builder.extract_features(concept_definitions)
    clusters = builder.cluster_concepts(features, n_clusters=2)
    categories = builder.build_categories(concepts, clusters)
    
    print("构建的范畴：")
    for category_name, category_data in categories.items():
        print(f"\n范畴: {category_name}")
        print(f"定义: {category_data['definition']}")
        print(f"包含概念: {[c['code'] for c in category_data['concepts']]}")
```

### 第二步：属性维度分析
```javascript
// 属性维度分析
class DimensionAnalyzer {
    constructor() {
        this.dimensions = new Map();
        this.dimensionTypes = ['连续型', '离散型', '分类型', '顺序型'];
    }
    
    addDimension(categoryName, dimensionName, dimensionType, range) {
        if (!this.dimensions.has(categoryName)) {
            this.dimensions.set(categoryName, []);
        }
        
        this.dimensions.get(categoryName).push({
            name: dimensionName,
            type: dimensionType,
            range: range,
            values: []
        });
    }
    
    locateOnDimension(categoryName, dimensionName, value, caseId) {
        const categoryDimensions = this.dimensions.get(categoryName);
        const dimension = categoryDimensions.find(d => d.name === dimensionName);
        
        if (dimension) {
            dimension.values.push({
                caseId: caseId,
                value: value,
                position: this.calculatePosition(value, dimension.range)
            });
        }
    }
    
    calculatePosition(value, range) {
        // 计算在维度上的位置
        if (range.includes('到')) {
            const [min, max] = range.split('到').map(s => s.trim());
            return this.normalizeValue(value, min, max);
        }
        return value;
    }
    
    normalizeValue(value, min, max) {
        // 将值标准化到0-1范围
        const numValue = parseFloat(value);
        const numMin = parseFloat(min);
        const numMax = parseFloat(max);
        
        if (numMax - numMin === 0) return 0.5;
        return (numValue - numMin) / (numMax - numMin);
    }
    
    analyzeDimensionDistribution(categoryName, dimensionName) {
        const categoryDimensions = this.dimensions.get(categoryName);
        const dimension = categoryDimensions.find(d => d.name === dimensionName);
        
        if (!dimension || dimension.values.length === 0) {
            return null;
        }
        
        const values = dimension.values.map(v => v.position);
        const distribution = {
            mean: this.calculateMean(values),
            median: this.calculateMedian(values),
            std: this.calculateStd(values),
            range: [Math.min(...values), Math.max(...values)],
            distribution: this.createDistribution(values)
        };
        
        return distribution;
    }
    
    calculateMean(values) {
        return values.reduce((sum, val) => sum + val, 0) / values.length;
    }
    
    calculateMedian(values) {
        const sorted = [...values].sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        return sorted.length % 2 === 0 ? 
            (sorted[mid - 1] + sorted[mid]) / 2 : sorted[mid];
    }
    
    calculateStd(values) {
        const mean = this.calculateMean(values);
        const squaredDiffs = values.map(val => Math.pow(val - mean, 2));
        const avgSquaredDiff = this.calculateMean(squaredDiffs);
        return Math.sqrt(avgSquaredDiff);
    }
    
    createDistribution(values, bins = 5) {
        const min = Math.min(...values);
        const max = Math.max(...values);
        const binWidth = (max - min) / bins;
        
        const distribution = [];
        for (let i = 0; i < bins; i++) {
            const binStart = min + i * binWidth;
            const binEnd = binStart + binWidth;
            const count = values.filter(val => 
                val >= binStart && (i === bins - 1 ? val <= binEnd : val < binEnd)
            ).length;
            
            distribution.push({
                range: `${binStart.toFixed(2)}-${binEnd.toFixed(2)}`,
                count: count,
                percentage: (count / values.length * 100).toFixed(1)
            });
        }
        
        return distribution;
    }
    
    generateDimensionReport(categoryName) {
        const categoryDimensions = this.dimensions.get(categoryName);
        const report = {
            category: categoryName,
            dimensions: []
        };
        
        for (const dimension of categoryDimensions) {
            const distribution = this.analyzeDimensionDistribution(categoryName, dimension.name);
            
            report.dimensions.push({
                name: dimension.name,
                type: dimension.type,
                range: dimension.range,
                sampleSize: dimension.values.length,
                distribution: distribution
            });
        }
        
        return report;
    }
}

// 使用示例
const analyzer = new DimensionAnalyzer();

// 添加维度
analyzer.addDimension('社会支持', '主动性', '连续型', '被动到主动');
analyzer.addDimension('社会支持', '频率', '连续型', '偶尔到经常');
analyzer.addDimension('社会支持', '来源', '分类型', '家庭、朋友、老师、同学');

// 定位案例在维度上
analyzer.locateOnDimension('社会支持', '主动性', '0.8', '案例1');
analyzer.locateOnDimension('社会支持', '主动性', '0.3', '案例2');
analyzer.locateOnDimension('社会支持', '频率', '0.9', '案例1');
analyzer.locateOnDimension('社会支持', '频率', '0.4', '案例2');

// 生成维度报告
const report = analyzer.generateDimensionReport('社会支持');
console.log('维度分析报告:', JSON.stringify(report, null, 2));
```

### 第三步：范畴关系建立
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import json

class CategoryRelationBuilder:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.relation_types = ['因果关系', '条件关系', '策略关系', '互动关系', '包含关系']
        
    def add_category(self, category_name: str, category_data: Dict):
        """添加范畴节点"""
        self.graph.add_node(category_name, **category_data)
    
    def add_relation(self, category1: str, category2: str, relation_type: str, 
                    strength: float, evidence: str):
        """添加范畴关系"""
        self.graph.add_edge(category1, category2, 
                           relation_type=relation_type,
                           strength=strength,
                           evidence=evidence)
    
    def identify_causal_relations(self, categories: Dict) -> List[Tuple]:
        """识别因果关系"""
        causal_relations = []
        
        # 基于时间序列识别因果关系
        for cat1_name, cat1_data in categories.items():
            for cat2_name, cat2_data in categories.items():
                if cat1_name != cat2_name:
                    causal_strength = self.calculate_causal_strength(cat1_data, cat2_data)
                    if causal_strength > 0.6:
                        causal_relations.append((cat1_name, cat2_name, '因果关系', causal_strength))
        
        return causal_relations
    
    def calculate_causal_strength(self, cat1_data: Dict, cat2_data: Dict) -> float:
        """计算因果强度"""
        # 基于概念重叠和时间顺序计算
        concepts1 = set(c['code'] for c in cat1_data['concepts'])
        concepts2 = set(c['code'] for c in cat2_data['concepts'])
        
        # 检查是否有时间序列关系
        time_keywords1 = ['开始', '首先', '初期', '早期']
        time_keywords2 = ['然后', '接着', '后期', '结果']
        
        time1_score = sum(1 for concept in concepts1 if any(kw in concept for kw in time_keywords1))
        time2_score = sum(1 for concept in concepts2 if any(kw in concept for kw in time_keywords2))
        
        # 计算概念重叠度
        overlap = len(concepts1.intersection(concepts2))
        union = len(concepts1.union(concepts2))
        overlap_score = overlap / union if union > 0 else 0
        
        # 综合评分
        causal_strength = (time1_score + time2_score) * 0.6 + overlap_score * 0.4
        
        return min(causal_strength, 1.0)
    
    def identify_conditional_relations(self, categories: Dict) -> List[Tuple]:
        """识别条件关系"""
        conditional_relations = []
        
        condition_keywords = ['如果', '当', '在', '由于', '因为']
        result_keywords = ['所以', '因此', '导致', '造成', '引起']
        
        for cat1_name, cat1_data in categories.items():
            for cat2_name, cat2_data in categories.items():
                if cat1_name != cat2_name:
                    condition_strength = self.calculate_conditional_strength(
                        cat1_data, cat2_data, condition_keywords, result_keywords
                    )
                    if condition_strength > 0.5:
                        conditional_relations.append((cat1_name, cat2_name, '条件关系', condition_strength))
        
        return conditional_relations
    
    def calculate_conditional_strength(self, cat1_data: Dict, cat2_data: Dict, 
                                    condition_keywords: List, result_keywords: List) -> float:
        """计算条件强度"""
        concepts1 = [c['code'] for c in cat1_data['concepts']]
        concepts2 = [c['code'] for c in cat2_data['concepts']]
        
        condition_score = sum(1 for concept in concepts1 if any(kw in concept for kw in condition_keywords))
        result_score = sum(1 for concept in concepts2 if any(kw in concept for kw in result_keywords))
        
        total_concepts = len(concepts1) + len(concepts2)
        conditional_strength = (condition_score + result_score) / total_concepts
        
        return min(conditional_strength, 1.0)
    
    def build_paradigm(self, central_category: str) -> Dict:
        """构建Paradigm模型"""
        paradigm = {
            'central_category': central_category,
            'conditions': [],
            'actions': [],
            'consequences': []
        }
        
        # 识别条件（指向中心范畴的关系）
        for predecessor in self.graph.predecessors(central_category):
            edge_data = self.graph[predecessor][central_category]
            if edge_data['relation_type'] in ['条件关系', '因果关系']:
                paradigm['conditions'].append({
                    'category': predecessor,
                    'type': edge_data['relation_type'],
                    'strength': edge_data['strength']
                })
        
        # 识别行动（中心范畴的属性）
        central_data = self.graph.nodes[central_category]
        if 'attributes' in central_data:
            paradigm['actions'] = [
                {
                    'attribute': attr['name'],
                    'definition': attr['definition']
                }
                for attr in central_data['attributes']
            ]
        
        # 识别结果（从中心范畴指向的关系）
        for successor in self.graph.successors(central_category):
            edge_data = self.graph[central_category][successor]
            if edge_data['relation_type'] in ['因果关系', '策略关系']:
                paradigm['consequences'].append({
                    'category': successor,
                    'type': edge_data['relation_type'],
                    'strength': edge_data['strength']
                })
        
        return paradigm
    
    def visualize_relations(self, output_file: str = 'category_relations.png'):
        """可视化范畴关系"""
        plt.figure(figsize=(12, 8))
        
        # 设置布局
        pos = nx.spring_layout(self.graph, k=2, iterations=50)
        
        # 绘制节点
        nx.draw_networkx_nodes(self.graph, pos, node_color='lightblue', 
                              node_size=3000, alpha=0.8)
        
        # 绘制边
        edge_colors = []
        for u, v, data in self.graph.edges(data=True):
            if data['relation_type'] == '因果关系':
                edge_colors.append('red')
            elif data['relation_type'] == '条件关系':
                edge_colors.append('blue')
            elif data['relation_type'] == '策略关系':
                edge_colors.append('green')
            else:
                edge_colors.append('gray')
        
        nx.draw_networkx_edges(self.graph, pos, edge_color=edge_colors, 
                              width=2, alpha=0.6, arrows=True, arrowsize=20)
        
        # 绘制标签
        nx.draw_networkx_labels(self.graph, pos, font_size=10, font_weight='bold')
        
        # 添加图例
        legend_elements = [
            plt.Line2D([0], [0], color='red', lw=2, label='因果关系'),
            plt.Line2D([0], [0], color='blue', lw=2, label='条件关系'),
            plt.Line2D([0], [0], color='green', lw=2, label='策略关系'),
            plt.Line2D([0], [0], color='gray', lw=2, label='其他关系')
        ]
        plt.legend(handles=legend_elements, loc='upper right')
        
        plt.title('范畴关系网络图', fontsize=16)
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.show()
    
    def export_relations(self, filename: str):
        """导出关系数据"""
        data = {
            'nodes': [],
            'edges': []
        }
        
        # 导出节点数据
        for node, node_data in self.graph.nodes(data=True):
            data['nodes'].append({
                'id': node,
                **node_data
            })
        
        # 导出边数据
        for u, v, edge_data in self.graph.edges(data=True):
            data['edges'].append({
                'source': u,
                'target': v,
                **edge_data
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# 使用示例
if __name__ == "__main__":
    # 示例范畴数据
    categories = {
        '社会支持': {
            'concepts': [
                {'code': '寻求支持', 'definition': '主动向他人寻求帮助'},
                {'code': '获得帮助', 'definition': '从他人那里得到帮助'}
            ]
        },
        '学习适应': {
            'concepts': [
                {'code': '适应策略', 'definition': '制定适应学习的策略'},
                {'code': '调整方法', 'definition': '调整学习方法'}
            ]
        },
        '学业成绩': {
            'concepts': [
                {'code': '提高成绩', 'definition': '学习成绩的提升'},
                {'code': '保持稳定', 'definition': '保持成绩稳定'}
            ]
        }
    }
    
    builder = CategoryRelationBuilder()
    
    # 添加范畴
    for cat_name, cat_data in categories.items():
        builder.add_category(cat_name, cat_data)
    
    # 识别关系
    causal_relations = builder.identify_causal_relations(categories)
    conditional_relations = builder.identify_conditional_relations(categories)
    
    # 添加关系到图中
    for relation in causal_relations + conditional_relations:
        cat1, cat2, rel_type, strength = relation
        builder.add_relation(cat1, cat2, rel_type, strength, "基于数据分析")
    
    # 构建Paradigm
    paradigm = builder.build_paradigm('学习适应')
    print("Paradigm模型:", json.dumps(paradigm, ensure_ascii=False, indent=2))
    
    # 可视化关系
    builder.visualize_relations()
    
    # 导出数据
    builder.export_relations('category_relations.json')
```

## 质量保证

### 范畴构建质量检查
- [ ] 范畴命名准确且有意义
- [ ] 范畴定义清晰完整
- [ ] 概念归类合理有据
- [ ] 范畴层级结构清晰
- [ ] 范畴间区分度明确

### 属性维度质量检查
- [ ] 属性识别全面准确
- [ ] 维度定义合理
- [ ] 维度范围适当
- [ ] 案例定位准确
- [ ] 分布分析科学

### 关系建立质量检查
- [ ] 关系类型判断准确
- [ ] 关系强度评估合理
- [ ] 关系证据充分
- [ ] 关系方向正确
- [ ] 关系网络完整

### Paradigm构建质量检查
- [ ] 条件识别完整
- [ ] 行动描述准确
- [ ] 结果分析全面
- [ ] 逻辑链条清晰
- [ ] 理论意义明确

## 输出格式

### 范畴体系格式
```json
{
  "categories": {
    "社会支持": {
      "name": "社会支持",
      "definition": "包含寻求支持、获得帮助等概念，描述了个体在社会互动中的支持系统",
      "concepts": [...],
      "attributes": [
        {
          "name": "主动性",
          "definition": "个体寻求支持的主动程度",
          "dimensions": [
            {
              "name": "主动性",
              "range": "被动到主动",
              "distribution": {...}
            }
          ]
        }
      ]
    }
  },
  "relations": [...],
  "paradigms": {...}
}
```

---

**此轴心编码技能专门为中文质性研究设计，提供从概念聚类到Paradigm构建的完整轴心编码支持，确保范畴体系的科学性和系统性。**