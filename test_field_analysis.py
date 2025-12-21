#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
场域分析技能测试
测试场域分析技能的基本功能
"""

import sys
import os
from pathlib import Path

def test_field_analysis_basic():
    """测试场域分析技能的基本功能"""
    print("🧪 测试场域分析技能 - 基本功能")
    
    # 检查技能文档是否存在
    skill_path = Path("skills/field-analysis/SKILL.md")
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
            "name: field-analysis",
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
        if "布迪厄" in content or "Bourdieu" in content:
            print("✅ 找到场域理论基础")
        else:
            print("❌ 未找到理论基础")
        
        # 检查核心概念
        core_concepts = [
            "场域边界", "资本分布", "自主性", "习性", "position", "capital", "habitus"
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

def test_field_analysis_concepts():
    """测试场域分析概念应用"""
    print("\n🧪 测试场域分析概念应用")
    
    # 创建一个模拟的场域分析场景
    field_scenario = {
        "field_name": "中国高等教育场域",
        "actors": [
            {"name": "清华大学", "type": "教育机构", "capital": {"学术": 95, "经济": 85, "文化": 90, "象征": 98}},
            {"name": "北京大学", "type": "教育机构", "capital": {"学术": 93, "经济": 80, "文化": 88, "象征": 96}},
            {"name": "普通高校A", "type": "教育机构", "capital": {"学术": 60, "经济": 50, "文化": 55, "象征": 45}},
            {"name": "教育部", "type": "政府机构", "capital": {"政治": 90, "经济": 85, "象征": 88}},
            {"name": "学生群体", "type": "社会群体", "capital": {"文化": 40, "经济": 20, "象征": 30}}
        ],
        "relationships": [
            {"from": "清华大学", "to": "教育部", "type": "依赖"},
            {"from": "北京大学", "to": "教育部", "type": "依赖"},
            {"from": "普通高校A", "to": "教育部", "type": "依赖"},
            {"from": "清华大学", "to": "北京大学", "type": "竞争"},
            {"from": "学生群体", "to": "高校", "type": "选择"}
        ],
        "field_rules": [
            "学术声誉是主要资本形式",
            "政府资助影响场域自主性",
            "国际化程度影响地位"
        ]
    }
    
    # 保存场景数据
    import json
    scenario_path = Path("test_data/field_analysis_scenario.json")
    scenario_path.parent.mkdir(exist_ok=True)
    with open(scenario_path, 'w', encoding='utf-8') as f:
        json.dump(field_scenario, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 创建场域分析场景: {scenario_path}")
    print(f"📊 场域名称: {field_scenario['field_name']}")
    print(f"📊 参与者数量: {len(field_scenario['actors'])}")
    print(f"📊 关系数量: {len(field_scenario['relationships'])}")
    
    return True

def run_field_analysis_tests():
    """运行场域分析技能测试"""
    print("🚀 开始测试场域分析技能")
    print("="*50)
    
    success = True
    
    # 测试基本功能
    if not test_field_analysis_basic():
        success = False
        print("❌ 基本功能测试失败")
    
    # 测试概念应用
    if not test_field_analysis_concepts():
        success = False
        print("❌ 概念应用测试失败")
    
    print("="*50)
    if success:
        print("✅ 场域分析技能测试通过")
    else:
        print("❌ 场域分析技能测试失败")
    
    return success

if __name__ == "__main__":
    run_field_analysis_tests()