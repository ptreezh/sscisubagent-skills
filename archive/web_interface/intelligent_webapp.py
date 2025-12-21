#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
真正的智能体Web应用
集成角色设定、技能调用、脚本执行的完整智能体系统
"""

import os
import sys
from pathlib import Path
from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import time
import json

# 添加父目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from web_interface.intelligent_agent import create_intelligent_routes

app = Flask(__name__)
CORS(app)

# 配置
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = Path(__file__).parent.parent / 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# 创建上传目录
app.config['UPLOAD_FOLDER'].mkdir(exist_ok=True)

# 集成智能体路由
create_intelligent_routes(app)

# HTML模板
INTELLIGENT_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>智能体研究助手</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        .chat-container {
            height: 70vh;
            overflow-y: auto;
            border: 1px solid #dee2e6;
            border-radius: 10px;
            padding: 20px;
            background: #f8f9fa;
        }
        .message {
            margin-bottom: 15px;
            padding: 10px 15px;
            border-radius: 10px;
            max-width: 80%;
        }
        .user-message {
            background: #007bff;
            color: white;
            margin-left: auto;
        }
        .agent-message {
            background: white;
            border: 1px solid #dee2e6;
        }
        .role-selector {
            border: 2px solid #007bff;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .role-card {
            cursor: pointer;
            transition: all 0.3s;
            border: 2px solid transparent;
        }
        .role-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .role-card.selected {
            border-color: #007bff;
            background: #e7f3ff;
        }
        .upload-area {
            border: 2px dashed #dee2e6;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
            margin: 20px 0;
            transition: all 0.3s;
        }
        .upload-area:hover {
            border-color: #007bff;
            background: #f8f9ff;
        }
        .upload-area.dragover {
            border-color: #007bff;
            background: #e7f3ff;
        }
        .typing-indicator {
            display: none;
            padding: 10px 15px;
            background: white;
            border-radius: 10px;
            border: 1px solid #dee2e6;
            margin-bottom: 15px;
        }
        .typing-indicator.active {
            display: block;
        }
        .typing-dots {
            display: inline-block;
        }
        .typing-dots span {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: #007bff;
            margin: 0 2px;
            animation: typing 1.4s infinite;
        }
        .typing-dots span:nth-child(2) {
            animation-delay: 0.2s;
        }
        .typing-dots span:nth-child(3) {
            animation-delay: 0.4s;
        }
        @keyframes typing {
            0%, 60%, 100% {
                transform: translateY(0);
            }
            30% {
                transform: translateY(-10px);
            }
        }
        .file-list {
            max-height: 200px;
            overflow-y: auto;
        }
        .script-execution {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
            font-family: monospace;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- 侧边栏 -->
            <div class="col-md-3">
                <div class="role-selector">
                    <h5><i class="fas fa-user-tie"></i> 选择智能体角色</h5>
                    <div id="roles-container">
                        <div class="text-center">
                            <div class="spinner-border" role="status">
                                <span class="visually-hidden">加载中...</span>
                            </div>
                        </div>
                    </div>
                </div>
                
                <div class="card">
                    <div class="card-header">
                        <h6><i class="fas fa-info-circle"></i> 会话信息</h6>
                    </div>
                    <div class="card-body">
                        <div id="session-info">
                            <p class="text-muted">请先选择角色开始会话</p>
                        </div>
                    </div>
                </div>
                
                <div class="card mt-3">
                    <div class="card-header">
                        <h6><i class="fas fa-file"></i> 已上传文件</h6>
                    </div>
                    <div class="card-body">
                        <div class="upload-area" id="upload-area">
                            <i class="fas fa-cloud-upload-alt fa-2x text-muted"></i>
                            <p class="mt-2">拖拽文件到此处或点击选择</p>
                            <input type="file" id="file-input" multiple accept=".txt,.md,.doc,.docx" style="display: none;">
                            <button class="btn btn-outline-primary btn-sm" onclick="document.getElementById('file-input').click()">
                                选择文件
                            </button>
                        </div>
                        <div id="file-list" class="file-list mt-2"></div>
                    </div>
                </div>
            </div>
            
            <!-- 主聊天区 -->
            <div class="col-md-9">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h4><i class="fas fa-robot"></i> 智能研究助手</h4>
                    <div>
                        <button class="btn btn-outline-secondary btn-sm" onclick="clearChat()">
                            <i class="fas fa-trash"></i> 清空对话
                        </button>
                        <button class="btn btn-outline-primary btn-sm" onclick="exportChat()">
                            <i class="fas fa-download"></i> 导出对话
                        </button>
                    </div>
                </div>
                
                <div class="chat-container" id="chat-container">
                    <div class="text-center text-muted">
                        <i class="fas fa-comments fa-3x mb-3"></i>
                        <p>选择一个智能体角色开始对话</p>
                    </div>
                </div>
                
                <div class="typing-indicator" id="typing-indicator">
                    <div class="typing-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                    <span class="ms-2">智能体正在思考...</span>
                </div>
                
                <div class="input-group mt-3">
                    <input type="text" class="form-control" id="message-input" 
                           placeholder="输入您的问题或需求..." disabled>
                    <button class="btn btn-primary" id="send-button" disabled>
                        <i class="fas fa-paper-plane"></i> 发送
                    </button>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // 全局状态
        let currentTaskId = null;
        let currentRole = null;
        let uploadedFiles = [];
        
        // 页面加载完成后初始化
        document.addEventListener('DOMContentLoaded', function() {
            loadRoles();
            setupEventListeners();
        });
        
        // 加载可用角色
        async function loadRoles() {
            try {
                const response = await fetch('/agent/roles');
                const data = await response.json();
                
                const container = document.getElementById('roles-container');
                container.innerHTML = '';
                
                for (const [roleId, role] of Object.entries(data)) {
                    const roleCard = createRoleCard(roleId, role);
                    container.appendChild(roleCard);
                }
            } catch (error) {
                console.error('加载角色失败:', error);
                document.getElementById('roles-container').innerHTML = 
                    '<div class="alert alert-danger">加载角色失败</div>';
            }
        }
        
        // 创建角色卡片
        function createRoleCard(roleId, role) {
            const card = document.createElement('div');
            card.className = 'card role-card mb-2';
            card.innerHTML = `
                <div class="card-body">
                    <h6 class="card-title">${role.name}</h6>
                    <p class="card-text small">${role.description}</p>
                    <div class="capabilities">
                        ${role.capabilities.map(cap => 
                            `<span class="badge bg-primary me-1">${cap}</span>`
                        ).join('')}
                    </div>
                </div>
            `;
            
            card.addEventListener('click', () => selectRole(roleId, role));
            return card;
        }
        
        // 选择角色
        async function selectRole(roleId, role) {
            // 更新UI
            document.querySelectorAll('.role-card').forEach(card => {
                card.classList.remove('selected');
            });
            event.currentTarget.classList.add('selected');
            
            currentRole = role;
            
            // 创建会话
            try {
                const response = await fetch('/agent/create_session', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        user_id: 'web_user_' + Date.now(),
                        role: roleId,
                        task_description: 'Web界面智能研究助手会话'
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    currentTaskId = data.task_id;
                    enableChat();
                    updateSessionInfo();
                    addMessage('system', `已连接到${role.name}智能体，请描述您的研究需求`);
                } else {
                    alert('创建会话失败: ' + data.error);
                }
            } catch (error) {
                console.error('创建会话失败:', error);
                alert('创建会话失败');
            }
        }
        
        // 启用聊天功能
        function enableChat() {
            document.getElementById('message-input').disabled = false;
            document.getElementById('send-button').disabled = false;
            document.getElementById('file-input').disabled = false;
        }
        
        // 更新会话信息
        async function updateSessionInfo() {
            if (!currentTaskId) return;
            
            try {
                const response = await fetch(`/agent/session/${currentTaskId}`);
                const data = await response.json();
                
                if (data.success) {
                    const session = data.session;
                    document.getElementById('session-info').innerHTML = `
                        <p><strong>角色:</strong> ${session.role}</p>
                        <p><strong>任务:</strong> ${session.task_description}</p>
                        <p><strong>阶段:</strong> ${session.current_stage}</p>
                        <p><strong>文件:</strong> ${session.files_count} 个</p>
                        <p><strong>对话:</strong> ${session.messages_count} 条</p>
                    `;
                }
            } catch (error) {
                console.error('获取会话信息失败:', error);
            }
        }
        
        // 设置事件监听器
        function setupEventListeners() {
            // 发送消息
            document.getElementById('send-button').addEventListener('click', sendMessage);
            document.getElementById('message-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
            
            // 文件上传
            const uploadArea = document.getElementById('upload-area');
            const fileInput = document.getElementById('file-input');
            
            uploadArea.addEventListener('click', () => fileInput.click());
            uploadArea.addEventListener('dragover', handleDragOver);
            uploadArea.addEventListener('drop', handleDrop);
            uploadArea.addEventListener('dragleave', handleDragLeave);
            
            fileInput.addEventListener('change', handleFileSelect);
        }
        
        // 发送消息
        async function sendMessage() {
            const input = document.getElementById('message-input');
            const message = input.value.trim();
            
            if (!message || !currentTaskId) return;
            
            // 添加用户消息
            addMessage('user', message);
            input.value = '';
            
            // 显示打字指示器
            showTypingIndicator();
            
            try {
                const response = await fetch(`/agent/chat/${currentTaskId}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        message: message
                    })
                });
                
                const data = await response.json();
                hideTypingIndicator();
                
                if (data.success) {
                    addMessage('agent', data.response);
                    
                    if (data.script_executed) {
                        addScriptExecutionNotice();
                    }
                    
                    updateSessionInfo();
                } else {
                    addMessage('error', '处理失败: ' + data.error);
                }
            } catch (error) {
                hideTypingIndicator();
                console.error('发送消息失败:', error);
                addMessage('error', '网络错误，请重试');
            }
        }
        
        // 添加消息到聊天容器
        function addMessage(type, content) {
            const container = document.getElementById('chat-container');
            
            // 清除初始提示
            if (container.querySelector('.text-center.text-muted')) {
                container.innerHTML = '';
            }
            
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${type}-message`;
            
            if (type === 'agent') {
                // 处理Markdown格式的响应
                messageDiv.innerHTML = formatMessage(content);
            } else {
                messageDiv.textContent = content;
            }
            
            container.appendChild(messageDiv);
            container.scrollTop = container.scrollHeight;
        }
        
        // 格式化消息
        function formatMessage(content) {
            // 简单的Markdown处理
            return content
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/`([^`]+)`/g, '<code>$1</code>')
                .replace(/\n/g, '<br>');
        }
        
        // 显示打字指示器
        function showTypingIndicator() {
            document.getElementById('typing-indicator').classList.add('active');
        }
        
        // 隐藏打字指示器
        function hideTypingIndicator() {
            document.getElementById('typing-indicator').classList.remove('active');
        }
        
        // 添加脚本执行提示
        function addScriptExecutionNotice() {
            const container = document.getElementById('chat-container');
            const notice = document.createElement('div');
            notice.className = 'script-execution';
            notice.innerHTML = '<i class="fas fa-cogs"></i> 智能体已调用专业分析脚本处理数据';
            container.appendChild(notice);
            container.scrollTop = container.scrollHeight;
        }
        
        // 文件处理
        function handleDragOver(e) {
            e.preventDefault();
            e.currentTarget.classList.add('dragover');
        }
        
        function handleDragLeave(e) {
            e.currentTarget.classList.remove('dragover');
        }
        
        function handleDrop(e) {
            e.preventDefault();
            e.currentTarget.classList.remove('dragover');
            
            const files = Array.from(e.dataTransfer.files);
            handleFiles(files);
        }
        
        function handleFileSelect(e) {
            const files = Array.from(e.target.files);
            handleFiles(files);
        }
        
        async function handleFiles(files) {
            if (!currentTaskId) {
                alert('请先选择智能体角色');
                return;
            }
            
            for (const file of files) {
                await uploadFile(file);
            }
        }
        
        async function uploadFile(file) {
            const formData = new FormData();
            formData.append('file', file);
            
            try {
                const response = await fetch(`/agent/upload_file/${currentTaskId}`, {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                if (data.success) {
                    uploadedFiles.push(file);
                    updateFileList();
                    addMessage('system', `已上传文件: ${file.name}`);
                } else {
                    alert('文件上传失败: ' + data.error);
                }
            } catch (error) {
                console.error('文件上传失败:', error);
                alert('文件上传失败');
            }
        }
        
        // 更新文件列表
        function updateFileList() {
            const fileList = document.getElementById('file-list');
            fileList.innerHTML = uploadedFiles.map((file, index) => `
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <small class="text-truncate">${file.name}</small>
                    <button class="btn btn-outline-danger btn-sm" onclick="removeFile(${index})">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `).join('');
        }
        
        // 移除文件
        function removeFile(index) {
            uploadedFiles.splice(index, 1);
            updateFileList();
        }
        
        // 清空对话
        function clearChat() {
            if (confirm('确定要清空所有对话吗？')) {
                document.getElementById('chat-container').innerHTML = `
                    <div class="text-center text-muted">
                        <i class="fas fa-comments fa-3x mb-3"></i>
                        <p>对话已清空，请继续提问</p>
                    </div>
                `;
            }
        }
        
        // 导出对话
        function exportChat() {
            const messages = document.querySelectorAll('.message');
            let content = `智能体对话记录\n`;
            content += `角色: ${currentRole?.name || '未知'}\n`;
            content += `时间: ${new Date().toLocaleString()}\n`;
            content += `文件: ${uploadedFiles.length} 个\n\n`;
            
            messages.forEach(msg => {
                const type = msg.classList.contains('user-message') ? '用户' : 
                             msg.classList.contains('agent-message') ? '智能体' : '系统';
                content += `${type}: ${msg.textContent}\n\n`;
            });
            
            const blob = new Blob([content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `chat_export_${Date.now()}.txt`;
            a.click();
            URL.revokeObjectURL(url);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    """主页"""
    return INTELLIGENT_HTML

@app.route('/health')
def health():
    """健康检查"""
    return jsonify({
        "status": "healthy",
        "timestamp": time.time(),
        "version": "1.0.0"
    })

if __name__ == '__main__':
    print("🤖 启动智能体Web应用...")
    print("🌐 访问地址: http://localhost:5000")
    print("🔧 需要配置环境变量:")
    print("   - OPENAI_API_KEY 或 QWEN_API_KEY")
    print("   - AI_MODEL (默认: gpt-4)")
    print("   - AI_BASE_URL (默认: OpenAI API)")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
