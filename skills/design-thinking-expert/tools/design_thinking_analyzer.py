#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
设计思维分析工具
Design Thinking Analyzer Tool

版本: 5.0.0-cli-native+agent
方法论: IDEO/Stanford d.school Design Thinking

功能:
- 同理心地图生成
- 用户旅程映射
- HMW问题生成
- 创意聚类分析
- 原型类型推荐
- 测试反馈分析
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from pathlib import Path


class EmpathyMapGenerator:
    """同理心地图生成器"""
    
    def __init__(self):
        self.template = {
            "say": [],      # 用户说
            "think": [],    # 用户想
            "do": [],       # 用户做
            "feel": [],     # 用户感
            "pains": [],    # 痛点
            "gains": []     # 收益
        }
    
    def generate(self, user_name: str, interview_data: Dict) -> Dict:
        """
        生成同理心地图
        
        Args:
            user_name: 用户名称
            interview_data: 访谈数据
        
        Returns:
            同理心地图字典
        """
        empathy_map = {
            "user_name": user_name,
            "created_at": datetime.now().isoformat(),
            "map": self.template.copy()
        }
        
        # 从访谈数据中提取信息
        if "quotes" in interview_data:
            empathy_map["map"]["say"] = interview_data["quotes"]
        
        if "thoughts" in interview_data:
            empathy_map["map"]["think"] = interview_data["thoughts"]
        
        if "behaviors" in interview_data:
            empathy_map["map"]["do"] = interview_data["behaviors"]
        
        if "emotions" in interview_data:
            empathy_map["map"]["feel"] = interview_data["emotions"]
        
        if "pain_points" in interview_data:
            empathy_map["map"]["pains"] = interview_data["pain_points"]
        
        if "desired_outcomes" in interview_data:
            empathy_map["map"]["gains"] = interview_data["desired_outcomes"]
        
        return empathy_map
    
    def to_markdown(self, empathy_map: Dict) -> str:
        """转换为Markdown格式"""
        md = f"# 同理心地图: {empathy_map['user_name']}\n\n"
        md += f"创建时间: {empathy_map['created_at']}\n\n"
        
        map_data = empathy_map["map"]
        
        md += "## 说 (Say)\n"
        for item in map_data.get("say", []):
            md += f"- {item}\n"
        md += "\n"
        
        md += "## 想 (Think)\n"
        for item in map_data.get("think", []):
            md += f"- {item}\n"
        md += "\n"
        
        md += "## 做 (Do)\n"
        for item in map_data.get("do", []):
            md += f"- {item}\n"
        md += "\n"
        
        md += "## 感 (Feel)\n"
        for item in map_data.get("feel", []):
            md += f"- {item}\n"
        md += "\n"
        
        md += "## 痛点 (Pains)\n"
        for item in map_data.get("pains", []):
            md += f"- {item}\n"
        md += "\n"
        
        md += "## 收益 (Gains)\n"
        for item in map_data.get("gains", []):
            md += f"- {item}\n"
        
        return md


class UserJourneyMapper:
    """用户旅程映射器"""
    
    def __init__(self):
        self.stages = []
    
    def add_stage(self, stage_name: str, behaviors: List[str], 
                  thoughts: List[str], emotions: List[str],
                  touchpoints: List[str], pain_points: List[str],
                  opportunities: List[str]):
        """添加旅程阶段"""
        self.stages.append({
            "stage": stage_name,
            "behaviors": behaviors,
            "thoughts": thoughts,
            "emotions": emotions,
            "touchpoints": touchpoints,
            "pain_points": pain_points,
            "opportunities": opportunities
        })
    
    def generate(self, user_persona: Dict) -> Dict:
        """
        生成用户旅程图
        
        Args:
            user_persona: 用户画像
        
        Returns:
            用户旅程图字典
        """
        journey = {
            "user_persona": user_persona,
            "created_at": datetime.now().isoformat(),
            "stages": self.stages,
            "key_insights": [],
            "innovation_opportunities": []
        }
        
        # 分析痛点和机会
        all_pains = []
        all_opportunities = []
        
        for stage in self.stages:
            all_pains.extend(stage["pain_points"])
            all_opportunities.extend(stage["opportunities"])
        
        # 识别关键洞察
        journey["key_insights"] = self._extract_insights(all_pains)
        journey["innovation_opportunities"] = list(set(all_opportunities))
        
        return journey
    
    def _extract_insights(self, pain_points: List[str]) -> List[str]:
        """从痛点中提取洞察"""
        insights = []
        # 简单的关键词提取
        keywords = {}
        for pain in pain_points:
            words = pain.split()
            for word in words:
                if len(word) > 2:
                    keywords[word] = keywords.get(word, 0) + 1
        
        # 取高频关键词作为洞察线索
        sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
        for keyword, count in sorted_keywords[:5]:
            if count > 1:
                insights.append(f"'{keyword}'是反复出现的痛点关键词")
        
        return insights
    
    def to_markdown(self, journey: Dict) -> str:
        """转换为Markdown格式"""
        md = "# 用户旅程图\n\n"
        md += f"创建时间: {journey['created_at']}\n\n"
        
        # 用户画像
        persona = journey.get("user_persona", {})
        md += "## 用户画像\n"
        md += f"- 姓名: {persona.get('name', 'N/A')}\n"
        md += f"- 年龄: {persona.get('age', 'N/A')}\n"
        md += f"- 目标: {persona.get('goals', 'N/A')}\n\n"
        
        # 阶段表格
        md += "## 旅程阶段\n\n"
        md += "| 阶段 | 行为 | 思考 | 情感 | 触点 | 痛点 | 机会 |\n"
        md += "|------|------|------|------|------|------|------|\n"
        
        for stage in journey["stages"]:
            behaviors = "; ".join(stage["behaviors"][:2]) if stage["behaviors"] else ""
            thoughts = "; ".join(stage["thoughts"][:2]) if stage["thoughts"] else ""
            emotions = "; ".join(stage["emotions"][:2]) if stage["emotions"] else ""
            touchpoints = "; ".join(stage["touchpoints"][:2]) if stage["touchpoints"] else ""
            pains = "; ".join(stage["pain_points"][:2]) if stage["pain_points"] else ""
            opportunities = "; ".join(stage["opportunities"][:2]) if stage["opportunities"] else ""
            
            md += f"| {stage['stage']} | {behaviors} | {thoughts} | {emotions} | {touchpoints} | {pains} | {opportunities} |\n"
        
        # 关键洞察
        md += "\n## 关键洞察\n"
        for insight in journey.get("key_insights", []):
            md += f"- {insight}\n"
        
        # 创新机会
        md += "\n## 创新机会\n"
        for opp in journey.get("innovation_opportunities", []):
            md += f"- {opp}\n"
        
        return md


class HMWGenerator:
    """HMW问题生成器"""
    
    def __init__(self):
        self.hmw_templates = [
            "我们如何能够[动词][对象]，以便[情境]？",
            "我们如何能够让[用户]更容易[行为]？",
            "我们如何能够消除[痛点]，同时保持[收益]？",
            "我们如何能够将[负面体验]转化为[正面体验]？",
            "我们如何能够帮助[用户]在[情境]中实现[目标]？"
        ]
    
    def generate_from_pov(self, pov: Dict) -> List[str]:
        """
        从POV陈述生成HMW问题
        
        Args:
            pov: POV陈述字典
        
        Returns:
            HMW问题列表
        """
        hmw_questions = []
        
        user = pov.get("user", "用户")
        need = pov.get("need", "")
        insight = pov.get("insight", "")
        
        # 生成核心HMW
        if need:
            hmw_questions.append(
                f"我们如何能够帮助{user}{need}？"
            )
        
        # 从洞察生成深层HMW
        if insight:
            # 提取洞察中的关键词
            keywords = self._extract_keywords(insight)
            for keyword in keywords:
                hmw_questions.append(
                    f"我们如何能够解决'{keyword}'这一核心挑战？"
                )
        
        # 生成扩展HMW
        hmw_questions.extend(self._generate_extended_hmws(user, need, insight))
        
        return hmw_questions
    
    def _extract_keywords(self, text: str) -> List[str]:
        """提取关键词"""
        # 简单的关键词提取
        words = text.split()
        keywords = [w for w in words if len(w) > 2 and not w in ["因为", "所以", "但是", "然而"]]
        return keywords[:5]
    
    def _generate_extended_hmws(self, user: str, need: str, insight: str) -> List[str]:
        """生成扩展HMW问题"""
        extended = []
        
        # 极端用户角度
        extended.append(f"如果{user}有无限资源，我们如何能够帮助他们{need}？")
        
        # 时间角度
        extended.append(f"我们如何能够在最短时间内帮助{user}{need}？")
        
        # 成本角度
        extended.append(f"我们如何能够以零成本帮助{user}{need}？")
        
        # 情感角度
        extended.append(f"我们如何能够让{user}在{need}时感到快乐？")
        
        return extended
    
    def to_markdown(self, hmw_questions: List[str]) -> str:
        """转换为Markdown格式"""
        md = "# HMW问题列表\n\n"
        
        md += "## 核心HMW问题\n"
        for i, hmw in enumerate(hmw_questions[:5], 1):
            md += f"{i}. {hmw}\n"
        
        if len(hmw_questions) > 5:
            md += "\n## 扩展HMW问题\n"
            for i, hmw in enumerate(hmw_questions[5:], 6):
                md += f"{i}. {hmw}\n"
        
        return md


class IdeaClusterAnalyzer:
    """创意聚类分析器"""
    
    def __init__(self):
        self.clusters = {}
    
    def add_idea(self, idea: str, category: str = None):
        """添加创意想法"""
        if category:
            if category not in self.clusters:
                self.clusters[category] = []
            self.clusters[category].append(idea)
        else:
            # 自动分类
            auto_category = self._auto_categorize(idea)
            if auto_category not in self.clusters:
                self.clusters[auto_category] = []
            self.clusters[auto_category].append(idea)
    
    def _auto_categorize(self, idea: str) -> str:
        """自动分类创意"""
        categories = {
            "功能创新": ["增加", "添加", "新功能", "智能", "自动"],
            "体验优化": ["更简单", "更方便", "更快", "更容易", "改善"],
            "视觉设计": ["颜色", "形状", "外观", "界面", "布局"],
            "技术方案": ["AI", "算法", "数据", "云计算", "物联网"],
            "商业模式": ["收费", "订阅", "免费", "会员", "增值"]
        }
        
        for category, keywords in categories.items():
            for keyword in keywords:
                if keyword in idea:
                    return category
        
        return "其他"
    
    def analyze(self) -> Dict:
        """分析创意分布"""
        total_ideas = sum(len(ideas) for ideas in self.clusters.values())
        
        analysis = {
            "total_ideas": total_ideas,
            "cluster_count": len(self.clusters),
            "clusters": {},
            "recommendations": []
        }
        
        for category, ideas in self.clusters.items():
            analysis["clusters"][category] = {
                "count": len(ideas),
                "percentage": round(len(ideas) / total_ideas * 100, 1) if total_ideas > 0 else 0,
                "ideas": ideas
            }
        
        # 生成建议
        if total_ideas < 50:
            analysis["recommendations"].append("创意数量不足50个，建议继续发散")
        
        if len(self.clusters) < 3:
            analysis["recommendations"].append("创意类型单一，建议尝试不同角度")
        
        max_cluster = max(analysis["clusters"].items(), key=lambda x: x[1]["count"])
        if max_cluster[1]["percentage"] > 50:
            analysis["recommendations"].append(f"'{max_cluster[0]}'类创意占比过高，建议拓展其他方向")
        
        return analysis
    
    def to_markdown(self, analysis: Dict) -> str:
        """转换为Markdown格式"""
        md = "# 创意聚类分析\n\n"
        md += f"**总创意数**: {analysis['total_ideas']}\n"
        md += f"**聚类数**: {analysis['cluster_count']}\n\n"
        
        md += "## 聚类分布\n\n"
        md += "| 类别 | 数量 | 占比 |\n"
        md += "|------|------|------|\n"
        
        for category, data in analysis["clusters"].items():
            md += f"| {category} | {data['count']} | {data['percentage']}% |\n"
        
        if analysis["recommendations"]:
            md += "\n## 建议\n"
            for rec in analysis["recommendations"]:
                md += f"- {rec}\n"
        
        return md


class PrototypeRecommender:
    """原型类型推荐器"""
    
    def __init__(self):
        self.prototype_types = {
            "storyboard": {
                "name": "故事板原型",
                "cost": "低",
                "fidelity": "低",
                "time": "1-2小时",
                "best_for": ["概念验证", "用户流程展示", "场景描述"]
            },
            "paper": {
                "name": "纸面原型",
                "cost": "低",
                "fidelity": "低",
                "time": "2-4小时",
                "best_for": ["交互流程验证", "界面布局", "快速迭代"]
            },
            "roleplay": {
                "name": "角色扮演",
                "cost": "低",
                "fidelity": "中",
                "time": "2-4小时",
                "best_for": ["服务流程验证", "人际交互", "流程优化"]
            },
            "wireframe": {
                "name": "数字线框",
                "cost": "中",
                "fidelity": "中",
                "time": "1-2天",
                "best_for": ["界面设计验证", "交互细节", "可用性测试"]
            },
            "functional": {
                "name": "功能原型",
                "cost": "高",
                "fidelity": "高",
                "time": "1-2周",
                "best_for": ["可用性测试", "技术验证", "用户接受度测试"]
            }
        }
    
    def recommend(self, context: Dict) -> List[Dict]:
        """
        推荐原型类型
        
        Args:
            context: 项目上下文
        
        Returns:
            推荐的原型类型列表
        """
        recommendations = []
        
        time_constraint = context.get("time_constraint", "medium")  # short/medium/long
        budget = context.get("budget", "medium")  # low/medium/high
        test_goal = context.get("test_goal", "")  # 验证目标
        
        for ptype, info in self.prototype_types.items():
            score = 0
            
            # 时间匹配
            if time_constraint == "short" and info["cost"] == "低":
                score += 3
            elif time_constraint == "medium" and info["cost"] in ["低", "中"]:
                score += 2
            elif time_constraint == "long":
                score += 1
            
            # 预算匹配
            if budget == "low" and info["cost"] == "低":
                score += 3
            elif budget == "medium" and info["cost"] in ["低", "中"]:
                score += 2
            elif budget == "high":
                score += 1
            
            # 目标匹配
            if test_goal and test_goal in str(info["best_for"]):
                score += 2
            
            recommendations.append({
                "type": ptype,
                "info": info,
                "score": score
            })
        
        # 按分数排序
        recommendations.sort(key=lambda x: x["score"], reverse=True)
        
        return recommendations[:3]
    
    def to_markdown(self, recommendations: List[Dict]) -> str:
        """转换为Markdown格式"""
        md = "# 原型类型推荐\n\n"
        
        for i, rec in enumerate(recommendations, 1):
            info = rec["info"]
            md += f"## 推荐{i}: {info['name']} (评分: {rec['score']})\n\n"
            md += f"- **成本**: {info['cost']}\n"
            md += f"- **保真度**: {info['fidelity']}\n"
            md += f"- **制作时间**: {info['time']}\n"
            md += f"- **最适用场景**: {', '.join(info['best_for'])}\n\n"
        
        return md


class FeedbackAnalyzer:
    """测试反馈分析器"""
    
    def __init__(self):
        self.feedbacks = []
    
    def add_feedback(self, user_id: str, feedback_type: str, 
                     content: str, severity: str = "medium"):
        """添加反馈"""
        self.feedbacks.append({
            "user_id": user_id,
            "type": feedback_type,  # positive/negative/neutral
            "content": content,
            "severity": severity,   # critical/major/minor
            "timestamp": datetime.now().isoformat()
        })
    
    def analyze(self) -> Dict:
        """分析反馈"""
        analysis = {
            "total_feedbacks": len(self.feedbacks),
            "by_type": {},
            "by_severity": {},
            "issues": [],
            "positive_points": [],
            "recommendations": []
        }
        
        # 按类型统计
        for fb in self.feedbacks:
            fb_type = fb["type"]
            analysis["by_type"][fb_type] = analysis["by_type"].get(fb_type, 0) + 1
            
            severity = fb["severity"]
            analysis["by_severity"][severity] = analysis["by_severity"].get(severity, 0) + 1
            
            if fb_type == "negative":
                analysis["issues"].append(fb["content"])
            elif fb_type == "positive":
                analysis["positive_points"].append(fb["content"])
        
        # 计算负面反馈比例
        total = len(self.feedbacks)
        if total > 0:
            negative_ratio = analysis["by_type"].get("negative", 0) / total
            if negative_ratio > 0.5:
                analysis["recommendations"].append(
                    f"负面反馈比例过高({negative_ratio:.1%})，建议重新评估设计方向"
                )
            
            critical_count = analysis["by_severity"].get("critical", 0)
            if critical_count > 0:
                analysis["recommendations"].append(
                    f"发现{critical_count}个严重问题，需优先解决"
                )
        
        return analysis
    
    def to_markdown(self, analysis: Dict) -> str:
        """转换为Markdown格式"""
        md = "# 测试反馈分析\n\n"
        md += f"**总反馈数**: {analysis['total_feedbacks']}\n\n"
        
        md += "## 反馈类型分布\n"
        for fb_type, count in analysis["by_type"].items():
            md += f"- {fb_type}: {count}\n"
        
        md += "\n## 问题严重程度\n"
        for severity, count in analysis["by_severity"].items():
            md += f"- {severity}: {count}\n"
        
        if analysis["issues"]:
            md += "\n## 发现的问题\n"
            for issue in analysis["issues"]:
                md += f"- {issue}\n"
        
        if analysis["positive_points"]:
            md += "\n## 正面反馈\n"
            for point in analysis["positive_points"]:
                md += f"- {point}\n"
        
        if analysis["recommendations"]:
            md += "\n## 迭代建议\n"
            for rec in analysis["recommendations"]:
                md += f"- {rec}\n"
        
        return md


def main():
    """主函数 - 演示用法"""
    print("设计思维分析工具 v5.0.0-cli-native+agent")
    print("=" * 50)
    
    # 创建测试数据
    test_interview = {
        "quotes": ["我不想刷牙", "这个牙刷太小了"],
        "thoughts": ["为什么要刷牙？", "我想快点结束"],
        "behaviors": ["用拳头握牙刷", "粗鲁地来回刷"],
        "emotions": ["无聊", "挫败"],
        "pain_points": ["刷牙不舒服", "牙刷难以控制"],
        "desired_outcomes": ["快速完成", "不受伤"]
    }
    
    # 测试同理心地图生成
    generator = EmpathyMapGenerator()
    empathy_map = generator.generate("测试用户", test_interview)
    print("\n同理心地图生成成功:")
    print(generator.to_markdown(empathy_map)[:500] + "...")
    
    # 测试HMW生成
    hmw_gen = HMWGenerator()
    pov = {
        "user": "儿童",
        "need": "更容易地刷牙",
        "insight": "他们用拳头握牙刷，而不是用手指"
    }
    hmw_questions = hmw_gen.generate_from_pov(pov)
    print("\nHMW问题生成成功:")
    for hmw in hmw_questions[:3]:
        print(f"- {hmw}")


if __name__ == "__main__":
    main()