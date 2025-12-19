#!/usr/bin/env node

/**
 * SSCI技能包 - 健康检查脚本
 * 检查系统环境和配置完整性
 */

const fs = require('fs-extra');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

class HealthChecker {
  constructor() {
    this.rootDir = path.resolve(__dirname, '..');
    this.issues = [];
    this.warnings = [];
  }

  async runHealthCheck() {
    console.log('🏥 SSCI技能包健康检查\n');
    console.log('='.repeat(50));

    // 重置问题列表
    this.issues = [];
    this.warnings = [];

    // 执行各项检查
    await this.checkNodeEnvironment();
    await this.checkPackageDependencies();
    await this.checkCLIInstallations();
    await this.checkDirectoryPermissions();
    await this.checkDiskSpace();
    await this.checkNetworkConnectivity();
    await this.checkStigmergyHealth();
    await this.checkSkillsIntegrity();

    // 生成健康报告
    this.generateHealthReport();
  }

  async checkNodeEnvironment() {
    console.log('🟢 Node.js环境检查');

    try {
      const nodeVersion = process.version;
      console.log(`✅ Node.js版本: ${nodeVersion}`);

      // 检查Node.js版本兼容性
      const majorVersion = parseInt(nodeVersion.slice(1).split('.')[0]);
      if (majorVersion < 16) {
        this.issues.push('Node.js版本过低，建议升级到v16或更高');
      }

      // 检查npm版本
      try {
        const npmVersion = execSync('npm --version', { encoding: 'utf8', timeout: 5000 });
        console.log(`✅ npm版本: ${npmVersion.trim()}`);
      } catch (error) {
        this.issues.push('npm不可用或未安装');
      }
    } catch (error) {
      this.issues.push('无法检查Node.js环境');
    }
  }

  async checkPackageDependencies() {
    console.log('\n📦 依赖包检查');

    try {
      const packagePath = path.join(this.rootDir, 'package.json');
      const packageJson = await fs.readJson(packagePath);
      
      const dependencies = Object.keys(packageJson.dependencies || {});
      const devDependencies = Object.keys(packageJson.devDependencies || {});

      console.log(`✅ 生产依赖: ${dependencies.length}个`);
      console.log(`✅ 开发依赖: ${devDependencies.length}个`);

      // 检查关键依赖
      const criticalDeps = ['fs-extra', 'path', 'yaml', 'chalk', 'ora', 'inquirer'];
      const missingDeps = criticalDeps.filter(dep => !dependencies[dep] && !devDependencies[dep]);
      
      if (missingDeps.length > 0) {
        this.issues.push(`缺少关键依赖: ${missingDeps.join(', ')}`);
      }

      // 检查package-lock.json
      const lockPath = path.join(this.rootDir, 'package-lock.json');
      if (!await fs.pathExists(lockPath)) {
        this.warnings.push('package-lock.json不存在，建议运行 npm install');
      }
    } catch (error) {
      this.issues.push('无法读取package.json');
    }
  }

  async checkCLIInstallations() {
    console.log('\n🛠️ CLI工具安装检查');

    const cliTools = [
      { name: 'Claude Code', command: 'claude', required: true },
      { name: 'Qwen CLI', command: 'qwen', required: true },
      { name: 'iFlow CLI', command: 'iflow', required: true },
      { name: 'Gemini CLI', command: 'gemini', required: false },
      { name: 'CodeBuddy CLI', command: 'codebuddy', required: false },
      { name: 'Codex CLI', command: 'codex', required: false },
      { name: 'QoderCLI', command: 'qodercli', required: false },
      { name: 'Stigmergy CLI', command: 'stigmergy', required: false }
    ];

    for (const cli of cliTools) {
      await this.checkSingleCLI(cli);
    }
  }

  async checkSingleCLI(cli) {
    const { name, command, required } = cli;

    try {
      const version = execSync(`${command} --version`, { 
        encoding: 'utf8', 
        timeout: 5000 
      });
      console.log(`✅ ${name}: ${version.trim()}`);
    } catch (error) {
      if (required) {
        this.issues.push(`必需CLI未安装: ${name}`);
      } else {
        this.warnings.push(`可选CLI未安装: ${name}`);
      }
    }
  }

  async checkDirectoryPermissions() {
    console.log('\n📁 目录权限检查');

    const directories = [
      { path: this.rootDir, description: '项目根目录' },
      { path: path.join(this.rootDir, 'skills'), description: '技能目录' },
      { path: path.join(this.rootDir, 'agents'), description: '智能体目录' },
      { path: path.join(os.homedir(), '.claude'), description: 'Claude配置目录' },
      { path: path.join(os.homedir(), '.qwen'), description: 'Qwen配置目录' },
      { path: path.join(os.homedir(), '.stigmergy'), description: 'Stigmergy目录' }
    ];

    for (const dir of directories) {
      try {
        await fs.access(dir.path, fs.constants.R_OK | fs.constants.W_OK);
        console.log(`✅ ${dir.description}: 可读写`);
      } catch (error) {
        this.issues.push(`权限问题: ${dir.description}`);
      }
    }
  }

  async checkDiskSpace() {
    console.log('\n💾 磁盘空间检查');

    try {
      const stats = await fs.stat(this.rootDir);
      
      // 检查可用空间（简化版）
      const freeCommand = os.platform() === 'win32' ? 'wmic logical get size=free' : 'df -h';
      
      try {
        const freeSpace = execSync(freeCommand, { encoding: 'utf8', timeout: 3000 });
        console.log(`✅ 可用空间: ${freeSpace.trim()}`);
      } catch (error) {
        this.warnings.push('无法检查磁盘空间');
      }
    } catch (error) {
      this.warnings.push('无法检查磁盘空间');
    }
  }

  async checkNetworkConnectivity() {
    console.log('\n🌐 网络连接检查');

    // 检查基本网络连接
    try {
      const result = execSync('ping -n 1 8.8.8.8', { 
        encoding: 'utf8', 
        timeout: 5000 
      });
      
      if (result.includes('bytes=')) {
        console.log('✅ 网络连接: 正常');
      } else {
        this.warnings.push('网络连接可能有问题');
      }
    } catch (error) {
      this.warnings.push('无法检查网络连接');
    }

    // 检查npm registry连接
    try {
      execSync('npm ping', { 
        encoding: 'utf8', 
        timeout: 5000 
      });
      console.log('✅ npm registry: 可访问');
    } catch (error) {
      this.issues.push('npm registry不可访问');
    }
  }

  async checkStigmergyHealth() {
    console.log('\n🔄 Stigmergy健康检查');

    try {
      const version = execSync('stigmergy --version', { 
        encoding: 'utf8', 
        timeout: 5000 
      });
      console.log(`✅ Stigmergy: ${version.trim()}`);

      // 检查Stigmergy状态
      const status = execSync('stigmergy status', { 
        encoding: 'utf8', 
        timeout: 10000 
      });
      
      if (status.includes('✅')) {
        console.log('✅ Stigmergy状态: 健康');
      } else {
        this.warnings.push('Stigmergy状态需要注意');
      }
    } catch (error) {
      this.warnings.push('Stigmergy未安装或不可用');
    }
  }

  async checkSkillsIntegrity() {
    console.log('\n🔍 技能完整性检查');

    const skillsDir = path.join(this.rootDir, 'skills');
    if (!await fs.pathExists(skillsDir)) {
      this.issues.push('技能目录不存在');
      return;
    }

    // 检查技能目录结构
    const categories = ['coding', 'analysis', 'methodology', 'writing', 'conflict-resolution', 'mathematical-statistics', 'network-computation', 'field-analysis', 'ant', 'validity-reliability'];
    
    for (const category of categories) {
      const categoryPath = path.join(skillsDir, category);
      if (await fs.pathExists(categoryPath)) {
        const items = await fs.readdir(categoryPath);
        const skillFiles = items.filter(item => item === 'SKILL.md');
        
        for (const skillFile of skillFiles) {
          const skillPath = path.join(categoryPath, skillFile);
          try {
            const content = await fs.readFile(skillPath, 'utf8');
            
            // 检查YAML frontmatter
            if (content.startsWith('---')) {
              const frontmatterEnd = content.indexOf('---\n', 3);
              if (frontmatterEnd > 0) {
                const frontmatter = content.slice(0, frontmatterEnd);
                if (frontmatter.includes('name:') && frontmatter.includes('description:')) {
                  console.log(`✅ ${category}/${skillFile}: 格式正确`);
                } else {
                  this.warnings.push(`${category}/${skillFile}: 缺少必需字段`);
                }
              } else {
                  this.warnings.push(`${category}/${skillFile}: YAML frontmatter格式错误`);
              }
            } else {
              this.warnings.push(`${category}/${skillFile}: 缺少YAML frontmatter`);
            }
          } catch (error) {
            this.issues.push(`${category}/${skillFile}: 读取失败`);
          }
        }
      }
    }
  }

  generateHealthReport() {
    console.log('\n' + '='.repeat(60));
    console.log('🏥 健康检查报告');
    console.log('='.repeat(60));

    const timestamp = new Date().toLocaleString('zh-CN');
    console.log(`检查时间: ${timestamp}`);

    if (this.issues.length === 0 && this.warnings.length === 0) {
      console.log('\n🎉 系统状态: 优秀');
      console.log('所有检查项目都通过，系统运行正常！');
    } else {
      if (this.issues.length > 0) {
        console.log('\n❌ 发现问题:');
        this.issues.forEach((issue, index) => {
          console.log(`  ${index + 1}. ${issue}`);
        });
      }

      if (this.warnings.length > 0) {
        console.log('\n⚠️ 注意事项:');
        this.warnings.forEach((warning, index) => {
          console.log(`  ${index + 1}. ${warning}`);
        });
      }

      console.log('\n🔧 建议操作:');
      if (this.issues.length > 0) {
        console.log('1. 修复上述问题后重新运行健康检查');
      }
      if (this.warnings.length > 0) {
        console.log('2. 考虑优化配置以提高性能');
      }
    }

    console.log('\n📋 更多帮助:');
    console.log('  npm run status     - 检查部署状态');
    console.log('  npm run deploy:all  - 重新部署所有CLI');
    console.log('  npm run clean     - 清理缓存文件');
    console.log('  npm run monitor   - 监控系统状态');
  }
}

// 主程序
if (require.main === module) {
  const checker = new HealthChecker();
  checker.runHealthCheck().catch(console.error);
}

module.exports = HealthChecker;