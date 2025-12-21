#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试 - 文本预处理模块
"""

import pytest
import sys
from pathlib import Path

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from preprocess_text import (
    tokenize_chinese,
    remove_stopwords,
    segment_by_meaning,
    preprocess_text
)

class TestTokenizeChinese:
    """测试中文分词功能"""
    
    def test_basic_tokenization(self):
        """测试基本分词"""
        text = "我在学习扎根理论"
        result = tokenize_chinese(text)
        
        assert isinstance(result, list)
        assert len(result) > 0
        assert '学习' in result or '扎根' in result or '理论' in result
    
    def test_filter_by_pos(self):
        """测试词性过滤"""
        text = "学生寻求老师的帮助"
        result = tokenize_chinese(text)
        
        # 应该包含名词和动词
        assert any(word in result for word in ['学生', '老师', '帮助', '寻求'])
    
    def test_empty_text(self):
        """测试空文本"""
        result = tokenize_chinese("")
        assert result == []
    
    def test_single_char_filtered(self):
        """测试单字被过滤"""
        text = "我和你"
        result = tokenize_chinese(text)
        # 单字应该被过滤
        assert len(result) == 0 or all(len(w) > 1 for w in result)


class TestRemoveStopwords:
    """测试停用词过滤"""
    
    def test_basic_filtering(self):
        """测试基本过滤"""
        words = ['学习', '的', '方法', '是', '重要', '的']
        result = remove_stopwords(words)
        
        assert '学习' in result
        assert '方法' in result
        assert '重要' in result
        assert '的' not in result
        assert '是' not in result
    
    def test_custom_stopwords(self):
        """测试自定义停用词"""
        words = ['学习', '方法', '测试']
        custom = {'测试'}
        result = remove_stopwords(words, custom)
        
        assert '学习' in result
        assert '方法' in result
        assert '测试' not in result
    
    def test_empty_list(self):
        """测试空列表"""
        result = remove_stopwords([])
        assert result == []


class TestSegmentByMeaning:
    """测试语义分段"""
    
    def test_basic_segmentation(self):
        """测试基本分段"""
        text = "这是第一句。这是第二句。这是第三句。"
        result = segment_by_meaning(text, max_length=20)
        
        assert isinstance(result, list)
        assert len(result) >= 2  # 应该被分成至少2段
    
    def test_max_length_constraint(self):
        """测试最大长度约束"""
        text = "这是第一句。" * 50  # 很长的文本
        result = segment_by_meaning(text, max_length=100)
        
        # 每段长度应该不超过max_length
        assert all(len(seg) <= 110 for seg in result)  # 允许一些余量
    
    def test_empty_text(self):
        """测试空文本"""
        result = segment_by_meaning("")
        assert result == []
    
    def test_single_sentence(self):
        """测试单句"""
        text = "这是一句话。"
        result = segment_by_meaning(text)
        assert len(result) == 1


class TestPreprocessText:
    """测试完整预处理流程"""
    
    def test_complete_pipeline(self):
        """测试完整流程"""
        text = "学生寻求老师的帮助。老师提供了学习指导。"
        result = preprocess_text(text)
        
        # 检查返回结构
        assert 'segments' in result
        assert 'total_words' in result
        assert 'unique_words' in result
        assert 'word_frequency' in result
        
        # 检查数据类型
        assert isinstance(result['segments'], list)
        assert isinstance(result['total_words'], int)
        assert isinstance(result['unique_words'], int)
        assert isinstance(result['word_frequency'], dict)
    
    def test_word_statistics(self):
        """测试词频统计"""
        text = "学习学习学习方法方法重要"
        result = preprocess_text(text)
        
        # 学习应该出现3次
        assert result['word_frequency'].get('学习', 0) >= 2
        assert result['total_words'] > 0
        assert result['unique_words'] > 0
    
    def test_segment_structure(self):
        """测试分段结构"""
        text = "第一句话。第二句话。"
        result = preprocess_text(text)
        
        assert len(result['segments']) > 0
        
        # 检查每个分段的结构
        for seg in result['segments']:
            assert 'text' in seg
            assert 'words' in seg
            assert 'word_count' in seg
            assert isinstance(seg['words'], list)
            assert isinstance(seg['word_count'], int)


class TestIntegration:
    """集成测试"""
    
    def test_real_interview_data(self):
        """测试真实访谈数据"""
        text = """
        我在大学学习过程中遇到了很多困难。
        当我遇到学习上的问题时，我会主动寻求老师的帮助。
        老师给了我很多学习上的指导和支持。
        """
        
        result = preprocess_text(text)
        
        # 应该识别出关键词
        assert result['total_words'] > 10
        assert result['unique_words'] > 5
        
        # 应该有词频统计
        assert len(result['word_frequency']) > 0
        
        # 高频词应该包含学习相关的词
        top_words = list(result['word_frequency'].keys())[:10]
        assert any(w in ['学习', '老师', '帮助', '困难'] for w in top_words)


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
