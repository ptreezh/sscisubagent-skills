"""
描述性统计工具的单元测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from descriptive_stats import calculate_descriptive_stats


class TestDescriptiveStats:
    """测试描述性统计"""
    
    def test_basic_stats(self):
        """测试基本统计量"""
        data = [1.0, 2.0, 3.0, 4.0, 5.0]
        
        result = calculate_descriptive_stats(data)
        
        assert result['count'] == 5
        assert result['mean'] == 3.0
        assert result['median'] == 3.0
        assert result['min'] == 1.0
        assert result['max'] == 5.0
    
    def test_std_and_variance(self):
        """测试标准差和方差"""
        data = [2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0]
        
        result = calculate_descriptive_stats(data)
        
        # 验证方差和标准差的关系
        assert abs(result['variance'] - result['std']**2) < 0.01
        assert result['std'] > 0
    
    def test_quartiles(self):
        """测试四分位数"""
        data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
        
        result = calculate_descriptive_stats(data)
        
        assert result['q1'] == 3.25
        assert result['median'] == 5.5
        assert result['q3'] == 7.75
        assert result['iqr'] == result['q3'] - result['q1']
    
    def test_skewness_and_kurtosis(self):
        """测试偏度和峰度"""
        # 正态分布数据
        data = [1.0, 2.0, 3.0, 4.0, 5.0, 4.0, 3.0, 2.0, 1.0]
        
        result = calculate_descriptive_stats(data)
        
        # 偏度和峰度应该存在
        assert 'skewness' in result
        assert 'kurtosis' in result
    
    def test_single_value(self):
        """测试单一值"""
        data = [5.0]
        
        result = calculate_descriptive_stats(data)
        
        assert result['count'] == 1
        assert result['mean'] == 5.0
        assert result['std'] == 0.0


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
