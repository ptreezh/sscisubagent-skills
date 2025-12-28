#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量更新作者和联系信息

统一所有智能体和技能文件中的作者信息为：
- 作者: socienceAI.com
- 联系邮箱: zhangshuren@freeagentskills.com
"""

import os
import re
from pathlib import Path
from datetime import datetime

# 目标信息
TARGET_AUTHOR = "socienceAI.com"
TARGET_EMAIL = "zhangshuren@freeagentskills.com"

# 需要处理的目录
DIRECTORIES_TO_PROCESS = [
    'agents',
    'skills'
]

# 文件扩展名
FILE_EXTENSIONS = ['.md', '.py']

# 需要排除的目录
EXCLUDE_DIRS = [
    'archive',
    'desktop_design',
    '__pycache__',
    'node_modules',
    '.git',
    'electron-src',
    'fixtures',
    'cache',
    'patches'
]


def should_process_file(file_path):
    """判断文件是否需要处理"""
    # 检查文件扩展名
    if file_path.suffix not in FILE_EXTENSIONS:
        return False

    # 检查是否在排除目录中
    for exclude_dir in EXCLUDE_DIRS:
        if exclude_dir in file_path.parts:
            return False

    # 排除特定文件
    exclude_files = [
        'update_author_info.py',
        'package.json',
        'package-lock.json',
        'yarn.lock'
    ]
    if file_path.name in exclude_files:
        return False

    return True


def update_file_content(file_path):
    """更新文件内容"""
    try:
        # 读取文件内容
        content = file_path.read_text(encoding='utf-8')

        original_content = content

        # 替换模式1: 作者: Claude Code / 作者: xxx
        content = re.sub(
            r'作者[:：]\s*[^\n]+',
            f'作者: {TARGET_AUTHOR}',
            content
        )

        # 替换模式2: Author: Claude Code / Author: xxx
        content = re.sub(
            r'Author[:：]\s*[^\n]+',
            f'Author: {TARGET_AUTHOR}',
            content
        )

        # 替换模式3: author: Claude Code / author: xxx
        content = re.sub(
            r'author[:：]\s*[^\n]+',
            f'author: {TARGET_AUTHOR}',
            content
        )

        # 替换模式4: 邮箱地址 (各种格式)
        # 匹配常见邮箱格式
        email_patterns = [
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
        ]

        for pattern in email_patterns:
            # 替换为统一邮箱，但保留TARGET_EMAIL本身
            def replace_email(match):
                email = match.group(0)
                if TARGET_EMAIL in email:
                    return email
                return TARGET_EMAIL

            content = re.sub(pattern, replace_email, content)

        # 替换模式5: 联系方式: xxx
        content = re.sub(
            r'联系方式[:：]\s*[^\n]+',
            f'联系方式: {TARGET_EMAIL}',
            content
        )

        # 替换模式6: Contact: xxx / contact: xxx
        content = re.sub(
            r'[Cc]ontact[:：]\s*[^\n]+',
            f'Contact: {TARGET_EMAIL}',
            content
        )

        # 替换模式7: Email: xxx / email: xxx
        content = re.sub(
            r'[Ee]mail[:：]\s*[^\n]+',
            f'Email: {TARGET_EMAIL}',
            content
        )

        # 如果内容有变化，写回文件
        if content != original_content:
            file_path.write_text(content, encoding='utf-8')
            return True

        return False

    except Exception as e:
        print(f"处理文件出错 {file_path}: {e}")
        return False


def main():
    """主函数"""
    print("=" * 70)
    print("批量更新作者和联系信息")
    print("=" * 70)
    print(f"目标作者: {TARGET_AUTHOR}")
    print(f"目标邮箱: {TARGET_EMAIL}")
    print()

    # 获取项目根目录
    root_dir = Path(__file__).parent

    # 统计信息
    total_files = 0
    updated_files = 0
    skipped_files = 0

    # 遍历目录
    for dir_name in DIRECTORIES_TO_PROCESS:
        dir_path = root_dir / dir_name

        if not dir_path.exists():
            print(f"跳过不存在的目录: {dir_path}")
            continue

        print(f"\n处理目录: {dir_path}")
        print("-" * 70)

        # 递归查找所有文件
        for file_path in dir_path.rglob('*'):
            # 只处理文件（跳过目录）
            if not file_path.is_file():
                continue

            # 判断是否需要处理
            if not should_process_file(file_path):
                skipped_files += 1
                continue

            # 处理文件
            total_files += 1
            if update_file_content(file_path):
                updated_files += 1
                print(f"  ✓ 已更新: {file_path.relative_to(root_dir)}")
            else:
                # 文件无需更新（可能已经正确或没有相关字段）
                pass

    # 打印统计信息
    print()
    print("=" * 70)
    print("更新完成")
    print("=" * 70)
    print(f"扫描文件总数: {total_files}")
    print(f"更新文件数量: {updated_files}")
    print(f"跳过文件数量: {skipped_files}")
    print()
    print(f"更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


if __name__ == "__main__":
    main()
