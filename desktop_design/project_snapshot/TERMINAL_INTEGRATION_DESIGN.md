# 终端集成与工作区同步功能设计文档

## 1. 引言

### 1.1 目的
本文档详细描述了在Stigmergy桌面应用程序中集成真实终端并与项目工作区路径同步功能的设计方案。

### 1.2 范围
本文档涵盖了系统的架构设计、组件结构、数据流和接口设计。

### 1.3 参考资料
- 终端集成需求规格说明书
- Electron官方文档
- xterm.js官方文档
- node-pty官方文档

## 2. 系统架构

### 2.1 总体架构
```
┌─────────────────────────────────────────────────────────────┐
│                    应用程序架构                             │
├─────────────────────────────────────────────────────────────┤
│ 渲染进程 (React)           │ 主进程 (Node.js)              │
├─────────────────────────────────────────────────────────────┤
│ ┌───────────────────────┐ │ ┌──────────────────────────┐ │
│ │   终端组件            │ │ │   终端管理器             │ │
│ │  (xterm.js)          │ │ │  (TerminalManager)       │ │
│ └───────────────────────┘ │ └──────────────────────────┘ │
│ ┌───────────────────────┐ │ ┌──────────────────────────┐ │
│ │   路径同步组件        │ │ │   PTY接口                │ │
│ │  (PathSyncManager)    │ │ │  (node-pty)              │ │
│ └───────────────────────┘ │ └──────────────────────────┘ │
│ ┌───────────────────────┐ │ ┌──────────────────────────┐ │
│ │   历史记录组件        │ │ │   命令历史管理器         │ │
│ │  (HistoryComponent)   │ │ │  (HistoryManager)        │ │
│ └───────────────────────┘ │ └──────────────────────────┘ │
│ ┌───────────────────────┐ │ ┌──────────────────────────┐ │
│ │   操作指导组件        │ │ │   指导引擎               │ │
│ │  (GuidanceComponent)  │ │ │  (GuidanceEngine)        │ │
│ └───────────────────────┘ │ └──────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          │
                   IPC通信 │
                          ▼
```

### 2.2 技术栈
- **前端**: React 18.x, xterm.js ^5.3.0, CSS/SCSS
- **后端**: Electron主进程 39.x, node-pty ^1.0.0
- **通信**: Electron IPC
- **状态管理**: React Context API
- **附加库**: 
  - xterm-addon-fit ^0.8.0 (终端自适应)
  - xterm-addon-search ^0.13.0 (终端搜索功能)
  - xterm-addon-web-links ^0.9.0 (链接识别)

## 3. 组件设计

### 3.1 终端组件 (TerminalComponent)

#### 3.1.1 职责
- 渲染终端界面
- 处理用户输入
- 显示终端输出

#### 3.1.2 接口
```javascript
class TerminalComponent extends React.Component {
  // 初始化终端
  initializeTerminal(containerElement)
  
  // 发送命令到终端
  sendCommand(command)
  
  // 清空终端
  clearTerminal()
  
  // 调整终端大小
  resizeTerminal(cols, rows)
}
```

#### 3.1.3 依赖
- xterm.js
- xterm-addon-fit
- TerminalContext (应用状态)

### 3.2 路径同步管理器 (PathSyncManager)

#### 3.2.1 职责
- 跟踪当前工作目录
- 协调文件浏览器和终端间的路径同步
- 验证路径有效性

#### 3.2.2 接口
```javascript
class PathSyncManager {
  // 更新当前工作路径
  updateCurrentPath(newPath)
  
  // 获取相对于项目根的路径
  getRelativePath(targetPath)
  
  // 验证路径是否在项目范围内
  validatePathWithinProject(path)
  
  // 同步终端到指定路径
  syncTerminalToPath(path)
  
  // 同步文件浏览器到终端路径
  syncFileBrowserToTerminalPath(path)
}
```

#### 3.2.3 依赖
- PathSyncContext (应用状态)
- IPC通信模块

### 3.3 终端管理器 (TerminalManager)

#### 3.3.1 职责
- 管理终端进程生命周期
- 处理终端输入输出
- 执行终端命令

#### 3.3.2 接口
```javascript
class TerminalManager {
  // 创建终端实例
  createTerminal(initialPath)
  
  // 销毁终端实例
  destroyTerminal()
  
  // 执行命令
  executeCommand(command)
  
  // 更改工作目录
  changeDirectory(path)
  
  // 获取当前工作目录
  getCurrentDirectory()
}
```

#### 3.3.3 依赖
- node-pty
- IPC通信模块

### 3.4 历史记录管理器 (HistoryManager)

#### 3.4.1 职责
- 存储和检索命令历史
- 管理历史记录持久化
- 提供历史记录搜索功能

#### 3.4.2 接口
```javascript
class HistoryManager {
  // 添加命令到历史记录
  addCommand(command, timestamp)
  
  // 获取历史记录
  getHistory(limit)
  
  // 清空历史记录
  clearHistory()
  
  // 搜索历史记录
  searchHistory(query)
}
```

#### 3.4.3 依赖
- LocalStorage或IndexedDB
- HistoryContext (应用状态)

### 3.5 指导引擎 (GuidanceEngine)

#### 3.5.1 职责
- 根据上下文提供操作建议
- 管理新手引导流程
- 提供快捷操作

#### 3.5.2 接口
```javascript
class GuidanceEngine {
  // 获取当前上下文的建议
  getSuggestions(context)
  
  // 获取新手引导步骤
  getOnboardingSteps()
  
  // 记录用户行为
  recordUserAction(action)
  
  // 获取快捷操作
  getQuickActions(currentPath)
}
```

#### 3.5.3 依赖
- GuidanceContext (应用状态)
- 项目上下文信息

## 4. 数据设计

### 4.1 状态管理

#### 4.1.1 TerminalContext
```javascript
{
  terminalInstance: object,     // xterm.js实例
  isConnected: boolean,         // 终端连接状态
  currentPath: string,          // 当前工作目录
  projectRoot: string,          // 项目根目录
  syncStatus: 'synced'|'unsynced'|'error'  // 同步状态
}
```

#### 4.1.2 HistoryContext
```javascript
{
  commands: Array<{          // 命令历史数组
    command: string,         // 命令内容
    timestamp: Date,         // 执行时间
    success: boolean         // 执行结果
  }>,
  maxSize: number            // 最大历史记录数
}
```

#### 4.1.3 PathSyncContext
```javascript
{
  projectRoot: string,       // 项目根目录
  currentPath: string,       // 当前工作目录
  previousPaths: string[],   // 历史路径
  isSyncEnabled: boolean     // 同步是否启用
}
```

## 5. 接口设计

### 5.1 IPC接口

#### 5.1.1 主进程到渲染进程
```javascript
// 终端输出数据
ipcMain.on('terminal-data', (event, data) => {
  // 将数据发送到渲染进程
})

// 路径变更通知
ipcMain.on('path-changed', (event, { path, source }) => {
  // 通知渲染进程路径变更
})
```

#### 5.1.2 渲染进程到主进程
```javascript
// 发送命令到终端
ipcRenderer.send('terminal-command', command)

// 请求更改目录
ipcRenderer.send('change-directory', path)

// 请求终端状态
ipcRenderer.send('get-terminal-status')
```

### 5.2 组件接口

#### 5.2.1 TerminalComponent Props
```javascript
{
  onPathChange: function,      // 路径变更回调
  onCommandExecute: function,  // 命令执行回调
  initialPath: string,         // 初始路径
  projectRoot: string          // 项目根目录
}
```

## 6. 部署设计

### 6.1 依赖安装
```bash
npm install xterm@^5.3.0 node-pty@^1.0.0
npm install @xterm/addon-fit@^0.8.0 @xterm/addon-search@^0.13.0 @xterm/addon-web-links@^0.9.0
```

### 6.2 构建配置
在webpack配置中需要处理node-pty的原生模块：
```javascript
module.exports = {
  // ...其他配置
  externals: {
    'node-pty': 'commonjs node-pty'
  },
  resolve: {
    fallback: {
      util: require.resolve('util/'),
      path: require.resolve('path-browserify'),
      os: require.resolve('os-browserify/browser'),
      crypto: require.resolve('crypto-browserify'),
      stream: require.resolve('stream-browserify'),
      buffer: require.resolve('buffer/')
    }
  }
}
```

### 6.3 Electron配置
在Electron主进程中需要正确处理node-pty：
```javascript
const pty = require('node-pty');
const os = require('os');

// 根据操作系统选择合适的shell
const shell = os.platform() === 'win32' ? 'powershell.exe' : os.platform() === 'darwin' ? 'zsh' : 'bash';

// 创建终端进程
function createTerminal(cwd) {
  return pty.spawn(shell, [], {
    name: 'xterm-color',
    cols: 80,
    rows: 30,
    cwd: cwd || process.cwd(),
    env: process.env,
    encoding: 'utf8'
  });
}
```

## 7. 设计原则遵循

### 7.1 KISS (Keep It Simple, Stupid)
- 每个组件只负责单一功能
- 避免过度复杂的配置选项
- 使用直观的用户界面

### 7.2 YAGNI (You Aren't Gonna Need It)
- 只实现当前明确需要的功能
- 避免预测未来可能的需求
- 保持代码简洁

### 7.3 SOLID原则

#### 7.3.1 单一职责原则 (SRP)
- TerminalComponent只负责UI渲染
- TerminalManager只负责终端进程管理
- PathSyncManager只负责路径同步

#### 7.3.2 开放/封闭原则 (OCP)
- 通过接口扩展功能而不修改现有代码
- 使用插件架构支持不同类型的终端

#### 7.3.3 里氏替换原则 (LSP)
- 所有管理器类都可以被其基类替换
- 保证接口一致性

#### 7.3.4 接口隔离原则 (ISP)
- 使用专门的接口而非通用接口
- 每个组件只依赖其需要的接口

#### 7.3.5 依赖倒置原则 (DIP)
- 依赖抽象而非具体实现
- 通过Context API解耦组件