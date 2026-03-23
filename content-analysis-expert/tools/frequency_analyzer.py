#!/usr/bin/env python3
"""
Frequency Analyzer for Content Analysis
Analyzes frequency distributions and patterns in coded data
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple, Optional, Union
from collections import Counter

class FrequencyAnalyzer:
    """Analyze frequency distributions in content analysis data"""
    
    def __init__(self):
        self.data = None
        self.categories = None
    
    def load_data(self, coded_data: List, categories: List[str] = None):
        """Load coded data for analysis"""
        self.data = coded_data
        self.categories = categories or sorted(set(coded_data))
    
    def frequency_distribution(self, coded_data: List = None) -> Dict:
        """Calculate frequency distribution"""
        data = coded_data or self.data
        if data is None:
            raise ValueError("No data loaded")
        
        counter = Counter(data)
        total = len(data)
        
        results = {
            'total_units': total,
            'unique_categories': len(counter),
            'frequencies': {},
            'percentages': {},
            'cumulative': {}
        }
        
        cumsum = 0
        for cat, count in counter.most_common():
            pct = count / total * 100
            cumsum += pct
            
            results['frequencies'][cat] = count
            results['percentages'][cat] = round(pct, 2)
            results['cumulative'][cat] = round(cumsum, 2)
        
        return results
    
    def contingency_table(self, var1: List, var2: List, 
                         labels1: List = None, labels2: List = None) -> Dict:
        """Create contingency table for two variables"""
        
        if len(var1) != len(var2):
            raise ValueError("Variables must have same length")
        
        # Get unique values
        cats1 = labels1 or sorted(set(var1))
        cats2 = labels2 or sorted(set(var2))
        
        # Build table
        table = np.zeros((len(cats1), len(cats2)), dtype=int)
        
        for v1, v2 in zip(var1, var2):
            i = cats1.index(v1) if v1 in cats1 else -1
            j = cats2.index(v2) if v2 in cats2 else -1
            if i >= 0 and j >= 0:
                table[i, j] += 1
        
        # Calculate row and column totals
        row_totals = table.sum(axis=1)
        col_totals = table.sum(axis=0)
        grand_total = table.sum()
        
        # Expected frequencies
        expected = np.outer(row_totals, col_totals) / grand_total if grand_total > 0 else table
        
        return {
            'observed': table.tolist(),
            'expected': expected.tolist(),
            'row_labels': cats1,
            'col_labels': cats2,
            'row_totals': row_totals.tolist(),
            'col_totals': col_totals.tolist(),
            'grand_total': int(grand_total)
        }
    
    def chi_square_test(self, var1: List, var2: List) -> Dict:
        """Perform chi-square test of independence"""
        
        contingency = self.contingency_table(var1, var2)
        observed = np.array(contingency['observed'])
        expected = np.array(contingency['expected'])
        
        # Chi-square statistic
        # Exclude cells with expected < 5
        mask = expected >= 5
        if not np.any(mask):
            return {
                'error': 'All expected frequencies < 5, chi-square not valid',
                'recommendation': 'Use Fisher\'s exact test or combine categories'
            }
        
        chi2 = np.sum(((observed - expected)**2) / np.maximum(expected, 0.001))
        
        # Degrees of freedom
        df = (len(contingency['row_labels']) - 1) * (len(contingency['col_labels']) - 1)
        
        # P-value
        p_value = 1 - stats.chi2.cdf(chi2, df) if df > 0 else 1.0
        
        # Cramér's V
        n = contingency['grand_total']
        min_dim = min(len(contingency['row_labels']), len(contingency['col_labels'])) - 1
        cramers_v = np.sqrt(chi2 / (n * min_dim)) if min_dim > 0 and n > 0 else 0
        
        return {
            'chi_square': float(chi2),
            'df': int(df),
            'p_value': float(p_value),
            'significant': p_value < 0.05,
            'cramers_v': float(cramers_v),
            'effect_size_interpretation': self._interpret_cramers_v(cramers_v),
            'contingency_table': contingency
        }
    
    def _interpret_cramers_v(self, v: float) -> str:
        """Interpret Cramér's V effect size"""
        if v < 0.10:
            return "Negligible"
        elif v < 0.30:
            return "Small"
        elif v < 0.50:
            return "Medium"
        else:
            return "Large"
    
    def co_occurrence_matrix(self, categories_list: List[List]) -> Dict:
        """
        Calculate co-occurrence matrix for multiple codes per unit
        
        Parameters
        ----------
        categories_list : list of lists
            Each inner list contains codes applied to one unit
        """
        all_codes = sorted(set(code for codes in categories_list for code in codes))
        n_codes = len(all_codes)
        
        matrix = np.zeros((n_codes, n_codes), dtype=int)
        
        for codes in categories_list:
            for c1 in codes:
                for c2 in codes:
                    i = all_codes.index(c1)
                    j = all_codes.index(c2)
                    matrix[i, j] += 1
        
        # Calculate Jaccard similarity
        jaccard = np.zeros((n_codes, n_codes))
        for i in range(n_codes):
            for j in range(n_codes):
                intersection = matrix[i, j]
                union = matrix[i, i] + matrix[j, j] - intersection
                jaccard[i, j] = intersection / union if union > 0 else 0
        
        return {
            'co_occurrence': matrix.tolist(),
            'jaccard_similarity': jaccard.tolist(),
            'codes': all_codes,
            'n_units': len(categories_list)
        }
    
    def trend_analysis(self, time_periods: List, coded_data: List[List]) -> Dict:
        """
        Analyze trends across time periods
        
        Parameters
        ----------
        time_periods : list
            Time period labels
        coded_data : list of lists
            Frequency data for each category per period
        """
        results = {
            'periods': time_periods,
            'trends': {}
        }
        
        # Get all categories
        all_cats = sorted(set(cat for period in coded_data for cat in period))
        
        for cat in all_cats:
            freqs = [Counter(period).get(cat, 0) for period in coded_data]
            totals = [len(period) for period in coded_data]
            pcts = [f/t*100 if t > 0 else 0 for f, t in zip(freqs, totals)]
            
            # Linear trend test
            x = np.arange(len(time_periods))
            y = np.array(pcts)
            
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            results['trends'][cat] = {
                'frequencies': freqs,
                'percentages': [round(p, 2) for p in pcts],
                'trend_slope': round(slope, 4),
                'trend_direction': 'increasing' if slope > 0 else 'decreasing' if slope < 0 else 'stable',
                'r_squared': round(r_value**2, 3),
                'p_value': round(p_value, 4),
                'significant_trend': p_value < 0.05
            }
        
        return results
    
    def comparison_report(self, group1: List, group2: List, 
                         group_names: Tuple[str, str] = ('Group 1', 'Group 2')) -> Dict:
        """Compare frequency distributions between two groups"""
        
        freq1 = self.frequency_distribution(group1)
        freq2 = self.frequency_distribution(group2)
        
        all_cats = sorted(set(freq1['frequencies'].keys()) | set(freq2['frequencies'].keys()))
        
        comparisons = []
        for cat in all_cats:
            n1 = freq1['frequencies'].get(cat, 0)
            n2 = freq2['frequencies'].get(cat, 0)
            pct1 = freq1['percentages'].get(cat, 0)
            pct2 = freq2['percentages'].get(cat, 0)
            
            diff = pct2 - pct1
            
            # Z-test for proportions
            p1 = n1 / freq1['total_units'] if freq1['total_units'] > 0 else 0
            p2 = n2 / freq2['total_units'] if freq2['total_units'] > 0 else 0
            p_pooled = (n1 + n2) / (freq1['total_units'] + freq2['total_units'])
            
            se = np.sqrt(p_pooled * (1 - p_pooled) * 
                        (1/freq1['total_units'] + 1/freq2['total_units']))
            
            z = (p2 - p1) / se if se > 0 else 0
            p_value = 2 * (1 - stats.norm.cdf(abs(z)))
            
            comparisons.append({
                'category': cat,
                f'{group_names[0]}_n': n1,
                f'{group_names[0]}_%': pct1,
                f'{group_names[1]}_n': n2,
                f'{group_names[1]}_%': pct2,
                'difference': round(diff, 2),
                'z_value': round(z, 3),
                'p_value': round(p_value, 4),
                'significant': p_value < 0.05
            })
        
        return {
            'comparisons': comparisons,
            'group1_name': group_names[0],
            'group2_name': group_names[1],
            'group1_total': freq1['total_units'],
            'group2_total': freq2['total_units']
        }
    
    def generate_report(self, coded_data: List = None, 
                       format: str = 'markdown') -> str:
        """Generate formatted frequency report"""
        
        freq = self.frequency_distribution(coded_data)
        
        if format == 'markdown':
            lines = [
                "# Frequency Distribution Report\n",
                f"**Total Units**: {freq['total_units']}",
                f"**Unique Categories**: {freq['unique_categories']}\n",
                "## Distribution Table\n",
                "| Category | Frequency | Percentage | Cumulative |",
                "|----------|-----------|------------|------------|"
            ]
            
            for cat in freq['frequencies'].keys():
                lines.append(
                    f"| {cat} | {freq['frequencies'][cat]} | "
                    f"{freq['percentages'][cat]}% | {freq['cumulative'][cat]}% |"
                )
            
            return "\n".join(lines)
        
        return str(freq)


def main():
    """Test frequency analyzer"""
    analyzer = FrequencyAnalyzer()
    
    # Test data
    np.random.seed(42)
    n = 200
    
    # Simulate coded data
    codes = ['Economy', 'Environment', 'Politics', 'Science', 'Morality']
    coded_data = np.random.choice(codes, n, p=[0.35, 0.25, 0.20, 0.12, 0.08])
    
    print("=" * 60)
    print("FREQUENCY ANALYSIS REPORT")
    print("=" * 60)
    
    # Frequency distribution
    freq = analyzer.frequency_distribution(coded_data.tolist())
    
    print(f"\nTotal Units: {freq['total_units']}")
    print(f"Unique Categories: {freq['unique_categories']}")
    
    print("\nCategory Distribution:")
    print("-" * 40)
    
    for cat in freq['frequencies'].keys():
        print(f"  {cat}: {freq['frequencies'][cat]} ({freq['percentages'][cat]}%)")
    
    # Chi-square test
    print("\n" + "=" * 60)
    print("CHI-SQUARE TEST")
    print("=" * 60)
    
    var1 = np.random.choice(['A', 'B'], n)
    var2 = coded_data
    
    chi_result = analyzer.chi_square_test(var1.tolist(), var2.tolist())
    
    print(f"\nChi-square: {chi_result.get('chi_square', 'N/A'):.3f}")
    print(f"df: {chi_result.get('df', 'N/A')}")
    print(f"p-value: {chi_result.get('p_value', 'N/A'):.4f}")
    print(f"Significant: {chi_result.get('significant', 'N/A')}")
    print(f"Effect size (Cramér's V): {chi_result.get('cramers_v', 'N/A'):.3f}")


if __name__ == '__main__':
    main()
