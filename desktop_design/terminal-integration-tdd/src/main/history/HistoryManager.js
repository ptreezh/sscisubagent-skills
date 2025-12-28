class HistoryManager {
  constructor(maxSize = 100) {
    this.commands = [];
    this.maxSize = maxSize;
  }

  /**
   * Add a command to history
   * @param {string} command - Command to add to history
   * @param {Date} timestamp - Timestamp of command execution
   * @param {boolean} success - Whether the command was successful
   */
  addCommand(command, timestamp = new Date(), success = true) {
    if (!command || typeof command !== 'string') {
      return false;
    }

    const historyEntry = {
      command,
      timestamp,
      success
    };

    this.commands.push(historyEntry);

    // Maintain max size by removing oldest entries
    if (this.commands.length > this.maxSize) {
      this.commands = this.commands.slice(-this.maxSize);
    }

    return true;
  }

  /**
   * Get command history
   * @param {number} limit - Maximum number of commands to return
   * @returns {Array} Array of command history entries
   */
  getHistory(limit = this.maxSize) {
    if (limit >= this.commands.length) {
      return [...this.commands];
    }
    return this.commands.slice(-limit);
  }

  /**
   * Clear all history
   */
  clearHistory() {
    this.commands = [];
  }

  /**
   * Search history for commands matching a query
   * @param {string} query - Search query
   * @returns {Array} Array of matching command history entries
   */
  searchHistory(query) {
    if (!query || typeof query !== 'string') {
      return [];
    }

    const normalizedQuery = query.toLowerCase();
    return this.commands.filter(entry => 
      entry.command.toLowerCase().includes(normalizedQuery)
    );
  }

  /**
   * Get the most recent command
   * @returns {Object|null} The most recent command entry or null if no commands
   */
  getLastCommand() {
    if (this.commands.length === 0) {
      return null;
    }
    return this.commands[this.commands.length - 1];
  }

  /**
   * Get commands executed within a specific time range
   * @param {Date} startTime - Start time for the range
   * @param {Date} endTime - End time for the range
   * @returns {Array} Array of command history entries within the time range
   */
  getCommandsByTimeRange(startTime, endTime) {
    return this.commands.filter(entry => 
      entry.timestamp >= startTime && entry.timestamp <= endTime
    );
  }

  /**
   * Update the success status of a command
   * @param {number} index - Index of the command to update
   * @param {boolean} success - New success status
   * @returns {boolean} True if the command was updated, false otherwise
   */
  updateCommandSuccess(index, success) {
    if (index < 0 || index >= this.commands.length) {
      return false;
    }

    this.commands[index].success = success;
    return true;
  }

  /**
   * Get the current size of the command history
   * @returns {number} Current number of commands in history
   */
  getCurrentSize() {
    return this.commands.length;
  }

  /**
   * Get the maximum size of the command history
   * @returns {number} Maximum number of commands allowed in history
   */
  getMaxSize() {
    return this.maxSize;
  }

  /**
   * Set the maximum size of the command history
   * @param {number} maxSize - New maximum size
   */
  setMaxSize(maxSize) {
    if (maxSize <= 0 || !Number.isInteger(maxSize)) {
      throw new Error('Max size must be a positive integer');
    }

    this.maxSize = maxSize;
    
    // Trim history if it exceeds the new max size
    if (this.commands.length > this.maxSize) {
      this.commands = this.commands.slice(-this.maxSize);
    }
  }
}

module.exports = HistoryManager;