// Terminal Simulation and File Manager Synchronization Test
// This test validates the integration between terminal simulation and file manager synchronization

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

class TerminalSyncTester {
  constructor() {
    this.testResults = [];
    this.testDirectory = path.join(os.tmpdir(), 'stigmergy-terminal-test');
  }

  /**
   * Setup test environment
   */
  async setupTestEnvironment() {
    // Create test directory
    if (!fs.existsSync(this.testDirectory)) {
      fs.mkdirSync(this.testDirectory, { recursive: true });
    }
    
    // Create some test files
    const testFiles = ['file1.txt', 'file2.js', 'file3.py'];
    for (const file of testFiles) {
      const filePath = path.join(this.testDirectory, file);
      fs.writeFileSync(filePath, `Test content for ${file}`);
    }
    
    // Create a subdirectory
    const subDir = path.join(this.testDirectory, 'subdir');
    if (!fs.existsSync(subDir)) {
      fs.mkdirSync(subDir, { recursive: true });
    }
    
    console.log(`Test environment created at: ${this.testDirectory}`);
  }

  /**
   * Execute a command in the test directory
   */
  async executeInDirectory(command, directory = this.testDirectory) {
    return new Promise((resolve, reject) => {
      const [cmd, ...args] = command.split(' ');
      
      const child = spawn(cmd, args, {
        cwd: directory,
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
          cwd: directory
        });
      });

      child.on('error', (error) => {
        reject(error);
      });
    });
  }

  /**
   * Test terminal simulation with various commands
   */
  async testTerminalSimulation() {
    console.log('Testing terminal simulation...\n');
    
    const tests = [
      { name: 'Directory listing', command: 'ls -la', expected: true },
      { name: 'Current directory', command: 'pwd', expected: true },
      { name: 'File listing', command: 'ls -F', expected: true },
      { name: 'Create file', command: 'touch test_file.txt', expected: true },
      { name: 'Remove file', command: 'rm test_file.txt', expected: true }
    ];
    
    for (const test of tests) {
      try {
        console.log(`Testing: ${test.name} (${test.command})`);
        const result = await this.executeInDirectory(test.command);
        
        const isValid = result.exitCode === 0 && test.expected;
        
        this.testResults.push({
          testName: test.name,
          command: test.command,
          result,
          isValid,
          type: 'terminal-simulation'
        });
        
        console.log(`✓ ${test.name} - Exit code: ${result.exitCode}`);
        console.log(`  Output length: ${result.stdout.length} chars`);
        console.log('');
        
      } catch (error) {
        console.log(`✗ ${test.name} - Error: ${error.message}`);
        console.log('');
        
        this.testResults.push({
          testName: test.name,
          command: test.command,
          error: error.message,
          isValid: false,
          type: 'terminal-simulation'
        });
      }
    }
  }

  /**
   * Test file manager synchronization
   */
  async testFileManagerSync() {
    console.log('Testing file manager synchronization...\n');
    
    // Test 1: Verify directory contents match expectations
    try {
      console.log('Testing directory content synchronization...');
      const lsResult = await this.executeInDirectory('ls -la');
      
      // Check if our test files are present
      const hasExpectedFiles = ['file1.txt', 'file2.js', 'file3.py', 'subdir'].every(file => 
        lsResult.stdout.includes(file)
      );
      
      this.testResults.push({
        testName: 'Directory content sync',
        command: 'ls -la',
        result: lsResult,
        isValid: hasExpectedFiles,
        type: 'file-manager-sync'
      });
      
      console.log(`✓ Directory content sync: ${hasExpectedFiles ? 'PASS' : 'FAIL'}`);
      console.log('');
      
    } catch (error) {
      console.log(`✗ Directory content sync - Error: ${error.message}`);
      console.log('');
      
      this.testResults.push({
        testName: 'Directory content sync',
        command: 'ls -la',
        error: error.message,
        isValid: false,
        type: 'file-manager-sync'
      });
    }
    
    // Test 2: Test path changes and synchronization
    try {
      console.log('Testing path change synchronization...');
      const subdirPath = path.join(this.testDirectory, 'subdir');
      
      // Change to subdirectory and list contents
      // Use platform-appropriate command for current directory
      const pwdCommand = os.platform() === 'win32' ? 'cd' : 'pwd';
      const pwdResult = await this.executeInDirectory(pwdCommand, subdirPath);
      const lsResult = await this.executeInDirectory('ls -la', subdirPath);
      
      // Normalize paths for comparison (handle Windows vs Unix path separators)
      const outputDir = pwdResult.stdout.trim().replace(/\\/g, '/').replace(/[\r\n]/g, '').toLowerCase();
      const normalizedSubdirPath = subdirPath.replace(/\\/g, '/').toLowerCase();
      const correctPath = outputDir.endsWith(normalizedSubdirPath.split('/').pop()) || 
                         outputDir.includes(normalizedSubdirPath);
      const isValid = correctPath;
      
      this.testResults.push({
        testName: 'Path change sync',
        command: 'pwd in subdir',
        result: { pwd: pwdResult, ls: lsResult },
        isValid,
        type: 'file-manager-sync'
      });
      
      console.log(`✓ Path change sync: ${isValid ? 'PASS' : 'FAIL'}`);
      if (correctPath) {
        console.log(`  Current path: ${pwdResult.stdout.trim()}`);
      }
      console.log('');
      
    } catch (error) {
      console.log(`✗ Path change sync - Error: ${error.message}`);
      console.log('');
      
      this.testResults.push({
        testName: 'Path change sync',
        command: 'pwd in subdir',
        error: error.message,
        isValid: false,
        type: 'file-manager-sync'
      });
    }
    
    // Test 3: Test file operations and synchronization
    try {
      console.log('Testing file operations synchronization...');
      
      // Create a file in the test directory
      const createResult = await this.executeInDirectory('touch sync_test_file.txt');
      
      // List to verify the file exists
      const listResult = await this.executeInDirectory('ls -la');
      const fileExists = listResult.stdout.includes('sync_test_file.txt');
      
      // Clean up
      await this.executeInDirectory('rm sync_test_file.txt');
      
      this.testResults.push({
        testName: 'File operations sync',
        command: 'touch and verify',
        result: { create: createResult, list: listResult },
        isValid: createResult.exitCode === 0 && fileExists,
        type: 'file-manager-sync'
      });
      
      console.log(`✓ File operations sync: ${fileExists ? 'PASS' : 'FAIL'}`);
      console.log('');
      
    } catch (error) {
      console.log(`✗ File operations sync - Error: ${error.message}`);
      console.log('');
      
      this.testResults.push({
        testName: 'File operations sync',
        command: 'touch and verify',
        error: error.message,
        isValid: false,
        type: 'file-manager-sync'
      });
    }
  }

  /**
   * Test integration between terminal and file manager
   */
  async testIntegration() {
    console.log('Testing terminal-file manager integration...\n');
    
    try {
      console.log('Testing integrated workflow...');
      
      // 1. Create a directory via terminal (use platform-appropriate command)
      const mkdirCommand = os.platform() === 'win32' ? 'mkdir integration_test_dir' : 'mkdir integration_test_dir';
      const mkdirResult = await this.executeInDirectory(mkdirCommand);
      
      // 2. Verify it exists via file manager (list command)
      const lsCommand = os.platform() === 'win32' ? 'dir' : 'ls -la';
      const lsResult = await this.executeInDirectory(lsCommand);
      const dirCreated = lsResult.stdout.includes('integration_test_dir') || 
                        lsResult.stdout.toLowerCase().includes('integration_test_dir');
      
      // 3. Create a file inside the new directory
      const subDirPath = path.join(this.testDirectory, 'integration_test_dir');
      const touchCommand = os.platform() === 'win32' ? 'echo. > test_integration_file.txt' : 'touch test_integration_file.txt';
      const touchResult = await this.executeInDirectory(
        touchCommand,
        subDirPath
      );
      
      // 4. Verify the file exists
      const lsInDirCommand = os.platform() === 'win32' ? 'dir' : 'ls -la';
      const lsInDirResult = await this.executeInDirectory(
        lsInDirCommand,
        subDirPath
      );
      const fileCreated = lsInDirResult.stdout.includes('test_integration_file.txt') || 
                         lsInDirResult.stdout.toLowerCase().includes('test_integration_file.txt');
      
      // 5. Clean up (use platform-appropriate command)
      const rmCommand = os.platform() === 'win32' ? 'rmdir /s /q integration_test_dir' : 'rm -rf integration_test_dir';
      await this.executeInDirectory(rmCommand);
      
      const isValid = mkdirResult.exitCode === 0 && 
                     dirCreated && 
                     touchResult.exitCode === 0 && 
                     fileCreated;
      
      this.testResults.push({
        testName: 'Terminal-file manager integration',
        commands: ['mkdir', 'touch', 'ls'],
        results: { mkdir: mkdirResult, ls: lsResult, touch: touchResult, lsInDir: lsInDirResult },
        isValid,
        type: 'integration'
      });
      
      console.log(`✓ Integration test: ${isValid ? 'PASS' : 'FAIL'}`);
      console.log('');
      
    } catch (error) {
      console.log(`✗ Integration test - Error: ${error.message}`);
      console.log('');
      
      this.testResults.push({
        testName: 'Terminal-file manager integration',
        error: error.message,
        isValid: false,
        type: 'integration'
      });
    }
  }

  /**
   * Generate test report
   */
  generateReport() {
    const totalTests = this.testResults.length;
    const passedTests = this.testResults.filter(r => r.isValid).length;
    const failedTests = totalTests - passedTests;
    
    const byType = {
      'terminal-simulation': this.testResults.filter(r => r.type === 'terminal-simulation'),
      'file-manager-sync': this.testResults.filter(r => r.type === 'file-manager-sync'),
      'integration': this.testResults.filter(r => r.type === 'integration')
    };
    
    const report = {
      summary: {
        total: totalTests,
        passed: passedTests,
        failed: failedTests,
        successRate: totalTests > 0 ? (passedTests / totalTests) * 100 : 0
      },
      byType,
      details: this.testResults,
      timestamp: new Date()
    };
    
    return report;
  }

  /**
   * Print detailed test results
   */
  printResults() {
    const report = this.generateReport();
    
    console.log('=== Terminal Simulation and File Manager Synchronization Test Results ===');
    console.log(`Total tests: ${report.summary.total}`);
    console.log(`Passed: ${report.summary.passed}`);
    console.log(`Failed: ${report.summary.failed}`);
    console.log(`Success rate: ${report.summary.successRate.toFixed(2)}%`);
    console.log('');
    
    // Print by type
    for (const [type, tests] of Object.entries(report.byType)) {
      if (tests.length > 0) {
        console.log(`--- ${type.toUpperCase().replace('-', ' ')} ---`);
        for (const result of tests) {
          const status = result.isValid ? '✓ PASS' : '✗ FAIL';
          console.log(`${status}: ${result.testName}`);
          
          if (result.error) {
            console.log(`  Error: ${result.error}`);
          } else if (result.result) {
            if (typeof result.result === 'object' && result.result.exitCode !== undefined) {
              console.log(`  Exit code: ${result.result.exitCode}`);
            }
          }
        }
        console.log('');
      }
    }
  }

  /**
   * Cleanup test environment
   */
  cleanup() {
    try {
      if (fs.existsSync(this.testDirectory)) {
        fs.rmSync(this.testDirectory, { recursive: true, force: true });
        console.log(`Test environment cleaned up: ${this.testDirectory}`);
      }
    } catch (error) {
      console.error(`Error cleaning up test environment: ${error.message}`);
    }
  }

  /**
   * Run all tests
   */
  async runAllTests() {
    try {
      await this.setupTestEnvironment();
      await this.testTerminalSimulation();
      await this.testFileManagerSync();
      await this.testIntegration();
      this.printResults();
    } finally {
      this.cleanup();
    }
    
    const report = this.generateReport();
    return report;
  }
}

// Run the test if this file is executed directly
if (require.main === module) {
  async function runTests() {
    const tester = new TerminalSyncTester();
    const report = await tester.runAllTests();
    
    // Exit with appropriate code based on test results
    process.exit(report.summary.failed > 0 ? 1 : 0);
  }
  
  runTests().catch(error => {
    console.error('Test execution failed:', error);
    process.exit(1);
  });
}

module.exports = TerminalSyncTester;