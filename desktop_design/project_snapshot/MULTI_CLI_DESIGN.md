# 多CLI集成设计文档

## 1. 架构设计

### 1.1 总体架构
```
Electron桌面应用
├── 主进程 (Node.js)
│   ├── CLI管理器
│   │   ├── Stigmergy CLI包装器
│   │   ├── Claude CLI包装器
│   │   ├── Qwen CLI包装器
│   │   ├── iFlow CLI包装器
│   │   ├── Gemini CLI包装器
│   │   └── Codex CLI包装器
│   ├── 进程管理器
│   ├── 配置管理器
│   └── 安全控制器
├── 渲染进程 (React)
│   ├── 统一CLI界面
│   ├── CLI特定功能组件
│   └── 状态管理
└── IPC通信层
    ├── 主进程 ↔ 渲染进程通信
    └── CLI执行结果传递
```

### 1.2 核心组件

#### 1.2.1 CLI管理器
- 统一的CLI工具管理接口
- 负责CLI工具的发现、加载和执行
- 提供标准化的命令执行和结果处理

#### 1.2.2 进程管理器
- 管理CLI工具的子进程
- 处理进程的启动、停止和资源回收
- 监控进程状态和性能指标

#### 1.2.3 配置管理器
- 管理各CLI工具的配置
- 提供统一的配置界面和存储
- 支持配置的导入导出和同步

## 2. CLI包装器设计

### 2.1 基础包装器类
```javascript
class BaseCLIWrapper {
  constructor(name, executablePath) {
    this.name = name;
    this.executablePath = executablePath;
    this.isAvailable = false;
  }
  
  async checkAvailability() { }
  async executeCommand(command, args) { }
  async parseOutput(output) { }
  async handleError(error) { }
}
```

### 2.2 特定CLI包装器

#### 2.2.1 Stigmergy CLI包装器
```javascript
class StigmergyCLIWrapper extends BaseCLIWrapper {
  constructor() {
    super('stigmergy', 'stigmergy');
  }
  
  // 特有功能实现
  async executeSkillCommand(subcommand, args) { }
  async crossCLICall(cliName, skillName) { }
}
```

#### 2.2.2 Claude CLI包装器
```javascript
class ClaudeCLIWrapper extends BaseCLIWrapper {
  constructor() {
    super('claude', 'claude');
  }
  
  // 特有功能实现
  async managePlugins(action, pluginName) { }
  async manageMCP(action, config) { }
}
```

#### 2.2.3 Qwen CLI包装器
```javascript
class QwenCLIWrapper extends BaseCLIWrapper {
  constructor() {
    super('qwen', 'qwen');
  }
  
  // 特有功能实现
  async manageExtensions(action, extensionName) { }
  async manageMCP(action, config) { }
}
```

#### 2.2.4 iFlow CLI包装器
```javascript
class IFlowCLIWrapper extends BaseCLIWrapper {
  constructor() {
    super('iflow', 'iflow');
  }
  
  // 特有功能实现
  async manageAgents(action, agentName) { }
  async manageWorkflows(action, workflowName) { }
}
```

#### 2.2.5 Gemini CLI包装器
```javascript
class GeminiCLIWrapper extends BaseCLIWrapper {
  constructor() {
    super('gemini', 'gemini');
  }
  
  // 特有功能实现
  async manageExtensions(action, extensionName) { }
  async manageMCP(action, config) { }
}
```

#### 2.2.6 Codex CLI包装器
```javascript
class CodexCLIWrapper extends BaseCLIWrapper {
  constructor() {
    super('codex', 'codex');
  }
  
  // 特有功能实现
  async manageMCP(action, config) { }
  async codeReview(files) { }
}
```

## 3. 技能管理系统设计

### 3.1 统一技能接口
```javascript
class SkillManager {
  async discoverSkills(cliWrapper) { }
  async installSkill(cliWrapper, skillSource) { }
  async removeSkill(cliWrapper, skillName) { }
  async listSkills(cliWrapper) { }
  async readSkill(cliWrapper, skillName) { }
}
```

### 3.2 技能数据结构
```javascript
class Skill {
  constructor(name, description, cliTool, version, path) {
    this.name = name;
    this.description = description;
    this.cliTool = cliTool;
    this.version = version;
    this.path = path;
    this.installedAt = new Date();
  }
}
```

## 4. 会话管理系统设计

### 4.1 统一会话接口
```javascript
class SessionManager {
  async createSession(cliWrapper, sessionId) { }
  async resumeSession(cliWrapper, sessionId) { }
  async saveSession(cliWrapper, sessionData) { }
  async listSessions(cliWrapper) { }
}
```

### 4.2 会话数据结构
```javascript
class Session {
  constructor(id, cliTool, createdAt, data) {
    this.id = id;
    this.cliTool = cliTool;
    this.createdAt = createdAt;
    this.data = data;
    this.lastAccessed = new Date();
  }
}
```

## 5. 用户界面设计

### 5.1 主界面布局
```
+---------------------------------------------------+
| 菜单栏                                           |
+-----------+---------------------------------------+
| 工具栏    |                                       |
+-----------+                                       |
| CLI选择   |                                       |
|           |                                       |
|           |                                       |
|           |          主工作区域                   |
|           |                                       |
|           |                                       |
|           |                                       |
+-----------+---------------------------------------+
| 状态栏                                           |
+---------------------------------------------------+
```

### 5.2 CLI选择面板
- 显示所有可用的CLI工具
- 显示各CLI工具的状态（已安装/未安装）
- 提供快速切换CLI工具的功能

### 5.3 统一命令执行界面
- 命令输入框
- 参数配置区域
- 执行按钮
- 结果展示区域

### 5.4 CLI特定功能界面
- 根据选中的CLI工具显示特定功能
- 如技能管理、会话管理、插件管理等

## 6. 安全设计

### 6.1 命令白名单
- 为每个CLI工具维护允许执行的命令列表
- 对危险命令进行特殊处理和确认

### 6.2 文件系统访问控制
- 限制CLI工具对文件系统的访问权限
- 实现沙箱机制隔离敏感操作

### 6.3 权限管理
- 最小权限原则
- 用户确认机制
- 审计日志记录

## 7. 数据存储设计

### 7.1 配置存储
- 使用Electron的userData目录存储配置
- 支持JSON格式的配置文件

### 7.2 会话存储
- SQLite数据库存储会话信息
- 支持会话数据的加密存储

### 7.3 技能存储
- 本地文件系统存储技能文件
- 数据库记录技能元信息

## 8. IPC通信设计

### 8.1 主进程到渲染进程
- CLI执行结果推送
- 状态更新通知
- 错误信息传递

### 8.2 渲染进程到主进程
- CLI命令执行请求
- 配置更新请求
- 会话管理请求

## 9. 错误处理设计

### 9.1 统一错误格式
```javascript
class CLIError extends Error {
  constructor(message, cliTool, command, exitCode, stderr) {
    super(message);
    this.cliTool = cliTool;
    this.command = command;
    this.exitCode = exitCode;
    this.stderr = stderr;
  }
}
```

### 9.2 错误处理策略
- 分类处理不同类型的错误
- 提供用户友好的错误提示
- 记录详细的错误日志