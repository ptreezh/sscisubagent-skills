const { CLIError } = require('../cli/BaseCLIWrapper');

/**
 * Agent class representing a CLI tool agent
 */
class Agent {
  /**
   * Constructor for Agent
   * @param {string} name - Name of the agent
   * @param {string} cliTool - CLI tool that provides the agent
   * @param {string} description - Description of the agent
   * @param {string} version - Version of the agent
   */
  constructor(name, cliTool, description = '', version = '') {
    this.name = name;
    this.cliTool = cliTool;
    this.description = description;
    this.version = version;
    this.registeredAt = new Date();
  }
}

/**
 * Manager class for handling agents across different CLI tools
 */
class AgentManager {
  /**
   * Constructor for AgentManager
   */
  constructor() {
    this.agents = [];
  }

  /**
   * Register a new agent
   * @param {Agent} agent - Agent to register
   */
  registerAgent(agent) {
    this.agents.push(agent);
  }

  /**
   * Get all agents
   * @returns {Agent[]} Array of agents
   */
  getAgents() {
    return this.agents;
  }

  /**
   * Find agents by CLI tool
   * @param {string} cliTool - CLI tool name
   * @returns {Agent[]} Array of agents for the CLI tool
   */
  getAgentsByCLITool(cliTool) {
    return this.agents.filter(agent => agent.cliTool === cliTool);
  }

  /**
   * Execute an agent with a given prompt
   * @param {BaseCLIWrapper} cliWrapper - CLI wrapper instance
   * @param {Agent} agent - Agent to execute
   * @param {string} prompt - Prompt to send to the agent
   * @returns {Promise<string>} Promise that resolves with agent execution output
   */
  async executeAgent(cliWrapper, agent, prompt) {
    try {
      // Use appropriate command based on CLI tool
      if (cliWrapper.name === 'stigmergy') {
        // For Stigmergy, we use the call command directly
        // Stigmergy handles smart routing internally based on the prompt
        return await cliWrapper.executeCommand('call', [prompt]);
      } else if (cliWrapper.name === 'claude') {
        // For Claude, we pass the prompt directly with print mode for non-interactive output
        return await cliWrapper.executeCommand('', ['-p', prompt]);
      } else if (cliWrapper.name === 'qwen') {
        // For Qwen, we pass the prompt directly with print mode
        return await cliWrapper.executeCommand('', ['-p', prompt]);
      } else if (cliWrapper.name === 'iflow') {
        // For iFlow, we pass the prompt directly with print mode
        return await cliWrapper.executeCommand('', ['-p', prompt]);
      } else if (cliWrapper.name === 'gemini') {
        // For Gemini, we pass the prompt directly with text output format
        return await cliWrapper.executeCommand('', ['-p', prompt]);
      } else if (cliWrapper.name === 'codex') {
        // For Codex, we use the exec command
        return await cliWrapper.executeCommand('exec', [prompt]);
      } else {
        // For other CLI tools, try a generic approach
        return await cliWrapper.executeCommand('', [prompt]);
      }
    } catch (error) {
      if (error instanceof CLIError) {
        throw error;
      } else {
        throw new CLIError(
          `Failed to execute agent: ${error.message}`,
          cliWrapper.name,
          'execute',
          null,
          error.message
        );
      }
    }
  }
}

module.exports = AgentManager;
module.exports.Agent = Agent;