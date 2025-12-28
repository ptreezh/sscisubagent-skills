#!/usr/bin/env python3
"""
发布技能到agentskills.io
作者: socienceAI.com
联系: zhangshuren@freeagentskills.com
"""

import os
import sys
import json
import yaml
import requests
from pathlib import Path
from datetime import datetime

def load_config():
    """加载配置文件"""
    config_path = Path('.agentskills/config.yml')

    if not config_path.exists():
        print("错误: 配置文件不存在 (.agentskills/config.yml)")
        sys.exit(1)

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def publish_skill(skill_data, api_key, base_url):
    """发布单个技能"""
    endpoint = f"{base_url}/skills/publish"

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(
            endpoint,
            headers=headers,
            json=skill_data,
            timeout=30
        )

        if response.status_code == 200:
            print(f"✅ 成功发布: {skill_data['name']}")
            return True
        else:
            print(f"❌ 发布失败: {skill_data['name']}")
            print(f"   状态码: {response.status_code}")
            print(f"   错误: {response.text}")
            return False

    except Exception as e:
        print(f"❌ 发布错误: {skill_data['name']}")
        print(f"   错误: {str(e)}")
        return False

def prepare_skill_data(skill_mapping, config):
    """准备技能数据"""
    source_path = Path(skill_mapping['source'])

    if not source_path.exists():
        print(f"警告: 技能文件不存在: {source_path}")
        return None

    # 读取SKILL.md内容
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取YAML frontmatter
    metadata = {}
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 2:
            try:
                metadata = yaml.safe_load(parts[1])
            except:
                pass

    # 准备发布数据
    skill_data = {
        'id': skill_mapping['target'],
        'name': skill_mapping.get('name', metadata.get('name', 'Unknown')),
        'description': skill_mapping.get('description', metadata.get('description', '')),
        'category': metadata.get('category', 'research-tools'),
        'tags': metadata.get('tags', []),
        'content': content,
        'metadata': {
            'source_file': str(source_path),
            'author': config['project']['author'],
            'email': config['project']['email'],
            'version': metadata.get('version', '1.0.0'),
            'repository': config['project']['repository'],
            'dependencies': skill_mapping.get('dependencies', []),
            'api_required': skill_mapping.get('api_required', False),
            'python_version': skill_mapping.get('python_version', '>=3.8'),
        },
        'published_at': datetime.now().isoformat()
    }

    return skill_data

def main():
    """主函数"""
    print("=" * 60)
    print("发布技能到 AgentSkills.io")
    print("=" * 60)
    print()

    # 加载配置
    config = load_config()

    # 获取API密钥
    api_key = os.environ.get('AGENTSKILLS_API_KEY')

    if not api_key:
        print("错误: 未设置AGENTSKILLS_API_KEY环境变量")
        print("请在GitHub Secrets中配置API密钥")
        sys.exit(1)

    base_url = config.get('api', {}).get('base_url', 'https://api.agentskills.io/v1')

    print(f"项目: {config['project']['name']}")
    print(f"版本: {config['project']['version']}")
    print(f"仓库: {config['project']['repository']}")
    print()

    # 准备发布统计
    total_skills = len(config['skills_mapping'])
    successful = 0
    failed = 0
    skipped = 0

    # 发布每个技能
    for skill_mapping in config['skills_mapping']:
        print(f"处理: {skill_mapping['source']}")

        # 准备技能数据
        skill_data = prepare_skill_data(skill_mapping, config)

        if not skill_data:
            skipped += 1
            continue

        # 发布技能
        if publish_skill(skill_data, api_key, base_url):
            successful += 1
        else:
            failed += 1

        print()

    # 打印统计
    print("=" * 60)
    print("发布统计")
    print("=" * 60)
    print(f"总技能数: {total_skills}")
    print(f"成功: {successful}")
    print(f"失败: {failed}")
    print(f"跳过: {skipped}")
    print()

    if failed > 0:
        print("❌ 部分技能发布失败")
        sys.exit(1)
    else:
        print("✅ 所有技能发布成功")
        sys.exit(0)

if __name__ == '__main__':
    main()
