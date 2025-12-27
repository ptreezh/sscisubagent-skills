# 科大讯飞星火大模型集成技能

集成科大讯飞星火大模型进行智能分析的标准化技能。

## 🚀 快速开始

### 基本信息
- **技能ID**: `spark-integration`
- **名称**: 科大讯飞星火大模型集成
- **版本**: 1.0.0
- **描述**: 集成科大讯飞星火大模型进行智能分析

### 初始化
```javascript
const SparkIntegrationSkill = require('./skill.js');
const config = {
    appId: process.env.SPARK_APP_ID,
    apiKey: process.env.SPARK_API_KEY,
    apiSecret: process.env.SPARK_API_SECRET
};

const skill = new SparkIntegrationSkill(config);
```

## 🛠️ 功能特性

- 文本分析：情感分析、摘要提取、主题识别
- 智能对话：基于星火大模型的自然语言交互
- 内容生成：文章、摘要、大纲生成
- 多模型支持：spark-max, spark-pro, spark-standard, spark-mini, spark-vision

## 📋 详细能力

### 文本分析
- `analyzeText(text, options)` - 分析文本内容
  - `text`: 待分析文本
  - `options.analysisType`: 分析类型（sentiment, summary, topic, general）
  - `options.model`: 指定模型

### 智能对话
- `chat(message, options)` - 进行智能对话
  - `message`: 用户消息
  - `options.history`: 对话历史
  - `options.model`: 指定模型

### 内容生成
- `generateContent(prompt, options)` - 生成内容
  - `prompt`: 生成提示
  - `options.contentType`: 内容类型（article, summary, outline, general）
  - `options.model`: 指定模型

## 📦 配置要求

### 环境变量
- `SPARK_APP_ID`: 科大讯飞应用ID
- `SPARK_API_KEY`: 科大讯飞API Key
- `SPARK_API_SECRET`: 科大讯飞API Secret

### 可选配置
- `model`: 默认模型（默认为spark-max）
- `baseUrl`: API基础URL

## 📖 完整API文档

### 方法列表

#### `getBasicInfo()`
获取技能基本信息

#### `getCapabilities()`
获取技能能力详情

#### `getAPIInterface()`
获取详细API接口信息

#### `getFullDocumentation()`
获取完整文档

#### `analyzeText(text, options)`
文本分析功能

#### `chat(message, options)`
智能对话功能

#### `generateContent(prompt, options)`
内容生成功能

#### `getAvailableModels()`
获取可用模型列表

#### `healthCheck()`
健康检查功能

## 🧪 使用示例

### 文本分析示例
```javascript
// 基本文本分析
const result = await skill.analyzeText("今天天气真好，心情也很愉悦");

// 情感分析
const sentiment = await skill.analyzeText("我对这个产品非常失望", {
    analysisType: "sentiment"
});

// 摘要提取
const summary = await skill.analyzeText("很长的文档内容...", {
    analysisType: "summary"
});
```

### 智能对话示例
```javascript
const response = await skill.chat("你好，介绍一下你自己");
console.log(response);

// 带历史记录的对话
const history = [
    { role: "user", content: "你好" },
    { role: "assistant", content: "你好，我是星火AI助手" }
];
const response2 = await skill.chat("你能做什么？", { history });
```

### 内容生成功能
```javascript
// 生成文章
const article = await skill.generateContent("人工智能发展趋势", {
    contentType: "article"
});

// 生成大纲
const outline = await skill.generateContent("在线教育的优势", {
    contentType: "outline"
});
```

## 🔒 安全说明

- API凭证应通过环境变量配置
- 不要在客户端代码中暴露API密钥
- 定期轮换API密钥

## 🐛 故障排除

### 常见问题
1. **API调用失败**：检查环境变量配置
2. **认证错误**：确认API凭证正确
3. **模型不可用**：检查指定模型是否支持

### 健康检查
```javascript
const health = await skill.healthCheck();
console.log(health);
```

## 📞 支持

如需技术支持，请查看主项目文档或联系开发团队。