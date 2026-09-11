#!/usr/bin/env python3
"""构图分析工具"""

import argparse
import json

def analyze_composition(image_data: dict) -> dict:
    """分析图像构图"""
    return {
        'layout': analyze_layout(image_data),
        'color': analyze_color(image_data),
        'perspective': analyze_perspective(image_data)
    }

def analyze_layout(image_data: dict) -> dict:
    """分析布局"""
    width = image_data.get('width', 0)
    height = image_data.get('height', 0)
    
    ratio = width / height if height > 0 else 1
    
    return {
        'aspect_ratio': ratio,
        'orientation': 'landscape' if ratio > 1 else 'portrait',
        'center_of_interest': 'center' if 0.9 <= ratio <= 1.1 else 'rule_of_thirds'
    }

def analyze_color(image_data: dict) -> dict:
    """分析色彩"""
    colors = image_data.get('dominant_colors', [])
    
    return {
        'dominant_colors': colors[:3] if colors else [],
        'temperature': 'warm' if any(is_warm(c) for c in colors) else 'cool',
        'saturation': 'high' if len(colors) < 3 else 'low'
    }

def is_warm(color: str) -> bool:
    """判断是否暖色"""
    warm_colors = ['red', 'orange', 'yellow']
    return color.lower() in warm_colors

def analyze_perspective(image_data: dict) -> dict:
    """分析视角"""
    return {
        'angle': image_data.get('camera_angle', 'eye_level'),
        'distance': image_data.get('distance', 'medium'),
        'framing': image_data.get('framing', 'close_up')
    }

def main():
    parser = argparse.ArgumentParser(description='构图分析')
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    
    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    result = analyze_composition(data)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
