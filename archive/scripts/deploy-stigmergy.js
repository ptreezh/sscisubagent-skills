#!/usr/bin/env node

/**
 * SSCI技能包 - Stigmergy部署脚本
 * 将技能部署到Stigmergy统一管理系统
 */

const fs = require('fs-extra');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

class StigmergyDeployer {
  constructor() {
    this.rootDir = path.resolve(__dirname, '..');
    this.skillsDir = path.join(this.rootDir, 'skills');
    this.stigmergyDir = path.join(os.homedir(), '.stigmergy');
    this.stigmergySkillsDir = path.join(this.stigmergyDir, 'skills');
  }

  async deploy() {
    console.log('🚀 开始部署到Stigmergy系统...\n');

    try {
      // 1. 检查Stigmergy安装
      await this.checkStigmergyInstallation();

      // 2. 创建Stigmergy目录
      await this.createStigmergyDirectories();

      // 3. 复制技能文件
      await this.copySkillsToStigmergy();

      // 4. 生成Stigmergy配置
      await this.generateStigmergyConfig();

      // 5. 同步到所有CLI
      await this.syncToAllCLIs();

      // 6. 验证部署
      await this.verifyDeployment();

      console.log('\n✅ Stigmergy部署完成！');
      console.log('\n📋 使用方法:');
      console.log('  stigmergy skill list                    # 列出所有技能');
      console.log('  stigmergy skill read <skill-name>        # 读取技能内容');
      console.log('  stigmergy use <cli> "<prompt>"        # 指定CLI执行');
      console.log('  stigmergy call "<prompt>"              # 智能路由执行');
      console.log('  stigmergy skill sync                    # 同步到所有CLI');

    } catch (error) {
      console.error('\n❌ 部署失败:', error.message);
      process.exit(1);
    }
  }

  async checkStigmergyInstallation() {
    console.log('🔍 检查Stigmergy安装状态...');
    
    try {
      const version = execSync('stigmergy --version', { encoding: 'utf8', timeout: 5000 });
      console.log('✅ Stigmergy已安装:', version.trim());
    } catch (error) {
      console.log('❌ Stigmergy未安装，请先安装:');
      console.log('   npm install -g stigmergy');
      throw new Error('Stigmergy未安装');
    }
  }

  async createStigmergyDirectories() {
    console.log('📁 创建Stigmergy目录结构...');
    
    const dirs = [
      this.stigmergyDir,
      this.stigmergySkillsDir,
      path.join(this.stigmergyDir, 'config'),
      path.join(this.stigmergyDir, 'logs')
    ];

    for (const dir of dirs) {
      await fs.ensureDir(dir);
      console.log(`   - ${dir}`);
    }
  }

  async copySkillsToStigmergy() {
    console.log('\n📦 复制技能到Stigmergy...');
    
    if (!await fs.pathExists(this.skillsDir)) {
      throw new Error('技能目录不存在');
    }

    // 递归复制技能目录
    await this.copyDirectory(this.skillsDir, this.stigmergySkillsDir);
    
    console.log('✅ 技能复制完成');
  }

  async copyDirectory(src, dest) {
    const items = await fs.readdir(src);
    
    for (const item of items) {
      const srcPath = path.join(src, item);
      const destPath = path.join(dest, item);
      
      const stat = await fs.stat(srcPath);
      
      if (stat.isDirectory()) {
        await fs.ensureDir(destPath);
        await this.copyDirectory(srcPath, destPath);
      } else {
        await fs.copy(srcPath, destPath);
      }
    }
  }

  async generateStigmergyConfig() {
    console.log('\n⚙️ 生成Stigmergy配置...');
    
    const configPath = path.join(this.stigmergyDir, 'config.json');
    
    const config = {
      version: '1.0.0',
      name: 'SSCI Skills Package',
      description: '中文社会科学研究AI技能包',
      skillsPath: this.stigmergySkillsDir,
      autoSync: true,
      cliTools: {
        claude: { enabled: true, priority: 'high' },
        qwen: { enabled: true, priority: 'high' },
        gemini: { enabled: true, priority: 'medium' },
        iflow: { enabled: true, priority: 'medium' },
        codebuddy: { enabled: true, priority: 'low' },
        codex: { enabled: true, priority: 'low' },
        qodercli: { enabled: true, priority: 'low' }
      },
      routing: {
        default: 'claude',
        rules: {
          'coding': 'claude',
          'analysis': 'claude',
          'writing': 'claude',
          'statistics': 'qwen',
          'literature': 'gemini',
          'chinese': 'iflow'
        }
      }
    };

    await fs.writeJson(configPath, config, { spaces: 2 });
    console.log(`   - 配置文件: ${configPath}`);
  }

  async syncToAllCLIs() {
    console.log('\n🔄 同步技能到所有CLI工具...');
    
    try {
      const result = execSync('stigmergy skill sync', { 
        encoding: 'utf8', 
        timeout: 30000 
      });
      
      console.log('✅ 同步完成');
      console.log('   ', result.trim());
    } catch (error) {
      console.log('⚠️ 同步出现警告:', error.message);
      // 不抛出错误，继续执行
    }
  }

  async verifyDeployment() {
    console.log('\n🔍 验证部署状态...');
    
    // 检查技能目录
    const skillCount = await this.countSkills();
    console.log(`   - 技能数量: ${skillCount}`);
    
    // 检查CLI配置
    const cliConfigs = await this.countCLIConfigs();
    console.log(`   - CLI配置: ${cliConfigs}`);
    
    // 测试技能读取
    await this.testSkillReading();
    
    console.log('✅ 部署验证通过');
  }

  async countSkills() {
    let count = 0;
    
    async function countSkills(dir) {
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
    }
    
    await countSkills(this.stigmergySkillsDir);
    return count;
  }

  async countCLIConfigs() {
    const cliDir = path.join(os.homedir());
    const clis = ['claude', 'qwen', 'gemini', 'iflow', 'codebuddy', 'codex', 'qodercli'];
    let count = 0;
    
    for (const cli of clis) {
      const configPath = path.join(cliDir, cli, `${cli}.md`);
      if (await fs.pathExists(configPath)) {
        count++;
      }
    }
    
    return count;
  }

  async testSkillReading() {
    try {
      const result = execSync('stigmergy skill list', { 
        encoding: 'utf8', 
        timeout: 10000 
      });
      
      if (result.includes('performing-open-coding')) {
        console.log('   - 技能读取: ✅');
      } else {
        console.log('   - 技能读取: ⚠️ 部分技能未识别');
      }
    } catch (error) {
      console.log('   - 技能读取: ❌', error.message);
    }
  }
}

// 主程序
if (require.main === module) {
  const deployer = new StigmergyDeployer();
  deployer.deploy().catch(console.error);
}

module.exports = StigmergyDeployer;