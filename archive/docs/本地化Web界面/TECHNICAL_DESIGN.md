# 本地化Subagent技能桌面应用 - 技术设计文档

## 📋 设计概述

### 设计目标
创建一个智能化的本地化图形界面应用，用户通过直观的界面输入需求，后台通过本地部署的Stigmergy和各个AI CLI工具进行调用，实现智能体协作和技能处理，最终将结果输出到用户界面。在AI互动过程中，用户可以直接创建项目目录、管理文件、编辑内容，形成完整的AI辅助开发环境。所有AI调用和文件操作都在本地完成，确保数据隐私和处理独立性。

### 设计原则
- **用户交互优先**：提供直观、友好的图形界面，降低AI使用门槛
- **本地化部署优先**：所有AI调用基于本地部署的Stigmergy和CLI工具
- **项目文件管理**：在AI互动中支持完整的项目和文件操作
- **智能路由机制**：通过本地Stigmergy自动选择最合适的AI CLI和技能
- **数据隐私保护**：所有AI处理和文件操作都在本地完成，不依赖云端服务
- **实时协作支持**：支持多个本地AI和智能体的实时协作和数据传递
- **结果可视化**：将AI处理结果以直观的方式呈现给用户
- **持续交互设计**：支持用户与AI的持续对话和迭代优化

---

## 🏗️ 系统架构设计

### 整体架构图 (智能交互架构)
```
┌─────────────────────────────────────────────────────────────┐
│              Electron桌面应用 (智能交互架构)                    │
├─────────────────────────────────────────────────────────────┤
│  用户界面层 (React智能交互界面)                                │
│  ├── 需求输入界面                                            │
│  │   ├── 自然语言输入框 (支持文本/文件上传)                   │
│  │   ├── 任务类型选择 (分析/编程/写作/研究等)                 │
│  │   ├── 参数配置面板 (设置处理参数和输出格式)                 │
│  │   └── 历史记录查看 (查看之前的交互记录)                     │
│  ├── 技能管理界面                                            │
│  │   ├── 技能上传功能 (拖拽上传/文件选择/URL下载)              │
│  │   ├── 技能安装功能 (一键安装/批量安装/依赖检查)              │
│  │   ├── 技能配置功能 (参数设置/启用禁用/优先级)               │
│  │   ├── 技能市场功能 (浏览/搜索/评价技能)                    │
│  │   └── 技能监控功能 (状态监控/版本管理/自动更新)             │
│  ├── 项目管理界面                                            │
│  │   ├── 项目创建功能 (基于AI建议创建项目结构)                  │
│  │   ├── 目录树展示 (实时显示项目文件结构)                     │
│  │   ├── 文件操作功能 (创建/删除/重命名/复制/移动)               │
│  │   ├── 文件编辑功能 (集成代码编辑器，支持语法高亮)           │
│  │   ├── 版本控制功能 (Git集成，支持提交/分支/合并)              │
│  │   └── 项目模板功能 (提供常用项目模板快速初始化)               │
│  ├── 实时处理界面                                             │
│  │   ├── 任务状态显示 (实时显示AI处理进度)                    │
│  │   ├── 协作流程可视化 (显示AI之间的协作关系)                 │
│  │   ├── 中间结果展示 (显示处理过程中的中间结果)               │
│  │   └── 错误提示和重试 (处理异常情况)                        │
│  ├── 结果展示界面                                             │
│  │   ├── 结果可视化 (图表/表格/文本等多种形式)                 │
│  │   ├── 结果分析解读 (AI对结果的解释和建议)                   │
│  │   ├── 结果导出功能 (支持多种格式导出)                      │
│  │   └── 结果分享功能 (分享给其他用户或平台)                   │
│  └── 交互控制界面                                             │
│      ├── 继续对话 (基于当前结果继续提问)                       │
│      ├── 修改参数 (调整处理参数重新处理)                       │
│      ├── 切换AI (选择不同的AI工具处理)                         │
│      └── 保存会话 (保存当前交互状态)                          │
├─────────────────────────────────────────────────────────────┤
│  接口层 (Node.js CLI包装和文件操作)                           │
│  ├── Stigmergy CLI包装器                                     │
│  │   ├── 命令执行器 (调用stigmergy命令)                     │
│  │   ├── 输出解析器 (解析stigmergy输出)                     │
│  │   ├── 错误处理器 (处理命令执行错误)                       │
│  │   └── 进度监控器 (监控命令执行进度)                       │
│  ├── CLI配置文件操作器                                         │
│  │   ├── 配置读取器 (读取CLI配置文件)                       │
│  │   ├── 配置写入器 (写入CLI配置文件)                       │
│  │   ├── 配置验证器 (验证配置文件格式)                       │
│  │   └── 备份管理器 (配置文件备份和恢复)                     │
│  ├── 技能文件管理器                                           │
│  │   ├── 文件复制器 (复制技能到CLI目录)                     │
│  │   ├── 文件删除器 (从CLI目录删除技能)                     │
│  │   ├── 目录扫描器 (扫描技能目录结构)                       │
│  │   └── 变更监控器 (监控技能文件变化)                       │
│  └── 实时同步监控器                                           │
│      ├── 文件监控 (监控配置文件变化)                         │
│      ├── 状态同步 (同步界面和文件状态)                       │
│      ├── 事件分发 (分发变更事件)                             │
│      └── 冲突处理 (处理并发操作冲突)                         │
├─────────────────────────────────────────────────────────────┤
│  数据层 (本地数据管理)                                       │
│  ├── 技能信息缓存 (SQLite数据库)                              │
│  │   ├── 技能元数据缓存                                       │
│  │   ├── 技能依赖关系缓存                                     │
│  │   └── 技能状态缓存                                         │
│  ├── 用户操作历史 (SQLite数据库)                              │
│  │   ├── 操作记录                                             │
│  │   ├── 撤销/重做支持                                       │
│  │   └── 操作统计分析                                       │
│  └── 界面配置存储 (JSON文件)                                 │
│      ├── 用户偏好设置                                         │
│      ├── 界面布局配置                                         │
│      └── 主题和样式配置                                       │
├─────────────────────────────────────────────────────────────┤
│  集成层 (与现有系统深度集成)                                 │
│  ├── Stigmergy CLI集成                                       │
│  │   ├── 完整命令支持 (支持所有stigmergy命令)                │
│  │   ├── 输出格式解析 (解析命令输出格式)                     │
│  │   └── 错误信息处理 (处理CLI错误信息)                       │
│  ├── 多CLI配置集成                                             │
│  │   ├── Claude配置集成 (~/.claude/)                        │
│  │   ├── Qwen配置集成 (~/.qwen/)                            │
│  │   ├── iFlow配置集成 (~/.iflow/)                           │
│  │   └── 其他CLI配置集成                                      │
│  ├── 技能系统集成                                             │
│  │   ├── 现有部署机制利用 (利用scripts/deploy-*.js)          │
│  │   ├── 技能目录管理 (管理skills/目录)                      │
│  │   └── 技能文件操作 (复制/删除/更新技能文件)               │
│  └── 协作系统集成                                             │
│      ├── 跨CLI调用支持 (支持stigmergy use/call)              │
│      ├── 协作流程构建 (构建复杂协作流程)                     │
│      └── 协作状态监控 (监控协作执行状态)                     │
└─────────────────────────────────────────────────────────────┘
```

### 核心组件设计

#### 1. 技能管理器
```javascript
// 技能管理器 - 完整的技能生命周期管理
class SkillManager {
  constructor() {
    this.stigmergyWrapper = new StigmergyCLIWrapper();
    this.fileManager = new SkillFileManager();
    this.configManager = new SkillConfigManager();
  }

  // 技能上传功能
  async uploadSkill(source, options = {}) {
    try {
      let skillPath;
      
      if (source.type === 'file') {
        // 文件上传
        skillPath = await this.fileManager.saveUploadedFile(source.file);
      } else if (source.type === 'url') {
        // URL下载
        skillPath = await this.fileManager.downloadFromURL(source.url);
      } else if (source.type === 'github') {
        // GitHub仓库下载
        skillPath = await this.fileManager.cloneFromGitHub(source.repo);
      }
      
      // 验证技能格式
      const validation = await this.validateSkill(skillPath);
      if (!validation.valid) {
        throw new Error(`技能验证失败: ${validation.errors.join(', ')}`);
      }
      
      return {
        success: true,
        skillPath: skillPath,
        metadata: validation.metadata
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // 技能安装功能
  async installSkill(skillPath, targetCLIs = []) {
    try {
      // 检查技能依赖
      const dependencies = await this.checkDependencies(skillPath);
      
      // 安装依赖
      for (const dep of dependencies) {
        await this.installDependency(dep);
      }
      
      // 安装到Stigmergy
      const stigmergyResult = await this.stigmergyWrapper.installSkill(skillPath);
      
      // 同步到各个CLI
      const syncResults = [];
      for (const cli of targetCLIs) {
        const result = await this.stigmergyWrapper.syncSkills(cli);
        syncResults.push({ cli, result });
      }
      
      return {
        success: true,
        stigmergyResult: stigmergyResult,
        syncResults: syncResults,
        dependencies: dependencies
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // 技能配置功能
  async configureSkill(skillName, config, targetCLIs = []) {
    try {
      const results = [];
      
      for (const cli of targetCLIs) {
        // 更新CLI配置文件
        const result = await this.configManager.updateSkillConfig(cli, skillName, config);
        results.push({ cli, result });
      }
      
      // 更新Stigmergy配置
      const stigmergyResult = await this.configManager.updateStigmergyConfig(skillName, config);
      
      return {
        success: true,
        results: results,
        stigmergyResult: stigmergyResult
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  // 技能启用/禁用
  async toggleSkill(skillName, enabled, targetCLIs = []) {
    return await this.configureSkill(skillName, { enabled }, targetCLIs);
  }

  // 批量技能操作
  async batchOperation(operation, skills, options = {}) {
    const results = [];
    
    for (const skill of skills) {
      let result;
      
      switch (operation) {
        case 'install':
          result = await this.installSkill(skill.path, options.targetCLIs);
          break;
        case 'configure':
          result = await this.configureSkill(skill.name, skill.config, options.targetCLIs);
          break;
        case 'enable':
          result = await this.toggleSkill(skill.name, true, options.targetCLIs);
          break;
        case 'disable':
          result = await this.toggleSkill(skill.name, false, options.targetCLIs);
          break;
        default:
          result = { success: false, error: `不支持的操作: ${operation}` };
      }
      
      results.push({
        skill: skill.name || skill.path,
        result: result
      });
    }
    
    return results;
  }

  // 验证技能格式
  async validateSkill(skillPath) {
    try {
      const skillFile = path.join(skillPath, 'SKILL.md');
      
      if (!await fs.pathExists(skillFile)) {
        return { valid: false, errors: ['缺少SKILL.md文件'] };
      }
      
      const content = await fs.readFile(skillFile, 'utf8');
      
      // 检查YAML frontmatter
      const frontmatterMatch = content.match(/^---\s*\n([\s\S]*?)\n---/);
      if (!frontmatterMatch) {
        return { valid: false, errors: ['缺少YAML frontmatter'] };
      }
      
      const frontmatter = frontmatterMatch[1];
      const metadata = this.parseYamlFrontmatter(frontmatter);
      
      // 验证必需字段
      const errors = [];
      if (!metadata.name) errors.push('缺少name字段');
      if (!metadata.description) errors.push('缺少description字段');
      
      return {
        valid: errors.length === 0,
        errors: errors,
        metadata: metadata
      };
    } catch (error) {
      return { valid: false, errors: [error.message] };
    }
  }

  // 检查技能依赖
  async checkDependencies(skillPath) {
    const skillFile = path.join(skillPath, 'SKILL.md');
    const content = await fs.readFile(skillFile, 'utf8');
    
    // 解析依赖关系
    const dependencies = [];
    const depMatch = content.match(/dependencies:\s*\n([\s\S]*?)(?=\n\w+:|$)/);
    
    if (depMatch) {
      const depLines = depMatch[1].split('\n').filter(line => line.trim());
      for (const line of depLines) {
        const dep = line.trim().replace(/^-\s*/, '');
        if (dep) dependencies.push(dep);
      }
    }
    
    return dependencies;
  }

  // 安装依赖
  async installDependency(dependency) {
    // 实现依赖安装逻辑
    return await this.stigmergyWrapper.installSkill(dependency);
  }

  // 解析YAML frontmatter
  parseYamlFrontmatter(frontmatter) {
    const metadata = {};
    const lines = frontmatter.split('\n');
    
    for (const line of lines) {
      const match = line.match(/^(\w+):\s*(.+)$/);
      if (match) {
        metadata[match[1]] = match[2].trim();
      }
    }
    
    return metadata;
  }
}
```

#### 2. 安全执行机制 (完全继承Open Interpreter)
```javascript
// 直接继承Open Interpreter的SafeExecutor
class SafeExecutor extends OpenInterpreterSafeExecutor {
  constructor() {
    super();
    // 完全采用Open Interpreter的配置
    this.allowedCommands = [
      'stigmergy', 'iflow', 'claude', 'qwen', 'gemini', 'iflow',
      'codebuddy', 'codex', 'qodercli', 'python'
    ];
    this.executionTimeout = 30000;
    this.securityPatterns = this.loadOpenInterpreterPatterns();
  }

  // 完全继承Open Interpreter的验证逻辑
  async validate(command, args) {
    // 直接使用Open Interpreter的验证方法
    return await this.performOpenInterpreterValidation(command, args);
  }

  // 完全继承Open Interpreter的执行逻辑
  async execute(command, args) {
    // 直接使用Open Interpreter的执行方法
    return await this.performOpenInterpreterExecution(command, args);
  }

  // 继承Open Interpreter的安全模式
  loadOpenInterpreterPatterns() {
    // 直接使用Open Interpreter的安全模式配置
    return this.getOpenInterpreterSecurityPatterns();
  }
}
```

#### 3. 插件系统 (完全继承Continue架构)
```typescript
// 直接继承Continue的插件系统
class StigmergyPluginSystem extends ContinuePluginSystem {
  constructor() {
    super();
    // 完全采用Continue的插件架构
    this.pluginRegistry = new ContinuePluginRegistry();
    this.pluginLoader = new ContinuePluginLoader();
    this.permissionManager = new ContinuePermissionManager();
  }

  // 完全继承Continue的插件加载机制
  async loadPlugin(pluginPath: string): Promise<void> {
    // 直接使用Continue的插件加载方法
    return await this.performContinuePluginLoad(pluginPath);
  }

  // 完全继承Continue的插件卸载机制
  async unloadPlugin(pluginName: string): void {
    // 直接使用Continue的插件卸载方法
    return await this.performContinuePluginUnload(pluginName);
  }

  // 完全继承Continue的插件执行机制
  async executePlugin(pluginName: string, method: string, ...args: any[]): any {
    // 直接使用Continue的插件执行方法
    return await this.performContinuePluginExecution(pluginName, method, ...args);
  }

  // 新增Stigmergy技能插件加载
  async loadStigmergySkillsAsPlugins() {
    const skillsDir = path.join(__dirname, '../skills');
    const skillFolders = await fs.readdir(skillsDir);

    for (const folder of skillFolders) {
      const skillPath = path.join(skillsDir, folder);
      if (fs.statSync(skillPath).isDirectory()) {
        await this.loadStigmergySkillPlugin(skillPath);
      }
    }
  }

  private async loadStigmergySkillPlugin(skillPath: string): Promise<void> {
    // 使用Continue的插件接口包装Stigmergy技能
    const skillPlugin = await this.createContinuePluginFromSkill(skillPath);
    await this.loadPlugin(skillPlugin);
  }
}
```

#### 4. 数据存储设计
```sql
-- SQLite数据库设计
-- 会话表
CREATE TABLE sessions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  metadata TEXT -- JSON格式存储会话元数据
);

-- 技能使用记录表
CREATE TABLE skill_usage (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER,
  skill_name TEXT NOT NULL,
  command TEXT NOT NULL,
  result TEXT,
  executed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (session_id) REFERENCES sessions (id)
);

-- 项目文件表
CREATE TABLE project_files (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  project_path TEXT NOT NULL,
  file_path TEXT NOT NULL,
  file_type TEXT,
  last_modified DATETIME,
  metadata TEXT -- JSON格式存储文件元数据
);

-- CLI配置表
CREATE TABLE cli_configs (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  cli_name TEXT NOT NULL UNIQUE,
  config_path TEXT NOT NULL,
  is_enabled BOOLEAN DEFAULT TRUE,
  priority INTEGER DEFAULT 0
);
```

---

## 🎨 前端设计

### React组件架构
```
src/
├── components/
│   ├── common/
│   │   ├── Layout.jsx          # 主布局组件
│   │   ├── Sidebar.jsx         # 侧边栏组件
│   │   ├── Header.jsx          # 头部组件
│   │   └── Loading.jsx         # 加载组件
│   ├── skills/
│   │   ├── SkillList.jsx       # 技能列表
│   │   ├── SkillCard.jsx       # 技能卡片
│   │   ├── SkillDetail.jsx     # 技能详情
│   │   └── SkillExecutor.jsx   # 技能执行器
│   ├── cli/
│   │   ├── CLIStatus.jsx       # CLI状态
│   │   ├── CrossCLIExecutor.jsx # 跨CLI执行器
│   │   └── CLIConfig.jsx       # CLI配置
│   ├── project/
│   │   ├── ProjectTree.jsx     # 项目文件树
│   │   ├── FilePreview.jsx     # 文件预览
│   │   └── ProjectMonitor.jsx  # 项目监控
│   └── session/
│       ├── SessionList.jsx     # 会话列表
│       ├── SessionDetail.jsx   # 会话详情
│       └── SessionRestore.jsx  # 会话恢复
├── hooks/
│   ├── useCLI.js               # CLI调用Hook
│   ├── useSkills.js            # 技能管理Hook
│   ├── useSessions.js          # 会话管理Hook
│   └── useProjects.js          # 项目管理Hook
├── store/
│   ├── index.js                # 状态管理入口
│   ├── slices/
│   │   ├── cliSlice.js         # CLI状态
│   │   ├── skillSlice.js       # 技能状态
│   │   ├── sessionSlice.js     # 会话状态
│   │   └── projectSlice.js     # 项目状态
└── services/
    ├── api.js                  # API服务
    ├── ipc.js                  # IPC通信
    └── storage.js              # 存储服务
```

### 关键组件实现

#### 1. 技能执行器组件
```jsx
import React, { useState } from 'react';
import { useCLI } from '../hooks/useCLI';

const SkillExecutor = ({ skill, onResult }) => {
  const [executing, setExecuting] = useState(false);
  const [progress, setProgress] = useState(0);
  const { executeSkill } = useCLI();

  const handleExecute = async () => {
    setExecuting(true);
    setProgress(0);

    try {
      const result = await executeSkill(skill.name, skill.params, {
        onProgress: (p) => setProgress(p)
      });
      
      onResult(result);
    } catch (error) {
      console.error('Skill execution failed:', error);
    } finally {
      setExecuting(false);
      setProgress(0);
    }
  };

  return (
    <div className="skill-executor">
      <h3>{skill.name}</h3>
      <p>{skill.description}</p>
      
      {executing && (
        <div className="progress">
          <div 
            className="progress-bar" 
            style={{ width: `${progress}%` }}
          >
            {progress}%
          </div>
        </div>
      )}
      
      <button 
        onClick={handleExecute} 
        disabled={executing}
        className="btn btn-primary"
      >
        {executing ? '执行中...' : '执行技能'}
      </button>
    </div>
  );
};
```

#### 2. 跨CLI协同组件
```jsx
import React, { useState } from 'react';
import { useCLI } from '../hooks/useCLI';

const CrossCLIExecutor = () => {
  const [command, setCommand] = useState('');
  const [targetCLI, setTargetCLI] = useState('claude');
  const [result, setResult] = useState(null);
  const { executeCrossCLI } = useCLI();

  const handleExecute = async () => {
    try {
      const executionResult = await executeCrossCLI(targetCLI, command);
      setResult(executionResult);
    } catch (error) {
      setResult({ success: false, error: error.message });
    }
  };

  return (
    <div className="cross-cli-executor">
      <h2>跨CLI协同执行</h2>
      
      <div className="form-group">
        <label>目标CLI:</label>
        <select 
          value={targetCLI} 
          onChange={(e) => setTargetCLI(e.target.value)}
        >
          <option value="claude">Claude</option>
          <option value="qwen">Qwen</option>
          <option value="gemini">Gemini</option>
          <option value="iflow">iFlow</option>
        </select>
      </div>

      <div className="form-group">
        <label>命令:</label>
        <textarea
          value={command}
          onChange={(e) => setCommand(e.target.value)}
          placeholder="输入要执行的命令..."
          rows={4}
        />
      </div>

      <button onClick={handleExecute} className="btn btn-primary">
        执行
      </button>

      {result && (
        <div className="result">
          <h3>执行结果:</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};
```

---

## 🔧 后端设计

### 主进程架构 (继承Codeium Chat架构)
```javascript
// main.js - 继承Codeium Chat的主进程架构
const { app, BrowserWindow, ipcMain } = require('electron');
const CodeiumChatApp = require('codeium-chat/src/main/app'); // 继承Codeium Chat主应用
const OpenInterpreterCLI = require('open-interpreter/src/cli'); // 继承Open Interpreter CLI
const ContinuePluginSystem = require('continue/src/plugins'); // 继承Continue插件系统

class StigmergyDesktopApp extends CodeiumChatApp {
  constructor() {
    super();
    // 继承Codeium Chat的所有基础功能
    this.cliManager = new OpenInterpreterCLI(); // 继承Open Interpreter CLI
    this.pluginSystem = new ContinuePluginSystem(); // 继承Continue插件系统
    this.stigmergyManager = new StigmergyManager(); // 新增Stigmergy管理器
  }

  // 继承Codeium Chat的窗口创建
  async createWindow() {
    // 完全使用Codeium Chat的窗口创建逻辑
    await this.createCodeiumChatWindow();
    
    // 初始化继承的系统
    await this.initializeInheritedSystems();
  }

  // 初始化继承的系统
  async initializeInheritedSystems() {
    // 初始化Open Interpreter CLI
    await this.cliManager.initialize();
    
    // 初始化Continue插件系统
    await this.pluginSystem.initialize();
    
    // 加载Stigmergy技能作为插件
    await this.pluginSystem.loadStigmergySkillsAsPlugins();
    
    // 设置IPC通信
    await this.setupInheritedIPC();
  }

  // 继承Codeium Chat的IPC设置，新增Stigmergy功能
  async setupInheritedIPC() {
    // 继承Codeium Chat的所有IPC处理器
    await this.setupCodeiumChatIPC();
    
    // 继承Open Interpreter的IPC处理器
    await this.setupOpenInterpreterIPC();
    
    // 继承Continue的IPC处理器
    await this.setupContinueIPC();
    
    // 新增Stigmergy特定的IPC处理器
    await this.setupStigmergyIPC();
  }

  // 新增Stigmergy IPC处理器
  async setupStigmergyIPC() {
    // Stigmergy命令执行
    ipcMain.handle('stigmergy:execute', async (event, { command, args }) => {
      return await this.stigmergyManager.executeCommand(command, args);
    });

    // 跨CLI协同
    ipcMain.handle('stigmergy:cross-cli', async (event, { cli, skill, args }) => {
      return await this.stigmergyManager.executeCrossCLI(cli, skill, args);
    });

    // 项目管理
    ipcMain.handle('stigmergy:project-scan', async (event, projectPath) => {
      return await this.stigmergyManager.scanProject(projectPath);
    });

    // 会话管理
    ipcMain.handle('stigmergy:session-create', async (event, sessionData) => {
      return await this.stigmergyManager.createSession(sessionData);
    });
  }
}

// 启动应用 (继承Codeium Chat启动逻辑)
const stigmergyApp = new StigmergyDesktopApp();
app.whenReady().then(() => stigmergyApp.start());
```

### CLI管理器实现
```javascript
// managers/cli-manager.js
const { spawn } = require('child_process');
const SafeExecutor = require('./safe-executor');
const path = require('path');

class CLIManager {
  constructor() {
    this.safeExecutor = new SafeExecutor();
    this.skillsPath = path.join(__dirname, '../skills');
    this.cliAdapters = this.loadAdapters();
  }

  loadAdapters() {
    return {
      'iflow': require('../adapters/iflow-cli-adapter'),
      'qwen': require('../adapters/qwen-cli-adapter'),
      'openskills': require('../adapters/openskills-universal-adapter')
    };
  }

  async executeCommand(command, args = []) {
    try {
      const result = await this.safeExecutor.execute(command, args);
      
      // 解析不同命令的返回结果
      const parsedResult = this.parseCommandResult(command, result);
      
      return {
        success: true,
        command: command,
        args: args,
        result: parsedResult,
        rawOutput: result.stdout
      };
    } catch (error) {
      return {
        success: false,
        command: command,
        error: error.message
      };
    }
  }

  async executeCrossCLI(targetCLI, command) {
    try {
      // 使用适配器执行跨CLI调用
      const adapter = this.cliAdapters[targetCLI];
      if (!adapter) {
        throw new Error(`CLI adapter for ${targetCLI} not found`);
      }

      const result = await adapter.execute(command);
      return {
        success: true,
        cli: targetCLI,
        command: command,
        result: result
      };
    } catch (error) {
      return {
        success: false,
        cli: targetCLI,
        command: command,
        error: error.message
      };
    }
  }

  async listSkills() {
    const skills = [];
    const skillFolders = await fs.readdir(this.skillsPath);

    for (const folder of skillFolders) {
      const skillPath = path.join(this.skillsPath, folder);
      const skillInfo = await this.analyzeSkill(skillPath);
      if (skillInfo) {
        skills.push(skillInfo);
      }
    }

    return skills;
  }

  async executeSkill(skillName, params) {
    // 复用web_interface.py的技能执行逻辑
    const skillPath = path.join(this.skillsPath, skillName);
    const scriptPath = path.join(skillPath, 'scripts', params.script);

    return await this.safeExecutor.execute('python', [
      scriptPath,
      ...this.buildScriptArgs(params)
    ]);
  }

  parseCommandResult(command, result) {
    // 根据不同命令解析结果
    if (command === 'list') {
      return this.parseSkillList(result.stdout);
    } else if (command === 'status') {
      return this.parseStatus(result.stdout);
    } else {
      return { raw: result.stdout };
    }
  }
}
```

---

## 🔐 安全设计

### 多层安全机制

#### 1. CLI调用安全 (Open Interpreter机制)
```javascript
class SecurityManager {
  constructor() {
    this.allowedCommands = new Set([
      'stigmergy', 'iflow', 'claude', 'qwen', 'gemini', 
      'codebuddy', 'codex', 'qodercli', 'python'
    ]);
    
    this.dangerousPatterns = [
      /rm\s+-rf/i,           // 危险删除命令
      />\s*\/dev\/null/i,     // 重定向到null
      /&&.*rm/i,             // 链式删除
      /\|\s*sh/i,            // 管道到shell
      /eval\s*\(/i,          // eval函数
      /exec\s*\(/i           // exec函数
    ];
  }

  validateCommand(command, args) {
    // 命令白名单检查
    if (!this.allowedCommands.has(command)) {
      return {
        safe: false,
        reason: `Command '${command}' is not in the allowed list`
      };
    }

    // 参数安全检查
    for (const arg of args) {
      for (const pattern of this.dangerousPatterns) {
        if (pattern.test(arg)) {
          return {
            safe: false,
            reason: `Argument '${arg}' contains dangerous pattern`
          };
        }
      }
    }

    return { safe: true };
  }

  sanitizePath(filePath) {
    // 路径安全检查，防止目录遍历
    const normalizedPath = path.normalize(filePath);
    if (normalizedPath.includes('..')) {
      throw new Error('Path traversal detected');
    }
    return normalizedPath;
  }
}
```

#### 2. 文件访问安全
```javascript
class FileManager {
  constructor() {
    this.allowedExtensions = new Set([
      '.txt', '.md', '.json', '.csv', '.py', '.js', '.html', '.css'
    ]);
    
    this.maxFileSize = 10 * 1024 * 1024; // 10MB
    this.basePath = process.cwd(); // 限制在当前工作目录
  }

  validateFile(filePath) {
    const fullPath = path.resolve(this.basePath, filePath);
    
    // 检查是否在允许的路径内
    if (!fullPath.startsWith(this.basePath)) {
      throw new Error('File access denied: outside allowed directory');
    }

    // 检查文件扩展名
    const ext = path.extname(fullPath);
    if (!this.allowedExtensions.has(ext)) {
      throw new Error(`File type '${ext}' is not allowed`);
    }

    return fullPath;
  }

  async readFile(filePath) {
    const safePath = this.validateFile(filePath);
    
    const stats = await fs.stat(safePath);
    if (stats.size > this.maxFileSize) {
      throw new Error('File too large');
    }

    return await fs.readFile(safePath, 'utf8');
  }
}
```

#### 3. 数据加密存储
```javascript
const crypto = require('crypto');

class SecureStorage {
  constructor() {
    this.algorithm = 'aes-256-gcm';
    this.secretKey = this.getOrCreateKey();
  }

  getOrCreateKey() {
    const keyPath = path.join(app.getPath('userData'), 'encryption.key');
    
    try {
      if (fs.existsSync(keyPath)) {
        return fs.readFileSync(keyPath);
      } else {
        const key = crypto.randomBytes(32);
        fs.writeFileSync(keyPath, key);
        return key;
      }
    } catch (error) {
      // 如果无法创建密钥文件，使用默认密钥
      return crypto.randomBytes(32);
    }
  }

  encrypt(text) {
    const iv = crypto.randomBytes(16);
    const cipher = crypto.createCipher(this.algorithm, this.secretKey);
    cipher.setAAD(Buffer.from('stigmergy-app', 'utf8'));
    
    let encrypted = cipher.update(text, 'utf8', 'hex');
    encrypted += cipher.final('hex');
    
    const authTag = cipher.getAuthTag();
    
    return {
      encrypted,
      iv: iv.toString('hex'),
      authTag: authTag.toString('hex')
    };
  }

  decrypt(encryptedData) {
    const decipher = crypto.createDecipher(this.algorithm, this.secretKey);
    decipher.setAAD(Buffer.from('stigmergy-app', 'utf8'));
    decipher.setAuthTag(Buffer.from(encryptedData.authTag, 'hex'));
    
    let decrypted = decipher.update(encryptedData.encrypted, 'hex', 'utf8');
    decrypted += decipher.final('utf8');
    
    return decrypted;
  }
}
```

---

## 📊 性能优化设计

### 1. 启动优化
```javascript
class StartupOptimizer {
  constructor() {
    this.preloadTasks = [];
    this.criticalTasks = [];
  }

  async optimizeStartup() {
    // 预加载关键组件
    await this.preloadCriticalComponents();
    
    // 延迟加载非关键组件
    this.scheduleDelayedLoading();
    
    // 缓存常用数据
    await this.cacheFrequentData();
  }

  async preloadCriticalComponents() {
    // 并行加载关键组件
    await Promise.all([
      this.loadCLIAdapters(),
      this.loadBasicSkills(),
      this.initializeDatabase(),
      this.setupIPC()
    ]);
  }

  scheduleDelayedLoading() {
    // 延迟加载非关键组件
    setTimeout(() => this.loadAllSkills(), 1000);
    setTimeout(() => this.loadPluginSystem(), 2000);
    setTimeout(() => this.performHealthCheck(), 3000);
  }

  async cacheFrequentData() {
    // 缓存常用技能和配置
    const frequentSkills = await this.getFrequentSkills();
    await this.cacheSkills(frequentSkills);
    
    const cliConfigs = await this.getCLIConfigs();
    await this.cacheConfigs(cliConfigs);
  }
}
```

### 2. 内存优化
```javascript
class MemoryManager {
  constructor() {
    this.cache = new Map();
    this.maxCacheSize = 100 * 1024 * 1024; // 100MB
    this.currentCacheSize = 0;
  }

  set(key, value) {
    const size = this.calculateSize(value);
    
    // 检查缓存大小限制
    while (this.currentCacheSize + size > this.maxCacheSize) {
      this.evictLeastRecentlyUsed();
    }
    
    this.cache.set(key, {
      value,
      size,
      lastAccessed: Date.now()
    });
    
    this.currentCacheSize += size;
  }

  get(key) {
    const item = this.cache.get(key);
    if (item) {
      item.lastAccessed = Date.now();
      return item.value;
    }
    return null;
  }

  evictLeastRecentlyUsed() {
    let oldestKey = null;
    let oldestTime = Date.now();
    
    for (const [key, item] of this.cache) {
      if (item.lastAccessed < oldestTime) {
        oldestTime = item.lastAccessed;
        oldestKey = key;
      }
    }
    
    if (oldestKey) {
      const item = this.cache.get(oldestKey);
      this.currentCacheSize -= item.size;
      this.cache.delete(oldestKey);
    }
  }
}
```

---

## 🧪 测试设计

### 测试架构
```
tests/
├── unit/
│   ├── managers/
│   │   ├── cli-manager.test.js
│   │   ├── file-manager.test.js
│   │   └── security-manager.test.js
│   ├── components/
│   │   ├── skill-executor.test.jsx
│   │   ├── cross-cli-executor.test.jsx
│   │   └── project-tree.test.jsx
│   └── utils/
│       ├── safe-executor.test.js
│       └── secure-storage.test.js
├── integration/
│   ├── cli-integration.test.js
│   ├── ipc-communication.test.js
│   └── plugin-system.test.js
├── e2e/
│   ├── skill-execution.test.js
│   ├── cross-cli-collaboration.test.js
│   └── session-management.test.js
└── performance/
    ├── startup-performance.test.js
    ├── memory-usage.test.js
    └── cli-response-time.test.js
```

### 关键测试用例

#### 1. CLI安全执行测试
```javascript
// tests/unit/utils/safe-executor.test.js
describe('SafeExecutor', () => {
  let safeExecutor;

  beforeEach(() => {
    safeExecutor = new SafeExecutor();
  });

  describe('validate', () => {
    test('should allow valid commands', () => {
      expect(safeExecutor.validate('stigmergy', ['list'])).toEqual({
        safe: true
      });
    });

    test('should reject dangerous commands', () => {
      expect(safeExecutor.validate('rm', ['-rf', '/'])).toEqual({
        safe: false,
        reason: "Command 'rm' is not in the allowed list"
      });
    });

    test('should reject dangerous arguments', () => {
      expect(safeExecutor.validate('python', ['-c', 'rm -rf /'])).toEqual({
        safe: false,
        reason: "Argument '-c rm -rf /' contains dangerous pattern"
      });
    });
  });

  describe('execute', () => {
    test('should execute safe commands successfully', async () => {
      const result = await safeExecutor.execute('echo', ['hello']);
      expect(result.success).toBe(true);
      expect(result.stdout).toContain('hello');
    });

    test('should timeout long-running commands', async () => {
      await expect(
        safeExecutor.execute('sleep', ['60'])
      ).rejects.toThrow('Command execution timeout');
    });
  });
});
```

#### 2. 跨CLI协同测试
```javascript
// tests/integration/cli-integration.test.js
describe('CLI Integration', () => {
  let cliManager;

  beforeEach(() => {
    cliManager = new CLIManager();
  });

  test('should execute cross-CLI commands', async () => {
    const result = await cliManager.executeCrossCLI('claude', 'help');
    expect(result.success).toBe(true);
    expect(result.cli).toBe('claude');
  });

  test('should handle CLI adapter errors', async () => {
    const result = await cliManager.executeCrossCLI('nonexistent', 'command');
    expect(result.success).toBe(false);
    expect(result.error).toContain('not found');
  });
});
```

---

**技术设计文档制定日期**: 2025年12月20日  
**设计文档版本**: v7.0 (基于完整本地化：图形化界面 + 项目管理 + 完整CLI配置 + 本地AI/CLI/技能调用)  
**适用范围**: 本地化Subagent技能桌面应用项目  
**核心策略**: 智能化图形界面 + 项目文件管理 + 完整CLI配置管理 + 本地AI/CLI/技能调用 + 实时协作支持  
**技术基础**: Electron桌面应用 + 本地Stigmergy集成 + 本地文件操作器 + 本地CLI配置管理器 + 本地多AI集成架构  
**项目定位**: 零CLI依赖的本地化AI辅助开发桌面应用  
**应用场景**: 用户输入需求 → 本地AI处理 → 结果输出 → 用户交互 + 项目创建/文件编辑 + 完整配置管理  
**核心价值**: 用户无需接触命令行即可完成所有本地AI辅助开发工作，包括项目管理、文件操作、数据完全本地化  
**下次更新**: 根据本地文件操作器开发进展和项目管理功能测试结果更新

---

*本技术设计文档基于完整本地化应用场景，确保项目能够提供完整的本地化AI辅助开发环境，实现真正的数据隐私保护、零CLI依赖和完整的项目管理功能。*