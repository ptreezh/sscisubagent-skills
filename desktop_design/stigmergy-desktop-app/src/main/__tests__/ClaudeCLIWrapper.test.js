const { spawn } = require('child_process');

// Mock child_process.spawn for testing
jest.mock('child_process', () => ({
  spawn: jest.fn()
}));

// Import the ClaudeCLIWrapper class
const ClaudeCLIWrapper = require('../cli/ClaudeCLIWrapper');

describe('ClaudeCLIWrapper', () => {
  let claudeCLIWrapper;
  let mockChildProcess;

  beforeEach(() => {
    // Create a new instance of ClaudeCLIWrapper for each test
    claudeCLIWrapper = new ClaudeCLIWrapper();
    
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
      expect(claudeCLIWrapper.name).toBe('claude');
      expect(claudeCLIWrapper.executablePath).toBe('claude');
    });
  });

  describe('managePlugins', () => {
    test('should execute plugin management command correctly', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Plugin management output');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await claudeCLIWrapper.managePlugins('list');
      
      expect(spawn).toHaveBeenCalledWith('claude', ['plugin', 'list'], {});
      expect(result).toBe('Plugin management output');
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
      
      const result = await claudeCLIWrapper.manageMCP('list');
      
      expect(spawn).toHaveBeenCalledWith('claude', ['mcp', 'list'], {});
      expect(result).toBe('MCP management output');
    });
  });
});