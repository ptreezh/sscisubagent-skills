// Project Templates Service
// This module provides project templates for quick project creation

class ProjectTemplatesService {
  /**
   * Get all available project templates
   * @returns {Array} - Array of template objects
   */
  getTemplates() {
    return [
      {
        id: 'research-project',
        name: '学术研究项目',
        description: '适用于学术研究的完整项目结构，包含文献、数据、分析和报告目录',
        structure: [
          { name: 'literature', type: 'directory' },
          { name: 'data', type: 'directory' },
          { name: 'analysis', type: 'directory' },
          { name: 'reports', type: 'directory' },
          { name: 'README.md', type: 'file', content: '# 学术研究项目\n\n## 项目概述\n\n## 目录结构\n\n- literature: 文献资料\n- data: 原始数据\n- analysis: 分析结果\n- reports: 研究报告' },
          { name: 'project-notes.txt', type: 'file', content: '项目笔记\n========\n\n- 项目启动日期:\n- 研究目标:\n- 关键里程碑:' }
        ]
      },
      {
        id: 'literature-review',
        name: '文献综述项目',
        description: '专门用于文献综述的项目模板，包含文献收集、整理和分析目录',
        structure: [
          { name: 'collected-literature', type: 'directory' },
          { name: 'organized-literature', type: 'directory' },
          { name: 'analysis', type: 'directory' },
          { name: 'synthesis', type: 'directory' },
          { name: 'README.md', type: 'file', content: '# 文献综述项目\n\n## 项目目标\n\n## 工作流程\n\n1. 文献收集\n2. 文献整理\n3. 内容分析\n4. 综合撰写' },
          { name: 'review-plan.md', type: 'file', content: '# 文献综述计划\n\n## 研究问题\n\n## 搜索策略\n\n## 筛选标准\n\n## 数据提取\n\n## 质量评估' }
        ]
      },
      {
        id: 'data-analysis',
        name: '数据分析项目',
        description: '用于数据分析的项目模板，包含数据、脚本、结果和可视化目录',
        structure: [
          { name: 'raw-data', type: 'directory' },
          { name: 'processed-data', type: 'directory' },
          { name: 'scripts', type: 'directory' },
          { name: 'results', type: 'directory' },
          { name: 'visualizations', type: 'directory' },
          { name: 'README.md', type: 'file', content: '# 数据分析项目\n\n## 项目描述\n\n## 分析目标\n\n## 数据来源\n\n## 方法论' },
          { name: 'analysis-plan.md', type: 'file', content: '# 数据分析计划\n\n## 数据预处理\n\n## 探索性分析\n\n## 统计检验\n\n## 结果解释' }
        ]
      },
      {
        "id": "empty-project",
        "name": "空项目",
        "description": "空白项目模板，只包含基本的README文件",
        "structure": [
          { "name": "README.md", "type": "file", "content": "# 新项目\n\n## 项目描述\n\n在此添加项目描述..." }
        ]
      }
    ];
  }

  /**
   * Get a specific template by ID
   * @param {string} templateId - The ID of the template to retrieve
   * @returns {Object|null} - Template object or null if not found
   */
  getTemplateById(templateId) {
    const templates = this.getTemplates();
    return templates.find(template => template.id === templateId) || null;
  }

  /**
   * Create project structure from template
   * @param {string} projectId - The ID of the project
   * @param {string} projectName - The name of the project
   * @param {string} templateId - The ID of the template to use
   * @returns {Promise<Object>} - Result of project creation
   */
  async createProjectFromTemplate(projectId, projectName, templateId) {
    try {
      const template = this.getTemplateById(templateId);
      
      if (!template) {
        return {
          success: false,
          error: `Template with ID ${templateId} not found`
        };
      }

      // In a real implementation, this would create the actual directory structure
      // For now, we'll just simulate the creation
      await new Promise(resolve => setTimeout(resolve, 1000));

      return {
        success: true,
        projectId,
        projectName,
        templateId,
        templateName: template.name,
        message: `Project "${projectName}" created successfully using template "${template.name}"`
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }
}

// Export a singleton instance
module.exports = new ProjectTemplatesService();