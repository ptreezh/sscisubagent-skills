#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Action Research Problem Diagnoser
行动研究问题诊断工具

使用方法:
    python problem_diagnoser.py --interviews "访谈数据..."
    python problem_diagnoser.py --observations "观察数据..."
    python problem_diagnoser.py --documents "文档数据..."
    python problem_diagnoser.py --analyze
"""

import json
import re
from typing import Dict, List, Optional, Tuple
from collections import Counter
from dataclasses import dataclass, field
import argparse


@dataclass
class ProblemDiagnosis:
    """问题诊断结果"""
    symptoms: List[str] = field(default_factory=list)
    root_causes: List[str] = field(default_factory=list)
    stakeholders: Dict[str, Dict] = field(default_factory=dict)
    impact_assessment: Dict = field(default_factory=dict)
    priority_issues: List[Tuple[str, int]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


class ProblemDiagnoser:
    """行动研究问题诊断器"""
    
    def __init__(self):
        self.data = {
            "interviews": [],
            "observations": [],
            "documents": [],
            "surveys": []
        }
        self.diagnosis = ProblemDiagnosis()
    
    def add_interview_data(self, content: str, interviewee: str = ""):
        """添加访谈数据"""
        self.data["interviews"].append({
            "content": content,
            "interviewee": interviewee,
            "word_count": len(content)
        })
    
    def add_observation_data(self, content: str, location: str = "", date: str = ""):
        """添加观察数据"""
        self.data["observations"].append({
            "content": content,
            "location": location,
            "date": date
        })
    
    def add_document_data(self, content: str, doc_type: str = "", source: str = ""):
        """添加文档数据"""
        self.data["documents"].append({
            "content": content,
            "doc_type": doc_type,
            "source": source
        })
    
    def analyze_symptoms(self) -> List[str]:
        """分析问题症状"""
        # 问题关键词模式
        problem_patterns = [
            r"问题[是为：:]\s*([^.。!?]+)",
            r"困难[是为：:]\s*([^.。!?]+)",
            r"挑战[是为：:]\s*([^.。!?]+)",
            r"障碍[是为：:]\s*([^.。!?]+)",
            r"不足[是为：:]\s*([^.。!?]+)",
            r"缺乏\s*([^.。!?]+)",
            r"难以\s*([^.。!?]+)",
            r"无法\s*([^.。!?]+)",
            r"不能\s*([^.。!?]+)"
        ]
        
        symptoms = []
        all_text = self._get_all_text()
        
        for pattern in problem_patterns:
            matches = re.findall(pattern, all_text)
            symptoms.extend(matches)
        
        # 去重并统计频率
        symptom_counts = Counter(symptoms)
        self.diagnosis.symptoms = [s for s, _ in symptom_counts.most_common(10)]
        
        return self.diagnosis.symptoms
    
    def analyze_root_causes(self) -> List[str]:
        """分析根本原因（使用5Why方法）"""
        causes = []
        all_text = self._get_all_text()
        
        # 原因关键词模式
        cause_patterns = [
            r"因为\s*([^.。!?]+)",
            r"由于\s*([^.。!?]+)",
            r"原因[是为：:]\s*([^.。!?]+)",
            r"导致\s*([^.。!?]+)",
            r"根源[是为：:]\s*([^.。!?]+)"
        ]
        
        for pattern in cause_patterns:
            matches = re.findall(pattern, all_text)
            causes.extend(matches)
        
        # 去重
        unique_causes = list(set(causes))
        
        # 使用启发式规则进行5Why深挖
        root_causes = []
        for cause in unique_causes[:5]:
            root_causes.append({
                "surface_cause": cause,
                "depth_1": f"为什么{cause}？",
                "analysis": f"需要进一步调查{cause}的深层原因"
            })
        
        self.diagnosis.root_causes = unique_causes[:10]
        return self.diagnosis.root_causes
    
    def analyze_stakeholders(self) -> Dict[str, Dict]:
        """分析利益相关者"""
        all_text = self._get_all_text()
        
        # 识别利益相关者类型
        stakeholder_types = {
            "管理层": ["经理", "主管", "领导", "管理者", "主任"],
            "员工": ["员工", "职员", "工作人员", "同事"],
            "客户": ["客户", "用户", "顾客", "消费者"],
            "合作方": ["供应商", "合作伙伴", "协作单位"]
        }
        
        stakeholders = {}
        for stype, keywords in stakeholder_types.items():
            count = sum(all_text.count(kw) for kw in keywords)
            if count > 0:
                stakeholders[stype] = {
                    "mention_count": count,
                    "likely_interest": self._infer_interest(stype),
                    "influence_level": self._assess_influence(stype, all_text),
                    "engagement_strategy": self._suggest_engagement(stype)
                }
        
        self.diagnosis.stakeholders = stakeholders
        return stakeholders
    
    def _infer_interest(self, stakeholder_type: str) -> str:
        """推断利益关切"""
        interests = {
            "管理层": "效率提升、成本控制、绩效改善",
            "员工": "工作条件、职业发展、工作满意度",
            "客户": "服务质量、产品体验、响应速度",
            "合作方": "合作效率、利益分配、沟通顺畅"
        }
        return interests.get(stakeholder_type, "待分析")
    
    def _assess_influence(self, stakeholder_type: str, text: str) -> str:
        """评估影响力"""
        # 简化评估逻辑
        high_influence_keywords = ["决策", "资源", "权力", "支持"]
        medium_influence_keywords = ["参与", "配合", "协作"]
        
        score = 0
        for kw in high_influence_keywords:
            score += text.count(kw) * 2
        for kw in medium_influence_keywords:
            score += text.count(kw)
        
        if score > 10:
            return "高"
        elif score > 5:
            return "中"
        else:
            return "低"
    
    def _suggest_engagement(self, stakeholder_type: str) -> str:
        """建议参与策略"""
        strategies = {
            "管理层": "定期汇报、邀请参与关键决策、展示成果",
            "员工": "建立反馈渠道、参与式设计、能力建设",
            "客户": "需求调研、体验测试、满意度评估",
            "合作方": "协调会议、利益共享机制、定期沟通"
        }
        return strategies.get(stakeholder_type, "建立沟通渠道")
    
    def assess_impact(self) -> Dict:
        """评估问题影响"""
        all_text = self._get_all_text()
        
        impact_areas = {
            "效率影响": ["效率", "时间", "进度", "延误"],
            "质量影响": ["质量", "错误", "缺陷", "问题"],
            "成本影响": ["成本", "费用", "资源", "预算"],
            "人员影响": ["员工", "满意度", "离职", "士气"],
            "客户影响": ["客户", "满意度", "投诉", "反馈"]
        }
        
        impact_assessment = {}
        for area, keywords in impact_areas.items():
            score = sum(all_text.count(kw) for kw in keywords)
            impact_assessment[area] = {
                "mention_score": score,
                "severity": "高" if score > 10 else "中" if score > 5 else "低"
            }
        
        self.diagnosis.impact_assessment = impact_assessment
        return impact_assessment
    
    def prioritize_issues(self) -> List[Tuple[str, int]]:
        """问题优先级排序"""
        # 基于症状频率和影响严重度计算优先级
        priorities = []
        
        for symptom in self.diagnosis.symptoms[:5]:
            score = 0
            # 症状频率
            score += self._get_all_text().count(symptom) * 2
            
            # 影响严重度
            for area, data in self.diagnosis.impact_assessment.items():
                if data["severity"] == "高":
                    score += 3
                elif data["severity"] == "中":
                    score += 1
            
            priorities.append((symptom, score))
        
        priorities.sort(key=lambda x: x[1], reverse=True)
        self.diagnosis.priority_issues = priorities
        return priorities
    
    def generate_recommendations(self) -> List[str]:
        """生成诊断建议"""
        recommendations = []
        
        # 基于优先问题生成建议
        if self.diagnosis.priority_issues:
            top_issue = self.diagnosis.priority_issues[0][0]
            recommendations.append(f"建议优先关注: {top_issue}")
        
        # 基于利益相关者分析
        high_influence = [k for k, v in self.diagnosis.stakeholders.items() 
                         if v["influence_level"] == "高"]
        if high_influence:
            recommendations.append(f"关键利益相关者: {', '.join(high_influence)}，需重点沟通")
        
        # 基于影响评估
        high_impact = [k for k, v in self.diagnosis.impact_assessment.items() 
                      if v["severity"] == "高"]
        if high_impact:
            recommendations.append(f"主要影响领域: {', '.join(high_impact)}")
        
        # 通用建议
        recommendations.extend([
            "建议收集更多数据以深入理解问题根源",
            "建议在规划阶段纳入关键利益相关者",
            "建议设定明确的基线指标以便评估"
        ])
        
        self.diagnosis.recommendations = recommendations
        return recommendations
    
    def _get_all_text(self) -> str:
        """获取所有文本数据"""
        all_text = []
        for data_list in self.data.values():
            for item in data_list:
                all_text.append(item.get("content", ""))
        return " ".join(all_text)
    
    def run_full_diagnosis(self) -> Dict:
        """运行完整诊断"""
        self.analyze_symptoms()
        self.analyze_root_causes()
        self.analyze_stakeholders()
        self.assess_impact()
        self.prioritize_issues()
        self.generate_recommendations()
        
        return {
            "symptoms": self.diagnosis.symptoms,
            "root_causes": self.diagnosis.root_causes,
            "stakeholders": self.diagnosis.stakeholders,
            "impact_assessment": self.diagnosis.impact_assessment,
            "priority_issues": self.diagnosis.priority_issues,
            "recommendations": self.diagnosis.recommendations
        }
    
    def generate_report(self) -> str:
        """生成诊断报告"""
        report = f"""# 行动研究问题诊断报告

## 一、问题症状

"""
        for i, symptom in enumerate(self.diagnosis.symptoms, 1):
            report += f"{i}. {symptom}\n"
        
        report += f"""
## 二、根本原因分析

"""
        for i, cause in enumerate(self.diagnosis.root_causes[:5], 1):
            report += f"{i}. {cause}\n"
        
        report += f"""
## 三、利益相关者分析

| 利益相关者 | 提及次数 | 影响力 | 利益关切 | 参与策略 |
|-----------|----------|--------|----------|----------|
"""
        for stype, data in self.diagnosis.stakeholders.items():
            report += f"| {stype} | {data['mention_count']} | {data['influence_level']} | {data['likely_interest']} | {data['engagement_strategy']} |\n"
        
        report += f"""
## 四、影响评估

| 影响领域 | 严重程度 |
|----------|----------|
"""
        for area, data in self.diagnosis.impact_assessment.items():
            report += f"| {area} | {data['severity']} |\n"
        
        report += f"""
## 五、问题优先级

"""
        for i, (issue, score) in enumerate(self.diagnosis.priority_issues[:5], 1):
            report += f"{i}. {issue} (优先级分数: {score})\n"
        
        report += f"""
## 六、诊断建议

"""
        for i, rec in enumerate(self.diagnosis.recommendations, 1):
            report += f"{i}. {rec}\n"
        
        return report


def main():
    parser = argparse.ArgumentParser(description="行动研究问题诊断器")
    
    parser.add_argument("--interviews", type=str, help="访谈数据")
    parser.add_argument("--observations", type=str, help="观察数据")
    parser.add_argument("--documents", type=str, help="文档数据")
    parser.add_argument("--analyze", action="store_true", help="运行完整分析")
    parser.add_argument("--report", action="store_true", help="生成诊断报告")
    parser.add_argument("--output", type=str, default="diagnosis_report.md", help="报告输出路径")
    
    args = parser.parse_args()
    
    diagnoser = ProblemDiagnoser()
    
    if args.interviews:
        diagnoser.add_interview_data(args.interviews)
    
    if args.observations:
        diagnoser.add_observation_data(args.observations)
    
    if args.documents:
        diagnoser.add_document_data(args.documents)
    
    if args.analyze:
        result = diagnoser.run_full_diagnosis()
        print(json.dumps(result, ensure_ascii=False, indent=2))
    
    if args.report:
        report = diagnoser.generate_report()
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"✅ 诊断报告已生成: {args.output}")


if __name__ == "__main__":
    main()
