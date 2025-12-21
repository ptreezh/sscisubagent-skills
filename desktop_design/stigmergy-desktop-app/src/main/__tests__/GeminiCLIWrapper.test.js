const { spawn } = require('child_process');

// Mock child_process.spawn for testing
jest.mock('child_process', () => ({
  spawn: jest.fn()
}));

// Import the GeminiCLIWrapper class
const GeminiCLIWrapper = require('../cli/GeminiCLIWrapper');

describe('GeminiCLIWrapper', () => {
  let geminiCLIWrapper;
  let mockChildProcess;

  beforeEach(() => {
    // Create a new instance of GeminiCLIWrapper for each test
    geminiCLIWrapper = new GeminiCLIWrapper();
    
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
      expect(geminiCLIWrapper.name).toBe('gemini');
      expect(geminiCLIWrapper.executablePath).toBe('gemini');
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
      
      const result = await geminiCLIWrapper.manageExtensions('list');
      
      expect(spawn).toHaveBeenCalledWith('gemini', ['extensions', 'list'], {});
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
      
      const result = await geminiCLIWrapper.manageMCP('list');
      
      expect(spawn).toHaveBeenCalledWith('gemini', ['mcp', 'list'], {});
      expect(result).toBe('MCP management output');
    });
  });
});