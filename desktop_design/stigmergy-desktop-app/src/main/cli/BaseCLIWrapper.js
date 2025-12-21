const { spawn } = require('child_process');

/**
 * Custom error class for CLI-related errors
 */
class CLIError extends Error {
  constructor(message, cliTool, command, exitCode, stderr) {
    super(message);
    this.name = 'CLIError';
    this.cliTool = cliTool;
    this.command = command;
    this.exitCode = exitCode;
    this.stderr = stderr;
  }
}

/**
 * Base class for all CLI wrappers
 */
class BaseCLIWrapper {
  /**
   * Constructor for BaseCLIWrapper
   * @param {string} name - Name of the CLI tool
   * @param {string} executablePath - Path to the executable
   */
  constructor(name, executablePath) {
    this.name = name;
    this.executablePath = executablePath;
    this.isAvailable = false;
  }

  /**
   * Execute a command with the CLI tool
   * @param {string} command - Command to execute
   * @param {string[]} args - Arguments for the command
   * @param {Object} options - Options for child_process.spawn
   * @returns {Promise<string>} Promise that resolves with the command output
   */
  executeCommand(command, args = [], options = {}) {
    return new Promise((resolve, reject) => {
      const fullArgs = [command, ...args];
      const child = spawn(this.executablePath, fullArgs, options);
      
      let stdout = '';
      let stderr = '';
      
      child.stdout.on('data', (data) => {
        stdout += data.toString();
      });
      
      child.stderr.on('data', (data) => {
        stderr += data.toString();
      });
      
      child.on('close', (code) => {
        if (code === 0) {
          resolve(stdout.trim());
        } else {
          const error = new CLIError(
            `Command failed with exit code ${code}: ${stderr.trim()}`,
            this.name,
            command,
            code,
            stderr.trim()
          );
          reject(error);
        }
      });
      
      child.on('error', (error) => {
        const cliError = new CLIError(
          `Failed to execute command: ${error.message}`,
          this.name,
          command,
          null,
          error.message
        );
        reject(cliError);
      });
    });
  }

  /**
   * Parse command output into lines
   * @param {string} output - Raw command output
   * @returns {string[]} Array of output lines
   */
  parseOutput(output) {
    return output.split('\n').filter(line => line.trim() !== '');
  }

  /**
   * Handle errors from CLI commands
   * @param {Error} error - Original error
   * @param {string} command - Command that failed
   * @param {number} exitCode - Exit code
   * @param {string} stderr - Standard error output
   * @returns {CLIError} Wrapped CLI error
   */
  handleError(error, command, exitCode, stderr) {
    return new CLIError(
      error.message,
      this.name,
      command,
      exitCode,
      stderr
    );
  }
}

module.exports = BaseCLIWrapper;
module.exports.CLIError = CLIError;