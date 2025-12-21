#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真正的智能体系统
集成大模型、角色设定、技能调用、脚本执行的完整流程
"""

import os
import json
import subprocess
import requests
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class AgentRole:
    """智能体角色"""
    name: str
    description: str
    system_prompt: str
    capabilities: List[str]
    skills: List[str]

@dataclass
class TaskContext:
    """任务上下文"""
    user_id: str
    task_id: str
    role: str
    task_description: str
    uploaded_files: List[Dict]
    conversation_history: List[Dict]
    current_stage: str

class IntelligentAgent:
    """真正的智能体系统"""
    
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.skills_dir = self.root_dir / "skills"
        self.agents_dir = self.root_dir / "agents"
        
        # 加载角色定义
        self.roles = self._load_roles()
        
        # AI配置
        self.ai_config = {
            "api_key": os.getenv("OPENAI_API_KEY") or os.getenv("QWEN_API_KEY"),
            "model": os.getenv("AI_MODEL", "gpt-4"),
            "base_url": os.getenv("AI_BASE_URL", "https://api.openai.com/v1")
        }
        
        # 会话管理
        self.active_sessions = {}
    
    def _load_roles(self) -> Dict[str, AgentRole]:
        """加载所有智能体角色"""
        roles = {}
        
        agent_files = list(self.agents_dir.glob("*.md"))
        for agent_file in agent_files:
            try:
                role = self._parse_agent_file(agent_file)
                if role:
                    roles[role.name] = role
                    logger.info(f"加载角色: {role.name}")
            except Exception as e:
                logger.error(f"加载角色失败 {agent_file}: {e}")
        
        return roles
    
    def _parse_agent_file(self, agent_file: Path) -> Optional[AgentRole]:
        """解析智能体配置文件"""
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 解析YAML前置内容
        yaml_match = content.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not yaml_match:
            return None
        
        yaml_content = yaml_match.group(1)
        config = {}
        for line in yaml_content.split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                config[key.strip()] = value.strip().strip('"\'')
        
        # 提取主要描述
        main_content = content.replace(yaml_match.group(0), '')
        
        return AgentRole(
            name=config.get('name', agent_file.stem),
            description=config.get('description', ''),
            system_prompt=self._build_system_prompt(main_content),
            capabilities=self._extract_capabilities(main_content),
            skills=config.get('core_skills', '').split(', ') if config.get('core_skills') else []
        )
    
    def _build_system_prompt(self, content: str) -> str:
        """构建系统提示"""
        # 提取专业领域、工作方法等关键部分
        sections = {
            '专业领域': r'## 专业领域\s*\n(.*?)(?=##|\n#|$)',
            '工作方法': r'## 工作方法\s*\n(.*?)(?=##|\n#|$)',
            '质量检查': r'## 质量检查清单\s*\n(.*?)(?=##|\n#|$)'
        }
        
        system_prompt = "你是" + content.split('\n')[0] + "\n\n"
        
        for section_name, pattern in sections.items():
            match = re.search(pattern, content, re.DOTALL)
            if match:
                system_prompt += f"## {section_name}\n{match.group(1).strip()}\n\n"
        
        # 添加智能体行为指导
        system_prompt += """
## 智能体行为指导

1. **理解用户需求**：仔细分析用户的任务描述和上传的文件
2. **选择合适的技能**：根据任务需求从你的技能库中选择最合适的技能
3. **调用相关脚本**：在需要数据处理时，调用相应的Python脚本
4. **整合分析结果**：将脚本执行结果与你的专业分析结合
5. **提供建议和下一步**：给出专业建议和后续工作指导

## 可用技能调用

你可以使用以下格式的特殊指令来调用脚本：
```
[SCRIPT_CALL: skill_name/script_name.py --param value]
```

系统会执行脚本并将结果返回给你，然后你基于结果进行专业分析。
"""
        
        return system_prompt
    
    def _extract_capabilities(self, content: str) -> List[str]:
        """提取能力列表"""
        capabilities = []
        
        if "文献" in content: capabilities.append("文献分析")
        if "编码" in content: capabilities.append("质性编码")
        if "网络" in content: capabilities.append("网络分析")
        if "理论" in content: capabilities.append("理论构建")
        if "统计" in content: capabilities.append("统计分析")
        
        return capabilities or ["综合分析"]
    
    def create_session(self, user_id: str, role_name: str, task_description: str) -> str:
        """创建新的智能体会话"""
        if role_name not in self.roles:
            raise ValueError(f"未知的角色: {role_name}")
        
        task_id = f"{user_id}_{int(time.time())}"
        
        session = TaskContext(
            user_id=user_id,
            task_id=task_id,
            role=role_name,
            task_description=task_description,
            uploaded_files=[],
            conversation_history=[],
            current_stage="initial"
        )
        
        self.active_sessions[task_id] = session
        
        logger.info(f"创建会话: {task_id}, 角色: {role_name}")
        return task_id
    
    def upload_file(self, task_id: str, file_data: bytes, filename: str) -> bool:
        """上传文件到会话"""
        if task_id not in self.active_sessions:
            return False
        
        session = self.active_sessions[task_id]
        
        # 保存文件
        uploads_dir = self.root_dir / "uploads" / task_id
        uploads_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = uploads_dir / filename
        with open(file_path, 'wb') as f:
            f.write(file_data)
        
        # 记录文件信息
        session.uploaded_files.append({
            "filename": filename,
            "path": str(file_path),
            "size": len(file_data),
            "uploaded_at": time.time()
        })
        
        logger.info(f"文件上传成功: {filename}")
        return True
    
    def process_message(self, task_id: str, user_message: str) -> Dict:
        """处理用户消息并返回智能体响应"""
        if task_id not in self.active_sessions:
            return {"error": "会话不存在"}
        
        session = self.active_sessions[task_id]
        role = self.roles[session.role]
        
        # 构建上下文
        context = self._build_context(session, user_message)
        
        # 调用大模型
        ai_response = self._call_ai_model(role.system_prompt, context)
        
        if not ai_response:
            return {"error": "AI服务不可用"}
        
        # 检查是否需要调用脚本
        script_calls = self._extract_script_calls(ai_response)
        
        if script_calls:
            # 执行脚本并重新分析
            script_results = self._execute_scripts(script_calls, session)
            
            # 将脚本结果返回给AI进行整合分析
            enhanced_context = context + f"\n\n脚本执行结果：\n{json.dumps(script_results, ensure_ascii=False, indent=2)}"
            final_response = self._call_ai_model(role.system_prompt, enhanced_context)
            
            ai_response = final_response or ai_response
        
        # 更新对话历史
        session.conversation_history.append({
            "role": "user",
            "content": user_message,
            "timestamp": time.time()
        })
        session.conversation_history.append({
            "role": "assistant", 
            "content": ai_response,
            "timestamp": time.time()
        })
        
        return {
            "success": True,
            "response": ai_response,
            "role": role.name,
            "stage": session.current_stage,
            "script_executed": len(script_calls) > 0
        }
    
    def _build_context(self, session: TaskContext, user_message: str) -> str:
        """构建完整的上下文"""
        context = f"""
任务描述：{session.task_description}

当前阶段：{session.current_stage}

用户消息：{user_message}
"""
        
        # 添加文件信息
        if session.uploaded_files:
            context += "\n\n已上传文件：\n"
            for file_info in session.uploaded_files:
                context += f"- {file_info['filename']} ({file_info['size']} bytes)\n"
                
                # 如果是文本文件，读取内容
                if file_info['filename'].endswith(('.txt', '.md')):
                    try:
                        with open(file_info['path'], 'r', encoding='utf-8') as f:
                            content = f.read()
                            if len(content) > 2000:
                                content = content[:2000] + "...\n[内容已截断]"
                            context += f"内容预览：\n{content}\n"
                    except:
                        pass
        
        # 添加对话历史
        if session.conversation_history:
            context += "\n\n对话历史：\n"
            for msg in session.conversation_history[-5:]:  # 只保留最近5条
                context += f"{msg['role']}: {msg['content']}\n"
        
        return context
    
    def _call_ai_model(self, system_prompt: str, user_input: str) -> Optional[str]:
        """调用大模型API"""
        if not self.ai_config["api_key"]:
            logger.error("未配置AI API密钥")
            return None
        
        try:
            headers = {
                "Authorization": f"Bearer {self.ai_config['api_key']}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": self.ai_config["model"],
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                "temperature": 0.7,
                "max_tokens": 4000
            }
            
            response = requests.post(
                f"{self.ai_config['base_url']}/chat/completions",
                headers=headers,
                json=data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]
            else:
                logger.error(f"AI API调用失败: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            logger.error(f"AI调用异常: {e}")
            return None
    
    def _extract_script_calls(self, ai_response: str) -> List[Dict]:
        """从AI响应中提取脚本调用指令"""
        import re
        
        pattern = r'\[SCRIPT_CALL: (.*?)\]'
        matches = re.findall(pattern, ai_response)
        
        script_calls = []
        for match in matches:
            parts = match.split()
            if len(parts) >= 1:
                script_path = parts[0]
                params = {}
                
                # 解析参数
                for part in parts[1:]:
                    if part.startswith('--'):
                        if '=' in part:
                            key, value = part[2:].split('=', 1)
                            params[key] = value
                        else:
                            params[part[2:]] = True
                
                script_calls.append({
                    "script": script_path,
                    "params": params
                })
        
        return script_calls
    
    def _execute_scripts(self, script_calls: List[Dict], session: TaskContext) -> Dict:
        """执行脚本并返回结果"""
        results = {}
        
        for i, call in enumerate(script_calls):
            script_name = f"script_{i}"
            
            try:
                # 构建脚本路径
                script_parts = call["script"].split('/')
                if len(script_parts) >= 2:
                    skill_name = script_parts[0]
                    script_file = script_parts[1]
                    script_path = self.skills_dir / skill_name / "scripts" / script_file
                else:
                    script_path = self.skills_dir / call["script"]
                
                if not script_path.exists():
                    results[script_name] = {"error": f"脚本不存在: {script_path}"}
                    continue
                
                # 构建命令
                cmd = ["python", str(script_path)]
                
                # 添加参数
                for key, value in call["params"].items():
                    cmd.extend([f"--{key}", str(value)])
                
                # 添加文件路径参数
                if session.uploaded_files:
                    latest_file = session.uploaded_files[-1]
                    cmd.extend(["--input", latest_file["path"]])
                
                # 执行脚本
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=120,
                    cwd=self.root_dir
                )
                
                results[script_name] = {
                    "command": " ".join(cmd),
                    "returncode": result.returncode,
                    "stdout": result.stdout,
                    "stderr": result.stderr
                }
                
                logger.info(f"脚本执行完成: {script_name}")
                
            except subprocess.TimeoutExpired:
                results[script_name] = {"error": "脚本执行超时"}
            except Exception as e:
                results[script_name] = {"error": f"脚本执行异常: {str(e)}"}
        
        return results
    
    def get_available_roles(self) -> Dict[str, Dict]:
        """获取可用角色列表"""
        return {
            name: {
                "name": role.name,
                "description": role.description,
                "capabilities": role.capabilities,
                "skills": role.skills
            }
            for name, role in self.roles.items()
        }
    
    def get_session_info(self, task_id: str) -> Optional[Dict]:
        """获取会话信息"""
        if task_id not in self.active_sessions:
            return None
        
        session = self.active_sessions[task_id]
        role = self.roles[session.role]
        
        return {
            "task_id": task_id,
            "role": role.name,
            "description": role.description,
            "task_description": session.task_description,
            "current_stage": session.current_stage,
            "files_count": len(session.uploaded_files),
            "messages_count": len(session.conversation_history),
            "created_at": session.conversation_history[0]["timestamp"] if session.conversation_history else None
        }

# Flask集成
def create_intelligent_routes(app):
    """为Flask应用创建智能体路由"""
    agent = IntelligentAgent()
    
    @app.route('/agent/roles')
    def get_roles():
        """获取可用角色"""
        return jsonify(agent.get_available_roles())
    
    @app.route('/agent/create_session', methods=['POST'])
    def create_session():
        """创建智能体会话"""
        data = request.get_json()
        user_id = data.get('user_id', 'anonymous')
        role_name = data.get('role')
        task_description = data.get('task_description', '')
        
        try:
            task_id = agent.create_session(user_id, role_name, task_description)
            return jsonify({
                "success": True,
                "task_id": task_id,
                "role": role_name
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)})
    
    @app.route('/agent/upload_file/<task_id>', methods=['POST'])
    def upload_file(task_id):
        """上传文件到会话"""
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "没有文件"})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "error": "文件名为空"})
        
        success = agent.upload_file(
            task_id, 
            file.read(), 
            file.filename
        )
        
        return jsonify({"success": success})
    
    @app.route('/agent/chat/<task_id>', methods=['POST'])
    def chat_with_agent(task_id):
        """与智能体对话"""
        data = request.get_json()
        user_message = data.get('message', '')
        
        result = agent.process_message(task_id, user_message)
        return jsonify(result)
    
    @app.route('/agent/session/<task_id>')
    def get_session(task_id):
        """获取会话信息"""
        info = agent.get_session_info(task_id)
        if info:
            return jsonify({"success": True, "session": info})
        else:
            return jsonify({"success": False, "error": "会话不存在"})

if __name__ == "__main__":
    # 测试智能体
    agent = IntelligentAgent()
    roles = agent.get_available_roles()
    print(f"可用角色: {list(roles.keys())}")