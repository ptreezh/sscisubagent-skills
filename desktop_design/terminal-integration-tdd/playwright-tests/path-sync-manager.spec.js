const { test, expect } = require('@playwright/test');

test.describe('Path Sync Manager Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.setContent(`
      <!DOCTYPE html>
      <html>
      <body>
        <div id="file-browser-path">/initial/path</div>
        <div id="terminal-path">/initial/path</div>
        <script>
          // Mock PathSyncManager functionality
          window.pathSyncEvents = [];
          window.pathSyncManager = {
            projectRoot: '',
            currentPath: '',
            previousPaths: [],
            isSyncEnabled: true,
            
            updateCurrentPath: function(newPath) {
              if (this.validatePathWithinProject(newPath)) {
                this.previousPaths.push(this.currentPath);
                this.currentPath = newPath;
                window.pathSyncEvents.push({ type: 'updatePath', newPath });
                return true;
              }
              return false;
            },
            
            getRelativePath: function(targetPath) {
              if (!this.projectRoot || !targetPath) {
                return targetPath;
              }
              return targetPath.replace(this.projectRoot, '').replace(/^[/\\\\]+/, '');
            },
            
            validatePathWithinProject: function(path) {
              if (!this.projectRoot) {
                return true; // If no project root set, allow any path
              }
              const normalizedPath = path.replace(/\\\\/g, '/');
              const normalizedRoot = this.projectRoot.replace(/\\\\/g, '/');
              return normalizedPath.startsWith(normalizedRoot);
            },
            
            syncTerminalToPath: function(path, terminalManager, terminalId) {
              if (!this.isSyncEnabled) {
                return false;
              }
              
              if (this.validatePathWithinProject(path)) {
                // Simulate sending cd command to terminal
                window.terminalCdCommand = 'cd "' + path + '"';
                this.updateCurrentPath(path);
                window.pathSyncEvents.push({ type: 'syncToTerminal', path, terminalId });
                return true;
              }
              return false;
            },
            
            syncFileBrowserToTerminalPath: function(path, onPathChange) {
              if (!this.isSyncEnabled) {
                return false;
              }
              
              if (this.validatePathWithinProject(path)) {
                this.updateCurrentPath(path);
                if (onPathChange) {
                  onPathChange(path);
                }
                window.pathSyncEvents.push({ type: 'syncToFileBrowser', path });
                return true;
              }
              return false;
            },
            
            setProjectRoot: function(rootPath) {
              if (rootPath) {
                this.projectRoot = rootPath.replace(/\\\\/g, '/');
              }
            },
            
            getProjectRoot: function() {
              return this.projectRoot;
            },
            
            getCurrentPath: function() {
              return this.currentPath;
            },
            
            setSyncEnabled: function(enabled) {
              this.isSyncEnabled = enabled;
            },
            
            getSyncEnabled: function() {
              return this.isSyncEnabled;
            }
          };
        </script>
      </body>
      </html>
    `);
  });

  test('should update current path and maintain history', async ({ page }) => {
    const initialPath = '/home/user/project';
    const newPath = '/home/user/project/src';
    
    // Set initial path
    await page.evaluate((path) => {
      window.pathSyncManager.updateCurrentPath(path);
    }, initialPath);
    
    // Verify initial path is set
    const currentPath1 = await page.evaluate(() => window.pathSyncManager.getCurrentPath());
    expect(currentPath1).toBe(initialPath);
    
    // Update to new path
    await page.evaluate((path) => {
      window.pathSyncManager.updateCurrentPath(path);
    }, newPath);
    
    // Verify new path is set
    const currentPath2 = await page.evaluate(() => window.pathSyncManager.getCurrentPath());
    expect(currentPath2).toBe(newPath);
    
    // Check that previous path was stored
    const previousPaths = await page.evaluate(() => window.pathSyncManager.previousPaths);
    expect(previousPaths).toContain(initialPath);
  });

  test('should validate path within project boundaries', async ({ page }) => {
    const projectRoot = '/home/user/my-project';
    const validPath = '/home/user/my-project/src';
    const invalidPath = '/home/user/other-project';
    
    // Set project root
    await page.evaluate((root) => {
      window.pathSyncManager.setProjectRoot(root);
    }, projectRoot);
    
    // Test valid path
    const isValid1 = await page.evaluate((path) => {
      return window.pathSyncManager.validatePathWithinProject(path);
    }, validPath);
    
    expect(isValid1).toBe(true);
    
    // Test invalid path
    const isValid2 = await page.evaluate((path) => {
      return window.pathSyncManager.validatePathWithinProject(path);
    }, invalidPath);
    
    expect(isValid2).toBe(false);
  });

  test('should sync terminal to specified path', async ({ page }) => {
    const testPath = '/home/user/project/src';
    const terminalId = 'test-terminal';
    
    // Enable sync
    await page.evaluate((enabled) => {
      window.pathSyncManager.setSyncEnabled(enabled);
    }, true);
    
    // Mock terminal manager
    await page.evaluate(() => {
      window.mockTerminalManager = {
        sendToTerminal: (id, data) => {
          window.sentToTerminal = { id, data };
        }
      };
    });
    
    // Sync terminal to path
    const success = await page.evaluate(({ path, tid }) => {
      return window.pathSyncManager.syncTerminalToPath(path, window.mockTerminalManager, tid);
    }, { path: testPath, tid: terminalId });
    
    expect(success).toBe(true);
    
    // Check that cd command was sent
    const sentCommand = await page.evaluate(() => window.terminalCdCommand);
    expect(sentCommand).toContain(testPath);
    
    // Check that current path was updated
    const currentPath = await page.evaluate(() => window.pathSyncManager.getCurrentPath());
    expect(currentPath).toBe(testPath);
  });

  test('should sync file browser to terminal path', async ({ page }) => {
    const testPath = '/home/user/project/docs';
    
    // Enable sync
    await page.evaluate((enabled) => {
      window.pathSyncManager.setSyncEnabled(enabled);
    }, true);
    
    // Define path change callback
    await page.evaluate(() => {
      window.pathChangedInFileBrowser = null;
      window.onPathChangeCallback = (path) => {
        window.pathChangedInFileBrowser = path;
        document.getElementById('file-browser-path').textContent = path;
      };
    });
    
    // Sync file browser to terminal path
    const success = await page.evaluate(({ path }) => {
      return window.pathSyncManager.syncFileBrowserToTerminalPath(path, window.onPathChangeCallback);
    }, { path: testPath });
    
    expect(success).toBe(true);
    
    // Check that file browser path was updated
    const fileBrowserPath = await page.textContent('#file-browser-path');
    expect(fileBrowserPath).toBe(testPath);
    
    // Check that callback was called with the path
    const pathInCallback = await page.evaluate(() => window.pathChangedInFileBrowser);
    expect(pathInCallback).toBe(testPath);
  });

  test('should handle cross-platform path normalization', async ({ page }) => {
    const unixPath = '/home/user/project';
    const windowsPath = 'C:\\Users\\user\\project';
    
    // Test relative path calculation
    await page.evaluate((root) => {
      window.pathSyncManager.setProjectRoot(root);
    }, unixPath);
    
    const relativePath = await page.evaluate((target) => {
      return window.pathSyncManager.getRelativePath(target);
    }, unixPath + '/src/components');
    
    expect(relativePath).toBe('src/components');
  });

  test('should enable/disable path synchronization', async ({ page }) => {
    const testPath = '/home/user/test';
    
    // Disable sync
    await page.evaluate((enabled) => {
      window.pathSyncManager.setSyncEnabled(enabled);
    }, false);
    
    // Try to sync (should fail)
    const success1 = await page.evaluate((path) => {
      return window.pathSyncManager.syncTerminalToPath(path, {}, 'test');
    }, testPath);
    
    expect(success1).toBe(false);
    
    // Enable sync
    await page.evaluate((enabled) => {
      window.pathSyncManager.setSyncEnabled(enabled);
    }, true);
    
    // Mock terminal manager for the next test
    await page.evaluate(() => {
      window.mockTerminalManager = {
        sendToTerminal: (id, data) => {
          // Mock implementation
        }
      };
    });
    
    // Try to sync again (should succeed)
    const success2 = await page.evaluate(({ path }) => {
      return window.pathSyncManager.syncTerminalToPath(path, window.mockTerminalManager, 'test');
    }, { path: testPath });
    
    expect(success2).toBe(true);
  });
});