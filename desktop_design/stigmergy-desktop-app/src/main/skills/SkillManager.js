const { CLIError } = require('../cli/BaseCLIWrapper');

/**
 * Skill class representing a CLI tool skill
 */
class Skill {
  /**
   * Constructor for Skill
   * @param {string} name - Name of the skill
   * @param {string} cliTool - CLI tool that provides the skill
   * @param {string} description - Description of the skill
   * @param {string} version - Version of the skill
   */
  constructor(name, cliTool, description = '', version = '') {
    this.name = name;
    this.cliTool = cliTool;
    this.description = description;
    this.version = version;
    this.installedAt = new Date();
  }
}

/**
 * Manager class for handling skills across different CLI tools
 */
class SkillManager {
  /**
   * Constructor for SkillManager
   */
  constructor() {
    this.skills = [];
  }

  /**
   * Discover skills available from a CLI tool
   * @param {BaseCLIWrapper} cliWrapper - CLI wrapper instance
   * @returns {Promise<string[]>} Promise that resolves with array of skill names
   */
  async discoverSkills(cliWrapper) {
    try {
      let output;
      
      // Use appropriate command based on CLI tool
      if (cliWrapper.name === 'stigmergy') {
        output = await cliWrapper.executeSkillCommand('list');
      } else if (cliWrapper.name === 'claude') {
        output = await cliWrapper.managePlugins('list');
      } else if (cliWrapper.name === 'qwen' || cliWrapper.name === 'gemini') {
        output = await cliWrapper.manageExtensions('list');
      } else if (cliWrapper.name === 'iflow') {
        output = await cliWrapper.executeCommand('commands', ['list']);
      } else if (cliWrapper.name === 'codex') {
        // Codex doesn't have a direct skill listing command
        return [];
      } else {
        // For other CLI tools, try a generic approach
        output = await cliWrapper.executeCommand('--help');
      }
      
      // Parse the output to extract skill names
      const skills = cliWrapper.parseOutput(output);
      return skills;
    } catch (error) {
      if (error instanceof CLIError) {
        throw error;
      } else {
        throw new CLIError(
          `Failed to discover skills: ${error.message}`,
          cliWrapper.name,
          'discover',
          null,
          error.message
        );
      }
    }
  }

  /**
   * Install a skill for a CLI tool
   * @param {BaseCLIWrapper} cliWrapper - CLI wrapper instance
   * @param {string} skillSource - Source of the skill to install
   * @returns {Promise<string>} Promise that resolves with installation output
   */
  async installSkill(cliWrapper, skillSource) {
    try {
      if (cliWrapper.name === 'stigmergy') {
        return await cliWrapper.executeSkillCommand('install', [skillSource]);
      } else if (cliWrapper.name === 'claude') {
        return await cliWrapper.managePlugins('install', skillSource);
      } else if (cliWrapper.name === 'qwen' || cliWrapper.name === 'gemini') {
        return await cliWrapper.manageExtensions('install', skillSource);
      } else if (cliWrapper.name === 'iflow') {
        return await cliWrapper.executeCommand('commands', ['install', skillSource]);
      } else {
        throw new CLIError(
          `Skill installation not supported for ${cliWrapper.name}`,
          cliWrapper.name,
          'install',
          null,
          `Skill installation not supported for ${cliWrapper.name}`
        );
      }
    } catch (error) {
      if (error instanceof CLIError) {
        throw error;
      } else {
        throw new CLIError(
          `Failed to install skill: ${error.message}`,
          cliWrapper.name,
          'install',
          null,
          error.message
        );
      }
    }
  }

  /**
   * Remove a skill from a CLI tool
   * @param {BaseCLIWrapper} cliWrapper - CLI wrapper instance
   * @param {string} skillName - Name of the skill to remove
   * @returns {Promise<string>} Promise that resolves with removal output
   */
  async removeSkill(cliWrapper, skillName) {
    try {
      if (cliWrapper.name === 'stigmergy') {
        return await cliWrapper.executeSkillCommand('remove', [skillName]);
      } else if (cliWrapper.name === 'claude') {
        return await cliWrapper.managePlugins('remove', skillName);
      } else if (cliWrapper.name === 'qwen' || cliWrapper.name === 'gemini') {
        return await cliWrapper.manageExtensions('remove', skillName);
      } else if (cliWrapper.name === 'iflow') {
        return await cliWrapper.executeCommand('commands', ['remove', skillName]);
      } else {
        throw new CLIError(
          `Skill removal not supported for ${cliWrapper.name}`,
          cliWrapper.name,
          'remove',
          null,
          `Skill removal not supported for ${cliWrapper.name}`
        );
      }
    } catch (error) {
      if (error instanceof CLIError) {
        throw error;
      } else {
        throw new CLIError(
          `Failed to remove skill: ${error.message}`,
          cliWrapper.name,
          'remove',
          null,
          error.message
        );
      }
    }
  }

  /**
   * Read a skill from a CLI tool
   * @param {BaseCLIWrapper} cliWrapper - CLI wrapper instance
   * @param {string} skillName - Name of the skill to read
   * @returns {Promise<string>} Promise that resolves with skill content
   */
  async readSkill(cliWrapper, skillName) {
    try {
      if (cliWrapper.name === 'stigmergy') {
        return await cliWrapper.executeSkillCommand('read', [skillName]);
      } else {
        throw new CLIError(
          `Reading skills not supported for ${cliWrapper.name}`,
          cliWrapper.name,
          'read',
          null,
          `Reading skills not supported for ${cliWrapper.name}`
        );
      }
    } catch (error) {
      if (error instanceof CLIError) {
        throw error;
      } else {
        throw new CLIError(
          `Failed to read skill: ${error.message}`,
          cliWrapper.name,
          'read',
          null,
          error.message
        );
      }
    }
  }

  /**
   * Add a skill to the manager
   * @param {Skill} skill - Skill to add
   */
  addSkill(skill) {
    this.skills.push(skill);
  }

  /**
   * Get all skills
   * @returns {Skill[]} Array of skills
   */
  getSkills() {
    return this.skills;
  }

  /**
   * Find skills by CLI tool
   * @param {string} cliTool - CLI tool name
   * @returns {Skill[]} Array of skills for the CLI tool
   */
  getSkillsByCLITool(cliTool) {
    return this.skills.filter(skill => skill.cliTool === cliTool);
  }
}

module.exports = SkillManager;
module.exports.Skill = Skill;