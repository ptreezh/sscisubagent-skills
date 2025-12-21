import React, { useState, useEffect } from 'react';
import UserPreferencesService from '../services/UserPreferencesService';

const UserPreferences = ({ onClose }) => {
  const [preferences, setPreferences] = useState({});
  const [notification, setNotification] = useState(null);
  const [saving, setSaving] = useState(false);

  // Load preferences
  useEffect(() => {
    const loadedPreferences = UserPreferencesService.getPreferences();
    setPreferences(loadedPreferences);
  }, []);

  // Show notification
  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  // Handle preference change
  const handlePreferenceChange = (key, value) => {
    setPreferences(prev => ({
      ...prev,
      [key]: value
    }));
  };

  // Handle save preferences
  const handleSavePreferences = async () => {
    setSaving(true);
    try {
      const success = UserPreferencesService.savePreferences(preferences);
      
      if (success) {
        showNotification('偏好设置已保存', 'success');
        setTimeout(() => {
          onClose();
        }, 1500);
      } else {
        showNotification('保存偏好设置失败', 'error');
      }
    } catch (error) {
      showNotification(`保存失败: ${error.message}`, 'error');
    } finally {
      setSaving(false);
    }
  };

  // Handle reset to default
  const handleResetToDefault = () => {
    if (window.confirm('确定要重置所有偏好设置为默认值吗？')) {
      try {
        const success = UserPreferencesService.resetToDefault();
        
        if (success) {
          const defaultPreferences = UserPreferencesService.getPreferences();
          setPreferences(defaultPreferences);
          showNotification('已重置为默认设置', 'success');
        } else {
          showNotification('重置失败', 'error');
        }
      } catch (error) {
        showNotification(`重置失败: ${error.message}`, 'error');
      }
    }
  };

  return (
    <div className="preferences-overlay">
      {notification && (
        <div className={`notification notification-${notification.type}`}>
          {notification.message}
        </div>
      )}
      
      <div className="preferences-modal card">
        <div className="preferences-header">
          <h2>用户偏好设置</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        
        <div className="preferences-content">
          <div className="preferences-section">
            <h3>界面设置</h3>
            
            <div className="form-group">
              <label className="form-label">主题</label>
              <select
                className="form-input"
                value={preferences.theme || 'light'}
                onChange={(e) => handlePreferenceChange('theme', e.target.value)}
              >
                <option value="light">浅色主题</option>
                <option value="dark">深色主题</option>
              </select>
            </div>
            
            <div className="form-group">
              <label className="form-label">语言</label>
              <select
                className="form-input"
                value={preferences.language || 'zh-CN'}
                onChange={(e) => handlePreferenceChange('language', e.target.value)}
              >
                <option value="zh-CN">简体中文</option>
                <option value="en-US">English</option>
              </select>
            </div>
          </div>
          
          <div className="preferences-section">
            <h3>功能设置</h3>
            
            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={preferences.autoSave ?? true}
                  onChange={(e) => handlePreferenceChange('autoSave', e.target.checked)}
                />
                <span>自动保存</span>
              </label>
              <p className="checkbox-description">自动保存您的工作进度</p>
            </div>
            
            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={preferences.notifications ?? true}
                  onChange={(e) => handlePreferenceChange('notifications', e.target.checked)}
                />
                <span>启用通知</span>
              </label>
              <p className="checkbox-description">显示操作结果和系统通知</p>
            </div>
            
            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={preferences.commandHistory ?? true}
                  onChange={(e) => handlePreferenceChange('commandHistory', e.target.checked)}
                />
                <span>保存命令历史</span>
              </label>
              <p className="checkbox-description">保留控制台命令执行历史</p>
            </div>
            
            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={preferences.filePreview ?? true}
                  onChange={(e) => handlePreferenceChange('filePreview', e.target.checked)}
                />
                <span>文件预览</span>
              </label>
              <p className="checkbox-description">在文件浏览器中显示文件内容预览</p>
            </div>
            
            <div className="form-group checkbox-group">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={preferences.autoUpdate ?? true}
                  onChange={(e) => handlePreferenceChange('autoUpdate', e.target.checked)}
                />
                <span>自动更新</span>
              </label>
              <p className="checkbox-description">自动检查和安装应用更新</p>
            </div>
          </div>
        </div>
        
        <div className="preferences-footer">
          <button 
            className="btn btn-secondary mr-10"
            onClick={handleResetToDefault}
          >
            重置为默认值
          </button>
          <div className="ml-auto">
            <button 
              className="btn btn-secondary mr-10"
              onClick={onClose}
            >
              取消
            </button>
            <button 
              className="btn btn-primary"
              onClick={handleSavePreferences}
              disabled={saving}
            >
              {saving ? '保存中...' : '保存设置'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default UserPreferences;