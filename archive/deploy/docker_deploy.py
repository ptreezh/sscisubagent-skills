#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Docker部署脚本
自动化构建和部署Docker容器
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DockerDeployer:
    """Docker部署器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.dockerfile = self.project_root / "Dockerfile"
        self.compose_file = self.project_root / "docker-compose.yml"
        self.requirements_file = self.project_root / "requirements-docker.txt"
        
        # 配置
        self.image_name = "grounded-theory-agent"
        self.container_name = "grounded-theory-agent"
        self.port = 5000
    
    def check_docker(self) -> bool:
        """检查Docker环境"""
        logger.info("🐳 检查Docker环境...")
        
        try:
            # 检查Docker是否安装
            result = subprocess.run(["docker", "--version"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("❌ Docker未安装")
                return False
            
            logger.info(f"✅ {result.stdout.strip()}")
            
            # 检查Docker是否运行
            result = subprocess.run(["docker", "info"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("❌ Docker服务未运行")
                return False
            
            logger.info("✅ Docker服务正常运行")
            return True
            
        except FileNotFoundError:
            logger.error("❌ Docker命令未找到")
            return False
    
    def build_image(self) -> bool:
        """构建Docker镜像"""
        logger.info("🔨 构建Docker镜像...")
        
        try:
            # 构建镜像
            cmd = [
                "docker", "build",
                "-t", self.image_name,
                "-f", str(self.dockerfile),
                str(self.project_root)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ 镜像构建成功")
                return True
            else:
                logger.error(f"❌ 镜像构建失败: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 构建过程出错: {str(e)}")
            return False
    
    def run_container(self) -> bool:
        """运行Docker容器"""
        logger.info("🚀 启动Docker容器...")
        
        try:
            # 停止现有容器
            self.stop_container()
            
            # 创建必要的目录
            (self.project_root / "data").mkdir(exist_ok=True)
            (self.project_root / "logs").mkdir(exist_ok=True)
            (self.project_root / "uploads").mkdir(exist_ok=True)
            
            # 运行容器
            cmd = [
                "docker", "run", "-d",
                "--name", self.container_name,
                "-p", f"{self.port}:{self.port}",
                "-v", f"{self.project_root}/data:/app/data",
                "-v", f"{self.project_root}/logs:/app/logs",
                "-v", f"{self.project_root}/uploads:/app/uploads",
                "--restart", "unless-stopped",
                self.image_name
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                container_id = result.stdout.strip()
                logger.info(f"✅ 容器启动成功: {container_id}")
                return True
            else:
                logger.error(f"❌ 容器启动失败: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 启动过程出错: {str(e)}")
            return False
    
    def stop_container(self):
        """停止容器"""
        try:
            subprocess.run(["docker", "stop", self.container_name], 
                         capture_output=True)
            subprocess.run(["docker", "rm", self.container_name], 
                         capture_output=True)
            logger.info("✅ 现有容器已停止")
        except:
            pass
    
    def check_container_health(self) -> bool:
        """检查容器健康状态"""
        try:
            # 检查容器是否运行
            result = subprocess.run([
                "docker", "ps", "--filter", f"name={self.container_name}"
            ], capture_output=True, text=True)
            
            if self.container_name not in result.stdout:
                logger.error("❌ 容器未运行")
                return False
            
            # 检查健康状态
            result = subprocess.run([
                "docker", "inspect", 
                "--format='{{.State.Health.Status}}'",
                self.container_name
            ], capture_output=True, text=True)
            
            if "healthy" in result.stdout:
                logger.info("✅ 容器健康状态良好")
                return True
            else:
                logger.warning("⚠️ 容器健康检查中...")
                return True
                
        except Exception as e:
            logger.error(f"❌ 健康检查出错: {str(e)}")
            return False
    
    def deploy_with_compose(self) -> bool:
        """使用docker-compose部署"""
        logger.info("🐳 使用docker-compose部署...")
        
        try:
            # 检查compose文件
            if not self.compose_file.exists():
                logger.error("❌ docker-compose.yml不存在")
                return False
            
            # 启动服务
            cmd = ["docker-compose", "-f", str(self.compose_file), "up", "-d"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ docker-compose部署成功")
                return True
            else:
                logger.error(f"❌ docker-compose部署失败: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 部署过程出错: {str(e)}")
            return False
    
    def show_logs(self):
        """显示容器日志"""
        try:
            subprocess.run([
                "docker", "logs", "-f", self.container_name
            ])
        except KeyboardInterrupt:
            logger.info("📋 停止查看日志")
    
    def deploy(self, use_compose: bool = False) -> bool:
        """执行部署"""
        logger.info("🚀 开始Docker部署...")
        
        # 1. 检查Docker环境
        if not self.check_docker():
            return False
        
        # 2. 构建镜像
        if not self.build_image():
            return False
        
        # 3. 运行容器
        if use_compose:
            success = self.deploy_with_compose()
        else:
            success = self.run_container()
        
        if not success:
            return False
        
        # 4. 健康检查
        time.sleep(5)  # 等待容器启动
        if self.check_container_health():
            logger.info(f"🎉 部署成功！")
            logger.info(f"📱 访问地址: http://localhost:{self.port}")
            logger.info(f"📋 查看日志: docker logs -f {self.container_name}")
            return True
        else:
            logger.error("❌ 部署后健康检查失败")
            return False
    
    def cleanup(self):
        """清理资源"""
        logger.info("🧹 清理Docker资源...")
        
        try:
            # 停止并删除容器
            self.stop_container()
            
            # 删除镜像
            subprocess.run(["docker", "rmi", self.image_name], 
                         capture_output=True)
            
            logger.info("✅ 清理完成")
        except Exception as e:
            logger.error(f"❌ 清理过程出错: {str(e)}")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Docker部署脚本")
    parser.add_argument("--project-root", default=".", help="项目根目录")
    parser.add_argument("--compose", action="store_true", help="使用docker-compose")
    parser.add_argument("--logs", action="store_true", help="查看日志")
    parser.add_argument("--cleanup", action="store_true", help="清理资源")
    parser.add_argument("--stop", action="store_true", help="停止容器")
    
    args = parser.parse_args()
    
    # 获取项目根目录
    project_root = os.path.abspath(args.project_root)
    
    # 创建部署器
    deployer = DockerDeployer(project_root)
    
    try:
        if args.cleanup:
            deployer.cleanup()
            return
        
        if args.stop:
            deployer.stop_container()
            return
        
        if args.logs:
            deployer.show_logs()
            return
        
        # 执行部署
        success = deployer.deploy(use_compose=args.compose)
        
        if success:
            logger.info("✅ 部署完成，按Ctrl+C停止服务")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                logger.info("👋 用户中断，正在停止服务...")
                deployer.cleanup()
        else:
            logger.error("❌ 部署失败")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"❌ 部署过程出错: {str(e)}")
        deployer.cleanup()
        sys.exit(1)

if __name__ == "__main__":
    main()