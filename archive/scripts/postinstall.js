/**
 * SSCI Subagent Skills Post-install Script
 * 在npm install后自动执行，检测并部署到所有可用的CLI
 */

const fs = require('fs-extra');
const path = require('path');
const chalk = require('chalk');
const ora = require('ora');
const inquirer = require('inquirer');

const MultiCLIAutoDeployer = require('./multi-cli-auto-deploy');

async function main() {
  console.log(chalk.blue('\n🚀 SSCI Subagent Skills 安装完成！\n'));

  // 询问是否自动部署
  const { autoDeploy } = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'autoDeploy',
      message: '是否自动检测并部署到所有可用的AI CLI工具？',
      default: true
    }
  ]);

  if (autoDeploy) {
    const spinner = ora('正在自动部署...').start();
    
    try {
      const deployer = new MultiCLIAutoDeployer();
      const success = await deployer.deploy();
      
      if (success) {
        spinner.succeed('自动部署完成！');
      } else {
        spinner.fail('自动部署失败');
      }
    } catch (error) {
      spinner.fail('部署过程中出错');
      console.error(chalk.red(error.message));
    }
  } else {
    // 显示手动部署说明
    console.log(chalk.cyan('📖 手动部署方法:'));
    console.log('1. 自动部署到所有CLI: npm run deploy:multi');
    console.log('2. 部署到Claude: npm run deploy:claude:auto');
    console.log('3. 使用CLI工具: ssci deploy --all');
    console.log('4. 交互式部署: ssci setup\n');
  }

  console.log(chalk.green('✅ 安装成功！感谢使用SSCI Subagent Skills。\n'));
}

// 检查是否在CI/CD环境中
if (process.env.CI || process.env.CONTINUOUS_INTEGRATION) {
  console.log(chalk.yellow('⚠️  检测到CI环境，跳过自动部署\n'));
  console.log(chalk.cyan('📖 手动部署方法:'));
  console.log('npm run deploy:multi\n');
} else {
  // 正常环境执行交互式安装
  main().catch(error => {
    console.error(chalk.red('❌ Post-install脚本执行失败:'), error.message);
    process.exit(1);
  });
}