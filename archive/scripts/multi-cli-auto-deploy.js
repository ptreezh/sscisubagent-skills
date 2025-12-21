/**
 * 多CLI自动检测和部署脚本
 * 支持Claude Code、Qwen CLI、iFlow CLI的自动检测和部署
 */

const fs = require('fs-extra');
const path = require('path');
const os = require('os');
const chalk = require('chalk');
const ora = require('ora');
const { execSync } = require('child_process');

class MultiCLIAutoDeployer {
  constructor() {
    this.packagePath = path.resolve(__dirname, '..');
    this.homeDir = os.homedir();
    this.supportedCLIs = {
      claude: {
        name: 'Claude Code',
        detectionMethods: [
          this.detectClaudeByPath.bind(this),
          this.detectClaudeByCommand.bind(this)
        ],
        configPaths: this.getClaudeConfigPaths()
      },
      qwen: {
        name: 'Qwen CLI',
        detectionMethods: [
          this.detectQwenByCommand.bind(this),
          this.detectQwenByPath.bind(this)
        ],
        configPaths: this.getQwenConfigPaths()
      },
      iflow: {
        name: 'iFlow CLI',
        detectionMethods: [
          this.detectIFlowByCommand.bind(this),
          this.detectIFlowByPath.bind(this)
        ],
        configPaths: this.getIFlowConfigPaths()
      },
      gemini: {
        name: 'Gemini CLI',
        detectionMethods: [
          this.detectGeminiByCommand.bind(this),
          this.detectGeminiByPath.bind(this)
        ],
        configPaths: this.getGeminiConfigPaths()
      },
      codebuddy: {
        name: 'CodeBuddy CLI',
        detectionMethods: [
          this.detectCodeBuddyByCommand.bind(this),
          this.detectCodeBuddyByPath.bind(this)
        ],
        configPaths: this.getCodeBuddyConfigPaths()
      },
      codex: {
        name: 'Codex CLI',
        detectionMethods: [
          this.detectCodexByCommand.bind(this),
          this.detectCodexByPath.bind(this)
        ],
        configPaths: this.getCodexConfigPaths()
      },
      qodercli: {
        name: 'QoderCLI',
        detectionMethods: [
          this.detectQoderCLIByCommand.bind(this),
          this.detectQoderCLIByPath.bind(this)
        ],
        configPaths: this.getQoderCLIConfigPaths()
      }
    };
  }

  /**
   * 获取Claude配置路径
   */
  getClaudeConfigPaths() {
    const platform = os.platform();
    const paths = [];

    if (platform === 'darwin') {
      paths.push(
        path.join(this.homeDir, 'Library', 'Application Support', 'Claude'),
        path.join(this.homeDir, '.claude')
      );
    } else if (platform === 'win32') {
      paths.push(
        path.join(this.homeDir, 'AppData', 'Roaming', 'Claude'),
        path.join(this.homeDir, '.claude'),
        path.join(process.env.LOCALAPPDATA || '', 'Claude')
      );
    } else {
      paths.push(
        path.join(this.homeDir, '.claude'),
        path.join(this.homeDir, '.config', 'claude')
      );
    }

    return paths;
  }

  /**
   * 获取Qwen配置路径
   */
  getQwenConfigPaths() {
    const platform = os.platform();
    const paths = [];

    if (platform === 'darwin') {
      paths.push(
        path.join(this.homeDir, '.qwen'),
        path.join(this.homeDir, 'Library', 'Application Support', 'Qwen')
      );
    } else if (platform === 'win32') {
      paths.push(
        path.join(this.homeDir, '.qwen'),
        path.join(this.homeDir, 'AppData', 'Roaming', 'Qwen'),
        path.join(process.env.LOCALAPPDATA || '', 'Qwen')
      );
    } else {
      paths.push(
        path.join(this.homeDir, '.qwen'),
        path.join(this.homeDir, '.config', 'qwen')
      );
    }

    return paths;
  }

  /**
   * 获取iFlow配置路径
   */
  getIFlowConfigPaths() {
    const platform = os.platform();
    const paths = [];

    if (platform === 'darwin') {
      paths.push(
        path.join(this.homeDir, '.iflow'),
        path.join(this.homeDir, 'Library', 'Application Support', 'iFlow')
      );
    } else if (platform === 'win32') {
      paths.push(
        path.join(this.homeDir, '.iflow'),
        path.join(this.homeDir, 'AppData', 'Roaming', 'iFlow'),
        path.join(process.env.LOCALAPPDATA || '', 'iFlow'),
        path.join(this.homeDir, 'AppData', 'Local', 'iFlow')
      );
    } else {
      paths.push(
        path.join(this.homeDir, '.iflow'),
        path.join(this.homeDir, '.config', 'iflow')
      );
    }

    return paths;
  }

  /**
   * 获取Gemini配置路径
   */
  getGeminiConfigPaths() {
    const platform = os.platform();
    const paths = [];

    if (platform === 'darwin') {
      paths.push(
        path.join(this.homeDir, '.gemini'),
        path.join(this.homeDir, 'Library', 'Application Support', 'Gemini')
      );
    } else if (platform === 'win32') {
      paths.push(
        path.join(this.homeDir, '.gemini'),
        path.join(this.homeDir, 'AppData', 'Roaming', 'Gemini'),
        path.join(process.env.LOCALAPPDATA || '', 'Gemini')
      );
    } else {
      paths.push(
        path.join(this.homeDir, '.gemini'),
        path.join(this.homeDir, '.config', 'gemini')
      );
    }

    return paths;
  }

  /**
   * 获取CodeBuddy配置路径
   */
  getCodeBuddyConfigPaths() {
    const platform = os.platform();
    const paths = [];

    if (platform === 'darwin') {
      paths.push(
        path.join(this.homeDir, '.codebuddy'),
        path.join(this.homeDir, 'Library', 'Application Support', 'CodeBuddy')
      );
    } else if (platform === 'win32') {
      paths.push(
        path.join(this.homeDir, '.codebuddy'),
        path.join(this.homeDir, 'AppData', 'Roaming', 'CodeBuddy'),
        path.join(process.env.LOCALAPPDATA || '', 'CodeBuddy')
      );
    } else {
      paths.push(
        path.join(this.homeDir, '.codebuddy'),
        path.join(this.homeDir, '.config', 'codebuddy')
      );
    }

    return paths;
  }

  /**
   * 获取Codex配置路径
   */
  getCodexConfigPaths() {
    const platform = os.platform();
    const paths = [];

    if (platform === 'darwin') {
      paths.push(
        path.join(this.homeDir, '.codex'),
        path.join(this.homeDir, 'Library', 'Application Support', 'Codex')
      );
    } else if (platform === 'win32') {
      paths.push(
        path.join(this.homeDir, '.codex'),
        path.join(this.homeDir, 'AppData', 'Roaming', 'Codex'),
        path.join(process.env.LOCALAPPDATA || '', 'Codex')
      );
    } else {
      paths.push(
        path.join(this.homeDir, '.codex'),
        path.join(this.homeDir, '.config', 'codex')
      );
    }

    return paths;
  }

  /**
   * 获取QoderCLI配置路径
   */
  getQoderCLIConfigPaths() {
    const platform = os.platform();
    const paths = [];

    if (platform === 'darwin') {
      paths.push(
        path.join(this.homeDir, '.qodercli'),
        path.join(this.homeDir, 'Library', 'Application Support', 'QoderCLI')
      );
    } else if (platform === 'win32') {
      paths.push(
        path.join(this.homeDir, '.qodercli'),
        path.join(this.homeDir, 'AppData', 'Roaming', 'QoderCLI'),
        path.join(process.env.LOCALAPPDATA || '', 'QoderCLI')
      );
    } else {
      paths.push(
        path.join(this.homeDir, '.qodercli'),
        path.join(this.homeDir, '.config', 'qodercli')
      );
    }

    return paths;
  }

  /**
   * 通过路径检测Claude
   */
  async detectClaudeByPath() {
    for (const claudePath of this.supportedCLIs.claude.configPaths) {
      try {
        const indicators = ['claude.exe', 'claude', 'Claude.exe', 'config.json'];
        for (const indicator of indicators) {
          if (await fs.pathExists(path.join(claudePath, indicator))) {
            return claudePath;
          }
        }
        if (claudePath.endsWith('.claude') && await fs.pathExists(claudePath)) {
          return claudePath;
        }
      } catch (error) {
        // 继续检查
      }
    }
    return null;
  }

  /**
   * 通过命令检测Claude
   */
  async detectClaudeByCommand() {
    try {
      const version = execSync('claude --version', { encoding: 'utf8', timeout: 5000 });
      if (version) {
        return path.join(this.homeDir, '.claude');
      }
    } catch (error) {
      // 命令不可用
    }
    return null;
  }

  /**
   * 通过命令检测Qwen
   */
  async detectQwenByCommand() {
    try {
      const version = execSync('qwen --version', { encoding: 'utf8', timeout: 5000 });
      if (version) {
        return path.join(this.homeDir, '.qwen');
      }
    } catch (error) {
      // 命令不可用
    }
    return null;
  }

  /**
   * 通过路径检测Qwen
   */
  async detectQwenByPath() {
    for (const qwenPath of this.supportedCLIs.qwen.configPaths) {
      try {
        if (await fs.pathExists(qwenPath)) {
          return qwenPath;
        }
      } catch (error) {
        // 继续检查
      }
    }
    return null;
  }

  /**
   * 通过命令检测iFlow
   */
  async detectIFlowByCommand() {
    try {
      const version = execSync('iflow --version', { encoding: 'utf8', timeout: 5000 });
      if (version) {
        return path.join(this.homeDir, '.iflow');
      }
    } catch (error) {
      // 命令不可用
    }
    return null;
  }

  /**
   * 通过路径检测iFlow
   */
  async detectIFlowByPath() {
    for (const iflowPath of this.supportedCLIs.iflow.configPaths) {
      try {
        if (await fs.pathExists(iflowPath)) {
          return iflowPath;
        }
      } catch (error) {
        // 继续检查
      }
    }
    return null;
  }

  /**
   * 通过命令检测Gemini
   */
  async detectGeminiByCommand() {
    try {
      const version = execSync('gemini --version', { encoding: 'utf8', timeout: 5000 });
      if (version) {
        return path.join(this.homeDir, '.gemini');
      }
    } catch (error) {
      // 命令不可用
    }
    return null;
  }

  /**
   * 通过路径检测Gemini
   */
  async detectGeminiByPath() {
    for (const geminiPath of this.supportedCLIs.gemini.configPaths) {
      try {
        if (await fs.pathExists(geminiPath)) {
          return geminiPath;
        }
      } catch (error) {
        // 继续检查
      }
    }
    return null;
  }

  /**
   * 通过命令检测CodeBuddy
   */
  async detectCodeBuddyByCommand() {
    try {
      const version = execSync('codebuddy --version', { encoding: 'utf8', timeout: 5000 });
      if (version) {
        return path.join(this.homeDir, '.codebuddy');
      }
    } catch (error) {
      // 命令不可用
    }
    return null;
  }

  /**
   * 通过路径检测CodeBuddy
   */
  async detectCodeBuddyByPath() {
    for (const codebuddyPath of this.supportedCLIs.codebuddy.configPaths) {
      try {
        if (await fs.pathExists(codebuddyPath)) {
          return codebuddyPath;
        }
      } catch (error) {
        // 继续检查
      }
    }
    return null;
  }

  /**
   * 通过命令检测Codex
   */
  async detectCodexByCommand() {
    try {
      const version = execSync('codex --version', { encoding: 'utf8', timeout: 5000 });
      if (version) {
        return path.join(this.homeDir, '.codex');
      }
    } catch (error) {
      // 命令不可用
    }
    return null;
  }

  /**
   * 通过路径检测Codex
   */
  async detectCodexByPath() {
    for (const codexPath of this.supportedCLIs.codex.configPaths) {
      try {
        if (await fs.pathExists(codexPath)) {
          return codexPath;
        }
      } catch (error) {
        // 继续检查
      }
    }
    return null;
  }

  /**
   * 通过命令检测QoderCLI
   */
  async detectQoderCLIByCommand() {
    try {
      const version = execSync('qodercli --version', { encoding: 'utf8', timeout: 5000 });
      if (version) {
        return path.join(this.homeDir, '.qodercli');
      }
    } catch (error) {
      // 命令不可用
    }
    return null;
  }

  /**
   * 通过路径检测QoderCLI
   */
  async detectQoderCLIByPath() {
    for (const qodercliPath of this.supportedCLIs.qodercli.configPaths) {
      try {
        if (await fs.pathExists(qodercliPath)) {
          return qodercliPath;
        }
      } catch (error) {
        // 继续检查
      }
    }
    return null;
  }

  /**
   * 检测所有CLI
   */
  async detectAllCLIs() {
    console.log(chalk.blue('🔍 检测支持的AI CLI工具...\n'));
    
    const detectedCLIs = {};

    for (const [cliKey, cliInfo] of Object.entries(this.supportedCLIs)) {
      console.log(chalk.yellow(`检测 ${cliInfo.name}...`));
      
      let detectedPath = null;
      for (const detectionMethod of cliInfo.detectionMethods) {
        detectedPath = await detectionMethod();
        if (detectedPath) break;
      }

      if (detectedPath) {
        detectedCLIs[cliKey] = {
          name: cliInfo.name,
          path: detectedPath,
          configPaths: cliInfo.configPaths
        };
        console.log(chalk.green(`  ✅ 找到: ${detectedPath}`));
      } else {
        console.log(chalk.red(`  ❌ 未找到`));
      }
    }

    return detectedCLIs;
  }

  /**
   * 创建CLI配置目录结构
   */
  async createCLIStructure(cliKey, cliPath) {
    const spinner = ora(`创建${this.supportedCLIs[cliKey].name}配置目录...`).start();
    
    try {
      // 确定配置目录
      const configDir = cliPath.endsWith(`.${cliKey}`) ? cliPath : path.join(this.homeDir, `.${cliKey}`);
      
      // 创建必要的目录
      const dirsToCreate = [
        path.join(configDir, 'skills'),
        path.join(configDir, 'agents'),
        path.join(configDir, 'config')
      ];

      for (const dir of dirsToCreate) {
        await fs.ensureDir(dir);
      }

      spinner.succeed(`${this.supportedCLIs[cliKey].name}配置目录创建完成`);
      return configDir;
    } catch (error) {
      spinner.fail('创建配置目录失败');
      throw error;
    }
  }

  /**
   * 部署skills到指定CLI
   */
  async deploySkills(configDir, cliKey) {
    const spinner = ora(`部署Skills到${this.supportedCLIs[cliKey].name}...`).start();
    
    try {
      const skillsSourceDir = path.join(this.packagePath, 'skills');
      const skillsTargetDir = path.join(configDir, 'skills');

      if (!(await fs.pathExists(skillsSourceDir))) {
        throw new Error('源skills目录不存在');
      }

      // 根据CLI类型可能需要不同的适配
      await this.copySkillsWithAdaptation(skillsSourceDir, skillsTargetDir, cliKey);

      // 创建skills索引
      await this.createSkillsIndex(skillsTargetDir, cliKey);

      spinner.succeed(`Skills部署完成: ${skillsTargetDir}`);
    } catch (error) {
      spinner.fail('Skills部署失败');
      throw error;
    }
  }

  /**
   * 部署agents到指定CLI
   */
  async deployAgents(configDir, cliKey) {
    const spinner = ora(`部署Subagents到${this.supportedCLIs[cliKey].name}...`).start();
    
    try {
      const agentsSourceDir = path.join(this.packagePath, 'agents');
      const agentsTargetDir = path.join(configDir, 'agents');

      if (!(await fs.pathExists(agentsSourceDir))) {
        throw new Error('源agents目录不存在');
      }

      // 根据CLI类型可能需要不同的适配
      await this.copyAgentsWithAdaptation(agentsSourceDir, agentsTargetDir, cliKey);

      // 创建agents索引
      await this.createAgentsIndex(agentsTargetDir, cliKey);

      spinner.succeed(`Subagents部署完成: ${agentsTargetDir}`);
    } catch (error) {
      spinner.fail('Subagents部署失败');
      throw error;
    }
  }

  /**
   * 根据CLI类型复制并适配skills
   */
  async copySkillsWithAdaptation(sourceDir, targetDir, cliKey) {
    await fs.copy(sourceDir, targetDir, {
      overwrite: true,
      filter: (src) => {
        const basename = path.basename(src);
        return !basename.startsWith('.') && basename !== '__pycache__';
      }
    });

    // 根据不同CLI进行特殊适配
    if (cliKey === 'qwen') {
      await this.adaptForQwen(targetDir);
    } else if (cliKey === 'iflow') {
      await this.adaptForIFlow(targetDir);
    } else if (cliKey === 'gemini') {
      await this.adaptForGemini(targetDir);
    } else if (cliKey === 'codebuddy') {
      await this.adaptForCodeBuddy(targetDir);
    } else if (cliKey === 'codex') {
      await this.adaptForCodex(targetDir);
    } else if (cliKey === 'qodercli') {
      await this.adaptForQoderCLI(targetDir);
    }
  }

  /**
   * 根据CLI类型复制并适配agents
   */
  async copyAgentsWithAdaptation(sourceDir, targetDir, cliKey) {
    await fs.copy(sourceDir, targetDir, {
      overwrite: true,
      filter: (src) => {
        const basename = path.basename(src);
        return !basename.startsWith('.') && !basename.includes('-v2');
      }
    });

    // 根据不同CLI进行特殊适配
    if (cliKey === 'qwen') {
      await this.adaptAgentsForQwen(targetDir);
    } else if (cliKey === 'iflow') {
      await this.adaptAgentsForIFlow(targetDir);
    }
  }

  /**
   * 为Qwen CLI适配skills
   */
  async adaptForQwen(skillsDir) {
    // Qwen特定的适配逻辑
    const adapterPath = path.join(this.packagePath, 'adapters', 'qwen-cli-adapter.js');
    if (await fs.pathExists(adapterPath)) {
      // 执行适配逻辑
      console.log(chalk.blue('  📝 应用Qwen CLI适配...'));
    }
  }

  /**
   * 为iFlow CLI适配skills
   */
  async adaptForIFlow(skillsDir) {
    // iFlow特定的适配逻辑
    const adapterPath = path.join(this.packagePath, 'adapters', 'iflow-cli-adapter.js');
    if (await fs.pathExists(adapterPath)) {
      // 执行适配逻辑
      console.log(chalk.blue('  📝 应用iFlow CLI适配...'));
    }
  }

  /**
   * 为Qwen CLI适配agents
   */
  async adaptAgentsForQwen(agentsDir) {
    // Qwen agents适配逻辑
  }

  /**
   * 为iFlow CLI适配agents
   */
  async adaptAgentsForIFlow(agentsDir) {
    // iFlow agents适配逻辑
  }

  /**
   * 为Gemini CLI适配skills
   */
  async adaptForGemini(skillsDir) {
    // Gemini特定的适配逻辑
    console.log(chalk.blue('  📝 应用Gemini CLI适配...'));
  }

  /**
   * 为CodeBuddy CLI适配skills
   */
  async adaptForCodeBuddy(skillsDir) {
    // CodeBuddy特定的适配逻辑
    console.log(chalk.blue('  📝 应用CodeBuddy CLI适配...'));
  }

  /**
   * 为Codex CLI适配skills
   */
  async adaptForCodex(skillsDir) {
    // Codex特定的适配逻辑
    console.log(chalk.blue('  📝 应用Codex CLI适配...'));
  }

  /**
   * 为QoderCLI适配skills
   */
  async adaptForQoderCLI(skillsDir) {
    // QoderCLI特定的适配逻辑
    console.log(chalk.blue('  📝 应用QoderCLI适配...'));
  }

  /**
   * 为Gemini CLI适配agents
   */
  async adaptAgentsForGemini(agentsDir) {
    // Gemini agents适配逻辑
  }

  /**
   * 为CodeBuddy CLI适配agents
   */
  async adaptAgentsForCodeBuddy(agentsDir) {
    // CodeBuddy agents适配逻辑
  }

  /**
   * 为Codex CLI适配agents
   */
  async adaptAgentsForCodex(agentsDir) {
    // Codex agents适配逻辑
  }

  /**
   * 为QoderCLI适配agents
   */
  async adaptAgentsForQoderCLI(agentsDir) {
    // QoderCLI agents适配逻辑
  }

  /**
   * 创建CLI特定的skills索引
   */
  async createSkillsIndex(skillsDir, cliKey) {
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
    
    const cliName = this.supportedCLIs[cliKey].name;
    const indexContent = `# ${cliName} Skills Index

本目录包含以下技能（适配${cliName}）：

${skills.map(skill => `- **${skill.name}**: ${skill.description}`).join('\n')}

## 使用方式

在${cliName}中直接提及相关任务，系统会自动加载相应技能。

---
*自动生成于 ${new Date().toISOString()}*
`;
    
    await fs.writeFile(path.join(skillsDir, 'README.md'), indexContent);
  }

  /**
   * 创建CLI特定的agents索引
   */
  async createAgentsIndex(agentsDir, cliKey) {
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
    
    const cliName = this.supportedCLIs[cliKey].name;
    const indexContent = `# ${cliName} Subagents Index

本目录包含以下智能体（适配${cliName}）：

${agents.map(agent => `- **${agent.name}**: ${agent.description}`).join('\n')}

## 使用方式

在${cliName}中提及相关领域的任务，系统会自动选择合适的智能体。

---
*自动生成于 ${new Date().toISOString()}*
`;
    
    await fs.writeFile(path.join(agentsDir, 'README.md'), indexContent);
  }

  /**
   * 创建CLI配置文件
   */
  async createCLIConfig(configDir, cliKey) {
    const configPath = path.join(configDir, 'config', 'ssci-skills-config.json');
    
    const config = {
      name: 'SSCI Subagent Skills',
      version: require('../package.json').version,
      description: '中文社会科学研究AI技能包',
      cli: cliKey,
      cliName: this.supportedCLIs[cliKey].name,
      installedAt: new Date().toISOString(),
      skillsPath: path.join(configDir, 'skills'),
      agentsPath: path.join(configDir, 'agents'),
      autoUpdate: true
    };
    
    await fs.writeFile(configPath, JSON.stringify(config, null, 2));
  }

  /**
   * 部署到单个CLI
   */
  async deployToCLI(cliKey, cliInfo) {
    console.log(chalk.cyan(`\n📦 部署到 ${cliInfo.name}...`));
    
    try {
      // 1. 创建配置目录
      const configDir = await this.createCLIStructure(cliKey, cliInfo.path);

      // 2. 部署skills
      await this.deploySkills(configDir, cliKey);

      // 3. 部署agents
      await this.deployAgents(configDir, cliKey);

      // 4. 创建配置文件
      await this.createCLIConfig(configDir, cliKey);

      console.log(chalk.green(`✅ ${cliInfo.name} 部署成功！`));
      console.log(chalk.cyan(`   📁 配置目录: ${configDir}\n`));

      return true;
    } catch (error) {
      console.log(chalk.red(`❌ ${cliInfo.name} 部署失败:`, error.message));
      return false;
    }
  }

  /**
   * 执行自动部署到所有检测到的CLI
   */
  async deploy() {
    console.log(chalk.cyan('🚀 SSCI Skills - 多CLI自动部署开始\n'));

    try {
      // 1. 检测所有CLI
      const detectedCLIs = await this.detectAllCLIs();

      if (Object.keys(detectedCLIs).length === 0) {
        console.log(chalk.yellow('\n⚠️  未检测到任何支持的CLI工具'));
        console.log(chalk.yellow('   将创建默认配置目录...\n'));
        
        // 创建默认配置
        const defaultCLIs = ['claude', 'qwen', 'iflow'];
        for (const cliKey of defaultCLIs) {
          const defaultPath = path.join(this.homeDir, `.${cliKey}`);
          detectedCLIs[cliKey] = {
            name: this.supportedCLIs[cliKey].name,
            path: defaultPath,
            configPaths: this.supportedCLIs[cliKey].configPaths
          };
        }
      }

      // 2. 部署到每个检测到的CLI
      let successCount = 0;
      for (const [cliKey, cliInfo] of Object.entries(detectedCLIs)) {
        const success = await this.deployToCLI(cliKey, cliInfo);
        if (success) successCount++;
      }

      // 3. 总结
      console.log(chalk.green('\n📊 部署总结:'));
      console.log(chalk.green(`   ✅ 成功部署: ${successCount}/${Object.keys(detectedCLIs).length} 个CLI`));
      
      if (successCount > 0) {
        console.log(chalk.cyan('\n🎯 现在可以在支持的AI CLI中使用所有SSCI技能和智能体了！'));
      }

      return successCount > 0;
    } catch (error) {
      console.log(chalk.red('\n❌ 自动部署失败:'), error.message);
      return false;
    }
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  const deployer = new MultiCLIAutoDeployer();
  deployer.deploy().then(success => {
    process.exit(success ? 0 : 1);
  });
}

module.exports = MultiCLIAutoDeployer;