const { spawn } = require('child_process');

// Mock child_process.spawn for testing
jest.mock('child_process', () => ({
  spawn: jest.fn()
}));

// Import the StigmergyCLIWrapper class
const StigmergyCLIWrapper = require('../cli/StigmergyCLIWrapper');

describe('StigmergyCLIWrapper', () => {
  let stigmergyCLIWrapper;
  let mockChildProcess;

  beforeEach(() => {
    // Create a new instance of StigmergyCLIWrapper for each test
    stigmergyCLIWrapper = new StigmergyCLIWrapper();
    
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
      expect(stigmergyCLIWrapper.name).toBe('stigmergy');
      expect(stigmergyCLIWrapper.executablePath).toBe('stigmergy');
    });
  });

  describe('executeSkillCommand', () => {
    test('should execute skill command correctly', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Skill command output');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await stigmergyCLIWrapper.executeSkillCommand('list', []);
      
      expect(spawn).toHaveBeenCalledWith('stigmergy', ['skill', 'list'], {});
      expect(result).toBe('Skill command output');
    });
  });

  describe('crossCLICall', () => {
    test('should execute cross-CLI call correctly', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Cross-CLI call output');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await stigmergyCLIWrapper.crossCLICall('claude', 'test-skill');
      
      expect(spawn).toHaveBeenCalledWith('stigmergy', ['use', 'claude', 'skill', 'test-skill'], {});
      expect(result).toBe('Cross-CLI call output');
    });
  });
});