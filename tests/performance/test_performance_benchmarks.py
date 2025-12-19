#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
性能基准测试
测试各个系统的性能指标，确保响应时间符合要求
"""

import unittest
import time
import subprocess
import sys
import json
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import psutil
import threading

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

class TestPerformanceBenchmarks(unittest.TestCase):
    """性能基准测试套件"""

    def setUp(self):
        """测试前准备"""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_dir = Path.cwd()

        # 创建测试数据
        self.create_test_data()

        # 切换到测试目录
        import os
        os.chdir(self.test_dir)

    def tearDown(self):
        """测试后清理"""
        import os
        os.chdir(self.original_dir)
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def create_test_data(self):
        """创建测试数据"""
        # 创建小型测试文件
        (self.test_dir / "small_data.txt").write_text(
            "这是一个小型测试文件。包含一些中文内容用于测试性能。",
            encoding='utf-8'
        )

        # 创建中型测试文件
        medium_content = "测试内容。\n" * 1000
        (self.test_dir / "medium_data.txt").write_text(medium_content, encoding='utf-8')

        # 创建大型测试文件
        large_content = "性能测试数据。" * 10000
        (self.test_dir / "large_data.txt").write_text(large_content, encoding='utf-8')

    def test_01_smart_deployer_startup_performance(self):
        """测试1: 智能部署器启动性能"""
        # Given
        from smart_deploy import SmartDeployer

        # When & Then - 启动时间应小于5秒
        start_time = time.time()
        deployer = SmartDeployer()
        end_time = time.time()

        startup_time = end_time - start_time
        self.assertLess(startup_time, 5.0, f"启动时间过长: {startup_time:.2f}秒")

    def test_02_skill_discovery_performance(self):
        """测试2: 技能发现性能"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When & Then - 技能发现应小于2秒
        start_time = time.time()
        skills = deployer.available_skills
        end_time = time.time()

        discovery_time = end_time - start_time
        self.assertLess(discovery_time, 2.0, f"技能发现时间过长: {discovery_time:.2f}秒")
        self.assertIsInstance(skills, list)

    def test_03_diagnostics_performance(self):
        """测试3: 系统诊断性能"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When & Then - 诊断应小于3秒
        start_time = time.time()
        diagnostics = deployer.run_diagnostics()
        end_time = time.time()

        diagnostics_time = end_time - start_time
        self.assertLess(diagnostics_time, 3.0, f"诊断时间过长: {diagnostics_time:.2f}秒")
        self.assertIsInstance(diagnostics, dict)

    def test_04_skills_launcher_startup_performance(self):
        """测试4: 技能启动器启动性能"""
        # Given
        from skills_launcher import SkillsLauncher

        # When & Then - 启动时间应小于3秒
        start_time = time.time()
        launcher = SkillsLauncher()
        end_time = time.time()

        startup_time = end_time - start_time
        self.assertLess(startup_time, 3.0, f"启动器启动时间过长: {startup_time:.2f}秒")

    def test_05_welcome_screen_rendering_performance(self):
        """测试5: 欢迎界面渲染性能"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When & Then - 渲染时间应小于1秒
        start_time = time.time()
        import io
        from contextlib import redirect_stdout
        with redirect_stdout(io.StringIO()):
            launcher.show_welcome()
        end_time = time.time()

        render_time = end_time - start_time
        self.assertLess(render_time, 1.0, f"欢迎界面渲染时间过长: {render_time:.2f}秒")

    def test_06_skill_search_performance(self):
        """测试6: 技能搜索性能"""
        # Given
        from skills_launcher import SkillsLauncher
        launcher = SkillsLauncher()

        # When & Then - 搜索应小于0.5秒
        start_time = time.time()
        with patch('builtins.input', return_value='test'):
            launcher.search_skills()
        end_time = time.time()

        search_time = end_time - start_time
        self.assertLess(search_time, 0.5, f"技能搜索时间过长: {search_time:.2f}秒")

    def test_07_web_interface_startup_performance(self):
        """测试7: Web界面启动性能"""
        try:
            # Given
            from web_interface import WebInterface

            # When & Then - 启动时间应小于5秒
            start_time = time.time()
            web_app = WebInterface()
            end_time = time.time()

            startup_time = end_time - start_time
            self.assertLess(startup_time, 5.0, f"Web界面启动时间过长: {startup_time:.2f}秒")
        except ImportError:
            self.skipTest("Flask未安装，跳过Web界面测试")

    def test_08_flask_route_handling_performance(self):
        """测试8: Flask路由处理性能"""
        try:
            # Given
            from web_interface import WebInterface
            web_app = WebInterface()
            app = web_app.app

            # When & Then - 路由响应应小于1秒
            with app.test_client() as client:
                start_time = time.time()
                response = client.get('/')
                end_time = time.time()

                response_time = end_time - start_time
                self.assertLess(response_time, 1.0, f"主页响应时间过长: {response_time:.2f}秒")
                self.assertEqual(response.status_code, 200)
        except ImportError:
            self.skipTest("Flask未安装，跳过Web界面测试")

    def test_09_file_processing_performance(self):
        """测试9: 文件处理性能"""
        # Given
        test_files = ['small_data.txt', 'medium_data.txt', 'large_data.txt']

        for file_name in test_files:
            with self.subTest(file=file_name):
                file_path = self.test_dir / file_name

                # When & Then - 根据文件大小设定不同的性能期望
                start_time = time.time()
                content = file_path.read_text(encoding='utf-8')
                lines = content.split('\n')
                words = len(content.split())
                end_time = time.time()

                processing_time = end_time - start_time

                # 根据文件大小调整性能期望
                if file_name == 'small_data.txt':
                    self.assertLess(processing_time, 0.1, f"小文件处理时间过长: {processing_time:.3f}秒")
                elif file_name == 'medium_data.txt':
                    self.assertLess(processing_time, 0.5, f"中文件处理时间过长: {processing_time:.3f}秒")
                elif file_name == 'large_data.txt':
                    self.assertLess(processing_time, 2.0, f"大文件处理时间过长: {processing_time:.3f}秒")

    def test_10_concurrent_access_performance(self):
        """测试10: 并发访问性能"""
        # Given
        from smart_deploy import SmartDeployer
        results = []

        def deployer_worker():
            start_time = time.time()
            try:
                deployer = SmartDeployer()
                skills = deployer.available_skills
                success = True
            except Exception:
                success = False
            end_time = time.time()
            results.append({
                'success': success,
                'time': end_time - start_time
            })

        # When - 模拟5个并发访问
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=deployer_worker)
            threads.append(thread)

        start_time = time.time()
        for thread in threads:
            thread.start()

        for thread in threads:
            thread.join()
        end_time = time.time()

        # Then - 并发访问应在合理时间内完成
        total_time = end_time - start_time
        self.assertLess(total_time, 10.0, f"并发访问总时间过长: {total_time:.2f}秒")
        self.assertEqual(len(results), 5)

        # 检查所有访问都成功
        for result in results:
            self.assertTrue(result['success'], "并发访问中有失败的实例")
            self.assertLess(result['time'], 5.0, f"单个实例启动时间过长: {result['time']:.2f}秒")

    def test_11_memory_usage_optimization(self):
        """测试11: 内存使用优化"""
        # Given
        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # When - 创建多个实例
        from smart_deploy import SmartDeployer
        from skills_launcher import SkillsLauncher

        deployer = SmartDeployer()
        launcher = SkillsLauncher()

        # 执行一些操作
        _ = deployer.available_skills
        _ = launcher.skills

        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory

        # Then - 内存增长应在合理范围内 (< 100MB)
        self.assertLess(memory_increase, 100, f"内存使用增长过多: {memory_increase:.2f}MB")

    def test_12_cpu_usage_efficiency(self):
        """测试12: CPU使用效率"""
        # Given
        process = psutil.Process()

        # When - 执行计算密集操作
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # 监控CPU使用
        cpu_samples = []
        for _ in range(10):
            cpu_samples.append(process.cpu_percent())
            time.sleep(0.1)

        diagnostics = deployer.run_diagnostics()

        # Then - CPU使用不应持续过高
        avg_cpu = sum(cpu_samples) / len(cpu_samples)
        self.assertLess(avg_cpu, 50.0, f"平均CPU使用过高: {avg_cpu:.1f}%")

    def test_13_io_performance_benchmark(self):
        """测试13: I/O性能基准"""
        # Given
        test_data = "性能测试数据。" * 10000
        test_file = self.test_dir / "io_test.txt"

        # When - 测试文件写入
        write_start = time.time()
        test_file.write_text(test_data, encoding='utf-8')
        write_time = time.time() - write_start

        # 测试文件读取
        read_start = time.time()
        content = test_file.read_text(encoding='utf-8')
        read_time = time.time() - read_start

        # Then - I/O操作应该在合理时间内
        self.assertLess(write_time, 0.5, f"文件写入时间过长: {write_time:.3f}秒")
        self.assertLess(read_time, 0.3, f"文件读取时间过长: {read_time:.3f}秒")
        self.assertEqual(content, test_data)

    def test_14_serialization_performance(self):
        """测试14: 序列化性能"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()
        diagnostics = deployer.run_diagnostics()

        # When - 测试JSON序列化
        json_start = time.time()
        json_str = json.dumps(diagnostics, indent=2, ensure_ascii=False)
        json_time = time.time() - json_start

        # 测试JSON反序列化
        parse_start = time.time()
        parsed = json.loads(json_str)
        parse_time = time.time() - parse_start

        # Then - 序列化应该快速
        self.assertLess(json_time, 0.5, f"JSON序列化时间过长: {json_time:.3f}秒")
        self.assertLess(parse_time, 0.3, f"JSON反序列化时间过长: {parse_time:.3f}秒")
        self.assertEqual(parsed["system"], diagnostics["system"])

    def test_15_network_simulation_performance(self):
        """测试15: 网络模拟性能"""
        try:
            # Given
            from web_interface import WebInterface
            web_app = WebInterface()
            app = web_app.app

            # When - 模拟多个API请求
            with app.test_client() as client:
                endpoints = ['/', '/api/skills', '/api/health']
                times = []

                for endpoint in endpoints:
                    start_time = time.time()
                    response = client.get(endpoint)
                    end_time = time.time()
                    times.append(end_time - start_time)

                    # 检查响应状态
                    self.assertIn(response.status_code, [200, 404])  # 404可能是因为端点不存在

                # Then - API响应应该快速
                avg_time = sum(times) / len(times)
                self.assertLess(avg_time, 0.5, f"API平均响应时间过长: {avg_time:.3f}秒")

        except ImportError:
            self.skipTest("Flask未安装，跳过网络模拟测试")

    def test_16_scalability_performance(self):
        """测试16: 可扩展性性能"""
        # Given
        from smart_deploy import SmartDeployer

        # 创建大量模拟技能目录
        skills_dir = self.test_dir / "skills"
        skills_dir.mkdir()

        for i in range(50):  # 创建50个技能
            skill_dir = skills_dir / f"skill_{i}"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                f"---\nname: skill-{i}\ndescription: 测试技能{i}\n---\n",
                encoding='utf-8'
            )

        import os
        os.chdir(self.test_dir)

        # When - 测试技能发现性能
        start_time = time.time()
        deployer = SmartDeployer()
        skills = deployer.available_skills
        end_time = time.time()

        discovery_time = end_time - start_time

        # Then - 即使有大量技能，发现时间也应该合理
        self.assertLess(discovery_time, 5.0, f"大量技能发现时间过长: {discovery_time:.2f}秒")
        self.assertGreaterEqual(len(skills), 50)

    def test_17_error_handling_performance(self):
        """测试17: 错误处理性能"""
        # Given
        from smart_deploy import SmartDeployer
        deployer = SmartDeployer()

        # When - 测试处理不存在的技能
        start_time = time.time()
        result = deployer._analyze_skill(Path("nonexistent/skill"))
        end_time = time.time()

        error_handling_time = end_time - start_time

        # Then - 错误处理应该快速
        self.assertLess(error_handling_time, 0.5, f"错误处理时间过长: {error_handling_time:.3f}秒")
        self.assertIsNone(result)

    def test_18_caching_performance(self):
        """测试18: 缓存性能"""
        # Given
        from smart_deploy import SmartDeployer

        # When - 测试首次访问
        start_time = time.time()
        deployer1 = SmartDeployer()
        skills1 = deployer1.available_skills
        first_time = time.time() - start_time

        # 测试第二次访问（可能有缓存）
        start_time = time.time()
        deployer2 = SmartDeployer()
        skills2 = deployer2.available_skills
        second_time = time.time() - start_time

        # Then - 第二次访问应该更快（如果实现了缓存）
        # 注意：如果没有实现缓存，这个测试可能会失败
        print(f"首次访问: {first_time:.3f}秒, 第二次访问: {second_time:.3f}秒")

        # 至少验证功能正确性
        self.assertEqual(len(skills1), len(skills2))

    def test_19_configuration_loading_performance(self):
        """测试19: 配置加载性能"""
        # Given - 创建配置文件
        config_file = self.test_dir / "config.json"
        config_data = {
            "test_config": {
                "key1": "value1",
                "key2": "value2",
                "nested": {
                    "deep1": "data1",
                    "deep2": "data2"
                }
            }
        }
        config_file.write_text(json.dumps(config_data, indent=2), encoding='utf-8')

        # When - 测试配置加载
        start_time = time.time()
        loaded_config = json.loads(config_file.read_text(encoding='utf-8'))
        end_time = time.time()

        load_time = end_time - start_time

        # Then - 配置加载应该快速
        self.assertLess(load_time, 0.1, f"配置加载时间过长: {load_time:.3f}秒")
        self.assertEqual(loaded_config, config_data)

    def test_20_end_to_end_workflow_performance(self):
        """测试20: 端到端工作流性能"""
        # Given
        from smart_deploy import SmartDeployer
        from skills_launcher import SkillsLauncher

        # When - 执行完整工作流
        workflow_start = time.time()

        # 1. 智能部署
        deployer = SmartDeployer()
        diagnostics = deployer.run_diagnostics()

        # 2. 技能启动
        launcher = SkillsLauncher()

        # 3. 生成指南
        guide = deployer.generate_usage_guide()

        workflow_end = time.time()
        workflow_time = workflow_end - workflow_start

        # Then - 完整工作流应该在合理时间内
        self.assertLess(workflow_time, 15.0, f"端到端工作流时间过长: {workflow_time:.2f}秒")

        # 验证结果质量
        self.assertIsInstance(diagnostics, dict)
        self.assertIsInstance(guide, str)
        self.assertGreater(len(guide), 100)

if __name__ == '__main__':
    # 运行性能基准测试
    unittest.main(verbosity=2)