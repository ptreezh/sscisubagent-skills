# SSCI子智能体技能包安装指南

本指南介绍如何使用 uv 包管理器安装 SSCI子智能体技能包的依赖。

## 系统要求

- Python 3.8 或更高版本
- uv 包管理器 (推荐) 或 pip
- 操作系统: Windows, macOS, Linux

## 安装方式

### 1. 基础安装（核心依赖）
```bash
uv install ssci-subagent-skills
```

### 2. 安装带统计分析功能
```bash
uv install "ssci-subagent-skills[statistics]"
```

### 3. 安装带信度效度分析功能
```bash
uv install "ssci-subagent-skills[psychometrics]"
```

### 4. 安装网络分析扩展功能
```bash
uv install "ssci-subagent-skills[network]"
```

### 5. 安装完整功能包
```bash
uv install "ssci-subagent-skills[all]"
```

## 可选依赖说明

### statistics (高级统计分析)
- `statsmodels`: 高级统计建模
- `pingouin`: 统计分析工具包
- `scikit-learn`: 机器学习算法

### psychometrics (心理测量学)
- `factor-analyzer`: 因子分析
- `statsmodels`: 高级统计建模
- `pingouin`: 统计分析工具包

### network (网络分析扩展)
- `python-louvain`: 社区检测算法
- `igraph`: 网络分析库

## 使用示例

### 安装完整功能
```bash
# 使用清华源加速下载
uv pip install --index https://pypi.tuna.tsinghua.edu.cn/simple/ "ssci-subagent-skills[all]"
```

### 为特定技能安装依赖
```bash
# 仅安装数学统计技能依赖
uv pip install --index https://pypi.tuna.tsinghua.edu.cn/simple/ "ssci-subagent-skills[statistics]"

# 仅安装信度效度分析技能依赖
uv pip install --index https://pypi.tuna.tsinghua.edu.cn/simple/ "ssci-subagent-skills[psychometrics]"

# 仅安装网络分析技能依赖
uv pip install --index https://pypi.tuna.tsinghua.edu.cn/simple/ "ssci-subagent-skills[network]"
```

## 验证安装

安装完成后，可以运行以下命令验证技能是否正常工作：

```bash
# 测试网络计算技能（基础功能）
python -c "from skills.performing-network-computation.scripts.calculate_centrality import *; print('网络计算技能正常')"

# 测试数学统计技能（需要statistics依赖）
python -c "from skills.mathematical-statistics.scripts.statistics_toolkit import SocialScienceStatistics; print('数学统计技能正常')"

# 测试信度效度技能（需要psychometrics依赖）
python -c "from skills.validity-reliability.scripts.validity_reliability_toolkit import ValidityReliabilityAnalyzer; print('信度效度技能正常')"

# 测试场域分析技能
python -c "from skills.field-analysis.scripts.identify_field_boundary import *; print('场域分析技能正常')"

# 测试扎根理论开放编码技能
python -c "from skills.performing-open-coding.scripts.preprocess_text import *; print('开放编码技能正常')"
```

## 配置和使用

### 1. 配置智能体
安装完成后，可以通过以下方式使用技能：

```python
# 导入技能系统
from ssci_skills_system import SS CISkillsSystem

# 初始化技能系统
system = SS CISkillsSystem()

# 使用特定技能
result = system.execute_skill("performing-open-coding", data, context)
```

### 2. 依赖管理
系统实现了智能依赖管理：
- 优先使用高级功能包
- 自动检测并安装缺失的依赖
- 当高级包不可用时自动降级到基础实现
- 保持功能完整性的同时提供最佳性能

## 注意事项

1. 高级依赖包（如 statsmodels, factor-analyzer）可能需要较长的安装时间
2. 某些包可能需要编译，需要相应的编译工具链
3. 建议使用虚拟环境进行安装，避免影响系统Python环境
4. 如果遇到安装问题，可以尝试使用国内镜像源（如清华源）
5. 部分技能包含定量计算脚本，需要相应依赖才能完全发挥功能

## 故障排除

### 安装失败
如果安装失败，可以尝试：
```bash
# 清理缓存后重试
uv cache clean
uv pip install --no-cache-dir --index https://pypi.tuna.tsinghua.edu.cn/simple/ "ssci-subagent-skills[all]"
```

### 缺少编译工具
如果遇到编译错误，Windows用户可以安装 Microsoft C++ Build Tools：
```bash
# 或使用 conda 安装依赖
conda install statsmodels factor-analyzer pingouin
```

### 依赖冲突
如果遇到依赖冲突：
```bash
# 创建新的虚拟环境
python -m venv ssci_env
source ssci_env/bin/activate  # Linux/macOS
# 或
ssci_env\Scripts\activate  # Windows

# 在新环境中安装
uv install "ssci-subagent-skills[all]"
```

## 性能优化建议

1. **选择性安装**: 根据需要安装特定功能组，避免安装不必要的依赖
2. **缓存机制**: 系统内置缓存机制，重复计算会更快
3. **并行处理**: 支持多线程处理大规模数据
4. **降级机制**: 在资源受限环境中自动使用轻量级实现

## 升级指南

要升级到最新版本：
```bash
uv pip install --upgrade "ssci-subagent-skills[all]"
```

## 支持的智能体

安装后，以下智能体可使用相应技能：
- `ant-expert` → 所有ANT相关技能
- `field-analysis-expert` → 所有场域分析技能
- `grounded-theory-expert` → 扎根理论系列技能
- `sna-expert` → 社会网络分析技能