# CLI匹配器

import subprocess
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from .intent_classifier import CLIIntentClassifier


class CLIMatcher:
    """CLI匹配器 - 执行实际的CLI调用"""
    
    def __init__(self):
        self.intent_classifier = CLIIntentClassifier()
    
    def execute_intent(self, user_input: str) -> Dict[str, Any]:
        """根据用户输入执行相应的CLI命令"""
        # 首先进行意图分类
        recommendations = self.intent_classifier.get_recommendations(user_input)
        primary = recommendations["primary_recommendation"]
        
        # 执行推荐的命令
        command = primary["command_suggestion"]
        
        result = {
            "command_executed": command,
            "cli_tool": primary["cli_tool"],
            "skills_used": primary["skills"],
            "execution_result": None,
            "error": None
        }
        
        try:
            # 解析命令
            command_parts = self._parse_command(command)
            
            # 执行命令
            execution_result = self._execute_command(command_parts)
            result["execution_result"] = execution_result
            
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _parse_command(self, command: str) -> List[str]:
        """解析命令字符串为参数列表"""
        import shlex
        try:
            # 使用shlex安全地分割命令
            parts = shlex.split(command)
            return parts
        except Exception:
            # 如果shlex失败，使用简单的分割
            return command.split()
    
    def _execute_command(self, command_parts: List[str]) -> Dict[str, Any]:
        """执行命令并返回结果"""
        try:
            # 执行命令
            result = subprocess.run(
                command_parts,
                capture_output=True,
                text=True,
                timeout=30  # 30秒超时
            )
            
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "command": " ".join(command_parts)
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": "Command timed out after 30 seconds",
                "command": " ".join(command_parts)
            }
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "command": " ".join(command_parts)
            }
    
    def get_execution_plan(self, user_input: str) -> Dict[str, Any]:
        """获取执行计划但不实际执行"""
        recommendations = self.intent_classifier.get_recommendations(user_input)
        
        return {
            "user_input": user_input,
            "primary_recommendation": recommendations["primary_recommendation"],
            "alternatives": recommendations["alternative_recommendations"],
            "confidence": recommendations["confidence_score"],
            "explanation": recommendations["explanation"]
        }
    
    def validate_command(self, command: str) -> Dict[str, Any]:
        """验证命令是否有效"""
        result = {
            "valid": False,
            "error": None,
            "suggestions": []
        }
        
        try:
            # 尝试解析命令
            command_parts = self._parse_command(command)
            
            if not command_parts:
                result["error"] = "Empty command"
                return result
            
            # 检查CLI工具是否存在
            cli_tool = command_parts[0]
            if self._cli_tool_exists(cli_tool):
                result["valid"] = True
            else:
                result["error"] = f"CLI tool '{cli_tool}' not found"
                # 提供可能的建议
                result["suggestions"] = self._get_tool_suggestions(cli_tool)
        
        except Exception as e:
            result["error"] = str(e)
        
        return result
    
    def _cli_tool_exists(self, tool_name: str) -> bool:
        """检查CLI工具是否存在"""
        try:
            # 尝试运行 --help 来检查工具是否存在
            result = subprocess.run([tool_name, "--help"], 
                                  capture_output=True, timeout=5)
            return result.returncode in [0, 1]  # 有些工具在没有参数时返回1
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
    
    def _get_tool_suggestions(self, tool_name: str) -> List[str]:
        """获取工具名称建议"""
        available_tools = list(self.intent_classifier.cli_info.get("cli_tools", {}).keys())
        
        # 简单的模糊匹配
        suggestions = []
        for tool in available_tools:
            if tool_name.lower() in tool.lower() or tool.lower() in tool_name.lower():
                suggestions.append(tool)
        
        return suggestions[:3]  # 返回前3个建议
    
    def execute_with_fallback(self, user_input: str) -> Dict[str, Any]:
        """执行命令，如果失败则尝试备选方案"""
        recommendations = self.intent_classifier.get_recommendations(user_input)
        primary = recommendations["primary_recommendation"]
        
        # 首先尝试主要推荐
        result = self._execute_with_command(primary["command_suggestion"])
        
        # 如果失败，尝试备选方案
        if result["error"] or (result["execution_result"] and result["execution_result"]["returncode"] != 0):
            for alt in recommendations["alternative_recommendations"]:
                alt_result = self._execute_with_command(alt["command_suggestion"])
                
                # 如果备选方案成功，使用它
                if not alt_result["error"] and alt_result["execution_result"]["returncode"] == 0:
                    result = alt_result
                    break
        
        return result
    
    def _execute_with_command(self, command: str) -> Dict[str, Any]:
        """使用特定命令执行"""
        result = {
            "command_executed": command,
            "execution_result": None,
            "error": None
        }
        
        try:
            command_parts = self._parse_command(command)
            execution_result = self._execute_command(command_parts)
            result["execution_result"] = execution_result
            
        except Exception as e:
            result["error"] = str(e)
        
        return result


def main():
    matcher = CLIMatcher()
    
    test_inputs = [
        "帮我设计一个按钮组件",
        "写一份项目文档",
        "帮我调试这段代码"
    ]
    
    for user_input in test_inputs:
        print(f"\n用户输入: {user_input}")
        
        # 获取执行计划
        plan = matcher.get_execution_plan(user_input)
        print(f"推荐工具: {plan['primary_recommendation']['cli_tool']}")
        print(f"推荐命令: {plan['primary_recommendation']['command_suggestion']}")
        print(f"置信度: {plan['confidence']:.2f}")
        
        # 尝试执行（注意：实际执行可能会有风险，这里只显示计划）
        print("执行计划已生成，实际执行已跳过以确保安全")


if __name__ == "__main__":
    main()