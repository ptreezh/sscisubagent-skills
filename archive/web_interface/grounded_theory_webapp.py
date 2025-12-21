#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扎根理论智能体Web界面
基于Flask的简单Web应用原型
"""

from flask import Flask, render_template, request, jsonify, session
import json
import os
import uuid
from datetime import datetime
import logging

# 导入核心引擎
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.core_engine import GroundedTheoryEngine

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # 在生产环境中应该使用安全的密钥

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化核心引擎
engine = GroundedTheoryEngine()

# 模拟数据存储
user_sessions = {}
coding_projects = {}

@app.route('/')
def index():
    """主页"""
    return render_template('index.html')

@app.route('/api/start_session', methods=['POST'])
def start_session():
    """开始新的研究会话"""
    try:
        data = request.get_json()
        user_request = data.get('request', '')
        
        # 生成会话ID
        session_id = str(uuid.uuid4())
        
        # 分析用户请求
        context, strategy = engine.analyze_user_request(user_request, session_id)
        
        # 创建会话
        user_sessions[session_id] = {
            'context': context,
            'strategy': strategy,
            'created_at': datetime.now().isoformat(),
            'status': 'active'
        }
        
        # 创建项目
        project_id = str(uuid.uuid4())
        coding_projects[project_id] = {
            'session_id': session_id,
            'stage': context.stage.value,
            'data': {},
            'history': [],
            'created_at': datetime.now().isoformat()
        }
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'project_id': project_id,
            'context': {
                'urgency': context.urgency.value,
                'stage': context.stage.value,
                'task_type': context.task_type.value,
                'data_type': context.data_type,
                'data_size': context.data_size
            },
            'strategy': {
                'priority': strategy.priority,
                'skills_to_use': strategy.skills_to_use,
                'estimated_time': strategy.estimated_time,
                'requires_human_review': strategy.requires_human_review
            }
        })
        
    except Exception as e:
        logger.error(f"启动会话失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/upload_text', methods=['POST'])
def upload_text():
    """上传文本数据"""
    try:
        session_id = request.form.get('session_id')
        project_id = request.form.get('project_id')
        text_file = request.files.get('text_file')
        
        if not all([session_id, project_id, text_file]):
            return jsonify({'success': False, 'error': '缺少必要参数'}), 400
        
        # 读取文件内容
        text_content = text_file.read().decode('utf-8')
        
        # 更新项目数据
        if project_id in coding_projects:
            coding_projects[project_id]['data']['raw_text'] = text_content
            coding_projects[project_id]['data']['filename'] = text_file.filename
            coding_projects[project_id]['data']['uploaded_at'] = datetime.now().isoformat()
            
            # 添加历史记录
            coding_projects[project_id]['history'].append({
                'action': 'upload_text',
                'filename': text_file.filename,
                'timestamp': datetime.now().isoformat()
            })
        
        return jsonify({
            'success': True,
            'message': '文本上传成功',
            'text_length': len(text_content),
            'line_count': len(text_content.split('\n'))
        })
        
    except Exception as e:
        logger.error(f"文本上传失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/execute_skill', methods=['POST'])
def execute_skill():
    """执行技能"""
    try:
        data = request.get_json()
        session_id = data.get('session_id')
        project_id = data.get('project_id')
        skill_name = data.get('skill_name')
        input_data = data.get('input_data', {})
        
        if not all([session_id, project_id, skill_name]):
            return jsonify({'success': False, 'error': '缺少必要参数'}), 400
        
        # 模拟技能执行
        result = simulate_skill_execution(skill_name, input_data, project_id)
        
        # 更新项目数据
        if project_id in coding_projects:
            coding_projects[project_id]['history'].append({
                'action': 'execute_skill',
                'skill_name': skill_name,
                'timestamp': datetime.now().isoformat(),
                'result_summary': result.get('summary', {})
            })
        
        return jsonify({
            'success': True,
            'result': result
        })
        
    except Exception as e:
        logger.error(f"技能执行失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_project_status', methods=['GET'])
def get_project_status():
    """获取项目状态"""
    try:
        project_id = request.args.get('project_id')
        
        if not project_id or project_id not in coding_projects:
            return jsonify({'success': False, 'error': '项目不存在'}), 404
        
        project = coding_projects[project_id]
        session_id = project['session_id']
        
        # 获取会话信息
        session_info = user_sessions.get(session_id, {})
        
        return jsonify({
            'success': True,
            'project': {
                'stage': project['stage'],
                'created_at': project['created_at'],
                'history_count': len(project['history']),
                'data_keys': list(project['data'].keys())
            },
            'session': {
                'urgency': session_info.get('context', {}).urgency.value if session_info.get('context') else 'unknown',
                'status': session_info.get('status', 'unknown')
            }
        })
        
    except Exception as e:
        logger.error(f"获取项目状态失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/get_history', methods=['GET'])
def get_history():
    """获取操作历史"""
    try:
        project_id = request.args.get('project_id')
        
        if not project_id or project_id not in coding_projects:
            return jsonify({'success': False, 'error': '项目不存在'}), 404
        
        history = coding_projects[project_id]['history']
        
        return jsonify({
            'success': True,
            'history': history
        })
        
    except Exception as e:
        logger.error(f"获取历史记录失败: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

def simulate_skill_execution(skill_name: str, input_data: dict, project_id: str) -> dict:
    """模拟技能执行"""
    # 这里应该调用实际的技能执行逻辑
    # 现在只是返回模拟数据
    
    if skill_name == 'performing-open-coding':
        return {
            'summary': {
                'total_concepts': 15,
                'processing_time': 2.5,
                'quality_score': 0.85
            },
            'details': {
                'concepts': [
                    {'name': '寻求支持', 'definition': '主动向他人寻求帮助的行为', 'examples': ['向同学请教问题', '向导师寻求指导']},
                    {'name': '建立关系', 'definition': '与他人建立联系的过程', 'examples': ['参加学术会议', '加入研究小组']},
                    {'name': '应对压力', 'definition': '面对压力时的应对策略', 'examples': '时间管理，情绪调节'}
                ]
            },
            'next_steps': ['review_concepts', 'proceed_to_axial_coding']
        }
    
    elif skill_name == 'performing-axial-coding':
        return {
            'summary': {
                'total_categories': 5,
                'core_categories': 2,
                'total_relations': 8
            },
            'details': {
                'categories': [
                    {'name': '社会支持', 'type': 'core', 'concepts': ['寻求支持', '建立关系']},
                    {'name': '学习策略', 'type': 'core', 'concepts': ['时间管理', '学习方法']},
                    {'name': '情感调节', 'type': 'secondary', 'concepts': ['应对压力', '情绪管理']}
                ],
                'relationships': [
                    {'from': '社会支持', 'to': '学习策略', 'type': '促进', 'strength': 0.8},
                    {'from': '情感调节', 'to': '学习策略', 'type': '影响', 'strength': 0.6}
                ]
            },
            'next_steps': ['build_theory', 'check_saturation']
        }
    
    else:
        return {
            'summary': {
                'status': 'completed',
                'processing_time': 1.0
            },
            'details': {
                'message': f'技能 {skill_name} 执行完成'
            },
            'next_steps': ['continue_analysis']
        }

# 创建模板目录和文件
def create_templates():
    """创建HTML模板"""
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    os.makedirs(templates_dir, exist_ok=True)
    
    # 主页模板
    index_html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>扎根理论智能体</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .stage-indicator {
            background: linear-gradient(90deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .stage-item {
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .stage-item.active {
            background-color: #007bff;
            color: white;
        }
        .upload-area {
            border: 2px dashed #dee2e6;
            border-radius: 10px;
            padding: 40px;
            text-align: center;
            margin: 20px 0;
        }
        .coding-workspace {
            background-color: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            min-height: 400px;
        }
        .concept-card {
            background: white;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .urgency-high {
            border-left: 4px solid #dc3545;
        }
        .urgency-normal {
            border-left: 4px solid #28a745;
        }
    </style>
</head>
<body>
    <div class="container-fluid">
        <div class="row">
            <!-- 左侧导航 -->
            <div class="col-md-3">
                <div class="stage-indicator">
                    <h5>研究阶段</h5>
                    <div class="stage-item" data-stage="initial">初始阶段</div>
                    <div class="stage-item" data-stage="data_preparation">数据准备</div>
                    <div class="stage-item" data-stage="open_coding">开放编码</div>
                    <div class="stage-item" data-stage="axial_coding">轴心编码</div>
                    <div class="stage-item" data-stage="selective_coding">选择式编码</div>
                    <div class="stage-item" data-stage="theory_building">理论构建</div>
                    <div class="stage-item" data-stage="saturation_check">饱和度检验</div>
                </div>
                
                <div class="mt-3">
                    <h6>项目状态</h6>
                    <div id="project-status" class="alert alert-info">
                        <small>等待开始...</small>
                    </div>
                </div>
            </div>
            
            <!-- 主工作区 -->
            <div class="col-md-9">
                <!-- 欢迎界面 -->
                <div id="welcome-section" class="text-center py-5">
                    <h2>扎根理论智能体</h2>
                    <p class="lead">专业的中文质性数据分析助手</p>
                    
                    <div class="row justify-content-center mt-4">
                        <div class="col-md-8">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">开始新的研究项目</h5>
                                    <form id="start-form">
                                        <div class="mb-3">
                                            <label for="user-request" class="form-label">描述您的需求</label>
                                            <textarea class="form-control" id="user-request" rows="4" 
                                                placeholder="例如：我需要分析20份大学生访谈数据，进行开放编码..."></textarea>
                                        </div>
                                        <button type="submit" class="btn btn-primary">开始分析</button>
                                    </form>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- 工作界面 -->
                <div id="work-section" style="display: none;">
                    <!-- 紧急程度指示器 -->
                    <div id="urgency-indicator" class="alert mb-3">
                        <span id="urgency-text"></span>
                    </div>
                    
                    <!-- 文件上传区 -->
                    <div id="upload-section">
                        <h4>数据上传</h4>
                        <div class="upload-area">
                            <input type="file" id="file-input" accept=".txt,.doc,.docx" style="display: none;">
                            <button class="btn btn-outline-primary" onclick="document.getElementById('file-input').click()">
                                选择文件
                            </button>
                            <p class="mt-2 text-muted">支持 .txt, .doc, .docx 格式</p>
                        </div>
                    </div>
                    
                    <!-- 编码工作区 -->
                    <div id="coding-section" style="display: none;">
                        <h4>编码工作区</h4>
                        <div class="row">
                            <div class="col-md-6">
                                <h5>概念列表</h5>
                                <div id="concepts-list" class="coding-workspace">
                                    <!-- 概念卡片将在这里动态生成 -->
                                </div>
                            </div>
                            <div class="col-md-6">
                                <h5>关系网络</h5>
                                <div id="relationships-network" class="coding-workspace">
                                    <!-- 关系网络将在这里显示 -->
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- 操作按钮 -->
                    <div class="mt-4">
                        <button id="execute-skill-btn" class="btn btn-success" style="display: none;">
                            执行分析
                        </button>
                        <button id="save-progress-btn" class="btn btn-secondary" style="display: none;">
                            保存进度
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- 模态框 -->
    <div class="modal fade" id="result-modal" tabindex="-1">
        <div class="modal-dialog modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">分析结果</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body">
                    <div id="result-content">
                        <!-- 结果内容将在这里显示 -->
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">关闭</button>
                    <button type="button" class="btn btn-primary" id="continue-btn">继续</button>
                </div>
            </div>
        </div>
    </div>
    
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        let currentSessionId = null;
        let currentProjectId = null;
        let currentStage = 'initial';
        
        // 开始新会话
        document.getElementById('start-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const userRequest = document.getElementById('user-request').value;
            if (!userRequest.trim()) {
                alert('请描述您的需求');
                return;
            }
            
            try {
                const response = await fetch('/api/start_session', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        request: userRequest
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    currentSessionId = data.session_id;
                    currentProjectId = data.project_id;
                    currentStage = data.context.stage;
                    
                    // 更新界面
                    updateInterface(data);
                    showWorkSection();
                } else {
                    alert('启动失败: ' + data.error);
                }
            } catch (error) {
                alert('网络错误: ' + error.message);
            }
        });
        
        // 更新界面
        function updateInterface(data) {
            // 更新紧急程度指示器
            const urgencyDiv = document.getElementById('urgency-indicator');
            const urgencyText = document.getElementById('urgency-text');
            
            if (data.context.urgency === 'high' || data.context.urgency === 'critical') {
                urgencyDiv.className = 'alert alert-danger urgency-high';
                urgencyText.textContent = '🚨 紧急任务 - 优先处理';
            } else {
                urgencyDiv.className = 'alert alert-success urgency-normal';
                urgencyText.textContent = '✅ 常规任务 - 标准处理';
            }
            
            // 更新阶段指示器
            document.querySelectorAll('.stage-item').forEach(item => {
                item.classList.remove('active');
                if (item.dataset.stage === currentStage) {
                    item.classList.add('active');
                }
            });
            
            // 更新项目状态
            const statusDiv = document.getElementById('project-status');
            statusDiv.innerHTML = `
                <small>
                    <strong>阶段:</strong> ${getStageName(data.context.stage)}<br>
                    <strong>任务:</strong> ${getTaskTypeName(data.context.task_type)}<br>
                    <strong>预计时间:</strong> ${data.strategy.estimated_time}分钟
                </small>
            `;
            
            // 显示相关按钮
            document.getElementById('execute-skill-btn').style.display = 'inline-block';
            document.getElementById('save-progress-btn').style.display = 'inline-block';
        }
        
        // 显示工作区
        function showWorkSection() {
            document.getElementById('welcome-section').style.display = 'none';
            document.getElementById('work-section').style.display = 'block';
        }
        
        // 文件上传
        document.getElementById('file-input').addEventListener('change', async function(e) {
            const file = e.target.files[0];
            if (!file) return;
            
            const formData = new FormData();
            formData.append('session_id', currentSessionId);
            formData.append('project_id', currentProjectId);
            formData.append('text_file', file);
            
            try {
                const response = await fetch('/api/upload_text', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                if (data.success) {
                    alert('文件上传成功！');
                    // 显示编码区
                    document.getElementById('coding-section').style.display = 'block';
                } else {
                    alert('上传失败: ' + data.error);
                }
            } catch (error) {
                alert('网络错误: ' + error.message);
            }
        });
        
        // 执行技能
        document.getElementById('execute-skill-btn').addEventListener('click', async function() {
            if (!currentSessionId || !currentProjectId) {
                alert('请先开始项目');
                return;
            }
            
            try {
                const response = await fetch('/api/execute_skill', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        session_id: currentSessionId,
                        project_id: currentProjectId,
                        skill_name: 'performing-open-coding',
                        input_data: {}
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    showResult(data.result);
                    updateConceptsList(data.result.details.concepts);
                } else {
                    alert('执行失败: ' + data.error);
                }
            } catch (error) {
                alert('网络错误: ' + error.message);
            }
        });
        
        // 显示结果
        function showResult(result) {
            const resultContent = document.getElementById('result-content');
            resultContent.innerHTML = `
                <h6>分析摘要</h6>
                <ul>
                    <li>识别概念: ${result.summary.total_concepts} 个</li>
                    <li>处理时间: ${result.summary.processing_time} 分钟</li>
                    <li>质量评分: ${result.summary.quality_score || 'N/A'}</li>
                </ul>
                
                <h6>下一步建议</h6>
                <ul>
                    ${result.next_steps.map(step => `<li>${step}</li>`).join('')}
                </ul>
            `;
            
            new bootstrap.Modal(document.getElementById('result-modal')).show();
        }
        
        // 更新概念列表
        function updateConceptsList(concepts) {
            const conceptsList = document.getElementById('concepts-list');
            conceptsList.innerHTML = concepts.map(concept => `
                <div class="concept-card">
                    <h6>${concept.name}</h6>
                    <p><strong>定义:</strong> ${concept.definition}</p>
                    <p><strong>示例:</strong> ${Array.isArray(concept.examples) ? concept.examples.join(', ') : concept.examples}</p>
                </div>
            `).join('');
        }
        
        // 辅助函数
        function getStageName(stage) {
            const names = {
                'initial': '初始阶段',
                'data_preparation': '数据准备',
                'open_coding': '开放编码',
                'axial_coding': '轴心编码',
                'selective_coding': '选择式编码',
                'theory_building': '理论构建',
                'saturation_check': '饱和度检验'
            };
            return names[stage] || stage;
        }
        
        function getTaskTypeName(taskType) {
            const names = {
                'coding': '编码',
                'analysis': '分析',
                'theory_building': '理论构建',
                'quality_check': '质量检查',
                'memo_writing': '备忘录写作',
                'collaboration': '协作'
            };
            return names[taskType] || taskType;
        }
    </script>
</body>
</html>'''
    
    with open(os.path.join(templates_dir, 'index.html'), 'w', encoding='utf-8') as f:
        f.write(index_html)

if __name__ == '__main__':
    # 创建模板
    create_templates()
    
    # 启动应用
    print("🚀 扎根理论智能体Web界面启动中...")
    print("📱 访问地址: http://localhost:5000")
    print("🔧 API文档: http://localhost:5000/api")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
