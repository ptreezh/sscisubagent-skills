// PathSyncManager unit tests
const PathSyncManager = require('../../src/main/path/PathSyncManager');

describe('PathSyncManager', () => {
  let pathSyncManager;

  beforeEach(() => {
    pathSyncManager = new PathSyncManager();
  });

  describe('constructor', () => {
    it('should initialize with default properties', () => {
      expect(pathSyncManager).toBeDefined();
      expect(pathSyncManager.projectRoot).toBe('');
      expect(pathSyncManager.currentPath).toBe('');
      expect(pathSyncManager.previousPaths).toEqual([]);
      expect(pathSyncManager.isSyncEnabled).toBe(true);
    });
  });

  describe('updateCurrentPath', () => {
    it('should update current path if within project', () => {
      pathSyncManager.setProjectRoot('/test/project');
      const result = pathSyncManager.updateCurrentPath('/test/project/subdir');
      expect(result).toBe(true);
      expect(pathSyncManager.getCurrentPath()).toBe('/test/project/subdir');
    });

    it('should not update current path if outside project', () => {
      pathSyncManager.setProjectRoot('/test/project');
      const result = pathSyncManager.updateCurrentPath('/outside/project');
      expect(result).toBe(false);
      expect(pathSyncManager.getCurrentPath()).toBe('');
    });

    it('should allow update if no project root is set', () => {
      const result = pathSyncManager.updateCurrentPath('/any/path');
      expect(result).toBe(true);
      expect(pathSyncManager.getCurrentPath()).toBe('/any/path');
    });
  });

  describe('getRelativePath', () => {
    it('should return relative path from project root', () => {
      pathSyncManager.setProjectRoot('/test/project');
      const relativePath = pathSyncManager.getRelativePath('/test/project/src/main.js');
      expect(relativePath).toBe('src/main.js');
    });

    it('should return original path if no project root is set', () => {
      const relativePath = pathSyncManager.getRelativePath('/test/project/src/main.js');
      expect(relativePath).toBe('/test/project/src/main.js');
    });
  });

  describe('validatePathWithinProject', () => {
    it('should return true for path within project', () => {
      pathSyncManager.setProjectRoot('/test/project');
      const result = pathSyncManager.validatePathWithinProject('/test/project/subdir');
      expect(result).toBe(true);
    });

    it('should return false for path outside project', () => {
      pathSyncManager.setProjectRoot('/test/project');
      const result = pathSyncManager.validatePathWithinProject('/other/project');
      expect(result).toBe(false);
    });

    it('should return true if no project root is set', () => {
      const result = pathSyncManager.validatePathWithinProject('/any/path');
      expect(result).toBe(true);
    });
  });

  describe('syncTerminalToPath', () => {
    it('should sync terminal to path if sync is enabled', () => {
      const mockTerminalManager = {
        sendToTerminal: jest.fn()
      };
      const terminalId = 'test-terminal';
      
      pathSyncManager.setProjectRoot('/test/project');
      const result = pathSyncManager.syncTerminalToPath('/test/project/subdir', mockTerminalManager, terminalId);
      
      expect(result).toBe(true);
      // The path should be normalized based on the platform
      const expectedPath = require('os').platform() === 'win32' ? '\\test\\project\\subdir' : '/test/project/subdir';
      expect(mockTerminalManager.sendToTerminal).toHaveBeenCalledWith(terminalId, `cd "${expectedPath}"\r`);
      expect(pathSyncManager.getCurrentPath()).toBe('/test/project/subdir');
    });

    it('should not sync terminal if sync is disabled', () => {
      const mockTerminalManager = {
        sendToTerminal: jest.fn()
      };
      const terminalId = 'test-terminal';
      
      pathSyncManager.setSyncEnabled(false);
      const result = pathSyncManager.syncTerminalToPath('/test/project/subdir', mockTerminalManager, terminalId);
      
      expect(result).toBe(false);
      expect(mockTerminalManager.sendToTerminal).not.toHaveBeenCalled();
    });
  });

  describe('syncFileBrowserToTerminalPath', () => {
    it('should sync file browser to terminal path', () => {
      const mockOnPathChange = jest.fn();
      
      pathSyncManager.setProjectRoot('/test/project');
      const result = pathSyncManager.syncFileBrowserToTerminalPath('/test/project/subdir', mockOnPathChange);
      
      expect(result).toBe(true);
      expect(mockOnPathChange).toHaveBeenCalledWith('/test/project/subdir');
      expect(pathSyncManager.getCurrentPath()).toBe('/test/project/subdir');
    });

    it('should not sync file browser if sync is disabled', () => {
      const mockOnPathChange = jest.fn();
      
      pathSyncManager.setSyncEnabled(false);
      const result = pathSyncManager.syncFileBrowserToTerminalPath('/test/project/subdir', mockOnPathChange);
      
      expect(result).toBe(false);
      expect(mockOnPathChange).not.toHaveBeenCalled();
    });
  });

  describe('project root management', () => {
    it('should set and get project root', () => {
      pathSyncManager.setProjectRoot('/test/project');
      expect(pathSyncManager.getProjectRoot()).toBe('/test/project');
    });

    it('should normalize project root path', () => {
      pathSyncManager.setProjectRoot('\\test\\project');
      expect(pathSyncManager.getProjectRoot()).toBe('/test/project');
    });
  });

  describe('sync status management', () => {
    it('should enable and disable sync', () => {
      pathSyncManager.setSyncEnabled(false);
      expect(pathSyncManager.getSyncEnabled()).toBe(false);
      
      pathSyncManager.setSyncEnabled(true);
      expect(pathSyncManager.getSyncEnabled()).toBe(true);
    });
  });
});