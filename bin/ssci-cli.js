#!/usr/bin/env node

/**
 * SSCI Subagent Skills CLI
 * 一键部署中文社会科学研究AI技能包
 */

const { Command } = require('commander');
const chalk = require('chalk');
const inquirer = require('inquirer');
const path = require('path');
const fs = require('fs-extra');

const deployCommands = require('../scripts/deploy-commands');
const { detectCLIs, validateDeployment } = require('../scripts/utils');

const program = new Command();

// 版本信息
program
  .name('ssci')
  .description('中文社会科学研究AI Subagent技能包 - 一键部署工具')
  .version(require('../package.json').version);

// 检测环境
program
  .command('detect')
  .description('检测已安装的AI CLI工具')
  .action(async () => {
    console.log(chalk.blue.bold('🔍 检测AI CLI工具环境...'));

    const clis = await detectCLIs();

    console.log('\n📊 检测结果:');
    Object.entries(clis).forEach(([name, info]) => {
      const status = info.installed ? chalk.green('✓ 已安装') : chalk.red('✗ 未安装');
      const version = info.version ? ` (${info.version})` : '';
      console.log(`  ${name}: ${status}${version}`);
    });
  });

// 一键部署到所有CLI
program
  .command('deploy [cli]')
  .description('一键部署技能包到AI CLI工具')
  .option('-a, --all', '部署到所有可用的CLI工具')
  .option('-f, --force', '强制覆盖现有技能')
  .action(async (cli, options) => {
    console.log(chalk.blue.bold('🚀 SSCI技能包部署开始...'));

    try {
      if (options.all || !cli) {
        // 部署到所有可用CLI
        await deployCommands.deployToAll(options.force);
      } else {
        // 部署到指定CLI
        await deployCommands.deployToCLI(cli, options.force);
      }

      console.log(chalk.green.bold('✅ 部署完成！'));
      console.log('\n📝 使用方法:');
      console.log('  Claude CLI: claude');
      console.log('  Qwen CLI: qwen');
      console.log('  iFlow CLI: iflow');

    } catch (error) {
      console.error(chalk.red.bold('❌ 部署失败:'), error.message);
      process.exit(1);
    }
  });

// 交互式部署
program
  .command('setup')
  .description('交互式设置和部署')
  .action(async () => {
    console.log(chalk.blue.bold('⚙️  SSCI技能包交互式设置'));

    try {
      // 检测可用CLI
      const clis = await detectCLIs();
      const availableCLIs = Object.entries(clis)
        .filter(([name, info]) => info.installed)
        .map(([name]) => name);

      if (availableCLIs.length === 0) {
        console.log(chalk.yellow('⚠️  未检测到支持的AI CLI工具'));
        console.log('请先安装 Claude Code、Qwen CLI 或 iFlow CLI');
        return;
      }

      // 选择要部署的CLI
      const { selectedCLIs } = await inquirer.prompt([
        {
          type: 'checkbox',
          name: 'selectedCLIs',
          message: '选择要部署到的AI CLI工具:',
          choices: availableCLIs
        }
      ]);

      if (selectedCLIs.length === 0) {
        console.log(chalk.yellow('未选择任何CLI工具，部署取消'));
        return;
      }

      // 选择要部署的技能
      const { skillCategories } = await inquirer.prompt([
        {
          type: 'checkbox',
          name: 'skillCategories',
          message: '选择要部署的技能类别:',
          choices: [
            { name: '🧠 智能体 (Agents)', value: 'agents', checked: true },
            { name: '📝 编码技能 (Coding)', value: 'coding', checked: true },
            { name: '📊 分析技能 (Analysis)', value: 'analysis', checked: true },
            { name: '✍️  写作技能 (Writing)', value: 'writing', checked: true },
            { name: '🔬 方法论技能 (Methodology)', value: 'methodology', checked: true }
          ]
        }
      ]);

      // 确认部署
      const { confirmed } = await inquirer.prompt([
        {
          type: 'confirm',
          name: 'confirmed',
          message: `确认部署技能包到 ${selectedCLIs.join(', ')}?`,
          default: true
        }
      ]);

      if (confirmed) {
        await deployCommands.interactiveDeploy(selectedCLIs, skillCategories);
        console.log(chalk.green.bold('✅ 交互式部署完成！'));
      } else {
        console.log(chalk.yellow('部署已取消'));
      }

    } catch (error) {
      console.error(chalk.red.bold('❌ 设置失败:'), error.message);
      process.exit(1);
    }
  });

// 验证部署
program
  .command('validate')
  .description('验证技能包部署状态')
  .option('-v, --verbose', '显示详细信息')
  .action(async (options) => {
    console.log(chalk.blue.bold('🔍 验证部署状态...'));

    try {
      const results = await validateDeployment(options.verbose);

      console.log('\n📊 验证结果:');
      Object.entries(results).forEach(([cli, status]) => {
        const icon = status.valid ? chalk.green('✓') : chalk.red('✗');
        console.log(`  ${icon} ${cli}: ${status.message}`);

        if (options.verbose && status.details) {
          status.details.forEach(detail => {
            console.log(`    - ${detail}`);
          });
        }
      });

    } catch (error) {
      console.error(chalk.red.bold('❌ 验证失败:'), error.message);
      process.exit(1);
    }
  });

// 卸载
program
  .command('uninstall [cli]')
  .description('从AI CLI工具中卸载技能包')
  .option('-a, --all', '从所有CLI工具中卸载')
  .action(async (cli, options) => {
    console.log(chalk.blue.bold('🗑️  卸载SSCI技能包...'));

    try {
      if (options.all || !cli) {
        await deployCommands.uninstallFromAll();
      } else {
        await deployCommands.uninstallFromCLI(cli);
      }

      console.log(chalk.green.bold('✅ 卸载完成！'));

    } catch (error) {
      console.error(chalk.red.bold('❌ 卸载失败:'), error.message);
      process.exit(1);
    }
  });

// 更新
program
  .command('update')
  .description('更新技能包到最新版本')
  .action(async () => {
    console.log(chalk.blue.bold('🔄 更新SSCI技能包...'));

    try {
      await deployCommands.updateSkills();
      console.log(chalk.green.bold('✅ 更新完成！'));

    } catch (error) {
      console.error(chalk.red.bold('❌ 更新失败:'), error.message);
      process.exit(1);
    }
  });

// 显示信息
program
  .command('info')
  .description('显示技能包信息')
  .action(() => {
    const packageJson = require('../package.json');

    console.log(chalk.blue.bold('📚 SSCI中文社会科学研究技能包'));
    console.log(`版本: ${packageJson.version}`);
    console.log(`作者: ${packageJson.author}`);
    console.log(`仓库: ${packageJson.repository.url}`);
    console.log('\n📦 包含组件:');

    const config = packageJson.ssci;
    Object.entries(config.skills).forEach(([category, skills]) => {
      console.log(`  ${category}: ${skills.length}个技能`);
    });

    console.log('\n🤖 支持的AI CLI:');
    Object.keys(config.cli_targets).forEach(cli => {
      console.log(`  - ${cli}`);
    });

    console.log('\n📖 使用方法:');
    console.log('  npm install -g ssci-subagent-skills');
    console.log('  ssci deploy --all');
    console.log('  ssci setup  # 交互式设置');
  });

// 错误处理
program.on('command:*', (operands) => {
  console.error(chalk.red('❌ 未知命令:'), operands[0]);
  console.log('使用 --help 查看可用命令');
  process.exit(1);
});

// 主程序
if (require.main === module) {
  program.parse();
}

module.exports = program;