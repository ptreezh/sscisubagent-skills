# 本地化Subagent技能Web界面方案

## 📋 项目概述

### 核心目标
创建一个完全支持Stigmergy包功能的本地化Web界面，让用户能够通过浏览器访问和使用本地的CLI工具、Subagent和Skills，实现完全离线的AI助手体验。

### 关键需求
- ✅ **完整支持Stigmergy包的所有命令和功能**
- ✅ **支持跨CLI协同调用的命令**
- ✅ **统一查看本地项目文件的功能**
- ✅ **扩展技能管理和会话恢复功能**
- ✅ **完全本地化运行，无需网络依赖**

### 用户使用流程
```
用户访问公网页面 → 下载Electron应用 → 本地安装运行 →
自动检测Stigmergy环境 → 完整功能使用 → 完全离线运行
```

---

## 🎯 技术方案对比

### 方案对比表

| 方案 | 开发复杂度 | 用户体验 | 维护成本 | CLI支持 | 推荐度 |
|------|------------|----------|----------|---------|--------|
| 云端服务平台 | 高 | 良好 | 高 | 完整 | ❌ 不推荐 |
| 纯HTML单文件 | 低 | 一般 | 极低 | 有限 | ⚠️ 基础版 |
| Electron桌面应用 | 中 | 优秀 | 低 | 完整 | ✅ 强烈推荐 |
| 浏览器扩展 | 中 | 良好 | 中 | 完整 | ⚠️ 高级版 |

### 最终推荐：Electron桌面应用

#### 优势分析
- ✅ **完全支持多CLI**：可调用任意本地CLI工具
- ✅ **原生跨CLI协同**：完美支持Stigmergy的跨CLI机制
- ✅ **系统级集成**：无安全限制，性能最佳
- ✅ **完整Stigmergy支持**：支持所有stigmergy命令和功能
- ✅ **项目管理能力**：统一查看和管理本地项目文件
- ✅ **技能管理增强**：安装、卸载、搜索、分类等完整功能
- ✅ **会话管理完善**：创建、保存、恢复、搜索会话
- ✅ **开发复杂度适中**：比Web方案简单，比纯手动方案强大
- ✅ **用户体验最佳**：桌面应用体验，功能完整

---

## 🛠️ 技术架构设计

### 核心组件架构
```
Electron桌面应用
├── 主进程 (main.js)
│   ├── CLI调用管理器
│   ├── 文件系统管理
│   ├── 进程管理
│   └── 安全控制
├── 渲染进程 (renderer.js)
│   ├── 用户界面
│   ├── 消息传递
│   ├── 状态管理
│   └── 事件处理
└── 通信层 (IPC)
    ├── 主进程↔渲染进程通信
    ├── CLI调用结果传递
    └── 错误处理机制
```

### 核心功能模块

#### 1. 完整的Stigmergy命令管理器
```javascript
class StigmergyManager {
    constructor() {
        this.cliPath = 'stigmergy';
        this.availableSkills = new Map();
        this.installedSkills = new Map();
        this.sessionHistory = [];
        this.currentSession = null;
    }
    
    // 执行任意stigmergy命令
    async executeCommand(command, args = []) {
        const fullCommand = [this.cliPath, command, ...args];
        
        try {
            const result = await this.callCLI(fullCommand);
            
            // 解析不同命令的返回结果
            const parsedResult = this.parseCommandResult(command, result);
            
            // 更新内部状态
            this.updateInternalState(command, parsedResult);
            
            return {
                success: true,
                command: command,
                args: args,
                result: parsedResult,
                rawOutput: result.output
            };
        } catch (error) {
            return {
                success: false,
                command: command,
                error: error.message
            };
        }
    }
    
    // 支持的stigmergy命令
    getSupportedCommands() {
        return [
            'list',           // 列出可用技能
            'use',            // 跨CLI技能调用
            'call',           // 直接技能调用
            'status',         // 查看系统状态
            'config',         // 配置管理
            'install',        // 安装技能
            'remove',         // 移除技能
            'update',         // 更新技能
            'search',         // 搜索技能
            'info',           // 技能详细信息
            'history',        // 命令历史
            'session',        // 会话管理
            'project'         // 项目管理
        ];
    }
    
    // 跨CLI技能调用
    async useCrossCLISkill(targetCLI, skillName, ...args) {
        return await this.executeCommand('use', [targetCLI, 'skill', skillName, ...args]);
    }
    
    // 直接技能调用
    async callSkill(skillName, ...args) {
        return await this.executeCommand('call', [skillName, ...args]);
    }
    
    // 项目管理功能
    async scanProjects(basePath) {
        return await this.executeCommand('project', ['scan', basePath]);
    }
    
    async viewProjectFiles(projectPath) {
        return await this.executeCommand('project', ['files', projectPath]);
    }
    
    async watchProject(projectPath) {
        return await this.executeCommand('project', ['watch', projectPath]);
    }
}
```

#### 2. Stigmergy跨CLI协同支持
```javascript
class StigmergyCoordinator {
    constructor() {
        this.cliCaller = new CLICaller();
    }
    
    // 执行stigmergy跨CLI调用
    async executeCrossCLICall(command) {
        try {
            // 解析stigmergy命令
            const parsed = this.parseStigmergyCommand(command);
            
            if (parsed.type === 'cross-cli') {
                return await this.handleCrossCLICall(parsed);
            } else if (parsed.type === 'single-cli') {
                return await this.cliCaller.callCLI(parsed.cli, parsed.args);
            }
        } catch (error) {
            return {
                success: false,
                error: `跨CLI调用失败: ${error.message}`
            };
        }
    }
    
    // 解析stigmergy命令
    parseStigmergyCommand(command) {
        // 解析类似 "stigmergy use claude skill grounded-theory" 的命令
        const parts = command.trim().split(' ');
        
        if (parts.includes('use') && parts.includes('skill')) {
            const useIndex = parts.indexOf('use');
            const skillIndex = parts.indexOf('skill');
            
            return {
                type: 'cross-cli',
                targetCLI: parts[useIndex + 1],
                skillName: parts[skillIndex + 1],
                args: parts.slice(skillIndex + 2)
            };
        }
        
        // 解析直接CLI调用
        const cliMap = {
            'iflow': 'iflow',
            'claude': 'claude', 
            'qwen': 'qwen'
        };
        
        for (const [key, cli] of Object.entries(cliMap)) {
            if (command.startsWith(cli)) {
                return {
                    type: 'single-cli',
                    cli: cli,
                    args: command.slice(cli.length).trim().split(' ')
                };
            }
        }
        
        return { type: 'unknown' };
    }
    
    // 处理跨CLI调用
    async handleCrossCLICall(parsed) {
        const { targetCLI, skillName, args } = parsed;
        
        try {
            // 方法1：直接调用目标CLI的技能
            if (targetCLI !== 'stigmergy') {
                return await this.cliCaller.callCLI(targetCLI, [
                    '--skill', skillName, ...args
                ]);
            }
            
            // 方法2：通过stigmergy协调
            return await this.cliCaller.callCLI('stigmergy', [
                'use', targetCLI, 'skill', skillName, ...args
            ]);
            
        } catch (error) {
            return {
                success: false,
                error: `跨CLI调用失败: ${error.message}`
            };
        }
    }
}
```

#### 3. 安全性控制
```python
def safe_execute(command, allowed_commands=None):
    if allowed_commands is None:
        allowed_commands = ['iflow', 'claude', 'qwen', 'stigmergy']
    
    # 解析命令
    parts = command.split()
    if not parts or parts[0] not in allowed_commands:
        raise SecurityError(f"Command {parts[0]} not allowed")
    
    # 执行命令
    try:
        result = subprocess.run(
            parts, 
            capture_output=True, 
            text=True, 
            timeout=30,
            check=True
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        raise TimeoutError("Command execution timeout")
```

---

## 🌟 用户界面设计

### 主要界面组件
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subagent本地助手</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { background: white; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .main-content { display: flex; gap: 20px; }
        .sidebar { width: 300px; background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .chat-area { flex: 1; background: white; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); display: flex; flex-direction: height: 80vh; }
        .chat-messages { flex: 1; padding: 20px; overflow-y: auto; }
        .chat-input { padding: 20px; border-top: 1px solid #eee; }
        .message { margin: 10px 0; padding: 15px; border-radius: 10px; max-width: 80%; }
        .user-message { background: #007bff; color: white; margin-left: auto; }
        .agent-message { background: #f8f9fa; border: 1px solid #dee2e6; }
        .status { padding: 10px; border-radius: 5px; margin: 10px 0; }
        .status.success { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .status.error { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .btn { padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        .btn-primary { background: #007bff; color: white; }
        .btn-secondary { background: #6c757d; color: white; }
        .form-control { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; margin: 5px 0; }
        .loading { display: none; text-align: center; padding: 20px; }
        .loading.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Subagent本地助手</h1>
            <p>完全本地运行，安全私密，无需网络</p>
            <div id="status" class="status">正在检测本地环境...</div>
        </div>
        
        <div class="main-content">
            <div class="sidebar">
                <h3>环境检测</h3>
                <div id="cli-status">
                    <div>🔍 检测CLI工具...</div>
                </div>
                
                <h3>可用Subagent</h3>
                <select id="subagent-select" class="form-control">
                    <option>加载中...</option>
                </select>
                
                <h3>跨CLI技能</h3>
                <div id="cross-cli-skills">
                    <!-- 动态加载跨CLI技能 -->
                </div>
                
                <h3>快速操作</h3>
                <button class="btn btn-primary" onclick="refreshSubagents()" style="width: 100%; margin: 5px 0;">刷新列表</button>
                <button class="btn btn-secondary" onclick="clearChat()" style="width: 100%; margin: 5px 0;">清空对话</button>
                <button class="btn btn-secondary" onclick="exportChat()" style="width: 100%; margin: 5px 0;">导出对话</button>
            </div>
            
            <div class="chat-area">
                <div class="chat-messages" id="chat-messages">
                    <div class="agent-message">
                       欢迎使用Subagent本地助手！请先确保已安装Stigmergy CLI工具。
                    </div>
                </div>
                <div class="chat-input">
                    <div style="display: flex; gap: 10px;">
                        <input type="text" id="message-input" class="form-control" placeholder="输入您的问题..." style="flex: 1;">
                        <button class="btn btn-primary" onclick="sendMessage()">发送</button>
                    </div>
                </div>
                <div class="loading" id="loading">
                    <div>🤖 AI正在思考...</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
```

---

## 📚 参考开源项目分析

### 直接相关的开源项目

#### 1. **Open Interpreter** (最相关)
```
GitHub: https://github.com/OpenInterpreter/open-interpreter
⭐ 45K+ stars

核心功能：
├── 本地CLI工具调用
├── 多种AI模型支持
├── 代码执行环境
├── 文件系统访问
└── 跨平台支持

技术栈：
├── Python后端
├── React前端
├── Electron桌面版
└── 终端界面

与我们需求的相似度：85%
```

#### 2. **Continue** (VS Code插件)
```
GitHub: https://github.com/continuedev/continue
⭐ 12K+ stars

核心功能：
├── VS Code集成
├── 多AI模型支持
├── 代码上下文理解
├── 本地文件访问
└── 插件系统

技术栈：
├── VS Code Extension API
├── TypeScript
├── React
└── 多AI提供商集成

相似度：70%
```

#### 3. **Codeium Chat**
```
GitHub: https://github.com/Exafunction/codeium-chat
⭐ 3K+ stars

核心功能：
├── 本地代码聊天
├── 多文件上下文
├── AI模型集成
├── 桌面应用
└── IDE集成

技术栈：
├── Electron
├── React
├── Python后端
└── 多AI支持

相似度：75%
```

### CLI集成相关的项目

#### 4. **Aider** (AI辅助编程)
```
GitHub: https://github.com/paul-gauthier/aider
⭐ 18K+ stars

核心功能：
├── Git集成
├── 多AI模型支持
├── 文件编辑
├── 终端界面
└── 代码理解

CLI集成方式：
├── 直接调用AI API
├── 本地文件操作
├── Git命令集成
└── 终端交互

相似度：60%
```

#### 5. **ChatGPT-CLI**
```
GitHub: https://github.com/kardolus/chatgpt-cli
⭐ 2K+ stars

核心功能：
├── 命令行ChatGPT
├── 文件上传
├── 对话历史
├── 配置管理
└── 多模型支持

CLI集成特点：
├── 纯终端界面
├── 配置文件管理
├── API密钥管理
└── 对话持久化

相似度：50%
```

### Web界面 + 本地CLI的项目

#### 6. **WebUI for Stable Diffusion**
```
GitHub: https://github.com/AUTOMATIC1111/stable-diffusion-webui
⭐ 115K+ stars

核心功能：
├── Web界面
├── 本地后端服务
├── Python脚本集成
├── 文件管理
└── 插件系统

架构特点：
├── Flask后端
├── React前端
├── 本地Python脚本调用
└── 文件系统访问

相似度：65%
```

#### 7. **Oobabooga WebUI**
```
GitHub: https://github.com/oobabooga/text-generation-webui
⭐ 25K+ stars

核心功能：
├── 多模型Web界面
├── 本地模型加载
├── 插件系统
├── API接口
└── 聊天界面

技术架构：
├── Gradio界面
├── Python后端
├── 模型管理
└── 扩展系统

相似度：60%
```

---

## 💡 从成功案例学到的关键经验

### 1. **Open Interpreter的成功模式**
```python
# 它的CLI调用架构
class LocalCodeExecutor:
    def __init__(self):
        self.allowed_commands = ['python', 'node', 'git', 'curl']
    
    def execute_command(self, command):
        if self.is_safe_command(command):
            return subprocess.run(command, shell=True, capture_output=True)
        else:
            raise SecurityError("Command not allowed")
```

**关键启示：**
- 安全性检查很重要
- 命令白名单机制
- 沙箱执行环境

### 2. **Continue的插件系统**
```typescript
// 它的插件架构
interface Provider {
  name: string;
  models: Model[];
  chat: (messages: Message[]) => Promise<string>;
}

class ModelManager {
  private providers: Map<string, Provider> = new Map();
  
  registerProvider(provider: Provider) {
    this.providers.set(provider.name, provider);
  }
}
```

**关键启示：**
- 插件化架构很灵活
- 统一的接口设计
- 易于扩展新模型

### 3. **WebUI的文件处理**
```python
# 它的文件管理
class FileManager:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.upload_path = self.base_path / "uploads"
    
    def save_upload(self, file, filename):
        file_path = self.upload_path / filename
        with open(file_path, 'wb') as f:
            f.write(file.getvalue())
        return str(file_path)
```

**关键启示：**
- 文件路径管理很重要
- 上传文件的存储策略
- 安全路径验证

---

## 🚀 推荐的架构实现

### 基于成功案例的综合架构
```javascript
// 基于Open Interpreter + Continue + WebUI的综合架构
class SubagentDesktop {
    constructor() {
        this.cliManager = new CLIManager();
        this.fileManager = new FileManager();
        this.modelManager = new ModelManager();
        this.pluginManager = new PluginManager();
    }
    
    // CLI管理（参考Open Interpreter）
    async callCLI(cli, args, options = {}) {
        const safetyCheck = await this.cliManager.checkSafety(cli, args);
        if (!safetyCheck.safe) {
            throw new SecurityError(safetyCheck.reason);
        }
        
        return await this.cliManager.execute(cli, args, options);
    }
    
    // 模型管理（参考Continue）
    async switchModel(provider, model) {
        return await this.modelManager.setActiveProvider(provider, model);
    }
    
    // 插件系统（参考Continue）
    loadPlugin(pluginPath) {
        return this.pluginManager.load(pluginPath);
    }
}
```

### 可以直接借鉴的代码

#### 1. **CLI安全执行**（来自Open Interpreter）
```python
def safe_execute(command, allowed_commands=None):
    if allowed_commands is None:
        allowed_commands = ['iflow', 'claude', 'qwen', 'stigmergy']
    
    # 解析命令
    parts = command.split()
    if not parts or parts[0] not in allowed_commands:
        raise SecurityError(f"Command {parts[0]} not allowed")
    
    # 执行命令
    try:
        result = subprocess.run(
            parts, 
            capture_output=True, 
            text=True, 
            timeout=30,
            check=True
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        raise TimeoutError("Command execution timeout")
```

#### 2. **文件上传处理**（来自WebUI）
```python
class SafeFileHandler:
    def __init__(self, upload_dir, max_size=10*1024*1024):
        self.upload_dir = Path(upload_dir)
        self.max_size = max_size
        self.allowed_extensions = ['.txt', '.md', '.py', '.json']
    
    def handle_upload(self, file, filename):
        # 安全检查
        if not self.is_safe_file(filename, file.size):
            raise SecurityError("File not allowed")
        
        # 保存文件
        file_path = self.upload_dir / filename
        with open(file_path, 'wb') as f:
            f.write.file.getvalue()
        
        return file_path
```

---

## 🌟 完整的Stigmergy功能支持需求

### 📋 Stigmergy核心功能需求清单

#### 🔧 命令执行系统
- ✅ **完整的stigmergy命令支持**
  - stigmergy list - 列出可用技能
  - stigmergy use <cli> skill <name> - 跨CLI技能调用
  - stigmergy call <skill> - 直接技能调用
  - stigmergy status - 查看系统状态
  - stigmergy config - 配置管理
  - stigmergy install/remove/update - 技能管理
  - stigmergy search/info - 技能搜索和信息
  - stigmergy history - 命令历史
  - stigmergy session - 会话管理

#### 🔄 跨CLI协同调用支持
- ✅ **跨CLI命令解析和执行**
  - 解析 "stigmergy use claude skill grounded-theory" 命令
  - 支持不同CLI间的技能调用
  - 处理跨CLI的数据传递
  - 错误处理和回滚机制

#### 📁 本地项目管理功能
- ✅ **项目文件统一查看**
  - 扫描本地项目目录
  - 文件树结构展示
  - 项目文件监控
  - 文件内容预览
  - 项目类型识别

#### 🛠️ 扩展技能管理功能
- ✅ **完整的技能生命周期管理**
  - 技能安装和卸载
  - 技能更新和版本管理
  - 技能搜索和分类
  - 技能依赖关系管理
  - 技能详细信息查看

#### 💾 会话恢复功能
- ✅ **完整的会话管理系统**
  - 会话创建和保存
  - 会话加载和恢复
  - 会话历史记录
  - 会话搜索和管理
  - 会话上下文恢复

---

## 📊 项目实施计划

### 开发阶段规划

#### 第一阶段：Stigmergy核心集成（4周）
```
Week 1-2: Stigmergy基础架构
├── Stigmergy命令管理器实现
├── 完整命令解析系统
├── 跨CLI协同支持
└── 基础UI界面开发

Week 3-4: 核心功能实现
├── 项目管理功能
├── 技能管理系统
├── 会话管理系统
└── 错误处理完善
```

#### 第二阶段：增强功能和用户体验（3周）
```
Week 5-6: 功能增强
├── 界面美化和优化
├── 技能分类和搜索
├── 项目文件树展示
├── 会话历史管理
└── 配置文件管理

Week 7: 高级功能
├── 插件系统实现
├── 性能优化
├── 快捷键支持
└── 用户文档编写
```

#### 第三阶段：测试和发布（2周）
```
Week 8-9: 测试和发布
├── Stigmergy功能测试
├── 跨CLI协同测试
├── 项目管理测试
├── 用户体验测试
├── 文档完善
└── 发布准备
```

### 开发资源需求

#### 人员配置
```
核心团队：
├── 前端开发工程师 × 1 (Electron + Web技术)
├── 后端开发工程师 × 1 (Node.js + Stigmergy集成)
├── Stigmergy专家 × 1 (功能需求验证)
└── 测试工程师 × 0.5 (功能测试 + 用户测试)

总开发周期：9周
总人力成本：约20-30万人民币
```

#### 技术栈
```
前端技术：
├── Electron (桌面应用框架)
├── HTML5 + CSS3 + JavaScript
├── React (复杂UI组件)
├── Bootstrap (UI框架)
└── Monaco Editor (代码编辑)

后端技术：
├── Node.js (主进程)
├── Child Process (CLI调用)
├── IPC (进程间通信)
├── File System API (文件处理)
└── SQLite (本地数据存储)

Stigmergy集成：
├── Stigmergy CLI 完整集成
├── 跨CLI协同机制
├── 技能包管理系统
└── 项目文件管理

开发工具：
├── VS Code (开发环境)
├── Git (版本控制)
├── GitHub (代码托管)
└── Electron Builder (打包发布)
```

---

## 🎯 成功指标和验收标准

### 功能指标
- ✅ **完整Stigmergy支持**：支持所有stigmergy命令和功能
- ✅ **跨CLI协同功能**：完美支持跨CLI技能调用
- ✅ **项目管理能力**：统一查看和管理本地项目文件
- ✅ **技能管理增强**：完整的技能生命周期管理
- ✅ **会话管理完善**：创建、保存、恢复、搜索会话
- ✅ **多CLI支持**：支持4+种主流CLI工具检测和调用
- ✅ **用户界面友好**：直观的操作界面和清晰的功能布局
- ✅ **文件处理能力**：支持项目文件查看和管理
- ✅ **安全性和稳定性**：确保本地数据安全和系统稳定

### Stigmergy特定指标
- ✅ **命令执行成功率**：> 95%
- ✅ **跨CLI协同响应时间**：< 3秒
- ✅ **技能管理响应时间**：< 2秒
- ✅ **项目文件加载时间**：< 5秒
- ✅ **会话恢复时间**：< 2秒
- ✅ **命令解析准确率**：> 98%

### 性能指标
- ✅ **CLI调用响应时间**：< 3秒
- ✅ **应用启动时间**：< 5秒
- ✅ **内存使用**：< 200MB
- ✅ **项目文件处理能力**：支持1000+文件的项目
- ✅ **并发处理能力**：支持多个CLI同时调用
- ✅ **文件上传支持**：支持10MB以内的文件

### 用户体验指标
- ✅ **零学习成本**：开箱即用，无需配置
- ✅ **界面美观直观**：现代化UI设计，操作逻辑清晰
- ✅ **错误提示友好**：详细的错误信息和解决建议
- ✅ **多平台支持**：Windows/Mac/Linux全平台兼容
- ✅ **功能完整性**：覆盖Stigmergy所有核心功能
- ✅ **响应速度**：界面操作响应时间 < 200ms

---

## 🔮 未来扩展计划

### 短期扩展（3-6个月）
```
Stigmergy功能增强：
├── 更多Stigmergy命令支持
├── 技能包市场建设
├── 项目模板系统
└── 自动化工作流支持

功能增强：
├── 更多CLI工具支持
├── 插件市场建设
├── 主题和界面定制
└── 快捷键和快捷操作
```

### 中期扩展（6-12个月）
```
生态建设：
├── 开发者API开放
├── 第三方插件支持
├── 云端同步功能
├── 技能包分享平台
└── 社区建设

Stigmergy生态：
├── 技能包开发和分发
├── 跨平台CLI支持
├── 企业级功能
└── 集成开发环境
```

### 长期扩展（1-2年）
```
平台化发展：
├── 多语言支持
├── 企业版功能
├── 移动端支持
├── AI能力增强
└── 云端协作平台

技术演进：
├── 微服务架构
├── 容器化部署
├── 分布式计算
└── 智能化推荐
```

---

## 📞 联系和支持

### 项目信息
- **项目名称**: Subagent本地助手
- **开发团队**: [团队名称]
- **许可证**: MIT License
- **源码地址**: [GitHub仓库地址]

### 技术支持
- **文档地址**: [文档网站]
- **问题反馈**: [Issues页面]
- **社区讨论**: [讨论区]
- **邮件联系**: [联系邮箱]

---

**本文档最后更新时间**: 2025年12月19日
**文档版本**: v1.0
**适用范围**: 本地化Subagent技能Web界面项目