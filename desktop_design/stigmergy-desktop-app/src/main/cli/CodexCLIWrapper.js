const BaseCLIWrapper = require('./BaseCLIWrapper');

/**
 * Wrapper class for Codex CLI
 */
class CodexCLIWrapper extends BaseCLIWrapper {
  /**
   * Constructor for CodexCLIWrapper
   */
  constructor() {
    super('codex', 'codex');
  }

  /**
   * Manage MCP servers for Codex CLI
   * @param {string} action - Action to perform (list, add, remove, etc.)
   * @param {string} config - Configuration for the MCP server
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  async manageMCP(action, config = '') {
    const args = config ? [action, config] : [action];
    return this.executeCommand('mcp', args);
  }

  /**
   * Perform code review with Codex CLI
   * @param {string[]} files - Files to review
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  async codeReview(files = []) {
    const args = ['review', ...files];
    return this.executeCommand('exec', args);
  }
}

module.exports = CodexCLIWrapper;