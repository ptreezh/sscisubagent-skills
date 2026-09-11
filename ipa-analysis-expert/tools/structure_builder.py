#!/usr/bin/env python3
"""
IPA主从结构构建工具

功能: 构建主从主题结构
用法: python structure_builder.py [选项]

选项:
  --build FILE       从主题列表构建结构
  --validate FILE    验证结构完整性
  --export FORMAT    导出格式 (json/markdown/tree)
"""

import argparse
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class SubTheme:
    """从主题"""
    name: str
    quotes: List[str] = field(default_factory=list)

@dataclass  
class MasterTheme:
    """主主题"""
    name: str
    sub_themes: List[SubTheme] = field(default_factory=list)

class IPAStructureBuilder:
    """IPA主从结构构建器"""
    
    def __init__(self):
        self.master_themes: List[MasterTheme] = []
    
    def add_master_theme(self, name: str) -> MasterTheme:
        """添加主主题"""
        theme = MasterTheme(name=name)
        self.master_themes.append(theme)
        return theme
    
    def add_sub_theme(self, master_name: str, sub_name: str, quotes: List[str] = None) -> bool:
        """添加从主题"""
        for master in self.master_themes:
            if master.name == master_name:
                sub = SubTheme(name=sub_name, quotes=quotes or [])
                master.sub_themes.append(sub)
                return True
        return False
    
    def build_from_dict(self, data: Dict) -> None:
        """从字典构建结构"""
        for master_name, master_data in data.items():
            master = self.add_master_theme(master_name)
            
            if isinstance(master_data, dict):
                for sub_name, sub_data in master_data.items():
                    quotes = sub_data.get("quotes", []) if isinstance(sub_data, dict) else []
                    master.sub_themes.append(SubTheme(name=sub_name, quotes=quotes))
    
    def validate(self) -> Dict:
        """验证结构完整性"""
        results = {
            "valid": True,
            "issues": [],
            "statistics": {
                "master_count": len(self.master_themes),
                "total_sub_count": 0,
                "themes_without_quotes": []
            }
        }
        
        for master in self.master_themes:
            if len(master.sub_themes) == 0:
                results["issues"].append(f"主主题 '{master.name}' 没有从主题")
            
            for sub in master.sub_themes:
                results["statistics"]["total_sub_count"] += 1
                
                if not sub.quotes:
                    results["statistics"]["themes_without_quotes"].append(
                        f"{master.name} > {sub.name}"
                    )
        
        # 每个从主题应有至少一个引语
        if results["statistics"]["themes_without_quotes"]:
            results["issues"].append(
                f"有 {len(results['statistics']['themes_without_quotes'])} 个从主题缺乏引语支撑"
            )
        
        if results["issues"]:
            results["valid"] = False
        
        return results
    
    def to_tree(self) -> str:
        """输出树形结构"""
        lines = []
        
        for i, master in enumerate(self.master_themes, 1):
            lines.append(f"主主题{i}: {master.name}")
            
            for j, sub in enumerate(master.sub_themes, 1):
                lines.append(f"├── 从主题{i}.{j}: {sub.name}")
                
                for k, quote in enumerate(sub.quotes[:2]):  # 最多显示2个引语
                    prefix = "│   └──" if j < len(master.sub_themes) else "    └──"
                    short_quote = quote[:50] + "..." if len(quote) > 50 else quote
                    lines.append(f"{prefix} 引语{k+1}: \"{short_quote}\"")
        
        return "\n".join(lines)
    
    def to_markdown(self) -> str:
        """输出Markdown格式"""
        lines = ["# IPA主从主题结构\n"]
        
        for i, master in enumerate(self.master_themes, 1):
            lines.append(f"## 主主题{i}: {master.name}\n")
            
            for j, sub in enumerate(master.sub_themes, 1):
                lines.append(f"### 从主题{i}.{j}: {sub.name}\n")
                
                if sub.quotes:
                    lines.append("**原文证据**:")
                    for quote in sub.quotes:
                        lines.append(f'> "{quote}"')
                    lines.append("")
        
        return "\n".join(lines)
    
    def to_json(self) -> Dict:
        """输出JSON格式"""
        return {
            "master_themes": [
                {
                    "name": master.name,
                    "sub_themes": [
                        {
                            "name": sub.name,
                            "quotes": sub.quotes
                        }
                        for sub in master.sub_themes
                    ]
                }
                for master in self.master_themes
            ]
        }


def main():
    parser = argparse.ArgumentParser(description="IPA主从结构构建工具")
    parser.add_argument("--build", type=str, help="从JSON文件构建结构")
    parser.add_argument("--validate", type=str, help="验证结构完整性")
    parser.add_argument("--export", choices=["json", "markdown", "tree"], help="导出格式")
    
    args = parser.parse_args()
    
    builder = IPAStructureBuilder()
    
    if args.build:
        try:
            with open(args.build, 'r', encoding='utf-8') as f:
                data = json.load(f)
            builder.build_from_dict(data)
            
            if args.export == "json":
                print(json.dumps(builder.to_json(), ensure_ascii=False, indent=2))
            elif args.export == "markdown":
                print(builder.to_markdown())
            else:
                print(builder.to_tree())
                
        except FileNotFoundError:
            print(f"文件未找到: {args.build}")
    
    elif args.validate:
        try:
            with open(args.validate, 'r', encoding='utf-8') as f:
                data = json.load(f)
            builder.build_from_dict(data)
            results = builder.validate()
            print(json.dumps(results, ensure_ascii=False, indent=2))
        except FileNotFoundError:
            print(f"文件未找到: {args.validate}")
    
    else:
        # 演示输出
        print("IPA主从结构构建工具")
        print("使用 --build 从JSON文件构建结构")
        print("使用 --validate 验证结构完整性")
        print("使用 --export 指定输出格式 (json/markdown/tree)")


if __name__ == "__main__":
    main()
