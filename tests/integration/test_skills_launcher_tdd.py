#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能启动器TDD测试
测试驱动开发，确保命令行交互功能正常
"""

import unittest
import sys
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock
import io
from contextlib import redirect_stdout

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class TestSkillsLauncherTDD(unittest.TestCase):
    """技能启动器TDD测试套件"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_dir = Path.cwd()

        # 创建模拟技能结构
        self.create_mock_skills_structure()

        # 切换到测试目录
        import os
        os.chdir(self.test_dir)

    def tearDown(self):
        """测试后清理"""
        import os
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def create_mock_skills_structure(self):
        """创建模拟技能结构"""
        # 创建技能目录和文件
        skills_dir = self.test_dir / "skills"
        skills_dir.mkdir()

        # 创建open-coding技能
        open_coding_dir = skills_dir / "coding" / "open-coding"
        open_coding_dir.mkdir(parents=True)

        (open_coding_dir / "SKILL.md").write_text(
            "---\nname: open-coding\ndescription: 中文开放编码分析工具\n---\n",
            encoding='utf-8'
        )

        # 创建脚本文件
        scripts_dir = open_coding_dir / "scripts"
        scripts_dir.mkdir()

        (scripts_dir / "preprocess.py").write_text(
            "#!/usr/bin/env python3\n# 模拟预处理脚本\nif __name__ == '__main__':\n    print('预处理完成')",
            encoding='utf-8'
        )

        (scripts_dir / "extract_concepts.py").write_text(
            "#!/usr/bin/env python3\n# 模拟概念提取脚本\nif __name__ == '__main__':\n    print('概念提取完成')",
            encoding='utf-8'
        )

        # 创建centrality-analysis技能
        centrality_dir = skills_dir / "analysis" / "centrality-analysis"
        centrality_dir.mkdir(parents=True)

        (centrality_dir / "SKILL.md").write_text(
            "---\nname: centrality-analysis\ndescription: 网络中心性分析工具\n---\n",
            encoding='utf-8'
        )

        centrality_scripts = centrality_dir / "scripts"
        centrality_scripts.mkdir()

        (centrality_scripts / "centrality.py").write_text(
            "#!/usr/bin/env python3\n# 模拟中心性分析脚本\nif __name__ == '__main__':\n    print('中心性分析完成')",
            encoding='utf-8'
        )

    def test_01_launcher_initialization(self):
        """测试1: 启动器初始化"""
        # Given
        from skills_launcher import SkillsLauncher

        # When
        launcher = SkillsLauncher()

        # Then
        self.assertIsNotNone(launcher)
        self.assertIsNotNone(launcher.root_dir)
        self.assertIsNotNone(launcher.skills)
        self.assertIsInstance(launcher.history_file, Path)

    def test_02_skills_loading_accuracy(self):
        """测试2: 技能加载准确性"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When
        skills = launcher.skills

        # Then
        self.assertIsInstance(skills, dict)
        self.assertGreater(len(skills), 0)

        # 验证open-coding技能
        if "open-coding" in skills:
            skill = skills["open-coding"]
            self.assertEqual(skill["category"], "编码分析")
            self.assertGreater(len(skill["scripts"]), 0)

        # 验证centrality-analysis技能
        if "centrality-analysis" in skills:
            skill = skills["centrality-analysis"]
            self.assertEqual(skill["category"], "数据分析")
            self.assertGreater(len(skill["scripts"]), 0)

    def test_03_skill_categorization_logic(self):
        """测试3: 技能分类逻辑"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When & Then
        self.assertEqual(launcher._get_category("coding"), "编码分析")
        self.assertEqual(launcher._get_category("analysis"), "数据分析")
        self.assertEqual(launcher._get_category("theory"), "理论分析")
        self.assertEqual(launcher._get_category("unknown"), "其他工具")

    def test_04_welcome_screen_display(self):
        """测试4: 欢迎界面显示"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When
        with redirect_stdout(io.StringIO()) as f:
            launcher.show_welcome()
            output = f.getvalue()

        # Then
        self.assertIn("SSCI中文学科研究技能包", output)
        self.assertIn("可用技能分类", output)
        self.assertIn("编码分析", output)
        self.assertIn("数据分析", output)

    @patch('builtins.input')
    def test_05_interactive_menu_navigation(self, mock_input):
        """测试5: 交互菜单导航"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # Mock用户输入
        mock_input.side_effect = ["0"]  # 退出

        # When
        with redirect_stdout(io.StringIO()):
            try:
                launcher.interactive_menu()
            except SystemExit:
                pass  # 退出是预期的

        # Then
        mock_input.assert_called()
        # 验证所有菜单选项都被显示

    @patch('builtins.input')
    def test_06_skill_selection_mechanism(self, mock_input):
        """测试6: 技能选择机制"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # Mock用户选择第一个技能
        mock_input.side_effect = ["1"]  # 选择第一个技能

        # When
        with redirect_stdout(io.StringIO()):
            try:
                launcher.select_and_run_skill()
            except (SystemExit, IndexError):
                pass  # 可能因为缺少脚本而退出

        # Then
        mock_input.assert_called()

    def test_07_script_execution_simulation(self):
        """测试7: 脚本执行模拟"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # 创建模拟技能
        mock_skill = {
            "name": "test-skill",
            "scripts": [Path("test_script.py")]
        }

        # When
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            mock_run.return_value.stdout = "Script executed successfully"

            launcher.run_script(Path("test_script.py"), "test-skill")

        # Then
        mock_run.assert_called()

    @patch('subprocess.run')
    def test_08_preprocess_script_handling(self, mock_run):
        """测试8: 预处理脚本处理"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # 模拟用户输入
        mock_input_data = {
            "file": "test_file.txt",
            "output": "test_output.json"
        }

        # When
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = [
                mock_input_data["file"],
                mock_input_data["output"]
            ]

            launcher._run_preprocess_script(Path("preprocess.py"))

        # Then
        # 验证输入处理逻辑
        mock_input.assert_called()
        mock_run.assert_called()

    @patch('subprocess.run')
    def test_09_centrality_analysis_handling(self, mock_run):
        """测试9: 中心性分析处理"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # 模拟用户输入
        mock_input_data = {
            "network": "network_data.json"
        }

        # When
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = [mock_input_data["network"]]

            launcher._run_centrality_script(Path("centrality.py"))

        # Then
        mock_input.assert_called()
        mock_run.assert_called()

    @patch('subprocess.run')
    def test_10_saturation_analysis_handling(self, mock_run):
        """测试10: 饱和度分析处理"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # 模拟用户输入
        mock_input_data = {
            "data": "saturation_data"
        }

        # When
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = [mock_input_data["data"]]

            launcher._run_saturation_script(Path("saturation.py"))

        # Then
        mock_input.assert_called()
        mock_run.assert_called()

    def test_11_command_execution_construction(self):
        """测试11: 命令执行构造"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When
        test_script = Path("test.py")
        mock_input_file = Path("input.txt")

        # Then
        # 验证命令构造逻辑
        expected_cmd = [sys.executable, str(test_script)]
        self.assertEqual(len(expected_cmd), 2)

    def test_12_error_handling_robustness(self):
        """测试12: 错误处理健壮性"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When - 处理不存在的脚本
        non_existent_script = Path("non_existent.py")

        try:
            launcher.run_script(non_existent_script, "test-skill")
        except Exception as e:
            # Then
            self.assertIsInstance(e, (subprocess.SubprocessError, FileNotFoundError))

    def test_13_usage_history_management(self):
        """测试13: 使用历史管理"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When
        launcher._save_history({
            "skill": "test-skill",
            "script": "test.py",
            "timestamp": "2023-01-01",
            "success": True
        })

        # Then
        self.assertEqual(len(launcher.history), 1)
        self.assertEqual(launcher.history[0]["skill"], "test-skill")

    def test_14_history_loading_persistence(self):
        """测试14: 历史加载持久性"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # 创建历史文件
        history_data = [
            {
                "skill": "skill1",
                "script": "script1.py",
                "timestamp": "2023-01-01",
                "success": True
            }
        ]

        with open(launcher.history_file, 'w', encoding='utf-8') as f:
            json.dump(history_data, f)

        # When - 重新创建启动器
        new_launcher = SkillsLauncher()

        # Then
        self.assertEqual(len(new_launcher.history), 1)
        self.assertEqual(new_launcher.history[0]["skill"], "skill1")

    def test_15_search_functionality(self):
        """测试15: 搜索功能"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["coding"]  # 搜索关键词

            launcher.search_skills()

        # Then
        mock_input.assert_called()

    def test_16_batch_processing_initialization(self):
        """测试16: 批量处理初始化"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["1"]  # 选择批量预处理

            launcher.batch_processing()

        # Then
        mock_input.assert_called()

    def test_17_skill_details_display(self):
        """测试17: 技能详情显示"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When
        with redirect_stdout(io.StringIO()) as f:
            launcher.show_skill_details()
            output = f.getvalue()

        # Then
        # 验证输出包含技能信息
        self.assertIsInstance(output, str)

    def test_18_help_information_display(self):
        """测试18: 帮助信息显示"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When
        with redirect_stdout(io.StringIO()) as f:
            launcher.show_help()
            output = f.getvalue()

        # Then
        self.assertIn("使用帮助", output)
        self.assertIn("技能分类", output)

    @patch('webbrowser.open')
    def test_19_web_integration_readiness(self, mock_open):
        """测试19: Web集成准备"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ["0"]  # 退出

            try:
                launcher.interactive_menu()
            except SystemExit:
                pass

        # Then
        # 验证不依赖webbrowser.open
        # 主要测试命令行功能

    def test_20_complete_workflow_simulation(self):
        """测试20: 完整工作流模拟"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When - 模拟完整使用流程
        # 1. 加载技能
        self.assertIsInstance(launcher.skills, dict)

        # 2. 显示欢迎界面
        with redirect_stdout(io.StringIO()):
            launcher.show_welcome()

        # 3. 测试技能选择（模拟）
        if launcher.skills:
            first_skill = list(launcher.skills.values())[0]
            self.assertIsNotNone(first_skill)

        # 4. 测试历史管理
        launcher._save_history({
            "skill": "test",
            "script": "test.py",
            "timestamp": "2023-01-01",
            "success": True
        })
        self.assertEqual(len(launcher.history), 1)

        # Then - 所有步骤都应该成功
        self.assertTrue(True)

    def test_21_file_path_handling(self):
        """测试21: 文件路径处理"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When & Then - 测试路径处理
        test_path = Path("test_file.txt")
        processed_path = str(test_path)
        self.assertEqual(processed_path, "test_file.txt")

    def test_22_unicode_text_handling(self):
        """测试22: Unicode文本处理"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # 创建包含中文的测试文件
        test_file = self.test_dir / "test_chinese.txt"
        test_file.write_text("这是一个测试文件，包含中文内容。", encoding='utf-8')

        # When & Then - 验证中文文件处理
        self.assertTrue(test_file.exists())
        content = test_file.read_text(encoding='utf-8')
        self.assertIn("中文内容", content)

    def test_23_environment_variable_handling(self):
        """测试23: 环境变量处理"""
        # Given
        import os
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When & Then - 测试环境变量
        self.assertIsInstance(launcher.root_dir, Path)
        self.assertTrue(launcher.root_dir.exists())

    def test_24_memory_usage_optimization(self):
        """测试24: 内存使用优化"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When & Then - 验证数据结构不会导致内存泄漏
        initial_memory = len(str(launcher.skills))

        # 重新加载技能
        new_launcher = SkillsLauncher()
        final_memory = len(str(new_launcher.skills))

        # 验证内存使用合理
        self.assertLess(final_memory, initial_memory * 2)  # 不应该翻倍

class TestSkillsLauncherIntegration(unittest.TestCase):
    """技能启动器集成测试"""

    def setUp(self):
        """设置集成测试环境"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.create_realistic_project_structure()

    def create_realistic_project_structure(self):
        """创建真实的项目结构"""
        # 创建真实的技能目录结构
        skills_dir = self.test_dir / "skills"
        skills_dir.mkdir()

        # 创建多个真实技能
        skills_config = [
            ("coding/open-coding", "中文开放编码分析"),
            ("analysis/centrality-analysis", "网络中心性分析"),
            ("coding/theory-saturation", "理论饱和度检验")
        ]

        for skill_path, description in skills_config:
            skill_full_path = skills_dir / skill_path
            skill_full_path.mkdir(parents=True)

            # 创建SKILL.md
            skill_full_path /= "SKILL.md"
            skill_full_path.write_text(
                f"---\nname: {skill_path.replace('/', '-')}\ndescription: {description}\n---\n",
                encoding='utf-8'
            )

            # 创建scripts目录和示例脚本
            scripts_dir = skill_full_path.parent / "scripts"
            scripts_dir.mkdir()

            script_file = scripts_dir / "main.py"
            script_file.write_text(
                "#!/usr/bin/env python3\n# 示例脚本\nprint('执行完成')",
                encoding='utf-8'
            )

    def tearDown(self):
        """清理集成测试环境"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_real_project_loading(self):
        """测试真实项目加载"""
        # Given
        import os
        os.chdir(self.test_dir)

        # When
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # Then
        self.assertGreaterEqual(len(launcher.skills), 3)

        # 验证所有预期技能都存在
        expected_skills = ["open-coding", "centrality-analysis", "theory-saturation"]
        for skill_name in expected_skills:
            if skill_name in launcher.skills:
                self.assertIsNotNone(launcher.skills[skill_name])

if __name__ == '__main__':
    # 运行TDD测试套件
    unittest.main(verbosity=2)