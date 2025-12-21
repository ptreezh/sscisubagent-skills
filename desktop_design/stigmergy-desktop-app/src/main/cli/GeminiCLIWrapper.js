const BaseCLIWrapper = require('./BaseCLIWrapper');

/**
 * Wrapper class for Gemini CLI
 */
class GeminiCLIWrapper extends BaseCLIWrapper {
  /**
   * Constructor for GeminiCLIWrapper
   */
  constructor() {
    super('gemini', 'gemini');
  }

  /**
   * Manage extensions for Gemini CLI
   * @param {string} action - Action to perform (install, list, remove, etc.)
   * @param {string} extensionName - Name of the extension
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  async manageExtensions(action, extensionName = '') {
    const args = extensionName ? [action, extensionName] : [action];
    return this.executeCommand('extensions', args);
  }

  /**
   * Manage MCP servers for Gemini CLI
   * @param {string} action - Action to perform (list, add, remove, etc.)
   * @param {string} config - Configuration for the MCP server
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  async manageMCP(action, config = '') {
    const args = config ? [action, config] : [action];
    return this.executeCommand('mcp', args);
  }
}

module.exports = GeminiCLIWrapper;