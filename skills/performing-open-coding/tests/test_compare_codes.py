#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
单元测试 - 持续比较模块
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from compare_codes import (
    calculate_similarity,
    identify_duplicates,
    suggest_merges,
    analyze_code_relationships
)


class TestCalculateSimilarity:
    """测试相似度计算"""
    
    def test_identical_codes(self):
        """测试完全相同的编码"""
        code1 = "寻求帮助"
        code2 = "寻求帮助"
        
        similarity = calculate_similarity(code1, code2)
        
        # 相同编码相似度应该接近1.0
        assert similarity > 0.95
    
    def test_similar_codes(self):
        """测试相似编码"""
        code1 = "寻求老师帮助"
        code2 = "寻求教师帮助"
        
        similarity = calculate_similarity(code1, code2)
        
        # 相似编码应该有较高相似度
        assert similarity > 0.5
    
    def test_different_codes(self):
        """测试不同编码"""
        code1 = "学习方法"
        code2 = "情感体验"
        
        similarity = calculate_similarity(code1, code2)
        
        # 不同编码相似度应该较低
        assert similarity < 0.3
    
    def test_empty_codes(self):
        """测试空编码"""
        similarity = calculate_similarity("", "")
        
        # 空编码应该返回0
        assert similarity == 0.0
    
    def test_partial_overlap(self):
        """测试部分重叠"""
        code1 = "学习困难"
        code2 = "学习方法"
        
        similarity = calculate_similarity(code1, code2)
        
        # 部分重叠应该有中等相似度
        assert 0.3 < similarity < 0.8


class TestIdentifyDuplicates:
    """测试重复识别"""
    
    def test_no_duplicates(self):
        """测试无重复情况"""
        codes = [
            {'concept': '学习方法', 'frequency': 5},
            {'concept': '情感体验', 'frequency': 3},
            {'concept': '时间管理', 'frequency': 4}
        ]
        
        duplicates = identify_duplicates(codes, threshold=0.8)
        
        assert isinstance(duplicates, list)
        assert len(duplicates) == 0
    
    def test_with_duplicates(self):
        """测试有重复情况"""
        codes = [
            {'concept': '寻求帮助', 'frequency': 5},
            {'concept': '寻求帮助', 'frequency': 3},  # 完全重复
            {'concept': '学习方法', 'frequency': 4}
        ]
        
        duplicates = identify_duplicates(codes, threshold=0.8)
        
        # 应该识别出重复
        assert len(duplicates) > 0
        assert duplicates[0]['similarity'] > 0.8
    
    def test_threshold_filtering(self):
        """测试阈值过滤"""
        codes = [
            {'concept': '寻求老师帮助', 'frequency': 5},
            {'concept': '寻求教师帮助', 'frequency': 3},
            {'concept': '学习方法', 'frequency': 4}
        ]
        
        # 高阈值
        duplicates_high = identify_duplicates(codes, threshold=0.9)
        # 低阈值
        duplicates_low = identify_duplicates(codes, threshold=0.5)
        
        # 低阈值应该识别出更多重复
        assert len(duplicates_low) >= len(duplicates_high)
    
    def test_duplicate_structure(self):
        """测试重复结构"""
        codes = [
            {'concept': '寻求帮助', 'frequency': 5},
            {'concept': '寻求帮助', 'frequency': 3}
        ]
        
        duplicates = identify_duplicates(codes, threshold=0.8)
        
        if len(duplicates) > 0:
            dup = duplicates[0]
            assert 'code1' in dup
            assert 'code2' in dup
            assert 'similarity' in dup
            assert 'index1' in dup
            assert 'index2' in dup
    
    def test_single_code(self):
        """测试单个编码"""
        codes = [{'concept': '学习方法', 'frequency': 5}]
        
        duplicates = identify_duplicates(codes, threshold=0.8)
        
        # 单个编码不应该有重复
        assert len(duplicates) == 0
    
    def test_empty_codes(self):
        """测试空编码列表"""
        duplicates = identify_duplicates([], threshold=0.8)
        assert len(duplicates) == 0


class TestSuggestMerges:
    """测试合并建议"""
    
    def test_basic_merge_suggestion(self):
        """测试基本合并建议"""
        codes = [
            {'concept': '寻求帮助', 'frequency': 5},
            {'concept': '寻求帮助', 'frequency': 3}
        ]
        
        duplicates = [
            {
                'code1': '寻求帮助',
                'code2': '寻求帮助',
                'similarity': 0.95,
                'index1': 0,
                'index2': 1
            }
        ]
        
        suggestions = suggest_merges(codes, duplicates)
        
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
    
    def test_merge_suggestion_structure(self):
        """测试合并建议结构"""
        codes = [
            {'concept': '寻求帮助', 'frequency': 5},
            {'concept': '寻求帮助', 'frequency': 3}
        ]
        
        duplicates = [
            {
                'code1': '寻求帮助',
                'code2': '寻求帮助',
                'similarity': 0.95,
                'index1': 0,
                'index2': 1
            }
        ]
        
        suggestions = suggest_merges(codes, duplicates)
        
        if len(suggestions) > 0:
            suggestion = suggestions[0]
            assert 'action' in suggestion
            assert suggestion['action'] == 'merge'
            assert 'primary_code' in suggestion
            assert 'secondary_code' in suggestion
            assert 'similarity' in suggestion
            assert 'reason' in suggestion
            assert 'combined_frequency' in suggestion
    
    def test_frequency_based_primary(self):
        """测试基于频率选择主编码"""
        codes = [
            {'concept': '寻求帮助', 'frequency': 3},
            {'concept': '寻求帮助', 'frequency': 5}  # 频率更高
        ]
        
        duplicates = [
            {
                'code1': '寻求帮助',
                'code2': '寻求帮助',
                'similarity': 0.95,
                'index1': 0,
                'index2': 1
            }
        ]
        
        suggestions = suggest_merges(codes, duplicates)
        
        # 应该选择频率更高的作为主编码
        assert suggestions[0]['combined_frequency'] == 8
    
    def test_empty_duplicates(self):
        """测试空重复列表"""
        codes = [{'concept': '学习方法', 'frequency': 5}]
        suggestions = suggest_merges(codes, [])
        
        assert len(suggestions) == 0


class TestAnalyzeCodeRelationships:
    """测试编码关系分析"""
    
    def test_basic_relationship_analysis(self):
        """测试基本关系分析"""
        codes = [
            {'concept': '学习方法', 'frequency': 5},
            {'concept': '学习计划', 'frequency': 3},
            {'concept': '时间管理', 'frequency': 4}
        ]
        
        result = analyze_code_relationships(codes)
        
        assert 'similarity_matrix' in result
        assert 'relationships' in result
        assert isinstance(result['similarity_matrix'], list)
        assert isinstance(result['relationships'], list)
    
    def test_similarity_matrix_shape(self):
        """测试相似度矩阵形状"""
        codes = [
            {'concept': '学习方法', 'frequency': 5},
            {'concept': '学习计划', 'frequency': 3},
            {'concept': '时间管理', 'frequency': 4}
        ]
        
        result = analyze_code_relationships(codes)
        matrix = result['similarity_matrix']
        
        # 矩阵应该是n×n
        assert len(matrix) == len(codes)
        assert all(len(row) == len(codes) for row in matrix)
    
    def test_relationship_structure(self):
        """测试关系结构"""
        codes = [
            {'concept': '学习方法', 'frequency': 5},
            {'concept': '学习计划', 'frequency': 3}
        ]
        
        result = analyze_code_relationships(codes)
        
        if len(result['relationships']) > 0:
            rel = result['relationships'][0]
            assert 'code' in rel
            assert 'related_codes' in rel
            assert isinstance(rel['related_codes'], list)
    
    def test_related_codes_limit(self):
        """测试相关编码数量限制"""
        codes = [
            {'concept': f'概念{i}', 'frequency': 5}
            for i in range(10)
        ]
        
        result = analyze_code_relationships(codes)
        
        # 每个编码最多3个相关编码
        for rel in result['relationships']:
            assert len(rel['related_codes']) <= 3
    
    def test_similarity_threshold(self):
        """测试相似度阈值"""
        codes = [
            {'concept': '学习方法', 'frequency': 5},
            {'concept': '情感体验', 'frequency': 3}  # 完全不同
        ]
        
        result = analyze_code_relationships(codes)
        
        # 不相关的编码不应该出现在关系中
        for rel in result['relationships']:
            for related in rel['related_codes']:
                assert related['similarity'] > 0.3


class TestIntegration:
    """集成测试"""
    
    def test_complete_comparison_workflow(self):
        """测试完整比较流程"""
        codes = [
            {'concept': '寻求帮助', 'frequency': 5},
            {'concept': '寻求帮助', 'frequency': 3},
            {'concept': '学习方法', 'frequency': 4},
            {'concept': '学习计划', 'frequency': 2}
        ]
        
        # 1. 识别重复
        duplicates = identify_duplicates(codes, threshold=0.8)
        assert len(duplicates) > 0
        
        # 2. 生成合并建议
        suggestions = suggest_merges(codes, duplicates)
        assert len(suggestions) > 0
        
        # 3. 分析关系
        relationships = analyze_code_relationships(codes)
        assert len(relationships['relationships']) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
