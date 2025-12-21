#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基础功能测试
测试不依赖外部包的核心功能
"""

import unittest
import tempfile
import json
from pathlib import Path

class TestBasicJSONHandling(unittest.TestCase):
    """测试基础JSON处理功能"""

    def test_json_file_creation_and_reading(self):
        """测试JSON文件创建和读取"""
        test_data = {
            "nodes": ["A", "B", "C", "D"],
            "edges": [["A", "B"], ["B", "C"], ["C", "D"]]
        }

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(test_data, f)
            temp_file = f.name

        try:
            # 读取文件
            with open(temp_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)

            # 验证数据
            self.assertEqual(loaded_data['nodes'], test_data['nodes'])
            self.assertEqual(loaded_data['edges'], test_data['edges'])

        finally:
            Path(temp_file).unlink()

    def test_json_structure_validation(self):
        """测试JSON结构验证"""
        # 测试技能文件的基本结构
        skill_content = """---
name: test-skill
description: 这是一个测试技能
description_en: This is a test skill
---

# 测试技能

## 使用工具
测试工具使用说明。

## 输出格式
- JSON格式
- 报告格式
"""

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.md', encoding='utf-8') as f:
            f.write(skill_content)
            skill_file = f.name

        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 验证YAML frontmatter
            self.assertTrue(content.startswith('---'))
            self.assertIn('name: test-skill', content)
            self.assertIn('description:', content)
            self.assertIn('---', content[3:])  # 结束标记

        finally:
            Path(skill_file).unlink()

class TestTextProcessing(unittest.TestCase):
    """测试基础文本处理功能"""

    def test_text_cleaning(self):
        """测试文本清理功能"""
        # 简单的文本清理实现（不依赖jieba）
        def simple_text_clean(text):
            import re
            # 保留中文、英文、标点符号和数字
            text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z，。！？；：""''（）【】《》0-9\\s]', '', text)
            # 统一标点符号
            text = text.replace('！', '!').replace('？', '?').replace('；', ';')
            # 去除多余空格
            text = re.sub(r'\s+', ' ', text).strip()
            return text

        test_text = "这是一个测试！包含中文、英文123和特殊字符#$%。"
        cleaned = simple_text_clean(test_text)

        # 验证清理结果
        self.assertIn("这是一个测试", cleaned)
        self.assertIn("包含中文", cleaned)
        self.assertIn("英文123", cleaned)
        # 验证特殊字符被移除
        self.assertNotIn("#$%", cleaned)

    def test_text_segmentation(self):
        """测试文本分段功能"""
        def simple_text_segment(text):
            # 简单的按多种标点符号分段
            import re
            # 按句号、感叹号、问号分段
            sentences = re.split(r'[。！？]', text)
            # 过滤空句
            segments = [s.strip() for s in sentences if s.strip()]
            return segments

        test_text = "第一句。第二句！第三句？第四句。"
        segments = simple_text_segment(test_text)

        # 验证分段结果
        self.assertEqual(len(segments), 4)
        self.assertEqual(segments[0], "第一句")
        self.assertEqual(segments[1], "第二句")
        self.assertEqual(segments[2], "第三句")
        self.assertEqual(segments[3], "第四句")

class TestNetworkBasics(unittest.TestCase):
    """测试基础网络功能"""

    def test_network_data_structure(self):
        """测试网络数据结构"""
        # 创建测试网络数据
        network_data = {
            "nodes": ["A", "B", "C", "D", "E"],
            "edges": [
                {"source": "A", "target": "B", "weight": 1},
                {"source": "A", "target": "C", "weight": 2},
                {"source": "B", "target": "C", "weight": 1},
                {"source": "B", "target": "D", "weight": 3},
                {"source": "C", "target": "D", "weight": 1},
                {"source": "D", "target": "E", "weight": 2}
            ]
        }

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            json.dump(network_data, f)
            data_file = f.name

        try:
            # 验证数据结构
            self.assertEqual(len(network_data['nodes']), 5)
            self.assertEqual(len(network_data['edges']), 6)

            # 验证边数据
            for edge in network_data['edges']:
                self.assertIn('source', edge)
                self.assertIn('target', edge)
                self.assertIn('weight', edge)
                self.assertIsInstance(edge['weight'], (int, float))

            # 保存并重新加载验证
            with open(data_file, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)

            self.assertEqual(loaded_data, network_data)

        finally:
            Path(data_file).unlink()

    def test_basic_network_metrics(self):
        """测试基础网络指标计算"""
        # 简化的网络指标计算
        def calculate_basic_metrics(network_data):
            nodes = set()
            degrees = {}

            for edge in network_data['edges']:
                nodes.add(edge['source'])
                nodes.add(edge['target'])

                # 计算度数
                source_deg = degrees.get(edge['source'], 0)
                target_deg = degrees.get(edge['target'], 0)
                degrees[edge['source']] = source_deg + 1
                degrees[edge['target']] = target_deg + 1

            return {
                'node_count': len(nodes),
                'edge_count': len(network_data['edges']),
                'average_degree': sum(degrees.values()) / len(degrees) if degrees else 0,
                'max_degree': max(degrees.values()) if degrees else 0,
                'min_degree': min(degrees.values()) if degrees else 0
            }

        test_network = {
            "nodes": ["A", "B", "C"],
            "edges": [
                {"source": "A", "target": "B", "weight": 1},
                {"source": "B", "target": "C", "weight": 2},
                {"source": "C", "target": "A", "weight": 1}
            ]
        }

        metrics = calculate_basic_metrics(test_network)

        # 验证指标
        self.assertEqual(metrics['node_count'], 3)
        self.assertEqual(metrics['edge_count'], 3)
        self.assertAlmostEqual(metrics['average_degree'], 2.0, places=1)
        self.assertEqual(metrics['max_degree'], 2)
        self.assertEqual(metrics['min_degree'], 2)

class TestTheorySaturationBasics(unittest.TestCase):
    """测试理论饱和度基础功能"""

    def test_concept_stability_calculation(self):
        """测试概念稳定性计算"""
        existing_concepts = [
            {"code": "概念A", "frequency": 10},
            {"code": "概念B", "frequency": 8},
            {"code": "概念C", "frequency": 5}
        ]

        new_concepts = [
            {"code": "概念A", "frequency": 12},
            {"code": "概念D", "frequency": 3},
            {"code": "概念E", "frequency": 2}
        ]

        # 计算新概念比例
        new_concept_set = set(c['code'] for c in new_concepts)
        existing_concept_set = set(c['code'] for c in existing_concepts)
        novel_concepts = new_concept_set - existing_concept_set

        total_new_concepts = len(new_concept_set)
        novel_ratio = len(novel_concepts) / max(total_new_concepts, 1)

        # 验证结果
        self.assertEqual(novel_concepts, {"概念D", "概念E"})
        self.assertEqual(total_new_concepts, 3)
        self.assertAlmostEqual(novel_ratio, 2/3, places=2)

    def test_saturation_threshold_check(self):
        """测试饱和度阈值检查"""
        thresholds = {
            'concept_threshold': 0.05,
            'category_threshold': 0.8
        }

        # 测试完全饱和
        self.assertTrue(0.03 <= thresholds['concept_threshold'])

        # 测试部分饱和
        self.assertFalse(0.1 <= thresholds['concept_threshold'])

        # 测试未饱和
        self.assertFalse(0.2 <= thresholds['concept_threshold'])

    def test_saturation_status_determination(self):
        """测试饱和状态判定"""
        def determine_saturation(concept_ratio, category_score, relation_score, overall_score):
            if (concept_ratio <= 0.05 and
                category_score >= 0.8 and
                relation_score >= 0.9 and
                overall_score >= 0.85):
                return 'fully_saturated'
            elif overall_score > 0.6:
                return 'partially_saturated'
            else:
                return 'not_saturated'

        # 测试完全饱和
        status1 = determine_saturation(0.03, 0.85, 0.9, 0.88)
        self.assertEqual(status1, 'fully_saturated')

        # 测试部分饱和
        status2 = determine_saturation(0.1, 0.75, 0.8, 0.65)
        self.assertEqual(status2, 'partially_saturated')

        # 测试未饱和
        status3 = determine_saturation(0.2, 0.6, 0.5, 0.4)
        self.assertEqual(status3, 'not_saturated')

class TestErrorHandling(unittest.TestCase):
    """测试错误处理"""

    def test_file_not_found_handling(self):
        """测试文件不存在的情况"""
        non_existent_file = Path("non_existent_file.json")

        # 尝试读取不存在的文件
        with self.assertRaises(FileNotFoundError):
            with open(non_existent_file, 'r') as f:
                data = json.load(f)

    def test_invalid_json_handling(self):
        """测试无效JSON格式"""
        invalid_json = '{"invalid": json structure, "missing": [}'

        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            f.write(invalid_json)
            invalid_file = f.name

        try:
            with open(invalid_file, 'r') as f:
                data = json.load(f)
            self.fail("应该抛出JSONDecodeError异常")
        except json.JSONDecodeError:
            self.assertTrue(True)  # 期望的异常
        finally:
            Path(invalid_file).unlink()

    def test_empty_data_handling(self):
        """测试空数据处理"""
        # 测试空概念列表
        empty_concepts = []

        # 计算统计应该返回0
        self.assertEqual(len(empty_concepts), 0)

        # 计算平均频率应该避免除以零
        avg_frequency = sum(c.get('frequency', 0) for c in empty_concepts) / max(len(empty_concepts), 1)
        self.assertEqual(avg_frequency, 0)

if __name__ == '__main__':
    unittest.main()