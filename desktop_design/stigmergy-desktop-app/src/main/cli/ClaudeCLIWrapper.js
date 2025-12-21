const BaseCLIWrapper = require('./BaseCLIWrapper');

/**
 * Wrapper class for Claude CLI
 */
class ClaudeCLIWrapper extends BaseCLIWrapper {
  /**
   * Constructor for ClaudeCLIWrapper
   */
  constructor() {
    super('claude', 'claude');
  }

  /**
   * Manage plugins for Claude CLI
   * @param {string} action - Action to perform (install, list, remove, etc.)
   * @param {string} pluginName - Name of the plugin
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  async managePlugins(action, pluginName = '') {
    const args = pluginName ? [action, pluginName] : [action];
    return this.executeCommand('plugin', args);
  }

  /**
   * Manage MCP servers for Claude CLI
   * @param {string} action - Action to perform (list, add, remove, etc.)
   * @param {string} config - Configuration for the MCP server
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  async manageMCP(action, config = '') {
    const args = config ? [action, config] : [action];
    return this.executeCommand('mcp', args);
  }
}

module.exports = ClaudeCLIWrapper;