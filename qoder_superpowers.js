#!/usr/bin/env node
/**
 * Qoder Superpowers Plugin
 * Registers via symlink to provide chat.message hook functionality
 * 
 * This plugin implements the superpowers pattern with:
 * - chat.message hook for automatic context injection
 * - Symlink registration mechanism
 * - Three-tier skill priority system
 */

const fs = require('fs').promises;
const path = require('path');

class QoderSuperpowersPlugin {
  constructor() {
    this.name = 'qoder-superpowers';
    this.version = '1.0.0';
    this.hooks = ['chat.message'];
  }

  /**
   * Hook into chat.message to inject planning context
   */
  async onChatMessage(message) {
    // Automatically inject planning context into messages
    const context = await this.getPlanningContext();
    if (context && context.length > 0) {
      // Prepend planning context to the message
      return {
        ...message,
        context: context,
        enhanced: true
      };
    }
    return message;
  }

  /**
   * Get current planning context from files
   */
  async getPlanningContext() {
    const context = [];

    // Try to read planning files
    const planningFiles = {
      'task_plan.md': 'Current Task Plan',
      'findings.md': 'Recent Findings', 
      'progress.md': 'Progress Status'
    };

    for (const [filename, description] of Object.entries(planningFiles)) {
      try {
        const content = await fs.readFile(filename, 'utf8');
        if (content.trim()) {
          context.push(`${description}:\n${content.substring(0, 500)}${content.length > 500 ? '...' : ''}`);
        }
      } catch (err) {
        // File doesn't exist, skip
      }
    }

    return context;
  }

  /**
   * Initialize the plugin
   */
  async initialize() {
    console.log(`${this.name} plugin initialized with hooks: ${this.hooks.join(', ')}`);
    
    // Set up the three-tier skill system
    await this.setupSkillDirectories();
    
    return true;
  }

  /**
   * Set up the three-tier skill directory structure
   */
  async setupSkillDirectories() {
    const os = require('os');
    const homeDir = os.homedir();
    
    const directories = [
      './.opencode/skills/',           // Project skills (highest priority)
      path.join(homeDir, '.config', 'qoder', 'skills'), // Personal skills (medium priority)
      './qoder/skills/'                // System skills (lowest priority)
    ];

    for (const dir of directories) {
      try {
        await fs.mkdir(dir, { recursive: true });
      } catch (err) {
        if (err.code !== 'EEXIST') {
          console.warn(`Warning: Could not create directory ${dir}:`, err.message);
        }
      }
    }
  }

  /**
   * Get plugin metadata
   */
  getMetadata() {
    return {
      name: this.name,
      version: this.version,
      hooks: this.hooks,
      description: 'Qoder Superpowers plugin with chat.message hook for automatic context injection'
    };
  }
}

// Export the plugin class
module.exports = QoderSuperpowersPlugin;

// If run directly, initialize the plugin
if (require.main === module) {
  const plugin = new QoderSuperpowersPlugin();
  plugin.initialize()
    .then(() => console.log('Plugin initialized successfully'))
    .catch(err => console.error('Plugin initialization failed:', err));
}