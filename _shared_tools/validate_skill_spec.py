#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
验证SKILL.md是否符合agentskills.io规范
"""

import re
from pathlib import Path

SKILLS_DIR = Path(__file__).parent.parent

SKILLS_TO_CHECK = [
    'grounded-theory-expert',
    'social-network-analysis-expert',
    'actor-network-analysis-expert',
    'bourdieu-field-analysis-expert',
    'digital-durkheim-expert',
    'digital-marx-expert',
    'digital-weber-expert',
    'cas-simulation-expert',
    'system-dynamics-expert',
    'did-analysis-expert',
    'qca-analysis-expert',
    'business-ecosystem-expert',
    'business-model-expert',
    'survey-design-expert',
    'data-analysis-expert',
    'skill-upgrade-expert',
]

def validate_frontmatter(content: str) -> dict:
    """验证YAML frontmatter格式"""
    issues = []
    
    # 检查是否以---开头
    if not content.startswith('---'):
        issues.append('文件必须以---开头')
        return {'valid': False, 'issues': issues}
    
    # 提取frontmatter
    match = re.match(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if not match:
        issues.append('未找到有效的frontmatter块')
        return {'valid': False, 'issues': issues}
    
    frontmatter = match.group(1)
    
    # 检查必需字段
    # name字段
    name_match = re.search(r'^name:\s*(.+)$', frontmatter, re.MULTILINE)
    if not name_match:
        issues.append('缺少必需的name字段')
    else:
        name = name_match.group(1).strip()
        # 验证name格式
        if not re.match(r'^[a-z0-9-]+$', name):
            issues.append(f'name格式错误: {name} (只能包含小写字母、数字和连字符)')
        if name.startswith('-') or name.endswith('-'):
            issues.append(f'name不能以连字符开头或结尾: {name}')
        if '--' in name:
            issues.append(f'name不能包含连续连字符: {name}')
    
    # description字段
    desc_match = re.search(r'^description:\s*\|?\s*(.+?)(?=^\w+:|$)', frontmatter, re.MULTILINE | re.DOTALL)
    if not desc_match:
        issues.append('缺少必需的description字段')
    else:
        desc = desc_match.group(1).strip()
        if len(desc) < 10:
            issues.append('description太短，应详细描述技能功能')
        if len(desc) > 1024:
            issues.append('description超过1024字符限制')
    
    # 检查是否有第二个frontmatter块（不允许）
    remaining = content[match.end():]
    if re.match(r'\s*---\s*\n.*?\n---', remaining, re.DOTALL):
        issues.append('发现多个frontmatter块，agentskills.io只允许一个')
    
    return {'valid': len(issues) == 0, 'issues': issues}

def main():
    print('=' * 60)
    print('agentskills.io 规范验证')
    print('=' * 60)
    
    results = {'valid': 0, 'invalid': 0, 'not_found': 0}
    
    for skill_name in SKILLS_TO_CHECK:
        skill_path = SKILLS_DIR / skill_name
        skill_md_path = skill_path / 'SKILL.md'
        
        if not skill_md_path.exists():
            print(f'❌ {skill_name}: SKILL.md不存在')
            results['not_found'] += 1
            continue
        
        content = skill_md_path.read_text(encoding='utf-8')
        result = validate_frontmatter(content)
        
        if result['valid']:
            print(f'✅ {skill_name}: 符合规范')
            results['valid'] += 1
        else:
            print(f'❌ {skill_name}: 不符合规范')
            for issue in result['issues']:
                print(f'   - {issue}')
            results['invalid'] += 1
    
    print('=' * 60)
    print(f'验证结果: 符合规范 {results["valid"]}, 不符合 {results["invalid"]}, 未找到 {results["not_found"]}')
    
    return results

if __name__ == '__main__':
    main()
