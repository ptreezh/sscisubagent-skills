#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
研究设计技能 - 文献分析模块
提供文献收集、整理、分析和知识缺口识别功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional, Union, Any
import warnings
import re
from datetime import datetime


class LiteratureAnalyzer:
    """文献分析器 - 分析研究领域的文献状况"""
    
    def __init__(self):
        self.literature_data = None
        self.analysis_results = {}
        
    def load_literature_data(self, data: Union[str, pd.DataFrame]) -> pd.DataFrame:
        """
        加载文献数据
        
        Args:
            data: CSV文件路径或DataFrame
            
        Returns:
            DataFrame: 文献数据
        """
        if isinstance(data, str):
            self.literature_data = pd.read_csv(data)
        else:
            self.literature_data = data.copy()
            
        # 确保必要的列存在
        required_columns = ['title', 'author', 'year', 'journal', 'abstract']
        for col in required_columns:
            if col not in self.literature_data.columns:
                # 创建虚拟列
                self.literature_data[col] = ""
                
        return self.literature_data
    
    def analyze_publication_trends(self) -> Dict[str, Any]:
        """
        分析出版趋势
        
        Returns:
            Dict: 出版趋势分析结果
        """
        if self.literature_data is None:
            return {}
            
        # 确保year列存在且为数值
        if 'year' in self.literature_data.columns:
            year_data = pd.to_numeric(self.literature_data['year'], errors='coerce')
            year_counts = year_data.value_counts().sort_index()
            
            trend_analysis = {
                'yearly_publications': year_counts.to_dict(),
                'total_publications': len(self.literature_data),
                'publication_period': {
                    'start_year': int(year_counts.index.min()) if not year_counts.empty else 0,
                    'end_year': int(year_counts.index.max()) if not year_counts.empty else 0,
                    'span_years': int(year_counts.index.max() - year_counts.index.min() + 1) if not year_counts.empty else 0
                },
                'average_annual_output': float(year_counts.mean()) if not year_counts.empty else 0.0
            }
        else:
            trend_analysis = {
                'yearly_publications': {},
                'total_publications': len(self.literature_data),
                'publication_period': {
                    'start_year': 0,
                    'end_year': 0,
                    'span_years': 0
                },
                'average_annual_output': 0.0
            }
            
        self.analysis_results['trend_analysis'] = trend_analysis
        return trend_analysis
    
    def analyze_research_themes(self, top_n: int = 10) -> Dict[str, Any]:
        """
        分析研究主题
        
        Args:
            top_n: 返回前N个主题
            
        Returns:
            Dict: 研究主题分析结果
        """
        if self.literature_data is None:
            return {}
            
        # 从标题和摘要中提取关键词
        all_texts = []
        if 'title' in self.literature_data.columns:
            all_texts.extend(self.literature_data['title'].fillna('').astype(str).tolist())
        if 'abstract' in self.literature_data.columns:
            all_texts.extend(self.literature_data['abstract'].fillna('').astype(str).tolist())
        
        # 简单的关键词提取（实际应用中可能需要更复杂的NLP技术）
        all_text = ' '.join(all_texts).lower()
        # 移除标点符号，提取单词
        words = re.findall(r'\b[a-zA-Z]{4,}\b', all_text)  # 只提取4个字母以上的单词
        
        # 统计词频
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # 排序并返回top_n
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:top_n]
        
        theme_analysis = {
            'top_keywords': dict(sorted_words),
            'total_unique_terms': len(word_freq),
            'dominant_themes': [word for word, count in sorted_words]
        }
        
        self.analysis_results['theme_analysis'] = theme_analysis
        return theme_analysis
    
    def identify_knowledge_gaps(self) -> List[Dict[str, Any]]:
        """
        识别知识缺口
        
        Returns:
            List: 知识缺口列表
        """
        if self.literature_data is None:
            return []
            
        gaps = []
        
        # 基于出版趋势识别可能的知识缺口
        trend_analysis = self.analysis_results.get('trend_analysis', {})
        if trend_analysis:
            yearly_pub = trend_analysis.get('yearly_publications', {})
            if yearly_pub:
                years = list(yearly_pub.keys())
                if len(years) > 1:
                    # 查找出版量显著下降的年份
                    avg_pub = np.mean(list(yearly_pub.values()))
                    low_pub_years = [year for year, count in yearly_pub.items() 
                                   if count < avg_pub * 0.5 and count > 0]
                    
                    if low_pub_years:
                        gaps.append({
                            'gap_type': 'temporal',
                            'description': f'出版量较低的年份: {low_pub_years}',
                            'significance': '可能反映研究兴趣或资源投入的变化'
                        })
        
        # 基于主题分析识别知识缺口
        theme_analysis = self.analysis_results.get('theme_analysis', {})
        if theme_analysis:
            top_keywords = theme_analysis.get('top_keywords', {})
            if len(top_keywords) < 10:  # 如果高频词汇较少，可能存在研究空白
                gaps.append({
                    'gap_type': 'thematic',
                    'description': f'高频研究主题较少，可能存在研究空白',
                    'significance': '研究领域可能较为新颖或分散'
                })
        
        # 基于文献数量识别知识缺口
        if len(self.literature_data) < 50:  # 偪设少于50篇为研究不足
            gaps.append({
                'gap_type': 'volume',
                'description': f'文献总数较少 ({len(self.literature_data)} 篇)',
                'significance': '研究领域可能较新或关注度不足'
            })
        
        self.analysis_results['knowledge_gaps'] = gaps
        return gaps
    
    def generate_literature_report(self) -> str:
        """
        生成文献分析报告
        
        Returns:
            str: 分析报告
        """
        if self.literature_data is None:
            return "未加载文献数据"
            
        report = []
        report.append("# 文献分析报告\n")
        report.append(f"分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        # 基本统计
        report.append("## 基本统计\n")
        report.append(f"- 文献总数: {len(self.literature_data)} 篇\n")
        report.append(f"- 数据时间范围: {self.literature_data.get('year', pd.Series()).min()} - {self.literature_data.get('year', pd.Series()).max()}\n\n")
        
        # 出版趋势
        trend_analysis = self.analysis_results.get('trend_analysis', {})
        if trend_analysis:
            report.append("## 出版趋势\n")
            period = trend_analysis.get('publication_period', {})
            report.append(f"- 出版时间跨度: {period.get('start_year', 'N/A')} - {period.get('end_year', 'N/A')} ({period.get('span_years', 'N/A')} 年)\n")
            report.append(f"- 年均出版量: {trend_analysis.get('average_annual_output', 0):.2f} 篇\n\n")
        
        # 研究主题
        theme_analysis = self.analysis_results.get('theme_analysis', {})
        if theme_analysis:
            report.append("## 主要研究主题\n")
            top_keywords = list(theme_analysis.get('top_keywords', {}).keys())[:5]
            report.append("- " + ", ".join(top_keywords) + "\n\n")
        
        # 知识缺口
        knowledge_gaps = self.analysis_results.get('knowledge_gaps', [])
        if knowledge_gaps:
            report.append("## 识别的知识缺口\n")
            for gap in knowledge_gaps:
                report.append(f"- **{gap['gap_type']}**: {gap['description']}\n")
                report.append(f"  - 意义: {gap['significance']}\n\n")
        else:
            report.append("## 知识缺口\n")
            report.append("未识别到明显的知识缺口\n\n")
        
        # 建议
        report.append("## 研究建议\n")
        if knowledge_gaps:
            report.append("基于识别的知识缺口，建议在以下方面加强研究：\n")
            for gap in knowledge_gaps:
                report.append(f"- {gap['description']}\n")
        else:
            report.append("当前研究领域文献较为丰富，建议深化现有研究方向或探索跨领域整合。\n")
        
        return "".join(report)


def main():
    """示例用法"""
    print("📚 研究设计 - 文献分析模块演示")
    
    # 创建示例数据
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'title': [
            'The Impact of Social Media on Mental Health',
            'Digital Technology and Psychological Well-being',
            'Social Networks Effects on Individual Behavior',
            'Technology Adoption in Modern Society',
            'Psychological Factors in Digital Engagement',
            'Social Media Usage Patterns Among Youth',
            'Digital Divide and Access to Technology',
            'Online Communities and Social Support',
            'Cyberbullying and Mental Health Outcomes',
            'Privacy Concerns in Digital Age'
        ],
        'author': [
            'Smith, J.', 'Johnson, A.', 'Williams, R.',
            'Brown, S.', 'Davis, M.', 'Miller, T.',
            'Wilson, K.', 'Moore, L.', 'Taylor, P.', 'Anderson, H.'
        ],
        'year': np.random.choice(range(2018, 2024), 10),
        'journal': [
            'Journal of Psychology', 'Digital Society Review', 'Tech & Behavior',
            'Modern Psychology', 'Cyberpsychology', 'Social Science Today',
            'Technology Quarterly', 'Digital Research', 'Psychological Science',
            'Online Behavior Studies'
        ],
        'abstract': [
            'This study examines the relationship between social media usage and mental health outcomes...',
            'Research on how digital technology affects psychological well-being...',
            'Analysis of how social networks influence individual behavioral patterns...',
            'Investigation of technology adoption trends in contemporary society...',
            'Study of psychological factors affecting digital engagement...',
            'Patterns of social media usage among young people...',
            'Examining the digital divide and technology access issues...',
            'Role of online communities in providing social support...',
            'Impact of cyberbullying on mental health outcomes...',
            'Privacy concerns in the age of digital technology...'
        ]
    })
    
    # 初始化分析器
    analyzer = LiteratureAnalyzer()
    
    # 加载数据
    analyzer.load_literature_data(sample_data)
    
    # 执行分析
    trend_analysis = analyzer.analyze_publication_trends()
    theme_analysis = analyzer.analyze_research_themes(top_n=5)
    knowledge_gaps = analyzer.identify_knowledge_gaps()
    
    # 生成报告
    report = analyzer.generate_literature_report()
    print(report)
    
    print("✅ 文献分析完成！")


if __name__ == "__main__":
    main()