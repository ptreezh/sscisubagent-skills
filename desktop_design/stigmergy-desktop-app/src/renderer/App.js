import React, { useState, useEffect } from 'react';
import OnboardingFlow from './components/OnboardingFlow';
import StigmergyConsole from './components/StigmergyConsole';
import SkillConfiguration from './components/SkillConfiguration';
import FileBrowser from './components/FileBrowser';
import HelpDocumentation from './components/HelpDocumentation';
import ProjectCreationWizard from './components/ProjectCreationWizard';
import UserPreferences from './components/UserPreferences';
import DataPersistenceService from './services/DataPersistenceService';
import UnifiedAgentService from './services/UnifiedAgentService';

const App = () => {
  const [skills, setSkills] = useState([]);
  const [projects, setProjects] = useState([]);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [loading, setLoading] = useState(false);
  const [notification, setNotification] = useState(null);
  const [showOnboarding, setShowOnboarding] = useState(false);
  const [configuringSkill, setConfiguringSkill] = useState(null);
  const [browsingProject, setBrowsingProject] = useState(null);
  const [showProjectWizard, setShowProjectWizard] = useState(false);
  const [showPreferences, setShowPreferences] = useState(false);

  // Load data from persistence service
  useEffect(() => {
    const savedProjects = DataPersistenceService.loadProjects();
    
    // Load agents and skills from the unified service
    const agents = UnifiedAgentService.getAgents();
    const skills = UnifiedAgentService.getAllSkills();
    
    setSkills(skills);
    
    if (savedProjects.length > 0) {
      setProjects(savedProjects);
    } else {
      // Default projects
      setProjects([
        { id: 1, name: '学术研究项目A', path: '/home/user/projects/research-a', lastModified: '2025-12-20' },
        { id: 2, name: '文献综述项目B', path: '/home/user/projects/literature-b', lastModified: '2025-12-19' }
      ]);
    }
  }, []);

  // Save skills when they change
  useEffect(() => {
    if (skills.length > 0) {
      DataPersistenceService.saveSkills(skills);
    }
  }, [skills]);

  // Save projects when they change
  useEffect(() => {
    if (projects.length > 0) {
      DataPersistenceService.saveProjects(projects);
    }
  }, [projects]);

  // Check if onboarding should be shown
  useEffect(() => {
    const hasSeenOnboarding = localStorage.getItem('hasSeenOnboarding');
    if (!hasSeenOnboarding) {
      setShowOnboarding(true);
    }
  }, []);

  // Show notification
  const showNotification = (message, type = 'info') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3000);
  };

  // Handle skill toggle
  const handleToggleSkill = (skillId) => {
    const updatedSkill = UnifiedAgentService.toggleSkillStatus(skillId);
    if (updatedSkill) {
      setSkills(skills.map(skill => 
        skill.id === skillId ? updatedSkill : skill
      ));
      showNotification('技能状态已更新');
    }
  };

  // Handle project action
  const handleProjectAction = (projectId, action) => {
    const project = projects.find(p => p.id === projectId);
    
    if (action === '打开') {
      setBrowsingProject(project);
      setActiveTab('filebrowser');
    } else {
      showNotification(`已执行操作: ${action} 项目 "${project.name}"`);
    }
  };

  // Handle onboarding completion
  const handleOnboardingComplete = () => {
    setShowOnboarding(false);
    localStorage.setItem('hasSeenOnboarding', 'true');
    showNotification('欢迎使用 Stigmergy 桌面应用！');
  };

  // Handle skill configuration
  const handleConfigureSkill = (skill) => {
    setConfiguringSkill(skill);
  };

  // Handle save skill configuration
  const handleSaveSkillConfig = (skillId, config) => {
    setSkills(skills.map(skill => 
      skill.id === skillId 
        ? { ...skill, config }
        : skill
    ));
    setConfiguringSkill(null);
    showNotification('技能配置已保存');
  };

  // Handle create new project
  const handleCreateProject = (newProject) => {
    setProjects(prev => [...prev, newProject]);
    setShowProjectWizard(false);
    showNotification(`项目 "${newProject.name}" 创建成功`, 'success');
  };

  return (
    <div className="app">
      {/* Notification */}
      {notification && (
        <div className={`notification notification-${notification.type}`}>
          {notification.message}
        </div>
      )}

      {/* Onboarding Flow */}
      {showOnboarding && (
        <OnboardingFlow onComplete={handleOnboardingComplete} />
      )}

      {/* Skill Configuration Modal */}
      {configuringSkill && (
        <SkillConfiguration
          skill={configuringSkill}
          onClose={() => setConfiguringSkill(null)}
          onSave={handleSaveSkillConfig}
        />
      )}

      {/* Project Creation Wizard */}
      {showProjectWizard && (
        <ProjectCreationWizard
          onClose={() => setShowProjectWizard(false)}
          onCreate={handleCreateProject}
        />
      )}

      {/* User Preferences */}
      {showPreferences && (
        <UserPreferences
          onClose={() => setShowPreferences(false)}
        />
      )}

      <header className="app-header">
        <div className="container d-flex justify-content-between align-items-center">
          <h1>AI 智能助手平台</h1>
          <nav>
            <button 
              className={`btn ${activeTab === 'dashboard' ? 'btn-primary' : 'btn-secondary'} mr-10`}
              onClick={() => setActiveTab('dashboard')}
            >
              仪表板
            </button>
            <button 
              className={`btn ${activeTab === 'agents' ? 'btn-primary' : 'btn-secondary'} mr-10`}
              onClick={() => setActiveTab('agents')}
            >
              智能体管理
            </button>
            <button 
              className={`btn ${activeTab === 'skills' ? 'btn-primary' : 'btn-secondary'} mr-10`}
              onClick={() => setActiveTab('skills')}
            >
              技能管理
            </button>
            <button 
              className={`btn ${activeTab === 'projects' ? 'btn-primary' : 'btn-secondary'} mr-10`}
              onClick={() => setActiveTab('projects')}
            >
              项目管理
            </button>
            <button 
              className={`btn ${activeTab === 'console' ? 'btn-primary' : 'btn-secondary'} mr-10`}
              onClick={() => setActiveTab('console')}
            >
              AI 助手
            </button>
            <button 
              className={`btn ${activeTab === 'filebrowser' && browsingProject ? 'btn-primary' : 'btn-secondary'} mr-10`}
              onClick={() => browsingProject && setActiveTab('filebrowser')}
              disabled={!browsingProject}
            >
              文件浏览器
            </button>
            <button 
              className={`btn ${activeTab === 'help' ? 'btn-primary' : 'btn-secondary'} mr-10`}
              onClick={() => setActiveTab('help')}
            >
              帮助
            </button>
            <button 
              className="btn btn-secondary"
              onClick={() => setShowPreferences(true)}
            >
              设置
            </button>
          </nav>
        </div>
      </header>

      <main className="app-main">
        <div className="container mt-20">
          {activeTab === 'dashboard' && <Dashboard />}
          {activeTab === 'agents' && <AgentsManagement />}
          {activeTab === 'skills' && (
            <SkillsManagement 
              skills={skills} 
              onToggleSkill={handleToggleSkill}
              onConfigureSkill={handleConfigureSkill}
              showNotification={showNotification}
            />
          )}
          {activeTab === 'projects' && (
            <ProjectManagement 
              projects={projects} 
              onProjectAction={handleProjectAction}
              onCreateProject={() => setShowProjectWizard(true)}
              showNotification={showNotification}
            />
          )}
          {activeTab === 'console' && <StigmergyConsole />}
          {activeTab === 'filebrowser' && browsingProject && (
            <FileBrowser 
              projectId={browsingProject.id}
              projectName={browsingProject.name}
            />
          )}
          {activeTab === 'help' && <HelpDocumentation />}
        </div>
      </main>

      {/* Help Button */}
      <button 
        className="help-button"
        onClick={() => setActiveTab('help')}
      >
        ?
      </button>
    </div>
  );
};

const Dashboard = () => {
  return (
    <div>
      <div className="dashboard-welcome">
        <h1>欢迎使用 AI 智能助手平台</h1>
        <p>集成多个AI助手的一站式智能工作平台</p>
      </div>
      
      <div className="dashboard-features">
        <div className="feature-card">
          <div className="feature-icon">🤖</div>
          <h3>智能体管理</h3>
          <p>查看和管理可用的AI智能体及其功能</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">🧠</div>
          <h3>技能管理</h3>
          <p>轻松管理各种AI技能，一键启用或禁用</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">📁</div>
          <h3>项目管理</h3>
          <p>创建和管理您的研究项目，组织文件更方便</p>
        </div>
        
        <div className="feature-card">
          <div className="feature-icon">💬</div>
          <h3>AI 助手</h3>
          <p>与多个AI助手对话，获取智能帮助</p>
        </div>
      </div>
      
      <div className="card">
        <h3>使用提示</h3>
        <ul>
          <li>所有操作都有明确的按钮和提示</li>
          <li>遇到问题时会有友好的错误提示</li>
          <li>点击右下角的帮助按钮可获取更多信息</li>
          <li>首次使用建议查看引导流程了解基本功能</li>
        </ul>
      </div>
    </div>
  );
};

const AgentsManagement = () => {
  const agents = UnifiedAgentService.getAgents();
  
  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-20">
        <h2>智能体管理</h2>
      </div>
      
      <div className="agents-grid">
        {agents.map(agent => (
          <div key={agent.id} className="card">
            <h3>{agent.name}</h3>
            <p>{agent.description}</p>
            <div className="mb-10">
              <span className={`status ${agent.status === '已启用' ? 'status-enabled' : 'status-disabled'}`}>
                {agent.status}
              </span>
            </div>
            <div className="capabilities">
              <h4>功能特性:</h4>
              <ul>
                {agent.capabilities.map((cap, index) => (
                  <li key={index}>{cap}</li>
                ))}
              </ul>
            </div>
            <div className="related-skills">
              <h4>相关技能:</h4>
              {(() => {
                const skills = UnifiedAgentService.getSkillsByAgent(agent.id);
                return skills.length > 0 ? (
                  <ul>
                    {skills.map(skill => (
                      <li key={skill.id}>{skill.name}</li>
                    ))}
                  </ul>
                ) : (
                  <p>暂无相关技能</p>
                );
              })()}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const SkillsManagement = ({ skills, onToggleSkill, onConfigureSkill, showNotification }) => {
  const [searchTerm, setSearchTerm] = useState('');

  const filteredSkills = skills.filter(skill =>
    skill.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    skill.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleAddSkill = () => {
    showNotification('添加技能功能即将推出');
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-20">
        <h2>技能管理</h2>
        <button className="btn btn-primary" onClick={handleAddSkill}>添加技能</button>
      </div>
      
      <div className="card mb-20">
        <div className="form-group">
          <label className="form-label">搜索技能:</label>
          <input
            type="text"
            className="form-input"
            placeholder="输入技能名称或描述..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>
      
      <div className="skills-grid">
        {filteredSkills.length > 0 ? (
          filteredSkills.map(skill => (
            <div key={skill.id} className="card">
              <h3>{skill.name}</h3>
              <p>{skill.description}</p>
              <div className="d-flex justify-content-between align-items-center">
                <span className={`status ${skill.status === '已启用' ? 'status-enabled' : 'status-disabled'}`}>
                  {skill.status}
                </span>
                <div>
                  <button 
                    className="btn btn-secondary mr-10"
                    onClick={() => onConfigureSkill(skill)}
                  >
                    配置
                  </button>
                  <button 
                    className={`btn ${skill.status === '已启用' ? 'btn-warning' : 'btn-success'}`}
                    onClick={() => onToggleSkill(skill.id)}
                  >
                    {skill.status === '已启用' ? '禁用' : '启用'}
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="card text-center">
            <p>未找到匹配的技能</p>
          </div>
        )}
      </div>
    </div>
  );
};

const ProjectManagement = ({ projects, onProjectAction, onCreateProject, showNotification }) => {
  const handleCreateProject = () => {
    onCreateProject();
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-20">
        <h2>项目管理</h2>
        <button className="btn btn-primary" onClick={handleCreateProject}>新建项目</button>
      </div>
      
      <div className="projects-list">
        {projects.length > 0 ? (
          projects.map(project => (
            <div key={project.id} className="card">
              <h3>{project.name}</h3>
              <p>路径: {project.path}</p>
              <div className="d-flex justify-content-between align-items-center">
                <span>最后修改: {project.lastModified}</span>
                <div>
                  <button 
                    className="btn btn-secondary mr-10"
                    onClick={() => onProjectAction(project.id, '打开')}
                  >
                    打开
                  </button>
                  <button 
                    className="btn btn-primary"
                    onClick={() => onProjectAction(project.id, '管理')}
                  >
                    管理
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="card text-center">
            <p>暂无项目</p>
            <button className="btn btn-primary mt-20" onClick={handleCreateProject}>
              创建您的第一个项目
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;