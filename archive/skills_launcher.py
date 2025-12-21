#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SSCI技能启动器
提供友好的技能选择和使用界面
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import argparse

class SkillsLauncher:
    """技能启动器"""

    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.skills = self._load_skills()
        self.history_file = self.root_dir / ".skills_history.json"
        self.history = self._load_history()

    def _load_skills(self) -> Dict:
        """加载所有可用技能"""
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
                    scripts.append(script)

        return {
            "name": skill_dir.name,
            "path": skill_dir,
            "description": description,
            "scripts": scripts,
            "category": self._get_category(skill_dir.name)
        }

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

    def _load_history(self) -> List[Dict]:
        """加载使用历史"""
        if self.history_file.exists():
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return []
        return []

    def _save_history(self, usage: Dict):
        """保存使用历史"""
        self.history.append(usage)
        # 只保留最近20条记录
        self.history = self.history[-20:]

        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=2, ensure_ascii=False)

    def show_welcome(self):
        """显示欢迎界面"""
        print("""
🎯 SSCI中文学科研究技能包
======================

📚 专业研究工具为中文社会科学研究提供支持

🔧 可用技能分类:
""")
        # 按分类显示技能
        categories = {}
        for skill_name, skill_info in self.skills.items():
            category = skill_info["category"]
            if category not in categories:
                categories[category] = []
            categories[category].append(skill_info)

        for category, skill_list in categories.items():
            print(f"\n📖 {category}")
            for skill in skill_list:
                print(f"  • {skill['name']} - {skill['description']}")

        print(f"\n📈 总计: {len(self.skills)} 个专业技能")

    def interactive_menu(self):
        """交互式菜单"""
        while True:
            print("\n" + "="*50)
            print("🚀 选择操作:")
            print("1. 🎯 选择并运行技能")
            print("2. 📋 查看技能详情")
            print("3. 📊 查看使用历史")
            print("4. 🔍 搜索技能")
            print("5. 🛠️ 批量处理")
            print("6. ❓ 帮助说明")
            print("0. 🚪 退出")

            choice = input("\n请选择 (0-6): ").strip()

            if choice == "1":
                self.select_and_run_skill()
            elif choice == "2":
                self.show_skill_details()
            elif choice == "3":
                self.show_usage_history()
            elif choice == "4":
                self.search_skills()
            elif choice == "5":
                self.batch_processing()
            elif choice == "6":
                self.show_help()
            elif choice == "0":
                print("👋 感谢使用SSCI技能包!")
                break
            else:
                print("❌ 无效选择，请重试")

    def select_and_run_skill(self):
        """选择并运行技能"""
        print("\n🎯 可用技能:")

        # 显示技能列表
        skill_list = list(self.skills.items())
        for i, (name, info) in enumerate(skill_list, 1):
            print(f"{i:2d}. {name} - {info['description']}")

        try:
            choice = int(input(f"\n选择技能 (1-{len(skill_list)}): "))
            if 1 <= choice <= len(skill_list):
                skill_name, skill_info = skill_list[choice - 1]
                self.run_skill(skill_name, skill_info)
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入数字")

    def run_skill(self, skill_name: str, skill_info: Dict):
        """运行技能"""
        print(f"\n🔧 运行技能: {skill_name}")

        if not skill_info["scripts"]:
            print("❌ 该技能没有可执行脚本")
            return

        # 显示可用脚本
        print("\n📝 可用脚本:")
        for i, script in enumerate(skill_info["scripts"], 1):
            print(f"{i:2d}. {script.name}")

        try:
            script_choice = int(input(f"\n选择脚本 (1-{len(skill_info['scripts'])}): "))
            if 1 <= script_choice <= len(skill_info["scripts"]):
                script = skill_info["scripts"][script_choice - 1]
                self.run_script(script, skill_name)
            else:
                print("❌ 无效选择")
        except ValueError:
            print("❌ 请输入数字")

    def run_script(self, script: Path, skill_name: str):
        """运行脚本"""
        print(f"\n⚡ 执行: {script.name}")

        # 交互式参数收集
        if "preprocess" in script.name:
            self._run_preprocess_script(script)
        elif "centrality" in script.name:
            self._run_centrality_script(script)
        elif "saturation" in script.name:
            self._run_saturation_script(script)
        elif "extract" in script.name:
            self._run_extract_script(script)
        elif "compare" in script.name:
            self._run_compare_script(script)
        else:
            # 通用脚本执行
            self._run_generic_script(script)

        # 记录使用历史
        usage = {
            "skill": skill_name,
            "script": script.name,
            "timestamp": str(Path().absolute()),
            "success": True
        }
        self._save_history(usage)

    def _run_preprocess_script(self, script: Path):
        """运行预处理脚本"""
        input_file = input("📁 输入文件路径: ").strip()
        output_file = input("📤 输出文件路径 (回车默认): ").strip() or None

        cmd = [sys.executable, str(script), "--input", input_file]
        if output_file:
            cmd.extend(["--output", output_file])

        self._execute_command(cmd)

    def _run_centrality_script(self, script: Path):
        """运行中心性分析脚本"""
        input_file = input("📊 网络数据文件路径: ").strip()
        output_file = input("📤 报告输出路径 (回车默认): ").strip() or None

        cmd = [sys.executable, str(script), "--input", input_file]
        if output_file:
            cmd.extend(["--output", output_file])

        self._execute_command(cmd)

    def _run_saturation_script(self, script: Path):
        """运行饱和度检验脚本"""
        data_dir = input("📂 数据目录路径: ").strip()
        output_file = input("📤 报告输出路径 (回车默认): ").strip() or None

        cmd = [sys.executable, str(script), "--data-dir", data_dir]
        if output_file:
            cmd.extend(["--output", output_file])

        self._execute_command(cmd)

    def _run_extract_script(self, script: Path):
        """运行概念提取脚本"""
        input_file = input("📁 输入文件路径: ").strip()
        output_file = input("📤 输出文件路径 (回车默认): ").strip() or None

        cmd = [sys.executable, str(script), "--input", input_file]
        if output_file:
            cmd.extend(["--output", output_file])

        self._execute_command(cmd)

    def _run_compare_script(self, script: Path):
        """运行编码比较脚本"""
        input_file = input("📁 编码文件路径: ").strip()
        output_file = input("📤 输出文件路径 (回车默认): ").strip() or None

        cmd = [sys.executable, str(script), "--input", input_file]
        if output_file:
            cmd.extend(["--output", output_file])

        self._execute_command(cmd)

    def _run_generic_script(self, script: Path):
        """运行通用脚本"""
        print(f"💡 脚本参数: python {script} --help")
        custom_args = input("⚙️  自定义参数 (回车跳过): ").strip()

        cmd = [sys.executable, str(script)]
        if custom_args:
            cmd.extend(custom_args.split())

        self._execute_command(cmd)

    def _execute_command(self, cmd: List[str]):
        """执行命令"""
        print(f"🔄 执行命令: {' '.join(cmd)}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')

            if result.stdout:
                print("📤 输出:")
                print(result.stdout)

            if result.stderr:
                print("⚠️ 错误信息:")
                print(result.stderr)

            if result.returncode == 0:
                print("✅ 执行成功!")
            else:
                print(f"❌ 执行失败 (代码: {result.returncode})")

        except Exception as e:
            print(f"❌ 执行异常: {e}")

    def show_skill_details(self):
        """显示技能详情"""
        print("\n📋 技能详情:")

        for name, info in self.skills.items():
            print(f"\n🎯 {name}")
            print(f"📝 描述: {info['description']}")
            print(f"📂 路径: {info['path']}")
            print(f"🏷️  分类: {info['category']}")
            print(f"📜 脚本数量: {len(info['scripts'])}")

            if info['scripts']:
                print("📄 可用脚本:")
                for script in info['scripts']:
                    print(f"  • {script.name}")

    def show_usage_history(self):
        """显示使用历史"""
        if not self.history:
            print("\n📊 暂无使用历史")
            return

        print(f"\n📊 最近使用历史 (共{len(self.history)}条):")

        for i, record in enumerate(reversed(self.history[-10:]), 1):
            print(f"{i:2d}. {record['skill']} - {record['script']}")
            print(f"    🕐 时间: {record['timestamp']}")
            print(f"    ✅ 状态: {'成功' if record.get('success', True) else '失败'}")
            print()

    def search_skills(self):
        """搜索技能"""
        keyword = input("🔍 搜索关键词: ").strip().lower()

        if not keyword:
            print("❌ 请输入搜索关键词")
            return

        print(f"\n🔍 搜索结果: '{keyword}'")

        found_skills = []
        for name, info in self.skills.items():
            if (keyword in name.lower() or
                keyword in info['description'].lower() or
                keyword in info['category'].lower()):
                found_skills.append((name, info))

        if not found_skills:
            print("❌ 未找到匹配的技能")
            return

        for name, info in found_skills:
            print(f"🎯 {name}")
            print(f"📝 {info['description']}")
            print(f"🏷️  {info['category']}")
            print()

    def batch_processing(self):
        """批量处理"""
        print("\n🛠️ 批量处理模式")
        print("1. 📁 批量预处理文件")
        print("2. 📊 批量分析网络")
        print("3. 🔍 批量检查饱和度")

        choice = input("选择批量操作 (1-3): ").strip()

        if choice == "1":
            self._batch_preprocess()
        elif choice == "2":
            self._batch_centrality()
        elif choice == "3":
            self._batch_saturation()
        else:
            print("❌ 无效选择")

    def _batch_preprocess(self):
        """批量预处理"""
        input_dir = input("📂 输入目录: ").strip()
        output_dir = input("📤 输出目录: ").strip()

        if not os.path.exists(input_dir):
            print("❌ 输入目录不存在")
            return

        os.makedirs(output_dir, exist_ok=True)

        script = self.root_dir / "skills" / "coding" / "open-coding" / "scripts" / "preprocess.py"

        for file_path in Path(input_dir).glob("*.txt"):
            output_path = Path(output_dir) / f"{file_path.stem}_preprocessed.json"
            cmd = [sys.executable, str(script), "--input", str(file_path), "--output", str(output_path)]
            self._execute_command(cmd)

    def _batch_centrality(self):
        """批量中心性分析"""
        # 实现批量网络分析
        print("🔄 批量网络分析功能开发中...")

    def _batch_saturation(self):
        """批量饱和度检查"""
        # 实现批量饱和度检查
        print("🔄 批量饱和度检查功能开发中...")

    def show_help(self):
        """显示帮助"""
        help_text = """
📖 SSCI技能包使用帮助
==================

🎯 技能分类:
• 编码分析 - 中文文本开放编码、概念提取、编码优化
• 数据分析 - 网络中心性分析、统计分析
• 理论分析 - 理论饱和度检验、范畴分析

💡 使用技巧:
1. 📁 准备好数据文件 (支持txt, json, csv等格式)
2. 🎯 选择合适的技能和脚本
3. ⚙️ 根据提示输入参数
4. 📊 查看分析结果

📚 数据格式要求:
• 开放编码: 访谈文本文件 (.txt)
• 中心性分析: 网络数据文件 (.json)
• 饱和度检验: 编码数据目录

🔧 高级功能:
• 批量处理: 同时处理多个文件
• 使用历史: 查看之前的分析记录
• 智能搜索: 快速找到合适的技能

❓ 获取更多帮助:
• 查看技能文档: skills/*/SKILL.md
• 运行测试: python -m pytest tests/
• 智能部署: python smart_deploy.py --deploy
        """
        print(help_text)

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='SSCI技能启动器')
    parser.add_argument('--welcome', action='store_true', help='显示欢迎界面')
    parser.add_argument('--quick', action='store_true', help='快速启动最近使用的技能')

    args = parser.parse_args()

    launcher = SkillsLauncher()

    if args.welcome:
        launcher.show_welcome()
        return

    if args.quick and launcher.history:
        # 快速启动最近使用的技能
        last_usage = launcher.history[-1]
        skill_info = launcher.skills.get(last_usage['skill'])
        if skill_info:
            print(f"🚀 快速启动: {last_usage['skill']} - {last_usage['script']}")
            launcher.run_skill(last_usage['skill'], skill_info)
            return

    # 默认启动交互式菜单
    launcher.show_welcome()
    launcher.interactive_menu()

if __name__ == "__main__":
    main()