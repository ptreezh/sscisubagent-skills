#!/usr/bin/env python
"""
调查数据清洗工具
清洗和预处理社会网络调查数据
"""

import argparse
import json
import sys
from datetime import datetime
from typing import Dict, List, Any

def check_required_fields(respondent: Dict) -> bool:
    """检查必需字段"""
    required_fields = ['id', 'name', 'collaborators']
    return all(field in respondent and respondent[field] for field in required_fields)

def clean_name(name: str) -> str:
    """清洗姓名"""
    if not name:
        return ""
    # 移除多余空格
    return " ".join(name.split())

def validate_collaborators(collaborators: List) -> List:
    """验证合作者数据"""
    if not isinstance(collaborators, list):
        return []
    
    cleaned = []
    for collab in collaborators:
        if isinstance(collab, dict) and 'name' in collab:
            # 确保有必要的字段
            cleaned_collab = {
                'name': clean_name(collab.get('name', '')),
                'frequency': collab.get('frequency', ''),
                'type': collab.get('type', '')
            }
            if cleaned_collab['name']:  # 只保留有姓名的
                cleaned.append(cleaned_collab)
    
    return cleaned

def clean_respondent_data(respondent: Dict) -> Dict:
    """清洗单个受访者数据"""
    cleaned = respondent.copy()
    
    # 清洗姓名
    cleaned['name'] = clean_name(respondent.get('name', ''))
    
    # 验证合作者数据
    cleaned['collaborators'] = validate_collaborators(respondent.get('collaborators', []))
    
    # 清理数值字段
    numeric_fields = ['age', 'publications', 'h_index', 'grant_amount']
    for field in numeric_fields:
        value = respondent.get(field)
        try:
            cleaned[field] = float(value) if value is not None else None
        except (ValueError, TypeError):
            cleaned[field] = None
    
    # 清理列表字段
    list_fields = ['research_areas']
    for field in list_fields:
        value = respondent.get(field, [])
        if isinstance(value, list):
            cleaned[field] = [str(v).strip() for v in value if v]
        else:
            cleaned[field] = []
    
    return cleaned

def detect_outliers(respondents: List[Dict]) -> Dict:
    """检测异常值"""
    numeric_fields = ['age', 'publications', 'h_index', 'grant_amount']
    outliers = {}
    
    for field in numeric_fields:
        values = [r.get(field) for r in respondents if r.get(field) is not None]
        if len(values) >= 3:
            values.sort()
            n = len(values)
            q1 = values[n // 4]
            q3 = values[3 * n // 4]
            iqr = q3 - q1
            
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            field_outliers = []
            for i, respondent in enumerate(respondents):
                value = respondent.get(field)
                if value is not None and (value < lower_bound or value > upper_bound):
                    field_outliers.append({
                        'respondent_id': respondent.get('id', ''),
                        'value': value,
                        'type': 'high' if value > upper_bound else 'low'
                    })
            
            if field_outliers:
                outliers[field] = field_outliers
    
    return outliers

def apply_cleaning_rules(respondents: List[Dict]) -> Dict:
    """应用清洗规则"""
    rules_applied = []
    
    # 规则1: 移除无效受访者
    original_count = len(respondents)
    valid_respondents = [r for r in respondents if check_required_fields(r)]
    invalid_count = original_count - len(valid_respondents)
    if invalid_count > 0:
        rules_applied.append(f"移除{invalid_count}个无效受访者")
    
    # 规则2: 清洗每个受访者的数据
    cleaned_respondents = [clean_respondent_data(r) for r in valid_respondents]
    rules_applied.append("清洗受访者数据格式")
    
    # 规则3: 移除没有合作者的受访者
    with_collaborators = [r for r in cleaned_respondents if r.get('collaborators')]
    no_collab_count = len(cleaned_respondents) - len(with_collaborators)
    if no_collab_count > 0:
        rules_applied.append(f"移除{no_collab_count}个无合作者的受访者")
    
    # 规则4: 检测异常值
    outliers = detect_outliers(with_collaborators)
    if outliers:
        rules_applied.append(f"检测到{sum(len(v) for v in outliers.values())}个异常值")
    
    return {
        'cleaned_data': with_collaborators,
        'rules_applied': rules_applied,
        'outliers': outliers,
        'cleaning_stats': {
            'original_count': original_count,
            'invalid_removed': invalid_count,
            'no_collaborator_removed': no_collab_count,
            'final_count': len(with_collaborators)
        }
    }

def generate_cleaning_report(result: Dict) -> Dict:
    """生成清洗报告"""
    stats = result['cleaning_stats']
    
    report = {
        'data_quality_score': 0.0,
        'completeness': {},
        'consistency': {},
        'issues_detected': []
    }
    
    # 计算数据质量得分
    if stats['original_count'] > 0:
        retention_rate = stats['final_count'] / stats['original_count']
        report['data_quality_score'] = round(retention_rate * 100, 2)
    
    # 完整性分析
    final_data = result['cleaned_data']
    if final_data:
        # 必需字段完整性
        required_fields = ['id', 'name', 'department', 'position']
        for field in required_fields:
            complete = sum(1 for r in final_data if r.get(field))
            report['completeness'][field] = {
                'complete': complete,
                'total': len(final_data),
                'rate': round(complete / len(final_data) * 100, 2)
            }
        
        # 数值字段完整性
        numeric_fields = ['age', 'publications', 'h_index']
        for field in numeric_fields:
            complete = sum(1 for r in final_data if r.get(field) is not None)
            report['completeness'][f'{field}_numeric'] = {
                'complete': complete,
                'total': len(final_data),
                'rate': round(complete / len(final_data) * 100, 2)
            }
    
    # 一致性检查
    if result['outliers']:
        report['issues_detected'].append("检测到数值异常值")
    
    if stats['invalid_removed'] > 0:
        report['issues_detected'].append("存在无效数据记录")
    
    return report

def main():
    parser = argparse.ArgumentParser(
        description='调查数据清洗工具',
        epilog='示例：python clean_survey_data.py --input survey.json --output cleaned.json'
    )
    
    parser.add_argument('--input', '-i', required=True, help='输入调查数据文件（JSON）')
    parser.add_argument('--output', '-o', default='cleaned_survey_data.json', help='输出文件')
    parser.add_argument('--remove-outliers', action='store_true',
                       help='移除异常值')
    
    args = parser.parse_args()
    
    # 读取数据
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"错误：无法读取输入文件 - {e}", file=sys.stderr)
        sys.exit(1)
    
    start_time = datetime.now()
    
    # 提取受访者数据
    respondents = data.get('respondents', [])
    if not respondents:
        print("错误：未找到受访者数据", file=sys.stderr)
        sys.exit(1)
    
    # 应用清洗规则
    result = apply_cleaning_rules(respondents)
    
    # 可选：移除异常值
    if args.remove_outliers and result['outliers']:
        outlier_ids = set()
        for field_outliers in result['outliers'].values():
            for outlier in field_outliers:
                outlier_ids.add(outlier['respondent_id'])
        
        original_count = len(result['cleaned_data'])
        result['cleaned_data'] = [
            r for r in result['cleaned_data'] 
            if r.get('id') not in outlier_ids
        ]
        removed_count = original_count - len(result['cleaned_data'])
        result['rules_applied'].append(f"移除{removed_count}个异常值受访者")
    
    # 生成清洗报告
    cleaning_report = generate_cleaning_report(result)
    
    end_time = datetime.now()
    
    # 准备输出
    output = {
        'summary': {
            'n_respondents': len(respondents),
            'n_valid_respondents': len(result['cleaned_data']),
            'n_rules_applied': len(result['rules_applied']),
            'data_quality_score': cleaning_report['data_quality_score'],
            'processing_time': round((end_time - start_time).total_seconds(), 2)
        },
        'details': {
            'cleaned_data': result['cleaned_data'],
            'rules_applied': result['rules_applied'],
            'cleaning_stats': result['cleaning_stats'],
            'outliers': result['outliers'],
            'cleaning_report': cleaning_report
        },
        'metadata': {
            'input_file': args.input,
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
            'skill': 'processing-network-data'
        }
    }
    
    # 保存结果
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        
        print(f"✓ 数据清洗完成")
        print(f"  - 原始受访者：{len(respondents)}")
        print(f"  - 有效受访者：{len(result['cleaned_data'])}")
        print(f"  - 数据质量得分：{cleaning_report['data_quality_score']:.2f}")
        print(f"  - 应用规则数：{len(result['rules_applied'])}")
        print(f"  - 输出文件：{args.output}")
        
    except Exception as e:
        print(f"错误：无法保存结果 - {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()