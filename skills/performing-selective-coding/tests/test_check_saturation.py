"""
饱和度检验工具的单元测试
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from check_saturation import (
    check_new_concepts,
    check_category_completeness,
    check_relation_stability,
    assess_theory_completeness
)


class TestCheckNewConcepts:
    """测试新概念检查"""
    
    def test_no_new_concepts(self):
        """测试无新概念（已饱和）"""
        new_data = [
            {'concept': '概念A'},
            {'concept': '概念B'}
        ]
        existing = ['概念A', '概念B', '概念C']
        
        result = check_new_concepts(new_data, existing)
        
        assert result['new_concept_count'] == 0
        assert result['new_concept_rate'] == 0.0
        assert result['is_saturated'] is True
    
    def test_some_new_concepts(self):
        """测试有少量新概念"""
        new_data = [
            {'concept': '概念A'},
            {'concept': '概念D'},  # 新概念
            {'concept': '概念B'}
        ]
        existing = ['概念A', '概念B', '概念C']
        
        result = check_new_concepts(new_data, existing)
        
        assert result['new_concept_count'] == 1
        assert abs(result['new_concept_rate'] - 1/3) < 0.001
        assert result['is_saturated'] is False  # >5%未饱和
    
    def test_high_new_concept_rate(self):
        """测试高新概念率（未饱和）"""
        new_data = [
            {'concept': '概念D'},
            {'concept': '概念E'},
            {'concept': '概念F'}
        ]
        existing = ['概念A', '概念B', '概念C']
        
        result = check_new_concepts(new_data, existing)
        
        assert result['new_concept_count'] == 3
        assert result['new_concept_rate'] == 1.0
        assert result['is_saturated'] is False


class TestCheckCategoryCompleteness:
    """测试范畴完整性检查"""
    
    def test_all_complete(self):
        """测试所有范畴都完整"""
        categories = [
            {'definition': 'def1', 'properties': ['p1'], 'examples': ['e1']},
            {'definition': 'def2', 'properties': ['p2'], 'examples': ['e2']}
        ]
        
        result = check_category_completeness(categories)
        
        assert result['complete_categories'] == 2
        assert result['completeness_rate'] == 1.0
        assert result['is_saturated'] is True
    
    def test_partial_complete(self):
        """测试部分范畴完整"""
        categories = [
            {'definition': 'def1', 'properties': ['p1'], 'examples': ['e1']},
            {'definition': 'def2', 'properties': None, 'examples': ['e2']},  # 缺少properties
            {'definition': 'def3', 'properties': ['p3'], 'examples': None}   # 缺少examples
        ]
        
        result = check_category_completeness(categories)
        
        assert result['complete_categories'] == 1
        assert abs(result['completeness_rate'] - 1/3) < 0.001
        assert result['is_saturated'] is False


class TestCheckRelationStability:
    """测试关系稳定性检查"""
    
    def test_stable_relations(self):
        """测试关系稳定（少量新关系）"""
        existing_relations = [{'source': 'A', 'target': 'B'}] * 10
        new_relations = [{'source': 'C', 'target': 'D'}]  # 只有1个新关系
        
        result = check_relation_stability(existing_relations, new_relations)
        
        assert result['new_relations'] == 1
        assert result['new_relation_rate'] < 0.10
        assert result['is_saturated'] is True
    
    def test_unstable_relations(self):
        """测试关系不稳定（大量新关系）"""
        existing_relations = [{'source': 'A', 'target': 'B'}] * 5
        new_relations = [{'source': 'C', 'target': 'D'}] * 3  # 3个新关系
        
        result = check_relation_stability(existing_relations, new_relations)
        
        assert result['new_relations'] == 3
        assert result['new_relation_rate'] > 0.10
        assert result['is_saturated'] is False


class TestAssessTheoryCompleteness:
    """测试理论完整性评估"""
    
    def test_complete_theory(self):
        """测试完整的理论"""
        theory = {
            'core_category': '核心范畴',
            'propositions': ['命题1', '命题2'],
            'framework': {'structure': 'framework'},
            'boundaries': {'scope': 'boundary'}
        }
        
        result = assess_theory_completeness(theory)
        
        assert result['completeness_rate'] == 1.0
        assert result['is_saturated'] is True
    
    def test_incomplete_theory(self):
        """测试不完整的理论"""
        theory = {
            'core_category': '核心范畴',
            'propositions': None,  # 缺失
            'framework': None,     # 缺失
            'boundaries': {'scope': 'boundary'}
        }
        
        result = assess_theory_completeness(theory)
        
        assert result['completeness_rate'] == 0.5
        assert result['is_saturated'] is False


if __name__ == '__main__':
    import pytest
    pytest.main([__file__, '-v'])
