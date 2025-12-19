/**
 * SSCI技能包部署命令
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const ora = require('ora');
const os = require('os');

const { detectCLIs, getHomeDir } = require('./utils');

class DeployCommands {
  constructor() {
    this.packagePath = path.resolve(__dirname, '..');
    this.packageJson = require('../package.json');
    this.ssciConfig = this.packageJson.ssci;
  }

  async deployToAll(force = false) {
    const clis = await detectCLIs();
    const availableCLIs = Object.entries(clis)
      .filter(([name, info]) => info.installed)
      .map(([name]) => name);

    if (availableCLIs.length === 0) {
      throw new Error('未检测到任何支持的AI CLI工具');
    }

    console.log(`检测到 ${availableCLIs.length} 个可用CLI工具: ${availableCLIs.join(', ')}`);

    for (const cli of availableCLIs) {
      await this.deployToCLI(cli, force);
    }
  }

  async deployToCLI(cliName, force = false) {
    const spinner = ora(`部署到 ${cliName}...`).start();

    try {
      const targetConfig = this.ssciConfig.cli_targets[cliName];
      if (!targetConfig) {
        throw new Error(`不支持的CLI工具: ${cliName}`);
      }

      const homeDir = getHomeDir();
      const targetDir = path.join(homeDir, targetConfig.config_dir);

      // 创建目标目录
      await fs.ensureDir(targetDir);

      // 部署智能体
      await this.deployAgents(cliName, targetDir, force);

      // 部署技能
      await this.deploySkills(cliName, targetDir, force);

      // 运行适配器（如果需要）
      await this.runAdapter(cliName);

      spinner.succeed(`成功部署到 ${cliName}`);

    } catch (error) {
      spinner.fail(`部署到 ${cliName} 失败`);
      throw error;
    }
  }

  async deployAgents(cliName, targetDir, force) {
    const agents = this.ssciConfig.agents;
    const spinner = ora('部署智能体...').start();

    try {
      for (const [agentName, agentPath] of Object.entries(agents)) {
        const sourcePath = path.join(this.packagePath, agentPath);
        const destPath = path.join(targetDir, `${agentName}.md`);

        if (await fs.pathExists(destPath) && !force) {
          spinner.text = `跳过已存在的智能体: ${agentName}`;
          continue;
        }

        await fs.copy(sourcePath, destPath);
        spinner.text = `已部署智能体: ${agentName}`;
      }

      spinner.succeed(`部署了 ${Object.keys(agents).length} 个智能体`);

    } catch (error) {
      spinner.fail('智能体部署失败');
      throw error;
    }
  }

  async deploySkills(cliName, targetDir, force) {
    const skills = this.ssciConfig.skills;
    const spinner = ora('部署技能...').start();

    try {
      let totalSkills = 0;

      for (const [category, skillList] of Object.entries(skills)) {
        const categoryDir = path.join(targetDir, category);
        await fs.ensureDir(categoryDir);

        for (const skillPath of skillList) {
          const sourcePath = path.join(this.packagePath, skillPath);
          const skillName = path.basename(skillPath);
          const destPath = path.join(categoryDir, skillName);

          if (await fs.pathExists(destPath) && !force) {
            spinner.text = `跳过已存在的技能: ${skillName}`;
            continue;
          }

          await fs.copy(sourcePath, destPath);
          totalSkills++;
          spinner.text = `已部署技能: ${category}/${skillName}`;
        }
      }

      spinner.succeed(`部署了 ${totalSkills} 个技能`);

    } catch (error) {
      spinner.fail('技能部署失败');
      throw error;
    }
  }

  async runAdapter(cliName) {
    const adapterScript = path.join(this.packagePath, 'adapters', `${cliName}-cli-adapter.js`);

    if (await fs.pathExists(adapterScript)) {
      const spinner = ora('运行格式适配器...').start();

      try {
        const { execSync } = require('child_process');
        execSync(`node "${adapterScript}" --install`, { stdio: 'pipe' });
        spinner.succeed('适配器运行完成');
      } catch (error) {
        spinner.warn('适配器运行失败，但不影响基本功能');
      }
    }
  }

  async interactiveDeploy(selectedCLIs, skillCategories) {
    for (const cli of selectedCLIs) {
      const spinner = ora(`部署到 ${cli}...`).start();

      try {
        const targetConfig = this.ssciConfig.cli_targets[cli];
        const homeDir = getHomeDir();
        const targetDir = path.join(homeDir, targetConfig.config_dir);

        await fs.ensureDir(targetDir);

        // 根据用户选择部署
        if (skillCategories.includes('agents')) {
          await this.deployAgents(cli, targetDir, false);
        }

        if (skillCategories.some(cat => cat !== 'agents')) {
          await this.deploySelectedSkills(cli, targetDir, skillCategories);
        }

        await this.runAdapter(cli);
        spinner.succeed(`成功部署到 ${cli}`);

      } catch (error) {
        spinner.fail(`部署到 ${cli} 失败`);
        throw error;
      }
    }
  }

  async deploySelectedSkills(cliName, targetDir, skillCategories) {
    const skills = this.ssciConfig.skills;
    let totalSkills = 0;

    for (const [category, skillList] of Object.entries(skills)) {
      if (!skillCategories.includes(category)) continue;

      const categoryDir = path.join(targetDir, category);
      await fs.ensureDir(categoryDir);

      for (const skillPath of skillList) {
        const sourcePath = path.join(this.packagePath, skillPath);
        const skillName = path.basename(skillPath);
        const destPath = path.join(categoryDir, skillName);

        await fs.copy(sourcePath, destPath);
        totalSkills++;
      }
    }

    return totalSkills;
  }

  async uninstallFromAll() {
    const clis = await detectCLIs();
    const availableCLIs = Object.entries(clis)
      .filter(([name, info]) => info.installed)
      .map(([name]) => name);

    for (const cli of availableCLIs) {
      await this.uninstallFromCLI(cli);
    }
  }

  async uninstallFromCLI(cliName) {
    const targetConfig = this.ssciConfig.cli_targets[cliName];
    if (!targetConfig) {
      throw new Error(`不支持的CLI工具: ${cliName}`);
    }

    const homeDir = getHomeDir();
    const targetDir = path.join(homeDir, targetConfig.config_dir);

    if (await fs.pathExists(targetDir)) {
      await fs.remove(targetDir);
      console.log(chalk.green(`✓ 已从 ${cliName} 卸载技能包`));
    } else {
      console.log(chalk.yellow(`⚠️  ${cliName} 中未找到技能包`));
    }
  }

  async updateSkills() {
    const clis = await detectCLIs();
    const availableCLIs = Object.entries(clis)
      .filter(([name, info]) => info.installed)
      .map(([name]) => name);

    // 先卸载再重新部署
    await this.uninstallFromAll();
    await this.deployToAll(true);

    console.log(chalk.green('✅ 技能包更新完成'));
  }
}

module.exports = {
  DeployCommands,
  deployCommands: new DeployCommands()
};