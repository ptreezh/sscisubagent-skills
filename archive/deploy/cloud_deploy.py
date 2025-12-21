#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云平台部署脚本
支持Railway.app、Heroku等平台
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CloudDeployer:
    """云平台部署器"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.platforms = {
            "railway": {
                "name": "Railway.app",
                "cli": "railway",
                "config_file": "railway.toml",
                "free_tier": True
            },
            "heroku": {
                "name": "Heroku",
                "cli": "heroku",
                "config_file": "Procfile",
                "free_tier": False
            },
            "vercel": {
                "name": "Vercel",
                "cli": "vercel",
                "config_file": "vercel.json",
                "free_tier": True
            }
        }
    
    def check_platform_cli(self, platform: str) -> bool:
        """检查平台CLI工具"""
        platform_info = self.platforms.get(platform)
        if not platform_info:
            logger.error(f"❌ 不支持的平台: {platform}")
            return False
        
        cli_name = platform_info["cli"]
        logger.info(f"🔍 检查{platform_info['name']} CLI...")
        
        try:
            result = subprocess.run([cli_name, "--version"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✅ {platform_info['name']} CLI已安装")
                logger.info(f"   {result.stdout.strip()}")
                return True
            else:
                logger.error(f"❌ {platform_info['name']} CLI未安装")
                return False
        except FileNotFoundError:
            logger.error(f"❌ {cli_name}命令未找到")
            return False
    
    def install_platform_cli(self, platform: str) -> bool:
        """安装平台CLI工具"""
        platform_info = self.platforms.get(platform)
        if not platform_info:
            return False
        
        cli_name = platform_info["cli"]
        logger.info(f"📦 安装{platform_info['name']} CLI...")
        
        install_commands = {
            "railway": "npm install -g @railway/cli",
            "heroku": "npm install -g heroku",
            "vercel": "npm install -g vercel"
        }
        
        try:
            cmd = install_commands.get(platform)
            if not cmd:
                logger.error(f"❌ 不支持的安装命令: {platform}")
                return False
            
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            if result.returncode == 0:
                logger.info(f"✅ {platform_info['name']} CLI安装成功")
                return True
            else:
                logger.error(f"❌ 安装失败: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"❌ 安装过程出错: {str(e)}")
            return False
    
    def prepare_project(self, platform: str) -> bool:
        """准备项目文件"""
        platform_info = self.platforms.get(platform)
        if not platform_info:
            return False
        
        logger.info(f"📋 准备{platform_info['name']}部署文件...")
        
        config_file = self.project_root / platform_info["config_file"]
        if not config_file.exists():
            logger.error(f"❌ 配置文件不存在: {config_file}")
            return False
        
        # 检查requirements文件
        requirements_file = self.project_root / "requirements-docker.txt"
        if not requirements_file.exists():
            logger.error("❌ requirements-docker.txt不存在")
            return False
        
        logger.info("✅ 项目文件准备完成")
        return True
    
    def deploy_to_railway(self) -> bool:
        """部署到Railway.app"""
        logger.info("🚀 部署到Railway.app...")
        
        try:
            # 登录检查
            logger.info("🔐 检查Railway登录状态...")
            result = subprocess.run(["railway", "status"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.info("🔑 需要登录Railway...")
                subprocess.run(["railway", "login"])
            
            # 初始化项目
            logger.info("📦 初始化Railway项目...")
            result = subprocess.run(["railway", "init"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("❌ 项目初始化失败")
                return False
            
            # 部署
            logger.info("🚀 开始部署...")
            result = subprocess.run(["railway", "up"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Railway部署成功")
                
                # 获取项目URL
                result = subprocess.run(["railway", "domain"], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    logger.info(f"🌐 项目URL: {result.stdout.strip()}")
                
                return True
            else:
                logger.error(f"❌ 部署失败: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 部署过程出错: {str(e)}")
            return False
    
    def deploy_to_heroku(self) -> bool:
        """部署到Heroku"""
        logger.info("🚀 部署到Heroku...")
        
        try:
            # 登录检查
            logger.info("🔐 检查Heroku登录状态...")
            result = subprocess.run(["heroku", "auth:whoami"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.info("🔑 需要登录Heroku...")
                subprocess.run(["heroku", "login"])
            
            # 创建应用
            app_name = f"grounded-theory-{int(time.time())}"
            logger.info(f"📦 创建Heroku应用: {app_name}")
            
            result = subprocess.run(["heroku", "create", app_name], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.error("❌ 应用创建失败")
                return False
            
            # 设置环境变量
            logger.info("⚙️ 设置环境变量...")
            subprocess.run(["heroku", "config:set", 
                          f"PYTHONPATH=/app", "--app", app_name])
            
            # 部署
            logger.info("🚀 开始部署...")
            result = subprocess.run(["git", "push", "heroku", "main"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Heroku部署成功")
                
                # 获取应用URL
                result = subprocess.run(["heroku", "info", "--app", app_name], 
                                      capture_output=True, text=True)
                if "Web URL:" in result.stdout:
                    for line in result.stdout.split('\n'):
                        if "Web URL:" in line:
                            url = line.split("Web URL:")[1].strip()
                            logger.info(f"🌐 应用URL: {url}")
                            break
                
                return True
            else:
                logger.error(f"❌ 部署失败: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 部署过程出错: {str(e)}")
            return False
    
    def deploy_to_vercel(self) -> bool:
        """部署到Vercel"""
        logger.info("🚀 部署到Vercel...")
        
        try:
            # 登录检查
            logger.info("🔐 检查Vercel登录状态...")
            result = subprocess.run(["vercel", "whoami"], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                logger.info("🔑 需要登录Vercel...")
                subprocess.run(["vercel", "login"])
            
            # 部署
            logger.info("🚀 开始部署...")
            result = subprocess.run(["vercel", "--prod"], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info("✅ Vercel部署成功")
                
                # 提取URL
                for line in result.stdout.split('\n'):
                    if "https://" in line and "vercel.app" in line:
                        logger.info(f"🌐 部署URL: {line.strip()}")
                        break
                
                return True
            else:
                logger.error(f"❌ 部署失败: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"❌ 部署过程出错: {str(e)}")
            return False
    
    def deploy(self, platform: str) -> bool:
        """执行部署"""
        platform_info = self.platforms.get(platform)
        if not platform_info:
            logger.error(f"❌ 不支持的平台: {platform}")
            return False
        
        logger.info(f"🚀 开始部署到{platform_info['name']}...")
        
        # 1. 检查CLI工具
        if not self.check_platform_cli(platform):
            if not self.install_platform_cli(platform):
                return False
        
        # 2. 准备项目
        if not self.prepare_project(platform):
            return False
        
        # 3. 执行部署
        if platform == "railway":
            return self.deploy_to_railway()
        elif platform == "heroku":
            return self.deploy_to_heroku()
        elif platform == "vercel":
            return self.deploy_to_vercel()
        else:
            logger.error(f"❌ 不支持的平台: {platform}")
            return False
    
    def show_platform_info(self):
        """显示平台信息"""
        logger.info("📋 支持的云平台:")
        
        for platform, info in self.platforms.items():
            status = "✅ 免费" if info["free_tier"] else "💰 付费"
            logger.info(f"  {platform}: {info['name']} ({status})")
            logger.info(f"    CLI: {info['cli']}")
            logger.info(f"    配置: {info['config_file']}")
            logger.info("")

def main():
    """主函数"""
    import argparse
    import time
    
    parser = argparse.ArgumentParser(description="云平台部署脚本")
    parser.add_argument("--project-root", default=".", help="项目根目录")
    parser.add_argument("--platform", choices=["railway", "heroku", "vercel"], 
                       help="部署平台")
    parser.add_argument("--list", action="store_true", help="列出支持的平台")
    
    args = parser.parse_args()
    
    # 获取项目根目录
    project_root = os.path.abspath(args.project_root)
    
    # 创建部署器
    deployer = CloudDeployer(project_root)
    
    try:
        if args.list:
            deployer.show_platform_info()
            return
        
        if not args.platform:
            logger.error("❌ 请指定部署平台")
            deployer.show_platform_info()
            sys.exit(1)
        
        # 执行部署
        success = deployer.deploy(args.platform)
        
        if success:
            logger.info("🎉 部署完成！")
        else:
            logger.error("❌ 部署失败")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"❌ 部署过程出错: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()