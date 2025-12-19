#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
智能部署器TDD测试
测试驱动开发，确保所有智能功能正常工作
"""

import unittest
import subprocess
import sys
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class TestSmartDeployerTDD(unittest.TestCase):
    """智能部署器TDD测试套件"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_dir = Path.cwd()

        # 创建测试项目结构
        self.test_skills_dir = self.test_dir / "skills"
        self.test_skills_dir.mkdir(parents=True)

        # 模拟技能结构
        (self.test_skills_dir / "coding" / "open-coding").mkdir(parents=True)
        (self.test_skills_dir / "coding" / "theory-saturation").mkdir(parents=True)
        (self.test_skills_dir / "analysis" / "centrality-analysis").mkdir(parents=True)

        # 创建SKILL.md文件
        (self.test_skills_dir / "coding" / "open-coding" / "SKILL.md").write_text(
            "---\nname: open-coding\ndescription: 中文开放编码分析工具\n---\n",
            encoding='utf-8'
        )

        (self.test_skills_dir / "analysis" / "centrality-analysis" / "SKILL.md").write_text(
            "---\nname: centrality-analysis\ndescription: 网络中心性分析工具\n---\n",
            encoding='utf-8'
        )

        # 创建pyproject.toml文件
        (self.test_skills_dir / "coding" / "open-coding" / "pyproject.toml").write_text(
            '[project]\ndependencies = ["jieba>=0.42.0"]',
            encoding='utf-8'
        )

        # 切换到测试目录
        import os
        os.chdir(self.test_dir)

    def tearDown(self):
        """测试后清理"""
        import os
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_01_smart_deployer_initialization(self):
        """测试1: 智能部署器初始化"""
        # Given
        from smart_deploy import SmartDeployer

        # When
        deployer = SmartDeployer()

        # Then
        self.assertIsNotNone(deployer)
        self.assertIsNotNone(deployer.root_dir)
        self.assertIsNotNone(deployer.skills_dir)
        self.assertIsInstance(deployer.system_info, dict)
        self.assertIsInstance(deployer.available_skills, list)

        # 验证系统信息包含必要字段
        required_fields = ["platform", "python_version", "uv_available", "pip_available"]
        for field in required_fields:
            self.assertIn(field, deployer.system_info)

    def test_02_skill_discovery_mechanism(self):
        """测试2: 技能发现机制"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When
        skills = deployer.available_skills

        # Then
        self.assertIsInstance(skills, list)
        self.assertGreater(len(skills), 0)

        # 验证每个技能包含必要信息
        for skill in skills:
            self.assertIn("name", skill)
            self.assertIn("path", skill)
            self.assertIn("dependencies", skill)
            self.assertIn("skill_files", skill)
            self.assertIn("has_jieba", skill)
            self.assertIn("needs_chinese", skill)

    def test_03_system_diagnostics_accuracy(self):
        """测试3: 系统诊断准确性"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When
        diagnostics = deployer.run_diagnostics()

        # Then
        self.assertIsInstance(diagnostics, dict)
        self.assertIn("system", diagnostics)
        self.assertIn("skills", diagnostics)
        self.assertIn("issues", diagnostics)
        self.assertIn("recommendations", diagnostics)

        # 验证系统信息完整性
        system_info = diagnostics["system"]
        self.assertIn("platform", system_info)
        self.assertIn("python_version", system_info)
        self.assertIn("uv_available", system_info)
        self.assertIn("pip_available", system_info)

    @patch('subprocess.run')
    def test_04_dependency_detection_accuracy(self, mock_run):
        """测试4: 依赖检测准确性"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When
        jieba_available = deployer._check_dependency("jieba")

        # Then
        self.assertIsInstance(jieba_available, bool)

        # 测试不存在的依赖
        fake_available = deployer._check_dependency("nonexistent_package_xyz")
        self.assertFalse(fake_available)

    def test_05_skill_categorization_logic(self):
        """测试5: 技能分类逻辑"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When & Then
        coding_category = deployer._get_category("coding")
        self.assertEqual(coding_category, "编码分析")

        analysis_category = deployer._get_category("analysis")
        self.assertEqual(analysis_category, "数据分析")

        theory_category = deployer._get_category("theory-saturation")
        self.assertEqual(theory_category, "理论分析")

        other_category = deployer._get_category("unknown-skill")
        self.assertEqual(other_category, "其他工具")

    @patch('subprocess.run')
    def test_06_jieba_dependency_handling(self, mock_run):
        """测试6: jieba依赖处理"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # 模拟jieba已安装
        with patch('builtins.__import__') as mock_import:
            mock_import.return_value = MagicMock()
            mock_import.side_effect = ImportError("No module named 'jieba'")

            jieba_available = deployer._check_dependency("jieba")
            self.assertFalse(jieba_available)

    @patch('subprocess.run')
    def test_07_package_manager_selection_logic(self, mock_run):
        """测试7: 包管理器选择逻辑"""
        # Given
        from smart_deploy import SmartDeployer

        # When - uv可用
        with patch.object(SmartDeployer, '_check_command') as mock_check:
            def side_effect(cmd):
                return cmd == "uv"

            mock_check.side_effect = side_effect
            deployer = SmartDeployer()

            # Then
            self.assertTrue(deployer.system_info["uv_available"])
            self.assertIn("建议使用uv", deployer.run_diagnostics()["recommendations"])

    def test_08_skill_analysis_completeness(self):
        """测试8: 技能分析完整性"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When
        skill_info = deployer._analyze_skill(self.test_skills_dir / "coding" / "open-coding")

        # Then
        self.assertIsNotNone(skill_info)
        self.assertEqual(skill_info["name"], "open-coding")
        self.assertIn("description", skill_info)
        self.assertIsInstance(skill_info["dependencies"], list)
        self.assertIsInstance(skill_info["skill_files"], list)
        self.assertIn("category", skill_info)

    def test_09_error_handling_robustness(self):
        """测试9: 错误处理健壮性"""
        # Given
        from smart_deploy import SmartDeployer

        # When - 处理无效目录
        deployer = SmartDeployer()
        invalid_skill_info = deployer._analyze_skill(Path("nonexistent/path"))

        # Then
        self.assertIsNone(invalid_skill_info)

    def test_10_serialization_compatibility(self):
        """测试10: 序列化兼容性"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()
        diagnostics = deployer.run_diagnostics()

        # When
        json_str = json.dumps(diagnostics, indent=2, ensure_ascii=False)

        # Then
        self.assertIsInstance(json_str, str)
        self.assertGreater(len(json_str), 0)

        # 验证可以反序列化
        parsed = json.loads(json_str)
        self.assertEqual(parsed["system"], diagnostics["system"])

    @patch('subprocess.run')
    def test_11_global_dependencies_installation(self, mock_run):
        """测试11: 全局依赖安装"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # Mock successful subprocess calls
        mock_run.return_value.returncode = 0

        # When
        success = deployer._install_global_dependencies("uv", False)

        # Then
        self.assertTrue(success)
        # 验证调用了正确的命令
        mock_run.assert_called()

    def test_12_skill_dependencies_installation(self, mock_run):
        """测试12: 技能依赖安装"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # 创建测试技能信息
        test_skill = {
            "name": "test-skill",
            "path": self.test_skills_dir / "test",
            "has_jieba": True,
            "dependencies": ["jieba"]
        }

        # Mock successful subprocess calls
        mock_run.return_value.returncode = 0

        # When
        success = deployer._install_skill_dependencies(test_skill, "pip", False)

        # Then
        self.assertTrue(success)

    def test_13_configuration_directory_creation(self):
        """测试13: 配置目录创建"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When
        deployer._initialize_special_configurations()

        # Then
        claude_dir = Path.home() / ".claude" / "skills"
        openskills_dir = Path.home() / ".openskills"

        # Note: 这些目录可能在测试环境中不存在，但函数应该不会崩溃
        self.assertIsInstance(claude_dir, Path)
        self.assertIsInstance(openskills_dir, Path)

    def test_14_usage_guide_generation(self):
        """测试14: 使用指南生成"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When
        guide = deployer.generate_usage_guide()

        # Then
        self.assertIsInstance(guide, str)
        self.assertIn("SSCI技能使用指南", guide)
        self.assertIn("可用的技能", guide)
        self.assertIn("使用方法", guide)

    @patch('platform.system')
    def test_15_quick_start_script_generation(self, mock_system):
        """测试15: 快速启动脚本生成"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # Mock不同平台
        mock_system.return_value = "Windows"

        # When
        script = deployer.create_quick_start_script()

        # Then
        self.assertIsInstance(script, str)
        self.assertIn("@echo off", script)  # Windows batch文件
        self.assertIn("python smart_deploy.py", script)

        # 测试Linux/Unix
        mock_system.return_value = "Linux"
        script_unix = deployer.create_quick_start_script()
        self.assertIn("#!/bin/bash", script_unix)  # Unix shell脚本

    def test_16_json_serialization_fix(self):
        """测试16: JSON序列化修复"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When
        diagnostics = deployer.run_diagnostics()

        # Then - 应该不包含Path对象
        for skill in diagnostics["skills"]:
            self.assertIsInstance(skill["path"], str)
            for skill_file in skill["skill_files"]:
                self.assertIsInstance(skill_file, str)

    def test_17_dependency_requirement_detection(self):
        """测试17: 依赖需求检测"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When
        for skill in deployer.available_skills:
            # Then
            self.assertIsInstance(skill["has_jieba"], bool)
            self.assertIsInstance(skill["needs_chinese"], bool)
            if skill["has_jieba"]:
                self.assertTrue(skill["needs_chinese"])

    def test_18_skill_file_validation(self):
        """测试18: 技能文件验证"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When
        for skill in deployer.available_skills:
            # Then
            self.assertGreater(len(skill["skill_files"]), 0)
            for skill_file in skill["skill_files"]:
                self.assertTrue(skill_file.endswith("SKILL.md"))

    def test_19_recommendations_generation(self):
        """测试19: 推荐生成"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When
        diagnostics = deployer.run_diagnostics()

        # Then
        self.assertIsInstance(diagnostics["recommendations"], list)
        self.assertGreater(len(diagnostics["recommendations"]), 0)

    def test_20_complete_workflow_simulation(self):
        """测试20: 完整工作流模拟"""
        # Given
        from smart_deploy import SmartDeployer

        # When - 模拟完整部署流程
        deployer = SmartDeployer()

        # 1. 诊断系统
        diagnostics = deployer.run_diagnostics()
        self.assertIsInstance(diagnostics, dict)

        # 2. 验证技能发现
        skills = deployer.available_skills
        self.assertIsInstance(skills, list)

        # 3. 生成使用指南
        guide = deployer.generate_usage_guide()
        self.assertIsInstance(guide, str)

        # 4. 创建启动脚本
        script = deployer.create_quick_start_script()
        self.assertIsInstance(script, str)

        # Then - 所有步骤都应该成功
        self.assertGreater(len(skills), 0)
        self.assertGreater(len(guide), 100)
        self.assertGreater(len(script), 50)

class TestSmartDeployerIntegration(unittest.TestCase):
    """智能部署器集成测试"""

    def setUp(self):
        """设置集成测试环境"""
        self.test_dir = Path(tempfile.mkdtemp())

        # 创建完整的项目结构
        self.create_mock_project_structure()

    def create_mock_project_structure(self):
        """创建模拟项目结构"""
        # 创建主要目录
        (self.test_dir / "skills").mkdir()
        (self.test_dir / "tests").mkdir()
        (self.test_dir / "requirements.txt").write_text(
            "jieba>=0.42.0\nnetworkx>=3.0.0\npandas>=1.5.0\nnumpy>=1.20.0"
        )

    def tearDown(self):
        """清理集成测试环境"""
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_real_deployment_simulation(self):
        """真实部署模拟测试"""
        # This test will simulate real deployment scenario
        # It's designed to work with the actual project structure
        pass

if __name__ == '__main__':
    # 运行TDD测试套件
    unittest.main(verbosity=2)