#!/usr/bin/env node

/**
 * SSCI技能包 - 系统监控脚本
 * 监控CLI工具状态和性能指标
 */

const fs = require('fs-extra');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

class SystemMonitor {
  constructor() {
    this.rootDir = path.resolve(__dirname, '..');
    this.monitoring = false;
    this.stats = {
      startTime: Date.now(),
      cliStatus: {},
      skillUsage: {},
      errorCount: 0,
      warningCount: 0
    };
  }

  async startMonitoring() {
    if (this.monitoring) {
      console.log('⚠️ 监控已在运行中');
      return;
    }

    console.log('🔍 开始系统监控...\n');
    this.monitoring = true;

    // 启动实时监控
    this.startRealTimeMonitoring();
    
    // 设置定时报告
    this.startPeriodicReporting();
  }

  stopMonitoring() {
    this.monitoring = false;
    console.log('\n⏹️ 停止监控');
  }

  startRealTimeMonitoring() {
    const interval = setInterval(() => {
      if (!this.monitoring) {
        clearInterval(interval);
        return;
      }

      this.collectMetrics();
    }, 5000); // 每5秒收集一次指标

    // 清理定时器
    process.on('SIGINT', () => {
      clearInterval(interval);
      this.stopMonitoring();
    });
  }

  startPeriodicReporting() {
    const interval = setInterval(() => {
      if (!this.monitoring) {
        clearInterval(interval);
        return;
      }

      this.generateReport();
    }, 60000); // 每分钟生成一次报告

    // 清理定时器
    process.on('SIGINT', () => {
      clearInterval(interval);
    });
  }

  async collectMetrics() {
    // 收集CLI状态
    await this.collectCLIMetrics();
    
    // 收集技能使用情况
    await this.collectSkillMetrics();
    
    // 收集系统资源
    await this.collectSystemMetrics();
  }

  async collectCLIMetrics() {
    const cliTools = [
      { name: 'claude', command: 'claude', configPath: '~/.claude' },
      { name: 'qwen', command: 'qwen', configPath: '~/.qwen' },
      { name: 'iflow', command: 'iflow', configPath: '~/.iflow' },
      { name: 'gemini', command: 'gemini', configPath: '~/.gemini' },
      { name: 'codebuddy', command: 'codebuddy', configPath: '~/.codebuddy' },
      { name: 'codex', command: 'codex', configPath: '~/.codex' },
      { name: 'qodercli', command: 'qodercli', configPath: '~/.qodercli' }
    ];

    for (const cli of cliTools) {
      try {
        const expandedPath = cli.configPath.replace('~', os.homedir());
        
        // 检查CLI可用性
        const version = execSync(`${cli.command} --version`, { 
          encoding: 'utf8', 
          timeout: 3000 
        });
        
        this.stats.cliStatus[cli.name] = {
          available: true,
          version: version.trim(),
          lastCheck: new Date().toISOString(),
          configPath: expandedPath,
          skillsCount: await this.countSkillsInCLI(expandedPath)
        };
      } catch (error) {
        this.stats.cliStatus[cli.name] = {
          available: false,
          lastCheck: new Date().toISOString(),
          error: error.message
        };
        this.stats.errorCount++;
      }
    }
  }

  async countSkillsInCLI(configPath) {
    try {
      const skillsPath = path.join(configPath, 'skills');
      if (await fs.pathExists(skillsPath)) {
        const items = await fs.readdir(skillsPath);
        return items.filter(item => {
          const itemPath = path.join(skillsPath, item);
          const stat = fs.statSync(itemPath);
          return stat.isDirectory();
        }).length;
      }
    } catch (error) {
      return 0;
    }
  }

  async collectSkillMetrics() {
    try {
      // 从Stigmergy收集技能使用统计
      const stigmergyDir = path.join(os.homedir(), '.stigmergy');
      if (await fs.pathExists(stigmergyDir)) {
        const logPath = path.join(stigmergyDir, 'logs', 'skill-usage.log');
        
        if (await fs.pathExists(logPath)) {
          const logContent = await fs.readFile(logPath, 'utf8');
          const lines = logContent.split('\n').filter(line => line.trim());
          
          // 简单的技能使用统计
          const skillUsage = {};
          lines.forEach(line => {
            if (line.includes('skill-read') || line.includes('skill use')) {
              const match = line.match(/skill-(?:read|use)\s+(\w+)/);
              if (match) {
                const skillName = match[1];
                skillUsage[skillName] = (skillUsage[skillName] || 0) + 1;
              }
            }
          });
          
          this.stats.skillUsage = skillUsage;
        }
      }
    } catch (error) {
      // 忽略Stigmergy错误
    }
  }

  async collectSystemMetrics() {
    try {
      const memoryUsage = process.memoryUsage();
      const cpuUsage = process.cpuUsage();
      
      // 系统负载（简化版）
      const loadAvg = cpuUsage.user + cpuUsage.system;
      
      this.stats.systemMetrics = {
        memory: {
          used: memoryUsage.heapUsed,
          total: memoryUsage.heapTotal,
          percentage: (memoryUsage.heapUsed / memoryUsage.heapTotal * 100).toFixed(2) + '%'
        },
        cpu: {
          usage: loadAvg.toFixed(2) + '%'
        },
        uptime: this.formatUptime(Date.now() - this.stats.startTime)
      };
    } catch (error) {
      this.stats.errorCount++;
    }
  }

  formatUptime(milliseconds) {
    const seconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);
    
    if (days > 0) {
      return `${days}天${hours % 24}小时${minutes % 60}分钟`;
    } else if (hours > 0) {
      return `${hours}小时${minutes % 60}分钟`;
    } else if (minutes > 0) {
      return `${minutes}分钟`;
    } else {
      return `${seconds}秒`;
    }
  }

  generateReport() {
    const timestamp = new Date().toLocaleString('zh-CN');
    
    console.log('\n' + '='.repeat(60));
    console.log('📊 系统监控报告');
    console.log('='.repeat(60));
    console.log(`报告时间: ${timestamp}`);
    console.log(`运行时间: ${this.formatUptime(Date.now() - this.stats.startTime)}`);

    console.log('\n🛠️ CLI工具状态:');
    Object.entries(this.stats.cliStatus).forEach(([name, status]) => {
      const statusIcon = status.available ? '✅' : '❌';
      const version = status.version || 'N/A';
      const skillsCount = status.skillsCount || 0;
      console.log(`  ${statusIcon} ${name}: ${version} (${skillsCount}个技能)`);
    });

    if (Object.keys(this.stats.skillUsage).length > 0) {
      console.log('\n📈 技能使用统计:');
      Object.entries(this.stats.skillUsage).forEach(([skill, count]) => {
        console.log(`  📊 ${skill}: ${count}次调用`);
      });
    }

    console.log('\n💻 系统资源:');
    if (this.stats.systemMetrics) {
      console.log(`  💾 内存使用: ${this.stats.systemMetrics.memory.used} / 1024 / 1024}MB (${this.stats.systemMetrics.memory.percentage})`);
      console.log(`  🔄 CPU使用: ${this.stats.systemMetrics.cpu.usage}`);
      console.log(`  ⏱️ 运行时间: ${this.stats.systemMetrics.uptime}`);
    }

    console.log('\n📈 统计信息:');
    console.log(`  ✅ 成功操作: ${this.stats.errorCount === 0 ? '正常' : this.stats.errorCount}`);
    console.log(`  ⚠️ 警告警告: ${this.stats.warningCount}`);
    console.log(`  📊 数据收集周期: 5秒`);
    console.log(`  📋 报告周期: 1分钟`);
  }

  async exportMetrics() {
    const timestamp = new Date().toISOString();
    const report = {
      timestamp,
      uptime: Date.now() - this.stats.startTime,
      cliStatus: this.stats.cliStatus,
      skillUsage: this.stats.skillUsage,
      systemMetrics: this.stats.systemMetrics,
      errorCount: this.stats.errorCount,
      warningCount: this.stats.warningCount
    };

    const reportPath = path.join(this.rootDir, 'monitoring', `metrics-${timestamp.replace(/[:.]/g, '-')}.json`);
    
    await fs.ensureDir(path.dirname(reportPath));
    await fs.writeJson(reportPath, report, { spaces: 2 });
    
    console.log(`📊 监控数据已导出: ${reportPath}`);
  }
}

// 主程序
if (require.main === module) {
  const monitor = new SystemMonitor();
  
  // 处理命令行参数
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    // 无参数时启动实时监控
    monitor.startMonitoring();
    
    // 处理退出信号
    process.on('SIGINT', () => {
      monitor.stopMonitoring();
    });
    
    // 在Windows中处理Ctrl+C
    if (process.platform === 'win32') {
      process.on('SIGINT', () => {
        process.exit(0);
      });
    }
  } else if (args[0] === 'start') {
    monitor.startMonitoring();
  } else if (args[0] === 'stop') {
    monitor.stopMonitoring();
  } else if (args[0] === 'report') {
    monitor.generateReport();
  } else if (args[0] === 'export') {
    await monitor.exportMetrics();
    } else {
      console.log('使用方法:');
      console.log('  npm run monitor start  - 启动实时监控');
      console.log('  npm run monitor stop   - 停止监控');
      console.log('  npm run monitor report - 生成监控报告');
      console.log('  npm run monitor export - 导出监控数据');
    }
}

module.exports = SystemMonitor;