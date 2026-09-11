#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
主题分析专家 - 主题聚类工具
Theme Cluster Tool for Thematic Analysis

功能:
- 将代码聚类为主题
- 识别代码间的关联
- 生成候选主题
- 评估主题质量

作者: Thematic Analysis Expert v5.0.0
创建时间: 2026-03-15
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import hashlib

# 跨平台兼容
def get_output_dir() -> Path:
    """获取输出目录"""
    output_dir = Path(__file__).parent.parent / "output"
    output_dir.mkdir(exist_ok=True)
    return output_dir


@dataclass
class Theme:
    """主题数据类"""
    theme_id: str
    theme_name: str
    theme_definition: str
    codes: List[str]
    supporting_quotes: List[str]
    internal_coherence: float = 0.0
    external_distinctiveness: float = 0.0
    status: str = "candidate"  # candidate, confirmed, rejected
    
    def to_dict(self) -> Dict:
        return asdict(self)


class ThemeCluster:
    """主题聚类器"""
    
    def __init__(self, codes: Dict[str, Dict] = None):
        """
        初始化
        
        Args:
            codes: 代码字典 {code_id: code_info}
        """
        self.codes = codes or {}
        self.themes: Dict[str, Theme] = {}
        self.theme_counter = 0
        self.code_theme_map: Dict[str, List[str]] = defaultdict(list)
        
    def generate_theme_id(self) -> str:
        """生成主题ID"""
        self.theme_counter += 1
        return f"T{self.theme_counter:02d}"
    
    def calculate_code_similarity(self, code1: Dict, code2: Dict) -> float:
        """计算两个代码之间的相似度"""
        similarity = 0.0
        
        # 基于定义文本的相似度（简化实现）
        def1 = code1.get("code_definition", "")
        def2 = code2.get("code_definition", "")
        
        # 关键词重叠
        words1 = set(def1.split())
        words2 = set(def2.split())
        if words1 or words2:
            overlap = len(words1 & words2)
            total = len(words1 | words2)
            similarity += overlap / total if total > 0 else 0
        
        # 共现频率（如果有coded_segments数据）
        # 这里简化处理
        
        return similarity
    
    def cluster_codes_by_similarity(
        self, 
        similarity_threshold: float = 0.3
    ) -> List[Set[str]]:
        """
        基于相似度聚类代码
        
        Returns:
            代码ID集合的列表，每个集合代表一个潜在主题
        """
        if not self.codes:
            return []
        
        code_ids = list(self.codes.keys())
        clusters = []
        assigned = set()
        
        for i, code_id1 in enumerate(code_ids):
            if code_id1 in assigned:
                continue
            
            cluster = {code_id1}
            assigned.add(code_id1)
            
            for j, code_id2 in enumerate(code_ids[i+1:], i+1):
                if code_id2 in assigned:
                    continue
                
                similarity = self.calculate_code_similarity(
                    self.codes[code_id1],
                    self.codes[code_id2]
                )
                
                if similarity >= similarity_threshold:
                    cluster.add(code_id2)
                    assigned.add(code_id2)
            
            if len(cluster) > 0:
                clusters.append(cluster)
        
        return clusters
    
    def create_theme_from_cluster(
        self,
        code_ids: Set[str],
        theme_name: str = None,
        theme_definition: str = None
    ) -> Theme:
        """从代码聚类创建主题"""
        # 收集代码信息
        code_names = [self.codes[cid]["code_name"] for cid in code_ids if cid in self.codes]
        quotes = []
        for cid in code_ids:
            if cid in self.codes:
                quote = self.codes[cid].get("source_quote", "")
                if quote:
                    quotes.append(quote)
        
        # 生成主题名称（如果未提供）
        if not theme_name:
            # 简化：使用最常见的代码名称关键词
            all_words = " ".join(code_names).split()
            word_freq = Counter(all_words)
            if word_freq:
                theme_name = word_freq.most_common(1)[0][0]
            else:
                theme_name = f"主题{self.theme_counter + 1}"
        
        # 生成主题定义（如果未提供）
        if not theme_definition:
            theme_definition = f"包含{len(code_ids)}个相关代码: {', '.join(code_names)}"
        
        theme = Theme(
            theme_id=self.generate_theme_id(),
            theme_name=theme_name,
            theme_definition=theme_definition,
            codes=list(code_ids),
            supporting_quotes=quotes[:5]  # 最多5个支持性引文
        )
        
        # 更新代码-主题映射
        for code_id in code_ids:
            self.code_theme_map[code_id].append(theme.theme_id)
        
        return theme
    
    def develop_themes(
        self,
        method: str = "similarity",
        **kwargs
    ) -> Dict:
        """
        发展主题
        
        Args:
            method: 聚类方法 (similarity/manual/semantic)
        
        Returns:
            发展结果
        """
        if method == "similarity":
            threshold = kwargs.get("similarity_threshold", 0.3)
            clusters = self.cluster_codes_by_similarity(threshold)
            
            for cluster in clusters:
                theme = self.create_theme_from_cluster(cluster)
                self.themes[theme.theme_id] = theme
        
        elif method == "manual":
            # 手动创建主题
            theme_name = kwargs.get("theme_name", "")
            theme_definition = kwargs.get("theme_definition", "")
            code_ids = kwargs.get("code_ids", set())
            
            if code_ids:
                theme = self.create_theme_from_cluster(
                    code_ids, theme_name, theme_definition
                )
                self.themes[theme.theme_id] = theme
        
        return {
            "status": "success",
            "total_themes": len(self.themes),
            "themes": {tid: t.to_dict() for tid, t in self.themes.items()}
        }
    
    def assess_theme_quality(self, theme_id: str) -> Dict:
        """评估主题质量"""
        if theme_id not in self.themes:
            return {"status": "error", "message": "主题不存在"}
        
        theme = self.themes[theme_id]
        
        # 计算内部一致性
        # 基于代码间相似度
        internal_coherence = 0.0
        code_pairs = 0
        for i, code_id1 in enumerate(theme.codes):
            for code_id2 in theme.codes[i+1:]:
                if code_id1 in self.codes and code_id2 in self.codes:
                    internal_coherence += self.calculate_code_similarity(
                        self.codes[code_id1],
                        self.codes[code_id2]
                    )
                    code_pairs += 1
        
        if code_pairs > 0:
            internal_coherence /= code_pairs
        
        theme.internal_coherence = internal_coherence
        
        # 计算外部异质性
        external_distinctiveness = 1.0  # 默认高区分度
        for other_id, other_theme in self.themes.items():
            if other_id != theme_id:
                # 计算与其他主题的重叠
                overlap = len(set(theme.codes) & set(other_theme.codes))
                if overlap > 0:
                    external_distinctiveness -= 0.1
        
        theme.external_distinctiveness = max(0, external_distinctiveness)
        
        return {
            "theme_id": theme_id,
            "internal_coherence": internal_coherence,
            "external_distinctiveness": external_distinctiveness,
            "quality_assessment": "good" if internal_coherence > 0.5 and external_distinctiveness > 0.5 else "needs_review"
        }
    
    def review_themes(self) -> Dict:
        """审查所有主题"""
        results = {
            "themes_to_keep": [],
            "themes_to_merge": [],
            "themes_to_split": [],
            "themes_to_delete": []
        }
        
        for theme_id, theme in self.themes.items():
            quality = self.assess_theme_quality(theme_id)
            
            if quality["internal_coherence"] > 0.5 and quality["external_distinctiveness"] > 0.5:
                results["themes_to_keep"].append(theme_id)
            elif quality["internal_coherence"] < 0.3:
                results["themes_to_split"].append(theme_id)
            elif quality["external_distinctiveness"] < 0.3:
                results["themes_to_merge"].append(theme_id)
            else:
                results["themes_to_keep"].append(theme_id)
        
        return results
    
    def merge_themes(self, theme_ids: List[str], new_name: str = None) -> Optional[Theme]:
        """合并主题"""
        all_codes = set()
        all_quotes = []
        
        for tid in theme_ids:
            if tid in self.themes:
                theme = self.themes[tid]
                all_codes.update(theme.codes)
                all_quotes.extend(theme.supporting_quotes)
                del self.themes[tid]
        
        if all_codes:
            new_theme = Theme(
                theme_id=self.generate_theme_id(),
                theme_name=new_name or f"合并主题{self.theme_counter}",
                theme_definition=f"由{len(theme_ids)}个主题合并而成",
                codes=list(all_codes),
                supporting_quotes=list(set(all_quotes))[:5]
            )
            self.themes[new_theme.theme_id] = new_theme
            return new_theme
        
        return None
    
    def split_theme(self, theme_id: str, split_criteria: Dict = None) -> List[Theme]:
        """拆分主题"""
        if theme_id not in self.themes:
            return []
        
        theme = self.themes[theme_id]
        del self.themes[theme_id]
        
        # 简化：按代码数量均分
        codes = theme.codes
        mid = len(codes) // 2
        
        new_themes = []
        for i, code_subset in enumerate([codes[:mid], codes[mid:]]):
            if code_subset:
                new_theme = Theme(
                    theme_id=self.generate_theme_id(),
                    theme_name=f"{theme.theme_name}_部分{i+1}",
                    theme_definition=f"从主题{theme_id}拆分",
                    codes=code_subset,
                    supporting_quotes=theme.supporting_quotes[:3]
                )
                self.themes[new_theme.theme_id] = new_theme
                new_themes.append(new_theme)
        
        return new_themes
    
    def get_theme_report(self) -> str:
        """生成主题报告"""
        report = "# 主题发展报告\n\n"
        
        for theme_id, theme in self.themes.items():
            quality = self.assess_theme_quality(theme_id)
            report += f"## {theme_id}: {theme.theme_name}\n\n"
            report += f"**定义**: {theme.theme_definition}\n\n"
            report += f"**包含代码**: {', '.join(theme.codes)}\n\n"
            report += f"**质量评估**:\n"
            report += f"- 内部一致性: {quality['internal_coherence']:.2f}\n"
            report += f"- 外部异质性: {quality['external_distinctiveness']:.2f}\n\n"
            
            if theme.supporting_quotes:
                report += "**支持性引文**:\n"
                for quote in theme.supporting_quotes[:3]:
                    report += f"> {quote}\n\n"
        
        return report
    
    def export_results(self, output_format: str = "json") -> str:
        """导出结果"""
        results = {
            "themes": {tid: t.to_dict() for tid, t in self.themes.items()},
            "review": self.review_themes(),
            "summary": {
                "total_themes": len(self.themes),
                "total_codes_assigned": sum(len(t.codes) for t in self.themes.values())
            }
        }
        
        if output_format == "json":
            output_path = get_output_dir() / "theme_results.json"
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            return str(output_path)
        
        elif output_format == "markdown":
            output_path = get_output_dir() / "theme_results.md"
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(self.get_theme_report())
            return str(output_path)
        
        return json.dumps(results, ensure_ascii=False, indent=2)


def process_codes(codes: Dict, options: Dict = None) -> Dict:
    """处理代码 - 主入口函数"""
    options = options or {}
    
    cluster = ThemeCluster(codes=codes)
    result = cluster.develop_themes(
        method=options.get("method", "similarity"),
        **options
    )
    
    return result


# 示例使用
if __name__ == "__main__":
    # 测试数据
    sample_codes = {
        "C001": {
            "code_name": "教学挑战",
            "code_definition": "教师在教学过程中遇到的困难和障碍",
            "source_quote": "在线教学最大的挑战是如何保持学生的注意力"
        },
        "C002": {
            "code_name": "技术困难",
            "code_definition": "技术相关的问题和障碍",
            "source_quote": "有时候网络不好，学生就听不清楚"
        },
        "C003": {
            "code_name": "教学优势",
            "code_definition": "在线教学的积极方面",
            "source_quote": "可以录播，学生可以反复看"
        },
        "C004": {
            "code_name": "技术支持需求",
            "code_definition": "对技术支持的需要和期望",
            "source_quote": "技术支持很重要，没有好的技术支持什么都做不了"
        }
    }
    
    # 创建聚类器
    cluster = ThemeCluster(codes=sample_codes)
    
    # 发展主题
    result = cluster.develop_themes(method="similarity", similarity_threshold=0.2)
    
    print(f"主题聚类结果:")
    print(f"- 总主题数: {result['total_themes']}")
    
    # 审查主题
    review = cluster.review_themes()
    print(f"\n主题审查:")
    print(f"- 保留: {review['themes_to_keep']}")
    print(f"- 需合并: {review['themes_to_merge']}")
    
    # 生成报告
    print("\n" + cluster.get_theme_report())
