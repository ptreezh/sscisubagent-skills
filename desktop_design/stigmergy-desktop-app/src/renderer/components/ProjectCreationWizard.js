import React, { useState, useEffect } from 'react';
import ProjectTemplatesService from '../services/ProjectTemplatesService';

const ProjectCreationWizard = ({ onClose, onCreate }) => {
  const [step, setStep] = useState(1);
  const [projectName, setProjectName] = useState('');
  const [selectedTemplate, setSelectedTemplate] = useState('');
  const [templates, setTemplates] = useState([]);
  const [creating, setCreating] = useState(false);
  const [notification, setNotification] = useState(null);

  // Load templates
  useEffect(() => {
    const loadedTemplates = ProjectTemplatesService.getTemplates();
    setTemplates(loadedTemplates);
    
    // Select the first template by default
    if (loadedTemplates.length > 0) {
      setSelectedTemplate(loadedTemplates[0].id);
    }
  }, []);

  // Show notification
  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  const handleNext = () => {
    if (step < 2) {
      if (step === 1 && !projectName.trim()) {
        showNotification('请输入项目名称', 'warning');
        return;
      }
      setStep(step + 1);
    }
  };

  const handlePrev = () => {
    if (step > 1) {
      setStep(step - 1);
    }
  };

  const handleCreateProject = async () => {
    if (!projectName.trim()) {
      showNotification('请输入项目名称', 'warning');
      return;
    }

    if (!selectedTemplate) {
      showNotification('请选择项目模板', 'warning');
      return;
    }

    setCreating(true);
    
    try {
      // Generate a random project ID
      const projectId = `proj_${Date.now()}_${Math.floor(Math.random() * 1000)}`;
      
      // Create project using the template service
      const result = await ProjectTemplatesService.createProjectFromTemplate(
        projectId,
        projectName,
        selectedTemplate
      );
      
      if (result.success) {
        if (onCreate) {
          onCreate({
            id: projectId,
            name: projectName,
            path: `/home/user/projects/${projectName.replace(/\s+/g, '-').toLowerCase()}`,
            lastModified: new Date().toISOString().split('T')[0]
          });
        }
        
        showNotification(result.message, 'success');
        setTimeout(() => {
          onClose();
        }, 1500);
      } else {
        showNotification(`创建项目失败: ${result.error}`, 'error');
      }
    } catch (error) {
      showNotification(`创建项目失败: ${error.message}`, 'error');
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="project-wizard-overlay">
      {notification && (
        <div className={`notification notification-${notification.type}`}>
          {notification.message}
        </div>
      )}
      
      <div className="project-wizard-modal card">
        <div className="project-wizard-header">
          <h2>创建新项目</h2>
          <button className="close-button" onClick={onClose}>×</button>
        </div>
        
        <div className="project-wizard-content">
          {step === 1 && (
            <div className="wizard-step">
              <h3>项目基本信息</h3>
              <div className="form-group">
                <label className="form-label">项目名称 *</label>
                <input
                  type="text"
                  className="form-input"
                  placeholder="输入项目名称"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                />
              </div>
              
              <div className="form-group">
                <label className="form-label">项目位置</label>
                <input
                  type="text"
                  className="form-input"
                  value="/home/user/projects/"
                  readOnly
                />
              </div>
            </div>
          )}
          
          {step === 2 && (
            <div className="wizard-step">
              <h3>选择项目模板</h3>
              <p>选择一个模板来快速开始您的项目</p>
              
              <div className="template-selection">
                {templates.map(template => (
                  <div 
                    key={template.id}
                    className={`template-card ${selectedTemplate === template.id ? 'selected' : ''}`}
                    onClick={() => setSelectedTemplate(template.id)}
                  >
                    <h4>{template.name}</h4>
                    <p>{template.description}</p>
                    <div className="template-structure">
                      <strong>包含:</strong>
                      <ul>
                        {template.structure.slice(0, 3).map((item, index) => (
                          <li key={index}>{item.name} ({item.type})</li>
                        ))}
                        {template.structure.length > 3 && (
                          <li>...及其他 {template.structure.length - 3} 项</li>
                        )}
                      </ul>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
        
        <div className="project-wizard-footer">
          <div className="wizard-progress">
            <div className={`progress-step ${step >= 1 ? 'active' : ''}`}></div>
            <div className={`progress-step ${step >= 2 ? 'active' : ''}`}></div>
          </div>
          
          <div className="wizard-actions">
            {step > 1 && (
              <button 
                className="btn btn-secondary mr-10"
                onClick={handlePrev}
              >
                上一步
              </button>
            )}
            
            {step < 2 ? (
              <button 
                className="btn btn-primary"
                onClick={handleNext}
              >
                下一步
              </button>
            ) : (
              <button 
                className="btn btn-success"
                onClick={handleCreateProject}
                disabled={creating}
              >
                {creating ? '创建中...' : '创建项目'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProjectCreationWizard;