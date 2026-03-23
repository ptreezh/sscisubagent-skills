#!/usr/bin/env python3
"""
部署 Skill 和扩展到 Qwen CLI
用于真实环境测试
"""

import os
import shutil
from pathlib import Path

def deploy():
    print("="*70)
    print("部署 Skill 和扩展到 Qwen CLI")
    print("="*70)
    print()
    
    # 设置路径
    qwenn_home = Path.home() / '.qwen'
    skills_source = Path(r'D:\socienceAI\agentskills')
    
    # 步骤 1: 创建目录
    print("[1/4] 创建目录结构...")
    (qwenn_home / 'skills').mkdir(exist_ok=True)
    (qwenn_home / 'extensions').mkdir(exist_ok=True)
    print("  [OK] 目录创建完成")
    print()
    
    # 步骤 2: 部署扩展
    print("[2/4] 部署扩展...")
    extensions = ['skill-evolution', 'skill-task-integration']
    
    for ext in extensions:
        src = skills_source / 'extensions' / ext
        dst = qwenn_home / 'extensions' / ext
        
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"  [OK] {ext}")
        else:
            print(f"  [ERROR] {ext} 不存在")
    
    print()
    
    # 步骤 3: 部署 skill
    print("[3/4] 部署 skill...")
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
    
    deployed = 0
    for skill in skills:
        src = skills_source / skill
        dst = qwenn_home / 'skills' / skill
        
        if src.exists():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"  [OK] {skill}")
            deployed += 1
        else:
            print(f"  [ERROR] {skill} 不存在")
    
    print()
    
    # 步骤 4: 配置 Qwen CLI
    print("[4/4] 配置 Qwen CLI...")
    config_path = qwenn_home / 'config.yaml'
    
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        if 'skill-evolution' not in content:
            with open(config_path, 'a', encoding='utf-8') as f:
                f.write("\nextensions:\n  enabled:\n    - skill-evolution\n    - skill-task-integration\n")
            print("  [OK] 已添加扩展配置")
        else:
            print("  [OK] 扩展配置已存在")
    else:
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write("extensions:\n  enabled:\n    - skill-evolution\n    - skill-task-integration\n")
        print("  [OK] 已创建配置文件")
    
    print()
    print("="*70)
    print("部署完成！")
    print("="*70)
    print()
    print("部署统计:")
    print(f"  - 扩展：{len(extensions)} 个")
    print(f"  - skill: {deployed} 个")
    print()
    print("下一步:")
    print("  1. 重启 Qwen CLI(如果需要)")
    print("  2. 启动测试：qwen")
    print("  3. 开始测试 grounded-theory-expert")
    print()

if __name__ == '__main__':
    deploy()
