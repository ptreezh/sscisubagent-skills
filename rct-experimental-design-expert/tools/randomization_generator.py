#!/usr/bin/env python3
"""
Randomization Sequence Generator
Generates randomization sequences for RCT designs
"""

import numpy as np
import hashlib
from typing import Dict, List, Tuple, Optional
from collections import Counter

class RandomizationGenerator:
    """Generate randomization sequences for RCT"""
    
    def __init__(self, seed: int = None):
        self.seed = seed
        if seed:
            np.random.seed(seed)
    
    def simple_randomization(self, n: int, 
                            allocation_ratio: Dict[str, int] = None) -> Dict:
        """
        Simple randomization
        
        Parameters
        ----------
        n : int
            Total sample size
        allocation_ratio : dict
            Ratio of allocations, e.g., {'A': 1, 'B': 1} for 1:1
        """
        if allocation_ratio is None:
            allocation_ratio = {'A': 1, 'B': 1}
        
        groups = []
        for group, ratio in allocation_ratio.items():
            groups.extend([group] * ratio)
        
        sequence = [np.random.choice(groups) for _ in range(n)]
        
        return {
            'method': 'Simple Randomization',
            'sequence': sequence,
            'counts': dict(Counter(sequence)),
            'n_total': n,
            'allocation_ratio': allocation_ratio
        }
    
    def block_randomization(self, n: int, 
                           block_sizes: List[int] = None,
                           allocation_ratio: Dict[str, int] = None) -> Dict:
        """
        Block randomization with variable block sizes
        
        Parameters
        ----------
        n : int
            Total sample size
        block_sizes : list
            Possible block sizes, e.g., [4, 6, 8]
        allocation_ratio : dict
            Ratio of allocations
        """
        if allocation_ratio is None:
            allocation_ratio = {'A': 1, 'B': 1}
        if block_sizes is None:
            block_sizes = [4, 6]
        
        # Validate block sizes
        total_ratio = sum(allocation_ratio.values())
        valid_blocks = [b for b in block_sizes if b % total_ratio == 0]
        if not valid_blocks:
            return {'error': f'Block sizes must be multiples of {total_ratio}'}
        
        sequence = []
        block_info = []
        subject_id = 1
        
        while len(sequence) < n:
            block_size = np.random.choice(valid_blocks)
            block_sequence = self._generate_block(block_size, allocation_ratio)
            
            for group in block_sequence:
                if len(sequence) < n:
                    sequence.append(group)
                    block_info.append({
                        'subject_id': subject_id,
                        'group': group,
                        'block_number': len(block_info) // block_size + 1,
                        'block_size': block_size
                    })
                    subject_id += 1
        
        return {
            'method': 'Block Randomization',
            'sequence': sequence,
            'block_details': block_info,
            'counts': dict(Counter(sequence)),
            'n_total': n,
            'block_sizes_used': block_sizes,
            'allocation_ratio': allocation_ratio
        }
    
    def _generate_block(self, block_size: int, 
                        allocation_ratio: Dict[str, int]) -> List[str]:
        """Generate a single randomization block"""
        block = []
        total_ratio = sum(allocation_ratio.values())
        
        for group, ratio in allocation_ratio.items():
            n_in_block = int(block_size * ratio / total_ratio)
            block.extend([group] * n_in_block)
        
        np.random.shuffle(block)
        return block
    
    def stratified_randomization(self, n: int,
                                strata: Dict[str, List],
                                allocation_ratio: Dict[str, int] = None,
                                block_size: int = 4) -> Dict:
        """
        Stratified block randomization
        
        Parameters
        ----------
        strata : dict
            Stratification factors, e.g., {'age': ['<50', '>=50'], 'sex': ['M', 'F']}
        """
        if allocation_ratio is None:
            allocation_ratio = {'A': 1, 'B': 1}
        
        # Generate all stratum combinations
        import itertools
        stratum_names = list(strata.keys())
        stratum_values = list(strata.values())
        combinations = list(itertools.product(*stratum_values))
        
        results = {
            'method': 'Stratified Block Randomization',
            'n_total': n,
            'strata': strata,
            'stratum_combinations': [],
            'overall_sequence': [],
            'overall_counts': {}
        }
        
        # Generate sequence for each stratum
        for combo in combinations:
            stratum_label = '_'.join(str(v) for v in combo)
            
            # Assume equal distribution across strata (simplified)
            n_per_stratum = n // len(combinations)
            
            block_result = self.block_randomization(
                n_per_stratum,
                block_sizes=[block_size],
                allocation_ratio=allocation_ratio
            )
            
            stratum_info = {
                'stratum': stratum_label,
                'factors': dict(zip(stratum_names, combo)),
                'n': n_per_stratum,
                'sequence': block_result['sequence'],
                'counts': block_result['counts']
            }
            
            results['stratum_combinations'].append(stratum_info)
            results['overall_sequence'].extend(block_result['sequence'])
        
        results['overall_counts'] = dict(Counter(results['overall_sequence']))
        
        return results
    
    def minimization(self, n: int,
                    factors: Dict[str, List[str]],
                    factor_weights: Dict[str, float] = None,
                    groups: List[str] = None,
                    probability: float = 0.8) -> Dict:
        """
        Minimization (dynamic allocation)
        
        Parameters
        ----------
        factors : dict
            Prognostic factors
        factor_weights : dict
            Weights for each factor
        groups : list
            Treatment groups
        probability : float
            Probability of assigning to optimal group (not 1 to maintain randomness)
        """
        if groups is None:
            groups = ['A', 'B']
        if factor_weights is None:
            factor_weights = {f: 1.0 for f in factors.keys()}
        
        sequence = []
        subject_details = []
        
        # Track assignments by factor level
        assignments = {g: {f: {level: 0 for level in levels} 
                          for f, levels in factors.items()} 
                      for g in groups}
        
        for i in range(n):
            # Generate random factor values for this subject
            subject_factors = {f: np.random.choice(levels) 
                             for f, levels in factors.items()}
            
            # Calculate imbalance for each group
            imbalance = {}
            for group in groups:
                total_imbalance = 0
                for factor, level in subject_factors.items():
                    # Sum of differences from other groups
                    other_groups = [g for g in groups if g != group]
                    diff = sum(abs(assignments[group][factor][level] - 
                                  assignments[g][factor][level]) 
                              for g in other_groups)
                    total_imbalance += factor_weights[factor] * diff
                imbalance[group] = total_imbalance
            
            # Find optimal group (minimum imbalance)
            min_imbalance = min(imbalance.values())
            optimal_groups = [g for g, imb in imbalance.items() 
                            if imb == min_imbalance]
            
            # Assign with probability
            if len(optimal_groups) == 1:
                if np.random.random() < probability:
                    assigned_group = optimal_groups[0]
                else:
                    other_groups = [g for g in groups if g not in optimal_groups]
                    assigned_group = np.random.choice(other_groups)
            else:
                assigned_group = np.random.choice(optimal_groups)
            
            sequence.append(assigned_group)
            
            # Update assignments
            for factor, level in subject_factors.items():
                assignments[assigned_group][factor][level] += 1
            
            subject_details.append({
                'subject_id': i + 1,
                'group': assigned_group,
                'factors': subject_factors
            })
        
        return {
            'method': 'Minimization',
            'sequence': sequence,
            'subject_details': subject_details,
            'counts': dict(Counter(sequence)),
            'n_total': n,
            'factors': factors,
            'factor_weights': factor_weights,
            'probability': probability
        }
    
    def generate_allocation_table(self, sequence: List[str],
                                  subject_ids: List[str] = None,
                                  include_envelope: bool = True) -> Dict:
        """Generate allocation table for trial use"""
        n = len(sequence)
        
        if subject_ids is None:
            subject_ids = [f"S{str(i+1).zfill(4)}" for i in range(n)]
        
        table = []
        for i, (sid, group) in enumerate(zip(subject_ids, sequence)):
            row = {
                'envelope_number': i + 1,
                'subject_id': sid,
                'allocation': group
            }
            table.append(row)
        
        return {
            'allocation_table': table,
            'n_total': n,
            'include_envelope_system': include_envelope
        }
    
    def concealment_verification(self, method: str = 'opaque_envelopes') -> Dict:
        """Verify allocation concealment methods"""
        methods = {
            'opaque_envelopes': {
                'description': 'Sequentially numbered, opaque, sealed envelopes',
                'pros': ['Simple', 'Low cost'],
                'cons': ['Risk of unblinding', 'Not suitable for multi-center'],
                'recommendation': 'Good for single-center trials'
            },
            'central_telephone': {
                'description': 'Central telephone/website randomization',
                'pros': ['High security', 'Multi-center compatible'],
                'cons': ['Requires infrastructure', 'May delay allocation'],
                'recommendation': 'Recommended for multi-center trials'
            },
            'pharmacy_controlled': {
                'description': 'Pharmacy-controlled allocation',
                'pros': ['Good for drug trials', 'Maintains blinding'],
                'cons': ['Requires pharmacy involvement'],
                'recommendation': 'Standard for pharmaceutical trials'
            }
        }
        
        return {
            'method': method,
            'details': methods.get(method, {}),
            'all_methods': list(methods.keys())
        }


def main():
    """Test randomization generator"""
    gen = RandomizationGenerator(seed=42)
    
    print("=" * 60)
    print("RANDOMIZATION SEQUENCE GENERATION")
    print("=" * 60)
    
    # Block randomization
    print("\n1. BLOCK RANDOMIZATION")
    print("-" * 40)
    result = gen.block_randomization(
        n=20,
        block_sizes=[4, 6],
        allocation_ratio={'Intervention': 1, 'Control': 1}
    )
    print(f"Sequence: {result['sequence']}")
    print(f"Counts: {result['counts']}")
    
    # Minimization
    print("\n2. MINIMIZATION")
    print("-" * 40)
    result = gen.minimization(
        n=20,
        factors={'age': ['<50', '>=50'], 'sex': ['M', 'F']},
        groups=['A', 'B']
    )
    print(f"Sequence: {result['sequence']}")
    print(f"Counts: {result['counts']}")


if __name__ == '__main__':
    main()
