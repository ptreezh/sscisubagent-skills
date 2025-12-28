// CLI Command Accuracy Test
// This test validates that CLI commands are executed accurately and responses are handled properly

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

class CLIAccuracyTester {
  constructor() {
    this.testResults = [];
    this.cliCommands = [
      'stigmergy --version',
      'stigmergy skill list',
      'stigmergy status',
      'stigmergy help'
    ];
  }

  /**
   * Execute a CLI command and capture output
   * @param {string} command - The CLI command to execute
   * @returns {Promise<Object>} Object containing stdout, stderr, and exit code
   */
  async executeCommand(command) {
    return new Promise((resolve, reject) => {
      const [cmd, ...args] = command.split(' ');
      
      const child = spawn(cmd, args, {
        cwd: process.cwd(),
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
          timestamp: new Date()
        });
      });

      child.on('error', (error) => {
        reject(error);
      });
    });
  }

  /**
   * Test accuracy of CLI command execution
   */
  async testCommandAccuracy() {
    console.log('Testing CLI command accuracy...\n');
    
    for (const command of this.cliCommands) {
      try {
        console.log(`Executing: ${command}`);
        const result = await this.executeCommand(command);
        
        // Validate the result
        const isValid = this.validateCommandResult(command, result);
        
        this.testResults.push({
          command,
          result,
          isValid,
          timestamp: new Date()
        });
        
        console.log(`✓ Command executed: ${command}`);
        console.log(`  Exit code: ${result.exitCode}`);
        console.log(`  Valid: ${isValid}`);
        console.log(`  Stdout length: ${result.stdout.length}`);
        console.log('');
        
      } catch (error) {
        console.log(`✗ Command failed: ${command}`);
        console.log(`  Error: ${error.message}`);
        console.log('');
        
        this.testResults.push({
          command,
          error: error.message,
          isValid: false,
          timestamp: new Date()
        });
      }
    }
    
    return this.testResults;
  }

  /**
   * Validate command result based on expected behavior
   * @param {string} command - The command that was executed
   * @param {Object} result - The result of the command execution
   * @returns {boolean} Whether the result is valid
   */
  validateCommandResult(command, result) {
    // Basic validation rules
    if (result.exitCode !== 0 && !command.includes('help')) {
      return false;
    }
    
    // Check for expected output patterns based on command
    if (command.includes('--version')) {
      // Version command should return a version string
      return result.stdout && result.stdout.trim().length > 0;
    }
    
    if (command.includes('skill list')) {
      // Skill list should return a list or empty list indication
      return result.stdout !== undefined;
    }
    
    if (command.includes('status')) {
      // Status command should return status information
      return result.stdout !== undefined;
    }
    
    if (command.includes('help')) {
      // Help command should return help text
      return result.stdout && result.stdout.length > 0;
    }
    
    // Default: command should execute without error
    return result.exitCode === 0;
  }

  /**
   * Generate test report
   */
  generateReport() {
    const totalTests = this.testResults.length;
    const passedTests = this.testResults.filter(r => r.isValid).length;
    const failedTests = totalTests - passedTests;
    
    const report = {
      summary: {
        total: totalTests,
        passed: passedTests,
        failed: failedTests,
        successRate: totalTests > 0 ? (passedTests / totalTests) * 100 : 0
      },
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
    
    console.log('=== CLI Command Accuracy Test Results ===');
    console.log(`Total tests: ${report.summary.total}`);
    console.log(`Passed: ${report.summary.passed}`);
    console.log(`Failed: ${report.summary.failed}`);
    console.log(`Success rate: ${report.summary.successRate.toFixed(2)}%`);
    console.log('');
    
    for (const result of this.testResults) {
      const status = result.isValid ? '✓ PASS' : '✗ FAIL';
      console.log(`${status}: ${result.command}`);
      
      if (result.error) {
        console.log(`  Error: ${result.error}`);
      } else if (result.result) {
        console.log(`  Exit code: ${result.result.exitCode}`);
        console.log(`  Output length: ${result.result.stdout.length} chars`);
      }
      console.log('');
    }
  }
}

// Run the test if this file is executed directly
if (require.main === module) {
  async function runTests() {
    const tester = new CLIAccuracyTester();
    await tester.testCommandAccuracy();
    tester.printResults();
    
    // Exit with appropriate code based on test results
    const report = tester.generateReport();
    process.exit(report.summary.failed > 0 ? 1 : 0);
  }
  
  runTests().catch(error => {
    console.error('Test execution failed:', error);
    process.exit(1);
  });
}

module.exports = CLIAccuracyTester;