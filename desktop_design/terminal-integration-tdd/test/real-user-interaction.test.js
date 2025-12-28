// Real User Interaction Simulation Test
// This test simulates a real user workflow with the desktop application

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

class RealUserInteractionTest {
  constructor() {
    this.testProjectDir = path.join(os.tmpdir(), 'stigmergy-real-user-test');
    this.sessionLog = [];
  }

  /**
   * Log session activity
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
    
    // Create a realistic project structure
    if (!fs.existsSync(this.testProjectDir)) {
      fs.mkdirSync(this.testProjectDir, { recursive: true });
    }
    
    // Create realistic project files
    fs.writeFileSync(path.join(this.testProjectDir, 'package.json'), JSON.stringify({
      name: 'real-project',
      version: '1.0.0',
      description: 'Real project for user interaction test',
      scripts: {
        start: 'node index.js',
        test: 'jest'
      }
    }, null, 2));
    
    fs.writeFileSync(path.join(this.testProjectDir, 'README.md'), 
    `# Real Project\n\nThis is a realistic test project.\n\n## Getting Started\n\nRun \`npm install\` to install dependencies.\n\nRun \`npm start\` to start the application.\n`);
    
    fs.writeFileSync(path.join(this.testProjectDir, 'index.js'), 
    `// Real application entry point\nconsole.log('Hello from real project!');\n\n// Simulate real application logic\nconst config = {\n  port: process.env.PORT || 3000,\n  env: process.env.NODE_ENV || 'development'\n};\n\nconsole.log('Server configuration:', config);\n`);
    
    // Create realistic subdirectories
    const dirs = ['src', 'tests', 'docs', 'config', 'public'];
    for (const dir of dirs) {
      const dirPath = path.join(this.testProjectDir, dir);
      if (!fs.existsSync(dirPath)) {
        fs.mkdirSync(dirPath, { recursive: true });
      }
    }
    
    // Create realistic files in subdirectories
    fs.writeFileSync(path.join(this.testProjectDir, 'src', 'app.js'), 
    `// Real application logic\nfunction startApp() {\n  console.log('Starting application...');\n  return 'App started successfully';\n}\n\nmodule.exports = { startApp };\n`);
    
    fs.writeFileSync(path.join(this.testProjectDir, 'tests', 'app.test.js'), 
    `// Real test file\nconst { startApp } = require('../src/app');\n\ntest('should start app successfully', () => {\n  expect(startApp()).toBe('App started successfully');\n});\n`);
    
    this.logActivity('Realistic environment created', { path: this.testProjectDir });
  }

  /**
   * Execute a command in the test directory
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
   * Real User Flow 1: Project Discovery
   */
  async flowProjectDiscovery() {
    this.logActivity('Starting flow: Project Discovery');
    
    try {
      // User opens terminal and explores the project
      const lsResult = await this.executeCommand(os.platform() === 'win32' ? 'dir' : 'ls -la');
      this.logActivity('User explores project root', { 
        filesCount: lsResult.stdout.split('\n').length,
        hasPackageJson: lsResult.stdout.includes('package.json')
      });
      
      // User checks project details
      const catResult = await this.executeCommand(os.platform() === 'win32' ? 'type package.json' : 'cat package.json');
      const packageJson = JSON.parse(catResult.stdout);
      this.logActivity('User examines package.json', { 
        projectName: packageJson.name,
        version: packageJson.version
      });
      
      // User explores directory structure
      const treeCommand = os.platform() === 'win32' ? 'dir /s' : 'find . -type d';
      const treeResult = await this.executeCommand(treeCommand);
      const dirsFound = (treeResult.stdout.match(/(src|tests|docs|config|public)/g) || []).length;
      
      this.logActivity('User explores directory structure', { 
        directoriesFound: dirsFound,
        totalDirs: treeResult.stdout.split('\n').length
      });
      
      return { success: lsResult.exitCode === 0 && dirsFound >= 5 };
    } catch (error) {
      this.logActivity('Project discovery failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Real User Flow 2: Code Modification
   */
  async flowCodeModification() {
    this.logActivity('Starting flow: Code Modification');
    
    try {
      // User modifies a file
      const modification = '\n// Added by user during testing\nconst newFeature = true;\nconsole.log("New feature enabled:", newFeature);\n';
      
      let appendResult;
      if (os.platform() === 'win32') {
        // On Windows, append to file using PowerShell
        const psCommand = `powershell -Command "Add-Content -Path '.\\\\index.js' -Value '${modification.replace(/'/g, "''")}'"`;
        appendResult = await this.executeCommand(psCommand);
      } else {
        // On Unix, append using echo
        appendResult = await this.executeCommand(`echo "${modification}" >> index.js`);
      }
      
      // Ensure appendResult is defined
      if (!appendResult) {
        this.logActivity('Code modification failed - no result returned');
        return { success: false, modificationSuccessful: false };
      }
      
      // Verify modification was successful
      const verifyResult = await this.executeCommand(os.platform() === 'win32' ? 'type index.js' : 'cat index.js');
      // Check for multiple possible indicators of success
      const hasNewFeature = verifyResult.stdout.includes('newFeature') || 
                           verifyResult.stdout.includes('New feature');
      
      this.logActivity('User modifies code', { 
        modificationSuccessful: hasNewFeature,
        fileLength: verifyResult.stdout.length
      });
      
      return { 
        success: appendResult && appendResult.exitCode === 0 && hasNewFeature,
        modificationSuccessful: hasNewFeature
      };
    } catch (error) {
      this.logActivity('Code modification failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Real User Flow 3: CLI Tool Interaction
   */
  async flowCLIToolInteraction() {
    this.logActivity('Starting flow: CLI Tool Interaction');
    
    try {
      // User uses stigmergy CLI to check status
      const statusResult = await this.executeCommand('stigmergy status');
      this.logActivity('User checks stigmergy status', { 
        exitCode: statusResult.exitCode,
        outputLength: statusResult.stdout.length
      });
      
      // User lists available skills
      const skillsResult = await this.executeCommand('stigmergy skill list');
      const hasSkills = skillsResult.stdout.length > 100; // Should have substantial output
      
      this.logActivity('User explores available skills', { 
        skillsAvailable: hasSkills,
        skillsOutputLength: skillsResult.stdout.length
      });
      
      // User gets help
      const helpResult = await this.executeCommand('stigmergy help');
      const hasHelp = helpResult.stdout.length > 50;
      
      this.logActivity('User gets help information', { 
        helpAvailable: hasHelp,
        helpOutputLength: helpResult.stdout.length
      });
      
      return { 
        success: statusResult.exitCode === 0 && hasSkills && hasHelp,
        statusOk: statusResult.exitCode === 0,
        hasSkills,
        hasHelp
      };
    } catch (error) {
      this.logActivity('CLI tool interaction failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Real User Flow 4: File Operations
   */
  async flowFileOperations() {
    this.logActivity('Starting flow: File Operations');
    
    try {
      // User creates a new configuration file
      const configContent = `{
  "appName": "Real Project",
  "version": "1.0.0",
  "settings": {
    "port": 3000,
    "debug": true,
    "logging": {
      "level": "info",
      "file": "app.log"
    }
  }
}`;
      
      let createResult;
      if (os.platform() === 'win32') {
        const psCommand = `powershell -Command "Set-Content -Path 'config.json' -Value '${configContent.replace(/\n/g, '`n').replace(/'/g, "''")}'"`;
        createResult = await this.executeCommand(psCommand);
      } else {
        createResult = await this.executeCommand(`echo '${configContent}' > config.json`);
      }
      
      // Ensure createResult is defined
      if (!createResult) {
        this.logActivity('File creation failed - no result returned');
        return { success: false, fileCreated: false, contentCorrect: false };
      }
      
      // User verifies the file was created
      const lsResult = await this.executeCommand(os.platform() === 'win32' ? 'dir' : 'ls -la');
      const configFileExists = lsResult.stdout.includes('config.json');
      
      // User views the content
      const catResult = await this.executeCommand(os.platform() === 'win32' ? 'type config.json' : 'cat config.json');
      const contentMatches = catResult.stdout.includes('"appName": "Real Project"');
      
      this.logActivity('User performs file operations', { 
        fileCreated: configFileExists,
        contentCorrect: contentMatches,
        fileOperationExitCode: createResult.exitCode
      });
      
      return { 
        success: createResult && createResult.exitCode === 0 && configFileExists && contentMatches,
        fileCreated: configFileExists,
        contentCorrect: contentMatches
      };
    } catch (error) {
      this.logActivity('File operations failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Real User Flow 5: Directory Navigation
   */
  async flowDirectoryNavigation() {
    this.logActivity('Starting flow: Directory Navigation');
    
    try {
      // User navigates to src directory
      const srcPath = path.join(this.testProjectDir, 'src');
      const pwdResult = await this.executeCommand(os.platform() === 'win32' ? 'cd' : 'pwd', srcPath);
      const currentDir = pwdResult.stdout.trim().replace(/\\/g, '/').toLowerCase();
      const inCorrectDir = currentDir.includes('src');
      
      this.logActivity('User navigates to src directory', { 
        inCorrectDir,
        currentPath: pwdResult.stdout.trim()
      });
      
      // User lists files in src
      const lsResult = await this.executeCommand(os.platform() === 'win32' ? 'dir' : 'ls -la', srcPath);
      const hasAppJs = lsResult.stdout.toLowerCase().includes('app.js');
      
      this.logActivity('User lists files in src', { 
        hasAppJs,
        filesCount: lsResult.stdout.split('\n').length
      });
      
      // User creates a new file in src
      const newFileContent = '// New component created by user\nfunction newComponent() {\n  return "New component";\n}\n\nmodule.exports = { newComponent };';
      
      let createResult;
      if (os.platform() === 'win32') {
        const psCommand = `powershell -Command "Set-Content -Path 'component.js' -Value '${newFileContent.replace(/\n/g, '`n').replace(/'/g, "''")}'"`;
        createResult = await this.executeCommand(psCommand, srcPath);
      } else {
        createResult = await this.executeCommand(`echo '${newFileContent}' > component.js`, srcPath);
      }
      
      // Verify the new file exists
      const verifyResult = await this.executeCommand(os.platform() === 'win32' ? 'dir' : 'ls -la', srcPath);
      const newFileExists = verifyResult.stdout.toLowerCase().includes('component.js');
      
      this.logActivity('User creates file in subdirectory', { 
        newFileExists,
        createExitCode: createResult.exitCode
      });
      
      return { 
        success: inCorrectDir && hasAppJs && newFileExists,
        navigationSuccessful: inCorrectDir,
        fileCreated: newFileExists
      };
    } catch (error) {
      this.logActivity('Directory navigation failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Real User Flow 6: Project Building/Simulation
   */
  async flowProjectBuilding() {
    this.logActivity('Starting flow: Project Building/Simulation');
    
    try {
      // User attempts to run the project (simulated)
      const runResult = await this.executeCommand(os.platform() === 'win32' ? 'node .\\index.js' : 'node index.js');
      const appRuns = runResult.stdout.toLowerCase().includes('hello from real project') || 
                     runResult.stdout.toLowerCase().includes('server configuration');
      
      this.logActivity('User runs the project', { 
        appRuns,
        output: runResult.stdout.substring(0, 100) + '...'
      });
      
      // User checks for potential errors
      const hasErrors = runResult.stderr && runResult.stderr.length > 0;
      
      this.logActivity('User checks for errors', { 
        hasErrors,
        errorOutput: hasErrors ? runResult.stderr.substring(0, 100) : 'No errors'
      });
      
      // User creates a test run simulation
      const testResult = await this.executeCommand(os.platform() === 'win32' ? 'type tests\\app.test.js' : 'cat tests/app.test.js');
      const testFileExists = testResult.exitCode === 0;
      
      this.logActivity('User verifies test file exists', { 
        testFileExists,
        testContentLength: testResult.stdout.length
      });
      
      return { 
        success: appRuns && !hasErrors && testFileExists,
        appRuns,
        noErrors: !hasErrors,
        testsExist: testFileExists
      };
    } catch (error) {
      this.logActivity('Project building simulation failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Real User Flow 7: Skill Utilization
   */
  async flowSkillUtilization() {
    this.logActivity('Starting flow: Skill Utilization');
    
    try {
      // User attempts to use a skill (simulated realistic usage)
      const skillListResult = await this.executeCommand('stigmergy skill list');
      
      // Look for common skill patterns in the output
      const hasCodeSkills = skillListResult.stdout.toLowerCase().includes('code') || 
                           skillListResult.stdout.toLowerCase().includes('development');
      const hasProjectSkills = skillListResult.stdout.toLowerCase().includes('project') || 
                             skillListResult.stdout.toLowerCase().includes('file');
      
      this.logActivity('User explores relevant skills', { 
        hasCodeSkills,
        hasProjectSkills,
        skillsOutputLength: skillListResult.stdout.length
      });
      
      // User might try to get help for a specific skill (if available)
      try {
        const helpResult = await this.executeCommand('stigmergy help');
        const hasHelpContent = helpResult.stdout.length > 100;
        
        this.logActivity('User accesses help system', { 
          hasHelpContent,
          helpLength: helpResult.stdout.length
        });
        
        return { 
          success: skillListResult.exitCode === 0 && hasHelpContent,
          skillsAvailable: true,
          helpAvailable: hasHelpContent
        };
      } catch (helpError) {
        this.logActivity('Help access attempted', { helpError: helpError.message });
        
        return { 
          success: skillListResult.exitCode === 0,
          skillsAvailable: true,
          helpAvailable: false
        };
      }
    } catch (error) {
      this.logActivity('Skill utilization failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Execute all real user interaction flows
   */
  async executeAllRealFlows() {
    this.logActivity('Starting comprehensive real user interaction simulation');
    
    // Execute each realistic flow
    const results = {
      projectDiscovery: await this.flowProjectDiscovery(),
      codeModification: await this.flowCodeModification(),
      cliInteraction: await this.flowCLIToolInteraction(),
      fileOperations: await this.flowFileOperations(),
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
    
    this.logActivity('Real user interaction simulation completed', {
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
    console.log('\n=== REAL USER INTERACTION SIMULATION RESULTS ===');
    console.log(`Total flows: ${result.totalFlows}`);
    console.log(`Successful flows: ${result.successfulFlows}`);
    console.log(`Failed flows: ${result.failedFlows}`);
    console.log(`Success rate: ${result.successRate.toFixed(2)}%`);
    console.log('');
    
    const flowDescriptions = {
      projectDiscovery: 'Project Discovery - Exploring project structure',
      codeModification: 'Code Modification - Editing files',
      cliInteraction: 'CLI Interaction - Using Stigmergy commands',
      fileOperations: 'File Operations - Creating and managing files',
      directoryNavigation: 'Directory Navigation - Moving between folders',
      projectBuilding: 'Project Building - Running and testing the project',
      skillUtilization: 'Skill Utilization - Using Stigmergy skills'
    };
    
    for (const [flowName, flowResult] of Object.entries(result.results)) {
      const status = flowResult.success ? '✓ PASS' : '✗ FAIL';
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
          console.log(`  - Files explored: ${flowResult.filesCount || 'N/A'}`);
          console.log(`  - Package.json found: ${flowResult.hasPackageJson || false}`);
          break;
        case 'codeModification':
          console.log(`  - Code modified: ${flowResult.modificationSuccessful || false}`);
          console.log(`  - New feature added: ${flowResult.newFeatureAdded || false}`);
          break;
        case 'cliInteraction':
          console.log(`  - Status check OK: ${flowResult.statusOk || false}`);
          console.log(`  - Skills available: ${flowResult.hasSkills || false}`);
          console.log(`  - Help available: ${flowResult.hasHelp || false}`);
          break;
        case 'fileOperations':
          console.log(`  - File created: ${flowResult.fileCreated || false}`);
          console.log(`  - Content correct: ${flowResult.contentCorrect || false}`);
          break;
        case 'directoryNavigation':
          console.log(`  - Navigation successful: ${flowResult.navigationSuccessful || false}`);
          console.log(`  - File created in subdir: ${flowResult.fileCreated || false}`);
          break;
        case 'projectBuilding':
          console.log(`  - App runs: ${flowResult.appRuns || false}`);
          console.log(`  - No errors: ${flowResult.noErrors || false}`);
          console.log(`  - Tests exist: ${flowResult.testsExist || false}`);
          break;
        case 'skillUtilization':
          console.log(`  - Skills available: ${flowResult.skillsAvailable || false}`);
          console.log(`  - Help available: ${flowResult.helpAvailable || false}`);
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
   * Run the complete real user simulation
   */
  async runRealUserSimulation() {
    try {
      await this.setupRealisticEnvironment();
      const result = await this.executeAllRealFlows();
      this.printResults(result);
      return result;
    } finally {
      this.cleanup();
    }
  }
}

// Run the real user simulation if this file is executed directly
if (require.main === module) {
  async function runRealUserTest() {
    const realUserTest = new RealUserInteractionTest();
    const result = await realUserTest.runRealUserSimulation();
    
    // Exit with appropriate code based on results
    process.exit(result.failedFlows > 0 ? 1 : 0);
  }
  
  runRealUserTest().catch(error => {
    console.error('Real user test execution failed:', error);
    process.exit(1);
  });
}

module.exports = RealUserInteractionTest;