// Unified Agent Service
// This module provides a unified interface for all AI agents and skills
// Abstracting away the underlying CLI tools from the end user

const EnhancedStigmergyService = require('./EnhancedStigmergyService');

class UnifiedAgentService {
  constructor() {
    // Define available agents with their capabilities
    this.agents = [
      {
        id: 'stigmergy',
        name: 'Stigmergy 协调器',
        description: '智能协调多个AI工具协同工作',
        capabilities: ['多工具协调', '智能路由', '任务分发'],
        status: '已启用'
      },
      {
        id: 'claude',
        name: 'Claude 助手',
        description: '强大的语言理解和生成能力',
        capabilities: ['文本生成', '代码编写', '分析推理'],
        status: '已启用'
      },
      {
        id: 'qwen',
        name: '通义千问',
        description: '阿里巴巴的超大规模语言模型',
        capabilities: ['多语言支持', '知识问答', '创意写作'],
        status: '已启用'
      },
      {
        id: 'iflow',
        name: 'iFlow 代理',
        description: '流程自动化和任务执行',
        capabilities: ['流程管理', '任务自动化', '工作流执行'],
        status: '已启用'
      },
      {
        id: 'gemini',
        name: 'Gemini 助手',
        description: 'Google的多功能AI助手',
        capabilities: ['多模态处理', '数据分析', '逻辑推理'],
        status: '已启用'
      },
      {
        id: 'codex',
        name: 'Codex 编程专家',
        description: '专业的编程和代码审查助手',
        capabilities: ['代码生成', '代码审查', '调试辅助'],
        status: '已启用'
      }
    ];

    // Define available skills grouped by category
    this.skillCategories = [
      {
        id: 'research',
        name: '学术研究',
        description: '支持学术研究和文献分析的技能',
        skills: [
          {
            id: 'literature-review',
            name: '文献综述专家',
            description: '协助进行学术文献综述和分析',
            agent: 'claude',
            status: '已启用'
          },
          {
            id: 'grounded-theory',
            name: '扎根理论专家',
            description: '支持扎根理论编码和分析',
            agent: 'qwen',
            status: '已启用'
          },
          {
            id: 'academic-writing',
            name: '学术写作助手',
            description: '协助撰写学术论文和报告',
            agent: 'gemini',
            status: '已启用'
          }
        ]
      },
      {
        id: 'analysis',
        name: '数据分析',
        description: '支持各种数据分析和可视化的技能',
        skills: [
          {
            id: 'social-network',
            name: '社会网络分析专家',
            description: '进行社会网络分析和可视化',
            agent: 'iflow',
            status: '未启用'
          },
          {
            id: 'statistical-analysis',
            name: '统计分析专家',
            description: '执行各种统计分析方法',
            agent: 'stigmergy',
            status: '已启用'
          }
        ]
      },
      {
        id: 'programming',
        name: '编程开发',
        description: '支持编程和软件开发的技能',
        skills: [
          {
            id: 'code-review',
            name: '代码审查专家',
            description: '专业代码审查和改进建议',
            agent: 'codex',
            status: '已启用'
          },
          {
            id: 'debug-assistant',
            name: '调试助手',
            description: '帮助定位和修复代码问题',
            agent: 'claude',
            status: '已启用'
          }
        ]
      }
    ];
  }

  /**
   * Get all available agents
   * @returns {Array} List of available agents
   */
  getAgents() {
    return this.agents;
  }

  /**
   * Get agent by ID
   * @param {string} agentId - Agent ID
   * @returns {Object|null} Agent object or null if not found
   */
  getAgentById(agentId) {
    return this.agents.find(agent => agent.id === agentId) || null;
  }

  /**
   * Get all skill categories
   * @returns {Array} List of skill categories
   */
  getSkillCategories() {
    return this.skillCategories;
  }

  /**
   * Get all skills
   * @returns {Array} List of all skills
   */
  getAllSkills() {
    return this.skillCategories.flatMap(category => category.skills);
  }

  /**
   * Get skill by ID
   * @param {string} skillId - Skill ID
   * @returns {Object|null} Skill object or null if not found
   */
  getSkillById(skillId) {
    for (const category of this.skillCategories) {
      const skill = category.skills.find(s => s.id === skillId);
      if (skill) return skill;
    }
    return null;
  }

  /**
   * Get skills by agent
   * @param {string} agentId - Agent ID
   * @returns {Array} List of skills for the agent
   */
  getSkillsByAgent(agentId) {
    return this.getAllSkills().filter(skill => skill.agent === agentId);
  }

  /**
   * Get skills by category
   * @param {string} categoryId - Category ID
   * @returns {Array} List of skills in the category
   */
  getSkillsByCategory(categoryId) {
    const category = this.skillCategories.find(cat => cat.id === categoryId);
    return category ? category.skills : [];
  }

  /**
   * Toggle skill status
   * @param {string} skillId - Skill ID
   * @returns {Object|null} Updated skill or null if not found
   */
  toggleSkillStatus(skillId) {
    for (const category of this.skillCategories) {
      const skill = category.skills.find(s => s.id === skillId);
      if (skill) {
        skill.status = skill.status === '已启用' ? '未启用' : '已启用';
        return skill;
      }
    }
    return null;
  }

  /**
   * Execute a task using the appropriate agent
   * @param {string} taskId - Task ID or description
   * @param {string} prompt - User prompt
   * @param {Object} options - Additional options
   * @returns {Promise<Object>} Result of the task execution
   */
  async executeTask(taskId, prompt, options = {}) {
    try {
      // For simplicity, we'll use Stigmergy's smart routing
      // In a real implementation, this would route to the appropriate agent
      const result = await EnhancedStigmergyService.executeCommand('call', [prompt]);
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Execute a skill
   * @param {string} skillId - Skill ID
   * @param {string} prompt - User prompt
   * @param {Object} options - Additional options
   * @returns {Promise<Object>} Result of the skill execution
   */
  async executeSkill(skillId, prompt, options = {}) {
    try {
      // Find the skill to get its associated agent
      const skill = this.getSkillById(skillId);
      if (!skill) {
        return {
          success: false,
          error: `未找到技能: ${skillId}`
        };
      }

      // Route to the appropriate agent
      const agent = this.getAgentById(skill.agent);
      if (!agent) {
        return {
          success: false,
          error: `未找到代理: ${skill.agent}`
        };
      }

      // For now, we'll use Stigmergy's cross-CLI calling
      // In a real implementation, this would directly call the appropriate CLI
      const result = await EnhancedStigmergyService.executeCommand('use', [agent.id, prompt]);
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Install a skill
   * @param {string} skillId - Skill ID
   * @returns {Promise<Object>} Result of the installation
   */
  async installSkill(skillId) {
    try {
      // In a real implementation, this would install the appropriate skill
      // for the specific CLI tool
      const result = await EnhancedStigmergyService.installSkill(skillId);
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * Remove a skill
   * @param {string} skillId - Skill ID
   * @returns {Promise<Object>} Result of the removal
   */
  async removeSkill(skillId) {
    try {
      // In a real implementation, this would remove the appropriate skill
      // for the specific CLI tool
      const result = await EnhancedStigmergyService.removeSkill(skillId);
      return result;
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
}

// Export a singleton instance
module.exports = new UnifiedAgentService();