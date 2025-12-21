#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Web界面AI集成模块
连接Web界面与大模型API
"""

import os
import json
import subprocess
import requests
from pathlib import Path
from typing import Dict, Optional

class AIIntegration:
    """AI集成管理器"""
    
    def __init__(self):
        self.skills_dir = Path(__file__).parent.parent / "skills"
        self.iflow_available = self._check_iflow()
        self.ai_api_key = os.getenv("OPENAI_API_KEY") or os.getenv("QWEN_API_KEY")
    
    def _check_iflow(self) -> bool:
        """检查iFlow CLI是否可用"""
        try:
            result = subprocess.run(["iflow", "--version"], 
                                  capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
    
    def load_skill_content(self, skill_name: str) -> str:
        """加载技能内容作为系统提示"""
        skill_file = self.skills_dir / skill_name / "SKILL.md"
        if skill_file.exists():
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 提取主要说明部分
                content = content.replace("---", "").split("##")[0]
                return content.strip()
        return ""
    
    def call_via_iflow(self, user_input: str, skill_name: str) -> Optional[str]:
        """通过iFlow CLI调用大模型"""
        if not self.iflow_available:
            return None
        
        try:
            # 构建iFlow命令
            command = [
                "iflow", 
                "--skill", skill_name,
                "--input", user_input
            ]
            
            result = subprocess.run(command, 
                                  capture_output=True, text=True, 
                                  timeout=60)
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                return None
                
        except Exception as e:
            print(f"iFlow调用失败: {e}")
            return None
    
    def call_direct_api(self, user_input: str, skill_name: str) -> Optional[str]:
        """直接调用大模型API"""
        if not self.ai_api_key:
            return None
        
        try:
            # 加载技能内容
            skill_content = self.load_skill_content(skill_name)
            system_prompt = f"""
你是扎根理论研究专家。请基于以下指导进行专业分析：

{skill_content}

请提供专业、详细的分析结果。
"""
            
            # 调用OpenAI API（示例）
            headers = {
                "Authorization": f"Bearer {self.ai_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-4",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                return None
                
        except Exception as e:
            print(f"API调用失败: {e}")
            return None
    
    def analyze_with_ai(self, user_input: str, skill_name: str, 
                       file_content: str = None) -> Dict:
        """使用AI进行分析"""
        
        # 构建完整的用户输入
        full_input = user_input
        if file_content:
            full_input += f"\n\n待分析内容：\n{file_content}"
        
        # 尝试通过iFlow调用
        ai_result = self.call_via_iflow(full_input, skill_name)
        
        # 如果iFlow不可用，尝试直接API调用
        if not ai_result:
            ai_result = self.call_direct_api(full_input, skill_name)
        
        # 如果都不可用，返回提示
        if not ai_result:
            return {
                "success": False,
                "message": "AI服务不可用，请检查iFlow CLI或API配置",
                "suggestion": "您可以安装iFlow CLI或配置API密钥来启用AI功能"
            }
        
        return {
            "success": True,
            "ai_analysis": ai_result,
            "skill_used": skill_name,
            "method": "iflow" if self.iflow_available else "direct_api"
        }
    
    def get_available_skills(self) -> Dict:
        """获取可用技能列表"""
        skills = {}
        
        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    try:
                        with open(skill_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # 提取技能名称和描述
                            name = skill_dir.name
                            description = content.split("description:")[1].split("\n")[0].strip() if "description:" in content else ""
                            
                            skills[name] = {
                                "name": name,
                                "description": description,
                                "file_path": str(skill_file)
                            }
                    except:
                        continue
        
        return skills

# Flask路由集成示例
def add_ai_routes(app):
    """为Flask应用添加AI路由"""
    ai_integration = AIIntegration()
    
    @app.route('/ai/analyze', methods=['POST'])
    def ai_analyze():
        """AI分析接口"""
        user_input = request.form.get('input', '')
        skill_name = request.form.get('skill', '')
        file_content = None
        
        # 处理文件上传
        if 'file' in request.files:
            file = request.files['file']
            if file.filename:
                file_content = file.read().decode('utf-8')
        
        result = ai_integration.analyze_with_ai(user_input, skill_name, file_content)
        return jsonify(result)
    
    @app.route('/ai/skills')
    def ai_skills():
        """获取可用技能"""
        skills = ai_integration.get_available_skills()
        return jsonify(skills)
    
    @app.route('/ai/status')
    def ai_status():
        """检查AI服务状态"""
        return jsonify({
            "iflow_available": ai_integration.iflow_available,
            "api_configured": bool(ai_integration.ai_api_key),
            "skills_count": len(ai_integration.get_available_skills())
        })

if __name__ == "__main__":
    # 测试AI集成
    ai = AIIntegration()
    print(f"iFlow可用: {ai.iflow_available}")
    print(f"API配置: {bool(ai.ai_api_key)}")
    print(f"可用技能: {len(ai.get_available_skills())}")