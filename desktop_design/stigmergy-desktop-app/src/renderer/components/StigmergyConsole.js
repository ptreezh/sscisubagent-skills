import React, { useState, useEffect } from 'react';
import UnifiedAgentService from '../services/UnifiedAgentService';

const StigmergyConsole = () => {
  const [command, setCommand] = useState('');
  const [output, setOutput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const [selectedAgent, setSelectedAgent] = useState('stigmergy');

  // Load command history from localStorage
  useEffect(() => {
    const savedHistory = localStorage.getItem('stigmergyCommandHistory');
    if (savedHistory) {
      setHistory(JSON.parse(savedHistory));
    }
  }, []);

  // Save command history to localStorage
  useEffect(() => {
    localStorage.setItem('stigmergyCommandHistory', JSON.stringify(history));
  }, [history]);

  const executeCommand = async () => {
    if (!command.trim()) return;

    setIsLoading(true);
    setOutput('执行中...');

    try {
      // Use the unified service to execute the task
      const response = await UnifiedAgentService.executeTask(selectedAgent, command);
      
      if (response.success) {
        setOutput(response.stdout || '命令执行成功');
        // Add to history
        setHistory(prev => [...prev.slice(-9), command]); // Keep only last 10 commands
      } else {
        setOutput(`错误: ${response.error}\nStderr: ${response.stderr}`);
      }
    } catch (error) {
      setOutput(`执行失败: ${error.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !isLoading) {
      executeCommand();
    }
  };

  const clearOutput = () => {
    setOutput('');
  };

  const loadCommandFromHistory = (cmd) => {
    setCommand(cmd);
  };

  // Get available agents for the dropdown
  const agents = UnifiedAgentService.getAgents();

  return (
    <div className="stigmergy-console card">
      <div className="d-flex justify-content-between align-items-center mb-20">
        <h2>AI 助手控制台</h2>
        <button className="btn btn-secondary" onClick={clearOutput}>清空输出</button>
      </div>

      {/* Agent selection */}
      <div className="form-group mb-20">
        <label className="form-label">选择 AI 助手:</label>
        <select
          className="form-select"
          value={selectedAgent}
          onChange={(e) => setSelectedAgent(e.target.value)}
        >
          {agents.map(agent => (
            <option key={agent.id} value={agent.id}>{agent.name}</option>
          ))}
        </select>
      </div>

      {/* Command input */}
      <div className="form-group">
        <label className="form-label">向 AI 助手提问:</label>
        <div className="d-flex">
          <input
            type="text"
            className="form-input"
            placeholder="输入您的问题或指令..."
            value={command}
            onChange={(e) => setCommand(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={isLoading}
          />
          <button 
            className="btn btn-primary ml-10"
            onClick={executeCommand}
            disabled={isLoading || !command.trim()}
          >
            {isLoading ? '执行中...' : '执行'}
          </button>
        </div>
      </div>

      {/* Command history */}
      {history.length > 0 && (
        <div className="mb-20">
          <label className="form-label">最近问题:</label>
          <div className="command-history">
            {history.map((cmd, index) => (
              <span 
                key={index} 
                className="command-history-item"
                onClick={() => loadCommandFromHistory(cmd)}
              >
                {cmd}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Output display */}
      <div className="form-group">
        <label className="form-label">助手回复:</label>
        <div className="console-output">
          <pre>{output}</pre>
        </div>
      </div>

      {/* Help section */}
      <div className="card mt-20">
        <h3>使用说明</h3>
        <ul>
          <li>选择合适的 AI 助手来处理您的任务</li>
          <li>直接用自然语言描述您的需求</li>
          <li>系统会自动将任务分配给最合适的助手</li>
          <li>历史记录可以帮助您快速重复之前的询问</li>
        </ul>
      </div>
    </div>
  );
};

export default StigmergyConsole;