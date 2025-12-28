const os = require('os');
const pty = require('node-pty');

// TerminalManager - Manages terminal processes for the Stigmergy desktop app
class TerminalManager {
  constructor() {
    this.terminals = {};
  }

  /**
   * Create a new terminal instance
   * @param {string} id - Unique identifier for the terminal
   * @param {string} cwd - Current working directory for the terminal
   * @returns {object} Terminal instance
   */
  createTerminal(id, cwd) {
    // Create a real terminal process using node-pty
    const shell = process.env.SHELL || (os.platform() === 'win32' ? 'powershell.exe' : 'bash');
    const terminal = pty.spawn(shell, [], {
      name: 'xterm-color',
      cols: 80,
      rows: 30,
      cwd: cwd,
      env: process.env
    });
    
    this.terminals[id] = terminal;
    return terminal;
  }

  /**
   * Send data to a terminal instance
   * @param {string} id - Terminal identifier
   * @param {string} data - Data to send to terminal
   */
  sendToTerminal(id, data) {
    const terminal = this.getTerminal(id);
    if (terminal) {
      terminal.write(data);
    }
  }

  /**
   * Resize a terminal instance
   * @param {string} id - Terminal identifier
   * @param {number} cols - Number of columns
   * @param {number} rows - Number of rows
   */
  resizeTerminal(id, cols, rows) {
    const terminal = this.getTerminal(id);
    if (terminal) {
      terminal.resize(cols, rows);
    }
  }

  /**
   * Get a terminal instance by ID
   * @param {string} id - Terminal identifier
   * @returns {object|null} Terminal instance or null if not found
   */
  getTerminal(id) {
    return this.terminals[id] || null;
  }

  /**
   * Remove a terminal instance by ID
   * @param {string} id - Terminal identifier
   * @returns {boolean} True if terminal was removed, false if not found
   */
  removeTerminal(id) {
    if (this.terminals[id]) {
      this.terminals[id].kill();
      delete this.terminals[id];
      return true;
    }
    return false;
  }
}

module.exports = TerminalManager;