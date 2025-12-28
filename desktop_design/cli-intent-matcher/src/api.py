# API接口

from flask import Flask, request, jsonify
from typing import Dict, Any
import sys
import os

# 添加src目录到Python路径
sys.path.append(os.path.join(os.path.dirname(__file__)))

from src.intent_classifier import CLIIntentClassifier
from src.cli_matcher import CLIMatcher
from src.satisfaction_tracker import SatisfactionFeedbackInterface
from src.intelligent_satisfaction_detector import IntelligentSatisfactionDetector


def create_app():
    app = Flask(__name__)
    
    # 初始化组件
    intent_classifier = CLIIntentClassifier()
    cli_matcher = CLIMatcher()
    
    # 初始化满意度跟踪组件
    satisfaction_interface = SatisfactionFeedbackInterface(intent_classifier.satisfaction_tracker)
    satisfaction_detector = IntelligentSatisfactionDetector(intent_classifier.satisfaction_tracker)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        """健康检查端点"""
        return jsonify({
            "status": "healthy",
            "message": "CLI Intent Matcher API is running"
        })
    
    @app.route('/classify', methods=['POST'])
    def classify_intent():
        """分类用户意图"""
        try:
            data = request.get_json()
            user_input = data.get('user_input', '')
            
            if not user_input:
                return jsonify({"error": "user_input is required"}), 400
            
            recommendations = intent_classifier.get_recommendations(user_input)
            
            return jsonify({
                "success": True,
                "data": recommendations
            })
        
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/execute', methods=['POST'])
    def execute_intent():
        """执行用户意图（安全模式，仅返回执行计划）"""
        try:
            data = request.get_json()
            user_input = data.get('user_input', '')
            execute_real = data.get('execute_real', False)
            
            if not user_input:
                return jsonify({"error": "user_input is required"}), 400
            
            if execute_real:
                # 实际执行（需要谨慎使用）
                result = cli_matcher.execute_with_fallback(user_input)
            else:
                # 仅返回执行计划
                result = cli_matcher.get_execution_plan(user_input)
            
            return jsonify({
                "success": True,
                "data": result
            })
        
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/plan', methods=['POST'])
    def get_execution_plan():
        """获取执行计划"""
        try:
            data = request.get_json()
            user_input = data.get('user_input', '')
            
            if not user_input:
                return jsonify({"error": "user_input is required"}), 400
            
            plan = cli_matcher.get_execution_plan(user_input)
            
            return jsonify({
                "success": True,
                "data": plan
            })
        
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/validate', methods=['POST'])
    def validate_command():
        """验证命令"""
        try:
            data = request.get_json()
            command = data.get('command', '')
            
            if not command:
                return jsonify({"error": "command is required"}), 400
            
            validation_result = cli_matcher.validate_command(command)
            
            return jsonify({
                "success": True,
                "data": validation_result
            })
        
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/skills', methods=['GET'])
    def get_skills():
        """获取可用技能列表"""
        try:
            skills = intent_classifier.cli_info.get("skills", {})
            
            return jsonify({
                "success": True,
                "data": {
                    "skills": skills,
                    "count": len(skills)
                }
            })
        
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/cli-tools', methods=['GET'])
    def get_cli_tools():
        """获取可用CLI工具列表"""
        try:
            cli_tools = intent_classifier.cli_info.get("cli_tools", {})
            
            return jsonify({
                "success": True,
                "data": {
                    "cli_tools": cli_tools,
                    "count": len(cli_tools)
                }
            })
        
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/satisfaction/feedback', methods=['POST'])
    def submit_satisfaction_feedback():
        """提交满意度反馈"""
        try:
            data = request.get_json()
            conversation_id = data.get('conversation_id', '')
            satisfaction_score = data.get('satisfaction_score', 0)
            feedback_text = data.get('feedback_text', '')
            
            if not conversation_id:
                return jsonify({"error": "conversation_id is required"}), 400
            
            if satisfaction_score < 1 or satisfaction_score > 5:
                return jsonify({"error": "satisfaction_score must be between 1 and 5"}), 400
            
            # 添加满意度反馈
            intent_classifier.satisfaction_tracker.add_satisfaction_feedback(
                conversation_id, satisfaction_score, feedback_text
            )
            
            return jsonify({
                "success": True,
                "message": "Satisfaction feedback recorded successfully"
            })
        
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/satisfaction/follow-up', methods=['POST'])
    def process_follow_up():
        """处理后续对话并检测满意度"""
        try:
            data = request.get_json()
            conversation_id = data.get('conversation_id', '')
            follow_up_input = data.get('follow_up_input', '')
            
            if not conversation_id or not follow_up_input:
                return jsonify({"error": "conversation_id and follow_up_input are required"}), 400
            
            # 处理后续对话
            intent_classifier.process_follow_up(conversation_id, follow_up_input)
            
            return jsonify({
                "success": True,
                "message": "Follow-up processed successfully"
            })
        
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/satisfaction/insights', methods=['GET'])
    def get_satisfaction_insights():
        """获取满意度洞察"""
        try:
            insights = intent_classifier.get_satisfaction_insights()
            overall_satisfaction = intent_classifier.satisfaction_tracker.calculate_overall_satisfaction()
            
            return jsonify({
                "success": True,
                "data": {
                    "insights": insights,
                    "overall_satisfaction": overall_satisfaction
                }
            })
        
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    @app.route('/satisfaction/conversation/<conversation_id>', methods=['GET'])
    def get_conversation_satisfaction(conversation_id: str):
        """获取特定对话的满意度信息"""
        try:
            feedback = intent_classifier.get_conversation_feedback(conversation_id)
            
            return jsonify({
                "success": True,
                "data": {
                    "conversation_id": conversation_id,
                    "feedback": feedback
                }
            })
        
        except Exception as e:
            return jsonify({
                "success": False,
                "error": str(e)
            }), 500
    
    return app


def main():
    app = create_app()
    
    print("启动CLI Intent Matcher API...")
    print("API将在 http://localhost:5000 上运行")
    print("可用端点:")
    print("  GET  /health - 健康检查")
    print("  POST /classify - 分类用户意图")
    print("  POST /execute - 执行用户意图")
    print("  POST /plan - 获取执行计划")
    print("  POST /validate - 验证命令")
    print("  GET  /skills - 获取可用技能")
    print("  GET  /cli-tools - 获取可用CLI工具")
    
    app.run(debug=True, host='0.0.0.0', port=5000)


if __name__ == "__main__":
    main()