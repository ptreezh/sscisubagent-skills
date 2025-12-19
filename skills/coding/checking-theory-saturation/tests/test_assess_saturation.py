"""
饱和度评估工具的单元测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from assess_saturation import (
    check_concept_saturation,
    check_category_completeness,
    check_relation_stability,
    check_theory_completeness,
    calculate_overall_saturation
)


class TestCheckConceptSaturation:
    """测试概念饱和度检查"""
    
    def test_fully_saturated(self):
        """测试完全饱和（无新概念）"""
        new_data = [{'concept': 'A'}, {'concept': 'B'}]
        existing = ['A', 'B', 'C']
        
        result = check_concept_saturation(new_data, existing)
        
        assert result['new_concept_count'] == 0
        assert result['new_concept_rate'] == 0.0
        assert result['is_saturated'] is True
        assert result['saturation_level'] == 'high'
    
    def test_partially_saturated(self):
        """测试部分饱和"""
        new_data = [{'concept': 'A'}, {'concept': 'D'}, {'concept': 'B'}]
        existing = ['A', 'B', 'C']
        
        result = check_concept_saturation(new_data, existing)
        
        assert result['new_concept_count'] == 1
        assert abs(result['new_concept_rate'] - 1/3) < 0.001
        assert result['is_saturated'] is False
        assert result['saturation_level'] == 'low'


class TestCheckCategoryCompleteness:
    """测试范畴完整性检查"""
    
    def test_all_complete(self):
        """测试所有范畴完整"""
        categories = [
            {'name': 'C1', 'definition': 'def', 'properties': ['p1'], 'examples': ['e1']},
            {'name': 'C2', 'definition': 'def', 'properties': ['p2'], 'examples': ['e2']}
        ]
        
        result = check_category_completeness(categories)
        
        assert result['complete_categories'] == 2
        assert result['completeness_rate'] == 1.0
        assert result['is_saturated'] is True
        assert result['saturation_level'] == 'high'
    
    def test_partial_complete(self):
        """测试部分完整"""
        categories = [
            {'name': 'C1', 'definition': 'def', 'properties': ['p1'], 'examples': ['e1']},
            {'name': 'C2', 'definition': 'def', 'properties': None, 'examples': ['e2']}
        ]
        
        result = check_category_completeness(categories)
        
        assert result['complete_categories'] == 1
        assert abs(result['completeness_rate'] - 0.5) < 0.001
        assert result['is_saturated'] is False


class TestCheckRelationStability:
    """测试关系稳定性检查"""
    
    def test_stable(self):
        """测试关系稳定"""
        existing = [
            {'source': 'A', 'target': 'B', 'type': 'causal'},
            {'source': 'B', 'target': 'C', 'type': 'causal'}
        ] * 10  # 20个现有关系
        
        new = [{'source': 'A', 'target': 'B', 'type': 'causal'}]  # 1个重复关系
        
        result = check_relation_stability(existing, new)
        
        assert result['truly_new_relations'] == 0
        assert result['new_relation_rate'] == 0.0
        assert result['is_saturated'] is True
    
    def test_unstable(self):
        """测试关系不稳定"""
        existing = [{'source': 'A', 'target': 'B', 'type': 'causal'}] * 5
        new = [
            {'source': 'C', 'target': 'D', 'type': 'causal'},
            {'source': 'E', 'target': 'F', 'type': 'causal'}
        ]
        
        result = check_relation_stability(existing, new)
        
        assert result['truly_new_relations'] == 2
        assert result['new_relation_rate'] > 0.10
        assert result['is_saturated'] is False


class TestCheckTheoryCompleteness:
    """测试理论完整性检查"""
    
    def test_complete_theory(self):
        """测试完整理论"""
        theory = {
            'core_category': '核心范畴',
            'propositions': ['命题1', '命题2'],
            'framework': {'structure': 'framework'},
            'boundaries': {'scope': 'boundary'}
        }
        
        result = check_theory_completeness(theory)
        
        assert result['complete_components'] == 4
        assert result['completeness_rate'] == 1.0
        assert result['is_saturated'] is True
    
    def test_incomplete_theory(self):
        """测试不完整理论"""
        theory = {
            'core_category': '核心范畴',
            'propositions': None
        }
        
        result = check_theory_completeness(theory)
        
        assert result['complete_components'] == 1
        assert result['completeness_rate'] == 0.25
        assert result['is_saturated'] is False


class TestCalculateOverallSaturation:
    """测试综合饱和度计算"""
    
    def test_fully_saturated(self):
        """测试完全饱和"""
        checks = {
            'concept_saturation': {'is_saturated': True},
            'category_completeness': {'is_saturated': True},
            'relation_stability': {'is_saturated': True},
            'theory_completeness': {'is_saturated': True}
        }
        
        result = calculate_overall_saturation(checks)
        
        assert result['overall_score'] == 1.0
        assert result['saturated_dimensions'] == 4
        assert result['saturation_level'] == 'fully_saturated'
    
    def test_mostly_saturated(self):
        """测试基本饱和"""
        checks = {
            'concept_saturation': {'is_saturated': True},
            'category_completeness': {'is_saturated': True},
            'relation_stability': {'is_saturated': True},
            'theory_completeness': {'is_saturated': False}
        }
        
        result = calculate_overall_saturation(checks)
        
        assert result['overall_score'] == 0.75
        assert result['saturated_dimensions'] == 3
        assert result['saturation_level'] == 'mostly_saturated'
    
    def test_not_saturated(self):
        """测试未饱和"""
        checks = {
            'concept_saturation': {'is_saturated': False},
            'category_completeness': {'is_saturated': False},
            'relation_stability': {'is_saturated': True},
            'theory_completeness': {'is_saturated': False}
        }
        
        result = calculate_overall_saturation(checks)
        
        assert result['overall_score'] == 0.25
        assert result['saturated_dimensions'] == 1
        assert result['saturation_level'] == 'not_saturated'


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
