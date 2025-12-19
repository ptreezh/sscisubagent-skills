#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试 - 自动加载器模块
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from auto_loader import OpenCodingAutoLoader


class TestOpenCodingAutoLoader:
    """测试开放编码自动加载器"""
    
    def setup_method(self):
        """每个测试前的设置"""
        self.loader = OpenCodingAutoLoader()
    
    def test_initialization(self):
        """测试初始化"""
        assert self.loader is not None
        assert isinstance(self.loader.stop_words, set)
        assert len(self.loader.stop_words) > 0
    
    def test_quick_concept_extract_basic(self):
        """测试基本概念提取"""
        text = "学生寻求老师的帮助。老师提供学习指导。"
        concepts = self.loader.quick_concept_extract(text)
        
        assert isinstance(concepts, list)
        assert len(concepts) > 0
        
        # 检查概念结构
        for concept in concepts:
            assert 'concept' in concept
            assert 'frequency' in concept
            assert 'type' in concept
    
    def test_quick_concept_extract_frequency(self):
        """测试词频统计"""
        text = "学习学习学习方法方法"
        concepts = self.loader.quick_concept_extract(text)
        
        # 学习应该出现3次
        learning_concept = next((c for c in concepts if c['concept'] == '学习'), None)
        assert learning_concept is not None
        assert learning_concept['frequency'] == 3
        
        # 方法应该出现2次
        method_concept = next((c for c in concepts if c['concept'] == '方法'), None)
        assert method_concept is not None
        assert method_concept['frequency'] == 2
    
    def test_quick_concept_extract_stopwords(self):
        """测试停用词过滤"""
        text = "我的学习方法是很好的"
        concepts = self.loader.quick_concept_extract(text)
        
        # 停用词应该被过滤
        concept_words = [c['concept'] for c in concepts]
        assert '的' not in concept_words
        assert '是' not in concept_words
        assert '我' not in concept_words
    
    def test_quick_concept_extract_empty(self):
        """测试空文本"""
        concepts = self.loader.quick_concept_extract("")
        assert concepts == []
    
    def test_quick_concept_extract_top_limit(self):
        """测试提取数量限制"""
        text = "学习 " * 100  # 重复100次
        concepts = self.loader.quick_concept_extract(text)
        
        # 应该限制在20个以内
        assert len(concepts) <= 20
    
    def test_classify_concept_action(self):
        """测试行动概念分类"""
        action_words = ['寻求帮助', '建立关系', '适应环境', '应对困难', '处理问题', '解决矛盾']
        
        for word in action_words:
            concept_type = self.loader._classify_concept(word)
            assert concept_type == '行动概念', f"{word} 应该被分类为行动概念"
    
    def test_classify_concept_emotion(self):
        """测试情感概念分类"""
        emotion_words = ['感受压力', '体验快乐', '情绪波动', '态度积极']
        
        for word in emotion_words:
            concept_type = self.loader._classify_concept(word)
            assert concept_type == '情感概念', f"{word} 应该被分类为情感概念"
    
    def test_classify_concept_relation(self):
        """测试关系概念分类"""
        relation_words = ['师生关系', '人际联系', '社会影响', '互动作用']
        
        for word in relation_words:
            concept_type = self.loader._classify_concept(word)
            assert concept_type == '关系概念', f"{word} 应该被分类为关系概念"
    
    def test_classify_concept_general(self):
        """测试一般概念分类"""
        general_words = ['学习', '方法', '时间', '计划']
        
        for word in general_words:
            concept_type = self.loader._classify_concept(word)
            assert concept_type == '一般概念', f"{word} 应该被分类为一般概念"
    
    def test_generate_coding_suggestions_basic(self):
        """测试编码建议生成"""
        concepts = [
            {'concept': '寻求帮助', 'frequency': 5, 'type': '行动概念'},
            {'concept': '感受压力', 'frequency': 3, 'type': '情感概念'},
            {'concept': '学习方法', 'frequency': 10, 'type': '一般概念'}
        ]
        
        suggestions = self.loader.generate_coding_suggestions(concepts)
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        
        # 应该包含行动概念建议
        assert any('行动概念' in s for s in suggestions)
    
    def test_generate_coding_suggestions_action_focus(self):
        """测试行动概念重点提示"""
        concepts = [
            {'concept': '寻求帮助', 'frequency': 5, 'type': '行动概念'},
            {'concept': '建立关系', 'frequency': 4, 'type': '行动概念'},
            {'concept': '学习', 'frequency': 10, 'type': '一般概念'}
        ]
        
        suggestions = self.loader.generate_coding_suggestions(concepts)
        
        # 应该有行动概念的建议
        action_suggestion = next((s for s in suggestions if '行动概念' in s), None)
        assert action_suggestion is not None
        assert '寻求帮助' in action_suggestion or '建立关系' in action_suggestion
    
    def test_generate_coding_suggestions_emotion_focus(self):
        """测试情感概念提示"""
        concepts = [
            {'concept': '感受压力', 'frequency': 5, 'type': '情感概念'},
            {'concept': '体验快乐', 'frequency': 3, 'type': '情感概念'},
            {'concept': '学习', 'frequency': 10, 'type': '一般概念'}
        ]
        
        suggestions = self.loader.generate_coding_suggestions(concepts)
        
        # 应该有情感概念的建议
        emotion_suggestion = next((s for s in suggestions if '情感' in s), None)
        assert emotion_suggestion is not None
    
    def test_generate_coding_suggestions_high_frequency(self):
        """测试高频概念建议"""
        concepts = [
            {'concept': '学习', 'frequency': 10, 'type': '一般概念'},
            {'concept': '方法', 'frequency': 5, 'type': '一般概念'},
            {'concept': '时间', 'frequency': 3, 'type': '一般概念'}
        ]
        
        suggestions = self.loader.generate_coding_suggestions(concepts)
        
        # 应该有高频概念建议
        high_freq_suggestion = next((s for s in suggestions if '高频概念' in s), None)
        assert high_freq_suggestion is not None
        assert '学习' in high_freq_suggestion  # 最高频的概念
    
    def test_generate_coding_suggestions_empty(self):
        """测试空概念列表"""
        suggestions = self.loader.generate_coding_suggestions([])
        
        # 应该至少有一个建议
        assert len(suggestions) >= 1


class TestIntegrationWorkflow:
    """集成测试 - 完整工作流"""
    
    def test_complete_workflow(self):
        """测试完整的分析流程"""
        loader = OpenCodingAutoLoader()
        
        # 真实访谈文本
        text = """
        我在大学学习过程中遇到了很多困难。
        当我遇到学习上的问题时，我会主动寻求老师的帮助。
        老师给了我很多学习上的指导和支持。
        我也会和同学建立良好的关系，互相帮助学习。
        """
        
        # 1. 提取概念
        concepts = loader.quick_concept_extract(text)
        assert len(concepts) > 0
        
        # 2. 生成建议
        suggestions = loader.generate_coding_suggestions(concepts)
        assert len(suggestions) > 0
        
        # 3. 验证结果质量
        concept_words = [c['concept'] for c in concepts]
        assert any(w in ['学习', '老师', '帮助', '困难'] for w in concept_words)
    
    def test_real_interview_analysis(self):
        """测试真实访谈数据分析"""
        loader = OpenCodingAutoLoader()
        
        text = """
        在适应大学生活的过程中，我学会了如何管理自己的时间。
        我制定了详细的学习计划，并努力执行。
        这帮助我更好地平衡学习和生活。
        我也学会了如何应对压力和挫折。
        """
        
        concepts = loader.quick_concept_extract(text)
        
        # 应该识别出关键行动概念
        action_concepts = [c for c in concepts if c['type'] == '行动概念']
        assert len(action_concepts) > 0
        
        # 应该有合理的词频分布
        frequencies = [c['frequency'] for c in concepts]
        assert max(frequencies) >= 1
        assert sum(frequencies) > len(concepts)  # 总频次应该大于概念数


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
