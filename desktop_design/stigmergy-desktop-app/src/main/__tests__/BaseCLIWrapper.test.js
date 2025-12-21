const { spawn } = require('child_process');

// Mock child_process.spawn for testing
jest.mock('child_process', () => ({
  spawn: jest.fn()
}));

// Import the BaseCLIWrapper class
const BaseCLIWrapper = require('../cli/BaseCLIWrapper');

describe('BaseCLIWrapper', () => {
  let baseCLIWrapper;
  let mockChildProcess;

  beforeEach(() => {
    // Create a new instance of BaseCLIWrapper for each test
    baseCLIWrapper = new BaseCLIWrapper('test-cli', '/path/to/test-cli');
    
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
      expect(baseCLIWrapper.name).toBe('test-cli');
      expect(baseCLIWrapper.executablePath).toBe('/path/to/test-cli');
      expect(baseCLIWrapper.isAvailable).toBe(false);
    });
  });

  describe('executeCommand', () => {
    test('should execute command and resolve with output', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Command output');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await baseCLIWrapper.executeCommand('test-command', ['--arg1', '--arg2']);
      
      expect(spawn).toHaveBeenCalledWith('/path/to/test-cli', ['test-command', '--arg1', '--arg2'], {});
      expect(result).toBe('Command output');
    });

    test('should reject with error when command fails', async () => {
      // Setup mock child process events for error
      mockChildProcess.stderr.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Error output');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(1); // Exit code 1 for error
        }
      });
      
      await expect(baseCLIWrapper.executeCommand('test-command', ['--arg1']))
        .rejects
        .toThrow('Command failed with exit code 1: Error output');
    });
  });

  describe('parseOutput', () => {
    test('should parse output correctly', () => {
      const output = 'Line 1\nLine 2\nLine 3';
      const expected = ['Line 1', 'Line 2', 'Line 3'];
      const result = baseCLIWrapper.parseOutput(output);
      expect(result).toEqual(expected);
    });
  });

  describe('handleError', () => {
    test('should create CLIError with correct properties', () => {
      const error = new Error('Test error');
      const cliError = baseCLIWrapper.handleError(error, 'test-command', 1, 'Error output');
      
      expect(cliError.message).toBe('Test error');
      expect(cliError.cliTool).toBe('test-cli');
      expect(cliError.command).toBe('test-command');
      expect(cliError.exitCode).toBe(1);
      expect(cliError.stderr).toBe('Error output');
    });
  });
});