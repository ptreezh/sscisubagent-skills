import React, { useState } from 'react';

const HelpDocumentation = () => {
  const [activeSection, setActiveSection] = useState('getting-started');

  const sections = [
    { id: 'getting-started', title: '入门指南' },
    { id: 'skills', title: '技能管理' },
    { id: 'projects', title: '项目管理' },
    { id: 'console', title: '控制台使用' },
    { id: 'troubleshooting', title: '故障排除' }
  ];

  const helpContent = {
    'getting-started': {
      title: '入门指南',
      content: (
        <div>
          <h3>欢迎使用 Stigmergy 桌面应用</h3>
          <p>这是一个为技术小白用户设计的图形化界面，让您无需接触命令行就能使用强大的 Stigmergy 功能。</p>
          
          <h4>首次使用步骤</h4>
          <ol>
            <li><strong>查看引导流程</strong> - 首次打开应用时，系统会自动显示引导流程，帮助您快速了解基本功能</li>
            <li><strong>探索界面</strong> - 熟悉顶部导航栏中的各个功能模块：仪表板、技能管理、项目管理、控制台</li>
            <li><strong>启用技能</strong> - 在"技能管理"页面中，启用您需要的AI技能</li>
            <li><strong>创建项目</strong> - 在"项目管理"页面中，创建您的第一个研究项目</li>
            <li><strong>开始工作</strong> - 使用控制台或直接在项目中使用AI技能</li>
          </ol>
          
          <h4>界面概览</h4>
          <ul>
            <li><strong>仪表板</strong> - 应用主界面，提供功能概览和快速入口</li>
            <li><strong>技能管理</strong> - 管理所有可用的AI技能</li>
            <li><strong>项目管理</strong> - 创建和管理您的研究项目</li>
            <li><strong>控制台</strong> - 直接执行 Stigmergy 命令</li>
            <li><strong>文件浏览器</strong> - 浏览和管理项目文件</li>
          </ul>
        </div>
      )
    },
    'skills': {
      title: '技能管理',
      content: (
        <div>
          <h3>技能管理功能</h3>
          <p>技能是预先编写好的功能模块，可以帮助您完成特定任务。</p>
          
          <h4>查看技能列表</h4>
          <p>在"技能管理"页面中，您可以查看所有已安装的技能，包括技能名称、描述和当前状态。</p>
          
          <h4>启用/禁用技能</h4>
          <p>点击技能卡片上的"启用"或"禁用"按钮，可以控制技能是否可用。</p>
          
          <h4>配置技能</h4>
          <p>点击"配置"按钮可以打开技能配置窗口，设置技能的参数和优先级。</p>
          
          <h4>搜索技能</h4>
          <p>使用搜索框可以根据技能名称或描述快速查找特定技能。</p>
        </div>
      )
    },
    'projects': {
      title: '项目管理',
      content: (
        <div>
          <h3>项目管理功能</h3>
          <p>项目是您工作的文件夹，包含所有相关的文档和数据。</p>
          
          <h4>创建项目</h4>
          <p>点击"新建项目"按钮，按照向导创建新的研究项目。</p>
          
          <h4>打开项目</h4>
          <p>在项目列表中点击"打开"按钮，进入项目文件浏览器。</p>
          
          <h4>管理项目</h4>
          <p>点击"管理"按钮可以查看项目详情和设置。</p>
          
          <h4>文件浏览器</h4>
          <p>在文件浏览器中，您可以：</p>
          <ul>
            <li>浏览项目文件和文件夹</li>
            <li>创建新文件</li>
            <li>删除文件</li>
            <li>导航到子文件夹</li>
          </ul>
        </div>
      )
    },
    'console': {
      title: '控制台使用',
      content: (
        <div>
          <h3>控制台功能</h3>
          <p>控制台允许您直接执行 Stigmergy 命令，查看实时输出。</p>
          
          <h4>执行命令</h4>
          <p>在命令输入框中输入 Stigmergy 命令，按回车键或点击"执行"按钮。</p>
          
          <h4>常用命令</h4>
          <ul>
            <li><code>stigmergy status</code> - 查看 Stigmergy 状态</li>
            <li><code>stigmergy skill list</code> - 列出所有技能</li>
            <li><code>stigmergy skill install &lt;skill-name&gt;</code> - 安装技能</li>
            <li><code>stigmergy skill remove &lt;skill-name&gt;</code> - 移除技能</li>
            <li><code>stigmergy use &lt;cli-name&gt; "&lt;prompt&gt;"</code> - 使用指定 CLI</li>
          </ul>
          
          <h4>命令历史</h4>
          <p>控制台会记住您执行过的命令，点击历史命令可以快速重新执行。</p>
          
          <h4>清空输出</h4>
          <p>点击"清空输出"按钮可以清除当前的命令输出显示。</p>
        </div>
      )
    },
    'troubleshooting': {
      title: '故障排除',
      content: (
        <div>
          <h3>常见问题和解决方案</h3>
          
          <h4>技能无法启用</h4>
          <p><strong>问题</strong>: 点击"启用"按钮后技能状态没有改变</p>
          <p><strong>解决方案</strong>:</p>
          <ul>
            <li>检查 Stigmergy CLI 是否正确安装</li>
            <li>重启应用程序</li>
            <li>查看控制台输出了解具体错误信息</li>
          </ul>
          
          <h4>项目文件无法显示</h4>
          <p><strong>问题</strong>: 文件浏览器中项目文件列表为空</p>
          <p><strong>解决方案</strong>:</p>
          <ul>
            <li>检查项目路径是否正确</li>
            <li>确认您有访问该项目文件夹的权限</li>
            <li>刷新文件浏览器</li>
          </ul>
          
          <h4>命令执行失败</h4>
          <p><strong>问题</strong>: 在控制台中执行命令时出现错误</p>
          <p><strong>解决方案</strong>:</p>
          <ul>
            <li>检查命令语法是否正确</li>
            <li>确认 Stigmergy CLI 已正确安装</li>
            <li>查看错误信息中的具体提示</li>
            <li>尝试在系统终端中手动执行相同命令</li>
          </ul>
          
          <h4>应用运行缓慢</h4>
          <p><strong>问题</strong>: 应用程序响应缓慢</p>
          <p><strong>解决方案</strong>:</p>
          <ul>
            <li>关闭不必要的技能</li>
            <li>减少同时打开的项目数量</li>
            <li>重启应用程序</li>
            <li>检查系统资源使用情况</li>
          </ul>
        </div>
      )
    }
  };

  return (
    <div className="help-documentation">
      <div className="container">
        <h1>帮助文档和用户指南</h1>
        
        <div className="help-content">
          <div className="help-sidebar">
            <nav>
              <ul>
                {sections.map(section => (
                  <li key={section.id}>
                    <button
                      className={`btn btn-link ${activeSection === section.id ? 'active' : ''}`}
                      onClick={() => setActiveSection(section.id)}
                    >
                      {section.title}
                    </button>
                  </li>
                ))}
              </ul>
            </nav>
          </div>
          
          <div className="help-main">
            <div className="card">
              <h2>{helpContent[activeSection].title}</h2>
              {helpContent[activeSection].content}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HelpDocumentation;