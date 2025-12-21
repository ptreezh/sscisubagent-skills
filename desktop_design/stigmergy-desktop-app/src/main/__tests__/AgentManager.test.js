// Mock child_process.spawn for testing
jest.mock('child_process', () => ({
  spawn: jest.fn()
}));

// Import the AgentManager class
const AgentManager = require('../agents/AgentManager');
const StigmergyCLIWrapper = require('../cli/StigmergyCLIWrapper');
const ClaudeCLIWrapper = require('../cli/ClaudeCLIWrapper');
const QwenCLIWrapper = require('../cli/QwenCLIWrapper');
const IFlowCLIWrapper = require('../cli/IFlowCLIWrapper');
const GeminiCLIWrapper = require('../cli/GeminiCLIWrapper');
const CodexCLIWrapper = require('../cli/CodexCLIWrapper');

describe('AgentManager', () => {
  let agentManager;
  let stigmergyCLI;
  let claudeCLI;
  let qwenCLI;
  let iflowCLI;
  let geminiCLI;
  let codexCLI;

  beforeEach(() => {
    // Create CLI wrappers
    stigmergyCLI = new StigmergyCLIWrapper();
    claudeCLI = new ClaudeCLIWrapper();
    qwenCLI = new QwenCLIWrapper();
    iflowCLI = new IFlowCLIWrapper();
    geminiCLI = new GeminiCLIWrapper();
    codexCLI = new CodexCLIWrapper();
    
    // Create a new instance of AgentManager for each test
    agentManager = new AgentManager();
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  describe('constructor', () => {
    test('should initialize with empty agents array', () => {
      expect(agentManager.agents).toEqual([]);
    });
  });

  describe('registerAgent', () => {
    test('should register a new agent', () => {
      const agent = {
        name: 'test-agent',
        cliTool: 'stigmergy',
        description: 'Test agent'
      };
      
      agentManager.registerAgent(agent);
      
      expect(agentManager.agents).toHaveLength(1);
      expect(agentManager.agents[0]).toEqual(agent);
    });
  });

  describe('getAgents', () => {
    test('should return all registered agents', () => {
      const agent1 = {
        name: 'test-agent-1',
        cliTool: 'stigmergy',
        description: 'Test agent 1'
      };
      
      const agent2 = {
        name: 'test-agent-2',
        cliTool: 'claude',
        description: 'Test agent 2'
      };
      
      agentManager.registerAgent(agent1);
      agentManager.registerAgent(agent2);
      
      const agents = agentManager.getAgents();
      
      expect(agents).toHaveLength(2);
      expect(agents).toContainEqual(agent1);
      expect(agents).toContainEqual(agent2);
    });
  });

  describe('getAgentsByCLITool', () => {
    test('should return agents for a specific CLI tool', () => {
      const agent1 = {
        name: 'test-agent-1',
        cliTool: 'stigmergy',
        description: 'Test agent 1'
      };
      
      const agent2 = {
        name: 'test-agent-2',
        cliTool: 'stigmergy',
        description: 'Test agent 2'
      };
      
      const agent3 = {
        name: 'test-agent-3',
        cliTool: 'claude',
        description: 'Test agent 3'
      };
      
      agentManager.registerAgent(agent1);
      agentManager.registerAgent(agent2);
      agentManager.registerAgent(agent3);
      
      const agents = agentManager.getAgentsByCLITool('stigmergy');
      
      expect(agents).toHaveLength(2);
      expect(agents).toContainEqual(agent1);
      expect(agents).toContainEqual(agent2);
    });
  });

  describe('executeAgent', () => {
    test('should execute an agent with Stigmergy CLI', async () => {
      // Mock the executeCommand method
      stigmergyCLI.executeCommand = jest.fn().mockResolvedValue('Agent execution result');
      
      const agent = {
        name: 'test-agent',
        cliTool: 'stigmergy',
        description: 'Test agent'
      };
      
      const result = await agentManager.executeAgent(stigmergyCLI, agent, 'Test prompt');
      
      expect(stigmergyCLI.executeCommand).toHaveBeenCalledWith('call', ['Test prompt']);
      expect(result).toBe('Agent execution result');
    });
    
    test('should execute an agent with Claude CLI', async () => {
      // Mock the executeCommand method
      claudeCLI.executeCommand = jest.fn().mockResolvedValue('Agent execution result');
      
      const agent = {
        name: 'test-agent',
        cliTool: 'claude',
        description: 'Test agent'
      };
      
      const result = await agentManager.executeAgent(claudeCLI, agent, 'Test prompt');
      
      expect(claudeCLI.executeCommand).toHaveBeenCalledWith('', ['-p', 'Test prompt']);
      expect(result).toBe('Agent execution result');
    });
    
    test('should execute an agent with Qwen CLI', async () => {
      // Mock the executeCommand method
      qwenCLI.executeCommand = jest.fn().mockResolvedValue('Agent execution result');
      
      const agent = {
        name: 'test-agent',
        cliTool: 'qwen',
        description: 'Test agent'
      };
      
      const result = await agentManager.executeAgent(qwenCLI, agent, 'Test prompt');
      
      expect(qwenCLI.executeCommand).toHaveBeenCalledWith('', ['-p', 'Test prompt']);
      expect(result).toBe('Agent execution result');
    });
    
    test('should execute an agent with iFlow CLI', async () => {
      // Mock the executeCommand method
      iflowCLI.executeCommand = jest.fn().mockResolvedValue('Agent execution result');
      
      const agent = {
        name: 'test-agent',
        cliTool: 'iflow',
        description: 'Test agent'
      };
      
      const result = await agentManager.executeAgent(iflowCLI, agent, 'Test prompt');
      
      expect(iflowCLI.executeCommand).toHaveBeenCalledWith('', ['-p', 'Test prompt']);
      expect(result).toBe('Agent execution result');
    });
    
    test('should execute an agent with Gemini CLI', async () => {
      // Mock the executeCommand method
      geminiCLI.executeCommand = jest.fn().mockResolvedValue('Agent execution result');
      
      const agent = {
        name: 'test-agent',
        cliTool: 'gemini',
        description: 'Test agent'
      };
      
      const result = await agentManager.executeAgent(geminiCLI, agent, 'Test prompt');
      
      expect(geminiCLI.executeCommand).toHaveBeenCalledWith('', ['-p', 'Test prompt']);
      expect(result).toBe('Agent execution result');
    });
    
    test('should execute an agent with Codex CLI', async () => {
      // Mock the executeCommand method
      codexCLI.executeCommand = jest.fn().mockResolvedValue('Agent execution result');
      
      const agent = {
        name: 'test-agent',
        cliTool: 'codex',
        description: 'Test agent'
      };
      
      const result = await agentManager.executeAgent(codexCLI, agent, 'Test prompt');
      
      expect(codexCLI.executeCommand).toHaveBeenCalledWith('exec', ['Test prompt']);
      expect(result).toBe('Agent execution result');
    });
  });
});