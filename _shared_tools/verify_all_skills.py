#!/usr/bin/env python3
"""验证所有技能更新结果"""

import re
from pathlib import Path

SKILLS = [
    'grounded-theory-expert', 'digital-marx-expert', 'social-network-analysis-expert',
    'did-analysis-expert', 'qca-analysis-expert', 'business-ecosystem-expert',
    'digital-durkheim-expert', 'bourdieu-field-analysis-expert', 'digital-weber-expert',
    'survey-design-expert', 'data-analysis-expert', 'business-model-expert',
    'actor-network-analysis-expert',
]

def verify_skill(skill_path: Path) -> dict:
    skill_md = skill_path / 'SKILL.md'
    
    if not skill_md.exists():
        return {'status': 'NOT_FOUND', 'auto': False, 'python': False, 'mkdir': False}
    
    content = skill_md.read_text(encoding='utf-8')
    
    has_auto = '强制自动执行规则' in content or '🔴' in content
    has_python = 'os.makedirs' in content
    has_mkdir = bool(re.search(r'mkdir\s+-p(?!\s*#)', content))  # 排除注释
    
    if has_auto and has_python and not has_mkdir:
        return {'status': 'PASS', 'auto': True, 'python': True, 'mkdir': False}
    else:
        return {'status': 'FAIL', 'auto': has_auto, 'python': has_python, 'mkdir': has_mkdir}


def main():
    base_path = Path(r'D:\socienceAI\agentskills')
    
    print("=" * 60)
    print("最终验证结果")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for skill in SKILLS:
        result = verify_skill(base_path / skill)
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        print(f"{status_icon} {skill}: {result['status']}")
        
        if result['status'] != 'PASS':
            print(f"   自动执行规则: {result['auto']}, Python初始化: {result['python']}, mkdir -p: {result['mkdir']}")
            failed += 1
        else:
            passed += 1
    
    print("=" * 60)
    print(f"结果: {passed} 通过, {failed} 失败")
    print("=" * 60)


if __name__ == "__main__":
    main()
