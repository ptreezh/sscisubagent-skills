#!/usr/bin/env python3
"""
Sample Size Calculator for RCT
Calculates required sample size for various RCT designs
"""

import numpy as np
from scipy import stats
from typing import Dict, Tuple, Optional

class SampleSizeCalculator:
    """Calculate sample size for RCT designs"""
    
    def __init__(self):
        self.z_values = {
            0.05: 1.96,  # Two-sided α = 0.05
            0.025: 1.96,  # One-sided α = 0.025
            0.01: 2.576,  # Two-sided α = 0.01
        }
        self.z_power = {
            0.80: 0.842,
            0.85: 1.036,
            0.90: 1.282,
            0.95: 1.645,
        }
    
    def continuous_outcome(self, mean_diff: float, std_dev: float,
                          alpha: float = 0.05, power: float = 0.80,
                          allocation_ratio: float = 1.0,
                          dropout_rate: float = 0.0) -> Dict:
        """
        Calculate sample size for continuous outcome
        
        Parameters
        ----------
        mean_diff : float
            Expected mean difference between groups
        std_dev : float
            Pooled standard deviation
        alpha : float
            Significance level (two-sided)
        power : float
            Statistical power (1 - β)
        allocation_ratio : float
            Ratio of sample sizes (n2/n1)
        dropout_rate : float
            Expected dropout rate (0-0.5)
        
        Returns
        -------
        dict
            Sample size calculations
        """
        z_alpha = self.z_values.get(alpha, 1.96)
        z_beta = self.z_power.get(power, 0.842)
        
        # Standard formula
        n1 = ((z_alpha + z_beta)**2 * std_dev**2 * (1 + allocation_ratio)) / (mean_diff**2)
        n1 = int(np.ceil(n1))
        
        n2 = int(np.ceil(n1 * allocation_ratio))
        
        # Effect size (Cohen's d)
        effect_size = mean_diff / std_dev
        
        # Adjust for dropout
        if dropout_rate > 0:
            n1_adj = int(np.ceil(n1 / (1 - dropout_rate)))
            n2_adj = int(np.ceil(n2 / (1 - dropout_rate)))
        else:
            n1_adj, n2_adj = n1, n2
        
        return {
            'n_per_group': n1,
            'n_group1': n1,
            'n_group2': n2,
            'total': n1 + n2,
            'adjusted_n_group1': n1_adj,
            'adjusted_n_group2': n2_adj,
            'adjusted_total': n1_adj + n2_adj,
            'dropout_rate': dropout_rate,
            'effect_size_cohen_d': round(effect_size, 3),
            'effect_size_interpretation': self._interpret_cohens_d(effect_size),
            'parameters': {
                'mean_difference': mean_diff,
                'standard_deviation': std_dev,
                'alpha': alpha,
                'power': power,
                'allocation_ratio': allocation_ratio
            }
        }
    
    def binary_outcome(self, p1: float, p2: float,
                       alpha: float = 0.05, power: float = 0.80,
                       allocation_ratio: float = 1.0,
                       dropout_rate: float = 0.0) -> Dict:
        """
        Calculate sample size for binary outcome
        
        Parameters
        ----------
        p1 : float
            Proportion in control group
        p2 : float
            Expected proportion in intervention group
        """
        z_alpha = self.z_values.get(alpha, 1.96)
        z_beta = self.z_power.get(power, 0.842)
        
        # Pooled proportion
        p_bar = (p1 + allocation_ratio * p2) / (1 + allocation_ratio)
        
        # Formula
        numerator = (z_alpha * np.sqrt((1 + allocation_ratio) * p_bar * (1 - p_bar)) +
                    z_beta * np.sqrt(p1 * (1 - p1) + allocation_ratio * p2 * (1 - p2)))**2
        denominator = (p1 - p2)**2
        
        n1 = int(np.ceil(numerator / denominator / allocation_ratio))
        n2 = int(np.ceil(n1 * allocation_ratio))
        
        # Effect sizes
        rr = p2 / p1 if p1 > 0 else float('inf')
        or_val = (p2 / (1 - p2)) / (p1 / (1 - p1)) if p1 < 1 and p2 < 1 else float('inf')
        
        # Adjust for dropout
        if dropout_rate > 0:
            n1_adj = int(np.ceil(n1 / (1 - dropout_rate)))
            n2_adj = int(np.ceil(n2 / (1 - dropout_rate)))
        else:
            n1_adj, n2_adj = n1, n2
        
        return {
            'n_per_group': n1,
            'n_group1': n1,
            'n_group2': n2,
            'total': n1 + n2,
            'adjusted_n_group1': n1_adj,
            'adjusted_n_group2': n2_adj,
            'adjusted_total': n1_adj + n2_adj,
            'dropout_rate': dropout_rate,
            'effect_sizes': {
                'risk_ratio': round(rr, 3),
                'odds_ratio': round(or_val, 3),
                'risk_difference': round(p2 - p1, 3)
            },
            'parameters': {
                'p_control': p1,
                'p_intervention': p2,
                'alpha': alpha,
                'power': power,
                'allocation_ratio': allocation_ratio
            }
        }
    
    def survival_outcome(self, hazard_ratio: float, 
                        median_control: float,
                        accrual_time: float,
                        follow_up_time: float,
                        alpha: float = 0.05, power: float = 0.80,
                        dropout_rate: float = 0.0) -> Dict:
        """
        Calculate sample size for time-to-event outcome
        """
        z_alpha = self.z_values.get(alpha, 1.96)
        z_beta = self.z_power.get(power, 0.842)
        
        # Control event rate
        lambda_control = np.log(2) / median_control
        
        # Overall event probability
        # Simplified approximation
        p_event = 1 - np.exp(-lambda_control * follow_up_time)
        
        # Number of events needed
        d = ((z_alpha + z_beta)**2) / (np.log(hazard_ratio)**2) * 4
        d = int(np.ceil(d))
        
        # Total sample size
        n_total = int(np.ceil(d / p_event))
        n_per_group = n_total // 2
        
        # Adjust for dropout
        if dropout_rate > 0:
            n_total_adj = int(np.ceil(n_total / (1 - dropout_rate)))
            n_per_group_adj = n_total_adj // 2
        else:
            n_total_adj = n_total
            n_per_group_adj = n_per_group
        
        return {
            'events_needed': d,
            'n_per_group': n_per_group,
            'total': n_total,
            'adjusted_total': n_total_adj,
            'adjusted_n_per_group': n_per_group_adj,
            'event_rate': round(p_event, 3),
            'parameters': {
                'hazard_ratio': hazard_ratio,
                'median_control_months': median_control,
                'accrual_time_months': accrual_time,
                'follow_up_time_months': follow_up_time,
                'alpha': alpha,
                'power': power
            }
        }
    
    def non_inferiority(self, margin: float, std_dev: float = None,
                        p_control: float = None,
                        alpha: float = 0.025, power: float = 0.80,
                        dropout_rate: float = 0.0) -> Dict:
        """
        Calculate sample size for non-inferiority trial
        """
        z_alpha = stats.norm.ppf(1 - alpha)  # One-sided
        z_beta = self.z_power.get(power, 0.842)
        
        if std_dev is not None:
            # Continuous outcome
            n = 2 * ((z_alpha + z_beta)**2) * std_dev**2 / margin**2
            n = int(np.ceil(n))
        elif p_control is not None:
            # Binary outcome (simplified)
            n = ((z_alpha + z_beta)**2 * 2 * p_control * (1 - p_control)) / margin**2
            n = int(np.ceil(n))
        else:
            return {'error': 'Need std_dev or p_control'}
        
        n_adj = int(np.ceil(n / (1 - dropout_rate))) if dropout_rate > 0 else n
        
        return {
            'n_per_group': n,
            'total': n * 2,
            'adjusted_n_per_group': n_adj,
            'adjusted_total': n_adj * 2,
            'non_inferiority_margin': margin,
            'parameters': {
                'margin': margin,
                'alpha_one_sided': alpha,
                'power': power
            }
        }
    
    def cluster_rct(self, icc: float, cluster_size: int,
                   mean_diff: float = None, std_dev: float = None,
                   p1: float = None, p2: float = None,
                   alpha: float = 0.05, power: float = 0.80) -> Dict:
        """
        Calculate sample size for cluster RCT
        """
        # Design effect
        design_effect = 1 + (cluster_size - 1) * icc
        
        # Get individual-level sample size
        if mean_diff is not None and std_dev is not None:
            individual = self.continuous_outcome(mean_diff, std_dev, alpha, power)
        elif p1 is not None and p2 is not None:
            individual = self.binary_outcome(p1, p2, alpha, power)
        else:
            return {'error': 'Need continuous or binary parameters'}
        
        n_individual = individual['n_per_group']
        
        # Adjusted sample size
        n_adjusted = int(np.ceil(n_individual * design_effect))
        
        # Number of clusters
        n_clusters = int(np.ceil(n_adjusted / cluster_size))
        
        return {
            'n_individuals_per_arm': n_adjusted,
            'n_clusters_per_arm': n_clusters,
            'total_individuals': n_adjusted * 2,
            'total_clusters': n_clusters * 2,
            'design_effect': round(design_effect, 3),
            'icc': icc,
            'cluster_size': cluster_size,
            'individual_sample_size': n_individual,
            'inflation_factor': round(design_effect, 2)
        }
    
    def _interpret_cohens_d(self, d: float) -> str:
        """Interpret Cohen's d effect size"""
        d_abs = abs(d)
        if d_abs < 0.2:
            return "Negligible"
        elif d_abs < 0.5:
            return "Small"
        elif d_abs < 0.8:
            return "Medium"
        else:
            return "Large"
    
    def power_analysis(self, n: int, mean_diff: float = None, std_dev: float = None,
                       p1: float = None, p2: float = None,
                       alpha: float = 0.05) -> Dict:
        """
        Calculate achieved power for given sample size
        """
        z_alpha = self.z_values.get(alpha, 1.96)
        n_per_group = n // 2
        
        if mean_diff is not None and std_dev is not None:
            # Continuous
            effect_size = mean_diff / std_dev
            z_beta = np.sqrt(n_per_group / 2) * effect_size - z_alpha
            power = stats.norm.cdf(z_beta)
        elif p1 is not None and p2 is not None:
            # Binary
            p_bar = (p1 + p2) / 2
            se = np.sqrt(2 * p_bar * (1 - p_bar) / n_per_group)
            z = abs(p1 - p2) / se
            z_beta = z - z_alpha
            power = stats.norm.cdf(z_beta)
        else:
            return {'error': 'Need continuous or binary parameters'}
        
        return {
            'power': round(power, 3),
            'sample_size_per_group': n_per_group,
            'total_sample_size': n,
            'alpha': alpha
        }


def main():
    """Test sample size calculator"""
    calc = SampleSizeCalculator()
    
    print("=" * 60)
    print("SAMPLE SIZE CALCULATIONS FOR RCT")
    print("=" * 60)
    
    # Continuous outcome
    print("\n1. CONTINUOUS OUTCOME")
    print("-" * 40)
    result = calc.continuous_outcome(
        mean_diff=5,      # 5 unit difference
        std_dev=10,       # SD = 10
        power=0.80,
        dropout_rate=0.15
    )
    print(f"Mean difference: 5, SD: 10")
    print(f"Sample size per group: {result['n_per_group']}")
    print(f"Adjusted (15% dropout): {result['adjusted_n_per_group']}")
    print(f"Effect size (Cohen's d): {result['effect_size_cohen_d']} ({result['effect_size_interpretation']})")
    
    # Binary outcome
    print("\n2. BINARY OUTCOME")
    print("-" * 40)
    result = calc.binary_outcome(
        p1=0.20,          # 20% in control
        p2=0.30,          # 30% in intervention
        power=0.80
    )
    print(f"Control: 20%, Intervention: 30%")
    print(f"Sample size per group: {result['n_per_group']}")
    print(f"Risk ratio: {result['effect_sizes']['risk_ratio']}")
    print(f"Odds ratio: {result['effect_sizes']['odds_ratio']}")


if __name__ == '__main__':
    main()
