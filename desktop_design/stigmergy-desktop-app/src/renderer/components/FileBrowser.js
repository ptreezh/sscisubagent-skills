import React, { useState, useEffect } from 'react';
import FileViewer from './FileViewer';

const FileBrowser = ({ projectId, projectName }) => {
  const [files, setFiles] = useState([]);
  const [currentPath, setCurrentPath] = useState('');
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);
  const [newFileName, setNewFileName] = useState('');
  const [showNewFileInput, setShowNewFileInput] = useState(false);
  const [viewingFile, setViewingFile] = useState(null);

  // Show notification
  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  // Load files (simulated)
  const loadFiles = async (path = '') => {
    setLoading(true);
    try {
      // In a real implementation, this would call the actual file system operations
      // For now, we'll simulate the file structure
      await new Promise(resolve => setTimeout(resolve, 500));
      
      // Mock file structure
      const mockFiles = [
        { name: 'documents', isDirectory: true, isFile: false },
        { name: 'data', isDirectory: true, isFile: false },
        { name: 'README.md', isDirectory: false, isFile: true },
        { name: 'project-notes.txt', isDirectory: false, isFile: true },
        { name: 'analysis-results.pdf', isDirectory: false, isFile: true },
        { name: 'config.json', isDirectory: false, isFile: true }
      ];
      
      setFiles(mockFiles);
      setCurrentPath(path);
    } catch (error) {
      showNotification(`加载文件失败: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  // Initialize with project files
  useEffect(() => {
    loadFiles('');
  }, [projectId]);

  const handleNavigate = (fileName) => {
    const newPath = currentPath ? `${currentPath}/${fileName}` : fileName;
    loadFiles(newPath);
  };

  const handleGoUp = () => {
    if (currentPath) {
      const pathParts = currentPath.split('/');
      pathParts.pop();
      const newPath = pathParts.join('/');
      loadFiles(newPath);
    }
  };

  const handleNewFile = async () => {
    if (!newFileName.trim()) {
      showNotification('请输入文件名', 'warning');
      return;
    }

    try {
      // In a real implementation, this would create an actual file
      // For now, we'll just add it to the mock list
      const newFile = {
        name: newFileName,
        isDirectory: false,
        isFile: true
      };
      
      setFiles(prev => [...prev, newFile]);
      setNewFileName('');
      setShowNewFileInput(false);
      showNotification('文件创建成功', 'success');
    } catch (error) {
      showNotification(`创建文件失败: ${error.message}`, 'error');
    }
  };

  const handleDeleteFile = async (fileName) => {
    if (!window.confirm(`确定要删除 "${fileName}" 吗?`)) {
      return;
    }

    try {
      // In a real implementation, this would delete the actual file
      // For now, we'll just remove it from the mock list
      setFiles(prev => prev.filter(f => f.name !== fileName));
      showNotification('文件删除成功', 'success');
    } catch (error) {
      showNotification(`删除文件失败: ${error.message}`, 'error');
    }
  };

  const handleViewFile = (file) => {
    setViewingFile(file);
  };

  const handleSaveFile = (fileName, content) => {
    showNotification(`文件 "${fileName}" 保存成功`, 'success');
  };

  return (
    <div className="file-browser card">
      {notification && (
        <div className={`notification notification-${notification.type}`}>
          {notification.message}
        </div>
      )}
      
      {/* File Viewer Modal */}
      {viewingFile && (
        <FileViewer
          file={viewingFile}
          onClose={() => setViewingFile(null)}
          onSave={handleSaveFile}
        />
      )}
      
      <div className="file-browser-header">
        <h2>项目文件浏览器: {projectName}</h2>
      </div>
      
      <div className="file-browser-toolbar mb-20">
        <div className="d-flex align-items-center">
          <button 
            className="btn btn-secondary mr-10"
            onClick={handleGoUp}
            disabled={!currentPath}
          >
            返回上级
          </button>
          
          <div className="current-path">
            当前路径: {currentPath || '/'}{currentPath && !currentPath.endsWith('/') ? '/' : ''}
          </div>
          
          <div className="ml-auto">
            <button 
              className="btn btn-primary mr-10"
              onClick={() => setShowNewFileInput(!showNewFileInput)}
            >
              新建文件
            </button>
          </div>
        </div>
        
        {showNewFileInput && (
          <div className="mt-10 d-flex align-items-center">
            <input
              type="text"
              className="form-input mr-10"
              placeholder="文件名"
              value={newFileName}
              onChange={(e) => setNewFileName(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleNewFile()}
            />
            <button 
              className="btn btn-success mr-10"
              onClick={handleNewFile}
            >
              创建
            </button>
            <button 
              className="btn btn-secondary"
              onClick={() => {
                setShowNewFileInput(false);
                setNewFileName('');
              }}
            >
              取消
            </button>
          </div>
        )}
      </div>
      
      <div className="file-browser-content">
        {loading ? (
          <div className="text-center">
            <p>加载中...</p>
          </div>
        ) : (
          <div className="file-list">
            {files.length > 0 ? (
              files.map((file, index) => (
                <div key={index} className="file-item">
                  <div className="d-flex align-items-center">
                    <span className="file-icon mr-10">
                      {file.isDirectory ? '📁' : '📄'}
                    </span>
                    <span 
                      className={`file-name ${file.isDirectory ? 'directory' : ''}`}
                      onClick={() => file.isDirectory ? handleNavigate(file.name) : handleViewFile(file)}
                    >
                      {file.name}
                    </span>
                  </div>
                  
                  <div className="file-actions">
                    {file.isFile && (
                      <button 
                        className="btn btn-secondary btn-sm mr-10"
                        onClick={() => handleViewFile(file)}
                      >
                        打开
                      </button>
                    )}
                    <button 
                      className="btn btn-danger btn-sm"
                      onClick={() => handleDeleteFile(file.name)}
                    >
                      删除
                    </button>
                  </div>
                </div>
              ))
            ) : (
              <div className="text-center">
                <p>该目录为空</p>
              </div>
            )}
          </div>
        )}
      </div>
      
      <div className="file-browser-footer mt-20">
        <p>提示: 双击文件夹可进入目录，点击文件可查看内容</p>
      </div>
    </div>
  );
};

export default FileBrowser;