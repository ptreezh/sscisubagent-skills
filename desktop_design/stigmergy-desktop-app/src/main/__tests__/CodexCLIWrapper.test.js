const { spawn } = require('child_process');

// Mock child_process.spawn for testing
jest.mock('child_process', () => ({
  spawn: jest.fn()
}));

// Import the CodexCLIWrapper class
const CodexCLIWrapper = require('../cli/CodexCLIWrapper');

describe('CodexCLIWrapper', () => {
  let codexCLIWrapper;
  let mockChildProcess;

  beforeEach(() => {
    // Create a new instance of CodexCLIWrapper for each test
    codexCLIWrapper = new CodexCLIWrapper();
    
    // Setup mock child process
    mockChildProcess = {
      stdout: {
        on: jest.fn()
      },
      stderr: {
        on: jest.fn()
      },
      on: jest.fn()
    };
    
    spawn.mockReturnValue(mockChildProcess);
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('constructor', () => {
    test('should initialize with correct properties', () => {
      expect(codexCLIWrapper.name).toBe('codex');
      expect(codexCLIWrapper.executablePath).toBe('codex');
    });
  });

  describe('manageMCP', () => {
    test('should execute MCP management command correctly', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('MCP management output');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await codexCLIWrapper.manageMCP('list');
      
      expect(spawn).toHaveBeenCalledWith('codex', ['mcp', 'list'], {});
      expect(result).toBe('MCP management output');
    });
  });

  describe('codeReview', () => {
    test('should execute code review command correctly', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Code review output');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await codexCLIWrapper.codeReview(['file1.js', 'file2.js']);
      
      expect(spawn).toHaveBeenCalledWith('codex', ['exec', 'review', 'file1.js', 'file2.js'], {});
      expect(result).toBe('Code review output');
    });
  });
});