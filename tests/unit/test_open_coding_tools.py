#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开放编码工具单元测试
测试预处理、概念提取和编码比较工具的功能
"""

import unittest
import sys
import os
import tempfile
import json
from pathlib import Path

# 添加技能脚本路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "skills" / "coding" / "open-coding" / "scripts"))

try:
    from preprocess import TextPreprocessor
    from extract_concepts import ConceptExtractor
    from compare_codes import CodeComparator
except ImportError as e:
    print(f"导入错误: {e}")
    sys.exit(1)

class TestTextPreprocessor(unittest.TestCase):
    """测试文本预处理器"""

    def setUp(self):
        self.processor = TextPreprocessor()
        self.sample_text = "这是一个测试文本。包含一些中文内容和标点符号！用于验证文本清理功能。"

    def test_clean_text(self):
        """测试文本清理功能"""
        cleaned = self.processor.clean_text(self.sample_text)

        # 应该保留中文和基本标点
        self.assertIn("这是一个测试文本", cleaned)
        self.assertIn("标点符号", cleaned)

        # 应该去掉特殊字符
        self.assertNotIn("@#$%^&*", cleaned)

    def test_segment_text(self):
        """测试文本分段功能"""
        segments = self.processor.segment_text(self.sample_text)

        self.assertIsInstance(segments, list)
        self.assertTrue(len(segments) > 0)

        # 每个段落都不为空
        for segment in segments:
            self.assertTrue(len(segment.strip()) > 0)

    def test_extract_keywords(self):
        """测试关键词提取功能"""
        keywords = self.processor.extract_keywords(self.sample_text)

        self.assertIsInstance(keywords, list)
        # 停用词应该被过滤
        stop_words = {'的', '了', '在', '是'}
        for keyword in keywords:
            self.assertNotIn(keyword, stop_words)

class TestConceptExtractor(unittest.TestCase):
    """测试概念提取器"""

    def setUp(self):
        self.extractor = ConceptExtractor()
        self.sample_segment = {
            'id': 1,
            'text': '学生在学习中遇到困难时需要寻求帮助',
            'keywords': ['学生', '学习', '困难', '寻求', '帮助']
        }

    def test_extract_action_concepts(self):
        """测试行动概念提取"""
        action_concepts = self.extractor.extract_action_concepts(self.sample_segment['text'])

        self.assertIsInstance(action_concepts, list)
        # 应该识别出"寻求"这个行动概念
        self.assertTrue(any("寻求" in concept for concept in action_concepts))

    def test_extract_key_phrases(self):
        """测试关键词组提取"""
        key_phrases = self.extractor.extract_key_phrases(self.sample_segment['text'])

        self.assertIsInstance(key_phrases, list)
        self.assertTrue(len(key_phrases) > 0)

    def test_identify_concepts_in_segment(self):
        """测试段落概念识别"""
        concepts = self.extractor.identify_concepts_in_segment(self.sample_segment)

        self.assertIn('segment_id', concepts)
        self.assertIn('action_concepts', concepts)
        self.assertIn('key_phrases', concepts)
        self.assertIn('suggested_codes', concepts)

class TestCodeComparator(unittest.TestCase):
    """测试编码比较器"""

    def setUp(self):
        self.comparator = CodeComparator()
        self.test_concepts = [
            {'code': '寻求帮助', 'frequency': 10, 'type': '行动概念'},
            {'code': '获得支持', 'frequency': 8, 'type': '行动概念'},
            {'code': '建立关系', 'frequency': 5, 'type': '关系概念'},
            {'code': '寻求支持', 'frequency': 12, 'type': '行动概念'}
        ]

    def test_calculate_semantic_similarity(self):
        """测试语义相似度计算"""
        # 相似概念
        similarity1 = self.comparator.calculate_semantic_similarity('寻求帮助', '获得支持')
        self.assertGreater(similarity1, 0)
        self.assertLessEqual(similarity1, 1)

        # 相同概念
        similarity2 = self.comparator.calculate_semantic_similarity('相同', '相同')
        self.assertEqual(similarity2, 1)

        # 无重叠概念
        similarity3 = self.comparator.calculate_semantic_similarity('学习', '运动')
        self.assertEqual(similarity3, 0)

    def test_identify_relationship(self):
        """测试关系识别"""
        # 相同关系
        relationship1 = self.comparator.identify_relationship('测试', '测试')
        self.assertEqual(relationship1, '相同')

        # 包含关系
        relationship2 = self.comparator.identify_relationship('测试', '测试数据')
        self.assertEqual(relationship2, '包含关系')

        # 独立关系
        relationship3 = self.comparator.identify_relationship('学习', '运动')
        self.assertEqual(relationship3, '独立关系')

    def test_suggest_merge_action(self):
        """测试合并建议"""
        # 高相似度
        action1 = self.comparator.suggest_merge_action('相似概念', '相似概念', 0.9)
        self.assertEqual(action1, '强烈建议合并')

        # 中等相似度 - 使用更高的阈值来触发"考虑合并"
        action2 = self.comparator.suggest_merge_action('相关概念', '相关概念', 0.7)
        self.assertEqual(action2, '考虑合并或明确区分')

        # 低相似度
        action3 = self.comparator.suggest_merge_action('不同概念', '不同概念', 0.2)
        self.assertEqual(action3, '保持独立编码')

class TestToolIntegration(unittest.TestCase):
    """测试工具集成"""

    def test_full_workflow(self):
        """测试完整工作流"""
        # 创建临时测试数据
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as f:
            f.write("这是一个测试访谈文本。学生在学习中需要帮助，老师提供了支持。同学之间也经常互相帮助。有时候会遇到困难，但通过寻求帮助能够解决。")
            test_file = f.name

        try:
            # 第一步：预处理
            processor = TextPreprocessor()
            preprocessed_file = test_file.replace('.txt', '_preprocessed.json')
            result = processor.process_file(test_file, preprocessed_file)

            self.assertIn('segments', result)
            self.assertGreater(result['total_segments'], 0)

            # 第二步：概念提取
            extractor = ConceptExtractor()
            concepts_result = extractor.process_preprocessed_data(preprocessed_file)

            self.assertIn('initial_code_list', concepts_result)
            self.assertGreater(len(concepts_result['initial_code_list']), 0)

            # 第三步：编码比较
            comparator = CodeComparator()
            optimization_result = comparator.optimize_codes(concepts_result['file_name'].replace('_preprocessed.json', '_concepts.json'))

            self.assertIn('optimized_codes', optimization_result)
            self.assertEqual(optimization_result['original_code_count'], len(concepts_result['initial_code_list']))

        finally:
            # 清理临时文件
            Path(test_file).unlink()
            if Path(preprocessed_file).exists():
                Path(preprocessed_file).unlink()

if __name__ == '__main__':
    unittest.main()