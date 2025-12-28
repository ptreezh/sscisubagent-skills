# 可信网站爬虫技能 (Trusted Web Scraper)

## 概述

可信网站爬虫技能专门用于从可信网站（企业官网、教育网、政务网）收集信息，确保数据来源的可靠性和权威性。该技能采用多种技术手段来验证网站可信度，并使用适当的爬取策略来获取所需信息。

## 依赖管理

此项目使用 `uv` 进行依赖管理。`uv` 是一个快速的 Python 包安装工具。

### 安装 uv

```bash
# 使用 pip 安装 uv
pip install uv

# 或者使用 Homebrew (macOS)
brew install uv

# 或者使用 winget (Windows)
winget install astral-sh.uv
```

### 设置项目环境

```bash
# 克航到项目目录
cd trusted-web-scraper

# 创建虚拟环境并安装依赖
uv venv
source .venv/bin/activate  # Linux/macOS
# 或
.venv\Scripts\Activate.ps1  # Windows PowerShell
# 或
.venv\Scripts\activate.bat  # Windows CMD

# 安装项目依赖
uv pip install -e .
```

### 安装完整功能依赖

```bash
# 安装所有依赖（包括可选依赖）
uv pip install -e .[full]
```

### 使用开发依赖

```bash
# 安装开发依赖
uv pip install -e .[dev]

# 运行测试
uv run pytest

# 格式化代码
uv run black .

# 检查代码风格
uv run flake8
```

## 功能特性

- **可信度验证**: 验证网站的可信度和权威性
- **智能解析**: 根据可用库自动选择最佳解析方法
- **数据提取**: 从可信网站提取所需信息
- **数据清洗**: 清洗和标准化提取的数据
- **结构化输出**: 提供结构化的数据输出

## 使用方法

### 命令行使用

```bash
# 基本使用
python scripts/trusted_web_scraper.py --url https://example.com --output results.json

# 指定内容类型
python scripts/trusted_web_scraper.py --url https://example.com --content-type text --output results.json

# 指定要提取的字段
python scripts/trusted_web_scraper.py --url https://example.com --data-fields title links --output results.json
```

### 作为模块使用

```python
from modules.scraper import trusted_web_scraper

data = {
    'url': 'https://example.com',
    'content_type': 'text',
    'data_fields': ['title', 'links'],
    'verification_level': 'standard'
}

results = trusted_web_scraper(data)
print(results)
```

## 依赖说明

- **核心依赖**:
  - `requests`: HTTP请求处理
  - `beautifulsoup4`: HTML解析（可选，如果没有则使用内置正则表达式方法）

- **可选依赖**:
  - `lxml`: 高性能XML/HTML解析
  - `selenium`: 动态内容处理
  - `playwright`: 现代化浏览器自动化

- **开发依赖**:
  - `pytest`: 测试框架
  - `black`: 代码格式化
  - `flake8`: 代码风格检查

## 技术架构

- **可信度验证层**: 验证网站SSL证书、域名类型等
- **爬取策略层**: 根据网站类型选择适当的爬取方法
- **内容解析层**: 解析HTML内容，提取所需信息
- **数据处理层**: 清洗和标准化提取的数据
- **输出生成层**: 生成结构化的输出结果

## 注意事项

- 遵遵守网站的robots.txt和使用条款
- 控制请求频率以避免对服务器造成负担
- 确保数据来源的可信度和权威性
- 尊重网站的版权和知识产权

## 许可证

MIT License