#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSCI智能部署系统
一键部署、智能检测、自动配置所有技能
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path
from typing import Dict, List, Optional
import argparse

class SmartDeployer:
    """智能部署器"""

    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.skills_dir = self.root_dir / "skills"
        self.system_info = self._get_system_info()
        self.available_skills = self._discover_skills()

    def _get_system_info(self) -> Dict:
        """获取系统信息"""
        return {
            "platform": platform.system(),
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
            "arch": platform.machine(),
            "uv_available": self._check_command("uv"),
            "pip_available": self._check_command("pip"),
            "git_available": self._check_command("git")
        }

    def _check_command(self, cmd: str) -> bool:
        """检查命令是否可用"""
        try:
            subprocess.run([cmd, "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def _discover_skills(self) -> List[Dict]:
        """发现所有可用技能"""
        skills = []

        if not self.skills_dir.exists():
            return skills

        for skill_dir in self.skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_info = self._analyze_skill(skill_dir)
                if skill_info:
                    skills.append(skill_info)

        return skills

    def _get_category(self, category_name: str) -> str:
        """获取技能分类的中文名称"""
        category_mapping = {
            "coding": "编码分析",
            "analysis": "数据分析",
            "theory": "理论分析",
            "theory-saturation": "理论分析",
            "methodology": "方法论",
            "mathematical-statistics": "数理统计",
            "network-computation": "网络计算",
            "validity-reliability": "信效度检验",
            "conflict-resolution": "冲突分析"
        }
        return category_mapping.get(category_name, "其他工具")

    def _analyze_skill(self, skill_dir: Path) -> Optional[Dict]:
        """分析单个技能"""
        skill_name = skill_dir.name

        # 查找技能文件
        skill_files = list(skill_dir.rglob("SKILL.md"))
        if not skill_files:
            return None

        # 分析依赖
        pyproject_path = skill_dir / "pyproject.toml"
        dependencies = []

        if pyproject_path.exists():
            try:
                with open(pyproject_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'dependencies' in content:
                        # 简单解析dependencies
                        start = content.find('dependencies = [')
                        if start != -1:
                            end = content.find(']', start)
                            deps_section = content[start:end]
                            for line in deps_section.split('\n'):
                                if 'jieba' in line:
                                    dependencies.append('jieba')
                                if 'networkx' in line:
                                    dependencies.append('networkx')
                                if 'pandas' in line:
                                    dependencies.append('pandas')
                                if 'numpy' in line:
                                    dependencies.append('numpy')
            except Exception:
                pass

        # 处理skill_files路径，避免relative_to错误
        skill_files_str = []
        for f in skill_files:
            try:
                skill_files_str.append(str(f.relative_to(self.root_dir)))
            except ValueError:
                skill_files_str.append(str(f))

        return {
            "name": skill_name,
            "path": str(skill_dir),
            "dependencies": dependencies,
            "skill_files": skill_files_str,
            "has_jieba": 'jieba' in dependencies,
            "needs_chinese": any(dep in ['jieba'] for dep in dependencies)
        }

    def run_diagnostics(self) -> Dict:
        """运行诊断"""
        print("🔍 系统诊断中...")

        # 转换Path对象为字符串
        serializable_skills = []
        for skill in self.available_skills:
            serializable_skills.append({
                "name": skill["name"],
                "path": str(skill["path"]),
                "dependencies": skill["dependencies"],
                "skill_files": [str(f) for f in skill["skill_files"]],
                "has_jieba": skill["has_jieba"],
                "needs_chinese": skill["needs_chinese"]
            })

        diagnostics = {
            "system": self.system_info,
            "skills": serializable_skills,
            "issues": [],
            "recommendations": []
        }

        # 检查Python版本
        if sys.version_info < (3, 8):
            diagnostics["issues"].append("Python版本过低，需要3.8+")

        # 检查包管理器
        if not self.system_info["uv_available"] and not self.system_info["pip_available"]:
            diagnostics["issues"].append("缺少包管理器 (uv 或 pip)")

        # 检查技能依赖
        for skill in self.available_skills:
            if skill["needs_chinese"] and not self._check_dependency("jieba"):
                diagnostics["issues"].append(f"技能 {skill['name']} 需要jieba但未安装")

        # 生成建议
        if self.system_info["uv_available"]:
            diagnostics["recommendations"].append("建议使用uv进行包管理 (更快更稳定)")

        return diagnostics

    def _check_dependency(self, dep: str) -> bool:
        """检查依赖是否安装"""
        try:
            __import__(dep)
            return True
        except ImportError:
            return False

    def deploy_smart(self, force_reinstall: bool = False) -> bool:
        """智能部署"""
        print("🚀 开始智能部署...")

        # 1. 系统检查
        diagnostics = self.run_diagnostics()

        if diagnostics["issues"]:
            print("❌ 发现问题:")
            for issue in diagnostics["issues"]:
                print(f"  - {issue}")
            return False

        # 2. 选择最佳包管理器
        package_manager = "uv" if self.system_info["uv_available"] else "pip"
        print(f"📦 使用包管理器: {package_manager}")

        # 3. 安装全局依赖
        success = self._install_global_dependencies(package_manager, force_reinstall)
        if not success:
            return False

        # 4. 安装技能依赖
        for skill in self.available_skills:
            if skill["dependencies"]:
                print(f"🔧 配置技能: {skill['name']}")
                self._install_skill_dependencies(skill, package_manager, force_reinstall)

        # 5. 初始化特殊配置
        self._initialize_special_configurations()

        print("✅ 智能部署完成!")
        return True

    def _install_global_dependencies(self, package_manager: str, force: bool) -> bool:
        """安装全局依赖"""
        print("📥 安装全局依赖...")

        try:
            if package_manager == "uv":
                if force or not self._check_dependency("jieba"):
                    subprocess.run(["uv", "sync"], check=True)
                else:
                    print("  ✓ 依赖已存在")
            else:
                req_file = self.root_dir / "requirements.txt"
                if req_file.exists():
                    if force:
                        subprocess.run([
                            sys.executable, "-m", "pip", "install", "-r", str(req_file)
                        ], check=True)
                    else:
                        print("  ✓ 依赖已存在")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 安装失败: {e}")
            return False

    def _install_skill_dependencies(self, skill: Dict, package_manager: str, force: bool) -> bool:
        """安装技能依赖"""
        skill_path = skill["path"]
        pyproject_path = skill_path / "pyproject.toml"

        if not pyproject_path.exists():
            return True

        try:
            os.chdir(skill_path)

            if package_manager == "uv":
                if force or skill["has_jieba"]:
                    subprocess.run(["uv", "sync"], check=True)

                # 初始化jieba (如果需要)
                if skill["has_jieba"]:
                    init_script = skill_path / "scripts" / "init_jieba.py"
                    if init_script.exists():
                        subprocess.run([sys.executable, str(init_script)], check=True)
            else:
                if force or skill["has_jieba"]:
                    subprocess.run([
                        sys.executable, "-m", "pip", "install", "-e", "."
                    ], check=True)

            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 技能 {skill['name']} 配置失败: {e}")
            return False
        finally:
            os.chdir(self.root_dir)

    def _initialize_special_configurations(self):
        """初始化特殊配置"""
        print("⚙️ 初始化特殊配置...")

        # 创建Claude技能目录结构
        claude_skills_dir = Path.home() / ".claude" / "skills"
        claude_skills_dir.mkdir(parents=True, exist_ok=True)

        # 创建OpenSkills配置
        openskills_dir = Path.home() / ".openskills"
        openskills_dir.mkdir(parents=True, exist_ok=True)

        print("  ✓ Claude技能目录已准备")
        print("  ✓ OpenSkills配置已准备")

    def generate_usage_guide(self) -> str:
        """生成使用指南"""
        guide = []
        guide.append("# 🎯 SSCI技能使用指南\n")
        guide.append(f"**系统信息**: {self.system_info['platform']} Python {self.system_info['python_version']}\n")
        guide.append("## 📚 可用技能\n")

        for skill in self.available_skills:
            guide.append(f"### {skill['name'].replace('-', ' ').title()}")
            guide.append(f"- 路径: `{skill['path']}`")
            guide.append(f"- 依赖: {', '.join(skill['dependencies']) if skill['dependencies'] else '无'}")

            # 添加使用示例
            if "open-coding" in skill["name"]:
                guide.extend([
                    "\n#### 使用方法:",
                    "```bash",
                    "# 中文文本预处理",
                    "python skills/coding/open-coding/scripts/preprocess.py --input interview.txt",
                    "",
                    "# 概念提取",
                    "python skills/coding/open-coding/scripts/extract_concepts.py --input preprocessed.json",
                    "",
                    "# 编码比较",
                    "python skills/coding/open-coding/scripts/compare_codes.py --input codes.json",
                    "```"
                ])
            elif "centrality-analysis" in skill["name"]:
                guide.extend([
                    "\n#### 使用方法:",
                    "```bash",
                    "# 网络中心性分析",
                    "python skills/analysis/centrality-analysis/scripts/centrality.py --input network.json",
                    "```"
                ])
            elif "theory-saturation" in skill["name"]:
                guide.extend([
                    "\n#### 使用方法:",
                    "```bash",
                    "# 理论饱和度检验",
                    "python skills/coding/theory-saturation/scripts/assess_saturation.py --data-dir data/",
                    "```"
                ])

            guide.append("")

        # 添加Claude Skills集成
        guide.extend([
            "## 🤖 Claude Skills集成",
            "```bash",
            "# 复制技能到Claude目录",
            "cp -r skills/* ~/.claude/skills/",
            "",
            "# 在Claude中使用:",
            "# \"请帮我进行中文开放编码分析\"",
            "# \"分析这个网络的中心性\"",
            "# 检查理论是否达到饱和",
            "```",
            "",
            "## 📦 OpenSkills集成",
            "```bash",
            "# 安装到OpenSkills",
            "openskills install . --local",
            "",
            "# 同步技能",
            "openskills sync",
            "",
            "# 使用技能",
            "openskills read open-coding",
            "```",
            "",
            "## 🧪 测试验证",
            "```bash",
            "# 运行所有测试",
            "python -m pytest tests/ -v",
            "",
            "# 测试特定技能",
            "python -m pytest tests/unit/test_open_coding_tools.py -v",
            "```"
        ])

        return "\n".join(guide)

    def create_quick_start_script(self) -> str:
        """创建快速启动脚本"""
        script_content = []

        if self.system_info["platform"] == "Windows":
            script_content.extend([
                "@echo off",
                "echo 🚀 SSCI技能快速启动",
                "echo ===================",
                "",
                "REM 检查Python",
                "python --version",
                "if errorlevel 1 (",
                "    echo ❌ Python未安装或不在PATH中",
                "    pause",
                "    exit /b 1",
                ")",
                "",
                "REM 检查技能目录",
                "if not exist skills (",
                "    echo ❌ 技能目录不存在",
                "    pause",
                "    exit /b 1",
                ")",
                "",
                "REM 选择操作",
                "echo 1. 运行诊断",
                "echo 2. 智能部署",
                "echo 3. 运行测试",
                "echo 4. 查看使用指南",
                "set /p choice=请选择操作 (1-4): ",
                "",
                "if \"%choice%\"==\"1\" (",
                "    python smart_deploy.py --diagnose",
                ") else if \"%choice%\"==\"2\" (",
                "    python smart_deploy.py --deploy",
                ") else if \"%choice%\"==\"3\" (",
                "    python -m pytest tests/ -v",
                ") else if \"%choice%\"==\"4\" (",
                "    python smart_deploy.py --guide",
                ") else (",
                "    echo 无效选择",
                ")",
                "",
                "pause"
            ])
        else:
            script_content.extend([
                "#!/bin/bash",
                "echo \"🚀 SSCI技能快速启动\"",
                "echo \"===================",
                "",
                "# 检查Python",
                "if ! command -v python3 &> /dev/null; then",
                "    echo \"❌ Python未安装\"",
                "    exit 1",
                "fi",
                "",
                "python3 --version",
                "",
                "# 检查技能目录",
                "if [ ! -d \"skills\" ]; then",
                "    echo \"❌ 技能目录不存在\"",
                "    exit 1",
                "fi",
                "",
                "# 选择操作",
                "echo \"1. 运行诊断\"",
                "echo \"2. 智能部署\"",
                "echo \"3. 运行测试\"",
                "echo \"4. 查看使用指南\"",
                "read -p \"请选择操作 (1-4): \" choice",
                "",
                "case $choice in",
                "    1) python3 smart_deploy.py --diagnose ;;",
                "    2) python3 smart_deploy.py --deploy ;;",
                "    3) python3 -m pytest tests/ -v ;;",
                "    4) python3 smart_deploy.py --guide ;;",
                "    *) echo \"无效选择\" ;;",
                "esac"
            ])

        return "\n".join(script_content)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='SSCI智能部署系统')
    parser.add_argument('--diagnose', action='store_true', help='运行系统诊断')
    parser.add_argument('--deploy', action='store_true', help='智能部署所有技能')
    parser.add_argument('--guide', action='store_true', help='生成使用指南')
    parser.add_argument('--quick-start', action='store_true', help='创建快速启动脚本')
    parser.add_argument('--force', action='store_true', help='强制重新安装')

    args = parser.parse_args()

    deployer = SmartDeployer()

    if args.diagnose:
        diagnostics = deployer.run_diagnostics()
        print(json.dumps(diagnostics, indent=2, ensure_ascii=False))

    elif args.deploy:
        success = deployer.deploy_smart(args.force)
        if success:
            print("\n🎉 部署成功!")
            print("💡 运行 'python smart_deploy.py --guide' 查看使用指南")
        else:
            print("\n❌ 部署失败!")
            sys.exit(1)

    elif args.guide:
        guide = deployer.generate_usage_guide()
        print(guide)

        # 保存到文件
        with open("USAGE_GUIDE.md", "w", encoding="utf-8") as f:
            f.write(guide)
        print("\n📖 使用指南已保存到: USAGE_GUIDE.md")

    elif args.quick_start:
        script = deployer.create_quick_start_script()
        script_name = "quick_start.bat" if platform.system() == "Windows" else "quick_start.sh"

        with open(script_name, "w", encoding="utf-8") as f:
            f.write(script)

        if platform.system() != "Windows":
            os.chmod(script_name, 0o755)

        print(f"🚀 快速启动脚本已创建: {script_name}")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()