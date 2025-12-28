// Systematic Walkthrough of User Interaction Flows
// This test simulates a complete user session with the desktop application

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

class UserInteractionWalkthrough {
  constructor() {
    this.testResults = [];
    this.testProjectDir = path.join(os.tmpdir(), 'stigmergy-walkthrough-test');
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
   * Setup test environment
   */
  async setupTestEnvironment() {
    this.logActivity('Setting up test environment');
    
    // Create test project directory
    if (!fs.existsSync(this.testProjectDir)) {
      fs.mkdirSync(this.testProjectDir, { recursive: true });
    }
    
    // Create some initial files
    fs.writeFileSync(path.join(this.testProjectDir, 'README.md'), '# Test Project\n\nThis is a test project.');
    fs.writeFileSync(path.join(this.testProjectDir, 'package.json'), JSON.stringify({
      name: 'test-project',
      version: '1.0.0',
      description: 'Test project for walkthrough'
    }, null, 2));
    
    // Create a subdirectory with files
    const srcDir = path.join(this.testProjectDir, 'src');
    if (!fs.existsSync(srcDir)) {
      fs.mkdirSync(srcDir, { recursive: true });
    }
    fs.writeFileSync(path.join(srcDir, 'index.js'), '// Main application file\nconsole.log("Hello, World!");');
    
    this.logActivity('Test environment created', { path: this.testProjectDir });
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
   * Flow 1: Initialize a new project
   */
  async flowInitializeProject() {
    this.logActivity('Starting flow: Initialize a new project');
    
    try {
      // Create a new project directory
      const newProjectDir = path.join(this.testProjectDir, 'new-project');
      fs.mkdirSync(newProjectDir, { recursive: true });
      
      // Initialize with basic files
      fs.writeFileSync(path.join(newProjectDir, 'main.py'), '# New Python project\nprint("Hello from new project!")');
      fs.writeFileSync(path.join(newProjectDir, 'requirements.txt'), '# Dependencies\n');
      
      this.logActivity('Project initialized successfully');
      
      return { success: true, projectPath: newProjectDir };
    } catch (error) {
      this.logActivity('Project initialization failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Flow 2: Use CLI tools for various operations
   */
  async flowUseCLITools() {
    this.logActivity('Starting flow: Use CLI tools for various operations');
    
    try {
      // Test stigmergy commands
      const versionResult = await this.executeCommand('stigmergy --version');
      this.logActivity('Checked stigmergy version', { version: versionResult.stdout.trim() });
      
      const statusResult = await this.executeCommand('stigmergy status');
      this.logActivity('Checked stigmergy status', { exitCode: statusResult.exitCode });
      
      const skillsResult = await this.executeCommand('stigmergy skill list');
      this.logActivity('Listed available skills', { skillsCount: skillsResult.stdout.split('\n').length });
      
      return { 
        success: versionResult.exitCode === 0 && statusResult.exitCode === 0,
        version: versionResult.stdout.trim(),
        skillsCount: skillsResult.stdout.split('\n').length
      };
    } catch (error) {
      this.logActivity('CLI tools flow failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Flow 3: Terminal interaction and file operations
   */
  async flowTerminalInteraction() {
    this.logActivity('Starting flow: Terminal interaction and file operations');
    
    try {
      // Create a new file using terminal commands
      const touchResult = await this.executeCommand(os.platform() === 'win32' ? 'echo. > terminal_test.txt' : 'touch terminal_test.txt');
      
      // List files to verify creation
      const lsCommand = os.platform() === 'win32' ? 'dir' : 'ls -la';
      const lsResult = await this.executeCommand(lsCommand);
      const fileCreated = lsResult.stdout.includes('terminal_test.txt');
      
      this.logActivity('File created via terminal', { fileCreated, commandExitCode: touchResult.exitCode });
      
      // On Windows, use PowerShell for more reliable content writing
      let writeResult;
      if (os.platform() === 'win32') {
        // Use PowerShell to write content more reliably
        const psCommand = `powershell -Command "Set-Content -Path terminal_test.txt -Value 'Hello from terminal!'"`
        writeResult = await this.executeCommand(psCommand);
      } else {
        // On Unix systems, use echo
        const writeCommand = 'echo "Hello from terminal!" > terminal_test.txt';
        writeResult = await this.executeCommand(writeCommand);
      }
      
      // Read the file content
      const readCommand = os.platform() === 'win32' ? 'type terminal_test.txt' : 'cat terminal_test.txt';
      const readResult = await this.executeCommand(readCommand);
      // Normalize content for comparison (remove Windows carriage returns, trim whitespace)
      const normalizedContent = readResult.stdout.replace(/\r/g, '').trim();
      const contentCorrect = normalizedContent === 'Hello from terminal!';
      
      this.logActivity('File content verified', { contentCorrect, content: readResult.stdout.trim() });
      
      return { 
        success: touchResult.exitCode === 0 && writeResult.exitCode === 0 && contentCorrect,
        fileCreated,
        contentCorrect
      };
    } catch (error) {
      this.logActivity('Terminal interaction flow failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Flow 4: File manager synchronization
   */
  async flowFileManagerSync() {
    this.logActivity('Starting flow: File manager synchronization');
    
    try {
      // Create a directory structure
      const syncDir = path.join(this.testProjectDir, 'sync-test');
      fs.mkdirSync(syncDir, { recursive: true });
      
      // Create files in the directory
      fs.writeFileSync(path.join(syncDir, 'sync-file1.txt'), 'Content 1');
      fs.writeFileSync(path.join(syncDir, 'sync-file2.js'), 'console.log("Sync test");');
      
      // Verify through terminal commands
      const lsCommand = os.platform() === 'win32' ? 'dir /s' : 'find . -name "sync*"';
      const lsResult = await this.executeCommand(lsCommand, syncDir);
      
      const hasFile1 = lsResult.stdout.includes('sync-file1.txt');
      const hasFile2 = lsResult.stdout.includes('sync-file2.js') || lsResult.stdout.includes('sync-file2');
      
      this.logActivity('File manager sync verified', { hasFile1, hasFile2 });
      
      return { 
        success: hasFile1 && hasFile2,
        hasFile1,
        hasFile2
      };
    } catch (error) {
      this.logActivity('File manager sync flow failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Flow 5: Skill management and usage
   */
  async flowSkillManagement() {
    this.logActivity('Starting flow: Skill management and usage');
    
    try {
      // List available skills
      const skillsResult = await this.executeCommand('stigmergy skill list');
      
      // Check if specific skills are available (looking for common ones)
      const hasSkillManagement = skillsResult.stdout.toLowerCase().includes('skill') || 
                                skillsResult.stdout.toLowerCase().includes('list');
      
      this.logActivity('Skill management verified', { hasSkillManagement, skillsOutputLength: skillsResult.stdout.length });
      
      // Try to get help with a skill (if available)
      try {
        const helpResult = await this.executeCommand('stigmergy help');
        this.logActivity('Help command executed', { exitCode: helpResult.exitCode });
      } catch (helpError) {
        this.logActivity('Help command failed (this is OK)', { error: helpError.message });
      }
      
      return { 
        success: skillsResult.exitCode === 0,
        skillsAvailable: hasSkillManagement
      };
    } catch (error) {
      this.logActivity('Skill management flow failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Flow 6: Project navigation and path management
   */
  async flowProjectNavigation() {
    this.logActivity('Starting flow: Project navigation and path management');
    
    try {
      // Test navigation to different directories
      const initialDir = await this.executeCommand(os.platform() === 'win32' ? 'cd' : 'pwd');
      this.logActivity('Initial directory', { path: initialDir.stdout.trim() });
      
      // Navigate to subdirectory
      const srcDir = path.join(this.testProjectDir, 'src');
      const lsInSrc = await this.executeCommand(os.platform() === 'win32' ? 'dir' : 'ls -la', srcDir);
      
      const hasIndexFile = lsInSrc.stdout.includes('index.js');
      this.logActivity('Navigation to subdirectory successful', { hasIndexFile, path: srcDir });
      
      // Test creating a file in subdirectory
      const touchInSubdirCommand = os.platform() === 'win32' ? 'echo. > subfile.txt' : 'touch subfile.txt';
      const touchResult = await this.executeCommand(touchInSubdirCommand, srcDir);
      
      // Verify file exists
      const lsAfterTouch = await this.executeCommand(os.platform() === 'win32' ? 'dir' : 'ls -la', srcDir);
      const fileExists = lsAfterTouch.stdout.includes('subfile.txt');
      
      this.logActivity('File created in subdirectory', { fileExists });
      
      return { 
        success: lsInSrc.exitCode === 0 && touchResult.exitCode === 0 && fileExists,
        navigationSuccessful: hasIndexFile,
        fileCreated: fileExists
      };
    } catch (error) {
      this.logActivity('Project navigation flow failed', { error: error.message });
      return { success: false, error: error.message };
    }
  }

  /**
   * Execute all user interaction flows
   */
  async executeAllFlows() {
    this.logActivity('Starting systematic walkthrough of all user interaction flows');
    
    // Execute each flow and collect results
    const results = {
      initializeProject: await this.flowInitializeProject(),
      cliTools: await this.flowUseCLITools(),
      terminalInteraction: await this.flowTerminalInteraction(),
      fileManagerSync: await this.flowFileManagerSync(),
      skillManagement: await this.flowSkillManagement(),
      projectNavigation: await this.flowProjectNavigation()
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
    
    this.logActivity('Walkthrough completed', {
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
    console.log('\n=== Systematic Walkthrough Results ===');
    console.log(`Total flows: ${result.totalFlows}`);
    console.log(`Successful flows: ${result.successfulFlows}`);
    console.log(`Failed flows: ${result.failedFlows}`);
    console.log(`Success rate: ${result.successRate.toFixed(2)}%`);
    console.log('');
    
    for (const [flowName, flowResult] of Object.entries(result.results)) {
      const status = flowResult.success ? '✓ PASS' : '✗ FAIL';
      console.log(`${status}: ${flowName.replace(/([A-Z])/g, ' $1').trim()}`);
      
      if (flowResult.error) {
        console.log(`  Error: ${flowResult.error}`);
      }
      
      // Print specific details for each flow
      switch(flowName) {
        case 'cliTools':
          console.log(`  Stigmergy version: ${flowResult.version || 'N/A'}`);
          console.log(`  Skills available: ${flowResult.skillsCount || 'N/A'}`);
          break;
        case 'terminalInteraction':
          console.log(`  File created: ${flowResult.fileCreated || false}`);
          console.log(`  Content correct: ${flowResult.contentCorrect || false}`);
          break;
        case 'fileManagerSync':
          console.log(`  File 1 exists: ${flowResult.hasFile1 || false}`);
          console.log(`  File 2 exists: ${flowResult.hasFile2 || false}`);
          break;
        case 'skillManagement':
          console.log(`  Skills available: ${flowResult.skillsAvailable || false}`);
          break;
        case 'projectNavigation':
          console.log(`  Navigation successful: ${flowResult.navigationSuccessful || false}`);
          console.log(`  File created: ${flowResult.fileCreated || false}`);
          break;
      }
      console.log('');
    }
    
    console.log('=== Session Log ===');
    for (const logEntry of this.sessionLog.slice(-10)) { // Show last 10 entries
      console.log(`${logEntry.timestamp.toISOString()} - ${logEntry.activity}`);
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
   * Run the complete walkthrough
   */
  async runWalkthrough() {
    try {
      await this.setupTestEnvironment();
      const result = await this.executeAllFlows();
      this.printResults(result);
      return result;
    } finally {
      this.cleanup();
    }
  }
}

// Run the walkthrough if this file is executed directly
if (require.main === module) {
  async function runWalkthrough() {
    const walkthrough = new UserInteractionWalkthrough();
    const result = await walkthrough.runWalkthrough();
    
    // Exit with appropriate code based on results
    process.exit(result.failedFlows > 0 ? 1 : 0);
  }
  
  runWalkthrough().catch(error => {
    console.error('Walkthrough execution failed:', error);
    process.exit(1);
  });
}

module.exports = UserInteractionWalkthrough;