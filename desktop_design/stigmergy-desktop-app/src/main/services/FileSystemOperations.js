// File System Operations Service
// This module provides file system operations for the Electron app

const fs = require('fs').promises;
const path = require('path');

class FileSystemOperations {
  /**
   * Read a file
   * @param {string} filePath - Path to the file
   * @returns {Promise<Object>} - File content or error
   */
  async readFile(filePath) {
    try {
      const content = await fs.readFile(filePath, 'utf8');
      return { success: true, content };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Write content to a file
   * @param {string} filePath - Path to the file
   * @param {string} content - Content to write
   * @returns {Promise<Object>} - Success status or error
   */
  async writeFile(filePath, content) {
    try {
      // Ensure directory exists
      const dir = path.dirname(filePath);
      await fs.mkdir(dir, { recursive: true });
      
      await fs.writeFile(filePath, content, 'utf8');
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * List directory contents
   * @param {string} dirPath - Path to the directory
   * @returns {Promise<Object>} - Directory contents or error
   */
  async listDirectory(dirPath) {
    try {
      const files = await fs.readdir(dirPath, { withFileTypes: true });
      const fileList = files.map(file => ({
        name: file.name,
        isDirectory: file.isDirectory(),
        isFile: file.isFile(),
        size: file.isFile() ? null : undefined // Will be populated later
      }));
      return { success: true, files: fileList };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Create a directory
   * @param {string} dirPath - Path to the directory
   * @returns {Promise<Object>} - Success status or error
   */
  async createDirectory(dirPath) {
    try {
      await fs.mkdir(dirPath, { recursive: true });
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Delete a file or directory
   * @param {string} pathToDelete - Path to delete
   * @returns {Promise<Object>} - Success status or error
   */
  async deletePath(pathToDelete) {
    try {
      await fs.rm(pathToDelete, { recursive: true, force: true });
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Rename a file or directory
   * @param {string} oldPath - Current path
   * @param {string} newPath - New path
   * @returns {Promise<Object>} - Success status or error
   */
  async renamePath(oldPath, newPath) {
    try {
      await fs.rename(oldPath, newPath);
      return { success: true };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * Get file statistics
   * @param {string} filePath - Path to the file
   * @returns {Promise<Object>} - File stats or error
   */
  async getFileStats(filePath) {
    try {
      const stats = await fs.stat(filePath);
      return { 
        success: true, 
        stats: {
          size: stats.size,
          isFile: stats.isFile(),
          isDirectory: stats.isDirectory(),
          createdAt: stats.birthtime,
          modifiedAt: stats.mtime
        }
      };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }
}

module.exports = FileSystemOperations;