// Stigmergy CLI Wrapper
// This module provides a JavaScript interface to the Stigmergy CLI

const { exec } = require('child_process');
const { promisify } = require('util');

const execPromise = promisify(exec);

class StigmergyCLIWrapper {
  constructor() {
    this.stigmergyPath = 'stigmergy'; // Default path, can be configured
  }

  /**
   * Execute a Stigmergy command
   * @param {string} command - The command to execute
   * @param {Array} args - Arguments for the command
   * @returns {Promise<Object>} - Result of the command execution
   */
  async executeCommand(command, args = []) {
    // Handle special cases for commands that don't follow the standard pattern
    let fullCommand;
    if (command === '--version') {
      fullCommand = `${this.stigmergyPath} ${command}`;
    } else if (command === '') {
      // For commands like 'stigmergy config' or 'stigmergy config key'
      fullCommand = `${this.stigmergyPath} ${args.join(' ')}`;
    } else {
      fullCommand = `${this.stigmergyPath} ${command} ${args.join(' ')}`;
    }
    
    try {
      const { stdout, stderr } = await execPromise(fullCommand);
      
      return {
        success: true,
        command: fullCommand,
        stdout: stdout.trim(),
        stderr: stderr.trim(),
        error: null
      };
    } catch (error) {
      return {
        success: false,
        command: fullCommand,
        stdout: error.stdout ? error.stdout.trim() : '',
        stderr: error.stderr ? error.stderr.trim() : '',
        error: error.message
      };
    }
  }

  /**
   * List all available skills
   * @returns {Promise<Object>}
   */
  async listSkills() {
    return await this.executeCommand('skill', ['list']);
  }

  /**
   * Install a skill
   * @param {string} skillName - Name of the skill to install
   * @returns {Promise<Object>}
   */
  async installSkill(skillName) {
    return await this.executeCommand('skill', ['install', skillName]);
  }

  /**
   * Remove a skill
   * @param {string} skillName - Name of the skill to remove
   * @returns {Promise<Object>}
   */
  async removeSkill(skillName) {
    return await this.executeCommand('skill', ['remove', skillName]);
  }

  /**
   * Sync skills
   * @returns {Promise<Object>}
   */
  async syncSkills() {
    return await this.executeCommand('skill', ['sync']);
  }

  /**
   * Get Stigmergy status
   * @returns {Promise<Object>}
   */
  async getStatus() {
    return await this.executeCommand('status');
  }

  /**
   * Use a specific CLI
   * @param {string} cliName - Name of the CLI to use
   * @param {string} prompt - Prompt to send to the CLI
   * @returns {Promise<Object>}
   */
  async useCLI(cliName, prompt) {
    return await this.executeCommand('use', [cliName, `"${prompt}"`]);
  }

  /**
   * Call Stigmergy with a prompt
   * @param {string} prompt - Prompt to send to Stigmergy
   * @returns {Promise<Object>}
   */
  async callIntelligent(prompt) {
    return await this.executeCommand('call', [`"${prompt}"`]);
  }

  /**
   * Configure Stigmergy
   * @param {string} key - Configuration key
   * @param {string} value - Configuration value
   * @returns {Promise<Object>}
   */
  async configure(key, value) {
    if (value === undefined) {
      // Get config value
      return await this.executeCommand('', ['config', key]);
    } else {
      // Set config value
      return await this.executeCommand('', ['config', key, value]);
    }
  }

  /**
   * Get Stigmergy configuration
   * @param {string} key - Configuration key to retrieve (optional)
   * @returns {Promise<Object>}
   */
  async getConfig(key = null) {
    if (key) {
      return await this.executeCommand('', ['config', key]);
    } else {
      return await this.executeCommand('config');
    }
  }

  /**
   * List available CLIs
   * @returns {Promise<Object>}
   */
  async listCLIs() {
    return await this.executeCommand('list');
  }

  /**
   * Check Stigmergy version
   * @returns {Promise<Object>}
   */
  async getVersion() {
    return await this.executeCommand('--version');
  }
}

module.exports = StigmergyCLIWrapper;