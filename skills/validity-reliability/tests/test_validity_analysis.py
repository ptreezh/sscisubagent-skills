"""
效度分析工具的单元测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from validity_analysis import (
    calculate_content_validity,
    calculate_construct_validity,
    calculate_criterion_validity,
    calculate_convergent_discriminant
)


class TestContentValidity:
    """测试内容效度"""
    
    def test_high_validity(self):
        """测试高效度"""
        expert_ratings = [
            {'ratings': [4, 5, 4, 5]},  # 项目1
            {'ratings': [5, 4, 5, 5]},  # 项目2
            {'ratings': [4, 4, 4, 4]},  # 项目3
        ]
        
        result = calculate_content_validity(expert_ratings)
        
        assert result['content_validity_index'] > 0.8
        assert result['interpretation'] in ['优秀', '良好']
        assert result['n_experts'] == 3
        assert result['n_items'] == 3
    
    def test_low_validity(self):
        """测试低效度"""
        expert_ratings = [
            {'ratings': [1, 2, 1, 2]},  # 项目1
            {'ratings': [2, 1, 2, 1]},  # 项目2
            {'ratings': [1, 1, 2, 1]},  # 项目3
        ]
        
        result = calculate_content_validity(expert_ratings)
        
        assert result['content_validity_index'] < 0.5
        assert result['interpretation'] in ['需要改进', '可接受']
    
    def test_no_ratings(self):
        """测试无评定数据"""
        result = calculate_content_validity([])
        
        assert result['content_validity_index'] == 0.0
        assert result['n_experts'] == 0


class TestConstructValidity:
    """测试结构效度"""
    
    def test_high_validity(self):
        """测试高效度"""
        test_scores = [80, 85, 90, 75, 95]
        related_scores = [78, 83, 88, 77, 92]
        
        result = calculate_construct_validity(test_scores, related_scores)
        
        assert result['construct_validity'] > 0.9
        assert result['interpretation'] == '优秀'
        assert result['statistical_significance'] is True
    
    def test_low_validity(self):
        """测试低效度"""
        test_scores = [80, 85, 90, 75, 95]
        related_scores = [40, 45, 50, 35, 55]
        
        result = calculate_construct_validity(test_scores, related_scores)
        
        assert result['construct_validity'] < 0.5
        assert result['interpretation'] in ['需要改进', '可接受']
    
    def test_different_lengths(self):
        """测试长度不匹配"""
        test_scores = [80, 85, 90]
        related_scores = [78, 83, 88, 77, 92]
        
        result = calculate_construct_validity(test_scores, related_scores)
        
        assert result['construct_validity'] == 0.0
        assert result['n_pairs'] == 0


class TestCriterionValidity:
    """测试效标效度"""
    
    def test_high_validity(self):
        """测试高效度"""
        test_scores = [70, 75, 80, 85, 90]
        criterion_scores = [72, 77, 82, 87, 92]
        
        result = calculate_criterion_validity(test_scores, criterion_scores)
        
        assert result['criterion_validity'] > 0.9
        assert result['r_squared'] > 0.8
        assert result['interpretation'] == '优秀'
    
    def test_moderate_validity(self):
        """测试中等效度"""
        test_scores = [70, 75, 80, 85, 90]
        criterion_scores = [65, 70, 75, 80, 85]
        
        result = calculate_criterion_validity(test_scores, criterion_scores)
        
        assert 0.6 <= result['criterion_validity'] <= 0.8
        assert result['interpretation'] in ['良好', '可接受']


class TestConvergentDiscriminant:
    """测试聚合效度和区分效度"""
    
    def test_good_validity(self):
        """测试良好效度"""
        test1 = [80, 85, 90, 75, 95]
        test2 = [82, 83, 88, 77, 93]  # 高相关性
        unrelated = [50, 55, 60, 65, 70]  # 低相关性
        
        result = calculate_convergent_discriminant(test1, test2, unrelated)
        
        assert result['convergent_validity']['acceptable'] is True
        assert result['discriminant_validity']['acceptable'] is True
        assert result['overall_validity'] is True
    
    def test_poor_discriminant(self):
        """测试区分效度差"""
        test1 = [80, 85, 90, 75, 95]
        test2 = [82, 83, 88, 77, 93]  # 高相关性
        unrelated = [78, 84, 89, 76, 94]  # 也高相关性
        
        result = calculate_convergent_discriminant(test1, test2, unrelated)
        
        assert result['convergent_validity']['acceptable'] is True
        assert result['discriminant_validity']['acceptable'] is False
        assert result['overall_validity'] is False


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])