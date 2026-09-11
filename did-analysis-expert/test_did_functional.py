#!/usr/bin/env python3
"""
DID Analysis Expert - Quick Functional Test Script
Run this script to verify all DID analysis functionality
"""

import sys
sys.path.insert(0, 'tools')

from treatment_effect_calculator import calculate_treatment_effect
from data_validator import validate_did_data
from parallel_trends_checker import check_parallel_trends

def test_data_validation():
    """Test 1: Data Validation"""
    print("=" * 60)
    print("TEST 1: Data Validation")
    print("=" * 60)

    test_data = [
        {'group': 'treatment', 'time': 0, 'y': 100},
        {'group': 'treatment', 'time': 1, 'y': 150},
        {'group': 'treatment', 'time': 0, 'y': 105},
        {'group': 'treatment', 'time': 1, 'y': 145},
        {'group': 'control', 'time': 0, 'y': 95},
        {'group': 'control', 'time': 1, 'y': 100},
        {'group': 'control', 'time': 0, 'y': 98},
        {'group': 'control', 'time': 1, 'y': 102},
    ]

    result = validate_did_data(test_data)
    print(f"Validation Status: {result['summary']}")
    print(f"Observations: {result.get('num_observations', 0)}")
    print(f"Valid: {result['valid']}\n")
    return result['valid']

def test_parallel_trends():
    """Test 2: Parallel Trends Check"""
    print("=" * 60)
    print("TEST 2: Parallel Trends Check")
    print("=" * 60)

    trend_data = [
        {'group': 'treatment', 'time': -2, 'y': 90},
        {'group': 'treatment', 'time': -1, 'y': 95},
        {'group': 'treatment', 'time': 0, 'y': 100},
        {'group': 'treatment', 'time': 1, 'y': 150},
        {'group': 'control', 'time': -2, 'y': 85},
        {'group': 'control', 'time': -1, 'y': 90},
        {'group': 'control', 'time': 0, 'y': 95},
        {'group': 'control', 'time': 1, 'y': 100},
    ]

    result = check_parallel_trends(trend_data)
    print(f"Treatment Slope: {result['treatment_slope']:.4f}")
    print(f"Control Slope: {result['control_slope']:.4f}")
    print(f"Slope Difference: {result['slope_difference']:.4f}")
    print(f"Parallel Trends: {result['verdict']}")
    print(f"Explanation: {result['explanation']}\n")
    return True

def test_treatment_effect():
    """Test 3: Treatment Effect Calculation"""
    print("=" * 60)
    print("TEST 3: Treatment Effect Calculation")
    print("=" * 60)

    test_data = [
        {'group': 'treatment', 'time': 0, 'y': 100},
        {'group': 'treatment', 'time': 1, 'y': 150},
        {'group': 'treatment', 'time': 0, 'y': 105},
        {'group': 'treatment', 'time': 1, 'y': 145},
        {'group': 'control', 'time': 0, 'y': 95},
        {'group': 'control', 'time': 1, 'y': 100},
        {'group': 'control', 'time': 0, 'y': 98},
        {'group': 'control', 'time': 1, 'y': 102},
    ]

    result = calculate_treatment_effect(test_data)
    print(f"Treatment Group (Before): {result['treatment_before']:.2f}")
    print(f"Treatment Group (After): {result['treatment_after']:.2f}")
    print(f"Control Group (Before): {result['control_before']:.2f}")
    print(f"Control Group (After): {result['control_after']:.2f}")
    print(f"Treatment Effect: {result['treatment_effect']:.2f}")
    print(f"Control Effect: {result['control_effect']:.2f}")
    print(f"DID Estimate: {result['did_estimate']:.2f}")
    print(f"Interpretation: {result['interpretation']}\n")
    return result['did_estimate']

def test_calculation_verification():
    """Test 4: Verify DID Calculation"""
    print("=" * 60)
    print("TEST 4: Calculation Verification")
    print("=" * 60)

    # Manual calculation
    manual_t_before = (100 + 105) / 2
    manual_t_after = (150 + 145) / 2
    manual_c_before = (95 + 98) / 2
    manual_c_after = (100 + 102) / 2
    manual_did = (manual_t_after - manual_t_before) - (manual_c_after - manual_c_before)

    test_data = [
        {'group': 'treatment', 'time': 0, 'y': 100},
        {'group': 'treatment', 'time': 1, 'y': 150},
        {'group': 'treatment', 'time': 0, 'y': 105},
        {'group': 'treatment', 'time': 1, 'y': 145},
        {'group': 'control', 'time': 0, 'y': 95},
        {'group': 'control', 'time': 1, 'y': 100},
        {'group': 'control', 'time': 0, 'y': 98},
        {'group': 'control', 'time': 1, 'y': 102},
    ]

    result = calculate_treatment_effect(test_data)
    tool_did = result['did_estimate']

    print(f"Manual DID Calculation: {manual_did:.2f}")
    print(f"Tool DID Calculation: {tool_did:.2f}")
    print(f"Match: {abs(manual_did - tool_did) < 0.01}\n")
    return abs(manual_did - tool_did) < 0.01

def test_dictionary_format():
    """Test 5: Dictionary Input Format"""
    print("=" * 60)
    print("TEST 5: Dictionary Input Format")
    print("=" * 60)

    dict_data = {
        'treatment_before': 100,
        'treatment_after': 150,
        'control_before': 95,
        'control_after': 100,
    }

    result = calculate_treatment_effect(dict_data)
    print(f"DID from Dict: {result['did_estimate']:.2f}")
    print(f"Interpretation: {result['interpretation']}\n")
    return result['did_estimate'] == 45.0

def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("DID ANALYSIS EXPERT - FUNCTIONAL TEST SUITE")
    print("=" * 60 + "\n")

    results = []

    # Run all tests
    results.append(("Data Validation", test_data_validation()))
    results.append(("Parallel Trends", test_parallel_trends()))
    results.append(("Treatment Effect", test_treatment_effect()))
    results.append(("Calculation Verification", test_calculation_verification()))
    results.append(("Dictionary Format", test_dictionary_format()))

    # Summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")

    all_passed = all(result for _, result in results)
    print("\n" + "=" * 60)
    if all_passed:
        print("ALL TESTS PASSED ✅")
    else:
        print("SOME TESTS FAILED ❌")
    print("=" * 60 + "\n")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
