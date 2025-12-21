const { spawn } = require('child_process');

// Mock child_process.spawn for testing
jest.mock('child_process', () => ({
  spawn: jest.fn()
}));

// Import the QwenCLIWrapper class
const QwenCLIWrapper = require('../cli/QwenCLIWrapper');

describe('QwenCLIWrapper', () => {
  let qwenCLIWrapper;
  let mockChildProcess;

  beforeEach(() => {
    // Create a new instance of QwenCLIWrapper for each test
    qwenCLIWrapper = new QwenCLIWrapper();
    
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
      expect(qwenCLIWrapper.name).toBe('qwen');
      expect(qwenCLIWrapper.executablePath).toBe('qwen');
    });
  });

  describe('manageExtensions', () => {
    test('should execute extension management command correctly', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Extension management output');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await qwenCLIWrapper.manageExtensions('list');
      
      expect(spawn).toHaveBeenCalledWith('qwen', ['extensions', 'list'], {});
      expect(result).toBe('Extension management output');
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
      
      const result = await qwenCLIWrapper.manageMCP('list');
      
      expect(spawn).toHaveBeenCalledWith('qwen', ['mcp', 'list'], {});
      expect(result).toBe('MCP management output');
    });
  });
});