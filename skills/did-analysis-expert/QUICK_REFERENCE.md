# DID Analysis Expert - Quick Reference Card

## What is This?

A **Difference-in-Differences (DiD)** causal inference analysis tool for evaluating treatment effects in observational studies.

---

## Quick Start

```python
import sys
sys.path.insert(0, 'tools')
from treatment_effect_calculator import calculate_treatment_effect

# Your data (list format)
data = [
    {'group': 'treatment', 'time': 0, 'y': 100},  # Before
    {'group': 'treatment', 'time': 1, 'y': 150},  # After
    {'group': 'control', 'time': 0, 'y': 95},
    {'group': 'control', 'time': 1, 'y': 100},
]

# Calculate DID
result = calculate_treatment_effect(data)
print(f"DID Effect: {result['did_estimate']:.2f}")
```

---

## Input Format

### Option 1: Individual Observations (List)
```python
data = [
    {'group': 'treatment', 'time': 0, 'y': 100},
    {'group': 'treatment', 'time': 1, 'y': 150},
    {'group': 'control', 'time': 0, 'y': 95},
    {'group': 'control', 'time': 1, 'y': 100},
]
```

**Required Fields**:
- `group`: "treatment" or "control"
- `time`: 0 (before) or 1 (after)
- `y`: outcome variable

### Option 2: Aggregated Data (Dictionary)
```python
data = {
    'treatment_before': 100,
    'treatment_after': 150,
    'control_before': 95,
    'control_after': 100,
}
```

---

## Output Interpretation

```python
{
    'treatment_before': 102.50,     # Treatment group mean (before)
    'treatment_after': 147.50,      # Treatment group mean (after)
    'control_before': 96.50,        # Control group mean (before)
    'control_after': 101.00,        # Control group mean (after)
    'treatment_effect': 45.00,      # Treatment group change
    'control_effect': 4.50,         # Control group change
    'did_estimate': 40.50,          # ⭐ DID effect
    'interpretation': '处理效应为40.50',
    'significant': True
}
```

---

## The DID Formula

```
DID = (Y_treatment_after - Y_treatment_before)
    - (Y_control_after - Y_control_before)

Example:
  Treatment: 100 → 150 (change = +50)
  Control:    95  → 100  (change = +5)
  DID = 50 - 5 = 45
```

---

## Available Tools

### 1. Treatment Effect Calculator
```python
from treatment_effect_calculator import calculate_treatment_effect
result = calculate_treatment_effect(data)
```

### 2. Data Validator
```python
from data_validator import validate_did_data
validation = validate_did_data(data)
# Returns: {'valid': True, 'summary': '验证通过', 'num_observations': 8}
```

### 3. Parallel Trends Checker
```python
from parallel_trends_checker import check_parallel_trends
trends = check_parallel_trends(data)
# Returns: {'parallel': True, 'verdict': '通过', 'treatment_slope': 5.0}
```

---

## When to Use DID

✅ **Good for**:
- Policy evaluation (before/after legislation)
- Natural experiments
- Quasi-experimental designs
- When you can't randomize

❌ **Not for**:
- Cross-sectional data (single time point)
- When parallel trends assumption violated
- With major spillover effects

---

## Critical Assumption

**Parallel Trends**: Treatment and control groups would have evolved similarly without treatment.

**How to Check**:
```python
from parallel_trends_checker import check_parallel_trends
result = check_parallel_trends(pre_treatment_data)
if result['parallel']:
    print("✅ Safe to use DID")
else:
    print("⚠️ Parallel trends violated - consider alternatives")
```

---

## Example Use Cases

### 1. Policy Evaluation
**Question**: Did a new law reduce unemployment?

```python
# States that adopted the law (treatment) vs didn't (control)
# Unemployment rates before and after law implementation
data = [
    {'group': 'treatment', 'time': 0, 'y': 8.5},  # Before law
    {'group': 'treatment', 'time': 1, 'y': 7.2},  # After law
    {'group': 'control', 'time': 0, 'y': 8.3},
    {'group': 'control', 'time': 1, 'y': 8.1},
]
result = calculate_treatment_effect(data)
# DID = (7.2 - 8.5) - (8.1 - 8.3) = -1.3 + 0.2 = -1.1
# Interpretation: Law reduced unemployment by 1.1 percentage points
```

### 2. Program Evaluation
**Question**: Did a training program increase wages?

```python
# Participants (treatment) vs non-participants (control)
# Wages before and after program
data = [
    {'group': 'treatment', 'time': 0, 'y': 2500},
    {'group': 'treatment', 'time': 1, 'y': 3200},
    {'group': 'control', 'time': 0, 'y': 2600},
    {'group': 'control', 'time': 1, 'y': 2700},
]
result = calculate_treatment_effect(data)
# DID = (3200 - 2500) - (2700 - 2600) = 700 - 100 = 600
# Interpretation: Program increased wages by $600/month
```

---

## Testing

Run the test suite:
```bash
cd D:/socienceAI/agentskills/did-analysis-expert
python test_did_functional.py
```

Expected output: ✅ ALL TESTS PASSED

---

## Common Issues & Solutions

### Issue 1: "Data validation failed"
**Cause**: Missing required fields or wrong format
**Solution**: Check that each row has `group`, `time`, and `y` fields

### Issue 2: "Parallel trends not satisfied"
**Cause**: Treatment and control groups had different trends before intervention
**Solution**:
- Collect more pre-treatment data
- Consider matching methods
- Use synthetic control approach

### Issue 3: "Unexpected DID value"
**Cause**: Data format confusion (time encoding)
**Solution**: Ensure time=0 for before, time=1 for after

---

## Advanced Usage

### Check Parallel Trends First
```python
# Step 1: Validate data
validation = validate_did_data(data)
assert validation['valid'], "Invalid data"

# Step 2: Check parallel trends (use pre-treatment data)
trends = check_parallel_trends(pre_treatment_data)
assert trends['parallel'], "Parallel trends violated"

# Step 3: Calculate DID
result = calculate_treatment_effect(data)
print(f"Causal effect: {result['did_estimate']:.2f}")
```

---

## Resources

- **Documentation**: `SKILL.md`
- **Test Report**: `DID_functional_test.md`
- **Test Script**: `test_did_functional.py`
- **Methodology**: Based on Angrist & Pischke (2009)

---

## Key References

- Angrist, J. D., & Pischke, J. S. (2009). *Mostly Harmless Econometrics*
- Card, D., & Krueger, A. B. (1994). "Minimum Wages and Employment"
- Bertrand, M., Duflo, E., & Mullainathan, S. (2004). "How Much Should We Trust Differences-in-Differences?"

---

**Version**: 5.0.0-cli-native+agent
**Last Updated**: 2026-03-12
**Status**: ✅ Fully Functional
