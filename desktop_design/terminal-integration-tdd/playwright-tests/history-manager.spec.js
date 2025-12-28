const { test, expect } = require('@playwright/test');

test.describe('History Manager Tests', () => {
  test.beforeEach(async ({ page }) => {
    await page.setContent(`
      <!DOCTYPE html>
      <html>
      <body>
        <div id="history-display"></div>
        <script>
          // Mock HistoryManager functionality
          window.historyManager = {
            commands: [],
            maxSize: 100,
            
            addCommand: function(command, timestamp = new Date(), success = true) {
              if (!command || typeof command !== 'string') {
                return false;
              }
              
              const historyEntry = {
                command,
                timestamp,
                success
              };
              
              this.commands.push(historyEntry);
              
              // Maintain max size by removing oldest entries
              if (this.commands.length > this.maxSize) {
                this.commands = this.commands.slice(-this.maxSize);
              }
              
              window.historyEvents = window.historyEvents || [];
              window.historyEvents.push({ type: 'addCommand', command, success });
              
              return true;
            },
            
            getHistory: function(limit = this.maxSize) {
              if (limit >= this.commands.length) {
                return [...this.commands];
              }
              return this.commands.slice(-limit);
            },
            
            clearHistory: function() {
              this.commands = [];
              window.historyEvents = window.historyEvents || [];
              window.historyEvents.push({ type: 'clearHistory' });
            },
            
            searchHistory: function(query) {
              if (!query || typeof query !== 'string') {
                return [];
              }
              
              const normalizedQuery = query.toLowerCase();
              return this.commands.filter(entry => 
                entry.command.toLowerCase().includes(normalizedQuery)
              );
            },
            
            getLastCommand: function() {
              if (this.commands.length === 0) {
                return null;
              }
              return this.commands[this.commands.length - 1];
            },
            
            getCommandsByTimeRange: function(startTime, endTime) {
              return this.commands.filter(entry => 
                entry.timestamp >= startTime && entry.timestamp <= endTime
              );
            },
            
            updateCommandSuccess: function(index, success) {
              if (index < 0 || index >= this.commands.length) {
                return false;
              }
              
              this.commands[index].success = success;
              window.historyEvents = window.historyEvents || [];
              window.historyEvents.push({ type: 'updateSuccess', index, success });
              
              return true;
            },
            
            getCurrentSize: function() {
              return this.commands.length;
            },
            
            getMaxSize: function() {
              return this.maxSize;
            },
            
            setMaxSize: function(newSize) {
              if (newSize <= 0 || !Number.isInteger(newSize)) {
                throw new Error('Max size must be a positive integer');
              }
              
              this.maxSize = newSize;
              
              // Trim history if it exceeds the new max size
              if (this.commands.length > this.maxSize) {
                this.commands = this.commands.slice(-this.maxSize);
              }
            }
          };
        </script>
      </body>
      </html>
    `);
  });

  test('should add command to history with proper metadata', async ({ page }) => {
    const testCommand = 'ls -la';
    
    const success = await page.evaluate((cmd) => {
      return window.historyManager.addCommand(cmd);
    }, testCommand);
    
    expect(success).toBe(true);
    
    // Check that command was added
    const history = await page.evaluate(() => window.historyManager.getHistory());
    expect(history.length).toBe(1);
    expect(history[0].command).toBe(testCommand);
    expect(history[0].success).toBe(true);
    expect(history[0].timestamp).toBeTruthy();
  });

  test('should maintain history size limit', async ({ page }) => {
    const maxSize = 3;
    
    // Set max size
    await page.evaluate((size) => {
      window.historyManager.maxSize = size;
    }, maxSize);
    
    // Add more commands than the max size
    for (let i = 1; i <= 5; i++) {
      await page.evaluate((cmd) => {
        window.historyManager.addCommand(cmd);
      }, 'cmd' + i);
    }
    
    // Check that only the last 3 commands remain
    const history = await page.evaluate(() => window.historyManager.getHistory());
    expect(history.length).toBe(maxSize);
    expect(history[0].command).toBe('cmd3');
    expect(history[1].command).toBe('cmd4');
    expect(history[2].command).toBe('cmd5');
  });

  test('should retrieve history with specified limit', async ({ page }) => {
    // Add several commands
    for (let i = 1; i <= 5; i++) {
      await page.evaluate((cmd) => {
        window.historyManager.addCommand(cmd);
      }, 'command' + i);
    }
    
    // Get history with limit
    const limitedHistory = await page.evaluate(() => {
      return window.historyManager.getHistory(3);
    });
    
    expect(limitedHistory.length).toBe(3);
    expect(limitedHistory[0].command).toBe('command3');
    expect(limitedHistory[1].command).toBe('command4');
    expect(limitedHistory[2].command).toBe('command5');
  });

  test('should search history for matching commands', async ({ page }) => {
    // Add commands with different content
    await page.evaluate(() => {
      window.historyManager.addCommand('ls -la');
      window.historyManager.addCommand('npm install');
      window.historyManager.addCommand('git status');
      window.historyManager.addCommand('git commit -m "test"');
    });
    
    // Search for commands containing 'git'
    const gitCommands = await page.evaluate(() => {
      return window.historyManager.searchHistory('git');
    });
    
    expect(gitCommands.length).toBe(2);
    expect(gitCommands[0].command).toBe('git status');
    expect(gitCommands[1].command).toBe('git commit -m "test"');
  });

  test('should handle case-insensitive search', async ({ page }) => {
    // Add command with uppercase
    await page.evaluate(() => {
      window.historyManager.addCommand('GIT STATUS');
    });
    
    // Search with lowercase
    const results = await page.evaluate(() => {
      return window.historyManager.searchHistory('git');
    });
    
    expect(results.length).toBe(1);
    expect(results[0].command).toBe('GIT STATUS');
  });

  test('should get the most recent command', async ({ page }) => {
    // Add commands
    await page.evaluate(() => {
      window.historyManager.addCommand('first command');
      window.historyManager.addCommand('second command');
      window.historyManager.addCommand('latest command');
    });
    
    // Get last command
    const lastCommand = await page.evaluate(() => {
      return window.historyManager.getLastCommand();
    });
    
    expect(lastCommand.command).toBe('latest command');
  });

  test('should clear all history', async ({ page }) => {
    // Add some commands
    await page.evaluate(() => {
      window.historyManager.addCommand('command1');
      window.historyManager.addCommand('command2');
    });
    
    // Verify commands exist
    let history = await page.evaluate(() => window.historyManager.getHistory());
    expect(history.length).toBe(2);
    
    // Clear history
    await page.evaluate(() => {
      window.historyManager.clearHistory();
    });
    
    // Verify history is empty
    history = await page.evaluate(() => window.historyManager.getHistory());
    expect(history.length).toBe(0);
  });

  test('should update command success status', async ({ page }) => {
    // Add a command
    await page.evaluate(() => {
      window.historyManager.addCommand('test command');
    });
    
    // Update success status
    const updateResult = await page.evaluate(() => {
      return window.historyManager.updateCommandSuccess(0, false);
    });
    
    expect(updateResult).toBe(true);
    
    // Check that success status was updated
    const history = await page.evaluate(() => window.historyManager.getHistory());
    expect(history[0].success).toBe(false);
  });

  test('should handle time-based command filtering', async ({ page }) => {
    const time1 = new Date('2023-01-01T10:00:00Z');
    const time2 = new Date('2023-01-01T11:00:00Z');
    const time3 = new Date('2023-01-01T12:00:00Z');
    
    // Add commands with specific timestamps
    await page.evaluate(({ t1, t2, t3 }) => {
      window.historyManager.addCommand('cmd1', new Date(t1), true);
      window.historyManager.addCommand('cmd2', new Date(t2), true);
      window.historyManager.addCommand('cmd3', new Date(t3), true);
    }, { t1: time1.toISOString(), t2: time2.toISOString(), t3: time3.toISOString() });
    
    // Get commands in time range
    const timeRangeCommands = await page.evaluate(() => {
      return window.historyManager.getCommandsByTimeRange(
        new Date('2023-01-01T10:30:00Z'),
        new Date('2023-01-01T11:30:00Z')
      );
    });
    
    expect(timeRangeCommands.length).toBe(1);
    expect(timeRangeCommands[0].command).toBe('cmd2');
  });

  test('should manage max size configuration', async ({ page }) => {
    // Add commands to fill history
    for (let i = 1; i <= 5; i++) {
      await page.evaluate((cmd) => {
        window.historyManager.addCommand(cmd);
      }, 'cmd' + i);
    }
    
    // Reduce max size
    await page.evaluate(() => {
      window.historyManager.setMaxSize(3);
    });
    
    // Check that history was trimmed
    const history = await page.evaluate(() => window.historyManager.getHistory());
    expect(history.length).toBe(3);
    expect(history[0].command).toBe('cmd3');
  });
});