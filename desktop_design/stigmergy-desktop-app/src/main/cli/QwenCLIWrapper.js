const BaseCLIWrapper = require('./BaseCLIWrapper');

/**
 * Wrapper class for Qwen CLI
 */
class QwenCLIWrapper extends BaseCLIWrapper {
  /**
   * Constructor for QwenCLIWrapper
   */
  constructor() {
    super('qwen', 'qwen');
  }

  /**
   * Manage extensions for Qwen CLI
   * @param {string} action - Action to perform (install, list, remove, etc.)
   * @param {string} extensionName - Name of the extension
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  async manageExtensions(action, extensionName = '') {
    const args = extensionName ? [action, extensionName] : [action];
    return this.executeCommand('extensions', args);
  }

  /**
   * Manage MCP servers for Qwen CLI
   * @param {string} action - Action to perform (list, add, remove, etc.)
   * @param {string} config - Configuration for the MCP server
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  async manageMCP(action, config = '') {
    const args = config ? [action, config] : [action];
    return this.executeCommand('mcp', args);
  }
}

module.exports = QwenCLIWrapper;