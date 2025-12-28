// TerminalManager unit tests
const TerminalManager = require('../../src/main/terminal/TerminalManager');

// Mock node-pty for testing
jest.mock('node-pty', () => ({
  spawn: jest.fn().mockImplementation((shell, args, options) => ({
    pid: 12345,
    kill: jest.fn(),
    on: jest.fn(),
    write: jest.fn(),
    resize: jest.fn()
  }))
}));

describe('TerminalManager', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  describe('constructor', () => {
    it('should initialize with default properties', () => {
      const terminalManager = new TerminalManager();
      expect(terminalManager).toBeDefined();
      expect(terminalManager.terminals).toEqual({});
    });
  });

  describe('createTerminal', () => {
    it('should create a new terminal instance', () => {
      const terminalManager = new TerminalManager();
      const terminalId = 'test-terminal';
      const cwd = '/test/path';
      
      const terminal = terminalManager.createTerminal(terminalId, cwd);
      
      expect(terminal).toBeDefined();
      expect(terminal.pid).toBe(12345);
      expect(terminalManager.terminals[terminalId]).toBe(terminal);
    });
  });

  describe('sendToTerminal', () => {
    it('should send data to an existing terminal', () => {
      const terminalManager = new TerminalManager();
      const terminalId = 'test-terminal';
      const testData = 'ls -la\r';
      
      // Create a terminal first
      terminalManager.createTerminal(terminalId, '/test/path');
      
      // Send data to terminal
      expect(() => {
        terminalManager.sendToTerminal(terminalId, testData);
      }).not.toThrow();
    });
  });

  describe('resizeTerminal', () => {
    it('should resize an existing terminal', () => {
      const terminalManager = new TerminalManager();
      const terminalId = 'test-terminal';
      const cols = 100;
      const rows = 50;
      
      // Create a terminal first
      terminalManager.createTerminal(terminalId, '/test/path');
      
      // Resize terminal
      expect(() => {
        terminalManager.resizeTerminal(terminalId, cols, rows);
      }).not.toThrow();
    });
  });

  describe('getTerminal', () => {
    it('should return an existing terminal', () => {
      const terminalManager = new TerminalManager();
      const terminalId = 'test-terminal';
      const cwd = '/test/path';
      
      // Create a terminal first
      const createdTerminal = terminalManager.createTerminal(terminalId, cwd);
      
      // Now get the terminal
      const terminal = terminalManager.getTerminal(terminalId);
      
      expect(terminal).toBeDefined();
      expect(terminal).toBe(createdTerminal);
    });
    
    it('should return null for non-existing terminal', () => {
      const terminalManager = new TerminalManager();
      const terminal = terminalManager.getTerminal('non-existing-terminal');
      
      expect(terminal).toBeNull();
    });
  });

  describe('removeTerminal', () => {
    it('should remove an existing terminal', () => {
      const terminalManager = new TerminalManager();
      const terminalId = 'test-terminal';
      
      // Create a terminal first
      terminalManager.createTerminal(terminalId, '/test/path');
      
      // Verify terminal exists
      expect(terminalManager.getTerminal(terminalId)).toBeDefined();
      
      // Remove the terminal
      const result = terminalManager.removeTerminal(terminalId);
      
      // Verify terminal is removed
      expect(result).toBe(true);
      expect(terminalManager.getTerminal(terminalId)).toBeNull();
    });
    
    it('should return false when removing non-existing terminal', () => {
      const terminalManager = new TerminalManager();
      const result = terminalManager.removeTerminal('non-existing-terminal');
      
      expect(result).toBe(false);
    });
  });
});