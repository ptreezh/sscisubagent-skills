#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSCI技能Web界面
提供浏览器友好的技能使用界面
"""

import os
import sys
import json
import subprocess
import threading
import webbrowser
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import argparse

try:
    from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
    from flask_cors import CORS
    import werkzeug.utils
    WEB_AVAILABLE = True
except ImportError:
    WEB_AVAILABLE = False

class WebInterface:
    """Web界面管理器"""

    def __init__(self, host: str = "127.0.0.1", port: int = 5000):
        self.host = host
        self.port = port
        self.root_dir = Path(__file__).parent
        self.app = None
        self.server_thread = None
        self.skills = self._load_skills()
        self.uploads_dir = self.root_dir / "uploads"
        self.results_dir = self.root_dir / "results"
        self._create_directories()

    def _create_directories(self):
        """创建必要的目录"""
        self.uploads_dir.mkdir(exist_ok=True)
        self.results_dir.mkdir(exist_ok=True)

    def _load_skills(self) -> Dict:
        """加载所有技能"""
        skills = {}
        skills_dir = self.root_dir / "skills"

        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_info = self._analyze_skill(skill_dir)
                if skill_info:
                    skills[skill_dir.name] = skill_info

        return skills

    def _analyze_skill(self, skill_dir: Path) -> Optional[Dict]:
        """分析技能"""
        skill_files = list(skill_dir.rglob("SKILL.md"))
        if not skill_files:
            return None

        # 读取技能描述
        description = "SSCI研究技能"
        main_skill_file = skill_dir / "SKILL.md"
        if main_skill_file.exists():
            try:
                with open(main_skill_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    for line in lines:
                        if line.startswith('description:'):
                            description = line.replace('description:', '').strip()
                            break
            except Exception:
                pass

        # 查找可执行脚本
        scripts = []
        scripts_dir = skill_dir / "scripts"
        if scripts_dir.exists():
            for script in scripts_dir.glob("*.py"):
                if not script.name.startswith('_'):
                    scripts.append({
                        "name": script.name,
                        "path": script,
                        "description": self._get_script_description(script)
                    })

        return {
            "name": skill_dir.name,
            "path": skill_dir,
            "description": description,
            "scripts": scripts,
            "category": self._get_category(skill_dir.name)
        }

    def _get_script_description(self, script: Path) -> str:
        """获取脚本描述"""
        if "preprocess" in script.name:
            return "中文文本预处理和清理"
        elif "centrality" in script.name:
            return "网络中心性分析"
        elif "saturation" in script.name:
            return "理论饱和度检验"
        elif "extract" in script.name:
            return "概念提取"
        elif "compare" in script.name:
            return "编码比较和优化"
        else:
            return "数据处理脚本"

    def _get_category(self, skill_name: str) -> str:
        """获取技能分类"""
        if "coding" in skill_name:
            return "编码分析"
        elif "analysis" in skill_name:
            return "数据分析"
        elif "theory" in skill_name:
            return "理论分析"
        else:
            return "其他工具"

    def create_app(self):
        """创建Flask应用"""
        if not WEB_AVAILABLE:
            raise ImportError("需要安装Flask和Flask-CORS: pip install flask flask-cors")

        app = Flask(__name__)
        CORS(app)
        app.config['UPLOAD_FOLDER'] = str(self.uploads_dir)
        app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

        # 首页
        @app.route('/')
        def index():
            return render_template('index.html', skills=self.skills)

        # 技能详情页
        @app.route('/skill/<skill_name>')
        def skill_detail(skill_name):
            if skill_name not in self.skills:
                return "技能不存在", 404
            return render_template('skill.html',
                                 skill=self.skills[skill_name],
                                 skill_name=skill_name)

        # 运行技能
        @app.route('/run/<skill_name>/<script_name>', methods=['POST'])
        def run_skill(skill_name, script_name):
            if skill_name not in self.skills:
                return jsonify({"error": "技能不存在"}), 404

            skill = self.skills[skill_name]
            script = None
            for s in skill["scripts"]:
                if script_name in s["name"]:
                    script = s["path"]
                    break

            if not script:
                return jsonify({"error": "脚本不存在"}), 404

            try:
                # 处理文件上传
                input_file = None
                if 'file' in request.files:
                    file = request.files['file']
                    if file.filename:
                        filename = werkzeug.utils.secure_filename(file.filename)
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{timestamp}_{filename}"
                        input_file = self.uploads_dir / filename
                        file.save(str(input_file))

                # 获取参数
                params = request.form.to_dict()

                # 执行脚本
                result = self._execute_script(script, input_file, params)

                return jsonify({
                    "success": True,
                    "result": result,
                    "timestamp": datetime.now().isoformat()
                })

            except Exception as e:
                return jsonify({
                    "success": False,
                    "error": str(e)
                }), 500

        # 下载结果
        @app.route('/download/<filename>')
        def download_file(filename):
            file_path = self.results_dir / filename
            if file_path.exists():
                return send_file(str(file_path), as_attachment=True)
            return "文件不存在", 404

        # API端点
        @app.route('/api/skills')
        def api_skills():
            return jsonify(self.skills)

        @app.route('/api/results')
        def api_results():
            results = []
            for file_path in self.results_dir.glob("*"):
                if file_path.is_file():
                    results.append({
                        "name": file_path.name,
                        "size": file_path.stat().st_size,
                        "modified": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                    })
            return jsonify(results)

        return app

    def _execute_script(self, script: Path, input_file: Optional[Path], params: Dict) -> Dict:
        """执行脚本"""
        cmd = [sys.executable, str(script)]

        # 添加输入文件参数
        if input_file:
            if "preprocess" in script.name or "extract" in script.name:
                cmd.extend(["--input", str(input_file)])
            elif "centrality" in script.name:
                cmd.extend(["--input", str(input_file)])
            elif "saturation" in script.name:
                cmd.extend(["--data-dir", str(input_file.parent)])

        # 添加输出文件参数
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        script_name = script.stem
        output_file = self.results_dir / f"{script_name}_result_{timestamp}.json"

        if "--output" not in " ".join(cmd):
            cmd.extend(["--output", str(output_file)])

        # 执行命令
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', timeout=300)

            return {
                "command": " ".join(cmd),
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "output_file": str(output_file) if output_file.exists() else None
            }
        except subprocess.TimeoutExpired:
            return {
                "command": " ".join(cmd),
                "error": "执行超时 (5分钟)"
            }
        except Exception as e:
            return {
                "command": " ".join(cmd),
                "error": str(e)
            }

    def create_templates(self):
        """创建HTML模板"""
        templates_dir = self.root_dir / "templates"
        templates_dir.mkdir(exist_ok=True)

        # 创建基础模板
        base_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}SSCI技能包{% endblock %}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        body { font-family: 'Microsoft YaHei', sans-serif; background-color: #f8f9fa; }
        .skill-card { transition: transform 0.2s; }
        .skill-card:hover { transform: translateY(-5px); }
        .category-badge { font-size: 0.8em; }
        .result-output { background-color: #f8f9fa; border-radius: 5px; padding: 15px; }
        .upload-area { border: 2px dashed #dee2e6; border-radius: 10px; padding: 30px; text-align: center; }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
        <div class="container">
            <a class="navbar-brand" href="/">
                <i class="fas fa-flask"></i> SSCI技能包
            </a>
            <div class="navbar-nav ms-auto">
                <a class="nav-link" href="/api/skills" target="_blank">
                    <i class="fas fa-code"></i> API
                </a>
                <a class="nav-link" href="/api/results" target="_blank">
                    <i class="fas fa-chart-line"></i> 结果
                </a>
            </div>
        </div>
    </nav>

    <div class="container mt-4">
        {% block content %}{% endblock %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        function showToast(message, type = 'info') {
            const toast = document.createElement('div');
            toast.className = `toast align-items-center text-white bg-${type} border-0`;
            toast.setAttribute('role', 'alert');
            toast.innerHTML = `
                <div class="d-flex">
                    <div class="toast-body">${message}</div>
                    <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
                </div>
            `;
            document.body.appendChild(toast);
            const bsToast = new bootstrap.Toast(toast);
            bsToast.show();
            setTimeout(() => toast.remove(), 5000);
        }
    </script>
    {% block scripts %}{% endblock %}
</body>
</html>
        """

        # 首页模板
        index_template = base_template.replace(
            "{% block title %}SSCI技能包 - {% endblock %}",
            "SSCI技能包 - 首页"
        ).replace(
            "{% block content %}{% endblock %}",
            """
<div class="row">
    <div class="col-12">
        <div class="jumbotron bg-white rounded-3 shadow-sm p-5">
            <h1 class="display-4">🎯 SSCI中文学科研究技能包</h1>
            <p class="lead">专业的中文社会科学研究工具集合，提供从文本处理到理论分析的完整解决方案。</p>
            <hr class="my-4">
            <p>支持编码分析、网络分析、理论饱和度检验等多种研究方法。</p>
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12">
        <h2>📚 可用技能</h2>
        <div class="row">
            {% for skill_name, skill in skills.items() %}
            <div class="col-md-6 col-lg-4 mb-4">
                <div class="card skill-card h-100 shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">
                            <i class="fas fa-tools"></i> {{ skill.name.replace('-', ' ').title() }}
                            <span class="badge bg-secondary category-badge ms-2">{{ skill.category }}</span>
                        </h5>
                        <p class="card-text">{{ skill.description }}</p>
                        <p class="text-muted small">
                            <i class="fas fa-file-code"></i> {{ skill.scripts|length }} 个脚本
                        </p>
                        <a href="/skill/{{ skill_name }}" class="btn btn-primary btn-sm">
                            <i class="fas fa-play"></i> 使用技能
                        </a>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
</div>

<div class="row mt-4">
    <div class="col-12">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-info-circle"></i> 使用说明</h5>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-4">
                        <h6>🎯 选择技能</h6>
                        <p>根据研究需求选择合适的分析技能。</p>
                    </div>
                    <div class="col-md-4">
                        <h6>📁 上传数据</h6>
                        <p>上传txt、json等格式的数据文件。</p>
                    </div>
                    <div class="col-md-4">
                        <h6>📊 查看结果</h6>
                        <p>实时查看分析结果并下载报告。</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
            """
        )

        # 技能详情模板
        skill_template = base_template.replace(
            "{% block title %}SSCI技能包 - {% endblock %}",
            "SSCI技能包 - {{ skill_name.replace('-', ' ').title() }}"
        ).replace(
            "{% block content %}{% endblock %}",
            """
<div class="row">
    <div class="col-12">
        <nav aria-label="breadcrumb">
            <ol class="breadcrumb">
                <li class="breadcrumb-item"><a href="/">首页</a></li>
                <li class="breadcrumb-item active">{{ skill_name.replace('-', ' ').title() }}</li>
            </ol>
        </nav>
    </div>
</div>

<div class="row mt-4">
    <div class="col-md-8">
        <div class="card">
            <div class="card-header">
                <h4><i class="fas fa-cogs"></i> {{ skill_name.replace('-', ' ').title() }}</h4>
            </div>
            <div class="card-body">
                <p class="card-text">{{ skill.description }}</p>

                {% if skill.scripts %}
                <h5>🔧 可用脚本</h5>
                <div class="list-group">
                    {% for script in skill.scripts %}
                    <div class="list-group-item">
                        <div class="d-flex w-100 justify-content-between">
                            <h6 class="mb-1">{{ script.name }}</h6>
                            <button class="btn btn-primary btn-sm run-script-btn"
                                    data-skill="{{ skill_name }}"
                                    data-script="{{ script.name }}">
                                <i class="fas fa-play"></i> 运行
                            </button>
                        </div>
                        <p class="mb-1">{{ script.description }}</p>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
            </div>
        </div>
    </div>

    <div class="col-md-4">
        <div class="card">
            <div class="card-header">
                <h5><i class="fas fa-upload"></i> 数据上传</h5>
            </div>
            <div class="card-body">
                <form id="uploadForm" enctype="multipart/form-data">
                    <div class="mb-3">
                        <label for="fileInput" class="form-label">选择文件</label>
                        <input type="file" class="form-control" id="fileInput" accept=".txt,.json,.csv">
                    </div>
                    <div class="mb-3">
                        <label for="paramsInput" class="form-label">参数设置</label>
                        <textarea class="form-control" id="paramsInput" rows="3"
                                  placeholder="如: --output result.json"></textarea>
                    </div>
                    <button type="submit" class="btn btn-success w-100">
                        <i class="fas fa-rocket"></i> 开始分析
                    </button>
                </form>
            </div>
        </div>

        <div class="card mt-3">
            <div class="card-header">
                <h5><i class="fas fa-chart-line"></i> 执行结果</h5>
            </div>
            <div class="card-body">
                <div id="resultOutput" class="result-output" style="display: none;">
                    <div id="resultContent"></div>
                </div>
                <div id="resultPlaceholder" class="text-muted text-center">
                    <i class="fas fa-info-circle"></i> 执行脚本后将显示结果
                </div>
            </div>
        </div>
    </div>
</div>
            """
        ).replace(
            "{% block scripts %}{% endblock %}",
            """
<script>
$(document).ready(function() {
    $('#uploadForm').on('submit', function(e) {
        e.preventDefault();

        const formData = new FormData();
        const fileInput = $('#fileInput')[0];
        const paramsInput = $('#paramsInput').val();

        if (fileInput.files.length > 0) {
            formData.append('file', fileInput.files[0]);
        }

        // 解析参数
        if (paramsInput) {
            const params = paramsInput.split(' ').filter(p => p.trim());
            params.forEach((param, index) => {
                if (param.startsWith('--')) {
                    const parts = param.split('=');
                    if (parts.length > 1) {
                        formData.append(parts[0].substring(2), parts[1]);
                    } else {
                        formData.append(parts[0].substring(2), 'true');
                    }
                }
            });
        }

        // 获取当前选择的脚本
        const activeScript = $('.run-script-btn.active').data('script');
        if (activeScript) {
            const currentSkill = '{{ skill_name }}';

            $('#resultPlaceholder').hide();
            $('#resultOutput').show();
            $('#resultContent').html('<div class="spinner-border" role="status"><span class="visually-hidden">执行中...</span></div>');

            fetch(`/run/${currentSkill}/${activeScript}`, {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    let resultHtml = '<div class="alert alert-success">执行成功!</div>';
                    resultHtml += '<h6>执行命令:</h6>';
                    resultHtml += `<code>${data.result.command}</code>`;

                    if (data.result.stdout) {
                        resultHtml += '<h6>输出:</h6>';
                        resultHtml += `<pre class="bg-light p-2 rounded">${data.result.stdout}</pre>`;
                    }

                    if (data.result.stderr) {
                        resultHtml += '<h6>错误信息:</h6>';
                        resultHtml += `<pre class="bg-warning p-2 rounded">${data.result.stderr}</pre>`;
                    }

                    if (data.result.output_file) {
                        const filename = data.result.output_file.split('/').pop();
                        resultHtml += `<h6>结果文件:</h6>`;
                        resultHtml += `<a href="/download/${filename}" class="btn btn-sm btn-outline-primary">下载 ${filename}</a>`;
                    }

                    $('#resultContent').html(resultHtml);
                    showToast('分析完成!', 'success');
                } else {
                    $('#resultContent').html(`<div class="alert alert-danger">执行失败: ${data.error}</div>`);
                    showToast('执行失败!', 'danger');
                }
            })
            .catch(error => {
                $('#resultContent').html(`<div class="alert alert-danger">请求错误: ${error}</div>`);
                showToast('请求错误!', 'danger');
            });
        } else {
            showToast('请先选择一个脚本', 'warning');
        }
    });

    $('.run-script-btn').on('click', function() {
        $('.run-script-btn').removeClass('active');
        $(this).addClass('active');
        showToast(`已选择: $(this).data('script')`, 'info');
    });
});
</script>
            """
        )

        # 写入模板文件
        with open(templates_dir / "base.html", "w", encoding="utf-8") as f:
            f.write(base_template)

        with open(templates_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(index_template)

        with open(templates_dir / "skill.html", "w", encoding="utf-8") as f:
            f.write(skill_template)

    def start_server(self, open_browser: bool = True):
        """启动Web服务器"""
        if not WEB_AVAILABLE:
            print("❌ 需要安装Flask和Flask-CORS")
            print("请运行: pip install flask flask-cors")
            return False

        try:
            self.create_templates()
            self.app = self.create_app()

            if open_browser:
                def open_browser_delayed():
                    import time
                    time.sleep(2)
                    webbrowser.open(f"http://{self.host}:{self.port}")

                threading.Thread(target=open_browser_delayed, daemon=True).start()

            print(f"🌐 启动Web界面: http://{self.host}:{self.port}")
            print("📝 按 Ctrl+C 停止服务器")

            self.app.run(host=self.host, port=self.port, debug=False)
            return True

        except Exception as e:
            print(f"❌ 启动失败: {e}")
            return False

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='SSCI技能Web界面')
    parser.add_argument('--host', default='127.0.0.1', help='服务器地址')
    parser.add_argument('--port', type=int, default=5000, help='服务器端口')
    parser.add_argument('--no-browser', action='store_true', help='不自动打开浏览器')

    args = parser.parse_args()

    web_interface = WebInterface(args.host, args.port)
    web_interface.start_server(not args.no_browser)

if __name__ == "__main__":
    main()