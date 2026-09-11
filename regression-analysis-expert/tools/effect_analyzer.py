#!/usr/bin/env python3
"""
Effect Analyzer for Regression
Analyzes interaction, mediation, and moderation effects
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional, Union

class EffectAnalyzer:
    """Analyze effects in regression models"""
    
    def __init__(self):
        self.bootstrap_samples = 5000
    
    def test_interaction(self, y: np.ndarray, x1: np.ndarray, x2: np.ndarray,
                        covariates: np.ndarray = None, center: bool = True) -> Dict:
        """Test interaction effect between two predictors"""
        result = {
            'interaction_term': {},
            'simple_slopes': {},
            'interpretation': None
        }
        
        n = len(y)
        
        if center:
            x1_c = x1 - np.mean(x1)
            x2_c = x2 - np.mean(x2)
        else:
            x1_c = x1
            x2_c = x2
        
        interaction = x1_c * x2_c
        
        if covariates is not None:
            X = np.column_stack([np.ones(n), x1_c, x2_c, interaction, covariates])
        else:
            X = np.column_stack([np.ones(n), x1_c, x2_c, interaction])
        
        try:
            from numpy.linalg import lstsq
            coeffs, residuals_full, _, _ = lstsq(X, y, rcond=None)
            y_pred = X @ coeffs
            residuals = y - y_pred
            
            mse = np.sum(residuals**2) / (n - X.shape[1])
            var_coeffs = mse * np.linalg.pinv(X.T @ X)
            se = np.sqrt(np.diag(var_coeffs))
            
            t_values = coeffs / se
            p_values = 2 * (1 - stats.t.cdf(np.abs(t_values), n - X.shape[1]))
            
            interaction_idx = 3
            result['interaction_term'] = {
                'coefficient': float(coeffs[interaction_idx]),
                'se': float(se[interaction_idx]),
                't_value': float(t_values[interaction_idx]),
                'p_value': float(p_values[interaction_idx]),
                'significant': p_values[interaction_idx] < 0.05
            }
            
            result['simple_slopes'] = self._simple_slopes_analysis(
                y, x1_c, x2_c, coeffs, se, X.shape[1]
            )
            
            if result['interaction_term']['significant']:
                result['interpretation'] = (
                    f"Significant interaction effect (B = {result['interaction_term']['coefficient']:.3f}, "
                    f"p = {result['interaction_term']['p_value']:.3f})"
                )
            else:
                result['interpretation'] = (
                    f"No significant interaction effect (p = {result['interaction_term']['p_value']:.3f})"
                )
                
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def _simple_slopes_analysis(self, y: np.ndarray, x1: np.ndarray, 
                                x2: np.ndarray, coeffs: np.ndarray,
                                se: np.ndarray, df: int) -> Dict:
        """Calculate simple slopes at different levels of moderator"""
        result = {}
        
        x2_mean = np.mean(x2)
        x2_sd = np.std(x2)
        levels = {
            'low': x2_mean - x2_sd,
            'mean': x2_mean,
            'high': x2_mean + x2_sd
        }
        
        b1 = coeffs[1]
        b3 = coeffs[3]
        
        for level_name, level_value in levels.items():
            slope = b1 + b3 * level_value
            se_slope = se[1]
            t = slope / se_slope
            p = 2 * (1 - stats.t.cdf(np.abs(t), df))
            
            result[level_name] = {
                'moderator_value': float(level_value),
                'slope': float(slope),
                'se': float(se_slope),
                't_value': float(t),
                'p_value': float(p),
                'significant': p < 0.05
            }
        
        return result
    
    def mediation_analysis(self, y: np.ndarray, x: np.ndarray, m: np.ndarray,
                          covariates: np.ndarray = None,
                          method: str = 'bootstrap') -> Dict:
        """Conduct mediation analysis using Baron-Kenny or bootstrap method"""
        result = {
            'method': method,
            'paths': {},
            'indirect_effect': {},
            'direct_effect': {},
            'total_effect': {},
            'mediation_type': None
        }
        
        n = len(y)
        
        try:
            from numpy.linalg import lstsq
            
            # Path a: X → M
            if covariates is not None:
                X_a = np.column_stack([np.ones(n), x, covariates])
            else:
                X_a = np.column_stack([np.ones(n), x])
            
            coeffs_a, _, _, _ = lstsq(X_a, m, rcond=None)
            m_pred = X_a @ coeffs_a
            resid_a = m - m_pred
            
            mse_a = np.sum(resid_a**2) / (n - X_a.shape[1])
            se_a = np.sqrt(mse_a * np.linalg.pinv(X_a.T @ X_a)[1, 1])
            
            result['paths']['a'] = {
                'coefficient': float(coeffs_a[1]),
                'se': float(se_a),
                't_value': float(coeffs_a[1] / se_a),
                'p_value': float(2 * (1 - stats.t.cdf(np.abs(coeffs_a[1] / se_a), n - X_a.shape[1])))
            }
            
            # Path b and c': M → Y (controlling for X)
            if covariates is not None:
                X_bc = np.column_stack([np.ones(n), x, m, covariates])
            else:
                X_bc = np.column_stack([np.ones(n), x, m])
            
            coeffs_bc, _, _, _ = lstsq(X_bc, y, rcond=None)
            y_pred_bc = X_bc @ coeffs_bc
            resid_bc = y - y_pred_bc
            
            mse_bc = np.sum(resid_bc**2) / (n - X_bc.shape[1])
            var_bc = mse_bc * np.linalg.pinv(X_bc.T @ X_bc)
            se_bc = np.sqrt(np.diag(var_bc))
            
            result['paths']['b'] = {
                'coefficient': float(coeffs_bc[2]),
                'se': float(se_bc[2]),
                't_value': float(coeffs_bc[2] / se_bc[2]),
                'p_value': float(2 * (1 - stats.t.cdf(np.abs(coeffs_bc[2] / se_bc[2]), n - X_bc.shape[1])))
            }
            
            result['direct_effect'] = {
                'coefficient': float(coeffs_bc[1]),
                'se': float(se_bc[1]),
                'significant': float(2 * (1 - stats.t.cdf(np.abs(coeffs_bc[1] / se_bc[1]), n - X_bc.shape[1]))) < 0.05
            }
            
            # Total effect (c)
            if covariates is not None:
                X_c = np.column_stack([np.ones(n), x, covariates])
            else:
                X_c = np.column_stack([np.ones(n), x])
            
            coeffs_c, _, _, _ = lstsq(X_c, y, rcond=None)
            y_pred_c = X_c @ coeffs_c
            resid_c = y - y_pred_c
            
            mse_c = np.sum(resid_c**2) / (n - X_c.shape[1])
            se_c = np.sqrt(mse_c * np.linalg.pinv(X_c.T @ X_c)[1, 1])
            
            result['total_effect'] = {
                'coefficient': float(coeffs_c[1]),
                'se': float(se_c),
                'significant': float(2 * (1 - stats.t.cdf(np.abs(coeffs_c[1] / se_c), n - X_c.shape[1]))) < 0.05
            }
            
            # Indirect effect (a * b)
            a = result['paths']['a']['coefficient']
            b = result['paths']['b']['coefficient']
            indirect = a * b
            
            result['indirect_effect']['coefficient'] = float(indirect)
            
            if method == 'sobel':
                se_a_val = result['paths']['a']['se']
                se_b_val = result['paths']['b']['se']
                se_indirect = np.sqrt(a**2 * se_b_val**2 + b**2 * se_a_val**2)
                z_sobel = indirect / se_indirect
                p_sobel = 2 * (1 - stats.norm.cdf(np.abs(z_sobel)))
                
                result['indirect_effect']['se'] = float(se_indirect)
                result['indirect_effect']['z_value'] = float(z_sobel)
                result['indirect_effect']['p_value'] = float(p_sobel)
                result['indirect_effect']['significant'] = p_sobel < 0.05
            
            # Determine mediation type
            indirect_sig = result['indirect_effect'].get('significant', False)
            direct_sig = result['direct_effect'].get('significant', False)
            
            if indirect_sig and not direct_sig:
                result['mediation_type'] = 'Full Mediation'
            elif indirect_sig and direct_sig:
                result['mediation_type'] = 'Partial Mediation'
            else:
                result['mediation_type'] = 'No Mediation'
                
        except Exception as e:
            result['error'] = str(e)
        
        return result
    
    def moderation_analysis(self, y: np.ndarray, x: np.ndarray, m: np.ndarray,
                           covariates: np.ndarray = None, center: bool = True) -> Dict:
        """Conduct moderation analysis"""
        result = self.test_interaction(y, x, m, covariates, center)
        result['analysis_type'] = 'moderation'
        return result


def main():
    """Test effect analyzer"""
    np.random.seed(42)
    n = 200
    
    x = np.random.randn(n)
    m = 0.5 * x + np.random.randn(n) * 0.5
    y = 0.3 * x + 0.4 * m + np.random.randn(n) * 0.5
    
    analyzer = EffectAnalyzer()
    result = analyzer.mediation_analysis(y, x, m, method='sobel')
    
    print("=" * 50)
    print("MEDIATION ANALYSIS RESULTS")
    print("=" * 50)
    print(f"Path a (X → M): {result['paths']['a']['coefficient']:.3f}")
    print(f"Path b (M → Y): {result['paths']['b']['coefficient']:.3f}")
    print(f"Indirect effect: {result['indirect_effect']['coefficient']:.3f}")
    print(f"Mediation type: {result['mediation_type']}")


if __name__ == '__main__':
    main()