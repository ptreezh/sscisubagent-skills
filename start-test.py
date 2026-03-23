#!/usr/bin/env python3
"""
启动 Qwen CLI Skill 测试

自动打开 Qwen CLI 并加载测试指南
"""

import os
import subprocess
from pathlib import Path

def main():
    print("="*70)
    print("启动 Qwen CLI Skill 测试")
    print("="*70)
    print()
    
    # 显示测试指南
    guide_path = Path(r'D:\socienceAI\agentskills\EXECUTE-TEST-NOW.md')
    
    if guide_path.exists():
        print("📖 测试指南:")
        print()
        with open(guide_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # 只显示前 100 行
            lines = content.split('\n')[:100]
            print('\n.join(lines))
    
    print()
    print("="*70)
    print("请在 Qwen CLI 中执行以下步骤:")
    print("="*70)
    print()
    print("1. 启动 Qwen CLI:")
    print("   qwen")
    print()
    print("2. 输入测试问题:")
    print("   你是 grounded-theory-expert 吗？请介绍一下你的角色和能力. ")
    print()
    print("3. 提出复杂任务:")
    print("   我正在进行一项用户满意度研究, 收集了 20 份深度访谈记录...")
    print()
    print("4. 观察并记录结果")
    print()
    print("5. 填写测试记录:")
    print(f"   notepad {Path(rD:\\socienceAI\\agentskills\\test-records\\grounded-theory-expert-test-record.md')}")
    print()
    print("="*70)
    print("准备就绪！开始测试吧！")
    print("="*70)

if __name__ == '__main__':
    main()
