const os = require('os');

class PathSyncManager {
  constructor() {
    this.projectRoot = '';
    this.currentPath = '';
    this.previousPaths = [];
    this.isSyncEnabled = true;
  }

  /**
   * Update the current working path
   * @param {string} newPath - New path to set as current
   */
  updateCurrentPath(newPath) {
    if (this.validatePathWithinProject(newPath)) {
      this.previousPaths.push(this.currentPath);
      this.currentPath = newPath;
      return true;
    }
    return false;
  }

  /**
   * Get the relative path from project root
   * @param {string} targetPath - Path to get relative to project root
   * @returns {string} Relative path from project root
   */
  getRelativePath(targetPath) {
    if (!this.projectRoot || !targetPath) {
      return targetPath;
    }
    return targetPath.replace(this.projectRoot, '').replace(/^[/\\]+/, '');
  }

  /**
   * Validate if path is within project boundaries
   * @param {string} path - Path to validate
   * @returns {boolean} True if path is within project, false otherwise
   */
  validatePathWithinProject(path) {
    if (!this.projectRoot) {
      return true; // If no project root set, allow any path
    }
    const normalizedPath = path.replace(/\\/g, '/');
    const normalizedRoot = this.projectRoot.replace(/\\/g, '/');
    return normalizedPath.startsWith(normalizedRoot);
  }

  /**
   * Sync terminal to specified path
   * @param {string} path - Path to sync terminal to
   * @param {object} terminalManager - TerminalManager instance
   * @param {string} terminalId - Terminal ID to sync
   */
  syncTerminalToPath(path, terminalManager, terminalId) {
    if (!this.isSyncEnabled) {
      return false;
    }
    
    if (this.validatePathWithinProject(path)) {
      // Send cd command to terminal
      if (terminalManager && terminalId) {
        // Normalize path for the current platform
        let pathForTerminal = path.replace(/\\/g, '/');
        if (os.platform() === 'win32') {
          pathForTerminal = pathForTerminal.replace(/\//g, '\\');
        }
        terminalManager.sendToTerminal(terminalId, `cd "${pathForTerminal}"\r`);
        this.updateCurrentPath(path);
        return true;
      }
    }
    return false;
  }

  /**
   * Sync file browser to terminal path
   * @param {string} path - Path from terminal to sync to file browser
   * @param {function} onPathChange - Callback to update file browser
   */
  syncFileBrowserToTerminalPath(path, onPathChange) {
    if (!this.isSyncEnabled) {
      return false;
    }
    
    if (this.validatePathWithinProject(path)) {
      this.updateCurrentPath(path);
      if (onPathChange) {
        onPathChange(path);
      }
      return true;
    }
    return false;
  }

  /**
   * Set the project root path
   * @param {string} rootPath - Project root path
   */
  setProjectRoot(rootPath) {
    if (rootPath) {
      this.projectRoot = rootPath.replace(/\\/g, '/');
    }
  }

  /**
   * Get the project root path
   * @returns {string} Project root path
   */
  getProjectRoot() {
    return this.projectRoot;
  }

  /**
   * Get the current path
   * @returns {string} Current path
   */
  getCurrentPath() {
    return this.currentPath;
  }

  /**
   * Enable or disable path synchronization
   * @param {boolean} enabled - Whether to enable path sync
   */
  setSyncEnabled(enabled) {
    this.isSyncEnabled = enabled;
  }

  /**
   * Get sync status
   * @returns {boolean} True if sync is enabled, false otherwise
   */
  getSyncEnabled() {
    return this.isSyncEnabled;
  }
}

module.exports = PathSyncManager;