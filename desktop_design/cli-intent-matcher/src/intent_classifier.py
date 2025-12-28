# CLI意图分类器

import joblib
import numpy as np
from pathlib import Path
import json
from typing import Dict, List, Tuple, Optional
import re

from .satisfaction_tracker import SatisfactionTracker, SatisfactionFeedbackInterface
from .intelligent_satisfaction_detector import IntelligentSatisfactionDetector
from .response_adjuster import SatisfactionBasedResponseAdjuster, AdaptiveResponseSystem


class CLIIntentClassifier:
    """CLI意图分类器 - 根据用户输入匹配最合适的CLI工具和参数"""
    
    def __init__(self, model_path: str = "cli-intent-matcher/data/models"):
        self.model_path = model_path
        self.vectorizer = None
        self.classifier = None
        self.metadata = None
        self.cli_info = {}
        
        # Initialize satisfaction tracking
        self.satisfaction_tracker = SatisfactionTracker()
        self.satisfaction_interface = SatisfactionFeedbackInterface(self.satisfaction_tracker)
        self.satisfaction_detector = IntelligentSatisfactionDetector(self.satisfaction_tracker)
        self.adaptive_response_system = AdaptiveResponseSystem(self)
        
        self._load_models()
        self._load_cli_info()
    
    def _load_models(self):
        """加载训练好的模型"""
        try:
            vectorizer_path = f"{self.model_path}/intent_classifier_vectorizer.pkl"
            classifier_path = f"{self.model_path}/intent_classifier_classifier.pkl"
            metadata_path = f"{self.model_path}/intent_classifier_metadata.json"
            
            if Path(vectorizer_path).exists():
                self.vectorizer = joblib.load(vectorizer_path)
            if Path(classifier_path).exists():
                self.classifier = joblib.load(classifier_path)
            if Path(metadata_path).exists():
                with open(metadata_path, 'r') as f:
                    self.metadata = json.load(f)
            
            print("模型加载成功")
        except Exception as e:
            print(f"模型加载失败: {e}")
            # 如果模型不存在，使用规则基础的分类器
            self._init_rule_based_classifier()
    
    def _init_rule_based_classifier(self):
        """初始化基于规则的分类器（当ML模型不可用时）"""
        print("使用基于规则的分类器")
        # 这里可以实现基于关键词匹配的规则
        pass
    
    def _load_cli_info(self):
        """加载CLI工具信息"""
        raw_data_path = Path("cli-intent-matcher/data/raw/cli_info.json")
        if raw_data_path.exists():
            with open(raw_data_path, 'r', encoding='utf-8') as f:
                self.cli_info = json.load(f)
        else:
            # 使用默认的CLI信息
            self.cli_info = {
                "cli_tools": {
                    "claude": {
                        "available": True,
                        "parameters": ["--print", "--model", "--agent", "--tools", "--system-prompt"]
                    },
                    "qwen": {
                        "available": True,
                        "parameters": ["--print", "--model", "--tools"]
                    },
                    "gemini": {
                        "available": True,
                        "parameters": ["--print", "--model", "--tools"]
                    },
                    "codebuddy": {
                        "available": True,
                        "parameters": ["--print", "--model", "--tools"]
                    },
                    "stigmergy": {
                        "available": True,
                        "parameters": ["call", "skill", "use"]
                    }
                },
                "skills": {
                    "frontend-design": {"description": "Create distinctive frontend interfaces"},
                    "docx": {"description": "Document creation and editing"},
                    "pdf": {"description": "PDF manipulation"},
                    "xlsx": {"description": "Spreadsheet operations"}
                }
            }
    
    def classify_intent(self, user_input: str) -> Dict[str, any]:
        """分类用户意图并返回最佳匹配的CLI配置"""
        if self.vectorizer and self.classifier:
            return self._ml_classify_intent(user_input)
        else:
            return self._rule_based_classify_intent(user_input)
    
    def _ml_classify_intent(self, user_input: str) -> Dict[str, any]:
        """使用机器学习模型分类意图"""
        try:
            # 向量化输入
            input_vector = self.vectorizer.transform([user_input])
            
            # 预测
            prediction = self.classifier.predict(input_vector)
            probabilities = self.classifier.predict_proba(input_vector)
            
            # 提取预测结果
            cli_tool = prediction[0][0] if len(prediction[0]) > 0 else "stigmergy"
            
            # 获取置信度
            confidence = max([max(prob) for prob in probabilities]) if probabilities else 0.0
            
            return {
                "cli_tool": cli_tool,
                "confidence": float(confidence),
                "recommended_params": self._get_default_params(cli_tool),
                "skills": self._match_skills(user_input),
                "command_suggestion": self._generate_command_suggestion(user_input, cli_tool)
            }
        except Exception as e:
            print(f"ML分类失败: {e}")
            # 回退到规则基础分类
            return self._rule_based_classify_intent(user_input)
    
    def _rule_based_classify_intent(self, user_input: str) -> Dict[str, any]:
        """基于规则的意图分类"""
        user_lower = user_input.lower()
        
        # 定义关键词映射
        keyword_mapping = {
            "code": ["claude", "codebuddy", "qwen"],
            "design": ["claude", "stigmergy"],  # 用于frontend-design技能
            "document": ["claude", "stigmergy"],  # 用于docx技能
            "pdf": ["stigmergy"],  # 用于pdf技能
            "spreadsheet": ["stigmergy"],  # 用于xlsx技能
            "research": ["gemini", "claude"],
            "debug": ["claude", "codebuddy"],
            "write": ["claude", "qwen"],
            "create": ["claude", "qwen", "stigmergy"],
            "explain": ["claude", "codebuddy"],
            "skill": ["stigmergy"],
            "stigmergy": ["stigmergy"]
        }
        
        # 根据关键词匹配工具
        matched_tools = []
        for keyword, tools in keyword_mapping.items():
            if keyword in user_lower:
                matched_tools.extend(tools)
        
        # 统计最匹配的工具
        if matched_tools:
            from collections import Counter
            tool_counts = Counter(matched_tools)
            primary_tool = tool_counts.most_common(1)[0][0]
        else:
            primary_tool = "stigmergy"  # 默认工具
        
        # 匹配技能
        matched_skills = self._match_skills(user_input)
        
        return {
            "cli_tool": primary_tool,
            "confidence": 0.7,  # 规则匹配的默认置信度
            "recommended_params": self._get_default_params(primary_tool),
            "skills": matched_skills,
            "command_suggestion": self._generate_command_suggestion(user_input, primary_tool, matched_skills)
        }
    
    def _match_skills(self, user_input: str) -> List[str]:
        """匹配相关的技能"""
        user_lower = user_input.lower()
        matched_skills = []
        
        for skill_name, skill_info in self.cli_info.get("skills", {}).items():
            # 检查技能名称和描述是否与用户输入匹配
            if (skill_name.lower() in user_lower or 
                skill_info["description"].lower() in user_lower or
                any(keyword in user_lower for keyword in skill_name.lower().split('-'))):
                matched_skills.append(skill_name)
        
        # 一些常见的技能关键词匹配
        skill_keywords = {
            "frontend-design": ["ui", "interface", "web", "design", "button", "component", "frontend", "html", "css"],
            "docx": ["document", "word", "doc", "format", "write", "edit"],
            "pdf": ["pdf", "extract", "merge", "split", "fill", "form"],
            "xlsx": ["excel", "spreadsheet", "data", "table", "formula", "chart"]
        }
        
        for skill, keywords in skill_keywords.items():
            if any(keyword in user_lower for keyword in keywords):
                if skill not in matched_skills:
                    matched_skills.append(skill)
        
        return matched_skills
    
    def _get_default_params(self, cli_tool: str) -> List[str]:
        """获取CLI工具的默认参数"""
        tool_info = self.cli_info.get("cli_tools", {}).get(cli_tool, {})
        return tool_info.get("parameters", [])
    
    def _generate_command_suggestion(self, user_input: str, cli_tool: str, skills: List[str] = None) -> str:
        """生成命令建议"""
        if skills:
            # 如果匹配到技能，生成使用技能的命令
            skill = skills[0]  # 使用第一个匹配的技能
            if cli_tool == "stigmergy":
                return f"stigmergy call skill {skill} \"{user_input}\""
            else:
                return f"stigmergy use {cli_tool} skill {skill} \"{user_input}\""
        else:
            # 生成普通命令
            if cli_tool == "stigmergy":
                return f"stigmergy call \"{user_input}\""
            else:
                # 为特定CLI工具生成命令
                default_params = self._get_default_params(cli_tool)
                params_str = " ".join(default_params) if default_params else "--print"
                return f"{cli_tool} \"{user_input}\" {params_str}"
    
    def get_base_recommendations(self, user_input: str) -> Dict[str, any]:
        """获取基础推荐结果（不包含满意度调整）"""
        classification = self.classify_intent(user_input)
        
        # Add conversation to satisfaction tracking
        conversation_id = self.satisfaction_tracker.add_conversation(
            user_input=user_input,
            cli_intent=classification["cli_tool"],
            cli_command=classification["command_suggestion"]
        )
        
        result = {
            "primary_recommendation": classification,
            "alternative_recommendations": self._get_alternatives(user_input, classification["cli_tool"]),
            "confidence_score": classification["confidence"],
            "explanation": self._explain_choice(user_input, classification),
            "conversation_id": conversation_id  # Include conversation ID for feedback
        }
        
        return result
    
    def get_recommendations(self, user_input: str) -> Dict[str, any]:
        """获取完整的推荐结果"""
        # Use adaptive recommendations based on satisfaction history
        return self.adaptive_response_system.get_adaptive_recommendations(user_input)
    
    def _get_alternatives(self, user_input: str, primary_tool: str) -> List[Dict[str, any]]:
        """获取替代推荐"""
        alternatives = []
        
        # 获取前几个可能的工具
        all_tools = list(self.cli_info.get("cli_tools", {}).keys())
        if primary_tool in all_tools:
            all_tools.remove(primary_tool)
        
        # 为每个工具生成建议
        for tool in all_tools[:3]:  # 只取前3个替代方案
            alternatives.append({
                "cli_tool": tool,
                "confidence": 0.3,  # 默认置信度
                "command_suggestion": self._generate_command_suggestion(user_input, tool)
            })
        
        return alternatives
    
    def _explain_choice(self, user_input: str, classification: Dict[str, any]) -> str:
        """解释选择该工具的原因"""
        tool = classification["cli_tool"]
        skills = classification["skills"]
        
        explanation = f"选择 {tool} 作为主要工具"
        
        if skills:
            explanation += f"，并使用 {', '.join(skills)} 技能"
        
        return explanation
    
    def process_follow_up(self, original_conversation_id: str, follow_up_input: str):
        """处理后续对话并检测满意度"""
        # Register the follow-up for analysis
        self.satisfaction_detector.register_follow_up(original_conversation_id, follow_up_input)
        
        # Analyze and update satisfaction if possible
        self.satisfaction_detector.analyze_and_update_satisfaction(original_conversation_id)
    
    def get_satisfaction_insights(self) -> Dict:
        """获取满意度洞察"""
        return self.satisfaction_detector.get_satisfaction_insights()
    
    def get_conversation_feedback(self, conversation_id: str) -> Optional[Dict]:
        """获取特定对话的反馈"""
        for conv in self.satisfaction_tracker.conversation_data:
            if conv["id"] == conversation_id:
                return conv.get("feedback")
        return None


def main():
    # 示例使用
    classifier = CLIIntentClassifier()
    
    test_inputs = [
        "帮我设计一个按钮组件",
        "写一份项目文档",
        "帮我调试这段代码",
        "分析这个PDF文件",
        "创建一个Excel表格统计销售数据"
    ]
    
    for user_input in test_inputs:
        print(f"\n用户输入: {user_input}")
        result = classifier.get_recommendations(user_input)
        print(f"推荐工具: {result['primary_recommendation']['cli_tool']}")
        print(f"推荐命令: {result['primary_recommendation']['command_suggestion']}")
        print(f"置信度: {result['confidence_score']:.2f}")
        print(f"解释: {result['explanation']}")


if __name__ == "__main__":
    main()