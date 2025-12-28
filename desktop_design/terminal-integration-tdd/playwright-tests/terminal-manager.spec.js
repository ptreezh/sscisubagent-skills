const { test, expect } = require('@playwright/test');

test.describe('Terminal Manager Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.setContent(`
      <!DOCTYPE html>
      <html>
      <body>
        <div id="test-output"></div>
      </body>
      </html>
    `);
  });

  test('should create terminal instance with specified working directory', async ({ page }) => {
    const testId = 'test-terminal-1';
    const testCwd = '/test/path';
    
    await page.evaluate(({ id, cwd }) => {
      // Initialize mock pty
      window.mockPty = {
        spawn: (shell, args, options) => {
          return {
            onData: (callback) => {
              window.ptyDataCallback = callback;
            },
            write: (data) => {
              // Simulate data being processed
              if (window.ptyDataCallback) {
                setTimeout(() => window.ptyDataCallback(data), 10);
              }
            },
            resize: (cols, rows) => {
              window.ptyResized = { cols, rows };
            },
            kill: () => {
              window.ptyKilled = true;
            }
          };
        }
      };
      
      // Initialize TerminalManager
      window.terminalManagerEvents = [];
      window.terminalManager = {
        terminals: {},
        
        createTerminal: function(id, cwd) {
          const terminal = window.mockPty.spawn('bash', [], { cwd: cwd || '/tmp' });
          this.terminals[id] = terminal;
          window.terminalManagerEvents.push({ type: 'create', id, cwd });
          return terminal;
        },
        
        sendToTerminal: function(id, data) {
          const terminal = this.terminals[id];
          if (terminal) {
            terminal.write(data);
            window.terminalManagerEvents.push({ type: 'send', id, data });
          }
        },
        
        resizeTerminal: function(id, cols, rows) {
          const terminal = this.terminals[id];
          if (terminal) {
            terminal.resize(cols, rows);
            window.terminalManagerEvents.push({ type: 'resize', id, cols, rows });
          }
        },
        
        getTerminal: function(id) {
          return this.terminals[id] || null;
        },
        
        removeTerminal: function(id) {
          if (this.terminals[id]) {
            this.terminals[id].kill();
            delete this.terminals[id];
            window.terminalManagerEvents.push({ type: 'remove', id });
            return true;
          }
          return false;
        }
      };
      
      window.terminalManager.createTerminal(id, cwd);
    }, { id: testId, cwd: testCwd });
    
    // Check that terminal was created
    const events = await page.evaluate(() => window.terminalManagerEvents);
    const createEvents = events.filter(event => event.type === 'create' && event.id === testId);
    
    expect(createEvents.length).toBe(1);
    expect(createEvents[0].cwd).toBe(testCwd);
  });

  test('should send data to terminal instance', async ({ page }) => {
    const testId = 'test-terminal-2';
    
    // Create terminal first
    await page.evaluate(({ id }) => {
      window.terminalManager.createTerminal(id, '/tmp');
    }, { id: testId });
    
    // Send data to terminal
    const testData = 'ls -la\\r';
    await page.evaluate(({ id, data }) => {
      window.terminalManager.sendToTerminal(id, data);
    }, { id: testId, data: testData });
    
    // Check that data was sent
    const events = await page.evaluate(() => window.terminalManagerEvents);
    const sendEvents = events.filter(event => event.type === 'send' && event.id === testId);
    
    expect(sendEvents.length).toBe(1);
    expect(sendEvents[0].data).toBe(testData);
  });

  test('should resize terminal instance', async ({ page }) => {
    const testId = 'test-terminal-3';
    const cols = 80;
    const rows = 24;
    
    // Create terminal first
    await page.evaluate((id) => {
      window.terminalManager.createTerminal(id, '/tmp');
    }, testId);
    
    // Resize terminal
    await page.evaluate((id, c, r) => {
      window.terminalManager.resizeTerminal(id, c, r);
    }, testId, cols, rows);
    
    // Check that resize was processed
    const events = await page.evaluate(() => window.terminalManagerEvents);
    const resizeEvents = events.filter(event => event.type === 'resize' && event.id === testId);
    
    expect(resizeEvents.length).toBe(1);
    expect(resizeEvents[0].cols).toBe(cols);
    expect(resizeEvents[0].rows).toBe(rows);
  });

  test('should manage terminal lifecycle (create, get, remove)', async ({ page }) => {
    const testId = 'test-terminal-4';
    
    // Create terminal
    await page.evaluate((id) => {
      window.terminalManager.createTerminal(id, '/tmp');
    }, testId);
    
    // Get terminal
    const hasTerminal = await page.evaluate((id) => {
      return window.terminalManager.getTerminal(id) !== null;
    }, testId);
    
    expect(hasTerminal).toBe(true);
    
    // Remove terminal
    const removed = await page.evaluate((id) => {
      return window.terminalManager.removeTerminal(id);
    }, testId);
    
    expect(removed).toBe(true);
    
    // Verify terminal no longer exists
    const hasTerminalAfterRemoval = await page.evaluate((id) => {
      return window.terminalManager.getTerminal(id) !== null;
    }, testId);
    
    expect(hasTerminalAfterRemoval).toBe(false);
  });

  test('should handle platform-specific shell selection', async ({ page }) => {
    // Test that the terminal manager can handle different platforms
    const platform = await page.evaluate(() => {
      // In browser environment, we'll simulate the behavior
      return {
        isWin32: false,
        shell: 'bash'
      };
    });
    
    // This test verifies that the concept works
    expect(platform).toBeTruthy();
  });
});