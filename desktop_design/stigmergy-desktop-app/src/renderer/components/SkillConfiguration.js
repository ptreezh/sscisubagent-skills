import React, { useState, useEffect } from 'react';

const SkillConfiguration = ({ skill, onClose, onSave }) => {
  const [config, setConfig] = useState({});
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);

  // Initialize config with skill defaults
  useEffect(() => {
    if (skill && skill.config) {
      setConfig(skill.config);
    } else {
      // Default configuration structure
      setConfig({
        enabled: true,
        priority: 1,
        parameters: {}
      });
    }
  }, [skill]);

  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const handleInputChange = (key, value) => {
    setConfig(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const handleParameterChange = (paramKey, value) => {
    setConfig(prev => ({
      ...prev,
      parameters: {
        ...prev.parameters,
        [paramKey]: value
      }
    }));
  };

  const addParameter = () => {
    const newParamKey = `param${Object.keys(config.parameters || {}).length + 1}`;
    handleParameterChange(newParamKey, '');
  };

  const removeParameter = (paramKey) => {
    setConfig(prev => {
      const newParams = { ...prev.parameters };
      delete newParams[paramKey];
      return {
        ...prev,
        parameters: newParams
      };
    });
  };

  const handleSave = async () => {
    setLoading(true);
    try {
      // In a real implementation, this would save to the actual Stigmergy CLI
      // For now, we'll just simulate the save
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      if (onSave) {
        onSave(skill.id, config);
      }
      
      showNotification('配置已保存', 'success');
    } catch (error) {
      showNotification(`保存失败: ${error.message}`, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="skill-configuration-overlay">
      {notification && (
        <div className={`notification notification-${notification.type}`}>
          {notification.message}
        </div>
      )}
      
      <div className="skill-configuration-modal card">
        <div className="skill-configuration-header">
          <h2>配置技能: {skill?.name || '未知技能'}</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        
        <div className="skill-configuration-content">
          <div className="form-group">
            <label className="form-label">启用状态</label>
            <select
              className="form-input"
              value={config.enabled ? 'enabled' : 'disabled'}
              onChange={(e) => handleInputChange('enabled', e.target.value === 'enabled')}
            >
              <option value="enabled">已启用</option>
              <option value="disabled">未启用</option>
            </select>
          </div>
          
          <div className="form-group">
            <label className="form-label">优先级</label>
            <input
              type="number"
              className="form-input"
              value={config.priority || 1}
              onChange={(e) => handleInputChange('priority', parseInt(e.target.value))}
              min="1"
              max="10"
            />
          </div>
          
          <div className="form-group">
            <div className="d-flex justify-content-between align-items-center">
              <label className="form-label">参数配置</label>
              <button className="btn btn-secondary" onClick={addParameter}>
                添加参数
              </button>
            </div>
            
            {config.parameters && Object.keys(config.parameters).length > 0 ? (
              <div className="parameters-list">
                {Object.entries(config.parameters).map(([key, value]) => (
                  <div key={key} className="parameter-item">
                    <input
                      type="text"
                      className="form-input param-key"
                      value={key}
                      readOnly
                    />
                    <input
                      type="text"
                      className="form-input param-value"
                      value={value}
                      onChange={(e) => handleParameterChange(key, e.target.value)}
                      placeholder="参数值"
                    />
                    <button 
                      className="btn btn-danger"
                      onClick={() => removeParameter(key)}
                    >
                      删除
                    </button>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-center">暂无自定义参数</p>
            )}
          </div>
        </div>
        
        <div className="skill-configuration-footer">
          <button className="btn btn-secondary mr-10" onClick={onClose}>
            取消
          </button>
          <button 
            className="btn btn-primary" 
            onClick={handleSave}
            disabled={loading}
          >
            {loading ? '保存中...' : '保存配置'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SkillConfiguration;