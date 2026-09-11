#!/usr/bin/env node

/**
 * Qoder CLI - Main Entry Point
 * Integrates planning-with-files functionality with SSCI skills
 */

const { QoderPluginManager } = require('./qoder_plugin_manager');
const { SSkillExecutor } = require('./skill_executor');
const fs = require('fs').promises;
const path = require('path');

class QoderCLI {
  constructor() {
    this.pluginManager = null;
    this.skillExecutor = null;
    this.currentFindings = [];
    this.planningEnabled = false;
  }

  /**
   * Initialize the CLI with configuration
   */
  async init() {
    // Load configuration
    const configPath = './qoder_config.json';
    try {
      const configContent = await fs.readFile(configPath, 'utf8');
      const config = JSON.parse(configContent);
      
      // Initialize plugin manager
      this.pluginManager = new QoderPluginManager(config);
      await this.pluginManager.loadPlugins();
      
      // Initialize skill executor
      this.skillExecutor = new SSkillExecutor(this);
      
      // Set up global hooks
      this.setupGlobalHooks();
      
      console.log('Qoder CLI initialized successfully');
    } catch (error) {
      console.error('Failed to initialize Qoder CLI:', error.message);
      throw error;
    }
  }

  /**
   * Set up global hooks as defined in configuration
   */
  setupGlobalHooks() {
    // Register global onStart hook
    this.registerGlobalHook('onStart', async () => {
      await this.initializePlanningFiles();
    });
    
    // Register global onClear hook
    this.registerGlobalHook('onClear', async () => {
      await this.preservePlanningContext();
    });
    
    // Register global onToolUse hook
    this.registerGlobalHook('onToolUse', async () => {
      await this.maintainContext();
    });
    
    console.log('Global hooks registered');
  }

  /**
   * Register a global hook
   */
  registerGlobalHook(hookName, fn) {
    if (!this.globalHooks) {
      this.globalHooks = {};
    }
    this.globalHooks[hookName] = fn;
  }

  /**
   * Execute a global hook
   */
  async executeGlobalHook(hookName) {
    if (this.globalHooks && this.globalHooks[hookName]) {
      await this.globalHooks[hookName]();
    }
  }

  /**
   * Initialize planning files as specified in config
   */
  async initializePlanningFiles() {
    try {
      const config = await this.getConfig();
      const files = config.plugins && config.plugins['planning-with-files'] ? config.plugins['planning-with-files'].files : {
        plan: 'task_plan.md',
        findings: 'findings.md',
        progress: 'progress.md'
      };
      
      // Create planning files if they don't exist
      for (const [key, fileName] of Object.entries(files)) {
        try {
          await fs.access(fileName);
        } catch {
          // File doesn't exist, create it with initial content
          let initialContent = '';
          switch(key) {
            case 'plan':
              initialContent = '# Task Plan\n\n## Goals\n\n## Steps\n\n## Resources Needed\n';
              break;
            case 'findings':
              initialContent = '# Findings\n\n## Key Insights\n\n## Data Points\n\n## Observations\n';
              break;
            case 'progress':
              initialContent = '# Progress Tracking\n\n## Completed Tasks\n\n## In Progress\n\n## Blocked Items\n';
              break;
          }
          
          await fs.writeFile(fileName, initialContent);
          console.log(`Created initial ${key} file: ${fileName}`);
        }
      }
      
      this.planningEnabled = true;
    } catch (error) {
      console.error('Error initializing planning files:', error.message);
      // Set defaults if config is unavailable
      this.planningEnabled = true;
    }
  }

  /**
   * Preserve planning context during clear operations
   */
  async preservePlanningContext() {
    if (!this.planningEnabled) return;
    
    console.log('Preserving planning context during clear operation...');
    // The planning files remain on disk and will be reloaded when needed
  }

  /**
   * Maintain context during tool use
   */
  async maintainContext() {
    if (!this.planningEnabled) return;
    
    // Ensure planning files are accessible and up to date
    console.log('Maintaining planning context during tool use...');
  }

  /**
   * Get current configuration
   */
  async getConfig() {
    const configPath = './qoder_config.json';
    const configContent = await fs.readFile(configPath, 'utf8');
    const config = JSON.parse(configContent);
    return config;
  }

  /**
   * Execute a command with planning integration
   */
  async executeCommand(command, args) {
    // Execute pre-execution hooks
    await this.executeGlobalHook('onStart');
    
    if (command === 'skill') {
      // Extract skill name and parameters
      const skillName = args[0];
      const params = args.slice(1);
      
      // Execute skill through plugin manager
      return await this.pluginManager.executeSkill(skillName, params, this);
    } else if (command === 'planning-with-files:start') {
      // Start planning session
      return await this.startPlanningSession();
    } else if (command === 'planning-with-files:status') {
      // Show planning status
      return await this.showPlanningStatus();
    } else {
      // Handle other commands
      console.log(`Unknown command: ${command}`);
      return { error: `Unknown command: ${command}` };
    }
  }

  /**
   * Start a planning session
   */
  async startPlanningSession() {
    await this.initializePlanningFiles();
    
    return {
      success: true,
      message: 'Planning session started',
      files: {
        plan: 'task_plan.md',
        findings: 'findings.md',
        progress: 'progress.md'
      }
    };
  }

  /**
   * Show planning status
   */
  async showPlanningStatus() {
    try {
      const config = await this.getConfig();
      const files = config.plugins && config.plugins['planning-with-files'] ? config.plugins['planning-with-files'].files : {
        plan: 'task_plan.md',
        findings: 'findings.md',
        progress: 'progress.md'
      };
      
      const status = {};
      for (const [key, fileName] of Object.entries(files)) {
        try {
          const content = await fs.readFile(fileName, 'utf8');
          status[key] = {
            exists: true,
            size: content.length,
            preview: content.substring(0, 100) + (content.length > 100 ? '...' : '')
          };
        } catch (err) {
          status[key] = {
            exists: false,
            error: err.message
          };
        }
      }
      
      return { success: true, status };
    } catch (error) {
      // If config is unavailable, check default files
      const defaultFiles = {
        plan: 'task_plan.md',
        findings: 'findings.md',
        progress: 'progress.md'
      };
      
      const status = {};
      for (const [key, fileName] of Object.entries(defaultFiles)) {
        try {
          const content = await fs.readFile(fileName, 'utf8');
          status[key] = {
            exists: true,
            size: content.length,
            preview: content.substring(0, 100) + (content.length > 100 ? '...' : '')
          };
        } catch (err) {
          status[key] = {
            exists: false,
            error: err.message
          };
        }
      }
      
      return { success: true, status };
    }
  }

  /**
   * Run the CLI
   */
  async run(args) {
    await this.init();
    
    if (args.length === 0) {
      console.log('Qoder CLI - Planning-enhanced AI Assistant');
      console.log('Usage: qoder [command] [args]');
      console.log('Commands:');
      console.log('  skill <skill-name> [params...] - Execute a skill');
      console.log('  planning-with-files:start - Start a planning session');
      console.log('  planning-with-files:status - Show planning status');
      return;
    }
    
    const command = args[0];
    const commandArgs = args.slice(1);
    
    const result = await this.executeCommand(command, commandArgs);
    console.log('Command result:', result);
  }
}

// Handle command line execution
if (require.main === module) {
  const cli = new QoderCLI();
  
  // Process command line arguments
  const args = process.argv.slice(2);
  
  cli.run(args).catch(err => {
    console.error('Error running Qoder CLI:', err);
    process.exit(1);
  });
}

module.exports = { QoderCLI };