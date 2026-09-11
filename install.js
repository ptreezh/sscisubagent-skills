#!/usr/bin/env node

/**
 * Qoder CLI Skills Installation Script
 * Sets up the Qoder CLI with planning-with-files and SSCI skills
 */

const fs = require('fs').promises;
const path = require('path');
const os = require('os');

async function installQoderSkills() {
  console.log('🚀 Installing Qoder CLI Skills System...\n');
  
  try {
    // Step 1: Check prerequisites
    console.log('🔍 Checking prerequisites...');
    const nodeVersion = process.version;
    const minVersion = '14.0.0';
    
    if (!isVersionGreaterOrEqual(nodeVersion.replace('v', ''), minVersion)) {
      throw new Error(`Node.js version ${minVersion} or higher is required. Current version: ${nodeVersion}`);
    }
    
    console.log(`✓ Node.js version: ${nodeVersion}`);
    console.log('✓ Prerequisites check passed\n');
    
    // Step 2: Create directory structure
    console.log('📁 Creating directory structure...');
    const homeDir = os.homedir();
    const personalSkillsDir = path.join(homeDir, '.config', 'qoder', 'skills');
    const projectSkillsDir = path.join(process.cwd(), '.opencode', 'skills');
    
    await createDirIfNotExists(personalSkillsDir);
    await createDirIfNotExists(projectSkillsDir);
    
    console.log(`✓ Created personal skills directory: ${personalSkillsDir}`);
    console.log(`✓ Created project skills directory: ${projectSkillsDir}\n`);
    
    // Step 3: Verify SSCI skills exist
    console.log('📦 Verifying SSCI skills...');
    try {
      await fs.access(path.join(process.cwd(), 'sscisubagent-skills'));
      console.log('✓ SSCI skills found\n');
    } catch {
      console.log('⚠️  SSCI skills not found. You may need to clone them separately:\n   git clone https://github.com/ptreezh/sscisubagent-skills.git\n');
    }
    
    // Step 4: Verify configuration exists
    console.log('⚙️  Verifying configuration...');
    try {
      await fs.access(path.join(process.cwd(), 'qoder_config.json'));
      console.log('✓ Configuration file found\n');
    } catch {
      console.log('⚠️  Configuration file not found. Creating a basic one...');
      await createBasicConfig();
      console.log('✓ Basic configuration created\n');
    }
    
    // Step 5: Create planning files
    console.log('📝 Creating planning files...');
    await createPlanningFiles();
    console.log('✓ Planning files created\n');
    
    // Step 6: Display installation summary
    console.log('✅ Qoder CLI Skills System installed successfully!\n');
    console.log('📋 Installation Summary:');
    console.log('- Configuration: qoder_config.json');
    console.log('- SSCI Skills: sscisubagent-skills/');
    console.log('- Planning Files: task_plan.md, findings.md, progress.md');
    console.log('- Personal Skills: ~/.config/qoder/skills/');
    console.log('- Project Skills: .opencode/skills/\n');
    
    console.log('🚀 Ready to use Qoder CLI! Try:');
    console.log('   node qoder_cli.js planning-with-files:start');
    console.log('   node qoder_cli.js skill grounded-theory-expert analyze data');
    
  } catch (error) {
    console.error('❌ Installation failed:', error.message);
    process.exit(1);
  }
}

/**
 * Helper function to compare versions
 */
function isVersionGreaterOrEqual(current, required) {
  const [currMajor, currMinor, currPatch] = current.split('.').map(Number);
  const [reqMajor, reqMinor, reqPatch] = required.split('.').map(Number);
  
  if (currMajor > reqMajor) return true;
  if (currMajor < reqMajor) return false;
  if (currMinor > reqMinor) return true;
  if (currMinor < reqMinor) return false;
  return currPatch >= reqPatch;
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
 * Create basic configuration if it doesn't exist
 */
async function createBasicConfig() {
  const config = {
    "skills": {
      "enabled": true,
      "directories": [
        "./sscisubagent-skills/skills",
        "./custom_skills",
        "~/.config/qoder/skills",
        "./.opencode/skills"
      ],
      "plugins": {
        "planning-with-files": {
          "enabled": true,
          "hooks": {
            "preExecution": ["read_plan"],
            "postExecution": ["save_findings", "update_progress"]
          },
          "files": {
            "plan": "task_plan.md",
            "findings": "findings.md",
            "progress": "progress.md"
          }
        }
      }
    },
    "hooks": {
      "global": {
        "onStart": ["initialize_planning_files"],
        "onClear": ["preserve_planning_context"],
        "onToolUse": ["maintain_context"]
      }
    }
  };
  
  await fs.writeFile('qoder_config.json', JSON.stringify(config, null, 2));
}

/**
 * Create initial planning files
 */
async function createPlanningFiles() {
  const planningFiles = {
    'task_plan.md': '# Task Plan\n\n## Goals\n\n## Steps\n\n## Resources Needed\n',
    'findings.md': '# Findings\n\n## Key Insights\n\n## Data Points\n\n## Observations\n',
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
  installQoderSkills();
}

module.exports = { installQoderSkills };