import numpy as np
from typing import Dict, List, Optional, Tuple
from .satisfaction_tracker import SatisfactionTracker


class SatisfactionBasedResponseAdjuster:
    """
    根据用户满意度数据调整CLI意图匹配响应的系统
    """
    
    def __init__(self, classifier, tracker):
        self.classifier = classifier
        self.tracker = tracker
    
    def adjust_recommendations_by_satisfaction(self, user_input: str, original_recommendations: Dict) -> Dict:
        """
        根据历史满意度数据调整推荐结果
        """
        # 获取用户的满意度历史
        user_satisfaction_history = self._get_user_satisfaction_history(user_input)
        
        # 如果用户历史满意度较低，提供更多替代方案
        if user_satisfaction_history["avg_satisfaction"] < 3.0:
            # 增加替代推荐的数量和多样性
            alternative_recommendations = self._generate_enhanced_alternatives(
                user_input, 
                original_recommendations["primary_recommendation"]["cli_tool"]
            )
            original_recommendations["alternative_recommendations"] = alternative_recommendations
        
        # 根据满意度调整置信度阈值
        adjusted_recommendations = self._adjust_by_satisfaction_patterns(
            user_input, 
            original_recommendations, 
            user_satisfaction_history
        )
        
        return adjusted_recommendations
    
    def _get_user_satisfaction_history(self, user_input: str) -> Dict:
        """
        获取用户满意度历史数据
        """
        feedback_data = self.tracker.feedback_data
        if not feedback_data:
            return {
                "avg_satisfaction": 3.0,  # 默认中性分数
                "total_feedback": 0,
                "satisfaction_trend": 0.0
            }
        
        total_score = sum(f["satisfaction_score"] for f in feedback_data)
        avg_satisfaction = total_score / len(feedback_data)
        
        # 计算满意度趋势（最近的反馈与早期反馈的比较）
        recent_count = min(5, len(feedback_data))
        if recent_count > 0:
            recent_feedback = feedback_data[-recent_count:]
            recent_avg = sum(f["satisfaction_score"] for f in recent_feedback) / len(recent_feedback)
            
            early_count = min(5, len(feedback_data) - recent_count)
            if early_count > 0:
                early_feedback = feedback_data[:early_count]
                early_avg = sum(f["satisfaction_score"] for f in early_feedback) / len(early_feedback)
                trend = recent_avg - early_avg
            else:
                trend = 0.0
        else:
            trend = 0.0
        
        return {
            "avg_satisfaction": avg_satisfaction,
            "total_feedback": len(feedback_data),
            "satisfaction_trend": trend
        }
    
    def _generate_enhanced_alternatives(self, user_input: str, primary_tool: str) -> List[Dict]:
        """
        生成增强的替代推荐
        """
        alternatives = []
        
        # 获取所有可用的CLI工具
        all_tools = list(self.classifier.cli_info.get("cli_tools", {}).keys())
        if primary_tool in all_tools:
            all_tools.remove(primary_tool)
        
        # 为每个工具生成建议，增加更多样化的参数
        for tool in all_tools[:5]:  # 取前5个替代方案
            # 生成更具体的命令建议
            command_suggestion = self._generate_specific_command_suggestion(user_input, tool)
            
            alternatives.append({
                "cli_tool": tool,
                "confidence": 0.4,  # 降低置信度，因为这是替代方案
                "command_suggestion": command_suggestion,
                "reason": "Enhanced alternative due to low user satisfaction"
            })
        
        return alternatives
    
    def _generate_specific_command_suggestion(self, user_input: str, cli_tool: str) -> str:
        """
        生成更具体的命令建议
        """
        # 根据用户输入的类型生成更合适的命令
        user_lower = user_input.lower()
        
        # 检查是否涉及特定技能
        matched_skills = self.classifier._match_skills(user_input)
        
        if matched_skills:
            skill = matched_skills[0]
            if cli_tool == "stigmergy":
                return f"stigmergy call skill {skill} \"{user_input}\" --verbose"
            else:
                return f"stigmergy use {cli_tool} skill {skill} \"{user_input}\" --detailed"
        else:
            # 为不同类型的请求生成特定参数
            if any(keyword in user_lower for keyword in ["debug", "troubleshoot", "fix", "error"]):
                return f"{cli_tool} \"{user_input}\" --debug --verbose"
            elif any(keyword in user_lower for keyword in ["write", "create", "document", "report"]):
                return f"{cli_tool} \"{user_input}\" --format markdown --output detailed"
            elif any(keyword in user_lower for keyword in ["analyze", "research", "study", "review"]):
                return f"{cli_tool} \"{user_input}\" --research --comprehensive"
            else:
                # 默认命令
                default_params = self.classifier._get_default_params(cli_tool)
                params_str = " ".join(default_params) if default_params else "--print --detailed"
                return f"{cli_tool} \"{user_input}\" {params_str}"
    
    def _adjust_by_satisfaction_patterns(self, user_input: str, original_recommendations: Dict, 
                                       user_satisfaction_history: Dict) -> Dict:
        """
        根据满意度模式调整推荐
        """
        # 如果最近满意度下降，提供更多的解释
        if user_satisfaction_history["satisfaction_trend"] < -0.5:
            explanation = original_recommendations.get("explanation", "")
            original_recommendations["explanation"] = explanation + " (根据您的反馈，我们提供了更详细的选项)"
            # 增加置信度的不确定性说明
            original_recommendations["confidence_explanation"] = (
                "由于近期反馈显示需要改进，此建议的置信度较低，提供更多替代方案供参考"
            )
        
        # 如果用户满意度很高，可以更自信地推荐
        if user_satisfaction_history["avg_satisfaction"] > 4.0:
            primary_rec = original_recommendations.get("primary_recommendation", {})
            if "confidence" in primary_rec:
                primary_rec["confidence"] = min(1.0, primary_rec["confidence"] + 0.1)
            explanation = original_recommendations.get("explanation", "")
            original_recommendations["explanation"] = explanation + " (基于您的高满意度历史)"
        
        return original_recommendations


class AdaptiveResponseSystem:
    """
    自适应响应系统，根据满意度数据动态调整响应
    """
    
    def __init__(self, classifier):
        self.classifier = classifier
        self.adjuster = SatisfactionBasedResponseAdjuster(classifier, classifier.satisfaction_tracker)
    
    def get_adaptive_recommendations(self, user_input: str) -> Dict:
        """
        获取自适应推荐结果
        """
        # 获取原始推荐
        original_recommendations = self.classifier.get_base_recommendations(user_input)
        
        # 根据满意度历史调整推荐
        adjusted_recommendations = self.adjuster.adjust_recommendations_by_satisfaction(
            user_input, 
            original_recommendations
        )
        
        return adjusted_recommendations
    
    def update_model_based_on_satisfaction(self):
        """
        根据满意度数据更新模型（简化版本）
        """
        feedback_data = self.classifier.satisfaction_tracker.feedback_data
        
        if not feedback_data:
            return False
        
        # 统计低满意度的模式
        low_satisfaction_feedback = [f for f in feedback_data if f["satisfaction_score"] <= 2]
        
        if len(low_satisfaction_feedback) > 0:
            print(f"发现 {len(low_satisfaction_feedback)} 个低满意度反馈，可考虑重新训练模型")
            # 在实际实现中，这里可以触发模型的重新训练或微调
            return True
        
        return False