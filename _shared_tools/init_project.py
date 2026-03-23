#!/usr/bin/env python3
"""
技能项目初始化脚本 - 跨平台兼容
支持 Windows/Linux/macOS

使用方法:
    python init_project.py "D:\\project_path\\项目名"
    python init_project.py "/home/user/project"
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path


def init_project(project_path: str, skill_name: str = "default") -> dict:
    """
    初始化技能项目目录结构
    
    参数:
        project_path: 项目根目录路径
        skill_name: 技能名称
    
    返回:
        初始化结果字典
    """
    project_path = Path(project_path)
    
    # 定义标准目录结构
    directories = [
        '.tasks',           # 任务状态和进度
        '.tasks/completed', # 已完成任务
        'data',             # 原始数据
        'data/raw',         # 原始数据
        'data/processed',   # 处理后数据
        'results',          # 分析结果
        'results/reports',  # 报告
        'results/analysis', # 分析输出
        'visualizations',   # 可视化
        'logs',             # 日志
    ]
    
    created_dirs = []
    errors = []
    
    # 创建目录
    for subdir in directories:
        dir_path = project_path / subdir
        try:
            dir_path.mkdir(parents=True, exist_ok=True)
            created_dirs.append(str(dir_path))
        except Exception as e:
            errors.append(f"创建目录失败 {dir_path}: {str(e)}")
    
    # 创建任务队列文件
    task_queue_path = project_path / '.tasks' / 'task_queue.json'
    task_queue = {
        "skill": skill_name,
        "created": datetime.now().isoformat(),
        "status": "initialized",
        "tasks": [],
        "current_task": None,
        "completed_tasks": [],
        "auto_execute": True,  # 默认自动执行
        "version": "1.0.0"
    }
    
    try:
        with open(task_queue_path, 'w', encoding='utf-8') as f:
            json.dump(task_queue, f, ensure_ascii=False, indent=2)
    except Exception as e:
        errors.append(f"创建任务队列失败: {str(e)}")
    
    # 创建项目信息文件
    info_path = project_path / 'project_info.json'
    project_info = {
        "skill": skill_name,
        "created": datetime.now().isoformat(),
        "platform": sys.platform,
        "python_version": sys.version,
        "project_path": str(project_path),
        "status": "initialized"
    }
    
    try:
        with open(info_path, 'w', encoding='utf-8') as f:
            json.dump(project_info, f, ensure_ascii=False, indent=2)
    except Exception as e:
        errors.append(f"创建项目信息失败: {str(e)}")
    
    # 返回结果
    result = {
        "success": len(errors) == 0,
        "project_path": str(project_path),
        "created_directories": len(created_dirs),
        "directories": created_dirs,
        "errors": errors
    }
    
    return result


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("使用方法: python init_project.py <项目路径> [技能名称]")
        print("示例: python init_project.py D:\\analysis\\my_project grounded-theory")
        sys.exit(1)
    
    project_path = sys.argv[1]
    skill_name = sys.argv[2] if len(sys.argv) > 2 else "unknown-skill"
    
    print(f"正在初始化项目: {project_path}")
    print(f"技能名称: {skill_name}")
    print(f"平台: {sys.platform}")
    print("-" * 50)
    
    result = init_project(project_path, skill_name)
    
    if result["success"]:
        print(f"✅ 项目初始化成功!")
        print(f"   创建目录: {result['created_directories']} 个")
        print(f"   项目路径: {result['project_path']}")
    else:
        print(f"❌ 项目初始化失败:")
        for error in result["errors"]:
            print(f"   - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()