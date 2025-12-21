const { spawn } = require('child_process');

// Mock child_process.spawn for testing
jest.mock('child_process', () => ({
  spawn: jest.fn()
}));

// Import the IFlowCLIWrapper class
const IFlowCLIWrapper = require('../cli/IFlowCLIWrapper');

describe('IFlowCLIWrapper', () => {
  let iFlowCLIWrapper;
  let mockChildProcess;

  beforeEach(() => {
    // Create a new instance of IFlowCLIWrapper for each test
    iFlowCLIWrapper = new IFlowCLIWrapper();
    
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
      expect(iFlowCLIWrapper.name).toBe('iflow');
      expect(iFlowCLIWrapper.executablePath).toBe('iflow');
    });
  });

  describe('manageAgents', () => {
    test('should execute agent management command correctly', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Agent management output');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await iFlowCLIWrapper.manageAgents('list');
      
      expect(spawn).toHaveBeenCalledWith('iflow', ['agent', 'list'], {});
      expect(result).toBe('Agent management output');
    });
  });

  describe('manageWorkflows', () => {
    test('should execute workflow management command correctly', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Workflow management output');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await iFlowCLIWrapper.manageWorkflows('list');
      
      expect(spawn).toHaveBeenCalledWith('iflow', ['workflow', 'list'], {});
      expect(result).toBe('Workflow management output');
    });
  });
});