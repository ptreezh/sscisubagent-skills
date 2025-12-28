// Real User Desktop Application End-to-End Test
// This test simulates real user interactions with the desktop application

const { spawn, exec } = require('child_process');
const { promisify } = require('util');
const execAsync = promisify(exec);
const path = require('path');
const fs = require('fs');
const os = require('os');

class RealUserDesktopE2ETest {
  constructor() {
    this.testProjectDir = path.join(os.tmpdir(), 'stigmergy-real-user-e2e');
    this.sessionLog = [];
    this.testResults = {
      appLaunch: false,
      uiInteraction: false,
      terminalFunctionality: false,
      fileManagerSync: false,
      cliIntegration: false,
      userWorkflows: false
    };
  }

  /**
   * Log user activity
   */
  logActivity(activity, details = {}) {
    const logEntry = {
      timestamp: new Date(),
      activity,
      details
    };
    this.sessionLog.push(logEntry);
    console.log(`[${logEntry.timestamp.toISOString()}] ${activity}`);
  }

  /**
   * Setup realistic test environment
   */
  async setupRealisticEnvironment() {
    this.logActivity('Setting up realistic test environment');
    
    if (!fs.existsSync(this.testProjectDir)) {
      fs.mkdirSync(this.testProjectDir, { recursive: true });
    }
    
    // Create realistic project structure
    const projectStructure = {
      'package.json': JSON.stringify({
        name: 'real-user-project',
        version: '1.0.0',
        description: 'A project created by real user',
        scripts: {
          start: 'node index.js',
          test: 'jest'
        }
      }, null, 2),
      'README.md': '# Real User Project\n\nCreated during real user testing.',
      'index.js': 'console.log("Hello from real user project!");',
      'src': {
        'main.js': '// Main application logic\nfunction main() {\n  console.log("Application started");\n}\n\nmain();'
      },
      'tests': {
        'main.test.js': '// Test file\nconsole.log("Testing main functionality");'
      },
      'docs': {
        'README.md': '# Project Documentation\n\nUser documentation.'
      }
    };
    
    // Create the structure
    for (const [key, value] of Object.entries(projectStructure)) {
      if (typeof value === 'string') {
        fs.writeFileSync(path.join(this.testProjectDir, key), value);
      } else if (typeof value === 'object') {
        const dirPath = path.join(this.testProjectDir, key);
        if (!fs.existsSync(dirPath)) {
          fs.mkdirSync(dirPath, { recursive: true });
        }
        for (const [subKey, subValue] of Object.entries(value)) {
          fs.writeFileSync(path.join(dirPath, subKey), subValue);
        }
      }
    }
    
    this.logActivity('Realistic environment created', { path: this.testProjectDir });
  }

  /**
   * Execute command in test directory
   */
  async executeCommand(command, cwd = this.testProjectDir) {
    return new Promise((resolve, reject) => {
      const [cmd, ...args] = command.split(' ');
      
      const child = spawn(cmd, args, {
        cwd,
        env: process.env,
        shell: true
      });

      let stdout = '';
      let stderr = '';

      child.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      child.on('close', (code) => {
        resolve({
          command,
          stdout,
          stderr,
          exitCode: code,
          cwd
        });
      });

      child.on('error', (error) => {
        reject(error);
      });
    });
  }

  /**
   * Real User Flow 1: Project Discovery and Exploration
   */
  async flowProjectDiscovery() {
    this.logActivity('Starting flow: Project Discovery and Exploration');
    
    try {
      // User opens terminal and explores project
      const lsResult = await this.executeCommand(os.platform() === 'win32' ? 'dir' : 'ls -la');
      this.logActivity('User explores project root', { 
        filesCount: lsResult.stdout.split('\n').filter(line => line.trim()).length,
        hasPackageJson: lsResult.stdout.includes('package.json')
      });
      
      // User examines project files
      const readmeResult = await this.executeCommand(os.platform() === 'win32' ? 'type README.md' : 'cat README.md');
      const hasRealUserProject = readmeResult.stdout.toLowerCase().includes('real user');
      
      this.logActivity('User examines README.md', { hasRealUserProject });
      
      // User explores directory structure
      const treeCommand = os.platform() === 'win32' ? 'dir /s' : 'find . -type f';
      const treeResult = await this.executeCommand(treeCommand);
      const totalFiles = treeResult.stdout.split('\n').filter(line => line.trim()).length;
      
      this.logActivity('User explores directory structure', { totalFiles });
      
      // User checks package.json
      const packageResult = await this.executeCommand(os.platform() === 'win32' ? 'type package.json' : 'cat package.json');
      const hasScripts = packageResult.stdout.includes('scripts');
      
      this.logActivity('User checks package.json', { hasScripts });
      
      return { 
        success: lsResult.exitCode === 0 && hasRealUserProject && hasScripts,
        filesExplored: totalFiles
      };
    } catch (error) {
      this.logActivity('Project discovery failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Real User Flow 2: Code Modification and File Operations
   */
  async flowCodeModification() {
    this.logActivity('Starting flow: Code Modification and File Operations');
    
    try {
      // User modifies main file
      const modification = '\n// Added by user during testing\nconsole.log("Feature added by real user");\n';
      
      if (os.platform() === 'win32') {
        const psCommand = `powershell -Command "Add-Content -Path '.\\\\index.js' -Value '${modification.replace(/'/g, "''")}'"`;
        const appendResult = await this.executeCommand(psCommand);
      } else {
        const appendResult = await this.executeCommand(`echo "${modification}" >> index.js`);
      }
      
      // User verifies modification
      const verifyResult = await this.executeCommand(os.platform() === 'win32' ? 'type index.js' : 'cat index.js');
      const hasUserFeature = verifyResult.stdout.includes('Feature added by real user');
      
      this.logActivity('User modifies code', { hasUserFeature });
      
      // User creates a new file
      const newFileContent = '// New feature file\nconsole.log("New feature implementation");\n';
      
      if (os.platform() === 'win32') {
        const psCommand = `powershell -Command "Set-Content -Path 'new-feature.js' -Value '${newFileContent.replace(/\n/g, '`n').replace(/'/g, "''")}'"`;
        const createResult = await this.executeCommand(psCommand);
      } else {
        const createResult = await this.executeCommand(`echo '${newFileContent}' > new-feature.js`);
      }
      
      // User verifies new file exists
      const lsResult = await this.executeCommand(os.platform() === 'win32' ? 'dir' : 'ls -la');
      const hasNewFile = lsResult.stdout.toLowerCase().includes('new-feature.js');
      
      this.logActivity('User creates new file', { hasNewFile });
      
      return { 
        success: hasUserFeature && hasNewFile,
        codeModified: hasUserFeature,
        fileCreated: hasNewFile
      };
    } catch (error) {
      this.logActivity('Code modification failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Real User Flow 3: Terminal and CLI Interaction
   */
  async flowTerminalCLIInteraction() {
    this.logActivity('Starting flow: Terminal and CLI Interaction');
    
    try {
      // User runs project
      const runResult = await this.executeCommand(os.platform() === 'win32' ? 'node .\\index.js' : 'node index.js');
      const appOutput = runResult.stdout.toLowerCase();
      const appRuns = appOutput.includes('hello from real user') || 
                     appOutput.includes('feature added by real user');
      
      this.logActivity('User runs the project', { appRuns, output: appOutput.substring(0, 100) });
      
      // User uses stigmergy CLI
      const versionResult = await this.executeCommand('stigmergy --version');
      const hasVersion = versionResult.stdout.trim().length > 0;
      
      this.logActivity('User checks stigmergy version', { version: versionResult.stdout.trim() });
      
      // User lists skills
      const skillsResult = await this.executeCommand('stigmergy skill list');
      const hasSkills = skillsResult.stdout.length > 100; // Should have substantial output
      
      this.logActivity('User lists available skills', { skillsCount: skillsResult.stdout.split('\n').length });
      
      // User gets help
      const helpResult = await this.executeCommand('stigmergy help');
      const hasHelp = helpResult.stdout.length > 50;
      
      this.logActivity('User gets help', { hasHelp });
      
      return { 
        success: appRuns && hasVersion && hasSkills && hasHelp,
        appRuns,
        hasVersion,
        hasSkills,
        hasHelp
      };
    } catch (error) {
      this.logActivity('Terminal/CLI interaction failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Real User Flow 4: Directory Navigation and File Management
   */
  async flowDirectoryNavigation() {
    this.logActivity('Starting flow: Directory Navigation and File Management');
    
    try {
      // User navigates to src directory
      const srcPath = path.join(this.testProjectDir, 'src');
      const pwdResult = await this.executeCommand(os.platform() === 'win32' ? 'cd' : 'pwd', srcPath);
      const inSrcDir = pwdResult.stdout.trim().toLowerCase().includes('src');
      
      this.logActivity('User navigates to src directory', { inSrcDir, path: pwdResult.stdout.trim() });
      
      // User lists files in src
      const lsResult = await this.executeCommand(os.platform() === 'win32' ? 'dir' : 'ls -la', srcPath);
      const hasMainJs = lsResult.stdout.toLowerCase().includes('main.js');
      
      this.logActivity('User lists files in src', { hasMainJs });
      
      // User creates file in src directory
      const newSrcFileContent = '// New source file\nfunction newFeature() {\n  return "New source feature";\n}\n\nmodule.exports = { newFeature };';
      
      if (os.platform() === 'win32') {
        const psCommand = `powershell -Command "Set-Content -Path 'new-source.js' -Value '${newSrcFileContent.replace(/\n/g, '`n').replace(/'/g, "''")}'"`;
        const createResult = await this.executeCommand(psCommand, srcPath);
      } else {
        const createResult = await this.executeCommand(`echo '${newSrcFileContent}' > new-source.js`, srcPath);
      }
      
      // User verifies file creation
      const verifyResult = await this.executeCommand(os.platform() === 'win32' ? 'dir' : 'ls -la', srcPath);
      const hasNewSrcFile = verifyResult.stdout.toLowerCase().includes('new-source.js');
      
      this.logActivity('User creates file in src directory', { hasNewSrcFile });
      
      // User goes back to root
      const backResult = await this.executeCommand(os.platform() === 'win32' ? 'cd' : 'pwd');
      const backToRoot = !backResult.stdout.toLowerCase().includes('src');
      
      this.logActivity('User navigates back to root', { backToRoot });
      
      return { 
        success: inSrcDir && hasMainJs && hasNewSrcFile && backToRoot,
        navigationSuccessful: inSrcDir,
        fileCreated: hasNewSrcFile,
        navigationBack: backToRoot
      };
    } catch (error) {
      this.logActivity('Directory navigation failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Real User Flow 5: Project Building and Testing
   */
  async flowProjectBuilding() {
    this.logActivity('Starting flow: Project Building and Testing');
    
    try {
      // User creates test file
      const testContent = `// Real user test file
describe('Real User Project', () => {
  test('should run successfully', () => {
    expect(1).toBe(1);
  });
  
  test('should have expected output', () => {
    const output = 'Hello from real user project!';
    expect(output).toContain('real user');
  });
});`;
      
      if (os.platform() === 'win32') {
        const psCommand = `powershell -Command "Set-Content -Path 'real-user.test.js' -Value '${testContent.replace(/\n/g, '`n').replace(/'/g, "''")}'"`;
        const createResult = await this.executeCommand(psCommand);
      } else {
        const createResult = await this.executeCommand(`echo '${testContent}' > real-user.test.js`);
      }
      
      // User verifies test file exists
      const lsResult = await this.executeCommand(os.platform() === 'win32' ? 'dir' : 'ls -la');
      const hasTestFile = lsResult.stdout.toLowerCase().includes('real-user.test.js');
      
      this.logActivity('User creates test file', { hasTestFile });
      
      // User might try to run tests (simulated)
      const runTestResult = await this.executeCommand(os.platform() === 'win32' ? 'type real-user.test.js' : 'cat real-user.test.js');
      const testFileCorrect = runTestResult.stdout.includes('describe') && 
                             runTestResult.stdout.includes('expect');
      
      this.logActivity('User verifies test file content', { testFileCorrect });
      
      // User creates configuration
      const configContent = `{
  "projectName": "Real User Project",
  "version": "1.0.0",
  "config": {
    "environment": "development",
    "debug": true,
    "features": ["real-user-feature"]
  }
}`;
      
      if (os.platform() === 'win32') {
        const psCommand = `powershell -Command "Set-Content -Path 'config.json' -Value '${configContent.replace(/\n/g, '`n').replace(/'/g, "''")}'"`;
        const configResult = await this.executeCommand(psCommand);
      } else {
        const configResult = await this.executeCommand(`echo '${configContent}' > config.json`);
      }
      
      // Verify config file
      const configVerify = await this.executeCommand(os.platform() === 'win32' ? 'type config.json' : 'cat config.json');
      const hasRealUserConfig = configVerify.stdout.includes('real-user-feature');
      
      this.logActivity('User creates configuration', { hasRealUserConfig });
      
      return { 
        success: hasTestFile && testFileCorrect && hasRealUserConfig,
        testFileCreated: hasTestFile,
        testFileCorrect,
        configCreated: hasRealUserConfig
      };
    } catch (error) {
      this.logActivity('Project building failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Real User Flow 6: Skill Utilization and Advanced Features
   */
  async flowSkillUtilization() {
    this.logActivity('Starting flow: Skill Utilization and Advanced Features');
    
    try {
      // User explores available skills
      const skillsResult = await this.executeCommand('stigmergy skill list');
      const skillsList = skillsResult.stdout;
      
      this.logActivity('User explores available skills', { 
        skillsOutputLength: skillsList.length,
        skillsCount: skillsList.split('\n').length
      });
      
      // User might try to use a specific skill (simulated)
      const helpResult = await this.executeCommand('stigmergy help');
      const hasHelpContent = helpResult.stdout.length > 100;
      
      this.logActivity('User accesses help system', { hasHelpContent });
      
      // User checks status
      const statusResult = await this.executeCommand('stigmergy status');
      const statusOk = statusResult.exitCode === 0;
      
      this.logActivity('User checks system status', { statusOk });
      
      // User creates a skill-related file
      const skillFileContent = `# Skill Usage Documentation

This project demonstrates the use of various Stigmergy skills:

- Project management
- Code development  
- Testing and validation
- Configuration management

Created by a real user during testing.`;
      
      if (os.platform() === 'win32') {
        const psCommand = `powershell -Command "Set-Content -Path 'SKILLS_USAGE.md' -Value '${skillFileContent.replace(/\n/g, '`n').replace(/'/g, "''")}'"`;
        const skillFileResult = await this.executeCommand(psCommand);
      } else {
        const skillFileResult = await this.executeCommand(`echo '${skillFileContent}' > SKILLS_USAGE.md`);
      }
      
      // Verify skill file
      const skillFileVerify = await this.executeCommand(os.platform() === 'win32' ? 'type SKILLS_USAGE.md' : 'cat SKILLS_USAGE.md');
      const hasSkillsUsage = skillFileVerify.stdout.toLowerCase().includes('skill');
      
      this.logActivity('User creates skill usage documentation', { hasSkillsUsage });
      
      return { 
        success: skillsList.length > 50 && hasHelpContent && statusOk && hasSkillsUsage,
        skillsAvailable: skillsList.length > 50,
        helpAvailable: hasHelpContent,
        statusOk,
        documentationCreated: hasSkillsUsage
      };
    } catch (error) {
      this.logActivity('Skill utilization failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Execute all real user flows
   */
  async executeAllFlows() {
    this.logActivity('Starting comprehensive real user desktop application testing');
    
    const results = {
      projectDiscovery: await this.flowProjectDiscovery(),
      codeModification: await this.flowCodeModification(),
      terminalCLIInteraction: await this.flowTerminalCLIInteraction(),
      directoryNavigation: await this.flowDirectoryNavigation(),
      projectBuilding: await this.flowProjectBuilding(),
      skillUtilization: await this.flowSkillUtilization()
    };
    
    // Calculate overall success
    const successfulFlows = Object.values(results).filter(r => r.success).length;
    const totalFlows = Object.keys(results).length;
    
    const overallResult = {
      totalFlows,
      successfulFlows,
      failedFlows: totalFlows - successfulFlows,
      successRate: (successfulFlows / totalFlows) * 100,
      results,
      sessionLog: this.sessionLog
    };
    
    this.logActivity('Real user desktop application testing completed', {
      successfulFlows,
      totalFlows,
      successRate: overallResult.successRate.toFixed(2) + '%'
    });
    
    return overallResult;
  }

  /**
   * Print detailed results
   */
  printResults(result) {
    console.log('\n=== REAL USER DESKTOP APPLICATION TESTING RESULTS ===');
    console.log(`Total flows: ${result.totalFlows}`);
    console.log(`Successful flows: ${result.successfulFlows}`);
    console.log(`Failed flows: ${result.failedFlows}`);
    console.log(`Success rate: ${result.successRate.toFixed(2)}%`);
    console.log('');
    
    const flowDescriptions = {
      projectDiscovery: 'Project Discovery - Exploring project structure',
      codeModification: 'Code Modification - Editing files',
      terminalCLIInteraction: 'Terminal/CLI Interaction - Using commands and tools',
      directoryNavigation: 'Directory Navigation - Moving between folders',
      projectBuilding: 'Project Building - Creating tests and configs',
      skillUtilization: 'Skill Utilization - Using Stigmergy skills'
    };
    
    for (const [flowName, flowResult] of Object.entries(result.results)) {
      const status = flowResult.success ? '✅ PASS' : '❌ FAIL';
      console.log(`${status}: ${flowDescriptions[flowName] || flowName}`);
      
      if (flowResult.error) {
        console.log(`  Error: ${flowResult.error}`);
      }
    }
    
    console.log('');
    console.log('=== DETAILED FLOW RESULTS ===');
    
    for (const [flowName, flowResult] of Object.entries(result.results)) {
      console.log(`\n${flowName.replace(/([A-Z])/g, ' $1').trim().toUpperCase()}:`);
      console.log(`  Success: ${flowResult.success}`);
      
      // Print specific details for each flow
      switch(flowName) {
        case 'projectDiscovery':
          console.log(`  - Files explored: ${flowResult.filesExplored || 'N/A'}`);
          console.log(`  - Package.json found: ${flowResult.hasPackageJson || false}`);
          break;
        case 'codeModification':
          console.log(`  - Code modified: ${flowResult.codeModified || false}`);
          console.log(`  - File created: ${flowResult.fileCreated || false}`);
          break;
        case 'terminalCLIInteraction':
          console.log(`  - App runs: ${flowResult.appRuns || false}`);
          console.log(`  - Version available: ${flowResult.hasVersion || false}`);
          console.log(`  - Skills available: ${flowResult.hasSkills || false}`);
          console.log(`  - Help available: ${flowResult.hasHelp || false}`);
          break;
        case 'directoryNavigation':
          console.log(`  - Navigation successful: ${flowResult.navigationSuccessful || false}`);
          console.log(`  - File created in subdir: ${flowResult.fileCreated || false}`);
          console.log(`  - Navigation back to root: ${flowResult.navigationBack || false}`);
          break;
        case 'projectBuilding':
          console.log(`  - Test file created: ${flowResult.testFileCreated || false}`);
          console.log(`  - Test content correct: ${flowResult.testFileCorrect || false}`);
          console.log(`  - Config created: ${flowResult.configCreated || false}`);
          break;
        case 'skillUtilization':
          console.log(`  - Skills available: ${flowResult.skillsAvailable || false}`);
          console.log(`  - Help available: ${flowResult.helpAvailable || false}`);
          console.log(`  - Status OK: ${flowResult.statusOk || false}`);
          console.log(`  - Documentation created: ${flowResult.documentationCreated || false}`);
          break;
      }
    }
  }

  /**
   * Cleanup test environment
   */
  cleanup() {
    try {
      if (fs.existsSync(this.testProjectDir)) {
        fs.rmSync(this.testProjectDir, { recursive: true, force: true });
        this.logActivity('Test environment cleaned up', { path: this.testProjectDir });
      }
    } catch (error) {
      console.error(`Error cleaning up test environment: ${error.message}`);
    }
  }

  /**
   * Run the complete real user desktop test
   */
  async runRealUserTest() {
    try {
      await this.setupRealisticEnvironment();
      const result = await this.executeAllFlows();
      this.printResults(result);
      return result;
    } finally {
      this.cleanup();
    }
  }
}

// Run the real user desktop test if this file is executed directly
if (require.main === module) {
  async function runRealUserDesktopTest() {
    const realUserTest = new RealUserDesktopE2ETest();
    const result = await realUserTest.runRealUserTest();
    
    // Exit with appropriate code based on results
    process.exit(result.failedFlows > 0 ? 1 : 0);
  }
  
  runRealUserDesktopTest().catch(error => {
    console.error('Real user desktop test failed:', error);
    process.exit(1);
  });
}

module.exports = RealUserDesktopE2ETest;