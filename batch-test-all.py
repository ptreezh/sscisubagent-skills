#!/usr/bin/env python3
"""
批量测试所有 13 个 skill
"""

import sys
import importlib.util

# 加载 auto_test_runner 模块
spec = importlib.util.spec_from_file_location("auto_test_runner", "auto-test-runner.py")
auto_test_runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(auto_test_runner)

AutomatedSkillTester = auto_test_runner.AutomatedSkillTester

skills = [
    'grounded-theory-expert',
    'social-network-analysis-expert',
    'bourdieu-field-analysis-expert',
    'msqca-analysis-expert',
    'did-analysis-expert',
    'data-analysis-expert',
    'business-ecosystem-analysis-expert',
    'business-model-analysis-expert',
    'actor-network-analysis-expert',
    'digital-marx-expert',
    'digital-durkheim-expert',
    'digital-weber-expert',
    'survey-design-expert'
]

print("="*70)
print("批量测试所有 13 个 skill")
print("="*70)
print()

results = []

for i, skill in enumerate(skills, 1):
    print(f"\n{'='*70}")
    print(f"[{i}/{len(skills)}] 测试：{skill}")
    print(f"{'='*70}\n")
    
    try:
        tester = AutomatedSkillTester(skill)
        tester.run_full_test()
        results.append({
            'skill': skill,
            'status': '✅ 通过',
            'score': tester.score['total']
        })
    except Exception as e:
        print(f"❌ 测试失败：{e}")
        results.append({
            'skill': skill,
            'status': '❌ 失败',
            'error': str(e)
        })
    
    print(f"\n完成：{skill}")

# 生成汇总报告
print("\n" + "="*70)
print("测试汇总报告")
print("="*70)
print()

print("| # | Skill 名称 | 状态 | 得分 |")
print("|---|------------|------|------|")

for i, result in enumerate(results, 1):
    status = result['status']
    score = result.get('score', 'N/A')
    print(f"| {i} | {result['skill']} | {status} | {score} |")

print()
print("="*70)
print("批量测试完成！")
print("="*70)
