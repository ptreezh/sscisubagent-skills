#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技能可用性测试工具
测试所有技能和对应的工具脚本是否能正常运行
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any

class SkillsTester:
    """技能测试器"""

    def __init__(self, skills_dir: str):
        self.skills_dir = Path(skills_dir)
        self.test_results = {}

    def test_all_skills(self) -> Dict[str, Any]:
        """测试所有技能"""
        print("开始测试技能可用性...\n")

        # 查找所有SKILL.md文件
        skill_files = list(self.skills_dir.rglob("SKILL.md"))

        for skill_file in skill_files:
            skill_name = self._extract_skill_name(skill_file)
            print(f"测试技能: {skill_name}")

            result = self._test_single_skill(skill_file)
            self.test_results[skill_name] = result

            # 显示测试结果
            status = "✓ 通过" if result['passed'] else "✗ 失败"
            print(f"  状态: {status}")
            if result['errors']:
                for error in result['errors']:
                    print(f"  错误: {error}")
            if result['warnings']:
                for warning in result['warnings']:
                    print(f"  警告: {warning}")
            print()

        return self.test_results

    def _extract_skill_name(self, skill_file: Path) -> str:
        """提取技能名称"""
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 提取YAML frontmatter中的name
            if content.startswith('---'):
                end_index = content.find('---', 3)
                if end_index != -1:
                    frontmatter_text = content[3:end_index].strip()
                    lines = frontmatter_text.split('\n')
                    for line in lines:
                        if line.startswith('name:'):
                            return line.split(':', 1)[1].strip()

            # 如果没有找到name，使用目录名
            return skill_file.parent.name

        except Exception:
            return skill_file.parent.name

    def _test_single_skill(self, skill_file: Path) -> Dict[str, Any]:
        """测试单个技能"""
        result = {
            'passed': True,
            'errors': [],
            'warnings': [],
            'has_scripts': False,
            'script_count': 0,
            'working_scripts': 0
        }

        try:
            # 检查技能文件格式
            self._validate_skill_file(skill_file, result)

            # 检查是否有脚本文件
            scripts_dir = skill_file.parent / 'scripts'
            if scripts_dir.exists():
                result['has_scripts'] = True
                script_files = list(scripts_dir.glob('*.py'))
                result['script_count'] = len(script_files)

                # 测试每个脚本
                for script_file in script_files:
                    if self._test_script(script_file):
                        result['working_scripts'] += 1
                    else:
                        result['warnings'].append(f"脚本 {script_file.name} 可能有问题")

        except Exception as e:
            result['errors'].append(f"测试过程出错: {e}")
            result['passed'] = False

        # 如果有脚本但没有一个能工作，标记为失败
        if result['has_scripts'] and result['working_scripts'] == 0:
            result['passed'] = False
            result['errors'].append("所有脚本都无法正常运行")

        return result

    def _validate_skill_file(self, skill_file: Path, result: Dict) -> None:
        """验证技能文件格式"""
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查YAML frontmatter
            if not content.startswith('---'):
                result['errors'].append("缺少YAML frontmatter")
                return

            # 检查必需字段
            end_index = content.find('---', 3)
            if end_index == -1:
                result['errors'].append("YAML frontmatter格式错误")
                return

            frontmatter_text = content[3:end_index].strip()
            if 'name:' not in frontmatter_text:
                result['errors'].append("缺少name字段")
            if 'description:' not in frontmatter_text:
                result['errors'].append("缺少description字段")

        except Exception as e:
            result['errors'].append(f"读取技能文件失败: {e}")

    def _test_script(self, script_file: Path) -> bool:
        """测试Python脚本"""
        try:
            # 检查语法
            with open(script_file, 'r', encoding='utf-8') as f:
                content = f.read()
            compile(content, str(script_file))

            # 测试是否能显示帮助信息
            result = subprocess.run(
                [sys.executable, str(script_file), '--help'],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=script_file.parent
            )

            return result.returncode in [0, 1, 2]  # 0=成功, 1=用户错误, 2=参数错误

        except SyntaxError as e:
            print(f"    语法错误: {e}")
            return False
        except subprocess.TimeoutExpired:
            print(f"    脚本运行超时")
            return False
        except Exception as e:
            print(f"    运行错误: {e}")
            return False

    def generate_test_report(self) -> str:
        """生成测试报告"""
        total_skills = len(self.test_results)
        passed_skills = sum(1 for result in self.test_results.values() if result['passed'])

        report = []
        report.append("=== 技能可用性测试报告 ===\n")
        report.append(f"总技能数: {total_skills}")
        report.append(f"通过测试: {passed_skills}")
        report.append(f"失败测试: {total_skills - passed_skills}")
        report.append(f"成功率: {passed_skills/total_skills*100:.1f}%\n")

        # 详细结果
        report.append("=== 详细测试结果 ===")
        for skill_name, result in self.test_results.items():
            status = "✓ 通过" if result['passed'] else "✗ 失败"
            report.append(f"{status} {skill_name}")

            if result['has_scripts']:
                report.append(f"  脚本: {result['working_scripts']}/{result['script_count']} 可用")

            for error in result['errors']:
                report.append(f"  ❌ {error}")

            for warning in result['warnings']:
                report.append(f"  ⚠️ {warning}")

        # 建议
        report.append("\n=== 改进建议 ===")
        failed_skills = [name for name, result in self.test_results.items() if not result['passed']]
        if failed_skills:
            report.append("需要修复的技能:")
            for skill_name in failed_skills:
                result = self.test_results[skill_name]
                report.append(f"- {skill_name}: {result['errors'][0] if result['errors'] else '脚本问题'}")

        return "\n".join(report)

def create_test_data():
    """创建测试数据"""
    test_dir = Path("test_data")
    test_dir.mkdir(exist_ok=True)

    # 创建测试文本文件
    test_text = """
这是一个测试文本，用于验证开放编码技能的功能。
文本内容包括一些基本的句子和段落。
用户可以测试文本预处理、概念提取等功能。
这是一个示例段落，包含一些关键词。
另一个段落用于测试分词和关键词提取功能。
    """

    with open(test_dir / "test_interview.txt", "w", encoding="utf-8") as f:
        f.write(test_text)

    # 创建测试网络数据
    test_network = {
        "nodes": ["A", "B", "C", "D", "E"],
        "edges": [
            ["A", "B"], ["A", "C"], ["B", "C"], ["B", "D"], ["C", "D"], ["D", "E"]
        ]
    }

    with open(test_dir / "test_network.json", "w", encoding="utf-8") as f:
        json.dump(test_network, f, ensure_ascii=False, indent=2)

    print(f"测试数据已创建在: {test_dir}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='技能可用性测试工具')
    parser.add_argument('--create-test-data', action='store_true', help='创建测试数据')
    parser.add_argument('--skills-dir', default='skills', help='技能目录路径')

    args = parser.parse_args()

    if args.create_test_data:
        create_test_data()
        return

    # 测试技能
    tester = SkillsTester(args.skills_dir)
    tester.test_all_skills()

    # 生成报告
    report = tester.generate_test_report()
    print(report)

    # 保存报告
    with open("skills_test_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print("\n详细报告已保存到: skills_test_report.txt")

if __name__ == "__main__":
    main()