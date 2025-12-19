/**
 * Claude自动检测和部署脚本
 * 自动检测Claude Code安装位置并部署subagent和skills
 */

const fs = require('fs-extra');
const path = require('path');
const os = require('os');
const chalk = require('chalk');
const ora = require('ora');

class ClaudeAutoDeployer {
  constructor() {
    this.packagePath = path.resolve(__dirname, '..');
    this.homeDir = os.homedir();
    this.possibleClaudePaths = this._getPossibleClaudePaths();
  }

  /**
   * 获取可能的Claude安装路径
   */
  _getPossibleClaudePaths() {
    const platform = os.platform();
    const paths = [];

    if (platform === 'darwin') {
      // macOS
      paths.push(
        path.join(this.homeDir, 'Library', 'Application Support', 'Claude'),
        path.join(this.homeDir, '.claude'),
        '/Applications/Claude.app/Contents/Resources',
        '/usr/local/claude'
      );
    } else if (platform === 'win32') {
      // Windows
      paths.push(
        path.join(this.homeDir, 'AppData', 'Roaming', 'Claude'),
        path.join(this.homeDir, '.claude'),
        'C:\\Program Files\\Claude',
        'C:\\Program Files (x86)\\Claude',
        path.join(process.env.LOCALAPPDATA || '', 'Claude')
      );
    } else {
      // Linux
      paths.push(
        path.join(this.homeDir, '.claude'),
        path.join(this.homeDir, '.config', 'claude'),
        '/usr/local/claude',
        '/opt/claude'
      );
    }

    return paths;
  }

  /**
   * 检测Claude安装目录
   */
  async detectClaude() {
    console.log(chalk.blue('🔍 检测Claude Code安装...'));

    for (const claudePath of this.possibleClaudePaths) {
      try {
        // 检查是否存在Claude相关文件
        const possibleIndicators = [
          'claude.exe',
          'claude',
          'Claude.exe',
          'config.json',
          'settings.json'
        ];

        for (const indicator of possibleIndicators) {
          const indicatorPath = path.join(claudePath, indicator);
          if (await fs.pathExists(indicatorPath)) {
            console.log(chalk.green(`✅ 找到Claude安装: ${claudePath}`));
            return claudePath;
          }
        }

        // 检查是否是.claude目录（即使没有可执行文件）
        if (claudePath.endsWith('.claude') && await fs.pathExists(claudePath)) {
          console.log(chalk.yellow(`⚠️  找到Claude配置目录: ${claudePath}`));
          return claudePath;
        }
      } catch (error) {
        // 继续检查下一个路径
      }
    }

    // 检查PATH环境变量
    try {
      const { execSync } = require('child_process');
      const claudeVersion = execSync('claude --version', { encoding: 'utf8', timeout: 5000 });
      if (claudeVersion) {
        console.log(chalk.green('✅ 通过PATH找到Claude命令'));
        return path.join(this.homeDir, '.claude'); // 返回默认配置目录
      }
    } catch (error) {
      // Claude命令不可用
    }

    console.log(chalk.red('❌ 未找到Claude Code安装'));
    return null;
  }

  /**
   * 创建Claude配置目录结构
   */
  async createClaudeStructure(claudePath) {
    const spinner = ora('创建Claude配置目录...').start();
    
    try {
      // 确定配置目录
      const configDir = claudePath.endsWith('.claude') ? claudePath : path.join(this.homeDir, '.claude');
      
      // 创建必要的目录
      const dirsToCreate = [
        path.join(configDir, 'skills'),
        path.join(configDir, 'agents'),
        path.join(configDir, 'config')
      ];

      for (const dir of dirsToCreate) {
        await fs.ensureDir(dir);
      }

      spinner.succeed('Claude配置目录创建完成');
      return configDir;
    } catch (error) {
      spinner.fail('创建配置目录失败');
      throw error;
    }
  }

  /**
   * 部署skills到Claude
   */
  async deploySkills(configDir) {
    const spinner = ora('部署Skills到Claude...').start();
    
    try {
      const skillsSourceDir = path.join(this.packagePath, 'skills');
      const skillsTargetDir = path.join(configDir, 'skills');

      if (!(await fs.pathExists(skillsSourceDir))) {
        throw new Error('源skills目录不存在');
      }

      // 复制所有skills
      await fs.copy(skillsSourceDir, skillsTargetDir, {
        overwrite: true,
        filter: (src) => {
          // 过滤掉不需要的文件
          const basename = path.basename(src);
          return !basename.startsWith('.') && basename !== '__pycache__';
        }
      });

      // 创建skills索引文件
      await this.createSkillsIndex(skillsTargetDir);

      spinner.succeed(`Skills部署完成: ${skillsTargetDir}`);
    } catch (error) {
      spinner.fail('Skills部署失败');
      throw error;
    }
  }

  /**
   * 部署agents到Claude
   */
  async deployAgents(configDir) {
    const spinner = ora('部署Subagents到Claude...').start();
    
    try {
      const agentsSourceDir = path.join(this.packagePath, 'agents');
      const agentsTargetDir = path.join(configDir, 'agents');

      if (!(await fs.pathExists(agentsSourceDir))) {
        throw new Error('源agents目录不存在');
      }

      // 复制所有agents
      await fs.copy(agentsSourceDir, agentsTargetDir, {
        overwrite: true,
        filter: (src) => {
          const basename = path.basename(src);
          return !basename.startsWith('.') && !basename.includes('-v2');
        }
      });

      // 创建agents索引文件
      await this.createAgentsIndex(agentsTargetDir);

      spinner.succeed(`Subagents部署完成: ${agentsTargetDir}`);
    } catch (error) {
      spinner.fail('Subagents部署失败');
      throw error;
    }
  }

  /**
   * 创建skills索引文件
   */
  async createSkillsIndex(skillsDir) {
    const skills = [];
    
    async function scanSkills(dir, prefix = '') {
      const items = await fs.readdir(dir);
      
      for (const item of items) {
        const itemPath = path.join(dir, item);
        const stat = await fs.stat(itemPath);
        
        if (stat.isDirectory()) {
          const skillFile = path.join(itemPath, 'SKILL.md');
          if (await fs.pathExists(skillFile)) {
            const content = await fs.readFile(skillFile, 'utf8');
            const match = content.match(/^---\nname:\s*(.+)\ndescription:\s*(.+)/m);
            
            if (match) {
              skills.push({
                name: match[1],
                description: match[2],
                path: prefix + item
              });
            }
          }
          await scanSkills(itemPath, prefix + item + '/');
        }
      }
    }
    
    await scanSkills(skillsDir);
    
    const indexContent = `# Claude Skills Index

本目录包含以下技能：

${skills.map(skill => `- **${skill.name}**: ${skill.description}`).join('\n')}

## 使用方式

在Claude中直接提及相关任务，系统会自动加载相应技能。

---
*自动生成于 ${new Date().toISOString()}*
`;
    
    await fs.writeFile(path.join(skillsDir, 'README.md'), indexContent);
  }

  /**
   * 创建agents索引文件
   */
  async createAgentsIndex(agentsDir) {
    const agents = [];
    const items = await fs.readdir(agentsDir);
    
    for (const item of items) {
      if (item.endsWith('.md') && !item.includes('-v2')) {
        const agentPath = path.join(agentsDir, item);
        const content = await fs.readFile(agentPath, 'utf8');
        const match = content.match(/^---\nname:\s*(.+)\ndescription:\s*(.+)/m);
        
        if (match) {
          agents.push({
            name: match[1],
            description: match[2],
            file: item
          });
        }
      }
    }
    
    const indexContent = `# Claude Subagents Index

本目录包含以下智能体：

${agents.map(agent => `- **${agent.name}**: ${agent.description}`).join('\n')}

## 使用方式

在Claude中提及相关领域的任务，系统会自动选择合适的智能体。

---
*自动生成于 ${new Date().toISOString()}*
`;
    
    await fs.writeFile(path.join(agentsDir, 'README.md'), indexContent);
  }

  /**
   * 创建Claude配置文件
   */
  async createClaudeConfig(configDir) {
    const configPath = path.join(configDir, 'config', 'ssci-skills-config.json');
    
    const config = {
      name: 'SSCI Subagent Skills',
      version: require('../package.json').version,
      description: '中文社会科学研究AI技能包',
      installedAt: new Date().toISOString(),
      skillsPath: path.join(configDir, 'skills'),
      agentsPath: path.join(configDir, 'agents'),
      autoUpdate: true
    };
    
    await fs.writeFile(configPath, JSON.stringify(config, null, 2));
  }

  /**
   * 执行自动部署
   */
  async deploy() {
    console.log(chalk.cyan('\n🚀 SSCI Skills - Claude自动部署开始\n'));

    try {
      // 1. 检测Claude
      const claudePath = await this.detectClaude();
      if (!claudePath) {
        console.log(chalk.yellow('\n⚠️  未检测到Claude Code，尝试创建默认配置...'));
        claudePath = path.join(this.homeDir, '.claude');
      }

      // 2. 创建配置目录
      const configDir = await this.createClaudeStructure(claudePath);

      // 3. 部署skills
      await this.deploySkills(configDir);

      // 4. 部署agents
      await this.deployAgents(configDir);

      // 5. 创建配置文件
      await this.createClaudeConfig(configDir);

      console.log(chalk.green('\n✅ 部署完成！'));
      console.log(chalk.cyan(`📁 配置目录: ${configDir}`));
      console.log(chalk.cyan('🎯 现在可以在Claude中使用所有SSCI技能和智能体了！\n'));

      return true;
    } catch (error) {
      console.log(chalk.red('\n❌ 部署失败:'), error.message);
      return false;
    }
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  const deployer = new ClaudeAutoDeployer();
  deployer.deploy().then(success => {
    process.exit(success ? 0 : 1);
  });
}

module.exports = ClaudeAutoDeployer;