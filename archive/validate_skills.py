#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claude Skills 验证工具
检查技能文件是否符合Claude Skills规范
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, List, Tuple

class SkillsValidator:
    """技能验证器"""

    def __init__(self, skills_dir: str):
        self.skills_dir = Path(skills_dir)
        self.validation_results = []

    def validate_all_skills(self) -> Dict[str, List[Dict]]:
        """验证所有技能"""
        results = {
            'valid': [],
            'invalid': [],
            'warnings': []
        }

        # 查找所有SKILL.md文件
        skill_files = list(self.skills_dir.rglob("SKILL.md"))

        for skill_file in skill_files:
            validation_result = self.validate_skill(skill_file)

            if validation_result['is_valid']:
                results['valid'].append(validation_result)
            else:
                results['invalid'].append(validation_result)

            if validation_result['warnings']:
                results['warnings'].append(validation_result)

        return results

    def validate_skill(self, skill_file: Path) -> Dict:
        """验证单个技能文件"""
        result = {
            'file_path': str(skill_file),
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'metadata': {},
            'design_score': 0
        }

        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # 检查YAML frontmatter
            if not content.startswith('---'):
                result['errors'].append("缺少YAML frontmatter")
                result['is_valid'] = False
                return result

            # 提取frontmatter
            try:
                end_index = content.find('---', 3)
                if end_index == -1:
                    result['errors'].append("YAML frontmatter格式错误")
                    result['is_valid'] = False
                    return result

                frontmatter_text = content[3:end_index].strip()
                frontmatter_data = yaml.safe_load(frontmatter_text)

                # 验证必需字段
                if 'name' not in frontmatter_data:
                    result['errors'].append("缺少name字段")
                    result['is_valid'] = False

                if 'description' not in frontmatter_data:
                    result['errors'].append("缺少description字段")
                    result['is_valid'] = False

                # 验证name格式
                if 'name' in frontmatter_data:
                    name = frontmatter_data['name']
                    if not re.match(r'^[a-z0-9-]+$', name):
                        result['errors'].append(f"技能名称'{name}'不符合格式要求（应为小写字母、数字、连字符）")
                        result['is_valid'] = False

                    if len(name) > 64:
                        result['warnings'].append(f"技能名称'{name}'超过64字符限制")

                # 验证description（符合渐进式披露原则）
                if 'description' in frontmatter_data:
                    desc = frontmatter_data['description']
                    if len(desc) < 10:
                        result['errors'].append("描述过短，不够具体")
                        result['is_valid'] = False

                    if len(desc) > 100:
                        result['warnings'].append("描述过长，建议简化以符合渐进式披露原则")

                    # 检查是否使用"当用户需要"的触发格式
                    if not desc.startswith('当用户需要'):
                        result['warnings'].append("建议使用'当用户需要...'的触发描述格式")

                result['metadata'] = frontmatter_data

            except yaml.YAMLError as e:
                result['errors'].append(f"YAML解析错误: {e}")
                result['is_valid'] = False

            # 检查内容结构（符合工具化思维）
            markdown_content = content[end_index + 3:]

            # 计算设计得分
            score = 0

            # 检查是否有工具使用部分
            if '## 🛠️ 使用工具' in markdown_content:
                score += 30

            # 检查是否有脚本文件
            skill_dir = skill_file.parent
            scripts_dir = skill_dir / 'scripts'
            if scripts_dir.exists() and any(scripts_dir.glob('*.py')):
                score += 30

            # 检查内容长度（避免信息过载）
            content_length = len(markdown_content.strip())
            if 500 <= content_length <= 2000:
                score += 20
            elif content_length > 2000:
                result['warnings'].append("内容可能过长，建议精简以符合渐进式披露原则")

            # 检查是否有处理步骤
            if '## 📋 处理步骤' in markdown_content:
                score += 10

            # 检查是否有输出格式说明
            if '## 📊 输出格式' in markdown_content:
                score += 10

            result['design_score'] = score

            # 根据得分给出建议
            if score < 50:
                result['warnings'].append("建议增加工具化支持和简化内容结构")

            # 特别检查是否遵循渐进式披露
            lines = markdown_content.split('\n')
            detailed_sections = 0
            for line in lines:
                if line.strip().startswith('#') and len(line.strip()) > 2:
                    detailed_sections += 1

            if detailed_sections > 8:
                result['warnings'].append("技能结构过于复杂，建议简化以减少认知负荷")

        except Exception as e:
            result['errors'].append(f"文件读取错误: {e}")
            result['is_valid'] = False

        return result

    def generate_report(self, results: Dict) -> str:
        """生成验证报告"""
        report = []
        report.append("=== Claude Skills 验证报告 ===\n")

        # 总体统计
        total_skills = len(results['valid']) + len(results['invalid'])
        valid_count = len(results['valid'])
        invalid_count = len(results['invalid'])

        report.append(f"总技能数: {total_skills}")
        report.append(f"有效技能: {valid_count}")
        report.append(f"无效技能: {invalid_count}")
        report.append(f"有警告的技能: {len(results['warnings'])}\n")

        # 有效技能列表
        if results['valid']:
            report.append("=== 有效技能 ===")
            for skill in results['valid']:
                report.append(f"✓ {skill['metadata']['name']} - {skill['file_path']}")
            report.append("")

        # 无效技能列表
        if results['invalid']:
            report.append("=== 无效技能 ===")
            for skill in results['invalid']:
                report.append(f"✗ {skill['file_path']}")
                for error in skill['errors']:
                    report.append(f"  - {error}")
            report.append("")

        # 警告列表
        if results['warnings']:
            report.append("=== 技能警告 ===")
            for skill in results['warnings']:
                report.append(f"⚠ {skill['metadata']['name']} - {skill['file_path']}")
                for warning in skill['warnings']:
                    report.append(f"  - {warning}")
            report.append("")

        return "\n".join(report)

def main():
    """主函数"""
    skills_dir = "skills"

    if not os.path.exists(skills_dir):
        print(f"错误: 找不到技能目录 '{skills_dir}'")
        return

    validator = SkillsValidator(skills_dir)
    results = validator.validate_all_skills()

    report = validator.generate_report(results)
    print(report)

    # 保存报告到文件
    with open("skills_validation_report.txt", "w", encoding="utf-8") as f:
        f.write(report)

    print("详细报告已保存到: skills_validation_report.txt")

if __name__ == "__main__":
    main()