---
name: skill-creator
description: 元技能生成器，指导用户创建符合Anthropic SKILL.md规范的高质量技能包。当用户需要创建新技能、优化现有技能或学习技能开发最佳实践时激活。
allowed-tools: ["bash", "text_editor", "web_search"]
---

# Skill Creator - 元技能生成器

## 触发条件
当用户请求涉及以下任一任务时，激活本技能：
- 创建新的技能包
- 优化现有技能结构
- 学习技能开发规范
- 技能质量评估
- 技能模板生成

## 核心原则

### 1. SKILL.md 格式规范
遵循 Anthropic 的标准格式：
```yaml
---
name: skill-name           # 必需：使用连字符的小写标识符
description: When to use   # 必需：1-2句话，第三人称描述
allowed-tools: []          # 可选：允许的工具列表
---
```

### 2. 写作风格
**命令式/不定式形式**（推荐）：
- "To accomplish X, execute Y"
- "Load this skill when Z"
- "See references/guide.md for details"

**避免使用第二人称**：
- ❌ "You should do X"
- ❌ "If you need Y"
- ❌ "When you want Z"

### 3. 渐进式披露
三层信息披露机制：
1. **元数据**（始终在上下文中）：name + description
2. **SKILL.md**（按需加载）：核心指令
3. **资源文件**（按需加载）：详细文档

### 4. 文件大小指南
- **SKILL.md**: 5,000字以内
- **references/**: 无限制（选择性加载）
- **scripts/**: 可执行文件，不计入字数
- **assets/**: 不加载到上下文

## 技能创建工作流程

### 第一步：需求分析
当用户说"我想创建一个XXX技能"时：

1. **识别技能类型**
   ```bash
   # 技能分类
   - 分析类：数据分析、代码审查、质量评估
   - 生成类：内容创建、代码生成、报告撰写
   - 转换类：格式转换、数据迁移、代码重构
   - 工作流类：多步骤流程、自动化任务、协同编辑
   ```

2. **确定核心能力**
   - 主要功能是什么？
   - 解决什么问题？
   - 目标用户是谁？
   - 预期使用场景？

3. **评估复杂度**
   - 简单技能：单一功能，无依赖
   - 中等技能：多功能，少量依赖
   - 复杂技能：多功能，需要脚本和参考文档

### 第二步：结构设计
根据复杂度选择结构：

#### 简单技能结构
```
simple-skill/
└── SKILL.md              # 仅需单文件
```

#### 中等技能结构
```
medium-skill/
├── SKILL.md              # 核心指令
└── references/
    └── guide.md          # 详细指南
```

#### 复杂技能结构
```
complex-skill/
├── SKILL.md              # 核心指令（简洁）
├── references/
│   ├── api-docs.md       # API文档
│   ├── examples.md       # 示例集合
│   └── best-practices.md # 最佳实践
├── scripts/
│   ├── analyzer.py       # 分析脚本
│   ├── processor.sh      # 处理脚本
│   └── validator.js      # 验证脚本
└── assets/
    ├── template.json     # 配置模板
    └── schema.yaml       # 数据模式
```

### 第三步：内容生成

#### 3.1 生成 YAML Frontmatter
```yaml
---
name: [技能名称-使用连字符]
description: [1-2句话描述何时使用此技能，第三人称]
allowed-tools: ["bash", "text_editor", "web_search"]  # 根据需要调整
---
```

**命名规范**：
- 使用小写字母和连字符
- 简洁且描述性强
- 例如：`data-analyzer`, `code-reviewer`, `wiki-creator`

**描述规范**：
- 第三人称视角
- 明确触发条件
- 1-2句话，不超过150字符
- 例如："Load when analyzing data patterns or generating statistical reports"

#### 3.2 编写核心指令

**基础结构模板**：
```markdown
# [技能名称]

## 触发条件
当用户请求涉及以下任一任务时，激活本技能：
- [任务类型1]
- [任务类型2]
- [任务类型3]

## 核心工作流程

### 第一步：任务理解
1. 分析用户需求
2. 识别关键要素
3. 确定执行策略
4. 评估可行性

### 第二步：执行处理
1. [具体步骤1]
2. [具体步骤2]
3. [具体步骤3]

### 第三步：质量控制
1. 结果验证
2. 错误处理
3. 优化改进
4. 输出交付

## 具体实施指南

### 场景1：[典型使用场景]
```
当用户说"[用户输入示例]"时：
1. [具体操作步骤1]
2. [具体操作步骤2]
3. [具体操作步骤3]
4. [预期输出]
```

### 场景2：[另一典型场景]
```
当用户说"[用户输入示例]"时：
1. [具体操作步骤1]
2. [具体操作步骤2]
3. [预期输出]
```

## 资源引用
详细的API文档和示例，参见：
- `references/api-docs.md` - 完整API参考
- `references/examples.md` - 实用示例集
- `scripts/processor.py` - 自动化处理脚本

## 最佳实践
- [实践建议1]
- [实践建议2]
- [实践建议3]

## 常见问题
- **问题1**：描述和解决方案
- **问题2**：描述和解决方案

## 技能边界
- 本技能适用范围：[...]
- 不适用场景：[...]
- 依赖条件：[...]
```

#### 3.3 创建参考文档（references/）

**何时需要参考文档**：
- SKILL.md 超过2000字
- 需要详细的API文档
- 有多个复杂示例
- 包含大量技术细节

**参考文档类型**：
```markdown
# references/api-docs.md
详细的API接口文档

# references/examples.md
完整的使用示例集合

# references/best-practices.md
最佳实践和注意事项

# references/troubleshooting.md
常见问题和故障排除
```

#### 3.4 创建脚本文件（scripts/）

**何时需要脚本**：
- 有确定性的重复任务
- 需要数据处理或转换
- 需要自动化验证
- 涉及复杂计算

**依赖管理策略**：
- **推荐**：使用 uv（极速包管理，零配置）
- **备选**：传统 pip + requirements.txt

**方式 1：uv + 内联依赖（推荐，PEP 723）**

使用 uv 的内联脚本依赖声明，无需 requirements.txt：

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas>=2.0.0",
#   "numpy>=1.24.0",
# ]
# ///
"""
数据分析脚本示例 - uv 版本（内联依赖）

使用方式：
  uv run scripts/analyze.py < input.json
  
优点：
- 无需安装依赖，uv 自动管理虚拟环境
- 依赖声明在脚本内，自包含
- 极速执行，自动缓存
"""
import json
import sys
from typing import Dict, List

def analyze_data(data: Dict) -> Dict:
    """分析输入数据并返回结果"""
    result = {
        "total_count": len(data),
        "summary": {},
        "insights": []
    }
    
    # 实现分析逻辑
    # ...
    
    return result

if __name__ == "__main__":
    # 从标准输入读取数据
    input_data = json.load(sys.stdin)
    
    # 执行分析
    result = analyze_data(input_data)
    
    # 输出结果
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

**方式 2：uv + requirements.txt（兼容模式）**

```python
#!/usr/bin/env python3
"""
数据分析脚本示例 - 传统依赖文件

使用方式：
  uv run --with-requirements requirements.txt scripts/analyze.py < input.json
  
或先安装依赖：
  uv pip install -r requirements.txt
  uv run scripts/analyze.py < input.json
"""
import json
import sys
from typing import Dict, List

def analyze_data(data: Dict) -> Dict:
    """分析输入数据并返回结果"""
    result = {
        "total_count": len(data),
        "summary": {},
        "insights": []
    }
    
    # 实现分析逻辑
    # ...
    
    return result

if __name__ == "__main__":
    # 从标准输入读取数据
    input_data = json.load(sys.stdin)
    
    # 执行分析
    result = analyze_data(input_data)
    
    # 输出结果
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

配套的 `requirements.txt`：
```
pandas>=2.0.0
numpy>=1.24.0
```

**方式 3：零依赖脚本（最佳跨平台兼容性）**

```python
#!/usr/bin/env python3
"""
数据分析脚本 - 零外部依赖版本

使用方式：
  python scripts/analyze.py < input.json
  
优点：
- 无需任何包管理器
- 标准库实现，最大兼容性
- 适合轻量级技能
"""
import json
import sys
from typing import Dict, List
from collections import Counter
from statistics import mean, median

def analyze_data(data: Dict) -> Dict:
    """分析输入数据并返回结果 - 仅使用标准库"""
    result = {
        "total_count": len(data),
        "summary": {},
        "insights": []
    }
    
    # 使用标准库实现分析
    if isinstance(data, list):
        # 计算基础统计
        if data and isinstance(data[0], (int, float)):
            result["summary"]["mean"] = mean(data)
            result["summary"]["median"] = median(data)
        
        # 频率统计
        counter = Counter(data)
        result["summary"]["frequency"] = dict(counter.most_common(10))
    
    return result

if __name__ == "__main__":
    input_data = json.load(sys.stdin)
    result = analyze_data(input_data)
    print(json.dumps(result, indent=2, ensure_ascii=False))
```

**uv 安装和使用**：

```bash
# 安装 uv（一次性）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 或使用 pip
pip install uv

# 使用 uv 运行脚本（自动管理依赖）
uv run scripts/analyze.py < input.json

# 使用 uv 在虚拟环境中运行
uv venv
uv pip install -r requirements.txt
uv run scripts/analyze.py < input.json
```

**依赖管理选择指南**：

| 场景 | 推荐方案 | 原因 |
|------|----------|------|
| 现代 Python 项目 | uv + 内联依赖 | 零配置，极速 |
| 需要兼容旧环境 | uv + requirements.txt | 兼容性好 |
| 轻量级技能 | 零依赖标准库 | 无需包管理 |
| 跨 CLI 使用 | 零依赖标准库 | 最大兼容性 |
| 复杂数据处理 | uv + 内联依赖 | 性能和易用性平衡 |

#### 3.5 准备资源文件（assets/）

**何时需要资源文件**：
- 配置文件模板
- 代码模板
- 数据模式定义
- 样式和主题文件

**资源示例**：
```json
{
  "template_name": "standard-config",
  "version": "1.0.0",
  "settings": {
    "option1": "value1",
    "option2": "value2"
  }
}
```

### 第四步：质量控制

#### 4.1 内容检查清单
- [ ] YAML frontmatter 格式正确
- [ ] name 使用连字符小写
- [ ] description 是第三人称，1-2句话
- [ ] 使用命令式/不定式语气
- [ ] 避免使用"你"、"您"等第二人称
- [ ] SKILL.md 少于5000字
- [ ] 有清晰的触发条件
- [ ] 有具体的执行步骤
- [ ] 包含实用的示例
- [ ] 引用资源文件时使用相对路径

#### 4.2 结构检查
- [ ] 文件命名规范（小写+连字符）
- [ ] 目录结构清晰
- [ ] 脚本文件可执行权限
- [ ] README.md 描述清晰（如果有）

#### 4.3 功能测试
```bash
# 测试技能加载
openskills read [skill-name]

# 测试脚本执行
bash scripts/test_script.sh

# 验证输出格式
python scripts/validator.py < test_input.json
```

### 第五步：部署和使用

#### 5.1 本地安装
```bash
# 复制技能到本地目录
cp -r new-skill ~/.claude/skills/

# 或安装到项目目录
cp -r new-skill ./.claude/skills/
```

#### 5.2 Git 仓库发布
```bash
# 创建独立仓库
git init new-skill
cd new-skill
git add .
git commit -m "Initial skill creation"
git remote add origin https://github.com/username/new-skill.git
git push -u origin main

# 用户可通过以下命令安装
openskills install username/new-skill
```

#### 5.3 集成到 AGENTS.md
```bash
# 同步技能到 AGENTS.md
openskills sync
```

## 技能类型模板

### 模板1：数据分析技能
```markdown
---
name: data-analyzer
description: Analyze data patterns and generate statistical insights. Load when processing datasets or generating reports.
allowed-tools: ["bash", "text_editor"]
---

# Data Analyzer

## 触发条件
- 数据模式分析
- 统计报告生成
- 数据质量评估

## 核心工作流程
### 第一步：数据加载
1. 读取输入数据
2. 验证数据格式
3. 检查数据完整性

### 第二步：分析处理
```bash
python scripts/analyzer.py < input.json > output.json
```

### 第三步：生成报告
1. 汇总统计信息
2. 识别关键模式
3. 生成可视化建议
```

### 模板2：代码审查技能
```markdown
---
name: code-reviewer
description: Review code quality, identify issues, and suggest improvements. Load when analyzing code or performing code reviews.
allowed-tools: ["bash", "text_editor"]
---

# Code Reviewer

## 触发条件
- 代码质量检查
- 安全漏洞扫描
- 最佳实践评估

## 核心工作流程
### 第一步：代码扫描
```bash
bash scripts/scan_code.sh --path ./src --output report.json
```

### 第二步：问题分类
1. 语法错误
2. 逻辑问题
3. 性能瓶颈
4. 安全风险

### 第三步：生成建议
详细的改进建议，参见 `references/review-guidelines.md`
```

### 模板3：内容生成技能
```markdown
---
name: content-generator
description: Generate structured content based on templates and user requirements. Load when creating documents or reports.
allowed-tools: ["bash", "text_editor", "web_search"]
---

# Content Generator

## 触发条件
- 文档创建
- 报告生成
- 模板实例化

## 核心工作流程
### 第一步：需求分析
1. 识别内容类型
2. 确定结构要求
3. 收集必要信息

### 第二步：内容生成
使用模板生成初稿：
```bash
python scripts/generate.py --template assets/template.md --data input.json
```

### 第三步：内容优化
1. 格式美化
2. 内容校对
3. 质量评估
```

### 模板4：工作流自动化技能
```markdown
---
name: workflow-automation
description: Automate multi-step workflows and coordinate complex tasks. Load when executing automated pipelines.
allowed-tools: ["bash", "text_editor"]
---

# Workflow Automation

## 触发条件
- 多步骤任务执行
- 流程自动化
- 批量处理

## 核心工作流程
### 第一步：工作流定义
```yaml
# workflow.yaml
steps:
  - name: prepare
    script: scripts/prepare.sh
  - name: process
    script: scripts/process.py
  - name: finalize
    script: scripts/finalize.sh
```

### 第二步：执行工作流
```bash
python scripts/workflow_runner.py --config workflow.yaml
```

### 第三步：结果验证
1. 检查输出
2. 验证完整性
3. 生成报告
```

## 高级特性

### 特性1：条件分支
```markdown
根据输入类型选择不同处理路径：
- JSON 数据 → 使用 `scripts/json_processor.py`
- CSV 数据 → 使用 `scripts/csv_processor.py`
- XML 数据 → 使用 `scripts/xml_processor.py`
```

### 特性2：错误处理
```bash
# 执行脚本并处理错误
if ! python scripts/processor.py < input.json > output.json 2> error.log; then
    echo "处理失败，查看 error.log 了解详情"
    exit 1
fi
```

### 特性3：并行处理
```bash
# 并行处理多个文件
for file in *.json; do
    python scripts/processor.py < "$file" > "processed_$file" &
done
wait
```

### 特性4：进度反馈
```python
from tqdm import tqdm

for i in tqdm(range(100), desc="Processing"):
    # 处理逻辑
    process_item(i)
```

## 质量标准

### 卓越技能的特征
1. **清晰的触发条件**：明确何时使用
2. **具体的执行步骤**：可操作的指令
3. **丰富的示例**：覆盖常见场景
4. **完善的文档**：易于理解和扩展
5. **健壮的脚本**：错误处理和验证
6. **适当的边界**：明确能做和不能做的

### 常见问题和解决

**问题1：SKILL.md 太长**
- 解决：将详细内容移到 `references/`
- 示例：`详见 references/detailed-guide.md`

**问题2：多个相似场景**
- 解决：使用参数化脚本处理
- 示例：`python scripts/processor.py --mode <type>`

**问题3：依赖外部工具**
- 解决：在 SKILL.md 中说明依赖
- 示例：`需要安装：pip install pandas numpy`

**问题4：跨平台兼容性**
- 解决：提供多平台脚本或使用 Python
- 示例：Python 脚本替代 Bash

## 持续改进

### 收集反馈
- 用户使用情况
- 常见错误
- 改进建议

### 版本迭代
```bash
# 版本管理
v1.0.0 - 初始版本
v1.1.0 - 新增功能X
v1.2.0 - 优化性能
v2.0.0 - 重大重构
```

### 文档更新
- 同步更新所有文档
- 添加新示例
- 更新最佳实践

## 技能发布检查清单

在发布技能之前，确认：
- [ ] 技能名称唯一且有意义
- [ ] Description 准确描述触发条件
- [ ] SKILL.md 格式规范
- [ ] 所有脚本可执行且有注释
- [ ] 参考文档完整
- [ ] 包含使用示例
- [ ] 错误处理完善
- [ ] 有 README.md（如果独立仓库）
- [ ] 通过本地测试
- [ ] 代码风格一致

## 示例：完整技能创建过程

### 用户输入
```
"我想创建一个分析Python代码质量的技能"
```

### 系统响应

#### Step 1: 需求分析
```
技能类型：分析类
核心功能：Python代码质量分析
目标用户：开发者
使用场景：代码审查、质量提升
复杂度：中等（需要脚本支持）
```

#### Step 2: 生成结构
```bash
mkdir -p python-code-analyzer/{references,scripts}
```

#### Step 3: 创建 SKILL.md
```yaml
---
name: python-code-analyzer
description: Analyze Python code quality, identify issues, and suggest improvements. Load when reviewing Python code or assessing code quality.
allowed-tools: ["bash", "text_editor"]
---

# Python Code Analyzer

## 触发条件
当用户请求涉及以下任一任务时，激活本技能：
- Python代码质量检查
- 代码风格审查
- 潜在问题识别
- 复杂度分析

## 核心工作流程

### 第一步：代码扫描
使用分析脚本扫描代码：
```bash
python scripts/analyze.py --path ./src --output report.json
```

### 第二步：问题分类
分析报告包含以下类别：
1. 语法错误
2. 代码风格问题（PEP 8）
3. 复杂度问题
4. 安全漏洞
5. 性能问题

### 第三步：生成建议
基于分析结果生成改进建议：
- 优先级排序
- 具体修改建议
- 代码示例

## 具体实施指南

### 场景1：完整项目分析
当用户说"分析整个Python项目"时：
```bash
python scripts/analyze.py --path . --recursive --output full_report.json
```

### 场景2：单文件分析
当用户说"检查这个文件的质量"时：
```bash
python scripts/analyze.py --file target.py --detailed
```

### 场景3：增量分析
当用户说"只分析修改的文件"时：
```bash
git diff --name-only | grep '\.py$' | xargs python scripts/analyze.py
```

## 资源引用
- `scripts/analyze.py` - 核心分析脚本
- `references/pep8-guide.md` - PEP 8 风格指南
- `references/security-checks.md` - 安全检查清单

## 最佳实践
- 定期运行质量检查
- 优先修复高优先级问题
- 配置自动化检查流程
- 保持代码风格一致

## 技能边界
- 适用于：Python 3.6+
- 依赖：pylint, flake8, bandit
- 不支持：动态代码生成分析
```

#### Step 4: 创建分析脚本（使用 uv）

**方式 1：uv 内联依赖（推荐）**

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pylint>=3.0.0",
#   "radon>=6.0.0",
#   "bandit>=1.7.0",
# ]
# ///
"""
Python 代码质量分析器 - uv 版本

使用方式：
  uv run scripts/analyze.py --path ./src --output report.json
  
依赖说明：
- pylint: 代码质量检查
- radon: 复杂度计算
- bandit: 安全漏洞扫描

优点：
- 无需手动安装依赖，uv 自动管理
- 依赖声明在脚本内，自包含
- 跨平台兼容，跨 CLI 兼容
"""
import json
import sys
import subprocess
from pathlib import Path
from typing import Dict, List

def analyze_code(path: str, recursive: bool = False) -> Dict:
    """分析Python代码质量"""
    
    result = {
        "path": path,
        "issues": [],
        "metrics": {},
        "suggestions": [],
        "security": []
    }
    
    # 1. 运行 pylint 检查代码质量
    try:
        pylint_output = subprocess.run(
            ["pylint", "--output-format=json", path],
            capture_output=True,
            text=True
        )
        if pylint_output.stdout:
            result["issues"].extend(json.loads(pylint_output.stdout))
    except Exception as e:
        result["errors"] = f"Pylint 错误: {str(e)}"
    
    # 2. 使用 radon 计算复杂度
    result["metrics"]["complexity"] = calculate_complexity(path)
    
    # 3. 使用 bandit 扫描安全问题
    result["security"] = scan_security(path)
    
    # 4. 生成改进建议
    result["suggestions"] = generate_suggestions(result["issues"], result["security"])
    
    return result

def calculate_complexity(path: str) -> Dict:
    """使用 radon 计算代码复杂度"""
    try:
        output = subprocess.run(
            ["radon", "cc", path, "-j"],
            capture_output=True,
            text=True
        )
        if output.stdout:
            complexity_data = json.loads(output.stdout)
            return {
                "average_complexity": calculate_average(complexity_data),
                "details": complexity_data
            }
    except Exception as e:
        return {"error": str(e)}
    return {}

def scan_security(path: str) -> List[Dict]:
    """使用 bandit 扫描安全问题"""
    try:
        output = subprocess.run(
            ["bandit", "-r", path, "-f", "json"],
            capture_output=True,
            text=True
        )
        if output.stdout:
            security_data = json.loads(output.stdout)
            return security_data.get("results", [])
    except Exception as e:
        return [{"error": str(e)}]
    return []

def calculate_average(complexity_data: Dict) -> float:
    """计算平均复杂度"""
    total = 0
    count = 0
    for file_data in complexity_data.values():
        for item in file_data:
            if isinstance(item, dict) and "complexity" in item:
                total += item["complexity"]
                count += 1
    return total / count if count > 0 else 0

def generate_suggestions(issues: List, security: List) -> List[str]:
    """基于问题生成改进建议"""
    suggestions = []
    
    # 基于代码质量问题生成建议
    issue_types = {}
    for issue in issues:
        msg_type = issue.get("type", "unknown")
        issue_types[msg_type] = issue_types.get(msg_type, 0) + 1
    
    if issue_types.get("convention", 0) > 10:
        suggestions.append("检测到大量代码风格问题，建议运行 black 自动格式化")
    
    if issue_types.get("refactor", 0) > 5:
        suggestions.append("存在多处需要重构的代码，建议简化复杂函数")
    
    # 基于安全问题生成建议
    if len(security) > 0:
        high_severity = [s for s in security if s.get("issue_severity") == "HIGH"]
        if high_severity:
            suggestions.append(f"发现 {len(high_severity)} 个高危安全问题，请优先修复")
    
    return suggestions

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Python 代码质量分析器（uv 驱动）"
    )
    parser.add_argument("--path", required=True, help="要分析的代码路径")
    parser.add_argument("--recursive", action="store_true", help="递归分析子目录")
    parser.add_argument("--output", default="report.json", help="输出报告路径")
    
    args = parser.parse_args()
    
    print(f"🔍 开始分析: {args.path}")
    result = analyze_code(args.path, args.recursive)
    
    # 保存报告
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    # 输出摘要
    print(f"\n✅ 分析完成！")
    print(f"   问题数量: {len(result['issues'])}")
    print(f"   安全问题: {len(result['security'])}")
    print(f"   平均复杂度: {result['metrics'].get('complexity', {}).get('average_complexity', 0):.2f}")
    print(f"   改进建议: {len(result['suggestions'])} 条")
    print(f"\n📄 详细报告: {args.output}")
```

**方式 2：零依赖版本（最大兼容性）**

```python
#!/usr/bin/env python3
"""
Python 代码质量分析器 - 零依赖版本

使用方式：
  python scripts/analyze_simple.py --path ./src --output report.json
  
特点：
- 仅使用 Python 标准库
- 无需任何外部依赖
- 跨平台、跨 CLI 完全兼容
- 适合轻量级快速检查
"""
import json
import sys
import ast
import re
from pathlib import Path
from typing import Dict, List
from collections import defaultdict

def analyze_code_simple(path: str, recursive: bool = False) -> Dict:
    """简单代码分析 - 零依赖"""
    
    result = {
        "path": path,
        "files_analyzed": 0,
        "metrics": {},
        "issues": [],
        "suggestions": []
    }
    
    path_obj = Path(path)
    
    # 收集所有 Python 文件
    if path_obj.is_file():
        files = [path_obj]
    else:
        pattern = "**/*.py" if recursive else "*.py"
        files = list(path_obj.glob(pattern))
    
    result["files_analyzed"] = len(files)
    
    # 分析每个文件
    total_lines = 0
    total_functions = 0
    total_classes = 0
    
    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 使用 AST 分析
            tree = ast.parse(content, filename=str(file_path))
            
            # 统计基本信息
            lines = content.count('\n') + 1
            total_lines += lines
            
            # 统计函数和类
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    total_functions += 1
                    # 检查函数复杂度（简单版）
                    complexity = calculate_simple_complexity(node)
                    if complexity > 10:
                        result["issues"].append({
                            "file": str(file_path),
                            "line": node.lineno,
                            "type": "complexity",
                            "message": f"函数 {node.name} 复杂度过高: {complexity}"
                        })
                
                elif isinstance(node, ast.ClassDef):
                    total_classes += 1
        
        except Exception as e:
            result["issues"].append({
                "file": str(file_path),
                "type": "parse_error",
                "message": str(e)
            })
    
    # 汇总指标
    result["metrics"] = {
        "total_lines": total_lines,
        "total_functions": total_functions,
        "total_classes": total_classes,
        "average_lines_per_file": total_lines / len(files) if files else 0
    }
    
    # 生成建议
    if total_lines / len(files) > 500:
        result["suggestions"].append("部分文件过大，建议拆分")
    
    if result["issues"]:
        result["suggestions"].append(f"发现 {len(result['issues'])} 个问题需要关注")
    
    return result

def calculate_simple_complexity(node: ast.FunctionDef) -> int:
    """计算简单的圈复杂度"""
    complexity = 1
    
    for child in ast.walk(node):
        # 计算决策点
        if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            complexity += len(child.values) - 1
    
    return complexity

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Python 代码质量分析器（零依赖版本）"
    )
    parser.add_argument("--path", required=True, help="要分析的代码路径")
    parser.add_argument("--recursive", action="store_true", help="递归分析子目录")
    parser.add_argument("--output", default="report.json", help="输出报告路径")
    
    args = parser.parse_args()
    
    print(f"🔍 开始分析: {args.path}")
    result = analyze_code_simple(args.path, args.recursive)
    
    # 保存报告
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    
    # 输出摘要
    print(f"\n✅ 分析完成！")
    print(f"   文件数量: {result['files_analyzed']}")
    print(f"   代码行数: {result['metrics']['total_lines']}")
    print(f"   函数数量: {result['metrics']['total_functions']}")
    print(f"   类数量: {result['metrics']['total_classes']}")
    print(f"   问题数量: {len(result['issues'])}")
    print(f"\n📄 详细报告: {args.output}")
```

#### Step 5: 测试和部署
```bash
# 测试技能
openskills read python-code-analyzer

# 安装到本地
cp -r python-code-analyzer ~/.claude/skills/

# 同步到 AGENTS.md
openskills sync
```

## Stigmergy 跨 CLI 适配系统

### OpenSkills 与 Stigmergy 的集成

#### 核心理念：统一技能标准

**关键洞察**：OpenSkills 和 Stigmergy 解决的是同一类问题的不同层面

```
OpenSkills 解决：技能的标准化格式和加载
    ↓
Stigmergy 解决：跨 CLI 的任务路由和协作
    ↓
结合：统一的跨 CLI 技能生态系统
```

#### 集成架构

```
                    Stigmergy 技能系统（集成 OpenSkills）
┌─────────────────────────────────────────────────────────────┐
│                                                               │
│  用户在任意 CLI 中                                             │
│    ↓                                                          │
│  "use data-analyzer skill"                                    │
│    ↓                                                          │
│  ┌──────────────────────────────────────────┐                │
│  │ Stigmergy 路由层                          │                │
│  │ - 检测技能调用意图                         │                │
│  │ - 解析技能名称                             │                │
│  │ - 选择最佳 CLI                             │                │
│  └──────────┬───────────────────────────────┘                │
│             ↓                                                 │
│  ┌──────────────────────────────────────────┐                │
│  │ Stigmergy Skill Manager                   │                │
│  │ (基于 OpenSkills 实现)                    │                │
│  │                                           │                │
│  │ • stigmergy skill install <source>        │                │
│  │ • stigmergy skill read <name>             │                │
│  │ • stigmergy skill list                    │                │
│  │ • stigmergy skill sync                    │                │
│  └──────────┬───────────────────────────────┘                │
│             ↓                                                 │
│  ┌──────────────────────────────────────────┐                │
│  │ 统一技能存储                               │                │
│  │ ~/.stigmergy/skills/                      │                │
│  │   ├── data-analyzer/                      │                │
│  │   │   └── SKILL.md                        │                │
│  │   ├── code-reviewer/                      │                │
│  │   │   └── SKILL.md                        │                │
│  │   └── ...                                 │                │
│  └──────────┬───────────────────────────────┘                │
│             ↓                                                 │
│  ┌──────────────────────────────────────────┐                │
│  │ CLI 适配器层                               │                │
│  │ - Claude 适配器：原生 openskills          │                │
│  │ - Qwen 适配器：stigmergy skill read       │                │
│  │ - Gemini 适配器：stigmergy skill read     │                │
│  │ - iFlow 适配器：stigmergy skill read      │                │
│  └────────────────────────────────────────────               │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

#### 具体集成方案

**方案 1：Stigmergy 包装 OpenSkills（推荐）**

```bash
# Stigmergy CLI 提供技能管理命令（内部调用 openskills）

# 安装技能
stigmergy skill install anthropics/skills
# 内部执行：openskills install anthropics/skills --universal

# 读取技能
stigmergy skill read pdf
# 内部执行：openskills read pdf

# 列出技能
stigmergy skill list
# 内部执行：openskills list

# 同步到所有 CLI
stigmergy skill sync
# 内部执行：
#   1. openskills sync (更新 AGENTS.md)
#   2. 为每个 CLI 部署技能声明
```

**技能存储位置**：

```
~/.stigmergy/skills/        # Stigmergy 统一技能库
    ├── data-analyzer/
    │   ├── SKILL.md
    │   ├── scripts/
    │   └── references/
    └── code-reviewer/
        └── SKILL.md

# 软链接到各 CLI（按需）
~/.claude/skills/data-analyzer → ~/.stigmergy/skills/data-analyzer
~/.qwen/skills/data-analyzer → ~/.stigmergy/skills/data-analyzer
```

**方案 2：Stigmergy 原生实现技能系统**

```javascript
// src/core/skills/SkillManager.js
class StigmergySkillManager {
    constructor() {
        this.skillsDir = path.join(os.homedir(), '.stigmergy', 'skills');
        this.cliAdapters = new Map();
    }

    async installSkill(source, options = {}) {
        // 从 GitHub 下载技能
        const skillDir = await this.downloadFromGitHub(source);
        
        // 解析 SKILL.md
        const skillMeta = await this.parseSkillMetadata(skillDir);
        
        // 注册到所有 CLI
        await this.registerToAllCLIs(skillMeta);
        
        return skillMeta;
    }

    async readSkill(skillName, targetCLI = null) {
        const skillPath = path.join(this.skillsDir, skillName, 'SKILL.md');
        const content = await fs.readFile(skillPath, 'utf-8');
        
        if (targetCLI) {
            // 通过适配器在指定 CLI 中激活
            const adapter = this.cliAdapters.get(targetCLI);
            return await adapter.activateSkill(skillName, content);
        }
        
        // 直接返回内容
        return {
            name: skillName,
            baseDir: path.dirname(skillPath),
            content: content
        };
    }

    async registerToAllCLIs(skillMeta) {
        // 为每个 CLI 生成技能声明
        const clis = ['claude', 'qwen', 'gemini', 'iflow', 'qoder'];
        
        for (const cli of clis) {
            const adapter = this.cliAdapters.get(cli);
            if (adapter) {
                await adapter.registerSkill(skillMeta);
            }
        }
    }
}
```

#### 统一的技能调用接口

**在各 CLI 的 AGENTS.md 中声明**：

```xml
<skills_system priority="1">

## Stigmergy 技能系统

<usage>
使用 Stigmergy 统一技能系统调用技能：

方式 1 - 直接调用（当前 CLI）:
  Bash("stigmergy skill read <skill-name>")

方式 2 - 跨 CLI 调用（指定 CLI）:
  Bash("stigmergy use <cli-name> skill <skill-name>")

方式 3 - 智能调用（自动选择最佳 CLI）:
  Bash("stigmergy call skill <skill-name>")

技能内容会加载并提供详细指令。
</usage>

<available_skills>

<skill>
<name>data-analyzer</name>
<description>Analyze data patterns and generate statistical reports</description>
<location>stigmergy</location>
<optimal-cli>claude</optimal-cli>
</skill>

<skill>
<name>code-reviewer</name>
<description>Review code quality and suggest improvements</description>
<location>stigmergy</location>
<optimal-cli>claude</optimal-cli>
</skill>

<skill>
<name>chinese-academic-writer</name>
<description>中文学术写作辅助</description>
<location>stigmergy</location>
<optimal-cli>qwen</optimal-cli>
</skill>

</available_skills>

</skills_system>
```

#### 命令对比和兼容性

| 操作 | OpenSkills 原生 | Stigmergy 集成 | 说明 |
|------|----------------|----------------|------|
| 安装技能 | `openskills install repo` | `stigmergy skill install repo` | Stigmergy 包装 |
| 读取技能 | `openskills read name` | `stigmergy skill read name` | 统一接口 |
| 列出技能 | `openskills list` | `stigmergy skill list` | 统一接口 |
| 同步配置 | `openskills sync` | `stigmergy skill sync` | 跨 CLI 同步 |
| 跨 CLI 调用 | ❌ 不支持 | `stigmergy use claude skill pdf` | Stigmergy 扩展 |
| 智能路由 | ❌ 不支持 | `stigmergy call skill data-analyzer` | Stigmergy 扩展 |

**向后兼容**：

```bash
# OpenSkills 命令仍然可用（如果安装了）
openskills read pdf

# Stigmergy 命令（推荐，增强功能）
stigmergy skill read pdf

# 两者可以共存，Stigmergy 优先使用统一存储
```

#### 集成优势分析

**1. 技能格式标准化**

```
统一使用 SKILL.md 格式
    ↓
所有 CLI 工具使用同一套技能
    ↓
开发者只需维护一份技能代码
    ↓
社区共享更容易
```

**2. 降低适配器复杂度**

```
之前：每个 CLI 需要格式转换适配器
    qwen-cli-adapter.js - 转换 SKILL.md → Qwen JSON
    iflow-cli-adapter.js - 转换 SKILL.md → iFlow YAML
    ...

现在：所有 CLI 统一读取 SKILL.md
    stigmergy skill read name
        ↓
    返回标准 SKILL.md 内容
        ↓
    各 CLI 的 Agent 直接理解 Markdown 指令
        ↓
    无需格式转换
```

**3. 跨 CLI 技能调用更简洁**

```bash
# 之前（复杂）
qwen> "load skill from claude format"
# 需要先转换格式，再加载

# 现在（简洁）
qwen> "use stigmergy skill data-analyzer"
# 或者
qwen> Bash("stigmergy skill read data-analyzer")
# 直接读取标准格式，立即可用
```

**4. 技能市场统一**

```
Stigmergy 技能市场
    ↓
存储在 GitHub
    ↓
使用标准 SKILL.md 格式
    ↓
一键安装：stigmergy skill install user/repo
    ↓
所有 CLI 立即可用
```

#### 实际使用场景

**场景 1：安装和使用技能**

```bash
# 1. 安装技能（一次性）
stigmergy skill install anthropics/skills
# 选择技能：pdf, xlsx, docx, ...
# 安装到：~/.stigmergy/skills/

# 2. 在 Claude CLI 中使用
claude> "use pdf skill to extract text from report.pdf"
# Claude 读取 AGENTS.md 中的技能声明
# 执行：stigmergy skill read pdf
# 加载技能内容并执行

# 3. 在 Qwen CLI 中跨 CLI 调用
qwen> "use claude's pdf skill to process document.pdf"
# Qwen 检测到跨 CLI 调用
# 调用：stigmergy use claude skill pdf
# 路由到 Claude CLI 执行
```

**场景 2：创建自定义技能**

```bash
# 1. 创建技能目录
mkdir -p ~/.stigmergy/skills/my-analyzer

# 2. 编写 SKILL.md（标准格式）
cat > ~/.stigmergy/skills/my-analyzer/SKILL.md << 'EOF'
---
name: my-analyzer
description: Custom data analyzer for my project
---

# My Analyzer

When user asks to analyze data:
1. Read the data file
2. Run analysis script
3. Generate report
EOF

# 3. 同步到所有 CLI
stigmergy skill sync

# 4. 立即在任意 CLI 中可用
claude> "use my-analyzer to process data.json"
qwen> "use my-analyzer to analyze sales_data.csv"
gemini> "用 my-analyzer 分析这些数据"
```

**场景 3：技能的智能路由**

```bash
# 用户不需要知道技能在哪个 CLI 中最优
stigmergy call skill pdf-editor

# Stigmergy 自动决策：
# 1. 检查技能元数据：optimal-cli = "claude"
# 2. 检查 Claude CLI 可用性
# 3. 路由到 Claude CLI
# 4. 加载 pdf-editor 技能
# 5. 执行任务
# 6. 返回结果
```

#### 实现路线图

**Phase 1：基础集成（最小可行产品）**

```bash
# 1. Stigmergy CLI 包装 OpenSkills
stigmergy skill install → openskills install
stigmergy skill read → openskills read
stigmergy skill list → openskills list

# 2. 统一技能存储
~/.stigmergy/skills/ (主存储)
~/.claude/skills/ → 软链接

# 3. 基础 AGENTS.md 集成
在各 CLI 的 AGENTS.md 中声明技能
```

**Phase 2：跨 CLI 增强**

```bash
# 4. 跨 CLI 调用
stigmergy use <cli> skill <name>

# 5. 智能路由
stigmergy call skill <name>

# 6. 技能元数据扩展
在 SKILL.md 中添加 optimal-cli 字段
```

**Phase 3：生态系统**

```bash
# 7. Stigmergy 技能市场
stigmergy skill search <keyword>
stigmergy skill publish <name>

# 8. 技能评分和推荐
stigmergy skill rate <name>
stigmergy skill recommend

# 9. 技能组合和工作流
stigmergy workflow create <name>
```

#### 配置文件示例

**~/.stigmergy/config.json**

```json
{
  "skills": {
    "storage": "~/.stigmergy/skills",
    "backends": ["openskills", "native"],
    "sync_to_clis": ["claude", "qwen", "gemini", "iflow"],
    "auto_sync": true,
    "preferred_sources": [
      "anthropics/skills",
      "stigmergy-project/skills"
    ]
  },
  "routing": {
    "auto_select_cli": true,
    "cli_preferences": {
      "pdf": "claude",
      "code-review": "claude",
      "chinese-academic": "qwen",
      "data-viz": "gemini"
    }
  }
}
```

**技能元数据扩展（SKILL.md）**

```yaml
---
name: data-analyzer
description: Comprehensive data analysis toolkit
version: 1.0.0
author: stigmergy-project

# Stigmergy 扩展字段
stigmergy:
  optimal-cli: claude              # 最佳执行 CLI
  fallback-cli: [qwen, gemini]     # 备选 CLI
  cross-cli-compatible: true       # 跨 CLI 兼容
  requires-tools:                  # 必需工具
    - file.read
    - shell.execute
  performance:
    execution-time: fast           # fast/medium/slow
    resource-usage: low            # low/medium/high
---
```

### 系统架构概览

Stigmergy 是一个多 AI CLI 协作系统，通过**适配器模式**实现跨 CLI 工具的无缝通信，并通过集成 OpenSkills 实现统一的技能标准：

```
用户输入 → Stigmergy 路由层 → CLI 适配器 → 目标 CLI 工具 → 返回结果
    ↓
自然语言解析
    ↓
意图识别（跨CLI调用？）
    ↓
选择最佳工具
```

**支持的 CLI 工具**：
- Claude CLI (Hook 系统)
- Gemini CLI (Extension 系统)
- Qwen CLI (类继承机制)
- iFlow CLI (工作流脚本)
- Qoder CLI (Plugin 系统)
- CodeBuddy CLI (Buddy 系统)
- Codex CLI (Slash 命令)
- GitHub Copilot CLI

### 核心原则

#### 1. 独立适配器架构
每个 CLI 工具有独立的适配器，**无依赖**、**无继承**：

```
src/adapters/
├── claude/
│   └── hook_adapter.py        # 独立实现
├── qwen/
│   └── class_adapter.py       # 独立实现
├── gemini/
│   └── extension_adapter.py   # 独立实现
└── iflow/
    └── workflow_adapter.py    # 独立实现
```

**禁止的模式**：
```python
# ❌ 禁止：抽象基类
class BaseCrossCLIAdapter(ABC):
    pass

# ❌ 禁止：工厂模式
class AdapterFactory:
    def get_adapter(self, name):
        pass
```

**推荐的模式**：
```python
# ✅ 推荐：独立函数实现
def detect_cross_cli_intent(user_input: str) -> bool:
    """检测是否为跨CLI调用 - 直接实现"""
    patterns = [
        r'use (\w+) to',
        r'ask (\w+) to',
        r'call (\w+)'
    ]
    for pattern in patterns:
        if re.search(pattern, user_input, re.IGNORECASE):
            return True
    return False

def execute_task(task: str, context: dict) -> dict:
    """执行任务 - 直接实现"""
    # 直接调用目标CLI
    result = subprocess.run(['target-cli', task], capture_output=True)
    return {'output': result.stdout, 'status': 'success'}
```

#### 2. 技能的跨 CLI 兼容性

技能文件本身是**CLI 无关**的，通过适配器实现跨 CLI 支持：

```markdown
---
name: my-skill
description: Example skill that works across all CLIs
---

# My Skill

## 使用方法

### 在 Claude CLI 中
```bash
openskills read my-skill
```

### 在 Qwen CLI 中（通过 stigmergy）
```bash
stigmergy use claude to "load my-skill"
```

### 在 iFlow CLI 中（通过 stigmergy）
```bash
stigmergy call "use my-skill from claude"
```
```

### 适配器开发指南

#### 步骤 1：创建独立适配器

以 Qwen CLI 为例：

```javascript
// adapters/qwen-cli-adapter.js
class QwenCLIAdapter {
    constructor() {
        this.sourceDir = './skills';
        this.outputDir = './qwen-compatible';
        this.toolMapping = {
            'read_file': 'file-read',
            'write_file': 'file-write',
            'bash': 'shell-exec'
        };
    }

    /**
     * 转换 SKILL.md 到 Qwen 格式
     */
    convertSkill(skillName, skillConfig) {
        return {
            name: skillName,
            description: skillConfig.description,
            systemPrompt: this.convertSystemPrompt(skillConfig),
            tools: this.mapTools(skillConfig['allowed-tools'] || []),
            model: 'qwen-max',
            category: this.determineCategory(skillConfig.description)
        };
    }

    /**
     * 工具权限映射
     */
    mapTools(tools) {
        return tools.map(tool => this.toolMapping[tool] || tool);
    }

    /**
     * 系统提示词转换
     */
    convertSystemPrompt(skillConfig) {
        let prompt = `# ${skillConfig.name}\n\n`;
        prompt += `${skillConfig.description}\n\n`;
        prompt += `## Qwen CLI 集成\n`;
        prompt += `你运行在 Qwen CLI 环境中，可以使用以下工具完成任务。\n`;
        return prompt;
    }
}
```

#### 步骤 2：实现跨 CLI 调用检测

```javascript
/**
 * 检测用户输入是否包含跨 CLI 调用意图
 */
function detectCrossCLIIntent(userInput) {
    const patterns = [
        /use (\w+) to (.+)/i,        // "use claude to analyze code"
        /ask (\w+) to (.+)/i,        // "ask gemini to translate"
        /call (\w+) (.+)/i,          // "call qwen analyze data"
        /stigmergy (\w+) (.+)/i      // "stigmergy claude write code"
    ];

    for (const pattern of patterns) {
        const match = userInput.match(pattern);
        if (match) {
            return {
                detected: true,
                targetCLI: match[1],
                task: match[2]
            };
        }
    }

    return { detected: false };
}
```

#### 步骤 3：技能加载适配

```javascript
/**
 * 跨 CLI 加载技能
 */
async function loadSkillCrossCLI(skillName, targetCLI, context) {
    // 1. 加载原始技能
    const skillPath = findSkillPath(skillName);
    const skillContent = await fs.readFile(skillPath, 'utf-8');
    
    // 2. 获取目标 CLI 适配器
    const adapter = getAdapter(targetCLI);
    
    // 3. 转换技能格式
    const adaptedSkill = adapter.convertSkill(skillName, parseSkill(skillContent));
    
    // 4. 在目标 CLI 中激活
    const result = await adapter.activateSkill(adaptedSkill, context);
    
    return result;
}
```

### 技能跨 CLI 部署流程

#### 方案 1：Stigmergy 命令直接使用

```bash
# 用户在任意 CLI 中执行
stigmergy use claude to "create a Python analysis script using data-analyzer skill"

# 系统处理流程：
# 1. 检测到跨 CLI 调用
# 2. 解析目标：claude
# 3. 解析任务：使用 data-analyzer 技能创建 Python 脚本
# 4. 路由到 claude CLI 适配器
# 5. 在 claude 中加载 data-analyzer 技能
# 6. 执行任务
# 7. 返回结果
```

#### 方案 2：Stigmergy 智能分配

```bash
# 系统自动选择最佳 CLI 工具
stigmergy call "analyze this codebase using code-reviewer skill"

# 系统决策流程：
# 1. 分析任务类型：代码审查
# 2. 检查可用技能：code-reviewer
# 3. 评估 CLI 能力：Claude > Qwen > Gemini
# 4. 自动选择 Claude CLI
# 5. 加载 code-reviewer 技能
# 6. 执行分析
# 7. 返回结果
```

#### 方案 3：CLI 内自然语言激活

```bash
# 在 Qwen CLI 中直接使用自然语言
qwen> "use claude's pdf-editor skill to extract text from report.pdf"

# 系统处理：
# 1. Qwen CLI 的 stigmergy 钩子检测到跨 CLI 意图
# 2. 解析：目标 CLI = claude，技能 = pdf-editor
# 3. 调用 stigmergy 路由层
# 4. 加载 pdf-editor 技能到 claude
# 5. 执行 PDF 提取任务
# 6. 结果返回到 Qwen CLI 上下文
```

### 技能创建时的跨 CLI 考虑

#### 1. 工具抽象化

使用通用的工具描述，让适配器负责映射：

```yaml
---
name: universal-analyzer
description: Universal code analyzer that works across all CLIs
allowed-tools:
  - file.read      # 通用：读取文件
  - file.write     # 通用：写入文件
  - shell.execute  # 通用：执行命令
  - web.search     # 通用：网络搜索
---
```

适配器自动映射：
- Claude CLI: `read_file` → `file.read`
- Qwen CLI: `file-read` → `file.read`
- iFlow CLI: `file.read` → `file.read` (原生支持)

#### 2. 脚本跨平台兼容

提供多平台脚本：

```
my-skill/
├── SKILL.md
├── scripts/
│   ├── analyze.py      # Python（跨平台）
│   ├── analyze.sh      # Linux/Mac
│   └── analyze.ps1     # Windows
└── references/
    └── api-docs.md
```

在 SKILL.md 中智能选择：

```markdown
## 执行分析

根据您的平台选择脚本：

### Linux/Mac
```bash
bash scripts/analyze.sh --input data.json
```

### Windows
```powershell
powershell scripts/analyze.ps1 -Input data.json
```

### 跨平台（推荐）
```bash
python scripts/analyze.py --input data.json
```
```

#### 3. 上下文传递

设计技能时考虑跨 CLI 上下文传递：

```markdown
---
name: context-aware-skill
description: Skill that maintains context across CLI switches
context-aware: true
context-schema:
  - project_path: string
  - file_history: array
  - previous_tasks: array
---

# Context-Aware Skill

## 上下文管理

此技能在跨 CLI 调用时会保留以下上下文：

1. **项目路径**：当前工作目录
2. **文件历史**：已处理的文件列表
3. **任务历史**：之前完成的任务

## 跨 CLI 使用示例

### 场景：在 Qwen 中开始，在 Claude 中继续

```bash
# 在 Qwen CLI 中开始项目分析
qwen> "analyze project structure"

# 切换到 Claude 继续代码审查（保留上下文）
qwen> "use claude to review the files we analyzed"

# Claude 接收到的上下文包含：
# - project_path: /path/to/project
# - file_history: [file1.py, file2.py, ...]
# - previous_tasks: ["project structure analysis"]
```
```

### 完整示例：跨 CLI 数据分析技能

```markdown
---
name: cross-cli-data-analyzer
description: Data analysis skill that works seamlessly across Claude, Qwen, Gemini, and iFlow CLIs
allowed-tools:
  - file.read
  - file.write
  - shell.execute
  - web.search
context-aware: true
cross-cli-compatible: true
version: 1.0.0
---

# Cross-CLI Data Analyzer

## 跨 CLI 兼容性声明

此技能完全兼容以下 CLI 工具：
- ✅ Claude CLI
- ✅ Qwen CLI  
- ✅ Gemini CLI
- ✅ iFlow CLI
- ✅ Qoder CLI
- ✅ CodeBuddy CLI
- ✅ Codex CLI

## 核心功能

### 1. 数据加载（CLI 无关）

使用通用文件读取接口：

```python
# scripts/load_data.py
import json
import sys

def load_data(file_path):
    """通用数据加载函数 - 跨 CLI 兼容"""
    with open(file_path, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    data = load_data(sys.argv[1])
    print(json.dumps(data, indent=2))
```

### 2. 数据分析（平台无关）

```python
# scripts/analyze.py
def analyze_data(data):
    """数据分析 - 纯 Python 实现，跨平台"""
    result = {
        "total_records": len(data),
        "summary": {},
        "insights": []
    }
    
    # 分析逻辑
    # ...
    
    return result
```

### 3. 报告生成（CLI 适配）

根据运行环境生成适配的报告：

```python
# scripts/generate_report.py
import os

def detect_cli_environment():
    """检测当前 CLI 环境"""
    if 'CLAUDE_CLI' in os.environ:
        return 'claude'
    elif 'QWEN_CLI' in os.environ:
        return 'qwen'
    elif 'IFLOW_CLI' in os.environ:
        return 'iflow'
    else:
        return 'unknown'

def generate_report(data, analysis):
    """生成适配当前 CLI 的报告"""
    cli_env = detect_cli_environment()
    
    if cli_env == 'claude':
        return generate_claude_report(data, analysis)
    elif cli_env == 'qwen':
        return generate_qwen_report(data, analysis)
    else:
        return generate_generic_report(data, analysis)
```

## 跨 CLI 使用场景

### 场景 1：在 Claude 中使用

```bash
# 直接加载
openskills read cross-cli-data-analyzer

# 执行分析
python scripts/analyze.py --input data.json --output report.json
```

### 场景 2：从 Qwen 调用 Claude 版本

```bash
# 在 Qwen CLI 中
qwen> "use claude's cross-cli-data-analyzer to analyze sales_data.json"

# Stigmergy 自动处理：
# 1. 检测跨 CLI 调用
# 2. 路由到 Claude
# 3. 加载技能
# 4. 执行分析
# 5. 返回结果到 Qwen
```

### 场景 3：智能 CLI 选择

```bash
# 让 Stigmergy 选择最佳 CLI
stigmergy call "analyze this dataset using cross-cli-data-analyzer"

# 系统决策：
# - 数据分析任务
# - Claude 的分析能力最强
# - 自动选择 Claude CLI
# - 加载并执行技能
```

## 适配器配置

### Claude CLI 适配器

```json
{
  "cli": "claude",
  "skill_format": "anthropic-skill-md",
  "tool_mapping": {
    "file.read": "read_file",
    "file.write": "write_file",
    "shell.execute": "run_shell_command"
  }
}
```

### Qwen CLI 适配器

```json
{
  "cli": "qwen",
  "skill_format": "qwen-agent-json",
  "tool_mapping": {
    "file.read": "file-read",
    "file.write": "file-write",
    "shell.execute": "shell-exec"
  }
}
```

### iFlow CLI 适配器

```json
{
  "cli": "iflow",
  "skill_format": "iflow-workflow-yaml",
  "tool_mapping": {
    "file.read": "file.read",
    "file.write": "file.write",
    "shell.execute": "shell.execute"
  }
}
```

## 部署清单

创建跨 CLI 兼容技能时，确保：

- [ ] SKILL.md 使用通用工具描述
- [ ] 提供跨平台脚本（Python 优先）
- [ ] 声明 `cross-cli-compatible: true`
- [ ] 提供适配器配置示例
- [ ] 文档说明各 CLI 使用方法
- [ ] 测试所有支持的 CLI 环境
- [ ] 提供上下文传递机制
- [ ] 错误处理兼容各 CLI
```

### Stigmergy 技能市场集成

创建技能后，可以发布到 Stigmergy 技能市场：

```bash
# 1. 创建技能包
stigmergy skill package cross-cli-data-analyzer

# 2. 验证跨 CLI 兼容性
stigmergy skill test --all-clis

# 3. 发布到市场
stigmergy skill publish --name cross-cli-data-analyzer \
  --category data-analysis \
  --tags "cross-cli,data,analysis"

# 4. 用户安装
stigmergy skill install cross-cli-data-analyzer

# 5. 在任意 CLI 中使用
# Claude CLI:
openskills read cross-cli-data-analyzer

# Qwen CLI (通过 stigmergy):
stigmergy use claude to "load cross-cli-data-analyzer"

# 或智能调用:
stigmergy call "use data analyzer skill"
```

## 技能验证与测试

### 核心机制解释

#### 1. 技能本身：CLI 无关的标准格式

**关键理解**：技能文件（SKILL.md）本身是 CLI 无关的纯文本文档。

```markdown
---
name: my-skill
description: What this skill does
---

# Instructions

When user asks X, do Y...
```

这个文件：
- ✅ 是标准的 Markdown 文件
- ✅ 包含 YAML frontmatter（元数据）
- ✅ 使用命令式语气的指令
- ✅ 不依赖任何特定的 CLI 工具

#### 2. 在 Claude CLI 中的直接使用

**工作原理**：

```
用户输入 → Claude CLI → openskills read my-skill → 加载 SKILL.md → 注入 Claude 上下文
```

**实际执行流程**：

```bash
# 1. 用户在 Claude CLI 中说
"Use the data-analyzer skill to process data.json"

# 2. Claude CLI 识别技能引用，执行
openskills read data-analyzer

# 3. openskills 输出技能内容：
Reading: data-analyzer
Base directory: /path/to/.claude/skills/data-analyzer

---
name: data-analyzer
description: Analyze data and generate reports
---

# Data Analyzer

When user provides data, follow these steps:
1. Load the data file
2. Run analysis script
3. Generate report

# 4. Claude 读取这些指令，加入到上下文中

# 5. Claude 按照指令执行任务
```

**关键点**：
- ✅ 技能不是"执行"，而是"指令"
- ✅ Claude 读取指令后，自己决定如何执行
- ✅ openskills 只是加载器，不是执行器

#### 3. 通过 Stigmergy 实现跨 CLI 的真实原理

**工作原理（分两层）**：

**第一层：Stigmergy 路由层**

```
用户在 Qwen CLI 中输入：
"use claude to analyze code with code-reviewer skill"
    ↓
Qwen CLI 的 stigmergy 钩子检测到跨 CLI 意图
    ↓
解析：target_cli = "claude", task = "analyze code with code-reviewer skill"
    ↓
调用 stigmergy 路由：stigmergy.route(target_cli, task, context)
    ↓
选择 Claude CLI 适配器
    ↓
通过适配器调用 Claude CLI
```

**第二层：Claude CLI 适配器**

```javascript
// src/adapters/claude/hook_adapter.py
async function executeThroughClaudeCLI(task, context) {
    // 1. 启动 Claude CLI 进程
    const claudeProcess = spawn('claude', ['--task', task]);
    
    // 2. 如果任务包含技能引用，Claude CLI 会自动通过 openskills 加载
    // "analyze code with code-reviewer skill"
    //   → Claude 识别 "code-reviewer skill"
    //   → 执行 openskills read code-reviewer
    //   → 加载技能指令
    //   → 按指令执行
    
    // 3. 捕获 Claude CLI 的输出
    const result = await claudeProcess.getOutput();
    
    // 4. 返回给 Qwen CLI
    return result;
}
```

**关键限制和真相**：

| 方面 | 真实情况 | 常见误解 |
|------|----------|----------|
| 技能格式 | SKILL.md 是通用的 Markdown | ❌ 需要为每个 CLI 重写 |
| 技能加载 | 只有 Claude CLI 原生支持 SKILL.md | ❌ 所有 CLI 都直接支持 |
| 跨 CLI 调用 | 通过 stigmergy 路由到 Claude CLI | ❌ 技能在所有 CLI 中原生运行 |
| 适配器作用 | 转换调用方式，不转换技能格式 | ❌ 适配器转换技能内容 |
| 实际执行 | 始终在 Claude CLI 中执行 | ❌ 在发起 CLI 中执行 |

**实际场景分析**：

```bash
# 场景 1：在 Claude CLI 中直接使用（原生）
claude> "use code-reviewer to check main.py"
# ✅ 直接通过 openskills 加载技能
# ✅ Claude 读取指令并执行
# ✅ 无需 stigmergy

# 场景 2：在 Qwen CLI 中使用 Claude 技能（跨 CLI）
qwen> "use claude's code-reviewer to check main.py"
# ⚠️ Qwen 不直接支持 SKILL.md 格式
# ✅ Qwen 的 stigmergy 钩子检测到跨 CLI 调用
# ✅ 调用 stigmergy 路由层
# ✅ 路由到 Claude CLI 适配器
# ✅ 启动 Claude CLI 执行任务
# ✅ 结果返回到 Qwen CLI
# ⚠️ 实际执行在 Claude CLI 中，不是 Qwen 中

# 场景 3：Qwen CLI 原生使用（需要转换）
qwen> "use data-analyzer"
# ❌ Qwen 不理解 SKILL.md 格式
# ✅ 需要通过适配器转换为 Qwen agent 格式
# ✅ 转换后的配置文件安装到 ~/.qwen/agents/
# ✅ Qwen 使用自己的格式执行
```

### 验证测试流程

#### 测试 1：验证 SKILL.md 格式正确性

```bash
# 检查 YAML frontmatter
cat my-skill/SKILL.md | head -n 10

# 预期输出：
---
name: my-skill
description: Brief description
---

# 验证工具
python << 'EOF'
import yaml
import re

with open('my-skill/SKILL.md', 'r') as f:
    content = f.read()

# 提取 YAML
match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
if match:
    try:
        metadata = yaml.safe_load(match.group(1))
        assert 'name' in metadata, "缺少 name 字段"
        assert 'description' in metadata, "缺少 description 字段"
        print("✅ YAML frontmatter 格式正确")
    except Exception as e:
        print(f"❌ YAML 解析失败: {e}")
else:
    print("❌ 未找到 YAML frontmatter")
EOF
```

#### 测试 2：在 Claude CLI 中直接测试

```bash
# 前提：已安装 openskills 和 Claude CLI

# 1. 安装技能到本地
cp -r my-skill ~/.claude/skills/

# 2. 验证技能可被找到
openskills list | grep my-skill

# 预期输出：
# my-skill    Brief description    project

# 3. 测试加载技能
openskills read my-skill

# 预期输出：
# Reading: my-skill
# Base directory: /home/user/.claude/skills/my-skill
# 
# ---
# name: my-skill
# description: Brief description
# ---
# 
# [技能内容]

# 4. 在 Claude CLI 中实际使用
claude << 'EOF'
Load the my-skill and use it to [具体任务]
EOF

# 5. 观察 Claude 是否：
#    - 正确加载技能指令
#    - 按照指令执行任务
#    - 产生预期结果
```

#### 测试 3：验证脚本可执行性

```bash
# 测试 uv 脚本
cd my-skill/scripts

# 方式 1：uv 内联依赖脚本
uv run analyze.py --help

# 预期：显示帮助信息，无错误

# 方式 2：测试实际功能
echo '{"test": "data"}' | uv run analyze.py

# 预期：正确处理输入，输出分析结果

# 方式 3：零依赖脚本
python analyze_simple.py --help

# 预期：显示帮助信息，无错误
```

#### 测试 4：跨 CLI 调用测试（需要 Stigmergy）

```bash
# 前提：已部署 stigmergy 系统

# 1. 验证 stigmergy 可用
stigmergy status

# 预期输出：
# ✅ Claude CLI: Available
# ✅ Qwen CLI: Available
# ✅ Adapters: Loaded

# 2. 从 Qwen CLI 调用 Claude 技能
stigmergy use claude to "use my-skill to analyze test.json"

# 观察：
# - 是否正确路由到 Claude CLI
# - Claude 是否加载了技能
# - 是否返回结果

# 3. 智能路由测试
stigmergy call "use my-skill"

# 观察：
# - stigmergy 是否自动选择 Claude CLI
# - 是否成功执行
```

#### 测试 5：适配器转换测试（可选）

```bash
# 将 Claude SKILL.md 转换为 Qwen agent 格式

# 1. 运行适配器
node sscisubagent-skills/adapters/qwen-cli-adapter.js --convert

# 2. 检查输出
ls sscisubagent-skills/qwen-compatible/

# 预期：生成 my-skill.json

# 3. 验证转换后的格式
cat sscisubagent-skills/qwen-compatible/my-skill.json

# 预期：符合 Qwen agent JSON 格式

# 4. 安装到 Qwen CLI
node sscisubagent-skills/adapters/qwen-cli-adapter.js --install

# 5. 在 Qwen CLI 中测试
qwen agent list | grep my-skill

# 6. 实际使用
qwen agent use my-skill
```

### 完整验证清单

#### 基础验证（必须）

- [ ] YAML frontmatter 格式正确
- [ ] `name` 字段使用连字符小写
- [ ] `description` 字段存在且有意义
- [ ] 指令使用命令式语气（非第二人称）
- [ ] SKILL.md 文件小于 5000 字
- [ ] 文件编码为 UTF-8

#### Claude CLI 验证（推荐）

- [ ] `openskills list` 能找到技能
- [ ] `openskills read` 能加载技能
- [ ] 技能内容正确显示
- [ ] 在 Claude CLI 中能实际使用
- [ ] 脚本（如有）可正确执行
- [ ] 产生预期结果

#### 脚本验证（如有脚本）

- [ ] uv 脚本有正确的 shebang：`#!/usr/bin/env -S uv run`
- [ ] 内联依赖格式正确（PEP 723）
- [ ] 脚本可独立运行：`uv run scripts/xxx.py`
- [ ] 零依赖版本（如有）使用标准库
- [ ] 提供跨平台版本（.py, .sh, .ps1）
- [ ] 错误处理完善
- [ ] 输入输出格式明确

#### 跨 CLI 验证（可选，需要 Stigmergy）

- [ ] stigmergy 系统已部署
- [ ] Claude CLI 适配器可用
- [ ] 从其他 CLI 能调用 Claude 技能
- [ ] 上下文正确传递
- [ ] 结果正确返回

#### 适配器转换验证（可选）

- [ ] 适配器脚本运行成功
- [ ] 生成目标 CLI 格式配置
- [ ] 工具权限正确映射
- [ ] 安装到目标 CLI 成功
- [ ] 在目标 CLI 中可用

### 常见问题与解决

#### Q1：技能在 Claude CLI 中加载成功，但 Claude 不执行指令

**原因**：
- 指令不够明确或使用了第二人称
- Claude 没有识别到使用技能的意图

**解决**：
```markdown
❌ 错误写法：
"You should analyze the data by running the script."

✅ 正确写法：
"To analyze data:
1. Run `python scripts/analyze.py --input data.json`
2. Review the output in report.json
3. Summarize key findings"
```

#### Q2：跨 CLI 调用失败

**原因**：
- stigmergy 未正确部署
- 适配器未加载
- 目标 CLI 不可用

**诊断**：
```bash
# 检查 stigmergy 状态
stigmergy status

# 检查适配器
stigmergy adapters list

# 检查目标 CLI
which claude
claude --version

# 查看日志
stigmergy logs --tail 50
```

#### Q3：uv 脚本无法运行

**原因**：
- uv 未安装
- shebang 不正确
- 依赖声明格式错误

**解决**：
```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 验证 uv
uv --version

# 测试脚本
uv run --verbose scripts/xxx.py

# 如果 shebang 问题，直接用 uv run
uv run scripts/xxx.py  # 而不是 ./scripts/xxx.py
```

#### Q4：适配器转换后的格式不工作

**原因**：
- 目标 CLI 格式理解错误
- 工具映射不正确
- 系统提示词过长

**解决**：
```bash
# 查看转换后的配置
cat qwen-compatible/my-skill.json

# 验证 JSON 格式
python -m json.tool qwen-compatible/my-skill.json

# 手动调整后重新安装
vim qwen-compatible/my-skill.json
node qwen-cli-adapter.js --install
```

### 可信度评估

#### 技能本身（SKILL.md 格式）

**可信度：⭐⭐⭐⭐⭐ (5/5)**

- ✅ 基于 Anthropic 官方规范
- ✅ openskills 项目验证可行
- ✅ Claude Code 原生支持
- ✅ 纯文本格式，易于验证

#### 在 Claude CLI 中直接使用

**可信度：⭐⭐⭐⭐⭐ (5/5)**

- ✅ openskills 是成熟项目
- ✅ 测试覆盖充分
- ✅ 社区验证
- ✅ 本项目已验证

#### 通过 Stigmergy 跨 CLI 调用

**可信度：⭐⭐⭐ (3/5)**

- ⚠️ Stigmergy 是本项目特有实现
- ⚠️ 适配器需要正确部署
- ⚠️ 依赖多个 CLI 工具安装
- ✅ 架构设计合理
- ⚠️ 需要实际环境测试

**限制说明**：
1. 跨 CLI 调用实际是在目标 CLI 中执行
2. 不是所有 CLI 都能无缝切换
3. 上下文传递有一定损耗
4. 性能开销比直接调用大

#### 适配器格式转换

**可信度：⭐⭐⭐ (3/5)**

- ⚠️ 转换规则基于推测
- ⚠️ 不同 CLI 格式差异大
- ⚠️ 工具映射可能不完整
- ✅ 提供了基础框架
- ⚠️ 需要针对实际 CLI 调整

### 推荐的使用策略

#### 1. 优先在 Claude CLI 中使用（最可靠）

```bash
# 创建技能
create-skill my-analyzer

# 测试技能
openskills read my-analyzer

# 在 Claude CLI 中使用
claude
> "Load my-analyzer and analyze data.json"
```

#### 2. 跨 CLI 调用作为增强功能（谨慎使用）

```bash
# 确保 stigmergy 正确部署
stigmergy status

# 使用跨 CLI 调用
stigmergy use claude to "use my-analyzer on data.json"

# 出问题时回退到直接调用
claude
> "Load my-analyzer and analyze data.json"
```

#### 3. 适配器转换作为实验性功能（可选）

```bash
# 尝试转换
node qwen-cli-adapter.js --convert

# 手动验证转换结果
cat qwen-compatible/my-analyzer.json

# 如果正确，安装并测试
node qwen-cli-adapter.js --install
qwen agent use my-analyzer

# 出问题时，通过 stigmergy 调用 Claude 版本
qwen
> "use claude's my-analyzer"
```

## 总结

创建高质量技能的关键步骤：
1. **明确需求**：清楚技能要解决的问题
2. **合理设计**：选择合适的结构和复杂度
3. **规范编写**：遵循 SKILL.md 格式标准
4. **跨 CLI 兼容**：使用通用工具抽象和跨平台脚本
5. **适配器支持**：为主要 CLI 工具提供适配器
6. **充分测试**：验证功能和边界情况，测试所有支持的 CLI
7. **持续改进**：基于反馈不断优化

### 跨 CLI 技能开发最佳实践

1. **工具抽象化**：使用 `file.read` 而不是 `read_file`
2. **脚本跨平台**：优先使用 Python，提供 .sh 和 .ps1 备选
3. **上下文感知**：支持跨 CLI 的上下文传递
4. **环境检测**：脚本能检测运行环境并适配
5. **文档完善**：明确说明各 CLI 的使用方法
6. **适配器配置**：提供各主要 CLI 的配置示例
7. **测试覆盖**：在所有支持的 CLI 环境中测试

通过本元技能，你可以系统化地创建符合 Anthropic 规范的高质量技能包，并通过 Stigmergy 系统实现跨 CLI 支持，最大化技能的适用范围和价值。
