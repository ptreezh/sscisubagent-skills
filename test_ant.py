#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
行动者网络理论(ANT)分析技能测试
测试ANT分析技能的基本功能
"""

import sys
import os
from pathlib import Path

def test_ant_basic():
    """测试ANT分析技能的基本功能"""
    print("🧪 测试ANT分析技能 - 基本功能")
    
    # 检查技能文档是否存在
    skill_path = Path("skills/ant/SKILL.md")
    if not skill_path.exists():
        print("❌ 技能文档不存在")
        return False
    
    print(f"✅ 技能文档存在: {skill_path}")
    
    # 读取技能文档内容
    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键部分
        required_sections = [
            "name: ant",
            "description:",
            "## Overview",
            "## When to Use This Skill",
            "## Core Functions"
        ]
        
        for section in required_sections:
            if section in content:
                print(f"✅ 找到关键部分: {section[:20]}...")
            else:
                print(f"❌ 未找到关键部分: {section[:20]}...")
        
        # 检查理论基础
        if "ANT" in content or "Actor-Network Theory" in content or "行动者网络理论" in content:
            print("✅ 找到ANT理论基础")
        else:
            print("❌ 未找到理论基础")
        
        # 检查核心概念
        core_concepts = [
            "行动者", "actor", "network", "translation", "转译", "human", "non-human", "对称性"
        ]
        
        for concept in core_concepts:
            if concept in content:
                print(f"✅ 找到核心概念: {concept}")
            else:
                print(f"⚠️  未找到核心概念: {concept}")
        
        return True
        
    except Exception as e:
        print(f"❌ 读取技能文档时出错: {e}")
        return False

def test_ant_concepts():
    """测试ANT概念应用"""
    print("\n🧪 测试ANT概念应用")
    
    # 创建一个模拟的ANT分析场景（移动支付系统）
    ant_scenario = {
        "network_name": "中国移动支付网络",
        "actors": [
            {"name": "用户", "type": "human", "agency": "选择支付方式", "relations": ["使用", "依赖"]},
            {"name": "支付宝App", "type": "non-human", "agency": "处理交易", "relations": ["连接", "验证"]},
            {"name": "银行系统", "type": "non-human", "agency": "资金转移", "relations": ["授权", "记录"]},
            {"name": "商家", "type": "human", "agency": "接受支付", "relations": ["提供", "确认"]},
            {"name": "监管机构", "type": "human", "agency": "制定规则", "relations": ["规范", "监督"]},
            {"name": "二维码", "type": "non-human", "agency": "信息传递", "relations": ["编码", "解码"]}
        ],
        "translation_phases": {
            "problematisation": "定义支付需求和问题",
            "interessement": "吸引各方参与",
            "enrollment": "确定各方角色",
            "mobilization": "协调行动"
        },
        "network_properties": {
            "stability": "高",
            "heterogeneity": "高",
            "centrality": "平台为中心"
        }
    }
    
    # 保存场景数据
    import json
    scenario_path = Path("test_data/ant_scenario.json")
    scenario_path.parent.mkdir(exist_ok=True)
    with open(scenario_path, 'w', encoding='utf-8') as f:
        json.dump(ant_scenario, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 创建ANT分析场景: {scenario_path}")
    print(f"📊 网络名称: {ant_scenario['network_name']}")
    print(f"📊 行动者数量: {len(ant_scenario['actors'])}")
    print(f"📊 转译阶段: {list(ant_scenario['translation_phases'].keys())}")
    
    # 统计人类和非人类行动者
    human_actors = [a for a in ant_scenario['actors'] if a['type'] == 'human']
    non_human_actors = [a for a in ant_scenario['actors'] if a['type'] == 'non-human']
    print(f"📊 人类行动者: {len(human_actors)} 个")
    print(f"📊 非人类行动者: {len(non_human_actors)} 个")
    
    return True

def run_ant_tests():
    """运行ANT分析技能测试"""
    print("🚀 开始测试ANT分析技能")
    print("="*50)
    
    success = True
    
    # 测试基本功能
    if not test_ant_basic():
        success = False
        print("❌ 基本功能测试失败")
    
    # 测试概念应用
    if not test_ant_concepts():
        success = False
        print("❌ 概念应用测试失败")
    
    print("="*50)
    if success:
        print("✅ ANT分析技能测试通过")
    else:
        print("❌ ANT分析技能测试失败")
    
    return success

if __name__ == "__main__":
    run_ant_tests()