const { spawn } = require('child_process');

// Mock child_process.spawn for testing
jest.mock('child_process', () => ({
  spawn: jest.fn()
}));

// Import the SkillManager class
const SkillManager = require('../skills/SkillManager');
const StigmergyCLIWrapper = require('../cli/StigmergyCLIWrapper');
const ClaudeCLIWrapper = require('../cli/ClaudeCLIWrapper');
const QwenCLIWrapper = require('../cli/QwenCLIWrapper');
const IFlowCLIWrapper = require('../cli/IFlowCLIWrapper');
const GeminiCLIWrapper = require('../cli/GeminiCLIWrapper');
const CodexCLIWrapper = require('../cli/CodexCLIWrapper');

describe('SkillManager', () => {
  let skillManager;
  let stigmergyCLI;
  let claudeCLI;
  let qwenCLI;
  let iflowCLI;
  let geminiCLI;
  let codexCLI;
  let mockChildProcess;

  beforeEach(() => {
    // Create CLI wrappers
    stigmergyCLI = new StigmergyCLIWrapper();
    claudeCLI = new ClaudeCLIWrapper();
    qwenCLI = new QwenCLIWrapper();
    iflowCLI = new IFlowCLIWrapper();
    geminiCLI = new GeminiCLIWrapper();
    codexCLI = new CodexCLIWrapper();
    
    // Create a new instance of SkillManager for each test
    skillManager = new SkillManager();
    
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
    test('should initialize with empty skills array', () => {
      expect(skillManager.skills).toEqual([]);
    });
  });

  describe('discoverSkills', () => {
    test('should discover skills from Stigmergy CLI', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('skill1\nskill2\nskill3');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const skills = await skillManager.discoverSkills(stigmergyCLI);
      
      expect(spawn).toHaveBeenCalledWith('stigmergy', ['skill', 'list'], {});
      expect(skills).toEqual(['skill1', 'skill2', 'skill3']);
    });
    
    test('should discover skills from Claude CLI', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('plugin1\nplugin2');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const skills = await skillManager.discoverSkills(claudeCLI);
      
      expect(spawn).toHaveBeenCalledWith('claude', ['plugin', 'list'], {});
      expect(skills).toEqual(['plugin1', 'plugin2']);
    });
    
    test('should discover skills from iFlow CLI', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('command1\ncommand2');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const skills = await skillManager.discoverSkills(iflowCLI);
      
      expect(spawn).toHaveBeenCalledWith('iflow', ['commands', 'list'], {});
      expect(skills).toEqual(['command1', 'command2']);
    });
  });

  describe('installSkill', () => {
    test('should install skill for Stigmergy CLI', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Skill installed successfully');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await skillManager.installSkill(stigmergyCLI, 'test-skill');
      
      expect(spawn).toHaveBeenCalledWith('stigmergy', ['skill', 'install', 'test-skill'], {});
      expect(result).toBe('Skill installed successfully');
    });
    
    test('should install skill for iFlow CLI', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Command installed successfully');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await skillManager.installSkill(iflowCLI, 'test-command');
      
      expect(spawn).toHaveBeenCalledWith('iflow', ['commands', 'install', 'test-command'], {});
      expect(result).toBe('Command installed successfully');
    });
  });

  describe('removeSkill', () => {
    test('should remove skill for Stigmergy CLI', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Skill removed successfully');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await skillManager.removeSkill(stigmergyCLI, 'test-skill');
      
      expect(spawn).toHaveBeenCalledWith('stigmergy', ['skill', 'remove', 'test-skill'], {});
      expect(result).toBe('Skill removed successfully');
    });
    
    test('should remove skill for iFlow CLI', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Command removed successfully');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await skillManager.removeSkill(iflowCLI, 'test-command');
      
      expect(spawn).toHaveBeenCalledWith('iflow', ['commands', 'remove', 'test-command'], {});
      expect(result).toBe('Command removed successfully');
    });
  });

  describe('readSkill', () => {
    test('should read skill for Stigmergy CLI', async () => {
      // Setup mock child process events
      mockChildProcess.stdout.on.mockImplementation((event, callback) => {
        if (event === 'data') {
          callback('Skill content');
        }
      });
      
      mockChildProcess.on.mockImplementation((event, callback) => {
        if (event === 'close') {
          callback(0); // Exit code 0 for success
        }
      });
      
      const result = await skillManager.readSkill(stigmergyCLI, 'test-skill');
      
      expect(spawn).toHaveBeenCalledWith('stigmergy', ['skill', 'read', 'test-skill'], {});
      expect(result).toBe('Skill content');
    });
  });
});