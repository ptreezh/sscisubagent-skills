// Preload script for Electron
// This script runs before the renderer process is loaded
const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
  // IPC communication methods
  sendMessage: (channel, data) => {
    // whitelist channels
    const validChannels = ['stigmergy-command', 'file-operation'];
    if (validChannels.includes(channel)) {
      ipcRenderer.send(channel, data);
    }
  },
  
  receiveMessage: (channel, func) => {
    const validChannels = ['stigmergy-response', 'file-operation-result'];
    if (validChannels.includes(channel)) {
      // Deliberately strip event as it includes `sender`
      ipcRenderer.on(channel, (event, ...args) => func(...args));
    }
  },
  
  // File system operations
  readFile: (filePath) => ipcRenderer.invoke('read-file', filePath),
  writeFile: (filePath, content) => ipcRenderer.invoke('write-file', filePath, content),
  listDirectory: (dirPath) => ipcRenderer.invoke('list-directory', dirPath),
  createDirectory: (dirPath) => ipcRenderer.invoke('create-directory', dirPath),
  deletePath: (pathToDelete) => ipcRenderer.invoke('delete-path', pathToDelete),
  renamePath: (oldPath, newPath) => ipcRenderer.invoke('rename-path', oldPath, newPath),
  getFileStats: (filePath) => ipcRenderer.invoke('get-file-stats', filePath),
  
  // Stigmergy CLI operations
  executeStigmergyCommand: (command, args) => ipcRenderer.invoke('execute-stigmergy-command', command, args),
  listStigmergySkills: () => ipcRenderer.invoke('stigmergy-list-skills'),
  installStigmergySkill: (skillName) => ipcRenderer.invoke('stigmergy-install-skill', skillName),
  removeStigmergySkill: (skillName) => ipcRenderer.invoke('stigmergy-remove-skill', skillName),
  getStigmergyStatus: () => ipcRenderer.invoke('stigmergy-get-status'),
  configureStigmergy: (key, value) => ipcRenderer.invoke('stigmergy-configure', key, value),
  getStigmergyConfig: (key) => ipcRenderer.invoke('stigmergy-get-config', key),
  listStigmergyCLIs: () => ipcRenderer.invoke('stigmergy-list-clis'),
  getStigmergyVersion: () => ipcRenderer.invoke('stigmergy-get-version'),
});