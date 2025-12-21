import React, { useState, useEffect } from 'react';

const FileViewer = ({ file, onClose, onSave }) => {
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(false);
  const [originalContent, setOriginalContent] = useState('');

  // Load file content
  useEffect(() => {
    const loadFileContent = async () => {
      setLoading(true);
      try {
        // In a real implementation, this would load the actual file content
        // For now, we'll simulate different content based on file type
        let mockContent = '';
        
        if (file.name.endsWith('.md')) {
          mockContent = `# ${file.name.replace('.md', '')}\n\n这是 ${file.name} 文件的内容。\n\n## 章节一\n\n这里是文件的一些内容。\n\n## 章节二\n\n更多内容在这里。`;
        } else if (file.name.endsWith('.txt')) {
          mockContent = `这是 ${file.name} 文件的内容。\n\n文件内容示例:\n- 第一行\n- 第二行\n- 第三行`;
        } else if (file.name.endsWith('.json')) {
          mockContent = `{\n  "fileName": "${file.name}",\n  "created": "2025-12-21",\n  "size": "1KB",\n  "type": "mock"\n}`;
        } else {
          mockContent = `这是 ${file.name} 文件的内容。\n\n文件类型: ${file.name.split('.').pop()}\n文件大小: 模拟大小\n创建时间: 2025-12-21`;
        }
        
        setContent(mockContent);
        setOriginalContent(mockContent);
      } catch (error) {
        setContent(`无法加载文件内容: ${error.message}`);
      } finally {
        setLoading(false);
      }
    };

    loadFileContent();
  }, [file]);

  const handleSave = async () => {
    setLoading(true);
    try {
      // In a real implementation, this would save the actual file content
      // For now, we'll just simulate the save
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      if (onSave) {
        onSave(file.name, content);
      }
      
      setOriginalContent(content);
      setIsEditing(false);
    } catch (error) {
      alert(`保存失败: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = () => {
    setContent(originalContent);
    setIsEditing(false);
  };

  return (
    <div className="file-viewer-overlay">
      <div className="file-viewer-modal card">
        <div className="file-viewer-header">
          <h2>{file.name}</h2>
          <div className="file-viewer-actions">
            {!isEditing ? (
              <button 
                className="btn btn-secondary mr-10"
                onClick={() => setIsEditing(true)}
              >
                编辑
              </button>
            ) : (
              <>
                <button 
                  className="btn btn-success mr-10"
                  onClick={handleSave}
                  disabled={loading}
                >
                  {loading ? '保存中...' : '保存'}
                </button>
                <button 
                  className="btn btn-secondary"
                  onClick={handleCancel}
                  disabled={loading}
                >
                  取消
                </button>
              </>
            )}
            <button 
              className="btn btn-primary ml-10"
              onClick={onClose}
            >
              关闭
            </button>
          </div>
        </div>
        
        <div className="file-viewer-content">
          {loading && !content ? (
            <div className="text-center">
              <p>加载中...</p>
            </div>
          ) : isEditing ? (
            <textarea
              className="file-editor"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              disabled={loading}
            />
          ) : (
            <div className="file-content">
              <pre>{content}</pre>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default FileViewer;