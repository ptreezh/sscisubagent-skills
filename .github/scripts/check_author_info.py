#!/usr/bin/env python3
"""
检查作者信息一致性
作者: socienceAI.com
联系: zhangshuren@freeagentskills.com
"""

import os
import re
from pathlib import Path

TARGET_AUTHOR = "socienceAI.com"
TARGET_EMAIL = "zhangshuren@freeagentskills.com"

def check_file_author_info(file_path):
    """检查文件中的作者信息"""
    errors = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查作者信息
        author_patterns = [
            r'作者[:：]\s*([^\n]+)',
            r'Author[:：]\s*([^\n]+)',
            r'author[:：]\s*([^\n]+)',
        ]

        for pattern in author_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if TARGET_AUTHOR not in match and 'Claude' not in match and 'Anthropic' not in match:
                    errors.append(f"作者信息不匹配: {match.strip()}")

        # 检查邮箱信息
        email_patterns = [
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        ]

        for pattern in email_patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                if TARGET_EMAIL not in match and 'anthropic.com' not in match:
                    errors.append(f"邮箱信息不匹配: {match}")

    except Exception as e:
        errors.append(f"读取文件错误: {str(e)}")

    return errors

def main():
    """主函数"""
    print("检查作者信息一致性...")

    project_root = Path('.')

    # 检查的目录
    check_dirs = ['agents', 'skills']

    total_errors = 0
    total_files = 0

    for check_dir in check_dirs:
        dir_path = project_root / check_dir

        if not dir_path.exists():
            continue

        # 查找所有.md和.py文件
        for file_path in dir_path.rglob('*.md'):
            if 'archive' in str(file_path) or 'project_backup' in str(file_path):
                continue

            errors = check_file_author_info(file_path)

            if errors:
                print(f"\n{file_path.relative_to(project_root)}:")
                for error in errors:
                    print(f"  ❌ {error}")
                    total_errors += 1

            total_files += 1

        for file_path in dir_path.rglob('*.py'):
            if 'archive' in str(file_path) or 'project_backup' in str(file_path):
                continue
            if 'node_modules' in str(file_path) or '__pycache__' in str(file_path):
                continue

            errors = check_file_author_info(file_path)

            if errors:
                print(f"\n{file_path.relative_to(project_root)}:")
                for error in errors:
                    print(f"  ❌ {error}")
                    total_errors += 1

            total_files += 1

    print(f"\n检查完成:")
    print(f"  扫描文件: {total_files}")
    print(f"  错误: {total_errors}")

    if total_errors > 0:
        print("\n❌ 作者信息检查失败")
        print(f"请确保所有文件的作者信息为: {TARGET_AUTHOR}")
        print(f"联系信息为: {TARGET_EMAIL}")
        return 1
    else:
        print("✅ 所有文件作者信息一致")
        return 0

if __name__ == '__main__':
    exit(main())
