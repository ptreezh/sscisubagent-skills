const BaseCLIWrapper = require('./BaseCLIWrapper');

/**
 * Wrapper class for Stigmergy CLI
 */
class StigmergyCLIWrapper extends BaseCLIWrapper {
  /**
   * Constructor for StigmergyCLIWrapper
   */
  constructor() {
    super('stigmergy', 'stigmergy');
  }

  /**
   * Execute a skill command with the Stigmergy CLI
   * @param {string} subcommand - Skill subcommand (install/list/read/validate/remove/sync)
   * @param {string[]} args - Arguments for the skill command
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  async executeSkillCommand(subcommand, args = []) {
    return this.executeCommand('skill', [subcommand, ...args]);
  }

  /**
   * Execute a cross-CLI call using Stigmergy
   * @param {string} cliName - Name of the target CLI tool
   * @param {string} skillName - Name of the skill to call
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  async crossCLICall(cliName, skillName) {
    return this.executeCommand('use', [cliName, 'skill', skillName]);
  }
}

module.exports = StigmergyCLIWrapper;