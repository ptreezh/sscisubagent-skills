#!/usr/bin/env python3
"""
Inter-Coder Reliability Tester
Calculates various reliability coefficients for content analysis
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional, Union
from collections import Counter
import warnings

class ReliabilityTester:
    """Calculate inter-coder reliability coefficients"""
    
    def __init__(self):
        self.coefficients = {}
    
    def calculate_all(self, coder1: List, coder2: List, 
                     data_type: str = 'nominal') -> Dict:
        """
        Calculate all applicable reliability coefficients
        
        Parameters
        ----------
        coder1, coder2 : list
            Coding decisions from two coders
        data_type : str
            Type of data: 'nominal', 'ordinal', 'interval', 'ratio'
        
        Returns
        -------
        dict
            All calculated reliability coefficients
        """
        results = {
            'data_type': data_type,
            'n_items': len(coder1),
            'coefficients': {}
        }
        
        # Percent Agreement
        results['coefficients']['percent_agreement'] = self.percent_agreement(coder1, coder2)
        
        # Cohen's Kappa (nominal)
        results['coefficients']['cohens_kappa'] = self.cohens_kappa(coder1, coder2)
        
        # Scott's Pi (nominal)
        results['coefficients']['scotts_pi'] = self.scotts_pi(coder1, coder2)
        
        # Krippendorff's Alpha (all types)
        results['coefficients']['krippendorffs_alpha'] = self.krippendorffs_alpha(
            [coder1, coder2], data_type
        )
        
        # Interpretation
        results['interpretation'] = self._interpret_results(results['coefficients'])
        
        return results
    
    def percent_agreement(self, coder1: List, coder2: List) -> Dict:
        """Calculate simple percent agreement"""
        if len(coder1) != len(coder2):
            raise ValueError("Coder lists must have same length")
        
        n = len(coder1)
        agreements = sum(1 for a, b in zip(coder1, coder2) if a == b)
        po = agreements / n
        
        return {
            'value': float(po),
            'agreements': agreements,
            'total': n,
            'interpretation': self._interpret_agreement(po)
        }
    
    def cohens_kappa(self, coder1: List, coder2: List) -> Dict:
        """
        Calculate Cohen's Kappa
        
        κ = (Po - Pe) / (1 - Pe)
        
        where Po = observed agreement
              Pe = expected agreement by chance
        """
        if len(coder1) != len(coder2):
            raise ValueError("Coder lists must have same length")
        
        n = len(coder1)
        
        # Observed agreement
        agreements = sum(1 for a, b in zip(coder1, coder2) if a == b)
        po = agreements / n
        
        # Expected agreement by chance
        categories = sorted(set(coder1) | set(coder2))
        
        # Marginal probabilities
        p1_dist = Counter(coder1)
        p2_dist = Counter(coder2)
        
        pe = sum(
            (p1_dist[cat] / n) * (p2_dist[cat] / n) 
            for cat in categories
        )
        
        # Kappa calculation
        if pe == 1:
            kappa = 1.0
        else:
            kappa = (po - pe) / (1 - pe)
        
        # Standard error (approximate)
        se = self._kappa_se(kappa, n, po, pe)
        
        # Z-test
        z_value = kappa / se if se > 0 else 0
        p_value = 2 * (1 - stats.norm.cdf(abs(z_value)))
        
        return {
            'value': float(kappa),
            'po': float(po),
            'pe': float(pe),
            'se': float(se),
            'z_value': float(z_value),
            'p_value': float(p_value),
            'interpretation': self._interpret_kappa(kappa)
        }
    
    def _kappa_se(self, kappa: float, n: int, po: float, pe: float) -> float:
        """Calculate standard error for Cohen's Kappa"""
        if n < 2:
            return 0
        
        # Approximate SE formula
        se_squared = (po * (1 - po)) / (n * (1 - pe)**2)
        return np.sqrt(max(0, se_squared))
    
    def scotts_pi(self, coder1: List, coder2: List) -> Dict:
        """
        Calculate Scott's Pi
        
        Similar to Cohen's Kappa but uses joint marginal probabilities
        """
        if len(coder1) != len(coder2):
            raise ValueError("Coder lists must have same length")
        
        n = len(coder1)
        
        # Observed agreement
        agreements = sum(1 for a, b in zip(coder1, coder2) if a == b)
        po = agreements / n
        
        # Expected agreement (joint marginals)
        categories = sorted(set(coder1) | set(coder2))
        
        joint_dist = Counter(coder1) + Counter(coder2)
        pe = sum(
            (joint_dist[cat] / (2 * n))**2 
            for cat in categories
        )
        
        # Pi calculation
        if pe == 1:
            pi = 1.0
        else:
            pi = (po - pe) / (1 - pe)
        
        return {
            'value': float(pi),
            'po': float(po),
            'pe': float(pe),
            'interpretation': self._interpret_kappa(pi)  # Same thresholds as Kappa
        }
    
    def krippendorffs_alpha(self, coders: List[List], 
                           data_type: str = 'nominal') -> Dict:
        """
        Calculate Krippendorff's Alpha
        
        α = 1 - Do/De
        
        where Do = observed disagreement
              De = expected disagreement
        
        Supports nominal, ordinal, interval, and ratio data
        """
        n_items = len(coders[0])
        n_coders = len(coders)
        
        # Build coincidence matrix
        categories = sorted(set().union(*[set(c) for c in coders]))
        cat_to_idx = {cat: i for i, cat in enumerate(categories)}
        n_cats = len(categories)
        
        # Calculate observed and expected disagreement
        if data_type == 'nominal':
            delta = self._nominal_delta
        elif data_type == 'ordinal':
            delta = self._ordinal_delta
        elif data_type == 'interval':
            delta = self._interval_delta
        else:
            delta = self._nominal_delta
        
        # Count coincidences
        coincidence = np.zeros((n_cats, n_cats))
        
        for i in range(n_items):
            values = [coders[j][i] for j in range(n_coders)]
            for j, v1 in enumerate(values):
                for k, v2 in enumerate(values):
                    if j != k and v1 is not None and v2 is not None:
                        coincidence[cat_to_idx[v1], cat_to_idx[v2]] += 1
        
        # Total pairs
        total = np.sum(coincidence)
        
        if total == 0:
            return {
                'value': None,
                'error': 'No valid pairs for comparison',
                'interpretation': 'Cannot calculate'
            }
        
        # Calculate Do and De
        Do = 0
        De = 0
        
        n_u = np.sum(coincidence, axis=1)
        
        for c1 in range(n_cats):
            for c2 in range(n_cats):
                if c1 != c2:
                    Do += coincidence[c1, c2] * delta(categories[c1], categories[c2])
        
        Do /= total
        
        for c1 in range(n_cats):
            for c2 in range(n_cats):
                if c1 != c2:
                    De += n_u[c1] * n_u[c2] * delta(categories[c1], categories[c2])
        
        De /= (total * (n_coders - 1))
        
        # Alpha
        if De == 0:
            alpha = 1.0
        else:
            alpha = 1 - (Do / De)
        
        return {
            'value': float(alpha),
            'do': float(Do),
            'de': float(De),
            'data_type': data_type,
            'interpretation': self._interpret_alpha(alpha)
        }
    
    def _nominal_delta(self, c1, c2) -> float:
        """Nominal difference metric"""
        return 0.0 if c1 == c2 else 1.0
    
    def _ordinal_delta(self, c1, c2, categories: List) -> float:
        """Ordinal difference metric"""
        if c1 == c2:
            return 0.0
        i1 = categories.index(c1)
        i2 = categories.index(c2)
        return (i2 - i1)**2
    
    def _interval_delta(self, c1, c2) -> float:
        """Interval difference metric"""
        try:
            return (float(c1) - float(c2))**2
        except:
            return self._nominal_delta(c1, c2)
    
    def fleiss_kappa(self, ratings: np.ndarray) -> Dict:
        """
        Calculate Fleiss' Kappa for multiple raters
        
        Parameters
        ----------
        ratings : array
            Shape (n_items, n_categories), counts of ratings per category
        
        Returns
        -------
        dict
            Fleiss' Kappa results
        """
        n_items, n_cats = ratings.shape
        n_ratings = np.sum(ratings[0])  # Ratings per item
        
        # Proportion of ratings per category
        p_j = np.sum(ratings, axis=0) / (n_items * n_ratings)
        
        # Agreement per item
        P_i = (np.sum(ratings**2, axis=1) - n_ratings) / (n_ratings * (n_ratings - 1))
        
        # Mean agreement
        P_bar = np.mean(P_i)
        
        # Expected agreement
        P_e = np.sum(p_j**2)
        
        # Kappa
        if P_e == 1:
            kappa = 1.0
        else:
            kappa = (P_bar - P_e) / (1 - P_e)
        
        return {
            'value': float(kappa),
            'p_bar': float(P_bar),
            'p_e': float(P_e),
            'interpretation': self._interpret_kappa(kappa)
        }
    
    def _interpret_agreement(self, po: float) -> str:
        """Interpret percent agreement"""
        if po >= 0.95:
            return "Excellent (≥95%)"
        elif po >= 0.90:
            return "Good (90-94%)"
        elif po >= 0.80:
            return "Acceptable (80-89%)"
        else:
            return "Poor (<80%)"
    
    def _interpret_kappa(self, kappa: float) -> str:
        """Interpret Kappa/Alpha values"""
        if kappa >= 0.80:
            return "Excellent (≥0.80)"
        elif kappa >= 0.60:
            return "Good (0.60-0.79)"
        elif kappa >= 0.40:
            return "Moderate (0.40-0.59)"
        elif kappa >= 0.20:
            return "Fair (0.20-0.39)"
        else:
            return "Poor (<0.20)"
    
    def _interpret_alpha(self, alpha: float) -> str:
        """Interpret Krippendorff's Alpha (stricter thresholds)"""
        if alpha >= 0.80:
            return "Excellent - Reliable for conclusions (≥0.80)"
        elif alpha >= 0.67:
            return "Acceptable for tentative conclusions (0.67-0.79)"
        elif alpha >= 0.50:
            return "Questionable reliability (0.50-0.66)"
        else:
            return "Unreliable - Do not draw conclusions (<0.50)"
    
    def _interpret_results(self, coefficients: Dict) -> Dict:
        """Provide overall interpretation"""
        interpretations = []
        
        # Check key coefficients
        if 'krippendorffs_alpha' in coefficients:
            alpha = coefficients['krippendorffs_alpha'].get('value')
            if alpha is not None:
                if alpha >= 0.80:
                    interpretations.append("✓ High reliability - suitable for publication")
                elif alpha >= 0.67:
                    interpretations.append("⚠ Acceptable reliability - note limitations")
                else:
                    interpretations.append("✗ Low reliability - recoding needed")
        
        if 'cohens_kappa' in coefficients:
            kappa = coefficients['cohens_kappa'].get('value')
            if kappa is not None:
                if kappa >= 0.70:
                    interpretations.append("✓ Kappa indicates acceptable agreement")
                else:
                    interpretations.append("⚠ Kappa below recommended threshold (0.70)")
        
        return {
            'overall': interpretations[0] if interpretations else "No interpretation available",
            'recommendations': self._get_recommendations(coefficients)
        }
    
    def _get_recommendations(self, coefficients: Dict) -> List[str]:
        """Generate recommendations based on results"""
        recs = []
        
        alpha = coefficients.get('krippendorffs_alpha', {}).get('value')
        kappa = coefficients.get('cohens_kappa', {}).get('value')
        po = coefficients.get('percent_agreement', {}).get('value')
        
        if alpha and alpha < 0.67:
            recs.append("Consider revising coding scheme definitions")
            recs.append("Provide additional coder training")
            recs.append("Add more examples to coding book")
        
        if kappa and po and (po - kappa) > 0.20:
            recs.append("High agreement but low Kappa suggests category imbalance")
            recs.append("Review marginal distributions for rare categories")
        
        if po and po > 0.90 and kappa and kappa < 0.60:
            recs.append("Paradox detected: high agreement but low Kappa")
            recs.append("Check for prevalence bias in categories")
        
        return recs if recs else ["Reliability levels are acceptable"]


def main():
    """Test reliability calculations"""
    tester = ReliabilityTester()
    
    # Test data
    np.random.seed(42)
    n = 100
    
    # High agreement scenario
    coder1 = np.random.choice(['A', 'B', 'C'], n, p=[0.5, 0.3, 0.2])
    coder2 = coder1.copy()
    # Add some disagreement
    for i in range(15):
        idx = np.random.randint(n)
        coder2[idx] = np.random.choice(['A', 'B', 'C'])
    
    print("=" * 60)
    print("INTER-CODER RELIABILITY TEST RESULTS")
    print("=" * 60)
    
    results = tester.calculate_all(coder1.tolist(), coder2.tolist())
    
    print(f"\nData Type: {results['data_type']}")
    print(f"N Items: {results['n_items']}")
    
    print("\nCoefficients:")
    print("-" * 40)
    
    for name, result in results['coefficients'].items():
        value = result.get('value', 'N/A')
        if isinstance(value, float):
            print(f"  {name}: {value:.3f}")
        else:
            print(f"  {name}: {value}")
        print(f"    → {result.get('interpretation', '')}")
    
    print("\nOverall Interpretation:")
    print("-" * 40)
    print(f"  {results['interpretation']['overall']}")
    
    print("\nRecommendations:")
    for rec in results['interpretation']['recommendations']:
        print(f"  • {rec}")


if __name__ == '__main__':
    main()
