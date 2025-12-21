#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扎根理论智能体部署脚本
自动化部署和测试流程
"""

import os
import sys
import subprocess
import json
import time
import requests
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AgentDeployer:
    """智能体部署器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.agent_dir = self.project_root / "agents"
        self.web_dir = self.project_root / "web_interface"
        self.skills_dir = self.project_root / "skills"
        
        # 部署配置
        self.config = {
            "host": "localhost",
            "port": 5000,
            "python_path": sys.executable,
            "requirements_file": self.project_root / "requirements.txt",
            "test_data_dir": self.project_root / "test_data"
        }
        
        # 服务状态
        self.service_process = None
        self.service_url = f"http://{self.config['host']}:{self.config['port']}"
    
    def check_dependencies(self) -> bool:
        """检查依赖项"""
        logger.info("🔍 检查系统依赖...")
        
        # 检查Python版本
        if sys.version_info < (3, 8):
            logger.error("❌ 需要Python 3.8或更高版本")
            return False
        
        # 检查必要的目录
        required_dirs = [self.agent_dir, self.web_dir, self.skills_dir]
        for dir_path in required_dirs:
            if not dir_path.exists():
                logger.error(f"❌ 缺少必要目录: {dir_path}")
                return False
        
        # 检查requirements文件
        if not self.config["requirements_file"].exists():
            logger.warning("⚠️ requirements.txt不存在，将创建基础依赖")
            self.create_basic_requirements()
        
        logger.info("✅ 依赖检查通过")
        return True
    
    def create_basic_requirements(self):
        """创建基础依赖文件"""
        requirements = """flask>=2.0.0
requests>=2.25.0
jieba>=0.42.1
pandas>=1.3.0
numpy>=1.21.0
scikit-learn>=1.0.0
matplotlib>=3.4.0
seaborn>=0.11.0
networkx>=2.6.0
wordcloud>=1.8.0
"""
        with open(self.config["requirements_file"], 'w', encoding='utf-8') as f:
            f.write(requirements)
        logger.info("📝 创建基础requirements.txt")
    
    def install_dependencies(self) -> bool:
        """安装Python依赖"""
        logger.info("📦 安装Python依赖...")
        
        try:
            result = subprocess.run([
                self.config["python_path"], "-m", "pip", "install", 
                "-r", str(self.config["requirements_file"])
            ], capture_output=True, text=True, timeout=300)
            
            if result.returncode == 0:
                logger.info("✅ 依赖安装成功")
                return True
            else:
                logger.error(f"❌ 依赖安装失败: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("❌ 依赖安装超时")
            return False
        except Exception as e:
            logger.error(f"❌ 依赖安装出错: {str(e)}")
            return False
    
    def start_service(self) -> bool:
        """启动Web服务"""
        logger.info("🚀 启动Web服务...")
        
        try:
            # 切换到web目录
            os.chdir(self.web_dir)
            
            # 启动Flask应用
            self.service_process = subprocess.Popen([
                self.config["python_path"], "grounded_theory_webapp.py"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # 等待服务启动
            time.sleep(3)
            
            # 检查服务是否正常运行
            if self.check_service_health():
                logger.info(f"✅ 服务启动成功: {self.service_url}")
                return True
            else:
                logger.error("❌ 服务启动失败")
                self.stop_service()
                return False
                
        except Exception as e:
            logger.error(f"❌ 启动服务出错: {str(e)}")
            return False
    
    def check_service_health(self) -> bool:
        """检查服务健康状态"""
        try:
            response = requests.get(f"{self.service_url}/", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def stop_service(self):
        """停止Web服务"""
        if self.service_process:
            logger.info("🛑 停止Web服务...")
            self.service_process.terminate()
            self.service_process.wait()
            self.service_process = None
            logger.info("✅ 服务已停止")
    
    def run_tests(self) -> bool:
        """运行测试"""
        logger.info("🧪 运行自动化测试...")
        
        test_results = {
            "api_tests": False,
            "skill_tests": False,
            "integration_tests": False
        }
        
        # API测试
        try:
            test_results["api_tests"] = self.test_api_endpoints()
        except Exception as e:
            logger.error(f"API测试失败: {str(e)}")
        
        # 技能测试
        try:
            test_results["skill_tests"] = self.test_skills()
        except Exception as e:
            logger.error(f"技能测试失败: {str(e)}")
        
        # 集成测试
        try:
            test_results["integration_tests"] = self.test_integration()
        except Exception as e:
            logger.error(f"集成测试失败: {str(e)}")
        
        # 输出测试结果
        logger.info("📊 测试结果:")
        for test_name, result in test_results.items():
            status = "✅ 通过" if result else "❌ 失败"
            logger.info(f"  {test_name}: {status}")
        
        return all(test_results.values())
    
    def test_api_endpoints(self) -> bool:
        """测试API端点"""
        logger.info("🔌 测试API端点...")
        
        # 测试主页
        try:
            response = requests.get(f"{self.service_url}/", timeout=5)
            if response.status_code != 200:
                logger.error("主页访问失败")
                return False
        except Exception as e:
            logger.error(f"主页访问出错: {str(e)}")
            return False
        
        # 测试会话启动
        try:
            response = requests.post(
                f"{self.service_url}/api/start_session",
                json={"request": "测试开放编码功能"},
                timeout=10
            )
            if response.status_code != 200:
                logger.error("会话启动失败")
                return False
            
            data = response.json()
            if not data.get("success"):
                logger.error("会话启动返回失败")
                return False
                
            session_id = data.get("session_id")
            project_id = data.get("project_id")
            
            if not session_id or not project_id:
                logger.error("会话ID或项目ID缺失")
                return False
                
        except Exception as e:
            logger.error(f"会话启动出错: {str(e)}")
            return False
        
        # 测试项目状态
        try:
            response = requests.get(
                f"{self.service_url}/api/get_project_status",
                params={"project_id": project_id},
                timeout=5
            )
            if response.status_code != 200:
                logger.error("项目状态查询失败")
                return False
        except Exception as e:
            logger.error(f"项目状态查询出错: {str(e)}")
            return False
        
        logger.info("✅ API端点测试通过")
        return True
    
    def test_skills(self) -> bool:
        """测试技能功能"""
        logger.info("🛠️ 测试技能功能...")
        
        try:
            # 导入核心引擎
            sys.path.append(str(self.agent_dir))
            from core_engine import GroundedTheoryEngine
            
            engine = GroundedTheoryEngine()
            
            # 测试请求分析
            test_requests = [
                "我需要分析访谈数据进行开放编码",
                "请帮我检查理论饱和度",
                "导师让我明天交轴心编码结果"
            ]
            
            for request in test_requests:
                context, strategy = engine.analyze_user_request(request, "test_user")
                
                # 验证上下文
                if not context or not strategy:
                    logger.error(f"请求分析失败: {request}")
                    return False
                
                # 验证策略
                if not strategy.skills_to_use:
                    logger.error(f"技能调度失败: {request}")
                    return False
            
            logger.info("✅ 技能功能测试通过")
            return True
            
        except Exception as e:
            logger.error(f"技能测试出错: {str(e)}")
            return False
    
    def test_integration(self) -> bool:
        """测试集成功能"""
        logger.info("🔗 测试集成功能...")
        
        try:
            # 测试完整的用户流程
            # 1. 启动会话
            response = requests.post(
                f"{self.service_url}/api/start_session",
                json={"request": "我需要分析10份访谈数据进行开放编码"},
                timeout=10
            )
            
            if response.status_code != 200:
                return False
            
            data = response.json()
            session_id = data.get("session_id")
            project_id = data.get("project_id")
            
            # 2. 模拟文本上传
            test_text = "这是一个测试访谈文本。受访者表示他们在学习过程中遇到了很多困难，但通过寻求帮助和建立学习习惯，最终克服了这些挑战。"
            
            # 创建测试文件
            test_file_path = self.config["test_data_dir"] / "test_interview.txt"
            test_file_path.parent.mkdir(exist_ok=True)
            
            with open(test_file_path, 'w', encoding='utf-8') as f:
                f.write(test_text)
            
            # 3. 上传文件
            with open(test_file_path, 'rb') as f:
                files = {'text_file': f}
                data = {
                    'session_id': session_id,
                    'project_id': project_id
                }
                
                response = requests.post(
                    f"{self.service_url}/api/upload_text",
                    files=files,
                    data=data,
                    timeout=10
                )
                
                if response.status_code != 200:
                    logger.error("文件上传失败")
                    return False
            
            # 4. 执行技能
            response = requests.post(
                f"{self.service_url}/api/execute_skill",
                json={
                    "session_id": session_id,
                    "project_id": project_id,
                    "skill_name": "performing-open-coding",
                    "input_data": {}
                },
                timeout=15
            )
            
            if response.status_code != 200:
                logger.error("技能执行失败")
                return False
            
            result = response.json()
            if not result.get("success"):
                logger.error("技能执行返回失败")
                return False
            
            logger.info("✅ 集成功能测试通过")
            return True
            
        except Exception as e:
            logger.error(f"集成测试出错: {str(e)}")
            return False
    
    def deploy(self) -> bool:
        """执行完整部署流程"""
        logger.info("🚀 开始部署扎根理论智能体...")
        
        # 1. 检查依赖
        if not self.check_dependencies():
            return False
        
        # 2. 安装依赖
        if not self.install_dependencies():
            return False
        
        # 3. 启动服务
        if not self.start_service():
            return False
        
        # 4. 运行测试
        if not self.run_tests():
            logger.warning("⚠️ 部分测试失败，但服务已启动")
        
        logger.info("🎉 部署完成！")
        logger.info(f"📱 访问地址: {self.service_url}")
        logger.info("🔧 使用 Ctrl+C 停止服务")
        
        return True
    
    def cleanup(self):
        """清理资源"""
        logger.info("🧹 清理部署资源...")
        self.stop_service()

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="扎根理论智能体部署脚本")
    parser.add_argument("--project-root", default=".", help="项目根目录路径")
    parser.add_argument("--test-only", action="store_true", help="仅运行测试")
    parser.add_argument("--clean", action="store_true", help="清理资源")
    
    args = parser.parse_args()
    
    # 获取项目根目录
    project_root = os.path.abspath(args.project_root)
    
    # 创建部署器
    deployer = AgentDeployer(project_root)
    
    try:
        if args.clean:
            deployer.cleanup()
            return
        
        if args.test_only:
            # 仅运行测试
            if deployer.check_dependencies() and deployer.start_service():
                deployer.run_tests()
                deployer.stop_service()
        else:
            # 完整部署
            deployer.deploy()
            
            # 保持服务运行
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("👋 用户中断，正在停止服务...")
                deployer.cleanup()
    
    except Exception as e:
        logger.error(f"❌ 部署失败: {str(e)}")
        deployer.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()