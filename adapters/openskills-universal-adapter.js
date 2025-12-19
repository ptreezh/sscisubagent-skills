/**
 * OpenSkills通用适配器
 * 解决不同CLI工具的技能兼容性问题
 */

const fs = require('fs-extra');
const path = require('path');
const yaml = require('yaml');

class OpenSkillsUniversalAdapter {
  constructor() {
    this.cliConfigs = {
      qwen: {
        skillsFile: 'QWEN.md',
        format: 'markdown-list',
        encoding: 'utf8',
        triggers: ['skill', '技能', '功能']
      },
      gemini: {
        skillsFile: 'GEMINI.md',
        format: 'yaml-frontmatter',
        encoding: 'utf8',
        triggers: ['skill', '技能', 'ability']
      },
      codebuddy: {
        skillsFile: 'CODEBUDDY.md',
        format: 'json-config',
        encoding: 'utf8',
        triggers: ['skill', '技能', 'tool']
      },
      codex: {
        skillsFile: 'CODEX.md',
        format: 'toml-config',
        encoding: 'utf8',
        triggers: ['skill', '技能', 'function']
      },
      qodercli: {
        skillsFile: 'QODER.md',
        format: 'markdown-table',
        encoding: 'utf8',
        triggers: ['skill', '技能', 'command']
      },
      iflow: {
        skillsFile: 'IFLOW.md',
        format: 'yaml-list',
        encoding: 'utf8',
        triggers: ['技能', '功能', '工具']
      }
    };
  }

  /**
   * 适配技能到指定CLI
   */
  async adaptSkillsToCLI(skillsDir, cliKey) {
    const config = this.cliConfigs[cliKey];
    if (!config) {
      throw new Error(`不支持的CLI: ${cliKey}`);
    }

    console.log(`🔄 适配技能到 ${cliKey}...`);

    // 1. 扫描所有技能
    const skills = await this.scanSkills(skillsDir);
    
    // 2. 转换技能格式
    const adaptedSkills = await this.convertSkills(skills, cliKey);
    
    // 3. 生成CLI特定的技能文件
    await this.generateSkillsFile(adaptedSkills, skillsDir, cliKey);
    
    // 4. 创建触发器配置
    await this.createTriggerConfig(skillsDir, cliKey);
    
    console.log(`✅ ${cliKey} 适配完成`);
  }

  /**
   * 扫描技能目录
   */
  async scanSkills(skillsDir) {
    const skills = [];

    async function scanDirectory(dir, prefix = '') {
      const items = await fs.readdir(dir);
      
      for (const item of items) {
        const itemPath = path.join(dir, item);
        const stat = await fs.stat(itemPath);
        
        if (stat.isDirectory()) {
          const skillFile = path.join(itemPath, 'SKILL.md');
          if (await fs.pathExists(skillFile)) {
            const skill = await this.parseSkillFile(skillFile, prefix + item);
            if (skill) skills.push(skill);
          }
          await scanDirectory(itemPath, prefix + item + '/');
        }
      }
    }

    await scanDirectory(skillsDir);
    return skills;
  }

  /**
   * 解析技能文件
   */
  async parseSkillFile(filePath, skillPath) {
    try {
      const content = await fs.readFile(filePath, 'utf8');
      
      // 提取YAML frontmatter
      const frontmatterMatch = content.match(/^---\n(.*?)\n---/s);
      if (!frontmatterMatch) return null;

      const frontmatter = yaml.parse(frontmatterMatch[1]);
      
      return {
        name: frontmatter.name || skillPath,
        description: frontmatter.description || '',
        path: skillPath,
        tags: frontmatter.tags || [],
        version: frontmatter.version || '1.0.0',
        filePath: filePath
      };
    } catch (error) {
      console.warn(`解析技能文件失败: ${filePath}`, error.message);
      return null;
    }
  }

  /**
   * 转换技能格式
   */
  async convertSkills(skills, cliKey) {
    const config = this.cliConfigs[cliKey];
    
    return skills.map(skill => {
      return {
        ...skill,
        cliName: this.generateCLIName(skill.name, cliKey),
        cliDescription: this.generateCLIDescription(skill.description, cliKey),
        triggers: this.generateTriggers(skill, config.triggers)
      };
    });
  }

  /**
   * 生成CLI特定的技能名称
   */
  generateCLIName(originalName, cliKey) {
    // 根据CLI特点调整名称
    const nameMap = {
      qwen: name => `${name} - Qwen技能`,
      gemini: name => `${name} - Gemini技能`,
      codebuddy: name => `${name} - CodeBuddy工具`,
      codex: name => `${name} - Codex功能`,
      qodercli: name => `${name} - Qoder命令`,
      iflow: name => name // 保持原名
    };

    return nameMap[cliKey] ? nameMap[cliKey](originalName) : originalName;
  }

  /**
   * 生成CLI特定的技能描述
   */
  generateCLIDescription(originalDesc, cliKey) {
    // 根据CLI特点调整描述
    const descMap = {
      qwen: desc => `${desc} (适用于Qwen CLI)`,
      gemini: desc => `${desc} (适用于Gemini CLI)`,
      codebuddy: desc => `${desc} (适用于CodeBuddy CLI)`,
      codex: desc => `${desc} (适用于Codex CLI)`,
      qodercli: desc => `${desc} (适用于QoderCLI)`,
      iflow: desc => desc // 保持原描述
    };

    return descMap[cliKey] ? descMap[cliKey](originalDesc) : originalDesc;
  }

  /**
   * 生成触发器关键词
   */
  generateTriggers(skill, baseTriggers) {
    const triggers = [...baseTriggers];
    
    // 从技能名称和描述中提取关键词
    const text = `${skill.name} ${skill.description}`.toLowerCase();
    const keywords = text.match(/[\u4e00-\u9fa5]+|[a-z]+/g) || [];
    
    triggers.push(...keywords.slice(0, 5)); // 限制关键词数量
    
    return [...new Set(triggers)]; // 去重
  }

  /**
   * 生成CLI特定的技能文件
   */
  async generateSkillsFile(skills, skillsDir, cliKey) {
    const config = this.cliConfigs[cliKey];
    const outputPath = path.join(skillsDir, config.skillsFile);

    let content;

    switch (config.format) {
      case 'markdown-list':
        content = this.generateMarkdownList(skills, cliKey);
        break;
      case 'yaml-frontmatter':
        content = this.generateYAMLFrontmatter(skills, cliKey);
        break;
      case 'json-config':
        content = this.generateJSONConfig(skills, cliKey);
        break;
      case 'toml-config':
        content = this.generateTOMLConfig(skills, cliKey);
        break;
      case 'markdown-table':
        content = this.generateMarkdownTable(skills, cliKey);
        break;
      case 'yaml-list':
        content = this.generateYAMLList(skills, cliKey);
        break;
      default:
        content = this.generateMarkdownList(skills, cliKey);
    }

    await fs.writeFile(outputPath, content, config.encoding);
  }

  /**
   * 生成Markdown列表格式
   */
  generateMarkdownList(skills, cliKey) {
    const sections = {
      coding: [],
      analysis: [],
      methodology: [],
      writing: [],
      other: []
    };

    // 分类技能
    skills.forEach(skill => {
      const category = this.categorizeSkill(skill);
      sections[category].push(skill);
    });

    let content = `# ${cliKey.toUpperCase()} 技能清单\n\n`;

    Object.entries(sections).forEach(([category, categorySkills]) => {
      if (categorySkills.length === 0) return;
      
      content += `## ${this.getCategoryName(category)}\n\n`;
      categorySkills.forEach(skill => {
        content += `- **${skill.cliName}**: ${skill.cliDescription}\n`;
        content += `  - 触发词: ${skill.triggers.join(', ')}\n`;
      });
      content += '\n';
    });

    return content;
  }

  /**
   * 生成YAML frontmatter格式
   */
  generateYAMLFrontmatter(skills, cliKey) {
    const yamlData = {
      name: `${cliKey} Skills`,
      version: '1.0.0',
      description: `${cliKey} CLI技能包`,
      skills: skills.map(skill => ({
        name: skill.cliName,
        description: skill.cliDescription,
        path: skill.path,
        triggers: skill.triggers
      }))
    };

    return `---
${yaml.stringify(yamlData)}
---

# ${cliKey.toUpperCase()} 技能说明

本配置文件包含所有可用的技能信息。

## 使用方法

在${cliKey}中提及相关任务时，系统会自动匹配相应的技能。

## 技能列表

${skills.map(skill => `
### ${skill.cliName}
${skill.cliDescription}

**触发词**: ${skill.triggers.join(', ')}
**路径**: ${skill.path}
`).join('')}
`;
  }

  /**
   * 生成JSON配置格式
   */
  generateJSONConfig(skills, cliKey) {
    const config = {
      version: '1.0.0',
      cli: cliKey,
      skills: skills.map(skill => ({
        id: skill.path.replace(/\//g, '-'),
        name: skill.cliName,
        description: skill.cliDescription,
        triggers: skill.triggers,
        metadata: {
          version: skill.version,
          tags: skill.tags
        }
      }))
    };

    return `# ${cliKey.toUpperCase()} 技能配置

\`\`\`json
${JSON.stringify(config, null, 2)}
\`\`\`

## 使用说明

将此配置添加到${cliKey}的配置文件中，即可启用技能识别功能。
`;
  }

  /**
   * 生成TOML配置格式
   */
  generateTOMLConfig(skills, cliKey) {
    let content = `# ${cliKey.toUpperCase()} 技能配置\n\n`;
    content += `[general]\n`;
    content += `version = "1.0.0"\n`;
    content += `cli = "${cliKey}"\n\n`;

    content += `[skills]\n`;
    skills.forEach(skill => {
      content += `\n[[skills.item]]\n`;
      content += `name = "${skill.cliName}"\n`;
      content += `description = "${skill.cliDescription.replace(/"/g, '\\"')}"\n`;
      content += `path = "${skill.path}"\n`;
      content += `triggers = [${skill.triggers.map(t => `"${t}"`).join(', ')}]\n`;
    });

    return content;
  }

  /**
   * 生成Markdown表格格式
   */
  generateMarkdownTable(skills, cliKey) {
    let content = `# ${cliKey.toUpperCase()} 技能表格\n\n`;
    content += '| 技能名称 | 描述 | 触发词 | 路径 |\n';
    content += '|---------|------|--------|------|\n';

    skills.forEach(skill => {
      content += `| ${skill.cliName} | ${skill.cliDescription} | ${skill.triggers.join(', ')} | ${skill.path} |\n`;
    });

    content += `\n## 使用说明\n\n`;
    content += `在${cliKey}中使用触发词来激活相应的技能。`;

    return content;
  }

  /**
   * 生成YAML列表格式
   */
  generateYAMLList(skills, cliKey) {
    const yamlData = {
      skills: skills.map(skill => ({
        name: skill.cliName,
        description: skill.cliDescription,
        triggers: skill.triggers,
        path: skill.path
      }))
    };

    return `# ${cliKey.toUpperCase()} 技能列表

\`\`\`yaml
${yaml.stringify(yamlData)}
\`\`\`

## 技能说明

${skills.map(skill => `- **${skill.cliName}**: ${skill.cliDescription}`).join('\n')}
`;
  }

  /**
   * 创建触发器配置
   */
  async createTriggerConfig(skillsDir, cliKey) {
    const configPath = path.join(skillsDir, 'triggers.json');
    
    const config = {
      cli: cliKey,
      version: '1.0.0',
      lastUpdated: new Date().toISOString(),
      triggers: {}
    };

    // 扫描所有技能，提取触发器
    const skills = await this.scanSkills(skillsDir);
    skills.forEach(skill => {
      config.triggers[skill.path] = {
        name: skill.name,
        description: skill.description,
        keywords: skill.name.toLowerCase().split(/[\s\-_]+/),
        patterns: this.generatePatterns(skill)
      };
    });

    await fs.writeFile(configPath, JSON.stringify(config, null, 2));
  }

  /**
   * 生成匹配模式
   */
  generatePatterns(skill) {
    const patterns = [];
    
    // 基于技能名称生成模式
    const nameWords = skill.name.toLowerCase().split(/[\s\-_]+/);
    patterns.push(...nameWords.map(word => `\\b${word}\\b`));
    
    // 基于描述生成模式
    const descWords = skill.description.toLowerCase().match(/[\u4e00-\u9fa5]+|[a-z]+/g) || [];
    patterns.push(...descWords.slice(0, 3).map(word => `\\b${word}\\b`));
    
    return [...new Set(patterns)];
  }

  /**
   * 技能分类
   */
  categorizeSkill(skill) {
    const name = skill.name.toLowerCase();
    const desc = skill.description.toLowerCase();
    
    if (name.includes('coding') || name.includes('编码') || name.includes('open') || name.includes('axial')) {
      return 'coding';
    } else if (name.includes('analysis') || name.includes('分析') || name.includes('network') || name.includes('centrality')) {
      return 'analysis';
    } else if (name.includes('methodology') || name.includes('方法论') || name.includes('conflict') || name.includes('validity')) {
      return 'methodology';
    } else if (name.includes('writing') || name.includes('写作') || name.includes('citation') || name.includes('literature')) {
      return 'writing';
    } else {
      return 'other';
    }
  }

  /**
   * 获取分类名称
   */
  getCategoryName(category) {
    const names = {
      coding: '编码技能',
      analysis: '分析技能',
      methodology: '方法论技能',
      writing: '写作技能',
      other: '其他技能'
    };
    return names[category] || '其他技能';
  }
}

module.exports = OpenSkillsUniversalAdapter;