#!/usr/bin/env python3
"""
Regression Diagnostic Tester
Tests regression assumptions and provides diagnostic reports
"""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, List, Tuple, Optional, Union
import warnings

class RegressionDiagnostic:
    """Comprehensive regression diagnostics"""
    
    def __init__(self):
        self.thresholds = {
            'vif': {'good': 5, 'acceptable': 10},
            'cooks_d': 0.5,
            'leverage_factor': 2,
            'dw_lower': 1.5,
            'dw_upper': 2.5,
            'shapiro_p': 0.05,
            'bp_p': 0.05,
            'reset_p': 0.05
        }
    
    def run_all_diagnostics(self, y: np.ndarray, y_pred: np.ndarray, 
                           residuals: np.ndarray, X: np.ndarray,
                           X_with_const: np.ndarray = None) -> Dict:
        """
        Run all diagnostic tests
        
        Parameters
        ----------
        y : array
            Observed dependent variable
        y_pred : array
            Predicted values
        residuals : array
            Residuals (y - y_pred)
        X : array
            Independent variables (without constant)
        X_with_const : array, optional
            Independent variables with constant column
        
        Returns
        -------
        dict
            Comprehensive diagnostic results
        """
        results = {
            'summary': {},
            'details': {},
            'warnings': [],
            'recommendations': []
        }
        
        # 1. Normality of residuals
        results['details']['normality'] = self.test_normality(residuals)
        
        # 2. Homoscedasticity
        results['details']['homoscedasticity'] = self.test_homoscedasticity(
            y_pred, residuals, X
        )
        
        # 3. Linearity
        results['details']['linearity'] = self.test_linearity(
            y, y_pred, residuals, X
        )
        
        # 4. Multicollinearity
        results['details']['multicollinearity'] = self.test_multicollinearity(X)
        
        # 5. Independence (if time series)
        results['details']['independence'] = self.test_independence(residuals)
        
        # 6. Outliers and influential points
        results['details']['outliers'] = self.detect_outliers(
            residuals, X, X_with_const
        )
        
        # Generate summary
        results['summary'] = self._generate_summary(results['details'])
        
        # Generate recommendations
        results['recommendations'] = self._generate_recommendations(results['details'])
        
        return results
    
    def test_normality(self, residuals: np.ndarray) -> Dict:
        """Test normality of residuals"""
        residuals = residuals[~np.isnan(residuals)]
        n = len(residuals)
        
        result = {
            'test': 'Shapiro-Wilk',
            'statistic': None,
            'p_value': None,
            'interpretation': None,
            'passed': None
        }
        
        # Shapiro-Wilk (limited to 5000 samples)
        if n >= 3:
            if n <= 5000:
                stat, p = stats.shapiro(residuals)
                result['statistic'] = float(stat)
                result['p_value'] = float(p)
            else:
                # Use subsample
                stat, p = stats.shapiro(np.random.choice(residuals, 5000, replace=False))
                result['statistic'] = float(stat)
                result['p_value'] = float(p)
                result['note'] = "Test performed on subsample (n=5000)"
            
            result['passed'] = p > self.thresholds['shapiro_p']
            if result['passed']:
                result['interpretation'] = "✓ Residuals appear normally distributed (p > .05)"
            else:
                result['interpretation'] = "✗ Residuals may not be normally distributed (p < .05)"
        
        # Additional statistics
        result['skewness'] = float(stats.skew(residuals))
        result['kurtosis'] = float(stats.kurtosis(residuals))
        
        # Skewness/kurtosis interpretation
        if abs(result['skewness']) > 2:
            result['warnings'] = ["High skewness detected (|skew| > 2)"]
        if abs(result['kurtosis']) > 7:
            result['warnings'] = result.get('warnings', []) + ["High kurtosis detected (|kurtosis| > 7)"]
        
        return result
    
    def test_homoscedasticity(self, y_pred: np.ndarray, residuals: np.ndarray,
                              X: np.ndarray = None) -> Dict:
        """Test for homoscedasticity"""
        result = {
            'tests': {},
            'passed': None,
            'interpretation': None
        }
        
        # Breusch-Pagan test
        n = len(residuals)
        
        # Regress squared residuals on X
        if X is not None:
            resid_sq = residuals ** 2
            
            # Simple BP test implementation
            X_const = np.column_stack([np.ones(n), X])
            
            # Regression of squared residuals on X
            try:
                from numpy.linalg import lstsq
                coeffs, _, _, _ = lstsq(X_const, resid_sq, rcond=None)
                pred_resid_sq = X_const @ coeffs
                ss_explained = np.sum((pred_resid_sq - np.mean(resid_sq))**2)
                
                # LM statistic
                lm_stat = n * ss_explained / np.sum((resid_sq - np.mean(resid_sq))**2)
                p_value = 1 - stats.chi2.cdf(lm_stat, X.shape[1])
                
                result['tests']['breusch_pagan'] = {
                    'statistic': float(lm_stat),
                    'p_value': float(p_value),
                    'passed': p_value > self.thresholds['bp_p']
                }
            except:
                result['tests']['breusch_pagan'] = {
                    'error': 'Could not compute Breusch-Pagan test'
                }
        
        # White test (simplified - uses fitted values)
        resid_sq = residuals ** 2
        y_pred_sq = y_pred ** 2
        
        X_white = np.column_stack([np.ones(n), y_pred, y_pred_sq])
        try:
            from numpy.linalg import lstsq
            coeffs, _, _, _ = lstsq(X_white, resid_sq, rcond=None)
            pred_resid_sq = X_white @ coeffs
            ss_explained = np.sum((pred_resid_sq - np.mean(resid_sq))**2)
            
            lm_stat = n * ss_explained / np.sum((resid_sq - np.mean(resid_sq))**2)
            p_value = 1 - stats.chi2.cdf(lm_stat, 2)
            
            result['tests']['white'] = {
                'statistic': float(lm_stat),
                'p_value': float(p_value),
                'passed': p_value > self.thresholds['bp_p']
            }
        except:
            result['tests']['white'] = {'error': 'Could not compute White test'}
        
        # Overall assessment
        bp_passed = result['tests'].get('breusch_pagan', {}).get('passed', True)
        white_passed = result['tests'].get('white', {}).get('passed', True)
        
        result['passed'] = bp_passed and white_passed
        
        if result['passed']:
            result['interpretation'] = "✓ Homoscedasticity assumption satisfied"
        else:
            result['interpretation'] = "✗ Heteroscedasticity detected. Consider robust standard errors or WLS."
        
        return result
    
    def test_linearity(self, y: np.ndarray, y_pred: np.ndarray,
                      residuals: np.ndarray, X: np.ndarray = None) -> Dict:
        """Test linearity assumption"""
        result = {
            'tests': {},
            'passed': None,
            'interpretation': None
        }
        
        # Ramsey RESET test (simplified)
        n = len(y)
        y_pred_sq = y_pred ** 2
        y_pred_cubed = y_pred ** 3
        
        # Residuals regressed on powers of fitted values
        try:
            X_reset = np.column_stack([np.ones(n), y_pred, y_pred_sq, y_pred_cubed])
            from numpy.linalg import lstsq
            coeffs, _, _, _ = lstsq(X_reset, residuals, rcond=None)
            
            # F-test for squared and cubed terms
            ss_full = np.sum((residuals - X_reset @ coeffs)**2)
            ss_restricted = np.sum(residuals**2)
            
            # Simplified RESET statistic
            reset_stat = (ss_restricted - ss_full) / (ss_full / (n - 4))
            p_value = 1 - stats.f.cdf(reset_stat, 2, n - 4)
            
            result['tests']['reset'] = {
                'statistic': float(reset_stat),
                'p_value': float(p_value),
                'passed': p_value > self.thresholds['reset_p']
            }
            
            result['passed'] = result['tests']['reset']['passed']
            
            if result['passed']:
                result['interpretation'] = "✓ Linearity assumption satisfied"
            else:
                result['interpretation'] = "✗ Non-linear relationship detected. Consider polynomial terms or transformations."
                
        except Exception as e:
            result['tests']['reset'] = {'error': str(e)}
            result['passed'] = None
            result['interpretation'] = "Could not perform RESET test"
        
        # Visual check data (for plotting)
        result['residual_vs_fitted_data'] = {
            'fitted': y_pred[:1000].tolist() if len(y_pred) > 1000 else y_pred.tolist(),
            'residuals': residuals[:1000].tolist() if len(residuals) > 1000 else residuals.tolist()
        }
        
        return result
    
    def test_multicollinearity(self, X: np.ndarray) -> Dict:
        """Calculate VIF for multicollinearity detection"""
        result = {
            'vif_values': [],
            'max_vif': None,
            'mean_vif': None,
            'passed': None,
            'interpretation': None
        }
        
        if X is None or X.shape[1] < 2:
            result['interpretation'] = "Only one predictor - no multicollinearity concern"
            result['passed'] = True
            return result
        
        n_vars = X.shape[1]
        vif_values = []
        
        # Calculate VIF for each variable
        for i in range(n_vars):
            # Use other variables to predict variable i
            X_other = np.delete(X, i, axis=1)
            y_i = X[:, i]
            
            # Add constant
            X_other_const = np.column_stack([np.ones(len(y_i)), X_other])
            
            try:
                from numpy.linalg import lstsq
                coeffs, _, _, _ = lstsq(X_other_const, y_i, rcond=None)
                y_pred_i = X_other_const @ coeffs
                
                ss_tot = np.sum((y_i - np.mean(y_i))**2)
                ss_res = np.sum((y_i - y_pred_i)**2)
                
                r_squared = 1 - ss_res / ss_tot if ss_tot > 0 else 0
                
                if r_squared < 1:
                    vif = 1 / (1 - r_squared)
                else:
                    vif = float('inf')
                
                vif_values.append(float(vif) if vif != float('inf') else 999.99)
            except:
                vif_values.append(None)
        
        result['vif_values'] = vif_values
        valid_vifs = [v for v in vif_values if v is not None]
        
        if valid_vifs:
            result['max_vif'] = max(valid_vifs)
            result['mean_vif'] = np.mean(valid_vifs)
            
            # Assess multicollinearity
            if result['max_vif'] < self.thresholds['vif']['good']:
                result['passed'] = True
                result['interpretation'] = f"✓ No multicollinearity concerns (max VIF = {result['max_vif']:.2f})"
            elif result['max_vif'] < self.thresholds['vif']['acceptable']:
                result['passed'] = True
                result['interpretation'] = f"⚠ Moderate multicollinearity (max VIF = {result['max_vif']:.2f})"
            else:
                result['passed'] = False
                result['interpretation'] = f"✗ Severe multicollinearity (max VIF = {result['max_vif']:.2f})"
        else:
            result['interpretation'] = "Could not calculate VIF values"
        
        return result
    
    def test_independence(self, residuals: np.ndarray) -> Dict:
        """Test independence of residuals (Durbin-Watson)"""
        result = {
            'test': 'Durbin-Watson',
            'statistic': None,
            'passed': None,
            'interpretation': None
        }
        
        n = len(residuals)
        if n < 3:
            result['interpretation'] = "Insufficient data for DW test"
            return result
        
        # Calculate Durbin-Watson statistic
        diff = np.diff(residuals)
        dw = np.sum(diff**2) / np.sum(residuals**2)
        
        result['statistic'] = float(dw)
        
        # Interpretation (approximate)
        if self.thresholds['dw_lower'] <= dw <= self.thresholds['dw_upper']:
            result['passed'] = True
            result['interpretation'] = f"✓ No autocorrelation (DW = {dw:.3f})"
        elif dw < self.thresholds['dw_lower']:
            result['passed'] = False
            result['interpretation'] = f"✗ Positive autocorrelation detected (DW = {dw:.3f})"
        else:
            result['passed'] = False
            result['interpretation'] = f"✗ Negative autocorrelation detected (DW = {dw:.3f})"
        
        return result
    
    def detect_outliers(self, residuals: np.ndarray, X: np.ndarray,
                       X_with_const: np.ndarray = None) -> Dict:
        """Detect outliers and influential observations"""
        result = {
            'outliers': [],
            'influential': [],
            'summary': {}
        }
        
        n = len(residuals)
        p = X.shape[1] if X is not None else 1
        
        # Standardized residuals
        std_residuals = residuals / np.std(residuals)
        
        # 1. Outliers based on standardized residuals
        outlier_idx = np.where(np.abs(std_residuals) > 3)[0]
        for idx in outlier_idx:
            result['outliers'].append({
                'index': int(idx),
                'type': 'standardized_residual',
                'value': float(std_residuals[idx]),
                'threshold': 3
            })
        
        # 2. Leverage values
        if X_with_const is not None:
            try:
                # Hat matrix
                XtX_inv = np.linalg.pinv(X_with_const.T @ X_with_const)
                H = X_with_const @ XtX_inv @ X_with_const.T
                leverage = np.diag(H)
                
                leverage_threshold = self.thresholds['leverage_factor'] * (p + 1) / n
                high_leverage_idx = np.where(leverage > leverage_threshold)[0]
                
                for idx in high_leverage_idx:
                    result['outliers'].append({
                        'index': int(idx),
                        'type': 'leverage',
                        'value': float(leverage[idx]),
                        'threshold': float(leverage_threshold)
                    })
                
                # 3. Cook's Distance
                mse = np.sum(residuals**2) / (n - p - 1)
                cooks_d = (std_residuals**2 / (p + 1)) * (leverage / (1 - leverage))
                
                cooks_threshold = 4 / n
                influential_idx = np.where(cooks_d > cooks_threshold)[0]
                
                for idx in influential_idx:
                    result['influential'].append({
                        'index': int(idx),
                        'cooks_d': float(cooks_d[idx]),
                        'threshold': float(cooks_threshold)
                    })
                
            except Exception as e:
                result['error'] = f"Could not calculate leverage/Cook's D: {str(e)}"
        
        # Summary
        result['summary'] = {
            'n_outliers': len(result['outliers']),
            'n_influential': len(result['influential']),
            'outlier_proportion': len(result['outliers']) / n if n > 0 else 0,
            'interpretation': None
        }
        
        if result['summary']['n_outliers'] == 0:
            result['summary']['interpretation'] = "✓ No outliers detected"
        elif result['summary']['outlier_proportion'] < 0.05:
            result['summary']['interpretation'] = f"⚠ Few outliers detected ({result['summary']['n_outliers']} observations)"
        else:
            result['summary']['interpretation'] = f"✗ Many outliers detected ({result['summary']['n_outliers']} observations)"
        
        return result
    
    def _generate_summary(self, details: Dict) -> Dict:
        """Generate overall summary of diagnostics"""
        summary = {
            'assumptions_met': 0,
            'assumptions_total': 5,
            'status': None,
            'issues': []
        }
        
        # Check each assumption
        if details.get('normality', {}).get('passed'):
            summary['assumptions_met'] += 1
        else:
            summary['issues'].append('Non-normal residuals')
        
        if details.get('homoscedasticity', {}).get('passed'):
            summary['assumptions_met'] += 1
        else:
            summary['issues'].append('Heteroscedasticity')
        
        if details.get('linearity', {}).get('passed'):
            summary['assumptions_met'] += 1
        else:
            summary['issues'].append('Non-linearity')
        
        if details.get('multicollinearity', {}).get('passed'):
            summary['assumptions_met'] += 1
        else:
            summary['issues'].append('Multicollinearity')
        
        if details.get('independence', {}).get('passed', True):  # Default pass if not time series
            summary['assumptions_met'] += 1
        else:
            summary['issues'].append('Autocorrelation')
        
        # Overall status
        if summary['assumptions_met'] == summary['assumptions_total']:
            summary['status'] = '✅ All assumptions satisfied'
        elif summary['assumptions_met'] >= summary['assumptions_total'] - 1:
            summary['status'] = '⚠️ Minor assumption violations'
        else:
            summary['status'] = '❌ Multiple assumption violations'
        
        return summary
    
    def _generate_recommendations(self, details: Dict) -> List[str]:
        """Generate recommendations based on diagnostic results"""
        recommendations = []
        
        # Normality
        if not details.get('normality', {}).get('passed', True):
            recommendations.append(
                "Consider variable transformation (log, sqrt) or robust methods"
            )
        
        # Homoscedasticity
        if not details.get('homoscedasticity', {}).get('passed', True):
            recommendations.append(
                "Use robust standard errors (HC0-HC3) or Weighted Least Squares"
            )
        
        # Linearity
        if not details.get('linearity', {}).get('passed', True):
            recommendations.append(
                "Add polynomial terms, use splines, or apply nonlinear transformations"
            )
        
        # Multicollinearity
        if not details.get('multicollinearity', {}).get('passed', True):
            recommendations.append(
                "Remove redundant predictors, use PCA, or apply ridge regression"
            )
        
        # Outliers
        outliers = details.get('outliers', {}).get('summary', {})
        if outliers.get('n_influential', 0) > 0:
            recommendations.append(
                f"Investigate {outliers['n_influential']} influential observations. Consider robust regression."
            )
        
        return recommendations


def main():
    """Test diagnostic module"""
    # Generate test data
    np.random.seed(42)
    n = 200
    X = np.random.randn(n, 3)
    y = 2 + 1.5 * X[:, 0] + 0.5 * X[:, 1] + np.random.randn(n) * 2
    
    # Fit OLS
    X_const = np.column_stack([np.ones(n), X])
    from numpy.linalg import lstsq
    coeffs, _, _, _ = lstsq(X_const, y, rcond=None)
    y_pred = X_const @ coeffs
    residuals = y - y_pred
    
    # Run diagnostics
    diagnostic = RegressionDiagnostic()
    results = diagnostic.run_all_diagnostics(y, y_pred, residuals, X, X_const)
    
    print("=" * 60)
    print("REGRESSION DIAGNOSTIC REPORT")
    print("=" * 60)
    print(f"\nOverall Status: {results['summary']['status']}")
    print(f"Assumptions Met: {results['summary']['assumptions_met']}/{results['summary']['assumptions_total']}")
    
    if results['summary']['issues']:
        print(f"\nIssues Found: {', '.join(results['summary']['issues'])}")
    
    print("\nDetailed Results:")
    print("-" * 40)
    
    for test_name, test_result in results['details'].items():
        print(f"\n{test_name.upper()}:")
        if 'interpretation' in test_result:
            print(f"  {test_result['interpretation']}")
        if 'passed' in test_result:
            print(f"  Passed: {test_result['passed']}")
    
    if results['recommendations']:
        print("\n" + "=" * 60)
        print("RECOMMENDATIONS:")
        for i, rec in enumerate(results['recommendations'], 1):
            print(f"  {i}. {rec}")


if __name__ == '__main__':
    main()
