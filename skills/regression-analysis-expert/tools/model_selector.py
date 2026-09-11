#!/usr/bin/env python3
"""
Regression Model Selector
Selects appropriate regression model based on data characteristics
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional, Union
import warnings

class RegressionModelSelector:
    """Selects appropriate regression model for given data"""
    
    def __init__(self):
        self.recommendations = {
            'ols': {
                'name': 'OLS Regression',
                'library': 'statsmodels',
                'requirements': ['Continuous dependent variable', 'Linear relationship', 'Homoscedasticity']
            },
            'logistic': {
                'name': 'Logistic Regression',
                'library': 'statsmodels',
                'requirements': ['Binary dependent variable']
            },
            'multinomial': {
                'name': 'Multinomial Logistic Regression',
                'library': 'statsmodels',
                'requirements': ['Nominal dependent variable with >2 categories']
            },
            'ordinal': {
                'name': 'Ordinal Logistic Regression',
                'library': 'statsmodels',
                'requirements': ['Ordinal dependent variable']
            },
            'poisson': {
                'name': 'Poisson Regression',
                'library': 'statsmodels',
                'requirements': ['Count dependent variable', 'Mean ≈ Variance']
            },
            'negative_binomial': {
                'name': 'Negative Binomial Regression',
                'library': 'statsmodels',
                'requirements': ['Count dependent variable', 'Overdispersion']
            },
            'robust': {
                'name': 'Robust Regression',
                'library': 'statsmodels',
                'requirements': ['Continuous dependent variable', 'Outliers present']
            }
        }
    
    def analyze_dependent_variable(self, y: np.ndarray) -> Dict:
        """Analyze characteristics of dependent variable"""
        result = {
            'n_obs': len(y),
            'n_missing': np.sum(np.isnan(y)),
            'dtype': self._infer_type(y)
        }
        
        if result['dtype'] == 'continuous':
            result.update(self._analyze_continuous(y))
        elif result['dtype'] == 'binary':
            result.update(self._analyze_binary(y))
        elif result['dtype'] == 'ordinal':
            result.update(self._analyze_ordinal(y))
        elif result['dtype'] == 'nominal':
            result.update(self._analyze_nominal(y))
        elif result['dtype'] == 'count':
            result.update(self._analyze_count(y))
        
        return result
    
    def _infer_type(self, y: np.ndarray) -> str:
        """Infer variable type from data"""
        y_clean = y[~np.isnan(y)]
        
        # Check if binary
        unique_values = np.unique(y_clean)
        if len(unique_values) == 2:
            return 'binary'
        
        # Check if count (non-negative integers)
        if np.all(y_clean == y_clean.astype(int)) and np.all(y_clean >= 0):
            # Check variance vs mean for count type
            if np.mean(y_clean) > 0:
                return 'count'
        
        # Check if categorical (few unique values)
        if len(unique_values) <= 10 and len(unique_values) < len(y_clean) * 0.1:
            # Could be ordinal or nominal - need more context
            return 'categorical'
        
        # Default to continuous
        return 'continuous'
    
    def _analyze_continuous(self, y: np.ndarray) -> Dict:
        """Analyze continuous variable"""
        y_clean = y[~np.isnan(y)]
        
        return {
            'mean': float(np.mean(y_clean)),
            'std': float(np.std(y_clean)),
            'min': float(np.min(y_clean)),
            'max': float(np.max(y_clean)),
            'skewness': float(stats.skew(y_clean)),
            'kurtosis': float(stats.kurtosis(y_clean)),
            'shapiro_p': stats.shapiro(y_clean[:5000])[1] if len(y_clean) >= 3 else None,
            'outliers': self._detect_outliers(y_clean)
        }
    
    def _analyze_binary(self, y: np.ndarray) -> Dict:
        """Analyze binary variable"""
        y_clean = y[~np.isnan(y)]
        unique, counts = np.unique(y_clean, return_counts=True)
        
        return {
            'categories': unique.tolist(),
            'counts': counts.tolist(),
            'proportions': (counts / len(y_clean)).tolist(),
            'balance_ratio': min(counts) / max(counts) if max(counts) > 0 else 0
        }
    
    def _analyze_ordinal(self, y: np.ndarray) -> Dict:
        """Analyze ordinal variable"""
        y_clean = y[~np.isnan(y)]
        unique, counts = np.unique(y_clean, return_counts=True)
        
        return {
            'n_categories': len(unique),
            'categories': unique.tolist(),
            'counts': counts.tolist(),
            'median': float(np.median(y_clean))
        }
    
    def _analyze_nominal(self, y: np.ndarray) -> Dict:
        """Analyze nominal variable"""
        y_clean = y[~np.isnan(y)]
        unique, counts = np.unique(y_clean, return_counts=True)
        
        return {
            'n_categories': len(unique),
            'categories': unique.tolist(),
            'counts': counts.tolist(),
            'mode': unique[np.argmax(counts)]
        }
    
    def _analyze_count(self, y: np.ndarray) -> Dict:
        """Analyze count variable for Poisson vs Negative Binomial"""
        y_clean = y[~np.isnan(y)]
        mean = np.mean(y_clean)
        var = np.var(y_clean)
        
        return {
            'mean': float(mean),
            'variance': float(var),
            'dispersion': float(var / mean) if mean > 0 else float('inf'),
            'overdispersed': var > mean * 1.5,
            'zeros': int(np.sum(y_clean == 0)),
            'zero_proportion': float(np.sum(y_clean == 0) / len(y_clean))
        }
    
    def _detect_outliers(self, y: np.ndarray, method: str = 'iqr') -> np.ndarray:
        """Detect outliers using specified method"""
        if method == 'iqr':
            q1, q3 = np.percentile(y, [25, 75])
            iqr = q3 - q1
            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr
            return (y < lower) | (y > upper)
        elif method == 'zscore':
            z = np.abs(stats.zscore(y))
            return z > 3
        return np.zeros(len(y), dtype=bool)
    
    def recommend_model(self, y: np.ndarray, x: np.ndarray = None, 
                       assumptions: Dict = None) -> Dict:
        """
        Recommend appropriate regression model
        
        Parameters
        ----------
        y : array-like
            Dependent variable
        x : array-like, optional
            Independent variables (for additional diagnostics)
        assumptions : dict, optional
            Pre-tested assumptions (linearity, normality, etc.)
        
        Returns
        -------
        dict
            Model recommendation with rationale
        """
        y_analysis = self.analyze_dependent_variable(y)
        
        recommendation = {
            'y_analysis': y_analysis,
            'recommended_model': None,
            'alternative_models': [],
            'rationale': [],
            'requirements_check': []
        }
        
        dtype = y_analysis['dtype']
        
        # Decision logic
        if dtype == 'binary':
            recommendation['recommended_model'] = 'logistic'
            recommendation['rationale'].append("Binary dependent variable → Logistic regression")
            recommendation['requirements_check'].append("✓ Binary outcome (2 categories)")
            
        elif dtype == 'continuous':
            # Check for outliers
            outlier_prop = np.mean(y_analysis.get('outliers', []))
            
            if outlier_prop > 0.05:
                recommendation['recommended_model'] = 'robust'
                recommendation['rationale'].append(
                    f"Outliers detected ({outlier_prop:.1%}) → Robust regression recommended"
                )
                recommendation['alternative_models'].append('ols')
            else:
                recommendation['recommended_model'] = 'ols'
                recommendation['rationale'].append("Continuous dependent variable → OLS regression")
                
                if y_analysis.get('shapiro_p', 1) < 0.05:
                    recommendation['rationale'].append(
                        "Note: Non-normal distribution detected. Consider transformation or robust methods."
                    )
                    recommendation['alternative_models'].extend(['robust'])
        
        elif dtype == 'count':
            dispersion = y_analysis.get('dispersion', 1)
            
            if dispersion <= 1.5:
                recommendation['recommended_model'] = 'poisson'
                recommendation['rationale'].append(
                    f"Count data with dispersion ≈ 1 ({dispersion:.2f}) → Poisson regression"
                )
            else:
                recommendation['recommended_model'] = 'negative_binomial'
                recommendation['rationale'].append(
                    f"Count data with overdispersion ({dispersion:.2f}) → Negative Binomial regression"
                )
                recommendation['alternative_models'].append('poisson')
        
        elif dtype == 'categorical':
            # Need to distinguish ordinal vs nominal
            # For now, default to multinomial
            recommendation['recommended_model'] = 'multinomial'
            recommendation['rationale'].append("Categorical dependent variable → Multinomial regression")
            recommendation['requirements_check'].append(
                "! Verify if categories are ordinal (use ordinal logistic) or nominal"
            )
        
        # Add model details
        if recommendation['recommended_model']:
            model_name = recommendation['recommended_model']
            recommendation['model_info'] = self.recommendations.get(model_name, {})
        
        # Sample size check
        n = y_analysis['n_obs']
        k = x.shape[1] if x is not None else 1
        
        if dtype in ['continuous', 'binary']:
            min_n = 10 * k
            if n < min_n:
                recommendation['warnings'] = [
                    f"⚠ Sample size (n={n}) may be insufficient. Recommended: n ≥ {min_n}"
                ]
        
        # For logistic, check events per variable
        if dtype == 'binary' and x is not None:
            minority_count = min(y_analysis['counts'])
            epv = minority_count / k
            if epv < 10:
                recommendation['warnings'] = recommendation.get('warnings', [])
                recommendation['warnings'].append(
                    f"⚠ Events per variable (EPV={epv:.1f}) < 10. Risk of overfitting."
                )
        
        return recommendation
    
    def get_model_syntax(self, model_type: str, y_name: str, x_names: List[str],
                        library: str = 'statsmodels') -> str:
        """Generate model syntax for specified library"""
        
        if library == 'statsmodels':
            if model_type == 'ols':
                return f"""
import statsmodels.api as sm
X = sm.add_constant(df[{x_names}])
model = sm.OLS(df['{y_name}'], X).fit()
print(model.summary())
"""
            elif model_type == 'logistic':
                return f"""
import statsmodels.api as sm
X = sm.add_constant(df[{x_names}])
model = sm.Logit(df['{y_name}'], X).fit()
print(model.summary())
# Odds ratios
print(np.exp(model.params))
"""
            elif model_type == 'poisson':
                return f"""
import statsmodels.api as sm
X = sm.add_constant(df[{x_names}])
model = sm.GLM(df['{y_name}'], X, family=sm.families.Poisson()).fit()
print(model.summary())
# IRR
print(np.exp(model.params))
"""
            elif model_type == 'negative_binomial':
                return f"""
import statsmodels.api as sm
X = sm.add_constant(df[{x_names}])
model = sm.GLM(df['{y_name}'], X, family=sm.families.NegativeBinomial()).fit()
print(model.summary())
# IRR
print(np.exp(model.params))
"""
        
        elif library == 'sklearn':
            if model_type == 'ols':
                return f"""
from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(df[{x_names}], df['{y_name}'])
print(f"R²: {{model.score(df[{x_names}], df['{y_name}'])}}")
print(f"Coefficients: {{dict(zip({x_names}, model.coef_))}}")
"""
            elif model_type == 'logistic':
                return f"""
from sklearn.linear_model import LogisticRegression
model = LogisticRegression()
model.fit(df[{x_names}], df['{y_name}'])
print(f"Accuracy: {{model.score(df[{x_names}], df['{y_name}'])}}")
"""
        
        return f"# Model syntax for {model_type} not implemented"


def main():
    """Test model selector"""
    selector = RegressionModelSelector()
    
    # Test with continuous data
    print("=" * 50)
    print("Test 1: Continuous DV")
    y_continuous = np.random.normal(100, 15, 200)
    result = selector.recommend_model(y_continuous)
    print(f"Recommended: {result['recommended_model']}")
    print(f"Rationale: {result['rationale']}")
    
    # Test with binary data
    print("\n" + "=" * 50)
    print("Test 2: Binary DV")
    y_binary = np.random.binomial(1, 0.3, 200)
    result = selector.recommend_model(y_binary)
    print(f"Recommended: {result['recommended_model']}")
    print(f"Rationale: {result['rationale']}")
    
    # Test with count data
    print("\n" + "=" * 50)
    print("Test 3: Count DV (Poisson)")
    y_count = np.random.poisson(5, 200)
    result = selector.recommend_model(y_count)
    print(f"Recommended: {result['recommended_model']}")
    print(f"Rationale: {result['rationale']}")


if __name__ == '__main__':
    main()
