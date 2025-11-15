---
name: performing-selective-coding
description: 执行扎根理论的选择式编码过程，包括核心范畴识别、故事线构建、理论框架整合和理论饱和度检验。当需要整合所有范畴构建核心理论，形成完整的故事线和理论模型时使用此技能。
---

# 选择式编码技能

专门用于扎根理论研究的选择式编码阶段，将轴心编码构建的范畴体系整合为系统的理论框架，形成核心理论和故事线。

## 核心能力

### 1. 核心范畴识别
- **系统性检查**：全面检查所有范畴的重要性
- **解释力评估**：评估范畴对现象的解释能力
- **中心性分析**：分析范畴在网络中的中心地位
- **理论价值判断**：判断范畴的理论贡献价值
- **数据支持验证**：验证范畴的数据支持程度

### 2. 故事线构建
- **主线梳理**：梳理研究现象的核心发展脉络
- **关键事件识别**：识别重要的转折点和关键事件
- **角色关系明确**：明确各参与者的角色和关系
- **时间序列组织**：按时间顺序组织事件发展
- **因果关系链**：构建完整的因果关系链条

### 3. 理论框架整合
- **理论命题形成**：基于范畴关系形成理论命题
- **概念框架构建**：构建完整的概念框架体系
- **机制解释**：解释现象背后的作用机制
- **边界条件**：明确理论的适用边界和条件
- **实践意义**：阐述理论的实践指导意义

### 4. 理论饱和度检验
- **新概念检验**：检查是否还有新的重要概念
- **关系完善验证**：验证范畴关系的完善程度
- **案例充分性**：评估案例数据的充分性
- **理论完整性**：检验理论的完整性和一致性
- **补充需求分析**：分析是否需要补充数据

## 处理流程

### 第一步：核心范畴识别分析
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import networkx as nx
from typing import Dict, List, Tuple
import json

class CoreCategoryIdentifier:
    def __init__(self):
        self.categories = {}
        self.relation_graph = nx.DiGraph()
        self.importance_scores = {}
        
    def load_categories(self, categories: Dict):
        """加载范畴数据"""
        self.categories = categories
        
        # 构建关系图
        self.build_relation_graph()
    
    def build_relation_graph(self):
        """构建范畴关系图"""
        for cat_name, cat_data in self.categories.items():
            self.relation_graph.add_node(cat_name, **cat_data)
        
        # 基于概念重叠添加边
        for cat1_name, cat1_data in self.categories.items():
            for cat2_name, cat2_data in self.categories.items():
                if cat1_name != cat2_name:
                    similarity = self.calculate_concept_similarity(
                        cat1_data['concepts'], cat2_data['concepts']
                    )
                    if similarity > 0.3:  # 阈值可调
                        self.relation_graph.add_edge(
                            cat1_name, cat2_name, 
                            weight=similarity,
                            similarity=similarity
                        )
    
    def calculate_concept_similarity(self, concepts1: List, concepts2: List) -> float:
        """计算概念相似度"""
        codes1 = set(c['code'] for c in concepts1)
        codes2 = set(c['code'] for c in concepts2)
        
        intersection = len(codes1.intersection(codes2))
        union = len(codes1.union(codes2))
        
        return intersection / union if union > 0 else 0
    
    def calculate_centrality_scores(self) -> Dict:
        """计算中心性指标"""
        centrality_scores = {}
        
        # 度中心性
        degree_centrality = nx.degree_centrality(self.relation_graph)
        
        # 接近中心性
        closeness_centrality = nx.closeness_centrality(self.relation_graph)
        
        # 介数中心性
        betweenness_centrality = nx.betweenness_centrality(self.relation_graph)
        
        # PageRank
        pagerank = nx.pagerank(self.relation_graph)
        
        for category in self.categories.keys():
            centrality_scores[category] = {
                'degree': degree_centrality.get(category, 0),
                'closeness': closeness_centrality.get(category, 0),
                'betweenness': betweenness_centrality.get(category, 0),
                'pagerank': pagerank.get(category, 0)
            }
        
        return centrality_scores
    
    def calculate_explanatory_power(self, category: str) -> float:
        """计算解释力"""
        category_data = self.categories[category]
        
        # 概念数量权重
        concept_weight = len(category_data['concepts']) / 10  # 标准化
        
        # 关系数量权重
        relation_weight = len(list(self.relation_graph.neighbors(category))) / 5
        
        # 属性数量权重
        attribute_weight = len(category_data.get('attributes', [])) / 3
        
        # 数据支持权重（基于概念频次）
        data_support_weight = self.calculate_data_support(category)
        
        # 综合评分
        explanatory_power = (
            concept_weight * 0.3 +
            relation_weight * 0.3 +
            attribute_weight * 0.2 +
            data_support_weight * 0.2
        )
        
        return min(explanatory_power, 1.0)
    
    def calculate_data_support(self, category: str) -> float:
        """计算数据支持度"""
        category_data = self.categories[category]
        total_frequency = 0
        
        for concept in category_data['concepts']:
            frequency = concept.get('frequency', 1)
            total_frequency += frequency
        
        # 标准化到0-1范围
        return min(total_frequency / 50, 1.0)  # 假设50为高频阈值
    
    def calculate_theoretical_value(self, category: str) -> float:
        """计算理论价值"""
        category_data = self.categories[category]
        
        # 新颖性评分
        novelty_score = self.assess_novelty(category)
        
        # 抽象层次评分
        abstraction_score = self.assess_abstraction_level(category)
        
        # 普适性评分
        generality_score = self.assess_generality(category)
        
        # 综合理论价值
        theoretical_value = (
            novelty_score * 0.4 +
            abstraction_score * 0.3 +
            generality_score * 0.3
        )
        
        return theoretical_value
    
    def assess_novelty(self, category: str) -> float:
        """评估新颖性"""
        # 基于概念的独特性评估新颖性
        category_concepts = set(c['code'] for c in self.categories[category]['concepts'])
        
        # 计算与其他范畴的重叠度
        total_overlap = 0
        for other_category, other_data in self.categories.items():
            if other_category != category:
                other_concepts = set(c['code'] for c in other_data['concepts'])
                overlap = len(category_concepts.intersection(other_concepts))
                total_overlap += overlap
        
        # 重叠度越低，新颖性越高
        avg_overlap = total_overlap / (len(self.categories) - 1)
        novelty_score = 1 - min(avg_overlap / len(category_concepts), 1.0)
        
        return novelty_score
    
    def assess_abstraction_level(self, category: str) -> float:
        """评估抽象层次"""
        category_data = self.categories[category]
        
        # 基于概念定义的抽象程度评估
        abstraction_indicators = ['过程', '机制', '模式', '系统', '结构', '关系']
        definition_text = ' '.join([c['definition'] for c in category_data['concepts']])
        
        abstraction_count = sum(1 for indicator in abstraction_indicators 
                               if indicator in definition_text)
        
        return min(abstraction_count / len(abstraction_indicators), 1.0)
    
    def assess_generality(self, category: str) -> float:
        """评估普适性"""
        # 基于范畴的连接广度评估普适性
        connections = len(list(self.relation_graph.neighbors(category)))
        max_connections = len(self.categories) - 1
        
        return connections / max_connections if max_connections > 0 else 0
    
    def identify_core_categories(self, top_k: int = 3) -> List[Tuple]:
        """识别核心范畴"""
        # 计算各项指标
        centrality_scores = self.calculate_centrality_scores()
        
        # 综合评分
        comprehensive_scores = {}
        for category in self.categories.keys():
            explanatory_power = self.calculate_explanatory_power(category)
            theoretical_value = self.calculate_theoretical_value(category)
            centrality_score = centrality_scores[category]['pagerank']
            
            comprehensive_score = (
                explanatory_power * 0.4 +
                theoretical_value * 0.3 +
                centrality_score * 0.3
            )
            
            comprehensive_scores[category] = comprehensive_score
        
        # 排序并返回前k个
        sorted_categories = sorted(comprehensive_scores.items(), 
                                 key=lambda x: x[1], reverse=True)
        
        return sorted_categories[:top_k]
    
    def generate_core_category_report(self, category: str) -> Dict:
        """生成核心范畴报告"""
        centrality_scores = self.calculate_centrality_scores()
        
        report = {
            'category': category,
            'explanatory_power': self.calculate_explanatory_power(category),
            'theoretical_value': self.calculate_theoretical_value(category),
            'centrality_scores': centrality_scores[category],
            'data_support': self.calculate_data_support(category),
            'related_categories': list(self.relation_graph.neighbors(category)),
            'key_concepts': [c['code'] for c in self.categories[category]['concepts']],
            'recommendation': self.generate_recommendation(category)
        }
        
        return report
    
    def generate_recommendation(self, category: str) -> str:
        """生成推荐意见"""
        explanatory_power = self.calculate_explanatory_power(category)
        theoretical_value = self.calculate_theoretical_value(category)
        
        if explanatory_power > 0.8 and theoretical_value > 0.7:
            return "强烈推荐作为核心范畴，具有很强的解释力和理论价值"
        elif explanatory_power > 0.6 and theoretical_value > 0.5:
            return "推荐作为核心范畴，具有较好的解释力和理论价值"
        elif explanatory_power > 0.4 or theoretical_value > 0.4:
            return "可考虑作为辅助范畴，需要进一步验证"
        else:
            return "不建议作为核心范畴，解释力和理论价值有限"

# 使用示例
if __name__ == "__main__":
    # 示例范畴数据
    categories = {
        '学习适应': {
            'concepts': [
                {'code': '适应策略', 'definition': '制定适应学习的策略', 'frequency': 15},
                {'code': '调整方法', 'definition': '调整学习方法', 'frequency': 12},
                {'code': '克服困难', 'definition': '克服学习困难', 'frequency': 10}
            ],
            'attributes': [
                {'name': '主动性', 'definition': '主动适应的程度'},
                {'name': '灵活性', 'definition': '适应方法的灵活性'}
            ]
        },
        '社会支持': {
            'concepts': [
                {'code': '寻求支持', 'definition': '向他人寻求帮助', 'frequency': 18},
                {'code': '获得帮助', 'definition': '得到实际帮助', 'frequency': 14}
            ],
            'attributes': [
                {'name': '支持类型', 'definition': '支持的类型和来源'}
            ]
        },
        '学业成就': {
            'concepts': [
                {'code': '提高成绩', 'definition': '学习成绩提升', 'frequency': 20},
                {'code': '保持稳定', 'definition': '保持成绩稳定', 'frequency': 8}
            ],
            'attributes': [
                {'name': '成就水平', 'definition': '学业成就的高低'}
            ]
        }
    }
    
    identifier = CoreCategoryIdentifier()
    identifier.load_categories(categories)
    
    # 识别核心范畴
    core_categories = identifier.identify_core_categories(top_k=2)
    
    print("核心范畴识别结果：")
    for category, score in core_categories:
        print(f"{category}: {score:.3f}")
        report = identifier.generate_core_category_report(category)
        print(f"  推荐: {report['recommendation']}")
```

### 第二步：故事线构建
```javascript
// 故事线构建器
class StorylineBuilder {
    constructor() {
        this.events = [];
        this.timeline = [];
        this.characters = new Map();
        this.theme = '';
    }
    
    addEvent(eventId, description, timestamp, participants, category) {
        this.events.push({
            id: eventId,
            description: description,
            timestamp: timestamp,
            participants: participants,
            category: category,
            type: this.identifyEventType(description)
        });
        
        // 更新参与者信息
        participants.forEach(participant => {
            if (!this.characters.has(participant)) {
                this.characters.set(participant, {
                    name: participant,
                    events: [],
                    role: this.identifyRole(participant)
                });
            }
            this.characters.get(participant).events.push(eventId);
        });
    }
    
    identifyEventType(description) {
        const triggerKeywords = ['开始', '触发', '引起', '导致'];
        const processKeywords = ['进行', '经历', '处理', '应对'];
        const outcomeKeywords = ['结果', '完成', '成功', '失败'];
        
        if (triggerKeywords.some(kw => description.includes(kw))) {
            return 'trigger';
        } else if (processKeywords.some(kw => description.includes(kw))) {
            return 'process';
        } else if (outcomeKeywords.some(kw => description.includes(kw))) {
            return 'outcome';
        }
        return 'general';
    }
    
    identifyRole(participant) {
        // 基于参与者名称识别角色
        if (participant.includes('老师') || participant.includes('教师')) {
            return '教师';
        } else if (participant.includes('学生') || participant.includes('同学')) {
            return '学生';
        } else if (participant.includes('家长') || participant.includes('家庭')) {
            return '家长';
        }
        return '其他';
    }
    
    buildTimeline() {
        // 按时间顺序排序事件
        this.timeline = [...this.events].sort((a, b) => a.timestamp - b.timestamp);
        
        // 识别关键转折点
        this.turningPoints = this.identifyTurningPoints();
        
        // 识别高潮和低谷
        this.climaxPoints = this.identifyClimaxPoints();
    }
    
    identifyTurningPoints() {
        const turningPoints = [];
        
        for (let i = 1; i < this.timeline.length - 1; i++) {
            const prevEvent = this.timeline[i - 1];
            const currentEvent = this.timeline[i];
            const nextEvent = this.timeline[i + 1];
            
            // 检查是否是转折点
            if (this.isTurningPoint(prevEvent, currentEvent, nextEvent)) {
                turningPoints.push({
                    event: currentEvent,
                    reason: this.analyzeTurningReason(prevEvent, currentEvent, nextEvent)
                });
            }
        }
        
        return turningPoints;
    }
    
    isTurningPoint(prevEvent, currentEvent, nextEvent) {
        // 基于事件类型变化判断转折点
        const typeChange = prevEvent.type !== currentEvent.type || 
                          currentEvent.type !== nextEvent.type;
        
        // 基于参与者变化判断转折点
        const participantChange = this.calculateParticipantOverlap(
            prevEvent.participants, currentEvent.participants
        ) < 0.5;
        
        // 基于情感强度变化判断转折点
        const emotionChange = this.calculateEmotionChange(prevEvent, currentEvent);
        
        return typeChange || participantChange || emotionChange > 0.7;
    }
    
    calculateParticipantOverlap(participants1, participants2) {
        const set1 = new Set(participants1);
        const set2 = new Set(participants2);
        const intersection = new Set([...set1].filter(x => set2.has(x)));
        const union = new Set([...set1, ...set2]);
        
        return intersection.size / union.size;
    }
    
    calculateEmotionChange(event1, event2) {
        // 简化的情感变化计算
        const emotionKeywords = {
            positive: ['成功', '进步', '满意', '高兴', '兴奋'],
            negative: ['失败', '困难', '挫折', '失望', '焦虑'],
            neutral: ['进行', '经历', '处理', '应对']
        };
        
        const emotion1 = this.extractEmotion(event1.description, emotionKeywords);
        const emotion2 = this.extractEmotion(event2.description, emotionKeywords);
        
        return emotion1 !== emotion2 ? 1.0 : 0.0;
    }
    
    extractEmotion(description, emotionKeywords) {
        for (const [emotion, keywords] of Object.entries(emotionKeywords)) {
            if (keywords.some(kw => description.includes(kw))) {
                return emotion;
            }
        }
        return 'neutral';
    }
    
    analyzeTurningReason(prevEvent, currentEvent, nextEvent) {
        const reasons = [];
        
        if (prevEvent.type !== currentEvent.type) {
            reasons.push('事件类型发生变化');
        }
        
        if (this.calculateParticipantOverlap(prevEvent.participants, currentEvent.participants) < 0.5) {
            reasons.push('参与者发生显著变化');
        }
        
        if (this.calculateEmotionChange(prevEvent, currentEvent) > 0.7) {
            reasons.push('情感状态发生转变');
        }
        
        return reasons.join(', ');
    }
    
    identifyClimaxPoints() {
        const climaxPoints = [];
        
        // 基于事件重要性识别高潮点
        const importanceScores = this.events.map(event => 
            this.calculateImportance(event)
        );
        
        const maxScore = Math.max(...importanceScores);
        const threshold = maxScore * 0.8;
        
        this.events.forEach((event, index) => {
            if (importanceScores[index] >= threshold) {
                climaxPoints.push({
                    event: event,
                    score: importanceScores[index],
                    reason: '事件重要性较高'
                });
            }
        });
        
        return climaxPoints;
    }
    
    calculateImportance(event) {
        let importance = 0;
        
        // 基于参与者数量
        importance += event.participants.length * 0.2;
        
        // 基于事件类型
        if (event.type === 'trigger') importance += 0.3;
        if (event.type === 'outcome') importance += 0.4;
        
        // 基于描述长度
        importance += Math.min(event.description.length / 100, 0.3);
        
        return importance;
    }
    
    generateStoryline() {
        this.buildTimeline();
        
        const storyline = {
            theme: this.identifyTheme(),
            summary: this.generateSummary(),
            phases: this.identifyPhases(),
            keyEvents: this.identifyKeyEvents(),
            characterArcs: this.generateCharacterArcs(),
            narrative: this.generateNarrative()
        };
        
        return storyline;
    }
    
    identifyTheme() {
        // 基于事件描述识别主题
        const allDescriptions = this.events.map(e => e.description).join(' ');
        
        const themeKeywords = {
            '成长': ['成长', '进步', '发展', '提升'],
            '适应': ['适应', '调整', '改变', '转变'],
            '关系': ['关系', '互动', '合作', '支持'],
            '挑战': ['挑战', '困难', '障碍', '问题']
        };
        
        let maxCount = 0;
        let identifiedTheme = '综合体验';
        
        for (const [theme, keywords] of Object.entries(themeKeywords)) {
            const count = keywords.reduce((sum, keyword) => 
                sum + (allDescriptions.split(keyword).length - 1), 0
            );
            
            if (count > maxCount) {
                maxCount = count;
                identifiedTheme = theme;
            }
        }
        
        return identifiedTheme;
    }
    
    generateSummary() {
        const startEvent = this.timeline[0];
        const endEvent = this.timeline[this.timeline.length - 1];
        const turningPointsCount = this.turningPoints.length;
        
        return `从${startEvent.description}开始，经历了${turningPointsCount}个重要转折点，最终${endEvent.description}。整个过程体现了${this.theme}的主题。`;
    }
    
    identifyPhases() {
        const phases = [];
        let currentPhase = {
            start: this.timeline[0],
            events: [this.timeline[0]],
            description: ''
        };
        
        for (let i = 1; i < this.timeline.length; i++) {
            const event = this.timeline[i];
            
            // 检查是否开始新阶段
            if (this.turningPoints.some(tp => tp.event.id === event.id)) {
                // 结束当前阶段
                currentPhase.end = this.timeline[i - 1];
                currentPhase.description = this.generatePhaseDescription(currentPhase);
                phases.push(currentPhase);
                
                // 开始新阶段
                currentPhase = {
                    start: event,
                    events: [event],
                    description: ''
                };
            } else {
                currentPhase.events.push(event);
            }
        }
        
        // 添加最后一个阶段
        currentPhase.end = this.timeline[this.timeline.length - 1];
        currentPhase.description = this.generatePhaseDescription(currentPhase);
        phases.push(currentPhase);
        
        return phases;
    }
    
    generatePhaseDescription(phase) {
        const keyEvents = phase.events.filter(e => 
            this.calculateImportance(e) > 0.5
        );
        
        if (keyEvents.length > 0) {
            return `主要经历${keyEvents.map(e => e.description).join('、')}等重要事件`;
        } else {
            return `经历了${phase.events.length}个相关事件`;
        }
    }
    
    identifyKeyEvents() {
        return this.events
            .filter(event => this.calculateImportance(event) > 0.6)
            .map(event => ({
                event: event,
                importance: this.calculateImportance(event),
                significance: this.analyzeSignificance(event)
            }));
    }
    
    analyzeSignificance(event) {
        const significance = [];
        
        if (event.type === 'trigger') {
            significance.push('触发后续发展');
        }
        
        if (event.type === 'outcome') {
            significance.push('标志重要结果');
        }
        
        if (this.turningPoints.some(tp => tp.event.id === event.id)) {
            significance.push('重要转折点');
        }
        
        return significance.join(', ');
    }
    
    generateCharacterArcs() {
        const arcs = [];
        
        for (const [name, character] of this.characters) {
            const characterEvents = this.events.filter(e => 
                e.participants.includes(name)
            );
            
            const arc = {
                character: name,
                role: character.role,
                events: characterEvents,
                development: this.analyzeCharacterDevelopment(characterEvents),
                significance: this.analyzeCharacterSignificance(name, characterEvents)
            };
            
            arcs.push(arc);
        }
        
        return arcs;
    }
    
    analyzeCharacterDevelopment(events) {
        if (events.length < 2) return '数据不足';
        
        const firstEvent = events[0];
        const lastEvent = events[events.length - 1];
        
        const emotion1 = this.extractEmotion(firstEvent.description, {
            positive: ['成功', '满意', '高兴'],
            negative: ['失败', '困难', '失望'],
            neutral: ['进行', '经历']
        });
        
        const emotion2 = this.extractEmotion(lastEvent.description, {
            positive: ['成功', '满意', '高兴'],
            negative: ['失败', '困难', '失望'],
            neutral: ['进行', '经历']
        });
        
        if (emotion1 === 'negative' && emotion2 === 'positive') {
            return '从困难走向成功';
        } else if (emotion1 === 'neutral' && emotion2 === 'positive') {
            return '逐步改善发展';
        } else if (emotion1 === 'positive' && emotion2 === 'positive') {
            return '保持积极状态';
        } else {
            return '发展轨迹复杂';
        }
    }
    
    analyzeCharacterSignificance(name, events) {
        const importance = events.reduce((sum, event) => 
            sum + this.calculateImportance(event), 0
        );
        
        if (importance > 2.0) {
            return '核心参与者';
        } else if (importance > 1.0) {
            return '重要参与者';
        } else {
            return '一般参与者';
        }
    }
    
    generateNarrative() {
        let narrative = `## ${this.theme}的故事线\n\n`;
        
        // 开端
        narrative += `### 起始阶段\n`;
        narrative += `${this.timeline[0].description}，这标志着整个过程的开始。\n\n`;
        
        // 发展过程
        narrative += `### 发展过程\n`;
        for (const phase of this.identifyPhases()) {
            narrative += `**${phase.description}**：`;
            narrative += `从${phase.start.description}开始，`;
            narrative += `到${phase.end.description}结束。\n\n`;
        }
        
        // 关键转折
        narrative += `### 关键转折\n`;
        for (const turningPoint of this.turningPoints) {
            narrative += `- **${turningPoint.event.description}**：${turningPoint.reason}\n`;
        }
        narrative += '\n';
        
        // 结局
        narrative += `### 最终结果\n`;
        narrative += `${this.timeline[this.timeline.length - 1].description}，`;
        narrative += `这为整个${this.theme}过程画上了句号。\n\n`;
        
        return narrative;
    }
}

// 使用示例
const builder = new StorylineBuilder();

// 添加事件
builder.addEvent(1, '开始遇到学习困难', 1, ['学生小明'], '挑战');
builder.addEvent(2, '向老师寻求帮助', 2, ['学生小明', '老师'], '应对');
builder.addEvent(3, '老师提供学习指导', 3, ['老师'], '支持');
builder.addEvent(4, '调整学习方法', 4, ['学生小明'], '适应');
builder.addEvent(5, '学习成绩提升', 5, ['学生小明'], '成果');

// 生成故事线
const storyline = builder.generateStoryline();
console.log('故事线:', JSON.stringify(storyline, null, 2));
```

## 质量保证

### 核心范畴识别质量检查
- [ ] 评估指标全面科学
- [ ] 权重分配合理
- [ ] 数据支持充分
- [ ] 理论价值明确
- [ ] 推荐意见准确

### 故事线构建质量检查
- [ ] 时间顺序正确
- [ ] 事件逻辑清晰
- [ ] 转折点识别准确
- [ ] 角色发展合理
- [ ] 主题表达明确

### 理论整合质量检查
- [ ] 理论命题逻辑严密
- [ ] 概念框架完整
- [ ] 机制解释深入
- [ ] 边界条件清晰
- [ ] 实践意义明确

### 饱和度检验质量检查
- [ ] 检验标准科学
- [ ] 数据充分性评估准确
- [ ] 理论完整性验证充分
- [ ] 补充需求分析合理
- [ ] 结论可靠

## 输出格式

### 选择式编码报告格式
```json
{
  "core_category": {
    "name": "学习适应",
    "selection_rationale": "具有很强的解释力和理论价值",
    "explanatory_power": 0.85,
    "theoretical_value": 0.78,
    "data_support": 0.82
  },
  "storyline": {
    "theme": "成长与适应",
    "summary": "从遇到困难到成功适应的完整过程",
    "phases": [...],
    "key_events": [...],
    "narrative": "完整的故事叙述"
  },
  "theoretical_framework": {
    "propositions": [...],
    "mechanisms": [...],
    "boundaries": [...],
    "implications": [...]
  },
  "saturation_check": {
    "is_saturated": true,
    "evidence": [...],
    "recommendations": [...]
  }
}
```

---

**此选择式编码技能专门为中文质性研究设计，提供从核心范畴识别到理论构建的完整选择式编码支持，确保理论构建的科学性和系统性。**