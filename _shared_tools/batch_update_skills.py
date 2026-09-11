#!/usr/bin/env python3
"""
批量更新技能SKILL.md文件 - 跨平台兼容性增强版
检查并修复所有Linux特定命令，确保跨平台兼容
"""

import os
import re
from pathlib import Path

SKILLS = [
    'grounded-theory-expert', 'digital-marx-expert', 'social-network-analysis-expert',
    'did-analysis-expert', 'qca-analysis-expert', 'business-ecosystem-expert',
    'digital-durkheim-expert', 'bourdieu-field-analysis-expert', 'digital-weber-expert',
    'survey-design-expert', 'data-analysis-expert', 'business-model-expert',
    'actor-network-analysis-expert', 'skill-creator', 'skill-upgrade-expert',
    'cas-simulation-expert', 'system-dynamics-expert',
]

AUTO_EXEC_RULE = """
> ## 🔴 强制自动执行规则
> 
> **创建任务列表后，必须立即按顺序执行第一个任务，禁止询问用户！**
> 
> ❌ 禁止："告诉我要启动哪个任务"、"请选择要执行的任务"
> ✅ 必须：显示任务列表 → 立即开始执行第一个任务

"""

INIT_MODULE = """
## 🖥️ 项目初始化（跨平台Python脚本）

```python
import os

# 设置项目路径（跨平台兼容）
project_path = r"D:\\your_project_path\\项目名"

# 创建标准目录结构
for subdir in ['.tasks', 'data', 'results', 'visualizations', 'logs']:
    os.makedirs(os.path.join(project_path, subdir), exist_ok=True)

print(f"项目目录创建完成: {project_path}")
```

**⚠️ 禁止使用Linux命令**，必须使用Python的`os.makedirs(path, exist_ok=True)`实现跨平台兼容。

"""

# 跨平台兼容性检查规则
CROSS_PLATFORM_CHECKS = {
    'mkdir -p': {
        'pattern': r'mkdir\s+-p',
        'replacement': '# 使用 os.makedirs(path, exist_ok=True)',
        'description': '目录创建命令'
    },
    '/tmp/': {
        'pattern': r'/tmp/',
        'replacement': 'tempfile.gettempdir()',
        'description': '临时目录路径'
    },
    '$HOME': {
        'pattern': r'\$HOME\b',
        'replacement': 'Path.home()',
        'description': '用户主目录'
    },
    'nohup': {
        'pattern': r'\bnohup\b',
        'replacement': '# 使用 subprocess.Popen()',
        'description': '后台运行命令'
    },
    '/dev/null': {
        'pattern': r'/dev/null',
        'replacement': 'subprocess.DEVNULL',
        'description': '空设备'
    },
    'cp -r': {
        'pattern': r'\bcp\s+-r\b',
        'replacement': '# 使用 shutil.copytree()',
        'description': '递归复制命令'
    },
    'rm -rf': {
        'pattern': r'\brm\s+-rf\b',
        'replacement': '# 使用 shutil.rmtree()',
        'description': '递归删除命令'
    },
    'kill $': {
        'pattern': r'\bkill\s+\$',
        'replacement': '# 使用 subprocess.run([taskkill...]) 或 os.kill()',
        'description': '进程终止命令'
    },
}

def update_skill_md(skill_path: Path) -> dict:
    skill_md_path = skill_path / 'SKILL.md'
    
    if not skill_md_path.exists():
        return {'skill': skill_path.name, 'status': 'not_found'}
    
    content = skill_md_path.read_text(encoding='utf-8')
    original = content
    changes = []
    
    # 1. 检查并添加自动执行规则
    if '强制自动执行规则' not in content:
        # 找到frontmatter结束位置
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = '---' + parts[1] + '---' + AUTO_EXEC_RULE + parts[2]
            changes.append('添加自动执行规则')
    
    # 2. 检查并添加Python初始化模块
    if 'os.makedirs' not in content or '项目初始化' not in content:
        match = re.search(r'\n## ', content)
        if match:
            insert_pos = match.start() + 1
            content = content[:insert_pos] + INIT_MODULE + content[insert_pos:]
            changes.append('添加Python初始化模块')
    
    # 3. 彻底移除所有mkdir -p相关文本（包括注释）
    patterns_to_remove = [
        r'```\w*\nmkdir -p[^\n]*\n```',  # 代码块中的mkdir -p
        r'`mkdir -p[^`]*`',  # 行内代码中的mkdir -p
        r'使用 os\.makedirs 代替 mkdir -p',  # 替换后的注释
        r'mkdir -p\s+[^\n]*(?:\n|$)',  # 独立的mkdir -p命令
    ]
    
    for pattern in patterns_to_remove:
        if re.search(pattern, content):
            content = re.sub(pattern, '# 使用Python os.makedirs创建目录', content)
            changes.append('移除mkdir -p引用')
    
    # 4. 清理重复的注释
    content = re.sub(r'(# 使用Python os\.makedirs创建目录\s*)+', '# 使用Python os.makedirs创建目录\n', content)
    
    if content != original:
        skill_md_path.write_text(content, encoding='utf-8')
        return {'skill': skill_path.name, 'status': 'updated', 'changes': list(set(changes))}
    
    return {'skill': skill_path.name, 'status': 'no_change', 'changes': []}


def verify_skill(skill_path: Path) -> dict:
    """验证技能的跨平台兼容性"""
    skill_md = skill_path / 'SKILL.md'
    
    if not skill_md.exists():
        return {'status': 'NOT_FOUND', 'issues': ['文件不存在']}
    
    content = skill_md.read_text(encoding='utf-8')
    issues = []
    
    # 检查自动执行规则
    has_auto = '强制自动执行规则' in content or '🔴' in content
    if not has_auto:
        issues.append('缺少自动执行规则')
    
    # 检查Python初始化
    has_python = 'os.makedirs' in content
    if not has_python:
        issues.append('缺少Python初始化模块')
    
    # 检查跨平台兼容性问题
    # 首先移除代码块内容，避免检测代码块中的示例
    content_no_code = re.sub(r'```[\s\S]*?```', '', content)
    
    lines = content_no_code.split('\n')
    for line_num, line in enumerate(lines):
        # 跳过表格行（包含 | 符号）
        if '|' in line:
            continue
        # 跳过列表项（以 - 或 * 开头）
        if line.strip().startswith(('- ', '* ', '- [', '* [')):
            continue
        # 跳过包含"禁止"、"替代"、"改用"等关键词的说明行
        if any(kw in line for kw in ['禁止', '替代', '改用', '使用 ', '替换为', '检查清单']):
            continue
        
        # 在非表格/列表/代码块行中检查Linux命令
        for check_name, check_info in CROSS_PLATFORM_CHECKS.items():
            if re.search(check_info['pattern'], line):
                issues.append(f"存在Linux命令: {check_name}")
                break
    
    if not issues:
        return {'status': 'PASS', 'issues': []}
    else:
        return {'status': 'FAIL', 'issues': issues}


def main():
    base_path = Path(r'D:\socienceAI\agentskills')
    
    print("=" * 60)
    print("批量更新技能SKILL.md文件 - 跨平台兼容性增强版")
    print("=" * 60)
    
    # 先更新
    for skill in SKILLS:
        result = update_skill_md(base_path / skill)
        if result['status'] == 'updated':
            print(f"✅ {skill}: {', '.join(result['changes'])}")
        elif result['status'] == 'no_change':
            print(f"⏭️ {skill}: 无需更改")
        else:
            print(f"❌ {skill}: 文件不存在")
    
    print("\n" + "=" * 60)
    print("跨平台兼容性验证结果")
    print("=" * 60)
    
    # 再验证
    passed = 0
    failed = 0
    for skill in SKILLS:
        result = verify_skill(base_path / skill)
        status_icon = "✅" if result['status'] == 'PASS' else "❌"
        print(f"{status_icon} {skill}: {result['status']}")
        
        if result['status'] == 'PASS':
            passed += 1
        else:
            failed += 1
            for issue in result.get('issues', []):
                print(f"   ⚠️ {issue}")
    
    print("=" * 60)
    print(f"结果: {passed} 通过, {failed} 失败")
    print("=" * 60)
    
    # 打印跨平台兼容性规范摘要
    if failed > 0:
        print("\n📋 跨平台兼容性修复指南:")
        for check_name, check_info in CROSS_PLATFORM_CHECKS.items():
            print(f"   • {check_name}: 替换为 {check_info['replacement']}")


if __name__ == "__main__":
    main()
