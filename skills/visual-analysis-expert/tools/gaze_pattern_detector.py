#!/usr/bin/env python3
"""凝视模式检测工具"""

import argparse
import json

def detect_gaze_pattern(image_data: dict) -> dict:
    """检测凝视模式"""
    return {
        'gaze_type': classify_gaze(image_data),
        'eye_contact': check_eye_contact(image_data),
        'viewing_relation': analyze_viewing_relation(image_data)
    }

def classify_gaze(image_data: dict) -> str:
    """分类凝视类型"""
    gaze_direction = image_data.get('gaze_direction', 'unknown')
    
    if gaze_direction == 'camera':
        return 'direct_gaze'
    elif gaze_direction == 'self':
        return 'self_gaze'
    elif gaze_direction in ['left', 'right', 'up', 'down']:
        return 'oblique_gaze'
    else:
        return 'unknown'

def check_eye_contact(image_data: dict) -> dict:
    """检查目光接触"""
    return {
        'present': image_data.get('eye_contact', False),
        'intensity': image_data.get('gaze_intensity', 'medium'),
        'viewer_position': 'addressed'
    }

def analyze_viewing_relation(image_data: dict) -> dict:
    """分析观看关系"""
    return {
        'power_relation': classify_power(image_data),
        'distance': image_data.get('social_distance', 'medium'),
        'viewer_role': 'observer'
    }

def classify_power(image_data: dict) -> str:
    """分类权力关系"""
    angle = image_data.get('camera_angle', 'eye_level')
    
    if angle == 'low_angle':
        return 'subject_powerful'
    elif angle == 'high_angle':
        return 'viewer_dominant'
    else:
        return 'equal'

def main():
    parser = argparse.ArgumentParser(description='凝视模式检测')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = detect_gaze_pattern(data)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
