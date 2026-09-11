#!/usr/bin/env node
/**
 * Qoder Superpowers Installation Script
 * 
 * Implements the superpowers installation pattern:
 * - Creates three-tier skill system (project → personal → superpowers/system)
 * - Registers plugins via symlinks to superpowers.js equivalent
 * - Sets up hooks like chat.message for automatic context injection
 * - Configures skill priority order
 */

const fs = require('fs').promises;
const path = require('path');
const os = require('os');

async function installQoderSuperpowers() {
  console.log('🚀 Installing Qoder Superpowers...\n');
  
  try {
    // Create three-tier skill directories
    console.log('📁 Setting up three-tier skill system...');
    const homeDir = os.homedir();
    
    const skillDirs = [
      './.opencode/skills/',                           // Project skills (highest priority)
      path.join(homeDir, '.config', 'qoder', 'skills'), // Personal skills (medium priority)  
      './qoder/skills/'                               // System skills (lowest priority)
    ];
    
    for (const dirPath of skillDirs) {
      await createDirIfNotExists(dirPath);
      console.log(`✓ Created skill directory: ${dirPath}`);
    }
    console.log('');
    
    // Register plugin via symlink mechanism (Windows-compatible approach)
    console.log('🔌 Registering plugins via symlink mechanism...');
    const pluginDir = path.join(homeDir, '.config', 'qoder', 'plugins');
    await createDirIfNotExists(pluginDir);
    
    // On Windows, we'll create a plugin registration file instead of symlink
    const pluginRegistration = {
      name: 'qoder_superpowers',
      path: path.resolve('./qoder_superpowers.js'),
      hooks: ['chat.message'],
      enabled: true
    };
    
    await fs.writeFile(
      path.join(pluginDir, 'qoder_superpowers.json'), 
      JSON.stringify(pluginRegistration, null, 2)
    );
    
    console.log('✓ Registered qoder_superpowers plugin with chat.message hook');
    console.log('');
    
    // Verify skill files exist
    console.log('🔍 Verifying skill files...');
    const requiredSkills = [
      './.opencode/SKILL.md',
      './.opencode/skills/planning-context-injector.md', 
      './.opencode/skills/research-skill-orchestrator.md'
    ];
    
    for (const skillPath of requiredSkills) {
      try {
        await fs.access(skillPath);
        console.log(`✓ Found skill: ${skillPath}`);
      } catch (err) {
        console.log(`⚠️  Missing skill: ${skillPath} (may need to be created)`);
      }
    }
    console.log('');
    
    // Set up configuration
    console.log('⚙️  Setting up configuration...');
    const config = {
      skills: {
        priorityOrder: [
          'project: ./.opencode/skills/',
          'personal: ~/.config/qoder/skills/',
          'system: ./qoder/skills/'
        ]
      },
      hooks: {
        'chat.message': {
          enabled: true,
          handlers: [
            './.opencode/skills/planning-context-injector.md',
            './.opencode/SKILL.md'
          ]
        }
      },
      plugins: {
        registered: [
          path.join(homeDir, '.config', 'qoder', 'plugins', 'qoder_superpowers.json')
        ]
      }
    };
    
    await fs.writeFile('./qoder_superpowers_config.json', JSON.stringify(config, null, 2));
    console.log('✓ Created superpowers configuration');
    console.log('');
    
    // Create initial planning files if they don't exist
    console.log('📝 Creating initial planning files...');
    await createInitialPlanningFiles();
    console.log('✓ Planning files created');
    console.log('');
    
    // Display installation summary
    console.log('✅ Qoder Superpowers installed successfully!\n');
    console.log('📋 Installation Summary:');
    console.log('• Three-tier skill system: project → personal → system');
    console.log('• Plugin registration: qoder_superpowers with chat.message hook');
    console.log('• Automatic context injection: Planning context added to messages');
    console.log('• Skill orchestration: Research skills automatically selected');
    console.log('');
    
    console.log('🎯 Available Capabilities:');
    console.log('• Automatic planning context injection via chat.message hook');
    console.log('• Research skill orchestration based on query analysis');
    console.log('• Three-tier skill priority system');
    console.log('• Persistent planning with task_plan.md, findings.md, progress.md');
    
  } catch (error) {
    console.error('❌ Installation failed:', error.message);
    process.exit(1);
  }
}

/**
 * Create directory if it doesn't exist
 */
async function createDirIfNotExists(dirPath) {
  try {
    await fs.mkdir(dirPath, { recursive: true });
  } catch (error) {
    if (error.code !== 'EEXIST') {
      throw error;
    }
  }
}

/**
 * Create initial planning files
 */
async function createInitialPlanningFiles() {
  const planningFiles = {
    'task_plan.md': '# Task Plan\n\n## Current Goals\n\n## Next Steps\n\n## Resources Needed\n',
    'findings.md': '# Research Findings\n\n## Key Insights\n\n## Data Points\n\n## Important Notes\n',
    'progress.md': '# Progress Tracking\n\n## Completed Tasks\n\n## In Progress\n\n## Blocked Items\n'
  };
  
  for (const [filename, content] of Object.entries(planningFiles)) {
    try {
      await fs.access(filename);
      // File exists, don't overwrite
    } catch {
      // File doesn't exist, create it
      await fs.writeFile(filename, content);
    }
  }
}

// Run installation if this script is executed directly
if (require.main === module) {
  installQoderSuperpowers();
}

module.exports = { installQoderSuperpowers };