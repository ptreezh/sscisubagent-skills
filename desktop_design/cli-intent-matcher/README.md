# CLI意图匹配器

CLI意图匹配器是一个本地AI模型，用于理解用户自然语言意图并自动匹配最适合的CLI工具、技能和参数配置。

## 功能特性

- **智能意图识别**: 理解用户自然语言输入，自动识别任务类型
- **CLI工具匹配**: 自动选择最适合的CLI工具（Claude、Qwen、Gemini等）
- **技能识别**: 识别并匹配相关的Stigmergy技能
- **参数推荐**: 推荐最优参数配置
- **安全执行**: 提供安全的命令执行和验证机制
- **备选方案**: 当首选方案失败时提供备选方案

## 系统架构

```
用户输入 → 意图分类器 → CLI匹配器 → 命令执行 → 结果返回
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 1. 数据收集
首先运行数据收集器以扫描系统中的CLI工具和技能：

```bash
python src/data_collector.py
```

### 2. 模型训练
训练意图分类模型：

```bash
python src/model_trainer.py
```

### 3. 运行API服务
启动API服务：

```bash
python src/api.py
```

## API端点

- `GET /health` - 健康检查
- `POST /classify` - 分类用户意图
- `POST /execute` - 执行用户意图
- `POST /plan` - 获取执行计划
- `POST /validate` - 验证命令
- `GET /skills` - 获取可用技能
- `GET /cli-tools` - 获取可用CLI工具

## API示例

### 分类用户意图
```bash
curl -X POST http://localhost:5000/classify \
  -H "Content-Type: application/json" \
  -d '{"user_input": "帮我设计一个按钮组件"}'
```

### 获取执行计划
```bash
curl -X POST http://localhost:5000/plan \
  -H "Content-Type: application/json" \
  -d '{"user_input": "写一份项目文档"}'
```

## 组件说明

### data_collector.py
扫描系统中的所有CLI工具和技能，收集其功能信息。

### model_trainer.py
训练意图分类模型，学习用户意图到CLI工具的映射关系。

### intent_classifier.py
根据用户输入分类意图并推荐最合适的工具和参数。

### cli_matcher.py
执行实际的CLI命令或生成执行计划。

### api.py
提供REST API接口，便于集成到桌面应用中。

## 安全考虑

- 所有命令执行都包含超时机制
- 提供命令验证功能
- 默认情况下仅返回执行计划而不实际执行
- 包含错误处理和备选方案机制

## 扩展性

- 易于添加新的CLI工具支持
- 可以持续训练模型以提高准确性
- 支持插件式技能扩展