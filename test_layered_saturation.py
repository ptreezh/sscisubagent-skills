#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试理论饱和度检验技能的真实数据
"""

import sys
import json
from pathlib import Path

# Add skills path
sys.path.insert(0, str(Path(__file__).parent / "skills" / "coding" / "theory-saturation" / "scripts"))

try:
    from assess_saturation import TheorySaturationAssessor

    # Test with real saturation data
    assessor = TheorySaturationAssessor()

    print("Testing theory saturation assessment...")
    # Load data from directory
    data_dir = 'test_data/real/theory_saturation'
    results = assessor.generate_saturation_report(data_dir)

    print('Theory Saturation Assessment Results:')
    print(f'Available keys: {list(results.keys())}')

    # Print whatever results are available
    for key, value in results.items():
        if isinstance(value, dict) and 'status' in value:
            print(f'{key}: Status = {value["status"]}')
        elif isinstance(value, dict) and 'score' in value:
            print(f'{key}: Score = {value["score"]:.3f}')
        elif isinstance(value, (int, float)):
            print(f'{key}: {value:.3f}')
        elif isinstance(value, str):
            print(f'{key}: {value}')

    print("\n✅ Theory saturation assessment with real data successful!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)