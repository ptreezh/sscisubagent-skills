# 依赖管理说明

## 当前状态
目前所有算法脚本仅使用Python标准库：
- json: 数据格式处理
- sys: 系统参数和命令行接口
- datetime: 时间戳处理

## 依赖管理原则
1. 优先使用Python标准库
2. 如需外部依赖，使用项目中已定义的依赖
3. 使用uv进行依赖管理

## 项目现有依赖
项目pyproject.toml中已定义的依赖包括：
- networkx>=2.6.0 (用于网络分析)
- numpy>=1.21.0 (用于数值计算)
- scipy>=1.7.0 (用于科学计算)

## 算法优化建议
如需更精确的网络分析，可考虑使用networkx替代当前的自实现算法：
- 使用networkx的社区检测算法
- 使用networkx的中心性计算算法
- 使用networkx的图分析工具

## 使用方式
如需使用networkx增强算法功能：

```python
# 在算法脚本中
try:
    import networkx as nx
    # 使用networkx功能
    use_networkx = True
except ImportError:
    # 回退到标准库实现
    use_networkx = False
```

## 依赖安装
```bash
# 使用uv安装依赖
uv pip install networkx
# 或安装项目所有依赖
uv pip install -e .
```