const { test, expect } = require('@playwright/test');

test.describe('Integration Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.setContent(`
      <!DOCTYPE html>
      <html>
      <body>
        <div id="terminal-output"></div>
        <div id="file-browser-path">/initial/path</div>
        <div id="command-history"></div>
        <script>
          // Mock all components for integration testing
          
          // Mock TerminalManager
          window.terminalManager = {
            terminals: {},
            createTerminal: (id, cwd) => {
              const terminal = {
                onData: (callback) => {
                  window.terminalDataCallback = callback;
                },
                write: (data) => {
                  if (window.terminalDataCallback) {
                    setTimeout(() => window.terminalDataCallback(data), 10);
                  }
                },
                resize: (cols, rows) => {},
                kill: () => {}
              };
              this.terminals[id] = terminal;
              return terminal;
            },
            sendToTerminal: (id, data) => {
              const terminal = this.terminals[id];
              if (terminal) {
                terminal.write(data);
              }
            },
            getTerminal: (id) => this.terminals[id] || null,
            removeTerminal: (id) => {
              if (this.terminals[id]) {
                this.terminals[id].kill();
                delete this.terminals[id];
                return true;
              }
              return false;
            }
          };
          
          // Mock PathSyncManager
          window.pathSyncManager = {
            projectRoot: '',
            currentPath: '/initial/path',
            previousPaths: [],
            isSyncEnabled: true,
            
            updateCurrentPath: function(newPath) {
              if (this.validatePathWithinProject(newPath)) {
                this.previousPaths.push(this.currentPath);
                this.currentPath = newPath;
                return true;
              }
              return false;
            },
            
            validatePathWithinProject: function(path) {
              if (!this.projectRoot) return true;
              const normalizedPath = path.replace(/\\\\/g, '/');
              const normalizedRoot = this.projectRoot.replace(/\\\\/g, '/');
              return normalizedPath.startsWith(normalizedRoot);
            },
            
            syncTerminalToPath: function(path, terminalManager, terminalId) {
              if (!this.isSyncEnabled) return false;
              if (this.validatePathWithinProject(path)) {
                if (terminalManager && terminalId) {
                  const pathForTerminal = path.replace(/\\\\/g, '/').replace(/\//g, '\\\\');
                  terminalManager.sendToTerminal(terminalId, \`cd "\${pathForTerminal}"\\\\r\`);
                  this.updateCurrentPath(path);
                  return true;
                }
              }
              return false;
            },
            
            syncFileBrowserToTerminalPath: function(path, onPathChange) {
              if (!this.isSyncEnabled) return false;
              if (this.validatePathWithinProject(path)) {
                this.updateCurrentPath(path);
                if (onPathChange) onPathChange(path);
                return true;
              }
              return false;
            },
            
            setProjectRoot: function(rootPath) {
              if (rootPath) this.projectRoot = rootPath.replace(/\\\\/g, '/');
            },
            
            getCurrentPath: function() {
              return this.currentPath;
            },
            
            getProjectRoot: function() {
              return this.projectRoot;
            }
          };
          
          // Mock HistoryManager
          window.historyManager = {
            commands: [],
            maxSize: 100,
            
            addCommand: function(command, timestamp = new Date(), success = true) {
              if (!command || typeof command !== 'string') return false;
              
              const historyEntry = { command, timestamp, success };
              this.commands.push(historyEntry);
              
              if (this.commands.length > this.maxSize) {
                this.commands = this.commands.slice(-this.maxSize);
              }
              
              // Update UI display
              const historyDisplay = document.getElementById('command-history');
              if (historyDisplay) {
                historyDisplay.innerHTML += '<br>' + command;
              }
              
              return true;
            },
            
            getHistory: function(limit = this.maxSize) {
              if (limit >= this.commands.length) {
                return [...this.commands];
              }
              return this.commands.slice(-limit);
            },
            
            searchHistory: function(query) {
              if (!query || typeof query !== 'string') return [];
              const normalizedQuery = query.toLowerCase();
              return this.commands.filter(entry => 
                entry.command.toLowerCase().includes(normalizedQuery)
              );
            },
            
            getLastCommand: function() {
              if (this.commands.length === 0) return null;
              return this.commands[this.commands.length - 1];
            }
          };
          
          // Global event tracking
          window.integrationEvents = [];
        </script>
      </body>
      </html>
    `);
  });

  test('should execute end-to-end CLI command flow', async ({ page }) => {
    const terminalId = 'integration-test-terminal';
    const testCommand = 'echo "Hello, Stigmergy!"';
    
    // 1. Create terminal
    await page.evaluate(({ id }) => {
      window.terminalManager.createTerminal(id, '/tmp');
    }, { id: terminalId });
    
    // 2. Execute command in terminal
    await page.evaluate(({ id, cmd }) => {
      window.terminalManager.sendToTerminal(id, cmd + '\\r');
    }, { id: terminalId, cmd: testCommand });
    
    // 3. Add command to history
    const historyAdded = await page.evaluate(({ cmd }) => {
      return window.historyManager.addCommand(cmd, new Date(), true);
    }, { cmd: testCommand });
    
    expect(historyAdded).toBe(true);
    
    // 4. Verify command appears in history
    const history = await page.evaluate(() => window.historyManager.getHistory());
    expect(history.length).toBe(1);
    expect(history[0].command).toBe(testCommand);
  });

  test('should synchronize terminal and file browser paths', async ({ page }) => {
    const newPath = '/home/user/project/src';
    const terminalId = 'sync-test-terminal';
    
    // Create terminal
    await page.evaluate(({ id }) => {
      window.terminalManager.createTerminal(id, '/tmp');
    }, { id: terminalId });
    
    // Update file browser path (simulating user action)
    await page.evaluate(({ path }) => {
      document.getElementById('file-browser-path').textContent = path;
    }, { path: newPath });
    
    // Sync terminal to file browser path
    const syncResult = await page.evaluate(({ path, tid }) => {
      return window.pathSyncManager.syncTerminalToPath(path, window.terminalManager, tid);
    }, { path: newPath, tid: terminalId });
    
    expect(syncResult).toBe(true);
    
    // Verify terminal path matches
    const currentPath = await page.evaluate(() => window.pathSyncManager.getCurrentPath());
    expect(currentPath).toBe(newPath);
    
    // Verify file browser path is still correct
    const fileBrowserPath = await page.textContent('#file-browser-path');
    expect(fileBrowserPath).toBe(newPath);
  });

  test('should maintain command history during path synchronization', async ({ page }) => {
    const testCommand = 'ls -la';
    const newPath = '/home/user/project';
    
    // Add command to history
    await page.evaluate(({ cmd }) => {
      window.historyManager.addCommand(cmd);
    }, { cmd: testCommand });
    
    // Change path
    await page.evaluate(({ path }) => {
      window.pathSyncManager.updateCurrentPath(path);
    }, { path: newPath });
    
    // Verify both command history and path are maintained
    const history = await page.evaluate(() => window.historyManager.getHistory());
    const currentPath = await page.evaluate(() => window.pathSyncManager.getCurrentPath());
    
    expect(history.length).toBe(1);
    expect(history[0].command).toBe(testCommand);
    expect(currentPath).toBe(newPath);
  });

  test('should handle error conditions gracefully', async ({ page }) => {
    // Test invalid command to history
    const invalidResult = await page.evaluate(() => {
      return window.historyManager.addCommand(null);
    });
    
    expect(invalidResult).toBe(false);
    
    // Test invalid path to path sync manager
    const invalidPathResult = await page.evaluate(() => {
      return window.pathSyncManager.updateCurrentPath(null);
    });
    
    expect(invalidPathResult).toBe(false);
    
    // Test non-existent terminal
    const invalidTerminalResult = await page.evaluate(() => {
      return window.terminalManager.getTerminal('non-existent-terminal');
    });
    
    expect(invalidTerminalResult).toBe(null);
  });

  test('should demonstrate complete workflow: command execution with path sync and history', async ({ page }) => {
    const terminalId = 'workflow-test-terminal';
    const projectPath = '/home/user/my-project';
    const testCommand = 'npm install';
    
    // 1. Set up project root
    await page.evaluate((root) => {
      window.pathSyncManager.setProjectRoot(root);
    }, projectPath);
    
    // 2. Create terminal in project path
    await page.evaluate((id, cwd) => {
      window.terminalManager.createTerminal(id, cwd);
    }, terminalId, projectPath);
    
    // 3. Execute command
    await page.evaluate((id, cmd) => {
      window.terminalManager.sendToTerminal(id, cmd + '\\r');
    }, terminalId, testCommand);
    
    // 4. Add to history
    const historyAdded = await page.evaluate((cmd) => {
      return window.historyManager.addCommand(cmd, new Date(), true);
    }, testCommand);
    
    expect(historyAdded).toBe(true);
    
    // 5. Change directory (simulating cd command effect)
    const newSubPath = projectPath + '/src';
    await page.evaluate((path) => {
      window.pathSyncManager.updateCurrentPath(path);
    }, newSubPath);
    
    // 6. Verify all components are in sync
    const history = await page.evaluate(() => window.historyManager.getHistory());
    const currentPath = await page.evaluate(() => window.pathSyncManager.getCurrentPath());
    const terminalExists = await page.evaluate(({ id }) => {
      return window.terminalManager.getTerminal(id) !== null;
    }, { id: terminalId });
    
    expect(history.length).toBe(1);
    expect(history[0].command).toBe(testCommand);
    expect(currentPath).toBe(newSubPath);
    expect(terminalExists).toBe(true);
  });
});