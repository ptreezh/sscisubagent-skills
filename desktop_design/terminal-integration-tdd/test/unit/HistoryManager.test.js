// HistoryManager unit tests
const HistoryManager = require('../../src/main/history/HistoryManager');

describe('HistoryManager', () => {
  let historyManager;

  beforeEach(() => {
    historyManager = new HistoryManager();
  });

  describe('constructor', () => {
    it('should initialize with default max size', () => {
      expect(historyManager).toBeDefined();
      expect(historyManager.commands).toEqual([]);
      expect(historyManager.maxSize).toBe(100);
    });

    it('should initialize with custom max size', () => {
      const customHistoryManager = new HistoryManager(50);
      expect(customHistoryManager.maxSize).toBe(50);
    });
  });

  describe('addCommand', () => {
    it('should add a command to history', () => {
      const result = historyManager.addCommand('ls -la');
      expect(result).toBe(true);
      expect(historyManager.commands).toHaveLength(1);
      expect(historyManager.commands[0].command).toBe('ls -la');
      expect(historyManager.commands[0].success).toBe(true);
      expect(historyManager.commands[0].timestamp).toBeInstanceOf(Date);
    });

    it('should add a command with custom timestamp and success status', () => {
      const customTime = new Date('2023-01-01');
      const result = historyManager.addCommand('pwd', customTime, false);
      expect(result).toBe(true);
      expect(historyManager.commands[0].command).toBe('pwd');
      expect(historyManager.commands[0].timestamp).toEqual(customTime);
      expect(historyManager.commands[0].success).toBe(false);
    });

    it('should not add an invalid command', () => {
      const result = historyManager.addCommand();
      expect(result).toBe(false);
      expect(historyManager.commands).toHaveLength(0);
    });

    it('should not add a non-string command', () => {
      const result = historyManager.addCommand(123);
      expect(result).toBe(false);
      expect(historyManager.commands).toHaveLength(0);
    });

    it('should maintain max size by removing oldest entries', () => {
      const maxSize = 3;
      historyManager = new HistoryManager(maxSize);
      
      historyManager.addCommand('cmd1');
      historyManager.addCommand('cmd2');
      historyManager.addCommand('cmd3');
      historyManager.addCommand('cmd4');
      
      expect(historyManager.commands).toHaveLength(maxSize);
      expect(historyManager.commands[0].command).toBe('cmd2');
      expect(historyManager.commands[2].command).toBe('cmd4');
    });
  });

  describe('getHistory', () => {
    beforeEach(() => {
      historyManager.addCommand('cmd1');
      historyManager.addCommand('cmd2');
      historyManager.addCommand('cmd3');
    });

    it('should return all commands when no limit is specified', () => {
      const history = historyManager.getHistory();
      expect(history).toHaveLength(3);
      expect(history[0].command).toBe('cmd1');
      expect(history[2].command).toBe('cmd3');
    });

    it('should return limited commands when limit is specified', () => {
      const history = historyManager.getHistory(2);
      expect(history).toHaveLength(2);
      expect(history[0].command).toBe('cmd2');
      expect(history[1].command).toBe('cmd3');
    });

    it('should return all commands when limit exceeds history size', () => {
      const history = historyManager.getHistory(10);
      expect(history).toHaveLength(3);
    });
  });

  describe('clearHistory', () => {
    beforeEach(() => {
      historyManager.addCommand('cmd1');
      historyManager.addCommand('cmd2');
    });

    it('should clear all history', () => {
      expect(historyManager.commands).toHaveLength(2);
      historyManager.clearHistory();
      expect(historyManager.commands).toHaveLength(0);
    });
  });

  describe('searchHistory', () => {
    beforeEach(() => {
      historyManager.addCommand('ls -la');
      historyManager.addCommand('pwd');
      historyManager.addCommand('npm install');
      historyManager.addCommand('git status');
    });

    it('should return matching commands', () => {
      const results = historyManager.searchHistory('ls');
      expect(results).toHaveLength(1);
      expect(results[0].command).toBe('ls -la');
    });

    it('should return multiple matching commands', () => {
      const results = historyManager.searchHistory('p');
      expect(results).toHaveLength(2);
      // Sort results by command to ensure consistent order for testing
      const sortedResults = results.sort((a, b) => a.command.localeCompare(b.command));
      expect(sortedResults[0].command).toBe('npm install'); // contains 'p' in 'npm'
      expect(sortedResults[1].command).toBe('pwd');
    });

    it('should return case-insensitive matches', () => {
      historyManager.addCommand('GIT COMMIT');
      const results = historyManager.searchHistory('git');
      expect(results).toHaveLength(2);
      expect(results[0].command).toBe('git status');
      expect(results[1].command).toBe('GIT COMMIT');
    });

    it('should return empty array for no matches', () => {
      const results = historyManager.searchHistory('xyz');
      expect(results).toHaveLength(0);
    });

    it('should return empty array for invalid query', () => {
      const results = historyManager.searchHistory();
      expect(results).toHaveLength(0);
    });
  });

  describe('getLastCommand', () => {
    it('should return null when no commands exist', () => {
      const lastCommand = historyManager.getLastCommand();
      expect(lastCommand).toBeNull();
    });

    it('should return the most recent command', () => {
      historyManager.addCommand('cmd1');
      historyManager.addCommand('cmd2');
      const lastCommand = historyManager.getLastCommand();
      expect(lastCommand.command).toBe('cmd2');
    });
  });

  describe('getCommandsByTimeRange', () => {
    it('should return commands within the specified time range', () => {
      const time1 = new Date('2023-01-01T10:00:00Z');
      const time2 = new Date('2023-01-01T11:00:00Z');
      const time3 = new Date('2023-01-01T12:00:00Z');
      
      historyManager.addCommand('cmd1', time1);
      historyManager.addCommand('cmd2', time2);
      historyManager.addCommand('cmd3', time3);
      
      const startTime = new Date('2023-01-01T10:30:00Z');
      const endTime = new Date('2023-01-01T11:30:00Z');
      
      const results = historyManager.getCommandsByTimeRange(startTime, endTime);
      expect(results).toHaveLength(1);
      expect(results[0].command).toBe('cmd2');
    });
  });

  describe('updateCommandSuccess', () => {
    beforeEach(() => {
      historyManager.addCommand('cmd1');
      historyManager.addCommand('cmd2');
    });

    it('should update the success status of a command', () => {
      const result = historyManager.updateCommandSuccess(0, false);
      expect(result).toBe(true);
      expect(historyManager.commands[0].success).toBe(false);
    });

    it('should return false for invalid index', () => {
      const result = historyManager.updateCommandSuccess(5, false);
      expect(result).toBe(false);
    });
  });

  describe('size methods', () => {
    beforeEach(() => {
      historyManager.addCommand('cmd1');
      historyManager.addCommand('cmd2');
    });

    it('should return current size', () => {
      expect(historyManager.getCurrentSize()).toBe(2);
    });

    it('should return max size', () => {
      expect(historyManager.getMaxSize()).toBe(100);
    });

    it('should set max size and trim history if necessary', () => {
      historyManager.addCommand('cmd3');
      historyManager.setMaxSize(2);
      expect(historyManager.getMaxSize()).toBe(2);
      expect(historyManager.getCurrentSize()).toBe(2);
    });

    it('should throw error for invalid max size', () => {
      expect(() => {
        historyManager.setMaxSize(-1);
      }).toThrow('Max size must be a positive integer');
      
      expect(() => {
        historyManager.setMaxSize(0);
      }).toThrow('Max size must be a positive integer');
      
      expect(() => {
        historyManager.setMaxSize(1.5);
      }).toThrow('Max size must be a positive integer');
    });
  });
});