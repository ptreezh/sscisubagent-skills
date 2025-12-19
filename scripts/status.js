#!/usr/bin/env node

/**
 * SSCI技能包 - 状态检查脚本
 * 检查所有CLI工具的部署状态
 */

const fs = require('fs-extra');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

class StatusChecker {
  constructor() {
    this.rootDir = path.resolve(__dirname, '..');
    this.cliTools = [
      { name: 'Claude Code', command: 'claude', configPath: '~/.claude' },
      { name: 'Qwen CLI', command: 'qwen', configPath: '~/.qwen' },
      { name: 'iFlow CLI', command: 'iflow', configPath: '~/.iflow' },
      { name: 'Gemini CLI', command: 'gemini', configPath: '~/.gemini' },
      { name: 'CodeBuddy CLI', command: 'codebuddy', configPath: '~/.codebuddy' },
      { name: 'Codex CLI', command: 'codex', configPath: '~/.codex' },
      { name: 'QoderCLI', command: 'qodercli', configPath: '~/.qodercli' }
    ];
  }

  async checkStatus() {
    console.log('🔍 SSCI技能包状态检查\n');
    console.log('='.repeat(50));

    // 检查npm包状态
    await this.checkPackageStatus();

    // 检查CLI工具状态
    await this.checkCLIToolsStatus();

    // 检查Stigmergy状态
    await this.checkStigmergyStatus();

    // 检查技能部署状态
    await this.checkSkillsDeploymentStatus();

    // 生成状态报告
    await this.generateStatusReport();
  }

  async checkPackageStatus() {
    console.log('\n📦 NPM包状态');
    console.log('-'.repeat(30));

    try {
      const packagePath = path.join(this.rootDir, 'package.json');
      if (await fs.pathExists(packagePath)) {
        const packageJson = await fs.readJson(packagePath);
        console.log(`✅ 包名: ${packageJson.name}`);
        console.log(`✅ 版本: ${packageJson.version}`);
        console.log(`✅ 描述: ${packageJson.description}`);
      } else {
        console.log('❌ package.json不存在');
      }
    } catch (error) {
      console.log('❌ 无法读取package.json:', error.message);
    }
  }

  async checkCLIToolsStatus() {
    console.log('\n🛠️ CLI工具状态');
    console.log('-'.repeat(30));

    for (const cli of this.cliTools) {
      await this.checkSingleCLI(cli);
    }
  }

  async checkSingleCLI(cli) {
    const { name, command, configPath } = cli;
    const expandedPath = configPath.replace('~', os.homedir());

    try {
      // 检查CLI是否安装
      const version = execSync(`${command} --version`, { 
        encoding: 'utf8', 
        timeout: 5000 
      });
      console.log(`✅ ${name}: ${version.trim()}`);

      // 检查配置目录
      if (await fs.pathExists(expandedPath)) {
        const skillsPath = path.join(expandedPath, 'skills');
        const agentsPath = path.join(expandedPath, 'agents');
        
        const skillsCount = await this.countDirectoryItems(skillsPath);
        const agentsCount = await this.countDirectoryItems(agentsPath);
        
        console.log(`   📁 技能: ${skillsCount}个`);
        console.log(`   🤖 智能体: ${agentsCount}个`);
      } else {
        console.log(`   ⚠️  配置目录不存在: ${expandedPath}`);
      }
    } catch (error) {
      console.log(`❌ ${name}: 未安装或不可用`);
    }
  }

  async checkStigmergyStatus() {
    console.log('\n🔄 Stigmergy状态');
    console.log('-'.repeat(30));

    try {
      const version = execSync('stigmergy --version', { 
        encoding: 'utf8', 
        timeout: 5000 
      });
      console.log(`✅ Stigmergy: ${version.trim()}`);

      const stigmergyDir = path.join(os.homedir(), '.stigmergy');
      if (await fs.pathExists(stigmergyDir)) {
        const skillsDir = path.join(stigmergyDir, 'skills');
        const skillsCount = await this.countDirectoryItems(skillsDir);
        console.log(`   📁 技能库: ${skillsCount}个`);
      } else {
        console.log('   ⚠️  Stigmergy目录不存在');
      }
    } catch (error) {
      console.log('❌ Stigmergy: 未安装或不可用');
    }
  }

  async checkSkillsDeploymentStatus() {
    console.log('\n📊 技能部署状态');
    console.log('-'.repeat(30));

    // 检查原始技能目录
    const originalSkillsDir = path.join(this.rootDir, 'skills');
    if (await fs.pathExists(originalSkillsDir)) {
      const originalCount = await this.countSkillsInDirectory(originalSkillsDir);
      console.log(`✅ 原始技能: ${originalCount}个`);
    } else {
      console.log('❌ 原始技能目录不存在');
    }

    // 检查各CLI中的技能数量
    for (const cli of this.cliTools) {
      const configPath = cli.configPath.replace('~', os.homedir());
      if (await fs.pathExists(configPath)) {
        const skillsPath = path.join(configPath, 'skills');
        const count = await this.countDirectoryItems(skillsPath);
        console.log(`   ${cli.name}: ${count}个技能`);
      }
    }
  }

  async countDirectoryItems(dirPath) {
    try {
      const items = await fs.readdir(dirPath);
      return items.length;
    } catch (error) {
      return 0;
    }
  }

  async countSkillsInDirectory(dirPath) {
    let count = 0;
    
    async function countSkills(dir) {
      try {
        const items = await fs.readdir(dir);
        
        for (const item of items) {
          const itemPath = path.join(dir, item);
          const stat = await fs.stat(itemPath);
          
          if (stat.isDirectory()) {
            const skillFile = path.join(itemPath, 'SKILL.md');
            if (await fs.pathExists(skillFile)) {
              count++;
            }
            await countSkills(itemPath);
          }
        }
      } catch (error) {
        // 忽略错误目录
      }
    }
    
    await countSkills(dirPath);
    return count;
  }

  async generateStatusReport() {
    console.log('\n📋 状态报告');
    console.log('='.repeat(50));

    const timestamp = new Date().toLocaleString('zh-CN');
    console.log(`生成时间: ${timestamp}`);
    
    console.log('\n🎯 推荐操作:');
    
    const installedCLIs = this.cliTools.filter(cli => {
      try {
        execSync(`${cli.command} --version`, { 
          encoding: 'utf8', 
          timeout: 2000 
        });
        return true;
      } catch (error) {
        return false;
      }
    });

    if (installedCLIs.length > 0) {
      console.log('1. 测试技能调用:');
      console.log('   claude "请帮我进行开放编码分析"');
      console.log('   qwen "请计算网络中心性指标"');
      console.log('   iflow "请帮我解决研究冲突"');
    }

    const stigmergyInstalled = (() => {
      try {
        execSync('stigmergy --version', { 
          encoding: 'utf8', 
          timeout: 2000 
        });
        return true;
      } catch (error) {
        return false;
      }
    })();

    if (stigmergyInstalled) {
      console.log('\n2. 使用Stigmergy:');
      console.log('   stigmergy skill list');
      console.log('   stigmergy call "进行复杂分析"');
      console.log('   stigmergy use claude "使用sna-expert"');
    }

    console.log('\n3. 维护操作:');
    console.log('   npm run deploy:all     # 重新部署所有CLI');
    console.log('   npm run deploy:stigmergy # 仅部署到Stigmergy');
    console.log('   npm run status           # 重新检查状态');
    console.log('   npm run health-check     # 健康检查');
  }
}

// 主程序
if (require.main === module) {
  const checker = new StatusChecker();
  checker.checkStatus().catch(console.error);
}

module.exports = StatusChecker;