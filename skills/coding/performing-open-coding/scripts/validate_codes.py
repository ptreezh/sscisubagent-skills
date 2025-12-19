#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
编码验证脚本 - 开放编码

功能：
- 检查命名规范
- 检查定义质量
- 检查示例充分性
- 生成质量报告

使用方式：
  python validate_codes.py --input codes.json --output validation.json
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict
import re

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def check_naming_convention(codes: List[Dict]) -> List[str]:
    """
    检查命名规范
    
    规范：
    - 使用动词开头（行动导向）
    - 长度适中（2-8个字符）
    - 避免过于抽象或具体
    
    Returns:
        问题列表
    """
    issues = []
    
    # 常见行动动词
    action_verbs = ['寻求', '建立', '适应', '应对', '处理', '解决', '获得', '提供',
                   '学习', '制定', '执行', '调整', '保持', '克服', '管理', '理解']
    
    for i, code in enumerate(codes):
        concept = code.get('concept') or code.get('code', '')
        
        if not concept:
            issues.append(f"编码{i+1}: 概念名称为空")
            continue
        
        # 检查长度
        if len(concept) < 2:
            issues.append(f"编码{i+1} '{concept}': 名称过短（少于2字符）")
        elif len(concept) > 10:
            issues.append(f"编码{i+1} '{concept}': 名称过长（超过10字符），建议简化")
        
        # 检查是否包含行动动词
        has_action_verb = any(verb in concept for verb in action_verbs)
        if not has_action_verb:
            issues.append(f"编码{i+1} '{concept}': 建议使用行动导向的命名（如：寻求帮助）")
        
        # 检查是否过于具体
        if any(char.isdigit() for char in concept):
            issues.append(f"编码{i+1} '{concept}': 包含数字，可能过于具体")
    
    return issues

def check_definition_quality(codes: List[Dict]) -> List[str]:
    """
    检查定义质量
    
    规范：
    - 定义应该清晰完整
    - 长度适中（10-100字符）
    - 包含关键要素
    
    Returns:
        问题列表
    """
    issues = []
    
    for i, code in enumerate(codes):
        concept = code.get('concept') or code.get('code', '')
        definition = code.get('definition', '')
        
        if not definition:
            issues.append(f"编码{i+1} '{concept}': 缺少定义")
            continue
        
        # 检查长度
        if len(definition) < 10:
            issues.append(f"编码{i+1} '{concept}': 定义过短（少于10字符）")
        elif len(definition) > 200:
            issues.append(f"编码{i+1} '{concept}': 定义过长（超过200字符），建议简化")
        
        # 检查是否包含关键词
        if concept not in definition and not any(word in definition for word in concept.split()):
            issues.append(f"编码{i+1} '{concept}': 定义中未包含概念名称或相关词汇")
    
    return issues

def check_example_sufficiency(codes: List[Dict]) -> List[str]:
    """
    检查示例充分性
    
    规范：
    - 至少1个示例
    - 示例应该具体
    - 示例长度适中
    
    Returns:
        问题列表
    """
    issues = []
    
    for i, code in enumerate(codes):
        concept = code.get('concept') or code.get('code', '')
        examples = code.get('examples', [])
        
        if not examples or len(examples) == 0:
            issues.append(f"编码{i+1} '{concept}': 缺少示例")
            continue
        
        # 检查示例数量
        if len(examples) < 2:
            issues.append(f"编码{i+1} '{concept}': 示例数量不足（建议至少2个）")
        
        # 检查示例质量
        for j, example in enumerate(examples):
            if len(example) < 5:
                issues.append(f"编码{i+1} '{concept}': 示例{j+1}过短（少于5字符）")
            elif len(example) > 200:
                issues.append(f"编码{i+1} '{concept}': 示例{j+1}过长（超过200字符）")
    
    return issues

def calculate_quality_score(codes: List[Dict], all_issues: Dict[str, List[str]]) -> Dict:
    """
    计算质量评分
    
    Returns:
        评分结果
    """
    total_codes = len(codes)
    
    # 统计各类问题数量
    naming_issues = len(all_issues['naming'])
    definition_issues = len(all_issues['definition'])
    example_issues = len(all_issues['example'])
    total_issues = naming_issues + definition_issues + example_issues
    
    # 计算评分（100分制）
    # 命名：40分，定义：30分，示例：30分
    naming_score = max(0, 40 - (naming_issues / total_codes) * 40)
    definition_score = max(0, 30 - (definition_issues / total_codes) * 30)
    example_score = max(0, 30 - (example_issues / total_codes) * 30)
    
    total_score = naming_score + definition_score + example_score
    
    # 评级
    if total_score >= 90:
        grade = 'A (优秀)'
    elif total_score >= 80:
        grade = 'B (良好)'
    elif total_score >= 70:
        grade = 'C (中等)'
    elif total_score >= 60:
        grade = 'D (及格)'
    else:
        grade = 'F (不及格)'
    
    return {
        'total_score': round(total_score, 1),
        'naming_score': round(naming_score, 1),
        'definition_score': round(definition_score, 1),
        'example_score': round(example_score, 1),
        'grade': grade,
        'total_issues': total_issues,
        'issue_breakdown': {
            'naming': naming_issues,
            'definition': definition_issues,
            'example': example_issues
        }
    }

def generate_recommendations(all_issues: Dict[str, List[str]]) -> List[str]:
    """
    生成改进建议
    
    Returns:
        建议列表
    """
    recommendations = []
    
    if all_issues['naming']:
        recommendations.append("命名规范：使用行动导向的动词开头，如'寻求帮助'、'建立关系'")
    
    if all_issues['definition']:
        recommendations.append("定义质量：确保每个概念都有清晰完整的定义（10-100字符）")
    
    if all_issues['example']:
        recommendations.append("示例充分性：为每个概念提供至少2个具体示例")
    
    if not any(all_issues.values()):
        recommendations.append("编码质量优秀，继续保持！")
    
    return recommendations

def main():
    parser = argparse.ArgumentParser(
        description='编码验证工具 - 开放编码',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例用法:
  python validate_codes.py --input codes.json --output validation.json
  python validate_codes.py -i codes.json -o report.json
        """
    )
    parser.add_argument('--input', '-i', required=True, help='输入的编码JSON文件')
    parser.add_argument('--output', '-o', default='validation.json', help='输出JSON文件')
    args = parser.parse_args()
    
    start_time = time.time()
    
    try:
        # 读取编码数据
        input_path = Path(args.input)
        if not input_path.exists():
            logging.error(f"文件不存在: {args.input}")
            sys.exit(1)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 提取编码列表
        if 'details' in data and 'concepts' in data['details']:
            codes = data['details']['concepts']
        elif isinstance(data, list):
            codes = data
        else:
            logging.error("无法识别的数据格式")
            sys.exit(2)
        
        if len(codes) == 0:
            logging.error("编码列表为空")
            sys.exit(3)
        
        logging.info(f"✓ 读取编码: {len(codes)} 个")
        
        # 执行验证
        all_issues = {
            'naming': check_naming_convention(codes),
            'definition': check_definition_quality(codes),
            'example': check_example_sufficiency(codes)
        }
        
        # 计算评分
        quality_score = calculate_quality_score(codes, all_issues)
        
        # 生成建议
        recommendations = generate_recommendations(all_issues)
        
        processing_time = time.time() - start_time
        
        # 构建输出
        output = {
            'summary': {
                'total_codes': len(codes),
                **quality_score,
                'processing_time': round(processing_time, 2)
            },
            'details': {
                'issues': all_issues,
                'recommendations': recommendations
            },
            'metadata': {
                'input_file': str(input_path.absolute()),
                'timestamp': datetime.now().isoformat(),
                'version': '1.0.0'
            }
        }
        
        # 保存
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        logging.info(f"✅ 验证完成")
        logging.info(f"   编码总数: {len(codes)}")
        logging.info(f"   质量评分: {quality_score['total_score']}/100 ({quality_score['grade']})")
        logging.info(f"   问题总数: {quality_score['total_issues']}")
        logging.info(f"📄 详细结果: {args.output}")
        
    except Exception as e:
        logging.error(f"处理失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(99)

if __name__ == "__main__":
    main()
