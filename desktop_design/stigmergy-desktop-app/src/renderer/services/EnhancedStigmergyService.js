// Enhanced Stigmergy Service
// This module provides enhanced integration with the Stigmergy CLI

const { ipcRenderer } = require('electron');

class EnhancedStigmergyService {
  /**
   * Execute a Stigmergy command
   * @param {string} command - The command to execute
   * @param {Array} args - Arguments for the command
   * @returns {Promise<Object>} - Result of the command execution
   */
  async executeCommand(command, args = []) {
    try {
      const result = await ipcRenderer.invoke('execute-stigmergy-command', command, args);
      return result;
    } catch (error) {
      return {
        success: false,
        command: `${command} ${args.join(' ')}`,
        stdout: '',
        stderr: '',
        error: error.message
      };
    }
  }

  /**
   * List all available skills
   * @returns {Promise<Object>}
   */
  async listSkills() {
    try {
      const result = await ipcRenderer.invoke('stigmergy-list-skills');
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Install a skill
   * @param {string} skillName - Name of the skill to install
   * @returns {Promise<Object>}
   */
  async installSkill(skillName) {
    try {
      const result = await ipcRenderer.invoke('stigmergy-install-skill', skillName);
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Remove a skill
   * @param {string} skillName - Name of the skill to remove
   * @returns {Promise<Object>}
   */
  async removeSkill(skillName) {
    try {
      const result = await ipcRenderer.invoke('stigmergy-remove-skill', skillName);
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get Stigmergy status
   * @returns {Promise<Object>}
   */
  async getStatus() {
    try {
      const result = await ipcRenderer.invoke('stigmergy-get-status');
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Configure Stigmergy
   * @param {string} key - Configuration key
   * @param {string} value - Configuration value
   * @returns {Promise<Object>}
   */
  async configure(key, value) {
    try {
      const result = await ipcRenderer.invoke('stigmergy-configure', key, value);
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Get Stigmergy configuration
   * @param {string} key - Configuration key to retrieve (optional)
   * @returns {Promise<Object>}
   */
  async getConfig(key = null) {
    try {
      const result = await ipcRenderer.invoke('stigmergy-get-config', key);
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * List available CLIs
   * @returns {Promise<Object>}
   */
  async listCLIs() {
    try {
      const result = await ipcRenderer.invoke('stigmergy-list-clis');
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Check Stigmergy version
   * @returns {Promise<Object>}
   */
  async getVersion() {
    try {
      const result = await ipcRenderer.invoke('stigmergy-get-version');
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
}

// Export a singleton instance
module.exports = new EnhancedStigmergyService();