"""
信度分析工具的单元测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from reliability_analysis import (
    calculate_cronbach_alpha,
    calculate_split_half,
    calculate_test_retest,
    calculate_inter_rater
)


class TestCronbachAlpha:
    """测试Cronbach's α系数计算"""
    
    def test_high_reliability(self):
        """测试高信度数据"""
        data = [
            [4, 5, 3, 4, 5],  # 参与者1
            [3, 4, 4, 3, 4],  # 参与者2
            [5, 4, 5, 5, 4],  # 参与者3
            [4, 3, 4, 4, 5],  # 参与者4
        ]
        
        result = calculate_cronbach_alpha(data)
        
        assert result['alpha'] > 0.8  # 高信度
        assert result['n_items'] == 5
        assert result['n_subjects'] == 4
        assert result['interpretation'] in ['优秀', '良好']
    
    def test_low_reliability(self):
        """测试低信度数据"""
        data = [
            [1, 5, 1, 5, 1],  # 参与者1
            [5, 1, 5, 1, 5],  # 参与者2
            [1, 5, 1, 5, 1],  # 参与者3
        ]
        
        result = calculate_cronbach_alpha(data)
        
        assert result['alpha'] < 0.5  # 低信度
        assert result['interpretation'] in ['差', '不可接受']
    
    def test_single_item(self):
        """测试单个项目"""
        data = [[1]]
        
        result = calculate_cronbach_alpha(data)
        
        assert result['alpha'] == 0.0  # 无法计算
        assert result['n_items'] == 1


class TestSplitHalf:
    """测试折半信度"""
    
    def test_even_number_items(self):
        """测试偶数项目数"""
        data = [
            [3, 4, 5, 6],
            [2, 3, 4, 5],
            [4, 5, 6, 7],
            [1, 2, 3, 4]
        ]
        
        result = calculate_split_half(data)
        
        assert result['split_half'] >= 0.7  # 应该有较好的相关性
        assert result['first_half_items'] == 2
        assert result['second_half_items'] == 2
    
    def test_odd_number_items(self):
        """测试奇数项目数"""
        data = [
            [3, 4, 5],
            [2, 3, 4],
            [4, 5, 6]
        ]
        
        result = calculate_split_half(data)
        
        assert result['split_half'] >= 0.5
        assert result['first_half_items'] == 1
        assert result['second_half_items'] == 2


class TestTestRetest:
    """测试重测信度"""
    
    def test_high_correlation(self):
        """测试高相关性"""
        test = [80, 85, 90, 75, 95]
        retest = [82, 83, 91, 78, 93]
        
        result = calculate_test_retest(test, retest)
        
        assert result['test_retest'] > 0.8
        assert result['interpretation'] == '优秀'
        assert result['n_pairs'] == 5
    
    def test_low_correlation(self):
        """测试低相关性"""
        test = [80, 85, 90, 75, 95]
        retest = [60, 65, 70, 55, 75]
        
        result = calculate_test_retest(test, retest)
        
        assert result['test_retest'] < 0.5
        assert result['interpretation'] == '差'
    
    def test_different_lengths(self):
        """测试长度不匹配"""
        test = [80, 85, 90]
        retest = [82, 83, 91]
        
        result = calculate_test_retest(test, retest)
        
        assert result['test_retest'] == 0.0
        assert result['n_pairs'] == 0


class TestInterRater:
    """测试评分者间信度"""
    
    def test_high_agreement(self):
        """测试高度一致"""
        data = {
            'rater1': [4, 3, 5, 4],
            'rater2': [4, 3, 5, 4],
            'rater3': [4, 4, 5, 3]
        }
        
        result = calculate_inter_rater(data)
        
        assert result['kendall_w'] > 0.8
        assert result['interpretation'] == '优秀'
        assert result['n_raters'] == 3
        assert result['n_items'] == 4
    
    def test_low_agreement(self):
        """测试低度一致"""
        data = {
            'rater1': [1, 5, 1, 5],
            'rater2': [5, 1, 5, 1],
            'rater3': [3, 3, 3, 3]
        }
        
        result = calculate_inter_rater(data)
        
        assert result['kendall_w'] < 0.4
        assert result['interpretation'] == '差'
    
    def test_single_rater(self):
        """测试单个评分者"""
        data = {'rater1': [4, 3, 5, 4]}
        
        result = calculate_inter_rater(data)
        
        assert result['kendall_w'] == 0.0
        assert result['n_raters'] == 1


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])