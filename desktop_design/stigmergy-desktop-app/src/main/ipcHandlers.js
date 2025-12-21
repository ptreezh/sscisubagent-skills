// IPC handlers for Electron main process
const { ipcMain } = require('electron');
const StigmergyCLIWrapper = require('./services/StigmergyCLIWrapper.js');
const FileSystemOperations = require('./services/FileSystemOperations.js');
const fs = require('fs').promises;
const path = require('path');

// Initialize services
const stigmergyWrapper = new StigmergyCLIWrapper();
const fileSystemOps = new FileSystemOperations();

// File system operations
ipcMain.handle('read-file', async (event, filePath) => {
  return await fileSystemOps.readFile(filePath);
});

ipcMain.handle('write-file', async (event, filePath, content) => {
  return await fileSystemOps.writeFile(filePath, content);
});

ipcMain.handle('list-directory', async (event, dirPath) => {
  return await fileSystemOps.listDirectory(dirPath);
});

ipcMain.handle('create-directory', async (event, dirPath) => {
  return await fileSystemOps.createDirectory(dirPath);
});

ipcMain.handle('delete-path', async (event, pathToDelete) => {
  return await fileSystemOps.deletePath(pathToDelete);
});

ipcMain.handle('rename-path', async (event, oldPath, newPath) => {
  return await fileSystemOps.renamePath(oldPath, newPath);
});

ipcMain.handle('get-file-stats', async (event, filePath) => {
  return await fileSystemOps.getFileStats(filePath);
});

// Stigmergy CLI operations
ipcMain.handle('execute-stigmergy-command', async (event, command, args) => {
  try {
    const result = await stigmergyWrapper.executeCommand(command, args);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

// Specific Stigmergy commands
ipcMain.handle('stigmergy-list-skills', async () => {
  try {
    const result = await stigmergyWrapper.listSkills();
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('stigmergy-install-skill', async (event, skillName) => {
  try {
    const result = await stigmergyWrapper.installSkill(skillName);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('stigmergy-remove-skill', async (event, skillName) => {
  try {
    const result = await stigmergyWrapper.removeSkill(skillName);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('stigmergy-get-status', async () => {
  try {
    const result = await stigmergyWrapper.getStatus();
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('stigmergy-configure', async (event, key, value) => {
  try {
    const result = await stigmergyWrapper.configure(key, value);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('stigmergy-get-config', async (event, key) => {
  try {
    const result = await stigmergyWrapper.getConfig(key);
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('stigmergy-list-clis', async () => {
  try {
    const result = await stigmergyWrapper.listCLIs();
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});

ipcMain.handle('stigmergy-get-version', async () => {
  try {
    const result = await stigmergyWrapper.getVersion();
    return result;
  } catch (error) {
    return { success: false, error: error.message };
  }
});