#!/usr/bin/env python3
"""
Qwen Skill 部署和测试脚本
"""

import os
import json
import shutil
from datetime import datetime

def deploy():
    """部署 Qwen skill"""
    print("="*50)
    print("Qwen CLI 自动化系统部署")
    print("="*50)
    print()
    
    # Qwen 目录
    qwen_dir = os.path.expanduser("~/.qwen/skills/autonomous-execution")
    source_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 步骤 1: 创建目录
    print("[1/4] 创建 Qwen skill 目录...")
    os.makedirs(qwen_dir, exist_ok=True)
    print(f"✅ 目录：{qwen_dir}")
    print()
    
    # 步骤 2: 复制文件
    print("[2/4] 复制 skill 文件...")
    files_to_copy = [
        'qwen-skill.yaml',
        'qwen-auto-executor.py',
        'QWEN-AUTO-README.md'
    ]
    
    for file in files_to_copy:
        src = os.path.join(source_dir, file)
        dst = os.path.join(qwen_dir, file)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"✅ {file}")
        else:
            print(f"❌ {file} 不存在")
    print()
    
    # 步骤 3: 创建索引
    print("[3/4] 创建 skill 索引...")
    index = {
        "name": "autonomous-execution",
        "version": "1.0.0",
        "enabled": True,
        "triggers": ["启动自动化", "执行任务", "继续执行"],
        "description": "Qwen CLI 内自动化任务执行技能"
    }
    
    with open(os.path.join(qwen_dir, 'index.json'), 'w', encoding='utf-8') as f:
        json.dump(index, f, ensure_ascii=False, indent=2)
    print("✅ index.json")
    print()
    
    # 步骤 4: 验证
    print("[4/4] 验证安装...")
    checks = [
        ('qwen-skill.yaml', 'skill 配置'),
        ('qwen-auto-executor.py', '执行器'),
        ('index.json', '索引')
    ]
    
    all_ok = True
    for file, name in checks:
        path = os.path.join(qwen_dir, file)
        if os.path.exists(path):
            print(f"✅ {name}: {file}")
        else:
            print(f"❌ {name}: {file}")
            all_ok = False
    print()
    
    # 完成
    print("="*50)
    if all_ok:
        print("✅ 部署完成！")
        print()
        print("使用方法:")
        print("  1. 打开 Qwen CLI")
        print("  2. 输入：启动自动化任务执行")
        print("  3. 或运行：qwen \"启动自动化\"")
        print()
        print("可用命令:")
        print("  - 启动自动化")
        print("  - 执行任务")
        print("  - 继续执行")
        print("  - 查看状态")
        print("  - 停止")
    else:
        print("❌ 部署失败, 请检查错误")
    print("="*50)
    
    return all_ok


def test_executor():
    """测试执行器"""
    print()
    print("="*50)
    print("测试 Qwen 自动执行器")
    print("="*50)
    print()
    
    # 导入执行器
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # 使用 importlib 导入(处理连字符)
    import importlib.util
    spec = importlib.util.spec_from_file_location("qwen_auto_executor", "qwen-auto-executor.py")
    qwen_executor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(qwen_executor)
    
    QwenAutoExecutor = qwen_executor.QwenAutoExecutor
    
    executor = QwenAutoExecutor()
    
    # 测试启动
    print("[测试 1] 启动...")
    result = executor.start()
    print(result)
    print()
    
    # 测试执行
    print("[测试 2] 执行一轮...")
    result = executor.execute_turn()
    print(result)
    print()
    
    # 测试状态
    print("[测试 3] 状态...")
    result = executor.get_status()
    print(result)
    print()
    
    # 测试停止
    print("[测试 4] 停止...")
    result = executor.stop()
    print(result)
    print()
    
    print("="*50)
    print("✅ 测试完成！")
    print("="*50)


def test_dialogue_flow():
    """测试对话流程"""
    print()
    print("="*50)
    print("模拟对话流程测试")
    print("="*50)
    print()
    
    import sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    # 使用 importlib 导入
    import importlib.util
    spec = importlib.util.spec_from_file_location("qwen_auto_executor", "qwen-auto-executor.py")
    qwen_executor = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(qwen_executor)
    
    QwenAutoExecutor = qwen_executor.QwenAutoExecutor
    
    executor = QwenAutoExecutor()
    
    # 模拟对话
    dialogues = [
        ("启动自动化", executor.start),
        ("执行任务", executor.execute_turn),
        ("查看状态", executor.get_status),
        ("继续", executor.continue_execution),
        ("停止", executor.stop),
    ]
    
    for i, (user_input, handler) in enumerate(dialogues, 1):
        print(f"[对话{i}] 用户：{user_input}")
        result = handler()
        print(f"[对话{i}] Qwen: {result[:100]}...")
        print()
    
    print("="*50)
    print("✅ 对话流程测试完成！")
    print("="*50)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == 'deploy':
            deploy()
        elif cmd == 'test':
            test_executor()
        elif cmd == 'dialogue':
            test_dialogue_flow()
        else:
            print("用法：python deploy-and-test.py [deploy|test|dialogue]")
    else:
        # 默认执行部署 + 测试
        if deploy():
            test_executor()
            test_dialogue_flow()
