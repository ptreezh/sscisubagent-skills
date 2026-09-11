#!/usr/bin/env python3
"""
IPA主题发展工具

功能: 辅助从注释发展主题
用法: python theme_developer.py [选项]

选项:
  --from-annotations FILE   从注释文件生成主题
  --validate THEME          验证主题质量
  --suggest                主题命名建议
"""

import argparse
import json
import re
from typing import Dict, List, Optional, Tuple

class IPAThemeDeveloper:
    """IPA主题发展类"""
    
    # 心理学术语关键词
    PSYCHOLOGICAL_TERMS = [
        "自我", "认同", "意义", "体验", "过程", "感受",
        "理解", "诠释", "建构", "关系", "边界", "转变",
        "冲突", "整合", "适应", "应对", "压力", "焦虑",
        "身份", "角色", "期望", "价值", "信念", "叙事"
    ]
    
    # 应避免的诊断术语
    DIAGNOSTIC_TERMS = [
        "症状", "诊断", "病理", "异常", "障碍", "患者",
        "治疗", "临床", "疾病", "综合征"
    ]
    
    def __init__(self):
        pass
    
    def develop_theme(self, annotations: Dict) -> Dict:
        """从注释发展主题"""
        themes = {
            "emergent_themes": [],
            "psychological_names": [],
            "connections": []
        }
        
        # 从概念性注释中提取主题
        if "conceptual" in annotations:
            concepts = annotations["conceptual"]
            
            # 识别关键词
            for term in self.PSYCHOLOGICAL_TERMS:
                if term in concepts:
                    themes["emergent_themes"].append(f"{term}的体验")
        
        return themes
    
    def validate_theme(self, theme_name: str, evidence: List[str]) -> Dict:
        """验证主题质量"""
        results = {
            "valid": True,
            "issues": [],
            "suggestions": []
        }
        
        # 检查是否使用心理学术语
        has_psychological_term = any(
            term in theme_name for term in self.PSYCHOLOGICAL_TERMS
        )
        if not has_psychological_term:
            results["issues"].append("主题命名未使用心理学术语")
            results["suggestions"].append(
                "建议使用如'自我'、'体验'、'意义'等心理学术语"
            )
        
        # 检查是否使用诊断术语
        has_diagnostic_term = any(
            term in theme_name for term in self.DIAGNOSTIC_TERMS
        )
        if has_diagnostic_term:
            results["valid"] = False
            results["issues"].append("主题命名使用了诊断术语（IPA应避免）")
        
        # 检查证据
        if not evidence or len(evidence) < 1:
            results["valid"] = False
            results["issues"].append("主题缺乏原文证据支撑")
        elif len(evidence) < 2:
            results["suggestions"].append("建议为每个主题提供至少2个原文证据")
        
        return results
    
    def suggest_names(self, emergent_theme: str) -> List[str]:
        """提供主题命名建议"""
        suggestions = []
        
        # 添加心理学术语前缀/后缀
        prefixes = ["体验中的", "对...的", "...过程中的"]
        suffixes = ["的体验", "的理解", "的意义", "的过程"]
        
        for suffix in suffixes:
            suggestions.append(f"{emergent_theme}{suffix}")
        
        return suggestions[:5]  # 返回最多5个建议
    
    def identify_master_slave(self, themes: List[Dict]) -> Dict:
        """识别主从关系"""
        structure = {
            "master_themes": [],
            "orphan_themes": []
        }
        
        for theme in themes:
            if theme.get("sub_themes"):
                structure["master_themes"].append(theme)
            elif theme.get("parent_theme"):
                pass  # 已有父主题
            else:
                structure["orphan_themes"].append(theme)
        
        return structure


def main():
    parser = argparse.ArgumentParser(description="IPA主题发展工具")
    parser.add_argument("--from-annotations", type=str, help="从注释文件生成主题")
    parser.add_argument("--validate", type=str, help="验证主题质量")
    parser.add_argument("--suggest", action="store_true", help="主题命名建议")
    
    args = parser.parse_args()
    
    developer = IPAThemeDeveloper()
    
    if args.from_annotations:
        try:
            with open(args.from_annotations, 'r', encoding='utf-8') as f:
                annotations = json.load(f)
            themes = developer.develop_theme(annotations)
            print(json.dumps(themes, ensure_ascii=False, indent=2))
        except FileNotFoundError:
            print(f"文件未找到: {args.from_annotations}")
    
    elif args.validate:
        print(f"验证主题: {args.validate}")
        # 简单验证演示
        results = developer.validate_theme(args.validate, ["示例证据"])
        print(json.dumps(results, ensure_ascii=False, indent=2))
    
    elif args.suggest:
        print("主题命名建议")
        print("输入新兴主题名称获取心理学术语命名建议...")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
