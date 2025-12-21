const BaseCLIWrapper = require('./BaseCLIWrapper');

/**
 * Wrapper class for iFlow CLI
 */
class IFlowCLIWrapper extends BaseCLIWrapper {
  /**
   * Constructor for IFlowCLIWrapper
   */
  constructor() {
    super('iflow', 'iflow');
  }

  /**
   * Manage agents for iFlow CLI
   * @param {string} action - Action to perform (list, add, remove, etc.)
   * @param {string} agentName - Name of the agent
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  async manageAgents(action, agentName = '') {
    const args = agentName ? [action, agentName] : [action];
    return this.executeCommand('agent', args);
  }

  /**
   * Manage workflows for iFlow CLI
   * @param {string} action - Action to perform (list, add, remove, etc.)
   * @param {string} workflowName - Name of the workflow
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  async manageWorkflows(action, workflowName = '') {
    const args = workflowName ? [action, workflowName] : [action];
    return this.executeCommand('workflow', args);
  }
}

module.exports = IFlowCLIWrapper;